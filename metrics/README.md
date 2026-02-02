# Acceptance Rate Metrics

This directory contains acceptance rate tracking data and reports for AI-generated suggestions across GitHub Actions.

## Overview

Acceptance rate tracking measures the quality and effectiveness of AI suggestions by tracking:

- **Suggestions Made**: Total number of suggestions generated
- **Suggestions Accepted**: Number of suggestions accepted without modification
- **Suggestions Rejected**: Number of suggestions rejected
- **Suggestions Modified**: Number of suggestions accepted with modifications

## Target

The primary quality goal for MS-002 is:

> **QA-001: Acceptance Rate >= 80%**

This target is defined in `.audit/config/intent.yml`.

## Files

- `acceptance_rate.json` - Raw aggregated metrics data (JSON format)
- `acceptance_report.md` - Human-readable metrics report (Markdown format)
- `README.md` - This file

## Data Collection

Metrics are collected automatically through:

1. **Tracking Integration**: Each AI-powered action integrates acceptance tracking
2. **Daily Aggregation**: GitHub Workflow runs daily to aggregate metrics
3. **Report Generation**: Automated report generation with insights and recommendations

## Viewing Metrics

### Latest Report

The most recent acceptance rate report is available in:
```
metrics/acceptance_report.md
```

### Raw Data

For detailed analysis, see the raw metrics data:
```
metrics/acceptance_rate.json
```

## Actions Tracked

The following AI-powered actions have acceptance tracking integrated:

1. **review-and-merge** - Code review suggestions
2. **spec-to-code** - Code generation from specifications
3. **action-fixer** - Automated fix suggestions
4. **auto-refactor** - Refactoring suggestions

## Manual Metrics Generation

To manually generate metrics and reports:

```bash
# Aggregate metrics from the last 7 days
python scripts/aggregate_metrics.py --since '7 days ago' --output metrics/acceptance_rate.json

# Generate report from aggregated data
python scripts/generate_metrics_report.py --input metrics/acceptance_rate.json --output metrics/acceptance_report.md
```

## Understanding the Report

### Overall Summary

The report shows overall acceptance metrics across all tracked actions:

- **Total Suggestions**: Total number of AI suggestions generated
- **Acceptance Rate**: Percentage of suggestions accepted (target: >= 80%)
- **Rejection Rate**: Percentage of suggestions rejected
- **Modification Rate**: Percentage of suggestions modified before acceptance

### Status Indicators

- ✅ **Target Achieved**: Acceptance rate >= 80%
- ⚠️ **Approaching Target**: Acceptance rate between 60-79%
- 🔴 **Below Target**: Acceptance rate < 60%

### Per-Action Breakdown

Each action's performance is tracked individually to identify:
- Best performing actions (to replicate success patterns)
- Actions needing improvement (to focus quality improvements)
- Trends over time (with data point counts)

## Implementation Details

### AcceptanceTracker Class

The `AcceptanceTracker` class in `actions/lib/acceptance_tracker.py` provides:

```python
from actions.lib.acceptance_tracker import AcceptanceTracker

tracker = AcceptanceTracker("action-name")
tracker.record_suggestion("made")
tracker.record_suggestion("accepted")
rate = tracker.get_acceptance_rate()
```

### Integration Pattern

Actions integrate tracking using the following pattern:

```python
# After generating a suggestion
tracker.record_suggestion("made")

# After user accepts/rejects/modifies
tracker.record_suggestion("accepted")  # or "rejected" or "modified"

# Export and persist
tracker.export_metrics()
tracker.save_to_file("metrics/data.json")
```

## Workflow Automation

The `.github/workflows/aggregate-metrics.yml` workflow:

- Runs daily at midnight UTC
- Aggregates metrics from the last 7 days
- Generates acceptance rate report
- Commits report to repository
- Uploads metrics as artifacts (30-day retention)

## Quality Improvement

This metrics infrastructure enables:

1. **Data-Driven Decisions**: Base quality improvements on actual data
2. **Trend Analysis**: Track acceptance rate over time
3. **Problem Identification**: Identify actions with low acceptance rates
4. **Impact Measurement**: Validate that improvements actually increase acceptance
5. **Goal Validation**: Verify if 80% target (QA-001) is achievable (ASM-002)

## Related Documentation

- `.audit/config/intent.yml` - Quality attributes and targets
- `.audit/proposal/changes/PR-001.md` - Original PR proposal
- `actions/lib/acceptance_tracker.py` - Implementation details
- `tests/metrics/test_acceptance_tracker.py` - Test suite

## Next Steps

After metrics collection begins:

1. **Establish Baseline**: Wait 7 days for initial baseline
2. **Analyze Trends**: Review acceptance rate trends in reports
3. **Identify Improvements**: Use data to prioritize PR-004 (Review Quality)
4. **Validate Target**: Confirm if 80% target (QA-001) is achievable (ASM-002)
5. **Iterate**: Continuously improve based on metrics

## Questions?

For questions about acceptance rate tracking, see:

- Implementation: `actions/lib/acceptance_tracker.py`
- Tests: `tests/metrics/test_acceptance_tracker.py`
- Scripts: `scripts/aggregate_metrics.py`, `scripts/generate_metrics_report.py`
