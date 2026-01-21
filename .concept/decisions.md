# Active AUTO Decisions (cache) — safe to delete

_Last regenerated: 2026-01-21T03:23:06Z_

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
