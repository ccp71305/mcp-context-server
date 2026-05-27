# MCP Context Server

A production-ready local MCP (Model Context Protocol) server for AI agent session context management, with integrations for Jira, Confluence, Git repositories, and filesystem knowledge base.

## Features

| Feature | Tools | Description |
|---------|-------|-------------|
| **Session Context** | `session_create`, `session_get`, `session_list`, `session_add_context`, `session_update_status`, `session_search`, `session_delete` | Persistent context tracking across agent conversations |
| **Jira** | `jira_get_issue`, `jira_search`, `jira_get_comments`, `jira_add_comment` | Issue lookup, JQL search, comment management |
| **Confluence** | `confluence_get_page`, `confluence_search`, `confluence_space_pages`, `confluence_page_children` | Page retrieval, CQL search, space browsing |
| **Git** | `git_status`, `git_log`, `git_diff`, `git_blame`, `git_branches`, `git_file_history`, `git_show_file` | Local repo operations — log, diff, blame, status |
| **Knowledge Base** | `kb_search`, `kb_read_file`, `kb_list_directory`, `kb_find_files`, `kb_grep` | Filesystem search, file reading, grep with regex |

## Quick Start

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd mcp-context-server
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -e ".[dev]"
```

### 2. Configure

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
# Edit .env with your Jira/Confluence credentials and paths
```

**Minimum configuration** (session management + git + KB work without Jira/Confluence):
```env
MCP_SESSIONS_DIR=~/.mcp-context-server/sessions
MCP_KB_ROOTS=["C:\\path\\to\\your\\projects"]
MCP_GIT_DEFAULT_REPOS=["C:\\path\\to\\your\\git-repo"]
```

### 3. Connect to VS Code

Add the MCP server to your workspace. Create or update `.vscode/mcp.json`:

```json
{
    "servers": {
        "mcp-context-server": {
            "type": "stdio",
            "command": "/path/to/mcp-context-server/.venv/Scripts/python.exe",
            "args": ["-m", "mcp_context_server.main"],
            "cwd": "/path/to/mcp-context-server"
        }
    }
}
```

Replace `/path/to/mcp-context-server` with your actual clone directory. On Linux/Mac, use `.venv/bin/python` instead of `.venv/Scripts/python.exe`.

### 4. Verify

In VS Code, open the Copilot Chat panel. You should see the MCP tools listed under the available tools. Try:

> "List all active sessions" → the agent should call `session_list`

## Architecture

```
mcp-context-server/
├── mcp_context_server/
│   ├── __init__.py
│   ├── main.py              # MCP server entry point, all tool registrations
│   ├── config.py            # Settings from environment variables
│   ├── sessions.py          # Session model and file-based persistence
│   ├── jira_client.py       # Async Jira REST API client
│   ├── confluence_client.py # Async Confluence REST API client
│   ├── git_service.py       # Git operations via GitPython
│   └── knowledge_base.py    # Filesystem search and indexing
├── tests/
│   ├── test_sessions.py
│   └── test_knowledge_base.py
├── .github/
│   ├── copilot-instructions.md
│   └── skills/              # Copilot skill definitions
├── docs/                    # Project documentation
├── .env.example
├── .env                     # Your config (gitignored)
├── .gitignore
├── pyproject.toml           # Project dependencies and build config
├── LICENSE
└── README.md
```

## Configuration Reference

All settings use the `MCP_` prefix and are loaded from environment variables or `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SESSIONS_DIR` | `~/.mcp-context-server/sessions` | Session storage directory |
| `MCP_JIRA_BASE_URL` | (empty) | Jira instance URL |
| `MCP_JIRA_EMAIL` | (empty) | Jira auth email |
| `MCP_JIRA_API_TOKEN` | (empty) | Jira API token |
| `MCP_CONFLUENCE_BASE_URL` | (empty) | Confluence instance URL |
| `MCP_CONFLUENCE_EMAIL` | (empty) | Confluence auth email |
| `MCP_CONFLUENCE_API_TOKEN` | (empty) | Confluence API token |
| `MCP_GIT_DEFAULT_REPOS` | `[]` | JSON list of git repo paths |
| `MCP_KB_ROOTS` | `[]` | JSON list of KB root directories |
| `MCP_KB_FILE_EXTENSIONS` | (common types) | JSON list of file extensions to index |
| `MCP_KB_MAX_FILE_SIZE_KB` | `512` | Max file size to index |
| `MCP_SERVER_NAME` | `mcp-context-server` | Server name |
| `MCP_LOG_LEVEL` | `INFO` | Logging level |

## Enabling Jira & Confluence

1. Generate an API token: https://id.atlassian.com/manage-profile/security/api-tokens
2. Add to `.env`:
   ```env
   MCP_JIRA_BASE_URL=https://yourorg.atlassian.net
   MCP_JIRA_EMAIL=your.email@company.com
   MCP_JIRA_API_TOKEN=your-token-here
   MCP_CONFLUENCE_BASE_URL=https://yourorg.atlassian.net/wiki
   MCP_CONFLUENCE_EMAIL=your.email@company.com
   MCP_CONFLUENCE_API_TOKEN=your-token-here
   ```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Using with Other Workspaces

To use this MCP server from any VS Code workspace, add the server config to that workspace's `.vscode/mcp.json`. The server is workspace-independent — it uses absolute paths for all operations.

## How Session Context Works

Sessions are stored as JSON files in the configured `MCP_SESSIONS_DIR`. Each session contains:
- Metadata (name, project, tags, status)
- Ordered list of context entries, each with:
  - Timestamp, agent name, category
  - Summary and detailed description
  - Tags and references (file paths, Jira keys, URLs)

Agents create sessions at the start of multi-step work and add entries as they progress. When resuming in a new conversation, the agent loads the session to rebuild context.
