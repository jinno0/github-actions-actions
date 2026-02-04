# PR Review Enqueuer

Automatically scans open pull requests and adds `/review` comments to trigger AI review workflows.

## Features

- **Smart PR Filtering**: Filter PRs by draft status, labels, age, and more
- **Batch Processing**: Process PRs in batches to avoid API rate limits
- **Dry Run Mode**: Preview what would be done without actually commenting
- **Flexible Exclusions**: Skip PRs with specific labels (e.g., merged, auto-merged)
- **Detailed Reporting**: Summary in GitHub Actions step summary

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | `${{ github.token }}` | GitHub token with repo scope |
| `pr-filter` | No | `all` | Filter PRs to process (all|drafts|ready|wip|no-label) |
| `label-filter` | No | `''` | Only process PRs with this label (empty = all PRs) |
| `age-threshold` | No | `0` | Only process PRs older than this many minutes (0 = all PRs) |
| `dry-run` | No | `false` | Log what would be done without actually commenting |
| `exclude-labels` | No | `auto-merged,merged,closed` | Skip PRs with these labels (comma-separated) |
| `batch-size` | No | `0` | Number of PRs to process per run (0 = unlimited) |

## Outputs

| Output | Description |
|--------|-------------|
| `prs-reviewed` | Number of PRs that received /review comment |
| `prs-skipped` | Number of PRs skipped |

## Example Usage

```yaml
name: Enqueue PR Reviews
on:
  schedule:
    # Run every hour
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  enqueue:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Enqueue PR Reviews
        uses: ./actions/pr-review-enqueuer
        with:
          pr-filter: 'ready'
          age-threshold: '30'
          exclude-labels: 'wip,do-not-merge'
          batch-size: '10'
```

## How It Works

1. **Scans PRs**: Uses GitHub CLI to find open PRs matching filters
2. **Checks Eligibility**: Verifies:
   - PR doesn't already have `/review` comment
   - PR meets age threshold (if specified)
   - PR doesn't have excluded labels
3. **Adds Comment**: Posts `/review` comment to trigger review workflow
4. **Reports**: Updates GitHub Actions step summary with results

## Filter Options

### PR Filters
- `all`: All open PRs (default)
- `drafts`: Only draft PRs
- `ready`: Only ready for review PRs (non-draft)
- `wip`: PRs with "wip", "work in progress", or "do not merge" labels
- `no-label`: PRs without any labels

### Exclusion Labels
Default excludes: `auto-merged`, `merged`, `closed`

## Use Cases

1. **Scheduled Reviews**: Run hourly to enqueue all ready PRs
2. **Label-Based**: Only review PRs with specific label (e.g., `needs-review`)
3. **Age-Gated**: Review only PRs older than 30 minutes (avoid premature reviews)
4. **Batch Processing**: Limit to 10 PRs per run to avoid overwhelming reviewers

## Requirements

- GitHub token with `pull-requests:write` scope
- Runner must have `gh` CLI installed

## See Also

- [Setup guide](../../instructions/pr-review-enqueuer.md)
- [Review workflow example](../../examples/review-workflow.yml)
