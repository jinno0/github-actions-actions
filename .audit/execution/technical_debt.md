# Technical Debt Notes - Run 2026-02-08T05:07:00Z

This document tracks technical debt introduced during PR-002 execution that should be addressed in future improvement cycles.

## High Priority Debt

### 1. Code Duplication in Metrics Calculation
**Location**:
- `scripts/test_data_collection.py` (lines 96-109)
- `scripts/calculate_acceptance_rate.py` (lines 17-83)

**Issue**: Acceptance rate calculation logic duplicated

**Recommendation**: Extract to `scripts/metrics_utils.py`
```python
def calculate_acceptance_rate(metrics: List[Dict]) -> Dict[str, float]:
    """Shared acceptance rate calculation."""
```

**Estimated Effort**: 4-6 hours

---

### 2. Inconsistent Metrics Schemas
**Location**:
- `metrics/review_metrics.json` (flat list format)
- `metrics/acceptance_rate.json` (aggregated format)

**Issue**: Two different schemas prevent data aggregation

**Recommendation**: Standardize on single schema (recommend aggregated with entries array)

**Estimated Effort**: 6-8 hours

---

### 3. Missing Privacy Controls
**Location**: `scripts/test_data_collection.py`

**Issue**: No `DISABLE_TELEMETRY` environment variable check

**Existing Pattern**:
```python
# From calculate_acceptance_rate.py:254-257
if os.getenv("DISABLE_TELEMETRY", "").lower() == "true":
    print("Quality metrics analysis is disabled...")
    return 0
```

**Recommendation**: Add privacy check to test data collection script

**Estimated Effort**: 1-2 hours

---

## Medium Priority Debt

### 4. Missing Type Annotations
**Location**: `scripts/test_data_collection.py`

**Issue**: No type hints, inconsistent with project style

**Existing Pattern**: All scripts use extensive type annotations
```python
def calculate_acceptance_rate(metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
```

**Recommendation**: Add type hints to all functions

**Estimated Effort**: 2-3 hours

---

### 5. Hardcoded Test Values
**Location**: `scripts/test_data_collection.py` (lines 25-127)

**Issue**: Test data hardcoded, no flexibility for different scenarios

**Recommendation**: Add CLI arguments for configuration
```python
parser.add_argument("--num-reviews", type=int, default=10)
parser.add_argument("--acceptance-rate", type=float, default=70.0)
parser.add_argument("--time-period", default="30d")
```

**Estimated Effort**: 3-4 hours

---

### 6. Workflow Duplication
**Location**: `.github/workflows/check-data-collection.yml`

**Issue**: Python setup, commit patterns duplicated across 4+ workflows

**Recommendation**: Create reusable composite actions

**Estimated Effort**: 4-6 hours

---

## Low Priority Debt

### 7. Mixed Language Documentation
**Location**: `scripts/test_data_collection.py`

**Issue**: Japanese docstrings, English code (inconsistent)

**Recommendation**: Standardize on English documentation

**Estimated Effort**: 1 hour

---

### 8. Missing Unit Tests
**Location**: No tests for `test_data_collection.py`

**Issue**: Cannot validate refactoring doesn't break functionality

**Recommendation**: Add test coverage in `tests/metrics/`

**Estimated Effort**: 3-4 hours

---

## Documentation Debt

### 9. Outdated README Warnings
**Location**: `README.md` (lines 185-211)

**Issue**: Warning about missing `metrics/review_metrics.json` is now outdated

**Recommendation**: Update to document test data collection capability

**Estimated Effort**: 30 minutes

---

### 10. Missing Cross-References
**Location**: Various documentation files

**Issue**: Scripts not linked, no usage flows documented

**Recommendation**:
- Update `metrics/README.md`
- Create `scripts/README.md`
- Add integration guide

**Estimated Effort**: 2-3 hours

---

## Total Estimated Effort

- **High Priority**: 11-16 hours
- **Medium Priority**: 9-13 hours
- **Low Priority**: 4-5 hours
- **Documentation**: 2.5-3.5 hours

**Total**: 22.5-37.5 hours

---

## Prioritization for Next Cycle

### Phase 1 (Must Do)
1. Add `DISABLE_TELEMETRY` check (1-2 hours)
2. Extract shared utilities (4-6 hours)
3. Update README.md (30 minutes)

### Phase 2 (Should Do)
4. Add type annotations (2-3 hours)
5. Add CLI arguments (3-4 hours)
6. Standardize metrics schema (6-8 hours)

### Phase 3 (Nice to Have)
7. Consolidate workflows (4-6 hours)
8. Add unit tests (3-4 hours)
9. Standardize documentation language (1 hour)

---

## Notes

- This debt was incurred to rapidly establish data collection infrastructure
- The functionality works correctly but needs alignment with project patterns
- All debt is documented and traceable for future improvement cycles
- No critical security issues or data loss risks identified

**Decision**: Acceptable debt given successful achievement of core objectives (AI review acceptance rate now measurable at 90%).
