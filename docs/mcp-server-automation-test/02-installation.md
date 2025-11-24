# 02 - Installation Guide

## 📋 Prerequisites

### 1. Python 3.11+

**Check Python**:

```bash
python --version
```

If not installed or version < 3.11, download from: https://www.python.org/downloads/

### 2. UV Package Manager

**UV** is a Python package manager (much faster than pip).

**Install UV**:

**Windows (PowerShell)**:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Check UV**:

```bash
uv --version
```

### 3. Git

To clone source code.

**Check Git**:

```bash
git --version
```

If not installed, download from: https://git-scm.com/downloads

## 🚀 Install MCP Server

### Step 1: Clone Source Code

```bash
# Clone repository
git clone <repository-url>

# Go to project directory
cd mcp-server-automation-framework
```

### Step 2: Install Dependencies

```bash
# Install all dependencies with UV
uv sync
```

**Note**: First run will take ~2-3 minutes to download all packages.

### Step 3: Install Playwright Browsers

```bash
# Install Chromium (recommended)
uv run playwright install chromium

# Or install all browsers
uv run playwright install
```

**Note**: Each browser ~100-200MB, choose browsers you need to test.

### Step 4: Verify Installation

```bash
# Test run server
uv run main.py --help
```

If you see help message → Installation successful! ✅

## ⚙️ Configuration

### Configure For Claude Desktop

**Step 1**: Find Claude Desktop config file

**Windows**:

```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS**:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux**:

```
~/.config/Claude/claude_desktop_config.json
```

**Step 2**: Add config to file

```json
{
  "mcpServers": {
    "browser-automation": {
      "command": "uv",
      "args": [
        "--directory",
        "D:/path/to/mcp-server-automation-framework",
        "run",
        "main.py",
        "--transport",
        "stdio",
        "--headless"
      ]
    }
  }
}
```

**Note**: Replace `D:/path/to/mcp-server-automation-framework` with actual path on your machine.

**Step 3**: Restart Claude Desktop

Close and reopen Claude Desktop to load new config.

**Step 4**: Verify

In Claude Desktop, type:

```
Can you control the browser?
```

If Claude answers "Yes" or lists tools → Success! ✅

### Configure For n8n

**Step 1**: Run MCP Server with SSE transport

```bash
# Default port 8000
uv run main.py --transport sse

# Or specify different port
uv run main.py --transport sse --port 8000
```

**Step 2**: In n8n workflow

1. Add **"MCP Client"** node
2. Configure:
   - **SSE Endpoint**: `http://localhost:8000/sse`
   - **Tools**: Select tools you need (or leave "All")

**Step 3**: Test connection

Run workflow, check if node can connect.

## 🔧 Configuration Options

### Run With Browser Display (Not Headless)

```bash
# Remove --headless flag to see browser
uv run main.py --transport stdio
```

### Choose Different Browser

```bash
# Use Firefox
uv run main.py --transport stdio --browser firefox

# Use Chrome
uv run main.py --transport stdio --browser chrome

# Use WebKit (Safari)
uv run main.py --transport stdio --browser webkit
```

### Change Port (For SSE)

```bash
# Default is port 8000, can change
uv run main.py --transport sse --port 3000
```

### Enable Only Some Capabilities

```bash
# Only enable core and vision tools
uv run main.py --transport stdio --caps core,vision
```

**Available capabilities**:

- `core`: Navigate, click, type, hover...
- `vision`: Screenshot, snapshot
- `tabs`: Tab management
- `console`: View console logs
- `keyboard`: Keyboard input
- `network`: Monitor network requests
- `files`: File operations
- `wait`: Wait strategies
- `api`: API testing
- `google_sheets`: Google Sheets integration
- `database`: Database operations

## 🐛 Troubleshooting

### Error: "uv: command not found"

**Cause**: UV not installed or not added to PATH.

**Solution**:

1. Reinstall UV following instructions above
2. Restart terminal/PowerShell
3. Check again: `uv --version`

### Error: "Python version mismatch"

**Cause**: Python version < 3.11

**Solution**:

1. Install Python 3.11+ from python.org
2. Run again: `uv sync`

### Error: "Playwright browsers not found"

**Cause**: Playwright browsers not installed.

**Solution**:

```bash
uv run playwright install chromium
```

### Error: "Port already in use"

**Cause**: Port 8000 (default) already used by another app.

**Solution**:

```bash
# Use different port
uv run main.py --transport sse --port 5002
```

### Claude Desktop Doesn't Recognize MCP Server

**Check**:

1. Is path in config correct?
2. Have you restarted Claude Desktop?
3. Try running server manually: `uv run main.py --transport stdio`

**View logs**:

- Windows: `%APPDATA%\Claude\logs\`
- macOS: `~/Library/Logs/Claude/`

## ✅ Post-Installation Checklist

- [ ] Python 3.11+ installed
- [ ] UV installed and working
- [ ] `uv sync` completed successfully
- [ ] Playwright browsers installed
- [ ] `uv run main.py --help` shows help
- [ ] (If using Claude) Config file added
- [ ] (If using Claude) Claude Desktop restarted
- [ ] (If using Claude) Claude recognizes MCP tools

---

**Next**: [03 - Usage](./03-usage.md)
