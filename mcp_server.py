"""
WordPress MCP Server
====================
This is the main server that listens for requests from AI agents and processes them.

How it works:
1. Server starts and listens on stdio (standard input/output)
2. AI agent connects and asks for available tools
3. Server responds with list of 4 tools
4. AI agent selects a tool and sends parameters
5. Server calls the corresponding WordPress function
6. Server sends results back to AI agent
"""

import asyncio
import json
import sys
import traceback
from typing import Any

# Import the MCP server framework
import mcp
from mcp.server import Server
from mcp.types import Tool, TextContent

# Import our configuration and WordPress API
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

# ============================================
# INITIALIZE MCP SERVER
# ============================================

# Create the MCP server instance
# This server will receive tool requests from AI agents
server = Server("wordpress-mcp")


# ============================================
# DEFINE AVAILABLE TOOLS
# ============================================

@server.list_tools()
async def list_tools () -> list[Tool]:
    """
    Define all available tools that AI agents can use.
    
    When an AI agent connects, it asks: "What tools do you have?"
    This function responds with a list of 4 tools with descriptions.
    
    Each tool has:
    - name: identifier for the tool
    - description: what it does (shown to AI)
    - inputSchema: what parameters it expects
    
    Returns:
    --------
    list
        List of Tool objects that describe what this server can do
    """
    
    # Tool 1: List Posts
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
    
    # Tool 2: Create Post
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
            "required": ["title", "content"]  # These MUST be provided
        }
    )
    
    # Tool 3: Manage Plugins
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
            "required": ["action"]  # Only action is required, slug depends on action
        }
    )
    
    # Tool 4: List Users
    list_users_tool = Tool(
        name="list_users",
        description="Get all WordPress users with their roles and emails",
        inputSchema={
            "type": "object",
            "properties": {}  # This tool takes no parameters
        }
    )
    
    # Tool 5: Get Site Statistics
    get_site_stats_tool = Tool(
        name="get_site_stats",
        description="Get WordPress site health, version info, and statistics",
        inputSchema={
            "type": "object",
            "properties": {}  # This tool takes no parameters
        }
    )
    
    # Return all tools as a list
    # AI agents will see all 5 tools when they connect
    return [
        list_posts_tool,
        create_post_tool,
        manage_plugins_tool,
        list_users_tool,
        get_site_stats_tool
    ]


# ============================================
# DEFINE TOOL HANDLERS
# ============================================

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Any:
    """
    Handle tool calls from AI agents.
    
    When an AI agent says:
    "Use the list_posts tool with per_page=5"
    
    This function:
    1. Receives name="list_posts" and arguments={"per_page": 5}
    2. Calls the appropriate function
    3. Returns the result to the AI agent
    
    Parameters:
    -----------
    name : str
        The name of the tool being called
        Examples: "list_posts", "create_post", "manage_plugins"
    
    arguments : dict
        The parameters for that tool
        Example: {"per_page": 5, "status": "publish"}
    
    Returns:
    --------
    Any
        The result from the tool, which gets sent back to the AI agent
    """
    
    try:
        # Tool 1: List Posts
        if name == "list_posts":
            per_page = arguments.get("per_page", 10)
            status = arguments.get("status", "publish")
            
            # Call the WordPress API function
            posts = await list_posts(per_page=per_page, status=status)
            
            # Return formatted result
            return {
                "success": True,
                "count": len(posts),
                "posts": posts
            }
        
        # Tool 2: Create Post
        elif name == "create_post":
            title = arguments.get("title")
            content = arguments.get("content")
            status = arguments.get("status", "draft")
            
            # Validate required parameters
            if not title or not content:
                return {
                    "success": False,
                    "error": "Title and content are required"
                }
            
            # Call the WordPress API function
            post = await create_post(title=title, content=content, status=status)
            
            # Return the newly created post
            return {
                "success": True,
                "message": f"Post created successfully!",
                "post": post
            }
        
        # Tool 3: Manage Plugins
        elif name == "manage_plugins":
            action = arguments.get("action")
            plugin_slug = arguments.get("plugin_slug")
            
            if action == "list":
                # List all plugins
                plugins = await list_plugins()
                return {
                    "success": True,
                    "count": len(plugins),
                    "plugins": plugins
                }
            
            else:  # activate, deactivate, delete
                # Validate plugin_slug is provided
                if not plugin_slug:
                    return {
                        "success": False,
                        "error": f"plugin_slug is required for {action} action"
                    }
                
                # Call the WordPress API function
                result = await manage_plugin(plugin_slug=plugin_slug, action=action)
                
                return {
                    "success": True,
                    "message": f"Plugin {action} successful!",
                    "result": result
                }
        
        # Tool 4: List Users
        elif name == "list_users":
            # Call the WordPress API function
            users = await list_users()
            
            # Return the user list
            return {
                "success": True,
                "count": len(users),
                "users": users
            }
        
        # Tool 5: Get Site Stats
        elif name == "get_site_stats":
            # Call the WordPress API function
            stats = await get_site_stats()
            
            # Return site statistics
            return {
                "success": True,
                "stats": stats
            }
        
        else:
            # Unknown tool
            return {
                "success": False,
                "error": f"Unknown tool: {name}"
            }
    
    except Exception as e:
        # If something goes wrong, return error message
        return {
            "success": False,
            "error": str(e)
        }


# ============================================
# MAIN ENTRY POINT
# ============================================

async def main():
    """
    Main function that starts the MCP server on stdio.
    
    The server listens for JSON-RPC messages from stdin and sends responses to stdout.
    """
    
    # Validate credentials before starting
    try:
        validate_config()
    except ValueError as e:
        print(f"❌ Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Print startup message to stderr so it doesn't interfere with MCP communication
    print("🚀 WordPress MCP Server Starting...", file=sys.stderr)
    print("📻 Listening for AI agent connections on stdio...", file=sys.stderr)
    print("✅ Server is ready! Waiting for requests...", file=sys.stderr)
    
    try:
        # Set up the stdio transport and connect the server
        async with mcp.stdio_server() as (read_stream, write_stream):
            print("📡 Connected to MCP client", file=sys.stderr)
            
            # Get initialization options and run the server
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


# ============================================
# RUN THE SERVER
# ============================================

if __name__ == "__main__":
    """
    This runs if the script is executed directly.
    
    Example usage in terminal:
    $ python mcp_server.py
    
    The server will start and wait for connections.
    """
    
    # Run the main async function
    asyncio.run(main())
