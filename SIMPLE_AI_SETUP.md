# 🤖 CONNECT AI AGENT TO YOUR WORDPRESS MCP SERVER

## Simple Step-by-Step Guide

---

## **UNDERSTANDING IN SIMPLE WORDS** 🎯

Imagine you have:

- **Your MCP Server** = A translator
- **WordPress** = A library
- **Claude AI** = A smart assistant

The conversation works like this:

```
You: "Show me my posts"
     ↓
Claude: "I need to ask the translator to get posts from the library"
     ↓
Claude sends message to MCP Server
     ↓
MCP Server: "Got it! Let me get posts from WordPress"
     ↓
WordPress: "Here are the posts" [sends data]
     ↓
MCP Server: "Got the posts, sending to Claude..."
     ↓
Claude: "Here are your posts!" [shows you the real data]
```

**That's it!** Your MCP Server is the middleman between Claude and WordPress.

---

## **EASY METHOD: USE CLAUDE DESKTOP** ✅ (RECOMMENDED)

### **Step 1: Download Claude Desktop**

1. Go to: https://claude.ai/download
2. Click "Download"
3. Install it like any other app
4. Open Claude Desktop

### **Step 2: Open Configuration File**

**On Windows:**

1. Open **File Explorer**
2. Copy this path to the address bar:
   ```
   C:\Users\Admin\AppData\Roaming\Claude
   ```
3. You should see a folder named "Claude"
4. Inside, look for: `claude_desktop_config.json`
5. If it doesn't exist, create a new text file and name it: `claude_desktop_config.json`
6. Open it with **Notepad** (right-click → Open with → Notepad)

### **Step 3: Add Your MCP Server**

Copy and paste this into the file:

```json
{
  "mcpServers": {
    "wordpress": {
      "command": "python",
      "args": ["C:\\Users\\Admin\\Desktop\\assignment\\mcp_server.py"]
    }
  }
}
```

**Important:** Make sure:

- The path `C:\\Users\\Admin\\Desktop\\assignment\\mcp_server.py` is correct
- Every `{` has a matching `}`
- All commas are in the right place (no comma after the last item)

### **Step 4: Save the File**

1. Press **Ctrl + S** to save
2. Close the file

### **Step 5: Restart Claude Desktop**

1. Close Claude Desktop completely
2. Wait 5 seconds
3. Open Claude Desktop again
4. It will now have your WordPress tools!

---

## **BEFORE YOU TEST: START YOUR SERVER** ⚡

1. Open **PowerShell** or **Command Prompt**
2. Navigate to your assignment folder:

   ```powershell
   cd "C:\Users\Admin\Desktop\assignment"
   ```

3. Start the server:

   ```powershell
   python mcp_server.py
   ```

4. You should see:

   ```
   ✅ Configuration loaded successfully!
   🚀 WordPress MCP Server Starting...
   📻 Listening for AI agent connections on stdio...
   ✅ Server is ready! Waiting for requests...
   ```

5. **IMPORTANT: Keep this window open!** The server must keep running.

---

## **NOW TEST YOUR AI AGENT** 🧪

1. Open Claude Desktop
2. Start a new conversation
3. Type one of these messages:

### **Test 1: List Posts**

```
Show me all WordPress posts from my blog
```

**Expected:** Claude shows real posts from your WordPress site

### **Test 2: Create a Post**

```
Create a new WordPress post titled "Test Post" with content "This is a test"
```

**Expected:** Claude creates the post and confirms it

### **Test 3: Check Plugins**

```
What plugins do I have on my WordPress site?
```

**Expected:** Claude lists your real plugins

### **Test 4: Check Site Health**

```
Tell me about my WordPress site - what version is it running? Any health issues?
```

**Expected:** Claude shows version info, PHP version, etc.

### **Test 5: List Users**

```
Who are the users on my WordPress site?
```

**Expected:** Claude lists users and their roles

---

## **HOW TO KNOW IT'S WORKING** ✅

### **Sign 1: Real Data**

When Claude responds, does it have REAL data from YOUR WordPress?

