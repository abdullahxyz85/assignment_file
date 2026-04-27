# Architecture & Flow Diagrams

Understanding the complete flow of the WordPress MCP Server.

---

## 1. 📐 PROJECT STRUCTURE DIAGRAM

```
assignment/
│
├── requirements.txt
│   └─ Lists all packages needed
│      (mcp, httpx, pydantic, python-dotenv)
│
├── .env.example
│   └─ Template for credentials
│      Copy to .env before running
│
├── .env (KEEP SECRET!)
│   └─ Your actual WordPress credentials
│      NEVER commit to Git!
│
├── .gitignore
│   └─ Prevents committing .env and other files
│
├── config.py
│   ├─ Loads .env file
│   ├─ Creates auth headers
│   ├─ Validates credentials
│   └─ Provides API endpoints
│
├── wordpress_api.py
│   ├─ HTTP client initialization
│   ├─ Generic make_request() function
│   ├─ list_posts() & create_post()
│   ├─ list_plugins() & manage_plugin()
│   ├─ list_users()
│   └─ get_site_stats()
│
├── mcp_server.py (MAIN FILE)
│   ├─ Initialize MCP Server
│   ├─ @server.list_tools() - Define 5 tools
│   ├─ @server.call_tool() - Handle tool calls
│   └─ main() - Start server
│
├── README.md
│   └─ Complete documentation
│
├── TESTING_GUIDE.md
│   └─ How to test everything
│
└── ARCHITECTURE_DIAGRAMS.md (this file)
    └─ Visual explanations
```

---

## 2. 🔄 REQUEST/RESPONSE FLOW

```
┌─────────────────────────────────────────────────────────────┐
│ AI AGENT (Claude, ChatGPT, etc.)                            │
│ "Get me all posts and list plugins"                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ (Step 1: Send MCP Request)
                   │ {"tool": "list_posts", "arguments": {...}}
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ MCP SERVER (mcp_server.py)                                  │
│                                                              │
│ Step 2: Receive request                                     │
│ Step 3: Validate parameters                                │
│ Step 4: Call wordpress_api.list_posts()                    │
│                                                              │
│ Step 5: Wait for response from WordPress                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ (Step 6: HTTPS Request with Auth Header)
                   │ GET /wp-json/wp/v2/posts
                   │ Authorization: Basic YWRtaW46YXBw...
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ WORDPRESS REST API                                          │
│ (yoursite.com/wp-json)                                      │
│                                                              │
│ Step 7: Authenticate credentials                            │
│ Step 8: Fetch posts from database                          │
│ Step 9: Format as JSON                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ (Step 10: JSON Response)
                   │ [
                   │   {"id": 1, "title": "Hello World", ...},
                   │   {"id": 2, "title": "My Post", ...}
                   │ ]
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ MCP SERVER (wordpress_api.py)                               │
│                                                              │
│ Step 11: Parse response                                     │
│ Step 12: Format nicely                                      │
│ Step 13: Return to MCP                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ (Step 14: Send MCP Result)
                   │ {
                   │   "success": true,
                   │   "count": 2,
                   │   "posts": [...]
                   │ }
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ AI AGENT receives result                                    │
│ Uses data for next action                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 🔐 AUTHENTICATION FLOW

```
┌──────────────────────────────────────────────────────────┐
│ .env File (Your Credentials)                             │
│                                                           │
│ WORDPRESS_URL=https://mysite.com                         │
│ WORDPRESS_USERNAME=admin                                 │
│ WORDPRESS_PASSWORD=abc123xyz789                          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ config.py loads credentials
                       ↓
┌──────────────────────────────────────────────────────────┐
│ Step 1: Combine credentials                              │
│ "admin:abc123xyz789"                                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ Python: .encode()
                       │ Converts string to bytes
                       ↓
┌──────────────────────────────────────────────────────────┐
│ Step 2: Bytes form                                        │
│ b'admin:abc123xyz789'                                    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ Python: base64.b64encode()
                       │ Encodes to Base64
                       ↓
┌──────────────────────────────────────────────────────────┐
│ Step 3: Base64 encoded                                   │
│ b'YWRtaW46YWJjMTIzeHl6Nzg5'                             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ Python: .decode()
                       │ Converts bytes to string
                       ↓
┌──────────────────────────────────────────────────────────┐
│ Step 4: Final auth string                                │
│ "YWRtaW46YWJjMTIzeHl6Nzg5"                              │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ Add to HTTP header
                       ↓
