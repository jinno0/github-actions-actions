# PR-001: Fix pytest.ini Duplicate addopts Configuration

## Priority
**CRITICAL** - Blocks all testing

## Problem Statement
pytest.ini ファイルに `addopts` ディレクティブが重複して定義されており（Line 13と29）、pytestが全く実行できない状態にある。

### Evidence
- **Error**: `ERROR: /home/jinno/github-actions-actions/pytest.ini:29: duplicate name 'addopts'`
- **Impact**: 既存の2つのテストも実行不可能
- **Affected**: All pytest commands fail

## Root Cause
Line 13で最初の `addopts` を定義し、Line 29で2回目の定義を行っている。おそらくカバレッジ設定追加時のマージエラー。

## Proposed Solution

### Step 1: Merge addopts Directives

**File**: `pytest.ini:13,29`

**Current State**:
```ini
# Line 13-17
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings

# Line 29-34 (DUPLICATE)
addopts =
    --cov=.
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=json:coverage.json
    --cov-fail-under=70
```

**Proposed Change**:
```ini
# Line 13-22 (MERGED)
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings
    --cov=.
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=json:coverage.json
    --cov-fail-under=70

# Remove duplicate definition at line 29-34
```

### Step 2: Verification

1. Run `pytest --collect-only` to verify configuration is valid
2. Run existing tests: `pytest tests/ -v`
3. Verify coverage reports are generated: `ls htmlcov/ coverage.json`

## Expected Outcome

### Success Criteria
- ✅ `pytest` command executes without configuration errors
- ✅ All existing tests (test_review_and_merge, test_spec_to_code) run successfully
- ✅ Coverage reports are generated correctly

### Side Effects
- None (pure configuration fix)

## Rollback Plan

If issues arise:
1. Restore original pytest.ini from git: `git checkout pytest.ini`
2. Revert to manual test execution without pytest

## Estimated Effort
- **Implementation**: 5 minutes
- **Testing**: 5 minutes
- **Total**: 10 minutes

## Related Issues
- Resolves: GAP-002 (pytest configuration error)
- Unblocks: GAP-001 (test coverage measurement)
- Enables: GAP-004 (Dry Run verification)

## Assumptions
Based on ASM-003 (quality.target_test_coverage >= 80%), this fix is the first step toward achieving that target.

## Verification Method
```bash
# After applying the fix
cd /home/jinno/github-actions-actions
pytest tests/ -v --tb=short
# Expected: Tests run successfully, coverage reports generated
```

## References
- Source: `.audit/analysis/as_is.yml -> issues.ISS-001`
- Source: `.audit/analysis/gap.yml -> GAP-002`
