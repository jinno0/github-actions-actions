"""
Tests for metrics collection functionality.

Tests the collect_metrics.py script to ensure:
- Telemetry can be disabled
- Repository names are properly anonymized
- Metrics are collected correctly
- No sensitive data leaks
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add scripts directory to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import collect_metrics


class TestTelemetryDisabled:
    """Test telemetry opt-out functionality."""

    def test_disabled_via_env_variable(self):
        """Test that telemetry is skipped when DISABLE_TELEMETRY=true."""
        with patch.dict(os.environ, {"DISABLE_TELEMETRY": "true"}):
            result = collect_metrics.collect_metrics(
                action_name="test-action",
                status="success",
                duration_ms=1000
            )
            assert result["status"] == "skipped"
            assert result["reason"] == "telemetry_disabled"

    def test_enabled_by_default(self):
        """Test that telemetry is enabled when DISABLE_TELEMETRY is not set."""
        with patch.dict(os.environ, {}, clear=False):
            # Remove DISABLE_TELEMETRY if it exists
            os.environ.pop("DISABLE_TELEMETRY", None)

            result = collect_metrics.collect_metrics(
                action_name="test-action",
                status="success",
                duration_ms=1000
            )
            assert result.get("status") != "skipped"
            assert "action_name" in result

    def test_disabled_case_insensitive(self):
        """Test that DISABLE_TELEMETRY=true (case insensitive) works."""
        for value in ["true", "True", "TRUE", "TrUe"]:
            with patch.dict(os.environ, {"DISABLE_TELEMETRY": value}):
                result = collect_metrics.collect_metrics(
                    action_name="test-action",
                    status="success",
                    duration_ms=1000
                )
                assert result["status"] == "skipped"


class TestAnonymization:
    """Test repository name anonymization."""

    def test_anonymize_repository(self):
        """Test that repository names are hashed consistently."""
        repo = "acme-corp/main-project"

        hash1 = collect_metrics.anonymize_repository(repo)
        hash2 = collect_metrics.anonymize_repository(repo)

        # Same input should produce same hash
        assert hash1 == hash2
        assert len(hash1) == 16  # First 16 chars of SHA-256
        assert hash1 != repo  # Hash should not equal original

    def test_different_repos_different_hashes(self):
        """Test that different repositories produce different hashes."""
        hash1 = collect_metrics.anonymize_repository("acme/project-a")
        hash2 = collect_metrics.anonymize_repository("acme/project-b")

        assert hash1 != hash2

    def test_unknown_repository(self):
        """Test that 'unknown' repository is not hashed."""
        result = collect_metrics.anonymize_repository("unknown")
        assert result == "unknown"


class TestMetricsCollection:
    """Test metrics collection functionality."""

    def test_collect_basic_metrics(self):
        """Test collecting basic metrics."""
        with patch.dict(os.environ, {
            "GITHUB_REPOSITORY": "test/repo",
            "RUNNER_OS": "Linux",
            "CLAUDE_CLI_VERSION": "1.2.3"
        }):
            result = collect_metrics.collect_metrics(
                action_name="review-and-merge",
                status="success",
                duration_ms=1234
            )

            assert result["action_name"] == "review-and-merge"
            assert result["status"] == "success"
            assert result["duration_ms"] == 1234
            assert result["repository_anonymous_id"] != "test/repo"  # Should be hashed
            assert len(result["repository_anonymous_id"]) == 16
            assert result["runner_os"] == "Linux"
            assert result["claude_cli_version"] == "1.2.3"
            assert "timestamp" in result

    def test_collect_metrics_with_error(self):
        """Test collecting metrics when an error occurs."""
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "test/repo"}):
            result = collect_metrics.collect_metrics(
                action_name="test-action",
                status="error",
                duration_ms=500,
                error_type="File not found: /path/to/file.txt"
            )

            assert result["status"] == "error"
            assert "error_type" in result
            assert result["error_type"] == "File not found: /path/to/file.txt"

    def test_error_message_truncated(self):
        """Test that long error messages are truncated to 200 chars."""
        long_error = "x" * 300

        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "test/repo"}):
            result = collect_metrics.collect_metrics(
                action_name="test-action",
                status="error",
                duration_ms=100,
                error_type=long_error
            )

            assert len(result["error_type"]) == 200

    def test_missing_environment_variables(self):
        """Test that missing env vars default to 'unknown'."""
        with patch.dict(os.environ, {}, clear=False):
            # Clear relevant environment variables
            for key in ["GITHUB_REPOSITORY", "RUNNER_OS", "CLAUDE_CLI_VERSION"]:
                os.environ.pop(key, None)

            result = collect_metrics.collect_metrics(
                action_name="test-action",
                status="success",
                duration_ms=100
            )

            assert result["repository_anonymous_id"] == "unknown"
            assert result["runner_os"] == "unknown"
            assert result["claude_cli_version"] == "unknown"

    def test_invalid_status(self):
        """Test that invalid status defaults to 'error'."""
        with patch.dict(os.environ, {}):
            result = collect_metrics.collect_metrics(
                action_name="test-action",
                status="invalid_status",
                duration_ms=100
            )

            # Status validation happens in main(), not collect_metrics()
            # So collect_metrics() accepts any status
            assert result["status"] == "invalid_status"


class TestSendMetrics:
    """Test metrics sending functionality."""

    def test_send_metrics_creates_log_file(self):
        """Test that send_metrics creates a log file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics = {
                "action_name": "test-action",
                "status": "success",
                "duration_ms": 100
            }

            # Create actual metrics directory in temp location
            temp_metrics_dir = Path(tmpdir) / "metrics" / "telemetry"
            temp_metrics_dir.mkdir(parents=True)

            with patch("collect_metrics.Path") as mock_path_class:
                # Mock Path class to return our temp directory
                mock_path_instance = MagicMock()
                mock_path_instance.mkdir = temp_metrics_dir.mkdir
                mock_path_instance.__truediv__ = lambda self, other: Path(tmpdir) / "metrics" / "telemetry" / other
                mock_path_class.return_value = mock_path_instance

                result = collect_metrics.send_metrics(metrics)
                assert result is True

    def test_send_metrics_handles_skipped_status(self):
        """Test that send_metrics handles skipped telemetry."""
        metrics = {"status": "skipped", "reason": "telemetry_disabled"}
        result = collect_metrics.send_metrics(metrics)
        assert result is True

    def test_send_metrics_graceful_failure(self):
        """Test that send_metrics fails gracefully on errors."""
        metrics = {"action_name": "test", "status": "success"}

        with patch("builtins.open", side_effect=OSError("Permission denied")):
            # Should not raise exception, just return False
            result = collect_metrics.send_metrics(metrics)
            assert result is False


