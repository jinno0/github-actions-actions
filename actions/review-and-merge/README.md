# AI Review and Fix

Automatically review and fix pull requests using Claude Code CLI with intelligent context-aware analysis.

## Features

- **AI-Powered Code Review**: Uses Claude Code CLI to understand code context and provide meaningful feedback
- **Automatic Fixes**: Can automatically fix issues found during review
- **Customizable Rules**: Support for custom review rules and prompt templates
- **Confidence Scoring**: Provides confidence scores (1-10) for review decisions
- **LGTM/Auto-Merge**: Can automatically merge PRs that meet quality thresholds

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `github-token` | No | `${{ github.token }}` | GitHub token for API operations |
| `claude-model` | No | `sonnet` | Claude model to use (sonnet/opus/haiku) |
| `lgtm-threshold` | No | `7` | Minimum confidence for LGTM (1-10) |
| `review-prompt-template` | No | Built-in | Path to custom review prompt template |
| `comment-template` | No | Built-in | Path to custom comment template |
| `custom-rules` | No | `''` | Additional review rules/guidelines |
| `auto-fix` | No | `true` | Whether to automatically fix issues |

## Outputs

| Output | Description |
|--------|-------------|
| `verdict` | Review verdict (LGTM or REQUEST_CHANGES) |
| `confidence` | Confidence score (1-10) |

## Example Usage

```yaml
name: AI Review
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: AI Review and Fix
        uses: ./actions/review-and-merge
        with:
          claude-model: 'sonnet'
          lgtm-threshold: '7'
          auto-fix: 'true'
          custom-rules: |
            - Follow Python PEP 8 style guidelines
            - Include docstrings for all functions
            - Maintain test coverage above 80%
```

## How It Works

1. **Checkout**: Automatically checks out the PR branch
2. **Diff Analysis**: Gets the diff of changes in the PR
3. **AI Review**: Uses Claude Code CLI to review the changes
4. **Auto-Fix (optional)**: Automatically fixes issues when enabled
5. **Verdict**: Returns LGTM or REQUEST_CHANGES based on confidence threshold

## Customization

### Custom Review Prompts

Create a custom prompt template:
```bash
cat > .github/review-prompts/custom.md << 'EOF'
You are reviewing a PR for a web application.
Focus on:
- Security vulnerabilities
- Performance issues
- Code maintainability
EOF
```

Reference it in the workflow:
```yaml
- uses: ./actions/review-and-merge
  with:
    review-prompt-template: '.github/review-prompts/custom.md'
```

### Custom Rules

Add project-specific rules:
```yaml
custom-rules: |
  - All new code must have tests
  - Database migrations must be reversible
  - API changes must update documentation
```

## Integration with Auto-Merge

Combine with auto-merge for fully automated PR handling:
```yaml
- name: AI Review and Merge
  uses: ./actions/review-and-merge
  with:
    lgtm-threshold: '8'
    auto-fix: 'true'

- name: Auto-merge if LGTM
  if: steps.review.outputs.verdict == 'LGTM'
  run: gh pr merge ${{ github.event.pull_request.number }} --squash
```

## Requirements

- Claude Code CLI must be installed on the runner
- GitHub token with `pull-requests:write` scope
- Runner must have `gh` CLI installed

## See Also

- [Full workflow example](../../examples/review-workflow.yml)
- [Usage guide](../../instructions/review-and-merge.md)
