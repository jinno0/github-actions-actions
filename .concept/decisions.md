# Active AUTO Decisions (cache) — safe to delete

_Last regenerated: 2026-01-22T00:30:00Z_

## AUTO:DryRun.term:accept_as_domain
- Status: ACTIVE
- Chosen: DryRun accepted as domain term with 3 evidence sources
- Policy: evidence_threshold + boundaries_clarity
- Evidence:
  - CLAUDE.md#L298-L324 (definition)
  - README.md#L43-L45 (description)
  - CLAUDE.md#L338-L367 (CI workflow implementation)
- Expires After Runs: 20
- Linked: TP-001
- Revert Triggers: primary_evidence_contradiction, better_merge_candidate

## AUTO:CIWorkflow.term:merge_into_CompositeAction
- Status: ACTIVE
- Chosen: CIWorkflow merged into CompositeAction (0.72 similarity)
- Policy: bloat_control + semantic_similarity
- Rationale: CI workflow is CompositeAction with testing lifecycle
- Expires After Runs: 20
- Linked: TP-002
- Revert Triggers: distinct_usage_patterns, structural_divergence

## AUTO:TestSuite.term:merge_into_DryRun
- Status: ACTIVE
- Chosen: TestSuite merged into DryRun (0.68 similarity)
- Policy: bloat_control + semantic_similarity
- Rationale: Test scripts are implementation detail of DryRun validation, not distinct concept
- Expires After Runs: 10
- Linked: TP-003
- Revert Triggers: test_becomes_independent_concept
