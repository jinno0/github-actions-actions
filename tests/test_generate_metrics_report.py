#!/usr/bin/env python3
"""Tests for generate_metrics_report.py"""

import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import generate_metrics_report


class TestGenerateMarkdownReport:
    """Test markdown report generation functionality."""

    def test_generate_report_with_complete_data(self):
        """Test generating report with complete metrics data."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 3
            },
            "by_action": {
                "action-a": {
                    "suggestions_made": 50,
                    "suggestions_accepted": 45,
                    "suggestions_rejected": 3,
                    "suggestions_modified": 2,
                    "acceptance_rate": 90.0,
                    "rejection_rate": 6.0,
                    "modification_rate": 4.0,
                    "entries": 5,
                    "first_seen": "2026-02-01T00:00:00Z",
                    "last_seen": "2026-02-07T12:00:00Z"
                },
                "action-b": {
                    "suggestions_made": 30,
                    "suggestions_accepted": 25,
                    "suggestions_rejected": 4,
                    "suggestions_modified": 1,
                    "acceptance_rate": 83.3,
                    "rejection_rate": 13.3,
                    "modification_rate": 3.3,
                    "entries": 3,
                    "first_seen": "2026-02-02T00:00:00Z",
                    "last_seen": "2026-02-06T12:00:00Z"
                },
                "action-c": {
                    "suggestions_made": 20,
                    "suggestions_accepted": 15,
                    "suggestions_rejected": 3,
                    "suggestions_modified": 2,
                    "acceptance_rate": 75.0,
                    "rejection_rate": 15.0,
                    "modification_rate": 10.0,
                    "entries": 2,
                    "first_seen": "2026-02-03T00:00:00Z",
                    "last_seen": "2026-02-05T12:00:00Z"
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Verify header
        assert "# Acceptance Rate Report" in report
        assert "**Generated:** 2026-02-07T12:00:00Z" in report

        # Verify overall summary
        assert "## Overall Summary" in report
        assert "**Total Suggestions:** 100" in report
        assert "**Accepted:** 85 (85.0%)" in report
        assert "**Rejected:** 10 (10.0%)" in report
        assert "**Modified:** 5 (5.0%)" in report
        assert "**Actions Tracked:** 3" in report

        # Verify status indicator for >= 80%
        assert "### ✅ Status: Target Achieved" in report
        assert "Acceptance rate of 85.0% meets or exceeds the 80% target" in report

        # Verify per-action breakdown
        assert "## Per-Action Breakdown" in report
        assert "### action-a" in report
        assert "### action-b" in report
        assert "### action-c" in report

        # Verify action metrics table
        assert "| Metric | Count | Percentage |" in report
        assert "| Accepted | 45 | 90.0% |" in report
        assert "| Rejected | 3 | 6.0% |" in report
        assert "| Modified | 2 | 4.0% |" in report
        assert "| **Total** | **50** | **100%** |" in report

        # Verify insights section
        assert "## Insights and Recommendations" in report
        assert "### 🏆 Best Performing Action" in report
        assert "**action-a:** 90.0% acceptance rate" in report

        # Verify footer
        assert "---" in report
        assert "*This report is generated automatically" in report
        assert "**Target:** Acceptance Rate >= 80% (QA-001)" in report

    def test_generate_report_with_below_target_acceptance(self):
        """Test generating report when acceptance rate is below target."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 50,
                "suggestions_rejected": 40,
                "suggestions_modified": 10,
                "acceptance_rate": 50.0,
                "rejection_rate": 40.0,
                "modification_rate": 10.0,
                "actions_tracked": 2
            },
            "by_action": {
                "action-a": {
                    "suggestions_made": 50,
                    "suggestions_accepted": 30,
                    "suggestions_rejected": 15,
                    "suggestions_modified": 5,
                    "acceptance_rate": 60.0,
                    "rejection_rate": 30.0,
                    "modification_rate": 10.0,
                    "entries": 5
                },
                "action-b": {
                    "suggestions_made": 50,
                    "suggestions_accepted": 20,
                    "suggestions_rejected": 25,
                    "suggestions_modified": 5,
                    "acceptance_rate": 40.0,
                    "rejection_rate": 50.0,
                    "modification_rate": 10.0,
                    "entries": 5
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Verify below target status
        assert "### 🔴 Status: Below Target" in report
        assert "Acceptance rate of 50.0% is significantly below the 80% target" in report
        assert "Consider reviewing suggestion quality and user feedback" in report

        # Verify actions needing improvement section
        assert "### 🔧 Actions Needing Improvement" in report
        assert "**action-a:** 60.0% acceptance rate" in report
        assert "**action-b:** 40.0% acceptance rate" in report
        assert "Recommendations:" in report
        assert "1. Review suggestion quality and relevance" in report

    def test_generate_report_with_approaching_target_acceptance(self):
        """Test generating report when acceptance rate is approaching target."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 70,
                "suggestions_rejected": 25,
                "suggestions_modified": 5,
                "acceptance_rate": 70.0,
                "rejection_rate": 25.0,
                "modification_rate": 5.0,
                "actions_tracked": 2
            },
            "by_action": {}
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Verify approaching target status
        assert "### ⚠️ Status: Approaching Target" in report
        assert "Acceptance rate of 70.0% is below the 80% target but shows positive trend" in report

    def test_generate_report_with_no_data(self):
        """Test generating report with no metrics data."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 0,
                "suggestions_accepted": 0,
                "suggestions_rejected": 0,
                "suggestions_modified": 0,
                "acceptance_rate": 0.0,
                "rejection_rate": 0.0,
                "modification_rate": 0.0,
                "actions_tracked": 0
            },
            "by_action": {}
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Verify no data message
        assert "### 📊 No Data Available" in report
        assert "No acceptance rate data has been collected yet" in report
        assert "Metrics will be populated as actions are used" in report
        assert "**Next Steps:**" in report
        assert "1. Ensure AI-powered actions are being used in workflows" in report

        # Verify insights section is not shown when no data
        assert "## Insights and Recommendations" not in report

    def test_generate_report_with_action_no_suggestions(self):
        """Test generating report when an action has no suggestions."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 80,
                "suggestions_rejected": 15,
                "suggestions_modified": 5,
                "acceptance_rate": 80.0,
                "rejection_rate": 15.0,
                "modification_rate": 5.0,
                "actions_tracked": 2
            },
            "by_action": {
                "active-action": {
                    "suggestions_made": 100,
                    "suggestions_accepted": 80,
                    "suggestions_rejected": 15,
                    "suggestions_modified": 5,
                    "acceptance_rate": 80.0,
                    "rejection_rate": 15.0,
                    "modification_rate": 5.0,
                    "entries": 10
                },
                "inactive-action": {
                    "suggestions_made": 0,
                    "suggestions_accepted": 0,
                    "suggestions_rejected": 0,
                    "suggestions_modified": 0,
                    "acceptance_rate": 0.0,
                    "rejection_rate": 0.0,
                    "modification_rate": 0.0,
                    "entries": 0
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Active action should have full details
        assert "### active-action" in report
        assert "**Acceptance Rate:** 80.0%" in report
        assert "✅" in report

        # Inactive action should show no suggestions message
        assert "### inactive-action" in report
        assert "No suggestions recorded yet" in report

    def test_generate_report_action_status_indicators(self):
        """Test that different acceptance rates get appropriate status indicators."""
        # High performing action
        high_metrics = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 1
            },
            "by_action": {
                "high-action": {
                    "suggestions_made": 50,
                    "suggestions_accepted": 45,
                    "suggestions_rejected": 3,
                    "suggestions_modified": 2,
                    "acceptance_rate": 90.0,
                    "rejection_rate": 6.0,
                    "modification_rate": 4.0,
                    "entries": 5
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(high_metrics)
        assert "✅ **Acceptance Rate:** 90.0%" in report

        # Medium performing action
        medium_metrics = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 70,
                "suggestions_rejected": 25,
                "suggestions_modified": 5,
                "acceptance_rate": 70.0,
                "rejection_rate": 25.0,
                "modification_rate": 5.0,
                "actions_tracked": 1
            },
            "by_action": {
                "medium-action": {
                    "suggestions_made": 50,
                    "suggestions_accepted": 35,
                    "suggestions_rejected": 12,
                    "suggestions_modified": 3,
                    "acceptance_rate": 70.0,
                    "rejection_rate": 24.0,
                    "modification_rate": 6.0,
                    "entries": 5
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(medium_metrics)
        assert "⚠️ **Acceptance Rate:** 70.0%" in report

        # Low performing action
        low_metrics = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 40,
                "suggestions_rejected": 50,
                "suggestions_modified": 10,
                "acceptance_rate": 40.0,
                "rejection_rate": 50.0,
                "modification_rate": 10.0,
                "actions_tracked": 1
            },
            "by_action": {
                "low-action": {
                    "suggestions_made": 50,
                    "suggestions_accepted": 15,
                    "suggestions_rejected": 30,
                    "suggestions_modified": 5,
                    "acceptance_rate": 30.0,
                    "rejection_rate": 60.0,
                    "modification_rate": 10.0,
                    "entries": 5
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(low_metrics)
        assert "🔴 **Acceptance Rate:** 30.0%" in report

    def test_generate_report_with_missing_optional_fields(self):
        """Test generating report with missing optional fields."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 1
            },
            "by_action": {
                "action-a": {
                    "suggestions_made": 100,
                    "suggestions_accepted": 85,
                    "suggestions_rejected": 10,
                    "suggestions_modified": 5,
                    "acceptance_rate": 85.0,
                    "rejection_rate": 10.0,
                    "modification_rate": 5.0
                    # Missing entries, first_seen, last_seen
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Should still generate valid report without crashing
        assert "# Acceptance Rate Report" in report
        assert "### action-a" in report
        assert "✅ **Acceptance Rate:** 85.0%" in report

    def test_generate_report_actions_sorted_by_acceptance_rate(self):
        """Test that actions are sorted by acceptance rate (descending)."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 150,
                "suggestions_accepted": 120,
                "suggestions_rejected": 20,
                "suggestions_modified": 10,
                "acceptance_rate": 80.0,
                "rejection_rate": 13.3,
                "modification_rate": 6.7,
                "actions_tracked": 3
            },
            "by_action": {
                "action-c": {  # 95%
                    "suggestions_made": 50,
                    "suggestions_accepted": 47,
                    "suggestions_rejected": 2,
                    "suggestions_modified": 1,
                    "acceptance_rate": 94.0,
                    "rejection_rate": 4.0,
                    "modification_rate": 2.0,
                    "entries": 5
                },
                "action-a": {  # 90%
                    "suggestions_made": 50,
                    "suggestions_accepted": 45,
                    "suggestions_rejected": 3,
                    "suggestions_modified": 2,
                    "acceptance_rate": 90.0,
                    "rejection_rate": 6.0,
                    "modification_rate": 4.0,
                    "entries": 5
                },
                "action-b": {  # 56%
                    "suggestions_made": 50,
                    "suggestions_accepted": 28,
                    "suggestions_rejected": 15,
                    "suggestions_modified": 7,
                    "acceptance_rate": 56.0,
                    "rejection_rate": 30.0,
                    "modification_rate": 14.0,
                    "entries": 5
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Find positions of each action in the report
        action_c_pos = report.find("### action-c")
        action_a_pos = report.find("### action-a")
        action_b_pos = report.find("### action-b")

        # Should be sorted: action-c (94%), action-a (90%), action-b (56%)
        assert action_c_pos < action_a_pos < action_b_pos

    def test_generate_report_includes_source_file(self):
        """Test that report includes source file reference."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 1
            },
            "by_action": {},
            "source_file": "custom/path/to/metrics.json"
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        assert "*For raw data, see: custom/path/to/metrics.json*" in report

    def test_generate_report_with_single_data_point(self):
        """Test generating report when action has only one data point."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 10,
                "suggestions_accepted": 8,
                "suggestions_rejected": 2,
                "suggestions_modified": 0,
                "acceptance_rate": 80.0,
                "rejection_rate": 20.0,
                "modification_rate": 0.0,
                "actions_tracked": 1
            },
            "by_action": {
                "action-a": {
                    "suggestions_made": 10,
                    "suggestions_accepted": 8,
                    "suggestions_rejected": 2,
                    "suggestions_modified": 0,
                    "acceptance_rate": 80.0,
                    "rejection_rate": 20.0,
                    "modification_rate": 0.0,
                    "entries": 1,
                    "first_seen": "2026-02-07T12:00:00Z",
                    "last_seen": "2026-02-07T12:00:00Z"
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Should not show data points count for single entry
        assert "*Data points:*" not in report

        # Should still show timestamps
        assert "*First seen: 2026-02-07T12:00:00Z*" in report
        assert "*Last seen: 2026-02-07T12:00:00Z*" in report

    def test_generate_report_with_multiple_data_points(self):
        """Test generating report when action has multiple data points."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 1
            },
            "by_action": {
                "action-a": {
                    "suggestions_made": 100,
                    "suggestions_accepted": 85,
                    "suggestions_rejected": 10,
                    "suggestions_modified": 5,
                    "acceptance_rate": 85.0,
                    "rejection_rate": 10.0,
                    "modification_rate": 5.0,
                    "entries": 10,
                    "first_seen": "2026-02-01T00:00:00Z",
                    "last_seen": "2026-02-07T12:00:00Z"
                }
            }
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Should show data points count
        assert "*Data points: 10*" in report

    def test_generate_report_empty_by_action(self):
        """Test generating report when by_action is empty but overall has data."""
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 0
            },
            "by_action": {}
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Should show overall summary
        assert "## Overall Summary" in report
        assert "**Total Suggestions:** 100" in report

        # Should not show per-action breakdown
        assert "## Per-Action Breakdown" not in report

        # Insights section is shown when total > 0, even if by_action is empty
        # This is expected behavior based on line 136 in the script
        assert "## Insights and Recommendations" in report

    def test_generate_report_missing_timestamp(self):
        """Test generating report when timestamp is missing."""
        metrics_data = {
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 1
            },
            "by_action": {}
        }

        report = generate_metrics_report.generate_markdown_report(metrics_data)

        # Should show Unknown for timestamp
        assert "**Generated:** Unknown" in report

    def test_generate_report_boundary_acceptance_rate(self):
        """Test boundary conditions for acceptance rate status."""
        # Exactly 80% - should be "Target Achieved"
        metrics_80 = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 80,
                "suggestions_rejected": 15,
                "suggestions_modified": 5,
                "acceptance_rate": 80.0,
                "rejection_rate": 15.0,
                "modification_rate": 5.0,
                "actions_tracked": 1
            },
            "by_action": {}
        }

        report = generate_metrics_report.generate_markdown_report(metrics_80)
        assert "### ✅ Status: Target Achieved" in report

        # Exactly 60% - should be "Approaching Target"
        metrics_60 = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 60,
                "suggestions_rejected": 30,
                "suggestions_modified": 10,
                "acceptance_rate": 60.0,
                "rejection_rate": 30.0,
                "modification_rate": 10.0,
                "actions_tracked": 1
            },
            "by_action": {}
        }

        report = generate_metrics_report.generate_markdown_report(metrics_60)
        assert "### ⚠️ Status: Approaching Target" in report

        # Just below 60% - should be "Below Target"
        metrics_59 = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 59,
                "suggestions_rejected": 30,
                "suggestions_modified": 11,
                "acceptance_rate": 59.0,
                "rejection_rate": 30.0,
                "modification_rate": 11.0,
                "actions_tracked": 1
            },
            "by_action": {}
        }

        report = generate_metrics_report.generate_markdown_report(metrics_59)
        assert "### 🔴 Status: Below Target" in report


