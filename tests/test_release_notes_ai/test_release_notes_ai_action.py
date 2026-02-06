"""Tests for the release-notes-ai GitHub Action."""



class TestReleaseNotesAiAction:
    """Test suite for release-notes-ai action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "release-notes-ai" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    def test_action_name_and_description(self, action_path):
        """Test that action has proper name and description."""
        action_file = action_path / "release-notes-ai" / "action.yml"
        content = action_file.read_text()

        assert "Release" in content and ("Notes" in content or "notes" in content)
        assert "AI" in content or "ai" in content

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "release-notes-ai" / "action.yml"
        content = action_file.read_text()

        assert "github-token:" in content, "github-token should be defined"
        # github-token is optional in this action with a default value
        assert "required: false" in content or "default:" in content, "github-token should have default"

    def test_action_uses_composite_run_type(self, action_path):
        """Test that action uses composite run type."""
        action_file = action_path / "release-notes-ai" / "action.yml"
        content = action_file.read_text()

        assert "using: 'composite'" in content, "Action should use composite run type"

    def test_action_has_shell_bash(self, action_path):
        """Test that action uses bash shell."""
        action_file = action_path / "release-notes-ai" / "action.yml"
        content = action_file.read_text()

        assert "shell: bash" in content, "Action should use bash shell"

    def test_action_invokes_claude_cli(self, action_path):
        """Test that action invokes Claude CLI."""
        action_file = action_path / "release-notes-ai" / "action.yml"
        content = action_file.read_text()

        assert "claude" in content, "Action should invoke claude CLI"

    def test_action_generates_notes(self, action_path):
        """Test that action generates release notes."""
        action_file = action_path / "release-notes-ai" / "action.yml"
        content = action_file.read_text()

        assert "release" in content.lower() and "notes" in content.lower()


class TestReleaseNotesAiIntegration:
    """Integration tests for release-notes-ai action."""

    def test_action_yaml_syntax(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        import yaml
        action_file = action_path / "release-notes-ai" / "action.yml"

        with open(action_file) as f:
            config = yaml.safe_load(f)

        assert config is not None
        assert "name" in config
        assert "inputs" in config
        assert "runs" in config

    def test_action_directory_structure(self, action_path):
        """Test that action directory has required structure."""
        action_dir = action_path / "release-notes-ai"

        assert action_dir.exists(), "Action directory should exist"
        assert (action_dir / "action.yml").exists(), "action.yml should exist"
