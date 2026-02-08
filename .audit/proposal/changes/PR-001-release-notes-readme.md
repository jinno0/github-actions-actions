# PR-001: Add README for release-notes-ai Action

**Priority:** Low
**Status:** Proposed
**Gap ID:** DG-001, FG-005
**Assumption Dependency:** None

## Problem Statement

The `release-notes-ai` action is missing its README.md file, while:
- It has an action.yml metadata file
- It has an example workflow
- It has an instruction guide
- It is listed as a production-ready action in ACTIONS.md

This creates an inconsistency in documentation completeness and makes it harder for users to quickly understand the action's purpose and usage.

## Proposed Solution

Create `actions/release-notes-ai/README.md` following the same pattern as other actions.

### File Structure

```
actions/release-notes-ai/
├── action.yml
├── README.md          # ← Create this
└── scripts/
    └── generate.sh
```

### README Template (Suggested)

```markdown
# Release Notes AI

Automatically generate comprehensive release notes from commit history and pull requests using Claude Code CLI.

## Features

- AI-powered summarization of changes
- Categorizes changes by type (features, fixes, breaking changes, etc.)
- Customizable output templates
- Automatic changelog generation
- Supports tag-based or date-based ranges

## Prerequisites

- Self-hosted runner with Claude Code CLI installed
- GitHub token with repository read access

## Inputs

### `since-tag` (required)
The starting tag for the release notes range.
Example: `v1.0.0`

### `until-tag` (optional)
The ending tag. If not specified, uses the latest tag.
Example: `v1.1.0`

### `output-path` (optional)
Path where the release notes will be written.
Default: `RELEASE_NOTES.md`

### `template-path` (optional)
Path to custom Jinja2 template for formatting.
Default: Uses built-in template

## Outputs

### `release-notes-path`
Path to the generated release notes file.

### `commits-count`
Number of commits included in the release notes.

## Example Usage

### Basic Usage

```yaml
name: Generate Release Notes
on:
  release:
    types: [published]

jobs:
  release-notes:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: Generate Release Notes
        uses: ./actions/release-notes-ai
        with:
          since-tag: 'v1.0.0'

      - name: Upload Release Notes
        uses: actions/upload-artifact@v3
        with:
          name: release-notes
          path: RELEASE_NOTES.md
```

### Custom Template

```yaml
- name: Generate with Custom Template
  uses: ./actions/release-notes-ai
  with:
    since-tag: 'v1.0.0'
    template-path: '.github/templates/release-notes.md'
```

## Customization

### Template Format

The default template organizes changes by category:

```markdown
# Release {{ version }}

## 🚀 Features
{% for commit in features %}
- {{ commit.message }}
{% endfor %}

## 🐛 Bug Fixes
{% for commit in fixes %}
- {{ commit.message }}
{% endfor %}

## 💥 Breaking Changes
{% for commit in breaking %}
- {{ commit.message }}
{% endfor %}
```

## Tips

1. **Semantic Versioning**: Works best with semantic versioning tags
2. **Conventional Commits**: Follows conventional commit format for better categorization
3. **Release Workflow**: Use with GitHub Release events for automatic notes generation

## Troubleshooting

**Issue**: "No commits found"
**Solution**: Ensure the `since-tag` exists and there are commits between tags

**Issue**: "Claude CLI not found"
**Solution**: Install Claude Code CLI on the self-hosted runner

**Issue**: "Poor summarization"
**Solution**: Use conventional commit format for better AI understanding

## See Also

- [Usage Guide](../../instructions/release-notes-ai.md)
- [Example Workflow](../../examples/release-notes-ai-example.yml)
```

## Implementation Steps

1. Create `actions/release-notes-ai/README.md`
2. Follow the template structure above
3. Ensure consistency with other action READMEs
4. Verify all links are correct

## Verification Criteria

- [ ] README.md exists at `actions/release-notes-ai/README.md`
- [ ] Contains Prerequisites section
- [ ] Contains Inputs section with all parameters from action.yml
- [ ] Contains Outputs section
- [ ] Contains Example Usage section
- [ ] Links to instruction guide and example workflow are correct
- [ ] Follows same formatting style as other action READMEs

## Expected Benefits

1. **Improved Discoverability**: Users can quickly understand the action's purpose
2. **Consistency**: All actions have complete documentation
3. **Reduced Support**: Fewer questions about usage
4. **Better Onboarding**: New users can adopt the action faster

## Risks

- **Low Risk**: Documentation-only change
- **No Breaking Changes**: Does not affect functionality
- **Rollback**: Simple file deletion if needed

## Alternatives Considered

1. **Do Nothing**: Keep relying on instruction guide only
   - **Rejected**: Inconsistent with other actions

2. **Link directly to instruction guide from ACTIONS.md**
   - **Rejected**: README is the standard first place users look

## Estimated Effort

- **Time**: 30 minutes
- **Complexity**: Low
- **Files Changed**: 1 (create)

## Related Issues

- Closes gap DG-001 (missing documentation)
- Addresses FG-005 (partial implementation of release-notes-ai)
