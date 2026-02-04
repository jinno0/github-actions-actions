# Bulk Rebase PRs

Automatically rebase multiple pull requests against the latest base branch.

## Features

- **Bulk Operations**: Rebase multiple PRs in one workflow run
- **Smart Filtering**: Filter by merge state status (BEHIND, CLEAN, DIRTY, etc.)
- **Limit Control**: Control the maximum number of PRs to rebase
- **Dry Run Mode**: Preview what would be done without actually rebasing
- **Detailed Reporting**: Summary of successful and failed rebases

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | `${{ github.token }}` | GitHub token |
| `limit` | No | `0` | Maximum number of PRs to rebase (0 for all) |
| `merge-state-status` | No | `BEHIND` | Filter by mergeStateStatus (BEHIND, CLEAN, DIRTY, UNKNOWN, UNSTABLE) |
| `dry-run` | No | `false` | Show what would be done without actually rebasing |

## Example Usage

```yaml
name: Bulk Rebase PRs
on:
  schedule:
    # Run daily at midnight
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  rebase:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Bulk Rebase PRs
        uses: ./actions/bulk-rebase-prs
        with:
          limit: '10'
          merge-state-status: 'BEHIND'
```

## How It Works

1. **Fetches PRs**: Uses GitHub CLI to find open PRs
2. **Filters by Status**: Selects PRs matching the `merge-state-status`
3. **Rebases**: Calls `gh pr rebase` for each PR
4. **Reports**: Updates GitHub Actions step summary with results

## Merge State Status Values

- `BEHIND`: PR branch is behind base branch (needs rebase) - **DEFAULT**
- `CLEAN`: PR has no conflicts with base branch
- `DIRTY`: PR has merge conflicts
- `UNKNOWN`: Merge state hasn't been calculated
- `UNSTABLE`: PR mergeability is being tested

## Use Cases

1. **Daily Maintenance**: Keep all PRs up-to-date with main branch
2. **Before Release**: Rebase all PRs before cutting a release
3. **CI Pipeline**: Automatically rebase PRs as part of CI/CD
4. **Manual Trigger**: On-demand bulk rebase with `workflow_dispatch`

## Requirements

- GitHub token with `pull-requests:write` scope
- Runner must have `gh` CLI installed

## See Also

- [Setup guide](../../instructions/bulk-rebase-prs.md)
- [Auto-rebase action](../auto-rebase/README.md)
