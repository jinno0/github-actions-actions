# GitHub Actions Fixer

Automatically validate and fix common GitHub Actions workflow errors using AI-powered analysis.

## Features

- **YAML Validation**: Validates all YAML files in `.github/workflows/`
- **Common Issue Detection**: Detects missing `runs-on`, deprecated actions, missing permissions
- **AI-Powered Fixes**: Uses Claude Code CLI to suggest fixes for validation issues
- **Auto-Fix Mode**: Can automatically commit fixes or create PRs
- **Customizable Fix Prompts**: Support for custom fix prompt templates

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | No | `${{ github.token }}` | GitHub token for API operations |
| `fail-on-error` | No | `true` | Fail the action if errors are found |
| `auto-fix` | No | `false` | Automatically fix issues and create a commit |
| `commit-message` | No | `fix: correct workflow validation issues` | Commit message for auto-fix |
| `claude-model` | No | `sonnet` | Claude model for AI-powered fixes (sonnet/opus/haiku) |
| `fix-prompt-template` | No | Built-in | Path to custom fix prompt template |

## Outputs

| Output | Description |
|--------|-------------|
| `errors` | Number of files with validation issues |

## Example Usage

```yaml
name: Workflow Validation
on:
  push:
    paths:
      - '.github/workflows/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate and Fix Workflows
        uses: ./actions/action-fixer
        with:
          auto-fix: 'true'
          claude-model: 'sonnet'
```

## How It Works

1. **Validation**: Scans all YAML files in `.github/`
2. **Issue Detection**: Checks for:
   - YAML syntax errors
   - Missing `runs-on` in jobs
   - Deprecated action versions
   - Missing `permissions` (security warning)
3. **AI Fix (optional)**: When `auto-fix: true`, uses Claude Code CLI to suggest fixes
4. **Commit/PR**: Auto-commits fixes or creates a PR

## Common Issues Detected

- Missing `runs-on` in workflow jobs
- Using deprecated `@v1` or `@v2` actions
- YAML syntax errors
- Missing `permissions` (recommended for security)

## Requirements

- Claude Code CLI must be installed on the runner (for auto-fix)
- GitHub token with `contents:write` scope (for auto-fix)
- Python 3.x with `yamllint` package

## See Also

- [Setup guide](../../instructions/action-fixer.md)
- [Security checklist](../../.github/security-checklist.md)
