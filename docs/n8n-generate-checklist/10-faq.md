# 10 - Frequently Asked Questions (FAQ)

## 🎯 About System

**Q: What does this system do?**
A: Automatically creates software testing checklists from URL or feature description. You send request via Slack, receive Google Sheet after 30-60 seconds.

**Q: Who can use it?**
A: Anyone with Slack account and added to channel with bot.

**Q: Does it cost money?**
A: No. Completely free for internal use.

**Q: Is there a request limit?**
A: No limit, but must wait in turn if many people use at once.

## 📝 About Checklist

**Q: What language is checklist in?**
A: Always in English (international QA standard).

**Q: Can request checklist in Vietnamese?**
A: Not currently supported. You can translate yourself after receiving.

**Q: Is checklist 100% accurate?**
A: About 95% accurate. Should review and edit if needed.

**Q: Can edit checklist?**
A: Yes, you have full edit permission for Google Sheet.

## ⏱️ About Time

**Q: How long to receive result?**
A: Usually 30-60 seconds. Complex spec or many attachments may take longer.

**Q: Maximum time?**
A: Maximum 2 minutes. Over 2 minutes means error.

**Q: Can send multiple requests at once?**
A: Yes, but will process sequentially. Later request must wait for previous to finish.

**Q: How to know request is being processed?**
A: Receive notification "Your request is being processed..." in Slack.

## 🌐 About Redmine Link and API Key

**Q: Must have API Key?**
A: Yes, required. Without API Key, bot cannot access Redmine.

**Q: Where to get API Key?**
A: Contact admin or find in internal documentation. Each user has their own API Key.

**Q: What format to send?**
A: `@Bot_Generate_Checklists [URL]?key=[API Key]` - Must have `?key=` after URL.

**Q: What does Redmine issue need?**
A: Need description, acceptance criteria. Should have business rules and attachments.

**Q: Can issue without acceptance criteria work?**
A: Yes, but checklist will lack detail. Should add before sending.

**Q: Can send Jira/Confluence link?**
A: No, only supports Redmine.

**Q: What if issue has 404 error?**
A: Check: (1) Is link correct, (2) Is API Key correct, (3) Do you have access permission.

**Q: What if forgot API Key?**
A: Contact admin to retrieve or reset new API Key.

## 📧 About Email and Google Sheet

**Q: What email needed to receive Google Sheet?**
A: Google email (Gmail or Google Workspace). Email from Slack profile.

**Q: Company email not Google, what to do?**
A: Add Gmail to Slack profile, or request IT to switch to Google Workspace.

**Q: Didn't receive email from Google Drive?**
A: Check spam folder. Or use link from Slack also works.

**Q: Does Google Sheet file auto-delete?**
A: No. File saves forever unless you delete it.

**Q: Can work offline on Google Sheet?**
A: Yes. Enable "Available offline" in Google Drive settings.

## 🔧 About Errors

**Q: Received "System is busy", what to do?**
A: Wait 1-2 minutes. System will automatically process your request.

**Q: Received "Unable to generate checklist", why?**
A: URL not accessible, or description too vague. Check again and resend.

**Q: Google Sheet link doesn't open?**
A: Check if logged into Google, if email has permission, if link is cut off.

**Q: Bot doesn't respond, what to do?**
A: Check if bot is online (green dot next to name). If offline, contact admin.

**Q: Want to cancel sent request?**
A: Cannot cancel. Wait for request to finish or contact admin.

## 🎨 About Format and Editing

**Q: Can change Google Sheet format?**
A: Yes. You have full edit permission for format.

**Q: Can add columns?**
A: Yes. Add columns "Status", "Assignee", "Priority"... as you like.

**Q: Can delete test cases?**
A: Yes. Delete row or mark "N/A".

**Q: Can merge multiple checklists?**
A: Yes. Copy/paste between sheets.

## 💾 About Export and Backup

**Q: Can export to Excel?**
A: Yes. File → Download → Excel (.xlsx).

**Q: Can export to PDF?**
A: Yes. File → Download → PDF.

**Q: Can import to Jira?**
A: Yes. Export to CSV, import to Jira.

**Q: How to backup checklist?**
A: Export to Excel periodically, save to shared drive.

## 👥 About Collaboration

**Q: Can share with others?**
A: Yes. Click "Share" button, enter email.

**Q: Can multiple people edit at once?**
A: Yes. Google Sheets supports real-time collaboration.

**Q: Can comment in sheet?**
A: Yes. Right-click cell → Insert comment.

**Q: Is there version history?**
A: Yes. File → Version history.

## 🔒 About Security

**Q: Who can view my checklist?**
A: Only you and people you share with. System doesn't save checklist content.

**Q: Can set password for file?**
A: No. But can limit access permissions (viewer/commenter/editor).

**Q: Is data encrypted?**
A: Yes. Google Sheets encrypts data according to Google standards.

## 📱 About Slack

**Q: Must mention bot to work?**
A: Yes. Must mention @bot_name.

**Q: Can DM bot directly?**
A: Depends on configuration. Usually must use in channel.

**Q: Do notifications spam channel?**
A: No. All replies in thread.

**Q: Can mute notification?**
A: Yes. Mute channel but still receive when mentioned.

## 🚀 About Advanced Features

**Q: Can create checklist template?**
A: Yes. Create sample file, copy format when needed.

**Q: Can schedule checklist creation?**
A: Not supported yet. Must send request manually.

**Q: Can integrate with CI/CD?**
A: Not directly supported yet. Can export and use in pipeline.

**Q: Is there API to call?**
A: No public API yet.

## 💡 Tips & Tricks

**Q: How to make checklist more accurate?**
A: Write detailed request, provide complete information about feature.

**Q: How to find old checklist?**
A: Search in Google Drive "Shared with me", or find old Slack message.

**Q: How to organize many checklists?**
A: Create folder in Google Drive, move all checklists there.

**Q: Can reuse checklist?**
A: Yes. Copy old checklist, edit to fit.

## 🆘 Contact Support

**Q: Have problem, contact who?**
A: Contact admin via Slack or email.

**Q: Want to request new feature?**
A: Send feedback to admin.

**Q: Want to report bug?**
A: Screenshot error, send to admin with detailed information.

---

## 📚 Related Documentation

- [01 - Introduction](./01-introduction.md)
- [02 - Workflow](./02-workflow.md)
- [03 - Preparation](./03-preparation.md)
- [04 - How to Request](./04-how-to-request.md)
- [05 - AI Analysis](./05-ai-analysis.md)
- [06 - Google Sheet](./06-google-sheet.md)
- [07 - Slack Notifications](./07-slack-notifications.md)
- [08 - Error Handling](./08-error-handling.md)
- [09 - Detailed Guide](./09-detailed-guide.md)

---

**🎉 DOCUMENTATION COMPLETED!**

If you have any questions not answered, please contact admin.
