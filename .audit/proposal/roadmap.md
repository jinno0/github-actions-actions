# Improvement Roadmap
# Generated: 2026-02-01T00:00:00Z
# Based on Phase 1 execution feedback and remaining gap analysis

version: "2.0"
run_id: "2026-02-01T00:00:00Z"

## Phase 1 Complete ✅

Phase 1 improvements were successfully executed:
- ✅ PR-001: Documentation coverage 46% → 100%
- ✅ PR-003: Core function verification 83% → 100%
- ✅ All assumptions confirmed with evidence
- ✅ Compliance: 85% → 95% (+10 percentage points)

## Phase 2: Quality & Verification Enhancement

### Priority 1: Enhanced Dry-Run Validation (ISS-003)
**Status**: Ready to implement
**Effort**: 2-4 hours
**Impact**: High - prevents production issues

#### PR-002: Enhance Dry-Run Validation
**Objective**: Verify actions actually execute (not just structure checks)

**Changes**:
1. Create `.github/workflows/test-with-dry-run.yml`
2. For each AI action (9 actions with templates/):
   - Execute action with `dry_run: true`
   - Capture Claude CLI output
   - Verify exit code = 0
   - Check for expected output patterns

**Implementation Steps**:
```yaml
# .github/workflows/test-with-dry-run.yml
name: Test Actions with Dry Run
on:
  pull_request:
  push:
    branches: [main]

jobs:
  dry-run-test:
    runs-on: self-hosted
    strategy:
      matrix:
        action: [review-and-merge, spec-to-code, action-fixer, auto-refactor, auto-document, release-notes-ai, auto-rebase]
    steps:
      - uses: actions/checkout@v3
      - name: Test ${{ matrix.action }} with dry-run
        uses: ./.actions/${{ matrix.action }}
        with:
          dry-run: true
          test-mode: true
```

**Success Criteria**:
- All 9 AI actions pass dry-run validation
- CI fails if any action returns non-zero exit code
- Action execution time logged

**Rollback**:
- Delete `.github/workflows/test-with-dry-run.yml`
- No code changes required

---

### Priority 2: Enable Test Coverage Measurement (ISS-004)
**Status**: Ready to implement
**Effort**: 1 hour
**Impact**: Medium - enables quality tracking
**Updated**: 2026-02-01 - pytest-cov availability confirmed (J-002)

#### PR-005: Enable Coverage Reporting

**Objective**: Measure and improve test coverage for Python helper scripts

**Changes**:
1. Uncomment pytest-cov in `pytest.ini`
2. Set coverage threshold (initial: 60%, target: 80%)
3. Add coverage report to CI

**Implementation**:
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts =
    --cov=.claude/skills
    --cov=tests
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=60
```

**CI Integration**:
```yaml
# .github/workflows/test-all-actions.yml (add step)
- name: Run tests with coverage
  run: |
    pip install pytest-cov
    pytest --cov=.claude/skills --cov-report=xml

- name: Upload coverage to artifacts
  uses: actions/upload-artifact@v3
  with:
    name: coverage-report
    path: htmlcov/
```

**Success Criteria**:
- Coverage report generated on each run
- CI fails if coverage < 60%
- HTML coverage report available as artifact

**Rollback**:
- Comment out `--cov` lines in pytest.ini
- Remove coverage upload step from CI

---

### Priority 3: Adoption Metrics Investigation (ISS-006)
**Status**: Requires manual investigation
**Effort**: 4-8 hours
**Impact**: Low-Medium - strategic importance

#### Investigation: Measure Action Usage Across Organization

**Objective**: Determine how many repositories are using these actions

**Approach Options**:

**Option A: Manual Search (Immediate)**
```bash
# Search for action references in org repos
gh repo list --limit 1000 --json name | \
  jq -r '.[].name' | \
  while read repo; do
    gh api repos/:owner/$repo/contents/.github/workflows | \
      jq -r '.[].name' | \
      xargs -I{} gh api repos/:owner/$repo/contents/.github/workflows/{} | \
      grep -h "actions/org-name/github-actions-actions" | \
      wc -l
  done
```

**Option B: Automated Tracking (Long-term)**
- Add usage tracking endpoint (optional opt-in)
- Log action invocations to central metrics
- Create dashboard for adoption visibility

**Success Criteria**:
- Baseline number of repositories using actions
- List of top 5 most-used actions
- Recommendation on whether to invest in automated tracking

**Deliverable**: `.audit/analysis/adoption_metrics.yml`

---

## Phase 3: Infrastructure Improvements (Future)

### Potential Improvements
- Linting configuration (ruff, yamllint)
- Pre-commit hooks
- Automated changelog generation
- Integration tests with test repositories
- Performance benchmarking

### Dependencies
- Phase 2 must complete successfully
- Adoption metrics should inform prioritization
- Community feedback should guide direction

---

## Execution Order

```
Phase 2a (Immediate - Week 1):
  ├─ PR-002: Enhanced Dry-Run Validation (2-4 hours)
  └─ PR-005: Enable Coverage Reporting (1 hour)

Phase 2b (Short-term - Week 2-4):
  └─ Adoption Metrics Investigation (4-8 hours)

Phase 3 (Future - TBD):
  └─ Based on Phase 2 results and feedback
```

---

## Risk Assessment

| PR | Risk | Mitigation |
|----|------|------------|
| PR-002 | Dry-run may expose hidden bugs | Low risk - finding bugs is the goal |
| PR-004 | Existing tests may have low coverage | Set initial threshold at 60% |
| Metrics | Privacy concerns about usage tracking | Opt-in only, no sensitive data |

---

## Success Metrics

### Phase 2 Success Criteria
- ✅ All 9 AI actions pass dry-run validation
- ✅ Coverage baseline established (>60%)
- ✅ Adoption baseline measured
- ✅ Overall compliance ≥ 97%

### Long-term Success Criteria
- 5+ repositories using actions in production
- 0 critical bugs in released actions
- Test coverage ≥ 80%
- Community contributions increase

---

## Process Improvements (ISS-008)

### Lesson Learned from PR-003
**Issue**: Verification script had bug (yaml.safe_load with Path object)
**Root Cause**: Audit phase created verification script but didn't execute it
**Fix Applied**: PR-003 fixed the bug
**Process Change**: Audit workflow now includes actual execution of verification scripts

### Updated Audit Protocol
```yaml
# Future audit phases will:
1. Create verification scripts
2. Execute verification scripts ✅ NEW
3. Fix any bugs discovered ✅ NEW
4. Document results
5. Mark task complete
```

---

## Next Steps

1. **Immediate**: Execute PR-002 (Enhanced Dry-Run Validation)
2. **Week 1**: Execute PR-005 (Enable Coverage Reporting)
3. **Week 2**: Conduct adoption metrics investigation
4. **Week 4**: Review Phase 2 results and plan Phase 3

---

**End of Roadmap**
