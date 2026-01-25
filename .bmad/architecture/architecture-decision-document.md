# Architecture Decision Document (ADD)
## AI Hub - GitHub Actions for AI-Native Development

**Document Version:** 1.0
**Last Updated:** 2026-01-26
**Project Status:** Phase 3 - Stabilization & Adoption
**Document Type:** Retrospective Architecture Documentation

---

## 1. Architecture Overview

### 1.1 System Purpose
AI Hub is a collection of composable GitHub Actions that leverage Claude Code CLI on self-hosted runners to provide intelligent automation for software development workflows. The architecture prioritizes modularity, human-in-the-loop oversight, and repository-agnostic reusability.

### 1.2 Design Philosophy
1. **Action Independence**: Each Action is self-contained with minimal dependencies
2. **Template-Based Configuration**: Prompts and messages externalized to templates
3. **Fail-Safe Operations**: Dry-run mode and validation before destructive operations
4. **Standardized Structure**: All Actions follow the same directory layout (action.yml, templates/, example, instruction)

### 1.3 Scope & Boundaries
- **In Scope**: GitHub Actions workflows, self-hosted runner orchestration, AI integration
- **Out of Scope**: Web UI, database storage, authentication (handled by GitHub), multi-model support (future)

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         GitHub Platform                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Repository │  │  Pull Request │  │   Workflow   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼─────────────────┐
│                     GitHub Actions Platform                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Trigger Event (push, pr, etc.)              │   │
│  └────────────────────┬─────────────────────────────────────┘   │
│                       │                                          │
│  ┌────────────────────▼─────────────────────────────────────┐   │
│  │         AI Hub Action (Composite Action)                  │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │ 1. Parse Inputs & Configuration                    │  │   │
│  │  │ 2. Load Templates (prompts, messages)              │  │   │
│  │  │ 3. Prepare Context (git logs, diffs, files)        │  │   │
│  │  │ 4. Execute Claude Code CLI                         │  │   │
│  │  │ 5. Parse AI Response                               │  │   │
│  │  │ 6. Apply Changes (commit, comment, merge)          │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────┬────────────────────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────────────────────────────┐
│                  Self-Hosted Runner Infrastructure               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Runner Environment (Container/VM)            │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │   │
│  │  │   Git CLI  │  │   Claude   │  │   Utils    │         │   │
│  │  │            │  │  Code CLI  │  │  (sed,     │         │   │
│  │  │            │  │            │  │   jq, etc) │         │   │
│  │  └────────────┘  └────────────┘  └────────────┘         │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────────────────────────────┐
│                    External AI Service                            │
│                  Anthropic Claude API                             │
└───────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Architecture

#### 2.2.1 Core Components

**GitHub Actions Layer**
- **Trigger System**: GitHub webhooks initiate workflows
- **Workflow Engine**: GitHub Actions orchestrates step execution
- **Composite Actions**: Reusable action definitions (action.yml)

**AI Hub Actions Layer**
- **Action Orchestrator**: Manages action execution flow
- **Template Engine**: Loads and substitutes placeholders in templates
- **Context Builder**: Gathers relevant context (git history, file contents)
- **AI Interface**: Invokes Claude Code CLI with prompts
- **Response Handler**: Parses AI output and executes operations

**Self-Hosted Runner Layer**
- **Runtime Environment**: Linux container with toolchain access
- **CLI Tools**: Git, Claude Code CLI, standard Unix utilities
- **Workspace**: Temporary file storage for operations

**External AI Service Layer**
- **Claude API**: Anthropic's language model API
- **Request/Response**: JSON payloads with prompts and completions

---

## 3. Data Architecture

### 3.1 Data Flow

```
┌──────────────┐
│   Trigger    │ (push, PR, manual)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Load       │ (action.yml, templates)
│  Templates   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Gather      │ (git log, diff, files)
│  Context     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Substitute  │ (replace {VARIABLES})
│  Placeholders│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Invoke      │ (claude command)
│  Claude CLI  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Parse       │ (extract AI response)
│  Response    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Execute     │ (commit, comment, merge)
│  Operations  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Return     │ (exit code, outputs)
│   Result     │
└──────────────┘
```

### 3.2 Data Models

**Action Configuration (action.yml)**
```yaml
name: string
description: string
inputs:
  input-name:
    description: string
    required: boolean
    default: string
outputs:
  output-name:
    description: string
    value: string
runs:
  using: composite
  steps: []
```

