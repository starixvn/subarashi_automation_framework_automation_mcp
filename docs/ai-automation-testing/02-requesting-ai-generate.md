# 02 - How to Request AI to Write Automation Tests

## 📋 Preparation Before Starting

### 1. Framework Already Setup

```bash
# Clone framework
git clone [REPO_URL] framework_automation_playwright

# Install dependencies
cd framework_automation_playwright
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. MCP Server Running

```bash
# Check MCP Server
uv run main.py --transport stdio --headless
```

### 3. Test Cases Written

Test cases in Google Sheets with all 9 columns:

- TC_ID, Title, Test_Type, Priority
- Preconditions, Steps, Expected_Result
- Status, Owner

## 📝 Prompt Template

### Basic Template

```
Please read test cases from Google Sheet:
https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit

Generate automation code for test cases: [TC_IDs]

Follow the framework structure in @framework_automation_playwright
Use system prompt: #file:ai-automation-test-generation.mdc

Environment: [ENV]
URL: [APP_URL]
Username: [USERNAME]
Password: [PASSWORD]
```

### Real Example

```
Please read test cases from Google Sheet:
https://docs.google.com/spreadsheets/d/1S3ynvvSHgq8hw3I34g15wAc_c3jWJ30LFCJoYJJLyP0/edit

Generate automation code for test cases: LAP_TC_1, LAP_TC_2, LAP_TC_3

Follow the framework structure in @framework_automation_playwright
Use system prompt: #file:ai-automation-test-generation.mdc

Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: vntest
Password: 1234aa
```

## 🎯 Code Generation Scenarios

### Scenario 1: Generate 1 Test Case

```
Generate automation code for test case LAP_TC_1 from:
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID

Framework: @framework_automation_playwright
System prompt: #file:ai-automation-test-generation.mdc

Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: vntest
Password: 1234aa
```

**AI will create**:

```
1. Interface file: src/Interfaces/interface_my_account.py
2. Action file: src/Action/action_my_account.py
3. Test file: TestSuites/test_lap.py (with 1 test method)
```

### Scenario 2: Generate Multiple Test Cases

```
Generate automation code for test cases LAP_TC_1, LAP_TC_2, LAP_TC_3, LAP_TC_4 from:
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID

Framework: @framework_automation_playwright
System prompt: #file:ai-automation-test-generation.mdc

Environment: staging
URL: https://staging.lap.nexdev.net/LAP/12bet?Language=en
Username: testuser
Password: Test123!
```

**AI will create**:

```
1. Interface files:
   - interface_my_account.py
   - interface_products.py
   - interface_cart.py

2. Action files:
   - action_my_account.py
   - action_products.py
   - action_cart.py

3. Test file: test_lap.py (with 4 test methods)
```

### Scenario 3: Generate All Test Cases

```
Generate automation code for ALL test cases from:
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID

Framework: @framework_automation_playwright
System prompt: #file:ai-automation-test-generation.mdc

Environment: production
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: produser
Password: Prod@2024
```

### Scenario 4: Generate By Priority

```
Generate automation code for all test cases with Priority = High from:
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID

Framework: @framework_automation_playwright
System prompt: #file:ai-automation-test-generation.mdc

Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: vntest
Password: 1234aa
```

### Scenario 5: Generate By Test Type

```
Generate automation code for all test cases with Test_Type = SMOKE from:
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID

Framework: @framework_automation_playwright
System prompt: #file:ai-automation-test-generation.mdc

Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: vntest
Password: 1234aa
```

## 🔄 AI Code Generation Process

### Phase 1: Read Test Cases (10-20 seconds)

AI will:

```
1. Connect to Google Sheets
2. Read all columns (A:I)
3. Parse test cases:
   - TC_ID
   - Preconditions
   - Steps
   - Expected_Result
4. Validate test case structure
5. Create execution plan
```

**Output**:

```
✓ Found 3 test cases: LAP_TC_1, LAP_TC_2, LAP_TC_3
✓ All test cases valid
✓ Execution plan created
```

### Phase 2: Capture Elements (30-60 seconds/test case)

AI will:

```
1. Navigate to application URL
2. Login (if needed)
3. Navigate to test page
4. Use MCP tools to capture elements:
   - browser_get_page_html → Get page structure
   - browser_evaluate → Inspect elements precisely
   - Verify element uniqueness
   - Test selectors work
5. Create Interface file with accurate selectors
```

**Output**:

```
Capturing elements for LAP_TC_1:
✓ Account icon: //div[@class='account-icon']
✓ Currency dropdown: //select[@id='base-currency']
✓ Save button: //button[text()='Save']
✓ Success message: //div[@class='success-message']

All selectors verified and tested!
```

### Phase 3: Generate Code (20-30 seconds/test case)

AI will create 3 files:

**1. Interface File** (`src/Interfaces/interface_my_account.py`):

```python
class InterfaceMyAccount:
    # Account elements
    ACCOUNT_ICON = "//div[@class='account-icon']"

    # Currency dropdown
    CURRENCY_DROPDOWN = "//select[@id='base-currency']"
    CURRENCY_OPTION = "//select[@id='base-currency']/option[@value='{currency}']"

    # Buttons
    SAVE_BUTTON = "//button[text()='Save']"
    CANCEL_BUTTON = "//button[text()='Cancel']"

    # Messages
    SUCCESS_MESSAGE = "//div[@class='success-message']"
    ERROR_MESSAGE = "//div[@class='error-message']"

    # Popup
    MY_ACCOUNT_POPUP = "//div[@id='my-account-popup']"
