# Active AUTO Decisions (cache) — safe to delete

_Last regenerated: 2026-01-28T23:35:00Z (Run 2026-01-28T23:35:00Z)_

## Summary
- Active AUTO Decisions: 3 (within expiration window)
- Pending term: 1 (ApprovalScreen - awaiting implementation evidence)
- No current ambiguities requiring AUTO decisions
- No conflicts requiring workarounds

## AUTO:ApprovalScreen.term:keep_pending
- Status: ACTIVE
- Chosen: Keep ApprovalScreen pending - require implementation evidence
- Policy: conservative_implementation_required + aux_layer_classification
- Evidence:
  - .claude/commands/approve.md#L1-L3 (specification)
  - .claude/commands/approve.md#L5-L7 (specification)
- Rationale: |
  Both sources are spec/doc, not implemented code. Missing:
  - No clear boundaries (includes/excludes)
  - No mappings to actual code/API
  - Only specification, no implementation
  Acceptance requires: implementation evidence, mappings, test coverage
- Expires After Runs: 10 (created Run 2026-01-28T23:35:00Z, expires Run ~2026-01-29T09:35:00Z)
- Linked: TP-006
- Revert Triggers: implementation_evidence_provided, mappings_established

## AUTO:ExternalDispatch.term:accept_as_domain
- Status: ACTIVE
- Chosen: ExternalDispatch accepted as domain term with 2 evidence sources
- Policy: evidence_threshold + boundaries_clarity
- Evidence:
  - .github/workflows/external-dispatch.yml#L1-L5 (definition)
  - .github/workflows/external-dispatch.yml#L7-L15 (16 event types)
- Rationale: Distinct from CompositeAction (0.65 similarity < 0.78 threshold)
- Expires After Runs: 20 (created Run 24, expires Run 44)
- Linked: TP-004
- Revert Triggers: primary_evidence_contradiction, merge_threshold_breach

## AUTO:ScriptExtraction.term:accept_as_aux
- Status: ACTIVE
- Chosen: ScriptExtraction accepted as aux term with 2 evidence sources
- Policy: evidence_threshold + semantic_distinctness
- Evidence:
  - actions/review-and-merge/scripts/review-and-fix.sh#L1-L4 (actual implementation)
  - commit b2f8f31 (refactoring rationale)
- Rationale: Low merge similarity (max 0.52 < 0.78), distinct from TemplateFile and CompositeAction
- Expires After Runs: 20 (created Run 27, expires Run 47)
- Linked: TP-005
- Revert Triggers: primary_evidence_contradiction, merge_threshold_breach
