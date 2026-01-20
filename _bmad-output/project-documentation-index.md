# GitHub Actions Actions - Project Documentation

**Generated:** 2025-01-21
**Project Type:** GitHub Actions Collection
**Documentation Mode:** Initial Scan (Autonomous)

## Project Overview

This repository is a collection of reusable GitHub Actions for CI/CD automation, code review, documentation generation, and development workflow automation.

### Repository Structure

```
github-actions-actions/
├── actions/              # Action implementations (15 actions)
├── examples/             # Usage example workflows
├── instructions/         # Setup and usage guides
├── .github/              # GitHub workflows
├── docs/                 # Documentation
├── AGENTS.md             # AI agent instructions
├── PURPOSE.md            # Project goals and priorities
├── SYSTEM_CONSTITUTION.md # Layer0: Unchangeable rules
└── README.md             # Project overview
```

## Actions Catalog

### 1. action-fixer
**Purpose:** Automatically fix code issues using AI
- **Path:** `actions/action-fixer/`
- **Key Features:** Issue detection, automatic fixes, commit creation
- **Templates:** `fix_prompt.txt`

### 2. auto-document
**Purpose:** Generate documentation from source code
- **Path:** `actions/auto-document/`
- **Key Features:** Source analysis, doc generation, README updates
- **Templates:** `doc_prompt.txt`

### 3. auto-refactor
**Purpose:** Refactor code based on instructions
- **Path:** `actions/auto-refactor/`
- **Key Features:** Instruction-based refactoring, code improvement
- **Templates:** `refactor_prompt.txt`

### 4. release-notes-ai
**Purpose:** Generate release notes using AI
- **Path:** `actions/release-notes-ai/`
- **Key Features:** Git log analysis, PR summarization, changelog generation
- **Templates:** `release_prompt.txt`

### 5. review-and-merge
**Purpose:** Automated PR review and merge
- **Path:** `actions/review-and-merge/`
- **Key Features:** PR review, approval logic, auto-merge
- **Templates:** `review_prompt.txt`, `comment_template.txt`

### 6. spec-to-code
**Purpose:** Generate code from specifications
- **Path:** `actions/spec-to-code/`
- **Key Features:** Spec parsing, code generation, multi-language support
- **Templates:** `gen_prompt.txt`

### Additional Actions
- **code-quality-check**: Code quality and standards validation
- **dependencies-check**: Dependency vulnerability scanning
- **performance-test**: Performance testing automation
- **security-scan**: Security scanning and reporting
- **test-automation**: Test generation and execution
- (Additional actions as present in repository)

## Architecture Patterns

### Template System
All actions use a template-based prompt system:
- **Location:** `actions/{name}/templates/*.txt`
- **Placeholder Format:** `{VARIABLE_NAME}`
- **Loading:** Dynamic template loading in `action.yml`
- **Customization:** Users can provide custom templates via inputs

### Standard Action Structure
Each action includes:
1. **Implementation:** `actions/{name}/action.yml`
2. **Templates:** `actions/{name}/templates/*.txt`
3. **Example:** `examples/{name}-example.yml`
4. **Instructions:** `instructions/{name}.md`

### YAML Best Practices
- **Avoid heredoc:** Use `echo` or template files instead
- **Placeholder naming:** `{UPPER_SNAKE_CASE}`
- **Security:** Quote variables, validate inputs

## CI/CD Integration

### Testing
- **Workflow:** `.github/workflows/test-all-actions.yml`
- **Triggers:** PR, push to main, manual
- **Features:** Dry run testing, YAML validation, structure checks

### Dry Run Mode
All actions support dry run execution:
- **Environment Variable:** `DRY_RUN=true`
- **Behavior:** Simulate execution without actual commits/pushes
- **Logging:** Log would-be operations

## Development Guidelines

### For New Actions
1. Create `actions/{name}/action.yml`
2. Add templates to `actions/{name}/templates/`
3. Create example workflow in `examples/{name}-example.yml`
4. Document in `instructions/{name}.md`
5. Run dry run tests locally
6. Verify CI passes

### Code Style
- **Language:** Bash/Shell for action.yml run blocks
- **Python:** For testing and tooling
- **Encoding:** UTF-8
- **Line Endings:** LF

## Project Constitution (Layer0)

From `SYSTEM_CONSTITUTION.md`:
- Change control rules
- Security requirements
- Quality standards
- (See file for complete rules)

## Current Priorities

From `PURPOSE.md`:
- **Goal:** Production-ready GitHub Actions
- **Non-goals:** (See PURPOSE.md for details)
- **Success Criteria:** Actions tested, documented, and usable

## AI Agent Instructions

From `AGENTS.md`:
- Auto-embedding system for runtime context
- Required reading sequence for agents
- Task execution workflow
- Feedback mechanisms

## Testing and Validation

### Local Testing
```bash
# YAML syntax check
find actions -name 'action.yml' -exec python3 -c "import yaml; yaml.safe_load(open('{}'))" \;

# Structure check
for action in actions/*/; do
  name=$(basename "$action")
  echo "Checking $name..."
done
```

### CI Testing
- Automatic on PR/push
- Manual trigger available
- Validates structure, syntax, and templates

## Dependencies

### Runtime
- Self-hosted runners (for Claude CLI access)
- Claude Code CLI (`claude` command)
- Bash shell

### Development
- Python 3.x (for testing)
- GitHub Actions

## Security Considerations

- Input validation on all user inputs
- Command injection prevention
- Token permissions minimization
- Secret handling via GitHub Secrets

## Maintenance

### Versioning
- Semantic versioning for actions
- Changelog in release notes
- Backward compatibility considerations

### Updating Actions
1. Modify `action.yml` or templates
2. Update examples and instructions
3. Run tests locally
4. Verify CI passes
5. Tag release

## Documentation Assets

### Existing Documentation
- `README.md`: Project overview
- `AGENTS.md`: AI agent guidelines
- `PURPOSE.md`: Project goals
- `SYSTEM_CONSTITUTION.md`: Constitutional rules
- `instructions/*.md`: Per-action setup guides

### Generated Documentation
This document serves as a comprehensive reference for:
- Repository structure
- Action catalog
- Architecture patterns
- Development workflows
- Testing and validation

## Autonomously Generated Information

**Decision Log:**
- Prerequisite workflow (1-pre-implementation-flow) not completed - skipped
- No traditional PRD/Architecture/Story artifacts exist (repository is action collection)
- Proceeded directly to documentation phase
- Generated comprehensive catalog of existing GitHub Actions

**Autonomous Decisions:**
- Used conservative defaults for missing configuration
- Analyzed existing repository structure
- Catalogued all actions and their relationships
- Documented template system and patterns

**Next Steps for Users:**
1. Review specific action instructions in `instructions/` directory
2. Examine example workflows in `examples/` directory
3. Refer to `AGENTS.md` for AI agent development guidelines
4. Check `PURPOSE.md` for project priorities

---

**Document Version:** 1.0.0
**Last Updated:** 2025-01-21T06:13:00Z
**Generated By:** BMAD Implementation & Test Flow (Autonomous Mode)
