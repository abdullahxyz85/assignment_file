import asyncio
import json
import sys
import traceback
from typing import Any
import mcp
from mcp.server import Server
from mcp.types import Tool, TextContent
from config import validate_config
from wordpress_api import (
    list_posts,
    create_post,
    list_plugins,
    manage_plugin,
    list_users,
    get_site_stats,
    close as close_api
)

server = Server("wordpress-mcp")

@server.list_tools()
async def list_tools() -> list[Tool]:
    list_posts_tool = Tool(
        name="list_posts",
        description="Get all WordPress posts from the blog",
        inputSchema={
            "type": "object",
            "properties": {
                "per_page": {
                    "type": "integer",
                    "description": "Number of posts to return (default: 10)",
                    "default": 10
                },
                "status": {
                    "type": "string",
                    "description": "Filter by status: 'publish', 'draft', 'pending' (default: 'publish')",
                    "default": "publish"
                }
            }
        }
    )
    create_post_tool = Tool(
        name="create_post",
        description="Create a new WordPress post",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Post title (required)"
                },
                "content": {
                    "type": "string",
                    "description": "Post content/body (required)"
                },
                "status": {
                    "type": "string",
                    "description": "Post status: 'draft' or 'publish' (default: 'draft')",
                    "default": "draft"
                }
            },
            "required": ["title", "content"]
        }
    )
    manage_plugins_tool = Tool(
        name="manage_plugins",
        description="List plugins or manage (activate/deactivate/delete) a specific plugin",
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform: 'list', 'activate', 'deactivate', 'delete'",
                    "enum": ["list", "activate", "deactivate", "delete"]
                },
                "plugin_slug": {
                    "type": "string",
                    "description": "Plugin slug (e.g., 'akismet', 'hello-dolly') - required for activate/deactivate/delete"
                }
            },
            "required": ["action"]
        }
    )
    list_users_tool = Tool(
        name="list_users",
        description="Get all WordPress users with their roles and emails",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    )
    get_site_stats_tool = Tool(
        name="get_site_stats",
        description="Get WordPress site health, version info, and statistics",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    )
    return [
        list_posts_tool,
        create_post_tool,
        manage_plugins_tool,
        list_users_tool,
        get_site_stats_tool
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Any:
    try:
        if name == "list_posts":
            per_page = arguments.get("per_page", 10)
            status = arguments.get("status", "publish")
            posts = await list_posts(per_page=per_page, status=status)
            return {
                "success": True,
                "count": len(posts),
                "posts": posts
            }
        elif name == "create_post":
            title = arguments.get("title")
            content = arguments.get("content")
            status = arguments.get("status", "draft")
            if not title or not content:
                return {
                    "success": False,
                    "error": "Title and content are required"
                }
            post = await create_post(title=title, content=content, status=status)
            return {
                "success": True,
                "message": f"Post created successfully!",
                "post": post
            }
        elif name == "manage_plugins":
            action = arguments.get("action")
            plugin_slug = arguments.get("plugin_slug")
            if action == "list":
                plugins = await list_plugins()
                return {
                    "success": True,
                    "count": len(plugins),
                    "plugins": plugins
                }
            else:
                if not plugin_slug:
                    return {
                        "success": False,
                        "error": f"plugin_slug is required for {action} action"
                    }
                result = await manage_plugin(plugin_slug=plugin_slug, action=action)
                return {
                    "success": True,
                    "message": f"Plugin {action} successful!",
                    "result": result
                }
        elif name == "list_users":
            users = await list_users()
            return {
                "success": True,
                "count": len(users),
                "users": users
            }
        elif name == "get_site_stats":
            stats = await get_site_stats()
            return {
                "success": True,
                "stats": stats
            }
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {name}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

async def main():
    try:
        validate_config()
    except ValueError as e:
        print(f"❌ Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    print("🚀 WordPress MCP Server Starting...", file=sys.stderr)
    print("📻 Listening for AI agent connections on stdio...", file=sys.stderr)
    print("✅ Server is ready! Waiting for requests...", file=sys.stderr)
    try:
        async with mcp.stdio_server() as (read_stream, write_stream):
            print("📡 Connected to MCP client", file=sys.stderr)
            init_options = server.create_initialization_options()
            await server.run(
                read_stream,
                write_stream,
                init_options,
                raise_exceptions=False
            )
    except KeyboardInterrupt:
        print("\n❌ Server stopped by user", file=sys.stderr)
    except ExceptionGroup as eg:
        print(f"❌ Server error group:", file=sys.stderr)
        for exc in eg.exceptions:
            print(f"   - {type(exc).__name__}: {exc}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Server error: {type(e).__name__}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
    finally:
        print("🧹 Cleaning up...", file=sys.stderr)
        await close_api()
        print("✅ Server stopped", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())
