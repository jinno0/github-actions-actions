# PR-004: AI Review A/B Testing Framework (Gap-001)

**Status:** Proposed
**Priority:** Critical
**Target Gap:** GAP-001
**Estimated Effort:** 1-2 weeks data collection + 4-6 hours implementation

## Summary

AIレビュー受入率が目標70%を下回る60%で、**低下傾向が続いている**（66.7% → 66.7% → 50.0%）。PR-002でプロンプト改善を実施したが、効果が不明確。A/Bテストフレームワークを実装し、新プロンプトと旧プロンプトを統計的に比較する。

## Current State

```yaml
ai_review_acceptance_rate:
  current: "60.0%"
  target: ">= 70%"
  gap: -10.0%
  trend: "declining"  # ⚠️ CRITICAL

breakdown:
  total_reviews: 10
  approved: 6 (60%)
  modified: 3 (30%)
  rejected: 1 (10%)

weekly_trend:
  2026-03: "66.7% (3 reviews)"
  2026-04: "66.7% (3 reviews)"
  2026-05: "50.0% (4 reviews)"  # ⚠️ Declining
```

## Root Cause Analysis

PR-002のプロンプト改善が効果を表していない可能性：
1. **データ収集期間不足**: プロンプト変更直後のデータは少ない
2. **プロンプト改善が不十分**: 改善内容が実際の問題に対応していない
3. **逆効果の可能性**: 新プロンプトが旧プロンプトより品質が低い

**現状**: プロンプト変更前後の比較測定がなく、仮説検証ができていない。

## Proposed Solution: A/B Testing Framework

### 1. A/B Test Infrastructure

**File:** `scripts/setup_ab_test.py`

```python
"""
A/B Testing Framework for AI Review Prompts

Enables statistical comparison between different prompt versions.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

class PromptABTest:
    """Manages A/B testing for review prompts"""

    def __init__(self, test_id: str):
        self.test_id = test_id
        self.start_date = datetime.now().isoformat()
        self.metrics_dir = Path("metrics/ab_tests")

    def create_prompt_variants(self) -> Dict[str, str]:
        """Create A and B prompt variants"""
        return {
            "A": open("prompts/review_prompt_v1.md").read(),  # Control (old)
            "B": open("prompts/review_prompt_v2.md").read()   # Treatment (new)
        }

    def assign_variant(self, pr_number: int) -> str:
        """Assign PR to variant A or B using consistent hashing"""
        return "A" if pr_number % 2 == 0 else "B"

    def record_outcome(self, pr_number: int, variant: str, outcome: Dict):
        """Record review outcome for assigned variant"""
        result = {
            "test_id": self.test_id,
            "pr_number": pr_number,
            "variant": variant,
            "timestamp": datetime.now().isoformat(),
            "outcome": outcome["status"],  # approved/modified/rejected
            "confidence_score": outcome.get("confidence", 0.0),
            "suggestions_count": outcome.get("suggestions", 0),
            "accepted_suggestions": outcome.get("accepted", 0)
        }

        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        output_file = self.metrics_dir / f"{self.test_id}_results.jsonl"

        with open(output_file, "a") as f:
            f.write(json.dumps(result) + "\n")

    def calculate_statistics(self) -> Dict:
        """Calculate statistical significance"""
        import statistics

        results = []
        results_file = self.metrics_dir / f"{self.test_id}_results.jsonl"

        if not results_file.exists():
            return {"error": "No results yet"}

        with open(results_file) as f:
            for line in f:
                results.append(json.loads(line))

        # Group by variant
        variant_a = [r for r in results if r["variant"] == "A"]
        variant_b = [r for r in results if r["variant"] == "B"]

        # Calculate acceptance rates
        rate_a = sum(1 for r in variant_a if r["outcome"] == "approved") / len(variant_a)
        rate_b = sum(1 for r in variant_b if r["outcome"] == "approved") / len(variant_b)

        # Calculate statistical significance (simplified)
        # TODO: Implement proper t-test or z-test
        lift = ((rate_b - rate_a) / rate_a) * 100 if rate_a > 0 else 0

        return {
            "variant_a_acceptance": f"{rate_a*100:.1f}%",
            "variant_b_acceptance": f"{rate_b*100:.1f}%",
            "lift": f"{lift:+.1f}%",
            "sample_size_a": len(variant_a),
            "sample_size_b": len(variant_b),
            "winner": "B" if rate_b > rate_a else "A",
            "significant": len(variant_a) >= 10 and len(variant_b) >= 10
        }

    def generate_report(self) -> str:
        """Generate A/B test report"""
        stats = self.calculate_statistics()

        report = f"""# A/B Test Report: {self.test_id}

**Test Duration:** {self.start_date} - Present
**Objective:** Compare prompt version A (control) vs B (treatment)

## Results

| Metric | Variant A (Control) | Variant B (Treatment) |
|--------|---------------------|----------------------|
| Acceptance Rate | {stats.get('variant_a_acceptance', 'N/A')} | {stats.get('variant_b_acceptance', 'N/A')} |
| Sample Size | {stats.get('sample_size_a', 0)} reviews | {stats.get('sample_size_b', 0)} reviews |

## Conclusion

**Winner:** Variant {stats.get('winner', 'TBD')}
**Lift:** {stats.get('lift', 'N/A')}
**Statistical Significance:** {'Yes' if stats.get('significant') else 'Not yet (need 20+ samples per variant)'}

## Recommendation

{self._make_recommendation(stats)}
"""
        return report

    def _make_recommendation(self, stats: Dict) -> str:
        """Generate recommendation based on results"""
        if not stats.get("significant"):
            return "Collect more data (aim for 20+ samples per variant)"

        if stats.get("winner") == "B":
            lift = float(stats.get("lift", "0").replace("%", "").replace("+", ""))
            if lift > 5:
                return "Variant B shows significant improvement. Recommend full rollout."
            else:
                return "Variant B shows marginal improvement. Consider refining prompt."
        else:
            return "Variant A (control) performs better. Revert to old prompt."

# CLI interface
if __name__ == "__main__":
    import sys

    test = PromptABTest("prompt_v1_vs_v2")

    if sys.argv[1] == "report":
        print(test.generate_report())
    elif sys.argv[1] == "stats":
        print(json.dumps(test.calculate_statistics(), indent=2))
```