class TestMain:
    """Test main entry point."""

    def test_main_with_valid_input_file(self, tmp_path, capsys):
        """Test main function with valid input file."""
        # Create input file
        input_path = tmp_path / "acceptance_rate.json"
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 2
            },
            "by_action": {
                "action-a": {
                    "suggestions_made": 50,
                    "suggestions_accepted": 45,
                    "suggestions_rejected": 3,
                    "suggestions_modified": 2,
                    "acceptance_rate": 90.0,
                    "rejection_rate": 6.0,
                    "modification_rate": 4.0,
                    "entries": 5
                }
            }
        }

        with open(input_path, 'w') as f:
            json.dump(metrics_data, f)

        output_path = tmp_path / "acceptance_report.md"

        # Run main
        import sys
        old_argv = sys.argv
        sys.argv = [
            "generate_metrics_report.py",
            "--input", str(input_path),
            "--output", str(output_path)
        ]

        try:
            result = generate_metrics_report.main()
        finally:
            sys.argv = old_argv

        captured = capsys.readouterr()

        # Verify return code
        assert result == 0

        # Verify output file was created
        assert output_path.exists()

        # Verify console output
        assert "Generating metrics report..." in captured.out
        assert f"Report saved to {output_path}" in captured.out
        assert "=== Preview ===" in captured.out
        assert "Acceptance Rate: 85.0%" in captured.out
        assert "Actions Tracked: 2" in captured.out

        # Verify report content
        report = output_path.read_text()
        assert "# Acceptance Rate Report" in report

    def test_main_with_nonexistent_input_file(self, tmp_path, capsys):
        """Test main function when input file doesn't exist."""
        input_path = tmp_path / "nonexistent.json"
        output_path = tmp_path / "acceptance_report.md"

        import sys
        old_argv = sys.argv
        sys.argv = [
            "generate_metrics_report.py",
            "--input", str(input_path),
            "--output", str(output_path)
        ]

        try:
            result = generate_metrics_report.main()
        finally:
            sys.argv = old_argv

        captured = capsys.readouterr()

        # Should return error code
        assert result == 1

        # Should show error message
        assert "Error: Input file" in captured.out
        assert "not found" in captured.out

    def test_main_creates_output_directory(self, tmp_path, capsys):
        """Test that main function creates output directory if needed."""
        # Create input file
        input_path = tmp_path / "acceptance_rate.json"
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 1
            },
            "by_action": {}
        }

        with open(input_path, 'w') as f:
            json.dump(metrics_data, f)

        # Create output path in non-existent subdirectory
        output_path = tmp_path / "subdir" / "nested" / "acceptance_report.md"

        import sys
        old_argv = sys.argv
        sys.argv = [
            "generate_metrics_report.py",
            "--input", str(input_path),
            "--output", str(output_path)
        ]

        try:
            result = generate_metrics_report.main()
        finally:
            sys.argv = old_argv

        # Should complete successfully
        assert result == 0

        # Should create parent directories
        assert output_path.parent.exists()
        assert output_path.exists()

    def test_main_with_no_metrics_data(self, tmp_path, capsys):
        """Test main function when metrics has no data."""
        # Create input file with no data
        input_path = tmp_path / "acceptance_rate.json"
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 0,
                "suggestions_accepted": 0,
                "suggestions_rejected": 0,
                "suggestions_modified": 0,
                "acceptance_rate": 0.0,
                "rejection_rate": 0.0,
                "modification_rate": 0.0,
                "actions_tracked": 0
            },
            "by_action": {}
        }

        with open(input_path, 'w') as f:
            json.dump(metrics_data, f)

        output_path = tmp_path / "acceptance_report.md"

        import sys
        old_argv = sys.argv
        sys.argv = [
            "generate_metrics_report.py",
            "--input", str(input_path),
            "--output", str(output_path)
        ]

        try:
            result = generate_metrics_report.main()
        finally:
            sys.argv = old_argv

        captured = capsys.readouterr()

        # Should complete successfully
        assert result == 0

        # Should show no data preview
        assert "No metrics data available yet" in captured.out

        # Report should be generated with no data message
        report = output_path.read_text()
        assert "### 📊 No Data Available" in report

    def test_main_default_paths(self, tmp_path, monkeypatch, capsys):
        """Test main function with default paths."""
        # Change to temp directory
        monkeypatch.chdir(tmp_path)

        # Create default metrics directory and file
        metrics_dir = tmp_path / "metrics"
        metrics_dir.mkdir()

        input_path = metrics_dir / "acceptance_rate.json"
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 50,
                "suggestions_accepted": 40,
                "suggestions_rejected": 8,
                "suggestions_modified": 2,
                "acceptance_rate": 80.0,
                "rejection_rate": 16.0,
                "modification_rate": 4.0,
                "actions_tracked": 1
            },
            "by_action": {}
        }

        with open(input_path, 'w') as f:
            json.dump(metrics_data, f)

        import sys
        old_argv = sys.argv
        sys.argv = ["generate_metrics_report.py"]

        try:
            result = generate_metrics_report.main()
        finally:
            sys.argv = old_argv

        # Should use default output path
        output_path = metrics_dir / "acceptance_report.md"
        assert result == 0
        assert output_path.exists()

    def test_main_source_file_added_to_metrics(self, tmp_path):
        """Test that main function adds source_file reference."""
        # Create input file
        input_path = tmp_path / "custom_metrics.json"
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 85,
                "suggestions_rejected": 10,
                "suggestions_modified": 5,
                "acceptance_rate": 85.0,
                "rejection_rate": 10.0,
                "modification_rate": 5.0,
                "actions_tracked": 1
            },
            "by_action": {}
        }

        with open(input_path, 'w') as f:
            json.dump(metrics_data, f)

        output_path = tmp_path / "acceptance_report.md"

        import sys
        old_argv = sys.argv
        sys.argv = [
            "generate_metrics_report.py",
            "--input", str(input_path),
            "--output", str(output_path)
        ]

        try:
            generate_metrics_report.main()
        finally:
            sys.argv = old_argv

        # Verify report includes source file
        report = output_path.read_text()
        # The source file path is converted to absolute path by the script
        assert "custom_metrics.json" in report


