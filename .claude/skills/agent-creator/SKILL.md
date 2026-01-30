---
name: agent-creator
description: >
  Autonomous agent creation skill that generates specialized agent definitions from templates.
  Use when you need to create new Claude Code agents for specific tasks like code review,
  deployment automation, testing, documentation, security analysis, or general-purpose research.
  This skill automates the creation of agent definition files (.md) with proper structure,
  workflow instructions, and tool access patterns following Miyabi framework standards.
---

# Agent Creator

## Overview

This skill enables the automatic creation of specialized agents for the Miyabi framework. It generates agent definition files (.md) with complete workflows, tool access configurations, and quality standards based on established templates.

## Quick Start

```bash
# Initialize the agents directory
python .claude/skills/agent-creator/scripts/init_agent.py --init

# Generate a code review agent
python .claude/skills/agent-creator/scripts/generate_agent.py code-review-expert code-review

# Validate generated agent
python .claude/skills/agent-creator/scripts/validate_agent.py code-review-expert.md
```

## Available Agent Types

| Type | Purpose | Key Features |
|------|---------|--------------|
| `code-review` | Code quality analysis | Architecture, security, performance review |
| `deployment` | CI/CD automation | Deployment pipelines, health checks, rollback |
| `testing` | Test automation | Coverage analysis, quality gates |
| `documentation` | Documentation generation | API docs, technical writing |
| `security` | Security analysis | Vulnerability scanning, compliance |
| `general-purpose` | Research & coordination | Multi-step task management |

## Usage

### Basic Generation

```bash
python .claude/skills/agent-creator/scripts/generate_agent.py <name> <type>
```

### With Custom Options

```bash
# Custom description
python .claude/skills/agent-creator/scripts/generate_agent.py \
  security-auditor security \
  --description "Specialized security auditor for web applications"

# Custom capabilities
python .claude/skills/agent-creator/scripts/generate_agent.py \
  api-tester testing \
  --capabilities "API testing" "Load testing" "Integration testing"

# Custom tool access
python .claude/skills/agent-creator/scripts/generate_agent.py \
  documentation-writer documentation \
  --tools Read Write Edit Grep Glob

# Custom workflow guidance
python .claude/skills/agent-creator/scripts/generate_agent.py \
  blockchain-auditor security \
  --workflow "Focus on smart contract security, DeFi vulnerability patterns, and gas optimization"

# Dry run to preview
python .claude/skills/agent-creator/scripts/generate_agent.py \
  custom-agent general-purpose --dry-run
```

### Validation

```bash
# Validate specific agent
python .claude/skills/agent-creator/scripts/validate_agent.py <agent-name>.md

# Validate all agents
python .claude/skills/agent-creator/scripts/validate_agent.py --all
```

## Best Practices

### Naming Conventions

Use kebab-case with descriptive suffixes:
```
code-review-expert
deployment-automator
security-analyzer
documentation-generator
testing-orchestrator
```

### Quality Standards

All generated agents should:
- Maintain 80+ quality score thresholds
- Provide clear, actionable feedback
- Follow established coding standards
- Document significant decisions
- Include proper error handling
- Validate inputs and outputs

### Integration Patterns

- **Sequential**: `code-review → testing → deployment`
- **Parallel**: `(code-review AND security) → testing`
- **Research to Implementation**: `general-purpose → specialized-agent`

## Resources

### Scripts

- `generate_agent.py` - Main agent generation script
- `init_agent.py` - Directory setup and initialization
- `validate_agent.py` - Agent definition validation

### Documentation

- `references/agent_types.md` - Agent type reference and characteristics
- `references/workflow_patterns.md` - Workflow patterns and quality standards
- `assets/template_example.md` - Example of properly structured agent definition

---

*This agent-creator skill follows the Miyabi framework principles and integrates with the common library system for consistent environment management.*
