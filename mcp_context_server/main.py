"""MCP Context Server — main entry point.

Registers all MCP tools for session context management, Jira, Confluence,
Git integration, and filesystem knowledge base.
"""

from __future__ import annotations

import json
import logging
import sys

from mcp.server.fastmcp import FastMCP

from .config import get_settings
from .confluence_client import ConfluenceClient
from .git_service import GitService
from .jira_client import JiraClient
from .knowledge_base import KnowledgeBase
from .sessions import ContextEntry, Session, SessionStore

# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    settings.server_name,
    instructions=(
        "MCP Context Server — provides tools for:\n"
        "1) Session context tracking across agent conversations\n"
        "2) Jira issue lookup and search\n"
        "3) Confluence page search and retrieval\n"
        "4) Local git repository operations (log, diff, status, blame)\n"
        "5) Filesystem knowledge base search\n\n"
        "Use session tools to persist context between conversations. "
        "Always load the relevant session at the start of a conversation."
    ),
)

# Service instances
session_store = SessionStore(settings.sessions_dir)
jira = JiraClient(settings.jira_base_url, settings.jira_email, settings.jira_api_token)
confluence = ConfluenceClient(settings.confluence_base_url, settings.confluence_email, settings.confluence_api_token)
git_svc = GitService()
kb = KnowledgeBase(settings.kb_roots, settings.kb_file_extensions, settings.kb_max_file_size_kb)


def _json(obj: object) -> str:
    """Serialize to pretty JSON string."""
    return json.dumps(obj, indent=2, default=str)


# ===================================================================
# SESSION CONTEXT TOOLS
# ===================================================================


@mcp.tool()
def session_create(name: str, description: str = "", project: str = "", tags: list[str] | None = None) -> str:
    """Create a new work session to track context across agent conversations.

    Use this at the start of a new task/feature/refactoring to create a persistent
    context container. Returns the session ID for future reference.

    Args:
        name: Human-readable session name (e.g. "ION-12310 CloudSDK Refactoring")
        description: What this session is about
        project: Associated project name
        tags: Tags for categorization (e.g. ["java", "refactoring", "aws"])
    """
    session = Session(name=name, description=description, project=project, tags=tags or [])
    session_store.save(session)
    logger.info("Created session %s: %s", session.id, name)
    return _json({"status": "created", "session_id": session.id, "name": name})


@mcp.tool()
def session_get(session_id: str, max_entries: int = 30) -> str:
    """Load a session and its recent context entries.

    Use this at the start of a conversation to restore context from a previous session.

    Args:
        session_id: The session ID to load
        max_entries: Maximum number of recent entries to return (default 30)
    """
    session = session_store.load(session_id)
    if not session:
        return _json({"error": f"Session {session_id} not found"})
    return _json(session.get_summary(max_entries))


@mcp.tool()
def session_list(status: str | None = None, project: str | None = None) -> str:
    """List all sessions, optionally filtered by status or project.

    Args:
        status: Filter by status (active, paused, completed, archived)
        project: Filter by project name
    """
    sessions = session_store.list_sessions(status_filter=status, project_filter=project)
    return _json({"sessions": sessions, "count": len(sessions)})


@mcp.tool()
def session_add_context(
    session_id: str,
    summary: str,
    category: str = "general",
    detail: str = "",
    agent: str = "unknown",
    tags: list[str] | None = None,
    references: list[str] | None = None,
) -> str:
    """Add a context entry to a session. Call this frequently to track progress.

    Categories: general, decision, finding, blocker, progress, code_change, test_result

    Args:
        session_id: Target session ID
        summary: Short summary of what happened or was decided
        category: Entry category for filtering
        detail: Extended details, code snippets, error messages, etc.
        agent: Which agent is adding this (e.g. "copilot-claude-opus", "copilot-gpt4")
        tags: Tags for filtering
        references: Related file paths, URLs, Jira keys, etc.
    """
    session = session_store.load(session_id)
    if not session:
        return _json({"error": f"Session {session_id} not found"})

    entry = ContextEntry(
        agent=agent,
        category=category,
        summary=summary,
        detail=detail,
        tags=tags or [],
        references=references or [],
    )
    session.add_entry(entry)
    session_store.save(session)
    return _json({"status": "added", "entry_id": entry.id, "total_entries": len(session.entries)})


