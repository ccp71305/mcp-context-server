---
name: jira-confluence
description: >
  **MCP SKILL** — Interact with Jira issues and Confluence documentation.
  USE FOR: looking up Jira ticket details, requirements, and acceptance criteria;
  searching Jira with JQL; reading Confluence architecture docs, runbooks, ADRs;
  adding comments to Jira issues to document progress.
  DO NOT USE FOR: creating Jira issues (not supported); modifying Confluence pages.
  INVOKES: jira_get_issue, jira_search, jira_get_comments, jira_add_comment,
  confluence_get_page, confluence_search, confluence_space_pages, confluence_page_children via MCP.
tools:
  - jira_get_issue
  - jira_search
  - jira_get_comments
  - jira_add_comment
  - confluence_get_page
  - confluence_search
  - confluence_space_pages
  - confluence_page_children
---

# Jira & Confluence Integration Skill

## When to Use

### Jira
- User mentions a Jira ticket key (e.g., ION-12310, PLAT-456)
- Need to understand requirements or acceptance criteria for a task
- Want to check the status of related tickets
- Need to find tickets by label, component, or sprint

### Confluence
- Looking for architecture decision records (ADRs)
- Need runbooks or deployment procedures
- Searching for migration guides or API documentation
- Looking up team conventions or standards

## Common JQL Patterns

```
# Issues assigned to current user in active sprint
assignee = currentUser() AND sprint in openSprints()

# Recently updated issues in a project
project = ION AND updated >= -7d ORDER BY updated DESC

# Bugs in a specific component
project = ION AND issuetype = Bug AND component = "cloud-sdk"

# Issues with a specific label
labels = "library-upgrade" AND status != Done

# Search by text
text ~ "DynamoDB migration"
```

## Common CQL Patterns (Confluence)

```
# Search by text in a space
type = page AND space = DEV AND text ~ "migration guide"

# Architecture decisions
type = page AND label = "architecture-decision-record"

# Recently modified runbooks
type = page AND label = "runbook" AND lastModified >= "2024-01-01"
```

## Workflow: Starting a Jira-Tracked Task

```
1. jira_get_issue("ION-12310")           — get requirements
2. jira_get_comments("ION-12310")        — check for discussion/clarifications
3. session_create(name="ION-12310 ...")   — create session to track work
4. confluence_search('text ~ "related topic"')  — find related docs
5. ... do the work ...
6. jira_add_comment("ION-12310", "Completed: <summary of changes>")
```

## Configuration Required

Set these environment variables (or in `.env`):
```
MCP_JIRA_BASE_URL=https://yourorg.atlassian.net
MCP_JIRA_EMAIL=your.email@company.com
MCP_JIRA_API_TOKEN=<your-api-token>
MCP_CONFLUENCE_BASE_URL=https://yourorg.atlassian.net/wiki
MCP_CONFLUENCE_EMAIL=your.email@company.com
MCP_CONFLUENCE_API_TOKEN=<your-api-token>
```

Generate API tokens at: https://id.atlassian.com/manage-profile/security/api-tokens
