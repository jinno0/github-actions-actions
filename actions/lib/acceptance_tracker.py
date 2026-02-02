"""
Acceptance Rate Tracking for AI Suggestions

This module provides tracking capabilities for measuring the quality and
effectiveness of AI-generated suggestions across GitHub Actions.

Tracks:
- Suggestions made
- Suggestions accepted
- Suggestions rejected
- Suggestions modified

Usage:
    tracker = AcceptanceTracker("review-and-merge")
    tracker.record_suggestion("made")
    tracker.record_suggestion("accepted")
    rate = tracker.get_acceptance_rate()
"""

from datetime import datetime
from typing import Dict, Literal, Optional
import json
import os


SuggestionOutcome = Literal["made", "accepted", "rejected", "modified"]


class AcceptanceTracker:
    """
    Tracks acceptance rate metrics for AI-generated suggestions.

    Attributes:
        action_name: Name of the GitHub Action being tracked
        metrics: Dictionary tracking suggestion outcomes
    """

    def __init__(self, action_name: str):
        """
        Initialize the acceptance tracker for a specific action.

        Args:
            action_name: Name of the GitHub Action (e.g., "review-and-merge")
        """
        self.action_name = action_name
        self.metrics = {
            "suggestions_made": 0,
            "suggestions_accepted": 0,
            "suggestions_rejected": 0,
            "suggestions_modified": 0,
        }

    def record_suggestion(self, outcome: SuggestionOutcome) -> None:
        """
        Record a suggestion outcome.

        Args:
            outcome: The outcome of the suggestion ("made", "accepted", "rejected", "modified")

        Raises:
            ValueError: If outcome is not one of the valid options
        """
        valid_outcomes = ["made", "accepted", "rejected", "modified"]
        if outcome not in valid_outcomes:
            raise ValueError(
                f"Invalid outcome '{outcome}'. Must be one of: {valid_outcomes}"
            )

        metric_key = f"suggestions_{outcome}"
        self.metrics[metric_key] += 1

    def get_acceptance_rate(self) -> float:
        """
        Calculate the acceptance rate as a percentage.

        Returns:
            Acceptance rate percentage (0.0 to 100.0)
            Returns 0.0 if no suggestions have been made
        """
        total = self.metrics["suggestions_made"]
        if total == 0:
            return 0.0
        return (self.metrics["suggestions_accepted"] / total) * 100

    def get_rejection_rate(self) -> float:
        """
        Calculate the rejection rate as a percentage.

        Returns:
            Rejection rate percentage (0.0 to 100.0)
            Returns 0.0 if no suggestions have been made
        """
        total = self.metrics["suggestions_made"]
        if total == 0:
            return 0.0
        return (self.metrics["suggestions_rejected"] / total) * 100

    def get_modification_rate(self) -> float:
        """
        Calculate the modification rate as a percentage.

        Returns:
            Modification rate percentage (0.0 to 100.0)
            Returns 0.0 if no suggestions have been made
        """
        total = self.metrics["suggestions_made"]
        if total == 0:
            return 0.0
        return (self.metrics["suggestions_modified"] / total) * 100

    def get_metrics(self) -> Dict[str, int]:
        """
        Get the current metrics dictionary.

        Returns:
            Dictionary with current metric values
        """
        return self.metrics.copy()

    def export_metrics(self) -> Dict:
        """
        Export metrics for reporting and aggregation.

        Returns:
            Dictionary containing action name, timestamp, metrics, and calculated rates
        """
        return {
            "action": self.action_name,
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics.copy(),
            "rates": {
                "acceptance_rate": self.get_acceptance_rate(),
                "rejection_rate": self.get_rejection_rate(),
                "modification_rate": self.get_modification_rate(),
            },
            "total_suggestions": self.metrics["suggestions_made"],
        }

    def save_to_file(self, filepath: str) -> None:
        """
        Save metrics to a JSON file for persistence.

        Args:
            filepath: Path to the JSON file where metrics will be saved
        """
        data = self.export_metrics()

        # Load existing data if file exists
        existing_data = []
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = []
                except json.JSONDecodeError:
                    existing_data = []

        # Append new data
        existing_data.append(data)

        # Write back to file
        with open(filepath, "w") as f:
            json.dump(existing_data, f, indent=2)

    def reset_metrics(self) -> None:
        """Reset all metrics to zero."""
        for key in self.metrics:
            self.metrics[key] = 0

    @classmethod
    def from_file(cls, action_name: str, filepath: str) -> "AcceptanceTracker":
        """
        Load or create a tracker from a JSON file.

        Args:
            action_name: Name of the GitHub Action
            filepath: Path to the JSON file with persisted metrics

        Returns:
            AcceptanceTracker instance with loaded metrics
        """
        tracker = cls(action_name)

        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list) and data:
                        # Sum up all metrics from the file
                        for entry in data:
                            if entry.get("action") == action_name:
                                for key, value in entry["metrics"].items():
                                    if key in tracker.metrics:
                                        tracker.metrics[key] += value
                except json.JSONDecodeError:
                    pass

        return tracker


def aggregate_metrics_by_action(
    metrics_data: list, action_name: Optional[str] = None
) -> Dict:
    """
    Aggregate metrics from multiple tracking entries.

    Args:
        metrics_data: List of metric entries from export_metrics()
        action_name: Optional filter for specific action

    Returns:
        Aggregated metrics dictionary
    """
    aggregated = {}

    for entry in metrics_data:
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
            }

        for key in aggregated[action]:
            if key == "entries":
                aggregated[action][key] += 1
            elif key in entry["metrics"]:
                aggregated[action][key] += entry["metrics"][key]

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
