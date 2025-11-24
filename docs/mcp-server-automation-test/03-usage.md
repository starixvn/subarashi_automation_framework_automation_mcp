# 03 - How to Use MCP Server

## 🎯 Using With Claude Desktop

### Step 1: Start

After installation and configuration, open Claude Desktop. MCP Server will automatically start when you open Claude.

### Step 2: Check Connection

Ask Claude:

```
Can you control the browser? List the tools you have.
```

Claude will list tools like:

- `browser_navigate`
- `browser_click`
- `browser_type`
- `browser_screenshot`
- ...

### Step 3: Start Testing

#### Example 1: Test Simple Login Page

**You**:

```
Please test the login page at https://example.com/login

Test information:
- Username: testuser
- Password: Test123!
- Check if it redirects to /dashboard after login
```

**Claude will**:

1. Open browser and navigate to URL
2. Find username input and enter "testuser"
3. Find password input and enter "Test123!"
4. Click Login button
5. Check current URL
6. Report results

#### Example 2: Test Form Validation

**You**:

```
Test registration form at https://example.com/register

Check these cases:
1. Invalid email (test@test)
2. Password too short (< 8 characters)
3. Confirm password doesn't match
4. All fields empty

For each case, check if error message appears.
```

**Claude will automatically**:

- Test each case one by one
- Capture screenshot for each case
- Report detailed results

#### Example 3: Test Complete User Flow

**You**:

```
Test complete shopping flow:

1. Go to homepage https://shop.example.com
2. Search for "iPhone 15"
3. Click first product
4. Add to cart
5. Go to cart
6. Proceed to checkout
7. Fill information:
   - Name: Test User
   - Email: test@example.com
   - Address: 123 Test St
8. Select payment method: Credit Card
9. Check order summary
10. Capture screenshot of final page

Report each step in detail.
```

**Claude will execute each step** and report results.

### Tips for Using With Claude

#### 1. Describe Clearly

❌ **Not good**:

```
Test login
```

✅ **Good**:

```
Test login at https://example.com/login
Username: admin
Password: admin123
Check redirect to /dashboard after successful login
```

#### 2. Request Screenshots

```
After each step, take a screenshot for me to see.
```

#### 3. Request Detailed Report

```
Report in detail:
- What each step does
- What the results are
- Any errors
- Screenshots of important steps
```

#### 4. Test Multiple Scenarios

```
Test login with these cases:
1. Correct username/password
2. Correct username, wrong password
3. Wrong username
4. Both empty
5. Username with special characters
```

## 🔄 Using With n8n

### Step 1: Start MCP Server

```bash
# Default port 8000
uv run main.py --transport sse
```

Keep this terminal running.

### Step 2: Create Workflow In n8n

1. Open n8n
2. Create new workflow
3. Add **"MCP Client"** node

### Step 3: Configure MCP Client Node

**Connection**:

- **SSE Endpoint**: `http://localhost:8000/sse`

**Tools**: Select tools you need, for example:

- `browser_navigate`
- `browser_click`
- `browser_type`
- `browser_screenshot`

### Step 4: Use In Workflow

#### Example: Automated Login Test Workflow

**Node 1: Schedule Trigger**

- Run daily at 9 AM

**Node 2: MCP Client - Navigate**

- Tool: `browser_navigate`
- URL: `https://example.com/login`

**Node 3: MCP Client - Type Username**

- Tool: `browser_type`
- Selector: `input[name="username"]`
- Text: `testuser`

**Node 4: MCP Client - Type Password**

- Tool: `browser_type`
- Selector: `input[name="password"]`
- Text: `Test123!`

**Node 5: MCP Client - Click Login**

- Tool: `browser_click`
- Selector: `button[type="submit"]`

**Node 6: MCP Client - Screenshot**

- Tool: `browser_screenshot`

**Node 7: Send Email**

- Send email with screenshot if test fails

### Tips for Using With n8n

#### 1. Use Error Workflow

Create error workflow to handle when test fails:

- Capture screenshot
- Send notification via Slack/Email
- Log to database

#### 2. Save Results

Save test results to:

- Google Sheets
- Database
- File system

#### 3. Run Parallel Tests

Create multiple MCP Client nodes running in parallel to test faster.

## 📊 Commonly Used Tools

### 1. Navigation

**browser_navigate**

```json
{
  "url": "https://example.com",
  "wait_until": "networkidle"
}
```

### 2. Interaction

**browser_click**

```json
{
  "selector": "button.login",
  "wait_for_selector": true
}
```

**browser_type**

```json
{
  "selector": "input[name='email']",
  "text": "test@example.com"
}
```

**browser_hover**

```json
{
  "selector": ".dropdown-menu"
}
```

### 3. Content

**browser_get_text**

```json
{
  "selector": ".error-message"
}
```

**browser_get_contents**

```json
{
  "selector": "body"
}
```

### 4. Vision

**browser_screenshot**

```json
{
  "full_page": true,
  "path": "screenshot.png"
}
```

**browser_snapshot**

```json
{
  "include_accessibility": true
}
```

### 5. Wait

**browser_wait_for_selector**

```json
{
  "selector": ".loading-spinner",
  "state": "hidden",
  "timeout": 30000
}
```

## 🎨 Common Patterns

### Pattern 1: Login Flow

```
1. Navigate to login page
2. Type username
3. Type password
4. Click login button
5. Wait for redirect
6. Verify URL or element
7. Screenshot for evidence
```

### Pattern 2: Form Validation

```
1. Navigate to form
2. Fill invalid data
3. Submit form
4. Check error messages
5. Screenshot errors
6. Repeat for each validation case
```

### Pattern 3: E2E User Journey

```
1. Navigate to homepage
2. Search for product
3. Click product
4. Add to cart
5. Go to cart
6. Checkout
7. Fill shipping info
8. Select payment
9. Review order
10. Screenshot final page
```

## ❓ FAQ

**Q: Can test websites requiring login?**
A: Yes. You can:

- Automatically login before testing
- Use storage state to save session
- Or test with authenticated cookies

**Q: Can test on mobile?**
A: Yes. Use `viewport` option to set mobile size:

```json
{
  "viewport": {
    "width": 375,
    "height": 667
  }
}
```

**Q: Can run multiple tests simultaneously?**
A: Yes. MCP Server supports multi-session, each session is independent.

**Q: How to debug when test fails?**
A:

- Run without headless to see browser
- Capture screenshot at each step
- View console logs
- Check network requests

---

**Next**: [04 - Features](./04-features.md)
