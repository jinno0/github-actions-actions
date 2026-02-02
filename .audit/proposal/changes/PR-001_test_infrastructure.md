# PR-001: Test Infrastructure for Remaining 10 Actions

**Priority**: Critical
**Effort**: High (20 hours)
**Related GAP**: GAP-001

## Problem
README.md では「全てのAI ActionsはDry Runモードで自動検証」と主張しているが、実際には3/13アクションしかテストが存在しない。

## Solution
残り10アクションのテストインフラを整備する。

## Scope

### Target Actions
1. auto-document
2. auto-merge
3. auto-rebase
4. auto-refactor
5. bulk-merge-prs
6. bulk-rebase-prs
7. pr-review-enqueuer
8. publish-pr
9. release-notes-ai
10. review-auto-merge

### Implementation Pattern
各アクションに以下のテストを実装:
- `test_action_yaml_exists`
- `test_action_required_inputs`
- `test_action_yaml_syntax_valid`
- `test_template_files_exist`
- `test_action_directory_structure`
- `test_action_has_composite_run_type`

## Changes

### Files to Create
```
tests/test_auto_document/test_auto_document_action.py
tests/test_auto_merge/test_auto_merge_action.py
tests/test_auto_rebase/test_auto_rebase_action.py
tests/test_auto_refactor/test_auto_refactor_action.py
tests/test_bulk_merge_prs/test_bulk_merge_prs_action.py
tests/test_bulk_rebase_prs/test_bulk_rebase_prs_action.py
tests/test_pr_review_enqueuer/test_pr_review_enqueuer_action.py
tests/test_publish_pr/test_publish_pr_action.py
tests/test_release_notes_ai/test_release_notes_ai_action.py
tests/test_review_auto_merge/test_review_auto_merge_action.py
```

### Files to Modify
- `tests/conftest.py`: Add new fixtures if needed

## Verification

### Manual Testing
```bash
pytest tests/ -v
# Expected: 260 tests pass (from current 60)
```

### Acceptance Criteria
- [ ] All 10 actions have dedicated test directories
- [ ] All 260 tests pass
- [ ] Test coverage for each action > 80%
- [ ] README.md claim is now accurate

## Rollback Plan
Remove test directories if quality issues arise. No production impact.

## Timeline
- Week 1: auto-document, auto-merge, auto-rebase
- Week 2: auto-refactor, bulk-merge-prs, bulk-rebase-prs
- Week 3: pr-review-enqueuer, publish-pr
- Week 4: release-notes-ai, review-auto-merge

## Estimated Impact
- Test count: 60 → 260 tests
- Coverage scope: 3/13 → 13/13 actions
- Maintains 95.3% coverage rate
