# 01 - Introduction to Generate Checklist Workflow

## 📖 Overview

**Generate Checklist** is an automated workflow on the n8n platform, designed to help QA Engineers create test checklists from software requirements quickly and accurately.

## 🎯 Purpose

### Problems to Solve

In software development, creating test checklists often encounters these issues:

1. **Time-consuming**: QA must manually read and analyze requirement documents
2. **Lack of consistency**: Each person has a different way of writing checklists
3. **Easy to miss**: May miss edge cases or negative scenarios
4. **Difficult to manage**: Checklists scattered in many places, hard to track

### Solution

This workflow provides:

- ✅ **Automatic analysis**: AI reads and understands requirements from URL, docs, mockups
- ✅ **Standardized format**: All checklists follow a unified format
- ✅ **Comprehensive coverage**: AI ensures coverage of happy path, negative cases, edge cases
- ✅ **Centralized management**: All checklists stored in Google Sheets

## 🌟 Key Features

### 1. Send Requests via Slack

- Send messages in Slack channel
- Can send URL, feature description, or specific requests
- System automatically receives and processes

### 2. AI Automatic Analysis

- AI will access the Redmine issue you provide
- Read all spec/requirements
- Analyze features to test
- Create a complete checklist

### 3. Automatic Google Sheet Creation

- Create new Google Sheet file
- Beautiful format, easy to read
- Automatically share with you
- You can edit immediately

### 4. Result Notification

- Receive "Processing..." notification immediately
- Receive Google Sheet link when completed
- Know immediately if errors occur

## 📋 How is the Checklist Created?

Each checklist item includes:

| Column             | Description        | Example                                |
| ------------------ | ------------------ | -------------------------------------- |
| **Test Type**      | Type of test       | Functional, UI, Security, API          |
| **Categories**     | Main feature group | Login, Dashboard, Payment              |
| **Sub Categories** | Sub-feature        | Username validation, Password rules    |
| **Checklist**      | What to check      | Verify username accepts email format   |
| **Expectation**    | Expected result    | System accepts valid email as username |

## 🎬 Workflow Process

```
Step 1: You send request via Slack
   ↓
Step 2: System receives and queues
   ↓
Step 3: AI analyzes your request
   ↓
Step 4: AI accesses Redmine (if link provided)
   ↓
Step 5: AI creates checklist
   ↓
Step 6: Create and format Google Sheet
   ↓
Step 7: Share file with you
   ↓
Step 8: Send link via Slack
```

## 💡 Usage Examples

### Example 1: Test Login Feature

**You send**: Redmine link containing login feature spec

```
@bot Generate checklist for https://redmine.company.com/issues/12345
```

**AI reads spec on Redmine**:

- Requirements: Username/password login, remember me, forgot password
- Business rules: Password min 8 chars, max 3 login attempts
- UI mockups: Form layout, error messages

**System creates**:

- Functional tests: Login flow according to spec
- UI tests: According to mockup on Redmine
- Security tests: According to security requirements
- Edge cases: According to business rules

### Example 2: Test API Feature

**You send**: Redmine link containing API spec

```
@bot Create test checklist for https://redmine.company.com/issues/12346
```

**AI reads API spec on Redmine**:

- Endpoints: GET/POST/PUT/DELETE /api/users
- Request/Response format
- Validation rules
- Error codes

**System creates**:

- API tests according to endpoints in spec
- Validation tests according to rules in spec
- Error handling according to defined error codes
- Performance tests if required in spec

### Example 3: Test Complex Feature

**You send**: Redmine link containing payment feature spec

```
@bot Generate checklist for https://redmine.company.com/issues/12347
```

**AI reads detailed spec on Redmine**:

- User flow: Add to cart → Checkout → Payment → Confirmation
- Payment methods: Credit card, PayPal, Bank transfer
- Business rules: Minimum order, shipping fees, discounts
- Integration: Payment gateway specs

**System creates**:

- Complete checklist according to entire spec
- Cover all payment methods
- Test specific business rules
- Integration tests according to spec

## ✅ Benefits

**Time Savings**:

- Before: 2-4 hours writing checklist manually
- After: 1 minute send request, 30-60 seconds receive result

**Better Quality**:

- AI analyzes comprehensively, doesn't miss anything
- Includes edge cases and security tests
- Standard format, easy to read

**Easy Sharing**:

- Google Sheet automatically shared with you
- Team can view and edit together
- Long-term storage, easy to search

## 💡 Tips for Best Checklist

- ✅ Ensure Redmine issue has complete spec/requirements
- ✅ Add clear acceptance criteria to Redmine
- ✅ Attach mockups, diagrams to Redmine issue
- ✅ Clearly state business rules and edge cases in description
- ✅ Have valid API Key to access Redmine

## 🔄 Workflow Lifecycle

1. **Initialization**: User mentions bot in Slack
2. **Queuing**: Request added to queue with status `pending`
3. **Processing**: Schedule trigger picks up request, changes status to `processing`
4. **Analysis**: AI Agent analyzes and generates checklist
5. **Validation**: Parse and validate JSON output
6. **Storage**: Create Google Sheet and append data
7. **Sharing**: Share file with user with edit permission
8. **Notification**: Notify result via Slack
9. **Completion**: Update status to `done` or `error`

---

**Next**: [02 - Workflow](./02-workflow.md)
