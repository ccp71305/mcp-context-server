"""Git repository integration using GitPython.

Provides structured access to git log, diff, status, blame, and branch info.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from git import InvalidGitRepositoryError, Repo  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


class GitService:
    """Interact with local git repositories."""

    @staticmethod
    def _open_repo(repo_path: str) -> Repo:
        p = Path(repo_path).resolve()
        if not p.is_dir():
            raise FileNotFoundError(f"Repository path does not exist: {p}")
        try:
            return Repo(p, search_parent_directories=True)
        except InvalidGitRepositoryError as exc:
            raise ValueError(f"Not a git repository: {p}") from exc

    @staticmethod
    def status(repo_path: str) -> dict:
        """Get working tree status."""
        repo = GitService._open_repo(repo_path)
        return {
            "repo": str(repo.working_dir),
            "branch": str(repo.active_branch) if not repo.head.is_detached else "DETACHED",
            "is_dirty": repo.is_dirty(),
            "untracked_files": repo.untracked_files[:50],
            "staged": [item.a_path for item in repo.index.diff("HEAD")][:50] if repo.head.is_valid() else [],
            "modified": [item.a_path for item in repo.index.diff(None)][:50],
        }

    @staticmethod
    def log(repo_path: str, max_count: int = 20, branch: str | None = None, file_path: str | None = None) -> list[dict]:
        """Get git log entries."""
        repo = GitService._open_repo(repo_path)
        kwargs: dict = {"max_count": min(max_count, 100)}
        if file_path:
            kwargs["paths"] = file_path

        rev = branch or "HEAD"
        commits = []
        for c in repo.iter_commits(rev, **kwargs):
            commits.append({
                "sha": c.hexsha[:12],
                "message": c.message.strip()[:200],
                "author": str(c.author),
                "date": c.committed_datetime.isoformat(),
                "files_changed": len(c.stats.files) if c.stats else 0,
            })
        return commits

    @staticmethod
    def diff(repo_path: str, ref_a: str = "HEAD~1", ref_b: str = "HEAD", file_path: str | None = None) -> dict:
        """Get diff between two refs."""
        repo = GitService._open_repo(repo_path)
        commit_a = repo.commit(ref_a)
        commit_b = repo.commit(ref_b)
        diffs = commit_a.diff(commit_b, create_patch=True)

        file_diffs = []
        for d in diffs:
            path = d.a_path or d.b_path
            if file_path and path != file_path:
                continue
            diff_text = ""
            try:
                diff_text = d.diff.decode("utf-8", errors="replace")[:5000]
            except Exception:
                diff_text = "<binary or undecodable>"
            file_diffs.append({
                "path": path,
                "change_type": d.change_type,
                "diff": diff_text,
            })

        return {
            "ref_a": ref_a,
            "ref_b": ref_b,
            "file_count": len(file_diffs),
            "files": file_diffs[:50],
        }

    @staticmethod
    def blame(repo_path: str, file_path: str, rev: str = "HEAD") -> list[dict]:
        """Get blame information for a file."""
        repo = GitService._open_repo(repo_path)
        blame_data = repo.blame(rev, file_path)
        results = []
        line_num = 1
        for commit, lines in blame_data:
            for line in lines:
                results.append({
                    "line": line_num,
                    "sha": commit.hexsha[:12],
                    "author": str(commit.author),
                    "date": commit.committed_datetime.isoformat(),
                    "text": str(line).rstrip()[:200],
                })
                line_num += 1
            if line_num > 500:
                break
        return results

    @staticmethod
    def branches(repo_path: str) -> dict:
        """List branches."""
        repo = GitService._open_repo(repo_path)
        current = str(repo.active_branch) if not repo.head.is_detached else "DETACHED"
        local = [str(b) for b in repo.branches]
        remote = [str(r) for r in repo.remotes.origin.refs] if repo.remotes else []
        return {
            "current": current,
            "local": local,
            "remote": remote[:50],
        }

    @staticmethod
    def file_history(repo_path: str, file_path: str, max_count: int = 20) -> list[dict]:
        """Get commit history for a specific file."""
        return GitService.log(repo_path, max_count=max_count, file_path=file_path)

    @staticmethod
    def show_file_at_ref(repo_path: str, file_path: str, ref: str = "HEAD") -> str:
        """Show file content at a specific ref."""
        repo = GitService._open_repo(repo_path)
        commit = repo.commit(ref)
        try:
            blob = commit.tree / file_path
            content = blob.data_stream.read().decode("utf-8", errors="replace")
            return content[:50000]  # Limit size
        except KeyError:
            raise FileNotFoundError(f"File {file_path} not found at ref {ref}")
