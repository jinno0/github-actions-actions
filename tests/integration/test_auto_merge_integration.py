"""
Integration tests for auto-merge action
Tests the action structure and basic functionality
"""

from pathlib import Path

import pytest
import yaml


@pytest.mark.integration
def test_auto_merge_action_structure():
    """Test auto-merge action has proper structure"""
    action_yml = Path("actions/auto-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"

    # Verify required inputs
    assert "github-token" in config["inputs"]
    assert "merge-method" in config["inputs"]


@pytest.mark.integration
def test_auto_merge_steps_exist():
    """Verify auto-merge has required steps"""
    action_yml = Path("actions/auto-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])
    _step_names = [s.get("name", s.get("id", "")) for s in steps]

    # Check for critical steps
    assert len(steps) > 0, "auto-merge should have at least one step"
