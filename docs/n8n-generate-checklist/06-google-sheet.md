# 06 - How Google Sheet is Created

## 📊 What Does Google Sheet File Look Like?

### Basic structure

**5 main columns**:
| Test Type | Categories | Sub Categories | Checklist | Expectation |
|-----------|------------|----------------|-----------|-------------|
| Functional | Login | Username Field | Verify username accepts email | System accepts valid email |
| UI | Login | Error Messages | Verify error shows for empty field | Red text appears below field |

**Characteristics**:

- Header (first row) always displays when scrolling
- Text automatically wraps, not cut off
- Column width just right for reading
- Header in bold, easy to distinguish

## 🎨 Automatic Formatting

### 1. Freeze Header

**Effect**:

- When you scroll down, title row still displays
- Always know which column you're viewing

**Without freeze**:

```
[Scroll down]
Row 50: Functional | Login | ... | ... | ...
(Don't remember what this column is)
```

**With freeze**:

```
[Header always displays]
Test Type | Categories | Sub Categories | Checklist | Expectation
Row 50: Functional | Login | ... | ... | ...
(Clear, easy to read)
```

### 2. Auto-Wrap Text

**Effect**:

- Long text automatically wraps
- Not cut off, can read everything

**Without wrap**:

```
| Verify user can login with valid email and pass... |
(Cut off, can't read all)
```

**With wrap**:

```
| Verify user can login with valid  |
| email and password credentials    |
(Can read everything)
```

### 3. Column Width

**Auto set**:

- Each column 220 pixels wide
- Just right for reading, not too wide
- No need to resize manually

### 4. Bold Header

**Effect**:

- Header stands out
- Easy to distinguish header and data
- Looks more professional

## 📝 File Name

### File name format

```
Checklist - [Date-Month-Year Hour:Minute:Second] - [Your name] - [Timestamp]
```

**Example**:

```
Checklist - 23-11-2024 21:30:45 - John Doe - 1700761845.123456
```

**Benefits**:

- Know when file was created
- Know who created it
- Easy to search by name
- No duplicate names

## 🔐 Access Permissions

### What permissions do you have?

**Writer (Edit)**:

- ✅ Read entire file
- ✅ Edit any cell
- ✅ Add/delete rows, columns
- ✅ Change format
- ✅ Share with others
- ✅ Download file
- ❌ Cannot delete file (only owner can delete)

### Who is the owner?

**Owner**: System account (service account)

**Why not you?**

- For centralized system management
- Avoid accidental file deletion
- You still have full edit permission

## 📧 Email Notification

### What email do you receive?

**Email from Google Drive**:

```
Subject: [System Account] has shared a file with you

Body:
[System Account] has shared the following file with you:
Checklist - 23-11-2024 21:30:45 - John Doe

[Open in Google Sheets]
```

**Click "Open in Google Sheets"** to open file.

### Didn't receive email?

**Check**:

1. Spam folder
2. Is Slack email correct
3. Is email Google

**No problem**:

- You still receive link via Slack
- Clicking Slack link also opens file

## 🗂️ File Management

### Find old files

**Way 1: Via Google Drive**

1. Open drive.google.com
2. Find "Shared with me"
3. Find file named "Checklist - ..."

**Way 2: Via Slack**

1. Find old message in Slack channel
2. Click on link

**Way 3: Via Email**

1. Find email from Google Drive
2. Click link in email

### Organize files

**Create folder**:

1. Create folder "QA Checklists" in Google Drive
2. Move all checklists to folder
3. Easy to manage, search

**Rename**:

- You can rename file
- Example: "Login Page Checklist - Sprint 10"

**Create shortcut**:

- Right-click file → "Add shortcut to Drive"
- Put in "My Drive" folder for easy access

## ✏️ Edit File

### What you can do

**Add test cases**:

- Add new row
- Copy format from row above
- Fill content

**Delete test cases**:

- Delete unnecessary rows
- Or mark "N/A" in Checklist column

**Edit content**:

- Click on cell
- Edit text
- Enter to save

**Add columns**:

- Add "Status" column to track
- Add "Assignee" column to assign
- Add "Priority" column to prioritize

**Change format**:

- Change header color
- Highlight important rows
- Add borders

### Example: Add Status column

**Before**:

```
| Test Type | Categories | Checklist | Expectation |
```

**After**:

1. Insert column after "Expectation"
2. Name it "Status"
3. Fill: Pass / Fail / Blocked / N/A

```
| Test Type | Categories | Checklist | Expectation | Status |
| Functional | Login | ... | ... | Pass |
| UI | Login | ... | ... | Fail |
```

## 📤 Share File

### Share with team

**Way 1: Share directly**

1. Click "Share" button
2. Enter colleague's email
3. Choose permission: Viewer / Commenter / Editor
4. Click "Send"

**Way 2: Get link**

1. Click "Share" button
2. Click "Copy link"
3. Paste link in Slack/Email

**Way 3: Add to shared drive**

1. Move file to Team Drive
2. All team automatically has permission

## 💾 Download File

### Export formats

**Google Sheets supports**:

- Excel (.xlsx)
- CSV (.csv)
- PDF (.pdf)
- HTML (.html)

**How to download**:

1. File → Download
2. Choose format
3. File automatically downloads

**When to download?**

- Attach to email
- Import to other tool (Jira, TestRail)
- Offline backup

## ❓ Frequently Asked Questions

**Q: Does file auto-delete?**
A: No. File saves forever unless you delete it.

**Q: Is there a file limit?**
A: No file limit, but Google Drive storage limit (15GB free).

**Q: Can work offline?**
A: Yes, enable "Available offline" in Google Drive settings.

**Q: Can multiple people edit at once?**
A: Yes. Google Sheets supports real-time collaboration.

**Q: Is there version history?**
A: Yes. File → Version history → See version history.

---

**Next**: [07 - Slack Notifications](./07-slack-notifications.md)
