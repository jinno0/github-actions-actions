# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

---

## Advanced Workflow Patterns

For more complex, multi-phase agent workflows (e.g., code review, deployment, testing, security analysis), refer to the comprehensive workflow patterns documented in:

`.claude/skills/agent-creator/references/workflow_patterns.md`

That document provides detailed phase breakdowns for:
- Code Review workflows (6 phases: Architecture, Quality, Security, Performance, Testing, Documentation)
- Deployment workflows (5 phases: Validation, Execution, Health Check, Rollback, Post-deployment)
- Testing workflows (5 phases: Planning, Execution, Analysis, Quality Validation, Reporting)
- Documentation workflows (5 phases: Analysis, Content Generation, Structure, Quality Assurance, Maintenance)
- Security workflows (5 phases: Scanning, Threat Analysis, Compliance, Risk Assessment, Reporting)
- General Purpose workflows (5 phases: Requirements, Information Gathering, Problem Decomposition, Execution, Synthesis)

Use those patterns when creating sophisticated agents that require structured, multi-phase approaches.