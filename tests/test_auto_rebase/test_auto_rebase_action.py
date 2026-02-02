"""Tests for the auto-rebase GitHub Action."""

import pytest
from pathlib import Path


class TestAutoRebaseAction:
    """Test suite for auto-rebase action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "auto-rebase" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    def test_action_name_and_description(self, action_path):
        """Test that action has proper name and description."""
        action_file = action_path / "auto-rebase" / "action.yml"
        content = action_file.read_text()

        assert "Auto Rebase" in content
        assert "rebase" in content.lower()

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "auto-rebase" / "action.yml"
        content = action_file.read_text()

        assert "github-token:" in content, "github-token should be defined"
        assert "required: true" in content, "github-token should be required"

    def test_action_optional_inputs(self, action_path):
        """Test that optional inputs have default values."""
        action_file = action_path / "auto-rebase" / "action.yml"
        content = action_file.read_text()

        assert "claude-model:" in content
        assert "default: 'sonnet'" in content, "claude-model should default to 'sonnet'"

        assert "rebase-strategy:" in content
        assert "default: 'interactive'" in content, "rebase-strategy should default to 'interactive'"

    def test_action_has_outputs(self, action_path):
        """Test that action defines outputs."""
        action_file = action_path / "auto-rebase" / "action.yml"
        content = action_file.read_text()

        assert "outputs:" in content, "Action should have outputs"
        assert "rebased:" in content, "Action should output rebased status"
        assert "conflicts-resolved:" in content, "Action should output conflicts-resolved status"
        assert "conflict-count:" in content, "Action should output conflict-count"

    def test_action_uses_composite_run_type(self, action_path):
        """Test that action uses composite run type."""
        action_file = action_path / "auto-rebase" / "action.yml"
        content = action_file.read_text()

        assert "using: 'composite'" in content, "Action should use composite run type"

    def test_action_checks_claude_cli(self, action_path):
        """Test that action checks Claude CLI availability."""
        action_file = action_path / "auto-rebase" / "action.yml"
        content = action_file.read_text()

        assert "command -v claude" in content, "Action should check for claude command"
        assert "CLAUDE_AVAILABLE" in content, "Action should set Claude availability flag"

    def test_action_has_error_handling(self, action_path):
        """Test that action has error handling."""
        action_file = action_path / "auto-rebase" / "action.yml"
        content = action_file.read_text()

        assert "exit 1" in content or "::error::" in content, "Action should have error handling"


class TestAutoRebaseIntegration:
    """Integration tests for auto-rebase action."""

    def test_action_yaml_syntax(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        import yaml
        action_file = action_path / "auto-rebase" / "action.yml"

        with open(action_file) as f:
            config = yaml.safe_load(f)

        assert config is not None
        assert "name" in config
        assert "inputs" in config
        assert "runs" in config

    def test_action_directory_structure(self, action_path):
        """Test that action directory has required structure."""
        action_dir = action_path / "auto-rebase"

        assert action_dir.exists(), "Action directory should exist"
        assert (action_dir / "action.yml").exists(), "action.yml should exist"

    def test_rebase_strategies_documented(self, action_path):
        """Test that rebase strategies are documented."""
        action_file = action_path / "auto-rebase" / "action.yml"
        content = action_file.read_text()

        assert "interactive" in content or "force" in content
