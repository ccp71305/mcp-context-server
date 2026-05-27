"""Configuration management using pydantic-settings.

Settings are loaded from environment variables and/or a .env file.
"""

import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MCP_",
        extra="ignore",
    )

    # --- Session Storage ---
    sessions_dir: Path = Field(
        default_factory=lambda: Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or str(Path.home())) / ".mcp-context-server" / "sessions",
        description="Directory to persist session context files",
    )

    # --- Jira ---
    jira_base_url: str = Field(default="", description="Jira base URL (e.g. https://myorg.atlassian.net)")
    jira_email: str = Field(default="", description="Jira user email for API auth")
    jira_api_token: str = Field(default="", description="Jira API token")

    # --- Confluence ---
    confluence_base_url: str = Field(default="", description="Confluence base URL")
    confluence_email: str = Field(default="", description="Confluence user email")
    confluence_api_token: str = Field(default="", description="Confluence API token")

    # --- Git ---
    git_default_repos: list[str] = Field(
        default_factory=list,
        description="List of default git repo paths to index",
    )

    # --- Knowledge Base ---
    kb_roots: list[str] = Field(
        default_factory=list,
        description="List of filesystem roots to search for knowledge base content",
    )
    kb_file_extensions: list[str] = Field(
        default_factory=lambda: [
            ".md", ".txt", ".rst", ".java", ".py", ".xml", ".json", ".yaml", ".yml",
            ".properties", ".gradle", ".toml", ".cfg", ".ini", ".sh", ".bat",
        ],
        description="File extensions to index in the knowledge base",
    )
    kb_max_file_size_kb: int = Field(default=512, description="Max file size in KB to index")

    # --- Server ---
    server_name: str = Field(default="mcp-context-server", description="MCP server name")
    log_level: str = Field(default="INFO", description="Logging level")


def get_settings() -> Settings:
    """Load and return application settings."""
    return Settings()
