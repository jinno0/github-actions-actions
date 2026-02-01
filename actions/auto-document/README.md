# Auto Document

Automatically keep documentation synchronized with code changes using Claude Code CLI's intelligent analysis.

## Features

- **Automatic Updates**: Keeps docs in sync with code changes
- **Intelligent Analysis**: Understands code context and generates meaningful documentation
- **Flexible Targeting**: Update any markdown documentation file
- **Custom Templates**: Support for documentation style guidelines
- **Multi-Language**: Works with any programming language

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `source-path` | No | `.` | Path to source code to analyze |
| `doc-path` | No | `README.md` | Path to documentation file to update |
| `claude-model` | No | `sonnet` | Claude model to use (sonnet/opus/haiku) |
| `doc-prompt-template` | No | Built-in | Path to custom doc prompt template |

## Example Usage

### Basic Documentation Update

```yaml
name: Update Documentation
on:
  push:
    branches: [main]

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Update README
        uses: ./actions/auto-document
        with:
          source-path: 'src/'
          doc-path: 'README.md'

      - name: Commit Documentation
        run: |
          git config user.name 'GitHub Actions Bot'
          git config user.email 'bot@github.com'
          git add README.md
          git diff --staged --quiet || git commit -m "Update documentation"
          git push
```

### Update API Documentation

```yaml
- name: Update API Docs
  uses: ./actions/auto-document
  with:
    source-path: 'src/api/'
    doc-path: 'docs/api.md'
```

### Update Multiple Documentation Files

```yaml
- name: Update Main README
  uses: ./actions/auto-document
  with:
    source-path: 'src/'
    doc-path: 'README.md'

- name: Update API Reference
  uses: ./actions/auto-document
  with:
    source-path: 'src/api/'
    doc-path: 'docs/api-reference.md'

- name: Update Contributing Guide
  uses: ./actions/auto-document
  with:
    source-path: '.github/workflows/'
    doc-path: 'CONTRIBUTING.md'
```

## Documentation Types

### API Documentation

```yaml
- name: Document API Endpoints
  uses: ./actions/auto-document
  with:
    source-path: 'src/api/controllers/'
    doc-path: 'docs/api/endpoints.md'
```

### Component Documentation

```yaml
- name: Document React Components
  uses: ./actions/auto-document
  with:
    source-path: 'src/components/'
    doc-path: 'docs/components.md'
```

### Usage Examples

```yaml
- name: Update Usage Examples
  uses: ./actions/auto-document
  with:
    source-path: 'examples/'
    doc-path: 'docs/usage.md'
```

## Custom Documentation Templates

Create a custom documentation style:

```bash
cat > .github/doc-templates/api-style.md << 'EOF'
You are generating API documentation.

Format:
## Endpoint Name
**Method**: GET/POST/PUT/DELETE
**Path**: /api/path

### Description
Brief description of what this endpoint does.

### Parameters
- `param1` (type): Description
- `param2` (type): Description

### Response
```json
{
  "field": "type"
}
```

### Example
\`\`\`bash
curl -X GET https://api.example.com/endpoint
\`\`\`
EOF
```

Use it:
```yaml
- uses: ./actions/auto-document
  with:
    source-path: 'src/api/'
    doc-path: 'docs/api.md'
    doc-prompt-template: '.github/doc-templates/api-style.md'
```

## Best Practices

### 1. Structure Your Documentation

Maintain clear sections in your documentation:

```markdown
# Project README

## Overview
[Brief project description]

## Installation
[Auto-generated from package.json/setup.py]

## Usage
[Auto-generated from examples/]

## API Reference
[Auto-generated from src/api/]

## Development
[Auto-generated from contributing docs]
```

### 2. Use Section Markers

Help the AI understand where to update:

```markdown
<!-- AUTO-GENERATED: API_DOCS -->
## API Reference
This section is auto-generated. Do not edit manually.
<!-- END-AUTO-GENERATED -->
```

### 3. Validate After Update

Always run checks after documentation updates:

```yaml
- name: Update Documentation
  uses: ./actions/auto-document
  with:
    source-path: 'src/'
    doc-path: 'README.md'

- name: Validate Markdown
  run: |
    npm install -g markdownlint-cli
    markdownlint README.md
```

## Workflow Examples

### PR Documentation Update

```yaml
name: Update PR Docs
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get Changed Files
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | grep '^src/')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: Update Affected Documentation
        if: steps.changed.outputs.files != ''
        uses: ./actions/auto-document
        with:
          source-path: ${{ steps.changed.outputs.files }}
          doc-path: 'README.md'

      - name: Comment Changes
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              body: '📝 Documentation updated automatically'
            })
```

### Release Documentation

```yaml
name: Release Docs
on:
  release:
    types: [published]

jobs:
  update-release-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Update Main Documentation
        uses: ./actions/auto-document
        with:
          source-path: 'src/'
          doc-path: 'README.md'

      - name: Generate Changelog
        uses: ./actions/auto-document
        with:
          source-path: '.'
          doc-path: 'CHANGELOG.md'

      - name: Commit to Release Branch
        run: |
          git checkout -b docs/${{ github.event.release.tag_name }}
          git add .
          git commit -m "Update documentation for ${{ github.event.release.tag_name }}"
          git push origin docs/${{ github.event.release.tag_name }}
```

### Multi-Language Project

```yaml
name: Update All Documentation
on:
  push:
    branches: [main]

jobs:
  update-docs:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        doc:
          - source: 'src/python/'
            target: 'docs/python.md'
          - source: 'src/typescript/'
            target: 'docs/typescript.md'
          - source: 'src/go/'
            target: 'docs/go.md'

    steps:
      - uses: actions/checkout@v4

      - name: Update Documentation
        uses: ./actions/auto-document
        with:
          source-path: ${{ matrix.doc.source }}
          doc-path: ${{ matrix.doc.target }}

      - name: Commit
        run: |
          git config user.name 'GitHub Actions Bot'
          git config user.email 'bot@github.com'
          git add ${{ matrix.doc.target }}
          git diff --staged --quiet || git commit -m "Update ${{ matrix.doc.target }}"
```

## Integration with Other Actions

### After Refactoring

```yaml
- name: Refactor Code
  uses: ./actions/auto-refactor
  with:
    path: 'src/'

- name: Update Documentation
  uses: ./actions/auto-document
  with:
    source-path: 'src/'
    doc-path: 'README.md'
```

### After Spec-to-Code

```yaml
- name: Generate Code
  uses: ./actions/spec-to-code
  with:
    spec-path: 'specs/feature.md'

- name: Document Generated Code
  uses: ./actions/auto-document
  with:
    source-path: 'src/generated/'
    doc-path: 'docs/generated-api.md'
```

## Requirements

- Claude Code CLI installed on runner
- GitHub token with `contents:write` scope
- Markdown documentation file must exist

## Tips

1. **Be Specific**: Narrow `source-path` for better results
2. **Review Changes**: Always review auto-generated docs before committing
3. **Maintain Structure**: Keep clear sections in your documentation
4. **Use Templates**: Custom templates ensure consistent style
5. **Validate**: Add markdown linting to catch formatting issues

## See Also

- [Auto Refactor action](../auto-refactor/) - Keep docs in sync after refactoring
- [Spec to Code action](../spec-to-code/) - Document generated code
- [Usage guide](../../instructions/auto-document.md)
