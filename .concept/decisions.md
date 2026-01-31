# Active AUTO Decisions (cache) — safe to delete

_Last regenerated: 2026-01-31T23:59:00Z (Run 48)_

## Summary
- Active AUTO Decisions: 0 (all expired)
- No ambiguities requiring AUTO decisions
- No conflicts requiring workarounds

## Expiration Summary (Run 48)

### EXPIRED: ScriptExtraction AUTO Decision
- Status: EXPIRED (was ACTIVE from Run 27-47)
- Was: ScriptExtraction accepted as aux term with 2 evidence sources
- Expired at Run 47 after 20 runs (TTL reached)
- Rationale: AUTO decisions have default 20-run TTL. No revert triggers fired.
- Note: ScriptExtraction term remains in ontology as `layer: aux, status: stable`

### EXPIRED: Queue Rejection AUTO Decisions (TP-006, TP-007, TP-008)
- Status: EXPIRED (were ACTIVE from Run 26-46)
- Were: Rejected SecurityVulnerability, CodeDuplication, SharedLibraryInfrastructure
- Expired at Run 46 after 20 runs (TTL reached)
- Rationale: AUTO decisions have default 20-run TTL. No revert triggers fired.
- Note: Rejected terms remain in term_queue.yml with `decision: rejected`

## System Health
- Ontology: 11 terms (5 core, 5 domain, 1 aux)
- Budget utilization: 13.75% (well under 80 limit)
- Draft ratio: 0.0% (well under 30% limit)
- Queue pending: 0 (well under 30 limit)
- No open ambiguities or conflicts
- All AUTO decisions expired cleanly
