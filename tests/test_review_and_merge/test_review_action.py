"""Tests for the review-and-merge GitHub Action."""

import pytest
import subprocess
import json
import tempfile
import shutil
from pathlib import Path


class TestReviewAction:
    """Test suite for review-and-merge action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "review-and-merge" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content
        assert "outputs:" in content

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "review-and-merge" / "action.yml"
        content = action_file.read_text()

        # Check required inputs
        required_inputs = ["github-token"]
        for input_name in required_inputs:
            assert f"{input_name}:" in content, f"Input {input_name} should be defined"
            assert "required: true" in content or "required: false" in content

    def test_action_optional_inputs(self, action_path):
        """Test that optional inputs have default values."""
        action_file = action_path / "review-and-merge" / "action.yml"
        content = action_file.read_text()

        # Check optional inputs with defaults
        optional_inputs = {
            "claude-model": "sonnet",
            "lgtm-threshold": "7",
            "auto-fix": "true",
        }

        for input_name, default_value in optional_inputs.items():
            assert f"{input_name}:" in content, f"Input {input_name} should be defined"
            assert f"default: '{default_value}'" in content, f"Input {input_name} should have default {default_value}"

    def test_action_outputs(self, action_path):
        """Test that all outputs are defined."""
        action_file = action_path / "review-and-merge" / "action.yml"
        content = action_file.read_text()

        # Note: summary and made_changes are set by the script but not exposed as action outputs
        expected_outputs = ["verdict", "confidence"]
        for output in expected_outputs:
            assert f"{output}:" in content, f"Output {output} should be defined"

    def test_review_script_exists(self, action_path):
        """Test that the review-and-fix.sh script exists."""
        script_file = action_path / "review-and-merge" / "scripts" / "review-and-fix.sh"
        assert script_file.exists(), "review-and-fix.sh should exist"
        assert script_file.stat().st_mode & 0o111, "Script should be executable"

    def test_post_comment_script_exists(self, action_path):
        """Test that the post-comment.sh script exists."""
        script_file = action_path / "review-and-merge" / "scripts" / "post-comment.sh"
        assert script_file.exists(), "post-comment.sh should exist"

    def test_review_prompt_template_exists(self, action_path):
        """Test that the review prompt template exists."""
        template_file = action_path / "review-and-merge" / "templates" / "review_prompt.txt"
        assert template_file.exists(), "review_prompt.txt should exist"

    def test_fix_prompt_template_exists(self, action_path):
        """Test that the fix prompt template exists."""
        template_file = action_path / "review-and-merge" / "templates" / "fix_prompt.txt"
        assert template_file.exists(), "fix_prompt.txt should exist"

    def test_comment_template_exists(self, action_path):
        """Test that the comment template exists."""
        template_file = action_path / "review-and-merge" / "templates" / "comment_template.txt"
        assert template_file.exists(), "comment_template.txt should exist"

    def test_review_script_has_error_handling(self, action_path):
        """Test that the review script has proper error handling."""
        script_file = action_path / "review-and-merge" / "scripts" / "review-and-fix.sh"
        content = script_file.read_text()

        # Check for error handling patterns
        assert "set -e" in content, "Script should use 'set -e' for error handling"
        assert "if [" in content or "if [[ " in content, "Script should have conditional checks"
        assert "echo" in content, "Script should have logging"

    def test_review_script_handles_auto_fix_mode(self, action_path):
        """Test that the script handles auto-fix mode correctly."""
        script_file = action_path / "review-and-merge" / "scripts" / "review-and-fix.sh"
        content = script_file.read_text()

        # The script checks for AUTO_FIX being equal to "true" (with quotes)
        assert '[ "$AUTO_FIX" = "true" ]' in content, "Script should check for auto-fix mode"
        assert "fix_prompt.txt" in content, "Script should use fix template in auto-fix mode"
        assert "review_prompt.txt" in content, "Script should use review template in review mode"

    def test_review_script_handles_git_operations(self, action_path):
        """Test that the script handles git operations safely."""
        script_file = action_path / "review-and-merge" / "scripts" / "review-and-fix.sh"
        content = script_file.read_text()

        # Check for git operations
        assert "git diff" in content, "Script should check for changes"
        assert "git config" in content, "Script should configure git user"
        assert "git commit" in content or "git push" in content, "Script should handle commits/pushes"

        # Check for retry logic
        assert "retry" in content.lower() or "max_retries" in content, "Script should have retry logic"

    def test_review_script_validates_json(self, action_path):
        """Test that the script validates JSON output."""
        script_file = action_path / "review-and-merge" / "scripts" / "review-and-fix.sh"
        content = script_file.read_text()

        assert "jq" in content, "Script should use jq for JSON parsing"
        assert "VERDICT=" in content, "Script should extract verdict"
        assert "CONFIDENCE=" in content, "Script should extract confidence"
        assert "SUMMARY=" in content, "Script should extract summary"

    def test_review_script_validates_verdict_values(self, action_path):
        """Test that the script validates verdict values."""
        script_file = action_path / "review-and-merge" / "scripts" / "review-and-fix.sh"
        content = script_file.read_text()

        assert "LGTM" in content, "Script should handle LGTM verdict"
        assert "REQUEST_CHANGES" in content, "Script should handle REQUEST_CHANGES verdict"
        assert "COMMENT" in content, "Script should handle COMMENT verdict"

    def test_review_script_sets_github_outputs(self, action_path):
        """Test that the script sets GitHub Actions outputs."""
        script_file = action_path / "review-and-merge" / "scripts" / "review-and-fix.sh"
        content = script_file.read_text()

        assert "GITHUB_OUTPUT" in content, "Script should set GitHub Outputs"
        assert "verdict=" in content, "Script should output verdict"
        assert "confidence=" in content, "Script should output confidence"
        assert "summary=" in content, "Script should output summary"


class TestReviewActionIntegration:
    """Integration tests for review-and-merge action."""

    def test_action_yaml_syntax(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        action_file = action_path / "review-and-merge" / "action.yml"

        # Try to parse as YAML
        import yaml
        with open(action_file) as f:
            try:
                config = yaml.safe_load(f)
                assert config is not None
                assert "name" in config
                assert "runs" in config
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML in action.yml: {e}")

    def test_review_prompt_template_content(self, action_path):
        """Test that the review prompt template has required content."""
        template_file = action_path / "review-and-merge" / "templates" / "review_prompt.txt"
        content = template_file.read_text().lower()

        # Check for key review elements
        assert any(word in content for word in ["review", "analyze", "feedback"]), "Template should mention review"
        assert any(word in content for word in ["verdict", "lgtm", "request_changes"]), "Template should mention verdicts"

    def test_fix_prompt_template_content(self, action_path):
        """Test that the fix prompt template has required content."""
        template_file = action_path / "review-and-merge" / "templates" / "fix_prompt.txt"
        content = template_file.read_text().lower()

        # Check for key fix elements
        assert any(word in content for word in ["fix", "correct", "improve"]), "Template should mention fixing"
        assert "diff" in content, "Template should reference the diff"

    def test_comment_template_content(self, action_path):
        """Test that the comment template has required structure."""
        template_file = action_path / "review-and-merge" / "templates" / "comment_template.txt"
        content = template_file.read_text()

        # Check for placeholders
        assert "{" in content or "{" in content, "Template should have placeholders for dynamic content"

    def test_action_directory_structure(self, action_path):
        """Test that the action directory has the expected structure."""
        action_dir = action_path / "review-and-merge"

        # Check for required directories
        assert (action_dir / "scripts").exists(), "scripts directory should exist"
        assert (action_dir / "templates").exists(), "templates directory should exist"

        # Check for required files
        assert (action_dir / "action.yml").exists(), "action.yml should exist"
        assert (action_dir / "scripts" / "review-and-fix.sh").exists(), "review-and-fix.sh should exist"
        assert (action_dir / "scripts" / "post-comment.sh").exists(), "post-comment.sh should exist"

    def test_all_templates_readable(self, action_path):
        """Test that all template files are readable."""
        templates_dir = action_path / "review-and-merge" / "templates"

        for template_file in templates_dir.glob("*.txt"):
            content = template_file.read_text()
            assert len(content) > 0, f"{template_file.name} should not be empty"

    def test_all_scripts_executable(self, action_path):
        """Test that all shell scripts are executable."""
        scripts_dir = action_path / "review-and-merge" / "scripts"

        for script_file in scripts_dir.glob("*.sh"):
            assert script_file.stat().st_mode & 0o111, f"{script_file.name} should be executable"
