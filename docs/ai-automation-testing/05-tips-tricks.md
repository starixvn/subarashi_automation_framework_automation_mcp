# 05 - Tips & Tricks

## 💡 Tips for Writing Test Cases for AI to Generate Good Code

### 1. Specific, Actionable Steps

**✅ Good**:

```
Steps:
1. Click on "Account" icon (top right corner, blue icon with user avatar)
2. Wait for "My Account" popup to appear
3. Click on "Default Base Currency" dropdown (label: "Currency")
4. Select "KRW" option from dropdown (value="KRW", text="Korean Won")
5. Click "Save" button (blue button, bottom right of popup)
6. Wait for success message to appear
```

**❌ Not good**:

```
Steps:
1. Go to account
2. Change currency
3. Save
```

**Why**: AI needs to know EXACTLY which element, where, what attributes to capture accurately.

### 2. Measurable Expected Results

**✅ Good**:

```
Expected_Result:
1. Verify "KRW" option exists in dropdown (option[@value='KRW'])
2. Verify success message "Update successfully" is displayed (green banner, top of page, visible for 3 seconds)
3. Verify "My Account" popup is closed (element with id="my-account-popup" has display:none)
4. Verify selected currency in dropdown is "KRW" (dropdown value attribute = "KRW")
```

**❌ Not good**:

```
Expected_Result:
1. Currency updated
2. Message shown
3. Popup closed
```

**Why**: AI needs to know EXACTLY what to verify, where, which attribute, what format.

### 3. Complete Preconditions

**✅ Good**:

```
Preconditions:
1. User is logged into portal as vntest/1234aa
2. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en
3. User is on Dashboard page (URL contains "/dashboard")
4. User has permission to change currency (role: admin or user)
5. At least 3 currencies are available in system (KRW, USD, EUR)
```

**❌ Not good**:

```
Preconditions:
1. User logged in
2. On dashboard
```

**Why**: AI needs to know complete context to setup test correctly.

### 4. Handle Special Cases

**✅ Good**:

```
Steps:
1. Click "Load More" button
2. Wait for loading spinner to disappear (max 10 seconds)
3. Wait for new products to appear (at least 10 products loaded)
4. Scroll to bottom of page
5. Click on product #15 (after loading more)

Note: Element is inside iframe with name="ProductFrame"
```

**❌ Not good**:

```
Steps:
1. Load more products
2. Click product
```

**Why**: AI needs to know about dynamic content, loading states, iframes.

## 🚀 Tips for Efficient Test Execution

### 1. Run Smoke Tests First

```bash
# Strategy
1. Run 5-10 critical tests (smoke)
2. If PASSED → Run full regression
3. If FAILED → Stop, fix issues first

# Command
pytest -m smoke -v
```

**Benefits**: Detect critical issues early, save time.

### 2. Parallel Execution

```bash
# Run with 4 workers
pytest TestSuites/ -v -n 4

# Or auto (number of CPU cores)
pytest TestSuites/ -v -n auto
```

**Benefits**:

```
Sequential: 100 tests × 15s = 1,500s (25 minutes)
Parallel (4 workers): 1,500s / 4 = 375s (6.25 minutes)

→ 4x faster!
```

**Note**: Only use parallel if tests are independent (no dependencies).

### 3. Run Failed Tests First

```bash
# Rerun failed tests to verify fix
pytest TestSuites/ -v --ff

# Or only run failed tests
pytest TestSuites/ -v --lf
```

**Benefits**: Verify fix quickly, no need to rerun all.

### 4. Stop On First Failure

```bash
# Stop immediately on first failure
pytest TestSuites/ -v -x
```

**Use case**: Debugging, don't want to wait for all tests to finish.

### 5. Generate Reports

```bash
# HTML report
pytest TestSuites/ -v --html=report.html --self-contained-html

# Allure report
pytest TestSuites/ -v --alluredir=allure-results
allure serve allure-results
```

**Benefits**: Share with stakeholders, track test history.

## 🐛 Troubleshooting

### Issue 1: Test Fails With "Element Not Found"

**Symptoms**:

```
TimeoutError: Timeout 10000ms exceeded waiting for selector
```

**Causes**:

1. Wrong selector
2. Element not loaded yet
3. Element in iframe
4. Element dynamic (ID changes)

**Solution**:

```
1. Request AI to fix:
   "Test failed with TimeoutError. Please fix following #file:ai-auto-run-and-fix.mdc"

2. AI will:
   - Re-capture element
   - Update selector
   - Add waits
   - Handle iframe if needed
```

### Issue 2: Test Passes Locally But Fails On CI/CD

**Symptoms**:

```
Local: PASSED
CI/CD: FAILED (TimeoutError)
```

**Causes**:

1. CI/CD server slower
2. Network latency
3. Different environment

**Solution**:

```python
# Increase timeouts for CI/CD
# In pytest.ini or conftest.py

if os.getenv("CI"):
    DEFAULT_TIMEOUT = 30  # CI/CD
else:
    DEFAULT_TIMEOUT = 10  # Local
```

### Issue 3: Test Flaky (Sometimes Pass, Sometimes Fail)

**Symptoms**:

