"""Tests for the acceptance rate calculator."""

import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta

# Import the module to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import calculate_acceptance_rate


class TestCalculateAcceptanceRate:
    """Test acceptance rate calculation."""

    def test_empty_metrics(self):
        """Test calculation with no metrics."""
        result = calculate_acceptance_rate.calculate_acceptance_rate([])

        assert result["acceptance_rate"] == 0.0
        assert result["total_reviews"] == 0
        assert result["outcome_breakdown"] == {}
        assert "no reviews to analyze" in result["interpretation"].lower()

    def test_all_approved(self):
        """Test with all approved reviews."""
        metrics = [
            {"outcome": "approved", "suggestions_count": 3},
            {"outcome": "approved", "suggestions_count": 5},
            {"outcome": "approved", "suggestions_count": 2},
        ]

        result = calculate_acceptance_rate.calculate_acceptance_rate(metrics)

        assert result["acceptance_rate"] == 100.0
        assert result["total_reviews"] == 3
        assert result["outcome_breakdown"]["approved"] == 3

    def test_mixed_outcomes(self):
        """Test with mixed review outcomes."""
        metrics = [
            {"outcome": "approved", "suggestions_count": 3, "accepted_count": 3},
            {"outcome": "modified", "suggestions_count": 5, "accepted_count": 2},
            {"outcome": "rejected", "suggestions_count": 2, "accepted_count": 0},
            {"outcome": "needs_work", "suggestions_count": 4, "accepted_count": 0},
            {"outcome": "approved", "suggestions_count": 1, "accepted_count": 1},
        ]

        result = calculate_acceptance_rate.calculate_acceptance_rate(metrics)

        # approved (2) + modified (1) = 3 out of 5 = 60%
        assert result["acceptance_rate"] == 60.0
        assert result["total_reviews"] == 5
        assert result["outcome_breakdown"]["approved"] == 2
        assert result["outcome_breakdown"]["modified"] == 1
        assert result["outcome_breakdown"]["rejected"] == 1
        assert result["outcome_breakdown"]["needs_work"] == 1

    def test_average_calculations(self):
        """Test average calculations."""
        metrics = [
            {"outcome": "approved", "suggestions_count": 3, "accepted_count": 2},
            {"outcome": "approved", "suggestions_count": 5, "accepted_count": 4},
            {"outcome": "rejected", "suggestions_count": 2, "accepted_count": 0},
        ]

        result = calculate_acceptance_rate.calculate_acceptance_rate(metrics)

        assert result["average_suggestions"] == pytest.approx(3.33, rel=0.1)
        assert result["average_accepted_suggestions"] == pytest.approx(2.0, rel=0.1)

    def test_rejection_reasons(self):
        """Test common rejection reason extraction."""
        metrics = [
            {"outcome": "rejected", "rejection_reasons": ["Too aggressive", "Missing context"]},
            {"outcome": "rejected", "rejection_reasons": ["Too aggressive", "Wrong approach"]},
            {"outcome": "rejected", "rejection_reasons": ["Missing context"]},
        ]

        result = calculate_acceptance_rate.calculate_acceptance_rate(metrics)

        reasons = result["common_rejection_reasons"]
        assert len(reasons) == 3
        assert reasons[0]["reason"] == "Too aggressive"
        assert reasons[0]["count"] == 2
        assert reasons[1]["reason"] == "Missing context"
        assert reasons[1]["count"] == 2


class TestFilterMetricsByTime:
    """Test time-based filtering."""

    def test_filter_last_7_days(self):
        """Test filtering to last 7 days."""
        now = datetime.utcnow()
        metrics = [
            {
                "outcome": "approved",
                "timestamp": (now - timedelta(days=3)).isoformat()
            },
            {
                "outcome": "rejected",
                "timestamp": (now - timedelta(days=10)).isoformat()
            },
            {
                "outcome": "approved",
                "timestamp": (now - timedelta(days=1)).isoformat()
            },
        ]

        filtered = calculate_acceptance_rate.filter_metrics_by_time(metrics, "7d")

        assert len(filtered) == 2  # Only the reviews from 3 days and 1 day ago
        assert all(m["outcome"] == "approved" for m in filtered)

    def test_filter_with_invalid_timestamps(self):
        """Test that metrics with invalid timestamps are handled gracefully."""
        metrics = [
            {"outcome": "approved", "timestamp": "invalid-date"},
            {"outcome": "rejected"},  # No timestamp
            {
                "outcome": "approved",
                "timestamp": datetime.utcnow().isoformat()
            },
        ]

        filtered = calculate_acceptance_rate.filter_metrics_by_time(metrics, "7d")

        # Valid timestamp and no timestamp should be included (2 total)
        # Invalid timestamp gets skipped in the try/except
        assert len(filtered) == 2


