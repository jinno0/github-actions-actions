"""
Integration tests for action-fixer action
Tests the action structure and basic functionality
"""

import pytest
import yaml
from pathlib import Path


@pytest.mark.integration
def test_action_fixer_action_structure():
    """Test action-fixer has proper structure"""
    action_yml = Path("actions/action-fixer/action.yml")

    if not action_yml.exists():
        pytest.skip("action-fixer action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"


@pytest.mark.integration
def test_action_fixer_inputs():
    """Verify action-fixer has required inputs"""
    action_yml = Path("actions/action-fixer/action.yml")

    if not action_yml.exists():
        pytest.skip("action-fixer action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Check for important inputs
    assert "github-token" in config["inputs"]
    assert "claude-model" in config["inputs"]


@pytest.mark.integration
def test_action_fixer_steps_exist():
    """Verify action-fixer has execution steps"""
    action_yml = Path("actions/action-fixer/action.yml")

    if not action_yml.exists():
        pytest.skip("action-fixer action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])
    assert len(steps) > 0, "action-fixer should have at least one step"
