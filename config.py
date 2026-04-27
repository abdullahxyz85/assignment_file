import os
import base64
from dotenv import load_dotenv

load_dotenv()

WORDPRESS_URL = os.getenv("WORDPRESS_URL", "").rstrip("/")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME", "")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD", "")
WORDPRESS_HTTPS = os.getenv("WORDPRESS_HTTPS", "true").lower() == "true"

def validate_config():
    required_settings = {
        "WORDPRESS_URL": WORDPRESS_URL,
        "WORDPRESS_USERNAME": WORDPRESS_USERNAME,
        "WORDPRESS_PASSWORD": WORDPRESS_PASSWORD,
    }
    for setting_name, setting_value in required_settings.items():
        if not setting_value:
            raise ValueError(
                f"❌ Missing configuration: {setting_name}\n"
                f"   Please create a .env file and set {setting_name}"
            )
    print("✅ Configuration loaded successfully!")

WORDPRESS_API_BASE = f"{WORDPRESS_URL}/wp-json/wp/v2"
WP_CORE_API_BASE = f"{WORDPRESS_URL}/wp-json"

def get_auth_header():
    credentials = f"{WORDPRESS_USERNAME}:{WORDPRESS_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }

if __name__ == "__main__":
    validate_config()
    print(f"WordPress URL: {WORDPRESS_URL}")
    print(f"API Base: {WORDPRESS_API_BASE}")
    print("Configuration is ready!")
