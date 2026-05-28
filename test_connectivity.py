"""Quick connectivity test for Jira and Confluence."""

import asyncio
import sys
import os

# Ensure .env is loaded from the project root
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from mcp_context_server.config import Settings
from mcp_context_server.jira_client import JiraClient
from mcp_context_server.confluence_client import ConfluenceClient


async def test_jira(settings: Settings) -> bool:
    """Test Jira connectivity by fetching server info."""
    print("\n=== JIRA CONNECTIVITY TEST ===")
    print(f"  Base URL : {settings.jira_base_url}")
    print(f"  User     : {settings.jira_email}")
    print(f"  Configured: {bool(settings.jira_base_url and settings.jira_email and settings.jira_api_token)}")

    if not settings.jira_base_url:
        print("  SKIP: No Jira base URL configured")
        return False

    client = JiraClient(settings.jira_base_url, settings.jira_email, settings.jira_api_token)
    try:
        # Try the server info endpoint (works on both Cloud and Server/DC)
        http = await client._get_client()

        # Test 1: Server info (v2 — works on Server/DC)
        print("\n  [1] Fetching Jira server info (/rest/api/2/serverInfo) ...")
        resp = await http.get("/rest/api/2/serverInfo")
        if resp.status_code == 200:
            info = resp.json()
            print(f"      OK — Server: {info.get('serverTitle', 'N/A')}, Version: {info.get('version', 'N/A')}")
        else:
            print(f"      WARN — Status {resp.status_code}: {resp.text[:200]}")

        # Test 2: Current user / myself
        print("\n  [2] Fetching current user (/rest/api/2/myself) ...")
        resp = await http.get("/rest/api/2/myself")
        if resp.status_code == 200:
            user = resp.json()
            print(f"      OK — Logged in as: {user.get('displayName', 'N/A')} ({user.get('emailAddress', 'N/A')})")
        else:
            print(f"      FAIL — Status {resp.status_code}: {resp.text[:200]}")
            return False

        # Test 3: Quick JQL search (recent issues)
        print("\n  [3] Running JQL search (order by updated, max 3) ...")
        resp = await http.get("/rest/api/2/search", params={"jql": "order by updated DESC", "maxResults": 3, "fields": "summary,status"})
        if resp.status_code == 200:
            data = resp.json()
            total = data.get("total", 0)
            issues = data.get("issues", [])
            print(f"      OK — Total issues visible: {total}")
            for issue in issues:
                key = issue.get("key")
                summary = issue.get("fields", {}).get("summary", "")
                status = issue.get("fields", {}).get("status", {}).get("name", "")
                print(f"      - {key}: {summary} [{status}]")
        else:
            print(f"      FAIL — Status {resp.status_code}: {resp.text[:200]}")

        print("\n  JIRA: CONNECTED SUCCESSFULLY")
        return True

    except Exception as e:
        print(f"\n  JIRA: CONNECTION FAILED — {type(e).__name__}: {e}")
        return False
    finally:
        await client.close()


async def test_confluence(settings: Settings) -> bool:
    """Test Confluence connectivity."""
    print("\n=== CONFLUENCE CONNECTIVITY TEST ===")
    print(f"  Base URL : {settings.confluence_base_url}")
    print(f"  User     : {settings.confluence_email}")
    print(f"  Configured: {bool(settings.confluence_base_url and settings.confluence_email and settings.confluence_api_token)}")

    if not settings.confluence_base_url:
        print("  SKIP: No Confluence base URL configured")
        return False

    client = ConfluenceClient(settings.confluence_base_url, settings.confluence_email, settings.confluence_api_token)
    try:
        http = await client._get_client()

        # Test 1: Get spaces (v1 API — works on Server/DC)
        print("\n  [1] Listing Confluence spaces (/rest/api/space?limit=5) ...")
        resp = await http.get("/rest/api/space", params={"limit": 5})
        if resp.status_code == 200:
            data = resp.json()
            spaces = data.get("results", [])
            print(f"      OK — Found {len(spaces)} space(s):")
            for s in spaces:
                print(f"      - {s.get('key', '?')}: {s.get('name', 'N/A')}")
        else:
            print(f"      FAIL — Status {resp.status_code}: {resp.text[:200]}")
            return False

        # Test 2: CQL search
        print("\n  [2] Running CQL search (type=page, limit 3) ...")
        resp = await http.get("/rest/api/content/search", params={"cql": "type=page order by lastmodified desc", "limit": 3})
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            print(f"      OK — Found {len(results)} page(s):")
            for p in results:
                print(f"      - [{p.get('space', {}).get('key', '?')}] {p.get('title', 'N/A')}")
        else:
            print(f"      WARN — CQL search status {resp.status_code}: {resp.text[:200]}")

        print("\n  CONFLUENCE: CONNECTED SUCCESSFULLY")
        return True

    except Exception as e:
        print(f"\n  CONFLUENCE: CONNECTION FAILED — {type(e).__name__}: {e}")
        return False
    finally:
        await client.close()


async def main():
    print("Loading settings from .env ...")
    settings = Settings()

    jira_ok = await test_jira(settings)
    conf_ok = await test_confluence(settings)

    print("\n" + "=" * 40)
    print(f"  Jira       : {'PASS' if jira_ok else 'FAIL'}")
    print(f"  Confluence : {'PASS' if conf_ok else 'FAIL'}")
    print("=" * 40)

    if not (jira_ok and conf_ok):
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
