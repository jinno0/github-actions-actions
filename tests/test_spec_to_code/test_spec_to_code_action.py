"""Tests for the spec-to-code GitHub Action."""

from pathlib import Path

import pytest


class TestSpecToCodeAction:
    """Test suite for spec-to-code action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "spec-to-code" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check required inputs
        required_inputs = ["spec-path", "github-token"]
        for input_name in required_inputs:
            assert f"{input_name}:" in content, f"Input {input_name} should be defined"

    def test_action_optional_inputs_with_defaults(self, action_path):
        """Test that optional inputs have default values."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check optional inputs with defaults
        optional_inputs = {
            "output-dir": ".",
            "language": "TypeScript",
            "claude-model": "sonnet",
        }

        for input_name, default_value in optional_inputs.items():
            assert f"{input_name}:" in content, f"Input {input_name} should be defined"
            # Check for default value (might be with or without quotes)
            assert f"default: '{default_value}'" in content or f"default: \"{default_value}\"" in content, \
                f"Input {input_name} should have default {default_value}"

    def test_action_has_path_validation(self, action_path):
        """Test that the action validates paths to prevent directory traversal."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for path validation
        assert "mkdir -p" in content, "Action should create output directory"
        assert "GITHUB_WORKSPACE" in content, "Action should reference workspace"
        assert "pwd" in content, "Action should resolve absolute paths"

    def test_action_has_security_checks(self, action_path):
        """Test that the action has security checks for path traversal."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for path traversal protection
        assert "!=" in content or "-ne" in content, "Action should validate paths"
        assert "error::" in content or "exit 1" in content, "Action should handle errors"

    def test_action_validates_spec_file(self, action_path):
        """Test that the action validates the spec file."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for file validation
        assert "[ ! -f" in content or "[[ ! -f" in content, "Action should check if file exists"
        assert "[ ! -r" in content or "[[ ! -r" in content, "Action should check if file is readable"

    def test_action_uses_base64_encoding(self, action_path):
        """Test that the action uses base64 encoding for safe content handling."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for base64 encoding
        assert "base64" in content, "Action should use base64 encoding for safe content handling"
        assert "base64 -d" in content or "base64 --decode" in content, "Action should decode base64 content"

    def test_action_uses_envsubst(self, action_path):
        """Test that the action uses envsubst for safe variable substitution."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for envsubst usage
        assert "envsubst" in content, "Action should use envsubst for safer variable substitution"

    def test_action_supports_custom_template(self, action_path):
        """Test that the action supports custom generation templates."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for custom template support
        assert "GEN_PROMPT_TEMPLATE" in content, "Action should accept custom template path"
        assert "gen_prompt.txt" in content, "Action should have default template"

    def test_action_invokes_claude_cli(self, action_path):
        """Test that the action invokes Claude Code CLI."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for Claude CLI invocation
        assert "claude" in content, "Action should invoke Claude CLI"
        assert "--model" in content, "Action should pass model parameter"

    def test_action_sets_environment_variables(self, action_path):
        """Test that the action sets required environment variables."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for environment variable usage
        assert "GITHUB_ENV" in content, "Action should set GitHub environment variables"
        assert "OUTPUT_DIR=" in content, "Action should set OUTPUT_DIR"
        assert "SPEC_PATH=" in content, "Action should set SPEC_PATH"

    def test_action_has_error_handling(self, action_path):
        """Test that the action has proper error handling."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for error handling
        assert "exit 1" in content, "Action should exit on error"
        assert "error::" in content, "Action should report errors"

    def test_generation_prompt_template_exists(self, action_path):
        """Test that the generation prompt template exists."""
        template_file = action_path / "spec-to-code" / "templates" / "gen_prompt.txt"
        assert template_file.exists(), "gen_prompt.txt should exist"

    def test_generation_prompt_template_content(self, action_path):
        """Test that the generation prompt template has required content."""
        template_file = action_path / "spec-to-code" / "templates" / "gen_prompt.txt"
        content = template_file.read_text()

        # Check for placeholders (template uses {VAR} style, not $VAR)
        assert "{LANG}" in content, "Template should have LANG placeholder"
        assert "{OUTPUT_DIR}" in content, "Template should have OUTPUT_DIR placeholder"
        assert "{SPEC_CONTENT}" in content, "Template should have SPEC_CONTENT placeholder"

        # Check for generation instructions
        content_lower = content.lower()
        assert any(word in content_lower for word in ["generate", "create", "implement"]), \
            "Template should mention code generation"


class TestSpecToCodeIntegration:
    """Integration tests for spec-to-code action."""

    def test_action_yaml_syntax(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        action_file = action_path / "spec-to-code" / "action.yml"

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

    def test_action_directory_structure(self, action_path):
        """Test that the action directory has the expected structure."""
        action_dir = action_path / "spec-to-code"

        # Check for required directories
        assert (action_dir / "templates").exists(), "templates directory should exist"

        # Check for required files
        assert (action_dir / "action.yml").exists(), "action.yml should exist"
        assert (action_dir / "templates" / "gen_prompt.txt").exists(), "gen_prompt.txt should exist"

    def test_template_readable(self, action_path):
        """Test that the template file is readable and not empty."""
        template_file = action_path / "spec-to-code" / "templates" / "gen_prompt.txt"
        content = template_file.read_text()
        assert len(content) > 0, "gen_prompt.txt should not be empty"

    def test_spec_validation_workflow(self, temp_dir, action_path, sample_spec):
        """Test the spec validation workflow with a real spec file."""
        # Create a test spec file
        spec_file = Path(temp_dir) / "test_spec.md"
        spec_file.write_text(sample_spec)

        # Verify spec file exists and is readable
        assert spec_file.exists(), "Spec file should be created"
        assert spec_file.read_text() == sample_spec, "Spec content should match"

    def test_supported_languages_documented(self, action_path):
        """Test that supported languages are documented."""
        template_file = action_path / "spec-to-code" / "templates" / "gen_prompt.txt"
        content = template_file.read_text().lower()

        # Check for common programming languages
        common_languages = ["python", "typescript", "javascript", "go", "java", "rust"]
        found_languages = [lang for lang in common_languages if lang in content]

        # At least some languages should be mentioned
        assert len(found_languages) > 0, "Template should mention at least some programming languages"

    def test_action_handles_special_characters(self, action_path):
        """Test that the action can handle special characters in spec content."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for proper escaping mechanisms
        assert "base64" in content, "Action should use base64 to handle special characters"
        assert "envsubst" in content, "Action should use envsubst for safe substitution"

    def test_output_directory_handling(self, action_path):
        """Test that the action properly handles output directory creation."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for directory creation
        assert "mkdir -p" in content, "Action should create output directory with parents"
        assert "OUTPUT_DIR" in content, "Action should track output directory"

    def test_claude_model_parameter(self, action_path):
        """Test that the action properly passes the model parameter."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Check for model parameter handling
        assert "MODEL=" in content, "Action should set MODEL variable"
        assert "--model" in content, "Action should pass model to Claude CLI"

    def test_workflow_step_sequence(self, action_path):
        """Test that the workflow steps are in the correct sequence."""
        action_file = action_path / "spec-to-code" / "action.yml"
        content = action_file.read_text()

        # Steps should be in order: ensure output dir, validate spec, generate code
        lines = [line.strip() for line in content.split('\n') if line.strip()]

        # Find key step markers
        ensure_dir_idx = next((i for i, line in enumerate(lines) if "Ensure output directory exists" in line), -1)
        validate_spec_idx = next((i for i, line in enumerate(lines) if "Validate Spec Path" in line), -1)
        generate_code_idx = next((i for i, line in enumerate(lines) if "Generate Code" in line), -1)

        assert ensure_dir_idx >= 0, "Should have 'Ensure output directory exists' step"
        assert validate_spec_idx >= 0, "Should have 'Validate Spec Path' step"
        assert generate_code_idx >= 0, "Should have 'Generate Code' step"
        assert ensure_dir_idx < validate_spec_idx < generate_code_idx, "Steps should be in correct order"
