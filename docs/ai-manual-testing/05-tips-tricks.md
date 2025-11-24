# 05 - Tips & Tricks

## 💡 Tips for Writing Good Test Cases

### 1. Clear Preconditions

**✅ Good**:

```
Preconditions:
1. User is logged into portal as vntest/1234aa
2. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en
3. User has at least 1 product in cart with total > $100
4. Payment method "Credit Card" is enabled in settings
```

**❌ Not good**:

```
Preconditions:
1. User logged in
2. Has products
```

**Why**: AI needs to know EXACTLY credentials, URL, data requirements to setup correctly.

### 2. Specific, Actionable Steps

**✅ Good**:

```
Steps:
1. Click on "Add to Cart" button (blue button, bottom right)
2. Wait for cart icon to update (top right corner)
3. Click on cart icon
4. Verify product "iPhone 15 Pro" is in cart
5. Click "Proceed to Checkout" button
```

**❌ Not good**:

```
Steps:
1. Add product
2. Go to cart
3. Checkout
```

**Why**: AI needs to know EXACTLY which element to click, which text to verify.

### 3. Measurable Expected Results

**✅ Good**:

```
Expected_Result:
1. Verify success message "Order placed successfully" is displayed (green banner, top of page)
2. Verify order number is shown (format: ORD-XXXXX, where X is digit)
3. Verify email confirmation is sent to user's email
4. Verify order status is "Pending" in My Orders page
5. Verify total amount matches cart total ($123.45)
```

**❌ Not good**:

```
Expected_Result:
1. Order successful
2. Everything works
```

**Why**: AI needs to know EXACTLY what to verify, where, and in what format.

### 4. One Test Case = One Purpose

**✅ Good**:

```
LAP_TC_1: Verify KRW currency selection
LAP_TC_2: Verify USD currency selection
LAP_TC_3: Verify EUR currency selection
```

**❌ Not good**:

```
LAP_TC_1: Test all currencies (KRW, USD, EUR, JPY, CNY...)
```

**Why**: If 1 currency fails, hard to debug. Separate is easier to maintain and debug.

## 🚀 Tips for Efficient Testing

### 1. Run SMOKE Tests First

```
✅ Strategy:
1. Run SMOKE tests first (5-10 critical tests)
2. If SMOKE PASSED → Run FUNCTIONAL tests
3. If SMOKE FAILED → Stop, fix bugs first

❌ Should not:
Run all 100 tests immediately, then discover login is broken
```

### 2. Batch Testing

```
✅ Good:
Batch 1: LAP_TC_1 to LAP_TC_10 (Login & Account)
Batch 2: LAP_TC_11 to LAP_TC_20 (Products)
Batch 3: LAP_TC_21 to LAP_TC_30 (Cart & Checkout)

❌ Not good:
Run all 100 tests at once
```

**Benefits**: Easy to debug, easy to track progress.

### 3. Test on Stable Environment

```
✅ Good:
1. Test on local/staging first
2. Confirm PASSED
3. Then test on production

❌ Not good:
Test directly on production
```

### 4. Check Credentials First

```
✅ Good:
1. Test login manually first
2. Confirm credentials correct
3. Then let AI run

❌ Not good:
Let AI test with wrong credentials → All tests BLOCKED
```

## 🐛 Troubleshooting

### Issue 1: AI Cannot Read Google Sheets

**Symptoms**:

```
Error: Cannot access Google Sheets
```

**Cause**:

- Sheet not public
- AI has no access permission

**Solution**:

```
1. Open Google Sheets
2. Click "Share" button (top right)
3. Set "Anyone with the link" → "Viewer"
4. Copy link
5. Paste into prompt and try again
```

### Issue 2: AI Cannot Find TC_ID

**Symptoms**:

```
BLOCKED - TC_ID not found in sheet
```

**Cause**:

- TC_ID wrong spelling
- TC_ID doesn't exist
- Sheet structure wrong

**Solution**:

```
1. Check TC_ID in sheet (column A)
2. Check spelling in prompt
3. Ensure row 1 is header
4. Ensure TC_ID in column A
```

### Issue 3: All Tests BLOCKED - Login Failed

**Symptoms**:

```
BLOCKED - Cannot proceed: Login failed with provided credentials
```

**Cause**:

- Wrong Username/Password
- Account locked
- Login page changed

**Solution**:

```
1. Test login manually with credentials in prompt
2. If login successful manually:
   - Check if login page changed
   - Check if selectors correct
3. If login fails manually:
   - Update credentials
   - Unlock account
   - Rerun test
```

