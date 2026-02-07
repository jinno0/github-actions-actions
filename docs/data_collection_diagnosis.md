# Review Data Collection Diagnosis

**Date:** 2026-02-07
**Issue:** `metrics/review_metrics.json` does not exist
**Impact:** Cannot calculate baseline acceptance rate
**Related:** ISS-NEW-001, GAP-001

---

## Current Status

❌ **File Missing:** `metrics/review_metrics.json` does not exist
⚠️ **Pilot Projects:** Unverified (ISS-NEW-002 - placeholders in ADOPTION.md)
❓ **Action Status:** Unknown if running in pilot projects
✅ **Calculation Script:** `scripts/calculate_acceptance_rate.py` works correctly

---

## Root Cause Hypotheses

### 1. Pilot Projects Not Using Action (HIGH LIKELIHOOD)

**Evidence:**
- ADOPTION.md shows placeholder repos (`example/repo-1`, `example/repo-2`)
- No actual pilot projects verified
- README mentions "2 pilot projects" but no actual repos listed

**Impact:**
- No Action runs = No data collected
- Cannot measure AI review quality
- Cannot calculate baseline acceptance rate

**Resolution Required:**
1. Identify real pilot projects (contact team leads, check GitHub organization logs)
2. Update ADOPTION.md with actual repository URLs
3. Verify Actions are actually running in these projects
4. Document contact information for pilot teams

**Related:** ISS-NEW-002, PR-003

---

### 2. Metrics Collection Not Enabled (MEDIUM LIKELIHOOD)

**Evidence:**
- Needs verification in pilot project workflows
- `REVIEW_METRICS_FILE` environment variable may not be set
- Pilot projects may not have metrics collection configured

**Impact:**
- Action runs but doesn't save data
- Weekly reports have no data to process
- Cannot track AI review quality over time

**Resolution Required:**
1. Check pilot project workflow files for `REVIEW_METRICS_FILE` configuration
2. Verify environment variables are set in workflows
3. Check if Action templates include metrics collection code

**Example Configuration:**
```yaml
env:
  REVIEW_METRICS_FILE: ${{ github.workspace }}/metrics/review_metrics.json

permissions:
  contents: write  # Allow writing to repository
```

---

### 3. Permissions Issue (LOW-MEDIUM LIKELIHOOD)

**Evidence:**
- Needs verification
- Workflow may lack write permissions
- Action may try to write but fail silently

**Impact:**
- Action runs, attempts to save data, but fails
- No error messages visible to users
- Silent failure makes diagnosis difficult

**Resolution Required:**
1. Check workflow permissions in pilot projects
2. Verify `contents: write` permission is granted
3. Review GitHub Actions logs for permission errors

**Required Permissions:**
```yaml
permissions:
  contents: write
  pull-requests: write
```

---

### 4. Metrics File Path Issue (LOW LIKELIHOOD)

**Evidence:**
- File path may be relative vs absolute
- Working directory may differ from expected
- GitHub Actions workspace context may be misunderstood

**Impact:**
- Action writes to wrong location
- File created but not in expected `metrics/` directory
- Weekly workflow cannot find the file

**Resolution Required:**
1. Check Action code for file path construction
2. Verify GitHub Actions workspace context
3. Use absolute paths: `${{ github.workspace }}/metrics/review_metrics.json`

---

## Diagnostic Commands

### For Pilot Project Administrators

Run these commands in each pilot project repository:

```bash
# 1. Check if review-and-merge workflow exists
gh workflow list --search review-and-merge

# 2. Check workflow runs (last 30 days)
gh run list --workflow=review-and-merge.yml --limit 20

# 3. Check workflow configuration for metrics settings
cat .github/workflows/*review*.yml | grep -A 5 -B 5 "REVIEW_METRICS_FILE"

# 4. Check permissions
cat .github/workflows/*review*.yml | grep -A 10 "permissions:"

# 5. Check recent logs for errors
gh run view --log-failed | tail -100

# 6. Check if metrics file exists
ls -la metrics/review_metrics.json

# 7. Check file contents if it exists
cat metrics/review_metrics.json | jq '.reviews | length'
```

---

## Resolution Steps

### Step 1: Verify Pilot Projects (PR-003)

**Priority:** CRITICAL (blocks all data collection)

- [ ] Identify actual repositories using review-and-merge Action
- [ ] Confirm workflows are enabled and running
- [ ] Check recent workflow runs for errors
- [ ] Document contact information for pilot teams

**Commands:**
```bash
# List all repos in organization
gh repo list --limit 100

# For each candidate repo, check workflows:
gh workflow list --repo ORG/REPO
gh run list --repo ORG/REPO --workflow=review-and-merge.yml --limit 10
```

**Expected Output:**
- Real repository URLs (not `example/*`)
- Evidence of recent workflow runs
- Contact information (email or Slack)

---

### Step 2: Enable Metrics Collection

If workflows exist but don't collect metrics, add this configuration:

