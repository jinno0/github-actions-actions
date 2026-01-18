# Task Completion Checklist

## When a Task is Completed

After completing any task (feature implementation, bug fix, refactoring), go through this checklist:

### 1. Code Quality

- [ ] **Single Responsibility**: Does each Action have exactly ONE clear purpose?
- [ ] **YAML Syntax**: Validated with `python3 -c "import yaml; yaml.safe_load(open('action.yml'))"`
- [ ] **No Hardcoded Prompts**: Prompts are in `templates/` directory
- [ ] **No Heredoc**: Used `echo` or template files instead of `<< EOF`
- [ ] **Proper Quoting**: All shell variables are quoted: `"$VARIABLE"`

### 2. Structure Compliance

- [ ] **Action Triple**: Action has (1) `action.yml`, (2) `example workflow`, (3) `instruction guide`
- [ ] **Naming**: Uses `kebab-case` for directories and files
- [ ] **Placeholders**: Template placeholders use `{VARIABLE_NAME}` format
- [ ] **Inputs/Outputs**: All have descriptions and defaults where applicable

### 3. Documentation

- [ ] **Action.yml**: Contains name, description, inputs, outputs
- [ ] **Example**: Complete working example in `examples/`
- [ ] **Instruction**: Includes Prerequisites, Setup, Usage sections
- [ ] **README**: Updated if new action or major feature

### 4. Testing

- [ ] **YAML Validation**: `find actions -name 'action.yml' -exec python3 -c "import yaml; yaml.safe_load(open('{}'))" \;`
- [ ] **Structure Check**: Action + example + instruction all exist
- [ ] **Manual Test**: Example workflow runs successfully on self-hosted runner
- [ ] **No @main**: Verified with `grep -r "@main" examples/`

### 5. Concept Sync

- [ ] **Ontology**: New concepts added to `.concept/ontology.yml` if needed
- [ ] **Mappings**: New concepts mapped to code/DB/API
- [ ] **Invariants**: New invariants added if required
- [ ] **Decisions**: Logged decision rationale
- [ ] **Bloat Check**: Verified no unnecessary concept proliferation

### 6. Git and Versioning

- [ ] **Changes Staged**: `git add` for all modified files
- [ ] **Commit Message**: Clear description of what and why
- [ ] **Version Tag**: Updated if breaking change or new feature
- [ ] **No @main**: Workflows use version tags (e.g., `uses: owner/repo@v1`)

### 7. Quality Gates (from autopilot.yml)

```bash
# Run lint
find actions -name '*.yml' -o -name '*.yaml' | xargs yamllint

# Run structure check
for action in actions/*/; do
  name=$(basename "$action")
  if [ ! -f "examples/${name}-example.yml" ] || [ ! -f "instructions/${name%.md}.md" ]; then
    echo "Missing example or instruction for $action"
    exit 1
  fi
done

# Run tests
for action in actions/*/; do
  [ -f "$action/test.sh" ] && bash "$action/test.sh" || true
done
```

### 8. Verification

- [ ] **Local Test**: Action works in example workflow locally
- [ ] **Self-Hosted Runner**: Confirmed Claude Code CLI is available
- [ ] **Permissions**: Workflow has necessary permissions
- [ ] **Security**: No secrets hardcoded, use inputs/secrets

### 9. Integration

- [ ] **Organization-Wide**: Action doesn't depend on repository-specific paths
- [ ] **Reusable**: Works in any repo in the organization
- [ ] **Dependencies**: Only uses commonly available tools (bash, gh, claude)

### 10. Final Checks

- [ ] **AGENTS.md Compliance**: Followed all conventions from AGENTS.md
- [ ] **Constitution Check**: Doesn't violate SYSTEM_CONSTITUTION.md
- [ ] **Purpose Alignment**: Supports charter milestones
- [ ] **No Regressions**: Existing actions still work

## Quick Validation Command

```bash
# Run all checks at once
echo "=== Validating YAML syntax ==="
find actions -name 'action.yml' -exec python3 -c "import yaml; yaml.safe_load(open('{}'))" \; && echo "✓ YAML valid"

echo -e "\n=== Checking structure ==="
for action in actions/*/; do
  name=$(basename "$action")
  [ -f "$action/action.yml" ] && [ -f "examples/${name}-example.yml" ] && [ -f "instructions/${name}.md" ] && echo "✓ $name complete" || echo "✗ $name incomplete"
done

echo -e "\n=== Checking for @main references ==="
(grep -r "@main" examples/ && echo "✗ Found @main references") || echo "✓ No @main references"

echo -e "\n=== Linting YAML ==="
(find actions -name '*.yml' -o -name '*.yaml' | xargs yamllint 2>&1 | head -20) || echo "✓ YAML lint passed"

echo -e "\n=== Validation complete ==="
```

## Before Committing

1. Review the checklist above
2. Run quality gates from `autopilot.yml`
3. Update documentation if needed
4. Stage and commit with clear message
5. Create tag if version update
6. Push and verify on self-hosted runner

## Common Issues and Solutions

| Issue | Check | Solution |
|-------|-------|----------|
| YAML parse error | `python3 -c "import yaml; yaml.safe_load(open('action.yml'))"` | Fix indentation/syntax |
| Action not found | `ls actions/*/action.yml` | Verify action directory exists |
| Template missing | `ls actions/*/templates/` | Create template file |
| Example workflow fails | `yamllint examples/*.yml` | Fix YAML syntax |
| Claude not found | `claude --version` on runner | Install Claude Code CLI |
| Permission denied | Check `permissions:` in workflow | Add required permissions |