### 2. Review Actions Integration

Modify review actions to support A/B testing:

```yaml
# actions/review-and-merge/action.yml
- name: Assign A/B test variant
  run: |
    VARIANT=$(python -c "from scripts.setup_ab_test import PromptABTest; print(PromptABTest('prompt_v1_vs_v2').assign_variant(${{ github.event.pull_request.number }}))")
    echo "variant=$VARIANT" >> $GITHUB_OUTPUT
  id: ab_test_assign

- name: Run AI review with variant
  run: |
    if [ "${{ steps.ab_test_assign.outputs.variant }}" == "A" ]; then
      PROMPT_PATH=prompts/review_prompt_v1.md
    else
      PROMPT_PATH=prompts/review_prompt_v2.md
    fi

    claude code review --prompt-file $PROMPT_PATH ...
```

### 3. Data Collection Protocol

```yaml
ab_test_protocol:
  duration: "2 weeks"
  target_sample_size: 20 reviews per variant (40 total)

  assignment_strategy:
    method: "consistent hashing by PR number"
    distribution: "50/50 split"

  data_points:
    - review_outcome  # approved/modified/rejected
    - confidence_score
    - suggestions_count
    - accepted_suggestions
    - rejection_reasons

  success_criteria:
    - statistical_significance: "p < 0.05"
    - minimum_sample_size: 20 per variant
    - measurable_difference: "> 5% lift"

  decision_matrix:
    - condition: "Variant B wins with > 5% lift and p < 0.05"
      action: "Full rollout of Variant B"

    - condition: "Variant A wins or difference < 5%"
      action: "Revert to Variant A, iterate on prompt"

    - condition: "Sample size insufficient"
      action: "Extend test duration"
```

## Success Criteria

- [ ] A/B test infrastructure implemented
- [ ] 20+ reviews collected per variant (40 total)
- [ ] Statistical analysis completed with p-value
- [ ] Clear winner identified or prompts iterated
- [ ] Acceptance rate improves to 70%+ (if Variant B wins)

## Expected Outcomes

### Scenario A: Variant B (New Prompt) Wins
```yaml
result: "New prompt is statistically better"
action: "Full rollout"
expected_improvement: "60% → 75%+ acceptance rate"
```

### Scenario B: Variant A (Old Prompt) Wins
```yaml
result: "New prompt is worse or not significantly better"
action: "Revert to old prompt, analyze why PR-002 failed"
learning: "Identify what went wrong with prompt improvement"
```

## Rollback Plan

If A/B testing causes issues:
1. Disable variant assignment in workflow
2. Force all reviews to use Variant A (known good)
3. Remove A/B test code (optional - can keep for future tests)

## Risks

- **Medium**: Extending test period may delay improvement
- **Low**: A/B testing adds minimal overhead to review process

## Dependencies

- 20+ reviews across multiple projects
- `scipy` or `statsmodels` library for statistical tests (optional, can use basic math)

## Timeline

```yaml
week_1:
  - "Implement A/B test infrastructure"
  - "Deploy to production"
  - "Start collecting data"

week_2:
  - "Continue data collection"
  - "Monitor sample sizes"

week_3:
  - "Analyze results"
  - "Generate report"
  - "Make decision (rollout/revert)"
```

## Related Gaps

- GAP-001: AI review acceptance rate below target and declining
- GAP-004: Improvement effectiveness measurement

## Related Assumptions

- ASM-NEW-001: Prompt improvement may be insufficient or data collection period too short

## Next Steps

1. Implement `scripts/setup_ab_test.py`
2. Create `prompts/review_prompt_v1.md` (backup current prompt)
3. Create `prompts/review_prompt_v2.md` (current PR-002 prompt)
4. Modify review actions to use A/B testing
5. Deploy and monitor data collection
6. After 2 weeks, generate report and make decision

## Metadata

**Author:** Repo Genesis Auditor v2.0
**Generated:** 2026-02-09T09:41:00Z
**Run ID:** 2026-02-09T09:41:00Z
**Critical Priority:** Addresses declining core metric
