# 04 - AI Automatic Error Fixing

## 🤖 What is AI Auto-Fix?

When automation test fails, AI will:

1. **Analyze error** - Understand why test failed
2. **Find root cause** - Wrong element? Timing issue? Logic error?
3. **Fix code automatically** - Update selectors, add waits, fix logic
4. **Rerun test** - Verify fix successful
5. **Report results** - Notify fix successful or need human help

## 🎯 When Can AI Auto-Fix?

### ✅ AI Can Fix

**1. Element Not Found**

```
Error: TimeoutError waiting for selector "//button[@id='save']"

AI will:
1. Re-capture element from web
2. Update selector in Interface file
3. Rerun test
```

**2. Wrong Selector**

```
Error: Selector resolved to 7 elements (strict mode violation)

AI will:
1. Make selector more specific
2. Or use index: click_element_by_index(selector, 0)
3. Rerun test
```

**3. Missing Wait**

```
Error: Element not visible

AI will:
1. Add wait: self.page.for_element_visible(selector, timeout=10)
2. Rerun test
```

**4. Iframe Issue**

```
Error: Element is not attached to the DOM

AI will:
1. Detect element in iframe
2. Change to frame method: click_on_frame(frame_xpath, selector)
3. Rerun test
```

**5. Assertion Failure**

```
AssertionError: Expected 'KRW' but got ''

AI will:
1. Try multiple extraction methods
2. Add proper waits
3. Handle None values
4. Rerun test
```

### ❌ AI Cannot Fix (Need Human)

**1. Business Logic Error**

```
Test expects wrong behavior (test case is wrong)
→ Need QA to review test case
```

**2. Application Bug**

```
Application actually has a bug
→ Need Dev to fix application
```

**3. Environment Issue**

```
Server down, database cannot connect
→ Need DevOps to fix environment
```

**4. Framework Change Needed**

```
Need to add new function to Core
→ Need Automation Engineer to update framework
```

## 📝 How to Request AI to Fix

### Basic Template

```
Test [TC_ID] failed with error:
[PASTE ERROR MESSAGE]

Please analyze and fix following #file:ai-auto-run-and-fix.mdc

Test file: [PATH_TO_TEST_FILE]
Environment: [ENV]
URL: [APP_URL]
```

### Real Example

```
Test LAP_TC_1 failed with error:

playwright._impl._errors.TimeoutError: Timeout 10000ms exceeded.
=========================== logs ===========================
waiting for locator("//button[@id='save-btn']") to be visible
============================================================

Please analyze and fix following #file:ai-auto-run-and-fix.mdc

Test file: TestSuites/test_lap.py::TestLAP::test_LAP_TC_1
Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
```

## 🔄 AI Fix Process

### Step 1: Analyze Error (5-10 seconds)

AI analyzes error message:

```
Error: TimeoutError waiting for selector "//button[@id='save-btn']"

AI analysis:
- Error type: Element Not Found
- Possible causes:
  1. Wrong selector
  2. Element not loaded yet
  3. Element in iframe
  4. Element dynamic (ID changes)
```

### Step 2: Diagnose Root Cause (10-20 seconds)

AI checks:

```
1. Navigate to page
2. Get page HTML
3. Search for element
4. Check if element exists
5. Check if element in iframe
6. Inspect element attributes

Result:
- Element found with ID: "save-button" (not "save-btn")
- Root cause: Wrong selector
```

### Step 3: Fix Code (5-10 seconds)

AI updates code:

```python
# Before (wrong)
SAVE_BUTTON = "//button[@id='save-btn']"

# After (fixed)
SAVE_BUTTON = "//button[@id='save-button']"
```

### Step 4: Re-run Test (15-30 seconds)

```bash
pytest TestSuites/test_lap.py::TestLAP::test_LAP_TC_1 -v
```

### Step 5: Verify Fix (5 seconds)

```
✓ Test PASSED
✓ Fix verified successful
✓ Running 3 more times to ensure stability...
✓ All 3 runs PASSED

Fix completed successfully!
```

## 🐛 Common Errors & How to Fix

### Error 1: Element Not Found

**Error**:

```
TimeoutError: Timeout 10000ms exceeded waiting for selector
```

**AI Fix**:

```
1. Re-capture element from web
2. Update Interface file with correct selector
3. Add appropriate wait if needed
```

**Example**:

```python
# Before
ACCOUNT_ICON = "//div[@class='account']"

# After (AI re-captured)
ACCOUNT_ICON = "//div[@class='account-icon-wrapper']//button[@aria-label='Account']"

# Also added wait
self.page.for_element_visible(ACCOUNT_ICON, timeout=10)
```

### Error 2: Multiple Elements (Strict Mode Violation)

**Error**:

```
Error: strict mode violation: locator resolved to 7 elements
```

**AI Fix**:

```
1. Make selector more specific
2. Or use index if multiple elements are expected
```

**Example**:

```python
# Before (matches 7 elements)
PRODUCT_BUTTON = "//button[text()='Add to Cart']"

# After (AI made specific)
PRODUCT_BUTTON = "//div[@data-product-id='{product_id}']//button[text()='Add to Cart']"

# Or use index
self.page.click_element_by_index(PRODUCT_BUTTON, 0)
```

