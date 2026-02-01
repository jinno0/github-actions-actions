# GitHub Actions - AI Actions Hub

Complete catalog of AI-powered GitHub Actions for automating development workflows with Claude Code CLI.

## Overview

This repository contains a collection of reusable GitHub Actions that leverage Claude Code CLI to provide intelligent automation capabilities. These actions are designed for self-hosted runners and can perform context-aware code review, generation, refactoring, and documentation tasks.

## Quick Reference

| Action | Purpose | Status |
|--------|---------|--------|
| **[review-and-merge](actions/review-and-merge/)** | AI-powered PR review with auto-fix | ✅ Production Ready |
| **[spec-to-code](actions/spec-to-code/)** | Generate code from Markdown specs | ✅ Production Ready |
| **[auto-refactor](actions/auto-refactor/)** | Intelligent code refactoring | ✅ Production Ready |
| **[auto-document](actions/auto-document/)** | Automatic documentation updates | ✅ Production Ready |
| **[action-fixer](actions/action-fixer/)** | Fix workflow syntax errors | ✅ Production Ready |
| **[release-notes-ai](actions/release-notes-ai/)** | Generate release notes | ✅ Production Ready |

---

## Development Support Actions

### AI Review and Fix
**Path:** `actions/review-and-merge/`

Automatically review pull requests using Claude Code CLI with context-aware analysis.

**Key Features:**
- Intelligent code review with confidence scoring
- Automatic issue fixing
- Custom review rules and templates
- LGTM/auto-merge support

**Quick Start:**
```yaml
- uses: ./actions/review-and-merge
  with:
    claude-model: 'sonnet'
    lgtm-threshold: '7'
    auto-fix: 'true'
```

**Documentation:** [README](actions/review-and-merge/README.md) | [Usage Guide](instructions/review-and-merge.md)

---

### Spec to Code
**Path:** `actions/spec-to-code/`

Convert Markdown specifications into production-ready code.

**Key Features:**
- Multi-language support (Python, TypeScript, Go, etc.)
- Security-first design with path validation
- Custom generation templates
- Base64 encoding for special characters

**Quick Start:**
```yaml
- uses: ./actions/spec-to-code
  with:
    spec-path: 'specs/feature.md'
    output-dir: 'src/'
    language: 'TypeScript'
```

**Documentation:** [README](actions/spec-to-code/README.md) | [Usage Guide](instructions/spec-to-code.md)

---

### Auto Refactor
**Path:** `actions/auto-refactor/`

Intelligently refactor code to improve quality and maintainability.

**Key Features:**
- Context-aware refactoring
- Custom instruction support
- Safe path validation
- File or directory targeting

**Quick Start:**
```yaml
- uses: ./actions/auto-refactor
  with:
    path: 'src/'
    instruction: 'Improve readability and add type hints'
```

**Documentation:** [README](actions/auto-refactor/README.md) | [Usage Guide](instructions/auto-refactor.md)

---

## Documentation Actions

### Auto Document
**Path:** `actions/auto-document/`

Keep documentation synchronized with code changes automatically.

**Key Features:**
- Intelligent code analysis
- Flexible documentation targeting
- Custom style templates
- Multi-language support

**Quick Start:**
```yaml
- uses: ./actions/auto-document
  with:
    source-path: 'src/'
    doc-path: 'README.md'
```

**Documentation:** [README](actions/auto-document/README.md) | [Usage Guide](instructions/auto-document.md)

---

### Release Notes AI
**Path:** `actions/release-notes-ai/`

Generate comprehensive release notes from commit history and PRs.

**Key Features:**
- AI-powered summarization
- Categorizes changes by type
- Customizable templates
- Changelog generation

**Quick Start:**
```yaml
- uses: ./actions/release-notes-ai
  with:
    since-tag: 'v1.0.0'
```

**Documentation:** [Usage Guide](instructions/release-notes-ai.md)

---

## Maintenance Actions

### Action Fixer
**Path:** `actions/action-fixer/`

Automatically detect and fix GitHub Actions workflow syntax errors.

**Key Features:**
- YAML syntax validation
- Automatic error correction
- Schema validation
- Best practices enforcement

**Quick Start:**
```yaml
- uses: ./actions/action-fixer
  with:
    workflow-path: '.github/workflows/'
```

**Documentation:** [Usage Guide](instructions/action-fixer.md)

---

## Automation Actions

### Auto Merge
**Path:** `actions/auto-merge/`

Automatically merge pull requests when specific criteria are met.

**Key Features:**
- Configurable merge conditions
- Branch protection integration
- Status check validation

---

### Auto Rebase
**Path:** `actions/auto-rebase/`

Automatically rebase branches onto the latest base branch.

**Key Features:**
- Conflict detection
- Automatic retry on conflicts
- Notification support

---

### Bulk Merge PRs
**Path:** `actions/bulk-merge-prs/`

Merge multiple pull requests in batch with validation.

**Key Features:**
- Batch processing
- Dependency-aware merging
- Rollback support

---

