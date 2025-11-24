# 02 - How to Write Test Cases for AI

## 📋 Google Sheets Structure

### 9 Required Columns

Google Sheets must have **EXACTLY 9 columns** in order:

| Column | Column Name         | Required | Description                               |
| ------ | ------------------- | -------- | ----------------------------------------- |
| A      | **TC_ID**           | ✅       | Unique test case ID (e.g., LAP_TC_1)      |
| B      | **Title**           | ✅       | Short test case name                      |
| C      | **Test_Type**       | ✅       | Test type: SMOKE, FUNCTIONAL, UI, API, DB |
| D      | **Priority**        | ✅       | Priority: High, Medium, Low               |
| E      | **Preconditions**   | ✅       | Prerequisites (numbered list)             |
| F      | **Steps**           | ✅       | Execution steps (numbered list)           |
| G      | **Expected_Result** | ✅       | Expected results (numbered list)          |
| H      | **Status**          | ⚠️       | AI will fill: PASSED/FAILED/BLOCKED       |
| I      | **Owner**           | ⚠️       | AI will fill with your name               |

**IMPORTANT NOTES**:

- ⚠️ Columns H and I leave EMPTY, AI will fill automatically
- ⚠️ Row 1 is HEADER, data starts from row 2
- ⚠️ TC_ID must be UNIQUE (no duplicates)

## ✍️ How to Write Each Column

### Column A: TC_ID

**Format**: `[PREFIX]_TC_[NUMBER]`

**Examples**:

```
LAP_TC_1
LAP_TC_2
LOGIN_TC_001
PAYMENT_TC_100
```

**Rules**:

- ✅ Must be unique (no duplicates)
- ✅ Should have prefix by module/feature
- ✅ Use underscore `_`, not space
- ❌ Cannot be empty
- ❌ No duplicates

### Column B: Title

**Format**: Short test case description

**Examples**:

```
✅ Good:
- NEW BASE CURRENCY - Verify there is new base currency KRW
- Login with valid credentials
- Add product to cart and checkout

❌ Not good:
- Test 1
- Check currency
- Login
```

**Rules**:

- ✅ Clear, easy to understand
- ✅ State test purpose clearly
- ❌ Not too long (< 100 characters)

### Column C: Test_Type

**Allowed values**:

- `SMOKE` - Quick test of main functions
- `FUNCTIONAL` - Detailed function test
- `UI` - Interface test
- `API` - API test
- `DB` - Database test

**Examples**:

```
SMOKE
FUNCTIONAL
UI
```

### Column D: Priority

**Allowed values**:

- `High` - High priority, must test first
- `Medium` - Medium priority
- `Low` - Low priority

**Examples**:

```
High
Medium
Low
```

### Column E: Preconditions

**Format**: Numbered list, one condition per line

**Examples**:

```
1. User is logged into portal as username/password
2. Click on Account icon at the top right corner
```

**Or**:

```
1. User is logged into portal as vntest/1234aa
2. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en
3. User has at least 1 product in cart
```

**Rules**:

- ✅ Numbered list (1. 2. 3...)
- ✅ Clear, specific
- ✅ Include login, navigation if needed
- ❌ Cannot be empty if there are preconditions

### Column F: Steps

**Format**: Numbered list, one step per line

**Examples**:

```
1. Click on Default Base Currency dropdown list
2. Select KRW in Default Base Currency dropdown list
3. Click Save
```

**Or**:

```
1. Enter email: test@example.com
2. Enter password: Test123!
3. Click Login button
4. Wait for dashboard to load
```

**Rules**:

- ✅ Numbered list (1. 2. 3...)
- ✅ Each step clear, specific
- ✅ State clearly element to interact (button, dropdown, input...)
- ✅ State clearly value to enter (if any)
- ❌ Don't write multiple actions in 1 step

**Detailed examples**:

```
✅ Good:
1. Click on "Add to Cart" button (blue button, bottom right)
2. Click on Cart icon at top right
3. Click "Proceed to Checkout" button
4. Enter shipping address: "123 Test St"
5. Select payment method: "Credit Card"
6. Click "Place Order" button

❌ Not good:
1. Add to cart and checkout
2. Enter info and pay
```

### Column G: Expected_Result

**Format**: Numbered list, one expected result per line

**Examples**:

```
1. Make sure there is KRW currency in Default Base Currency dropdown list
2. Make sure text "Update successfully" is shown
3. Make sure My Account popup is hidden
```

**Or**:

```
1. User is redirected to dashboard page
2. Welcome message "Hello, Test User" is displayed
3. Logout button is visible at top right
```

**Rules**:

- ✅ Numbered list (1. 2. 3...)
- ✅ Each expected result is a specific assertion
- ✅ State clearly element/text/behavior to verify
- ✅ Use "Make sure", "Verify", "Check" for clarity
- ❌ Don't write multiple verifications in 1 line

