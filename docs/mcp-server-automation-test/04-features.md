# 04 - Main Features

## 🎯 Capabilities Overview

MCP Server provides 11 capability groups, each with multiple tools.

| Capability      | Description                      | Tools |
| --------------- | -------------------------------- | ----- |
| `core`          | Basic navigation and interaction | 6     |
| `vision`        | Screenshot and snapshot          | 3     |
| `tabs`          | Tab management                   | 4     |
| `console`       | View console logs                | 2     |
| `keyboard`      | Keyboard input                   | 2     |
| `network`       | Monitor network                  | 2     |
| `files`         | File operations                  | 2     |
| `wait`          | Wait for elements                | 3     |
| `api`           | API testing                      | 4     |
| `google_sheets` | Google Sheets integration        | 5     |
| `database`      | Database operations              | 3     |

## 🔧 Core Capabilities

### 1. browser_navigate

Navigate to a URL.

**When to use**:

- Open web page to test
- Navigate between pages

**Example**:

```
Navigate to https://example.com/login
```

### 2. browser_click

Click on an element.

**When to use**:

- Click button
- Click link
- Click checkbox/radio

**Example**:

```
Click button with text "Login"
Click link "Forgot Password"
```

### 3. browser_type

Type text into input field.

**When to use**:

- Fill form
- Enter search query
- Enter username/password

**Example**:

```
Type "test@example.com" into email field
Type "password123" into password field
```

### 4. browser_hover

Hover mouse over element.

**When to use**:

- Test dropdown menu
- Test tooltip
- Test hover effects

**Example**:

```
Hover over "Products" menu to see dropdown
```

### 5. browser_select_option

Select option in dropdown.

**When to use**:

- Select country
- Select category
- Select date

**Example**:

```
Select "Vietnam" in Country dropdown
```

### 6. browser_get_text

Get text content of element.

**When to use**:

- Check error message
- Get product price
- Verify displayed text

**Example**:

```
Get text of error message
Get displayed product price
```

## 📸 Vision Capabilities

### 1. browser_screenshot

Take screenshot of web page.

**When to use**:

- Save evidence
- Compare UI
- Report bugs

**Example**:

```
Take screenshot of entire page
Take screenshot of login form only
```

### 2. browser_snapshot

Capture DOM tree with accessibility info.

**When to use**:

- Analyze page structure
- Test accessibility
- Debug element selectors

**Example**:

```
Capture snapshot of page for analysis
```

### 3. browser_get_contents

Get HTML content.

**When to use**:

- Check source code
- Verify meta tags
- Extract data

**Example**:

```
Get HTML of entire page
Get HTML of product card
```

## 🗂️ Tabs Capabilities

### 1. browser_tab_new

Open new tab.

**When to use**:

- Test multi-tab scenarios
- Open link in new tab

**Example**:

```
Open new tab and navigate to https://example.com
```

### 2. browser_tab_list

List all open tabs.

**When to use**:

- Check number of tabs
- Get tab information

**Example**:

```
List all open tabs
```

### 3. browser_tab_select

Switch to another tab.

**When to use**:

- Switch between tabs
- Test tab navigation

**Example**:

```
Switch to tab 2
```

### 4. browser_tab_close

Close tab.

**When to use**:

- Cleanup after test
- Test close tab behavior

**Example**:

```
Close current tab
```

## ⏱️ Wait Capabilities

### 1. browser_wait_for_selector

Wait for element to appear.

**When to use**:

- Wait for element to load
- Wait for dynamic content

**Example**:

```
Wait for "Submit" button to appear
Wait for loading spinner to disappear
```

### 2. browser_wait_for_navigation

Wait for navigation to complete.

**When to use**:

- After clicking link
- After submitting form

**Example**:

```
Click Login and wait for redirect to complete
```

### 3. browser_wait_for_timeout

Wait for a period of time.

**When to use**:

- Wait for animation
- Delay between actions

**Example**:

```
Wait 2 seconds for animation to finish
```

## 🌐 API Capabilities

### 1. api_request

Call API endpoint.

**When to use**:

- Test REST API
- Verify API response

**Example**:

```
GET https://api.example.com/users
POST https://api.example.com/login with body {username, password}
```

### 2. api_validate_response

Validate API response.

**When to use**:

- Check status code
- Validate response schema

**Example**:

```
Check response status is 200
Check response has "token" field
```

## 📊 Google Sheets Capabilities

### 1. sheets_read

Read data from Google Sheets.

**When to use**:

- Get test data
- Read config

**Example**:

```
Read test cases from Google Sheet
```

### 2. sheets_write

Write data to Google Sheets.

**When to use**:

- Save test results
- Export data

**Example**:

```
Write test results to Google Sheet
```

## 🗄️ Database Capabilities

### 1. db_query

Execute SQL query.

**When to use**:

- Verify data in DB
- Setup test data

**Example**:

```
SELECT * FROM users WHERE email = 'test@example.com'
```

### 2. db_execute

Execute SQL command (INSERT, UPDATE, DELETE).

**When to use**:

- Create test data
- Cleanup after test

**Example**:

```
INSERT INTO users (email, password) VALUES ('test@example.com', 'hash')
```

## 💡 Real Use Cases

### Use Case 1: Test Login With Multiple Accounts

```
1. Read account list from Google Sheets
2. For each account:
   - Navigate to login page
   - Type username
   - Type password
   - Click login
   - Screenshot result
   - Write result to Google Sheets
```

### Use Case 2: Test E-commerce Checkout

```
1. Navigate to product page
2. Add to cart
3. Go to cart
4. Proceed to checkout
5. Fill shipping info
6. Select payment method
7. Screenshot order summary
8. Verify order in database
9. Write test result to Google Sheets
```

### Use Case 3: Test Form Validation

```
1. Navigate to form
2. For each validation case:
   - Fill invalid data
   - Submit
   - Screenshot error
   - Get error message text
   - Verify error message
3. Write all results to Google Sheets
```

### Use Case 4: Monitor Website Uptime

```
1. Schedule: Run every 5 minutes
2. Navigate to homepage
3. Screenshot
4. Check response time
5. Verify critical elements
6. If error:
   - Send alert via Slack
   - Write log to database
```

## 🎯 Best Practices

### 1. Always Wait For Elements

❌ **Not good**:

```
Click button immediately
```

✅ **Good**:

```
Wait for button to appear, then click
```

### 2. Use Descriptive Selectors

❌ **Not good**:

```
Click on div.abc123
```

✅ **Good**:

```
Click button with text "Login"
Click link "Forgot Password"
```

### 3. Capture Evidence

```
After each important action, take screenshot
```

### 4. Verify Results

```
After clicking Login:
- Verify URL has changed
- Verify user name is displayed
- Verify logout button appears
```

### 5. Cleanup After Test

```
After test completes:
- Close all tabs
- Clear cookies
- Logout
```

---

**Next**: [05 - Troubleshooting](./05-troubleshooting.md)