class TestIntegration:
    """Integration tests for full workflow."""

    def test_full_workflow_realistic_data(self, tmp_path):
        """Test complete workflow with realistic metrics data."""
        # Create input file with realistic metrics
        input_path = tmp_path / "acceptance_rate.json"
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 500,
                "suggestions_accepted": 420,
                "suggestions_rejected": 60,
                "suggestions_modified": 20,
                "acceptance_rate": 84.0,
                "rejection_rate": 12.0,
                "modification_rate": 4.0,
                "actions_tracked": 5
            },
            "by_action": {
                "review-and-merge": {
                    "suggestions_made": 200,
                    "suggestions_accepted": 180,
                    "suggestions_rejected": 15,
                    "suggestions_modified": 5,
                    "acceptance_rate": 90.0,
                    "rejection_rate": 7.5,
                    "modification_rate": 2.5,
                    "entries": 20,
                    "first_seen": "2026-01-15T00:00:00Z",
                    "last_seen": "2026-02-07T11:00:00Z"
                },
                "auto-refactor": {
                    "suggestions_made": 150,
                    "suggestions_accepted": 120,
                    "suggestions_rejected": 20,
                    "suggestions_modified": 10,
                    "acceptance_rate": 80.0,
                    "rejection_rate": 13.3,
                    "modification_rate": 6.7,
                    "entries": 15,
                    "first_seen": "2026-01-20T00:00:00Z",
                    "last_seen": "2026-02-07T10:00:00Z"
                },
                "auto-test": {
                    "suggestions_made": 100,
                    "suggestions_accepted": 70,
                    "suggestions_rejected": 20,
                    "suggestions_modified": 10,
                    "acceptance_rate": 70.0,
                    "rejection_rate": 20.0,
                    "modification_rate": 10.0,
                    "entries": 10,
                    "first_seen": "2026-02-01T00:00:00Z",
                    "last_seen": "2026-02-07T09:00:00Z"
                },
                "spec-to-code": {
                    "suggestions_made": 30,
                    "suggestions_accepted": 25,
                    "suggestions_rejected": 3,
                    "suggestions_modified": 2,
                    "acceptance_rate": 83.3,
                    "rejection_rate": 10.0,
                    "modification_rate": 6.7,
                    "entries": 5,
                    "first_seen": "2026-02-05T00:00:00Z",
                    "last_seen": "2026-02-07T08:00:00Z"
                },
                "code-review": {
                    "suggestions_made": 20,
                    "suggestions_accepted": 11,
                    "suggestions_rejected": 2,
                    "suggestions_modified": 7,
                    "acceptance_rate": 55.0,
                    "rejection_rate": 10.0,
                    "modification_rate": 35.0,
                    "entries": 3,
                    "first_seen": "2026-02-06T00:00:00Z",
                    "last_seen": "2026-02-07T07:00:00Z"
                }
            }
        }

        with open(input_path, 'w') as f:
            json.dump(metrics_data, f)

        output_path = tmp_path / "acceptance_report.md"

        # Run main
        import sys
        old_argv = sys.argv
        sys.argv = [
            "generate_metrics_report.py",
            "--input", str(input_path),
            "--output", str(output_path)
        ]

        try:
            result = generate_metrics_report.main()
        finally:
            sys.argv = old_argv

        # Verify success
        assert result == 0
        assert output_path.exists()

        # Verify comprehensive report
        report = output_path.read_text()

        # Verify overall summary
        assert "**Total Suggestions:** 500" in report
        assert "**Accepted:** 420 (84.0%)" in report

        # Verify status (84% >= 80%)
        assert "### ✅ Status: Target Achieved" in report

        # Verify all actions are present
        assert "### review-and-merge" in report
        assert "### auto-refactor" in report
        assert "### auto-test" in report
        assert "### spec-to-code" in report
        assert "### code-review" in report

        # Verify best performing action
        assert "### 🏆 Best Performing Action" in report
        assert "**review-and-merge:** 90.0% acceptance rate" in report

        # Verify actions needing improvement (< 60%)
        # code-review has 55% acceptance rate
        assert "### 🔧 Actions Needing Improvement" in report

        # Verify data points shown for actions with multiple entries
        assert "*Data points: 20*" in report
        assert "*Data points: 15*" in report

        # Verify timestamps shown
        assert "*First seen: 2026-01-15T00:00:00Z*" in report
        assert "*Last seen: 2026-02-07T11:00:00Z*" in report

    def test_edge_case_all_actions_below_target(self, tmp_path):
        """Test report when all actions are below target."""
        input_path = tmp_path / "acceptance_rate.json"
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 100,
                "suggestions_accepted": 45,
                "suggestions_rejected": 45,
                "suggestions_modified": 10,
                "acceptance_rate": 45.0,
                "rejection_rate": 45.0,
                "modification_rate": 10.0,
                "actions_tracked": 3
            },
            "by_action": {
                "action-a": {
                    "suggestions_made": 50,
                    "suggestions_accepted": 25,
                    "suggestions_rejected": 20,
                    "suggestions_modified": 5,
                    "acceptance_rate": 50.0,
                    "rejection_rate": 40.0,
                    "modification_rate": 10.0,
                    "entries": 5
                },
                "action-b": {
                    "suggestions_made": 30,
                    "suggestions_accepted": 12,
                    "suggestions_rejected": 15,
                    "suggestions_modified": 3,
                    "acceptance_rate": 40.0,
                    "rejection_rate": 50.0,
                    "modification_rate": 10.0,
                    "entries": 3
                },
                "action-c": {
                    "suggestions_made": 20,
                    "suggestions_accepted": 8,
                    "suggestions_rejected": 10,
                    "suggestions_modified": 2,
                    "acceptance_rate": 40.0,
                    "rejection_rate": 50.0,
                    "modification_rate": 10.0,
                    "entries": 2
                }
            }
        }

        with open(input_path, 'w') as f:
            json.dump(metrics_data, f)

        output_path = tmp_path / "acceptance_report.md"

        import sys
        old_argv = sys.argv
        sys.argv = [
            "generate_metrics_report.py",
            "--input", str(input_path),
            "--output", str(output_path)
        ]

        try:
            generate_metrics_report.main()
        finally:
            sys.argv = old_argv

        report = output_path.read_text()

        # All actions should be in needs improvement section
        assert "### 🔧 Actions Needing Improvement" in report
        assert "**action-a:** 50.0% acceptance rate" in report
        assert "**action-b:** 40.0% acceptance rate" in report
        assert "**action-c:** 40.0% acceptance rate" in report

    def test_edge_case_mixed_performance(self, tmp_path):
        """Test report with mixed performance across actions."""
        input_path = tmp_path / "acceptance_rate.json"
        metrics_data = {
            "timestamp": "2026-02-07T12:00:00Z",
            "overall": {
                "suggestions_made": 300,
                "suggestions_accepted": 210,
                "suggestions_rejected": 70,
                "suggestions_modified": 20,
                "acceptance_rate": 70.0,
                "rejection_rate": 23.3,
                "modification_rate": 6.7,
                "actions_tracked": 3
            },
            "by_action": {
                "excellent-action": {  # >= 80%
                    "suggestions_made": 100,
                    "suggestions_accepted": 90,
                    "suggestions_rejected": 8,
                    "suggestions_modified": 2,
                    "acceptance_rate": 90.0,
                    "rejection_rate": 8.0,
                    "modification_rate": 2.0,
                    "entries": 10
                },
                "approaching-action": {  # 60-79%
                    "suggestions_made": 100,
                    "suggestions_accepted": 70,
                    "suggestions_rejected": 22,
                    "suggestions_modified": 8,
                    "acceptance_rate": 70.0,
                    "rejection_rate": 22.0,
                    "modification_rate": 8.0,
                    "entries": 10
                },
                "needs-work-action": {  # < 60%
                    "suggestions_made": 100,
                    "suggestions_accepted": 50,
                    "suggestions_rejected": 40,
                    "suggestions_modified": 10,
                    "acceptance_rate": 50.0,
                    "rejection_rate": 40.0,
                    "modification_rate": 10.0,
                    "entries": 10
                }
            }
        }

        with open(input_path, 'w') as f:
            json.dump(metrics_data, f)

        output_path = tmp_path / "acceptance_report.md"

        import sys
        old_argv = sys.argv
        sys.argv = [
            "generate_metrics_report.py",
            "--input", str(input_path),
            "--output", str(output_path)
        ]

        try:
            generate_metrics_report.main()
        finally:
            sys.argv = old_argv

        report = output_path.read_text()

        # Verify different status indicators
        assert "✅ **Acceptance Rate:** 90.0%" in report
        assert "⚠️ **Acceptance Rate:** 70.0%" in report
        assert "🔴 **Acceptance Rate:** 50.0%" in report

        # Verify best performing action
        assert "### 🏆 Best Performing Action" in report
        assert "**excellent-action:** 90.0% acceptance rate" in report

        # Verify needs improvement section
        assert "### 🔧 Actions Needing Improvement" in report
        assert "**needs-work-action:** 50.0% acceptance rate" in report
