# 05 - How AI Analyzes

## 🤖 What Does AI Do When Receiving Request?

When you send a request, AI will:

1. **Read** your message
2. **Understand** what you want to test
3. **Access** Redmine (if link provided)
4. **Read spec/requirements**
5. **Create** checklist

## 🌐 How Does AI Read Redmine?

### Read all information

AI reads **all content** on Redmine issue:

**AI can read**:

- ✅ Subject (issue title)
- ✅ Description (detailed description)
- ✅ Acceptance Criteria (acceptance conditions)
- ✅ Business Rules (business rules)
- ✅ Comments (discussions, Q&A)
- ✅ Attachments (mockups, diagrams)
- ✅ Related Issues (related issues)

**Example**: Redmine issue #12345 - Login Feature

```
Description:
- User can login with email/username and password
- Support "Remember Me" checkbox
- Support "Forgot Password" flow
- Max 3 login attempts before lockout

Acceptance Criteria:
- Login form displays correctly
- Invalid credentials show error
- Successful login redirects to dashboard

Attachments:
- login-mockup.png
- user-flow.pdf
```

From this AI knows it needs to create checklist for:

- Email/username field validation
- Password field validation
- Remember me functionality
- Forgot password flow
- Login attempt limit (max 3)
- UI according to mockup
- Flow according to diagram

## 🧠 How Does AI Understand Content?

### What can AI read?

**Displayed text**:

- Titles, labels, placeholders
- Error messages
- Success messages
- Tooltips, hints

**Page structure**:

- How many fields in form
- Which buttons are important
- Where links lead to
- What's in menu

**Behavior**:

- What happens when clicking this button
- What error shows when filling form incorrectly
- Which page to navigate after form submission

### Real example

**Redmine issue has**:

```
Description:
- Email field: must be valid email format, required
- Password field: minimum 8 characters, required
- Sign In button: submit form
- Forgot Password link: redirect to password reset page

Acceptance Criteria:
- Valid email accepted
- Invalid email shows error
- Password less than 8 chars shows error
- Successful login redirects to dashboard
```

**AI understands**:

- Email field: must be valid email, required
- Password field: minimum 8 characters, required
- Sign In button: submit form
- Forgot Password link: has separate flow to test

**AI creates checklist**:

```
✓ Verify email field accepts valid email format
✓ Verify email field shows error for invalid format
✓ Verify email field is required
✓ Verify password field accepts minimum 8 characters
✓ Verify password field shows error for less than 8 characters
✓ Verify password field is required
✓ Verify Sign In button is clickable
✓ Verify Forgot Password link navigates correctly
```

## 📚 What Does AI Remember?

### Remember previous requests

AI remembers **last 10 conversations** with you.

**Benefits**:

- More consistent checklists
- AI understands context better
- No need to explain again

**Example**:

```
Time 1: @bot Generate checklist for login page
       → AI creates 40 checklist items

Time 2: @bot Also add checklist for social login
       → AI understands "also" = add to login page
       → AI creates additional checklist items for Google/Facebook login
```

### Remember created checklists

AI saves **all checklists** created for you.

**Benefits**:

- Reference old checklists
- Avoid duplication
- Learn from your feedback

## 🎯 How Does AI Create Checklist?

### Rules AI follows

**1. Minimum 40 items**:

- Each request at least 40 test cases
- Can be more if feature is complex

**2. Clear categorization**:

- Test Type: Functional, UI, Security, API, Performance
- Categories: Main feature groups
- Sub Categories: Specific sub-features

**3. Complete coverage**:

- ✅ Happy path (main flow)
- ✅ Negative cases (wrong input, errors)
- ✅ Edge cases (boundary values, special)
- ✅ Security (SQL injection, XSS...)

**4. Each item must have**:

- Checklist: What to check (clear, specific)
- Expectation: Expected result (measurable, verifiable)

### Example checklist structure

```
Test Type: Functional
Categories: User Authentication
Sub Categories: Login Form
Checklist: Verify user can login with valid email and password
Expectation: User is redirected to dashboard and sees welcome message

Test Type: UI
Categories: User Authentication
Sub Categories: Login Form
Checklist: Verify error message displays when email field is empty
Expectation: Red error text "Email is required" appears below email field

Test Type: Security
Categories: User Authentication
Sub Categories: Login Form
Checklist: Verify system prevents SQL injection in email field
Expectation: System rejects input with SQL commands and shows error
```

## 🔍 AI Deep Analysis

### AI doesn't just look at surface

**AI checks**:

- Form validation rules
- Error handling
- Success/failure flows
- Navigation paths
- Data persistence
- Session management

**Example**: Registration page

**AI analyzes**:

```
1. Form fields:
   - Username: alphanumeric, 3-20 chars
   - Email: valid email format
   - Password: min 8 chars, 1 uppercase, 1 number
   - Confirm Password: must match password

2. Validation:
   - Client-side: instant feedback
   - Server-side: final check

3. Success flow:
   - Create account
   - Send verification email
   - Redirect to email verification page

4. Error flows:
   - Username taken
   - Email already registered
   - Weak password
   - Network error
```

**AI creates 50+ checklist items** covering all above scenarios.

## 💡 How Does AI Generate Checklist?

### 1. Read spec from Redmine

**AI DOES NOT imagine**, AI only reads what's in Redmine:

- Description
- Acceptance Criteria
- Business Rules
- Comments
- Attachments (mockups, diagrams)

### 2. Analyze spec

**AI analyzes spec** to find:

- Features to test
- Validation rules
- Business logic
- UI elements
- Integration points
- Error cases mentioned in spec

### 3. Generate checklist according to spec

**AI creates checklist 100% based on spec**:

- Each acceptance criteria → multiple checklist items
- Each business rule → corresponding checklist items
- Each UI element in mockup → UI checklist items
- Each error case in spec → negative test items

**Example**:

```
Spec says: "Password must be 8-20 characters, contain uppercase, lowercase, number"

AI creates checklist:
- ✅ Test password with 7 characters (should fail)
- ✅ Test password with 8 characters (should pass)
- ✅ Test password with 20 characters (should pass)
- ✅ Test password with 21 characters (should fail)
- ✅ Test password without uppercase (should fail)
- ✅ Test password without lowercase (should fail)
- ✅ Test password without number (should fail)
- ✅ Test password with all requirements (should pass)
```

**IMPORTANT**: AI only creates checklist for what's **in the spec**. If spec doesn't mention, AI doesn't create!

## ❓ Frequently Asked Questions

**Q: Can AI read private Redmine issues?**
A: Yes, if you have valid API Key and have permission to access that issue.

**Q: Does AI understand Vietnamese?**
A: Yes, but better to use English for better results.

**Q: What language does AI create checklist in?**
A: Always in English

**Q: Can AI create checklist for mobile app?**
A: Yes. Just need Redmine issue with mobile app spec, AI will create appropriate checklist.

**Q: Is AI-created checklist 100% accurate?**
A: About 95%. You should review and edit if needed.

---

**Next**: [06 - How Google Sheet is Created](./06-google-sheet.md)
