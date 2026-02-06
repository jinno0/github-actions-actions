"""Tests for the publish-pr GitHub Action."""



class TestPublishPrAction:
    """Test suite for publish-pr action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "publish-pr" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    def test_action_name_and_description(self, action_path):
        """Test that action has proper name and description."""
        action_file = action_path / "publish-pr" / "action.yml"
        content = action_file.read_text()

        assert "Publish PR" in content
        assert "Convert a draft pull request to ready for review" in content

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "publish-pr" / "action.yml"
        content = action_file.read_text()

        assert "github-token:" in content, "github-token should be defined"
        assert "required: true" in content, "github-token should be required"

    def test_action_uses_composite_run_type(self, action_path):
        """Test that action uses composite run type."""
        action_file = action_path / "publish-pr" / "action.yml"
        content = action_file.read_text()

        assert "using: 'composite'" in content, "Action should use composite run type"

    def test_action_has_shell_bash(self, action_path):
        """Test that action uses bash shell."""
        action_file = action_path / "publish-pr" / "action.yml"
        content = action_file.read_text()

        assert "shell: bash" in content, "Action should use bash shell"

    def test_action_invokes_gh_cli(self, action_path):
        """Test that action invokes gh CLI."""
        action_file = action_path / "publish-pr" / "action.yml"
        content = action_file.read_text()

        assert "gh pr ready" in content, "Action should invoke gh pr ready"
        assert "$PR_NUMBER" in content, "Action should use PR number variable"

    def test_action_has_simple_workflow(self, action_path):
        """Test that action has a simple, focused workflow."""
        action_file = action_path / "publish-pr" / "action.yml"
        content = action_file.read_text()

        # The action should be simple - just mark PR as ready
        assert "Mark PR as Ready" in content or "ready for review" in content


class TestPublishPrIntegration:
    """Integration tests for publish-pr action."""

    def test_action_yaml_syntax(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        import yaml
        action_file = action_path / "publish-pr" / "action.yml"

        with open(action_file) as f:
            config = yaml.safe_load(f)

        assert config is not None
        assert "name" in config
        assert "inputs" in config
        assert "runs" in config

    def test_action_directory_structure(self, action_path):
        """Test that action directory has required structure."""
        action_dir = action_path / "publish-pr"

        assert action_dir.exists(), "Action directory should exist"
        assert (action_dir / "action.yml").exists(), "action.yml should exist"

    def test_github_token_permissions_documented(self, action_path):
        """Test that github token permissions are documented."""
        action_file = action_path / "publish-pr" / "action.yml"
        content = action_file.read_text()

        assert "repo permissions" in content or "repo" in content.lower()

    def test_workflow_documentation(self, action_path):
        """Test that workflow documentation is available."""
        workflow_file = action_path.parent.parent / "examples" / "publish-pr.yml"

        if workflow_file.exists():
            content = workflow_file.read_text()
            assert "publish-pr" in content or "publish_pr" in content