**Detailed examples**:

```
✅ Good:
1. Verify order confirmation message "Order placed successfully" is shown
2. Verify order number is displayed (format: ORD-XXXXX)
3. Verify email confirmation is sent to user
4. Verify order status is "Pending" in My Orders page

❌ Not good:
1. Order is successful
2. Everything works
```

### Column H: Status

**⚠️ LEAVE EMPTY** - AI will fill automatically

AI will fill one of 3 values:

**PASSED**:

```
PASSED - All 3 assertions validated successfully. KRW available in dropdown
```

**FAILED**:

```
FAILED - Assertion 2 failed: Expected "Update successfully" but got "Update failed"
```

**BLOCKED**:

```
BLOCKED - Cannot proceed: Login failed with provided credentials
```

### Column I: Owner

**⚠️ LEAVE EMPTY** - AI will fill automatically

AI will fill your name (from prompt):

```
Owner name: YourName
```

## 📝 Complete Test Case Template

### Example 1: UI Test

| TC_ID    | Title                                   | Test_Type | Priority | Preconditions                                                                                                 | Steps                                                                                                                                                                        | Expected_Result                                                                                                                                                          | Status | Owner |
| -------- | --------------------------------------- | --------- | -------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ----- |
| LAP_TC_1 | NEW BASE CURRENCY - Verify KRW currency | SMOKE     | High     | 1. User is logged into portal as vntest/1234aa<br>2. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en | 1. Click on Account icon at the top right corner<br>2. Click on Default Base Currency dropdown list<br>3. Select KRW in Default Base Currency dropdown list<br>4. Click Save | 1. Make sure there is KRW currency in Default Base Currency dropdown list<br>2. Make sure text "Update successfully" is shown<br>3. Make sure My Account popup is hidden |        |       |

### Example 2: Login Test

| TC_ID      | Title                        | Test_Type  | Priority | Preconditions                                                        | Steps                                                                           | Expected_Result                                                                                      | Status | Owner |
| ---------- | ---------------------------- | ---------- | -------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------ | ----- |
| LOGIN_TC_1 | Login with valid credentials | FUNCTIONAL | High     | 1. User is on login page<br>2. User has valid account: vntest/1234aa | 1. Enter username: vntest<br>2. Enter password: 1234aa<br>3. Click Login button | 1. User is redirected to dashboard<br>2. Welcome message is displayed<br>3. Logout button is visible |        |       |

### Example 3: E-commerce Test

| TC_ID     | Title               | Test_Type  | Priority | Preconditions                                      | Steps                                                                            | Expected_Result                                                                                                 | Status | Owner |
| --------- | ------------------- | ---------- | -------- | -------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------ | ----- |
| CART_TC_1 | Add product to cart | FUNCTIONAL | High     | 1. User is logged in<br>2. User is on product page | 1. Click "Add to Cart" button<br>2. Click Cart icon<br>3. Verify product in cart | 1. Product is added to cart<br>2. Cart count increases by 1<br>3. Product details match (name, price, quantity) |        |       |

## 💡 Tips for Writing Good Test Cases

### 1. Clear Preconditions

```
✅ Good:
1. User is logged into portal as vntest/1234aa
2. Navigate to https://lap.nexdev.net/LAP/12bet?Language=en
3. User has at least 1 product in cart

❌ Not good:
1. User logged in
2. On product page
```

### 2. Specific Steps

```
✅ Good:
1. Click on "Default Base Currency" dropdown list
2. Select "KRW" option from dropdown
3. Click "Save" button

❌ Not good:
1. Select currency
2. Save
```

### 3. Measurable Expected Results

```
✅ Good:
1. Verify text "Update successfully" is displayed
2. Verify dropdown value is "KRW"
3. Verify popup is closed (not visible)

❌ Not good:
1. Success message shown
2. Currency updated
```

### 4. One Test Case = One Purpose

```
✅ Good:
TC_1: Verify KRW currency selection
TC_2: Verify USD currency selection
TC_3: Verify EUR currency selection

❌ Not good:
TC_1: Test all currencies (KRW, USD, EUR, JPY...)
```

## ⚠️ Common Errors

### Error 1: Missing Columns

```
❌ Only 7 columns (missing Status and Owner)
✅ Must have all 9 columns
```

### Error 2: Duplicate TC_ID

```
❌ LAP_TC_1 appears twice
✅ Each TC_ID must be unique
```

### Error 3: Steps Not Numbered

```
❌
Click button
Enter text
Verify result

✅
1. Click button
2. Enter text
3. Verify result
```

### Error 4: Vague Expected Results

```
❌ Everything works correctly

✅
1. Verify success message is shown
2. Verify data is saved
3. Verify page redirects to dashboard
```

---

**Next**: [03 - Running Tests](./03-running-tests.md)
