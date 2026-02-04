# Bulk Merge PRs

Automatically merge multiple pull requests that are ready (CLEAN status) in one workflow run.

## Features

- **Bulk Operations**: Merge multiple PRs at once
- **Smart Filtering**: Only merges PRs with CLEAN merge status
- **Draft Support**: Optionally mark draft PRs as ready before merging
- **Limit Control**: Control maximum number of PRs to merge
- **Dry Run Mode**: Preview what would be done without actually merging

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | `${{ github.token }}` | GitHub token |
| `limit` | No | `0` | Maximum number of PRs to merge (0 for all) |
| `merge-method` | No | `squash` | Merge method (squash, merge, rebase) |
| `include-drafts` | No | `true` | Include draft PRs (they will be marked as ready first) |
| `dry-run` | No | `false` | Show what would be done without actually merging |

## Example Usage

```yaml
name: Bulk Merge PRs
on:
  schedule:
    # Run daily at 9 AM
    - cron: '0 9 * * 1-5'
  workflow_dispatch:

jobs:
  bulk-merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Bulk Merge Ready PRs
        uses: ./actions/bulk-merge-prs
        with:
          limit: '20'
          merge-method: 'squash'
          include-drafts: 'true'
```

## How It Works

1. **Fetches PRs**: Finds open PRs with CLEAN merge status
2. **Handles Drafts**: Optionally marks draft PRs as ready first
3. **Merges**: Calls `gh pr merge` for each PR
4. **Reports**: Updates GitHub Actions step summary with results

## Merge Status

Only PRs with the following status are merged:
- `mergeable: "MERGEABLE"`
- `mergeStateStatus: "CLEAN"`

This ensures:
- All CI checks have passed
- No merge conflicts
- PR is ready to be merged

## Use Cases

### Daily Bulk Merge
```yaml
on:
  schedule:
    - cron: '0 9 * * 1-5'  # Weekdays at 9 AM
```
Merges all ready PRs at the start of each business day.

### After Release
```yaml
on:
  workflow_dispatch:
    inputs:
      reason:
        description: 'Reason for bulk merge'
```
Manually trigger after a release to merge accumulated PRs.

### Limited Batch
```yaml
with:
  limit: '10'
  include-drafts: 'false'
```
Merge only 10 non-draft PRs at a time.

## Requirements

- GitHub token with `pull-requests:write` scope
- Runner must have `gh` CLI installed
- All PRs must have required reviews and CI checks passed

## Safety Features

- **Dry Run**: Test without merging using `dry-run: 'true'`
- **Limit**: Control maximum merges per run
- **Status Check**: Only merges CLEAN PRs
- **Draft Control**: Optionally exclude drafts

## See Also

- [Setup guide](../../instructions/bulk-merge-prs.md)
- [Auto-merge action](../auto-merge/README.md)
- [Bulk rebase action](../bulk-rebase-prs/README.md)
