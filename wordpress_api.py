import httpx
from config import WORDPRESS_API_BASE, WP_CORE_API_BASE, get_auth_header, WORDPRESS_HTTPS
from typing import Optional, List, Dict, Any

client = httpx.AsyncClient(timeout=30.0, verify=WORDPRESS_HTTPS)

async def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    url = f"{WORDPRESS_API_BASE}{endpoint}"
    headers = get_auth_header()
    try:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise Exception(
            f"WordPress API Error ({e.response.status_code}): {e.response.text}"
        )
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")

async def list_posts(
    per_page: int = 10,
    page: int = 1,
    status: str = "publish"
) -> List[Dict[str, Any]]:
    params = {
        "per_page": per_page,
        "page": page,
        "status": status
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    response = await make_request("GET", f"/posts?{query_string}")
    posts = []
    for post in response:
        posts.append({
            "id": post.get("id"),
            "title": post.get("title", {}).get("rendered", ""),
            "content": post.get("content", {}).get("rendered", "")[:200],
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
    post_data = {
        "title": title,
        "content": content,
        "status": status
    }
    response = await make_request("POST", "/posts", data=post_data)
    return {
        "id": response.get("id"),
        "title": response.get("title", {}).get("rendered", ""),
        "status": response.get("status"),
        "link": response.get("link"),
        "date_created": response.get("date")
    }

async def list_plugins() -> List[Dict[str, Any]]:
    url = f"{WP_CORE_API_BASE}/plugins"
    headers = get_auth_header()
    try:
        response = await client.request("GET", url, headers=headers)
        response.raise_for_status()
        plugins = response.json()
    except Exception as e:
        raise Exception(f"Failed to list plugins: {str(e)}")
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
    valid_actions = ["activate", "deactivate", "delete"]
    if action not in valid_actions:
        raise ValueError(f"Invalid action. Use: {', '.join(valid_actions)}")
    url = f"{WP_CORE_API_BASE}/plugins/{plugin_slug}"
    headers = get_auth_header()
    action_data = {"status": action}
    try:
        if action == "activate":
            action_data = {"status": "active"}
        elif action == "deactivate":
            action_data = {"status": "inactive"}
        elif action == "delete":
            response = await client.request("DELETE", url, headers=headers)
            response.raise_for_status()
            return {"plugin": plugin_slug, "action": "deleted", "success": True}
        response = await client.request(
            "PUT",
            url,
            headers=headers,
            json=action_data
        )
        response.raise_for_status()
        return {
            "plugin": plugin_slug,
            "action": action + "d",
            "success": True
        }
    except Exception as e:
        raise Exception(f"Failed to {action} plugin '{plugin_slug}': {str(e)}")

async def list_users() -> List[Dict[str, Any]]:
    response = await make_request("GET", "/users")
    formatted_users = []
    for user in response:
        formatted_users.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "slug": user.get("slug"),
            "roles": user.get("roles", [])
        })
    return formatted_users

async def get_site_stats() -> Dict[str, Any]:
    try:
        url = f"{WP_CORE_API_BASE}/settings"
        headers = get_auth_header()
        settings_response = await client.request("GET", url, headers=headers)
        settings_response.raise_for_status()
        settings = settings_response.json()
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

async def close():
    await client.aclose()