@mcp.tool()
def session_update_status(session_id: str, status: str) -> str:
    """Update session status.

    Args:
        session_id: Target session ID
        status: New status — one of: active, paused, completed, archived
    """
    if status not in ("active", "paused", "completed", "archived"):
        return _json({"error": f"Invalid status: {status}. Must be one of: active, paused, completed, archived"})

    session = session_store.load(session_id)
    if not session:
        return _json({"error": f"Session {session_id} not found"})

    session.status = status
    session_store.save(session)
    return _json({"status": "updated", "session_id": session_id, "new_status": status})


@mcp.tool()
def session_search(
    query: str,
    session_id: str | None = None,
    category: str | None = None,
    tags: list[str] | None = None,
) -> str:
    """Search across session entries for specific context.

    Args:
        query: Text to search for in summaries and details
        session_id: Optionally limit search to a specific session
        category: Filter by category
        tags: Filter by tags
    """
    results = session_store.search_entries(query, session_id=session_id, category=category, tags=tags)
    return _json({"results": results, "count": len(results)})


@mcp.tool()
def session_delete(session_id: str) -> str:
    """Delete a session permanently.

    Args:
        session_id: The session ID to delete
    """
    deleted = session_store.delete(session_id)
    return _json({"status": "deleted" if deleted else "not_found", "session_id": session_id})


# ===================================================================
# JIRA TOOLS
# ===================================================================


@mcp.tool()
async def jira_get_issue(issue_key: str) -> str:
    """Fetch a Jira issue by key (e.g. PROJ-123). Returns summary, description, status, and metadata.

    Args:
        issue_key: The Jira issue key (e.g. ION-12310)
    """
    if not jira.configured:
        return _json({"error": "Jira is not configured. Set MCP_JIRA_BASE_URL, MCP_JIRA_EMAIL, MCP_JIRA_API_TOKEN."})
    result = await jira.get_issue(issue_key)
    return _json(result)


@mcp.tool()
async def jira_search(jql: str, max_results: int = 25) -> str:
    """Search Jira issues using JQL (Jira Query Language).

    Examples:
        - project = ION AND status = "In Progress"
        - assignee = currentUser() AND sprint in openSprints()
        - labels = refactoring AND updated >= -7d

    Args:
        jql: JQL query string
        max_results: Maximum results to return (default 25, max 100)
    """
    if not jira.configured:
        return _json({"error": "Jira is not configured. Set MCP_JIRA_BASE_URL, MCP_JIRA_EMAIL, MCP_JIRA_API_TOKEN."})
    results = await jira.search_issues(jql, max_results)
    return _json({"issues": results, "count": len(results)})


@mcp.tool()
async def jira_get_comments(issue_key: str, max_results: int = 20) -> str:
    """Get comments on a Jira issue.

    Args:
        issue_key: The Jira issue key
        max_results: Maximum comments to return
    """
    if not jira.configured:
        return _json({"error": "Jira is not configured."})
    comments = await jira.get_issue_comments(issue_key, max_results)
    return _json({"issue_key": issue_key, "comments": comments, "count": len(comments)})


@mcp.tool()
async def jira_add_comment(issue_key: str, comment: str) -> str:
    """Add a comment to a Jira issue.

    Args:
        issue_key: The Jira issue key
        comment: Comment text to add
    """
    if not jira.configured:
        return _json({"error": "Jira is not configured."})
    result = await jira.add_comment(issue_key, comment)
    return _json(result)


# ===================================================================
# CONFLUENCE TOOLS
# ===================================================================


