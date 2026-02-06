"""
Integration tests for Action structure validation
Tests that all actions have proper action.yml files with required fields
"""

import pytest
import yaml


class TestActionStructure:
    """Test the basic structure of all GitHub Actions"""

    @pytest.fixture
    def actions_dir(self, action_path):
        """Get the actions directory path"""
        actions = action_path / "actions"
        return actions

    @pytest.fixture
    def all_actions(self, actions_dir):
        """Get all action directories"""
        if not actions_dir.exists():
            return []
        return [d for d in actions_dir.iterdir() if d.is_dir() and not d.name.startswith("_")]

    def test_all_actions_have_action_yml(self, all_actions):
        """Verify every action has an action.yml file"""
        missing = []
        for action_dir in all_actions:
            action_yml = action_dir / "action.yml"
            if not action_yml.exists():
                missing.append(action_dir.name)

        assert len(missing) == 0, f"Actions missing action.yml: {', '.join(missing)}"

    def test_review_and_merge_action_structure(self, action_path):
        """Test review-and-merge action has proper structure"""
        action_yml = action_path / "actions" / "review-and-merge" / "action.yml"

        if not action_yml.exists():
            pytest.skip("review-and-merge action not found")

        config = yaml.safe_load(action_yml.read_text())

        # Verify required fields
        assert "name" in config
        assert "description" in config
        assert "runs" in config
        assert config["runs"]["using"] == "composite"

        # Verify required inputs
        assert "github-token" in config["inputs"]
        assert "claude-model" in config["inputs"]

    def test_actions_have_required_metadata(self, all_actions):
        """Verify all actions have required metadata fields"""
        missing_metadata = []

        for action_dir in all_actions:
            action_yml = action_dir / "action.yml"
            if not action_yml.exists():
                continue

            try:
                config = yaml.safe_load(action_yml.read_text())

                # Check for required top-level fields
                if "name" not in config:
                    missing_metadata.append(f"{action_dir.name}: missing 'name'")
                if "description" not in config:
                    missing_metadata.append(f"{action_dir.name}: missing 'description'")
                if "runs" not in config:
                    missing_metadata.append(f"{action_dir.name}: missing 'runs'")

            except Exception as e:
                missing_metadata.append(f"{action_dir.name}: parsing error - {str(e)}")

        assert len(missing_metadata) == 0, "Metadata issues:\n" + "\n".join(missing_metadata)

    def test_action_composite_steps_exist(self, action_path):
        """Verify composite actions have at least one step"""
        actions_dir = action_path / "actions"

        if not actions_dir.exists():
            pytest.skip("actions directory not found")

        for action_dir in actions_dir.iterdir():
            if not action_dir.is_dir() or action_dir.name.startswith("_"):
                continue

            action_yml = action_dir / "action.yml"
            if not action_yml.exists():
                continue

            config = yaml.safe_load(action_yml.read_text())

            if config.get("runs", {}).get("using") == "composite":
                steps = config.get("runs", {}).get("steps", [])
                assert len(steps) > 0, f"{action_dir.name}: composite action has no steps"
