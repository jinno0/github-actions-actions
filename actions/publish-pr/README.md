# Publish PR

Convert a draft pull request to ready for review.

## Features

- **Simple Publishing**: One-step conversion from draft to ready
- **Event-Based**: Automatically triggered when PR is ready
- **Clean Workflow**: Part of automated PR management pipeline

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | - | GitHub token with repo permissions |

## Example Usage

### Auto-Publish on Label
```yaml
name: Auto-Publish Draft PR
on:
  pull_request:
    types: [labeled]

jobs:
  publish:
    if: github.event.label.name == 'ready-for-review'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Publish PR
        uses: ./actions/publish-pr
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Publish After Checks Pass
```yaml
name: Publish When Ready
on:
  check_suite:
    types: [completed]

jobs:
  publish:
    if: |
      github.event.check_suite.conclusion == 'success' &&
      github.event.check_suite.pull_requests[0].draft == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Publish Draft PR
        uses: ./actions/publish-pr
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Manual Publishing
```yaml
name: Publish PR
on:
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Mark as Ready
        uses: ./actions/publish-pr
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## How It Works

1. **Detects Draft PR**: Uses GitHub event context to find PR number
2. **Converts to Ready**: Calls `gh pr ready` to mark PR as ready for review
3. **Notifications**: Reviewers are notified that PR is ready

## Typical Workflow

```yaml
# 1. Developer creates draft PR
# 2. CI runs and passes all checks
# 3. Publish PR action marks it as ready
# 4. Reviewers are notified
# 5. Review process begins
```

## Use Cases

1. **Label-Based**: Add `ready-for-review` label to publish
2. **CI-Passed**: Automatically publish when all checks pass
3. **Time-Based**: Publish at specific times (e.g., during work hours)
4. **Manual**: On-demand publishing with workflow_dispatch

## Requirements

- GitHub token with `pull-requests:write` scope
- Runner must have `gh` CLI installed
- PR must be in draft state

## See Also

- [Setup guide](../../instructions/publish-pr.md)
- [PR review enqueuer](../pr-review-enqueuer/README.md)
- [Review and merge workflow](../../examples/review-workflow.yml)