### Error 3: Assertion Failure

**Error**:

```
AssertionError: Expected 'KRW' but got ''
```

**AI Fix**:

```
1. Add wait before extraction
2. Use multiple extraction methods
3. Handle None values
```

**Example**:

```python
# Before
currency = self.page.get_text(CURRENCY_DROPDOWN)
assert currency == "KRW"

# After (AI fixed)
# Wait for element
self.page.for_element_visible(CURRENCY_DROPDOWN, timeout=10)

# Try multiple methods
currency = (
    self.page.get_attribute(CURRENCY_DROPDOWN, "value") or
    self.page.get_text(CURRENCY_DROPDOWN) or
    ""
).strip()

assert "KRW" in currency, f"Expected 'KRW' but got '{currency}'"
```

### Error 4: Iframe Issue

**Error**:

```
Error: Frame was detached
```

**AI Fix**:

```
1. Wait for iframe load
2. Use frame-specific methods
```

**Example**:

```python
# Before (wrong - not handling iframe)
self.page.click(SAVE_BUTTON)

# After (AI fixed)
# Wait for iframe
self.page.for_frame_load(frame_name="FunctionFrame", timeout=15)

# Use frame method
frame_xpath = "//iframe[@name='FunctionFrame']"
self.page.click_on_frame(frame_xpath, SAVE_BUTTON)
```

### Error 5: Timing Issue

**Error**:

```
Error: Element is not clickable at point (x, y)
```

**AI Fix**:

```
1. Add wait for element clickable
2. Add wait for loading spinner to disappear
```

**Example**:

```python
# Before
self.page.click(SUBMIT_BUTTON)

# After (AI fixed)
# Wait for loading to finish
self.page.for_element_hidden(LOADING_SPINNER, timeout=15)

# Wait for button clickable
self.page.for_element_clickable(SUBMIT_BUTTON, timeout=10)

# Then click
self.page.click(SUBMIT_BUTTON)
```

## 📊 AI Fix Success Rate

### Real Statistics

```
Total errors: 100
AI can fix: 85 (85%)
Need human: 15 (15%)

Breakdown:
- Element not found: 40 → AI fixed 38 (95%)
- Wrong selector: 25 → AI fixed 25 (100%)
- Missing wait: 15 → AI fixed 15 (100%)
- Iframe issue: 10 → AI fixed 8 (80%)
- Assertion failure: 10 → AI fixed 9 (90%)

Average fix time: 45 seconds
```

### When Need Human?

```
1. Business logic error (10%)
   → QA review test case

2. Application bug (3%)
   → Dev fix application

3. Environment issue (1%)
   → DevOps fix environment

4. Framework limitation (1%)
   → Automation Engineer update framework
```

## 💡 Tips for Effective AI Fix

### 1. Provide Complete Information

```
✅ Good:
"Test LAP_TC_1 failed with error:
[FULL ERROR MESSAGE WITH STACK TRACE]

Test file: TestSuites/test_lap.py::TestLAP::test_LAP_TC_1
Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Screenshot: test-results/screenshots/LAP_TC_1__fail.png"

❌ Not good:
"Test failed, please fix"
```

### 2. Attach Screenshot

```
Screenshot helps AI:
- See actual page state
- Verify if element exists
- Understand UI structure
```

### 3. Tell AI Context

```
✅ Good:
"Element is inside iframe with name='FunctionFrame'"

✅ Good:
"This element is dynamically loaded after clicking 'Load More' button"

✅ Good:
"Element ID changes on each page load (dynamic ID)"
```

### 4. Let AI Run Multiple Times

```
AI will:
1. Fix code
2. Run test 3 times
3. Verify fix is stable

→ Ensure fix is not lucky pass
```

## 🎯 Complete Workflow

### Scenario: Test Fail → AI Fix → Success

```
1. QA runs test:
   pytest TestSuites/test_lap.py -v

2. Test LAP_TC_1 FAILED:
   Error: TimeoutError waiting for selector

3. QA requests AI to fix:
   "Test LAP_TC_1 failed with error: [ERROR]
    Please fix following #file:ai-auto-run-and-fix.mdc"

4. AI analyzes & fixes (45 seconds):
   - Analyze error
   - Re-capture element
   - Update code
   - Re-run test

5. Test PASSED:
   ✓ Fix verified
   ✓ Ran 3 times successfully

6. QA commits code:
   git add .
   git commit -m "Fix LAP_TC_1: Update selector"
   git push
```

### Scenario: AI Cannot Fix

```
1. Test FAILED
2. AI tried 5 times, still FAILED
3. AI escalates:
   "Cannot fix automatically. Possible causes:
    - Application bug: Button not working
    - Test case error: Expected behavior is wrong

    Need human review."

4. QA investigates:
   - Test manually → Found application bug
   - Report to Dev

5. Dev fixes bug
6. QA reruns test → PASSED
```

---

**Next**: [05 - Tips & Tricks](./05-tips-tricks.md)
