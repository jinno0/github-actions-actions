# Code Style and Conventions

## File Naming

- **Action directories**: `kebab-case` (e.g., `review-and-merge`, `action-fixer`)
- **Action definitions**: `action.yml` (singular) in each action directory
- **Template files**: `descriptive_name.txt` in `templates/` subdirectory
- **Example workflows**: `{action-name}-example.yml` in `examples/`
- **Instruction guides**: `{action-name}.md` in `instructions/`

## YAML Conventions

### Action Structure
- Use `runs: using: "composite"` for all actions
- Define all inputs with `description` and `default` (if applicable)
- Use `|` (literal style scalar) for multi-line shell scripts
- **Avoid heredoc** in YAML - use `echo` or template files instead

### Input/Output Naming
- **kebab-case** for input/output names (e.g., `prompt-template`, `auto-fix`)
- Use descriptive names (e.g., `gh-token` instead of `token`)

### Placeholder Convention (Templates)
- Format: `{VARIABLE_NAME}` (uppercase snake_case)
- Example: `{SOURCE_PATH}`, `{PR_NUMBER}`, `{VERDICT}`
- Replace using: `sed -e "s/{VARIABLE_NAME}/$value/g"`

## Shell Script Conventions

1. **Variable Expansion**:
   - Always quote variables: `"$VARIABLE"`
   - Use `${}` for clarity: `"${{ inputs.token }}"`

2. **Error Handling**:
   - Use `set -e` for fail-fast behavior
   - Check command exit codes explicitly

3. **Conditional Logic**:
   ```bash
   if [ -n "$VAR" ] && [ -f "$FILE" ]; then
     # ...
   fi
   ```

4. **String Replacement**:
   ```bash
   sed -e "s/{PLACEHOLDER}/$VALUE/g" template.txt
   ```

## Action Development Pattern

### 1. Create Action Structure
```bash
actions/my-new-action/
├── action.yml
└── templates/
    └── prompt.txt
```

### 2. Define action.yml
```yaml
name: 'My New Action'
description: 'Does one thing well'
inputs:
  my-input:
    description: 'Input description'
    required: true
    default: 'default-value'
outputs:
  my-output:
    description: 'Output description'
    value: ${{ steps.run-script.outputs.result }}
runs:
  using: 'composite'
  steps:
    - name: Run script
      id: run-script
      shell: bash
      run: |
        # Your logic here
        echo "result=value" >> $GITHUB_OUTPUT
```

### 3. Create Example Workflow
```yaml
name: 'My New Action Example'
on: [push]
jobs:
  example:
    runs-on: self-hosted
    steps:
      - uses: ./actions/my-new-action
        with:
          my-input: 'test'
```

### 4. Write Instruction Guide
See `instructions/` directory for examples - must include:
- Prerequisites
- Setup Instructions
- Usage

## Documentation Standards

### README.md
- Overview table of all Actions
- Links to examples and instructions
- Prerequisites section
- Developer guide link (AGENTS.md)

### Instruction Guides
- **Prerequisites**: What's needed before use
- **Setup Instructions**: Step-by-step setup
- **Usage**: How to use triggers and options
- Include complete examples

## Version Management

- Use Git tags for versioning: `v1.0.0`, `v1.1.0`, `v2.0.0`
- Major version for breaking changes
- Minor version for features
- Patch version for fixes
- **Never** reference `@main` in workflows

## Testing Strategy

- Manual testing via example workflows
- Validate YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('action.yml'))"`
- Check structure: action.yml + example + instruction must exist
- Test on self-hosted runner with Claude Code CLI installed
