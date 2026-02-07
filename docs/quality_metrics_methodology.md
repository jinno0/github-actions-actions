# Quality Metrics Methodology

**Last Updated:** 2026-02-07
**Version:** 1.0
**Owner:** DevOps Team

## Overview

This document defines how AI review quality is measured in the github-actions-actions project.

## Acceptance Rate Calculation

### Formula

```
Acceptance Rate = (Accepted + Modified) / Total Reviews * 100
```

### Outcome Categories

#### 1. Accepted ✅

**Definition:** The AI-generated review is applied to the codebase without any modifications.

**Example:**
```yaml
AI Review: "Add error handling for file not found"
Developer Action: Applies exactly as suggested
Outcome: Accepted
```

**Counts Toward:** Acceptance Rate ✓

---

#### 2. Modified 📝

**Definition:** The AI-generated review is applied with minor adjustments (typos, variable names, formatting).

**Example:**
```yaml
AI Review: "Add error handling for file not found"
Developer Action: Applies suggestion but changes variable name from `err` to `error`
Outcome: Modified
```

**Counts Toward:** Acceptance Rate ✓

**Criteria for "Minor":**
- Typos/grammar corrections
- Variable/function renaming
- Code style adjustments
- Comment clarifications

**Does NOT Include:**
- Logic changes
- Alternative implementations
- Partial application

---

#### 3. Rejected ❌

**Definition:** The AI-generated review is not applied because it is incorrect, irrelevant, or harmful.

**Example:**
```yaml
AI Review: "Add error handling for file not found"
Developer Action: Does not apply, comments: "File existence is checked upstream"
Outcome: Rejected (reason: incorrect assumption)
```

**Counts Toward:** Acceptance Rate ✗

**Common Reasons:**
- Incorrect understanding of context
- Suggests already-implemented features
- Introduces bugs
- Conflicts with requirements

---

#### 4. Needs Work 🔧

**Definition:** The AI-generated review requires substantial revisions or provides a useful direction but needs significant rework.

**Example:**
```yaml
AI Review: "Add error handling for file not found"
Developer Action: Partially implements, but reworks 50%+ of the suggestion
Outcome: Needs Work
```

**Counts Toward:** Acceptance Rate ✗

**Criteria for "Substantial":**
- Logic changes
- Alternative implementation approach
- Only uses the concept, not the code

---

## Data Collection

### Sources

1. **GitHub Issues:** Developers comment with outcome categorization
2. **PR Comments:** AI review comments with reactions/feedback
3. **Workflow Logs:** Automated workflow execution outcomes

### Automated Tracking

The `scripts/calculate_acceptance_rate.py` script:

1. Scans merged PRs with AI review comments
2. Parses developer feedback
3. Categorizes based on keyword analysis:
   ```python
   keywords = {
       'accepted': ['lgtm', 'looks good', 'applied', '+1'],
       'modified': ['applied with', 'changed', 'tweaked'],
       'rejected': ['incorrect', 'wrong', 'not applicable', 'n/a'],
       'needs_work': ['partially', 'rework', 'revision']
   }
   ```

4. Calculates acceptance rate

### Manual Categorization

For ambiguous cases, developers can add labels:
- `outcome:accepted`
- `outcome:modified`
- `outcome:rejected`
- `outcome:needs_work`

## Target Setting

### Current Target: >= 70%

**Rationale:**
- Allows for 30% of reviews to be rejected or need rework
- Balances quality with automation efficiency
- Industry benchmark for AI assistance tools

### Adjustment Criteria

The target should be reviewed quarterly and adjusted if:
- Acceptance rate consistently exceeds 90% → raise target
- Acceptance rate consistently below 60% → investigate quality issues
- Context changes (e.g., new AI model)

## Reporting

### Weekly Reports

Every Monday at 9:00 JST, a GitHub Actions workflow generates:
- Previous 7 days' acceptance rate
- Comparison to baseline
- Trend analysis (↑→↓)
- Top 3 rejection reasons

**Workflow:** `.github/workflows/generate-quality-report.yml`

### Monthly Reports

Every first Monday, include:
- 30-day rolling acceptance rate
- Outcome breakdown trends
- Correlation with code quality metrics

### Baseline Reports

Initial baseline established at project start (or after 20+ reviews).

**Current Baseline:** [acceptance-rate-baseline-2026-02-07.md](../metrics/acceptance-rate-baseline-2026-02-07.md)

## Limitations

1. **Subjectivity:** Distinguishing "modified" vs "needs work" can be subjective
2. **Incomplete Data:** Not all developers provide feedback
3. **Context Blind:** Acceptance rate doesn't capture "partially accepted" nuance

## Future Improvements

- [ ] Add sentiment analysis to feedback
- [ ] Track time saved by AI reviews
- [ ] Correlate acceptance with bug rates
- [ ] A/B test different review prompts

---

**Document Owner:** DevOps Team
**Review Frequency:** Quarterly
**Next Review:** 2026-05-07

## Related Documents

- [Baseline Report](../metrics/acceptance-rate-baseline-2026-02-07.md)
- [Quality Metrics Overview](../metrics/QUALITY_METRICS.md)
- [Outcome Examples](../examples/quality-metrics/outcome-examples.md)
