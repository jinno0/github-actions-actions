#!/usr/bin/env python3
"""
Acceptance Rate Calculator for AI Review Quality Metrics

This script calculates and analyzes acceptance rate metrics for the review-and-merge action,
providing insights into AI review quality and effectiveness.
"""

import json
import os
import sys
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any


def calculate_acceptance_rate(metrics: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Calculate acceptance rate from review metrics.

    Args:
        metrics: List of review outcome metrics

    Returns:
        Dictionary containing acceptance rate statistics
    """
    if not metrics:
        return {
            "acceptance_rate": 0.0,
            "total_reviews": 0,
            "outcome_breakdown": {},
            "interpretation": "No reviews to analyze"
        }

    total = len(metrics)

    # Count outcomes
    outcome_counts = defaultdict(int)
    for metric in metrics:
        outcome = metric.get("outcome", "unknown")
        outcome_counts[outcome] += 1

    # Calculate acceptance rate
    # Accepted = approved + modified (human made changes but ultimately accepted)
    accepted_count = (
        outcome_counts.get("approved", 0) +
        outcome_counts.get("modified", 0)
    )

    acceptance_rate = (accepted_count / total * 100) if total > 0 else 0.0

    # Calculate other statistics
    avg_suggestions = 0.0
    suggestions_data = [m.get("suggestions_count", 0) for m in metrics if m.get("suggestions_count")]
    if suggestions_data:
        avg_suggestions = sum(suggestions_data) / len(suggestions_data)

    avg_accepted = 0.0
    accepted_data = [m.get("accepted_count", 0) for m in metrics if m.get("accepted_count") is not None]
    if accepted_data:
        avg_accepted = sum(accepted_data) / len(accepted_data)

    # Get common rejection reasons
    rejection_reasons = []
    for metric in metrics:
        if metric.get("outcome") in ["rejected", "needs_work"]:
            reasons = metric.get("rejection_reasons", [])
            if isinstance(reasons, list):
                rejection_reasons.extend(reasons)
            elif reasons:
                rejection_reasons.append(reasons)

    common_rejections = get_common_items(rejection_reasons)

    return {
        "acceptance_rate": round(acceptance_rate, 2),
        "total_reviews": total,
        "outcome_breakdown": dict(outcome_counts),
        "average_suggestions": round(avg_suggestions, 2),
        "average_accepted_suggestions": round(avg_accepted, 2),
        "common_rejection_reasons": common_rejections,
        "interpretation": get_interpretation(acceptance_rate, total)
    }


def get_common_items(items: list[str], top_n: int = 5) -> list[dict[str, Any]]:
    """Get most common items from a list."""
    if not items:
        return []

    from collections import Counter
    counter = Counter(items)

    return [
        {"reason": reason, "count": count, "percentage": round(count / len(items) * 100, 1)}
        for reason, count in counter.most_common(top_n)
    ]


def get_interpretation(acceptance_rate: float, total_reviews: int) -> str:
    """Provide human-readable interpretation of acceptance rate."""
    if total_reviews < 10:
        return f"Insufficient data for reliable analysis ({total_reviews} reviews)"

    if acceptance_rate >= 80:
        return f"Excellent - AI reviews are highly reliable ({acceptance_rate}% acceptance)"
    elif acceptance_rate >= 70:
        return f"Good - AI reviews are generally reliable ({acceptance_rate}% acceptance)"
    elif acceptance_rate >= 50:
        return f"Moderate - AI reviews need improvement ({acceptance_rate}% acceptance)"
    else:
        return f"Poor - AI review quality needs significant improvement ({acceptance_rate}% acceptance)"


def load_metrics_from_file(filepath: str) -> list[dict[str, Any]]:
    """Load metrics from a JSON file."""
    try:
        with open(filepath, encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def filter_metrics_by_time(
    metrics: list[dict[str, Any]],
    time_period: str = "7d"
) -> list[dict[str, Any]]:
    """Filter metrics by time period."""
    if not metrics:
        return []

    # Parse time period (e.g., "7d", "24h", "1w")
    now = datetime.now(UTC)

    if time_period.endswith('d'):
        days = int(time_period[:-1])
        cutoff = now - timedelta(days=days)
    elif time_period.endswith('h'):
        hours = int(time_period[:-1])
        cutoff = now - timedelta(hours=hours)
    elif time_period.endswith('w'):
        weeks = int(time_period[:-1])
        cutoff = now - timedelta(weeks=weeks)
    else:
        # Default to 7 days
        cutoff = now - timedelta(days=7)

    # Filter metrics by timestamp
    filtered = []
    for metric in metrics:
        timestamp_str = metric.get("timestamp")
        if not timestamp_str:
            # Include metrics without timestamps
            filtered.append(metric)
        else:
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                # Both timestamps are timezone-aware - direct comparison
                if timestamp >= cutoff:
                    filtered.append(metric)
            except (ValueError, AttributeError):
                # Skip metrics with invalid timestamps
                pass

    return filtered


def generate_quality_report(metrics: list[dict[str, Any]], time_period: str = "7d") -> str:
    """Generate a human-readable quality report."""
    filtered = filter_metrics_by_time(metrics, time_period)
    stats = calculate_acceptance_rate(filtered)

    report = []
    report.append(f"# AI Review Quality Report (Last {time_period})")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append("| Metric | Value | Target | Status |")
    report.append("|--------|-------|--------|--------|")

    acceptance_rate = stats["acceptance_rate"]
    target = 70
    status = "✅" if acceptance_rate >= target else "⚠️"
    report.append(f"| Acceptance Rate | {acceptance_rate}% | >= {target}% | {status} |")

    total = stats["total_reviews"]
    target_min = 20
    status = "✅" if total >= target_min else "⚠️"
    report.append(f"| Total Reviews | {total} | >= {target_min} | {status} |")

    avg_suggestions = stats.get("average_suggestions", 0)
    report.append(f"| Avg Suggestions | {avg_suggestions} | N/A | - |")

    report.append("")
    report.append("## Outcome Breakdown")

    breakdown = stats.get("outcome_breakdown", {})
    if breakdown:
        for outcome, count in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            report.append(f"- **{outcome.title()}**: {count} ({percentage:.1f}%)")

    report.append("")

    common_rejections = stats.get("common_rejection_reasons", [])
    if common_rejections:
        report.append("## Common Rejection Reasons")
        report.append("")
        for item in common_rejections:
            report.append(f"{item['count']}. \"{item['reason']}\" ({item['percentage']}%)")
        report.append("")

    interpretation = stats.get("interpretation", "")
    report.append("## Interpretation")
    report.append("")
    report.append(interpretation)

    return "\n".join(report)


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate acceptance rate for AI review quality metrics"
    )
    parser.add_argument(
        "--metrics-file",
        default="metrics/review_metrics.json",
        help="Path to metrics JSON file"
    )
    parser.add_argument(
        "--time-period",
        default="7d",
        help="Time period to analyze (e.g., 7d, 24h, 1w)"
    )
    parser.add_argument(
        "--output",
        choices=["json", "report", "summary"],
        default="summary",
        help="Output format"
    )
    parser.add_argument(
        "--target-rate",
        type=float,
        default=70.0,
        help="Target acceptance rate (default: 70%%)"
    )

    args = parser.parse_args()

    # Respect privacy settings - check if telemetry is disabled
    if os.getenv("DISABLE_TELEMETRY", "").lower() == "true":
        print("Quality metrics analysis is disabled via DISABLE_TELEMETRY environment variable.", file=sys.stderr)
        return 0

    # Load metrics
    metrics = load_metrics_from_file(args.metrics_file)

    # Filter by time period
    filtered = filter_metrics_by_time(metrics, args.time_period)

    # Calculate statistics
    stats = calculate_acceptance_rate(filtered)

    # Add target comparison
    stats["target_acceptance_rate"] = args.target_rate
    stats["meets_target"] = stats["acceptance_rate"] >= args.target_rate

    # Output results
    if args.output == "json":
        print(json.dumps(stats, indent=2))
    elif args.output == "report":
        print(generate_quality_report(metrics, args.time_period))
    else:  # summary
        print(f"Acceptance Rate: {stats['acceptance_rate']}%")
        print(f"Total Reviews: {stats['total_reviews']}")
        print(f"Target: {args.target_rate}%")
        print(f"Status: {'✅ PASS' if stats['meets_target'] else '⚠️  BELOW TARGET'}")
        if stats.get("outcome_breakdown"):
            print("\nOutcome Breakdown:")
            for outcome, count in stats["outcome_breakdown"].items():
                print(f"  {outcome}: {count}")

    return 0 if stats.get("meets_target", False) else 1


if __name__ == "__main__":
    sys.exit(main())
