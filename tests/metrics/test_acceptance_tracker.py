"""
Tests for acceptance rate tracking functionality
"""

import json
import os
import tempfile

import pytest

from actions.lib.acceptance_tracker import (
    AcceptanceTracker,
    aggregate_metrics_by_action,
)


class TestAcceptanceTracker:
    """Test AcceptanceTracker class functionality"""

    def test_initialization(self):
        """Test tracker initialization"""
        tracker = AcceptanceTracker("test-action")
        assert tracker.action_name == "test-action"
        assert tracker.metrics["suggestions_made"] == 0
        assert tracker.metrics["suggestions_accepted"] == 0

    def test_record_suggestion_made(self):
        """Test recording a suggestion was made"""
        tracker = AcceptanceTracker("test-action")
        tracker.record_suggestion("made")
        assert tracker.metrics["suggestions_made"] == 1
        assert tracker.metrics["suggestions_accepted"] == 0

    def test_record_suggestion_accepted(self):
        """Test recording a suggestion was accepted"""
        tracker = AcceptanceTracker("test-action")
        tracker.record_suggestion("made")
        tracker.record_suggestion("accepted")
        assert tracker.metrics["suggestions_made"] == 1
        assert tracker.metrics["suggestions_accepted"] == 1

    def test_record_suggestion_rejected(self):
        """Test recording a suggestion was rejected"""
        tracker = AcceptanceTracker("test-action")
        tracker.record_suggestion("made")
        tracker.record_suggestion("rejected")
        assert tracker.metrics["suggestions_made"] == 1
        assert tracker.metrics["suggestions_rejected"] == 1

    def test_record_suggestion_modified(self):
        """Test recording a suggestion was modified"""
        tracker = AcceptanceTracker("test-action")
        tracker.record_suggestion("made")
        tracker.record_suggestion("modified")
        assert tracker.metrics["suggestions_made"] == 1
        assert tracker.metrics["suggestions_modified"] == 1

    def test_record_invalid_outcome(self):
        """Test that invalid outcomes raise ValueError"""
        tracker = AcceptanceTracker("test-action")
        with pytest.raises(ValueError, match="Invalid outcome"):
            tracker.record_suggestion("invalid")

    def test_acceptance_rate_calculation(self):
        """Test acceptance rate calculation"""
        tracker = AcceptanceTracker("test-action")

        # No suggestions yet
        assert tracker.get_acceptance_rate() == 0.0

        # 10 suggestions, 8 accepted
        for _ in range(10):
            tracker.record_suggestion("made")
        for _ in range(8):
            tracker.record_suggestion("accepted")

        assert tracker.get_acceptance_rate() == 80.0

    def test_acceptance_rate_100_percent(self):
        """Test 100% acceptance rate"""
        tracker = AcceptanceTracker("test-action")
        tracker.record_suggestion("made")
        tracker.record_suggestion("accepted")
        assert tracker.get_acceptance_rate() == 100.0

    def test_acceptance_rate_0_percent(self):
        """Test 0% acceptance rate (all rejected)"""
        tracker = AcceptanceTracker("test-action")
        tracker.record_suggestion("made")
        tracker.record_suggestion("rejected")
        assert tracker.get_acceptance_rate() == 0.0

    def test_rejection_rate(self):
        """Test rejection rate calculation"""
        tracker = AcceptanceTracker("test-action")

        # 10 suggestions, 2 rejected
        for _ in range(10):
            tracker.record_suggestion("made")
        for _ in range(2):
            tracker.record_suggestion("rejected")

        assert tracker.get_rejection_rate() == 20.0

    def test_modification_rate(self):
        """Test modification rate calculation"""
        tracker = AcceptanceTracker("test-action")

        # 10 suggestions, 3 modified
        for _ in range(10):
            tracker.record_suggestion("made")
        for _ in range(3):
            tracker.record_suggestion("modified")

        assert tracker.get_modification_rate() == 30.0

    def test_get_metrics(self):
        """Test getting metrics dictionary"""
        tracker = AcceptanceTracker("test-action")
        tracker.record_suggestion("made")
        tracker.record_suggestion("accepted")

        metrics = tracker.get_metrics()
        assert metrics["suggestions_made"] == 1
        assert metrics["suggestions_accepted"] == 1
        # Verify it's a copy, not the original
        metrics["suggestions_made"] = 999
        assert tracker.metrics["suggestions_made"] == 1

    def test_export_metrics(self):
        """Test exporting metrics for reporting"""
        tracker = AcceptanceTracker("test-action")
        tracker.record_suggestion("made")
        tracker.record_suggestion("accepted")

        exported = tracker.export_metrics()

        assert exported["action"] == "test-action"
        assert "timestamp" in exported
        assert exported["metrics"]["suggestions_made"] == 1
        assert exported["rates"]["acceptance_rate"] == 100.0
        assert exported["total_suggestions"] == 1

    def test_save_to_file(self):
        """Test saving metrics to a JSON file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "metrics.json")

            # Create and save tracker
            tracker = AcceptanceTracker("test-action")
            tracker.record_suggestion("made")
            tracker.record_suggestion("accepted")
            tracker.save_to_file(filepath)

            # Verify file exists and contains data
            assert os.path.exists(filepath)

            with open(filepath) as f:
                data = json.load(f)

            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]["action"] == "test-action"

    def test_save_to_file_appends(self):
        """Test that save_to_file appends to existing data"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "metrics.json")

            # First save
            tracker1 = AcceptanceTracker("test-action")
            tracker1.record_suggestion("made")
            tracker1.record_suggestion("accepted")
            tracker1.save_to_file(filepath)

            # Second save
            tracker2 = AcceptanceTracker("test-action")
            tracker2.record_suggestion("made")
            tracker2.record_suggestion("rejected")
            tracker2.save_to_file(filepath)

            # Verify both entries are saved
            with open(filepath) as f:
                data = json.load(f)

            assert len(data) == 2

    def test_reset_metrics(self):
        """Test resetting metrics to zero"""
        tracker = AcceptanceTracker("test-action")
        tracker.record_suggestion("made")
        tracker.record_suggestion("accepted")
        tracker.record_suggestion("rejected")

        tracker.reset_metrics()

        assert tracker.metrics["suggestions_made"] == 0
        assert tracker.metrics["suggestions_accepted"] == 0
        assert tracker.metrics["suggestions_rejected"] == 0

    def test_from_file_no_existing_file(self):
        """Test from_file when file doesn't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "nonexistent.json")

            tracker = AcceptanceTracker.from_file("test-action", filepath)

            assert tracker.action_name == "test-action"
            assert tracker.metrics["suggestions_made"] == 0

    def test_from_file_loads_existing_data(self):
        """Test from_file loads and aggregates existing metrics"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "metrics.json")

            # Create some initial data
            tracker1 = AcceptanceTracker("test-action")
            tracker1.record_suggestion("made")
            tracker1.record_suggestion("accepted")
            tracker1.save_to_file(filepath)

            # Load the data into a new tracker
            tracker2 = AcceptanceTracker.from_file("test-action", filepath)

            assert tracker2.metrics["suggestions_made"] == 1
            assert tracker2.metrics["suggestions_accepted"] == 1


