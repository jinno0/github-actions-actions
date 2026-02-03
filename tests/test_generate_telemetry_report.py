#!/usr/bin/env python3
"""Tests for generate_telemetry_report.py"""

import json
import sys
from pathlib import Path
from unittest.mock import patch
import tempfile

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import generate_telemetry_report


class TestLoadTelemetryData:
    """Test telemetry data loading functionality."""

    def test_load_from_nonexistent_file(self):
        """Test loading from file that doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "nonexistent" / "telemetry.log"
            events = generate_telemetry_report.load_telemetry_data(data_path)
            assert events == []

    def test_load_from_valid_file(self):
        """Test loading from file with valid telemetry data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "telemetry.log"

            # Write sample telemetry data
            sample_events = [
                {"action_name": "review-and-merge", "status": "success", "timestamp": "2026-02-04T00:00:00Z"},
                {"action_name": "auto-refactor", "status": "failure", "timestamp": "2026-02-04T01:00:00Z"}
            ]

            with open(data_path, 'w') as f:
                for event in sample_events:
                    f.write(json.dumps(event) + "\n")

            events = generate_telemetry_report.load_telemetry_data(data_path)

            assert len(events) == 2
            assert events[0]["action_name"] == "review-and-merge"
            assert events[1]["action_name"] == "auto-refactor"

    def test_load_handles_invalid_json(self):
        """Test that invalid JSON lines are skipped gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "telemetry.log"

            with open(data_path, 'w') as f:
                f.write('{"valid": "event"}\n')
                f.write('invalid json line\n')
                f.write('{"another": "event"}\n')

            events = generate_telemetry_report.load_telemetry_data(data_path)

            # Should only load valid lines
            assert len(events) == 2
            assert events[0]["valid"] == "event"
            assert events[1]["another"] == "event"


class TestFilterEventsByPeriod:
    """Test time-based filtering functionality."""

    def test_filter_with_zero_days_returns_all(self):
        """Test that days=0 returns all events."""
        events = [
            {"timestamp": "2026-01-01T00:00:00Z"},
            {"timestamp": "2026-02-01T00:00:00Z"}
        ]

        filtered = generate_telemetry_report.filter_events_by_period(events, 0)
        assert len(filtered) == 2

    def test_filter_by_recent_days(self):
        """Test filtering to last N days."""
        events = [
            {"timestamp": "2026-01-01T00:00:00Z"},  # Old event
            {"timestamp": "2026-02-04T00:00:00Z"}   # Recent event (today)
        ]

        # Filter to last 7 days - should only get recent event
        filtered = generate_telemetry_report.filter_events_by_period(events, 7)
        assert len(filtered) == 1
        assert filtered[0]["timestamp"] == "2026-02-04T00:00:00Z"

    def test_filter_handles_invalid_timestamps(self):
        """Test that events with invalid timestamps are included."""
        events = [
            {"timestamp": "invalid-timestamp"},
            {"timestamp": "2026-02-04T00:00:00Z"}
        ]

        filtered = generate_telemetry_report.filter_events_by_period(events, 7)
        # Invalid timestamp events should be included
        assert len(filtered) == 2


class TestAggregateMetrics:
    """Test metrics aggregation functionality."""

    def test_aggregate_empty_events(self):
        """Test aggregating empty event list."""
        metrics = generate_telemetry_report.aggregate_metrics([])
        assert metrics == {}

    def test_aggregate_successful_events(self):
        """Test aggregating successful events."""
        events = [
            {"action_name": "test-action", "status": "success"},
            {"action_name": "test-action", "status": "success"}
        ]

        metrics = generate_telemetry_report.aggregate_metrics(events)

        assert "test-action" in metrics
        assert metrics["test-action"]["total_runs"] == 2
        assert metrics["test-action"]["successes"] == 2
        assert metrics["test-action"]["failures"] == 0

    def test_aggregate_mixed_events(self):
        """Test aggregating mix of success and failure."""
        events = [
            {"action_name": "test-action", "status": "success"},
            {"action_name": "test-action", "status": "failure", "error_type": "Test error"}
        ]

        metrics = generate_telemetry_report.aggregate_metrics(events)

        assert metrics["test-action"]["total_runs"] == 2
        assert metrics["test-action"]["successes"] == 1
        assert metrics["test-action"]["failures"] == 1
        assert len(metrics["test-action"]["errors"]) == 1
        assert metrics["test-action"]["errors"][0] == "Test error"

    def test_aggregate_multiple_actions(self):
        """Test aggregating multiple different actions."""
        events = [
            {"action_name": "action-a", "status": "success"},
            {"action_name": "action-b", "status": "success"},
            {"action_name": "action-a", "status": "success"}
        ]

        metrics = generate_telemetry_report.aggregate_metrics(events)

        assert len(metrics) == 2
        assert metrics["action-a"]["total_runs"] == 2
        assert metrics["action-b"]["total_runs"] == 1


class TestGenerateReport:
    """Test report generation functionality."""

    def test_generate_report_with_empty_metrics(self):
        """Test generating report with no metrics."""
        report = generate_telemetry_report.generate_report({}, 7)

        assert "# AI Actions Telemetry Report" in report
        assert "No Data Available" in report
        assert "Total Runs: 0" not in report

    def test_generate_report_with_metrics(self):
        """Test generating report with actual metrics."""
        metrics = {
            "review-and-merge": {
                "total_runs": 100,
                "successes": 95,
                "failures": 5,
                "errors": ["Error 1", "Error 2"]
            }
        }

        report = generate_telemetry_report.generate_report(metrics, 7)

        assert "**Total Runs** | 100" in report
        assert "**Overall Success Rate** | 95.0%" in report
        assert "review-and-merge" in report
        assert "**Runs** | 100" in report
        assert "**Success Rate** | 95.0%" in report
        assert "Common Errors" in report

    def test_generate_report_includes_period(self):
        """Test that report includes time period."""
        metrics = {"test": {"total_runs": 1, "successes": 1, "failures": 0, "errors": []}}

        report_7days = generate_telemetry_report.generate_report(metrics, 7)
        assert "last 7 days" in report_7days

        report_all = generate_telemetry_report.generate_report(metrics, 0)
        assert "all time" in report_all

    def test_generate_report_has_status_indicator(self):
        """Test that report includes visual status indicator."""
        metrics = {
            "test": {
                "total_runs": 100,
                "successes": 95,  # 95% = Excellent
                "failures": 5,
                "errors": []
            }
        }

        report = generate_telemetry_report.generate_report(metrics, 7)
        assert "✅" in report
        assert "Excellent" in report

    def test_generate_report_has_privacy_notice(self):
        """Test that report includes privacy notice."""
        metrics = {"test": {"total_runs": 1, "successes": 1, "failures": 0, "errors": []}}

        report = generate_telemetry_report.generate_report(metrics, 7)

        assert "Privacy Notice" in report
        assert "SHA-256 hashed" in report
        assert "DISABLE_TELEMETRY" in report


class TestIntegration:
    """Integration tests for the full workflow."""

    def test_full_workflow_with_sample_data(self):
        """Test complete workflow from telemetry.log to report."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup: Create sample telemetry.log
            data_path = Path(tmpdir) / "telemetry.log"
            sample_events = [
                {
                    "action_name": "review-and-merge",
                    "status": "success",
                    "timestamp": "2026-02-04T00:00:00Z"
                },
                {
                    "action_name": "auto-refactor",
                    "status": "failure",
                    "timestamp": "2026-02-04T01:00:00Z",
                    "error_type": "Test error"
                }
            ]

            with open(data_path, 'w') as f:
                for event in sample_events:
                    f.write(json.dumps(event) + "\n")

            # Execute: Load, filter, aggregate, generate report
            events = generate_telemetry_report.load_telemetry_data(data_path)
            events = generate_telemetry_report.filter_events_by_period(events, 7)
            metrics = generate_telemetry_report.aggregate_metrics(events)
            report = generate_telemetry_report.generate_report(metrics, 7)

            # Verify
            assert "review-and-merge" in report
            assert "auto-refactor" in report
            assert "**Total Runs** | 2" in report
            assert "**Overall Success Rate** | 50.0%" in report
            assert "Common Errors" in report
            assert "Test error" in report
