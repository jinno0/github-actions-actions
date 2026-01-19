# Active AUTO Decisions (cache) — safe to delete

## AUTO:AutoFix.lgtm_on_success
- Status: ACTIVE
- Chosen: auto-fix成功時はconfidence=10としてLGTM扱い
- Policy: industry_convention
- Expires After Runs: 20
- Linked: AutoFix

## AUTO:ConflictResolution.theirs_priority
- Status: ACTIVE
- Chosen: 競合解決はtheirs（base branch）を採用
- Policy: safety
- Expires After Runs: 20
- Linked: ConflictResolution

## AUTO:PublishPrAction.single_responsibility
- Status: ACTIVE
- Chosen: 単一責務（draft→ready変換のみ）としてdomain layerに配置
- Policy: single_responsibility
- Expires After Runs: 20
- Linked: PublishPrAction

## AUTO:AutoMergeAction.single_responsibility
- Status: ACTIVE
- Chosen: 単一責務（マージのみ）としてdomain layerに配置
- Policy: single_responsibility
- Expires After Runs: 20
- Linked: AutoMergeAction

## AUTO:ReviewAutoMergeAction.distinct_from_automerge
- Status: ACTIVE
- Chosen: Keep separate for now. ReviewAutoMergeAction focuses on retry logic, AutoMergeAction on method configuration. Similarity 0.72 < 0.78 threshold.
- Policy: similarity_threshold + pragmatic_separation
- Expires After Runs: 15 (created: 2026-01-19T01:28:18Z)
- Linked: ReviewAutoMergeAction / AMB-003
- Revert Triggers: user_requests_consolidation, similarity_increases_above_078

## AUTO:ReviewAndFixAction.replaces_review_merge
- Status: ACTIVE
- Chosen: ReviewAndMergeActionの後継としてdraft扱い
- Policy: evolutionary + conservative
- Expires After Runs: 20 (created: 2026-01-18T14:21:00Z)
- Linked: ReviewAndFixAction / ASM-REVIEWFIX-001
- Revert Triggers: user_explicit_feedback, breaking_change

## AUTO:ReviewAutoMergeAction.cohesive_workflow
- Status: ACTIVE
- Chosen: rebase+mergeは単一のマージワークフローの一部として結合（単一責務違反ではない）
- Policy: single_responsibility + cohesion
- Expires After Runs: 20 (created: 2026-01-19T13:08:00Z)
- Linked: ReviewAutoMergeAction / CFLT-002 (resolved)
- Revert Triggers: user_explicit_feedback, invariant_violation_detected