### Bulk Rebase PRs
**Path:** `actions/bulk-rebase-prs/`

Rebase multiple branches simultaneously.

**Key Features:**
- Parallel processing
- Conflict handling
- Progress reporting

---

## Workflow Orchestration

### Review and Auto Merge
**Path:** `instructions/review-and-auto-merge-workflow.md`

Complete workflow combining AI review with automatic merging.

**Flow:**
1. PR opened/updated
2. AI review with confidence scoring
3. Auto-fix if issues found
4. Auto-merge if LGTM threshold met
5. Comment with review summary

---

## Prerequisites

### Required Setup

1. **Self-Hosted Runner**
   - Runner must have access to Claude Code CLI
   - Recommended: Ubuntu 20.04+ or similar
   - At least 2GB RAM, 2 CPU cores

2. **Claude Code CLI Installation**
   ```bash
   npm install -g @anthropic-ai/claude-code-cli
   ```

3. **GitHub Token Permissions**
   - `contents:write` - For committing changes
   - `pull-requests:write` - For PR operations
   - `issues:write` - For commenting

### Optional Dependencies

- **gh CLI** - For GitHub API operations
- **Python 3.8+** - For Python-based actions
- **Node.js 16+** - For Node-based actions

---

## Usage Patterns

### Pattern 1: PR Quality Gate

Ensure code quality before merging:

```yaml
name: PR Quality Check
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality-gate:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: AI Review
        uses: ./actions/review-and-merge
        with:
          lgtm-threshold: '8'
          auto-fix: 'true'

      - name: Refactor if Needed
        if: steps.review.outputs.confidence < 8
        uses: ./actions/auto-refactor

      - name: Update Docs
        uses: ./actions/auto-document
```

### Pattern 2: Spec-Driven Development

Generate code from specifications:

```yaml
name: Spec to Code
on:
  push:
    paths:
      - 'specs/**/*.md'

jobs:
  generate:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: Generate Code
        uses: ./actions/spec-to-code
        with:
          spec-path: '${{ github.event.changed_files[0] }}'

      - name: Generate Tests
        uses: ./actions/spec-to-code
        with:
          spec-path: '${{ github.event.changed_files[0] }}'
          output-dir: 'tests/'

      - name: Update Documentation
        uses: ./actions/auto-document
```

### Pattern 3: Continuous Improvement

Maintain code quality over time:

```yaml
name: Weekly Maintenance
on:
  schedule:
    - cron: '0 0 * * 0'

jobs:
  maintenance:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: Refactor Legacy Code
        uses: ./actions/auto-refactor
        with:
          path: 'src/legacy/'
          instruction: 'Update to modern patterns'

      - name: Update All Documentation
        uses: ./actions/auto-document
        with:
          source-path: 'src/'
          doc-path: 'README.md'

      - name: Fix Workflow Issues
        uses: ./actions/action-fixer
```

---

## Customization

### Custom Prompt Templates

All actions support custom prompt templates for tailored behavior:

```yaml
- uses: ./actions/review-and-merge
  with:
    review-prompt-template: '.github/prompts/custom-review.md'
```

### Example Custom Template

```markdown
# .github/prompts/custom-review.md

You are reviewing code for a high-security financial application.

Focus areas:
1. Security vulnerabilities (OWASP Top 10)
2. Data validation and sanitization
3. Error handling and logging
4. Regulatory compliance (GDPR, PCI-DSS)

Reject if:
- User input not validated
- Hardcoded credentials
- Missing error handling
- Insecure dependencies
```

---

## Best Practices

### 1. Start Simple
Begin with basic configurations and gradually add complexity.

### 2. Review AI Suggestions
Always review AI-generated changes before merging.

### 3. Use Branch Protection
Require reviews for automated changes to critical paths.

### 4. Monitor Performance
Track AI action execution time and optimize if needed.

### 5. Maintain Context
Provide clear instructions and templates for better AI output.

---

## Troubleshooting

### Common Issues

**Issue:** "Claude Code CLI not found"
**Solution:** Ensure CLI is installed on self-hosted runner

**Issue:** "Permission denied"
**Solution:** Check GitHub token has required scopes

**Issue:** "Low confidence scores"
**Solution:** Improve custom rules and provide better context

**Issue:** "Generated code doesn't compile"
**Solution:** Be more specific in your spec files

---

## Contributing

Contributions are welcome! Please check for existing documentation in the repository for guidelines on contributing new actions or improving existing ones.

### Adding New Actions

1. Create action directory under `actions/`
2. Add `action.yml` with metadata
3. Implement scripts in `scripts/` subdirectory
4. Add README.md with documentation
5. Create usage guide in `instructions/`
6. Add tests to `tests/`

---

## Support

For issues, questions, or contributions, please refer to the main repository documentation.

---

## License

MIT License - see [LICENSE](LICENSE) for details

---

## Related Resources

- [Claude Code CLI Documentation](https://docs.anthropic.com/claude-code-cli)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Self-Hosted Runner Guide](https://docs.github.com/en/actions/hosting-your-own-runners)
