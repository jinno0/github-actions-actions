# PR-003: Test Coverage Recovery (Gap-003)

**Status:** Proposed
**Priority:** High
**Target Gap:** GAP-003
**Estimated Effort:** 3-5 hours

## Summary

`generate_review_quality_dashboard.py`がテストなしで追加されたため、全体のテストカバレッジが88.31% → 78.15%に低下した。このスクリプトのテストを追加し、カバレッジを80%以上に回復させる。

## Current State

```yaml
test_coverage:
  total: 78.15%
  target: ">= 80%"
  status: "approaching"
  gap: -1.85%

uncovered_scripts:
  - generate_review_quality_dashboard.py: 0.00% (128行全て未カバー)
  - test_data_collection.py: 0.00% (38行全て未カバー)
```

## Root Cause

改善実行プロセスで「新規コードにはテストを追加する」という原則が守られていなかった：
- `generate_review_quality_dashboard.py`はPR-002で追加されたが、テストが含まれていなかった
- レビュープロセスでカバレッジ低下が検出されなかった

## Proposed Changes

### 1. Test File Creation

**File:** `tests/test_generate_review_quality_dashboard.py`

```python
"""
Tests for generate_review_quality_dashboard.py script
"""
import json
import pytest
from pathlib import Path
from scripts.generate_review_quality_dashboard import (
    load_review_metrics,
    calculate_acceptance_rate,
    generate_dashboard_markdown,
    analyze_trends,
    identify_rejection_reasons
)

def test_load_review_metrics(temp_metrics_file):
    """Test loading review metrics from JSON file"""
    metrics = load_review_metrics(temp_metrics_file)
    assert isinstance(metrics, list)
    assert len(metrics) > 0

def test_calculate_acceptance_rate():
    """Test acceptance rate calculation"""
    metrics = [
        {"outcome": "approved"},
        {"outcome": "approved"},
        {"outcome": "modified"},
        {"outcome": "rejected"}
    ]
    rate = calculate_acceptance_rate(metrics)
    assert rate == 50.0  # 2/4 = 50%

def test_calculate_acceptance_rate_empty():
    """Test acceptance rate with empty metrics"""
    rate = calculate_acceptance_rate([])
    assert rate == 0.0

def test_generate_dashboard_markdown():
    """Test dashboard markdown generation"""
    metrics = [
        {
            "outcome": "approved",
            "timestamp": "2026-02-01T00:00:00Z",
            "confidence_score": 0.9
        }
    ]
    markdown = generate_dashboard_markdown(metrics)
    assert "# AI Review Quality Dashboard" in markdown
    assert "60.0%" in markdown or "Acceptance Rate" in markdown

def test_analyze_trends():
    """Test trend analysis"""
    metrics = [
        {"outcome": "approved", "timestamp": "2026-02-01T00:00:00Z"},
        {"outcome": "rejected", "timestamp": "2026-02-08T00:00:00Z"}
    ]
    trends = analyze_trends(metrics)
    assert "weekly_breakdown" in trends
    assert "trend_direction" in trends

def test_identify_rejection_reasons():
    """Test rejection reason identification"""
    metrics = [
        {"outcome": "rejected", "rejection_reasons": ["Low quality suggestions"]},
        {"outcome": "approved"}
    ]
    reasons = identify_rejection_reasons(metrics)
    assert "Low quality suggestions" in reasons

def test_integration_end_to_end(temp_metrics_file, temp_output_file):
    """Test end-to-end dashboard generation"""
    # Import main function
    from scripts.generate_review_quality_dashboard import main

    # Run main with test paths
    main(str(temp_metrics_file), str(temp_output_file))

    # Verify output file created
    assert temp_output_file.exists()

    # Verify content
    content = temp_output_file.read_text()
    assert "# AI Review Quality Dashboard" in content
```

### 2. Coverage Target

```yaml
expected_coverage:
  before: "78.15%"
  after: "82.5%"
  improvement: "+4.35%"

breakdown:
  generate_review_quality_dashboard:
    before: "0.00%"
    after: "85.0%"
    lines_covered: "109/128"
```

### 3. Test Execution Command

```bash
# Run new tests
pytest tests/test_generate_review_quality_dashboard.py -v

# Verify coverage improvement
pytest --cov=scripts --cov-report=term-missing
```

## Success Criteria

- [ ] `tests/test_generate_review_quality_dashboard.py` created with 7+ test cases
- [ ] All new tests pass
- [ ] Overall coverage increases to 82%+ (78.15% → 82.5%)
- [ ] `generate_review_quality_dashboard.py` coverage reaches 85%+
- [ ] CI passes with new coverage threshold

## Rollback Plan

If tests introduce issues:
1. Delete `tests/test_generate_review_quality_dashboard.py`
2. Coverage returns to 78.15%
3. No impact on production code

## Dependencies

None

## Risks

- **Low**: Tests are additive, no production code changes
- **Risk**: Test quality may be low (need proper fixtures, mocks)

## Next Steps

1. Create test file with above test cases
2. Run `pytest` to verify all tests pass
3. Run `pytest --cov` to verify coverage improvement
4. Submit PR for review

## Related Gaps

- GAP-003: Test coverage below 80% target
- GAP-006: Technical debt (0% coverage scripts)

## Related Assumptions

- ASM-NEW-001: Coverage decline is temporary due to new script

## Metadata

**Author:** Repo Genesis Auditor v2.0
**Generated:** 2026-02-09T09:41:00Z
**Run ID:** 2026-02-09T09:41:00Z
