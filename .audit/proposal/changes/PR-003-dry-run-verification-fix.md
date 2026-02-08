# PR-003: Dry Run Verification Implementation (Critical)

**Status:** Proposed
**Priority:** P0 - CRITICAL
**Estimated Effort:** 2-3 days (Option 1) / 15 minutes (Option 2)
**Gap ID:** GAP-003

---

## Problem Statement

**Current State:**
- README.md:122-124 claims: "全てのAI ActionsはDry Runモードで自動検証されます"
- Actual implementation: Only 3/13 (23%) Actions have Dry Run verification
- **Gap**: Documentation and reality are significantly misaligned

**Implemented Actions (3/13):**
1. pr-review-enqueuer
2. bulk-rebase-prs
3. bulk-merge-prs

**Missing Implementation (10/13):**
1. action-fixer
2. review-and-merge
3. spec-to-code
4. auto-document
5. release-notes-ai
6. auto-rebase
7. review-auto-merge
8. auto-merge
9. auto-refactor
10. publish-pr

**Impact:**
- High: Repository credibility is at risk
- Users cannot safely test Actions before production use
- Documentation promises functionality that doesn't exist

---

## Proposed Solutions

### Option 1: Implement Dry Run Verification (RECOMMENDED)

**Approach:** Add Dry Run mode to all 10 missing Actions

**Implementation Pattern:**
```yaml
# In each action.yml
inputs:
  dry-run:
    description: "Dry run mode (no actual changes)"
    required: false
    default: false
    type: boolean

# In entrypoint script
if [ "${{ inputs.dry-run }}" = "true" ]; then
  echo "Dry run mode: skipping actual execution"
  # Print what would be done without doing it
  exit 0
fi
```

**Files to Modify:**
1. `actions/action-fixer/action.yml`
2. `actions/action-fixer/entrypoint.sh`
3. `actions/review-and-merge/action.yml`
4. `actions/review-and-merge/entrypoint.sh`
5. `actions/spec-to-code/action.yml`
6. `actions/spec-to-code/entrypoint.sh`
7. `actions/auto-document/action.yml`
8. `actions/auto-document/entrypoint.sh`
9. `actions/release-notes-ai/action.yml`
10. `actions/release-notes-ai/entrypoint.sh`
11. `actions/auto-rebase/action.yml`
12. `actions/auto-rebase/entrypoint.sh`
13. `actions/review-auto-merge/action.yml`
14. `actions/review-auto-merge/entrypoint.sh`
15. `actions/auto-merge/action.yml`
16. `actions/auto-merge/entrypoint.sh`
17. `actions/auto-refactor/action.yml`
18. `actions/auto-refactor/entrypoint.sh`
19. `actions/publish-pr/action.yml`
20. `actions/publish-pr/entrypoint.sh`

**Testing:**
```bash
# Test each action with dry-run
for action in action-fixer review-and-merge spec-to-code auto-document release-notes-ai auto-rebase review-auto-merge auto-merge auto-refactor publish-pr; do
  echo "Testing $action with dry-run..."
  # Add dry-run input to workflow
  # Verify no actual changes are made
  # Verify expected output is produced
done
```

**Benefits:**
- ✅ Aligns documentation with implementation
- ✅ Enables safe testing of all Actions
- ✅ Maintains repository's value proposition
- ✅ Improves user confidence

**Drawbacks:**
- ⏱️ Requires development time (2-3 days)
- 🔧 Need to update 20 files across 10 Actions

**Verification:**
```bash
# After implementation
pytest tests/ -k dry_run
# Expected: All 13 Actions pass dry-run tests
```

---

### Option 2: Update Documentation (QUICK FIX)

**Approach:** Update README.md to reflect current state

**Changes to `README.md`:**
```markdown
# BEFORE (line 122-124):
全ての AI Actions は Dry Run モードで自動検証されます。

# AFTER:
一部の AI Actions (3/13) で Dry Run モードが実装されています。
- 実装済み: pr-review-enqueuer, bulk-rebase-prs, bulk-merge-prs
- 未実装: action-fixer, review-and-merge, spec-to-code, auto-document, release-notes-ai, auto-rebase, review-auto-merge, auto-merge, auto-refactor, publish-pr
```

**Files to Modify:**
1. `README.md:122-124`

**Benefits:**
- ✅ Immediate documentation accuracy
- ✅ Minimal time investment (15 minutes)
- ✅ Transparent about current limitations

**Drawbacks:**
- ❌ Weakens repository's value proposition
- ❌ Users cannot safely test 10/13 Actions
- ❌ May reduce adoption rate

---

## Recommendation

**Choose Option 1 (Implement Dry Run Verification)**

**Rationale:**
1. **Strategic Alignment**: Dry Run verification is a core promise of the repository
2. **User Safety**: Essential for testing Actions before production use
3. **Credibility**: Maintains trust with users
4. **Competitive Advantage**: Distinguishes this repository from alternatives

**Implementation Plan:**
1. Day 1: Implement Dry Run for 5 Actions (action-fixer, review-and-merge, spec-to-code, auto-document, release-notes-ai)
2. Day 2: Implement Dry Run for 5 Actions (auto-rebase, review-auto-merge, auto-merge, auto-refactor, publish-pr)
3. Day 3: Testing and documentation updates

**Rollback Plan:**
```bash
# If issues arise, revert to Option 2
git revert <commit-hash>
# Update README.md as per Option 2
```

---

## Success Criteria

- [ ] All 13 Actions support dry-run input
- [ ] All 13 Actions pass dry-run tests
- [ ] README.md documentation is accurate
- [ ] Test coverage remains >= 80%
- [ ] No regressions in existing functionality

---

## Related Issues

- Gap: GAP-003
- Assumption: ASM-006 (rejected)
- Core Function: CF-004 (failed)
