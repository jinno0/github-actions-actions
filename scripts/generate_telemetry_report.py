#!/usr/bin/env python3
"""
Generate telemetry report from collected metrics.

This script reads telemetry.log and generates a weekly report showing
usage patterns, success rates, and error trends.

Usage:
    python scripts/generate_telemetry_report.py [--days N] [--input PATH] [--output PATH]

Arguments:
    --days: Number of days to include (default: 7, use 0 for all-time)
    --input: Path to telemetry.log file (default: metrics/telemetry/telemetry.log)
    --output: Output report path (default: docs/telemetry_report.md)

Environment Variables:
    TELEMETRY_DATA_PATH: Override default input path
    OUTPUT_PATH: Override default output path

Data Source:
    Reads from metrics/telemetry/telemetry.log (newline-delimited JSON)
"""
import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path


def load_telemetry_data(data_path: Path) -> list[dict]:
    """
    Load telemetry data from log file.

    Args:
        data_path: Path to telemetry.log file

    Returns:
        List of telemetry event dictionaries
    """
    if not data_path.exists():
        print(f"Warning: Telemetry data file not found: {data_path}")
        return []

    events = []
    failed_lines = 0

    try:
        with open(data_path) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    events.append(event)
                except json.JSONDecodeError as e:
                    failed_lines += 1
                    if failed_lines <= 5:  # Limit error output
                        print(f"Warning: Failed to parse line {line_num}: {e}")
                    continue

        if failed_lines > 5:
            print(f"Warning: {failed_lines} total lines failed to parse")

    except OSError as e:
        print(f"Error: Could not read telemetry file: {e}")
        return []

    return events


def filter_events_by_period(events: list[dict], days: int) -> list[dict]:
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

    cutoff = datetime.now(UTC) - timedelta(days=days)
    filtered = []

    for event in events:
        try:
            timestamp_str = event.get("timestamp", "")
            # Handle both 'Z' and '+00:00' timezone formats
            timestamp_str = timestamp_str.replace('Z', '+00:00')
            timestamp = datetime.fromisoformat(timestamp_str)
            if timestamp > cutoff:
                filtered.append(event)
        except (KeyError, ValueError):
            # Include events with invalid timestamps
            filtered.append(event)

    return filtered


def aggregate_metrics(events: list[dict]) -> dict[str, dict]:
    """
    Aggregate metrics from telemetry events.

    Args:
        events: List of telemetry events

    Returns:
        Dictionary mapping action names to aggregated statistics
    """
    metrics = defaultdict(lambda: {
        "total_runs": 0,
        "successes": 0,
        "failures": 0,
        "errors": []
    })

    for event in events:
        action_name = event.get("action_name", "unknown")
        metrics[action_name]["total_runs"] += 1

        if event.get("status") == "success":
            metrics[action_name]["successes"] += 1
        else:
            metrics[action_name]["failures"] += 1
            if "error_type" in event:
                metrics[action_name]["errors"].append(event["error_type"])

    return dict(metrics)


