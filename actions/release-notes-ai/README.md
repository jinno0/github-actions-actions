# AI Release Notes

Automatically generate high-quality release notes from commit history using Claude Code CLI.

## Features

- **AI-Powered Generation**: Uses Claude Code CLI to analyze commits and generate meaningful release notes
- **Smart Grouping**: Automatically categorizes changes by type (features, bug fixes, breaking changes, etc.)
- **Customizable**: Support for custom prompt templates to match your project's style
- **Multi-Source**: Analyzes both commit messages and merged PR information
- **Flexible Output**: Save to file or use in workflow

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `base-ref` | No | `main` | Base reference (e.g., previous tag or main) |
| `head-ref` | No | `HEAD` | Head reference (e.g., current branch or tag) |
| `output-file` | No | `RELEASE_NOTES.md` | File to save the release notes to |
| `claude-model` | No | `sonnet` | Claude model to use (sonnet/opus/haiku) |
| `release-prompt-template` | No | Built-in | Path to custom release prompt template |
| `github-token` | No | `${{ github.token }}` | GitHub token for API operations |

## Example Usage

```yaml
name: Generate Release Notes
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate Release Notes
        uses: ./actions/release-notes-ai
        with:
          base-ref: 'v1.0.0'
          head-ref: 'v1.1.0'
          output-file: 'RELEASE_NOTES.md'
          claude-model: 'sonnet'

      - name: Upload Release Notes
        uses: actions/upload-artifact@v4
        with:
          name: release-notes
          path: RELEASE_NOTES.md
```

## How It Works

1. **Collects Data**:
   - Git commit logs between base and head refs
   - Merged PR information from GitHub
2. **AI Generation**: Uses Claude Code CLI to analyze and synthesize release notes
3. **Categorization**: Automatically groups changes by type
4. **Output**: Saves formatted release notes to specified file

## Customization

### Custom Release Prompts

Create a custom prompt template:
```markdown
# Custom Release Notes Template

Generate release notes for {{PROJECT_NAME}} focusing on:
- New features
- Bug fixes
- Breaking changes
- Migration guide

Format in Markdown with sections for each category.
```

Reference it in the workflow:
```yaml
- uses: ./actions/release-notes-ai
  with:
    release-prompt-template: '.github/release-templates/custom.md'
```

## Typical Output Structure

```markdown
# Release Notes v1.1.0

## ✨ New Features
- Feature A description
- Feature B description

## 🐛 Bug Fixes
- Bug fix A
- Bug fix B

## ⚠️ Breaking Changes
- Breaking change description with migration notes

## 📝 Other Changes
- Documentation updates
- Refactoring changes
```

## Requirements

- Claude Code CLI must be installed on the runner
- GitHub token with `repo` scope (for PR information)
- Git history must be available (use `fetch-depth: 0` in checkout)

## See Also

- [Setup guide](../../instructions/release-notes-ai.md)
- [Release workflow example](../../examples/release-workflow.yml)