**Template Format (templates/*.txt)**
```
Human-readable prompt with {PLACEHOLDER} variables
Variables are substituted at runtime using sed
```

**Context Data**
- Git logs: Commit history, author, timestamp
- File diffs: Unified diff format
- PR metadata: Title, description, labels, author

---

## 4. Technology Stack

### 4.1 Core Technologies

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Orchestration** | GitHub Actions | Latest | Native GitHub integration |
| **Runtime** | Bash/Shell | POSIX | Universal availability on runners |
| **AI Engine** | Claude Code CLI | Latest | Official Anthropic CLI tool |
| **Language Model** | Claude Sonnet 4 | 20250929 | Balanced speed/capability |
| **Template Engine** | sed | GNU | Standard Unix utility, no dependencies |
| **Git Operations** | git | 2.x+ | Standard version control |
| **Data Processing** | jq | 1.6+ | JSON parsing for API responses |

### 4.2 Infrastructure

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Hosting** | GitHub Actions | Workflow execution platform |
| **Runners** | Self-hosted (Linux) | Full toolchain access, cost efficiency |
| **Container** | Docker (optional) | Isolated execution environments |
| **Storage** | Git Repository | Version-controlled code and configs |
| **Monitoring** | GitHub Actions Logs | Execution tracking and debugging |

### 4.3 External Dependencies

| Service | Purpose | SLA |
|---------|---------|-----|
| **Anthropic Claude API** | AI inference | Best-effort, with retry logic |
| **GitHub API** | Repository operations | Inherits GitHub's SLA |
| **N/A** | No database, no cache, no message queue | Stateless design |

---

## 5. Key Design Decisions

### 5.1 Decision Records

#### ADR-001: Self-Hosted Runners vs. GitHub-Hosted
**Status**: Accepted
**Context**: Need to execute Claude Code CLI with full filesystem access

**Decision**: Use self-hosted runners
**Rationale**:
- Full toolchain access (can install any CLI tool)
- Cost efficiency for high-volume AI operations
- Ability to access internal resources and services
- No restrictions on execution time

**Consequences**:
- (+) Unlimited flexibility in tooling
- (+) Better cost control
- (-) Operational overhead of maintaining runners
- (-) Need to manage runner scaling

#### ADR-002: Composite Actions vs. Custom JavaScript Actions
**Status**: Accepted
**Context**: Choose between composite (shell-based) or JavaScript (node-based) Actions

**Decision**: Use composite Actions with shell scripts
**Rationale**:
- Easier to read and modify by developers
- No npm dependencies or build process
- Direct access to system tools (git, claude CLI)
- Simpler debugging (can test locally)

**Consequences**:
- (+) Lower barrier to entry for contributors
- (+) Faster iteration without builds
- (-) Limited error handling compared to JavaScript
- (-) Platform-dependent (though standard Linux tools assumed)

#### ADR-003: Template-Based Prompts vs. Inline Prompts
**Status**: Accepted
**Context**: Where to store AI prompt templates

**Decision**: Externalize prompts to template files
**Rationale**:
- Separation of logic and content
- Easier to update prompts without touching action.yml
- Users can provide custom templates
- Better version control of prompt changes

**Consequences**:
- (+) Prompt maintenance is simpler
- (+) Customization via template injection
- (-) More files to manage
- (-) Need to track action.yml ↔ template dependencies

#### ADR-004: Human-in-the-Loop by Default
**Status**: Accepted
**Context**: Should AI Actions operate autonomously or require approval

**Decision**: Require human approval for destructive operations by default
**Rationale**:
- AI hallucination risk mitigation
- Maintains human accountability
- Allows gradual trust building
- Aligns with "AI proposes, human decides" philosophy

**Consequences**:
- (+) Safer deployment, especially in early stages
- (+) Learning opportunity from AI suggestions
- (-) Slower workflow than fully autonomous
- (-) Potential for approval fatigue

#### ADR-005: Dry-Run Mode for All Actions
**Status**: Accepted
**Context**: Need safe testing mechanism for Actions

**Decision**: All Actions must support dry-run mode
**Rationale**:
- Enables safe testing in production repos
- Facilitates CI/CD integration testing
- Allows validation before destructive operations
- Supports development workflow

**Consequences**:
- (+) Safe experimentation and learning
- (+) Automated testing in CI
- (-) Additional code complexity
- (-) Need to mock/simulate operations

#### ADR-006: Standardized Action Structure
**Status**: Accepted
**Context**: How to organize Action files and documentation

**Decision**: All Actions must have: action.yml, templates/, example.yml, instruction.md
**Rationale**:
- Consistent user experience across Actions
- Lowers learning curve
- Ensures complete documentation
- Enables automated validation

**Consequences**:
- (+) Predictable structure for users
- (+) Automated CI checks possible
- (-) More boilerplate for new Actions
- (-) May not fit all Action types

#### ADR-007: YAML Syntax Avoidance of Heredoc
**Status**: Accepted
**Context**: YAML multiline string syntax options

**Decision**: Avoid heredoc (<< EOF), use echo/sed instead
**Rationale**:
- Heredoc has inconsistent parsing across YAML parsers
- Echo/sed more portable and reliable
- Easier to debug when issues arise

**Consequences**:
- (+) Better YAML parser compatibility
- (+) More predictable behavior
- (-) Slightly more verbose syntax
- (-) Requires careful quoting

---

## 6. Integration Patterns

### 6.1 GitHub API Integration

**Authentication**:
```bash
GITHUB_TOKEN="${{ inputs.github-token }}"
export GITHUB_TOKEN
```

**Common Operations**:
- PR comments: `gh pr comment $PR_NUMBER --body-file comment.txt`
- Merging: `gh pr merge $PR_NUMBER --merge --delete-branch`
- Creating branches: `gh repo create-branch` (via git)

### 6.2 Claude Code CLI Integration

**Basic Invocation**:
```bash
claude --prompt "$PROMPT" > /tmp/claude_response.txt
```

**Error Handling**:
```bash
if ! claude --prompt "$PROMPT"; then
  echo "Claude CLI failed"
  exit 1
fi
```

**Response Parsing**:
```bash
RESPONSE=$(cat /tmp/claude_response.txt)
# Extract specific sections using sed/awk
```

### 6.3 Git Operations

**Safe Commit Pattern**:
```bash
git config user.name "AI Bot"
git config user.email "ai-bot@example.com"
git add .
git commit -m "$COMMIT_MSG"
git push
```

**Branch Safety**:
```bash
# Always operate on feature branch, never main
if [ "$(git branch --show-current)" = "main" ]; then
  echo "Cannot operate on main branch"
  exit 1
fi
```

---

## 7. Security Architecture

### 7.1 Security Principles

1. **Principle of Least Privilege**: Actions request only permissions they need
2. **Secrets Management**: Use GitHub Secrets for sensitive data
3. **Audit Trail**: Log all AI decisions and operations
4. **Sandboxing**: Execute in isolated runner environments

### 7.2 Threat Model

| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| **Prompt Injection** | Medium | High | Input validation, escape special chars |
| **Credential Exposure** | Low | Critical | Use GitHub Secrets, no logging |
| **Code Injection** | Low | High | Static analysis, review processes |
| **Data Exfiltration** | Low | Medium | No external API calls except Claude |
| **Resource Exhaustion** | Medium | Medium | Resource limits, timeouts |

### 7.3 Security Controls

**Input Validation**:
```bash
# Validate file paths to prevent directory traversal
if echo "$FILE" | grep -q '\.\.'; then
  echo "Invalid file path"
  exit 1
fi
```

**Secret Handling**:
```bash
# Never log secrets
set +x  # Disable command echo
SECRET="${{ secrets.API_KEY }}"
```

**Audit Logging**:
```bash
# Log all operations for compliance
echo "[$(date)] Action: $ACTION_NAME, PR: $PR_NUMBER, Decision: $DECISION" >> audit.log
```

---

## 8. Performance & Scalability

### 8.1 Performance Characteristics

| Action | Typical Duration | Max Duration | Bottleneck |
|--------|------------------|--------------|------------|
| review-and-merge | 2-3 min | 10 min | Claude API |
| spec-to-code | 3-5 min | 15 min | Code generation |
| action-fixer | 1-2 min | 5 min | Error parsing |
| auto-refactor | 3-5 min | 15 min | Analysis + changes |
| auto-document | 1-2 min | 5 min | File processing |
| release-notes-ai | 1-2 min | 5 min | Commit aggregation |

### 8.2 Scalability Considerations

**Horizontal Scaling**:
- Spin up more self-hosted runners
- Use runner groups for different teams
- Implement job queueing for high-demand periods

**Vertical Scaling**:
- Increase runner CPU/memory allocations
- Optimize CLI operations (parallel processing)
- Cache frequently accessed data

**Rate Limiting**:
- Implement exponential backoff for Claude API
- Use GitHub API rate limit awareness
- Queue operations when limits approached

---

## 9. Monitoring & Observability

### 9.1 Logging Strategy

**Action-Level Logs**:
- Structured JSON logs for machine parsing
- Human-readable logs for GitHub UI
- Separate stdout (results) and stderr (errors)

**Log Levels**:
```
DEBUG: Detailed execution trace
INFO: Normal operation milestones
WARN: Non-critical issues (retries, fallbacks)
ERROR: Failures requiring attention
```

**Example Log Format**:
```json
{
  "timestamp": "2026-01-26T10:00:00Z",
  "action": "review-and-merge",
  "run_id": 123456789,
  "level": "INFO",
  "message": "PR review completed",
  "pr_number": 123,
  "decision": "approve",
  "confidence": 0.95
}
```

### 9.2 Metrics Collection

**Key Metrics**:
- Action execution count (by action type)
- Success/failure rates
- Average execution time
- AI confidence scores
- Human acceptance rates

**Collection Method**:
- GitHub Actions logs (primary)
- Optional: Export to monitoring system (future)

### 9.3 Alerting

**Alert Conditions**:
- Action failure rate > 10% (1 hour window)
- Average execution time > 2x baseline
- Claude API error rate > 5%
- Runner unavailability

**Alert Channels**:
- GitHub Issues (auto-created)
- Slack notifications (optional integration)
- Email for critical alerts

---

## 10. Deployment Architecture

### 10.1 Deployment Strategy

**Version Control**:
- Semantic versioning for all Actions (v1.0.0, v1.1.0, etc.)
- Tagged releases for stable versions
- Main branch for development

**Rollout Process**:
1. Develop in feature branch
2. Test with dry-run mode
3. Create PR with changelog
4. Code review by team
5. Merge to main
6. Tag release
7. Users update references

**Rollback Plan**:
- Revert to previous git tag
- Users pin to specific version in workflows
- Hotfix process for critical issues

### 10.2 Environment Configuration

**Development Environment**:
- Local testing with Act (GitHub Actions local runner)
- Dry-run mode enabled
- Mock Claude CLI responses

**Staging Environment**:
- Self-hosted runner in isolated environment
- Test repositories with no production impact
- Real Claude API calls

**Production Environment**:
- Production self-hosted runners
- Real repositories and workflows
- Full monitoring and alerting

---

## 11. Testing Strategy

### 11.1 Testing Levels

**Unit Testing** (Not applicable - shell scripts):
- Individual function testing via bash scripts
- Template substitution testing

**Integration Testing**:
- Dry-run mode validation in CI
- Action workflow execution with mock data
- Template rendering validation

**End-to-End Testing**:
- Execute Actions on test repositories
- Validate actual git operations
- Test Claude API integration

**Example Test Script** (`test-action-fixer.sh`):
```bash
#!/bin/bash
# Test action structure
test_file_exists "actions/action-fixer/action.yml"
test_file_exists "actions/action-fixer/templates/fix_prompt.txt"
test_yaml_syntax "actions/action-fixer/action.yml"
test_example_exists "action-fixer-example.yml"
test_instruction_exists "action-fixer.md"
```

### 11.2 Test Automation

**CI Workflow** (`.github/workflows/test-all-actions.yml`):
- Trigger: PR to main, push to main
- Steps:
  1. Check Action structure
  2. Validate YAML syntax
  3. Run dry-run tests
  4. Verify template placeholders
  5. Check examples/instructions completeness

---

## 12. Disaster Recovery & Business Continuity

### 12.1 Backup Strategy

**Code Repository**:
- Git is distributed, inherently backed up
- GitHub provides repository mirroring
- Regular git clones to backup location

**Templates & Configuration**:
- Version controlled in git
- Tagged releases for rollback points

**Runner State**:
- Stateless design, no persistent data
- Ephemeral containers, auto-recovery

### 12.2 Recovery Procedures

**Scenario 1: Runner Failure**
- Detection: Health check fails
- Recovery: Terminate runner, autoscaling creates new one
- RTO: < 5 minutes

**Scenario 2: Claude API Outage**
- Detection: API calls fail
- Mitigation: Retry with exponential backoff
- Fallback: Queue jobs for later execution

**Scenario 3: Action Bug**
- Detection: Monitoring alerts, user reports
- Recovery: Rollback to previous tag
- RTO: < 1 hour (after fix validation)

**Scenario 4: Data Corruption**
- Detection: Git integrity checks
- Recovery: Restore from git history
- RTO: < 30 minutes

---

## 13. Future Architecture Evolution

### 13.1 Planned Enhancements

**Phase 4: Advanced Features (2026-Q3+)**

1. **Multi-Model Support**:
   - Abstract AI provider interface
   - Support for GPT-4, Gemini, etc.
   - Provider-specific optimizations

2. **Workflow Orchestration**:
   - Multi-action composition
   - Dependency management
   - State sharing between actions

3. **Analytics Dashboard**:
   - Usage metrics visualization
   - Cost tracking
   - Effectiveness analysis

4. **Custom Model Fine-Tuning**:
   - Organization-specific training
   - Private model deployment
   - Fine-tuned prompts per repo

### 13.2 Technical Debt & Refactoring Needs

| Area | Issue | Priority | Proposed Solution |
|------|-------|----------|-------------------|
| **Error Handling** | Limited error recovery in bash | Medium | Refactor to more robust error handling |
| **Testing** | No automated unit tests | High | Add test framework for shell scripts |
| **Configuration** | Hardcoded values in some Actions | Low | Externalize to config files |
| **Logging** | Inconsistent log formats | Medium | Standardize logging library/functions |

---

## 14. Architecture Decision Log

| Date | Decision | Context | Status |
|------|----------|---------|--------|
| 2025-12-01 | Use self-hosted runners | Infrastructure | Accepted |
| 2025-12-01 | Composite Actions over JavaScript | Development experience | Accepted |
| 2025-12-01 | Template-based prompts | Maintainability | Accepted |
| 2025-12-01 | Human-in-the-loop default | Safety | Accepted |
| 2025-12-01 | Dry-run mode requirement | Testing | Accepted |
| 2025-12-01 | Standardized structure | UX consistency | Accepted |
| 2025-12-01 | Avoid heredoc in YAML | Parser compatibility | Accepted |

---

## 15. Appendices

### 15.1 Action Registry

| Action | Purpose | Status | Dependencies |
|--------|---------|--------|--------------|
| review-and-merge | PR review + auto-merge | ✅ Stable | Claude CLI, gh |
| spec-to-code | Spec to code generation | ✅ Stable | Claude CLI |
| action-fixer | Workflow error fixing | ✅ Stable | Claude CLI |
| auto-refactor | AI-powered refactoring | ✅ Stable | Claude CLI |
| auto-document | Documentation updates | ✅ Stable | Claude CLI |
| release-notes-ai | Release note generation | ✅ Stable | Claude CLI |
| auto-merge | Simple auto-merge | ✅ Stable | gh |
| auto-rebase | Branch rebasing | ✅ Stable | git |
| bulk-merge-prs | Bulk PR merging | ✅ Stable | gh |
| bulk-rebase-prs | Bulk rebasing | ✅ Stable | git |
| pr-review-enqueuer | Review queueing | ✅ Stable | gh |
| publish-pr | PR publishing | ✅ Stable | gh |
| review-auto-merge | Combined review+merge | ✅ Stable | Claude CLI, gh |

### 15.2 File Structure Reference

```
github-actions-actions/
├── actions/                          # Action implementations
│   ├── {action-name}/
│   │   ├── action.yml                # Action definition
│   │   └── templates/                # Prompt templates
│   │       └── {template-name}.txt
├── examples/                         # Usage examples
│   └── {action-name}-example.yml
├── instructions/                     # User guides
│   └── {action-name}.md
├── .github/workflows/               # CI/CD workflows
├── .bmad/                           # BMAD artifacts (this doc)
│   ├── prd/
│   ├── architecture/
│   ├── ux-design/
│   ├── epics/
│   ├── stories/
│   └── sprint/
├── PURPOSE.md                       # Project mission
├── SYSTEM_CONSTITUTION.md           # Immutable principles
├── AGENTS.md                        # Developer guidelines
└── README.md                        # Project overview
```

### 15.3 References

- [PURPOSE.md](../PURPOSE.md) - Project mission and goals
- [SYSTEM_CONSTITUTION.md](../SYSTEM_CONSTITUTION.md) - Immutable principles
- [AGENTS.md](../AGENTS.md) - Developer guidelines
- [PRD](./prd/product-requirements-document.md) - Product requirements
- [Claude Code CLI Documentation](https://docs.anthropic.com/claude-code)

---

**Document Status**: ✅ Approved
**Architecture Review**: Completed
**Next Review**: 2026-04-26 or upon major changes
**Maintainers**: AI Hub Development Team