```yaml
# .github/workflows/review-and-merge.yml

name: Review and Merge
on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: write
  pull-requests: write

env:
  REVIEW_METRICS_FILE: ${{ github.workspace }}/metrics/review_metrics.json

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Ensure metrics directory exists
      - name: Setup metrics directory
        run: mkdir -p metrics

      # Initialize metrics file if it doesn't exist
      - name: Initialize metrics file
        run: |
          if [ ! -f ${{ env.REVIEW_METRICS_FILE }} ]; then
            echo '{"reviews":[]}' > ${{ env.REVIEW_METRICS_FILE }}
          fi

      # Run review-and-merge action
      - uses: your-org/github-actions-actions/review-and-merge@v1
        with:
          # ... your existing parameters ...
```

---

### Step 3: Create Metrics Directory and Initial File

```bash
# In pilot project repository
mkdir -p metrics
echo '{"reviews":[]}' > metrics/review_metrics.json
git add metrics/
git commit -m "chore: initialize review metrics file"
git push
```

---

### Step 4: Verify Data Collection

After enabling metrics collection:

- [ ] Wait for next PR to be reviewed (1-7 days)
- [ ] Check that `metrics/review_metrics.json` is updated
- [ ] Verify file contains review data
- [ ] Run acceptance rate calculation script

**Verification Commands:**
```bash
# Check file exists and has data
test -f metrics/review_metrics.json && echo "✅ File exists"
cat metrics/review_metrics.json | jq '.reviews | length'

# Calculate acceptance rate (if 20+ reviews collected)
python scripts/calculate_acceptance_rate.py
```

---

## Expected File Format

`metrics/review_metrics.json` should follow this structure:

```json
{
  "reviews": [
    {
      "pr_number": 123,
      "repo": "org/repo",
      "timestamp": "2026-02-07T10:00:00Z",
      "outcome": "accepted|modified|rejected",
      "suggestions_count": 5,
      "accepted_count": 4,
      "modified_count": 1,
      "rejected_count": 0,
      "reviewer": "claude-4-5",
      "files_touched": ["src/main.py", "tests/test_main.py"]
    }
  ]
}
```

---

## Troubleshooting

### Issue: File exists but is empty

**Symptoms:**
```bash
$ cat metrics/review_metrics.json
{"reviews":[]}
```

**Diagnosis:**
- Action may not be recording outcomes
- Check Action logs for errors
- Verify Action has metrics recording code

**Resolution:**
- Check review-and-merge Action source code
- Verify metrics writing logic is implemented
- Test with a sample PR

---

### Issue: Permission denied error

**Symptoms:**
```
Error: Permission denied (metrics/review_metrics.json)
```

**Diagnosis:**
- Workflow lacks `contents: write` permission
- GitHub Actions token has insufficient scopes

**Resolution:**
```yaml
permissions:
  contents: write  # Add this to workflow
```

---

### Issue: File not created

**Symptoms:**
```bash
$ ls metrics/review_metrics.json
ls: cannot access 'metrics/review_metrics.json': No such file or directory
```

**Diagnosis:**
- Action not running
- Metrics collection not enabled
- File path incorrect

**Resolution:**
- Verify Action is triggering on PR events
- Check `REVIEW_METRICS_FILE` environment variable
- Use absolute path: `${{ github.workspace }}/metrics/review_metrics.json`

---

## Next Actions

### Immediate (This Week)

1. **Complete PR-003** to identify real pilot projects
2. **Contact pilot teams** to verify Action usage
3. **Share this diagnostic document** with pilot project administrators

### Short-term (Next 1-2 Weeks)

4. **Enable metrics collection** in pilot project workflows
5. **Verify data collection** after next PR review
6. **Calculate baseline acceptance rate** once 20+ reviews collected

### Medium-term (Month 1)

7. **Generate weekly reports** using automated workflow
8. **Analyze acceptance rate trends**
9. **Identify improvement opportunities**

---

## Success Criteria

- [ ] Both pilot projects identified and contacted
- [ ] `metrics/review_metrics.json` exists in pilot projects
- [ ] At least 5 reviews collected within 7 days of enabling
- [ ] `scripts/calculate_acceptance_rate.py` can read the file successfully
- [ ] Baseline acceptance rate calculated (after 20+ reviews)
- [ ] Weekly reports generating automatically

---

## Related Documentation

- [Quality Metrics Methodology](quality_metrics_methodology.md)
- [Baseline Report](../metrics/acceptance-rate-baseline-2026-02-07.md)
- [Review and Merge Action Instructions](../instructions/review-and-merge.md)
- [Custom Rules Tutorial](../examples/custom-rules-tutorial.md)

---

## Appendix: Data Flow Diagram

```
┌─────────────────┐
│  PR Opens       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ review-and-merge Action │
│ triggers on PR          │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Claude Code CLI generates    │
│ review suggestions           │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Developer applies/modifies/  │
│ rejects suggestions          │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Action records outcome to    │
│ metrics/review_metrics.json  │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Weekly workflow reads file   │
│ and generates report         │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Acceptance rate calculated   │
│ and trend analysis           │
└──────────────────────────────┘
```

---

**Document Owner:** DevOps Team
**Next Review:** After PR-003 completion or 2026-02-14
**Status:** 🔍 AWAITING PILOT PROJECT VERIFICATION
