# Auto Refactor

Automatically refactor code to improve quality, readability, and maintainability using Claude Code CLI.

## Features

- **AI-Powered Refactoring**: Context-aware code improvements using Claude
- **Custom Instructions**: Tailor refactoring to your project's needs
- **Multi-Language Support**: Works with any programming language
- **Safe Operations**: Validates paths before refactoring
- **Flexible Targeting**: Refactor single files or entire directories

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `path` | **Yes** | - | File or directory to refactor |
| `instruction` | No | `Improve code quality...` | Specific refactoring instructions |
| `claude-model` | No | `sonnet` | Claude model to use (sonnet/opus/haiku) |
| `refactor-prompt-template` | No | Built-in | Path to custom refactor prompt template |

## Example Usage

### Basic Refactoring

```yaml
name: Auto Refactor
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  refactor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Refactor Changed Files
        uses: ./actions/auto-refactor
        with:
          path: 'src/'
          instruction: 'Improve readability and add type hints'

      - name: Commit Refactoring
        run: |
          git config user.name 'GitHub Actions Bot'
          git config user.email 'bot@github.com'
          git add .
          git diff --staged --quiet || git commit -m "Refactor code"
          git push
```

### Specific Refactoring Tasks

```yaml
# Convert callbacks to async/await
- uses: ./actions/auto-refactor
  with:
    path: 'src/api/'
    instruction: |
      Convert all callback-based code to async/await pattern.
      Ensure proper error handling.

# Add type hints
- uses: ./actions/auto-refactor
  with:
    path: 'src/utils.py'
    instruction: |
      Add comprehensive type hints to all functions.
      Use typing module for complex types.

# Improve performance
- uses: ./actions/auto-refactor
  with:
    path: 'src/algorithms/'
    instruction: |
      Optimize for performance.
      Use appropriate data structures.
      Add algorithmic complexity comments.
```

### Interactive Refactoring

Trigger refactoring via comment:

```yaml
name: Refactor on Command
on:
  issue_comment:
    types: [created]

jobs:
  refactor:
    if: contains(github.event.comment.body, '/refactor')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Parse Command
        id: parse
        run: |
          COMMENT="${{ github.event.comment.body }}"
          # Extract: /refactor <path> <instruction>
          echo "Continue..."

      - name: Execute Refactoring
        uses: ./actions/auto-refactor
        with:
          path: ${{ steps.parse.outputs.path }}
          instruction: ${{ steps.parse.outputs.instruction }}
```

## Common Refactoring Instructions

### Code Quality
```yaml
instruction: |
  - Improve variable naming for clarity
  - Extract complex logic into separate functions
  - Add comprehensive docstrings
  - Remove code duplication
```

### Modernization
```yaml
instruction: |
  - Upgrade to modern syntax (e.g., f-strings in Python)
  - Replace deprecated APIs
  - Use language-specific best practices
  - Apply language version-specific features
```

### Performance
```yaml
instruction: |
  - Identify and optimize bottlenecks
  - Use appropriate data structures
  - Add lazy loading where beneficial
  - Cache expensive operations
```

### Security
```yaml
instruction: |
  - Sanitize user inputs
  - Use parameterized queries
  - Validate all external data
  - Add security-related comments
```

### Testing
```yaml
instruction: |
  - Make code more testable
  - Extract dependencies for easier mocking
  - Add test fixtures
  - Improve test coverage
```

## Custom Refactor Templates

Create a custom template:

```bash
cat > .github/refactor-templates/strict.md << 'EOF'
You are refactoring code for a mission-critical system.

Requirements:
- Do not change external APIs
- Maintain backward compatibility
- Add comprehensive error handling
- Include type hints for all parameters
- Add docstrings with examples
- Ensure thread safety
- Add logging at key points
- Follow project's style guide strictly
EOF
```

Use it:
```yaml
- uses: ./actions/auto-refactor
  with:
    path: 'src/core/'
    refactor-prompt-template: '.github/refactor-templates/strict.md'
```

## Best Practices

### 1. Start Small
```yaml
# Good: Target specific module
path: 'src/auth/password-reset.ts'

# Risky: Entire codebase at once
path: 'src/'
```

### 2. Be Specific
```yaml
# Good: Clear objective
instruction: 'Convert Promise chains to async/await'

# Vague: Too broad
instruction: 'Make it better'
```

### 3. Review Changes
Always review refactored code before merging:
```yaml
- name: Create PR for Review
  run: |
    git checkout -b refactor/$(date +%s)
    git commit -am "Auto refactor"
    gh pr create --title "Auto Refactor" --body "Review changes"
```

### 4. Use Branch Protection
Require reviews for refactored code:
```yaml
# In branch protection rules:
# - Require pull request reviews
# - Require status checks to pass
# - Include test suite in required checks
```

## Safety Features

### Path Validation
```yaml
# These will be rejected:
path: '../../../etc/passwd'
path: '/absolute/path/outside/repo'

# These will work:
path: 'src/utils.ts'
path: 'lib/components/'
```

### Pre-Checks
- Verifies target path exists
- Validates file permissions
- Checks template path if provided

## Workflow Integration Examples

### Pre-Merge Refactoring
```yaml
name: PR Quality Check
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get Changed Files
        id: changed
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }})
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: Refactor Changed Files
        uses: ./actions/auto-refactor
        with:
          path: ${{ steps.changed.outputs.files }}
          instruction: 'Improve code quality and fix lint issues'

      - name: Run Tests
        run: npm test

      - name: Comment Results
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              body: '✅ Auto-refactoring complete. Review changes.'
            })
```

### Scheduled Maintenance
```yaml
name: Weekly Refactor
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  refactor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Refactor Deprecated Code
        uses: ./actions/auto-refactor
        with:
          path: 'src/legacy/'
          instruction: 'Update deprecated APIs and improve patterns'

      - name: Run Full Test Suite
        run: npm test

      - name: Create PR
        if: success()
        run: |
          git checkout -b refactor/weekly-$(date +%Y%m%d)
          git commit -am "Weekly auto-refactor"
          git push origin refactor/weekly-$(date +%Y%m%d)
          gh pr create --title "Weekly Refactor" --body "Automated refactoring"
```

## Requirements

- Claude Code CLI installed on runner
- GitHub token with `contents:write` scope
- Runner must have write permissions

## See Also

- [Setup guide](../../instructions/auto-refactor.md) - Quick setup instructions
- [Review and Merge action](../review-and-merge/) - Pair with review for quality assurance
- [Auto Document action](../auto-document/) - Update docs after refactoring
