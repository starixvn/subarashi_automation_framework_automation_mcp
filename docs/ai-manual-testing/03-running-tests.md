# 03 - How to Run AI Manual Testing

## 🚀 Preparation Before Running

### 1. Check MCP Server

MCP Server must be running:

```bash
# Check MCP Server
uv run main.py --transport stdio --headless
```

If MCP Server not installed yet, see [MCP Server docs](../mcp-server-automation-test/README.md)

### 2. Prepare Information

You need:

- ✅ **Google Sheets URL**: Link to sheet containing test cases
- ✅ **TC_IDs**: List of test cases to run (e.g., LAP_TC_1, LAP_TC_2)
- ✅ **Environment**: local, staging, production
- ✅ **URL**: Link to application to test
- ✅ **Username/Password**: Credentials to login
- ✅ **Owner Name**: Your name

## 📝 Prompt Template

### Complete Template

```
Please review the Google Sheet at [SHEET_URL] and check the test cases
[TC_IDs] one by one. Act as a QC with 10 years of experience, read carefully,
and strictly follow the rules in file #file:ai-manual-qc-rules.mdc.
After completing the test, close the browser.

Environment: [ENV]
URL: [APP_URL]
Username: [USERNAME]
Password: [PASSWORD]
Owner name: [YOUR_NAME]
```

### Real Example

```
Please review the Google Sheet at https://docs.google.com/spreadsheets/d/1S3ynvvSHgq8hw3I34g15wAc_c3jWJ30LFCJoYJJLyP0/edit?gid=0#gid=0 and check the test cases LAP_TC_1, LAP_TC_2 one by one. Act as a QC with 10 years of experience, read carefully, and strictly follow the rules in file #file:ai-manual-qc-rules.mdc. After completing the test, close the browser.

Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: vntest
Password: 1234aa
Owner name: GitHub Copilot
```

## 🎯 Test Running Scenarios

### Scenario 1: Run 1 Test Case

```
Please review the Google Sheet at https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit and check the test case LAP_TC_1. Act as a QC with 10 years of experience, read carefully, and strictly follow the rules in file #file:ai-manual-qc-rules.mdc. After completing the test, close the browser.

Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: vntest
Password: 1234aa
Owner name: YourName
```

### Scenario 2: Run Multiple Test Cases

```
Please review the Google Sheet at https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit and check the test cases LAP_TC_1, LAP_TC_2, LAP_TC_3, LAP_TC_4 one by one. Act as a QC with 10 years of experience, read carefully, and strictly follow the rules in file #file:ai-manual-qc-rules.mdc. After completing the test, close the browser.

Environment: staging
URL: https://staging.lap.nexdev.net/LAP/12bet?Language=en
Username: testuser
Password: Test123!
Owner name: YourName
```

### Scenario 3: Run ALL Test Cases

```
Please review the Google Sheet at https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit and check ALL test cases one by one. Act as a QC with 10 years of experience, read carefully, and strictly follow the rules in file #file:ai-manual-qc-rules.mdc. After completing the test, close the browser.

Environment: production
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: produser
Password: Prod@2024
Owner name: YourName
```

### Scenario 4: Run By Priority

```
Please review the Google Sheet at https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit and check all test cases with Priority = High one by one. Act as a QC with 10 years of experience, read carefully, and strictly follow the rules in file #file:ai-manual-qc-rules.mdc. After completing the test, close the browser.

Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: vntest
Password: 1234aa
Owner name: YourName
```

### Scenario 5: Run By Test Type

```
Please review the Google Sheet at https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit and check all test cases with Test_Type = SMOKE one by one. Act as a QC with 10 years of experience, read carefully, and strictly follow the rules in file #file:ai-manual-qc-rules.mdc. After completing the test, close the browser.

Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: vntest
Password: 1234aa
Owner name: YourName
```

## 📋 Components in Prompt

### 1. Google Sheets URL

**Format**:

```
https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit?gid=[GID]#gid=[GID]
```

**Get URL**:

1. Open Google Sheets
2. Copy URL from address bar
3. Paste into prompt

### 2. TC_IDs

**Format**:

```
# One test case
LAP_TC_1

# Multiple test cases
LAP_TC_1, LAP_TC_2, LAP_TC_3

# All test cases
ALL test cases
```

### 3. Environment

**Common values**:

```
local
dev
staging
uat
production
```

### 4. URL

**Format**: Full application URL

```
https://lap.nexdev.net/LAP/12bet?Language=en
https://staging.example.com/app
http://localhost:3000
```

### 5. Username/Password

**Format**: Plain text

```
Username: vntest
Password: 1234aa

Username: admin@example.com
Password: Admin@123
```

**NOTE**: Don't share credentials publicly!

### 6. Owner Name

