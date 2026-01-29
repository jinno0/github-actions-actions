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

### auto-refactor-example.yml

Demonstrates how to use the `auto-refactor` action to automatically improve code quality and readability using Claude Code CLI.

To use this example in your repository:

1. Copy `auto-refactor-example.yml` to your repository's `.github/workflows/` directory
2. Ensure you are running on a `self-hosted` runner where the `claude` CLI is available
3. Commit and push the file
4. Trigger the workflow manually via the Actions tab and specify the path and instructions

### auto-document-example.yml

Demonstrates how to use the `auto-document` action to keep your documentation in sync with your source code changes.

To use this example in your repository:

1. Copy `auto-document-example.yml` to your repository's `.github/workflows/` directory
2. Adjust the `source-path` and `doc-path` as needed
3. Ensure you are running on a `self-hosted` runner where the `claude` CLI is available
4. Commit and push the file

### release-notes-ai-example.yml

Demonstrates how to use the `release-notes-ai` action to generate human-readable release notes from your commit history and Pull Requests.

To use this example in your repository:

1. Copy `release-notes-ai-example.yml` to your repository's `.github/workflows/` directory
2. Ensure you are running on a `self-hosted` runner where the `claude` CLI and `gh` CLI are available
3. Commit and push the file
4. Create a new tag (e.g., `git tag v1.0.1 && git push origin v1.0.1`) to trigger the workflow

### auto-merge-example.yml

Demonstrates how to use the `auto-merge` action to automatically merge Pull Requests when they meet specified conditions.

To use this example in your repository:

1. Copy `auto-merge-example.yml` to your repository's `.github/workflows/` directory
2. Configure the `merge-method` (squash, merge, or rebase)
3. Set `auto-merge` to `true` to enable automatic merging
4. Adjust trigger conditions as needed
5. Commit and push the file

### auto-rebase-example.yml

Demonstrates how to use the `auto-rebase` action to automatically rebase Pull Requests against the target branch.

To use this example in your repository:

1. Copy `auto-rebase-example.yml` to your repository's `.github/workflows/` directory
2. Ensure you are running on a `self-hosted` runner where the `claude` CLI is available
3. Configure trigger conditions (e.g., on label, on schedule)
4. Commit and push the file

### bulk-merge-prs-example.yml

Demonstrates how to use the `bulk-merge-prs` action to merge multiple Pull Requests at once, useful for cleaning up backlog after successful CI/CD.

To use this example in your repository:

1. Copy `bulk-merge-prs-example.yml` to your repository's `.github/workflows/` directory
2. Configure the merge method and whether to include draft PRs
3. Trigger manually via the Actions tab with parameters for limit and dry-run
4. Commit and push the file

### bulk-rebase-prs-example.yml

Demonstrates how to use the `bulk-rebase-prs` action to rebase multiple Pull Requests simultaneously, useful for updating many PRs after main branch changes.

To use this example in your repository:

1. Copy `bulk-rebase-prs-example.yml` to your repository's `.github/workflows/` directory
2. Configure the limit of PRs to process (0 for all eligible PRs)
3. Trigger manually via the Actions tab
4. Commit and push the file

### pr-review-enqueuer-example.yml

Demonstrates how to use the `pr-review-enqueuer` action to queue Pull Requests for automated review, useful for managing high-volume PR workflows.

To use this example in your repository:

1. Copy `pr-review-enqueuer-example.yml` to your repository's `.github/workflows/` directory
2. Ensure you are running on a `self-hosted` runner where the `claude` CLI is available
3. Configure queue size and processing rules
4. Commit and push the file

### publish-pr-example.yml

Demonstrates how to use the `publish-pr` action to automatically publish draft Pull Requests when they're marked ready for review.

To use this example in your repository:

1. Copy `publish-pr-example.yml` to your repository's `.github/workflows/` directory
2. Ensure you are running on a `self-hosted` runner where the `claude` CLI is available
3. Commit and push the file
4. When a draft PR is marked ready for review, it will be automatically published

### review-auto-merge-example.yml

Demonstrates the comprehensive workflow of using AI to review Pull Requests and automatically merge them if they pass quality checks, with pre-flight checks and CI status verification.

To use this example in your repository:

1. Copy `review-auto-merge-example.yml` to your repository's `.github/workflows/` directory
2. Ensure you are running on a `self-hosted` runner where the `claude` CLI is available
3. Configure WIP label detection and draft PR skipping
4. Adjust branch rules and merge methods as needed
5. Commit and push the file

## Using Actions from This Repository

When using actions from this repository in other repositories, always use version tags (e.g., `@v1`, `@v2`) instead of `@main` for stability:

```yaml
- uses: owner/repo/actions/action-name@v1
```

Or when using within this repository during development:

```yaml
- uses: ./actions/action-name
```

## Available Actions

| Action | Description |
|--------|-------------|
| `action-fixer` | Validate and auto-fix GitHub Actions workflow errors |
| `auto-document` | Automatically update documentation based on code changes |
| `auto-merge` | Automatically merge Pull Requests when conditions are met |
| `auto-refactor` | Automatically refactor code using Claude Code CLI |
| `auto-rebase` | Automatically rebase Pull Requests against target branch |
| `bulk-merge-prs` | Merge multiple Pull Requests at once |
| `bulk-rebase-prs` | Rebase multiple Pull Requests simultaneously |
| `pr-review-enqueuer` | Queue Pull Requests for automated review |
| `publish-pr` | Automatically publish draft Pull Requests |
| `release-notes-ai` | Generate high-quality release notes from commit history |
| `review-and-merge` | Review a PR using Claude Code CLI and merge if LGTM |
| `review-auto-merge` | AI review with pre-flight checks and automatic merging |
| `spec-to-code` | Generate code from Markdown specifications |
