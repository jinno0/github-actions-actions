# Auto Merge PR Setup Guide

> **Note**: For complete AI review + auto-merge workflow setup, see [review-and-auto-merge-workflow.md](./review-and-auto-merge-workflow.md).

This action merges a pull request using the specified merge method (squash, merge, or rebase) and can optionally enable GitHub's built-in auto-merge feature.

## Prerequisites

- **Runner**: A self-hosted runner with the `gh` (GitHub CLI) installed and configured.
- **Permissions**: The workflow requires `contents: write` and `pull-requests: write`.

## Setup Instructions

1. **Create Workflow File**:
   Create a new file at `.github/workflows/auto-merge.yml`.

2. **Copy Example Configuration**:
   Copy the content from the [Auto Merge Example](../examples/auto-merge-example.yml).

   ```yaml
   # Reference: examples/auto-merge-example.yml
   uses: owner/repo/actions/auto-merge@v1
   with:
     github-token: ${{ secrets.GITHUB_TOKEN }}
     merge-method: 'squash'
     auto-merge: 'false'
   ```

## Merge Methods

This action supports three merge methods: `squash` (default), `merge`, and `rebase`. See [GitHub's documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-merge-methods-on-github) for details on each method.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | - | GitHub token with `repo` permissions. Use `${{ secrets.GITHUB_TOKEN }}`. |
| `merge-method` | No | `squash` | Merge method: `squash`, `merge`, or `rebase`. |
| `auto-merge` | No | `false` | Enable GitHub's auto-merge feature (`true`/`false`). |

## Usage Modes

### Mode 1: Immediate Merge

The action immediately merges the PR using the specified method:

```yaml
- name: Auto Merge
  uses: ./actions/auto-merge
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    merge-method: 'squash'
    auto-merge: 'false'
```

Use this when:
- You have already validated the PR (e.g., after successful review and tests)
- You want immediate control over when the merge happens

### Mode 2: Enable Auto-Merge

The action enables GitHub's built-in auto-merge feature, which will merge the PR automatically after all branch protection rules pass:

```yaml
- name: Enable Auto-Merge
  uses: ./actions/auto-merge
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    merge-method: 'squash'
    auto-merge: 'true'
```

Use this when:
- You have branch protection rules (e.g., required reviews, status checks)
- You want GitHub to handle the merge after requirements are satisfied

## Integration Examples

### After AI Review

Combine with the review action to automatically merge LGTM PRs:

```yaml
jobs:
  ai-pipeline:
    runs-on: self-hosted
    steps:
      # 1. AI Review
      - name: AI Review
        id: review
        uses: ./actions/review-and-merge
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          lgtm-threshold: '7'

      # 2. Auto Merge if LGTM
      - name: Auto Merge
        if: steps.review.outputs.verdict == 'LGTM'
        uses: ./actions/auto-merge
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          merge-method: 'squash'
```

### Label-Triggered Merge

Merge only when a specific label is added:

```yaml
on:
  pull_request:
    types: [labeled]

jobs:
  auto-merge-on-label:
    if: contains(github.event.pull_request.labels.*.name, 'auto-merge')
    steps:
      - uses: ./actions/auto-merge
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          merge-method: 'squash'
```

## Branch Deletion

By default, this action deletes the branch after merging using the `--delete-branch` flag. This keeps your repository clean by automatically removing merged feature branches.

## Outputs

None. This action performs a side effect (merging the PR).