- Real post titles? ✅
- Real plugin names? ✅
- Real user information? ✅

If YES → It's working!

### **Sign 2: Server Shows Activity**

Look at the terminal where you ran `python mcp_server.py`:

- Does it show any messages?
- Is there activity?

If YES → Data is flowing through!

### **Sign 3: Claude Acknowledges Tools**

Does Claude say things like:

- "I'll check your WordPress..."
- "Let me access your WordPress site..."
- "I'll create that post for you..."

If YES → Claude is using your tools!

---

## **COMMON PROBLEMS & FIXES** 🔧

### **Problem: "Claude doesn't know about WordPress tools"**

**Fix:**

1. Check if server is running in terminal
   - Look for: `✅ Server is ready! Waiting for requests...`
   - If not visible, start it: `python mcp_server.py`

2. Check config file path is EXACTLY correct
   - Open: `C:\Users\Admin\AppData\Roaming\Claude\claude_desktop_config.json`
   - Make sure path points to: `C:\Users\Admin\Desktop\assignment\mcp_server.py`

3. Restart Claude completely
   - Close it
   - Wait 5 seconds
   - Open again

---

### **Problem: "Server error when I ask Claude about WordPress"**

**Fix:**

1. Kill the server: Press **Ctrl + C** in the terminal
2. Wait 2 seconds
3. Start it again: `python mcp_server.py`
4. Try again in Claude

---

### **Problem: "Authentication failed" error**

**Fix:**

1. Check `.env` file exists in: `C:\Users\Admin\Desktop\assignment\.env`
2. It should contain:

   ```
   WORDPRESS_URL=https://myblog12367.wordpress.com
   WORDPRESS_USERNAME=Abdullah Jameel
   WORDPRESS_PASSWORD=kg!BRrCj%uk@ZM3yRcFK@whV
   WORDPRESS_HTTPS=true
   ```

3. Test config by running:
   ```powershell
   python config.py
   ```
   Should show: `✅ Configuration loaded successfully!`

---

## **WHAT YOU CAN DO NOW** 🎉

Your AI agent (Claude) can now:

1. **List Posts** - "Show me all my WordPress posts"
2. **Create Posts** - "Write a new post about..."
3. **Manage Plugins** - "Activate/deactivate plugin..."
4. **List Users** - "Who has access to my WordPress?"
5. **Check Site Health** - "Is my WordPress site healthy?"

---

## **COMPLETE WORKFLOW EXAMPLE** 📋

```
1. Open Terminal
   → cd C:\Users\Admin\Desktop\assignment
   → python mcp_server.py
   [Terminal shows: Server is ready!]
   [KEEP THIS WINDOW OPEN]

2. Open Claude Desktop
   → Start new conversation
   → Type: "List my WordPress posts"
   → Claude connects to your server
   → Your server gets WordPress data
   → Claude shows you the posts
   → SUCCESS! ✅
```

---

## **DEBUGGING CHECKLIST** ✓

Before asking for help, check:

- [ ] Server is running: `python mcp_server.py`
- [ ] Server shows: `📡 Connected to MCP client`
- [ ] Config file exists and has correct path
- [ ] Claude Desktop is closed and reopened
- [ ] `.env` file has correct credentials
- [ ] Testing with Claude Desktop (not web version)

---

## **NEXT STEPS AFTER IT WORKS** 🚀

Once you confirm it's working:

1. **Use it for real tasks**
   - Let Claude manage your WordPress from chat
   - Create posts, manage plugins, check users

2. **Add more tools** (optional)
   - Add more WordPress functions to `wordpress_api.py`
   - Register them as tools in `mcp_server.py`

3. **Deploy it** (optional)
   - Run on a server
   - Connect multiple clients
   - Use in production

---

## **YOU'RE ALL SET!** 🎊

Your WordPress MCP server is:

- ✅ Created
- ✅ Configured
- ✅ Tested
- ✅ Ready to connect to AI agents

Now go **talk to Claude** and watch your WordPress server in action!

**Questions?** Check the troubleshooting section above or review the detailed guide in `AI_AGENT_CONNECTION_GUIDE.py`
