"""
Comprehensive tests for aggregate_metrics.py script.

Tests the aggregate_metrics module to ensure:
- Metrics files can be found correctly
- Metrics data can be loaded from JSON files
- Metrics are aggregated properly by action
- Edge cases are handled appropriately (empty dirs, invalid JSON, etc.)
- Overall metrics are calculated correctly
"""

import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import pytest

# Add scripts directory to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import aggregate_metrics


class TestFindMetricsFiles:
    """Test the find_metrics_files function."""

    def test_finds_files_in_metrics_directory(self, temp_dir):
        """Test finding files in the metrics/ directory."""
        # Create metrics directory with JSON files
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()
        (metrics_dir / "metrics1.json").write_text('{"test": "data"}')
        (metrics_dir / "metrics2.json").write_text('{"test": "data"}')

        files = aggregate_metrics.find_metrics_files(temp_dir)

        assert len(files) == 2
        assert all(path.endswith(".json") for path in files)

    def test_finds_files_in_dot_metrics_directory(self, temp_dir):
        """Test finding files in the .metrics/ directory."""
        # Create .metrics directory
        metrics_dir = Path(temp_dir) / ".metrics"
        metrics_dir.mkdir()
        (metrics_dir / "data.json").write_text('{"test": "data"}')

        files = aggregate_metrics.find_metrics_files(temp_dir)

        assert len(files) == 1
        assert files[0].endswith("data.json")

    def test_finds_files_in_audit_metrics_directory(self, temp_dir):
        """Test finding files in .audit/metrics/ directory."""
        # Create .audit/metrics directory
        metrics_dir = Path(temp_dir) / ".audit" / "metrics"
        metrics_dir.mkdir(parents=True)
        (metrics_dir / "audit_metrics.json").write_text('{"test": "data"}')

        files = aggregate_metrics.find_metrics_files(temp_dir)

        assert len(files) == 1
        assert "audit_metrics.json" in files[0]

    def test_searches_multiple_locations(self, temp_dir):
        """Test that all metric directories are searched."""
        # Create files in multiple locations
        (Path(temp_dir) / "metrics").mkdir()
        (Path(temp_dir) / "metrics" / "m1.json").write_text('{}')

        (Path(temp_dir) / ".metrics").mkdir()
        (Path(temp_dir) / ".metrics" / "m2.json").write_text('{}')

        (Path(temp_dir) / ".audit" / "metrics").mkdir(parents=True)
        (Path(temp_dir) / ".audit" / "metrics" / "m3.json").write_text('{}')

        files = aggregate_metrics.find_metrics_files(temp_dir)

        assert len(files) == 3

    def test_filters_by_modification_time(self, temp_dir):
        """Test filtering files by modification time."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()

        # Create an old file
        old_file = metrics_dir / "old.json"
        old_file.write_text('{"old": "data"}')

        # Set modification time to 10 days ago
        old_time = datetime.now() - timedelta(days=10)
        old_mtime = old_time.timestamp()
        os.utime(old_file, (old_mtime, old_mtime))

        # Create a new file
        new_file = metrics_dir / "new.json"
        new_file.write_text('{"new": "data"}')

        # Search for files modified in last 7 days
        since = datetime.now() - timedelta(days=7)
        files = aggregate_metrics.find_metrics_files(temp_dir, since)

        assert len(files) == 1
        assert "new.json" in files[0]
        assert "old.json" not in files[0]

    def test_handles_nonexistent_directories(self, temp_dir):
        """Test that nonexistent directories are skipped gracefully."""
        files = aggregate_metrics.find_metrics_files(temp_dir)
        assert files == []

    def test_handles_deeply_nested_files(self, temp_dir):
        """Test finding files in nested subdirectories."""
        metrics_dir = Path(temp_dir) / "metrics"
        nested_dir = metrics_dir / "level1" / "level2" / "level3"
        nested_dir.mkdir(parents=True)
        (nested_dir / "deep.json").write_text('{"deep": "data"}')

        files = aggregate_metrics.find_metrics_files(temp_dir)

        assert len(files) == 1
        assert "deep.json" in files[0]

    def test_non_json_files_ignored(self, temp_dir):
        """Test that non-JSON files are not included."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()
        (metrics_dir / "data.json").write_text('{}')
        (metrics_dir / "readme.md").write_text('# Documentation')
        (metrics_dir / "script.py").write_text('print("hello")')

        files = aggregate_metrics.find_metrics_files(temp_dir)

        assert len(files) == 1
        assert files[0].endswith("data.json")