@mcp.tool()
async def confluence_get_page(page_id: str) -> str:
    """Fetch a Confluence page by its ID. Returns title, body text, and metadata.

    Args:
        page_id: The Confluence page ID (numeric)
    """
    if not confluence.configured:
        return _json({"error": "Confluence is not configured. Set MCP_CONFLUENCE_BASE_URL, MCP_CONFLUENCE_EMAIL, MCP_CONFLUENCE_API_TOKEN."})
    result = await confluence.get_page(page_id)
    return _json(result)


@mcp.tool()
async def confluence_search(cql: str, max_results: int = 20) -> str:
    """Search Confluence using CQL (Confluence Query Language).

    Examples:
        - type = page AND space = DEV AND text ~ "migration guide"
        - title = "Architecture Decision Record" AND space = ARCH
        - label = "runbook" AND lastModified >= "2024-01-01"

    Args:
        cql: CQL query string
        max_results: Maximum results to return
    """
    if not confluence.configured:
        return _json({"error": "Confluence is not configured."})
    results = await confluence.search(cql, max_results)
    return _json({"results": results, "count": len(results)})


@mcp.tool()
async def confluence_space_pages(space_key: str, max_results: int = 50) -> str:
    """List pages in a Confluence space.

    Args:
        space_key: The space key (e.g. DEV, ARCH, OPS)
        max_results: Maximum pages to return
    """
    if not confluence.configured:
        return _json({"error": "Confluence is not configured."})
    results = await confluence.get_space_pages(space_key, max_results)
    return _json({"space": space_key, "pages": results, "count": len(results)})


@mcp.tool()
async def confluence_page_children(page_id: str) -> str:
    """Get child pages of a Confluence page.

    Args:
        page_id: The parent page ID
    """
    if not confluence.configured:
        return _json({"error": "Confluence is not configured."})
    results = await confluence.get_page_children(page_id)
    return _json({"parent_id": page_id, "children": results, "count": len(results)})


# ===================================================================
# GIT TOOLS
# ===================================================================


@mcp.tool()
def git_status(repo_path: str) -> str:
    """Get git working tree status for a repository.

    Args:
        repo_path: Absolute path to the git repository
    """
    result = git_svc.status(repo_path)
    return _json(result)


@mcp.tool()
def git_log(repo_path: str, max_count: int = 20, branch: str | None = None, file_path: str | None = None) -> str:
    """Get git commit log.

    Args:
        repo_path: Absolute path to the git repository
        max_count: Maximum number of commits to return (default 20)
        branch: Branch name (default: HEAD)
        file_path: Optional — limit to commits affecting this file
    """
    result = git_svc.log(repo_path, max_count=max_count, branch=branch, file_path=file_path)
    return _json({"repo": repo_path, "commits": result, "count": len(result)})


@mcp.tool()
def git_diff(repo_path: str, ref_a: str = "HEAD~1", ref_b: str = "HEAD", file_path: str | None = None) -> str:
    """Get diff between two git refs.

    Args:
        repo_path: Absolute path to the git repository
        ref_a: Starting ref (default: HEAD~1)
        ref_b: Ending ref (default: HEAD)
        file_path: Optional — limit diff to this file
    """
    result = git_svc.diff(repo_path, ref_a=ref_a, ref_b=ref_b, file_path=file_path)
    return _json(result)


@mcp.tool()
def git_blame(repo_path: str, file_path: str, rev: str = "HEAD") -> str:
    """Get git blame for a file — shows who last modified each line.

    Args:
        repo_path: Absolute path to the git repository
        file_path: Path to the file (relative to repo root)
        rev: Revision to blame (default: HEAD)
    """
    result = git_svc.blame(repo_path, file_path, rev=rev)
    return _json({"file": file_path, "lines": result, "count": len(result)})


@mcp.tool()
def git_branches(repo_path: str) -> str:
    """List branches in a git repository.

    Args:
        repo_path: Absolute path to the git repository
    """
    result = git_svc.branches(repo_path)
    return _json(result)


