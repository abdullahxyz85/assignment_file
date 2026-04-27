# WordPress MCP Server - Complete Assignment Solution

A Python-based MCP (Model Context Protocol) server that allows AI agents to manage WordPress sites via REST API.

---

## 📋 PROJECT STRUCTURE

```
assignment/
├── requirements.txt          # All Python packages needed
├── .env.example              # Template for credentials (copy to .env)
├── .env                      # Your actual credentials (NEVER commit!)
├── config.py                 # Loads & validates credentials
├── wordpress_api.py          # WordPress REST API wrapper
├── mcp_server.py             # Main MCP server with tools
└── README.md                 # This file
```

---

## 🎯 WHAT EACH FILE DOES

### 1️⃣ **requirements.txt**

Lists all Python packages your server needs.

**What each package does:**

- `mcp` - The MCP server framework that communicates with AI agents
- `httpx` - Makes HTTPS requests to WordPress
- `pydantic` - Validates data types
- `python-dotenv` - Reads credentials from .env file

**Installation:**

```bash
pip install -r requirements.txt
```

---

### 2️⃣ **.env (Your Credentials - KEEP SECRET!)**

**DON'T commit this file to Git!**

Create `.env` file from `.env.example`:

```
WORDPRESS_URL=https://yourdomain.com
WORDPRESS_USERNAME=your_admin_username
WORDPRESS_PASSWORD=your_app_password_here
WORDPRESS_HTTPS=true
```

**Getting WordPress App Password:**

1. Go to WordPress Admin → Users → Your Profile
2. Scroll to "Application Passwords"
3. Enter app name (e.g., "MCP Server")
4. Generate password
5. Copy and paste into .env

---

### 3️⃣ **config.py** - Configuration Module

**What it does:**

- Loads credentials from .env file
- Creates authentication headers (Base64 encoded)
- Validates all required settings
- Provides API endpoint URLs

**Key Functions:**

```python
# Loads environment variables
load_dotenv()

# Gets credentials
WORDPRESS_URL = os.getenv("WORDPRESS_URL")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")

# Creates Base64 auth header
get_auth_header() -> {"Authorization": "Basic YWRtaW46YXBwcGFzcw=="}

# Validates all settings are set
validate_config() -> Raises error if anything missing
```

**Authentication Flow:**

```
admin:mypassword
    ↓
Base64 encode
    ↓
YWRtaW46bXlwYXNzd29yZA==
    ↓
Authorization: Basic YWRtaW46bXlwYXNzd29yZA==
    ↓
Sent in HTTP header to WordPress
```

---

### 4️⃣ **wordpress_api.py** - WordPress API Wrapper

**What it does:**

- Provides functions to interact with WordPress REST API
- Handles all HTTP requests
- Formats responses nicely
- Error handling

**Functions:**

#### **Posts Management**

```python
# Get posts
await list_posts(per_page=10, status="publish")
# Returns: [{"id": 1, "title": "Hello", "content": "...", "status": "publish"}]

# Create post
await create_post(title="My Post", content="Content here", status="draft")
# Returns: {"id": 2, "title": "My Post", "status": "draft"}
```

#### **Plugins Management**

```python
# List all plugins
await list_plugins()
# Returns: [{"name": "Akismet", "slug": "akismet", "status": "active"}]

# Manage plugin
await manage_plugin(plugin_slug="akismet", action="activate")
# Returns: {"plugin": "akismet", "action": "activated", "success": True}
```

#### **Users**

```python
# Get all users
await list_users()
# Returns: [{"id": 1, "name": "Admin", "email": "admin@example.com", "roles": ["administrator"]}]
```

#### **Site Stats**

```python
# Get site information
await get_site_stats()
# Returns: {
#   "wordpress_version": "6.4",
#   "php_version": "8.1",
#   "health_status": "good"
# }
```

**How API Requests Work:**

```python
# Example: Making a request to WordPress
async def make_request(method, endpoint, data=None):
    url = f"{WORDPRESS_API_BASE}{endpoint}"
    # "https://mysite.com/wp-json/wp/v2/posts"

    headers = get_auth_header()
    # {"Authorization": "Basic YWRtaW46YXBwcGFzcw==", "Content-Type": "application/json"}

    response = await client.request(method, url, headers=headers, json=data)
    return response.json()
```

---

### 5️⃣ **mcp_server.py** - Main MCP Server

**What it does:**

- Listens for AI agent connections
- Defines 5 available tools
- Handles tool calls
- Returns results to AI agents

**The 5 Available Tools:**

