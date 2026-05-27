"""Tests for session context management."""

import json
import tempfile
from pathlib import Path

import pytest

from mcp_context_server.sessions import ContextEntry, Session, SessionStore


@pytest.fixture
def tmp_sessions_dir(tmp_path):
    return tmp_path / "sessions"


@pytest.fixture
def store(tmp_sessions_dir):
    return SessionStore(tmp_sessions_dir)


class TestSession:
    def test_create_session(self):
        s = Session(name="Test Session", project="myproject", tags=["java"])
        assert s.name == "Test Session"
        assert s.status == "active"
        assert len(s.id) == 16

    def test_add_entry(self):
        s = Session(name="Test")
        entry = ContextEntry(summary="Found a bug", category="finding", agent="copilot")
        s.add_entry(entry)
        assert len(s.entries) == 1
        assert s.entries[0].summary == "Found a bug"

    def test_get_summary(self):
        s = Session(name="Test", project="proj")
        for i in range(5):
            s.add_entry(ContextEntry(summary=f"Entry {i}"))
        summary = s.get_summary(max_entries=3)
        assert summary["total_entries"] == 5
        assert len(summary["recent_entries"]) == 3


class TestSessionStore:
    def test_save_and_load(self, store):
        s = Session(name="Persist Test")
        s.add_entry(ContextEntry(summary="hello"))
        store.save(s)

        loaded = store.load(s.id)
        assert loaded is not None
        assert loaded.name == "Persist Test"
        assert len(loaded.entries) == 1

    def test_load_nonexistent(self, store):
        assert store.load("nonexistent12345") is None

    def test_delete(self, store):
        s = Session(name="Delete Me")
        store.save(s)
        assert store.delete(s.id) is True
        assert store.load(s.id) is None

    def test_delete_nonexistent(self, store):
        assert store.delete("nonexistent12345") is False

    def test_list_sessions(self, store):
        s1 = Session(name="Session A", project="proj1", status="active")
        s2 = Session(name="Session B", project="proj2", status="completed")
        store.save(s1)
        store.save(s2)

        all_sessions = store.list_sessions()
        assert len(all_sessions) == 2

        active = store.list_sessions(status_filter="active")
        assert len(active) == 1
        assert active[0]["name"] == "Session A"

        proj2 = store.list_sessions(project_filter="proj2")
        assert len(proj2) == 1

    def test_search_entries(self, store):
        s = Session(name="Search Test")
        s.add_entry(ContextEntry(summary="Upgraded Jackson to 2.17", category="code_change", tags=["jackson"]))
        s.add_entry(ContextEntry(summary="Fixed failing test", category="test_result", tags=["junit"]))
        s.add_entry(ContextEntry(summary="Jackson migration complete", category="progress"))
        store.save(s)

        results = store.search_entries("jackson")
        assert len(results) == 2

        results = store.search_entries("", category="test_result")
        assert len(results) == 1

        results = store.search_entries("", tags=["junit"])
        assert len(results) == 1

    def test_invalid_session_id(self, store):
        with pytest.raises(ValueError):
            store.load("../../../etc/passwd")