class TestAggregateMetricsByAction:
    """Test aggregate_metrics_by_action function"""

    def test_aggregate_empty_list(self):
        """Test aggregating empty metrics list"""
        result = aggregate_metrics_by_action([])
        assert result == {}

    def test_aggregate_single_action(self):
        """Test aggregating metrics for single action"""
        metrics_data = [
            {
                "action": "test-action",
                "metrics": {
                    "suggestions_made": 10,
                    "suggestions_accepted": 8,
                    "suggestions_rejected": 2,
                    "suggestions_modified": 0,
                },
            }
        ]

        result = aggregate_metrics_by_action(metrics_data)

        assert "test-action" in result
        assert result["test-action"]["suggestions_made"] == 10
        assert result["test-action"]["acceptance_rate"] == 80.0

    def test_aggregate_multiple_actions(self):
        """Test aggregating metrics for multiple actions"""
        metrics_data = [
            {
                "action": "action-1",
                "metrics": {
                    "suggestions_made": 10,
                    "suggestions_accepted": 8,
                    "suggestions_rejected": 2,
                    "suggestions_modified": 0,
                },
            },
            {
                "action": "action-2",
                "metrics": {
                    "suggestions_made": 20,
                    "suggestions_accepted": 15,
                    "suggestions_rejected": 5,
                    "suggestions_modified": 0,
                },
            },
        ]

        result = aggregate_metrics_by_action(metrics_data)

        assert len(result) == 2
        assert result["action-1"]["acceptance_rate"] == 80.0
        assert result["action-2"]["acceptance_rate"] == 75.0

    def test_aggregate_filter_by_action(self):
        """Test filtering aggregation by specific action"""
        metrics_data = [
            {
                "action": "action-1",
                "metrics": {
                    "suggestions_made": 10,
                    "suggestions_accepted": 8,
                    "suggestions_rejected": 2,
                    "suggestions_modified": 0,
                },
            },
            {
                "action": "action-2",
                "metrics": {
                    "suggestions_made": 20,
                    "suggestions_accepted": 15,
                    "suggestions_rejected": 5,
                    "suggestions_modified": 0,
                },
            },
        ]

        result = aggregate_metrics_by_action(metrics_data, action_name="action-1")

        assert len(result) == 1
        assert "action-1" in result
        assert "action-2" not in result

    def test_aggregate_sum_multiple_entries(self):
        """Test that aggregation sums multiple entries for same action"""
        metrics_data = [
            {
                "action": "test-action",
                "metrics": {
                    "suggestions_made": 10,
                    "suggestions_accepted": 8,
                    "suggestions_rejected": 2,
                    "suggestions_modified": 0,
                },
            },
            {
                "action": "test-action",
                "metrics": {
                    "suggestions_made": 5,
                    "suggestions_accepted": 3,
                    "suggestions_rejected": 2,
                    "suggestions_modified": 0,
                },
            },
        ]

        result = aggregate_metrics_by_action(metrics_data)

        assert result["test-action"]["suggestions_made"] == 15
        assert result["test-action"]["suggestions_accepted"] == 11
        assert result["test-action"]["suggestions_rejected"] == 4
        assert result["test-action"]["acceptance_rate"] == pytest.approx(73.33, rel=1e-2)

    def test_aggregate_calculates_all_rates(self):
        """Test that all rates are calculated"""
        metrics_data = [
            {
                "action": "test-action",
                "metrics": {
                    "suggestions_made": 100,
                    "suggestions_accepted": 60,
                    "suggestions_rejected": 20,
                    "suggestions_modified": 20,
                },
            },
        ]

        result = aggregate_metrics_by_action(metrics_data)

        assert result["test-action"]["acceptance_rate"] == 60.0
        assert result["test-action"]["rejection_rate"] == 20.0
        assert result["test-action"]["modification_rate"] == 20.0
