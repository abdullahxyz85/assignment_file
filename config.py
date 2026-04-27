"""
Configuration Module for WordPress MCP Server
==============================================
This file loads credentials from .env file and provides them to the server.
Think of it as the "settings" for the entire application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This reads the .env file and makes variables accessible via os.environ
load_dotenv()

# ============================================
# WORDPRESS CONFIGURATION
# ============================================

# Get WordPress URL from .env (e.g., "https://mysite.com")
WORDPRESS_URL = os.getenv("WORDPRESS_URL", "").rstrip("/")
# The .rstrip("/") removes trailing slash so we have clean URLs like:
# "https://mysite.com" instead of "https://mysite.com/"

# Get WordPress admin username from .env
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME", "")

# Get WordPress Application Password from .env
# (This is NOT your regular WordPress password - it's a special app-specific password)
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD", "")

# Should we enforce HTTPS (secure connection)?
# os.getenv returns string, so we check if it's "true" (case-insensitive)
WORDPRESS_HTTPS = os.getenv("WORDPRESS_HTTPS", "true").lower() == "true"

# ============================================
# VALIDATION - Check if credentials are set
# ============================================

def validate_config():
    """
    Check if all required credentials are provided.
    If any are missing, raise an error to prevent the server from starting.
    """
    
    # List of required settings
    required_settings = {
        "WORDPRESS_URL": WORDPRESS_URL,
        "WORDPRESS_USERNAME": WORDPRESS_USERNAME,
        "WORDPRESS_PASSWORD": WORDPRESS_PASSWORD,
    }
    
    # Check each setting
    for setting_name, setting_value in required_settings.items():
        if not setting_value:  # If empty or None
            raise ValueError(
                f"❌ Missing configuration: {setting_name}\n"
                f"   Please create a .env file and set {setting_name}"
            )
    
    # All settings are valid
    print("✅ Configuration loaded successfully!")


# ============================================
# WORDPRESS API ENDPOINTS
# ============================================

# Base URL for all WordPress REST API calls
# Example: "https://mysite.com/wp-json/wp/v2"
WORDPRESS_API_BASE = f"{WORDPRESS_URL}/wp-json/wp/v2"

# Base URL for WordPress core REST API
WP_CORE_API_BASE = f"{WORDPRESS_URL}/wp-json"

# ============================================
# AUTHENTICATION HEADER
# ============================================

import base64

def get_auth_header():
    """
    Create the authentication header for WordPress API requests.
    
    How it works:
    1. Combine username:password -> "admin:myapppassword"
    2. Encode to Base64 -> "YWRtaW46bXlhcHBwYXNzd29yZA=="
    3. Return as header -> {"Authorization": "Basic YWRtaW46bXlhcHBwYXNzd29yZA=="}
    
    Why Base64? 
    - It's a standard way to encode credentials for HTTP Basic Auth
    - WordPress expects this format
    - It's NOT encryption (don't send over plain HTTP!)
    """
    
    # Combine username and password with colon
    credentials = f"{WORDPRESS_USERNAME}:{WORDPRESS_PASSWORD}"
    
    # Encode to bytes, then Base64, then decode back to string
    # encode() -> converts string to bytes
    # b64encode() -> converts bytes to Base64 bytes
    # decode() -> converts bytes back to string
    encoded = base64.b64encode(credentials.encode()).decode()
    
    # Return as a dictionary ready to use in HTTP headers
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"  # Tell WordPress we're sending JSON
    }


if __name__ == "__main__":
    # This runs if you execute this file directly (for testing)
    validate_config()
    print(f"WordPress URL: {WORDPRESS_URL}")
    print(f"API Base: {WORDPRESS_API_BASE}")
    print("Configuration is ready!")
