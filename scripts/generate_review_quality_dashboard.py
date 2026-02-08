#!/usr/bin/env python3
"""
Generate AI Review Quality Dashboard

This script analyzes review_metrics.json to generate a dashboard
showing AI review quality trends and patterns.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List


def load_metrics(metrics_file: Path) -> List[Dict[str, Any]]:
    """Load review metrics from JSON file."""
    if not metrics_file.exists():
        print(f"Error: Metrics file not found: {metrics_file}", file=sys.stderr)
        return []

    try:
        data = json.loads(metrics_file.read_text())
        return data if isinstance(data, list) else []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {metrics_file}: {e}", file=sys.stderr)
        return []


def calculate_acceptance_rate(metrics: List[Dict]) -> float:
    """Calculate overall acceptance rate."""
    if not metrics:
        return 0.0

    approved = sum(1 for m in metrics if m.get("outcome") == "approved")
    return (approved / len(metrics)) * 100 if metrics else 0.0


def group_by_week(metrics: List[Dict]) -> Dict[str, List[Dict]]:
    """Group metrics by week."""
    weekly = defaultdict(list)
    for m in metrics:
        timestamp = m.get("timestamp", "")
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                week_key = dt.strftime("%Y-%W")  # Year-Week
                weekly[week_key].append(m)
            except ValueError:
                continue
    return dict(sorted(weekly.items()))


def extract_rejection_reasons(metrics: List[Dict]) -> Counter:
    """Extract and count rejection reasons."""
    reasons = Counter()
    for m in metrics:
        if m.get("outcome") in ["rejected", "modified"]:
            for reason in m.get("rejection_reasons", []):
                reasons[reason] += 1
    return reasons


def categorize_suggestions(metrics: List[Dict]) -> Dict[str, int]:
    """Categorize suggestions by type (placeholder for future enhancement)."""
    # This would need to be populated from actual suggestion data
    # For now, return empty dict
    return {
        "security": 0,
        "performance": 0,
        "style": 0,
        "logic": 0,
    }


def calculate_confidence_correlation(metrics: List[Dict]) -> Dict[str, float]:
    """Calculate correlation between confidence and acceptance."""
    accepted_confidences = [m.get("confidence_score", 0) for m in metrics if m.get("outcome") == "approved"]
    rejected_confidences = [m.get("confidence_score", 0) for m in metrics if m.get("outcome") == "rejected"]

    avg_accepted = sum(accepted_confidences) / len(accepted_confidences) if accepted_confidences else 0.0
    avg_rejected = sum(rejected_confidences) / len(rejected_confidences) if rejected_confidences else 0.0

    return {
        "average_confidence_accepted": avg_accepted,
        "average_confidence_rejected": avg_rejected,
    }


def generate_markdown_dashboard(metrics: List[Dict]) -> str:
    """Generate a markdown dashboard from metrics."""
    if not metrics:
        return "# AI Review Quality Dashboard\n\n**No data available**\n"

    total_reviews = len(metrics)
    acceptance_rate = calculate_acceptance_rate(metrics)
    weekly_data = group_by_week(metrics)
    rejection_reasons = extract_rejection_reasons(metrics)
    correlation = calculate_confidence_correlation(metrics)

    md = "# AI Review Quality Dashboard\n\n"
    md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    md += f"**Total Reviews:** {total_reviews}\n"
    md += f"**Overall Acceptance Rate:** {acceptance_rate:.1f}%\n\n"

    # Acceptance rate trend
    md += "## Acceptance Rate Trend\n\n"
    md += "| Week | Reviews | Acceptance Rate |\n"
    md += "|------|---------|----------------|\n"
    for week, week_metrics in weekly_data.items():
        week_rate = calculate_acceptance_rate(week_metrics)
        md += f"| {week} | {len(week_metrics)} | {week_rate:.1f}% |\n"
    md += "\n"

    # Rejection reasons
    if rejection_reasons:
        md += "## Top Rejection Reasons\n\n"
        for reason, count in rejection_reasons.most_common(5):
            percentage = (count / total_reviews) * 100
            md += f"{count + 1}. **{reason}** ({percentage:.0f}%)\n"
        md += "\n"

    # Confidence correlation
    if correlation["average_confidence_accepted"] > 0 or correlation["average_confidence_rejected"] > 0:
        md += "## Confidence Score Analysis\n\n"
        md += f"- **Average confidence (accepted):** {correlation['average_confidence_accepted']:.2f}\n"
        md += f"- **Average confidence (rejected):** {correlation['average_confidence_rejected']:.2f}\n"
        md += "\n"

    # Interpretation
    md += "## Interpretation\n\n"
    if acceptance_rate >= 80:
        md += "✅ **Excellent**: AI review quality is high and consistently trusted.\n"
    elif acceptance_rate >= 70:
        md += "✅ **Good**: AI review quality meets target (70%+).\n"
    elif acceptance_rate >= 60:
        md += "⚠️ **Moderate**: AI review quality is acceptable but needs improvement.\n"
    else:
        md += "❌ **Poor**: AI review quality needs significant improvement.\n"

    if weekly_data and len(weekly_data) > 1:
        recent_rate = calculate_acceptance_rate(weekly_data[list(weekly_data.keys())[-1]])
        if recent_rate > acceptance_rate:
            md += "\n📈 **Trend**: Acceptance rate is improving.\n"
        elif recent_rate < acceptance_rate:
            md += "\n📉 **Trend**: Acceptance rate is declining.\n"
        else:
            md += "\n➡️ **Trend**: Acceptance rate is stable.\n"

    md += "\n## Recommendations\n\n"

    if acceptance_rate < 70:
        md += "- **Priority**: Improve prompt template to reduce false positives\n"
        md += "- **Action**: Analyze rejection reasons to identify patterns\n"
    elif rejection_reasons and "Low quality suggestions" in rejection_reasons:
        md += "- **Priority**: Address low-quality suggestions\n"
        md += "- **Action**: Add more context to review prompts\n"
    else:
        md += "- Continue monitoring trends\n"
        md += "- Consider A/B testing prompt variations\n"

    return md


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI Review Quality Dashboard"
    )
    parser.add_argument(
        "--metrics",
        type=Path,
        default=Path("metrics/review_metrics.json"),
        help="Path to review_metrics.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("metrics/review_quality_dashboard.md"),
        help="Output dashboard file",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format",
    )

    args = parser.parse_args()

    # Load metrics
    metrics = load_metrics(args.metrics)
    if not metrics:
        print(f"Warning: No metrics found in {args.metrics}", file=sys.stderr)
        # Still create an empty dashboard

    # Generate dashboard
    if args.format == "markdown":
        output = generate_markdown_dashboard(metrics)
    else:
        output = json.dumps(metrics, indent=2)

    # Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output)
    print(f"Dashboard generated: {args.output}")

    # Print summary
    if metrics:
        rate = calculate_acceptance_rate(metrics)
        print(f"Acceptance rate: {rate:.1f}% ({len(metrics)} reviews)")
        if rate >= 70:
            print("✅ Target achieved (70%+)")
        else:
            print(f"⚠️ Below target (70%): Gap: {70 - rate:.1f}%")

    return 0


if __name__ == "__main__":
    sys.exit(main())
