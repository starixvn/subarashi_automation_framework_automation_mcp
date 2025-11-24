# Framework Automation MCP - AI-Powered Testing Platform

## 📋 Overview

**Framework Automation MCP** is a comprehensive AI-powered testing platform that combines multiple automation tools and workflows to streamline software testing processes. This framework integrates MCP (Model Context Protocol) with AI capabilities to enable intelligent browser automation, automated test case generation, and AI-assisted manual testing.

## 🎯 What Can This Framework Do?

This framework provides four main capabilities:

1. **📝 n8n Generate Checklist** - AI creates testing checklists from Redmine specifications
2. **🌐 MCP Server Browser Automation** - AI controls web browsers for automated testing
3. **🤖 AI Manual Testing** - AI executes manual test cases from Google Sheets automatically
4. **⚡ AI Automation Testing** - AI automatically writes automation test code for you

## 🚀 Quick Navigation

### 1. n8n Generate Checklist

**AI creates testing checklists from Redmine specs!**

- ✅ Reads specifications from Redmine automatically
- ✅ AI analyzes and generates detailed checklists
- ✅ Stores results in Google Sheets
- ✅ Integrates with Slack for notifications
- ✅ Queue management system

**📖 Full Documentation**: [docs/n8n-generate-checklist/README.md](./docs/n8n-generate-checklist/README.md)

**Quick Start**:

```
In Slack: @Bot_Generate_Checklists https://redmine.company.com/issues/12345?key=YOUR_API_KEY
```

**⚠️ Important Notes**:

- Must have `?key=` after Redmine URL
- API Key is required to access Redmine
- Must create Slack channel and add bot first

### 2. MCP Server - Browser Testing Automation

**AI controls web browsers for automated testing!**

- ✅ AI automatically writes and runs tests
- ✅ Just describe in natural language
- ✅ AI adapts when website changes
- ✅ Integrates with Claude Desktop and n8n
- ✅ Full browser control capabilities

**📖 Full Documentation**: [docs/mcp-server-automation-test/README.md](./docs/mcp-server-automation-test/README.md)

**Quick Start**:

```bash
# Install and run
uv sync
uv run playwright install chromium
uv run main.py --transport stdio --headless
```

### 3. AI Manual Testing

**AI performs manual testing for you!**

- ✅ Write test cases in Google Sheets
- ✅ AI automatically executes each step
- ✅ Takes screenshots as evidence
- ✅ Updates results (PASSED/FAILED/BLOCKED) automatically
- ✅ Saves 80% manual testing time

**📖 Full Documentation**: [docs/ai-manual-testing/README.md](./docs/ai-manual-testing/README.md)

**Quick Start**:

```
Tell AI: "Please run all test cases in this Google Sheet: [YOUR_SHEET_URL]"
```

### 4. AI Automation Testing

**AI automatically writes automation test code for you!**

- ✅ AI reads test cases from Google Sheets
- ✅ Automatically writes automation code (Python + Playwright)
- ✅ Creates Page Objects, Actions, Test Suites
- ✅ If test fails → AI automatically fixes and reruns
- ✅ No coding knowledge required!

**📖 Full Documentation**: [docs/ai-automation-testing/README.md](./docs/ai-automation-testing/README.md)

**Quick Start**:

```
Tell AI: "Generate automation code for test cases from: [YOUR_SHEET_URL]
Use framework: @framework_automation_playwright"
```

## 💡 Real-World Examples

### Example 1: n8n Generate Checklist

**Before**: Read Redmine spec → Create checklist manually → 2-3 hours  
**Now**: Send Redmine URL to bot → AI creates checklist → 2-3 minutes

### Example 2: MCP Server Browser Automation

**Before**: Write Playwright/Selenium code → 30-60 minutes per test  
**Now**: Tell AI what to test → AI writes and runs test → 2-5 minutes

### Example 3: AI Manual Testing

**Before**: Manually test 50 test cases → 5-10 minutes each = 4-8 hours  
**Now**: AI tests 50 test cases → 30-60 seconds each = 25-50 minutes

### Example 4: AI Automation Testing

**Before**: Write automation code manually → 30-60 minutes per test case  
**Now**: AI generates automation code → 5-10 minutes per test case (no coding needed!)

## 🛠️ Technologies Used

- **Python**: 3.11 or higher
- **Playwright**: Browser automation
- **MCP (Model Context Protocol)**: AI-browser integration
- **n8n**: Workflow automation platform
- **Google Gemini**: AI model for analysis
- **Google Sheets API**: Data storage and management
- **Slack API**: Team communication
- **UV**: Python package manager

## ⚙️ System Requirements

