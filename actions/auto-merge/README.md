# Auto Merge PR

Automatically merge a pull request with your preferred merge method.

## Features

- **Immediate Merge**: Merges PRs immediately when triggered
- **Auto-Merge Support**: Can enable GitHub's auto-merge feature instead
- **Multiple Methods**: Supports squash, merge, and rebase strategies
- **Branch Cleanup**: Automatically deletes branch after merge

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | - | GitHub token |
| `merge-method` | No | `squash` | Merge method (squash, merge, rebase) |
| `auto-merge` | No | `false` | Enable auto-merge instead of immediate merge (true/false) |

## Example Usage

### Immediate Merge
```yaml
name: Auto-Merge on Approval
on:
  pull_request_review:
    types: [submitted]

jobs:
  auto-merge:
    if: github.event.review.state == 'approved'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Auto-Merge PR
        uses: ./actions/auto-merge
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          merge-method: 'squash'
```

### Enable Auto-Merge
```yaml
name: Enable Auto-Merge
on:
  check_suite:
    types: [completed]

jobs:
  enable-auto-merge:
    if: github.event.check_suite.conclusion == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Enable Auto-Merge
        uses: ./actions/auto-merge
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          auto-merge: 'true'
```

## How It Works

### Immediate Merge Mode (`auto-merge: false`)
1. Calls `gh pr merge` with specified method
2. Merges PR immediately
3. Deletes branch after successful merge

### Auto-Merge Mode (`auto-merge: true`)
1. Enables GitHub's built-in auto-merge feature
2. PR will merge automatically after all requirements are met
3. Useful for CI-passed workflows

## Merge Methods

### Squash (Default)
- Combines all commits into one
- Cleaner git history
- Recommended for most workflows

### Merge
- Creates a merge commit
- Preserves full commit history
- Useful for seeing individual commits

### Rebase
- Replays commits on top of base branch
- Linear history
- Use when you want to avoid merge commits

## Use Cases

1. **Approval-Based**: Merge immediately when approved
2. **CI-Passed**: Enable auto-merge when CI checks pass
3. **Label-Based**: Merge when specific label is added
4. **Scheduled**: Merge PRs during business hours only

## Requirements

- GitHub token with `pull-requests:write` scope
- Runner must have `gh` CLI installed
- PR must have all required reviews and checks passed

## See Also

- [Setup guide](../../instructions/auto-merge.md)
- [Bulk merge action](../bulk-merge-prs/README.md)
- [Review auto-merge action](../review-auto-merge/README.md)
