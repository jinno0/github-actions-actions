# Active AUTO Decisions (cache) — safe to delete

_Last regenerated: 2026-01-30T09:10:00Z (Run 25)_

## Summary
- Active AUTO Decisions: 5 (term acceptance and merges)
- No ambiguities requiring AUTO decisions
- No conflicts requiring workarounds

## AUTO:ScriptExtraction.term:accept_as_aux
- Status: ACTIVE
- Chosen: ScriptExtraction accepted as aux term with 2 evidence sources
- Policy: evidence_threshold + semantic_distinctness
- Evidence:
  - actions/review-and-merge/scripts/review-and-fix.sh (implementation)
  - commit b2f8f31 (refactoring rationale)
- Rationale: Low merge similarity (max 0.52 < 0.78), distinct from TemplateFile and CompositeAction
- Expires After Runs: 20
- Linked: TP-005
- Revert Triggers: primary_evidence_contradiction, merge_threshold_breach

## Pending Queue Items (3)
- TP-006: SecurityVulnerability (aux) - 2 evidence sources, pending evaluation
- TP-007: CodeDuplication (aux) - 2 evidence sources, similarity 0.42 to CompositeAction
- TP-008: SharedLibraryInfrastructure (domain) - 2 evidence sources, similarity 0.55 to CompositeAction
