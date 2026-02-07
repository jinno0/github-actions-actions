#!/usr/bin/env python3
"""
Generate adoption metrics report from telemetry data.

This script analyzes telemetry.log and generates a summary report showing
adoption metrics (unique repositories, action usage breakdown) while
preserving privacy (all repo IDs are SHA-256 hashes).

Usage:
    python scripts/generate_adoption_report.py [--telemetry-data PATH] [--output PATH]

Environment Variables:
    TELEMETRY_DATA_PATH: Path to telemetry.log file (default: metrics/telemetry/telemetry.log)
    OUTPUT_PATH: Path for generated report (default: metrics/ADOPTION_REPORT.md)
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path


def load_telemetry_data(data_path: Path) -> list:
    """
    Load telemetry data from log file.

    Args:
        data_path: Path to telemetry.log file

    Returns:
        List of telemetry event dictionaries
    """
    if not data_path.exists():
        return []

    events = []
    with open(data_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                events.append(event)
            except json.JSONDecodeError:
                # Skip malformed lines
                continue

    return events


def filter_events_by_period(events: list, days: int) -> list:
    """
    Filter events by time period.

    Args:
        events: List of telemetry events
        days: Number of days to look back (0 = all time)

    Returns:
        Filtered list of events
    """
    if days == 0:
        return events

    cutoff = datetime.now().replace(tzinfo=None) - timedelta(days=days)
    filtered = []

    for event in events:
        try:
            timestamp = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00'))
            # Convert to naive datetime for comparison
            timestamp_naive = timestamp.replace(tzinfo=None)
            if timestamp_naive > cutoff:
                filtered.append(event)
        except (KeyError, ValueError):
            # Skip events with invalid timestamps
            continue

    return filtered


def calculate_unique_repos(events: list) -> int:
    """
    Calculate number of unique repositories.

    Args:
        events: List of telemetry events

    Returns:
        Number of unique repository_anonymous_id values
    """
    repo_ids = set()
    for event in events:
        repo_id = event.get("repository_anonymous_id")
        if repo_id and repo_id != "unknown":
            repo_ids.add(repo_id)

    return len(repo_ids)


def calculate_action_usage(events: list) -> dict:
    """
    Calculate action usage breakdown.

    Args:
        events: List of telemetry events

    Returns:
        Dictionary mapping action names to number of unique repositories
    """
    action_repos = defaultdict(set)

    for event in events:
        action = event.get("action_name")
        repo_id = event.get("repository_anonymous_id")
        if action and repo_id and repo_id != "unknown":
            action_repos[action].add(repo_id)

    # Convert sets to counts
    return {action: len(repos) for action, repos in action_repos.items()}


def calculate_success_rate(events: list) -> dict:
    """
    Calculate success rate by action.

    Args:
        events: List of telemetry events

    Returns:
        Dictionary mapping action names to success rates (0-100)
    """
    action_stats = defaultdict(lambda: {"success": 0, "total": 0})

    for event in events:
        action = event.get("action_name")
        status = event.get("status")
        if action and status:
            action_stats[action]["total"] += 1
            if status == "success":
                action_stats[action]["success"] += 1

    # Calculate percentages
    return {
        action: round((stats["success"] / stats["total"] * 100), 1) if stats["total"] > 0 else 0
        for action, stats in action_stats.items()
    }


def generate_report(
    all_events: list,
    events_30d: list,
    events_7d: list,
    output_path: Path
) -> None:
    """
    Generate adoption metrics report in Markdown format.

    Args:
        all_events: All telemetry events
        events_30d: Events from last 30 days
        events_7d: Events from last 7 days
        output_path: Path to write report
    """
    # Calculate metrics
    unique_repos_all = calculate_unique_repos(all_events)
    unique_repos_30d = calculate_unique_repos(events_30d)
    unique_repos_7d = calculate_unique_repos(events_7d)

    action_usage_all = calculate_action_usage(all_events)
    action_usage_30d = calculate_action_usage(events_30d)

    success_rates_all = calculate_success_rate(all_events)

    # Total executions
    total_executions_all = len(all_events)
    total_executions_30d = len(events_30d)

    # Generate report
    report = f"""# Adoption Metrics Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
