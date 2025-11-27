@echo off
setlocal enabledelayedexpansion

REM Set PATH to include all required tools
set "PATH=C:\Program Files\nodejs;%APPDATA%\npm;C:\Program Files\Python311;C:\Program Files\Python311\Scripts;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0;%PATH%"

REM Set Python environment variables
set "PYTHONUNBUFFERED=1"
set "PYTHONIOENCODING=utf-8"

echo =========================================
echo STEP 1: Check UV Installation
echo =========================================
where uv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] UV not found, installing...
    powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
    echo UV installed successfully
) else (
    echo UV already installed
)

call uv --version
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] UV installation failed
    exit /b 1
)

echo.
echo =========================================
echo STEP 2: Sync Dependencies
echo =========================================
echo Installing dependencies with UV...
echo =========================================
call uv sync --no-dev
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)

echo.
echo =========================================
echo STEP 3: Install Playwright Browsers
echo =========================================
echo Installing Playwright browsers...
echo =========================================
call uv run playwright install chromium
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Playwright chromium
    exit /b 1
)

call uv run playwright install-deps chromium
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Failed to install Playwright deps (may not be critical)
)

echo.
echo =========================================
echo STEP 4: Check Node.js Installation
echo =========================================
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Node.js not found, installing...
    
    REM Try Chocolatey first
    where choco >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo Installing Node.js via Chocolatey...
        call choco install nodejs -y
        set "PATH=%ProgramFiles%\nodejs;%APPDATA%\npm;%PATH%"
    ) else (
        REM Try Scoop
        where scoop >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            echo Installing Node.js via Scoop...
            call scoop install nodejs
            call scoop install nodejs-lts
        ) else (
            REM Try winget (Windows 10+)
            where winget >nul 2>&1
            if %ERRORLEVEL% EQU 0 (
                echo Installing Node.js via winget...
                call winget install OpenJS.NodeJS.LTS --silent --accept-package-agreements --accept-source-agreements
                set "PATH=%ProgramFiles%\nodejs;%APPDATA%\npm;%PATH%"
            ) else (
                echo [WARNING] No package manager found (choco, scoop, winget)
                echo Please install Node.js manually or ask admin to install
                echo Continuing without Node.js...
            )
        )
    )
    
    REM Verify Node.js installation
    where node >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [SUCCESS] Node.js installed successfully
        call node --version
        call npm --version
    )
) else (
    echo Node.js already installed
    call node --version
    call npm --version
)

echo.
echo =========================================
echo STEP 5: Check Allure Installation
echo =========================================

REM Add Node.js to PATH first
set "PATH=%ProgramFiles%\nodejs;%APPDATA%\npm;%PATH%"

where allure >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Allure not found, installing via NPM...
    
    REM Try to install using npm directly
    if exist "%ProgramFiles%\nodejs\npm.cmd" (
        echo Found NPM at: %ProgramFiles%\nodejs\npm.cmd
        echo Installing Allure Commandline...
        
        call "%ProgramFiles%\nodejs\npm.cmd" install -g allure-commandline
        
        echo Verifying Allure installation...
        
        REM Try to find allure in PATH
        where allure >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            echo [SUCCESS] Allure command found in PATH
            call allure --version
        ) else (
            REM Try direct path
            if exist "%APPDATA%\npm\allure.cmd" (
                echo [SUCCESS] Allure installed at: %APPDATA%\npm\allure.cmd
                call "%APPDATA%\npm\allure.cmd" --version
                
                REM Add to PATH for this session
                set "PATH=%APPDATA%\npm;%PATH%"
            ) else (
                echo [WARNING] Allure not found after installation
                echo Checking installation directory...
                if exist "%APPDATA%\npm" (
                    echo NPM global directory exists
                    dir "%APPDATA%\npm\allure*" 2>nul
                )
            )
        )
    ) else (
        REM Try npm from PATH
        where npm >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            echo Found NPM in PATH
            echo Installing Allure Commandline...
            call npm install -g allure-commandline
            
            echo Verifying Allure installation...
            where allure >nul 2>&1
            if %ERRORLEVEL% EQU 0 (
                echo [SUCCESS] Allure found in PATH
                call allure --version
            )
        ) else (
            echo [ERROR] NPM not found
            echo Please install Node.js
        )
    )
) else (
    echo Allure already installed
    call allure --version
)

echo.
echo =========================================
echo STEP 6: Run Automation Tests
echo =========================================
echo Environment: PROD
echo Site: LAP
echo Browser: Chromium
echo Headless: True
echo =========================================

call uv run pytest TestSuites/ ^
  --env=prod ^
  --site=lap ^
  --headless=true ^
  --tb=short

set TEST_EXIT_CODE=%ERRORLEVEL%

echo.
echo =========================================
echo Test Execution Completed
echo =========================================
echo Exit Code: %TEST_EXIT_CODE%
echo =========================================

if %TEST_EXIT_CODE% EQU 0 (
    echo [SUCCESS] All tests passed
) else (
    echo [FAILED] Some tests failed
)

echo.
echo =========================================
echo Preparing Allure Results
echo =========================================
if exist "test-results\allure-results\*.json" (
    echo Allure results found - ready for report generation
) else (
    echo [WARNING] No Allure results found
)

echo.
echo =========================================
echo Build Step Finished
echo =========================================

exit /b %TEST_EXIT_CODE%

