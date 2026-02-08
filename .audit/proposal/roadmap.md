# Improvement Roadmap

**Generated:** 2026-02-08
**Run ID:** 20260208-151100
**Status:** Draft

## Overview

This roadmap prioritizes improvements based on gap analysis, focusing on high-value, low-risk changes that bring the repository closer to its mission goals.

## Priority Matrix

```
High Impact + Low Risk    → Do First (P0)
High Impact + High Risk   → Plan Carefully (P1)
Low Impact + Low Risk     → Do When Convenient (P2)
Low Impact + High Risk    → Defer or Reject (P3)
```

## Phase 1: Critical Metrics & Visibility (Week 1-2)

**Goal:** Establish measurement for success criteria

### PR-002: Automated Acceptance Rate Tracking
- **Priority:** P0 (High Impact, Medium Risk)
- **Effort:** 2-3 hours
- **Impact:** Enables measurement of "AI提案の修正率向上" success criterion
- **Dependencies:** None
- **Action Items:**
  1. Create `.github/workflows/track-acceptance-rate.yml`
  2. Enhance `calculate_acceptance_rate.py` with history tracking
  3. Add `.audit/metrics/README.md`
  4. Test and enable weekly schedule

**Success Criteria:**
- Weekly workflow runs successfully
- Historical data is accumulated
- Trend visualization is available
- Organization can track AI quality over time

---

## Phase 2: Quality Foundation (Week 3-5)

**Goal:** Ensure actual (not perceived) test coverage

### PR-003: Shell Script Testing Framework
- **Priority:** P0 (High Impact, Medium Risk)
- **Effort:** 16-22 hours total
- **Impact:** True test coverage, bug detection in production code
- **Dependencies:** None (but learning curve for BATS)
- **Action Items:**
  1. Week 3: Setup BATS, create framework
  2. Week 4: Write tests for 2-3 core actions
  3. Week 5: Expand to all 6 core actions

**Success Criteria:**
- BATS tests run in CI
- Shell script coverage >= 70%
- All core actions have test suites
- Total coverage (Python + Shell) remains >= 80%

---

## Phase 3: Documentation Completeness (Week 6)

**Goal:** Ensure all actions have complete documentation

### PR-001: Release Notes README
- **Priority:** P2 (Low Impact, Low Risk)
- **Effort:** 30 minutes
- **Impact:** Documentation consistency
- **Dependencies:** None
- **Action Items:**
  1. Create `actions/release-notes-ai/README.md`
  2. Follow template structure
  3. Verify links

**Success Criteria:**
- All 6 core actions have README files
- Documentation completeness score = 100%

---

## Phase 4: Standardization & Best Practices (Week 7-8)

**Goal:** Ensure all actions follow GitHub Actions standards

### PR-004: Standardize action.yml for All Actions
- **Priority:** P1 (Medium Impact, Low Risk)
- **Effort:** 3-4 hours
- **Impact:** Reusability, Marketplace readiness
- **Dependencies:** None
- **Scope:** Create action.yml for 7 actions missing it

**Action Items:**
1. Audit each action without action.yml
2. Determine if action should be standalone or composite
3. Create action.yml with proper metadata
4. Deprecate or remove unused actions

**Success Criteria:**
- All actively used actions have action.yml
- Actions can be referenced as `uses: ./actions/name`

---

### PR-005: Path Validation Security Audit
- **Priority:** P0 (High Impact, Low Risk)
- **Effort:** 2-3 hours
- **Impact:** Security vulnerability prevention
- **Dependencies:** None
- **Scope:** Review all user-input paths in actions

**Action Items:**
1. List all actions that accept file paths
2. Review each for path traversal protection
3. Create unified path validation helper
4. Add tests for path validation

**Success Criteria:**
- All file paths are validated
- Path traversal tests exist
- Security checklist is created

---

## Phase 5: Operational Excellence (Week 9-10)

**Goal:** Automate tracking and monitoring

### PR-006: Adoption Tracking Automation
- **Priority:** P1 (High Impact, Medium Risk)
- **Effort:** 2-3 hours
- **Impact:** Measure "組織内の複数リポジトリで採用" success criterion
- **Dependencies:** GitHub API access
- **Action Items:**
  1. Create workflow for `scan_adoption.py`
  2. Run weekly
  3. Store results in `.audit/metrics/adoption.ndjson`
  4. Create dashboard

**Success Criteria:**
- Adoption numbers are tracked automatically
- Weekly reports show trend
- Organization has visibility into usage