class TestInterpretation:
    """Test interpretation generation."""

    def test_insufficient_data(self):
        """Test interpretation with insufficient data."""
        interpretation = calculate_acceptance_rate.get_interpretation(75, 5)
        assert "insufficient data" in interpretation.lower()

    def test_excellent_acceptance(self):
        """Test interpretation for excellent acceptance rate."""
        interpretation = calculate_acceptance_rate.get_interpretation(85, 50)
        assert "excellent" in interpretation.lower()
        assert "85" in interpretation

    def test_good_acceptance(self):
        """Test interpretation for good acceptance rate."""
        interpretation = calculate_acceptance_rate.get_interpretation(72, 50)
        assert "good" in interpretation.lower()

    def test_moderate_acceptance(self):
        """Test interpretation for moderate acceptance rate."""
        interpretation = calculate_acceptance_rate.get_interpretation(60, 50)
        assert "moderate" in interpretation.lower()

    def test_poor_acceptance(self):
        """Test interpretation for poor acceptance rate."""
        interpretation = calculate_acceptance_rate.get_interpretation(40, 50)
        assert "poor" in interpretation.lower()


class TestGenerateQualityReport:
    """Test quality report generation."""

    def test_report_generation(self):
        """Test generating a quality report."""
        metrics = [
            {
                "outcome": "approved",
                "timestamp": datetime.utcnow().isoformat(),
                "suggestions_count": 3,
                "accepted_count": 3
            },
            {
                "outcome": "modified",
                "timestamp": datetime.utcnow().isoformat(),
                "suggestions_count": 5,
                "accepted_count": 2,
                "rejection_reasons": ["Too aggressive"]
            },
        ]

        report = calculate_acceptance_rate.generate_quality_report(metrics, "7d")

        assert "AI Review Quality Report" in report
        assert "Acceptance Rate" in report
        assert "100.0%" in report  # All approved/modified = 100%
        assert "Outcome Breakdown" in report
        assert "approved" in report.lower()

    def test_report_with_rejections(self):
        """Test report includes rejection reasons."""
        metrics = [
            {
                "outcome": "rejected",
                "timestamp": datetime.utcnow().isoformat(),
                "rejection_reasons": ["Too aggressive", "Missing context"]
            },
            {
                "outcome": "rejected",
                "timestamp": datetime.utcnow().isoformat(),
                "rejection_reasons": ["Too aggressive"]
            },
        ]

        report = calculate_acceptance_rate.generate_quality_report(metrics, "7d")

        assert "Common Rejection Reasons" in report
        assert "Too aggressive" in report


class TestLoadAndSave:
    """Test file I/O operations."""

    def test_load_from_file(self, tmp_path):
        """Test loading metrics from a file."""
        metrics_file = tmp_path / "metrics.json"
        test_metrics = [
            {"outcome": "approved", "timestamp": "2026-02-03T00:00:00Z"},
            {"outcome": "rejected", "timestamp": "2026-02-03T01:00:00Z"},
        ]

        metrics_file.write_text(json.dumps(test_metrics))

        loaded = calculate_acceptance_rate.load_metrics_from_file(str(metrics_file))

        assert len(loaded) == 2
        assert loaded[0]["outcome"] == "approved"

    def test_load_nonexistent_file(self, tmp_path):
        """Test loading from a non-existent file."""
        loaded = calculate_acceptance_rate.load_metrics_from_file(str(tmp_path / "nonexistent.json"))
        assert loaded == []

    def test_load_invalid_json(self, tmp_path):
        """Test loading from a file with invalid JSON."""
        metrics_file = tmp_path / "invalid.json"
        metrics_file.write_text("not valid json")

        loaded = calculate_acceptance_rate.load_metrics_from_file(str(metrics_file))
        assert loaded == []


class TestCliInterface:
    """Test CLI interface."""

    def test_main_with_sample_data(self, tmp_path, capsys):
        """Test main function with sample data."""
        # Create test metrics file
        metrics_file = tmp_path / "metrics.json"
        test_metrics = [
            {"outcome": "approved", "timestamp": "2026-02-03T00:00:00Z"},
            {"outcome": "modified", "timestamp": "2026-02-03T01:00:00Z"},
            {"outcome": "rejected", "timestamp": "2026-02-03T02:00:00Z"},
        ]
        metrics_file.write_text(json.dumps(test_metrics))

        # Run main
        import sys
        old_argv = sys.argv
        sys.argv = [
            "calculate_acceptance_rate.py",
            "--metrics-file", str(metrics_file),
            "--target-rate", "70"
        ]

        try:
            result = calculate_acceptance_rate.main()
        finally:
            sys.argv = old_argv

        captured = capsys.readouterr()

        # Should print summary
        assert "Acceptance Rate:" in captured.out
        assert "66.67%" in captured.out  # 2/3 = 66.67%
        assert "Total Reviews: 3" in captured.out
        assert "BELOW TARGET" in captured.out or "PASS" in captured.out

        # Return code should indicate target not met (66.67% < 70%)
        assert result == 1