```python
# Tool 1: List Posts
{
  "name": "list_posts",
  "parameters": {"per_page": 10, "status": "publish"}
}

# Tool 2: Create Post
{
  "name": "create_post",
  "parameters": {"title": "...", "content": "...", "status": "draft"}
}

# Tool 3: Manage Plugins
{
  "name": "manage_plugins",
  "parameters": {"action": "list|activate|deactivate|delete", "plugin_slug": "akismet"}
}

# Tool 4: List Users
{
  "name": "list_users",
  "parameters": {} // No parameters needed
}

# Tool 5: Site Stats
{
  "name": "get_site_stats",
  "parameters": {} // No parameters needed
}
```

**How the Server Works:**

```
1. Start Server
   └─→ Validates config
   └─→ Starts listening on stdio
   └─→ Waits for AI agent connection

2. AI Agent Connects
   └─→ Asks "What tools do you have?"
   └─→ Server responds: list_posts, create_post, manage_plugins, list_users, get_site_stats

3. AI Selects Tool
   └─→ Sends: {"tool": "list_posts", "arguments": {"per_page": 5}}
   └─→ Server receives the request

4. Server Processes
   └─→ Calls: await list_posts(per_page=5)
   └─→ WordPress API returns posts
   └─→ Format result

5. Return to AI
   └─→ Server sends: {"success": True, "posts": [...]}
   └─→ AI agent uses the data
```

---

## 🚀 HOW TO RUN

### **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 2: Create .env File**

Copy `.env.example` to `.env` and fill in your WordPress credentials:

```
WORDPRESS_URL=https://yoursite.com
WORDPRESS_USERNAME=admin
WORDPRESS_PASSWORD=your_app_password
WORDPRESS_HTTPS=true
```

### **Step 3: Start the Server**

```bash
python mcp_server.py
```

You should see:

```
🚀 WordPress MCP Server Starting...
📻 Listening for AI agent connections on stdio...
✅ Server is ready! Waiting for requests...
```

### **Step 4: Connect an AI Agent**

In your AI client (like Claude), configure it to use this MCP server on stdio.

---

## 📝 DETAILED CODE EXPLANATIONS

### **Understanding Authentication**

```python
# Step 1: Combine username and password
credentials = f"admin:myapppassword"

# Step 2: Convert to bytes
credentials_bytes = credentials.encode()
# Result: b'admin:myapppassword'

# Step 3: Base64 encode
encoded_bytes = base64.b64encode(credentials_bytes)
# Result: b'YWRtaW46bXlhcHBwYXNzd29yZA=='

# Step 4: Convert back to string
encoded_string = encoded_bytes.decode()
# Result: "YWRtaW46bXlhcHBwYXNzd29yZA=="

# Step 5: Create header
header = {"Authorization": f"Basic {encoded_string}"}
# Result: {"Authorization": "Basic YWRtaW46bXlhcHBwYXNzd29yZA=="}

# Step 6: Send with request
response = await client.request("GET", url, headers=header)
```

Why Base64?