┌──────────────────────────────────────────────────────────┐
│ Step 5: HTTP Header                                       │
│ {                                                         │
│   "Authorization": "Basic YWRtaW46YWJjMTIzeHl6Nzg5",   │
│   "Content-Type": "application/json"                     │
│ }                                                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ Send to WordPress
                       ↓
┌──────────────────────────────────────────────────────────┐
│ WordPress REST API                                       │
│ Decodes Base64                                           │
│ Gets: "admin:abc123xyz789"                               │
│ Verifies credentials                                     │
│ Grants access if valid                                   │
└──────────────────────────────────────────────────────────┘
```

---

## 4. 🛠️ MCP TOOL DEFINITION & CALL

```
┌────────────────────────────────────────────────────────────┐
│ list_tools() Function in mcp_server.py                      │
│                                                             │
│ Defines 5 Tools:                                            │
│                                                             │
│ Tool 1: list_posts                                          │
│   ├─ Name: "list_posts"                                    │
│   ├─ Description: "Get WordPress posts"                    │
│   └─ Parameters: per_page (int), status (string)           │
│                                                             │
│ Tool 2: create_post                                         │
│   ├─ Name: "create_post"                                   │
│   ├─ Description: "Create new post"                        │
│   └─ Parameters: title (required), content (required),     │
│                  status (optional)                          │
│                                                             │
│ Tool 3: manage_plugins                                      │
│   ├─ Name: "manage_plugins"                                │
│   ├─ Description: "List or manage plugins"                 │
│   └─ Parameters: action (required), plugin_slug (optional) │
│                                                             │
│ Tool 4: list_users                                          │
│   ├─ Name: "list_users"                                    │
│   └─ Description: "Get WordPress users"                    │
│                                                             │
│ Tool 5: get_site_stats                                      │
│   └─ Description: "Get site health & stats"                │
└────────────────────────────────────────────────────────────┘
                        │
                        │ When AI connects:
                        │ "What tools do you have?"
                        ↓
┌────────────────────────────────────────────────────────────┐
│ Server Responds:                                            │
│ [                                                           │
│   {name: "list_posts", description: "..."},               │
│   {name: "create_post", description: "..."},              │
│   {name: "manage_plugins", description: "..."},           │
│   {name: "list_users", description: "..."},               │
│   {name: "get_site_stats", description: "..."}            │
│ ]                                                           │
└────────────────────────────────────────────────────────────┘
                        │
                        │ AI selects tool
                        │ "Use list_posts with per_page=5"
                        ↓
┌────────────────────────────────────────────────────────────┐
│ call_tool() Function                                        │
│                                                             │
│ Receives:                                                   │
│   name = "list_posts"                                      │
│   arguments = {"per_page": 5, "status": "publish"}        │
│                                                             │
│ Step 1: Check if name == "list_posts" ✓                   │
│ Step 2: Extract per_page = 5, status = "publish"          │
│ Step 3: Call: await list_posts(per_page=5, status=...)    │
│ Step 4: Get result from WordPress                          │
│ Step 5: Format as dict with success=true                   │
│ Step 6: Return to AI agent                                 │
└────────────────────────────────────────────────────────────┘
                        │
                        │ Server Returns:
                        │ {
                        │   "success": true,
                        │   "count": 5,
                        │   "posts": [...]
                        │ }
                        ↓
┌────────────────────────────────────────────────────────────┐
│ AI Agent uses the result                                    │
└────────────────────────────────────────────────────────────┘
```

---

## 5. 📞 ASYNC REQUEST HANDLING

```
┌─────────────────────────────────────────────────────────┐
│ Multiple Concurrent Requests (Why async matters)         │
└─────────────────────────────────────────────────────────┘

Time →

Request 1 (list_posts):     ░░░░████████░░░░░ Response
Request 2 (create_post):        ░░░░████████░░░░░ Response
Request 3 (list_users):             ░░░░████████░░░░░ Response

Without async (blocking):
Request 1:  ████████ → Wait for response
Request 2:          ████████ → Wait for response
Request 3:                  ████████ → Wait for response
(Total time = sum of all requests)

