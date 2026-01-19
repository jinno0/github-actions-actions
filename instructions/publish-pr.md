# Publish PR Setup Guide

This action converts a draft pull request to ready for review using the GitHub CLI.

## Prerequisites

- **Runner**: A self-hosted runner with the `gh` (GitHub CLI) installed and configured.
- **Permissions**: The workflow requires `pull-requests: write`.

## Setup Instructions

1. **Create Workflow File**:
   Create a new file at `.github/workflows/publish-pr.yml`.

2. **Copy Example Configuration**:
   Copy the content from the [Publish PR Example](../examples/publish-pr-example.yml).

   ```yaml
   # Reference: examples/publish-pr-example.yml
   uses: owner/repo/actions/publish-pr@main
   with:
     github-token: ${{ secrets.GITHUB_TOKEN }}
   ```

## Usage

The action triggers automatically on Pull Request events (opened, ready_for_review) targeting the configured branches (default: `main`, `develop`).

### How It Works

1. **Detects Draft PRs**: The action checks if the PR is in draft status using `github.event.pull_request.draft == true`.
2. **Converts to Ready**: Uses `gh pr ready` to mark the PR as ready for review.
3. **Idempotent**: If the PR is already ready for review, the command does nothing (safe to run multiple times).

### Common Use Cases

1. **Automatic Publishing**: Automatically publish draft PRs when they're opened (useful for teams that don't use drafts).
2. **Manual Trigger with Automation**: Combine with other conditions (e.g., after all checks pass).

### Integration Example

This action is often used as part of a larger PR pipeline:

```yaml
jobs:
  ai-pipeline:
    runs-on: self-hosted
    steps:
      # 1. Publish PR if it is a draft
      - name: Publish PR
        if: github.event.pull_request.draft == true
        uses: ./actions/publish-pr
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

      # 2. Run review, tests, or other automation...
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | - | GitHub token with `repo` permissions. Use `${{ secrets.GITHUB_TOKEN }}`. |

## Outputs

None. This action performs a side effect (converting draft PR to ready).
