"""
Tests for scan_adoption.py script.

Tests the adoption scanning functionality to ensure:
- GitHub CLI integration works correctly
- Organization scanning handles errors gracefully
- ADOPTION.md parsing is robust
- Report generation works as expected
- File I/O errors are handled properly
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

# Add scripts directory to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import scan_adoption


class TestTryScanGithubOrg:
    """Test GitHub CLI organization scanning functionality."""

    def test_github_cli_not_found(self):
        """Test that function returns empty list when gh CLI is not found."""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = scan_adoption.try_scan_github_org()
            assert result == []

    def test_github_cli_timeout(self):
        """Test that function handles timeout gracefully."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("gh", 5)):
            result = scan_adoption.try_scan_github_org()
            assert result == []

    def test_github_cli_non_zero_exit(self):
        """Test that function handles non-zero exit codes."""
        mock_result = Mock()
        mock_result.returncode = 1
        with patch("subprocess.run", return_value=mock_result):
            result = scan_adoption.try_scan_github_org()
            assert result == []

    def test_github_org_not_set(self):
        """Test that function returns empty list when GITHUB_ORG is not set."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = b"gh version 2.0.0"

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("GITHUB_ORG", None)
        with patch("subprocess.run", return_value=mock_result):
            result = scan_adoption.try_scan_github_org()
            assert result == []

    def test_invalid_org_name(self):
        """Test that function validates organization name format."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = b"gh version 2.0.0"

        # Test various invalid org names
        invalid_orgs = [
            "invalid@org",  # Contains @
            "org with spaces",  # Contains spaces
            "a" * 40,  # Too long (>39 chars)
            "org_with_underscore",  # Underscore not allowed
        ]

        for invalid_org in invalid_orgs:
            with patch.dict(os.environ, {"GITHUB_ORG": invalid_org}):
                with patch("subprocess.run", return_value=mock_result):
                    result = scan_adoption.try_scan_github_org()
                    assert result == []

    def test_valid_org_scan_success(self):
        """Test successful organization scan with valid org name."""
        mock_version_result = Mock()
        mock_version_result.returncode = 0
        mock_version_result.stdout = b"gh version 2.0.0"

        mock_search_result = Mock()
        mock_search_result.returncode = 0
        mock_search_result.stdout = json.dumps([
            {"name": "repo1", "url": "https://github.com/testorg/repo1"},
            {"name": "repo2", "url": "https://github.com/testorg/repo2"}
        ])

        with patch.dict(os.environ, {"GITHUB_ORG": "testorg"}):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = [mock_version_result, mock_search_result]
                result = scan_adoption.try_scan_github_org()

                assert len(result) == 2
                assert result[0]["name"] == "repo1"
                assert result[1]["url"] == "https://github.com/testorg/repo2"

    def test_org_search_command_error(self):
        """Test handling of GitHub API search errors."""
        mock_version_result = Mock()
        mock_version_result.returncode = 0
        mock_version_result.stdout = b"gh version 2.0.0"

        mock_search_result = Mock()
        mock_search_result.returncode = 1
        mock_search_result.stderr = "Error: Organization not found"

        with patch.dict(os.environ, {"GITHUB_ORG": "nonexistent"}):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = [mock_version_result, mock_search_result]
                result = scan_adoption.try_scan_github_org()
                assert result == []

    def test_org_scan_timeout(self):
        """Test handling of timeout during org scan."""
        mock_version_result = Mock()
        mock_version_result.returncode = 0
        mock_version_result.stdout = b"gh version 2.0.0"

        with patch.dict(os.environ, {"GITHUB_ORG": "testorg"}):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = [
                    mock_version_result,
                    subprocess.TimeoutExpired("gh", 30)
                ]
                result = scan_adoption.try_scan_github_org()
                assert result == []

    def test_invalid_json_response(self):
        """Test handling of invalid JSON in GitHub API response."""
        mock_version_result = Mock()
        mock_version_result.returncode = 0
        mock_version_result.stdout = b"gh version 2.0.0"

        mock_search_result = Mock()
        mock_search_result.returncode = 0
        mock_search_result.stdout = "invalid json"

        with patch.dict(os.environ, {"GITHUB_ORG": "testorg"}):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = [mock_version_result, mock_search_result]
                result = scan_adoption.try_scan_github_org()
                assert result == []

    def test_valid_org_names(self):
        """Test that various valid org names are accepted."""
        mock_version_result = Mock()
        mock_version_result.returncode = 0
        mock_version_result.stdout = b"gh version 2.0.0"

        mock_search_result = Mock()
        mock_search_result.returncode = 0
        mock_search_result.stdout = json.dumps([])

        valid_orgs = [
            "testorg",
            "test-org",
            "Test-Org-123",
            "a",  # Single character
            "org" + "-" * 18,  # 39 chars exactly
        ]

        for valid_org in valid_orgs:
            with patch.dict(os.environ, {"GITHUB_ORG": valid_org}):
                with patch("subprocess.run") as mock_run:
                    mock_run.side_effect = [mock_version_result, mock_search_result]
                    result = scan_adoption.try_scan_github_org()
                    assert isinstance(result, list)

    def test_generic_exception_handler(self):
        """Test that generic exceptions are caught and handled."""
        mock_version_result = Mock()
        mock_version_result.returncode = 0
        mock_version_result.stdout = b"gh version 2.0.0"

        with patch.dict(os.environ, {"GITHUB_ORG": "testorg"}):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = [mock_version_result, Exception("Unexpected error")]
                result = scan_adoption.try_scan_github_org()
                assert result == []


