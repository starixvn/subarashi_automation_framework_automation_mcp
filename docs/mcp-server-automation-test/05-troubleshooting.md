# 05 - Common Error Handling

## 🔧 Installation Errors

### Error 1: "uv: command not found"

**Symptoms**:

```bash
$ uv --version
uv: command not found
```

**Cause**:

- UV not installed
- UV not added to PATH

**Solution**:

**Windows**:

```powershell
# Install UV
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Restart PowerShell
# Check again
uv --version
```

**macOS/Linux**:

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.cargo/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc

# Check again
uv --version
```

### Error 2: "Python version mismatch"

**Symptoms**:

```
Error: Python 3.10 found, but 3.11+ required
```

**Cause**:
Python version too old.

**Solution**:

1. Download Python 3.11+ from https://www.python.org/downloads/
2. Install
3. Check: `python --version`
4. Run again: `uv sync`

### Error 3: "Playwright browsers not installed"

**Symptoms**:

```
Error: Executable doesn't exist at /path/to/chromium
```

**Cause**:
Playwright browsers not installed.

**Solution**:

```bash
# Install Chromium
uv run playwright install chromium

# Or install all browsers
uv run playwright install
```

### Error 4: "Permission denied"

**Symptoms** (Windows):

```
Error: Access denied when installing
```

**Solution**:

- Run PowerShell/CMD **as Administrator**
- Or install to user directory (no admin needed)

**Symptoms** (macOS/Linux):

```
Error: Permission denied
```

**Solution**:

```bash
# Add sudo
sudo uv sync

# Or fix permissions
chmod +x /path/to/script
```

## 🚀 Server Running Errors

### Error 5: "Port already in use"

**Symptoms**:

```
Error: Address already in use: 0.0.0.0:8000
```

**Cause**:
Port 8000 (default) already used by another app.

**Solution**:

**Method 1**: Use different port

```bash
uv run main.py --transport sse --port 5002
```

**Method 2**: Kill process using port

**Windows**:

```powershell
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

**macOS/Linux**:

```bash
# Find and kill
lsof -ti:8000 | xargs kill -9
```

### Error 6: "Module not found"

**Symptoms**:

```
ModuleNotFoundError: No module named 'playwright'
```

**Cause**:
Dependencies not installed.

**Solution**:

```bash
# Reinstall dependencies
uv sync

# Check
uv run python -c "import playwright; print('OK')"
```

### Error 7: "Browser launch failed"

**Symptoms**:

```
Error: Failed to launch browser
```

**Cause**:

- Missing system dependencies (Linux)
- Antivirus blocking (Windows)

**Solution**:

**Linux**:

```bash
# Install dependencies
sudo apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2
```

**Windows**:

- Temporarily disable antivirus
- Or add exception for Playwright

## 🔌 Connection Errors

### Error 8: Claude Desktop Doesn't Recognize MCP Server

**Symptoms**:
Claude doesn't list MCP tools when asked.

**Check**:

**Step 1**: Check config file

**Windows**:

```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS**:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Ensure config is correct:

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

**Step 2**: Check path

Ensure path in config is **absolute path** and **exists**.

**Step 3**: Test manual run

```bash
cd D:/path/to/mcp-server-automation-framework
uv run main.py --transport stdio --headless
```

If runs → Config wrong
If doesn't run → Fix server error first

**Step 4**: View logs

**Windows**:

```
%APPDATA%\Claude\logs\mcp*.log
```

**macOS**:

```
~/Library/Logs/Claude/mcp*.log
```

**Step 5**: Restart Claude Desktop

Completely close Claude Desktop and reopen.

### Error 9: n8n Cannot Connect

**Symptoms**:
MCP Client node reports connection error.

**Check**:

**Step 1**: Is server running?

```bash
# Check
curl http://localhost:8000/sse
```

If no response → Server not running

**Step 2**: Is port correct?

Ensure:

- Server running port 8000 (default): `uv run main.py --transport sse`
- n8n config endpoint: `http://localhost:8000/sse`

**Step 3**: Firewall

Check if firewall is blocking port 8000.

**Windows**:

```powershell
# Allow port
netsh advfirewall firewall add rule name="MCP Server" dir=in action=allow protocol=TCP localport=8000
```

## 🐛 Testing Errors

### Error 10: "Element not found"

**Symptoms**:

```
Error: Element not found: button.login
```

**Cause**:

- Element not loaded yet
- Wrong selector
- Element hidden

**Solution**:

**Method 1**: Wait for element to appear

```
Wait for button.login to appear, then click
```

**Method 2**: Use different selector

```
Click button with text "Login"
```

**Method 3**: Check if element is visible

```
Take screenshot to see if element is displayed
```

### Error 11: "Timeout waiting for element"

**Symptoms**:

```
Error: Timeout 30000ms exceeded waiting for selector
```

**Cause**:

- Page loads slowly
- Element doesn't exist
- Wrong selector

**Solution**:

**Method 1**: Increase timeout

```
Wait for element with 60 second timeout
```

**Method 2**: Wait for network idle

```
Navigate and wait for network idle
```

**Method 3**: Debug

```
Take screenshot to see current page
Get HTML to check selector
```

### Error 12: "Click intercepted"

**Symptoms**:

```
Error: Element is not clickable, another element would receive the click
```

**Cause**:

- Element covered by another element (modal, overlay)
- Element scrolled out of viewport

**Solution**:

**Method 1**: Close modal/overlay first

```
Click X button to close modal
Then click the button you need
```

**Method 2**: Scroll to element

```
Scroll to button, then click
```

**Method 3**: Force click

```
Force click button (skip visibility check)
```

### Error 13: "Navigation timeout"

**Symptoms**:

```
Error: Navigation timeout of 30000ms exceeded
```

**Cause**:

- Website loads slowly
- Slow network
- Website error

**Solution**:

**Method 1**: Increase timeout

```
Navigate with 60 second timeout
```

**Method 2**: Wait for different load event

```
Navigate and wait for "domcontentloaded" instead of "load"
```

**Method 3**: Check network

```
Check network requests to see which request is stuck
```

## 💡 Debugging Tips

### Tip 1: Run Without Headless

```bash
# Remove --headless flag to see browser
uv run main.py --transport stdio
```

You'll see browser open and watch AI work.

### Tip 2: Screenshot Every Step

```
After each action, take screenshot for debugging
```

### Tip 3: View Console Logs

```
Get console logs of page
```

### Tip 4: View Network Requests

```
Monitor network requests to see which APIs are called
```

### Tip 5: Slow Down

```
Add 1 second delay between each action for easier tracking
```

## 📞 When to Contact Support?

If you've tried everything above and still have errors:

1. **Collect information**:

   - Full error message
   - Steps to reproduce
   - Screenshots
   - Logs

2. **Check again**:

   - Python version: `python --version`
   - UV version: `uv --version`
   - OS version
   - Config files

3. **Contact support**:
   - Send information above
   - Describe problem in detail
   - What you've tried

---

**Next**: [06 - FAQ](./06-faq.md)
