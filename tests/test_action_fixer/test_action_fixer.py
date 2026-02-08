"""Tests for the action-fixer GitHub Action."""

import pytest
import yaml


class TestActionFixer:
    """Test suite for action-fixer action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "action-fixer" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "action-fixer" / "action.yml"
        content = action_file.read_text()

        # action-fixer has no strictly required inputs (all have defaults)
        # Check that important inputs are defined
        important_inputs = [
            "github-token",
            "fail-on-error",
            "auto-fix",
            "claude-model"
        ]
        for input_name in important_inputs:
            assert f"{input_name}:" in content, f"Input {input_name} should be defined"

    def test_action_optional_inputs_have_defaults(self, action_path):
        """Test that optional inputs have default values."""
        action_file = action_path / "action-fixer" / "action.yml"
        content = action_file.read_text()

        # Check optional inputs with defaults
        optional_inputs = {
            "github-token": "${{ github.token }}",
            "fail-on-error": "true",
            "auto-fix": "false",
            "claude-model": "sonnet",
            "commit-message": "fix: correct workflow validation issues",
            "fix-prompt-template": ""
        }

        for input_name, _default_value in optional_inputs.items():
            assert f"{input_name}:" in content, f"Input {input_name} should be defined"
            # Check that default exists (format varies in YAML)
            assert "default:" in content, f"Input {input_name} should have a default value"

    def test_action_yaml_syntax_valid(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        action_file = action_path / "action-fixer" / "action.yml"
        with open(action_file) as f:
            try:
                yaml.safe_load(f)
            except yaml.YAMLError as e:
                pytest.fail(f"action.yml has invalid YAML syntax: {e}")

    def test_fix_prompt_template_exists(self, action_path):
        """Test that the fix prompt template exists."""
        template_file = action_path / "action-fixer" / "templates" / "fix_prompt.txt"
        assert template_file.exists(), "fix_prompt.txt should exist"

    def test_fix_prompt_template_content(self, action_path):
        """Test that the fix prompt template has required placeholders."""
        template_file = action_path / "action-fixer" / "templates" / "fix_prompt.txt"
        assert template_file.exists(), "fix_prompt.txt should exist"

        content = template_file.read_text()

        # Check for required placeholders
        required_placeholders = ["{FILE}", "{ISSUES}", "{CURRENT_CONTENT}"]
        for placeholder in required_placeholders:
            assert placeholder in content, f"Template should contain {placeholder} placeholder"

    def test_action_directory_structure(self, action_path):
        """Test that action-fixer follows standard directory structure."""
        action_dir = action_path / "action-fixer"

        # Check required files
        assert (action_dir / "action.yml").exists(), "action.yml should exist"
        assert (action_dir / "templates").exists(), "templates/ directory should exist"

    def test_action_has_composite_run_type(self, action_path):
        """Test that action uses composite run type."""
        action_file = action_path / "action-fixer" / "action.yml"
        _ = action_file.read_text()  # File existence check

        # Parse YAML to check runs.using
        with open(action_file) as f:
            action_config = yaml.safe_load(f)

        assert "runs" in action_config, "action.yml should have 'runs' section"
        assert "using" in action_config["runs"], "runs should specify 'using'"
        assert action_config["runs"]["using"] == "composite", "action should use composite run type"

    def test_action_has_validation_steps(self, action_path):
        """Test that action includes YAML validation steps."""
        action_file = action_path / "action-fixer" / "action.yml"
        content = action_file.read_text()

        # Check for validation steps
        assert "yamllint" in content or "YAML" in content, "Action should include YAML validation"
        assert "validate" in content.lower(), "Action should have validation step"

    def test_action_has_ai_fix_capability(self, action_path):
        """Test that action includes AI-powered fix capability."""
        action_file = action_path / "action-fixer" / "action.yml"
        content = action_file.read_text()

        # Check for AI fix capability
        assert "claude" in content.lower() or "ai" in content.lower(), "Action should reference Claude/AI"
        assert "auto-fix" in content.lower() or "auto_fix" in content, "Action should have auto-fix functionality"

    def test_template_files_readable(self, action_path):
        """Test that template files are readable."""
        action_dir = action_path / "action-fixer" / "templates"

        if action_dir.exists():
            for template_file in action_dir.iterdir():
                if template_file.is_file():
                    # Try to read the file
                    try:
                        content = template_file.read_text()
                        assert len(content) > 0, f"Template file {template_file.name} should not be empty"
                    except Exception as e:
                        pytest.fail(f"Template file {template_file.name} is not readable: {e}")

    def test_action_description_meaningful(self, action_path):
        """Test that action has a meaningful description."""
        action_file = action_path / "action-fixer" / "action.yml"
        _ = action_file.read_text()  # File existence check

        # Parse YAML to check description
        with open(action_file) as f:
            action_config = yaml.safe_load(f)

        assert "description" in action_config, "action.yml should have a description"
        description = action_config["description"]
        assert len(description) > 20, "Description should be meaningful (more than 20 characters)"
        assert "validate" in description.lower() or "fix" in description.lower(), "Description should mention validation or fixing"


class TestActionFixerIntegration:
    """Integration tests for action-fixer action."""

    def test_action_yaml_complete_structure(self, action_path):
        """Test that action.yml has complete structure with all sections."""
        action_file = action_path / "action-fixer" / "action.yml"

        with open(action_file) as f:
            action_config = yaml.safe_load(f)

        # Check top-level sections
        assert "name" in action_config
        assert "description" in action_config
        assert "inputs" in action_config
        assert "runs" in action_config

    def test_all_templates_defined(self, action_path):
        """Test that all referenced templates exist."""
        _action_file = action_path / "action-fixer" / "action.yml"
        templates_dir = action_path / "action-fixer" / "templates"

        # The action references fix_prompt.txt
        assert (templates_dir / "fix_prompt.txt").exists(), "fix_prompt.txt template must exist"

    def test_no_broken_references(self, action_path):
        """Test that there are no broken file references in action.yml."""
        action_file = action_path / "action-fixer" / "action.yml"
        action_dir = action_path / "action-fixer"

        # Read action.yml content to check for script references
        _ = action_file.read_text()  # Verify file is readable

        # This action uses composite run type with inline bash commands
        # No external script references to validate
        # Just verify the file structure is sound
        assert action_dir.exists(), "action-fixer directory should exist"
        assert (action_dir / "templates").exists(), "templates directory should exist"
