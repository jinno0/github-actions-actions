"""
Tests for generate_review_quality_dashboard.py script
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.generate_review_quality_dashboard import (
    calculate_acceptance_rate,
    calculate_confidence_correlation,
    categorize_suggestions,
    extract_rejection_reasons,
    generate_markdown_dashboard,
    group_by_week,
    load_metrics,
)


class TestLoadMetrics:
    """Test metrics loading functionality."""

    def test_load_valid_metrics(self, tmp_path):
        """Test loading valid metrics file."""
        metrics_file = tmp_path / "metrics.json"
        test_data = [{"outcome": "approved"}]
        metrics_file.write_text(json.dumps(test_data))

        result = load_metrics(metrics_file)
        assert result == test_data

    def test_load_nonexistent_file(self, tmp_path, capsys):
        """Test loading nonexistent file returns empty list."""
        metrics_file = tmp_path / "nonexistent.json"

        result = load_metrics(metrics_file)
        assert result == []

        captured = capsys.readouterr()
        assert "Error: Metrics file not found" in captured.err

    def test_load_invalid_json(self, tmp_path, capsys):
        """Test loading invalid JSON returns empty list."""
        metrics_file = tmp_path / "invalid.json"
        metrics_file.write_text("{invalid json}")

        result = load_metrics(metrics_file)
        assert result == []

        captured = capsys.readouterr()
        assert "Error: Invalid JSON" in captured.err

    def test_load_non_list_data(self, tmp_path):
        """Test loading non-list JSON returns empty list."""
        metrics_file = tmp_path / "object.json"
        metrics_file.write_text('{"key": "value"}')

        result = load_metrics(metrics_file)
        assert result == []


class TestCalculateAcceptanceRate:
    """Test acceptance rate calculation."""

    def test_all_approved(self):
        """Test with all approved outcomes."""
        data = [
            {"outcome": "approved"},
            {"outcome": "approved"},
            {"outcome": "approved"},
        ]
        rate = calculate_acceptance_rate(data)
        assert rate == 100.0

    def test_mixed_outcomes(self):
        """Test with mixed outcomes."""
        data = [
            {"outcome": "approved"},
            {"outcome": "modified"},
            {"outcome": "rejected"},
        ]
        rate = calculate_acceptance_rate(data)
        assert rate == pytest.approx(33.33, rel=0.01)  # 1/3

    def test_empty_data(self):
        """Test with empty data."""
        rate = calculate_acceptance_rate([])
        assert rate == 0.0

    def test_no_outcome_field(self):
        """Test with entries missing outcome field."""
        data = [{"pr": 1}, {"pr": 2}]
        rate = calculate_acceptance_rate(data)
        assert rate == 0.0

    def test_case_sensitive_outcome(self):
        """Test that outcome matching is case-sensitive."""
        data = [
            {"outcome": "Approved"},  # Capital A
            {"outcome": "approved"},
        ]
        rate = calculate_acceptance_rate(data)
        assert rate == 50.0


class TestGroupByWeek:
    """Test weekly grouping functionality."""

    def test_group_by_week_single_week(self):
        """Test grouping data from single week."""
        data = [
            {"timestamp": "2026-02-09T12:00:00Z"},
            {"timestamp": "2026-02-10T13:00:00Z"},
        ]
        result = group_by_week(data)

        assert len(result) == 1
        assert "2026-06" in result  # Week number depends on date
        assert len(result["2026-06"]) == 2

    def test_group_by_week_multiple_weeks(self):
        """Test grouping data across multiple weeks."""
        data = [
            {"timestamp": "2026-02-01T12:00:00Z"},
            {"timestamp": "2026-02-09T12:00:00Z"},
            {"timestamp": "2026-02-16T12:00:00Z"},
        ]
        result = group_by_week(data)

        # Should be grouped into different weeks
        assert len(result) >= 1

    def test_group_by_week_invalid_timestamp(self):
        """Test handling of invalid timestamps."""
        data = [
            {"timestamp": "invalid-date"},
            {"timestamp": "2026-02-09T12:00:00Z"},
        ]
        result = group_by_week(data)

        # Should skip invalid entries
        assert len(result) == 1
        assert len(list(result.values())[0]) == 1

    def test_group_by_week_empty_data(self):
        """Test with empty data."""
        result = group_by_week([])
        assert result == {}


class TestExtractRejectionReasons:
    """Test rejection reason extraction."""

    def test_extract_rejected_reasons(self):
        """Test extracting reasons from rejected reviews."""
        data = [
            {"outcome": "rejected", "rejection_reasons": ["Low quality", "Security issue"]},
            {"outcome": "rejected", "rejection_reasons": ["Low quality"]},
        ]
        reasons = extract_rejection_reasons(data)

        assert reasons["Low quality"] == 2
        assert reasons["Security issue"] == 1

    def test_extract_modified_reasons(self):
        """Test extracting reasons from modified reviews."""
        data = [
            {"outcome": "modified", "rejection_reasons": ["Style issue"]},
        ]
        reasons = extract_rejection_reasons(data)

        assert reasons["Style issue"] == 1

    def test_ignore_approved_reviews(self):
        """Test that approved reviews don't contribute reasons."""
        data = [
            {"outcome": "approved", "rejection_reasons": ["Some reason"]},
        ]
        reasons = extract_rejection_reasons(data)

        assert len(reasons) == 0

    def test_no_reasons_field(self):
        """Test handling missing rejection_reasons field."""
        data = [
            {"outcome": "rejected"},
            {"outcome": "rejected", "rejection_reasons": ["Valid reason"]},
        ]
        reasons = extract_rejection_reasons(data)

        assert reasons["Valid reason"] == 1
        assert len(reasons) == 1


