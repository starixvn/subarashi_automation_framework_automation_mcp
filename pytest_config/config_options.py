import logging
import os
import shutil
import subprocess
import sys

import pytest
from config.config import Config

logger = logging.getLogger(__name__)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--env", default=None, help="Environment: local, uat, prod")
    parser.addoption("--site", default=None, help="Site: lrf, lap")
    parser.addoption("--headless", default=None, help="Headless mode: true, false")
    parser.addoption(
        "--allure",
        action="store_true",
        default=None,
        help="Enable Allure reporting (overrides config)",
    )
    parser.addoption(
        "--no-allure",
        action="store_true",
        default=False,
        help="Disable Allure reporting (overrides config)",
    )
    parser.addoption(
        "--allure-serve",
        action="store_true",
        default=False,
        help="Auto-open Allure report after test execution (local only)",
    )
    parser.addoption(
        "--allure-report-url",
        default=None,
        help="Allure report URL for Jenkins/CI notifications",
    )


def pytest_configure(config: pytest.Config) -> None:
    env_option = config.getoption("--env")
    if env_option is not None:
        Config.ENVIRONMENT = env_option

    site_option = config.getoption("--site")
    if site_option is not None:
        Config.SITE = site_option

    headless_option = config.getoption("--headless")
    if headless_option is not None:
        Config.HEADLESS = headless_option.lower() == "true"

    if config.getoption("--no-allure"):
        Config.ALLURE_ENABLED = False
        logger.info("Allure reporting DISABLED via --no-allure flag")
    elif config.getoption("--allure"):
        Config.ALLURE_ENABLED = True
        logger.info("Allure reporting ENABLED via --allure flag")

    allure_report_url = config.getoption("--allure-report-url")
    if allure_report_url:
        Config.ALLURE_REPORT_URL = allure_report_url


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if not Config.ALLURE_ENABLED:
        return

    is_ci = bool(os.getenv("BUILD_URL") or os.getenv("CI") or os.getenv("JENKINS_URL"))

    if is_ci:
        return

    if session.testscollected == 0:
        return

    if session.testsfailed + session.testscollected == 0:
        return

    if not Config.ALLURE_RESULTS_DIR.exists() or not list(
        Config.ALLURE_RESULTS_DIR.glob("*.json")
    ):
        logger.warning("No Allure results found")
        return

    try:
        allure_cmd = shutil.which("allure")

        if not allure_cmd:
            raise FileNotFoundError("Allure command not found in PATH")

        if sys.platform == "win32":
            batch_content = f'''@echo off
echo ================================================================
echo Allure Report Server Started
echo ================================================================
echo.
echo Browser will open automatically when ready
echo.
echo To stop the server:
echo   1. Close this window, OR
echo   2. Press Ctrl+C
echo.
echo ================================================================
echo.
"{allure_cmd}" serve "{Config.ALLURE_RESULTS_DIR}"
'''
            Config.ALLURE_BATCH_FILE.write_text(batch_content, encoding="utf-8")

            subprocess.Popen(
                f'start "Allure Report Server - Close to stop" cmd /c "{Config.ALLURE_BATCH_FILE}"',
                shell=True,
            )
        else:
            subprocess.Popen(
                [allure_cmd, "serve", str(Config.ALLURE_RESULTS_DIR)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    except FileNotFoundError:
        logger.error(
            "Allure CLI not found - Install: npm install -g allure-commandline"
        )
    except Exception as e:
        logger.error(f"Failed to open Allure report: {e}")
