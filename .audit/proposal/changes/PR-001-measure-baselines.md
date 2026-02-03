# PR-001: Establish Quality Baselines

**Priority**: 1 (Critical for Phase 3 completion)
**Status**: Proposed
**Estimated Effort**: Low (1-2 hours)

## Problem

The repository has quality standards defined but no baseline measurements:
- Test coverage target: >= 70% (pytest.ini:22) → Current: Unknown
- AI review acceptance rate target: >= 70% (README.md:127) → Current: Unknown

Without baseline measurements, we cannot:
1. Verify if current quality standards are being met
2. Track progress over time
3. Demonstrate value to stakeholders
4. Complete Phase 3 (Stabilization & Adoption)

## Proposed Solution

### Action 1: Run Test Coverage Analysis
Execute pytest with coverage and save baseline:

```bash
cd /home/jinno/github-actions-actions
pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=json:coverage-baseline.json
```

Create `.audit/metrics/baselines/coverage-baseline-2026-02-04.json` with results.

### Action 2: Establish Acceptance Rate Baseline
Execute acceptance rate calculation:

```bash
cd /home/jinno/github-actions-actions
python scripts/calculate_acceptance_rate.py --time-period 30d --output json --output-file .audit/metrics/baselines/acceptance-baseline-2026-02-04.json
```

If no data exists yet, document this as "initial state - awaiting production adoption".

### Action 3: Document Baseline in README
Add a "Quality Metrics" section to README.md:

```markdown
## 📊 Current Quality Metrics

| Metric | Target | Current | Last Updated |
|--------|--------|---------|--------------|
| Test Coverage | >= 70% | [XX]% | YYYY-MM-DD |
| AI Review Acceptance Rate | >= 70% | [XX]% | YYYY-MM-DD |

*Baseline established 2026-02-04*
```

### Action 4: Create Automated Baseline Tracking
Add to `.github/workflows/` a workflow that runs weekly to update metrics:

```yaml
name: Update Quality Metrics
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:
```

## Benefits

1. **Visibility**: Stakeholders can see current quality state
2. **Progress Tracking**: Measure improvement over time
3. **Goal Validation**: Confirm if targets are being met
4. **Phase 3 Completion**: Satisfy "組織内プロジェクトへの導入とフィードバック収集" requirement

## Risks

- **Risk**: Initial coverage may be below 70%
  - **Mitigation**: Document current state as baseline, create improvement plan
- **Risk**: No acceptance rate data if not yet in production
  - **Mitigation**: Document as "awaiting production adoption", set up tracking for future

## Verification

**Success Criteria**:
- [ ] Coverage baseline JSON exists in `.audit/metrics/baselines/`
- [ ] Acceptance rate baseline exists or "no data yet" documented
- [ ] README updated with current metrics table
- [ ] Automated workflow created for weekly updates

**Validation Method**:
```bash
# Verify baseline files exist
ls -la .audit/metrics/baselines/

# Verify README includes metrics section
grep -A 10 "Quality Metrics" README.md

# Verify workflow exists
ls -la .github/workflows/update-quality-metrics.yml
```

## Rollback

If automated metrics cause issues:
```bash
# Remove automated workflow
rm .github/workflows/update-quality-metrics.yml

# Revert README changes
git checkout HEAD -- README.md
```

Baseline data files remain as valuable historical data.

## Alternatives Considered

1. **Skip baseline measurement**
   - **Rejected**: Cannot improve what you don't measure
2. **Manual monthly tracking**
   - **Rejected**: Automation reduces friction and increases reliability
3. **Use external monitoring service**
   - **Rejected**: Adds dependency, GitHub-native solution sufficient

## Related Gaps

- Closes: GAP-001 (Actual test coverage unknown)
- Closes: GAP-002 (AI review acceptance rate unknown)

## Related Assumptions

- Validates: ASM-002 (coverage target)
- Validates: ASM-003 (acceptance rate target)
