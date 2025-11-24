# 08 - Error Handling

## 🔴 Common Errors

### Error 1: "System is busy"

**Notification**:

```
⏳ The system is currently processing another request.
Please wait a moment.
```

**Cause**:

- Someone else is using the system
- System only processes 1 request at a time

**Solution**:
✅ **Wait 1-2 minutes** then system will automatically process
✅ **Don't resend** request
✅ **Don't do anything**

**Don't**:
❌ Resend request multiple times
❌ Mention bot continuously
❌ Restart bot

### Error 2: "Unable to generate checklist"

**Notification**:

```
❌ Unable to generate checklist.
The AI could not analyze the provided information.
```

**Causes**:

- Redmine link not accessible
- Redmine issue doesn't exist (404)
- AI doesn't have permission to access issue
- Issue doesn't have spec/requirements yet
- Description too vague

**Solution**:

**Step 1**: Check URL

```bash
# Try opening URL in browser
# See if it opens
```

**Step 2**: If URL requires login

```
# Don't send URL
# Instead, describe feature

Example:
@bot Generate checklist for user profile page
Features: Edit name, email, password, avatar
```

**Step 3**: If description too short

```
# Add details

❌ Not good:
@bot test login

✅ Better:
@bot Generate checklist for login page
Features: Email/username login, password, remember me, forgot password
```

### Error 3: "Failed to create Google Sheet"

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

**Step 1**: Wait 5 minutes, try again

```
@bot [Resend request]
```

**Step 2**: If still error

- Screenshot error notification
- Send to admin
- Include time of error

### Error 4: "Failed to share file"

**Notification**:

```
❌ Google Sheet created but failed to share.
File ID: 1S3ynvvSHgq8hw3I34g15wAc_c3jWJ30LFCJoYJJLyP0
```

**Causes**:

- Slack email invalid
- Email not Google
- Google Drive API error

**Solution**:

**Step 1**: Copy File ID

```
File ID: 1S3ynvvSHgq8hw3I34g15wAc_c3jWJ30LFCJoYJJLyP0
```

**Step 2**: Send to admin

```
Subject: Cannot access Google Sheet
File ID: 1S3ynvvSHgq8hw3I34g15wAc_c3jWJ30LFCJoYJJLyP0
My email: john.doe@company.com
```

**Step 3**: Admin will share manually

### Error 5: "AI Agent Error"

**Notification**:

```
❌ AI Agent encountered an error.
Please try again or contact administrator.
```

**Causes**:

- AI timeout (over 30 iterations)
- Spec too complex or too long
- MCP Server error

**Solution**:

**Step 1**: Simplify request

```
# Instead of sending multiple URLs
❌ @bot Test https://site1.com, https://site2.com, https://site3.com

# Send one URL at a time
✅ @bot Test https://site1.com
```

**Step 2**: Add spec to Redmine

```
# If issue lacks information
✅ Update description, acceptance criteria in Redmine
✅ Attach mockups, diagrams
✅ Then send link
```

## 🔧 Troubleshooting Steps

### General error handling process

```
1. Read error notification
   ↓
2. Identify error type
   ↓
3. Try corresponding solution
   ↓
4. If doesn't work, contact admin
```

### Checklist when encountering error

- [ ] Read error notification carefully?
- [ ] Tried again after 5 minutes?
- [ ] Checked if URL is correct?
- [ ] Checked Slack email?
- [ ] Screenshot error?
- [ ] Noted time of error?

## 📞 When to Contact Admin?

### Contact immediately if:

1. **Error repeats multiple times**:

   - Send 3 different requests
   - All error
   - → System may be down

2. **Serious error**:

   - Bot doesn't respond at all
   - All requests timeout
   - → Need to restart system

3. **Error affects many people**:
   - Many people report same error
   - → May be system error

### Information to provide to admin:

```
1. Time of error: 23-11-2024 21:30:00
2. Request sent: @bot Generate checklist for...
3. Error notification: [Screenshot]
4. Slack username: @john.doe
5. Email: john.doe@company.com
```

## 🔄 Retry Strategy

### When to retry?

**Should retry**:

- ✅ Error "System is busy" → Wait 2 minutes
- ✅ Error "Failed to create sheet" → Wait 5 minutes
- ✅ Timeout error → Wait 5 minutes

**Should not retry**:

- ❌ Error "Unable to generate" → Fix request
- ❌ Error "Failed to share" → Contact admin
- ❌ Error "AI Agent error" → Simplify request

### Maximum retry attempts

**Rule**:

- Try maximum **3 times**
- Each time **5 minutes** apart
- If still error → Contact admin

## 💡 Tips to Avoid Errors

### Tip 1: Check Redmine issue before sending

```bash
# Open Redmine link in browser
# See if issue exists
# See if has complete spec
# Check if has attachments
```

### Tip 2: Write clear request

```
❌ Not clear:
@bot test this

✅ Clear:
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE
```

### Tip 3: Send one request at a time

```
❌ Send consecutively:
@bot test page 1
@bot test page 2
@bot test page 3

✅ Send sequentially:
@bot test page 1
[Wait for result]
@bot test page 2
[Wait for result]
```

### Tip 4: Avoid peak hours

**Peak hours** (many users):

- 9:00 - 10:00 AM
- 2:00 - 3:00 PM

**Off-peak hours** (few users):

- 7:00 - 8:00 AM
- 5:00 - 6:00 PM

## 📊 Track System Status

### How to know if system is working?

**Check bot status**:

```
# In Slack
# See if bot has green dot (online)
```

**Quick test**:

```
@bot hello
# If bot replies → System OK
# If no reply → System down
```

## ❓ Frequently Asked Questions

**Q: Sent request but received no notification?**
A:

- Check if bot is online
- Check if you mentioned correct bot name
- Wait 1 minute, system may be busy

**Q: Received "Processing..." but waiting forever for result?**
A:

- Wait maximum 2 minutes
- If over 2 minutes, system may be stuck
- Contact admin

**Q: Google Sheet link doesn't open?**
A:

- Check if logged into Google
- Check if email has access permission
- Copy full link again (may be cut off)

**Q: Want to cancel sent request?**
A:

- Cannot cancel
- Wait for request to finish
- Or contact admin to stop

---

**Next**: [09 - Detailed Usage Guide](./09-detailed-guide.md)
