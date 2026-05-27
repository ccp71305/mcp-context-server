"""Filesystem knowledge base search and indexing.

Provides tools to search through local files, read content, and build
lightweight indexes for quick lookup during agent sessions.
"""

from __future__ import annotations

import fnmatch
import logging
import os
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Search and read files from configured filesystem roots."""

    def __init__(
        self,
        roots: list[str],
        extensions: list[str],
        max_file_size_kb: int = 512,
    ) -> None:
        self._roots = [Path(r).resolve() for r in roots if Path(r).is_dir()]
        self._extensions = set(extensions)
        self._max_size = max_file_size_kb * 1024

    def _is_indexable(self, path: Path) -> bool:
        if path.suffix.lower() not in self._extensions:
            return False
        try:
            if path.stat().st_size > self._max_size:
                return False
        except OSError:
            return False
        return True

    def _iter_files(self, root: Path, pattern: str | None = None) -> list[Path]:
        """Walk a root directory and yield matching files."""
        results: list[Path] = []
        skip_dirs = {".git", "node_modules", "__pycache__", ".idea", ".vscode",
                     "target", "build", "dist", ".gradle", "venv", ".venv", ".tox"}
        for dirpath, dirnames, filenames in os.walk(root):
            # Prune hidden/build directories
            dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith(".")]
            for fname in filenames:
                fp = Path(dirpath) / fname
                if not self._is_indexable(fp):
                    continue
                if pattern and not fnmatch.fnmatch(fname.lower(), pattern.lower()):
                    continue
                results.append(fp)
                if len(results) >= 5000:
                    return results
        return results

    def search_files(
        self,
        query: str,
        root_path: str | None = None,
        file_pattern: str | None = None,
        max_results: int = 30,
    ) -> list[dict]:
        """Search file contents for a text query across knowledge base roots."""
        query_lower = query.lower()
        roots = [Path(root_path).resolve()] if root_path else self._roots
        results: list[dict] = []

        for root in roots:
            if not root.is_dir():
                continue
            for fp in self._iter_files(root, file_pattern):
                try:
                    content = fp.read_text(encoding="utf-8", errors="replace")
                    if query_lower in content.lower():
                        # Find matching lines
                        matches = []
                        for i, line in enumerate(content.splitlines(), 1):
                            if query_lower in line.lower():
                                matches.append({"line": i, "text": line.strip()[:200]})
                                if len(matches) >= 5:
                                    break
                        results.append({
                            "path": str(fp),
                            "relative_path": str(fp.relative_to(root)),
                            "matches": matches,
                        })
                        if len(results) >= max_results:
                            return results
                except Exception:
                    continue

        return results

    def read_file(self, file_path: str, start_line: int = 1, end_line: int | None = None) -> dict:
        """Read a file's content, optionally a specific line range."""
        fp = Path(file_path).resolve()
        if not fp.is_file():
            raise FileNotFoundError(f"File not found: {fp}")

        # Validate the path is under one of the allowed roots or is absolute
        content = fp.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()

        start = max(1, start_line) - 1
        end = end_line if end_line else len(lines)
        selected = lines[start:end]

        return {
            "path": str(fp),
            "total_lines": len(lines),
            "start_line": start + 1,
            "end_line": min(end, len(lines)),
            "content": "\n".join(selected),
        }

    def list_directory(self, dir_path: str, recursive: bool = False, max_depth: int = 3) -> dict:
        """List directory contents."""
        dp = Path(dir_path).resolve()
        if not dp.is_dir():
            raise FileNotFoundError(f"Directory not found: {dp}")

        items: list[dict] = []

        def _list(path: Path, depth: int) -> None:
            if depth > max_depth:
                return
            try:
                for entry in sorted(path.iterdir()):
                    name = entry.name
                    if name.startswith(".") or name in {"node_modules", "__pycache__", "target", ".git"}:
                        continue
                    if entry.is_dir():
                        items.append({"name": name + "/", "type": "directory", "path": str(entry)})
                        if recursive and depth < max_depth:
                            _list(entry, depth + 1)
                    elif entry.is_file():
                        try:
                            size = entry.stat().st_size
                        except OSError:
                            size = 0
                        items.append({"name": name, "type": "file", "path": str(entry), "size": size})
            except PermissionError:
                pass

        _list(dp, 1)
        return {
            "path": str(dp),
            "item_count": len(items),
            "items": items[:500],
        }

    def find_files(
        self,
        name_pattern: str,
        root_path: str | None = None,
        max_results: int = 50,
    ) -> list[dict]:
        """Find files by name pattern (glob-style)."""
        roots = [Path(root_path).resolve()] if root_path else self._roots
        results: list[dict] = []

        for root in roots:
            if not root.is_dir():
                continue
            for fp in self._iter_files(root, name_pattern):
                results.append({
                    "path": str(fp),
                    "relative_path": str(fp.relative_to(root)),
                    "size": fp.stat().st_size,
                })
                if len(results) >= max_results:
                    return results

        return results

    def grep(
        self,
        pattern: str,
        root_path: str | None = None,
        file_pattern: str | None = None,
        is_regex: bool = False,
        max_results: int = 30,
    ) -> list[dict]:
        """Grep-like search through files. Supports regex patterns."""
        if is_regex:
            try:
                compiled = re.compile(pattern, re.IGNORECASE)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}")
            match_fn = compiled.search
        else:
            pattern_lower = pattern.lower()
            match_fn = lambda line: pattern_lower in line.lower()  # noqa: E731

        roots = [Path(root_path).resolve()] if root_path else self._roots
        results: list[dict] = []

        for root in roots:
            if not root.is_dir():
                continue
            for fp in self._iter_files(root, file_pattern):
                try:
                    file_matches = []
                    for i, line in enumerate(fp.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                        if match_fn(line):
                            file_matches.append({"line": i, "text": line.strip()[:200]})
                            if len(file_matches) >= 10:
                                break
                    if file_matches:
                        results.append({
                            "path": str(fp),
                            "relative_path": str(fp.relative_to(root)),
                            "matches": file_matches,
                        })
                        if len(results) >= max_results:
                            return results
                except Exception:
                    continue

        return results
