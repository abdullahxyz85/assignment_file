# Testing Guide - WordPress MCP Server

This guide shows you how to test each component step-by-step.

---

## 📋 PRE-TESTING SETUP

### 1. Install Dependencies

```bash
cd c:\Users\Admin\Desktop\assignment
pip install -r requirements.txt
```

### 2. Create .env File

Copy `.env.example` to `.env` and fill in your WordPress credentials:

```bash
copy .env.example .env
```

Then edit `.env` with your values:

```
WORDPRESS_URL=https://yourdomain.com
WORDPRESS_USERNAME=your_admin_username
WORDPRESS_PASSWORD=your_app_password
WORDPRESS_HTTPS=true
```

### 3. Verify Installation

```bash
python -c "import mcp; import httpx; import pydantic; print('All imports OK!')"
```

---

## 🧪 TEST 1: Configuration

**What to test:** Is the configuration loading correctly?

**Test File:** `test_config.py`

```python
# Create file: test_config.py

from config import (
    WORDPRESS_URL,
    WORDPRESS_USERNAME,
    WORDPRESS_PASSWORD,
    WORDPRESS_API_BASE,
    get_auth_header,
    validate_config
)

# Test 1: Are variables loaded?
print("🔍 Test 1: Loading Variables")
print(f"WordPress URL: {WORDPRESS_URL}")
print(f"Username: {WORDPRESS_USERNAME}")
print(f"API Base: {WORDPRESS_API_BASE}")

# Test 2: Is auth header correct?
print("\n🔍 Test 2: Authentication Header")
header = get_auth_header()
print(f"Auth Header: {header}")
assert "Authorization" in header, "❌ Authorization header missing!"
print("✅ Auth header looks good!")

# Test 3: Validate config
print("\n🔍 Test 3: Config Validation")
try:
    validate_config()
    print("✅ Configuration is valid!")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

**Run it:**

```bash
python test_config.py
```

---

## 🧪 TEST 2: WordPress API Connection

**What to test:** Can we connect to WordPress and retrieve data?

**Test File:** `test_wordpress_api.py`

```python
# Create file: test_wordpress_api.py

import asyncio
from wordpress_api import (
    list_posts,
    list_plugins,
    list_users,
    get_site_stats,
    close
)

async def test_all():
    """Test all WordPress API functions"""

    # Test 1: Get Posts
    print("🔍 Test 1: Retrieving Posts")
    try:
        posts = await list_posts(per_page=3)
        print(f"✅ Retrieved {len(posts)} posts")
        for post in posts[:2]:
            print(f"   - {post['title']} (ID: {post['id']})")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 2: Get Plugins
    print("\n🔍 Test 2: Retrieving Plugins")
    try:
        plugins = await list_plugins()
        print(f"✅ Retrieved {len(plugins)} plugins")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: Get Users
    print("\n🔍 Test 3: Retrieving Users")
    try:
        users = await list_users()
        print(f"✅ Retrieved {len(users)} users")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 4: Get Site Stats
    print("\n🔍 Test 4: Retrieving Site Stats")
    try:
        stats = await get_site_stats()
        print(f"✅ Site Stats Retrieved")
    except Exception as e:
        print(f"❌ Error: {e}")

    await close()
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_all())
```

**Run it:**

```bash
python test_wordpress_api.py
```

---

## 🧪 TEST 3: MCP Server

**Run the server:**

```bash
python mcp_server.py
```

**Expected Output:**

```
🚀 WordPress MCP Server Starting...
📻 Listening for AI agent connections on stdio...
✅ Configuration loaded successfully!
✅ Server is ready! Waiting for requests...
```

---

## ✅ TESTING COMPLETE

When all tests pass, your WordPress MCP Server is ready to use!