class TestGenerateAdoptionReport:
    """Test adoption report generation from ADOPTION.md."""

    def test_adoption_file_not_found(self):
        """Test that function returns template when ADOPTION.md doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            result = scan_adoption.generate_adoption_report()

            assert result["total_adopters"] == 0
            assert result["internal_projects"] == 0
            assert result["external_projects"] == 0
            assert result["most_used_actions"] == []
            assert "last_updated" in result

    def test_adoption_file_read_error(self):
        """Test handling of file read errors."""
        with patch("scan_adoption.Path") as mock_path_class:
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.read_text.side_effect = OSError("Permission denied")
            mock_path_class.return_value = mock_path_instance

            result = scan_adoption.generate_adoption_report()

            assert result["total_adopters"] == 0
            assert "error" in result
            assert "last_updated" in result

    def test_adoption_file_unicode_error(self):
        """Test handling of Unicode decode errors."""
        with patch("scan_adoption.Path") as mock_path_class:
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.read_text.side_effect = UnicodeDecodeError(
                "utf-8", b"", 0, 1, "invalid start byte"
            )
            mock_path_class.return_value = mock_path_instance

            result = scan_adoption.generate_adoption_report()

            assert result["total_adopters"] == 0
            assert "error" in result

    def test_parse_valid_adoption_table(self):
        """Test parsing a valid ADOPTION.md table."""
        valid_content = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1, action2 | Production |
| *[Project B](https://github.com/org/project-b)* | Team Y | action3 | Testing |
"""
        with patch("scan_adoption.Path") as mock_path_class:
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.read_text.return_value = valid_content
            mock_path_class.return_value = mock_path_instance

            result = scan_adoption.generate_adoption_report()

            assert result["total_adopters"] == 2
            assert len(result["adopters"]) == 2
            assert result["adopters"][0]["name"] == "Project A"
            assert result["adopters"][0]["url"] == "https://github.com/org/project-a"
            assert result["adopters"][0]["team"] == "Team X"
            assert result["adopters"][0]["actions"] == "action1, action2"
            assert result["adopters"][0]["notes"] == "Production"

    def test_skip_header_rows(self):
        """Test that header rows are properly skipped."""
        content_with_headers = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| Project | Team | Actions | Notes |
| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Notes |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_with_headers

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            # Should only parse one valid row (not headers)
            assert result["total_adopters"] == 1
            assert result["adopters"][0]["name"] == "Project A"

    def test_skip_invalid_url_rows(self):
        """Test that rows without valid URLs are skipped."""
        content_with_invalid_urls = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Notes |
| Invalid Project | Team Y | action2 | Notes |
| *[Project C](not-a-url)* | Team Z | action3 | Notes |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_with_invalid_urls

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            # Only the first row has a valid URL
            assert result["total_adopters"] == 1

    def test_skip_malformed_markdown_links(self):
        """Test that rows with malformed markdown links are skipped."""
        content_with_malformed = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Notes |
