"""
PRACTICAL TEST SCRIPT
====================

This script tests if your MCP server and WordPress connection are working correctly.

Run this: python test_setup.py
"""

import subprocess
import json
import sys
import time
from pathlib import Path


def print_header(text):
    """Print a fancy header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_success(text):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"❌ {text}")


def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")


def test_files_exist():
    """Test if all required files exist"""
    print_header("TEST 1: Checking Required Files")
    
    files = {
        "mcp_server.py": "Main MCP server",
        "config.py": "Configuration handler",
        "wordpress_api.py": "WordPress API wrapper",
        ".env": "Credentials file",
        "requirements.txt": "Python dependencies",
    }
    
    all_exist = True
    for filename, description in files.items():
        path = Path(filename)
        if path.exists():
            print_success(f"{filename} - {description}")
        else:
            print_error(f"{filename} - {description} [MISSING!]")
            all_exist = False
    
    return all_exist


def test_config():
    """Test if configuration loads correctly"""
    print_header("TEST 2: Testing WordPress Configuration")
    
    try:
        from config import validate_config, WORDPRESS_API_BASE, WORDPRESS_USERNAME
        
        # Test validation
        validate_config()
        print_success("Configuration validation passed")
        print_info(f"  WordPress URL: {WORDPRESS_API_BASE}")
        print_info(f"  Username: {WORDPRESS_USERNAME}")
        return True
        
    except Exception as e:
        print_error(f"Configuration test failed: {e}")
        return False


def test_imports():
    """Test if all imports work"""
    print_header("TEST 3: Testing Python Imports")
    
    imports = {
        "mcp": "MCP Framework",
        "httpx": "HTTP Client",
        "pydantic": "Data Validation",
        "python-dotenv": "Environment Variables",
    }
    
    all_ok = True
    for module, description in imports.items():
        try:
            __import__(module)
            print_success(f"{module} - {description}")
        except ImportError as e:
            print_error(f"{module} - {description} [Failed: {e}]")
            all_ok = False
    
    return all_ok


def test_wordpress_connection():
    """Test WordPress API connection"""
    print_header("TEST 4: Testing WordPress API Connection")
    
    try:
        import asyncio
        from wordpress_api import list_posts
        
        print_info("Attempting to connect to WordPress...")
        
        async def test():
            posts = await list_posts(per_page=1, status="publish")
            return posts
        
        posts = asyncio.run(test())
        print_success(f"WordPress connection successful!")
        print_info(f"  Found {len(posts)} posts")
        if posts:
            print_info(f"  Latest post: {posts[0].get('title', 'N/A')}")
        return True
        
    except Exception as e:
        print_error(f"WordPress connection failed: {e}")
        print_info("Make sure:")
        print_info("  1. .env file has correct WordPress credentials")
        print_info("  2. Your WordPress site is online")
        print_info("  3. Application password is set correctly")
        return False


def test_mcp_server_startup():
    """Test if MCP server can start"""
    print_header("TEST 5: Testing MCP Server Startup")
    
    print_info("Starting server (will run for 3 seconds)...")
    
    try:
        # Start server with timeout
        process = subprocess.Popen(
            [sys.executable, "mcp_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let it run for 3 seconds
        time.sleep(3)
        
        # Check if still running
        if process.poll() is None:
            print_success("Server started and is running")
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            stdout, stderr = process.communicate()
            print_error(f"Server crashed: {stderr}")
            return False
            
    except Exception as e:
        print_error(f"Server startup test failed: {e}")
        return False


def show_summary(results):
    """Show test results summary"""
    print_header("TEST SUMMARY")
    
    tests = [
        ("Files exist", results.get("files", False)),
        ("Config loads", results.get("config", False)),
        ("Imports work", results.get("imports", False)),
        ("WordPress API", results.get("wordpress", False)),
        ("MCP Server", results.get("server", False)),
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("ALL TESTS PASSED! Your setup is ready! ✨")
        print("\nNext steps:")
        print("  1. Keep 'python mcp_server.py' running in a terminal")
        print("  2. Open Claude Desktop")
        print("  3. Ask about WordPress (e.g., 'Show my posts')")
        return True
    else:
        print_error("Some tests failed. Fix issues above before connecting AI agents.")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         WORDPRESS MCP SERVER - SETUP TEST SCRIPT          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    results = {}
    
    # Run tests
    results["files"] = test_files_exist()
    results["config"] = test_config()
    results["imports"] = test_imports()
    results["wordpress"] = test_wordpress_connection()
    results["server"] = test_mcp_server_startup()
    
    # Show summary
    success = show_summary(results)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
