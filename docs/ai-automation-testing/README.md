# AI Automation Testing - Guide for QA

## 🎯 What is AI Automation Testing?

**AI Automation Testing** = AI automatically writes automation test code for you!

**How it works**:

1. You write test cases in Google Sheets (like AI Manual Testing)
2. Tell AI: "Generate automation code for these test cases"
3. AI automatically:
   - Reads test cases
   - Writes automation code (Python + Playwright)
   - Creates Page Objects, Actions, Test Suites
   - Runs tests automatically
   - If test fails → AI automatically fixes and reruns

## ✨ Why Use AI Automation Testing?

### Comparison With Manual Automation

**Traditional Automation**:

```
QA/Automation Engineer must:
1. Read test case
2. Write code to locate elements (XPath, CSS...)
3. Write code to click, type, verify...
4. Debug when code fails
5. Maintain code when UI changes

⏱️ Time: 30-60 minutes/test case
🐛 Error-prone, hard to maintain
📝 Need to know Python/Playwright
```

**AI Automation Testing**:

```
QA only needs to:
1. Write test cases in Google Sheets
2. Tell AI: "Generate automation code"
3. AI automatically writes code
4. Run tests
5. If fails → AI auto-fixes

⚡ Time: 5-10 minutes/test case
🎯 Accurate, auto-fix
📝 NO coding knowledge needed!
```

### Specific Benefits

**1. No Coding Knowledge Required**

- AI writes automation code for you
- You only need to write test cases (like manual testing)

**2. Automatic Error Fixing**

- Test fails? AI automatically analyzes error
- AI automatically fixes code and reruns
- No manual debugging needed

**3. Easy Re-runs**

- Regression testing: Just rerun command
- No need to test manually again

**4. Parallel Execution**

- Run multiple tests simultaneously
- Save time

## 🔄 Complete Workflow

### Step 1: Write Test Cases

Write test cases in Google Sheets (like AI Manual Testing):

| TC_ID    | Title               | Test_Type | Priority | Preconditions  | Steps                                              | Expected_Result                              | Status | Owner |
| -------- | ------------------- | --------- | -------- | -------------- | -------------------------------------------------- | -------------------------------------------- | ------ | ----- |
| LAP_TC_1 | Verify KRW currency | SMOKE     | High     | User logged in | 1. Click Account<br>2. Select KRW<br>3. Click Save | 1. KRW available<br>2. Success message shown |        |       |

### Step 2: Request AI to Generate Code

Tell AI:

```
Please read test cases from Google Sheet:
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID

Generate automation code for test cases: LAP_TC_1, LAP_TC_2

Follow the framework structure in @framework_automation_playwright
Use system prompt: #file:ai-automation-test-generation.mdc
```

AI will automatically:

- ✅ Read test cases
- ✅ Capture elements from web
- ✅ Write automation code (Page Objects, Actions, Tests)
- ✅ Create correct file structure

### Step 3: Run Tests

```bash
# Run 1 test
pytest TestSuites/test_lap.py::TestLAP::test_LAP_TC_1 -v

# Run all tests
pytest TestSuites/test_lap.py -v

# Run with report
pytest TestSuites/test_lap.py -v --html=report.html
```

### Step 4: AI Auto-Fix (If Fails)

If test fails, tell AI:

```
Test LAP_TC_1 failed with error:
[PASTE ERROR MESSAGE]

Please analyze and fix following #file:ai-auto-run-and-fix.mdc
```

AI will:

- ✅ Analyze error
- ✅ Fix code automatically
- ✅ Rerun test
- ✅ Verify fix successful

## 📚 Documentation Structure

1. **[01-introduction.md](./01-introduction.md)** - What is AI Automation, benefits
2. **[02-requesting-ai-generate.md](./02-requesting-ai-generate.md)** - How to request AI to generate code
3. **[03-running-tests.md](./03-running-tests.md)** - How to run automation tests
4. **[04-ai-auto-fix.md](./04-ai-auto-fix.md)** - AI automatic error fixing
5. **[05-tips-tricks.md](./05-tips-tricks.md)** - Tips and troubleshooting

## 🚀 Quick Start

### Step 1: Preparation

```bash
# Clone framework
git clone [REPO_URL]

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Write Test Case

Create Google Sheet with test case:

```
TC_ID: LAP_TC_1
Title: Verify KRW currency selection
Steps:
1. Click Account icon
2. Click Default Base Currency dropdown
3. Select KRW
4. Click Save

