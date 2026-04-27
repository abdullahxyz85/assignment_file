import httpx
from config import WORDPRESS_API_BASE, WP_CORE_API_BASE, get_auth_header, WORDPRESS_HTTPS
from typing import Optional, List, Dict, Any

client = httpx.AsyncClient(timeout=30.0, verify=WORDPRESS_HTTPS)

async def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generic function to make requests to WordPress REST API.
    
    Parameters:
    -----------
    method : str
        HTTP method: "GET", "POST", "PUT", "DELETE", etc.
    
    endpoint : str
        WordPress API endpoint path
        Example: "/posts" becomes "https://mysite.com/wp-json/wp/v2/posts"
    
    data : dict, optional
        Request body for POST/PUT requests
        Example: {"title": "My Post", "content": "Post content"}
    
    Returns:
    --------
    dict
        The JSON response from WordPress
        Example: {"id": 1, "title": "My Post", "status": "publish"}
    
    Raises:
    -------
    Exception
        If the request fails (network error, wrong credentials, etc.)
    """
    
    # Build the full URL
    # Example: "https://mysite.com" + "/wp-json/wp/v2" + "/posts"
    url = f"{WORDPRESS_API_BASE}{endpoint}"
    
    # Get authentication headers
    headers = get_auth_header()
    
    try:
        # Make the HTTP request
        # For POST/PUT requests, convert data to JSON
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            json=data  # Automatically converts dict to JSON string
        )
        
        # Check if request was successful (status code 200-299)
        response.raise_for_status()
        
        # Return the response as JSON (dictionary)
        return response.json()
    
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors (e.g., 404 Not Found, 401 Unauthorized)
        raise Exception(
            f"WordPress API Error ({e.response.status_code}): {e.response.text}"
        )
    except Exception as e:
        # Handle other errors (network, timeout, etc.)
        raise Exception(f"Request failed: {str(e)}")


# ============================================
# POSTS FUNCTIONS
# ============================================

async def list_posts(
    per_page: int = 10,
    page: int = 1,
    status: str = "publish"
) -> List[Dict[str, Any]]:
    """
    Get a list of WordPress posts.
    
    Parameters:
    -----------
    per_page : int
        How many posts to return (default: 10)
    page : int
        Which page of results (default: 1, first page)
    status : str
        Filter by status: "publish", "draft", "pending", etc.
    
    Returns:
    --------
    list
        List of post dictionaries
        Example: [
            {"id": 1, "title": "Hello World", "content": "...", "status": "publish"},
            {"id": 2, "title": "My Post", "content": "...", "status": "draft"}
        ]
    """
    
    # Create query parameters for the API
    params = {
        "per_page": per_page,
        "page": page,
        "status": status
    }
    
    # Build query string: "?per_page=10&page=1&status=publish"
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    
    # Make the GET request to /posts endpoint
    response = await make_request("GET", f"/posts?{query_string}")
    
    # Response is a list of posts, so extract just what we need
    posts = []
    for post in response:
        posts.append({
            "id": post.get("id"),
            "title": post.get("title", {}).get("rendered", ""),
            "content": post.get("content", {}).get("rendered", "")[:200],  # First 200 chars
            "status": post.get("status"),
            "date": post.get("date"),
            "link": post.get("link")
        })
    
    return posts


async def create_post(
    title: str,
    content: str,
    status: str = "draft"
) -> Dict[str, Any]:
    """
    Create a new WordPress post.
    
    Parameters:
    -----------
    title : str
        Post title (required)
    content : str
        Post content/body (required)
    status : str
        Post status: "draft" or "publish" (default: "draft")
    
    Returns:
    --------
    dict
        The newly created post
        Example: {"id": 123, "title": "New Post", "status": "draft", "link": "..."}
    """
    
    # Prepare the post data
    post_data = {
        "title": title,
        "content": content,
        "status": status
    }
    
    # Make POST request to create the post
    response = await make_request("POST", "/posts", data=post_data)
    
    # Return formatted response
    return {
        "id": response.get("id"),
        "title": response.get("title", {}).get("rendered", ""),
        "status": response.get("status"),
        "link": response.get("link"),
        "date_created": response.get("date")
    }


# ============================================
# PLUGINS FUNCTIONS
# ============================================

async def list_plugins() -> List[Dict[str, Any]]:
    """
    Get a list of installed WordPress plugins.
    
    Returns:
    --------
    list
        List of plugin dictionaries
        Example: [
            {"name": "Akismet", "slug": "akismet", "status": "active"},
            {"name": "Hello Dolly", "slug": "hello-dolly", "status": "inactive"}
        ]
    """
    
    # Make GET request to plugins endpoint
    # Note: This uses WP_CORE_API_BASE because it's a different API route
    url = f"{WP_CORE_API_BASE}/plugins"
    headers = get_auth_header()
    
    try:
        response = await client.request("GET", url, headers=headers)
        response.raise_for_status()
        plugins = response.json()
    except Exception as e:
        raise Exception(f"Failed to list plugins: {str(e)}")
    
    # Format the response
    formatted_plugins = []
    for plugin in plugins:
        formatted_plugins.append({
            "name": plugin.get("name", "Unknown"),
            "slug": plugin.get("slug", "unknown"),
            "status": "active" if plugin.get("status") == "active" else "inactive",
            "version": plugin.get("version", "Unknown"),
            "description": plugin.get("description", "")
        })
    
    return formatted_plugins


async def manage_plugin(
    plugin_slug: str,
    action: str
) -> Dict[str, Any]:
    """
    Manage a WordPress plugin (activate, deactivate, delete).
    
    Parameters:
    -----------
    plugin_slug : str
        Plugin slug (e.g., "akismet", "hello-dolly")
    action : str
        Action to perform: "activate", "deactivate", "delete"
    
    Returns:
    --------
    dict
        Result of the action
        Example: {"plugin": "akismet", "action": "activated", "success": True}
    """
    
    # Valid actions
    valid_actions = ["activate", "deactivate", "delete"]
    
    if action not in valid_actions:
        raise ValueError(f"Invalid action. Use: {', '.join(valid_actions)}")
    
    # Build the request
    url = f"{WP_CORE_API_BASE}/plugins/{plugin_slug}"
    headers = get_auth_header()
    
    # Prepare the action data
    action_data = {"status": action}
    
    try:
        # Different endpoints for different actions
        if action == "activate":
            action_data = {"status": "active"}
        elif action == "deactivate":
            action_data = {"status": "inactive"}
        elif action == "delete":
            # For delete, we use DELETE method
            response = await client.request("DELETE", url, headers=headers)
            response.raise_for_status()
            return {"plugin": plugin_slug, "action": "deleted", "success": True}
        
        # For activate/deactivate, use PUT method
        response = await client.request(
            "PUT",
            url,
            headers=headers,
            json=action_data
        )
        response.raise_for_status()
        
        return {
            "plugin": plugin_slug,
            "action": action + "d",  # "activated", "deactivated"
            "success": True
        }
    
    except Exception as e:
        raise Exception(f"Failed to {action} plugin '{plugin_slug}': {str(e)}")


# ============================================
# USERS FUNCTIONS
# ============================================

async def list_users() -> List[Dict[str, Any]]:
    """
    Get a list of WordPress users.
    
    Returns:
    --------
    list
        List of user dictionaries
        Example: [
            {"id": 1, "name": "Admin", "email": "admin@example.com", "role": "administrator"},
            {"id": 2, "name": "Editor", "email": "editor@example.com", "role": "editor"}
        ]
    """
    
    # Make GET request to users endpoint
    response = await make_request("GET", "/users")
    
    # Format the response
    formatted_users = []
    for user in response:
        formatted_users.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "slug": user.get("slug"),
            "roles": user.get("roles", [])  # List of roles like ["administrator"]
        })
    
    return formatted_users


# ============================================
# SITE HEALTH & STATISTICS
# ============================================

async def get_site_stats() -> Dict[str, Any]:
    """
    Get WordPress site health and statistics.
    
    Returns:
    --------
    dict
        Site statistics
        Example: {
            "wordpress_version": "6.4",
            "php_version": "8.1",
            "latest_wordpress": "6.5",
            "updates_available": 3,
            "health_status": "good"
        }
    """
    
    try:
        # Get site settings
        url = f"{WP_CORE_API_BASE}/settings"
        headers = get_auth_header()
        
        settings_response = await client.request("GET", url, headers=headers)
        settings_response.raise_for_status()
        settings = settings_response.json()
        
        # Get site health
        health_url = f"{WP_CORE_API_BASE}/site-health/status"
        health_response = await client.request("GET", health_url, headers=headers)
        
        health_data = {}
        if health_response.status_code == 200:
            health_data = health_response.json()
        
        return {
            "wordpress_version": settings.get("version", "Unknown"),
            "php_version": settings.get("php_version", "Unknown"),
            "site_url": settings.get("url", "Unknown"),
            "site_title": settings.get("title", "Unknown"),
            "health_status": health_data.get("status", "unknown"),
            "health_tests": len(health_data.get("tests", {})),
            "timestamp": settings.get("date", "Unknown")
        }
    
    except Exception as e:
        raise Exception(f"Failed to get site stats: {str(e)}")


# ============================================
# CLEANUP (Close HTTP connection when done)
# ============================================

async def close():
    """Close the HTTP client connection."""
    await client.aclose()
