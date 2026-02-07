# Improvement Roadmap

**Generated**: 2026-02-08  
**Based on Audit**: 2026-02-08  
**Priority**: Critical gaps first

---

## Immediate Actions (Week 1-2)

### 1. Resolve ISS-001: Onboard Pilot Projects
**Priority**: CRITICAL  
**Effort**: 1-2 weeks  
**Owner**: Repository Maintainers + Org Leadership

**Steps**:
1. Identify 2-3 candidate repositories for pilot adoption
2. Create pilot onboarding checklist:
   - Verify self-hosted runner access
   - Install Claude Code CLI (document version)
   - Configure GitHub secrets
   - Create first test workflow
3. Set up weekly feedback collection
4. Document success criteria for pilot phase

**Success Criteria**: At least 1 pilot project onboarded by 2026-02-22

---

### 2. Resolve ISS-002: Document Claude CLI Version
**Priority**: CRITICAL  
**Effort**: 2-3 days  
**Owner**: Repository Maintainers

**Steps**:
1. Test which Claude CLI versions work with all 13 actions
2. Document minimum supported version in README.md
3. Add CLI version to `.github/workflows/*.yml` examples
4. Document CLI upgrade testing process
5. Pin CLI version in pilot project workflows

**Success Criteria**: README updated with CLI version requirements by 2026-02-15

---

### 3. Resolve ISS-003: Inventory Self-Hosted Runners
**Priority**: CRITICAL  
**Effort**: 3-5 days  
**Owner**: Infrastructure Team + DevOps

**Steps**:
1. Audit organization's self-hosted runners
2. Verify Claude CLI installation on each runner
3. Document runner capacity and scaling strategy
4. Create runner verification checklist for pilot projects
5. Identify if additional runners are needed

**Success Criteria**: Runner inventory documented by 2026-02-22

---

## Short-Term Actions (Week 3-4)

### 4. Resolve ISS-004: Enable Metrics Collection
**Priority**: HIGH  
**Effort**: 1 week  
**Owner**: Pilot Project Teams

**Steps**:
1. Ensure metrics collection enabled in pilot workflows
2. Document metrics troubleshooting guide
3. Set up weekly metrics report (automated)
4. Define action plan if acceptance rate < 70%

**Success Criteria**: Metrics collection active in all pilots by 2026-03-01

---

### 5. Resolve ISS-005: Execute Dry-Run Verification
**Priority**: HIGH  
**Effort**: 2-3 days  
**Owner**: Repository Maintainers

**Steps**:
1. Execute `.github/workflows/test-with-dry-run.yml`
2. Verify all 13 actions pass dry-run validation
3. Document any failures and remediation
4. Add dry-run results to audit checklist
5. Consider making dry-run a blocking CI check

**Success Criteria**: All actions pass dry-run by 2026-03-01

---

### 6. Resolve ISS-006: Add YAML Linting
**Priority**: HIGH  
**Effort**: 1-2 days  
**Owner**: Repository Maintainers

**Steps**:
1. Install yamllint in development environment
2. Run `yamllint actions/*/action.yml examples/*.yml`
3. Fix any syntax errors found
4. Add yamllint to `.github/workflows/lint.yml`
5. Document YAML coding standards

**Success Criteria**: YAML linting in CI by 2026-03-01

---

## Long-Term Actions (Month 2-3)

### 7. Improve Test Coverage (ISS-007)
**Priority**: MEDIUM  
**Effort**: 1-2 weeks  
**Owner**: Development Team

**Steps**:
1. Review 65 uncovered lines in coverage report
2. Add tests for error handling paths
3. Assess if uncovered lines are defensive code
4. Target 95%+ coverage for next quarter

**Success Criteria**: 95% coverage achieved by 2026-04-01

---

### 8. Verify AGENTS.md Compliance (ISS-008)
**Priority**: MEDIUM  
**Effort**: 3-5 days  
**Owner**: Repository Maintainers

**Steps**:
1. Read AGENTS.md development guidelines
2. Verify all 13 actions comply with structure requirements
3. Document any structural inconsistencies
4. Consider adding automated compliance check
5. Update AGENTS.md if needed

**Success Criteria**: All actions verified compliant by 2026-03-15

---

## Success Metrics

### Phase 3 Completion Criteria
- [ ] At least 3 pilot projects actively using actions
- [ ] Acceptance rate >= 70% (if sufficient data collected)
- [ ] All critical gaps (ISS-001, ISS-002, ISS-003) resolved
- [ ] Dry-run validation passing for all actions
- [ ] YAML linting integrated in CI
- [ ] Self-hosted runner capacity documented

### Quality Metrics
- Test coverage remains >= 90%
- Zero YAML syntax errors in production
- Zero dry-run failures
- Metrics collection reliability >= 95%

---

## Risk Mitigation

### High-Risk Items
1. **Pilot adoption stalls**: Mitigated by executive sponsorship and clear onboarding checklist
2. **CLI compatibility issues**: Mitigated by version testing and documentation
3. **Runner capacity insufficient**: Mitigated by early infrastructure audit

### Rollback Plans
Each action includes rollback steps:
- Pilot projects can disable actions if issues arise
- CLI versions can be pinned and rolled back
- YAML changes can be reverted via git

---

## Timeline Summary

| Week | Focus | Owner | Deliverable |
|------|-------|-------|-------------|
| 1-2 | Pilot onboarding | Maintainers + Leadership | 1+ pilot projects active |
| 1-2 | CLI versioning | Maintainers | CLI version documented |
| 1-2 | Runner inventory | Infrastructure | Runner capacity documented |
| 3-4 | Metrics enablement | Pilot teams | Metrics collecting |
| 3-4 | Dry-run validation | Maintainers | All actions pass |
| 3-4 | YAML linting | Maintainers | Linting in CI |
| 5-8 | Coverage improvement | Dev team | 95% coverage |
| 5-8 | AGENTS.md compliance | Maintainers | All verified |

---

**Next Review**: 2026-03-01 (after initial pilot onboarding)  
**Owner**: Repository Maintainers  
**Stakeholders**: Organization Leadership, Pilot Project Teams, Infrastructure Team
