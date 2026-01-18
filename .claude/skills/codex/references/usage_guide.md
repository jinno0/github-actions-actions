# Codex CLI Usage Guide

## Overview

OpenAI Codex CLI is a command-line tool that provides AI-powered code review, analysis, and Q&A capabilities.

## Basic Command Structure

```bash
codex exec --full-auto --sandbox read-only --cd <project_directory> "<request>"
```

## Command Options

| Option | Description |
|--------|-------------|
| `--full-auto` | Run in fully automated mode without user interaction |
| `--sandbox` | Set sandbox mode (`read-only` for safe analysis) |
| `--cd <dir>` | Specify the project directory to analyze |
| `<request>` | The request/question in natural language |

## Sandbox Modes

- **read-only**: Safe for code review and analysis (recommended)
  - Cannot modify files
  - Cannot execute arbitrary commands
  - Can only read and analyze code

- **write**: Allows modifications (use with caution)
  - Can edit files
  - Can create new files
  - Risky for production codebases

## Common Use Cases

### 1. Code Review

```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "Review this codebase and identify potential issues"
```

### 2. Bug Investigation

```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "Investigate why the authentication is failing"
```

### 3. Architecture Analysis

```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "Analyze the architecture and identify potential improvements"
```

### 4. Security Review

```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "Review for security vulnerabilities"
```

## Best Practices

1. **Be Specific**: Provide clear, specific requests
   - Good: "Review the authentication flow for SQL injection vulnerabilities"
   - Bad: "Review the code"

2. **Set Context**: Mention the area of focus
   - "In the user authentication module, check for..."
   - "For the API endpoints, verify..."

3. **Use Read-First**: Always use `--sandbox read-only` for initial analysis
   - Prevents accidental modifications
   - Safer for production codebases

4. **Time Management**: Codex may take time for large codebases
   - Start with specific directories
   - Use iterative refinement

## Limitations

- Maximum project size depends on Codex configuration
- Execution timeout may occur for very large projects
- Read-only sandbox cannot modify files (use write sandbox carefully)

## Integration

This skill integrates Codex CLI into your workflow by:
- Auto-detecting project root
- Simplifying command invocation
- Providing standardized request patterns
