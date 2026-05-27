---
name: git-operations
description: >
  **MCP SKILL** — Access local git repositories for log, diff, blame, status, and file history.
  USE FOR: understanding recent changes to code; finding who last modified a file;
  comparing branches or commits; reviewing file history before refactoring;
  checking working tree status for uncommitted changes.
  DO NOT USE FOR: making git commits, pushing, or branching (use terminal for those).
  INVOKES: git_status, git_log, git_diff, git_blame, git_branches, git_file_history, git_show_file via MCP.
tools:
  - git_status
  - git_log
  - git_diff
  - git_blame
  - git_branches
  - git_file_history
  - git_show_file
---

# Git Operations Skill

## When to Use

- Before refactoring: check `git_log` to see recent changes to files you'll modify
- Understanding code ownership: use `git_blame` to see who wrote specific code
- Reviewing changes: use `git_diff` to see what changed between commits or branches
- Finding context: use `git_file_history` to understand evolution of a file
- Checking state: use `git_status` to see if there are uncommitted changes

## Tool Reference

### git_status
Shows current branch, dirty state, staged/modified/untracked files.
```
git_status(repo_path="C:\\Users\\akundu\\projects\\mercury-services-commons")
```

### git_log
Recent commits. Optionally filter by branch or file.
```
git_log(repo_path="...", max_count=10)
git_log(repo_path="...", branch="main", file_path="cloud-sdk-api/pom.xml")
```

### git_diff
Compare two refs. Shows actual patch content.
```
git_diff(repo_path="...", ref_a="main", ref_b="HEAD")
git_diff(repo_path="...", ref_a="HEAD~5", ref_b="HEAD", file_path="path/to/file.java")
```

### git_blame
Line-by-line attribution. Who changed each line and when.
```
git_blame(repo_path="...", file_path="cloud-sdk-api/src/main/java/com/example/MyClass.java")
```

### git_branches
List local and remote branches, show current branch.
```
git_branches(repo_path="...")
```

### git_file_history
Commit history filtered to a specific file.
```
git_file_history(repo_path="...", file_path="pom.xml", max_count=15)
```

### git_show_file
View file content at any historical ref (commit, tag, branch).
```
git_show_file(repo_path="...", file_path="pom.xml", ref="main")
git_show_file(repo_path="...", file_path="pom.xml", ref="abc1234")
```

## Workflow: Pre-Refactoring Assessment

```
1. git_status(repo)                  — ensure clean working tree
2. git_log(repo, max_count=20)       — recent activity overview
3. git_file_history(repo, "target_file.java")  — understand file evolution
4. git_blame(repo, "target_file.java")         — identify code owners
5. git_diff(repo, ref_a="main", ref_b="HEAD")  — see current branch changes
```
