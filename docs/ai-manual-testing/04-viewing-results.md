# 04 - Viewing Test Results

## 📊 View Results in Google Sheets

### Column H: Status

AI will update one of 3 values:

#### 1. PASSED

**Format**:

```
PASSED - [Details of assertions that passed]
```

**Examples**:

```
PASSED - All 3 assertions validated successfully. KRW available in dropdown

PASSED - Login successful. User redirected to dashboard, welcome message shown

PASSED - Product added to cart. Cart count increased, product details match
```

**Meaning**: ALL Expected Results PASSED ✅

#### 2. FAILED

**Format**:

```
FAILED - [Details of which assertion failed, expected vs actual]
```

**Examples**:

```
FAILED - Assertion 2 failed: Expected "Update successfully" but got "Update failed"

FAILED - Login failed: Expected redirect to /dashboard but stayed on /login

FAILED - Product price mismatch: Expected $99.99 but got $89.99
```

**Meaning**: AT LEAST 1 Expected Result FAILED ❌

#### 3. BLOCKED

**Format**:

```
BLOCKED - [Reason cannot test]
```

**Examples**:

```
BLOCKED - Cannot proceed: Login failed with provided credentials

BLOCKED - Data setup needed: No products available in database

BLOCKED - Environment issue: Server returned 500 error
```

**Meaning**: Cannot execute test due to environment/data issues 🚫

### Column I: Owner

AI will fill your name (from prompt):

```
Owner name: GitHub Copilot
→ Column I: GitHub Copilot

Owner name: John Doe
→ Column I: John Doe
```

## 📸 View Screenshots

### Naming Convention

AI creates screenshots following format:

```
{TC_ID}__{step_index}__{action}.png
```

**Examples**:

```
LAP_TC_1__1__click_account.png
LAP_TC_1__2__click_dropdown.png
LAP_TC_1__3__select_krw.png
LAP_TC_1__4__click_save.png
LAP_TC_1__5__verify_success.png
```

### Folder Structure

Screenshots saved in folder:

```
mcp_output/
├── LAP_TC_1__1__click_account.png
├── LAP_TC_1__2__click_dropdown.png
├── LAP_TC_1__3__select_krw.png
├── LAP_TC_1__4__click_save.png
├── LAP_TC_1__5__verify_success.png
├── LAP_TC_2__1__navigate.png
├── LAP_TC_2__2__login.png
└── ...
```

### How to View Screenshots

**Step 1**: Open `mcp_output` folder

**Step 2**: Find screenshots by TC_ID

```
# Find all screenshots of LAP_TC_1
LAP_TC_1__*.png
```

**Step 3**: View in step_index order

```
LAP_TC_1__1__*.png  → Step 1
LAP_TC_1__2__*.png  → Step 2
LAP_TC_1__3__*.png  → Step 3
...
```

## 📝 View AI Report

### Summary Report

AI will create summary report:

```
Test Execution Summary
======================

Execution Date: 2024-11-23 23:45:00
Owner: GitHub Copilot
Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en

Total Test Cases: 5
- PASSED: 3 (60%)
- FAILED: 1 (20%)
- BLOCKED: 1 (20%)

Passed Tests:
-------------
✓ LAP_TC_1: NEW BASE CURRENCY - Verify KRW currency
  Duration: 45 seconds
  Screenshots: 5 files

✓ LAP_TC_2: Verify USD currency selection
  Duration: 38 seconds
  Screenshots: 4 files

✓ LAP_TC_3: Verify EUR currency selection
  Duration: 42 seconds
  Screenshots: 4 files

Failed Tests:
-------------
✗ LAP_TC_4: Verify JPY currency selection
  Duration: 35 seconds
  Screenshots: 4 files
  Reason: Assertion 1 failed - JPY not found in dropdown
  Expected: JPY currency available
  Actual: Only KRW, USD, EUR available

Blocked Tests:
--------------
⊘ LAP_TC_5: Verify CNY currency selection
  Reason: Cannot proceed - Previous test failed, data inconsistent

Total Duration: 3 minutes 20 seconds
Screenshots Saved: 21 files
```

### Detailed Report (Per Test Case)

AI also creates detailed report for each test case:

