---
name: java-refactoring
description: >
  **WORKFLOW SKILL** — Guide enterprise Java refactoring and library upgrade tasks.
  USE FOR: library version upgrades (Jackson, AWS SDK, JUnit, etc.); API migrations;
  Maven dependency management; module-by-module refactoring with test verification;
  deprecation workflows; breaking change assessment.
  DO NOT USE FOR: greenfield development; simple bug fixes; Python work.
  INVOKES: session context tools, git tools, kb tools, jira tools, terminal commands.
---

# Java Refactoring & Library Upgrade Skill

## Pre-Refactoring Checklist

Before starting any refactoring or library upgrade:

### 1. Gather Requirements
```
jira_get_issue("<TICKET-KEY>")         — understand scope and acceptance criteria
jira_get_comments("<TICKET-KEY>")      — check for discussion/constraints
session_list(project="<project>")      — check for prior related work
```

### 2. Create Session
```
session_create(
    name="<TICKET-KEY> <description>",
    project="mercury-services-commons",
    tags=["java", "refactoring", "<library-name>"]
)
```

### 3. Assess Impact
```
# Find all usages of the library/API being changed
kb_grep(pattern="<old-import-or-class>", file_pattern="*.java")
kb_grep(pattern="<library-artifact>", file_pattern="pom.xml")

# Check recent changes
git_log(repo_path, max_count=20)
git_file_history(repo_path, "pom.xml")
```

### 4. Document Plan
```
session_add_context(
    session_id=...,
    summary="Refactoring plan: <overview>",
    category="decision",
    detail="1. Module X first\n2. Then module Y\n...",
    references=["TICKET-KEY", "affected/files"]
)
```

## Module-by-Module Execution Order

For `mercury-services-commons`, always follow this order due to dependencies:

1. **`cloud-sdk-api`** — Core interfaces, no AWS dependency. Change here first.
2. **`dynamo-integration-test`** — Integration tests. Depends on cloud-sdk-api.
3. **`cloud-sdk-aws`** — AWS implementations. Depends on cloud-sdk-api.
4. **`commons`** — Shared utilities. depend on cloud-sdk-api and cloud-sdk-aws


### For Each Module:

```bash
# 1. Make changes to source files

# 2. Compile
mvn compile -pl <module> -am

# 3. Run unit tests
mvn test -pl <module>

# 4. Track progress
session_add_context(session_id, summary="Module <X> compilation and tests pass", category="test_result")
```

### After All Modules:

```bash
# Full build with tests
mvn clean verify

# Integration tests
mvn verify -pl dynamo-integration-test
```

## Library Upgrade Patterns

### Maven Version Update
```xml
<!-- In parent pom.xml or module pom.xml -->
<properties>
    <library.version>NEW_VERSION</library.version>
</properties>
```

### Import Migration
When a library changes packages (e.g., `javax` → `jakarta`, AWS SDK v1 → v2):
1. Find all imports: `kb_grep(pattern="import old\\.package", file_pattern="*.java")`
2. Create a mapping: old → new for each class
3. Update imports module by module
4. Fix compilation errors (API changes, method renames)
5. Run tests after each module

### Deprecation Handling
```java
// Step 1: Add @Deprecated with javadoc pointing to replacement
@Deprecated(since = "X.Y.Z", forRemoval = true)
public OldReturnType oldMethod() { ... }

// Step 2: Add new method alongside
public NewReturnType newMethod() { ... }

// Step 3: Update internal callers
// Step 4: Document in session context for downstream consumers
```

## Common Pitfalls

- **Don't change public API signatures** in `cloud-sdk-api` without deprecation period
- **Watch for transitive dependencies** — changing a version in parent POM affects all modules
- **Jackson serialization** — changing model classes can break JSON compatibility
- **Thread safety** — Dropwizard resources are shared across requests
- **Test classpath** — integration tests may need different dependency versions than unit tests

## Tracking Progress

After each significant step:
```
session_add_context(
    session_id=...,
    summary="<what was done>",
    category="code_change",  # or "test_result", "blocker", etc.
    detail="<specifics>",
    references=["changed/file/paths"]
)
```
