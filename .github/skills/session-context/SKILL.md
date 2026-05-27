---
name: session-context
description: >
  **MCP SKILL** — Manage persistent session contexts across agent conversations.
  USE FOR: starting work on a Jira ticket; resuming multi-conversation refactoring;
  tracking decisions, findings, blockers, and progress across agent sessions;
  searching historical context from previous conversations.
  DO NOT USE FOR: one-shot questions; simple code lookups; tasks completed in a single exchange.
  INVOKES: session_create, session_get, session_list, session_add_context, session_update_status, session_search, session_delete via MCP.
tools:
  - session_create
  - session_get
  - session_list
  - session_add_context
  - session_update_status
  - session_search
  - session_delete
---

# Session Context Management Skill

## When to Use

Activate this skill whenever:
- You are starting work that spans multiple conversations (refactoring, upgrades, migrations)
- The user mentions a Jira ticket or feature branch that implies ongoing work
- You need to recall what was done in a previous conversation
- The user asks to "continue where we left off" or "what did we do last time"

## Workflow

### Starting a New Task
```
1. session_list(status="active", project="<project>")  — check for existing sessions
2. If found: session_get(session_id) — load context
3. If not found: session_create(name="<ticket> <description>", project="<project>", tags=[...])
```

### During Work
After every significant action, call:
```
session_add_context(
    session_id="<id>",
    summary="<what happened>",
    category="<decision|finding|blocker|progress|code_change|test_result>",
    detail="<extended info, code snippets, error messages>",
    agent="copilot-claude-opus",
    references=["file/paths", "JIRA-123", "urls"]
)
```

### Ending a Conversation
```
session_add_context(session_id, summary="Session paused: <state>", category="progress")
# If task complete:
session_update_status(session_id, status="completed")
```

### Searching Context
```
session_search(query="jackson upgrade", category="decision")
session_search(query="", tags=["blockers"])
```

## Categories Reference

| Category | When to Use |
|---|---|
| `general` | Default, miscellaneous context |
| `decision` | Architectural or implementation decisions made |
| `finding` | Discoveries about the codebase, bugs found, patterns identified |
| `blocker` | Issues that blocked progress, workarounds needed |
| `progress` | Milestones, completed steps, status updates |
| `code_change` | Files modified, refactoring performed |
| `test_result` | Test runs, pass/fail results, coverage changes |

## Best Practices

- Keep summaries concise (1-2 sentences). Put details in the `detail` field.
- Always include file paths and Jira keys in `references`.
- Use consistent tags across sessions (e.g., `java`, `refactoring`, `aws`, `junit`).
- Add a context entry before AND after risky operations.
- When resuming, read the last 5-10 entries to rebuild mental model.
