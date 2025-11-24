# 01 - Introduction to AI Manual Testing

## 🤔 What is AI Manual Testing?

**AI Manual Testing** is a method of using AI to perform manual testing automatically.

### Simple Comparison

**Traditional Manual Testing**:

```
QA Engineer:
1. Read test case from Google Sheets
2. Open browser
3. Login to system
4. Execute each test step
5. Verify results
6. Take screenshots
7. Write results to Google Sheets
8. Repeat for next test case...

⏱️ Time: 5-10 minutes/test case
😴 Boring, error-prone
📸 Must take screenshots manually
```

**AI Manual Testing**:

```
QA Engineer:
1. Write test cases in Google Sheets
2. Tell AI: "Run test cases LAP_TC_1, LAP_TC_2"
3. Do other work or get coffee ☕

AI will:
- Read test cases from Google Sheets
- Open browser automatically
- Login and execute each step
- Verify results
- Take screenshots automatically
- Update results in Google Sheets

⚡ Time: 30-60 seconds/test case
🎯 Accurate, no omissions
📸 Automatic screenshots with naming convention
```

## 🎯 Specific Benefits

### 1. Save Time

**Real example**:

- 50 manual test cases: 50 × 7 minutes = **350 minutes (5.8 hours)**
- 50 AI test cases: 50 × 1 minute = **50 minutes**
- **Saved: 300 minutes (5 hours)**

### 2. No Omissions

AI will:

- ✅ Read ALL test cases in sheet
- ✅ Execute CORRECT steps
- ✅ Verify ALL Expected Results
- ✅ Not skip any assertion

### 3. Complete Evidence

AI automatically creates screenshots with naming convention:

```
LAP_TC_1__1__click_account.png
LAP_TC_1__2__select_currency.png
LAP_TC_1__3__click_save.png
LAP_TC_1__4__verify_success.png
```

### 4. Clear Results

AI updates Google Sheets with:

- **Status**: PASSED / FAILED / BLOCKED
- **Owner**: Your name
- **Details**: If FAILED, AI writes clear reason

## 🔧 How It Works

### Step 1: QA Prepares

```
1. Write test cases in Google Sheets
2. Prepare test environment (URL, username, password)
```

### Step 2: QA Requests AI

```
Tell AI (Claude Desktop):

"Please review the Google Sheet at [SHEET_URL] and check the test cases
LAP_TC_1, LAP_TC_2 one by one. Act as a QC with 10 years of experience,
read carefully, and strictly follow the rules in file #file:ai-manual-qc-rules.mdc.
After completing the test, close the browser.

Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en
Username: vntest
Password: 1234aa
Owner name: YourName"
```

### Step 3: AI Executes

AI will automatically:

**PHASE 1 - PREPARATION**:

- Read all test cases from Google Sheets
- Create mapping: TC_ID → Row Number
- Identify tools needed (browser, API, DB...)

**PHASE 2 - ANALYSIS**:

- Analyze each test case
- Understand Preconditions, Steps, Expected Results
- Plan detailed execution

**PHASE 3 - EXECUTION**:

- Open browser
- Login to system
- Execute each test step
- Take screenshots
- Verify results

**PHASE 4 - REPORTING**:

- Update Status in Google Sheets
- Update Owner
- Write details if FAILED/BLOCKED

**PHASE 5 - CLEANUP**:

- Close browser
- Save screenshots
- Create summary report

### Step 4: QA Views Results

```
1. Open Google Sheets → View Status column
2. View screenshots in folder
3. Read summary report from AI
```

## 📊 Real Example

### Test Case

```
TC_ID: LAP_TC_2
Title: NEW BASE CURRENCY - Verify KRW currency in dropdown
Test_Type: SMOKE
Priority: High

Preconditions:
1. User is logged into portal as vntest/1234aa
2. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en

Steps:
1. Click on Account icon at the top right corner
2. Click on Default Base Currency dropdown list
3. Select KRW in Default Base Currency dropdown list
4. Click Save button

Expected_Result:
1. Make sure there is KRW currency in Default Base Currency dropdown list
2. Make sure text "Update successfully" is shown
3. Make sure My Account popup is hidden after save

Status: (AI will fill)
Owner: (AI will fill)
```

### Results After AI Runs

**Google Sheets updated**:

```
Status: PASSED - All 3 assertions validated successfully.
        KRW available in dropdown, success message shown, popup hidden.
Owner: GitHub Copilot
```

**Screenshots created**:

```
LAP_TC_2__1__click_account_icon.png
LAP_TC_2__2__click_currency_dropdown.png
LAP_TC_2__3__select_krw.png
LAP_TC_2__4__click_save.png
LAP_TC_2__5__verify_success_message.png
LAP_TC_2__6__verify_popup_hidden.png
```

**AI Report**:

```
Test Execution Summary:
- TC_ID: LAP_TC_2
- Status: PASSED
- Duration: 45 seconds
- Screenshots: 6 files
- All expected results verified successfully:
  ✓ KRW currency found in dropdown
  ✓ "Update successfully" message displayed
  ✓ My Account popup closed after save
```

## 🎁 When to Use AI Manual Testing?

### ✅ Should Use When

1. **Regression Testing**

   - Re-run 50-100 test cases each sprint
   - Test cases are stable, rarely change

2. **Smoke Testing**

   - Quickly test main functions
   - Verify new build is stable

3. **Repetitive Tests**

   - Test cases repeat over and over
   - Boring, error-prone

4. **Multi-Environment Testing**
   - Test on local, staging, production
   - Just change URL and credentials

### ❌ Should Not Use When

1. **Exploratory Testing**

   - Need creativity, find new bugs
   - AI cannot replace QA thinking

2. **UX/UI Review**

   - Need subjective evaluation (beautiful/ugly, good/bad UX)
   - AI only verifies technical aspects

3. **New, Unstable Test Cases**
   - Test cases still changing frequently
   - Should test manually first

## 🔑 Requirements

### Mandatory

- ✅ **MCP Server**: Installed and running (see [MCP Server docs](../mcp-server-automation-test/README.md))
- ✅ **AI**: Claude Desktop (or ChatGPT, Gemini)
- ✅ **Google Sheets**: Test cases written in correct format
- ✅ **System Prompt**: File `ai-manual-qc-rules.mdc` available

### Optional

- Browser: Chrome/Firefox (AI will control)
- Database: If test cases need to verify DB
- API: If test cases need to call API

---

**Next**: [02 - Writing Test Cases](./02-writing-testcases.md)
