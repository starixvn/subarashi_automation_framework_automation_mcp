# 09 - Detailed Usage Guide

## 🎯 Step-by-Step Guide

### Step 1: Preparation

**Before starting**:

- [ ] Joined Slack channel with bot
- [ ] Have URL or feature description to test
- [ ] Checked Slack email is Google email

### Step 2: Send Request

**Open Slack channel** → **Type message in CORRECT FORMAT**:

```
@Bot_Generate_Checklists [Redmine URL]?key=[Your API Key]
```

**Specific example**:

```
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE
```

**Press Enter** to send.

**Check before sending**:

- ✅ Tagged correct bot name: `@Bot_Generate_Checklists`
- ✅ Complete Redmine URL
- ✅ Have `?key=` after URL
- ✅ Correct API Key

### Step 3: Wait for Processing

**You will see**:

```
Your request is being processed. Kindly wait a moment...
```

**Wait time**: 30-60 seconds

**While waiting**:

- ✅ Can do other work
- ✅ No need to refresh
- ❌ Don't resend request

### Step 4: Receive Result

**Success notification**:

```
✅ Google Sheet has been successfully created!
📌 Title: Checklist - 23-11-2024 21:30:45 - John Doe
🗂️ Total checklist items: 45
📄 Link: https://docs.google.com/spreadsheets/d/...
```

**Click on link** to open Google Sheet.

### Step 5: Review Checklist

**Open Google Sheet** → **Review checklist**:

- Read each test case
- Check if complete
- See if any test case is missing

### Step 6: Edit (If Needed)

**Add test cases**:

1. Insert new row
2. Fill content
3. Copy format from row above

**Delete test cases**:

1. Select row
2. Right-click → Delete row

**Edit content**:

1. Click on cell
2. Edit text
3. Enter to save

### Step 7: Use Checklist

**During testing**:

- Add "Status" column to track
- Add "Assignee" column to assign
- Highlight failed test cases

**After testing**:

- Export to PDF/Excel if needed
- Archive file to folder
- Share with team

## Best Practices

### 1. Write Clear Request

**❌ Not good**:

```
@bot test login
```

**✅ Good**:

```
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE
(Redmine issue has complete spec about email/username login, social login, forgot password)
```

### 2. Review Before Using

**Always review checklist**:

- Read all test cases
- Delete irrelevant cases
- Add project-specific cases

### 3. Customize for Project

**Add appropriate columns**:

- Priority (P0, P1, P2)
- Assignee
- Status (Pass/Fail/Blocked)
- Bug ID
- Notes

### 4. Version Control

**Name file with version**:

```
Login Checklist - v1.0 - Sprint 10
Login Checklist - v1.1 - Sprint 10 (Updated)
```

### 5. Backup Regularly

**Create backup**:

- Export to Excel weekly
- Save to shared drive
- Avoid data loss

## ⚡ Tips & Tricks

### Tip 1: Use Template

**Create checklist template**:

1. Create sample file with standard format
2. Copy format when creating new checklist
3. Save time formatting

### Tip 2: Integrate With Other Tools

**Export to Jira**:

- Export checklist to CSV
- Import to Jira as test cases

**Export to TestRail**:

- Export to Excel
- Import to TestRail

### Tip 3: Create Checklist Library

**Store all checklists**:

- Create folder "Checklist Library"
- Organize by module
- Easy to search, reuse

### Tip 4: Collaborate With Team

**Real-time collaboration**:

- Share file with team
- Review checklist together
- Comment directly in sheet

## ❓ Frequently Asked Questions

**Q: Can create checklist for mobile app?**
A: Yes, but don't send URL. Describe feature instead of sending link.

**Q: Can checklist be used for automation?**
A: Yes. Export to format compatible with automation tool.

**Q: Is there a checklist limit?**
A: No limit.

**Q: Can edit checklist after creation?**
A: Yes, you have full edit permission.

**Q: How to share checklist with people without Google account?**
A: Export to PDF or Excel, send via email.

---

**Next**: [10 - Frequently Asked Questions](./10-faq.md)
