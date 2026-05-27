# Copilot Instructions — MCP Context Server

## About This Project

This is a Python MCP (Model Context Protocol) server that provides session context management, Jira/Confluence integration, Git repository access, and filesystem knowledge base search. It runs locally via stdio transport and is used by GitHub Copilot and other AI agents in VS Code.

## Tech Stack

- **Python 3.11+** with type hints throughout
- **MCP SDK** (`mcp[cli]`) with `FastMCP` server pattern
- **Pydantic v2** for models and settings
- **httpx** for async HTTP calls (Jira/Confluence)
- **GitPython** for git operations
- **pytest** for testing

## Session Context Protocol

This server IS the session context server. When working on it:
1. Use `session_create` to track your own development sessions
2. Test changes by running `python -m pytest tests/ -v`
3. Verify the server starts: `python -m mcp_context_server.main` (it will wait for stdio input)

## Code Conventions

- All MCP tools are registered in `main.py` using `@mcp.tool()` decorators
- Business logic lives in separate modules (`sessions.py`, `jira_client.py`, etc.)
- Tool functions return JSON strings via the `_json()` helper
- Async tools (Jira, Confluence) use `async def`; sync tools (Git, KB, Sessions) use `def`
- Settings from environment variables with `MCP_` prefix via pydantic-settings

## Adding New Tools

1. Create the service module in `mcp_context_server/`
2. Register tools in `main.py` with `@mcp.tool()` decorator
3. Include comprehensive docstrings — they become the tool descriptions for agents
4. Add tests in `tests/`
5. Add any new env vars to `config.py` Settings class and `.env.example`
