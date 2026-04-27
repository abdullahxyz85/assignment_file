"""
AI AGENT CONNECTION GUIDE
==========================

This guide explains how to connect an AI agent (like Claude) to your WordPress MCP server
and make it actually work!
"""

# ============================================================
# PART 1: UNDERSTANDING HOW IT WORKS
# ============================================================

"""
SIMPLE EXPLANATION (for beginners):

Think of it like this:

    [AI Agent - Claude]
            |
            | (sends JSON-RPC messages on stdin/stdout)
            |
            v
    [MCP Server - Your server]
            |
            | (reads requests, calls WordPress)
            |
            v
    [WordPress API]
            |
            | (returns data)
            |
            v
    [Back to AI Agent]
    (AI now has the data and can use it)


HOW THE CONVERSATION WORKS:

1. User: "Show me all WordPress posts"
   ↓
2. Claude AI: "I need to use the 'list_posts' tool"
   ↓
3. Claude sends JSON message: {"method": "tools/call", "params": {"name": "list_posts"}}
   ↓
4. Your MCP Server: "Receives message → Calls list_posts() → Gets posts from WordPress"
   ↓
5. Server sends response: {"result": [list of posts]}
   ↓
6. Claude AI: "Got the posts! Here they are for the user..."
"""

# ============================================================
# PART 2: 3 WAYS TO CONNECT YOUR AI AGENT
# ============================================================

"""
METHOD 1: USE CLAUDE DESKTOP (RECOMMENDED) ✅
================================================

Claude Desktop is the easiest way to use your MCP server!

STEP 1: Download Claude Desktop
  - Go to https://claude.ai/download
  - Download and install Claude Desktop
  - Launch the application

STEP 2: Find the configuration file
  - On Windows: Open this file in Notepad:
    C:\Users\%USERNAME%\AppData\Roaming\Claude\claude_desktop_config.json
    
    (Replace %USERNAME% with your actual username, e.g., Admin)
    
    Full path: C:\Users\Admin\AppData\Roaming\Claude\claude_desktop_config.json

STEP 3: Add your MCP server to the config
  - Copy this text and paste it into the file:
  
{
  "mcpServers": {
    "wordpress": {
      "command": "python",
      "args": [
        "C:\\Users\\Admin\\Desktop\\assignment\\mcp_server.py"
      ]
    }
  }
}

STEP 4: Save the file and restart Claude Desktop
  - Save (Ctrl+S)
  - Close Claude Desktop completely
  - Open Claude Desktop again
  - It will now have access to your WordPress tools!

STEP 5: Test it!
  - Type to Claude: "What WordPress posts do I have?"
  - Claude will automatically use your MCP server to check!


METHOD 2: USE VS CODE WITH MCP EXTENSION
==========================================

STEP 1: Install the MCP Client extension in VS Code
  - Open VS Code
  - Go to Extensions (Ctrl+Shift+X)
  - Search for "MCP"
  - Install "MCP Client" extension

STEP 2: Configure the extension
  - Open settings (Ctrl+,)
  - Search for "MCP"
  - Add your server configuration

STEP 3: Connect to your server
  - Use the extension to connect to localhost:stdio
  - Select your mcp_server.py file
  - The extension will show you available tools


METHOD 3: USE COMMAND LINE (ADVANCED)
======================================

If you're using an AI CLI tool or custom client:

python mcp_server.py

Then connect your AI client to the server on stdin/stdout.

The AI client needs to send JSON-RPC 2.0 messages like:

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "my-ai-client",
      "version": "1.0"
    }
  }
}
"""

# ============================================================
# PART 3: HOW TO VERIFY IT'S WORKING
# ============================================================

"""
SIGNS THAT YOUR MCP SERVER IS CONNECTED:

✅ 1. Claude shows a "tools" indicator
   - When MCP server is connected, Claude shows a small tool icon
   - You'll see it in the chat interface

✅ 2. Claude mentions using your tools
   - When Claude needs info from WordPress, it will say:
   - "I'll check your WordPress posts..."
   - "Let me access your WordPress site..."

✅ 3. You get WordPress data in the response
   - Claude responds with actual data from your WordPress site
   - Not generic/made-up responses

✅ 4. Server console shows activity
   - Look at your terminal running "python mcp_server.py"
   - You should see messages flowing through


TESTING STEPS:

1. Start your server (keep it running):
   C:\Users\Admin\Desktop\assignment> python mcp_server.py
   
   You should see:
   ✅ Configuration loaded successfully!
   🚀 WordPress MCP Server Starting...
   📻 Listening for AI agent connections on stdio...
   ✅ Server is ready! Waiting for requests...
   📡 Connected to MCP client

2. Open Claude Desktop (or your AI client)

3. Test with these messages:

   Test 1: "List all my WordPress posts"
   Expected: Claude shows your actual posts from WordPress
   
   Test 2: "Create a new WordPress post titled 'Hello World'"
   Expected: Claude creates the post (you can check WordPress)
   
   Test 3: "What WordPress plugins do I have?"
   Expected: Claude lists your plugins
   
   Test 4: "Tell me about WordPress users on my site"
   Expected: Claude lists users with their roles

4. Check the response:
   - Is the data real (from your WordPress site)?
   - Or is it generic/made up?
   - If real → Server is working! ✅
"""

