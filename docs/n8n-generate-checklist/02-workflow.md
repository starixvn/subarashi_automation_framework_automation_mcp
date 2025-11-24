# 02 - How the System Works

## 🎬 Quick Summary

When you send a request via Slack, the system will:

1. **Receive request** and queue it
2. **AI reads and analyzes** the content you send
3. **Create checklist** automatically
4. **Create Google Sheet** and format beautifully
5. **Send link** to you via Slack

The entire process takes about **30-60 seconds**!

## 📊 Simple Flow Diagram

```
You send Slack message (with Redmine link)
         ↓
System receives and queues
         ↓
AI reads your request
         ↓
AI accesses Redmine (if URL provided)
         ↓
AI reads all spec/requirements on Redmine
         ↓
AI analyzes and creates checklist based on spec
         ↓
Create new Google Sheet
         ↓
Format beautifully (freeze header, auto-wrap...)
         ↓
Share file with you
         ↓
Send link via Slack
```

## 📝 Detailed Steps

### Step 1: Receive Request and Queue

**What happens?**

- When you send a message in Slack, the system saves it to a Google Sheet
- Each request has status: `pending` (waiting for processing)
- System checks every second if there are new requests

**Why queue?**

- If multiple people send at the same time, system processes sequentially
- Avoid conflicts and errors
- Ensure everyone is processed completely

**Request statuses**:

```
pending (waiting) → processing (processing) → done (completed) or error (error)
```

### Step 2: AI Reads Spec on Redmine

**What does AI do?**

- Read the message content you send
- If there's a Redmine link, AI will access that link
- Read all spec/requirements on Redmine
- Read description, comments, attachments
- Analyze features to test from spec

**What can AI read on Redmine?**

- **Description**: Detailed feature description
- **Acceptance Criteria**: Acceptance conditions
- **Business Rules**: Business rules
- **UI Mockups**: Interface images (if attached)
- **Comments**: Discussions, clarifications
- **Related Issues**: Related issues

### Step 3: Create Checklist

**How does AI create checklist?**

- Divide into groups: Functional, UI, Security, API...
- Each item has complete: test type, feature group, check condition, expected result
- Include error cases and edge cases

**Example checklist created**:

```
Test Type: Functional
Categories: Login
Sub Categories: Username Field
Checklist: Verify username accepts valid email format
Expectation: System accepts email and allows user to proceed
```

### Step 4: Create Google Sheet

**What does system do?**

- Create new Google Sheet file
- Name file: `Checklist - [Date time] - [Your name]`
- Create table with 5 columns: Test Type, Categories, Sub Categories, Checklist, Expectation
- Fill all checklist items into table

### Step 5: Format Beautifully

**Automatic formats**:

- **Freeze header**: Title row always displays when scrolling
- **Auto-wrap text**: Text automatically wraps, not cut off
- **Column width**: Column width just right for reading
- **Bold header**: Title in bold, easy to see

### Step 6: Share File

**Access permissions**:

- File automatically shared with your Slack email
- You have **edit** permission (writer)
- You receive email notification from Google
- You can share with others

### Step 7: Send Notification

**What do you receive?**

- Direct link to Google Sheet
- Number of checklist items created
- Completion time

**Sample message**:

```
✅ Google Sheet has been successfully created!
📌 Title: Checklist - 23-11-2024 21:00:00 - John Doe
🗂️ Total checklist items: 45
📄 Link: https://docs.google.com/spreadsheets/d/...
```

## ⚙️ Handling Multiple Requests Simultaneously

### Scenario: 3 people send requests at the same time

**What happens?**

1. **Person A** sends at 10:00:00 → Process immediately
2. **Person B** sends at 10:00:05 → Wait for A to finish
3. **Person C** sends at 10:00:10 → Wait for B to finish

**Notification for B and C**:

```
⏳ The system is currently processing another request.
Please wait a moment.
```

**Timeline**:

- 10:00:00 - A sends request
- 10:00:05 - B sends request (receives wait notification)
- 10:00:10 - C sends request (receives wait notification)
- 10:00:45 - A receives result
- 10:00:46 - B starts processing
- 10:01:30 - B receives result
- 10:01:31 - C starts processing
- 10:02:15 - C receives result

## 🔄 Request Status

### Possible statuses:

| Status       | Meaning                | What You See                         |
| ------------ | ---------------------- | ------------------------------------ |
| `pending`    | Waiting for processing | No notification yet                  |
| `processing` | Processing             | "Your request is being processed..." |
| `done`       | Completed              | Google Sheet link                    |
| `error`      | Error occurred         | Specific error notification          |
| `notified`   | System busy notified   | "System is busy..."                  |

## 💾 Memory System

### What does AI remember?

**Remember previous requests**:

- AI remembers your last 10 conversations
- If you send similar request, AI will reference old results
- Helps checklist be more consistent

**Example**:

- Time 1: You send "Test login page"
- Time 2: You send "Also test forgot password"
- AI will understand both requests relate to authentication

## ❓ Frequently Asked Questions

**Q: How long to receive result?**
A: Usually 30-60 seconds. If spec is complex or has many attachments, may take longer.

**Q: Is there a limit on number of requests?**
A: No limit, but must wait in turn.

**Q: What if I send wrong request?**
A: You can send a new request, system will process the latest request.

**Q: Does Google Sheet file auto-delete?**
A: No, file will be saved forever in your Google Drive.

**Q: Can I edit checklist after receiving?**
A: Yes, you have full edit permission for the file.

---

**Next**: [03 - Preparation Before Use](./03-preparation.md)
