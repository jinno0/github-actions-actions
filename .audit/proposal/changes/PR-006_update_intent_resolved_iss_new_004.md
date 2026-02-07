# PR-006: Update intent.yml - Resolve ISS-NEW-004 (Coverage Discrepancy)

**Status:** ✅ READY TO APPLY  
**Priority:** LOW  
**Effort:** 5 minutes  
**Type:** Documentation update  
**Blocks:** None

## Problem Statement

ISS-NEW-004 was opened due to a perceived discrepancy between coverage.json (92.99%) and pytest --cov (11.11%). This issue has been **resolved** - both tools now report 92.99%.

The intent.yml still contains ASM-003 with `status: needs_revision`, which should be updated to reflect resolution.

## Evidence

```bash
# Verification executed 2026-02-07T09:21:04Z
$ python -c "import json; data=json.load(open('coverage.json')); print(data['totals']['percent_covered'])"
92.99

$ pytest --cov=actions --cov=scripts --cov-report=term
TOTAL                                  927      65    92.99%
```

Both measurements now agree. The discrepancy has been resolved.

## Proposed Changes

### File: `.audit/config/intent.yml`

```yaml
# BEFORE
assumptions:
  - id: "ASM-003"
    field: "quality_attributes.test_coverage"
    value: ">= 70% (ただし測定値の不整合あり: reported 92.99% vs pytest 11.11%)"
    reason: "README.mdに「このプロジェクトでは、テストカバレッジ >= 70% を目標としています」と明記。ただしcoverage.jsonとpytest reportの値が大きく異なり、実態が不明。"
    confidence: "low"
    status: "needs_revision"
    recommended_action: "ISS-NEW-004の解決を優先（coverage.py設定の調査）"

# AFTER
assumptions:
  - id: "ASM-003"
    field: "quality_attributes.test_coverage"
    value: "92.99% (目標70%を達成)"
    reason: "README.mdに「このプロジェクトでは、テストカバレッジ >= 70% を目標としています」と明記。coverage.jsonとpytest --covの両方が92.99%を報告。ISS-NEW-004解決済み。"
    confidence: "high"
    status: "confirmed"
    verification_date: "2026-02-07"
    verification_method: "coverage.jsonとpytest --covの値を照合"
```

## Impact

**Benefits:**
- Removes confusion about test coverage discrepancy
- Updates assumption confidence from "low" to "high"
- Documents ISS-NEW-004 resolution
- Aligns intent.yml with verified state

**Risks:**
- None (documentation-only change)

## Verification Criteria

- [ ] ASM-003 status changed from "needs_revision" to "confirmed"
- [ ] ASM-003 confidence changed from "low" to "high"
- [ ] Discrepancy note removed from value field
- [ ] Verification date and method documented

## Rollback Plan

If incorrect:
1. Revert intent.yml to previous state
2. Re-open ISS-NEW-004 if discrepancy reappears

No operational impact. Intent.yml is audit metadata only.

## Implementation Steps

```bash
# 1. Backup current intent.yml
cp .audit/config/intent.yml .audit/config/intent.yml.backup

# 2. Edit .audit/config/intent.yml
#    - Update ASM-003 as shown above

# 3. Verify YAML syntax
python -c "import yaml; yaml.safe_load(open('.audit/config/intent.yml'))"

# 4. Commit
git add .audit/config/intent.yml
git commit -m "audit: resolve ISS-NEW-004 - update ASM-003 test coverage assumption

- coverage.json and pytest --cov both report 92.99%
- Update ASM-003 confidence: low -> high
- Update ASM-003 status: needs_revision -> confirmed"
```

---

**Ready for autonomous application**  
**Estimated time: 5 minutes**  
**Risk: None (documentation only)**
