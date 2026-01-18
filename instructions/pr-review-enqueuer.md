# PR Review Enqueuer

Automatically scans open PRs and adds `/review` comment to trigger the review-and-merge workflow.

## Prerequisites

- GitHub repository with a review workflow that responds to `/review` comment
- GitHub token with `repo` scope (usually `GITHUB_TOKEN` is sufficient)
- Self-hosted runner is NOT required (runs on standard `ubuntu-latest`)

## Setup Instructions

### 1. Copy the Example Workflow

Copy the example workflow to your repository:

```bash
mkdir -p .github/workflows
cp examples/pr-review-enqueuer-example.yml .github/workflows/pr-review-enqueue.yml
```

### 2. Configure the Workflow

Edit `.github/workflows/pr-review-enqueue.yml`:

```yaml
name: Scheduled PR Review Enqueue

on:
  schedule:
    - cron: '0 */3 * * *'  # Every 3 hours (customize as needed)
  workflow_dispatch:       # Allow manual trigger

jobs:
  enqueue-prs-for-review:
    runs-on: ubuntu-latest
    steps:
      - uses: your-org/github-actions-actions/actions/pr-review-enqueuer@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pr-filter: 'all'          # Options: all, drafts, ready, wip, no-label
          age-threshold: '5'        # Only PRs older than 5 minutes
          exclude-labels: 'auto-merged,merged,closed'
```

### 3. Customize Parameters

#### `pr-filter` (default: `all`)

Filter which PRs to process:

| Value | Description |
|-------|-------------|
| `all` | Process all open PRs |
| `drafts` | Only draft PRs |
| `ready` | Only ready-for-review PRs (non-draft) |
| `wip` | Only PRs with WIP-related labels |
| `no-label` | Only PRs without any labels |

#### `label-filter` (default: empty)

Only process PRs with a specific label:

```yaml
label-filter: 'needs-review'  # Only PRs labeled "needs-review"
```

#### `age-threshold` (default: `0`)

Skip PRs younger than N minutes:

```yaml
age-threshold: '5'  # Only process PRs older than 5 minutes
```

This helps avoid race conditions with newly created PRs.

#### `exclude-labels` (default: `auto-merged,merged,closed`)

Skip PRs with these labels:

```yaml
exclude-labels: 'auto-merged,merged,closed,on-hold,blocked'
```

#### `batch-size` (default: `0` = unlimited)

Limit number of PRs to process per run:

```yaml
batch-size: '10'  # Process at most 10 PRs per run
```

#### `dry-run` (default: `false`)

Log what would be done without actually commenting:

```yaml
dry-run: 'true'  # Test mode - no actual comments
```

## Usage

### Automatic Trigger

The workflow runs automatically on the schedule defined in the cron expression:

```yaml
schedule:
  - cron: '0 */3 * * *'  # Every 3 hours at minute 0
```

Common schedules:

| Cron Expression | Description |
|-----------------|-------------|
| `0 */3 * * *` | Every 3 hours |
| `0 */1 * * *` | Every hour |
| `0 0,6,12,18 * * *` | 4 times daily (midnight, 6am, noon, 6pm) |
| `0 9 * * 1-5` | Weekdays at 9am |
| `*/30 * * * *` | Every 30 minutes |

### Manual Trigger

You can also trigger the workflow manually from GitHub Actions UI:

1. Go to **Actions** tab
2. Select **Scheduled PR Review Enqueue**
3. Click **Run workflow**

## Example Configurations

### Example 1: Process All PRs Every Hour

```yaml
on:
  schedule:
    - cron: '0 */1 * * *'  # Every hour

jobs:
  enqueue:
    runs-on: ubuntu-latest
    steps:
      - uses: your-org/github-actions-actions/actions/pr-review-enqueuer@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pr-filter: 'all'
          age-threshold: '5'
```

### Example 2: Only Ready PRs, Limited Batch

```yaml
on:
  schedule:
    - cron: '0 */2 * * *'  # Every 2 hours

jobs:
  enqueue:
    runs-on: ubuntu-latest
    steps:
      - uses: your-org/github-actions-actions/actions/pr-review-enqueuer@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pr-filter: 'ready'          # Only non-draft PRs
          batch-size: '5'             # Max 5 PRs per run
          exclude-labels: 'wip,on-hold,blocked'
```

### Example 3: Process Labeled PRs Only

```yaml
on:
  schedule:
    - cron: '*/30 * * * *'  # Every 30 minutes

jobs:
  enqueue:
    runs-on: ubuntu-latest
    steps:
      - uses: your-org/github-actions-actions/actions/pr-review-enqueuer@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pr-filter: 'all'
          label-filter: 'needs-review'   # Only PRs with "needs-review" label
          age-threshold: '1'
```

### Example 4: Dry Run for Testing

```yaml
on:
  workflow_dispatch:  # Manual only for testing

jobs:
  enqueue:
    runs-on: ubuntu-latest
    steps:
      - uses: your-org/github-actions-actions/actions/pr-review-enqueuer@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pr-filter: 'all'
          dry-run: 'true'  # Test mode - no actual comments
```

## Outputs

The action provides two outputs:

- `prs-reviewed`: Number of PRs that received `/review` comment
- `logs-reviewed`: Number of PRs skipped (already had `/review`, too young, etc.)

```yaml
jobs:
  enqueue:
    runs-on: ubuntu-latest
    steps:
      - id: enqueue
        uses: your-org/github-actions-actions/actions/pr-review-enqueuer@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Check results
        run: |
          echo "PRs enqueued: ${{ steps.enqueue.outputs.prs-reviewed }}"
          echo "PRs skipped: ${{ steps.enqueue.outputs.prs-skipped }}"
```

## Permissions

The action requires the following permissions:

```yaml
permissions:
  pull-requests: write  # For adding /review comments
  contents: read        # For reading PR information
```

The `GITHUB_TOKEN` automatically has these permissions.

## Troubleshooting

### No PRs are being enqueued

1. Check the workflow logs for the query being executed
2. Verify that PRs exist matching your filter criteria
3. Check if `age-threshold` is excluding new PRs
4. Verify `exclude-labels` isn't filtering out your PRs

### PRs are being enqueued multiple times

The action checks for existing `/review` comments before adding one. If you're seeing duplicates:

1. Check if multiple workflows are running
2. Verify the `/review` comment is being posted correctly (check GitHub token permissions)

### Workflow fails with permission error

Ensure the workflow has `pull-requests: write` permission:

```yaml
permissions:
  pull-requests: write
  contents: read
```

## Best Practices

1. **Use `age-threshold`**: Set to 5-10 minutes to avoid race conditions with PR creation
2. **Limit batch size**: For large repos, use `batch-size` to avoid long-running workflows
3. **Test with `dry-run`**: First run with `dry-run: 'true'` to verify behavior
4. **Monitor frequency**: Don't run too frequently (every 30 min minimum recommended)
5. **Use labels strategically**: Combine with `label-filter` for targeted review queues

## Related Actions

- **review-and-merge**: Main review workflow that responds to `/review` comments
- **auto-document**: Automatic documentation generation on PR merge
