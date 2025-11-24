# 07 - Slack Notifications

## 📱 Types of Notifications

You will receive 3 types of notifications via Slack:

### 1. "Processing" Notification

**When received**:

- Right after you send request (< 1 second)

**Content**:

```
Your request is being processed. Kindly wait a moment...
```

**Meaning**:

- System has received request
- Starting to process
- You just need to wait

### 2. "System Busy" Notification

**When received**:

- When someone else is using the system

**Content**:

```
⏳ The system is currently processing another request.
Please wait a moment.
```

**Meaning**:

- Your request has been saved
- Queued for processing
- Will be processed after previous request finishes

**What do you need to do?**

- Don't need to do anything
- Wait 1-2 minutes
- System will automatically process

### 3. "Completed" Notification

**When received**:

- After 30-60 seconds from start of processing

**Content**:

```
✅ Google Sheet has been successfully created!
📌 Title: Checklist - 23-11-2024 21:30:45 - John Doe - 1700761845.123456
🗂️ Total checklist items: 45
📄 Link: https://docs.google.com/spreadsheets/d/1S3ynvvSHgq8hw3I34g15wAc_c3jWJ30LFCJoYJJLyP0/edit
```

**Information includes**:

- ✅ Success confirmation icon
- 📌 Google Sheet file name
- 🗂️ Number of checklist items
- 📄 Direct link to file

**What do you need to do?**

- Click on link
- Open Google Sheet
- Review checklist
- Edit if needed

## 🔴 Error Notifications

### Possible error types

#### Error 1: AI Cannot Create Checklist

**Notification**:

```
❌ Unable to generate checklist.
The AI could not analyze the provided information.
Please try again with more details.
```

**Causes**:

- Redmine link not accessible
- Redmine issue doesn't exist
- API Key wrong or expired
- Description too vague

**Solution**:

- Check if URL is correct
- Use public URL (no login required)
- Describe in more detail

#### Error 2: Cannot Create Google Sheet

**Notification**:

```
❌ Failed to create Google Sheet.
Please contact administrator.
```

**Causes**:

- Google API temporary error
- Out of quota
- Connection error

**Solution**:

- Try again after 5 minutes
- Contact admin if still error

#### Error 3: Cannot Share File

**Notification**:

```
❌ Google Sheet created but failed to share.
File ID: 1S3ynvvSHgq8hw3I34g15wAc_c3jWJ30LFCJoYJJLyP0
Please contact administrator.
```

**Causes**:

- Slack email invalid
- Email not Google

**Solution**:

- Contact admin with File ID
- Admin will share manually

## 📍 Notification Location

### Where do notifications appear?

**In thread**:

- All notifications reply in thread of original message
- Keeps conversation tidy
- Easy to follow

**Example**:

```
[You send]
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE

  [Bot replies in thread]
  ↳ Your request is being processed...

  [Bot continues in thread]
  ↳ ✅ Google Sheet has been successfully created!
     📄 Link: ...
```

### Broadcast option

**Some notifications have "Also send to channel"**:

- Important notifications will also appear in main channel
- Not just in thread
- So other team members can see

## ⏱️ Notification Timeline

### Normal case

```
00:00 - You send request
00:01 - Receive "Processing..."
00:45 - Receive "Success!" with link
```

### Case with someone using

```
00:00 - You send request
00:01 - Receive "System is busy..."
01:30 - Previous request finishes
01:31 - Receive "Processing..."
02:15 - Receive "Success!" with link
```

### Error case

```
00:00 - You send request
00:01 - Receive "Processing..."
00:30 - Receive "Error..." with error description
```

## 🔔 Notification Settings

### Slack notification preferences

**To not miss notifications**:

1. **Enable notification for channel**:

   - Channel settings → Notifications
   - Choose "All new messages"

2. **Enable notification for mentions**:

   - Preferences → Notifications
   - "Notify me about" → "Direct messages, mentions & keywords"

3. **Add keyword**:
   - Preferences → Notifications → Keywords
   - Add: "Google Sheet", "checklist", "successfully"

## 📊 Track Status

### View request history

**All requests saved in management Google Sheet**.

**Columns**:

- userId: Your Slack ID
- text: Request content
- status: Status (pending/processing/done/error)
- event_ts: Send time
- createdAt: Creation time

**View status**:

- Contact admin to view management table
- Or check in Slack thread

## 💡 Usage Tips

### Tip 1: Save link immediately

When receiving Google Sheet link:

- Copy link immediately
- Paste in private note
- Or bookmark in browser

### Tip 2: Mute channel if too many notifications

If channel too crowded:

- Mute channel
- But still receive notification when mentioned
- Or create separate channel for bot

### Tip 3: Pin important messages

Pin messages with Google Sheet link:

- Hover message → More actions → Pin
- Easy to find later

### Tip 4: Use thread

Always reply in thread:

- Keeps channel tidy
- Easy to follow conversation
- Doesn't spam channel

## ❓ Frequently Asked Questions

**Q: Not receiving notification in Slack?**
A: Check:

- Notification settings
- Is bot online
- Are you in channel

**Q: Received notification but no link?**
A: May be error. Scroll up to see if there's error notification.

**Q: Google Sheet link doesn't open?**
A: Check:

- Have you logged into Google
- Does email have access permission
- Is link cut off (copy full link again)

**Q: Want to turn off notification?**
A: Mute channel, but still receive when mentioned.

---

**Next**: [08 - Error Handling](./08-error-handling.md)
