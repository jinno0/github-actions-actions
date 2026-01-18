# Suggested Commands

## Project Structure Commands

```bash
# List all actions
ls -d actions/*/

# Check action structure compliance
for action in actions/*/; do
  name=$(basename "$action")
  echo "Checking $name:"
  echo "  action.yml: $([ -f "$action/action.yml" ] && echo '✓' || echo '✗')"
  echo "  example: $([ -f "examples/${name}-example.yml" ] && echo '✓' || echo '✗')"
  echo "  instruction: $([ -f "instructions/${name}.md" ] && echo '✓' || echo '✗')"
done
```

## Validation Commands

```bash
# Validate YAML syntax for all actions
find actions -name 'action.yml' -exec python3 -c "import yaml; yaml.safe_load(open('{}'))" \;

# Check for @main references (forbidden)
grep -r "@main" examples/

# Lint YAML files
find actions -name '*.yml' -o -name '*.yaml' | xargs yamllint

# Check for heredoc in action.yml (anti-pattern)
grep -E '<< EOF|<< "EOF"' actions/*/action.yml
```

## Testing Commands

```bash
# Run all action tests
for action in actions/*/; do
  [ -f "$action/test.sh" ] && bash "$action/test.sh" || echo "No test for $action"
done

# Test specific action
bash actions/review-and-merge/test.sh
```

## Git Commands

```bash
# Create a new version tag
git tag -a v1.0.0 -m "Release v1.0.0: Feature description"
git push origin v1.0.0

# List tags
git tag -l

# Show recent commits
git log --oneline -10

# Check git status
git status
```

## File System Commands

```bash
# Find all template files
find actions -name 'templates' -type d -exec ls -la {} \;

# List all example workflows
ls -la examples/*.yml

# List all instruction guides
ls -la instructions/*.md

# Check concept sync status
ls -la .concept/
```

## Claude Code CLI Commands (on self-hosted runner)

```bash
# Check Claude Code CLI version
claude --version

# Run Claude Code with task
claude --task "Review this PR" --context .

# Run with timeout
timeout 300 claude --task "Fix the issue" --max-tokens 4000
```

## GitHub CLI Commands

```bash
# View PR
gh pr view 123

# List PRs
gh pr list

# Comment on PR
gh pr comment 123 --body "LGTM!"

# Merge PR
gh pr merge 123 --squash
```

## Utility Commands

```bash
# Search for patterns in action files
grep -r "inputs:" actions/*/action.yml

# Find all uses of Claude Code CLI
grep -r "claude" actions/

# Check permissions in examples
grep -r "permissions:" examples/

# View file count and size
find actions -type f | wc -l
du -sh actions/
```

## Concept Sync Commands

```bash
# View concept status
cat .concept/decisions.md

# Check unmapped concepts
grep "__UNMAPPED__" .concept/mappings.yml

# View invariants
cat .concept/invariants.yml
```

## Development Workflow Commands

```bash
# Create new action (template)
mkdir -p actions/my-new-action/templates
cat > actions/my-new-action/action.yml << 'EOF'
name: 'My New Action'
description: 'Does one thing well'
inputs:
  example-input:
    description: 'Example input'
    required: false
runs:
  using: 'composite'
  steps:
    - shell: bash
      run: |
        echo "Running my action"
EOF

# Create example workflow
cat > examples/my-new-action-example.yml << 'EOF'
name: 'My New Action Example'
on: [push]
jobs:
  example:
    runs-on: self-hosted
    steps:
      - uses: ./actions/my-new-action
EOF

# Create instruction guide
cat > instructions/my-new-action.md << 'EOF'
# My New Action

## Prerequisites
- Self-hosted runner
- Claude Code CLI

## Setup
1. Copy example workflow
2. Configure inputs

## Usage
Trigger on push/PR
EOF
```

## Troubleshooting Commands

```bash
# Check action syntax
yamllint actions/*/action.yml

# Verify template file references
grep -h "templates/" actions/*/action.yml

# Check for hardcoded prompts (anti-pattern)
grep -E "PROMPT=.*You are" actions/*/action.yml

# Verify all actions have required structure
for action in actions/*/; do
  name=$(basename "$action")
  missing=0
  [ ! -f "$action/action.yml" ] && echo "$name: Missing action.yml" && missing=1
  [ ! -f "examples/${name}-example.yml" ] && echo "$name: Missing example" && missing=1
  [ ! -f "instructions/${name}.md" ] && echo "$name: Missing instruction" && missing=1
  [ $missing -eq 0 ] && echo "$name: ✓ Complete"
done
```
