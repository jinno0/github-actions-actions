# Active AUTO Decisions (cache) — safe to delete

_Last regenerated: 2026-02-01T04:16:31Z (Run 49)_

## Summary
- Active AUTO Decisions: 0 (all expired)
- No ambiguities requiring AUTO decisions
- No conflicts requiring workarounds

## Recent Security Validation (Run 49)

### Verified: Security Invariants Compliance
- Status: VERIFIED (commit 75571a9)
- Invariants validated: INV-012, INV-013, INV-014
- Security fixes applied:
  - Shell injection prevention (replaced unsafe sed with envsubst)
  - Path traversal validation (added to all template paths)
  - Git race condition fixes (force-with-lease, backoff)
  - Input sanitization enforcement
- Impact: All 45 tests pass, no regressions

## Expiration History

### EXPIRED: ScriptExtraction AUTO Decision
- Status: EXPIRED (was ACTIVE from Run 27-47)
- Was: ScriptExtraction accepted as aux term with 2 evidence sources
- Expired at Run 47 after 20 runs (TTL reached)
- Note: ScriptExtraction term remains in ontology as `layer: aux, status: stable`

### EXPIRED: Queue Rejection AUTO Decisions (TP-006, TP-007, TP-008)
- Status: EXPIRED (were ACTIVE from Run 26-46)
- Were: Rejected SecurityVulnerability, CodeDuplication, SharedLibraryInfrastructure
- Expired at Run 46 after 20 runs (TTL reached)
- Note: Rejected terms remain in term_queue.yml with `decision: rejected`

## System Health
- Ontology: 11 terms (5 core, 5 domain, 1 aux)
- Budget utilization: 13.75% (well under 80 limit)
- Draft ratio: 0.0% (well under 30% limit)
- Queue pending: 0 (well under 30 limit)
- No open ambiguities or conflicts
- All security invariants verified