```

**2. Action File** (`src/Action/action_my_account.py`):

```python
from src.Interfaces.interface_my_account import InterfaceMyAccount

class ActionMyAccount:
    def __init__(self, page):
        self.page = PageManager(page)
        self.interface = InterfaceMyAccount()

    def select_currency(self, currency):
        # Click account icon
        self.page.click(self.interface.ACCOUNT_ICON)

        # Wait for dropdown visible
        self.page.for_element_visible(self.interface.CURRENCY_DROPDOWN, timeout=10)

        # Select currency
        self.page.select_option(self.interface.CURRENCY_DROPDOWN, currency)

        # Click save
        self.page.click(self.interface.SAVE_BUTTON)

    def verify_success_message(self):
        # Wait for success message
        self.page.for_element_visible(self.interface.SUCCESS_MESSAGE, timeout=10)

        # Verify message text
        message = self.page.get_text(self.interface.SUCCESS_MESSAGE)
        assert "Update successfully" in message

    def verify_popup_hidden(self):
        # Wait for popup to disappear
        self.page.for_element_hidden(self.interface.MY_ACCOUNT_POPUP, timeout=10)

        # Verify popup not visible
        assert not self.page.element_visible(self.interface.MY_ACCOUNT_POPUP)
```

**3. Test File** (`TestSuites/test_lap.py`):

```python
import pytest
from src.Action.action_my_account import ActionMyAccount

class TestLAP:
    @pytest.fixture(autouse=True)
    def setup_action(self, page):
        self.action_my_account = ActionMyAccount(page)

    @pytest.mark.tc_id("LAP_TC_1")
    def test_LAP_TC_1_verify_krw_currency(self):
        """NEW BASE CURRENCY - Verify there is new base currency KRW"""
        # Step 1-3: Select KRW currency
        self.action_my_account.select_currency("KRW")

        # Expected Result 1-2: Verify success message
        self.action_my_account.verify_success_message()

        # Expected Result 3: Verify popup hidden
        self.action_my_account.verify_popup_hidden()
```

### Phase 4: Verify Code (10-20 seconds)

AI will:

```
1. Check code syntax
2. Verify imports correct
3. Verify file structure correct
4. Create summary report
```

**Output**:

```
Code generation completed!

Files created:
✓ src/Interfaces/interface_my_account.py (15 elements)
✓ src/Action/action_my_account.py (3 methods)
✓ TestSuites/test_lap.py (1 test)

Ready to run:
pytest TestSuites/test_lap.py::TestLAP::test_LAP_TC_1 -v
```

## 💡 Tips for AI to Generate Good Code

### 1. Clear Test Cases

**✅ Good**:

```
Steps:
1. Click on "Account" icon at the top right corner
2. Click on "Default Base Currency" dropdown list
3. Select "KRW" option from the dropdown
4. Click "Save" button

Expected_Result:
1. Verify "KRW" currency is available in dropdown list
2. Verify text "Update successfully" is displayed
3. Verify "My Account" popup is hidden after save
```

**❌ Not good**:

```
Steps:
1. Select currency
2. Save

Expected_Result:
1. Success
```

**Why**: AI needs to know EXACTLY which element, which text to capture and verify.

### 2. Complete Preconditions

**✅ Good**:

```
Preconditions:
1. User is logged into portal as vntest/1234aa
2. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en
3. User is on My Account page
```

**❌ Not good**:

```
Preconditions:
1. User logged in
```

**Why**: AI needs to know URL, credentials to navigate and test.

### 3. Specific Expected Results

**✅ Good**:

```
Expected_Result:
1. Verify dropdown contains option "KRW" with value "KRW"
2. Verify success message "Update successfully" is displayed in green banner at top of page
3. Verify "My Account" popup (id="my-account-popup") is not visible
```

**❌ Not good**:

```
Expected_Result:
1. Currency updated
2. Message shown
```

**Why**: AI needs to know EXACTLY what to verify, where, in what format.

### 4. One Test Case = One Flow

**✅ Good**:

```
LAP_TC_1: Verify KRW currency selection
LAP_TC_2: Verify USD currency selection
LAP_TC_3: Verify EUR currency selection
```

**❌ Not good**:

```
LAP_TC_1: Test all currencies (KRW, USD, EUR, JPY...)
```

**Why**: Easy to debug, easy to maintain, easy to rerun individual tests.

## ⚠️ Common Errors

### Error 1: Cannot Read Google Sheets

**Symptoms**:

```
Error: Cannot access Google Sheets
```

**Solution**:

```
1. Open Google Sheets
2. Click "Share"
3. Set "Anyone with the link" → "Viewer"
4. Copy link and try again
```

### Error 2: Wrong Framework Path

**Symptoms**:

```
Error: Cannot find framework_automation_playwright
```

**Solution**:

```
1. Check if framework is cloned
2. Check if path in prompt is correct
3. Use absolute path: @/full/path/to/framework_automation_playwright
```

### Error 3: MCP Server Not Running

**Symptoms**:

```
Error: Cannot connect to MCP Server
```

**Solution**:

```
1. Check MCP Server:
   uv run main.py --transport stdio --headless

2. Check Claude Desktop config
3. Restart Claude Desktop
```

### Error 4: Element Capture Failed

**Symptoms**:

```
AI: Cannot capture element "Account icon"
```

**Solution**:

```
1. Check if URL is correct
2. Check if credentials are correct
3. Check if element exists (test manually)
4. Provide more info to AI:
   "Element is inside iframe with name='FunctionFrame'"
```

---

**Next**: [03 - Running Tests](./03-running-tests.md)
