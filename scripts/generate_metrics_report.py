#!/usr/bin/env python3
"""
Generate Metrics Report

This script reads aggregated acceptance rate metrics and generates a
human-readable markdown report.

Usage:
    python scripts/generate_metrics_report.py --input metrics/acceptance_rate.json --output metrics/acceptance_report.md
"""

import argparse
import json
from pathlib import Path


def generate_markdown_report(metrics_data: dict) -> str:
    """
    Generate a markdown report from aggregated metrics.

    Args:
        metrics_data: Aggregated metrics dictionary

    Returns:
        Markdown formatted report
    """
    lines = []

    # Header
    lines.append("# Acceptance Rate Report")
    lines.append("")
    lines.append(f"**Generated:** {metrics_data.get('timestamp', 'Unknown')}")
    lines.append("")

    # Overall Summary
    lines.append("## Overall Summary")
    lines.append("")

    overall = metrics_data.get("overall", {})
    total = overall.get("suggestions_made", 0)

    if total > 0:
        lines.append(f"- **Total Suggestions:** {total}")
        lines.append(f"- **Accepted:** {overall.get('suggestions_accepted', 0)} ({overall.get('acceptance_rate', 0):.1f}%)")
        lines.append(f"- **Rejected:** {overall.get('suggestions_rejected', 0)} ({overall.get('rejection_rate', 0):.1f}%)")
        lines.append(f"- **Modified:** {overall.get('suggestions_modified', 0)} ({overall.get('modification_rate', 0):.1f}%)")
        lines.append(f"- **Actions Tracked:** {overall.get('actions_tracked', 0)}")
        lines.append("")

        # Status indicator
        acceptance_rate = overall.get('acceptance_rate', 0)
        if acceptance_rate >= 80:
            lines.append("### ✅ Status: Target Achieved")
            lines.append("")
            lines.append(f"Acceptance rate of {acceptance_rate:.1f}% meets or exceeds the 80% target (QA-001).")
        elif acceptance_rate >= 60:
            lines.append("### ⚠️ Status: Approaching Target")
            lines.append("")
            lines.append(f"Acceptance rate of {acceptance_rate:.1f}% is below the 80% target but shows positive trend.")
        else:
            lines.append("### 🔴 Status: Below Target")
            lines.append("")
            lines.append(f"Acceptance rate of {acceptance_rate:.1f}% is significantly below the 80% target.")
            lines.append("Consider reviewing suggestion quality and user feedback.")
    else:
        lines.append("### 📊 No Data Available")
        lines.append("")
        lines.append("No acceptance rate data has been collected yet.")
        lines.append("Metrics will be populated as actions are used.")
        lines.append("")
        lines.append("**Next Steps:**")
        lines.append("1. Ensure AI-powered actions are being used in workflows")
        lines.append("2. Verify that acceptance tracking is properly integrated")
        lines.append("3. Check back after actions have been executed")

    lines.append("")

    # Per-Action Breakdown
    by_action = metrics_data.get("by_action", {})

    if by_action:
        lines.append("## Per-Action Breakdown")
        lines.append("")

        # Sort by acceptance rate
        sorted_actions = sorted(
            by_action.items(),
            key=lambda x: x[1].get("acceptance_rate", 0),
            reverse=True
        )

        for action_name, action_metrics in sorted_actions:
            lines.append(f"### {action_name}")
            lines.append("")

            suggestions = action_metrics.get("suggestions_made", 0)
            acceptance_rate = action_metrics.get("acceptance_rate", 0)

            if suggestions > 0:
                # Status indicator
                if acceptance_rate >= 80:
                    status = "✅"
                elif acceptance_rate >= 60:
                    status = "⚠️"
                else:
                    status = "🔴"

                lines.append(f"{status} **Acceptance Rate:** {acceptance_rate:.1f}%")
                lines.append("")
                lines.append("| Metric | Count | Percentage |")
                lines.append("|--------|-------|------------|")
                lines.append(f"| Accepted | {action_metrics.get('suggestions_accepted', 0)} | {acceptance_rate:.1f}% |")
                lines.append(f"| Rejected | {action_metrics.get('suggestions_rejected', 0)} | {action_metrics.get('rejection_rate', 0):.1f}% |")
                lines.append(f"| Modified | {action_metrics.get('suggestions_modified', 0)} | {action_metrics.get('modification_rate', 0):.1f}% |")
                lines.append(f"| **Total** | **{suggestions}** | **100%** |")
                lines.append("")

                # Add trend indicator if we have enough data points
                entries = action_metrics.get("entries", 0)
                if entries > 1:
                    lines.append(f"*Data points: {entries}*")
                    lines.append("")

                # Timestamps
                first_seen = action_metrics.get("first_seen")
                last_seen = action_metrics.get("last_seen")
                if first_seen and last_seen:
                    lines.append(f"*First seen: {first_seen}*")
                    lines.append(f"*Last seen: {last_seen}*")
                    lines.append("")
            else:
                lines.append("No suggestions recorded yet.")
                lines.append("")

    # Insights and Recommendations
    if total > 0:
        lines.append("## Insights and Recommendations")
        lines.append("")

        # Identify best performing actions
        sorted_by_rate = sorted(
            by_action.items(),
            key=lambda x: x[1].get("acceptance_rate", 0),
            reverse=True
        )

        if sorted_by_rate:
            best_action, best_metrics = sorted_by_rate[0]
            lines.append("### 🏆 Best Performing Action")
            lines.append("")
            lines.append(f"**{best_action}:** {best_metrics.get('acceptance_rate', 0):.1f}% acceptance rate")
            lines.append("")
            lines.append("Consider analyzing what makes this action successful and applying those patterns to other actions.")

        # Identify actions needing improvement
        needs_improvement = [
            (name, metrics) for name, metrics in sorted_by_rate
            if metrics.get("suggestions_made", 0) > 0 and metrics.get("acceptance_rate", 0) < 60
        ]

        if needs_improvement:
            lines.append("")
            lines.append("### 🔧 Actions Needing Improvement")
            lines.append("")
            for action_name, action_metrics in needs_improvement:
                rate = action_metrics.get("acceptance_rate", 0)
                lines.append(f"- **{action_name}:** {rate:.1f}% acceptance rate")
            lines.append("")
            lines.append("Recommendations:")
            lines.append("1. Review suggestion quality and relevance")
            lines.append("2. Gather user feedback on rejected suggestions")
            lines.append("3. Consider adjusting suggestion parameters or prompts")
            lines.append("4. Implement custom rules to better match user preferences")

    # Footer
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*This report is generated automatically from acceptance rate tracking data.*")
    lines.append("")
    lines.append("**Target:** Acceptance Rate >= 80% (QA-001)")
    lines.append("")
    lines.append(f"*For raw data, see: {metrics_data.get('source_file', 'metrics/acceptance_rate.json')}*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate acceptance rate metrics report"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="metrics/acceptance_rate.json",
        help="Input metrics JSON file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="metrics/acceptance_report.md",
        help="Output markdown report file",
    )

    args = parser.parse_args()

    # Read input data
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found")
        return 1

    with open(input_path, "r") as f:
        metrics_data = json.load(f)

    # Add source file reference
    metrics_data["source_file"] = args.input

    # Generate report
    print("Generating metrics report...")
    report = generate_markdown_report(metrics_data)

    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write report
    with open(output_path, "w") as f:
        f.write(report)

    print(f"Report saved to {args.output}")
    print("")

    # Print preview
    if metrics_data.get("overall", {}).get("suggestions_made", 0) > 0:
        print("=== Preview ===")
        overall = metrics_data["overall"]
        print(f"Acceptance Rate: {overall.get('acceptance_rate', 0):.1f}%")
        print(f"Actions Tracked: {overall.get('actions_tracked', 0)}")
    else:
        print("No metrics data available yet")

    return 0


if __name__ == "__main__":
    exit(main())