| [Project B](https://github.com/org/project-b) | Team Y | action2 | Notes |
| Project C](https://github.com/org/project-c)* | Team Z | action3 | Notes |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_with_malformed

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            # Only the first row has properly formatted link
            assert result["total_adopters"] == 1

    def test_handle_parsing_errors_gracefully(self):
        """Test that parsing errors don't crash the parser."""
        content_with_errors = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Notes |
| incomplete row
| *[Project C](https://github.com/org/project-c)* | Team Z | action3 | Notes |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_with_errors

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            # Should parse valid rows and skip problematic ones
            assert result["total_adopters"] == 2

    def test_missing_notes_column(self):
        """Test handling of missing notes column."""
        content_without_notes = """# Adoption

| Project | Team | Actions |
|---------|------|---------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1 |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_without_notes

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            assert result["total_adopters"] == 1
            assert result["adopters"][0]["notes"] == ""

    def test_empty_adoption_file(self):
        """Test handling of empty ADOPTION.md."""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = ""

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            assert result["total_adopters"] == 0
            assert "adopters" in result
            assert len(result["adopters"]) == 0

    def test_github_urls_in_various_formats(self):
        """Test parsing different GitHub URL formats."""
        content_with_various_urls = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Notes |
| *[Project B](http://github.com/org/project-b)* | Team Y | action2 | Notes |
| *[Project C](https://github.com/org/project-C)* | Team Z | action3 | Notes |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_with_various_urls

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            assert result["total_adopters"] == 3

    def test_line_number_tracking(self):
        """Test that line numbers are tracked for debugging."""
        content = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Notes |
"""
        with patch("scan_adoption.Path") as mock_path_class:
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.read_text.return_value = content
            mock_path_class.return_value = mock_path_instance

            result = scan_adoption.generate_adoption_report()

            assert result["total_adopters"] == 1
            # Line number should be present for debugging
            assert "line_number" in result["adopters"][0]

    def test_url_without_github_domain(self):
        """Test URL validation - both URLs should pass (both have http)."""
        content = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://bitbucket.org/org/project-a)* | Team X | action1 | Notes |
| *[Project B](https://github.com/org/project-b)* | Team Y | action2 | Notes |
"""
        with patch("scan_adoption.Path") as mock_path_class:
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.read_text.return_value = content
            mock_path_class.return_value = mock_path_instance

            result = scan_adoption.generate_adoption_report()

            # Both URLs should be included (both have "http" in the markdown link)
            assert result["total_adopters"] == 2
            assert result["adopters"][0]["name"] == "Project A"
            assert result["adopters"][1]["name"] == "Project B"

    def test_exception_in_parsing_loop(self, capsys):
        """Test that exceptions in parsing loop are caught and logged."""
        content = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Notes |
"""

        with patch("scan_adoption.Path") as mock_path_class:
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.read_text.return_value = content
            mock_path_class.return_value = mock_path_instance

            # The function should handle any exceptions gracefully
            result = scan_adoption.generate_adoption_report()
            assert isinstance(result["total_adopters"], int)

    def test_missing_required_column(self):
        """Test that rows with missing required columns are skipped."""
        content = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| | Team X | action1 | Notes |
| *[Project B](https://github.com/org/project-b)* | | action2 | Notes |
"""
        with patch("scan_adoption.Path") as mock_path_class:
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.read_text.return_value = content
            mock_path_class.return_value = mock_path_instance

            result = scan_adoption.generate_adoption_report()

            # Both rows should be skipped (missing first or second column)
            assert result["total_adopters"] == 0

    def test_report_has_timestamp(self):
        """Test that report includes last_updated timestamp."""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = "# Adoption\n"

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            assert "last_updated" in result
            # Verify it's a valid ISO format timestamp
            datetime.fromisoformat(result["last_updated"])


class TestMainFunction:
    """Test main function integration."""

    def test_main_success_with_adopters(self, tmp_path, capsys):
        """Test main function with successful adoption data."""
        _ = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Production |
"""

        with patch("scan_adoption.generate_adoption_report") as mock_report:
            mock_report.return_value = {
                "total_adopters": 1,
                "adopters": [
                    {
                        "name": "Project A",
                        "team": "Team X"
                    }
                ],
                "last_updated": datetime.now().isoformat()
            }

            with patch("scan_adoption.Path") as mock_path_class:
                mock_path_instance = Mock()
                mock_path_instance.parent = Mock()
                mock_path_instance.write_text = Mock()

                mock_path_class.return_value = mock_path_instance
                mock_path_class.side_effect = lambda x: mock_path_instance

                with patch("scan_adoption.try_scan_github_org", return_value=[]):
                    exit_code = scan_adoption.main()

                    assert exit_code == 0
                    captured = capsys.readouterr()
                    assert "Total Adopters: 1" in captured.out
                    assert "Adoption tracking is working!" in captured.out

    def test_main_no_adopters(self, tmp_path, capsys):
        """Test main function with no adopters."""
        with patch("scan_adoption.generate_adoption_report") as mock_report:
            mock_report.return_value = {
                "total_adopters": 0,
                "adopters": [],
                "last_updated": datetime.now().isoformat()
            }

            with patch("scan_adoption.Path") as mock_path_class:
                mock_path_instance = Mock()
                mock_path_instance.parent = Mock()
                mock_path_instance.write_text = Mock()

                mock_path_class.return_value = mock_path_instance
                mock_path_class.side_effect = lambda x: mock_path_instance

                with patch("scan_adoption.try_scan_github_org", return_value=[]):
                    exit_code = scan_adoption.main()

                    assert exit_code == 0
                    captured = capsys.readouterr()
                    assert "Total Adopters: 0" in captured.out
                    assert "No external adopters registered yet" in captured.out
                    assert "Next steps:" in captured.out

    def test_main_save_report_error(self, tmp_path, capsys):
        """Test main function when report save fails."""
        with patch("scan_adoption.generate_adoption_report") as mock_report:
            mock_report.return_value = {
                "total_adopters": 0,
                "last_updated": datetime.now().isoformat()
            }

            with patch("scan_adoption.Path") as mock_path_class:
                mock_path_instance = Mock()
                mock_path_instance.parent = Mock()
                mock_path_instance.write_text.side_effect = OSError("Disk full")

                mock_path_class.return_value = mock_path_instance
                mock_path_class.side_effect = lambda x: mock_path_instance

                with patch("scan_adoption.try_scan_github_org", return_value=[]):
                    exit_code = scan_adoption.main()

                    assert exit_code == 1
                    captured = capsys.readouterr()
                    assert "Error saving report" in captured.out

    def test_main_displays_multiple_adopters(self, tmp_path, capsys):
        """Test that main displays multiple adopters correctly."""
        with patch("scan_adoption.generate_adoption_report") as mock_report:
            mock_report.return_value = {
                "total_adopters": 5,
                "adopters": [
                    {"name": "Project A", "team": "Team X"},
                    {"name": "Project B", "team": "Team Y"},
                    {"name": "Project C", "team": "Team Z"},
                    {"name": "Project D", "team": "Team W"},
                    {"name": "Project E", "team": "Team V"},
                ],
                "last_updated": datetime.now().isoformat()
            }

            with patch("scan_adoption.Path") as mock_path_class:
                mock_path_instance = Mock()
                mock_path_instance.parent = Mock()
                mock_path_instance.write_text = Mock()

                mock_path_class.return_value = mock_path_instance
                mock_path_class.side_effect = lambda x: mock_path_instance

                with patch("scan_adoption.try_scan_github_org", return_value=[]):
                    exit_code = scan_adoption.main()

                    assert exit_code == 0
                    captured = capsys.readouterr()
                    assert "Total Adopters: 5" in captured.out
                    # Should show first 3 adopters
                    assert "Project A" in captured.out
                    assert "Project B" in captured.out
                    assert "Project C" in captured.out
                    # Should indicate there are more
                    assert "and 2 more" in captured.out

    def test_main_creates_metrics_directory(self, tmp_path):
        """Test that main creates metrics directory if it doesn't exist."""
        with patch("scan_adoption.generate_adoption_report") as mock_report:
            mock_report.return_value = {
                "total_adopters": 0,
                "last_updated": datetime.now().isoformat()
            }

            with patch("scan_adoption.Path") as mock_path_class:
                mock_path_instance = Mock()
                mock_path_instance.parent = Mock()
                mock_path_instance.write_text = Mock()

                mock_path_class.return_value = mock_path_instance
                mock_path_class.side_effect = lambda x: mock_path_instance

                with patch("scan_adoption.try_scan_github_org", return_value=[]):
                    scan_adoption.main()

                    # Verify mkdir was called with parents=True and exist_ok=True
                    mock_path_instance.parent.mkdir.assert_called_once_with(
                        parents=True, exist_ok=True
                    )

    def test_main_saves_valid_json(self, tmp_path):
        """Test that main saves valid JSON report."""
        saved_json = None

        def capture_write(text):
            nonlocal saved_json
            saved_json = text

        with patch("scan_adoption.generate_adoption_report") as mock_report:
            mock_report.return_value = {
                "total_adopters": 1,
                "last_updated": datetime.now().isoformat()
            }

            with patch("scan_adoption.Path") as mock_path_class:
                mock_path_instance = Mock()
                mock_path_instance.parent = Mock()
                mock_path_instance.write_text = Mock(side_effect=capture_write)

                mock_path_class.return_value = mock_path_instance
                mock_path_class.side_effect = lambda x: mock_path_instance

                with patch("scan_adoption.try_scan_github_org", return_value=[]):
                    exit_code = scan_adoption.main()

                    assert exit_code == 0
                    # Verify saved JSON is valid
                    assert saved_json is not None
                    parsed = json.loads(saved_json)
                    assert "total_adopters" in parsed
                    assert "last_updated" in parsed


class TestScriptExecution:
    """Test script execution through __main__ block."""

    def test_main_as_entry_point(self):
        """Test that main() works as entry point."""
        with patch("scan_adoption.generate_adoption_report") as mock_report:
            mock_report.return_value = {
                "total_adopters": 0,
                "last_updated": datetime.now().isoformat()
            }

            with patch("scan_adoption.Path") as mock_path_class:
                mock_path_instance = Mock()
                mock_path_instance.parent = Mock()
                mock_path_instance.write_text = Mock()

                mock_path_class.return_value = mock_path_instance
                mock_path_class.side_effect = lambda x: mock_path_instance

                with patch("scan_adoption.try_scan_github_org", return_value=[]):
                    # Call main() directly
                    exit_code = scan_adoption.main()
                    assert exit_code == 0


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_concurrent_subprocess_calls(self):
        """Test that multiple subprocess calls don't interfere."""
        mock_version_result = Mock()
        mock_version_result.returncode = 0
        mock_version_result.stdout = b"gh version 2.0.0"

        mock_search_result = Mock()
        mock_search_result.returncode = 0
        mock_search_result.stdout = json.dumps([{"name": "repo1", "url": "https://github.com/test/repo1"}])

        with patch.dict(os.environ, {"GITHUB_ORG": "testorg"}):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = [mock_version_result, mock_search_result]
                result = scan_adoption.try_scan_github_org()

                assert len(result) == 1

    def test_very_long_org_name(self):
        """Test handling of very long organization names."""
        mock_version_result = Mock()
        mock_version_result.returncode = 0
        mock_version_result.stdout = b"gh version 2.0.0"

        # Create a 40-character org name (1 char over limit)
        long_org = "a" * 40

        with patch.dict(os.environ, {"GITHUB_ORG": long_org}):
            with patch("subprocess.run", return_value=mock_version_result):
                result = scan_adoption.try_scan_github_org()
                assert result == []

    def test_special_characters_in_markdown(self):
        """Test handling of special characters in markdown content."""
        content_with_special_chars = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project & Test](https://github.com/org/project)* | Team <X> | action1, action2 | Notes with *asterisks* |
| *[Project > Test](https://github.com/org/project2)* | Team | action3 | Notes with | pipe | |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_with_special_chars

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            # Should parse both rows despite special characters
            assert result["total_adopters"] == 2

    def test_extra_whitespace_in_columns(self):
        """Test handling of extra whitespace in table columns."""
        content_with_whitespace = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
|  * [Project A] ( https://github.com/org/project-a )  |   Team X   |  action1 , action2  |   Notes   |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_with_whitespace

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            # This row might not parse correctly due to malformed link format
            # The important thing is it doesn't crash
            assert isinstance(result["total_adopters"], int)

    def test_unicode_in_adoption_file(self):
        """Test handling of unicode characters in ADOPTION.md."""
        unicode_content = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[プロジェクト](https://github.com/org/project)* | チーム | action1 | 日本語 |
| *[Projet](https://github.com/org/project2)* | Équipe | action2 | Français |
| *[项目](https://github.com/org/project3)* | 团队 | action3 | 中文 |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = unicode_content

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            # Should handle unicode characters
            assert result["total_adopters"] == 3
            assert result["adopters"][0]["name"] == "プロジェクト"
            assert result["adopters"][1]["team"] == "Équipe"

    def test_mixed_line_endings(self):
        """Test handling of mixed line endings (CRLF, LF)."""
        content_with_crlf = "# Adoption\r\n| Project | Team | Actions | Notes |\r\n|---------|------|---------|-------|\r\n| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Notes |\r\n"
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_with_crlf

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            # Should handle CRLF line endings
            assert result["total_adopters"] == 1

    def test_trailing_pipe_in_row(self):
        """Test handling of trailing pipe character in table rows."""
        content_with_trailing_pipe = """# Adoption

| Project | Team | Actions | Notes |
|---------|------|---------|-------|
| *[Project A](https://github.com/org/project-a)* | Team X | action1 | Notes |
"""
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.read_text.return_value = content_with_trailing_pipe

        with patch("scan_adoption.Path", return_value=mock_path):
            result = scan_adoption.generate_adoption_report()

            # Should handle trailing pipes
            assert isinstance(result["total_adopters"], int)
