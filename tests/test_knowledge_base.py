"""Tests for knowledge base filesystem operations."""

import tempfile
from pathlib import Path

import pytest

from mcp_context_server.knowledge_base import KnowledgeBase


@pytest.fixture
def kb_dir(tmp_path):
    """Create a temp directory with sample files."""
    # Create some files
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "Main.java").write_text("public class Main {\n    // TODO: implement\n}\n")
    (tmp_path / "src" / "Helper.java").write_text("public class Helper {\n    public void help() {}\n}\n")
    (tmp_path / "README.md").write_text("# My Project\n\nThis is a sample project for testing.\n")
    (tmp_path / "config.yaml").write_text("server:\n  port: 8080\n  host: localhost\n")
    (tmp_path / "pom.xml").write_text("<project>\n  <groupId>com.test</groupId>\n</project>\n")
    return tmp_path


@pytest.fixture
def kb(kb_dir):
    return KnowledgeBase(
        roots=[str(kb_dir)],
        extensions=[".java", ".md", ".yaml", ".xml"],
        max_file_size_kb=512,
    )


class TestKnowledgeBase:
    def test_search_files(self, kb):
        results = kb.search_files("TODO")
        assert len(results) == 1
        assert "Main.java" in results[0]["path"]

    def test_search_no_results(self, kb):
        results = kb.search_files("nonexistent_string_xyz")
        assert len(results) == 0

    def test_read_file(self, kb, kb_dir):
        result = kb.read_file(str(kb_dir / "README.md"))
        assert "My Project" in result["content"]
        assert result["total_lines"] == 3

    def test_read_file_range(self, kb, kb_dir):
        result = kb.read_file(str(kb_dir / "src" / "Main.java"), start_line=2, end_line=2)
        assert "TODO" in result["content"]
        assert result["start_line"] == 2
        assert result["end_line"] == 2

    def test_list_directory(self, kb, kb_dir):
        result = kb.list_directory(str(kb_dir))
        names = [item["name"] for item in result["items"]]
        assert "src/" in names
        assert "README.md" in names

    def test_find_files(self, kb):
        results = kb.find_files("*.java")
        assert len(results) == 2

    def test_grep(self, kb):
        results = kb.grep("class")
        assert len(results) >= 1

    def test_grep_regex(self, kb):
        results = kb.grep(r"public\s+class", is_regex=True)
        assert len(results) == 2

    def test_file_not_found(self, kb):
        with pytest.raises(FileNotFoundError):
            kb.read_file("/nonexistent/path/file.txt")
