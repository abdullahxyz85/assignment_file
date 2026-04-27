# ⚡ QUICK START GUIDE - Get Running in 5 Minutes!

Complete beginner? Start here!

---

## 🎯 OBJECTIVE

Build a Python server that lets AI agents control WordPress via REST API.

---

## 📋 WHAT YOU HAVE

All files are already created! Here they are:

```
c:\Users\Admin\Desktop\assignment\
├── requirements.txt          ✅
├── .env.example              ✅
├── .env (create this!)
├── config.py                 ✅
├── wordpress_api.py          ✅
├── mcp_server.py             ✅
├── README.md                 ✅
├── BEGINNERS_GUIDE.md        ✅
├── ARCHITECTURE_DIAGRAMS.md  ✅
├── TESTING_GUIDE.md          ✅
└── QUICK_START.md            ✅ (this file)
```

---

## ⏱️ 5-MINUTE SETUP

### **Minute 1: Install Packages**

Open PowerShell in `c:\Users\Admin\Desktop\assignment\` and run:

```powershell
pip install -r requirements.txt
```

**What this does:** Downloads all Python packages needed

---

### **Minute 2: Create .env File**

Copy the template:

```powershell
copy .env.example .env
```

**Now edit `.env` file with your WordPress info:**

```
WORDPRESS_URL=https://yourdomain.com
WORDPRESS_USERNAME=admin
WORDPRESS_PASSWORD=your_app_password_here
WORDPRESS_HTTPS=true
```

**How to get WordPress App Password:**

1. Go to: `https://yourdomain.com/wp-admin`
2. Click: `Users` → `Your Profile`
3. Scroll to: `Application Passwords`
4. Type app name: `MCP Server`
5. Click: `Generate`
6. Copy the password
7. Paste into `.env` file

---

### **Minute 3: Test Configuration**

Run this to verify settings:

```powershell
python config.py
```

**Expected output:**

```
✅ Configuration loaded successfully!
WordPress URL: https://yourdomain.com
API Base: https://yourdomain.com/wp-json/wp/v2
Configuration is ready!
```

**If you see error:** Check your `.env` file (URL, username, password)

---

### **Minute 4: Start the Server**

Run:

```powershell
python mcp_server.py
```

**Expected output:**

```
🚀 WordPress MCP Server Starting...
📻 Listening for AI agent connections on stdio...
✅ Configuration loaded successfully!
✅ Server is ready! Waiting for requests...
```

**Leave this running!** Don't close the window.

---

### **Minute 5: Use with AI Agent**

In your AI client (Claude, ChatGPT, etc.):

- Configure MCP server
- Point to stdio (standard input/output)
- Select this server

**Now send requests like:**

- "Get all published posts"
- "Create a draft post"
- "List all plugins"
- "Show me all users"
- "Get site statistics"

---

## 📖 WHAT EACH FILE DOES

| File                       | Purpose                  | Edit?        |
| -------------------------- | ------------------------ | ------------ |
| `requirements.txt`         | Python packages list     | ❌ No        |
| `.env.example`             | Credentials template     | ❌ No        |
| `.env`                     | Your actual credentials  | ✅ **YES**   |
| `.gitignore`               | Don't upload these files | ❌ No        |
| `config.py`                | Load & verify settings   | ❌ No        |
| `wordpress_api.py`         | Talk to WordPress        | ❌ No        |
| `mcp_server.py`            | Main server (run this!)  | ❌ No        |
| `README.md`                | Full documentation       | ℹ️ Reference |
| `BEGINNERS_GUIDE.md`       | Concepts explained       | ℹ️ Reference |
| `ARCHITECTURE_DIAGRAMS.md` | Visual explanations      | ℹ️ Reference |
| `TESTING_GUIDE.md`         | How to test              | ℹ️ Reference |

---

## 🛠️ THE 5 TOOLS YOUR SERVER PROVIDES

When AI connects, it can use these 5 tools:

### **Tool 1: list_posts**

Get all blog posts

**Example:**

```
AI: "Get 5 published posts"
Server: Returns 5 latest posts with title, content, date
```

### **Tool 2: create_post**

Create a new blog post

**Example:**

```
AI: "Create draft post titled 'Hello' with content 'World'"
Server: Creates post, returns new post ID
```

### **Tool 3: manage_plugins**

List or control plugins

**Example:**

```
AI: "List all plugins"
Server: Shows all plugins with active/inactive status

AI: "Activate Akismet plugin"
Server: Activates plugin
```

### **Tool 4: list_users**

Get all WordPress users

**Example:**

```
AI: "Show all users"
Server: Lists all users with names, emails, roles
```

### **Tool 5: get_site_stats**

Get site information

**Example:**

```
AI: "Get site statistics"
Server: Shows WordPress version, PHP version, health status
```

---

## 🔒 SECURITY REMINDERS

✅ **DO:**

