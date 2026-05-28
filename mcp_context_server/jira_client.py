"""Jira integration via REST API v3 (Atlassian Cloud) or v2 (Server/DC).

All calls are async using httpx.
"""

from __future__ import annotations

import base64
import logging
from html.parser import HTMLParser
from io import StringIO

import httpx

logger = logging.getLogger(__name__)


class _HTMLTextExtractor(HTMLParser):
    """Simple HTML-to-text converter for Jira description fields."""

    def __init__(self) -> None:
        super().__init__()
        self._result = StringIO()

    def handle_data(self, data: str) -> None:
        self._result.write(data)

    def get_text(self) -> str:
        return self._result.getvalue().strip()


def _html_to_text(html: str) -> str:
    if not html:
        return ""
    parser = _HTMLTextExtractor()
    parser.feed(html)
    return parser.get_text()


class JiraClient:
    """Async Jira REST API client."""

    def __init__(self, base_url: str, email: str, api_token: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._auth_header = self._make_auth_header(email, api_token)
        self._client: httpx.AsyncClient | None = None

    @staticmethod
    def _make_auth_header(email: str, token: str) -> str:
        creds = base64.b64encode(f"{email}:{token}".encode()).decode()
        return f"Basic {creds}"

    @property
    def configured(self) -> bool:
        return bool(self._base_url and self._auth_header and self._auth_header != "Basic Og==")

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                headers={
                    "Authorization": self._auth_header,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                timeout=30.0,
            )
        return self._client

    async def get_issue(self, issue_key: str) -> dict:
        """Fetch a single Jira issue by key (e.g., PROJ-123)."""
        client = await self._get_client()
        resp = await client.get(f"/rest/api/2/issue/{issue_key}")
        resp.raise_for_status()
        data = resp.json()
        fields = data.get("fields", {})

        # Extract description text
        description = ""
        desc_field = fields.get("description")
        if isinstance(desc_field, dict):
            # ADF format - extract text content
            description = self._extract_adf_text(desc_field)
        elif isinstance(desc_field, str):
            description = _html_to_text(desc_field)

        return {
            "key": data.get("key"),
            "summary": fields.get("summary", ""),
            "description": description,
            "status": fields.get("status", {}).get("name", ""),
            "assignee": (fields.get("assignee") or {}).get("displayName", "Unassigned"),
            "reporter": (fields.get("reporter") or {}).get("displayName", ""),
            "priority": (fields.get("priority") or {}).get("name", ""),
            "issue_type": (fields.get("issuetype") or {}).get("name", ""),
            "labels": fields.get("labels", []),
            "created": fields.get("created", ""),
            "updated": fields.get("updated", ""),
            "components": [c.get("name", "") for c in fields.get("components", [])],
            "subtasks": [
                {"key": st.get("key"), "summary": st.get("fields", {}).get("summary", "")}
                for st in fields.get("subtasks", [])
            ],
        }

    async def search_issues(self, jql: str, max_results: int = 25) -> list[dict]:
        """Search issues using JQL."""
        client = await self._get_client()
        resp = await client.get(
            "/rest/api/2/search",
            params={"jql": jql, "maxResults": min(max_results, 100), "fields": "summary,status,assignee,priority,issuetype,labels,updated"},
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for issue in data.get("issues", []):
            fields = issue.get("fields", {})
            results.append({
                "key": issue.get("key"),
                "summary": fields.get("summary", ""),
                "status": (fields.get("status") or {}).get("name", ""),
                "assignee": (fields.get("assignee") or {}).get("displayName", "Unassigned"),
                "priority": (fields.get("priority") or {}).get("name", ""),
                "type": (fields.get("issuetype") or {}).get("name", ""),
                "labels": fields.get("labels", []),
                "updated": fields.get("updated", ""),
            })
        return results

    async def get_issue_comments(self, issue_key: str, max_results: int = 20) -> list[dict]:
        """Get comments on an issue."""
        client = await self._get_client()
        resp = await client.get(
            f"/rest/api/2/issue/{issue_key}/comment",
            params={"maxResults": max_results, "orderBy": "-created"},
        )
        resp.raise_for_status()
        data = resp.json()
        comments = []
        for c in data.get("comments", []):
            body = c.get("body", "")
            if isinstance(body, dict):
                body = self._extract_adf_text(body)
            elif isinstance(body, str):
                body = _html_to_text(body)
            comments.append({
                "author": (c.get("author") or {}).get("displayName", ""),
                "created": c.get("created", ""),
                "body": body,
            })
        return comments

    async def add_comment(self, issue_key: str, body: str) -> dict:
        """Add a comment to an issue."""
        client = await self._get_client()
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": body}]}],
            }
        }
        resp = await client.post(f"/rest/api/2/issue/{issue_key}/comment", json=payload)
        resp.raise_for_status()
        return {"status": "ok", "issue_key": issue_key}

    @staticmethod
    def _extract_adf_text(adf: dict) -> str:
        """Recursively extract text from Atlassian Document Format."""
        texts = []

        def _walk(node: dict | list) -> None:
            if isinstance(node, list):
                for item in node:
                    _walk(item)
                return
            if isinstance(node, dict):
                if node.get("type") == "text":
                    texts.append(node.get("text", ""))
                for child in node.get("content", []):
                    _walk(child)

        _walk(adf)
        return " ".join(texts)

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
