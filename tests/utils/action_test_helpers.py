"""Shared helper methods for testing GitHub Actions.

This module provides reusable utilities for test files that need to interact
with action.yml files, templates, and action directory structures.

Usage Example:
    from tests.utils.action_test_helpers import ActionTestHelpers

    def test_action_yaml_exists(self, action_path):
        action_file = ActionTestHelpers.get_action_file(action_path, "spec-to-code")
        assert action_file.exists()
"""

from pathlib import Path


class ActionTestHelpers:
    """Shared helper methods for testing GitHub Actions.

    This class provides static methods for common path operations needed
    across multiple test files, eliminating code duplication and providing
    a single point of maintenance for test path logic.
    """

    ACTION_FILE_NAME = "action.yml"
    TEMPLATES_DIR = "templates"

    @staticmethod
    def get_action_file(action_path: Path, action_name: str) -> Path:
        """Get the action.yml file path for a given action.

        Args:
            action_path: Base path to the actions directory
            action_name: Name of the action (e.g., "spec-to-code", "auto-merge")

        Returns:
            Path object pointing to the action's action.yml file

        Example:
            action_file = ActionTestHelpers.get_action_file(action_path, "spec-to-code")
            # Returns: Path("actions/spec-to-code/action.yml")
        """
        return action_path / action_name / ActionTestHelpers.ACTION_FILE_NAME

    @staticmethod
    def get_template_file(
        action_path: Path,
        action_name: str,
        template_name: str = "gen_prompt.txt"
    ) -> Path:
        """Get the template file path for a given action.

        Args:
            action_path: Base path to the actions directory
            action_name: Name of the action
            template_name: Name of the template file (default: "gen_prompt.txt")

        Returns:
            Path object pointing to the action's template file

        Example:
            template = ActionTestHelpers.get_template_file(action_path, "spec-to-code")
            # Returns: Path("actions/spec-to-code/templates/gen_prompt.txt")
        """
        return (
            action_path /
            action_name /
            ActionTestHelpers.TEMPLATES_DIR /
            template_name
        )

    @staticmethod
    def get_action_content(action_path: Path, action_name: str) -> str:
        """Read and return action.yml content for a given action.

        Args:
            action_path: Base path to the actions directory
            action_name: Name of the action

        Returns:
            String content of the action.yml file

        Raises:
            FileNotFoundError: If action.yml doesn't exist
            UnicodeDecodeError: If file contains invalid UTF-8

        Example:
            content = ActionTestHelpers.get_action_content(action_path, "auto-merge")
            assert "name:" in content
        """
        return ActionTestHelpers.get_action_file(action_path, action_name).read_text()

    @staticmethod
    def get_action_dir(action_path: Path, action_name: str) -> Path:
        """Get the action directory path for a given action.

        Args:
            action_path: Base path to the actions directory
            action_name: Name of the action

        Returns:
            Path object pointing to the action's directory

        Example:
            action_dir = ActionTestHelpers.get_action_dir(action_path, "spec-to-code")
            # Returns: Path("actions/spec-to-code")
        """
        return action_path / action_name
