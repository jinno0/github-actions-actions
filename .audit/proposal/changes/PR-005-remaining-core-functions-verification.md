# PR-005: Remaining Core Functions Verification

**Status:** Proposed
**Priority:** P2 - MEDIUM
**Estimated Effort:** 3-4 hours
**Gap ID:** GAP-006

---

## Problem Statement

**Current State:**
- 6 Core Functions defined in `intent.yml`
- 4 have been verified (CF-001, CF-002, CF-004, CF-005)
- 2 remain unverified (CF-003, CF-006)

**Unverified Core Functions:**

### CF-003: Custom Review Rules Injection
- **Claim**: "カスタムレビュールール注入機能を提供し、プロジェクト固有のコーディング規約をAIレビューに反映できる"
- **Source**: README.md:65-77
- **Status**: Not verified
- **Risk**: Users cannot confirm this feature works as documented

### CF-006: AI Review Quality Metrics Tracking
- **Claim**: "AIレビュー品質メトリクス（受入率）を追跡・測定できる"
- **Source**: README.md:171-217
- **Status**: Partially verified (data collection works, but tracking needs validation)
- **Current Data**: 75.0% (3/4件)
- **Risk**: Metrics system may not be tracking correctly

**Impact:**
- Medium: README.md claims may not match reality
- Users cannot trust that documented features work
- May affect adoption decisions

---

## Proposed Solution: Generate Verification Scenarios

### Phase 1: CF-003 Verification (1.5 hours)

**Verification Scenario:**
```yaml
# .audit/analysis/verification_scenarios.yml
scenarios:
  - function_id: "CF-003"
    name: "Custom Review Rules Injection"

    input:
      type: "config"
      path: ".audit/test_data/custom_rules.json"
      content: |
        {
          "rules": [
            {
              "id": "rule-1",
              "pattern": "TODO|FIXME",
              "message": "Resolve TODOs before committing"
            },
            {
              "id": "rule-2",
              "pattern": "print\\(.*\\)",
              "message": "Use logging instead of print statements"
            }
          ]
        }

    expected_output:
      type: "review_comments"
      contains:
        - "Custom rule matched: TODO|FIXME"
        - "Custom rule matched: print\\("
      validation_rules:
        - "Custom rules are loaded from config"
        - "Rules are applied during review"
        - "Custom rule violations are reported"

    edge_cases:
      - name: "Empty rules file"
        input: "{}"
        expected: "No custom rules applied, defaults only"
      - name: "Invalid rule pattern"
        input: '{"rules": [{"pattern": "["}]}'
        expected: "Error: Invalid regex pattern"
```

**Verification Script:**
```python
# .audit/verification/verify_cf003.py
def verify_cf003_custom_rules():
    """CF-003: Custom review rules injection"""

    # 1. Create test custom rules
    test_rules = {
        "rules": [
            {"id": "rule-1", "pattern": "TODO", "message": "Resolve TODOs"},
            {"id": "rule-2", "pattern": "print(", "message": "Use logging"}
        ]
    }

    # 2. Create test code with violations
    test_code = """
def process():
    TODO: implement this
    print("debugging")
"""

    # 3. Run review with custom rules
    try:
        from review_and_merge import apply_custom_rules
        result = apply_custom_rules(test_code, test_rules)

        # 4. Verify custom rules were applied
        assert "TODO" in result.violations
        assert "print(" in result.violations

        return VerificationResult(
            function_id="CF-003",
            scenario_name="Custom Review Rules Injection",
            passed=True,
            actual_output=result.violations,
            expected_output=["TODO", "print("],
            interpretation="Custom rules are correctly injected and applied"
        )

    except Exception as e:
        return VerificationResult(
            function_id="CF-003",
            scenario_name="Custom Review Rules Injection",
            passed=False,
            error_message=str(e),
            interpretation="Custom rules injection failed or not implemented"
        )
```

### Phase 2: CF-006 Verification (1.5 hours)

