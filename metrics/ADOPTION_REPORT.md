# Adoption Metrics Report

**Generated**: 2026-02-22 02:10:53 UTC
**Data Source**: metrics/telemetry/telemetry.log

---

## Executive Summary

| Metric | All Time | Last 30 Days | Last 7 Days |
|--------|----------|--------------|-------------|
| **Unique Repositories** | 0 | 0 | 0 |
| **Total Executions** | 0 | 0 | 0 |

---

## Unique Repositories Over Time

This table shows how many unique repositories (anonymized) have used these Actions.

| Period | Unique Repositories |
|--------|-------------------|
| Last 7 days | 0 |
| Last 30 days | 0 |
| All time | 0 |

**Note**: Repository names are SHA-256 hashed (first 16 characters) for privacy.

---

## Action Usage Breakdown (All Time)

Number of unique repositories that have used each Action.

| Action | Repos Using | % of Total |
|--------|-------------|------------|
| _No data yet_ | - | - |


---

## Action Usage Breakdown (Last 30 Days)

Recent adoption trends.

| Action | Repos Using | % of Total |
|--------|-------------|------------|
| _No data yet_ | - | - |


---

## Success Rates (All Time)

Percentage of successful executions by Action.

| Action | Success Rate | Total Executions |
|--------|--------------|------------------|
| _No data yet_ | - | - |


---

## Privacy Notice

This report is generated from anonymous telemetry data. Key privacy features:

- **Repository Anonymization**: All repository names are SHA-256 hashed (first 16 characters)
- **No Identifiable Information**: No personal data, code snippets, or credentials collected
- **Opt-Out Available**: Users can disable telemetry by setting `DISABLE_TELEMETRY=true`
- **Small Organizations Excluded**: Aggregation excludes very small samples to prevent inference

**Data Limitations**:
- Actual adoption may be higher (some users disable telemetry)
- "Unique repositories" counts anonymous hashes, not actual repository names
- Data is voluntarily collected and may not represent all usage

---

## Methodology

### Unique Repository Definition
A unique repository is identified by its `repository_anonymous_id` field (SHA-256 hash).

### Active Definition
An "active" repository is one that has triggered any action in the specified time period.

### Data Source
Anonymous telemetry collected by `scripts/collect_metrics.py` and stored in `metrics/telemetry/telemetry.log`.

---

## How to Regenerate

To regenerate this report with the latest data:

```bash
python scripts/generate_adoption_report.py
```

With custom paths:

```bash
python scripts/generate_adoption_report.py \
    --telemetry-data /path/to/telemetry.log \
    --output /path/to/ADOPTION_REPORT.md
```

---

*This report is auto-generated. Do not edit manually.*