With async (non-blocking):
Request 1:  ░░░░████████░░░░░
Request 2:      ░░░░████████░░░░░  (runs while 1 waits)
Request 3:          ░░░░████████░░░░░  (runs while 1,2 wait)
(Total time = longest request only)
```

---

## 6. 📊 DATA FLOW THROUGH MODULES

```
┌──────────────────────────────────────────────────────────┐
│ User/AI Agent Request                                     │
│ "Create a post titled 'Hello' with content 'World'"      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────┐
│ mcp_server.py                                             │
│ call_tool("create_post", {                                │
│   "title": "Hello",                                       │
│   "content": "World"                                      │
│ })                                                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────┐
│ wordpress_api.py                                          │
│ await create_post(                                        │
│   title="Hello",                                          │
│   content="World",                                        │
│   status="draft"                                          │
│ )                                                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────┐
│ config.py provides:                                       │
│ - URL: "https://site.com/wp-json/wp/v2"                 │
│ - Headers: {Authorization: "Basic ..."}                  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────┐
│ HTTPS Request Sent:                                       │
│ POST https://site.com/wp-json/wp/v2/posts               │
│ Headers: {Authorization: ..., Content-Type: json}        │
│ Body: {title: "Hello", content: "World", status: draft} │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────┐
│ WordPress Creates Post                                    │
│ Stores in database                                        │
│ Returns: {id: 123, title: "Hello", ...}                 │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────┐
│ wordpress_api.py formats response                         │
│ Returns: {id: 123, title: "Hello", status: "draft"}     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────┐
│ mcp_server.py wraps result                                │
│ Returns: {                                                │
│   success: true,                                          │
│   message: "Post created successfully!",                │
│   post: {id: 123, title: "Hello", status: "draft"}      │
│ }                                                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌──────────────────────────────────────────────────────────┐
│ AI Agent receives result                                  │
│ Shows success message with post ID                        │
└──────────────────────────────────────────────────────────┘
```

---

## 7. 🔍 ERROR HANDLING FLOW

```
┌──────────────────────────────────────────────────────────┐
│ Request Sent to WordPress                                 │
└──────────────────────┬──────────────────────────────────┘
                       │
            ┌──────────┴──────────┐
            │                      │
            ↓                      ↓
    ┌──────────────────┐  ┌──────────────────┐
    │ Success          │  │ Error            │
    │ (200-299)        │  │ (400+, network)  │
    └────────┬─────────┘  └─────────┬────────┘
             │                      │
             ↓                      ↓
    ┌──────────────────┐  ┌──────────────────┐
    │ Parse JSON       │  │ Catch Exception  │
    │ Extract data     │  │ Log error        │
    │ Format response  │  │ Return error msg │
    └────────┬─────────┘  └─────────┬────────┘
             │                      │
             ↓                      ↓
    ┌──────────────────┐  ┌──────────────────┐
    │ Return:          │  │ Return:          │
    │ {                │  │ {                │
    │   success: true, │  │   success: false,│
    │   data: [...]    │  │   error: "..."   │
    │ }                │  │ }                │
    └──────────────────┘  └──────────────────┘
             │                      │
             └──────────┬───────────┘
                        │
                        ↓
            ┌──────────────────────┐
            │ AI Agent Receives    │
            │ Either way gets      │
            │ structured response  │
            └──────────────────────┘
```

---

## 8. 🚀 SERVER STARTUP SEQUENCE

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: User runs: python mcp_server.py                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Import all modules                              │
│ - config.py (loads .env)                                │
│ - wordpress_api.py (initializes HTTP client)            │
│ - MCP framework                                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Run main() async function                       │
│ - Call validate_config()                                │
│   └─ Check all credentials present                      │
│   └─ Print error if missing                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Print startup messages                          │
│ "🚀 WordPress MCP Server Starting..."                  │
│ "📻 Listening for AI agent connections..."             │
│ "✅ Server is ready! Waiting for requests..."          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Start MCP server                                │
│ async with server: ← Block here listening               │
│   await server.wait() ← Wait for connections            │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴──────────┐
         │                      │
         ↓                      ↓
   ┌──────────────┐      ┌─────────────┐
   │ AI connects  │      │ User stops  │
   │ Server ready │      │ (Ctrl+C)    │
   │ for requests │      │             │
   └──────────────┘      └──────┬──────┘
                                │
                                ↓
                        ┌──────────────────┐
                        │ Print message:   │
                        │ "❌ Server       │
                        │ stopped by user" │
                        │                  │
                        │ Close connection:│
                        │ await close_api()│
                        └──────────────────┘
```

---

This visualization helps you understand the complete architecture and flow of the WordPress MCP Server!
