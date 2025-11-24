# 06 - Frequently Asked Questions (FAQ)

## 🎯 About MCP Server

**Q: What is MCP Server?**
A: MCP Server is a tool that allows AI to control web browsers for automated website testing. You just describe in natural language, AI will do the rest.

**Q: Is MCP Server free?**
A: Yes, MCP Server is completely free and open source. You only pay for AI service (Claude, ChatGPT...) if used.

**Q: Do I need programming knowledge?**
A: Not required. With Claude Desktop, you just talk in Vietnamese/English. With n8n, need basic workflow understanding.

**Q: Can MCP Server replace QA Engineers?**
A: No. MCP Server is a tool to support QA, not replace humans. QA still needs to:

- Design test strategy
- Review test results
- Decide if bug is critical
- Analyze root cause

## 💻 About Installation

**Q: Minimum system requirements?**
A:

- Python 3.11+
- RAM: 4GB
- Disk: 500MB (for browsers)
- OS: Windows 10+, macOS 10.15+, or Linux

**Q: Why use UV instead of pip?**
A: UV is much faster than pip (10-100x) and manages dependencies better. This project is designed to use UV.

**Q: Can I use pip?**
A: Not recommended. Some dependencies may conflict. Should use UV as instructed.

**Q: How long does installation take?**
A:

- Install UV: 1 minute
- `uv sync`: 2-3 minutes
- Install Playwright browsers: 2-3 minutes
- **Total: ~5-7 minutes**

**Q: Need to install all browsers?**
A: No. Only install browsers you want to test:

```bash
uv run playwright install chromium  # Recommended
```

## 🔧 About Usage

**Q: How to get started?**
A:

1. Install following [02-installation.md](./02-installation.md)
2. Configure for Claude Desktop or n8n
3. Start testing following [03-usage.md](./03-usage.md)

**Q: Can test websites requiring login?**
A: Yes. There are 3 ways:

1. Automatically login before testing
2. Use storage state (save cookies/session)
3. Test with authenticated cookies

**Q: Can test on mobile?**
A: Yes. Set viewport size:

```
Test with mobile viewport (375x667)
```

**Q: Can test multiple browsers simultaneously?**
A: Yes. MCP Server supports multi-session, each session can use different browser.

**Q: Can run headless?**
A: Yes. Add `--headless` flag:

```bash
uv run main.py --transport stdio --headless
```

**Q: How to see what browser is doing?**
A: Remove `--headless` flag:

```bash
uv run main.py --transport stdio
```

Browser will display and you'll see AI control it.

## 🎨 About Features

**Q: What can MCP Server do?**
A:

- ✅ Test functionality (login, form, checkout...)
- ✅ Test UI/UX (layout, responsive, colors...)
- ✅ Test performance (page load, network...)
- ✅ Test API (REST, GraphQL...)
- ✅ Screenshot and snapshot
- ✅ Google Sheets integration
- ✅ Database integration

**Q: Can test file upload?**
A: Yes. Use `browser_upload_file` tool.

**Q: Can test file download?**
A: Yes. MCP Server automatically tracks downloads.

**Q: Can test iframe?**
A: Yes. AI can switch into iframe and test.

**Q: Can test shadow DOM?**
A: Yes, but needs special selector.

**Q: Can run custom JavaScript?**
A: Yes. Use `browser_evaluate` tool.

## 🔗 About Integrations

**Q: How to integrate with Claude Desktop?**
A: See details at [02-installation.md](./02-installation.md#configure-for-claude-desktop)

**Q: How to integrate with n8n?**
A: See details at [03-usage.md](./03-usage.md#using-with-n8n)

**Q: Can use with ChatGPT?**
A: Yes, if ChatGPT supports MCP Protocol (currently no official support).

**Q: Can use with Gemini?**
A: Yes, if Gemini supports MCP Protocol.

**Q: Can integrate into CI/CD?**
A: Yes. Run MCP Server in Docker and call from CI/CD pipeline.

## 🐛 About Errors

**Q: Error "uv: command not found"?**
A: See [05-troubleshooting.md](./05-troubleshooting.md#error-1-uv-command-not-found)

**Q: Error "Port already in use"?**
A: See [05-troubleshooting.md](./05-troubleshooting.md#error-5-port-already-in-use)

**Q: Claude Desktop doesn't recognize MCP Server?**
A: See [05-troubleshooting.md](./05-troubleshooting.md#error-8-claude-desktop-doesnt-recognize-mcp-server)

**Q: Element not found?**
A: See [05-troubleshooting.md](./05-troubleshooting.md#error-10-element-not-found)

**Q: Timeout errors?**
A: See [05-troubleshooting.md](./05-troubleshooting.md#error-11-timeout-waiting-for-element)

## 📊 About Performance

**Q: Is MCP Server fast?**
A: Depends on:

- Website speed
- Test complexity
- Headless or not

Average: 5-10 seconds for a simple test case.

**Q: Can run parallel tests?**
A: Yes. MCP Server supports multi-session, can run multiple tests simultaneously.

**Q: How much RAM is used?**
A:

- Headless: ~200-300MB per browser
- Headed: ~300-500MB per browser

**Q: Is there a session limit?**
A: No hard limit, but depends on your machine's RAM. Recommended: 5-10 concurrent sessions.

## 🔒 About Security

**Q: Is MCP Server safe?**
A: Yes. MCP Server:

- Runs locally on your machine
- Doesn't send data anywhere
- Open source, code can be audited

**Q: Does it send data to cloud?**
A: No. Unless you use cloud AI (Claude, ChatGPT), then AI will receive:

- Your requests
- Test results (if you ask AI to analyze)

**Q: Can test internal websites?**
A: Yes. MCP Server runs locally, can test:

- localhost
- Internal network
- VPN

**Q: Will credentials be leaked?**
A: No, if you:

- Don't share screenshots with credentials
- Don't log credentials
- Use environment variables for sensitive data

## 💰 About Cost

**Q: Does MCP Server charge?**
A: No. MCP Server is free.

**Q: Does AI service charge?**
A:

- **Claude**: Yes (pay-as-you-go or Pro plan)
- **ChatGPT**: Yes (Plus plan or API)
- **Gemini**: Has free tier, then charges

**Q: Approximately how much does AI cost?**
A: Depends on usage:

- Light usage (few tests/day): ~$5-10/month
- Medium usage (many tests/day): ~$20-50/month
- Heavy usage (CI/CD): ~$100+/month

**Q: Any way to reduce cost?**
A:

- Use local AI models (free but less capable)
- Optimize prompts to reduce tokens
- Cache results for reuse

## 🚀 About Future

**Q: Will MCP Server be updated?**
A: Yes. Project is actively maintained and regularly updated.

**Q: Is there a roadmap?**
A: Yes. Features in development:

- Visual regression testing
- AI-powered bug detection
- Auto-healing tests
- More integrations

**Q: Can I contribute?**
A: Yes! Project is open source, contributions welcome.

## 📚 Additional Documentation

**Q: Is documentation complete?**
A: There are 6 documentation files:

1. [README.md](./README.md) - Overview
2. [01-introduction.md](./01-introduction.md) - Introduction
3. [02-installation.md](./02-installation.md) - Installation
4. [03-usage.md](./03-usage.md) - Usage
5. [04-features.md](./04-features.md) - Features
6. [05-troubleshooting.md](./05-troubleshooting.md) - Troubleshooting

**Q: Are there video tutorials?**
A: Not yet. In the plans.

**Q: Is there a community?**
A: Yes. Join Discord/Slack for Q&A and sharing experiences.

---

**Back to**: [README](./README.md)
