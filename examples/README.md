# Examples

This directory contains example workflows demonstrating how to use the actions in this repository.

## Available Examples

### action-fixer-example.yml

Demonstrates how to use the `action-fixer` action to validate and auto-fix GitHub Actions workflow files.

To use this example in your repository:

1. Copy `action-fixer-example.yml` to your repository's `.github/workflows/` directory
2. Adjust the paths and triggers as needed
3. Commit and push the file

### review-and-merge-example.yml

Demonstrates how to use the `review-and-merge` action to automatically review Pull Requests using Claude Code CLI and merge them if they meet quality standards.

To use this example in your repository:

1. Copy `review-and-merge-example.yml` to your repository's `.github/workflows/` directory
2. Ensure you are running on a `self-hosted` runner where the `claude` CLI is available
3. Adjust branches and custom rules as needed
4. Commit and push the file

### spec-to-code-example.yml

Demonstrates how to use the `spec-to-code` action to generate source code from Markdown specifications using Claude Code CLI.

To use this example in your repository:

1. Copy `spec-to-code-example.yml` to your repository's `.github/workflows/` directory
2. Create a `specs/` directory and add your Markdown specification files
3. Ensure you are running on a `self-hosted` runner where the `claude` CLI is available
4. Commit and push the file

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
