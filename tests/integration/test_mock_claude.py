"""
Integration tests for Mock Claude CLI
Tests the mock Claude CLI behavior in different scenarios
"""

import subprocess
import pytest
from pathlib import Path


class TestMockClaudeCLI:
    """Test the mock Claude CLI functionality"""

    def test_mock_exists_and_executable(self):
        """Verify mock Claude CLI exists and is executable"""
        mock_path = Path(__file__).parent.parent.parent / ".github" / "mocks" / "claude"
        assert mock_path.exists()
        assert mock_path.stat().st_mode & 0o111  # Check executable bit

    def test_mock_default_success_scenario(self, tmp_path):
        """Test mock Claude default success scenario"""
        mock_path = Path(__file__).parent.parent.parent / ".github" / "mocks" / "claude"

        result = subprocess.run(
            [str(mock_path), "code", "test instruction"],
            capture_output=True,
            text=True,
            env={**subprocess.os.environ, "MOCK_OUTPUT_DIR": str(tmp_path / "output")}
        )

        assert result.returncode == 0
        assert "Mock output written" in result.stdout

    def test_mock_lgtm_scenario(self, tmp_path):
        """Test mock Claude LGTM scenario for PR reviews"""
        mock_path = Path(__file__).parent.parent.parent / ".github" / "mocks" / "claude"

        result = subprocess.run(
            [str(mock_path), "code", "review this PR"],
            capture_output=True,
            text=True,
            env={**subprocess.os.environ, "MOCK_SCENARIO": "lgtm"}
        )

        assert result.returncode == 0
        assert "LGTM" in result.stdout
        assert "Confidence: 9" in result.stdout

    def test_mock_request_changes_scenario(self, tmp_path):
        """Test mock Claude request changes scenario"""
        mock_path = Path(__file__).parent.parent.parent / ".github" / "mocks" / "claude"

        result = subprocess.run(
            [str(mock_path), "code", "review this PR"],
            capture_output=True,
            text=True,
            env={**subprocess.os.environ, "MOCK_SCENARIO": "request_changes"}
        )

        assert result.returncode == 0
        assert "REQUEST_CHANGES" in result.stdout
        assert "Issues found" in result.stdout

    def test_mock_error_scenario(self, tmp_path):
        """Test mock Claude error scenario"""
        mock_path = Path(__file__).parent.parent.parent / ".github" / "mocks" / "claude"

        result = subprocess.run(
            [str(mock_path), "code", "test"],
            capture_output=True,
            text=True,
            env={**subprocess.os.environ, "MOCK_SCENARIO": "error"}
        )

        assert result.returncode == 1
        assert "Simulated error" in result.stderr


class TestSecurityPatterns:
    """Test security patterns are implemented"""

    def test_review_and_merge_has_cli_check(self):
        """Verify review-and-merge action has CLI availability check"""
        script_path = Path(__file__).parent.parent.parent / "actions" / "review-and-merge" / "scripts" / "review-and-fix.sh"

        assert script_path.exists()
        content = script_path.read_text()

        # Verify CLI check exists
        assert "command -v claude" in content
        assert "Claude CLI not found" in content

    def test_shared_script_has_path_validation(self):
        """Verify shared script has path validation"""
        script_path = Path(__file__).parent.parent.parent / "actions" / "_shared" / "scripts" / "validate-template-path.sh"

        assert script_path.exists()
        content = script_path.read_text()

        # Verify path validation exists (case-insensitive check)
        assert "traversal" in content.lower()
        assert "check_claude_cli" in content


class TestSecurityChecklist:
    """Test security checklist exists and is documented"""

    def test_security_checklist_exists(self):
        """Verify SECURITY_CHECKLIST.md exists"""
        checklist_path = Path(__file__).parent.parent.parent / "SECURITY_CHECKLIST.md"
        assert checklist_path.exists()

    def test_security_checklist_content(self):
        """Verify security checklist has required sections"""
        checklist_path = Path(__file__).parent.parent.parent / "SECURITY_CHECKLIST.md"
        content = checklist_path.read_text()

        # Verify key sections exist
        assert "CLI Availability Check" in content
        assert "Path Validation" in content
        assert "Input Sanitization" in content
        assert "GitHub Token Permissions" in content
        assert "Security Audit Results" in content

    def test_security_checklist_audit_results(self):
        """Verify security checklist has audit results"""
        checklist_path = Path(__file__).parent.parent.parent / "SECURITY_CHECKLIST.md"
        content = checklist_path.read_text()

        # Verify audit results section
        assert "Actions with CLI Check" in content
        assert "Actions NOT Using Claude" in content
        assert "Compliant Rate:" in content
        assert "100%" in content  # All actions using Claude now have checks
