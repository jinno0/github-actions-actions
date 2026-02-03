# AI Review Quality Metrics

**Last Updated**: 2026-02-03
**Version**: 1.0.0

## Overview

This document describes the quality metrics collected for the AI review functionality in the `review-and-merge` action. These metrics help us understand the effectiveness and reliability of AI-powered code reviews.

## Why Track Quality Metrics?

AI code review is a powerful tool, but it's important to measure its actual effectiveness. Quality metrics help us:

1. **Measure Effectiveness**: Understand how often AI suggestions are accepted
2. **Identify Improvement Areas**: Discover patterns in rejected suggestions
3. **Build User Confidence**: Provide transparency about review quality
4. **Track Progress**: Monitor improvements in AI review capabilities over time

## Metrics Collected

### 1. Acceptance Rate

**Definition**: The percentage of AI reviews that are accepted by humans.

**Calculation**:
```
Acceptance Rate = (Approved + Modified) / Total Reviews × 100%
```

**Categories**:
- **Approved**: AI approved changes and human accepted without modification
- **Modified**: Human made changes before accepting AI suggestions
- **Rejected**: Human rejected AI suggestions
- **Needs Work**: AI requested changes to the PR

**Target**: >= 70%

**Interpretation**:
- **>= 80%**: Excellent - AI reviews are highly reliable
- **70-79%**: Good - AI reviews are generally reliable
- **50-69%**: Moderate - AI reviews need improvement
- **< 50%**: Poor - AI review quality needs significant improvement

### 2. Average Suggestions per Review

**Definition**: The average number of suggestions provided by the AI per review.

**Purpose**: Helps understand the verbosity and thoroughness of AI reviews.

**Current Average**: N/A (data collection in progress)

### 3. Average Accepted Suggestions

**Definition**: The average number of AI suggestions that are accepted per review.

**Purpose**: Measures the practical value and relevance of AI suggestions.

**Current Average**: N/A (data collection in progress)

### 4. Common Rejection Reasons

**Definition**: The most frequently cited reasons for rejecting AI suggestions.

**Purpose**: Identifies specific areas where AI understanding can be improved.

**Current Top Reasons**: N/A (data collection in progress)

## Data Collection

### How Data is Collected

1. **Automatic Collection**: Each execution of the `review-and-merge` action collects:
   - Review outcome (approved/modified/rejected/needs_work)
   - Number of suggestions made
   - Number of suggestions accepted
   - Rejection reasons (if provided)

2. **Storage**: Metrics are stored in `metrics/review_metrics.json`

3. **Privacy**: All data is anonymized and respects the `DISABLE_TELEMETRY` setting

### How to Analyze Metrics

```bash
# Generate summary report
python scripts/calculate_acceptance_rate.py --metrics-file metrics/review_metrics.json

# Generate full quality report
python scripts/calculate_acceptance_rate.py --output report --time-period 7d

# Check if target acceptance rate is met
python scripts/calculate_acceptance_rate.py --target-rate 70
```

## Example Quality Report

```
# AI Review Quality Report (Last 7d)

## Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Acceptance Rate | 75% | >= 70% | ✅ |
| Total Reviews | 45 | >= 20 | ✅ |
| Avg Suggestions | 3.2 | N/A | - |

## Outcome Breakdown
- **Approved**: 25 (55.6%)
- **Modified**: 8 (17.8%)
- **Rejected**: 7 (15.6%)
- **Needs Work**: 5 (11.1%)

## Common Rejection Reasons
1. "Incorrect context understanding" (40%)
2. "Too aggressive changes" (30%)
3. "Missed edge case" (20%)

## Interpretation
Good - AI reviews are generally reliable (75% acceptance)
```

## Improving Acceptance Rate

### If Acceptance Rate is Low (< 70%)

1. **Analyze Rejection Reasons**: Look at the common rejection reasons to identify patterns
2. **Adjust Review Prompt**: Customize the review prompt template to be more conservative
3. **Increase LGTM Threshold**: Raise the confidence threshold for auto-approval
4. **Provide Context**: Ensure AI has enough context about the codebase
5. **Use Custom Rules**: Add project-specific rules to guide the AI

### If Acceptance Rate is High (>= 80%)

1. **Consider Lowering Threshold**: May be able to auto-approve more confidently
2. **Expand Scope**: Could review more types of changes
3. **Share Success**: Document success stories to help others adopt

## Privacy and Data Protection

### What We Collect

- **Review Outcome**: Whether the review was accepted/modified/rejected
- **Suggestion Counts**: Number of suggestions and acceptances
- **Rejection Reasons**: Categorical reasons for rejection (if provided)
- **Timestamp**: When the review occurred

### What We Don't Collect

- ❌ Code content
- ❌ Suggestion details
- ❌ Repository names (anonymized with SHA-256 hash)
- ❌ User identities
- ❌ Confidential information

### Opt-Out

To disable quality metrics collection:

```yaml
- uses: ./.github/actions/review-and-merge
  env:
    DISABLE_TELEMETRY: "true"
```

## Goals and Targets

### Short-term (1-3 months)

- [ ] Collect baseline metrics (minimum 50 reviews)
- [ ] Achieve >= 70% acceptance rate
- [ ] Document top 5 rejection reasons
- [ ] Create improvement plan if needed

### Medium-term (3-6 months)

- [ ] Increase acceptance rate to >= 75%
- [ ] Reduce common rejection reasons
- [ ] Implement feedback loops for improvement

### Long-term (6-12 months)

- [ ] Achieve >= 80% acceptance rate
- [ ] Publish case studies
- [ ] Share best practices with community

## Contributing

If you have ideas for improving our quality metrics or want to share your experience:

1. **Report Issues**: GitHub Issues with `quality-metrics` label
2. **Share Insights**: Discussions or PRs with analysis
3. **Suggest Improvements**: Propose new metrics or collection methods

## References

- [Main README](../README.md)
- [Telemetry Privacy Policy](telemetry.md)
- [Adoption Guide](../ADOPTION_GUIDE.md)

---

**Questions?** Please open an issue or start a discussion on GitHub.
