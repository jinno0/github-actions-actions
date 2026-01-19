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
- Expires After Runs: 15
- Linked: ReviewAutoMergeAction / AMB-003
- Revert Triggers: user_requests_consolidation, similarity_increases_above_078