class TestCategorizeSuggestions:
    """Test suggestion categorization."""

    def test_categorize_returns_expected_keys(self):
        """Test that all expected categories exist."""
        data = []
        result = categorize_suggestions(data)

        expected_keys = {"security", "performance", "style", "logic"}
        assert set(result.keys()) == expected_keys

    def test_all_categories_zero(self):
        """Test that all categories are zero (placeholder implementation)."""
        data = [{"outcome": "approved"}]
        result = categorize_suggestions(data)

        assert all(v == 0 for v in result.values())


class TestCalculateConfidenceCorrelation:
    """Test confidence score correlation calculation."""

    def test_confidence_accepted_only(self):
        """Test with only accepted reviews."""
        data = [
            {"outcome": "approved", "confidence_score": 0.8},
            {"outcome": "approved", "confidence_score": 0.9},
        ]
        correlation = calculate_confidence_correlation(data)

        assert correlation["average_confidence_accepted"] == pytest.approx(0.85)
        assert correlation["average_confidence_rejected"] == 0.0

    def test_confidence_rejected_only(self):
        """Test with only rejected reviews."""
        data = [
            {"outcome": "rejected", "confidence_score": 0.5},
            {"outcome": "rejected", "confidence_score": 0.6},
        ]
        correlation = calculate_confidence_correlation(data)

        assert correlation["average_confidence_accepted"] == 0.0
        assert correlation["average_confidence_rejected"] == 0.55

    def test_confidence_mixed(self):
        """Test with mixed outcomes."""
        data = [
            {"outcome": "approved", "confidence_score": 0.8},
            {"outcome": "rejected", "confidence_score": 0.5},
        ]
        correlation = calculate_confidence_correlation(data)

        assert correlation["average_confidence_accepted"] == 0.8
        assert correlation["average_confidence_rejected"] == 0.5

    def test_confidence_missing_score(self):
        """Test handling of missing confidence scores."""
        data = [
            {"outcome": "approved"},  # No confidence_score
            {"outcome": "approved", "confidence_score": 0.9},
        ]
        correlation = calculate_confidence_correlation(data)

        # Should treat missing as 0
        assert correlation["average_confidence_accepted"] == pytest.approx(0.45, rel=0.01)

    def test_confidence_empty_data(self):
        """Test with empty data."""
        correlation = calculate_confidence_correlation([])

        assert correlation["average_confidence_accepted"] == 0.0
        assert correlation["average_confidence_rejected"] == 0.0