**Format**: Your name

```
Owner name: John Doe
Owner name: GitHub Copilot
Owner name: QA Team
```

## 🔄 AI Execution Process

After you send prompt, AI will:

### PHASE 1: PREPARATION (10-20 seconds)

AI will:

```
1. Read Google Sheets (A:I)
2. Create mapping: TC_ID → Row Number
3. Validate test cases (TC_ID unique, columns complete)
4. Create execution plan
```

**Output**:

```
✓ Found 3 test cases: LAP_TC_1, LAP_TC_2, LAP_TC_3
✓ All TC_IDs are unique
✓ All required columns present
✓ Execution plan created
```

### PHASE 2: ANALYSIS (5-10 seconds/test case)

AI analyzes each test case:

```
1. Read Preconditions, Steps, Expected_Results
2. Identify tools needed (browser, API, DB)
3. Plan detailed steps
```

**Output**:

```
Analyzing LAP_TC_1:
- Preconditions: Login required
- Steps: 4 steps (click, select, click, verify)
- Expected Results: 3 assertions
- Tools: Browser automation
```

### PHASE 3: EXECUTION (30-60 seconds/test case)

AI executes test:

```
1. Open browser
2. Navigate to URL
3. Login (if in Preconditions)
4. Execute each Step
5. Take screenshot after each action
6. Verify Expected Results
```

**Output**:

```
Executing LAP_TC_1:
✓ Step 1: Clicked Account icon
  Screenshot: LAP_TC_1__1__click_account.png
✓ Step 2: Clicked currency dropdown
  Screenshot: LAP_TC_1__2__click_dropdown.png
✓ Step 3: Selected KRW
  Screenshot: LAP_TC_1__3__select_krw.png
✓ Step 4: Clicked Save
  Screenshot: LAP_TC_1__4__click_save.png
✓ Verification 1: KRW found in dropdown
✓ Verification 2: Success message shown
✓ Verification 3: Popup hidden
```

### PHASE 4: REPORTING (5 seconds/test case)

AI updates results:

```
1. Read Google Sheets again (A:I)
2. Find row of TC_ID
3. Update Status (H column)
4. Update Owner (I column)
5. Verify update successful
```

**Output**:

```
Updating Google Sheets:
✓ Found LAP_TC_1 at row 2
✓ Updated H2: PASSED - All 3 assertions validated
✓ Updated I2: GitHub Copilot
✓ Verified update successful
```

### PHASE 5: CLEANUP (2-3 seconds)

AI cleans up:

```
1. Close browser
2. Save screenshots
3. Create summary report
```

**Output**:

```
Cleanup:
✓ Browser closed
✓ Screenshots saved: 12 files
✓ Summary report created
```

## 📊 Summary Report

After completion, AI will create summary:

```
Test Execution Summary
======================

Total Test Cases: 3
- PASSED: 2 (66.7%)
- FAILED: 1 (33.3%)
- BLOCKED: 0 (0%)

Details:
--------
✓ LAP_TC_1: PASSED - All assertions validated
✓ LAP_TC_2: PASSED - KRW currency verified
✗ LAP_TC_3: FAILED - Expected "Success" but got "Error"

Screenshots: 18 files saved
Duration: 3 minutes 45 seconds
Owner: GitHub Copilot
```

## 💡 Tips for Efficient Testing

### 1. Run Small Batches

```
✅ Good: Run 5-10 test cases at a time
❌ Not good: Run 100 test cases at once
```

### 2. Run SMOKE Tests First

```
✅ Good:
1. Run SMOKE tests first
2. If PASSED → Run FUNCTIONAL tests
3. If FAILED → Fix bugs first

❌ Not good: Run all immediately
```

### 3. Check Credentials

```
✅ Good: Test login manually first
❌ Not good: Let AI test with wrong credentials
```

### 4. Watch AI Logs

```
AI will log each step:
- Read sheet
- Analyze test case
- Execute actions
- Verify results
- Update sheet

→ Monitor to know what AI is doing
```

## ⚠️ Common Errors

### Error 1: Cannot Read Google Sheets

**Cause**: Sheet not public or AI has no permission

**Solution**:

```
1. Open Google Sheets
2. Click "Share"
3. Set "Anyone with the link" → "Viewer"
4. Copy link and try again
```

### Error 2: Login Failed

**Cause**: Wrong Username/Password

**Solution**:

```
1. Check credentials
2. Test login manually
3. Update prompt with correct credentials
```

### Error 3: TC_ID Not Found

**Cause**: TC_ID doesn't exist in sheet

**Solution**:

```
1. Check TC_ID in sheet
2. Ensure correct spelling
3. Update prompt with correct TC_ID
```

---

**Next**: [04 - Viewing Results](./04-viewing-results.md)