@mcp.tool()
def git_file_history(repo_path: str, file_path: str, max_count: int = 20) -> str:
    """Get commit history for a specific file.

    Args:
        repo_path: Absolute path to the git repository
        file_path: Path to the file (relative to repo root)
        max_count: Maximum commits to return
    """
    result = git_svc.file_history(repo_path, file_path, max_count=max_count)
    return _json({"file": file_path, "commits": result, "count": len(result)})


@mcp.tool()
def git_show_file(repo_path: str, file_path: str, ref: str = "HEAD") -> str:
    """Show file content at a specific git ref.

    Args:
        repo_path: Absolute path to the git repository
        file_path: Path to the file (relative to repo root)
        ref: Git ref (commit SHA, branch, tag) — default: HEAD
    """
    content = git_svc.show_file_at_ref(repo_path, file_path, ref=ref)
    return content


# ===================================================================
# KNOWLEDGE BASE / FILESYSTEM TOOLS
# ===================================================================


@mcp.tool()
def kb_search(query: str, root_path: str | None = None, file_pattern: str | None = None, max_results: int = 30) -> str:
    """Search file contents across the knowledge base for a text query.

    Args:
        query: Text string to search for
        root_path: Optional — limit search to this directory tree
        file_pattern: Optional glob pattern for filenames (e.g. "*.java", "pom.xml")
        max_results: Maximum results to return
    """
    results = kb.search_files(query, root_path=root_path, file_pattern=file_pattern, max_results=max_results)
    return _json({"query": query, "results": results, "count": len(results)})


@mcp.tool()
def kb_read_file(file_path: str, start_line: int = 1, end_line: int | None = None) -> str:
    """Read a file from the knowledge base. Optionally read a specific line range.

    Args:
        file_path: Absolute path to the file
        start_line: Start line number (1-based, default 1)
        end_line: End line number (optional, reads to end if omitted)
    """
    result = kb.read_file(file_path, start_line=start_line, end_line=end_line)
    return _json(result)


@mcp.tool()
def kb_list_directory(dir_path: str, recursive: bool = False, max_depth: int = 3) -> str:
    """List contents of a directory in the knowledge base.

    Args:
        dir_path: Absolute path to the directory
        recursive: Whether to list recursively (default False)
        max_depth: Maximum depth for recursive listing (default 3)
    """
    result = kb.list_directory(dir_path, recursive=recursive, max_depth=max_depth)
    return _json(result)


@mcp.tool()
def kb_find_files(name_pattern: str, root_path: str | None = None, max_results: int = 50) -> str:
    """Find files by name pattern (glob-style matching).

    Args:
        name_pattern: Glob pattern for filename (e.g. "*.java", "pom.xml", "*Test*.py")
        root_path: Optional — limit search to this directory tree
        max_results: Maximum results to return
    """
    results = kb.find_files(name_pattern, root_path=root_path, max_results=max_results)
    return _json({"pattern": name_pattern, "results": results, "count": len(results)})


@mcp.tool()
def kb_grep(
    pattern: str,
    root_path: str | None = None,
    file_pattern: str | None = None,
    is_regex: bool = False,
    max_results: int = 30,
) -> str:
    """Grep-like search through files. Supports plain text and regex.

    Args:
        pattern: Search pattern (text or regex)
        root_path: Optional — limit search to this directory tree
        file_pattern: Optional glob pattern for filenames
        is_regex: Whether pattern is a regex (default False)
        max_results: Maximum files with matches to return
    """
    results = kb.grep(pattern, root_path=root_path, file_pattern=file_pattern, is_regex=is_regex, max_results=max_results)
    return _json({"pattern": pattern, "is_regex": is_regex, "results": results, "count": len(results)})


# ===================================================================
# ENTRY POINT
# ===================================================================


def main() -> None:
    """Run the MCP server using stdio transport."""
    logger.info("Starting %s...", settings.server_name)
    logger.info("Sessions directory: %s", settings.sessions_dir)
    logger.info("Jira configured: %s", jira.configured)
    logger.info("Confluence configured: %s", confluence.configured)
    logger.info("Knowledge base roots: %s", settings.kb_roots)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
