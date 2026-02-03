#!/usr/bin/env python3
"""
Generate telemetry report from collected metrics
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def load_metrics(metrics_dir: Path) -> dict:
    """Load metrics from JSON files"""
    metrics = defaultdict(lambda: {
        "total_runs": 0,
        "successes": 0,
        "failures": 0,
        "errors": []
    })

    if not metrics_dir.exists():
        return dict(metrics)

    for file in metrics_dir.glob("*.json"):
        try:
            data = json.loads(file.read_text())
            action_name = data.get("action_name", "unknown")
            metrics[action_name]["total_runs"] += 1
            if data.get("status") == "success":
                metrics[action_name]["successes"] += 1
            else:
                metrics[action_name]["failures"] += 1
                if "error" in data:
                    metrics[action_name]["errors"].append(data["error"])
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to parse {file}: {e}")
            continue

    return dict(metrics)

def generate_report(metrics: dict) -> str:
    """Generate markdown report"""
    report = ["# AI Actions Telemetry Report\n"]
    report.append(f"Generated: {datetime.now().isoformat()}\n\n")

    # Summary
    total_runs = sum(m["total_runs"] for m in metrics.values())
    total_successes = sum(m["successes"] for m in metrics.values())
    overall_success_rate = (total_successes / total_runs * 100) if total_runs > 0 else 0

    report.append("## Summary\n")
    report.append(f"- Total Runs: {total_runs}\n")
    report.append(f"- Overall Success Rate: {overall_success_rate:.1f}%\n\n")

    # Per-Action Breakdown
    report.append("## Per-Action Breakdown\n\n")
    for action_name, data in sorted(metrics.items(), key=lambda x: x[1]["total_runs"], reverse=True):
        if data["total_runs"] == 0:
            continue
        success_rate = (data["successes"] / data["total_runs"] * 100)
        report.append(f"### {action_name}\n")
        report.append(f"- Runs: {data['total_runs']}\n")
        report.append(f"- Success Rate: {success_rate:.1f}%\n")
        if data["failures"] > 0:
            report.append(f"- Failures: {data['failures']}\n")
        report.append("\n")

    return "".join(report)

if __name__ == "__main__":
    metrics_dir = Path("metrics")
    output_file = Path("docs/telemetry_report.md")

    # Create docs directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    metrics = load_metrics(metrics_dir)
    report = generate_report(metrics)

    output_file.write_text(report)
    print(f"Report generated: {output_file}")
