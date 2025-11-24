# 03 - How to Run Automation Tests

## 🚀 Basic Test Execution

### Run 1 Test Case

```bash
# Format
pytest TestSuites/[test_file].py::[TestClass]::[test_method] -v

# Example
pytest TestSuites/test_lap.py::TestLAP::test_LAP_TC_1_verify_krw_currency -v
```

**Output**:

```
test_LAP_TC_1_verify_krw_currency PASSED [100%]

✓ Test completed in 15.3s
✓ Screenshots saved: 4 files
✓ All assertions passed
```

### Run All Tests in 1 File

```bash
pytest TestSuites/test_lap.py -v
```

**Output**:

```
test_LAP_TC_1_verify_krw_currency PASSED [25%]
test_LAP_TC_2_verify_usd_currency PASSED [50%]
test_LAP_TC_3_verify_eur_currency PASSED [75%]
test_LAP_TC_4_verify_jpy_currency PASSED [100%]

✓ 4 passed in 58.2s
```

### Run All Tests in Folder

```bash
pytest TestSuites/ -v
```

## 📊 Run Tests With Options

### Show Details

```bash
# -v: Verbose (show test names)
pytest TestSuites/test_lap.py -v

# -s: Show print statements
pytest TestSuites/test_lap.py -v -s

# -vv: Extra verbose (show assertions)
pytest TestSuites/test_lap.py -vv
```

### Run With Markers

```bash
# Run tests with tc_id marker
pytest -m "tc_id" -v

# Run specific TC_ID
pytest -m "tc_id('LAP_TC_1')" -v

# Run multiple TC_IDs
pytest -m "tc_id('LAP_TC_1') or tc_id('LAP_TC_2')" -v
```

### Run in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run with 4 workers
pytest TestSuites/ -v -n 4

# Run with auto workers (number of CPU cores)
pytest TestSuites/ -v -n auto
```

**Benefits**:

```
Sequential: 4 tests × 15s = 60s
Parallel (4 workers): 15s

→ 4x faster!
```

### Rerun Failed Tests

```bash
# First run
pytest TestSuites/test_lap.py -v

# Rerun only failed tests
pytest TestSuites/test_lap.py -v --lf

# Run failed tests first, then passed tests
pytest TestSuites/test_lap.py -v --ff
```

### Stop On Failure

```bash
# Stop immediately on first failure
pytest TestSuites/test_lap.py -v -x

# Stop after 3 failures
pytest TestSuites/test_lap.py -v --maxfail=3
```

## 📸 Screenshots & Reports

### Automatic Screenshots

Framework automatically takes screenshots:

```
test-results/
├── screenshots/
│   ├── LAP_TC_1__step_1__click_account.png
│   ├── LAP_TC_1__step_2__select_currency.png
│   ├── LAP_TC_1__step_3__click_save.png
│   └── LAP_TC_1__step_4__verify_success.png
```

**Naming convention**:

```
{TC_ID}__{step_index}__{action}.png
```

### HTML Report

```bash
# Install pytest-html
pip install pytest-html

# Run with HTML report
pytest TestSuites/test_lap.py -v --html=report.html --self-contained-html
```

**Output**: `report.html` with:

- Test results summary
- Pass/Fail count
- Duration
- Screenshots embedded
- Error messages

### Allure Report

```bash
# Install allure-pytest
pip install allure-pytest

# Run tests with allure
pytest TestSuites/test_lap.py -v --alluredir=allure-results

# Generate report
allure serve allure-results
```

**Benefits**:

- Beautiful UI
- Test history
- Screenshots
- Logs
- Trends

## 🔧 Run With Different Environments

### Config File

Create `pytest.ini` file:

```ini
[pytest]
markers =
    tc_id: Test case ID marker
    smoke: Smoke tests
    regression: Regression tests

addopts = -v --html=report.html --self-contained-html
```

### Environment Variables

```bash
# Set environment
export ENV=staging
export BASE_URL=https://staging.lap.nexdev.net

# Run tests
pytest TestSuites/test_lap.py -v
```

### Command Line Override

```bash
# Override URL
pytest TestSuites/test_lap.py -v --base-url=https://staging.lap.nexdev.net

# Override browser
pytest TestSuites/test_lap.py -v --browser=firefox

