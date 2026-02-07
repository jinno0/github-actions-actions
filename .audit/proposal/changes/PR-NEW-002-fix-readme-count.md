# PR-NEW-002: Fix README.md Action Count

**Status:** Open
**Priority:** Low
**Gap ID:** ISS-NEW-006
**Estimated Effort:** 10 minutes
**Type:** documentation

## Summary

Update README.md to accurately reflect the current number of actions (12 instead of 13).

## Gap Being Addressed

- **Gap ID:** ISS-NEW-006
- **Title:** README.mdのAction数が実際と不一致
- **Impact:** 軽微なドキュメント不一致
- **Evidence:** C-006

## Problem

README.md:8 states:
> 現在、以下の AI Actions を提供しています（全13件）。

However, the actual count is 12 actions:

```bash
$ find actions -name "action.yml" | wc -l
12
```

**List of Actions:**
1. action-fixer
2. auto-document
3. auto-merge
4. auto-refactor
5. bulk-merge-prs
6. bulk-rebase-prs
7. pr-review-enqueuer
8. publish-pr
9. release-notes-ai
10. review-and-merge
11. review-auto-merge
12. spec-to-code

## Solution

Update line 8 of README.md from:
```markdown
現在、以下の AI Actions を提供しています（全13件）。
```

To:
```markdown
現在、以下の AI Actions を提供しています（全12件）。
```

### Investigation Step (Optional)

Before making the change, investigate why the discrepancy exists:
1. Was an action removed?
2. Was this a typo from the beginning?
3. Check git history for when the count became incorrect

This investigation may reveal if a 13th action was planned but never created.

## Expected Outcome

- README accurately reflects the repository state
- User confusion is eliminated

## Rollback Plan

If the count should actually be 13 (e.g., a 13th action is being developed):
1. Revert the change
2. Add a comment about the upcoming action

**Risk Level:** Very Low - documentation change only

## Alternatives Considered

1. **Add a 13th action** - Rejected: Out of scope for this PR
2. **Leave as-is** - Rejected: Causes confusion for users

## Related Issues

- Closes ISS-NEW-006
- Improves documentation accuracy

## Notes

- This is a trivial fix that improves documentation quality
- Consider whether the count should be dynamically generated in the future
- The discrepancy has existed since at least the previous audit cycle