class TestLoadMetricsData:
    """Test the load_metrics_data function."""

    def test_loads_single_object(self, temp_dir):
        """Test loading a JSON file with a single object."""
        metrics_file = Path(temp_dir) / "metrics.json"
        data = {
            "action": "test-action",
            "metrics": {"suggestions_made": 10, "suggestions_accepted": 5}
        }
        metrics_file.write_text(json.dumps(data))

        result = aggregate_metrics.load_metrics_data([str(metrics_file)])

        assert len(result) == 1
        assert result[0]["action"] == "test-action"
        assert result[0]["metrics"]["suggestions_made"] == 10

    def test_loads_list_of_objects(self, temp_dir):
        """Test loading a JSON file with a list of objects."""
        metrics_file = Path(temp_dir) / "metrics.json"
        data = [
            {"action": "action1", "metrics": {"suggestions_made": 10}},
            {"action": "action2", "metrics": {"suggestions_made": 20}}
        ]
        metrics_file.write_text(json.dumps(data))

        result = aggregate_metrics.load_metrics_data([str(metrics_file)])

        assert len(result) == 2
        assert result[0]["action"] == "action1"
        assert result[1]["action"] == "action2"

    def test_loads_multiple_files(self, temp_dir):
        """Test loading metrics from multiple files."""
        file1 = Path(temp_dir) / "metrics1.json"
        file1.write_text(json.dumps([{"action": "action1"}]))

        file2 = Path(temp_dir) / "metrics2.json"
        file2.write_text(json.dumps([{"action": "action2"}]))

        result = aggregate_metrics.load_metrics_data([str(file1), str(file2)])

        assert len(result) == 2
        assert result[0]["action"] == "action1"
        assert result[1]["action"] == "action2"

    def test_handles_invalid_json_gracefully(self, temp_dir, capsys):
        """Test that invalid JSON is handled with a warning."""
        invalid_file = Path(temp_dir) / "invalid.json"
        invalid_file.write_text('{"invalid": json}')

        result = aggregate_metrics.load_metrics_data([str(invalid_file)])

        assert result == []
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "invalid.json" in captured.out

    def test_handles_file_read_error(self, capsys):
        """Test that file read errors are handled gracefully."""
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            result = aggregate_metrics.load_metrics_data(["/fake/path.json"])

        assert result == []
        captured = capsys.readouterr()
        assert "Warning" in captured.out

    def test_handles_empty_file(self, temp_dir):
        """Test that empty JSON files are handled."""
        empty_file = Path(temp_dir) / "empty.json"
        empty_file.write_text('')

        result = aggregate_metrics.load_metrics_data([str(empty_file)])

        assert result == []

    def test_handles_mixed_valid_and_invalid_files(self, temp_dir):
        """Test loading with some valid and some invalid files."""
        valid_file = Path(temp_dir) / "valid.json"
        valid_file.write_text(json.dumps([{"action": "valid"}]))

        invalid_file = Path(temp_dir) / "invalid.json"
        invalid_file.write_text('not json')

        result = aggregate_metrics.load_metrics_data([
            str(valid_file),
            str(invalid_file)
        ])

        assert len(result) == 1
        assert result[0]["action"] == "valid"


