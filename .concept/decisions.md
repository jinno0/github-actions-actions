# Active AUTO Decisions (cache) — safe to delete

## AUTO:CLIAvailabilityCheck.rate:post_audit_cleanup
- Status: ACTIVE
- Chosen: Audit reports removed (commit cc1e88e). Current CLI check implementation rate is unknown. SECURITY_CHECKLIST.md requires 100% (13/13 actions). Target remains 100% compliance per security requirements.
- Policy: recent_authoritative_source + safety
- Expires After Runs: 20
- Linked: AMB-CLI-001 / ASM-CLI-001
- Revert Triggers: primary_evidence_contradiction, security_risk
- Evidence: SECURITY_CHECKLIST.md#L9-L31, commit cc1e88e

## AUTO:FunctionalTesting.phasing:post_audit_cleanup
- Status: ACTIVE
- Chosen: Audit reports removed (commit cc1e88e). Phase 2 (Integration Testing) was previously confirmed as COMPLETED with 100% coverage (13/13 actions) per commit a5a4475. Phase 2b (Runtime Testing with act) remains PROPOSED.
- Policy: authoritative_git_evidence + roadmap_update
- Expires After Runs: 20
- Linked: ASM-FUNC-TEST-002
- Revert Triggers: primary_evidence_contradiction, security_risk
- Evidence: commit a5a4475

## AUTO:CLAUDE-CLI.installation:npm_global
- Status: ACTIVE
- Chosen: Claude Code CLI must be installed via npm globally on self-hosted runners
- Policy: industry_convention + safety
- Expires After Runs: 20
- Linked: ASM-CLAUDE-001
- Revert Triggers: primary_evidence_contradiction, security_risk
- Evidence: ACTIONS.md#L241-L244

## AUTO:LGTM.threshold:configurable
- Status: ACTIVE
- Chosen: LGTM threshold is configurable via action input parameter (default 7-10 scale)
- Policy: flexibility + safety
- Expires After Runs: 20
- Linked: ASM-LGTM-001
- Revert Triggers: primary_evidence_contradiction, security_risk
- Evidence: ACTIONS.md#L38-L40

## AUTO:GitHubToken.permissions:required_scopes
- Status: ACTIVE
- Chosen: GitHub token must have contents:write, pull-requests:write, and issues:write for actions to function
- Policy: security + safety
- Expires After Runs: 20
- Linked: ASM-TOKEN-001, INV-003
- Revert Triggers: primary_evidence_contradiction, security_risk
- Evidence: ACTIONS.md#L246-L250

## AUTO:VersionManagement.policy:stability
- Status: ACTIVE
- Chosen: Version management requires @main for development/testing, @v1 for production, NEVER @main in production
- Policy: stability + safety
- Expires After Runs: 20
- Linked: ASM-VERSION-001
- Revert Triggers: primary_evidence_contradiction, stability_risk
- Evidence: pilot-workflow-template.yml#L11-L14

## AUTO:SuccessMetric.QA-001:hierarchical
- Status: ACTIVE
- Chosen: QA-001 (Acceptance Rate >= 80%) is a specific quality invariant that implements the broader SuccessMetric concept for MS-002
- Policy: hierarchy + clarity
- Expires After Runs: 20
- Linked: ASM-INV-010, AMB-SUCCESS-001, INV-010
- Revert Triggers: primary_evidence_contradiction, new_quality_gates_defined
- Evidence: metrics/README.md#L15-L20, charter.yml#L6-L15

## AUTO:Telemetry.privacy:compliance
- Status: ACTIVE
- Chosen: Telemetry system respects DISABLE_TELEMETRY setting and follows GDPR/CCPA compliance requirements with SHA-256 anonymization and opt-out mechanism
- Policy: privacy + compliance + safety
- Expires After Runs: 20
- Linked: ASM-TELE-001
- Revert Triggers: primary_evidence_contradiction, privacy_risk, legal_noncompliance
- Evidence: docs/telemetry.md#L129-L139

_last_updated: 2026-02-06T12:55:40Z_
