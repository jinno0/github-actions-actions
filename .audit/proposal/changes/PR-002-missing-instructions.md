# PR-002: Complete Documentation for Automation Actions

**Priority**: 2 (Usability improvement)
**Status**: Proposed
**Estimated Effort**: Low (2-3 hours)

## Problem

Four automation actions lack dedicated instruction files:
1. `auto-merge` - Automatic PR merging
2. `publish-pr` - Draft PR publishing
3. `bulk-merge-prs` - Bulk PR merging
4. `bulk-rebase-prs` - Bulk PR rebasing

While all actions have examples in `examples/`, the missing `instructions/*.md` files mean:
- Users must infer usage from example YAML only
- No detailed setup guidance
- No troubleshooting information
- Inconsistent documentation pattern

## Proposed Solution

### Action 1: Create instruction files following template

For each action, create `instructions/{action-name}.md` with sections:

```markdown
# {Action Name} - Setup Guide

## Overview
[Brief description of what this action does]

## Prerequisites
- [Required permissions]
- [Required configurations]
- [Any limitations]

## Setup Steps

### 1. Configure Permissions
[Detailed permission requirements]

### 2. Example Workflow
[Reference to examples/{action}-example.yml]

### 3. Customization
[Common customization options]

## Troubleshooting

### Issue: {Common problem}
**Solution**: {Fix}

### Issue: {Another problem}
**Solution**: {Fix}

## Advanced Usage
[For complex configurations]

## Related Actions
- [Link to related actions]
```

### Action 2: Create instruction file for `auto-merge`

File: `instructions/auto-merge.md`

Key points to document:
- Squash vs merge vs rebase options
- Required branch protection rules
- Status check requirements
- Permission scope needed

### Action 3: Create instruction file for `publish-pr`

File: `instructions/publish-pr.md`

Key points to document:
- Draft PR detection logic
- Label-based triggering
- Permission requirements
- Integration with review workflows

### Action 4: Create instruction file for `bulk-merge-prs`

File: `instructions/bulk-merge-prs.md`

Key points to document:
- Input format (PR list)
- Bulk operation safety considerations
- Rollback procedures
- Rate limiting awareness

### Action 5: Create instruction file for `bulk-rebase-prs`

File: `instructions/bulk-rebase-prs.md`

Key points to document:
- Conflict handling
- Input format
- Dependency ordering
- Verification steps

## Benefits

1. **Consistency**: All actions follow same documentation pattern
2. **Usability**: Users have complete guidance for setup
3. **Reduced Support**: Fewer questions, faster adoption
4. **Quality**: Satisfies QC-002 constraint ("Every action must have setup instructions")

## Risks

- **Risk**: Documentation may become outdated if actions change
  - **Mitigation**: Include documentation review in action modification checklist

## Verification

**Success Criteria**:
- [ ] `instructions/auto-merge.md` exists and complete
- [ ] `instructions/publish-pr.md` exists and complete
- [ ] `instructions/bulk-merge-prs.md` exists and complete
- [ ] `instructions/bulk-rebase-prs.md` exists and complete
- [ ] Each file follows standard template structure
- [ ] README.md table includes these actions (if not already)

**Validation Method**:
```bash
# Verify all instruction files exist
ls -1 instructions/*.md | wc -l  # Should be 13 (one per action)

# Verify template structure
for f in instructions/auto-merge.md instructions/publish-pr.md instructions/bulk-merge-prs.md instructions/bulk-rebase-prs.md; do
    grep -q "## Overview" $f && grep -q "## Prerequisites" $f && grep -q "## Troubleshooting" $f
done
```

## Rollback

If documentation causes confusion:
```bash
# Remove new instruction files
rm instructions/auto-merge.md instructions/publish-pr.md instructions/bulk-merge-prs.md instructions/bulk-rebase-prs.md
```

Examples remain in `examples/` as fallback documentation.

## Alternatives Considered

1. **Add only minimal comments to existing examples**
   - **Rejected**: Instructions provide dedicated space for detailed guidance
2. **Consolidate all automation actions into single guide**
   - **Rejected**: Reduces discoverability, harder to maintain
3. **Skip documentation (users can figure it out)**
   - **Rejected**: Violates QC-002, increases support burden

## Related Gaps

- Closes: GAP-003 (Missing instructions for some actions)

## Related Constraints

- Satisfies: QC-002 ("Every action must have setup instructions")