# ============================================================
# PART 4: EXAMPLE CONVERSATIONS
# ============================================================

"""
EXAMPLE 1: List Posts
======================

You: "What posts do I have on my WordPress blog?"

Claude: 
"I'll check your WordPress blog for you.
[Claude uses MCP to call: list_posts()]

You have the following posts:
1. "Welcome to My Blog" - Published
2. "Getting Started" - Draft
3. "My First Post" - Published

[Shows real data from your WordPress site]"


EXAMPLE 2: Create a Post
=========================

You: "Create a post titled 'Amazing Discovery' with content 'This is amazing!'"

Claude:
"I'll create that post for you now.
[Claude uses MCP to call: create_post(title=..., content=..., status=...)]

✅ Post created successfully!
- Title: Amazing Discovery
- Status: Draft (saved as draft)
- You can publish it from WordPress dashboard"


EXAMPLE 3: Manage Plugins
==========================

You: "Do I have the Akismet plugin? If so, activate it"

Claude:
"Let me check your plugins.
[Claude uses MCP to call: list_plugins()]

I found Akismet! Let me activate it.
[Claude uses MCP to call: manage_plugin(plugin_slug='akismet', action='activate')]

✅ Akismet is now activated!"


EXAMPLE 4: Get Site Info
=========================

You: "Tell me about my WordPress site health"

Claude:
"I'll get your site information.
[Claude uses MCP to call: get_site_stats()]

Your WordPress Site:
- WordPress Version: 6.4.1
- PHP Version: 8.0.0
- MySQL Version: 5.7.0
- Site Health: Good ✅
- Total Posts: 15
- Total Users: 3"
"""

# ============================================================
# PART 5: TROUBLESHOOTING
# ============================================================

"""
PROBLEM 1: "Claude doesn't recognize my tools"
===============================================

CAUSE: MCP server not properly connected

FIX:
1. Check if mcp_server.py is running in terminal
   - If not, start it: python mcp_server.py
   - Keep terminal open while using Claude

2. Verify configuration file
   - Check C:\Users\Admin\AppData\Roaming\Claude\claude_desktop_config.json
   - Make sure path is correct
   - Make sure JSON syntax is valid (no missing commas/brackets)

3. Restart Claude Desktop
   - Close it completely
   - Wait 5 seconds
   - Open again


PROBLEM 2: "Server error: Connection failed"
==============================================

CAUSE: Port issues or server not responding

FIX:
1. Check if server is still running
   - Look at terminal - should show no errors
   - Should say "Connected to MCP client"

2. Kill any existing processes
   - Press Ctrl+C in the server terminal
   - Wait 2 seconds
   - Start again: python mcp_server.py

3. Check firewall
   - Windows Firewall might be blocking
   - Try disabling it temporarily


PROBLEM 3: "WordPress authentication failed"
=============================================

CAUSE: Wrong credentials or .env file missing

FIX:
1. Check .env file exists
   - Look for: C:\Users\Admin\Desktop\assignment\.env
   - Should contain WordPress credentials

2. Verify credentials
   - Username: Abdullah Jameel (or your actual username)
   - Password: Application password (not regular password)
   - URL: https://myblog12367.wordpress.com

3. Test config
   - Run: python config.py
   - Should show: "✅ Configuration loaded successfully!"


PROBLEM 4: "AI not using my tools / Just making up responses"
==============================================================

CAUSE: MCP server not connected to AI client

FIX:
1. Verify server terminal shows activity
   - Run python mcp_server.py
   - Look for messages when you interact with Claude

2. Check configuration again
   - Path must be exact and correct
   - No typos in file path

3. Restart everything
   - Close Claude
   - Kill server (Ctrl+C)
   - Start server again
   - Open Claude again
"""

# ============================================================
# PART 6: QUICK REFERENCE
# ============================================================

"""
QUICK SETUP CHECKLIST:

□ Server created and tested ✅ (Done)
□ WordPress credentials working ✅ (Done)
□ MCP dependencies installed ✅ (Done)
□ Server runs without errors ✅ (Done)

Now do these:

□ Step 1: Download Claude Desktop from https://claude.ai/download
□ Step 2: Find config file: 
           C:\Users\Admin\AppData\Roaming\Claude\claude_desktop_config.json
□ Step 3: Add MCP server config (see METHOD 1 above)
□ Step 4: Save and restart Claude Desktop
□ Step 5: Start MCP server: python mcp_server.py (keep running)
□ Step 6: Ask Claude about WordPress in chat
□ Step 7: Watch as Claude uses your WordPress tools!


5 COMMANDS TO TEST:

1. "List all my WordPress posts"
2. "Create a test post called 'Hello World'"
3. "What plugins do I have installed?"
4. "Show me my WordPress users"
5. "Is my WordPress site healthy? Tell me the details"
"""

print(__doc__)
