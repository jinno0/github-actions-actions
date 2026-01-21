---
description: Initialize .gitignore with Claude Code specific patterns
allowed-tools: Read, Edit, Write, Bash(echo:*), Bash(cat:*), Bash(test:*)
category: workflow
---

# Initialize .gitignore for Claude Code

Set up or update the project's .gitignore file with Claude Code specific patterns.

## Patterns to Add

```gitignore
# Claude Code local files
CLAUDE.local.md
.claude/settings.local.json
.mcp.local.json

# Temporary and debug files
temp/
temp-*/
test-*/
debug-*.js
test-*.js
*-test.js
*-debug.js
```

## Current .gitignore Status

!`[ -f .gitignore ] && echo "EXISTS: .gitignore found" && echo "---CONTENTS---" && cat .gitignore || echo "MISSING: No .gitignore file found"`

## Task

Based on the above status:
1. Create `.gitignore` if it doesn't exist
2. Add all patterns that aren't already present
3. Preserve existing entries and comments
4. Report what was added

Implement this by:
1. Using the gitignore status above to determine what's missing
2. Adding missing patterns with appropriate comments
3. Preserving the existing file structure and entries