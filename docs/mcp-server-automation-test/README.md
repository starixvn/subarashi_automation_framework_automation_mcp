# MCP Server - Browser Testing Automation

## 🎯 What is MCP Server?

**MCP Server** is a tool that enables AI (like Claude, ChatGPT) to **control web browsers** for automated website testing.

**Simple example**:

- You tell AI: "Go to the login page and test the login functionality"
- AI will automatically: open browser → enter username/password → click Login → check results

## ✨ Why Do You Need MCP Server?

### Before MCP Server

❌ Must write test code manually  
❌ Time-consuming setup  
❌ Difficult to maintain when website changes

### With MCP Server

✅ AI automatically writes and runs tests  
✅ Just describe in natural language  
✅ AI automatically adapts when website changes

## 📚 Documentation Structure

Documentation is divided into 6 concise, easy-to-understand parts:

1. **[01-introduction.md](./01-introduction.md)** - What is MCP Server and how it works
2. **[02-installation.md](./02-installation.md)** - Step-by-step installation guide
3. **[03-usage.md](./03-usage.md)** - How to use with Claude Desktop and n8n
4. **[04-features.md](./04-features.md)** - Main features and examples
5. **[05-troubleshooting.md](./05-troubleshooting.md)** - Common error handling
6. **[06-faq.md](./06-faq.md)** - Frequently asked questions

## 🚀 Quick Start

### Step 1: Installation

```bash
# Clone code
git clone <repository-url>
cd mcp-server-automation-framework

# Install dependencies with UV
uv sync

# Install Playwright browsers
uv run playwright install chromium
```

### Step 2: Run Server

```bash
# Run with Claude Desktop (stdio)
uv run main.py --transport stdio --headless

# Run with SSE (default port 8000)
uv run main.py --transport sse
```

### Step 3: Usage

**With Claude Desktop**: Talk to Claude normally, Claude will automatically use MCP Server to test websites.

**With n8n**: Create workflow, add MCP Client node, connect to server.

## 💡 Usage Examples

### Example 1: Test Login

**You tell AI**:

```
Test the login page at https://example.com/login
- Username: testuser
- Password: testpass123
- Check if it redirects to dashboard
```

**AI will automatically**:

1. Open browser and go to URL
2. Enter username and password
3. Click Login button
4. Check if URL redirects to /dashboard
5. Report results

### Example 2: Test Form

**You tell AI**:

```
Test registration form at https://example.com/register
Check validation for fields:
- Invalid email
- Password too short
- Confirm password doesn't match
```

**AI will automatically test all cases** and report results.

## 🎁 Benefits

### For QA Engineers

- ✅ Save time writing test cases
- ✅ AI automatically detects bugs
- ✅ Easy to test multiple scenarios

### For Developers

- ✅ Quickly verify fixes
- ✅ Automated regression testing
- ✅ Easy CI/CD integration

### For Teams

- ✅ No deep programming knowledge required
- ✅ Test documentation automatically created
- ✅ Easy to share and collaborate

## ⚙️ System Requirements

- **Python**: 3.11 or higher
- **UV**: Package manager (install at https://docs.astral.sh/uv/)
- **RAM**: Minimum 4GB
- **Disk**: ~500MB for Playwright browsers
- **OS**: Windows, macOS, or Linux

## 🔗 Integrations

MCP Server can integrate with:

- ✅ **Claude Desktop**: Use directly in chat
- ✅ **n8n**: Integrate into workflow automation
- ✅ **Custom AI**: Any AI that supports MCP Protocol

## 📞 Support

If you encounter issues:

1. See [05-troubleshooting.md](./05-troubleshooting.md) for troubleshooting
2. See [06-faq.md](./06-faq.md) for frequently asked questions
3. Contact support team

---

**Get Started**: [01 - Introduction](./01-introduction.md)
