# Roadmap for github-actions-actions Improvements

## Overview
This roadmap prioritizes improvements based on gap analysis conducted on 2026-01-31.

## Priority Framework
- **Critical**: Blocks project success or adoption
- **High**: Significant impact on quality or maintainability
- **Medium**: Important but not blocking
- **Low**: Nice to have or clarifications

---

## Phase 1: Quick Wins (Week 1)
*Total Effort: ~3 hours*

### 1.1 Update README.md (PR-001)
**Priority**: Critical  
**Effort**: 15 minutes  
**Impact**: High

Document all 13 actions in README.md with consistent formatting and categorization.

**Why First**: 
- Critical visibility issue
- Zero risk (documentation only)
- Immediate impact on discoverability
- Unblocks adoption

**Steps**:
1. Read all 13 instruction.md files
2. Categorize actions by purpose
3. Update README.md table
4. Verify all links
5. Commit and push

**Success**: All 13 actions visible and discoverable from README

---

## Phase 2: Quality Foundation (Week 1-2)
*Total Effort: ~3 hours*

### 2.1 Core Function Verification (PR-003)
**Priority**: High  
**Effort**: 1 hour  
**Impact**: High

Create automated structural verification tests for 6 core functions.

**Why Second**:
- Required by audit instruction
- Proves repository purpose
- Enables regression detection
- Fast to implement

**Steps**:
1. Create verify_core_functions.py
2. Implement structural checks for each core function
3. Test locally
4. Add to CI pipeline
5. Generate baseline report

**Success**: All 6 core functions pass structural verification

### 2.2 Enable Test Coverage (PR-004)
**Priority**: High  
**Effort**: 30 minutes  
**Impact**: Medium

Enable pytest coverage measurement for Python helper scripts.

**Why Now**:
- Addresses ISS-004 (quality measurement gap)
- Fast to enable (uncomment existing config)
- Provides baseline metrics

**Steps**:
1. Uncomment pytest-cov in pytest.ini
2. Run pytest with --cov
3. Document baseline coverage
4. Set minimum threshold (e.g., 60%)

**Success**: Coverage reports generated, baseline established

### 2.3 Enhance Dry Run Validation (PR-002)
**Priority**: High  
**Effort**: 2 hours  
**Impact**: High

Enhance test-all-actions.yml to verify execution flow and template substitution.

**Why Now**:
- Addresses ISS-003 (verification gap)
- Prevents broken actions in production
- Builds on existing CI

**Steps**:
1. Add functional validation step
2. Implement template substitution test
3. Add Claude CLI availability check
4. Test on all 13 actions
5. Update CI workflow

**Success**: All actions pass functional validation in CI

---

## Phase 3: Maintainability (Week 2-3)
*Total Effort: ~4 hours*

### 3.1 Review Actions Without Templates
**Priority**: Medium  
**Effort**: 2 hours  
**Impact**: Medium

Investigate 6 actions without templates/ and determine if they need prompts externalized.

**Why Later**:
- Requires investigation per action
- May be intentional (utility actions)
- Not blocking (structure compliant)

**Steps**:
1. Review action.yml for each of 6 actions
2. Determine if prompts are hardcoded
3. If yes, extract to templates/
4. If no, document why templates aren't needed
5. Update AGENTS.md if needed

**Success**: All actions either have templates/ or documented rationale

### 3.2 Add Linting Configuration
**Priority**: Medium  
**Effort**: 1 hour  
**Impact**: Medium

Add Python linting (ruff/flake8) and YAML linting (yamllint) configuration.

**Why Now**:
- Improves code quality
- Catches issues early
- Standard practice

**Steps**:
1. Choose linter (ruff recommended)
2. Add configuration file
3. Add pre-commit hook
4. Document in AGENTS.md

**Success**: Linting runs in CI and pre-commit

### 3.3 Document Testing Strategy
**Priority**: Medium  
**Effort**: 1 hour  
**Impact**: Medium

Create TESTING.md documenting testing approach, coverage goals, and how to add tests.

**Why Now**:
- Guides future development
- Sets quality expectations
- Supports onboarding

