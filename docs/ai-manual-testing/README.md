# AI Manual Testing - Guide for QA

## 🎯 What is AI Manual Testing?

**AI Manual Testing** = AI performs manual testing for you!

**How it works**:

1. You write test cases in Google Sheets
2. Tell AI: "Please run all test cases in this sheet"
3. AI automatically:
   - Reads each test case
   - Opens browser and executes each step
   - Takes screenshots as evidence
   - Updates results (PASSED/FAILED/BLOCKED) in Google Sheets
   - Writes your name in Owner column

## ✨ Why Use AI Manual Testing?

### Before (Manual Testing)

```
You had to:
1. Read test case from Google Sheets
2. Open browser
3. Execute each step (click, type, verify...)
4. Take screenshots
5. Write results to sheet
6. Repeat for 50-100 test cases...

⏱️ Time: 5-10 minutes/test case
😴 Boring and error-prone
```

### Now (AI Manual Testing)

```
You only need to:
1. Write test cases in Google Sheets
2. Tell AI: "Run all tests"
3. Go get coffee ☕

⚡ Time: 30-60 seconds/test case
🎯 Accurate, no omissions
📸 Automatic screenshots
```

## 📚 Documentation Structure

Documentation consists of 5 concise parts:

1. **[01-introduction.md](./01-introduction.md)** - What is AI Manual Testing, benefits
2. **[02-writing-testcases.md](./02-writing-testcases.md)** - How to write test cases in Google Sheets
3. **[03-running-tests.md](./03-running-tests.md)** - How to ask AI to run tests
4. **[04-viewing-results.md](./04-viewing-results.md)** - How to view results and screenshots
5. **[05-tips-tricks.md](./05-tips-tricks.md)** - Tips for writing good test cases

## 🚀 Quick Start

### Step 1: Prepare Google Sheets

Create Google Sheet with 9 columns:

| TC_ID    | Title               | Test_Type | Priority | Preconditions  | Steps                                                                                     | Expected_Result                                                | Status | Owner |
| -------- | ------------------- | --------- | -------- | -------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------- | ------ | ----- |
| LAP_TC_1 | Verify KRW currency | SMOKE     | High     | User logged in | 1. Click Account icon<br>2. Click Default Base Currency<br>3. Select KRW<br>4. Click Save | 1. KRW available in dropdown<br>2. "Update successfully" shown |        |       |

### Step 2: Ask AI to Run Test

Tell AI (Claude Desktop):

```
Please run all test cases in this Google Sheet:
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID

Owner name: YourName
```

### Step 3: View Results

AI will:

- ✅ Update **Status** column: PASSED/FAILED/BLOCKED
- ✅ Update **Owner** column: YourName
- ✅ Create screenshots: `LAP_TC_1__1__click.png`, `LAP_TC_1__2__verify.png`...

## 💡 Real Example

### Sample Test Case

```
TC_ID: LAP_TC_1
Title: NEW BASE CURRENCY - Verify there is new base currency KRW
Test_Type: SMOKE
Priority: High
Preconditions:
  1. User is logged into portal as username/password
  2. Click on Account icon at the top right corner

Steps:
  1. Click on Default Base Currency dropdown list
  2. Select KRW in Default Base Currency dropdown list
  3. Click Save

Expected_Result:
  1. Make sure there is KRW currency in Default Base Currency dropdown list
  2. Make sure text "Update successfully" is shown and then My Account popup is hidden

Status: (AI will fill)
Owner: (AI will fill)
```

### Results After AI Runs

```
Status: PASSED - All 3 assertions validated successfully. KRW available in dropdown
Owner: GitHub Copilot
```

**Screenshots created**:

- `LAP_TC_1__1__click_dropdown.png`
- `LAP_TC_1__2__select_krw.png`
- `LAP_TC_1__3__click_save.png`
- `LAP_TC_1__4__verify_success.png`

## ⚙️ Requirements

- **AI**: Claude Desktop (or ChatGPT, Gemini)
- **MCP Server**: Installed and configured (see [MCP Server docs](../mcp-server-automation-test/README.md))
- **Google Sheets**: Test cases written in correct format
- **Browser**: Chrome/Firefox (AI will control automatically)

## 🎁 Benefits

### For QA

- ⚡ Save 80% manual testing time
- 🎯 No test cases missed
- 📸 Complete evidence (automatic screenshots)
- 📊 Results automatically updated in Google Sheets

### For Team

- 🔄 Easy regression testing (just re-run)
- 📈 Increase test coverage
- 🤝 Easy handover (clear test cases)
- 💰 Reduce manual testing costs

## 📞 Support

If you encounter issues:

1. See [05-tips-tricks.md](./05-tips-tricks.md) - Troubleshooting
2. Check if MCP Server is running
3. Check if Google Sheets format is correct

---

**Get Started**: [01 - Introduction](./01-introduction.md)
