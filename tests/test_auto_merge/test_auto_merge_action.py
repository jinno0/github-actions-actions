"""Tests for the auto-merge GitHub Action."""

import pytest
from pathlib import Path


class TestAutoMergeAction:
    """Test suite for auto-merge action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "auto-merge" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    def test_action_name_and_description(self, action_path):
        """Test that action has proper name and description."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert "Auto Merge PR" in content
        assert "Merge a pull request with specified method" in content

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert "github-token:" in content, "github-token should be defined"
        assert "required: true" in content, "github-token should be required"

    def test_action_optional_inputs(self, action_path):
        """Test that optional inputs have default values."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert "merge-method:" in content
        assert "default: 'squash'" in content, "merge-method should default to 'squash'"

        assert "auto-merge:" in content
        assert "default: 'false'" in content, "auto-merge should default to 'false'"

    def test_action_uses_composite_run_type(self, action_path):
        """Test that action uses composite run type."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert "using: 'composite'" in content, "Action should use composite run type"

    def test_action_has_shell_bash(self, action_path):
        """Test that action uses bash shell."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert "shell: bash" in content, "Action should use bash shell"

    def test_action_invokes_gh_cli(self, action_path):
        """Test that action invokes gh CLI."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert "gh pr merge" in content, "Action should invoke gh pr merge"
        assert "$PR_NUMBER" in content, "Action should use PR number variable"

    def test_action_supports_merge_methods(self, action_path):
        """Test that action supports different merge methods."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert "--$METHOD" in content, "Action should support merge methods"
        assert "ARGS=" in content, "Action should build args dynamically"

    def test_action_handles_auto_merge_flag(self, action_path):
        """Test that action handles auto-merge flag."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert '--auto' in content, "Action should support --auto flag"
        assert "AUTO=" in content, "Action should check auto-merge input"

    def test_action_deletes_branch_after_merge(self, action_path):
        """Test that action deletes branch after merge."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert "--delete-branch" in content, "Action should delete branch after merge"


class TestAutoMergeIntegration:
    """Integration tests for auto-merge action."""

    def test_action_yaml_syntax(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        import yaml
        action_file = action_path / "auto-merge" / "action.yml"

        with open(action_file) as f:
            config = yaml.safe_load(f)

        assert config is not None
        assert "name" in config
        assert "inputs" in config
        assert "runs" in config

    def test_action_directory_structure(self, action_path):
        """Test that action directory has required structure."""
        action_dir = action_path / "auto-merge"

        assert action_dir.exists(), "Action directory should exist"
        assert (action_dir / "action.yml").exists(), "action.yml should exist"

    def test_merge_methods_documented(self, action_path):
        """Test that merge methods are properly documented."""
        action_file = action_path / "auto-merge" / "action.yml"
        content = action_file.read_text()

        assert "squash, merge, rebase" in content or "merge-method" in content

    def test_workflow_documentation(self, action_path):
        """Test that workflow documentation is available."""
        workflow_file = action_path.parent.parent / "examples" / "auto-merge.yml"

        if workflow_file.exists():
            content = workflow_file.read_text()
            assert "auto-merge" in content or "auto_merge" in content