### Issue 4: Test FAILED But Manual PASSED

**Symptoms**:

```
FAILED - Element not found: button.save
```

**Cause**:

- Element loads slowly
- Wrong selector
- Dynamic content

**Solution**:

```
1. Add wait step:
   Steps:
   1. Click Save button
   2. Wait for 2 seconds
   3. Verify success message

2. Or update Expected_Result:
   Expected_Result:
   1. Wait for success message to appear (max 5 seconds)
   2. Verify message text is "Update successfully"
```

### Issue 5: Screenshots Not Clear

**Symptoms**:

- Screenshots cropped
- Cannot see element to verify

**Solution**:

```
Add step to capture full page:
Steps:
1. Click Save button
2. Wait for page to load completely
3. Scroll to top of page
4. Take full page screenshot
5. Verify success message
```

## 📊 Best Practices

### 1. Naming Convention

**TC_ID**:

```
✅ Good:
LOGIN_TC_001
CART_TC_001
CHECKOUT_TC_001

❌ Not good:
TC1
Test1
A001
```

**Benefits**: Easy to find, easy to group by module.

### 2. Test Data Management

**✅ Good**:

```
Create separate sheet for test data:

Sheet: TestData
| Username | Password | Role  |
|----------|----------|-------|
| admin    | Admin123 | Admin |
| user1    | User123  | User  |
| guest    | Guest123 | Guest |

In test case reference:
Preconditions:
1. Login as user from TestData sheet (Username: admin)
```

**❌ Not good**:

```
Hardcode credentials in each test case
```

### 3. Reusable Preconditions

**✅ Good**:

```
Create common preconditions:

Common_Precondition_1: User Logged In
1. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en
2. Enter username: vntest
3. Enter password: 1234aa
4. Click Login button
5. Verify dashboard is displayed

In test case:
Preconditions:
1. Execute Common_Precondition_1: User Logged In
2. Navigate to Account Settings page
```

**❌ Not good**:

```
Copy-paste login steps into each test case
```

### 4. Version Control

**✅ Good**:

```
Create new sheet for each version:

TestCases_v1.0
TestCases_v1.1
TestCases_v2.0

Or add Version column:
| TC_ID | Version | Title | ... |
|-------|---------|-------|-----|
| TC_1  | 1.0     | ...   | ... |
| TC_1  | 2.0     | ...   | ... |
```

**❌ Not good**:

```
Overwrite old test cases
```

## 🎯 Advanced Tips

### 1. Parallel Testing

```
Run multiple batches in parallel:

Terminal 1:
"Check test cases LAP_TC_1 to LAP_TC_10"

Terminal 2:
"Check test cases LAP_TC_11 to LAP_TC_20"

Terminal 3:
"Check test cases LAP_TC_21 to LAP_TC_30"

→ 3x faster
```

### 2. Conditional Testing

```
Prompt:
"Check test cases LAP_TC_1 to LAP_TC_10.
If any test FAILED, stop immediately and report."

→ Save time if there's critical bug
```

### 3. Regression Testing

```
Create Regression Suite:

Sheet: RegressionSuite
| TC_ID | Last_Run | Last_Status | Current_Status |
|-------|----------|-------------|----------------|
| TC_1  | 2024-11-23 | PASSED    |                |
| TC_2  | 2024-11-23 | PASSED    |                |

Prompt:
"Check all test cases in RegressionSuite sheet.
Compare Current_Status with Last_Status and report any changes."
```

### 4. Data-Driven Testing

```
Sheet: TestData
| TC_ID | Currency | Expected_Symbol |
|-------|----------|-----------------|
| TC_1  | KRW      | ₩               |
| TC_2  | USD      | $               |
| TC_3  | EUR      | €               |

Prompt:
"For each row in TestData sheet, execute test case with Currency value
and verify Expected_Symbol is displayed."
```

## 📞 When You Need Support

### 1. Check Checklist

```
□ Is MCP Server running?
□ Is Google Sheets public?
□ Is TC_ID spelled correctly?
□ Are credentials correct?
□ Is sheet structure correct (9 columns)?
□ Is row 1 header?
□ Is TC_ID unique?
```

### 2. Collect Information

```
When reporting issue, provide:
- TC_ID
- Google Sheets URL
- Prompt used
- Error message from AI
- Screenshots (if any)
- Expected vs Actual
```

### 3. Contact Support

```
Email: support@example.com
Slack: #ai-testing-support
Include:
- Checklist checked
- Information collected
- Steps to reproduce
```

---

**Back to**: [README](./README.md)