```
Run 1: PASSED
Run 2: FAILED
Run 3: PASSED
```

**Causes**:

1. Timing issue (race condition)
2. Dynamic content
3. Unstable network

**Solution**:

```
1. Request AI to fix:
   "Test is flaky. Please add intelligent waits following #file:ai-auto-run-and-fix.mdc"

2. AI will add:
   - Wait for network idle
   - Wait for element stable
   - Wait for loading spinner disappear
   - Retry logic
```

### Issue 4: Tests Running Too Slow

**Symptoms**:

```
100 tests: 45 minutes (too long!)
```

**Solution**:

```bash
# 1. Parallel execution
pytest TestSuites/ -v -n auto

# 2. Optimize waits (reduce unnecessary timeouts)
# 3. Skip heavy tests in development
pytest TestSuites/ -v -m "not slow"

# 4. Use headless mode
pytest TestSuites/ -v --headless
```

### Issue 5: Screenshots Not Clear

**Symptoms**:

- Screenshots cropped
- Cannot see element to verify

**Solution**:

```python
# Add to Action method
def verify_element(self):
    # Scroll to element
    self.page.scroll_to_element(ELEMENT)

    # Take full page screenshot
    self.page.screenshot_full_page("verify_element.png")

    # Then verify
    assert self.page.element_visible(ELEMENT)
```

## 📊 Best Practices

### 1. Test Organization

```
TestSuites/
├── test_smoke.py          # Critical tests (5-10 tests)
├── test_regression.py     # Full regression (100+ tests)
├── test_login.py          # Login module
├── test_products.py       # Products module
└── test_checkout.py       # Checkout module
```

**Benefits**: Easy to maintain, easy to run selective tests.

### 2. Naming Convention

```python
# Test file
test_[module].py

# Test class
class Test[Module]:

# Test method
def test_[TC_ID]_[description](self):
```

**Example**:

```python
# test_lap.py
class TestLAP:
    def test_LAP_TC_1_verify_krw_currency(self):
        pass
```

### 3. Use Markers

```python
# pytest.ini
[pytest]
markers =
    smoke: Smoke tests
    regression: Regression tests
    slow: Slow tests (skip in dev)

# Test file
@pytest.mark.smoke
@pytest.mark.tc_id("LAP_TC_1")
def test_LAP_TC_1_verify_krw_currency(self):
    pass
```

**Run**:

```bash
pytest -m smoke -v
pytest -m "smoke and not slow" -v
```

### 4. Data-Driven Testing

```python
# Test with multiple data sets
@pytest.mark.parametrize("currency,expected", [
    ("KRW", "Korean Won"),
    ("USD", "US Dollar"),
    ("EUR", "Euro"),
])
def test_currency_selection(self, currency, expected):
    self.action.select_currency(currency)
    self.action.verify_currency_selected(expected)
```

**Benefits**: 1 test code, test multiple scenarios.

### 5. Fixtures For Setup/Teardown

```python
# conftest.py
@pytest.fixture
def setup_test_data(page):
    # Setup
    create_test_user()
    create_test_products()

    yield

    # Teardown
    delete_test_user()
    delete_test_products()

# Test file
def test_checkout(self, setup_test_data):
    # Test with setup data
    pass
```

## 🎯 Advanced Tips

### 1. Retry Failed Tests

```python
# pytest.ini
[pytest]
addopts = --reruns 3 --reruns-delay 2

# Or specific test
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_flaky_test(self):
    pass
```

### 2. Custom Assertions

```python
# src/Core/utilities/assertions.py
def assert_element_visible_with_retry(page, selector, max_retries=3):
    for i in range(max_retries):
        if page.element_visible(selector):
            return True
        time.sleep(1)
    raise AssertionError(f"Element {selector} not visible after {max_retries} retries")
```

### 3. Screenshot On Failure

```python
# conftest.py
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            page.screenshot(f"failure_{item.name}.png")
```

### 4. Video Recording

```python
# conftest.py
@pytest.fixture(scope="function")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "test-results/videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }
```

### 5. Trace On Failure

```python
# conftest.py
@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True)

    yield context

    # Save trace on failure
    context.tracing.stop(path="trace.zip")
```

## 📞 When You Need Support

### Checklist Before Asking

```
□ Is framework setup correctly?
□ Is MCP Server running?
□ Are test cases written in correct format?
□ Have you tried AI auto-fix?
□ Have you checked screenshots/logs?
□ Have you tested manually?
```

### Information to Provide

```
1. Test case ID
2. Error message (full stack trace)
3. Screenshot when failed
4. Test file path
5. Environment (local/staging/production)
6. Steps to reproduce
7. Expected vs Actual behavior
```

### Escalation Path

```
Level 1: AI Auto-Fix
- Request AI to fix following #file:ai-auto-run-and-fix.mdc
- 85% cases AI can fix

Level 2: QA Review
- If AI cannot fix
- QA reviews test case, checks application manually
- 10% cases need QA review

Level 3: Dev/DevOps
- Application bug → Dev fixes
- Environment issue → DevOps fixes
- 5% cases need Dev/DevOps
```

---

**Back to**: [README](./README.md)