# Override headless
pytest TestSuites/test_lap.py -v --headed
```

## 🎯 Run Tests By Scenarios

### Scenario 1: Smoke Testing

```bash
# Run only SMOKE tests
pytest -m smoke -v

# Or run High priority tests
pytest TestSuites/ -v -k "high"
```

**Use case**: Quick test after each build

### Scenario 2: Regression Testing

```bash
# Run all tests
pytest TestSuites/ -v -n auto --html=regression_report.html
```

**Use case**: Full test before release

### Scenario 3: Debugging

```bash
# Run 1 test with debug info
pytest TestSuites/test_lap.py::TestLAP::test_LAP_TC_1 -vv -s --headed
```

**Use case**: Debug test failure

### Scenario 4: CI/CD

```bash
# Run with strict mode
pytest TestSuites/ -v --strict-markers --tb=short -n auto
```

**Use case**: Run in CI/CD pipeline

## 📋 View Results

### Console Output

```
test_LAP_TC_1_verify_krw_currency PASSED [100%]

Duration: 15.3s
Screenshots: 4 files
Assertions: 3 passed
```

### Test Results Folder

```
test-results/
├── screenshots/
│   ├── LAP_TC_1__*.png
│   ├── LAP_TC_2__*.png
│   └── ...
├── videos/ (if enabled)
│   ├── LAP_TC_1.webm
│   └── ...
├── traces/ (if enabled)
│   ├── LAP_TC_1.zip
│   └── ...
└── report.html
```

### HTML Report

Open `report.html` in browser:

```
Test Results Summary
====================
Total: 4 tests
Passed: 3 (75%)
Failed: 1 (25%)
Duration: 58.2s

Details:
--------
✓ LAP_TC_1: PASSED (15.3s)
✓ LAP_TC_2: PASSED (14.8s)
✓ LAP_TC_3: PASSED (16.1s)
✗ LAP_TC_4: FAILED (12.0s)
  Error: TimeoutError waiting for selector
  Screenshot: [embedded]
```

## 🐛 Troubleshooting

### Test Won't Run

**Symptoms**:

```
ERROR: file not found: TestSuites/test_lap.py
```

**Solution**:

```bash
# Check if file exists
ls TestSuites/test_lap.py

# Check current directory
pwd

# Run from framework root folder
cd framework_automation_playwright
pytest TestSuites/test_lap.py -v
```

### Import Error

**Symptoms**:

```
ImportError: No module named 'src.Action'
```

**Solution**:

```bash
# Check PYTHONPATH
echo $PYTHONPATH

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or add to pytest.ini
[pytest]
pythonpath = .
```

### Browser Won't Open

**Symptoms**:

```
Error: Executable doesn't exist at /path/to/chromium
```

**Solution**:

```bash
# Reinstall Playwright browsers
playwright install chromium

# Or install all browsers
playwright install
```

### Test Timeout

**Symptoms**:

```
TimeoutError: Timeout 30000ms exceeded
```

**Solution**:

```bash
# Increase timeout in pytest.ini
[pytest]
timeout = 60

# Or run with higher timeout
pytest TestSuites/test_lap.py -v --timeout=120
```

## 💡 Tips for Efficient Testing

### 1. Run Smoke Tests First

```bash
# Run smoke tests first (5-10 tests)
pytest -m smoke -v

# If PASSED → Run full regression
pytest TestSuites/ -v -n auto
```

### 2. Use Parallel Execution

```bash
# Run in parallel for faster execution
pytest TestSuites/ -v -n auto
```

**Note**: Don't use parallel if tests have dependencies.

### 3. Run Failed Tests First

```bash
# Rerun failed tests to verify fix
pytest TestSuites/ -v --ff
```

### 4. Generate Report for Stakeholders

```bash
# Generate beautiful HTML report
pytest TestSuites/ -v --html=report.html --self-contained-html

# Send report via email/Slack
```

### 5. CI/CD Integration

Create `.gitlab-ci.yml` or `Jenkinsfile`:

```yaml
test:
  script:
    - pip install -r requirements.txt
    - playwright install chromium
    - pytest TestSuites/ -v -n auto --html=report.html
  artifacts:
    paths:
      - report.html
      - test-results/
```

---

**Next**: [04 - AI Auto-Fix Errors](./04-ai-auto-fix.md)
