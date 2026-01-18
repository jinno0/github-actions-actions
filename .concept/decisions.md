# Active AUTO Decisions (cache) — safe to delete

## AUTO:ReviewAndMergeAction.refactoring_strategy
- Status: ACTIVE
- Chosen: ReviewAndFixAction replaces ReviewAndMergeAction; new split actions follow single responsibility
- Policy: single_responsibility + clarity
- Expires After Runs: 20
- Linked: AMB-001
- Revert Triggers: user_explicit_feedback, breaking_change_detected

## AUTO:StandardActionStructure.gap_tolerance
- Status: ACTIVE
- Chosen: Gap is high-severity violation. Must create examples/instructions or mark as internal-only.
- Policy: invariant_enforcement + safety
- Expires After Runs: 10
- Linked: AMB-002 / CFLT-001
- Revert Triggers: actions_marked_internal, explicit_exemption_granted

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

## AUTO:ReviewAndFixAction.replaces_review_merge
- Status: ACTIVE
- Chosen: ReviewAndMergeActionの後継としてdraft扱い
- Policy: clarity
- Expires After Runs: 20
- Linked: ReviewAndFixAction

## AUTO:StandardActionStructure.enforcement
- Status: ACTIVE
- Chosen: 違反をhigh severityとして扱い、是正アクションを要求
- Policy: invariant_enforcement
- Expires After Runs: 10
- Linked: INV-STD-STRUCT-003
