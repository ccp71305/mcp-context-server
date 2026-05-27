"""Confluence integration via REST API v2 / v1 (Cloud and Server/DC).

All calls are async using httpx.
"""

from __future__ import annotations

import base64
import logging
import re

import httpx

logger = logging.getLogger(__name__)


def _strip_html(html: str) -> str:
    """Remove HTML tags, keeping text content."""
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()


class ConfluenceClient:
    """Async Confluence REST API client."""

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

    async def get_page(self, page_id: str) -> dict:
        """Fetch a Confluence page by ID with body content."""
        client = await self._get_client()
        resp = await client.get(
            f"/rest/api/content/{page_id}",
            params={"expand": "body.storage,version,space,ancestors"},
        )
        resp.raise_for_status()
        data = resp.json()
        body_html = data.get("body", {}).get("storage", {}).get("value", "")
        return {
            "id": data.get("id"),
            "title": data.get("title", ""),
            "space_key": data.get("space", {}).get("key", ""),
            "version": data.get("version", {}).get("number", 0),
            "body_text": _strip_html(body_html),
            "url": f"{self._base_url}{data.get('_links', {}).get('webui', '')}",
            "ancestors": [
                {"id": a.get("id"), "title": a.get("title", "")}
                for a in data.get("ancestors", [])
            ],
        }

    async def search(self, cql: str, max_results: int = 20) -> list[dict]:
        """Search Confluence using CQL."""
        client = await self._get_client()
        resp = await client.get(
            "/rest/api/content/search",
            params={"cql": cql, "limit": min(max_results, 50), "expand": "space,version"},
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("results", []):
            results.append({
                "id": item.get("id"),
                "title": item.get("title", ""),
                "type": item.get("type", ""),
                "space_key": item.get("space", {}).get("key", ""),
                "version": item.get("version", {}).get("number", 0),
                "url": f"{self._base_url}{item.get('_links', {}).get('webui', '')}",
            })
        return results

    async def get_space_pages(self, space_key: str, max_results: int = 50) -> list[dict]:
        """List pages in a Confluence space."""
        client = await self._get_client()
        resp = await client.get(
            "/rest/api/content",
            params={
                "spaceKey": space_key,
                "type": "page",
                "limit": min(max_results, 100),
                "expand": "version",
                "orderby": "title",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return [
            {
                "id": p.get("id"),
                "title": p.get("title", ""),
                "version": p.get("version", {}).get("number", 0),
            }
            for p in data.get("results", [])
        ]

    async def get_page_children(self, page_id: str) -> list[dict]:
        """Get child pages of a given page."""
        client = await self._get_client()
        resp = await client.get(
            f"/rest/api/content/{page_id}/child/page",
            params={"limit": 100, "expand": "version"},
        )
        resp.raise_for_status()
        data = resp.json()
        return [
            {
                "id": p.get("id"),
                "title": p.get("title", ""),
                "version": p.get("version", {}).get("number", 0),
            }
            for p in data.get("results", [])
        ]

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
