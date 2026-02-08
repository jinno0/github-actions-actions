# Examples

This directory contains example workflows demonstrating how to use the actions in this repository.

## Usage

To use any example in your repository:

1. Copy the example `.yml` file to your repository's `.github/workflows/` directory
2. Adjust paths, triggers, and configuration as needed
3. Commit and push the file
4. If required, ensure you're running on a `self-hosted` runner with the `claude` CLI and/or `gh` CLI available

## Available Examples

| Action | Description | Requires Self-Hosted |
|--------|-------------|---------------------|
| `action-fixer` | Validate and auto-fix GitHub Actions workflow errors | No |
| `auto-document` | Automatically update documentation based on code changes | Yes |
| `auto-merge` | Automatically merge Pull Requests when conditions are met | No |
| `auto-refactor` | Automatically refactor code using Claude Code CLI | Yes |
| `auto-rebase` | Automatically rebase Pull Requests against target branch | Yes |
| `bulk-merge-prs` | Merge multiple Pull Requests at once | No |
| `bulk-rebase-prs` | Rebase multiple Pull Requests simultaneously | Yes |
| `pr-review-enqueuer` | Queue Pull Requests for automated review | Yes |
| `publish-pr` | Automatically publish draft Pull Requests | Yes |
| `release-notes-ai` | Generate high-quality release notes from commit history | Yes |
| `review-and-merge` | Review a PR using Claude Code CLI and merge if LGTM | Yes |
| `review-auto-merge` | AI review with pre-flight checks and automatic merging | Yes |
| `spec-to-code` | Generate code from Markdown specifications | Yes |

## Version Tags

When using actions from this repository in other repositories, always use version tags (e.g., `@v1`, `@v2`) instead of `@main` for stability:

```yaml
- uses: owner/repo/actions/action-name@v1
```

Or when using within this repository during development:

```yaml
- uses: ./actions/action-name
```
