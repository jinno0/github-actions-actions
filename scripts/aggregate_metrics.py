#!/usr/bin/env python3
"""
Aggregate Acceptance Rate Metrics

This script collects and aggregates acceptance rate metrics from GitHub Actions
workflow runs. It reads metrics stored in JSON files and generates summary reports.

Usage:
    python scripts/aggregate_metrics.py --since '7 days ago' --output metrics/acceptance_rate.json
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


def find_metrics_files(
    root_dir: str = ".", since: Optional[datetime] = None
) -> List[str]:
    """
    Find all metrics JSON files in the repository.

    Args:
        root_dir: Root directory to search
        since: Only include files modified after this datetime

    Returns:
        List of file paths containing metrics
    """
    metrics_files = []

    # Search in common locations where actions might store metrics
    search_paths = [
        Path(root_dir) / "metrics",
        Path(root_dir) / ".metrics",
        Path(root_dir) / ".audit" / "metrics",
    ]

    for search_path in search_paths:
        if not search_path.exists():
            continue

        for file_path in search_path.rglob("*.json"):
            # Filter by modification time if since is provided
            if since:
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mod_time < since:
                    continue

            metrics_files.append(str(file_path))

    return metrics_files


def load_metrics_data(file_paths: List[str]) -> List[Dict]:
    """
    Load metrics data from multiple JSON files.

    Args:
        file_paths: List of JSON file paths to load

    Returns:
        List of metric entries
    """
    all_metrics = []

    for file_path in file_paths:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

                # Handle both list and single object formats
                if isinstance(data, list):
                    all_metrics.extend(data)
                elif isinstance(data, dict):
                    all_metrics.append(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load {file_path}: {e}")

    return all_metrics


def aggregate_metrics(
    metrics_data: List[Dict], action_name: Optional[str] = None
) -> Dict:
    """
    Aggregate metrics by action.

    Args:
        metrics_data: List of metric entries
        action_name: Optional filter for specific action

    Returns:
        Aggregated metrics dictionary
    """
    aggregated = {}

    for entry in metrics_data:
        # Filter by action if specified
        if action_name and entry.get("action") != action_name:
            continue

        action = entry.get("action", "unknown")

        if action not in aggregated:
            aggregated[action] = {
                "suggestions_made": 0,
                "suggestions_accepted": 0,
                "suggestions_rejected": 0,
                "suggestions_modified": 0,
                "entries": 0,
                "first_seen": entry.get("timestamp"),
                "last_seen": entry.get("timestamp"),
            }

        # Aggregate metrics
        for key in ["suggestions_made", "suggestions_accepted", "suggestions_rejected", "suggestions_modified"]:
            if key in entry.get("metrics", {}):
                aggregated[action][key] += entry["metrics"][key]

        aggregated[action]["entries"] += 1

        # Update timestamps
        timestamp = entry.get("timestamp", "")
        if timestamp:
            if timestamp < aggregated[action]["first_seen"]:
                aggregated[action]["first_seen"] = timestamp
            if timestamp > aggregated[action]["last_seen"]:
                aggregated[action]["last_seen"] = timestamp

    # Calculate rates for each action
    for action in aggregated:
        total = aggregated[action]["suggestions_made"]
        if total > 0:
            aggregated[action]["acceptance_rate"] = (
                aggregated[action]["suggestions_accepted"] / total
            ) * 100
            aggregated[action]["rejection_rate"] = (
                aggregated[action]["suggestions_rejected"] / total
            ) * 100
            aggregated[action]["modification_rate"] = (
                aggregated[action]["suggestions_modified"] / total
            ) * 100
        else:
            aggregated[action]["acceptance_rate"] = 0.0
            aggregated[action]["rejection_rate"] = 0.0
            aggregated[action]["modification_rate"] = 0.0

    return aggregated


def calculate_overall_metrics(aggregated: Dict) -> Dict:
    """
    Calculate overall metrics across all actions.

    Args:
        aggregated: Aggregated metrics by action

    Returns:
        Overall metrics summary
    """
    overall = {
        "suggestions_made": 0,
        "suggestions_accepted": 0,
        "suggestions_rejected": 0,
        "suggestions_modified": 0,
        "actions_tracked": len(aggregated),
    }

    for action_metrics in aggregated.values():
        overall["suggestions_made"] += action_metrics["suggestions_made"]
        overall["suggestions_accepted"] += action_metrics["suggestions_accepted"]
        overall["suggestions_rejected"] += action_metrics["suggestions_rejected"]
        overall["suggestions_modified"] += action_metrics["suggestions_modified"]

    # Calculate overall rates
    total = overall["suggestions_made"]
    if total > 0:
        overall["acceptance_rate"] = (overall["suggestions_accepted"] / total) * 100
        overall["rejection_rate"] = (overall["suggestions_rejected"] / total) * 100
        overall["modification_rate"] = (
            overall["suggestions_modified"] / total
        ) * 100
    else:
        overall["acceptance_rate"] = 0.0
        overall["rejection_rate"] = 0.0
        overall["modification_rate"] = 0.0

    return overall


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate acceptance rate metrics from GitHub Actions"
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Time range for aggregation (e.g., '7 days ago', '1 hour ago')",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="metrics/acceptance_rate.json",
        help="Output file path for aggregated metrics",
    )
    parser.add_argument(
        "--action",
        type=str,
        help="Filter metrics for a specific action",
    )
    parser.add_argument(
        "--root-dir",
        type=str,
        default=".",
        help="Root directory to search for metrics files",
    )

    args = parser.parse_args()

    # Parse time range
    since = None
    if args.since:
        try:
            # Simple parsing for common formats
            if "days ago" in args.since:
                days = int(args.since.split()[0])
                since = datetime.now() - timedelta(days=days)
            elif "hours ago" in args.since:
                hours = int(args.since.split()[0])
                since = datetime.now() - timedelta(hours=hours)
            elif "minutes ago" in args.since:
                minutes = int(args.since.split()[0])
                since = datetime.now() - timedelta(minutes=minutes)
        except (ValueError, IndexError):
            print(f"Warning: Could not parse time range '{args.since}', ignoring")

    # Find and load metrics files
    print(f"Searching for metrics files in {args.root_dir}...")
    metrics_files = find_metrics_files(args.root_dir, since)
    print(f"Found {len(metrics_files)} metrics file(s)")

    if not metrics_files:
        print("No metrics files found. This is expected for initial setup.")
        print("Metrics will be collected as actions are used.")
        # Create empty output
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "time_range": args.since,
            "overall": {
                "suggestions_made": 0,
                "suggestions_accepted": 0,
                "suggestions_rejected": 0,
                "suggestions_modified": 0,
                "actions_tracked": 0,
                "acceptance_rate": 0.0,
            },
            "by_action": {},
            "note": "No metrics data available yet. Metrics will be collected as actions are used.",
        }
    else:
        # Load and aggregate metrics
        print("Loading metrics data...")
        metrics_data = load_metrics_data(metrics_files)
        print(f"Loaded {len(metrics_data)} metric entries")

        print("Aggregating metrics...")
        aggregated = aggregate_metrics(metrics_data, args.action)
        overall = calculate_overall_metrics(aggregated)

        output_data = {
            "timestamp": datetime.now().isoformat(),
            "time_range": args.since,
            "overall": overall,
            "by_action": aggregated,
        }

    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write output
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\nAggregated metrics saved to {output_path}")

    # Print summary
    if output_data["overall"]["suggestions_made"] > 0:
        print("\n=== Summary ===")
        print(f"Total suggestions: {output_data['overall']['suggestions_made']}")
        print(f"Acceptance rate: {output_data['overall']['acceptance_rate']:.2f}%")
        print(f"Rejection rate: {output_data['overall']['rejection_rate']:.2f}%")
        print(f"Modification rate: {output_data['overall']['modification_rate']:.2f}%")
        print(f"Actions tracked: {output_data['overall']['actions_tracked']}")
    else:
        print("\nNo metrics data available yet. Metrics will be collected as actions are used.")


if __name__ == "__main__":
    main()
