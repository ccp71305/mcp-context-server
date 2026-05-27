"""Session context models and persistence.

Sessions are stored as JSON files on disk, one file per session.
Each session tracks: metadata, context entries, decisions, and status.
"""

from __future__ import annotations

import json
import logging
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ContextEntry(BaseModel):
    """A single context entry within a session."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent: str = Field(default="unknown", description="Which agent added this entry")
    category: str = Field(
        default="general",
        description="Category: general, decision, finding, blocker, progress, code_change, test_result",
    )
    summary: str = Field(description="Short summary of the context")
    detail: str = Field(default="", description="Extended details, code snippets, etc.")
    tags: list[str] = Field(default_factory=list, description="Tags for filtering")
    references: list[str] = Field(default_factory=list, description="File paths, URLs, Jira keys, etc.")


class Session(BaseModel):
    """A tracked work session with context entries."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    name: str = Field(description="Human-readable session name")
    description: str = Field(default="", description="What this session is about")
    project: str = Field(default="", description="Associated project name")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = Field(default="active", description="active, paused, completed, archived")
    tags: list[str] = Field(default_factory=list)
    entries: list[ContextEntry] = Field(default_factory=list)

    def add_entry(self, entry: ContextEntry) -> None:
        self.entries.append(entry)
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def get_summary(self, max_entries: int = 20) -> dict:
        """Return a lightweight summary of this session."""
        recent = self.entries[-max_entries:] if self.entries else []
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "project": self.project,
            "status": self.status,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "total_entries": len(self.entries),
            "recent_entries": [e.model_dump() for e in recent],
        }


_SAFE_FILENAME_RE = re.compile(r"^[a-zA-Z0-9_\-]{1,64}$")


class SessionStore:
    """File-based session persistence."""

    def __init__(self, sessions_dir: Path) -> None:
        self._dir = sessions_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def _path(self, session_id: str) -> Path:
        if not _SAFE_FILENAME_RE.match(session_id):
            raise ValueError(f"Invalid session id: {session_id!r}")
        return self._dir / f"{session_id}.json"

    def save(self, session: Session) -> None:
        path = self._path(session.id)
        path.write_text(session.model_dump_json(indent=2), encoding="utf-8")
        logger.debug("Saved session %s to %s", session.id, path)

    def load(self, session_id: str) -> Session | None:
        path = self._path(session_id)
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return Session.model_validate(data)

    def delete(self, session_id: str) -> bool:
        path = self._path(session_id)
        if path.exists():
            path.unlink()
            return True
        return False

    def list_sessions(self, status_filter: str | None = None, project_filter: str | None = None) -> list[dict]:
        """List all sessions with optional filters. Returns lightweight summaries."""
        results = []
        for fp in sorted(self._dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
                session = Session.model_validate(data)
                if status_filter and session.status != status_filter:
                    continue
                if project_filter and session.project != project_filter:
                    continue
                results.append({
                    "id": session.id,
                    "name": session.name,
                    "project": session.project,
                    "status": session.status,
                    "tags": session.tags,
                    "created_at": session.created_at,
                    "updated_at": session.updated_at,
                    "entry_count": len(session.entries),
                })
            except Exception:
                logger.warning("Skipping corrupt session file: %s", fp, exc_info=True)
        return results

    def search_entries(
        self,
        query: str,
        session_id: str | None = None,
        category: str | None = None,
        tags: list[str] | None = None,
    ) -> list[dict]:
        """Search session entries by text, category, or tags."""
        query_lower = query.lower()
        results = []

        session_files = [self._path(session_id)] if session_id else self._dir.glob("*.json")

        for fp in session_files:
            if not isinstance(fp, Path) or not fp.exists():
                continue
            try:
                session = Session.model_validate(json.loads(fp.read_text(encoding="utf-8")))
                for entry in session.entries:
                    if category and entry.category != category:
                        continue
                    if tags and not set(tags).intersection(set(entry.tags)):
                        continue
                    if query_lower and query_lower not in entry.summary.lower() and query_lower not in entry.detail.lower():
                        continue
                    results.append({
                        "session_id": session.id,
                        "session_name": session.name,
                        **entry.model_dump(),
                    })
            except Exception:
                logger.warning("Error searching %s", fp, exc_info=True)

        return results[:100]  # Limit results