def generate_report(metrics: dict[str, dict], period_days: int) -> str:
    """
    Generate markdown telemetry report.

    Args:
        metrics: Aggregated metrics by action
        period_days: Number of days included in report

    Returns:
        Markdown formatted report
    """
    period_desc = "all time" if period_days == 0 else f"last {period_days} days"

    report = f"""# AI Actions Telemetry Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
**Period**: {period_desc}

---

## Executive Summary

"""

    # Calculate summary statistics
    total_runs = sum(m["total_runs"] for m in metrics.values())
    total_successes = sum(m["successes"] for m in metrics.values())
    overall_success_rate = (total_successes / total_runs * 100) if total_runs > 0 else 0

    # Add status indicator
    if overall_success_rate >= 95:
        status_emoji = "✅"
        status_text = "Excellent"
    elif overall_success_rate >= 80:
        status_emoji = "🟢"
        status_text = "Good"
    elif overall_success_rate >= 60:
        status_emoji = "⚠️"
        status_text = "Fair"
    else:
        status_emoji = "🔴"
        status_text = "Poor"

    report += f"{status_emoji} **Overall Status**: {status_text} ({overall_success_rate:.1f}% success rate)\n\n"
    report += "| Metric | Value |\n"
    report += "|--------|-------|\n"
    report += f"| **Total Runs** | {total_runs} |\n"
    report += f"| **Overall Success Rate** | {overall_success_rate:.1f}% |\n"
    report += f"| **Unique Actions** | {len(metrics)} |\n\n"

    if total_runs == 0:
        report += """## No Data Available

No telemetry data was found for the selected period. This could mean:

- Telemetry collection hasn't started yet
- No Actions have been executed
- Telemetry is disabled (`DISABLE_TELEMETRY=true`)
- Data is outside the selected time period

To generate telemetry data, run any GitHub Action in this repository.
"""
        return report

    # Per-Action Breakdown
    report += """---

## Per-Action Breakdown

"""

    for action_name, data in sorted(metrics.items(), key=lambda x: x[1]["total_runs"], reverse=True):
        if data["total_runs"] == 0:
            continue

        success_rate = (data["successes"] / data["total_runs"] * 100)
        report += f"### {action_name}\n\n"
        report += "| Metric | Value |\n"
        report += "|--------|-------|\n"
        report += f"| **Runs** | {data['total_runs']} |\n"
        report += f"| **Success Rate** | {success_rate:.1f}% |\n"
        report += f"| **Successes** | {data['successes']} |\n"
        report += f"| **Failures** | {data['failures']} |\n"

        # Add error summary if there are errors
        if data["errors"]:
            report += "\n#### Common Errors\n\n"
            # Count error occurrences
            error_counts = defaultdict(int)
            for error in data["errors"]:
                # Truncate long errors for display
                error_short = error[:80] + "..." if len(error) > 80 else error
                error_counts[error_short] += 1

            # Show top 5 errors
            for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                report += f"- {error} ({count}x)\n"

        report += "\n"

    # Add privacy notice
    report += """---

## Privacy Notice

This report is generated from anonymous telemetry data. Key privacy features:

- **Repository Anonymization**: All repository names are SHA-256 hashed (first 16 characters)
- **No Identifiable Information**: No personal data, code snippets, or credentials collected
- **Opt-Out Available**: Users can disable telemetry by setting `DISABLE_TELEMETRY=true`
- **Local Storage**: All data is stored locally in `metrics/telemetry/telemetry.log`

**Data Limitations**:
- Actual usage may be higher (some users disable telemetry)
- Data is voluntarily collected and may not represent all usage
- Only includes Actions that have implemented the telemetry collection script

For more information, see [docs/telemetry.md](../docs/telemetry.md).

---

## How to Regenerate

To regenerate this report with different parameters:

```bash
# Default: Last 7 days
python scripts/generate_telemetry_report.py

# Custom time period (last 30 days)
python scripts/generate_telemetry_report.py --days 30

# All historical data
python scripts/generate_telemetry_report.py --days 0

# Custom input/output paths
python scripts/generate_telemetry_report.py \\
    --input metrics/telemetry/telemetry.log \\
    --output custom_report.md
```
"""

    return report


def main() -> int:
    """Main entry point."""
    # Get environment variable overrides
    default_input = Path(os.getenv("TELEMETRY_DATA_PATH", "metrics/telemetry/telemetry.log"))
    default_output = Path(os.getenv("OUTPUT_PATH", "docs/telemetry_report.md"))

    parser = argparse.ArgumentParser(
        description="Generate weekly telemetry report from collected metrics",
        epilog=__doc__
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to include in report (default: 7, use 0 for all-time)"
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input,
        help="Path to telemetry.log file (default: metrics/telemetry/telemetry.log)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output,
        help="Output report path (default: docs/telemetry_report.md)"
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Load and filter events
    all_events = load_telemetry_data(args.input)
    events = filter_events_by_period(all_events, args.days) if args.days > 0 else all_events

    # Aggregate and generate report
    metrics = aggregate_metrics(events)
    report = generate_report(metrics, args.days)

    # Write report
    args.output.write_text(report)
    print(f"Report generated: {args.output}")
    print(f"  Events processed: {len(events)}")
    print(f"  Period: {args.days} days")

    return 0


if __name__ == "__main__":
    sys.exit(main())
