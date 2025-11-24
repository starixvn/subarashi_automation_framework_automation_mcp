# 04 - How to Send Requests

## 🎯 Basic Request Method

### EXACT message format

```
@Bot_Generate_Checklists [Redmine URL]?key=[Your API Key]
```

**Real example**:

```
@Bot_Generate_Checklists https://redmine.company.com/projects/myproject/wiki/Login_Feature?key=YOUR_API_KEY_HERE
```

**Explanation**:

- `@Bot_Generate_Checklists`: Tag bot (exact name)
- `https://redmine.company.com/projects/myproject/wiki/Login_Feature`: Redmine URL
- `?key=YOUR_API_KEY_HERE`: Your API Key (replace YOUR_API_KEY_HERE with actual key)

**IMPORTANT NOTES**:

- ⚠️ Must have `?key=` after URL
- ⚠️ API Key must be correct, if wrong cannot access Redmine
- ⚠️ No space between URL and `?key=`

## 📝 Types of Requests

### 1. Send Redmine Link (With API Key)

**When to use**: When you have Redmine link containing spec/requirements

**EXACT format**:

```
@Bot_Generate_Checklists [Redmine URL]?key=[Your API Key]
```

**Real examples**:

```
@Bot_Generate_Checklists https://nexdev.net/projects/onehub/wiki/202511_-_ONE_Hub_-_Generate_Link?key=Your_API_Key

@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=Your_API_Key

@Bot_Generate_Checklists https://redmine.company.com/projects/myproject/wiki/Feature_Spec?key=Your_API_Key
```

**Supported Redmine URL types**:

- Wiki page: `/projects/[project]/wiki/[page]?key=...`
- Issue: `/issues/[number]?key=...`
- Project: `/projects/[project]?key=...`

**What will AI do**:

- Use API Key to access Redmine
- Read description, acceptance criteria
- Read comments, business rules
- View attachments (mockups, diagrams)
- Create checklist based on spec

### 2. Feature Description (No Redmine Link)

**When to use**: When no Redmine issue yet, only have spec

**Format**:

```
@bot_name Generate checklist for [Feature description]
```

**Examples**:

```
@bot_name Generate checklist for login feature with username, password, and remember me checkbox

@bot_name Create test cases for payment feature supporting credit card and PayPal

@bot_name Generate checklist for user registration with email verification
```

**What will AI do**:

- Read your description
- Based on QA experience
- Create checklist according to best practices
- Include edge cases

### 3. Send Multiple Redmine Links

**When to use**: Test multiple related features

**Format**:

```
@bot_name Generate checklist for:
- [Redmine URL 1]
- [Redmine URL 2]
- [Redmine URL 3]
```

**Example**:

```
@bot_name Generate checklist for:
- https://redmine.company.com/issues/12345 (Login)
- https://redmine.company.com/issues/12346 (Register)
- https://redmine.company.com/issues/12347 (Forgot Password)
```

**What will AI do**:

- Read spec from all issues
- Create comprehensive checklist
- Categorize by feature

### 4. Specific Requests

**When to use**: When you want to focus on one aspect

**Format**:

```
@bot_name Generate [Test type] checklist for [URL/Feature]
```

**Examples**:

```
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE
(Focus on security tests)

@Bot_Generate_Checklists https://redmine.company.com/issues/12346?key=YOUR_API_KEY_HERE
(Focus on UI tests)
```

## ✍️ Tips for Writing Good Requests

### Tip 1: More detail is better

**❌ Not good**:

```
@bot_name test login
```

**✅ Better**:

```
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE
```

**✅ Best**:

```
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE

(Redmine issue #12345 has complete:
- Description: Email/username login, social login, remember me, forgot password
- Clear Acceptance Criteria
- Detailed Business Rules
- Attachments: mockups, flow diagrams)
```

### Tip 2: Mention special edge cases

**Example**:

```
@bot_name Generate checklist for payment page
Note: We support installment payment and gift cards
```

AI will create additional test cases for installment and gift cards.

### Tip 3: State platform clearly

**Example**:

```
@bot_name Generate checklist for mobile app login (iOS and Android)

@bot_name Generate checklist for web dashboard (desktop only)
```

### Tip 4: Mention integrations

**Example**:

```
@bot_name Generate checklist for checkout page
We integrate with Stripe, PayPal, and bank transfer
```

## 🎯 Real Step-by-Step Examples

### Scenario 1: Test Login Feature

**Step 1**: Get Redmine issue link containing login spec

```
https://redmine.company.com/issues/12345
```

**Step 2**: Get your API Key (contact admin)

```
YOUR_API_KEY_HERE
```

**Step 3**: Go to Slack channel, send:

```
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE
```

**Step 4**: Wait for "Processing..." notification

**Step 5**: Receive Google Sheet link after 30-60 seconds

**Step 6**: Open sheet, review checklist

**Step 7**: Edit if needed (add/remove test cases)

### Scenario 2: Test Payment Feature

**Step 1**: Get Redmine wiki link containing payment spec

```
https://redmine.company.com/projects/ecommerce/wiki/Payment_Feature
```

**Step 2**: Send request:

```
@Bot_Generate_Checklists https://redmine.company.com/projects/ecommerce/wiki/Payment_Feature?key=YOUR_API_KEY_HERE
```

**Step 3**: Receive checklist with:

- Payment flow tests
- Validation tests
- Integration tests
- Error handling tests

### Scenario 3: Test Complex Feature

**Step 1**: Ensure Redmine issue has complete spec

```
Redmine issue #12346 must have:
- Description: Detailed user journey
- Acceptance Criteria: Pass/fail conditions
- Business Rules: Validation rules, constraints
- Attachments: Mockups, flow diagrams
```

**Step 2**: Send request

```
@Bot_Generate_Checklists https://redmine.company.com/issues/12346?key=YOUR_API_KEY_HERE
```

**Step 3**: Receive complete checklist based on spec

## ⏱️ Processing Time

| Request Type                 | Estimated Time |
| ---------------------------- | -------------- |
| Simple URL (1 page)          | 30-45 seconds  |
| Complex URL (many features)  | 45-60 seconds  |
| Feature description (no URL) | 30-40 seconds  |
| Multiple URLs (2-3 pages)    | 60-90 seconds  |

## ❌ What Not to Do

### 1. Send vague requests

**❌ Avoid**:

```
@bot_name test this
@bot_name checklist
@bot_name help
```

**✅ Should**:

```
@bot_name Generate checklist for [URL or specific description]
```

### 2. Send multiple requests consecutively

**❌ Avoid**:

```
@bot_name test page 1
@bot_name test page 2
@bot_name test page 3
```

(Send all at once within seconds)

**✅ Should**:

- Send 1 request
- Wait for result
- Then send next request

### 3. Send inaccessible URLs

**❌ Avoid**:

```
@bot_name Generate checklist for http://localhost:3000
@bot_name test login
```

**✅ Should**:

- Use Redmine issue link with complete spec
- Ensure valid API Key

## 📊 Track Requests

### Check status

System saves all requests in management Google Sheet.

**Statuses**:

- `pending`: Waiting for processing
- `processing`: Processing
- `done`: Completed
- `error`: Error occurred

**View history**:

- All your requests are saved
- Can review old checklists
- Search by date, file name

---

**Next**: [05 - How AI Analyzes](./05-ai-analysis.md)
