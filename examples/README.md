# Examples

This directory contains example workflows demonstrating how to use the actions in this repository.

## Available Examples

### action-fixer-example.yml

Demonstrates how to use the `action-fixer` action to validate and auto-fix GitHub Actions workflow files.

To use this example in your repository:

1. Copy `action-fixer-example.yml` to your repository's `.github/workflows/` directory
2. Adjust the paths and triggers as needed
3. Commit and push the file

## Using Actions from This Repository

All actions in this repository can be referenced as:

```yaml
- uses: owner/repo/actions/action-name@main
```

Or when using within this repository:

```yaml
- uses: ./actions/action-name
```

## Available Actions

| Action | Description |
|--------|-------------|
| `action-fixer` | Validate and auto-fix GitHub Actions workflow errors |
| `auto-document` | Automatically update documentation based on code changes |
| `auto-refactor` | Automatically refactor code using Claude Code CLI |
| `release-notes-ai` | Generate high-quality release notes from commit history |
| `review-and-merge` | Review a PR using Claude Code CLI and merge if LGTM |
| `spec-to-code` | Generate code from Markdown specifications |
