"""Tests for the auto-refactor GitHub Action."""

import pytest
from pathlib import Path


class TestAutoRefactorAction:
    """Test suite for auto-refactor action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "auto-refactor" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    def test_action_name_and_description(self, action_path):
        """Test that action has proper name and description."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "Auto Refactor" in content
        assert "refactor" in content.lower()

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "path:" in content, "path should be defined"
        assert "required: true" in content, "path should be required"

    def test_action_optional_inputs(self, action_path):
        """Test that optional inputs have default values."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "instruction:" in content
        assert "Improve code quality" in content, "instruction should have default"

        assert "claude-model:" in content
        assert "default: 'sonnet'" in content, "claude-model should default to 'sonnet'"

    def test_action_uses_composite_run_type(self, action_path):
        """Test that action uses composite run type."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "using: 'composite'" in content, "Action should use composite run type"

    def test_action_has_shell_bash(self, action_path):
        """Test that action uses bash shell."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "shell: bash" in content, "Action should use bash shell"

    def test_action_validates_path_exists(self, action_path):
        """Test that action validates target path exists."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "[ ! -e" in content or "if [ ! -e" in content, "Action should check path exists"
        assert "Target path not found" in content or "not found" in content, "Action should error if path not found"

    def test_action_validates_template_path(self, action_path):
        """Test that action validates template path."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "validate-template-path.sh" in content, "Action should validate template path"
        assert "validate_template_path" in content, "Action should call validate_template_path function"

    def test_action_uses_safe_variable_substitution(self, action_path):
        """Test that action uses awk for safe variable substitution."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "awk" in content, "Action should use awk for safe variable substitution"
        assert "gsub" in content, "Action should use gsub for placeholder replacement"

    def test_action_invokes_claude_cli(self, action_path):
        """Test that action invokes Claude CLI."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "claude --model" in content, "Action should invoke claude CLI"

    def test_action_uses_shared_scripts(self, action_path):
        """Test that action uses shared validation scripts."""
        action_file = action_path / "auto-refactor" / "action.yml"
        content = action_file.read_text()

        assert "../_shared/scripts" in content, "Action should reference shared scripts"

    def test_refactor_prompt_template_exists(self, action_path):
        """Test that the refactor prompt template exists."""
        template_file = action_path / "auto-refactor" / "templates" / "refactor_prompt.txt"
        assert template_file.exists(), "refactor_prompt.txt template should exist"


class TestAutoRefactorIntegration:
    """Integration tests for auto-refactor action."""

    def test_action_yaml_syntax(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        import yaml
        action_file = action_path / "auto-refactor" / "action.yml"

        with open(action_file) as f:
            config = yaml.safe_load(f)

        assert config is not None
        assert "name" in config
        assert "inputs" in config
        assert "runs" in config

    def test_action_directory_structure(self, action_path):
        """Test that action directory has required structure."""
        action_dir = action_path / "auto-refactor"

        assert action_dir.exists(), "Action directory should exist"
        assert (action_dir / "action.yml").exists(), "action.yml should exist"
        assert (action_dir / "templates").exists(), "templates directory should exist"

    def test_template_readable(self, action_path):
        """Test that template file is readable."""
        template_file = action_path / "auto-refactor" / "templates" / "refactor_prompt.txt"

        assert template_file.exists(), "Template should exist"
        content = template_file.read_text()
        assert len(content) > 0, "Template should not be empty"
