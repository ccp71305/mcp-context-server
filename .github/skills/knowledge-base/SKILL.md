---
name: knowledge-base
description: >
  **MCP SKILL** — Search and read files across local filesystem knowledge bases.
  USE FOR: finding code patterns across projects; searching documentation and config files;
  reading files from any configured directory; finding files by name pattern;
  grep-like text search with regex support.
  DO NOT USE FOR: modifying files (use editor tools); searching git history (use git-operations skill).
  INVOKES: kb_search, kb_read_file, kb_list_directory, kb_find_files, kb_grep via MCP.
tools:
  - kb_search
  - kb_read_file
  - kb_list_directory
  - kb_find_files
  - kb_grep
---

# Knowledge Base & Filesystem Skill

## When to Use

- Searching for code patterns across multiple projects
- Finding configuration files, documentation, or examples
- Reading files that aren't in the current workspace
- Exploring directory structures
- Grep-like search with regex support

## Tool Reference

### kb_search
Full-text search across knowledge base roots. Returns matching files with line numbers.
```
kb_search(query="CloudAttributeValue", file_pattern="*.java")
kb_search(query="DynamoDB", root_path="C:\\Users\\akundu\\projects")
```

### kb_read_file
Read a file's content, optionally a specific line range.
```
kb_read_file(file_path="C:\\Users\\akundu\\projects\\myproject\\pom.xml")
kb_read_file(file_path="...", start_line=10, end_line=50)
```

### kb_list_directory
List directory contents with optional recursion.
```
kb_list_directory(dir_path="C:\\Users\\akundu\\projects\\mercury-services-commons")
kb_list_directory(dir_path="...", recursive=True, max_depth=2)
```

### kb_find_files
Find files by name pattern (glob-style).
```
kb_find_files(name_pattern="pom.xml")
kb_find_files(name_pattern="*Test*.java", root_path="C:\\Users\\akundu\\projects")
kb_find_files(name_pattern="*.md")
```

### kb_grep
Grep-like search. Supports plain text and regex.
```
kb_grep(pattern="@Deprecated", file_pattern="*.java")
kb_grep(pattern="import\\s+software\\.amazon", is_regex=True)
kb_grep(pattern="<version>2\\.1[0-9]", is_regex=True, file_pattern="pom.xml")
```

## Workflow: Finding All Usages of a Pattern

```
1. kb_grep(pattern="OldClassName", file_pattern="*.java")     — find all usages
2. kb_grep(pattern="OldClassName", file_pattern="*.xml")       — check configs too
3. kb_read_file(file_path, start_line=X, end_line=Y)           — read context around each usage
```

## Workflow: Project Exploration

```
1. kb_list_directory(dir_path, recursive=True, max_depth=2)    — get structure overview
2. kb_find_files(name_pattern="pom.xml")                       — find all Maven modules
3. kb_search(query="main class", file_pattern="*.java")        — find entry points
```

## Configuration

Knowledge base roots are configured in environment:
```
MCP_KB_ROOTS=["C:\\Users\\akundu\\projects","C:\\Users\\akundu\\docs"]
MCP_KB_FILE_EXTENSIONS=[".md",".java",".py",".xml",".json",".yaml"]
MCP_KB_MAX_FILE_SIZE_KB=512
```