**Data Source**: metrics/telemetry/telemetry.log

---

## Executive Summary

| Metric | All Time | Last 30 Days | Last 7 Days |
|--------|----------|--------------|-------------|
| **Unique Repositories** | {unique_repos_all} | {unique_repos_30d} | {unique_repos_7d} |
| **Total Executions** | {total_executions_all} | {total_executions_30d} | {len(events_7d)} |

---

## Unique Repositories Over Time

This table shows how many unique repositories (anonymized) have used these Actions.

| Period | Unique Repositories |
|--------|-------------------|
| Last 7 days | {unique_repos_7d} |
| Last 30 days | {unique_repos_30d} |
| All time | {unique_repos_all} |

**Note**: Repository names are SHA-256 hashed (first 16 characters) for privacy.

---

## Action Usage Breakdown (All Time)

Number of unique repositories that have used each Action.

| Action | Repos Using | % of Total |
|--------|-------------|------------|
"""

    # Add action usage table (sorted by count)
    if action_usage_all:
        total_repos = sum(action_usage_all.values())
        sorted_actions = sorted(action_usage_all.items(), key=lambda x: -x[1])

        for action, count in sorted_actions:
            percentage = round((count / total_repos * 100), 1) if total_repos > 0 else 0
            report += f"| `{action}` | {count} | {percentage}% |\n"
    else:
        report += "| _No data yet_ | - | - |\n"

    report += """

---

## Action Usage Breakdown (Last 30 Days)

Recent adoption trends.

| Action | Repos Using | % of Total |
|--------|-------------|------------|
"""

    if action_usage_30d:
        total_repos_30d = sum(action_usage_30d.values())
        sorted_actions_30d = sorted(action_usage_30d.items(), key=lambda x: -x[1])

        for action, count in sorted_actions_30d:
            percentage = round((count / total_repos_30d * 100), 1) if total_repos_30d > 0 else 0
            report += f"| `{action}` | {count} | {percentage}% |\n"
    else:
        report += "| _No data yet_ | - | - |\n"

    report += """

---

## Success Rates (All Time)

Percentage of successful executions by Action.

| Action | Success Rate | Total Executions |
|--------|--------------|------------------|
"""

    if success_rates_all:
        # Get execution counts
        action_counts = defaultdict(int)
        for event in all_events:
            action = event.get("action_name")
            if action:
                action_counts[action] += 1

        sorted_rates = sorted(success_rates_all.items(), key=lambda x: -x[1])

        for action, rate in sorted_rates:
            total = action_counts.get(action, 0)
            report += f"| `{action}` | {rate}% | {total} |\n"
    else:
        report += "| _No data yet_ | - | - |\n"

    report += """

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
python scripts/generate_adoption_report.py \\
    --telemetry-data /path/to/telemetry.log \\
    --output /path/to/ADOPTION_REPORT.md
```

---

*This report is auto-generated. Do not edit manually.*
"""

    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)

    print(f"✅ Adoption report generated: {output_path}")
    print(f"   - Unique repos (all time): {unique_repos_all}")
    print(f"   - Unique repos (30 days): {unique_repos_30d}")
    print(f"   - Total actions tracked: {len(action_usage_all)}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate adoption metrics report from telemetry data"
    )
    parser.add_argument(
        "--telemetry-data",
        type=Path,
        default=Path("metrics/telemetry/telemetry.log"),
        help="Path to telemetry.log file"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("metrics/ADOPTION_REPORT.md"),
        help="Path for generated report"
    )

    args = parser.parse_args()

    # Load telemetry data
    print(f"Loading telemetry data from: {args.telemetry_data}")
    all_events = load_telemetry_data(args.telemetry_data)

    if not all_events:
        print("⚠️  Warning: No telemetry data found. Report will show zeros.")
        print(f"   Expected file: {args.telemetry_data}")
        print("   Telemetry collection may be disabled or not yet used.")

    # Filter by time periods
    events_30d = filter_events_by_period(all_events, days=30)
    events_7d = filter_events_by_period(all_events, days=7)

    # Generate report
    generate_report(all_events, events_30d, events_7d, args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
