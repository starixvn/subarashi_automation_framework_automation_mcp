# n8n Generate Checklist - Documentation Guide

## ⚠️ IMPORTANT NOTE

**What is the URL in the request?**

- ✅ URL is a **Redmine link** containing spec/requirements of the feature
- ✅ AI will read **all spec on Redmine** (description, acceptance criteria, comments, attachments)
- ✅ AI creates checklist **based on the spec** it reads

**Correct example**:

```
@Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY_HERE
```

**CRITICAL NOTES**:

- ⚠️ Must have `?key=` after Redmine URL
- ⚠️ API Key is required to access Redmine (replace YOUR_API_KEY_HERE with your actual key)
- ⚠️ Exact bot name: `@Bot_Generate_Checklists`
- ⚠️ Must create Slack channel and add bot first
- ⚠️ DO NOT share API Key with others

AI will:

1. Use API Key to access Redmine
2. Read description, acceptance criteria, business rules
3. Read comments, attachments (mockups, diagrams)
4. Create checklist based on all that information

## 📋 Overview

This is a detailed documentation guide for the **Generate Checklist** system - an automated workflow on n8n that helps create software testing checklists (QA Testing Checklist) from user requests via Slack.

## 🎯 Purpose

This system is designed to:

- Automatically read spec/requirements from Redmine
- Use AI Agent (Google Gemini) to analyze spec and create detailed checklists
- Store results in Google Sheets and share with requesters
- Manage processing queue and request status via Google Sheets
- Fully integrate with Slack for user communication

## 📚 Documentation Structure

Documentation is divided into small files for easy reading and maintenance:

1. **[01-introduction.md](./01-introduction.md)** - Introduction and system purpose
2. **[02-workflow.md](./02-workflow.md)** - System workflow
3. **[03-preparation.md](./03-preparation.md)** - Preparation before use
4. **[04-how-to-request.md](./04-how-to-request.md)** - How to send requests
5. **[05-ai-analysis.md](./05-ai-analysis.md)** - How AI analyzes
6. **[06-google-sheet.md](./06-google-sheet.md)** - How Google Sheet is created
7. **[07-slack-notifications.md](./07-slack-notifications.md)** - Slack notifications
8. **[08-error-handling.md](./08-error-handling.md)** - Error handling
9. **[09-detailed-guide.md](./09-detailed-guide.md)** - Detailed usage guide
10. **[10-faq.md](./10-faq.md)** - Frequently asked questions

## 🚀 Quick Start

### System Requirements

- n8n (self-hosted or cloud)
- Google Cloud Project with enabled APIs:
  - Google Sheets API
  - Google Drive API
- Slack Workspace with Bot Token
- Google Gemini API Key
- MCP Server for browser automation

### Basic Setup

1. Import `Generate_Checklist.json` file into n8n
2. Configure credentials (Google Sheets API, Slack Bot Token, Gemini API Key)
3. Create Google Sheet for queue management
4. Activate workflow

## 🔑 Key Features

- ✅ **AI-Powered Analysis**: Uses Google Gemini with Chain-of-Thought reasoning
- ✅ **Redmine Integration**: Integrates MCP Client to read spec from Redmine
- ✅ **Memory Management**: Stores context and history for each user
- ✅ **Queue System**: Processes requests sequentially to avoid overload
- ✅ **Auto-formatting**: Automatically formats Google Sheets with header, column width, text wrap
- ✅ **Error Handling**: Comprehensive error handling with status tracking
- ✅ **Slack Integration**: Real-time communication with users

## 📊 Workflow Overview

```
Slack Request → Queue Management → AI Analysis → Parse JSON →
Create Google Sheet → Append Data → Share File → Notify User
```

## 🛠️ Technologies Used

- **n8n**: Workflow automation platform
- **Google Gemini**: AI model for analysis and generation
- **Google Sheets API**: Data storage and management
- **Google Drive API**: File sharing
- **Slack API**: User communication
- **MCP (Model Context Protocol)**: Read spec from Redmine
- **Vector Store**: Store user memory and context

## 📝 Important Notes

- Workflow processes **sequentially** (1 request at a time) to avoid rate limits
- Each user has **separate memory** stored in Vector Store
- Checklists are created in standard format with 5 columns: Test Type, Categories, Sub Categories, Checklist, Expectation
- Number of checklist items depends on spec complexity

## 🤝 Contributing

This documentation is created to support the team in using and maintaining the workflow. If you have questions or need updates, please create an issue or pull request.

## 📞 Support

If you encounter issues while using, please:

1. Check [08-error-handling.md](./08-error-handling.md) for troubleshooting
2. Review logs in n8n execution history
3. Check status in queue management Google Sheet

---

**Version**: 1.0  
**Last Updated**: 2024  
**Language**: English