---

### PR-007: Performance Monitoring
- **Priority:** P2 (Medium Impact, Low Risk)
- **Effort:** 3-4 hours
- **Impact:** Ensure performance constraints are met
- **Dependencies:** None
- **Action Items:**
  1. Add timing logs to critical actions
  2. Create workflow to analyze logs
  3. Alert on threshold violations

**Success Criteria:**
- Execution times are tracked
- Actions meeting 5-minute target are identified
- Slow actions are flagged for optimization

---

## Phase 6: Quality Tools & CI (Week 11-12)

**Goal:** Integrate quality gates into CI

### PR-008: Ruff Check in CI
- **Priority:** P2 (Medium Impact, Low Risk)
- **Effort:** 1 hour
- **Impact:** Ensure code quality standards
- **Dependencies:** None
- **Action Items:**
  1. Add Ruff check to `.github/workflows/lint.yml`
  2. Fail PR on Ruff errors
  3. Add auto-fix option

**Success Criteria:**
- Ruff runs on every PR
- 0 errors threshold is enforced
- Code quality is maintained

---

### PR-009: YAML Validation in CI
- **Priority:** P2 (Low Impact, Low Risk)
- **Effort:** 1 hour
- **Impact:** Catch workflow syntax errors early
- **Dependencies:** None
- **Action Items:**
  1. Add yamllint to CI
  2. Validate all action.yml files
  3. Validate example workflows

**Success Criteria:**
- All YAML files are validated
- Syntax errors are caught in PR
- QA-003 is satisfied

---

## Execution Order Summary

1. **Quick Wins (Week 1):** PR-001, PR-008, PR-009
2. **Critical Foundation (Week 2-6):** PR-002, PR-003
3. **Security & Standards (Week 7-8):** PR-004, PR-005
4. **Operations (Week 9-12):** PR-006, PR-007

---

## Risk Mitigation

### High Risk Items

**PR-003 (Shell Testing):**
- **Risk:** Team unfamiliar with BATS
- **Mitigation:** Provide training and templates
- **Fallback:** Start with manual test checklist

**PR-006 (Adoption Tracking):**
- **Risk:** GitHub API rate limits
- **Mitigation:** Cache results, use pagination
- **Fallback:** Manual weekly scan

### Dependencies

- PR-002 depends on working `calculate_acceptance_rate.py`
- PR-006 depends on organization access
- All PRs depend on maintaining existing functionality

---

## Success Metrics

By end of Week 12, we should have:

1. **Measurement:**
   - Acceptance rate is tracked weekly
   - Adoption numbers are known
   - Shell script coverage >= 70%
   - Total coverage (Python + Shell) >= 80%

2. **Quality:**
   - All actions have action.yml
   - All paths are validated
   - Ruff checks pass in CI
   - YAML validation passes in CI

3. **Documentation:**
   - All core actions have README
   - All actions have examples
   - All actions have instructions

4. **Operations:**
   - Weekly workflows run automatically
   - Performance is monitored
   - Metrics are visible to organization

---

## Rollback Plan

Each PR includes rollback instructions:
- PR-001: Delete README
- PR-002: Disable workflow, delete metrics
- PR-003: Remove BATS tests, disable workflow
- PR-004: Delete created action.yml files
- PR-005: Revert path validation changes
- PR-006: Disable workflow
- PR-007: Remove performance logging
- PR-008: Remove Ruff check from CI
- PR-009: Remove yamllint from CI

---

## Next Steps

1. **Review this roadmap** with team
2. **Prioritize based on capacity** (can run multiple phases in parallel)
3. **Create tracking issues** in GitHub for each PR
4. **Assign owners** to each PR
5. **Start execution** with Phase 1

---

## Unknowns to Resolve

1. **U-001 (Actual Adoption Count):** Will be resolved by PR-006
2. **U-002 (Claude CLI Version):** Research and document
3. **U-003 (Execution Time):** Will be measured by PR-007
4. **U-004 (Acceptance Rate):** Will be tracked by PR-002
5. **U-005 (Shell Coverage):** Will be measured by PR-003

---

## Assumptions to Validate

1. **ASM-002 (80% Coverage):** Validate after PR-003
2. **ASM-003 (Organization Deployment):** Validate after PR-006
3. **I-003 (Coverage Illusion):** Confirm/disprove after PR-003
4. **I-004 (Adoption Not Tracked):** Validate after PR-006
