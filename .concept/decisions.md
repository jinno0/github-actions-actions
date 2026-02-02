# Active AUTO Decisions (cache) — safe to delete

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

## AUTO:FunctionalTesting.phasing:future
- Status: ACTIVE
- Chosen: Functional testing phases (Phase 2 Integration Testing, Phase 3 End-to-End Testing) are planned but not yet implemented
- Policy: roadmap_alignment + scope_control
- Expires After Runs: 20
- Linked: ASM-FUNC-TEST-001, MS-001
- Revert Triggers: primary_evidence_contradiction, implementation_complete
- Evidence: TESTING.md#L158-L184