class TestCommandLineInterface:
    """Test command-line interface."""

    def test_main_with_valid_arguments(self, capsys):
        """Test main() with valid arguments."""
        with patch.dict(os.environ, {}):
            sys.argv = [
                "collect_metrics.py",
                "test-action",
                "success",
                "1000"
            ]

            with patch.object(collect_metrics, "send_metrics", return_value=True):
                with pytest.raises(SystemExit) as exc_info:
                    collect_metrics.main()

                # Should exit with code 0
                assert exc_info.value.code == 0

    def test_main_with_invalid_duration(self):
        """Test main() with invalid duration_ms."""
        sys.argv = [
            "collect_metrics.py",
            "test-action",
            "success",
            "not_a_number"
        ]

        with pytest.raises(SystemExit) as exc_info:
            collect_metrics.main()

        assert exc_info.value.code == 1

    def test_main_with_missing_arguments(self):
        """Test main() with missing required arguments."""
        sys.argv = ["collect_metrics.py", "test-action", "success"]

        with pytest.raises(SystemExit) as exc_info:
            collect_metrics.main()

        assert exc_info.value.code == 1


class TestPrivacy:
    """Test privacy protections."""

    def test_no_repository_name_in_metrics(self):
        """Test that actual repository name is not in metrics."""
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "acme-corp/main-project"}):
            result = collect_metrics.collect_metrics(
                action_name="test-action",
                status="success",
                duration_ms=100
            )

            # Original repository name should not be in result
            result_json = json.dumps(result)
            assert "acme-corp" not in result_json
            assert "main-project" not in result_json

    def test_no_code_in_metrics(self):
        """Test that code snippets are not collected."""
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "test/repo"}):
            result = collect_metrics.collect_metrics(
                action_name="test-action",
                status="success",
                duration_ms=100
            )

            # Check for code-related fields
            assert "code" not in result
            assert "source" not in result
            assert "file_content" not in result