- Keep `.env` file secret
- Use strong app passwords
- Always use HTTPS (WordPress_HTTPS=true)
- Add `.env` to `.gitignore` (already done!)
- Only share code, never credentials

❌ **DON'T:**

- Commit `.env` to Git
- Share `.env` file
- Use regular WordPress password
- Use plain HTTP (HTTP_HTTPS=false)
- Hardcode passwords in code

---

## 🐛 QUICK TROUBLESHOOTING

### **"pip: command not found"**

```
Python not installed or not in PATH
1. Install Python from python.org
2. Make sure "Add to PATH" is checked during install
3. Restart PowerShell
```

### **"ModuleNotFoundError: No module named 'mcp'"**

```
Packages not installed
1. Run: pip install -r requirements.txt
2. Wait for completion
3. Try again
```

### **"401 Unauthorized"**

```
Wrong credentials
1. Check WORDPRESS_USERNAME in .env
2. Check WORDPRESS_PASSWORD in .env
3. Verify user has admin privileges
4. Regenerate app password from WordPress
```

### **"Connection refused"**

```
Can't connect to WordPress
1. Check WORDPRESS_URL is correct
2. Make sure HTTPS is enabled (true in .env)
3. Check internet connection
4. Verify WordPress is online
```

### **"Server doesn't respond"**

```
Server crashed
1. Check PowerShell for error messages
2. Stop server (Ctrl+C)
3. Fix error
4. Restart: python mcp_server.py
```

---

## 📚 LEARNING PATH

**Already know Python?**

1. ✅ Skip BEGINNERS_GUIDE.md
2. ✅ Read README.md
3. ✅ Read ARCHITECTURE_DIAGRAMS.md
4. ✅ Start using!

**New to Python?**

1. ✅ Read BEGINNERS_GUIDE.md (explains concepts)
2. ✅ Read ARCHITECTURE_DIAGRAMS.md (visual explanations)
3. ✅ Read README.md (detailed reference)
4. ✅ Read TESTING_GUIDE.md (practice)
5. ✅ Start using!

**Want to modify code?**

1. ✅ Read BEGINNERS_GUIDE.md
2. ✅ Understand each file
3. ✅ Read comments in the code
4. ✅ Test changes with TESTING_GUIDE.md

---

## 🎓 KEY CONCEPTS (30-Second Version)

**MCP Server** = A program that gives AI access to tools

- AI asks: "What can you do?"
- Server responds: "I can list posts, create posts, etc."

**WordPress REST API** = A way to control WordPress via internet

- Like WordPress admin, but for programs instead of people

**Base64 Authentication** = Secure way to send passwords

- Username:Password → Encode → Send to WordPress

**Async/Await** = Code that handles multiple requests at once

- Multiple AI agents can use server simultaneously

**Tools** = Functions the AI can call

- list_posts, create_post, manage_plugins, list_users, get_site_stats

---

## ✅ VERIFICATION CHECKLIST

Before using with AI:

- [ ] Installed packages: `pip install -r requirements.txt`
- [ ] Created `.env` file
- [ ] Filled in WORDPRESS_URL
- [ ] Filled in WORDPRESS_USERNAME
- [ ] Filled in WORDPRESS_PASSWORD (app password, not regular password)
- [ ] Set WORDPRESS_HTTPS=true
- [ ] Tested config: `python config.py` (no errors)
- [ ] Server starts: `python mcp_server.py` (shows ✅ ready)
- [ ] Server doesn't crash
- [ ] All 5 tools available

---

## 🚀 YOU'RE READY!

**Congratulations!** Your WordPress MCP Server is set up and ready to use!

**Next steps:**

1. Keep server running: `python mcp_server.py`
2. Connect AI agent to it
3. Send requests
4. Watch the magic happen! ✨

---

## 📞 REFERENCE QUICK LINKS

**Need help understanding?**

- Concepts: See `BEGINNERS_GUIDE.md`
- Visual flow: See `ARCHITECTURE_DIAGRAMS.md`
- Full docs: See `README.md`
- Testing: See `TESTING_GUIDE.md`
- This file: `QUICK_START.md`

**For each Python file:**

- Every line has comments explaining what it does
- Open the file and read the comments!

---

## 💬 COMMON QUESTIONS

**Q: Can I modify the code?**
A: Yes! Each file is well-commented. Change and test.

**Q: Can I add more tools?**
A: Yes! Add functions to `wordpress_api.py` and tools in `mcp_server.py`.

**Q: Can I use this in production?**
A: Yes! But add error logging and rate limiting first.

**Q: Do I need to know Python?**
A: Not really! Comments explain everything.

**Q: Can I use different AI agents?**
A: Yes! Any AI that supports MCP protocol.

**Q: Is my data safe?**
A: Yes! Uses HTTPS encryption and app passwords.

---

**You're all set! Happy coding! 🎉**
