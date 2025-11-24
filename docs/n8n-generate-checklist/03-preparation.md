# 03 - Preparation Before Use

## 🎯 What Do You Need to Get Started?

To use the system, you only need:

1. ✅ Slack account (already available in company)
2. ✅ Google account (to receive Google Sheet)
3. ✅ Added to Slack channel with bot

**Not needed**:

- ❌ Install any software
- ❌ Programming knowledge
- ❌ Admin rights

## 📱 Step 1: Create Slack Channel and Add Bot

### Create new channel (if not available)

**Step 1**: Create channel

1. Open Slack workspace
2. Click **+** next to "Channels"
3. Select "Create a channel"
4. Name it: `qa-checklist` or `generate-checklist`
5. Choose **Public** or **Private**
6. Click "Create"

**Step 2**: Add bot to channel

1. Go to newly created channel
2. Click channel name at top of page
3. Select "Integrations" tab
4. Click "Add apps"
5. Search for bot: `Bot_Generate_Checklists`
6. Click "Add" to add bot to channel

**Step 3**: Check bot has joined channel

- You will see notification: `Bot_Generate_Checklists added to #channel-name`
- Bot appears in members list

### Get API Key

**How to get API Key from Redmine**:

1. Log in to Redmine
2. Click on user name in top right corner
3. Select **"My account"**
4. Scroll down to **"API access key"** section
5. Click **"Show"** to display API Key
6. Copy API Key (format: `e57727d4c9b49ba851c33e1cdf387e44cf1094ef`)

**If you don't have API Key yet**:

- Click **"Reset"** to create new API Key
- Note: Reset will invalidate old API Key

**Note**:

- Each user has their own API Key
- DO NOT share API Key with others
- If API Key is leaked, reset immediately

## Step 2: Check Google Email

### Why need Google email?

System needs Google email to:

- Automatically share Google Sheet with you
- Send notification when file is created
- Give you edit permission for file

### Which email is used?

**Email from Slack profile**:

- System gets email from your Slack account
- Ensure Slack email is Google email (Gmail or Google Workspace)

**How to check Slack email**:

1. Click on your avatar in Slack
2. Select "Profile"
3. View "Email" section

**If email is not Google**:

- Request admin to update Slack email
- Or add Google email to Slack profile

## 🧪 Step 3: Test

### Send simple request

**Test message**:

```
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE
```

**What you will see**:

1. **Immediately** (< 1 second):

   ```
   Your request is being processed. Kindly wait a moment...
   ```

2. **After 30-60 seconds**:

   ```
   ✅ Google Sheet has been successfully created!
   📌 Title: Checklist - 23-11-2024 21:00:00 - Your Name
   🗂️ Total checklist items: 42
   📄 Link: https://docs.google.com/spreadsheets/d/...
   ```

3. **Check email**:
   - You will receive email from Google Drive
   - Subject: "[Your Name] has shared a file with you"

### Open Google Sheet

**Click on link** in Slack message or email.

**You will see**:

- Table with 5 columns: Test Type, Categories, Sub Categories, Checklist, Expectation
- About 40-100 rows of checklist items
- Header is frozen (always displays when scrolling)
- Text automatically wraps (not cut off)

### Check edit permission

**Try editing**:

- Click on any cell
- Type text
- If you can type → You have edit permission ✅
- If you can't type → Contact admin ❌

## 📋 Preparation Checklist

Before official use, ensure:

- [ ] Can access Slack channel with bot
- [ ] Bot responds when mentioned
- [ ] Slack email is Google email
- [ ] Tested and received Google Sheet
- [ ] Have edit permission for Google Sheet
- [ ] Received email notification from Google Drive

## ❓ Frequently Asked Questions

**Q: I don't have Google account, can I use it?**
A: No. You need to create free Gmail account at gmail.com

**Q: Company email is not Google, what to do?**
A: There are 2 ways:

- Way 1: Add personal Gmail to Slack profile
- Way 2: Request IT to switch company email to Google Workspace

**Q: I don't see bot in channel?**
A: Request admin to:

- Add bot to channel
- Or add you to channel with bot

**Q: Bot doesn't respond when mentioned?**
A: Check:

- Is bot online (green dot next to name)
- Did you mention correct bot name
- Contact admin if still not working

**Q: Received "System is busy" notification?**
A: Normal. Someone else is using, wait 1-2 minutes and try again.

## 🎓 Usage Tips

### Tip 1: Prepare URL in advance

- Copy URL you need to test
- Paste directly into Slack
- Save time

### Tip 2: Describe clearly

- If no URL, describe feature in detail
- More detailed, more accurate checklist

### Tip 3: Bookmark channel

- Mark Slack channel for quick access
- Or pin channel to top

### Tip 4: Save Google Sheet link

- Create separate folder in Google Drive
- Move all checklists to that folder
- Easy to manage and search

---

**Next**: [04 - How to Send Requests](./04-how-to-request.md)
