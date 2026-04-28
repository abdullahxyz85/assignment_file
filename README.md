# WordPress MCP Server

A Python-based MCP (Model Context Protocol) server for managing WordPress sites via REST API.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Credentials

Copy `.env.example` to `.env` and add your WordPress credentials:

```
WORDPRESS_URL=https://yourdomain.com
WORDPRESS_USERNAME=admin
WORDPRESS_PASSWORD=your_app_password
WORDPRESS_HTTPS=true
```

### 3. Run Server

```bash
python mcp_server.py
```

## Available Tools

1. **list_posts** - Get WordPress posts
2. **create_post** - Create new post
3. **manage_plugins** - Control plugins (activate/deactivate/delete)
4. **list_users** - Get WordPress users
5. **get_site_stats** - Site information

## File Structure

- `config.py` - Loads credentials, provides authentication headers
- `wordpress_api.py` - WordPress REST API wrapper
- `mcp_server.py` - MCP server with 5 tools
- `requirements.txt` - Python dependencies
- `.env` - Your credentials (keep secret!)

## Getting WordPress App Password

1. WordPress Admin → Users → Your Profile
2. Scroll to "Application Passwords"
3. Enter app name and generate password
4. Copy to `.env`

## Troubleshooting

| Error                 | Solution                               |
| --------------------- | -------------------------------------- |
| Missing configuration | Verify `.env` file has all fields      |
| 401 Unauthorized      | Check credentials in `.env`            |
| Connection refused    | Verify WORDPRESS_URL and HTTPS setting |
