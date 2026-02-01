# PR-005: Enable Test Coverage Reporting

## Summary
pytest-cov is installed but not enabled in pytest.ini. This PR enables coverage reporting to establish quality metrics for the repository.

## Problem
- Test coverage percentage is unknown (ISS-004)
- Cannot measure code quality of helper scripts
- No baseline to track improvement over time
- Quality is not measurable (violates intent.yml quality_attributes)

## Current State
```ini
# pytest.ini:29
# Coverage options (if pytest-cov is installed)
# addopts = --cov=actions --cov-report=html --cov-report=term
```

## Verification (J-002)
```bash
$ python3 -c "import pytest_cov"
# Result: pytest-cov is installed
```

## Proposed Changes

### 1. Enable Coverage in pytest.ini

```diff
 # Coverage options (if pytest-cov is installed)
-# addopts = --cov=actions --cov-report=html --cov-report=term
+addopts = --cov=. --cov-report=html --cov-report=term-missing --cov-report=json
+           --cov-fail-under=70  # Initial threshold, adjust based on baseline
```

**Changes:**
- `--cov=.` instead of `--cov=actions`: Cover all Python code in repository
- `--cov-report=term-missing`: Show missing lines in terminal output
- `--cov-report=json`: Generate coverage.json for CI integration
- `--cov-fail-under=70`: Set initial 70% threshold (adjustable)

### 2. Update .gitignore (if needed)

```diff
+# Coverage reports
+htmlcov/
+.coverage
+coverage.json
```

### 3. Add Coverage Badge to README.md (Optional)

```markdown
![Test Coverage](https://img.shields.io/badge/coverage-?color=brightgreen)
```

Note: Update badge after baseline measurement.

### 4. Document Coverage Threshold in AGENTS.md

Add section to AGENTS.md:

```markdown
## Test Coverage

Target coverage: 70% (configurable in pytest.ini)

To measure coverage:
```bash
pytest --cov
```

To view detailed HTML report:
```bash
open htmlcov/index.html
```
```

## Benefits
1. **Quality Visibility**: See which code is tested vs untested
2. **Baseline Measurement**: Establish current coverage percentage
3. **Trend Tracking**: Monitor improvement over time
4. **CI Integration**: Fail PRs if coverage drops significantly
5. **Code Review**: Identify risky changes in untested code

## Alternatives Considered
1. **Use different coverage tool (e.g., coverage.py directly)**
   - Rejected: pytest-cov already installed and integrated
   - Reason: No benefit to switching tools

2. **Set higher threshold (e.g., 80-90%)**
   - Rejected: Don't know baseline yet
   - Reason: Set realistic threshold after measurement

3. **Only cover actions/ directory**
   - Rejected: Helper scripts also matter
   - Reason: All Python code should be quality-assured

## Risks
- **Low**: Coverage may be lower than expected
- **Mitigation**: `--cov-fail-under=70` is reasonable, adjustable after baseline

## Testing
1. Run `pytest --cov` to measure baseline coverage
2. Review htmlcov/index.html for detailed coverage report
3. Adjust threshold based on baseline
4. Verify CI passes with new configuration

## Rollback
Revert pytest.ini to previous version (comment out coverage lines)

## Estimated Effort
1 hour (enable + measure baseline + adjust threshold)

## Success Criteria
- Coverage report generated successfully
- Baseline coverage percentage measured
- Threshold set to reasonable value (≥60%)
- All existing tests still pass
- CI integrates coverage reporting

## Related Issues
Addresses ISS-004 (Medium priority quality gap)

## Dependencies
- None (pytest-cov already installed)

## Notes
- This is Phase 2 of quality improvement (after Phase 1 structural fixes)
- Coverage threshold should be reviewed quarterly
- Consider aiming for 80%+ in future once baseline is established
- HTML report provides detailed line-by-line coverage analysis