class TestGenerateMarkdownDashboard:
    """Test markdown dashboard generation."""

    def test_generate_dashboard_no_data(self):
        """Test dashboard with no data."""
        dashboard = generate_markdown_dashboard([])

        assert "No data available" in dashboard
        assert "# AI Review Quality Dashboard" in dashboard

    def test_generate_dashboard_with_data(self):
        """Test dashboard with review data."""
        data = [
            {
                "outcome": "approved",
                "timestamp": "2026-02-09T12:00:00Z",
                "confidence_score": 0.85,
            },
            {
                "outcome": "rejected",
                "timestamp": "2026-02-09T13:00:00Z",
                "confidence_score": 0.6,
                "rejection_reasons": ["Low quality"],
            },
        ]
        dashboard = generate_markdown_dashboard(data)

        assert "# AI Review Quality Dashboard" in dashboard
        assert "**Total Reviews:** 2" in dashboard
        assert "50.0%" in dashboard  # Acceptance rate
        assert "Low quality" in dashboard

    def test_dashboard_excellent_rating(self):
        """Test dashboard shows excellent rating for 80%+."""
        data = [{"outcome": "approved", "timestamp": "2026-02-09T12:00:00Z"}] * 8
        data.append({"outcome": "rejected", "timestamp": "2026-02-09T12:00:00Z"})

        dashboard = generate_markdown_dashboard(data)
        assert "Excellent" in dashboard

    def test_dashboard_good_rating(self):
        """Test dashboard shows good rating for 70-79%."""
        data = [{"outcome": "approved", "timestamp": "2026-02-09T12:00:00Z"}] * 7
        data += [{"outcome": "rejected", "timestamp": "2026-02-09T12:00:00Z"}] * 3

        dashboard = generate_markdown_dashboard(data)
        assert "Good" in dashboard

    def test_dashboard_moderate_rating(self):
        """Test dashboard shows moderate rating for 60-69%."""
        data = [{"outcome": "approved", "timestamp": "2026-02-09T12:00:00Z"}] * 6
        data += [{"outcome": "rejected", "timestamp": "2026-02-09T12:00:00Z"}] * 4

        dashboard = generate_markdown_dashboard(data)
        assert "Moderate" in dashboard

    def test_dashboard_poor_rating(self):
        """Test dashboard shows poor rating below 60%."""
        data = [{"outcome": "approved", "timestamp": "2026-02-09T12:00:00Z"}] * 5
        data += [{"outcome": "rejected", "timestamp": "2026-02-09T12:00:00Z"}] * 5

        dashboard = generate_markdown_dashboard(data)
        assert "Poor" in dashboard

    def test_dashboard_includes_trend(self):
        """Test dashboard includes trend section."""
        data = [
            {"outcome": "approved", "timestamp": "2026-02-01T12:00:00Z"},
            {"outcome": "approved", "timestamp": "2026-02-09T12:00:00Z"},
        ]
        dashboard = generate_markdown_dashboard(data)

        assert "Trend" in dashboard

    def test_dashboard_includes_recommendations(self):
        """Test dashboard includes recommendations."""
        data = [
            {"outcome": "approved", "timestamp": "2026-02-09T12:00:00Z"},
        ]
        dashboard = generate_markdown_dashboard(data)

        assert "Recommendations" in dashboard

    def test_dashboard_low_acceptance_recommendations(self):
        """Test recommendations for low acceptance rate."""
        data = [{"outcome": "approved", "timestamp": "2026-02-09T12:00:00Z"}] * 5
        data += [{"outcome": "rejected", "timestamp": "2026-02-09T12:00:00Z"}] * 5

        dashboard = generate_markdown_dashboard(data)
        assert "Improve prompt template" in dashboard
        assert "Analyze rejection reasons" in dashboard