- **Python**: 3.11 or higher
- **UV**: Package manager ([install here](https://docs.astral.sh/uv/))
- **RAM**: Minimum 4GB
- **Disk**: ~500MB for Playwright browsers
- **OS**: Windows, macOS, or Linux

## 📦 Installation

### Step 1: Clone Repository

```bash
git clone https://gitlab.nexdev.net/subarashi/automation/framework_automation_mcp.git
cd framework_automation_mcp
```

### Step 2: Install Dependencies

```bash
# Install UV package manager first
# Then install project dependencies
uv sync

# Install Playwright browsers
uv run playwright install chromium
```

### Step 3: Configure MCP Server

```bash
# Run with Claude Desktop (stdio)
uv run main.py --transport stdio --headless

# Or run with SSE (default port 8000)
uv run main.py --transport sse
```

## 🎁 Benefits

### For QA Engineers

- ⚡ Save 80% manual testing time
- 🎯 No test cases missed
- 📸 Complete evidence (automatic screenshots)
- 📊 Results automatically updated in Google Sheets
- 🔄 Easy regression testing

### For Developers

- ✅ Quickly verify fixes
- ✅ Automated regression testing
- ✅ Easy CI/CD integration
- 🐛 AI automatically detects bugs

### For Teams

- 🚀 No deep programming knowledge required
- 📝 Test documentation automatically created
- 🤝 Easy to share and collaborate
- 💰 Reduce manual testing costs
- 📈 Increase test coverage

## 📚 Detailed Documentation

Each component has comprehensive documentation with step-by-step guides:

### n8n Generate Checklist

- [01-introduction.md](./docs/n8n-generate-checklist/01-introduction.md) - Introduction and system purpose
- [02-workflow.md](./docs/n8n-generate-checklist/02-workflow.md) - System workflow
- [03-preparation.md](./docs/n8n-generate-checklist/03-preparation.md) - Preparation before use
- [04-how-to-request.md](./docs/n8n-generate-checklist/04-how-to-request.md) - How to send requests
- [05-ai-analysis.md](./docs/n8n-generate-checklist/05-ai-analysis.md) - How AI analyzes
- [06-google-sheet.md](./docs/n8n-generate-checklist/06-google-sheet.md) - How Google Sheet is created
- [07-slack-notifications.md](./docs/n8n-generate-checklist/07-slack-notifications.md) - Slack notifications
- [08-error-handling.md](./docs/n8n-generate-checklist/08-error-handling.md) - Error handling
- [09-detailed-guide.md](./docs/n8n-generate-checklist/09-detailed-guide.md) - Detailed usage guide
- [10-faq.md](./docs/n8n-generate-checklist/10-faq.md) - Frequently asked questions

### MCP Server Browser Automation

- [01-introduction.md](./docs/mcp-server-automation-test/01-introduction.md) - What is MCP Server and how it works
- [02-installation.md](./docs/mcp-server-automation-test/02-installation.md) - Step-by-step installation guide
- [03-usage.md](./docs/mcp-server-automation-test/03-usage.md) - How to use with Claude Desktop and n8n
- [04-features.md](./docs/mcp-server-automation-test/04-features.md) - Main features and examples
- [05-troubleshooting.md](./docs/mcp-server-automation-test/05-troubleshooting.md) - Common error handling
- [06-faq.md](./docs/mcp-server-automation-test/06-faq.md) - Frequently asked questions

### AI Manual Testing

- [01-introduction.md](./docs/ai-manual-testing/01-introduction.md) - What is AI Manual Testing, benefits
- [02-writing-testcases.md](./docs/ai-manual-testing/02-writing-testcases.md) - How to write test cases in Google Sheets
- [03-running-tests.md](./docs/ai-manual-testing/03-running-tests.md) - How to ask AI to run tests
- [04-viewing-results.md](./docs/ai-manual-testing/04-viewing-results.md) - How to view results and screenshots
- [05-tips-tricks.md](./docs/ai-manual-testing/05-tips-tricks.md) - Tips for writing good test cases

### AI Automation Testing

- [01-introduction.md](./docs/ai-automation-testing/01-introduction.md) - What is AI Automation, benefits
- [02-requesting-ai-generate.md](./docs/ai-automation-testing/02-requesting-ai-generate.md) - How to request AI to generate code
- [03-running-tests.md](./docs/ai-automation-testing/03-running-tests.md) - How to run automation tests
- [04-ai-auto-fix.md](./docs/ai-automation-testing/04-ai-auto-fix.md) - AI automatic error fixing
- [05-tips-tricks.md](./docs/ai-automation-testing/05-tips-tricks.md) - Tips and troubleshooting

## 🔗 Integrations

This framework integrates with:

- ✅ **Claude Desktop**: Use AI directly in chat
- ✅ **n8n**: Workflow automation
- ✅ **Google Sheets**: Test case management and results
- ✅ **Slack**: Team notifications
- ✅ **Redmine**: Specification management
- ✅ **Custom AI**: Any AI that supports MCP Protocol

## 📞 Support

If you encounter issues:

1. **n8n Generate Checklist**: See [docs/n8n-generate-checklist/08-error-handling.md](./docs/n8n-generate-checklist/08-error-handling.md)
2. **MCP Server**: See [docs/mcp-server-automation-test/05-troubleshooting.md](./docs/mcp-server-automation-test/05-troubleshooting.md)
3. **AI Manual Testing**: See [docs/ai-manual-testing/05-tips-tricks.md](./docs/ai-manual-testing/05-tips-tricks.md)
4. **AI Automation Testing**: See [docs/ai-automation-testing/05-tips-tricks.md](./docs/ai-automation-testing/05-tips-tricks.md)
5. Contact support team

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

**Subarashi Automation Team**

## 🎯 Project Status

**Status**: Active Development  
**Version**: 1.0  
**Last Updated**: 2024

---

**Get Started Now**: Choose one of the four tools above and follow the documentation link to begin!
