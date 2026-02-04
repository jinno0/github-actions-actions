# Auto Rebase

Automatically rebase a PR with AI-powered conflict resolution.

## Features

- **Auto-Rebase**: Automatically rebase PRs when they fall behind the base branch
- **AI Conflict Resolution**: Uses Claude Code CLI to intelligently resolve merge conflicts
- **Interactive Mode**: Can use AI only when conflicts occur
- **Force Mode**: Always use AI for rebase (safer for complex PRs)
- **Conflict Reporting**: Tracks and reports number of conflicts resolved

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | Yes | - | GitHub token with repo permissions |
| `pr_number` | No | Event context | PR number to rebase (defaults to event context) |
| `claude-model` | No | `sonnet` | Claude model to use (sonnet/opus/haiku) |
| `rebase-strategy` | No | `interactive` | Rebase strategy: interactive (ai-assisted) or force (always use ai) |
| `conflict-resolution-prompt-template` | No | Built-in | Path to custom conflict resolution prompt template |

## Outputs

| Output | Description |
|--------|-------------|
| `rebased` | Whether the PR was successfully rebased (true/false) |
| `conflicts-resolved` | Whether conflicts were resolved by AI (true/false) |
| `conflict-count` | Number of conflicts encountered |

## Example Usage

```yaml
name: Auto Rebase
on:
  pull_request:
    types: [synchronize]

jobs:
  rebase:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: Auto Rebase with AI Conflict Resolution
        uses: ./actions/auto-rebase
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          claude-model: 'sonnet'
          rebase-strategy: 'interactive'
```

## How It Works

1. **Detects Rebase Need**: Checks if PR is behind base branch
2. **Attempts Rebase**: Tries to rebase using git
3. **AI Conflict Resolution**: If conflicts occur:
   - Uses Claude Code CLI to analyze conflicts
   - Applies intelligent resolution favoring PR branch
   - Continues rebase
4. **Reports**: Outputs whether rebase succeeded and conflicts resolved

## Rebase Strategies

### Interactive (Default)
- Uses standard git rebase by default
- Invokes AI only when conflicts occur
- Best for: Most PRs, faster execution

### Force
- Always uses AI-assisted rebase
- More careful but slower
- Best for: Complex PRs, high-conflict scenarios

## Conflict Resolution

When conflicts occur, this action:
1. Pauses the rebase at each conflict
2. Uses Claude Code CLI to analyze the conflict
3. Applies resolution preferring PR branch changes
4. Continues the rebase process
5. Tracks total conflicts resolved

## Requirements

- **Self-hosted runner** with Claude Code CLI installed
- GitHub token with `pull-requests:write` scope
- Runner must have `git` and `gh` CLI installed

## See Also

- [Setup guide](../../instructions/auto-rebase.md)
- [Bulk rebase action](../bulk-rebase-prs/README.md)