**Verification Scenario:**
```yaml
# .audit/analysis/verification_scenarios.yml
scenarios:
  - function_id: "CF-006"
    name: "AI Review Quality Metrics Tracking"

    input:
      type: "review_data"
      path: ".audit/test_data/reviews.json"
      content: |
        {
          "reviews": [
            {"id": "1", "accepted": true, "timestamp": "2026-02-08T10:00:00Z"},
            {"id": "2", "accepted": true, "timestamp": "2026-02-08T11:00:00Z"},
            {"id": "3", "accepted": false, "timestamp": "2026-02-08T12:00:00Z"},
            {"id": "4", "accepted": true, "timestamp": "2026-02-08T13:00:00Z"}
          ]
        }

    expected_output:
      type: "metrics"
      content: |
        {
          "acceptance_rate": 75.0,
          "total_reviews": 4,
          "accepted": 3,
          "rejected": 1,
          "baseline_date": "2026-02-08"
        }
      validation_rules:
        - "Acceptance rate calculated correctly: 3/4 = 75%"
        - "Metrics saved to review_metrics.json"
        - "Baseline date is tracked"

    edge_cases:
      - name: "Empty reviews file"
        input: "[]"
        expected: "No data available, acceptance rate: N/A"
      - name: "New review data"
        input: "[{\"id\": \"5\", \"accepted\": true}]"
        expected: "Acceptance rate updates to 4/5 = 80%"
```

**Verification Script:**
```python
# .audit/verification/verify_cf006.py
def verify_cf006_metrics_tracking():
    """CF-006: AI review quality metrics tracking"""

    # 1. Create test review data
    test_reviews = [
        {"id": "1", "accepted": True},
        {"id": "2", "accepted": True},
        {"id": "3", "accepted": False},
        {"id": "4", "accepted": True}
    ]

    # 2. Run metrics calculation
    try:
        from scripts.calculate_acceptance_rate import calculate_metrics
        result = calculate_metrics(test_reviews)

        # 3. Verify metrics are correct
        assert result.acceptance_rate == 75.0
        assert result.total_reviews == 4
        assert result.accepted == 3
        assert result.rejected == 1

        # 4. Verify metrics are saved
        import json
        from pathlib import Path
        metrics_file = Path("metrics/review_metrics.json")
        assert metrics_file.exists()

        saved_metrics = json.loads(metrics_file.read_text())
        assert saved_metrics["acceptance_rate"] == 75.0

        return VerificationResult(
            function_id="CF-006",
            scenario_name="AI Review Quality Metrics Tracking",
            passed=True,
            actual_output=result.__dict__,
            expected_output={"acceptance_rate": 75.0, "total": 4, "accepted": 3},
            interpretation="Metrics are correctly tracked and persisted"
        )

    except Exception as e:
        return VerificationResult(
            function_id="CF-006",
            scenario_name="AI Review Quality Metrics Tracking",
            passed=False,
            error_message=str(e),
            interpretation="Metrics tracking failed or not implemented correctly"
        )
```

### Phase 3: Update Verification Script (1 hour)

**Update `.audit/verification/verify_core_functions.py`:**

```python
# Add to existing verify_core_functions.py

def verify_cf003_custom_review_rules() -> VerificationResult:
    """CF-003: Custom review rules injection"""
    # Import from verify_cf003.py
    # ... (implementation from above)

def verify_cf006_metrics_tracking() -> VerificationResult:
    """CF-006: AI review quality metrics tracking"""
    # Import from verify_cf006.py
    # ... (implementation from above)

def main():
    """Verify all core functions"""
    results = [
        # ... existing verifications
        verify_cf003_custom_review_rules(),
        verify_cf006_metrics_tracking(),
    ]
    # ... existing reporting
```

---

## Implementation Plan

### Step 1: Create Verification Scenarios (1 hour)
- Document test cases for CF-003 and CF-006
- Define input data, expected output, edge cases
- Save to `.audit/analysis/verification_scenarios.yml`

### Step 2: Implement Verification Scripts (2 hours)
- Create `verify_cf003.py`
- Create `verify_cf006.py`
- Update `verify_core_functions.py` to include new tests

### Step 3: Execute Verification (30 minutes)
- Run verification scripts
- Generate verification report
- Update `intent.yml` with results

### Step 4: Document Results (30 minutes)
- Update `.audit/output/verification_result.json`
- Document any gaps or issues found
- Create follow-up tasks if needed

---

## Success Criteria

- [ ] CF-003 verification scenario defined
- [ ] CF-006 verification scenario defined
- [ ] Verification scripts implemented
- [ ] Verification executed and results documented
- [ ] `intent.yml` updated with verification status
- [ ] All 6 Core Functions now have verification status

---

## Expected Outcomes

**Best Case:**
- Both CF-003 and CF-006 pass verification
- Documentation is accurate
- Users can trust these features work

**Medium Case:**
- One or both functions have minor issues
- Clear understanding of what needs fixing
- Follow-up issues created

**Worst Case:**
- One or both functions are not implemented
- Documentation needs significant updates
- May need to revisit value proposition

---

## Related Issues

- Gap: GAP-006
- Core Functions: CF-003 (unverified), CF-006 (partial)
- Verification: `.audit/verification/verify_core_functions.py`