- It's a standard for HTTP Basic Authentication
- Encodes credentials in a format WordPress expects
- **NOT encryption** (don't use over plain HTTP!)
- Always use HTTPS with authentication

---

### **Understanding Async/Await**

```python
# Regular function (blocks)
def fetch_data():
    result = api_call()  # Waits here until done
    return result

# Async function (doesn't block)
async def fetch_data():
    result = await api_call()  # Waits, but other code can run
    return result

# How to call async function
await fetch_data()  # Must use await

# Running async code
asyncio.run(main())  # Starts the async runtime
```

Why use async?

- Multiple AI agents can make requests at same time
- Server doesn't freeze waiting for WordPress
- Better performance

---

### **Understanding MCP Tools Definition**

```python
# This is what we define:
tool = types.Tool(
    name="list_posts",                    # Unique identifier
    description="Get all WordPress posts",  # Shown to AI agent
    inputSchema={                         # Parameters format
        "type": "object",
        "properties": {
            "per_page": {
                "type": "integer",
                "description": "Number of posts",
                "default": 10
            },
            "status": {
                "type": "string",
                "description": "Filter by status",
                "default": "publish"
            }
        }
    }
)

# AI agent sees this and can call it like:
# "Use list_posts with per_page=5"
# Server receives: {"name": "list_posts", "arguments": {"per_page": 5}}
```

---

### **Understanding WordPress API Endpoints**

```python
# Base API URL
https://yoursite.com/wp-json/wp/v2

# Posts endpoint
GET /posts              # List posts
GET /posts/123          # Get post with ID 123
POST /posts             # Create new post
PUT /posts/123          # Update post
DELETE /posts/123       # Delete post

# Plugins endpoint
GET /plugins            # List plugins
PUT /plugins/akismet    # Activate/deactivate plugin
DELETE /plugins/akismet # Delete plugin

# Users endpoint
GET /users              # List users

# Settings endpoint
GET /settings           # Get site settings
```

---

## 🧪 TESTING EXAMPLES

### **Test 1: List Posts**

```
AI Request: "List 5 published posts"

Server does:
1. Calls: await list_posts(per_page=5, status="publish")
2. Makes HTTPS request to WordPress
3. Formats response
4. Returns to AI

AI Receives:
{
  "success": True,
  "count": 5,
  "posts": [
    {"id": 1, "title": "Hello World", "status": "publish"},
    ...
  ]
}
```

### **Test 2: Create Post**

```
AI Request: "Create a draft post titled 'New Article' with content 'This is my article'"

Server does:
1. Validates title and content provided
2. Calls: await create_post(title="New Article", content="This is my article", status="draft")
3. Sends POST request to WordPress
4. Returns new post info

AI Receives:
{
  "success": True,
  "message": "Post created successfully!",
  "post": {
    "id": 123,
    "title": "New Article",
    "status": "draft",
    "link": "https://yoursite.com/?p=123"
  }
}
```

### **Test 3: Manage Plugin**

```
AI Request: "Activate the Akismet plugin"

Server does:
1. Validates action="activate" and plugin_slug="akismet"
2. Calls: await manage_plugin(plugin_slug="akismet", action="activate")
3. Sends PUT request to WordPress
4. Returns result

AI Receives:
{
  "success": True,
  "message": "Plugin activated successful!",
  "result": {"plugin": "akismet", "action": "activated", "success": True}
}
```

---

## 🔐 SECURITY CHECKLIST

- ✅ Credentials stored in .env (not in code)
- ✅ .env not committed to Git
- ✅ Using HTTPS (enforced)
- ✅ Using Base64 authentication
- ✅ Using Application Passwords (not regular password)
- ✅ Validating all inputs
- ✅ Error handling for failed requests

---

## 🐛 TROUBLESHOOTING

### **Error: "Missing configuration: WORDPRESS_URL"**

- Make sure .env file exists
- All fields filled in
- Run: `python config.py` to validate

### **Error: "401 Unauthorized"**

- Check WordPress credentials
- Verify app password is correct
- Make sure user has admin privileges

### **Error: "Connection refused"**

- Check WORDPRESS_URL is correct
- Make sure HTTPS is enabled
- Check internet connection

### **Error: "timeout"**

- WordPress server is slow
- Check internet connection
- Increase timeout in config.py

---

## 📚 KEY CONCEPTS SUMMARY

| Concept              | Explanation                                         |
| -------------------- | --------------------------------------------------- |
| **MCP**              | Protocol for AI agents to use external tools        |
| **REST API**         | Interface to interact with WordPress remotely       |
| **OAuth/Basic Auth** | Method to authenticate requests (we use Basic Auth) |
| **Base64**           | Encoding method for credentials                     |
| **Async/Await**      | Allows multiple requests simultaneously             |
| **Tool Definition**  | Describes what parameters a tool accepts            |
| **Tool Call**        | When AI asks server to use a tool                   |

---

## 🎓 LEARNING OUTCOMES

After completing this assignment, you understand:

1. ✅ How MCP servers work
2. ✅ How to authenticate with REST APIs
3. ✅ How to make async HTTP requests
4. ✅ How to define tools for AI agents
5. ✅ How to handle errors gracefully
6. ✅ How to structure a Python project
7. ✅ Security best practices for credentials

---

## 📞 QUICK REFERENCE

**Start server:**

```bash
python mcp_server.py
```

**Install packages:**

```bash
pip install -r requirements.txt
```

**Check configuration:**

```bash
python config.py
```

**5 Available Tools:**

1. `list_posts` - Get WordPress posts
2. `create_post` - Create new post
3. `manage_plugins` - Control plugins
4. `list_users` - Get WordPress users
5. `get_site_stats` - Site information

---

## 📄 FILE DEPENDENCIES

```
mcp_server.py
  ├─ imports config.py (credentials & validation)
  ├─ imports wordpress_api.py (all API functions)
  └─ uses MCP framework

wordpress_api.py
  ├─ imports config.py (authentication headers)
  └─ uses httpx (HTTP requests)

config.py
  └─ uses python-dotenv (load .env)

.env
  └─ loaded by config.py
```

---

**You now have a complete, production-ready WordPress MCP Server! 🎉**