```
Test Case: LAP_TC_1
===================

TC_ID: LAP_TC_1
Title: NEW BASE CURRENCY - Verify there is new base currency KRW
Test_Type: SMOKE
Priority: High
Status: PASSED
Owner: GitHub Copilot
Duration: 45 seconds

Preconditions:
--------------
1. User is logged into portal as vntest/1234aa
2. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en

Execution Steps:
----------------
Step 1: Click on Account icon at the top right corner
  ✓ Action completed successfully
  Screenshot: LAP_TC_1__1__click_account.png

Step 2: Click on Default Base Currency dropdown list
  ✓ Action completed successfully
  Screenshot: LAP_TC_1__2__click_dropdown.png

Step 3: Select KRW in Default Base Currency dropdown list
  ✓ Action completed successfully
  Screenshot: LAP_TC_1__3__select_krw.png

Step 4: Click Save
  ✓ Action completed successfully
  Screenshot: LAP_TC_1__4__click_save.png

Verification Results:
---------------------
Expected Result 1: Make sure there is KRW currency in dropdown
  ✓ PASSED - KRW found in dropdown list
  Screenshot: LAP_TC_1__5__verify_krw.png

Expected Result 2: Make sure text "Update successfully" is shown
  ✓ PASSED - Success message displayed
  Screenshot: LAP_TC_1__6__verify_success.png

Expected Result 3: Make sure My Account popup is hidden
  ✓ PASSED - Popup closed successfully
  Screenshot: LAP_TC_1__7__verify_popup_hidden.png

Final Status: PASSED
All 3 assertions validated successfully
```

## 🔍 Analyze Results

### When Test PASSED

**You need to**:

1. ✅ View screenshots to confirm
2. ✅ Mark test case as stable
3. ✅ Move to next test case

**Don't need to**:

- ❌ Don't need to retest (unless code changes)

### When Test FAILED

**You need to**:

1. 🔍 Read FAILED reason carefully
2. 📸 View screenshots to understand issue
3. 🐛 Create bug report with:
   - TC_ID
   - Expected vs Actual
   - Screenshots
4. 🔄 After bug fix, rerun test

**Example Bug Report**:

```
Bug: JPY currency not available in dropdown

TC_ID: LAP_TC_4
Environment: local
URL: https://lap.nexdev.net/LAP/12bet?Language=en

Expected: JPY currency should be available in dropdown
Actual: Only KRW, USD, EUR available

Steps to Reproduce:
1. Login as vntest/1234aa
2. Click Account icon
3. Click Default Base Currency dropdown
4. Check available currencies

Evidence:
- Screenshot: LAP_TC_4__3__verify_dropdown.png
- AI Report: FAILED - JPY not found in dropdown

Priority: High
Assigned to: Dev Team
```

### When Test BLOCKED

**You need to**:

1. 🔍 Read BLOCKED reason carefully
2. 🛠️ Fix issue:
   - If wrong credentials → Update credentials
   - If missing data → Setup data
   - If environment issue → Fix environment
3. 🔄 Rerun test after fix

**Example**:

```
BLOCKED - Cannot proceed: Login failed with provided credentials

→ Check username/password
→ Test login manually
→ Update credentials in prompt
→ Rerun test
```

## 📈 Tracking Test Results

### Create Test Summary Sheet

Create separate sheet to track:

| Date       | Total | Passed | Failed | Blocked | Pass Rate | Owner    |
| ---------- | ----- | ------ | ------ | ------- | --------- | -------- |
| 2024-11-23 | 50    | 45     | 3      | 2       | 90%       | John Doe |
| 2024-11-24 | 50    | 48     | 2      | 0       | 96%       | John Doe |

### Create Bug Tracking Sheet

| Bug ID  | TC_ID    | Title               | Status | Priority | Assigned | Fixed Date |
| ------- | -------- | ------------------- | ------ | -------- | -------- | ---------- |
| BUG-001 | LAP_TC_4 | JPY not in dropdown | Open   | High     | Dev Team |            |
| BUG-002 | LAP_TC_7 | Timeout on save     | Fixed  | Medium   | Dev Team | 2024-11-24 |

## 💡 Tips for Efficient Result Viewing

### 1. View Summary First

```
✅ Good:
1. View summary report first
2. Know overview: how many PASSED/FAILED/BLOCKED
3. Focus on FAILED tests

❌ Not good:
View each test case one by one
```

### 2. Prioritize FAILED Tests

```
✅ Good:
1. View FAILED tests first
2. Create bug reports
3. Assign to dev
4. Then view PASSED tests

❌ Not good:
View in TC_ID order
```

### 3. Save Important Screenshots

```
✅ Good:
1. Copy screenshots of FAILED tests
2. Attach to bug reports
3. Save to shared folder

❌ Not good:
Delete screenshots after viewing
```

### 4. Compare Results Between Runs

```
✅ Good:
Run 1: LAP_TC_4 FAILED
Run 2: LAP_TC_4 PASSED (after bug fix)
→ Confirm bug is fixed

❌ Not good:
Only view last run results
```

---

**Next**: [05 - Tips & Tricks](./05-tips-tricks.md)