Expected_Result:
1. KRW available in dropdown
2. "Update successfully" message shown
```

### Step 3: Request AI to Generate

```
Generate automation code for LAP_TC_1 from:
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID

Use framework: @framework_automation_playwright
System prompt: #file:ai-automation-test-generation.mdc
```

### Step 4: Run Test

```bash
pytest TestSuites/test_lap.py::TestLAP::test_LAP_TC_1 -v
```

### Step 5: View Results

```
✓ Test PASSED
✓ Screenshots saved: test-results/screenshots/
✓ Report: test-results/report.html
```

## 💡 Real Example

### Test Case

```
TC_ID: LAP_TC_1
Title: NEW BASE CURRENCY - Verify KRW currency

Preconditions:
1. User is logged into portal as vntest/1234aa
2. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en

Steps:
1. Click on Account icon at the top right corner
2. Click on Default Base Currency dropdown list
3. Select KRW in Default Base Currency dropdown list
4. Click Save

Expected_Result:
1. Make sure there is KRW currency in Default Base Currency dropdown list
2. Make sure text "Update successfully" is shown
3. Make sure My Account popup is hidden
```

### AI Generated Code

AI will create:

**1. Interface File** (`src/Interfaces/interface_my_account.py`):

```python
# Elements for My Account page
ACCOUNT_ICON = "//div[@class='account-icon']"
CURRENCY_DROPDOWN = "//select[@id='base-currency']"
SAVE_BUTTON = "//button[text()='Save']"
SUCCESS_MESSAGE = "//div[@class='success-message']"
```

**2. Action File** (`src/Action/action_my_account.py`):

```python
# Business logic for My Account
def select_currency(self, currency):
    self.page.click(ACCOUNT_ICON)
    self.page.select_option(CURRENCY_DROPDOWN, currency)
    self.page.click(SAVE_BUTTON)

def verify_success_message(self):
    assert self.page.element_visible(SUCCESS_MESSAGE)
```

**3. Test File** (`TestSuites/test_lap.py`):

```python
@pytest.mark.tc_id("LAP_TC_1")
def test_LAP_TC_1_verify_krw_currency(self):
    self.action.select_currency("KRW")
    self.action.verify_success_message()
```

### Run Test

```bash
$ pytest TestSuites/test_lap.py::TestLAP::test_LAP_TC_1 -v

test_LAP_TC_1_verify_krw_currency PASSED [100%]

✓ Test completed in 15.3s
✓ Screenshots: 4 files
✓ All assertions passed
```

## 🎁 Detailed Benefits

### For QA

**1. No Need to Learn Coding**

- Only need to write test cases
- AI writes automation code

**2. Save Time**

- Write test case: 5 minutes
- AI generates code: 2 minutes
- Total: 7 minutes (vs 60 minutes manual coding)

**3. Auto-Fix**

- Test fails? AI auto-fixes
- No debugging needed

**4. Easy Regression Testing**

- Just rerun command
- No manual testing needed

### For Team

**1. Increase Test Coverage**

- Generate many tests quickly
- Run regression frequently

**2. Reduce Maintenance Cost**

- AI auto-fixes when UI changes
- No manual code updates needed

**3. Easy Onboarding**

- New QA doesn't need coding knowledge
- Only need to learn writing test cases

## ⚙️ Requirements

### Mandatory

- ✅ **Framework**: `framework_automation_playwright` cloned
- ✅ **Python**: 3.8+
- ✅ **Playwright**: Installed
- ✅ **AI**: Claude Desktop (or ChatGPT, Gemini)
- ✅ **MCP Server**: Installed and running
- ✅ **Google Sheets**: Test cases written in correct format

### Optional

- Browser: Chrome/Firefox
- CI/CD: Jenkins, GitLab CI
- Report: Allure, HTML

## 🔗 Related

- **[AI Manual Testing](../ai-manual-testing/README.md)** - AI performs manual testing
- **[MCP Server](../mcp-server-automation-test/README.md)** - MCP Server automation framework

## 📞 Support

If you encounter issues:

1. See [05-tips-tricks.md](./05-tips-tricks.md)
2. Check if framework is setup correctly
3. Check if MCP Server is running

---

**Get Started**: [01 - Introduction](./01-introduction.md)
