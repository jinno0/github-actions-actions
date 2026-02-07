"""Tests for the pr-review-enqueuer GitHub Action."""


class TestPrReviewEnqueuerAction:
    """Test suite for pr-review-enqueuer action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "pr-review-enqueuer" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    def test_action_name_and_description(self, action_path):
        """Test that action has proper name and description."""
        action_file = action_path / "pr-review-enqueuer" / "action.yml"
        content = action_file.read_text()

        assert "enqueuer" in content.lower() or "enqueue" in content.lower()
        assert "review" in content.lower()

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "pr-review-enqueuer" / "action.yml"
        content = action_file.read_text()

        assert "github-token:" in content, "github-token should be defined"
        assert "required: true" in content, "github-token should be required"

    def test_action_uses_composite_run_type(self, action_path):
        """Test that action uses composite run type."""
        action_file = action_path / "pr-review-enqueuer" / "action.yml"
        content = action_file.read_text()

        assert "using: 'composite'" in content, "Action should use composite run type"

    def test_action_has_shell_bash(self, action_path):
        """Test that action uses bash shell."""
        action_file = action_path / "pr-review-enqueuer" / "action.yml"
        content = action_file.read_text()

        assert "shell: bash" in content, "Action should use bash shell"

    def test_action_has_queue_logic(self, action_path):
        """Test that action has queue management logic."""
        action_file = action_path / "pr-review-enqueuer" / "action.yml"
        content = action_file.read_text()

        # Should have some queue-related logic
        assert "queue" in content.lower() or "enqueue" in content.lower()


class TestPrReviewEnqueuerIntegration:
    """Integration tests for pr-review-enqueuer action."""

    def test_action_yaml_syntax(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        import yaml
        action_file = action_path / "pr-review-enqueuer" / "action.yml"

        with open(action_file) as f:
            config = yaml.safe_load(f)

        assert config is not None
        assert "name" in config
        assert "inputs" in config
        assert "runs" in config

    def test_action_directory_structure(self, action_path):
        """Test that action directory has required structure."""
        action_dir = action_path / "pr-review-enqueuer"

        assert action_dir.exists(), "Action directory should exist"
        assert (action_dir / "action.yml").exists(), "action.yml should exist"
