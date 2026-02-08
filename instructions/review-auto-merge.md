# Review Auto-Merge Setup Guide

This action automatically merges pull requests after AI review and CI checks pass. It implements retry logic with multiple merge methods (squash, merge, rebase) to handle edge cases like race conditions.

## Architecture

This action does not use Claude Code CLI. The AI review is performed by a separate action (`review-and-merge`), and this action uses the GitHub API to execute the merge after CI passes. It handles post-review merge execution with retry logic and does not require code understanding.

## Prerequisites

- **Runner**: A self-hosted runner with the `gh` (GitHub CLI) installed.
- **Permissions**: `pull-requests: write` and `contents: write` to merge PRs and delete branches.
- **CI**: All CI checks must pass before auto-merge attempts.

## Setup Instructions

1. **Create Workflow File**:
   Create a new file at `.github/workflows/review-auto-merge.yml`.

2. **Copy Example Configuration**:
   Copy the content from the [Review Auto-Merge Example](../examples/review-auto-merge-example.yml).

   ```yaml
   # Reference: examples/review-auto-merge-example.yml
   uses: owner/repo/actions/review-auto-merge@main
   with:
     github-token: ${{ secrets.GITHUB_TOKEN }}
     max-attempts: '5'
   ```

## Usage

This action is typically used as the final step in an AI-powered PR pipeline:

1. **AI Review**: Code is reviewed by Claude (using `review-and-merge` action)
2. **CI Checks**: Wait for all CI checks to complete
3. **Auto-Merge**: Merge the PR if review is LGTM and CI passes

### Features

- **Pre-flight Checks**: Automatically skips draft PRs and PRs with WIP labels (configurable)
- **Retry Logic**: Attempts merging up to `max-attempts` times (default: 10) with 5-second delays
- **Multiple Merge Methods**: Tries squash → merge → rebase in order
- **Branch Cleanup**: Automatically deletes the PR branch after successful merge
- **State Verification**: Checks PR state before each attempt to avoid errors
- **CI Validation**: Waits for CI checks to complete and verifies they passed before merging

### Configuration Options

### Environment Variables

You can configure the workflow behavior by setting environment variables in the `env` section of your workflow file:

- **`SKIP_DRAFT`**: Skip draft PRs (default: `true`)
  - Set to `'true'` to skip auto-merge for draft PRs
  - Set to `'false'` to process draft PRs like regular PRs

- **`SKIP_WIP`**: Skip PRs with WIP labels (default: `true`)
  - Set to `'true'` to skip auto-merge for PRs marked as work-in-progress
  - Set to `'false'` to ignore WIP labels

- **`WIP_LABELS`**: Comma-separated list of WIP labels to check (default: `'WIP,Work in Progress,Do not merge,dont merge,wip'`)
  - Customize this list to match your team's workflow
  - Labels are case-insensitive

### Workflow Configuration

- **`max-attempts`**: Number of merge attempts (default: 10). Increase if you frequently encounter race conditions.
- **Concurrency**: Set up concurrency control in your workflow to ensure only one workflow runs per PR at a time.

### Example Configuration

```yaml
env:
  # Skip draft PRs
  SKIP_DRAFT: 'true'
  # Skip PRs with WIP labels
  SKIP_WIP: 'true'
  # Custom WIP labels
  WIP_LABELS: 'WIP,Work in Progress,Do not merge,dont merge,wip,IN PROGRESS'
```

### Example Pipeline

```yaml
jobs:
  ai-review:
    # Uses review-and-merge action
    uses: ./actions/review-and-merge

  wait-for-ci:
    # Waits for CI checks to complete
    needs: ai-review

  auto-merge:
    # Uses review-auto-merge action
    uses: ./actions/review-auto-merge
    needs: [ai-review, wait-for-ci]
```

### Troubleshooting

- **Merge Fails**: Check if PR is still open and if CI checks have passed
- **Race Conditions**: Increase `max-attempts` or add delays between attempts
- **Branch Not Deleted**: Ensure permissions include `contents: write`
