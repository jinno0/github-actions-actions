# Active AUTO Decisions (cache) — safe to delete

_Last regenerated: 2026-01-30T13:00:00Z (Run 26)_

## Summary
- Active AUTO Decisions: 8 (term acceptance and queue rejections)
- No ambiguities requiring AUTO decisions
- No conflicts requiring workarounds

## Queue AUTO Decisions (Run 26)

### AUTO:TP-006:reject
- Status: ACTIVE
- Chosen: REJECTED - SecurityVulnerability merged into CompositeAction
- Policy: semantic_subsumption
- Rationale: Security vulnerabilities are quality concerns within CompositeAction development, not a distinct canonical concept
- Confidence: 0.82
- Evidence: 2 sources (code review report, completion report)
- Expires After Runs: 20
- Revert Triggers: primary_evidence_contradiction, security_domain_emergence

### AUTO:TP-007:reject
- Status: ACTIVE
- Chosen: REJECTED - CodeDuplication merged into CompositeAction
- Policy: semantic_subsumption
- Rationale: Code duplication is a quality metric within CompositeAction development, not a distinct canonical concept
- Confidence: 0.79
- Evidence: 2 sources (completion report, code review report)
- Expires After Runs: 20
- Revert Triggers: primary_evidence_contradiction, quality_metrics_domain_emergence

### AUTO:TP-008:reject
- Status: ACTIVE
- Chosen: REJECTED - SharedLibraryInfrastructure merged into CompositeAction
- Policy: semantic_subsumption
- Rationale: Shared library infrastructure is an implementation solution pattern within CompositeAction development, not a distinct canonical concept
- Confidence: 0.71
- Evidence: 2 sources (completion report, code review report)
- Expires After Runs: 20
- Revert Triggers: primary_evidence_contradiction, architecture_domain_emergence

## Previous AUTO Decisions

### AUTO:ScriptExtraction.term:accept_as_aux
- Status: ACTIVE
- Chosen: ScriptExtraction accepted as aux term with 2 evidence sources
- Policy: evidence_threshold + semantic_distinctness
- Evidence:
  - actions/review-and-merge/scripts/review-and-fix.sh (implementation)
  - commit b2f8f31 (refactoring rationale)
- Rationale: Low merge similarity (max 0.52 < 0.78), distinct from TemplateFile and CompositeAction
- Expires After Runs: 20 (created Run 27, expires Run 47)
- Linked: TP-005
- Revert Triggers: primary_evidence_contradiction, merge_threshold_breach
