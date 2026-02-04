# Review and Auto-Merge PR

Automatically merge pull requests after they pass review and CI checks.

## Features

- **Auto-Merge**: Automatically merges PRs that meet criteria
- **Retry Logic**: Makes multiple attempts to handle transient issues
- **Squash Merge**: Uses squash merge strategy by default
- **Branch Deletion**: Automatically deletes branch after merge
- **Status Reporting**: Reports merge status in outputs

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | `${{ github.token }}` | GitHub token |
| `max-attempts` | No | `5` | Maximum merge attempts |

## Outputs

| Output | Description |
|--------|-------------|
| `merged` | Whether the PR was successfully merged (true/false) |

## Example Usage

```yaml
name: Auto-Merge
on:
  pull_request:
    types: [labeled, approved, ready_for_review]

jobs:
  auto-merge:
    if: github.event.label.name == 'auto-merge' || github.event.review.state == 'approved'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Review and Auto-Merge
        uses: ./actions/review-auto-merge
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          max-attempts: '5'

      - name: Comment on Merge
        if: steps.auto-merge.outputs.merged == 'true'
        run: |
          gh pr comment ${{ github.event.pull_request.number }} \
            --body "✅ Automatically merged"
```

## How It Works

1. **Checks PR State**: Verifies PR is still open
2. **Attempts Merge**: Tries squash merge with retry
3. **Deletes Branch**: Removes branch after successful merge
4. **Reports Status**: Sets `merged` output based on result

## Use Cases

### Label-Based Auto-Merge
```yaml
on:
  pull_request:
    types: [labeled]
jobs:
  auto-merge:
    if: github.event.label.name == 'auto-merge'
    # ... merge workflow
```

### Approval-Based Auto-Merge
```yaml
on:
  pull_request:
    types: [submitted]
jobs:
  auto-merge:
    if: github.event.review.state == 'approved'
    # ... merge workflow
```

### CI-Passed Auto-Merge
```yaml
on:
  check_run:
    types: [completed]
jobs:
  auto-merge:
    if: github.event.check_run.conclusion == 'success'
    # ... merge workflow
```

## Requirements

- GitHub token with `pull-requests:write` scope
- Runner must have `gh` CLI installed
- PR must have all required reviews and CI checks passed

## See Also

- [Setup guide](../../instructions/review-auto-merge.md)
- [Auto-merge action](../auto-merge/README.md)
