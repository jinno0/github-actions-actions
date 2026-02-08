"""
Integration tests for publish-pr action
Tests the action structure and basic functionality
"""

from pathlib import Path

import pytest
import yaml


@pytest.mark.integration
def test_publish_pr_action_structure():
    """Test publish-pr action has proper structure"""
    action_yml = Path("actions/publish-pr/action.yml")

    if not action_yml.exists():
        pytest.skip("publish-pr action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"


@pytest.mark.integration
def test_publish_pr_inputs():
    """Verify publish-pr has required inputs"""
    action_yml = Path("actions/publish-pr/action.yml")

    if not action_yml.exists():
        pytest.skip("publish-pr action not found")

    config = yaml.safe_load(action_yml.read_text())

    assert "github-token" in config["inputs"]