**Steps**:
1. Document current test infrastructure
2. Define coverage targets
3. Explain how to test actions
4. Add troubleshooting section

**Success**: Clear testing strategy documented

---

## Phase 4: Strategic Improvements (Month 2)
*Total Effort: ~8 hours*

### 4.1 Adoption Metrics
**Priority**: Low-Medium  
**Effort**: 4 hours  
**Impact**: Medium

Implement system to track action usage across organization.

**Why Later**:
- Requires cross-repo infrastructure
- Strategic importance but not urgent
- Can be manual initially

**Approach**:
1. Manual: Survey teams using actions
2. Automated: Add usage reporting to actions
3. Dashboard: Create metrics dashboard

**Success**: Measurable adoption metrics

### 4.2 Action Examples Repository
**Priority**: Low  
**Effort**: 4 hours  
**Impact**: Medium

Create separate repository with example projects using each action.

**Why Later**:
- Nice-to-have for adoption
- Not required for current users
- Can be community contribution

**Approach**:
1. Create github-actions-actions-examples repo
2. Add example project for each action
3. Document setup and expected output
4. Link from main README

**Success**: Users have working examples to reference

---

## Phase 5: Continuous Improvement (Ongoing)

### 5.1 Regular Audits
- Schedule quarterly genesis audits
- Track progress on gaps
- Update intent.yml as project matures

### 5.2 Feedback Collection
- Add feedback mechanism to actions
- Survey users quarterly
- Track adoption and satisfaction

### 5.3 Documentation Maintenance
- Keep README.md synchronized with actions
- Update instructions/ based on user feedback
- Maintain AGENTS.md as source of truth

---

## Dependencies

```
Phase 1 (Quick Wins)
    ↓
Phase 2 (Quality Foundation) ← Requires Phase 1 complete
    ↓
Phase 3 (Maintainability) ← Requires Phase 2 complete
    ↓
Phase 4 (Strategic) ← Requires Phase 3 complete
    ↓
Phase 5 (Continuous) ← Ongoing
```

---

## Resource Requirements

### Time
- Week 1: ~3 hours (Phase 1 + start Phase 2)
- Week 2-3: ~4 hours (finish Phase 2 + Phase 3)
- Month 2: ~8 hours (Phase 4)
- Ongoing: ~1 hour/quarter (Phase 5)

### Skills
- GitHub Actions YAML
- Python testing (pytest)
- Documentation writing
- No special skills required for Phases 1-2

### Tools
- All tools already available (pytest, Python, YAML validators)
- No additional infrastructure needed for Phases 1-3

---

## Risk Mitigation

### Risk: Time Constraints
**Mitigation**: Phase 1 takes only 15 minutes, provides immediate value

### Risk: Breaking Changes
**Mitigation**: All changes are additive (documentation, tests) or backwards-compatible

### Risk: Low Adoption
**Mitigation**: Phase 1 directly addresses discoverability, unblocks adoption

---

## Success Criteria

### Phase 1 Success
- [ ] All 13 actions documented in README
- [ ] Links work and descriptions are accurate

### Phase 2 Success
- [ ] All 6 core functions verified
- [ ] Coverage reporting enabled
- [ ] CI includes functional validation

### Phase 3 Success
- [ ] All actions have templates/ or documented rationale
- [ ] Linting configured and running
- [ ] Testing strategy documented

### Phase 4 Success
- [ ] Adoption metrics collected
- [ ] Examples repository created

### Overall Success
- README.md coverage: 100% (up from 46%)
- Structural verification: 100% of core functions
- Test coverage: Measured and improving
- CI: Includes functional tests
- Adoption: Measurable and growing

---

## Next Actions

1. **Immediate** (Today): Execute PR-001 (update README)
2. **This Week**: Execute PR-003 and PR-004 (verification + coverage)
3. **Next Week**: Execute PR-002 (enhance CI validation)
4. **Following Weeks**: Phase 3 improvements

---

*Last Updated: 2026-01-31*
*Next Review: After Phase 1 completion*