class TestAggregateMetrics:
    """Test the aggregate_metrics function."""

    def test_aggregates_by_action(self):
        """Test that metrics are grouped by action."""
        metrics_data = [
            {
                "action": "action1",
                "metrics": {
                    "suggestions_made": 10,
                    "suggestions_accepted": 5,
                    "suggestions_rejected": 3,
                    "suggestions_modified": 2
                },
                "timestamp": "2024-01-01T00:00:00"
            },
            {
                "action": "action1",
                "metrics": {
                    "suggestions_made": 20,
                    "suggestions_accepted": 15,
                    "suggestions_rejected": 3,
                    "suggestions_modified": 2
                },
                "timestamp": "2024-01-02T00:00:00"
            },
            {
                "action": "action2",
                "metrics": {
                    "suggestions_made": 5,
                    "suggestions_accepted": 4,
                    "suggestions_rejected": 1,
                    "suggestions_modified": 0
                },
                "timestamp": "2024-01-03T00:00:00"
            }
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert "action1" in result
        assert "action2" in result

        assert result["action1"]["suggestions_made"] == 30
        assert result["action1"]["suggestions_accepted"] == 20
        assert result["action1"]["suggestions_rejected"] == 6
        assert result["action1"]["suggestions_modified"] == 4
        assert result["action1"]["entries"] == 2

        assert result["action2"]["suggestions_made"] == 5
        assert result["action2"]["suggestions_accepted"] == 4
        assert result["action2"]["entries"] == 1

    def test_filters_by_action_name(self):
        """Test filtering by specific action name."""
        metrics_data = [
            {"action": "action1", "metrics": {"suggestions_made": 10}},
            {"action": "action2", "metrics": {"suggestions_made": 20}},
            {"action": "action1", "metrics": {"suggestions_made": 5}},
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data, "action1")

        assert "action1" in result
        assert "action2" not in result
        assert result["action1"]["suggestions_made"] == 15

    def test_calculates_acceptance_rate(self):
        """Test that acceptance rate is calculated correctly."""
        metrics_data = [
            {
                "action": "test",
                "metrics": {
                    "suggestions_made": 100,
                    "suggestions_accepted": 60,
                    "suggestions_rejected": 30,
                    "suggestions_modified": 10
                }
            }
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert result["test"]["acceptance_rate"] == 60.0
        assert result["test"]["rejection_rate"] == 30.0
        assert result["test"]["modification_rate"] == 10.0

    def test_handles_zero_suggestions(self):
        """Test that zero suggestions doesn't cause division by zero."""
        metrics_data = [
            {
                "action": "test",
                "metrics": {
                    "suggestions_made": 0,
                    "suggestions_accepted": 0,
                    "suggestions_rejected": 0,
                    "suggestions_modified": 0
                }
            }
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert result["test"]["acceptance_rate"] == 0.0
        assert result["test"]["rejection_rate"] == 0.0
        assert result["test"]["modification_rate"] == 0.0

    def test_tracks_timestamps(self):
        """Test that first_seen and last_seen are tracked."""
        metrics_data = [
            {
                "action": "test",
                "metrics": {"suggestions_made": 10},
                "timestamp": "2024-01-01T00:00:00"
            },
            {
                "action": "test",
                "metrics": {"suggestions_made": 20},
                "timestamp": "2024-01-05T00:00:00"
            },
            {
                "action": "test",
                "metrics": {"suggestions_made": 15},
                "timestamp": "2024-01-03T00:00:00"
            }
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert result["test"]["first_seen"] == "2024-01-01T00:00:00"
        assert result["test"]["last_seen"] == "2024-01-05T00:00:00"

    def test_handles_missing_action_name(self):
        """Test entries without action name are grouped as 'unknown'."""
        metrics_data = [
            {"metrics": {"suggestions_made": 10}},
            {"action": "test", "metrics": {"suggestions_made": 5}}
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert "unknown" in result
        assert "test" in result
        assert result["unknown"]["suggestions_made"] == 10
        assert result["test"]["suggestions_made"] == 5

    def test_handles_missing_metrics(self):
        """Test entries without metrics dict."""
        metrics_data = [
            {"action": "test", "metrics": {"suggestions_made": 10}},
            {"action": "test"}  # No metrics field
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert result["test"]["suggestions_made"] == 10
        assert result["test"]["entries"] == 2

    def test_handles_partial_metrics(self):
        """Test entries with partial metric fields."""
        metrics_data = [
            {
                "action": "test",
                "metrics": {
                    "suggestions_made": 100,
                    "suggestions_accepted": 50
                    # Missing rejected and modified
                }
            }
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert result["test"]["suggestions_made"] == 100
        assert result["test"]["suggestions_accepted"] == 50
        assert result["test"]["suggestions_rejected"] == 0
        assert result["test"]["suggestions_modified"] == 0

    def test_handles_empty_metrics_list(self):
        """Test with empty metrics data list."""
        result = aggregate_metrics.aggregate_metrics([])

        assert result == {}

    def test_rounds_timestamps_correctly(self):
        """Test timestamp string comparison works correctly."""
        metrics_data = [
            {
                "action": "test",
                "metrics": {"suggestions_made": 10},
                "timestamp": "2024-01-01T10:00:00"
            },
            {
                "action": "test",
                "metrics": {"suggestions_made": 20},
                "timestamp": "2024-01-01T09:00:00"
            },
            {
                "action": "test",
                "metrics": {"suggestions_made": 30},
                "timestamp": "2024-01-01T11:00:00"
            }
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        # String comparison should work for ISO format timestamps
        assert result["test"]["first_seen"] == "2024-01-01T09:00:00"
        assert result["test"]["last_seen"] == "2024-01-01T11:00:00"


class TestCalculateOverallMetrics:
    """Test the calculate_overall_metrics function."""

    def test_calculates_totals(self):
        """Test that overall metrics are summed correctly."""
        aggregated = {
            "action1": {
                "suggestions_made": 100,
                "suggestions_accepted": 60,
                "suggestions_rejected": 30,
                "suggestions_modified": 10
            },
            "action2": {
                "suggestions_made": 50,
                "suggestions_accepted": 40,
                "suggestions_rejected": 5,
                "suggestions_modified": 5
            }
        }

        result = aggregate_metrics.calculate_overall_metrics(aggregated)

        assert result["suggestions_made"] == 150
        assert result["suggestions_accepted"] == 100
        assert result["suggestions_rejected"] == 35
        assert result["suggestions_modified"] == 15
        assert result["actions_tracked"] == 2

    def test_calculates_overall_rates(self):
        """Test that overall rates are calculated correctly."""
        aggregated = {
            "action1": {
                "suggestions_made": 100,
                "suggestions_accepted": 60,
                "suggestions_rejected": 30,
                "suggestions_modified": 10
            }
        }

        result = aggregate_metrics.calculate_overall_metrics(aggregated)

        assert result["acceptance_rate"] == 60.0
        assert result["rejection_rate"] == 30.0
        assert result["modification_rate"] == 10.0

    def test_handles_empty_aggregated_metrics(self):
        """Test with empty aggregated metrics."""
        result = aggregate_metrics.calculate_overall_metrics({})

        assert result["suggestions_made"] == 0
        assert result["suggestions_accepted"] == 0
        assert result["suggestions_rejected"] == 0
        assert result["suggestions_modified"] == 0
        assert result["actions_tracked"] == 0
        assert result["acceptance_rate"] == 0.0
        assert result["rejection_rate"] == 0.0
        assert result["modification_rate"] == 0.0

    def test_handles_zero_suggestions_overall(self):
        """Test overall metrics with zero total suggestions."""
        aggregated = {
            "action1": {
                "suggestions_made": 0,
                "suggestions_accepted": 0,
                "suggestions_rejected": 0,
                "suggestions_modified": 0
            }
        }

        result = aggregate_metrics.calculate_overall_metrics(aggregated)

        assert result["acceptance_rate"] == 0.0
        assert result["rejection_rate"] == 0.0
        assert result["modification_rate"] == 0.0

    def test_counts_actions_tracked(self):
        """Test that actions_tracked counts unique actions."""
        aggregated = {
            "action1": {
                "suggestions_made": 10,
                "suggestions_accepted": 5,
                "suggestions_rejected": 3,
                "suggestions_modified": 2
            },
            "action2": {
                "suggestions_made": 20,
                "suggestions_accepted": 10,
                "suggestions_rejected": 5,
                "suggestions_modified": 5
            },
            "action3": {
                "suggestions_made": 30,
                "suggestions_accepted": 15,
                "suggestions_rejected": 10,
                "suggestions_modified": 5
            }
        }

        result = aggregate_metrics.calculate_overall_metrics(aggregated)

        assert result["actions_tracked"] == 3


class TestMainFunction:
    """Test the main function and CLI interface."""

    def test_main_with_no_metrics_files(self, temp_dir, capsys):
        """Test main() when no metrics files exist."""
        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(Path(temp_dir) / "output.json")
        ]):
            aggregate_metrics.main()

        captured = capsys.readouterr()

        assert "No metrics files found" in captured.out
        assert "metrics will be collected" in captured.out.lower()

        # Check that output file was created with empty structure
        output_file = Path(temp_dir) / "output.json"
        assert output_file.exists()

        with open(output_file) as f:
            output_data = json.load(f)

        assert output_data["overall"]["suggestions_made"] == 0
        assert output_data["overall"]["actions_tracked"] == 0
        assert "note" in output_data

    def test_main_with_metrics_files(self, temp_dir, capsys):
        """Test main() with actual metrics files."""
        # Create metrics directory with test data
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()

        metrics_file = metrics_dir / "test_metrics.json"
        test_data = [{
            "action": "test-action",
            "metrics": {
                "suggestions_made": 10,
                "suggestions_accepted": 7,
                "suggestions_rejected": 2,
                "suggestions_modified": 1
            },
            "timestamp": "2024-01-01T00:00:00"
        }]
        metrics_file.write_text(json.dumps(test_data))

        output_path = Path(temp_dir) / "output.json"

        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(output_path)
        ]):
            aggregate_metrics.main()

        captured = capsys.readouterr()

        assert "Found 1 metrics file" in captured.out
        assert "Loaded 1 metric entries" in captured.out

        # Check output file
        assert output_path.exists()
        with open(output_path) as f:
            output_data = json.load(f)

        assert output_data["overall"]["suggestions_made"] == 10
        assert output_data["overall"]["acceptance_rate"] == 70.0
        assert "test-action" in output_data["by_action"]

    def test_main_with_time_filter(self, temp_dir):
        """Test main() with --since argument."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()

        # Create old and new files
        old_file = metrics_dir / "old.json"
        old_file.write_text('[]')
        old_time = datetime.now() - timedelta(days=10)
        os.utime(old_file, (old_time.timestamp(), old_time.timestamp()))

        new_file = metrics_dir / "new.json"
        new_file.write_text(json.dumps([{
            "action": "test",
            "metrics": {"suggestions_made": 5}
        }]))

        output_path = Path(temp_dir) / "output.json"

        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(output_path),
            "--since", "7 days ago"
        ]):
            aggregate_metrics.main()

        with open(output_path) as f:
            output_data = json.load(f)

        # Should only include new file
        assert output_data["overall"]["suggestions_made"] == 5

    def test_main_with_action_filter(self, temp_dir):
        """Test main() with --action filter."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()

        metrics_file = metrics_dir / "metrics.json"
        test_data = [
            {"action": "action1", "metrics": {"suggestions_made": 10}},
            {"action": "action2", "metrics": {"suggestions_made": 20}}
        ]
        metrics_file.write_text(json.dumps(test_data))

        output_path = Path(temp_dir) / "output.json"

        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(output_path),
            "--action", "action1"
        ]):
            aggregate_metrics.main()

        with open(output_path) as f:
            output_data = json.load(f)

        # Should only include action1
        assert "action1" in output_data["by_action"]
        assert "action2" not in output_data["by_action"]
        assert output_data["overall"]["suggestions_made"] == 10

    def test_main_creates_output_directory(self, temp_dir):
        """Test that main() creates output directory if needed."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()
        (metrics_dir / "test.json").write_text('[]')

        # Output in nested directory that doesn't exist
        output_path = Path(temp_dir) / "nested" / "dir" / "output.json"

        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(output_path)
        ]):
            aggregate_metrics.main()

        assert output_path.exists()
        assert output_path.parent.exists()

    def test_main_prints_summary(self, temp_dir, capsys):
        """Test that main() prints summary when metrics exist."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()

        metrics_file = metrics_dir / "test.json"
        metrics_file.write_text(json.dumps([{
            "action": "test",
            "metrics": {
                "suggestions_made": 100,
                "suggestions_accepted": 60,
                "suggestions_rejected": 30,
                "suggestions_modified": 10
            }
        }]))

        output_path = Path(temp_dir) / "output.json"

        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(output_path)
        ]):
            aggregate_metrics.main()

        captured = capsys.readouterr()

        assert "=== Summary ===" in captured.out
        assert "Total suggestions: 100" in captured.out
        assert "Acceptance rate: 60.00%" in captured.out
        assert "Rejection rate: 30.00%" in captured.out
        assert "Modification rate: 10.00%" in captured.out
        assert "Actions tracked: 1" in captured.out

    def test_main_with_invalid_time_range(self, temp_dir, capsys):
        """Test main() with invalid time range format."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()
        (metrics_dir / "test.json").write_text('[]')

        output_path = Path(temp_dir) / "output.json"

        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(output_path),
            "--since", "invalid days ago"  # This will trigger ValueError
        ]):
            aggregate_metrics.main()

        captured = capsys.readouterr()

        # Should show warning but continue
        assert "Warning" in captured.out
        assert "Could not parse time range" in captured.out

    def test_main_parses_days_ago(self, temp_dir):
        """Test parsing 'X days ago' format."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()

        # Create file modified 3 days ago
        metrics_file = metrics_dir / "test.json"
        metrics_file.write_text(json.dumps([{
            "action": "test",
            "metrics": {"suggestions_made": 10}
        }]))
        old_time = datetime.now() - timedelta(days=3)
        os.utime(metrics_file, (old_time.timestamp(), old_time.timestamp()))

        output_path = Path(temp_dir) / "output.json"

        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(output_path),
            "--since", "5 days ago"
        ]):
            aggregate_metrics.main()

        with open(output_path) as f:
            output_data = json.load(f)

        # Should include the 3-day-old file
        assert output_data["overall"]["suggestions_made"] == 10

    def test_main_parses_hours_ago(self, temp_dir):
        """Test parsing 'X hours ago' format."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()

        metrics_file = metrics_dir / "test.json"
        metrics_file.write_text(json.dumps([{
            "action": "test",
            "metrics": {"suggestions_made": 10}
        }]))

        output_path = Path(temp_dir) / "output.json"

        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(output_path),
            "--since", "2 hours ago"
        ]):
            aggregate_metrics.main()

        # Recent file should be included
        with open(output_path) as f:
            output_data = json.load(f)
        assert output_data["overall"]["suggestions_made"] == 10

    def test_main_parses_minutes_ago(self, temp_dir):
        """Test parsing 'X minutes ago' format."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()

        metrics_file = metrics_dir / "test.json"
        metrics_file.write_text(json.dumps([{
            "action": "test",
            "metrics": {"suggestions_made": 10}
        }]))

        output_path = Path(temp_dir) / "output.json"

        with patch("sys.argv", [
            "aggregate_metrics.py",
            "--root-dir", temp_dir,
            "--output", str(output_path),
            "--since", "30 minutes ago"
        ]):
            aggregate_metrics.main()

        # Recent file should be included
        with open(output_path) as f:
            output_data = json.load(f)
        assert output_data["overall"]["suggestions_made"] == 10


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_corrupted_json_files(self, temp_dir, capsys):
        """Test handling of corrupted JSON files."""
        metrics_dir = Path(temp_dir) / "metrics"
        metrics_dir.mkdir()

        # Create corrupted file
        (metrics_dir / "corrupted.json").write_text('{invalid json}')

        # Create valid file
        valid_file = metrics_dir / "valid.json"
        valid_file.write_text(json.dumps([{
            "action": "test",
            "metrics": {"suggestions_made": 10}
        }]))

        files = aggregate_metrics.find_metrics_files(temp_dir)
        metrics_data = aggregate_metrics.load_metrics_data(files)

        # Should load only the valid file
        assert len(metrics_data) == 1
        assert metrics_data[0]["action"] == "test"

        captured = capsys.readouterr()
        assert "Warning" in captured.out

    def test_malformed_metrics_entries(self):
        """Test aggregation with malformed entries."""
        metrics_data = [
            {"action": "test", "metrics": {"suggestions_made": 10}},
            {},  # Completely empty
            {"action": "test"},  # No metrics
            {"metrics": {"suggestions_made": 5}},  # No action
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert "test" in result
        assert "unknown" in result
        assert result["test"]["suggestions_made"] == 10
        assert result["unknown"]["suggestions_made"] == 5

    def test_very_long_action_names(self):
        """Test with unusually long action names."""
        long_name = "a" * 1000
        metrics_data = [{
            "action": long_name,
            "metrics": {"suggestions_made": 10}
        }]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert long_name in result
        assert result[long_name]["suggestions_made"] == 10

    def test_unicode_in_action_names(self):
        """Test with Unicode characters in action names."""
        metrics_data = [{
            "action": "test-acción-测试",
            "metrics": {"suggestions_made": 10}
        }]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert "test-acción-测试" in result

    def test_negative_metric_values(self):
        """Test handling of negative metric values."""
        metrics_data = [{
            "action": "test",
            "metrics": {
                "suggestions_made": -10,
                "suggestions_accepted": -5
            }
        }]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        # Should aggregate as-is (validation is not responsibility of this module)
        assert result["test"]["suggestions_made"] == -10
        assert result["test"]["suggestions_accepted"] == -5

    def test_fractional_metric_values(self):
        """Test handling of fractional metric values."""
        metrics_data = [{
            "action": "test",
            "metrics": {
                "suggestions_made": 10.5,
                "suggestions_accepted": 5.3
            }
        }]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert result["test"]["suggestions_made"] == 10.5
        assert result["test"]["acceptance_rate"] == pytest.approx(50.48, rel=0.1)

    def test_missing_timestamp_field(self):
        """Test entries without timestamp field."""
        metrics_data = [
            {
                "action": "test",
                "metrics": {"suggestions_made": 10},
                "timestamp": "2024-01-01T00:00:00"
            },
            {
                "action": "test",
                "metrics": {"suggestions_made": 20}
                # No timestamp
            }
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        # Should handle gracefully
        assert result["test"]["first_seen"] == "2024-01-01T00:00:00"
        assert result["test"]["last_seen"] == "2024-01-01T00:00:00"

    def test_empty_timestamp_field(self):
        """Test entries with empty timestamp field."""
        metrics_data = [{
            "action": "test",
            "metrics": {"suggestions_made": 10},
            "timestamp": ""
        }]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        # Should handle empty string
        assert result["test"]["first_seen"] == ""
        assert result["test"]["last_seen"] == ""

    def test_very_large_metric_values(self):
        """Test with very large metric values."""
        metrics_data = [{
            "action": "test",
            "metrics": {
                "suggestions_made": 10**15,
                "suggestions_accepted": 10**14
            }
        }]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        assert result["test"]["suggestions_made"] == 10**15
        assert result["test"]["acceptance_rate"] == 10.0

    def test_multiple_actions_with_same_name(self):
        """Test that same action name gets aggregated together."""
        metrics_data = [
            {"action": "test", "metrics": {"suggestions_made": 10}},
            {"action": "test", "metrics": {"suggestions_made": 20}},
            {"action": "TEST", "metrics": {"suggestions_made": 30}}  # Different case
        ]

        result = aggregate_metrics.aggregate_metrics(metrics_data)

        # Case-sensitive, so "test" and "TEST" are different
        assert "test" in result
        assert "TEST" in result
        assert result["test"]["suggestions_made"] == 30
        assert result["TEST"]["suggestions_made"] == 30
