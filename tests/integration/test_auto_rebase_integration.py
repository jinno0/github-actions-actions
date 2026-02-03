"""
Integration tests for auto-rebase action
Tests the action structure and basic functionality
"""

import pytest
import yaml
from pathlib import Path


@pytest.mark.integration
def test_auto_rebase_action_structure():
    """Test auto-rebase action has proper structure"""
    action_yml = Path("actions/auto-rebase/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-rebase action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"

    # Verify required inputs
    assert "github-token" in config["inputs"]
    assert "rebase-strategy" in config["inputs"]


@pytest.mark.integration
def test_auto_rebase_outputs_defined():
    """Test auto-rebase action has proper outputs"""
    action_yml = Path("actions/auto-rebase/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-rebase action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify outputs are defined
    outputs = config.get("outputs", {})
    assert "rebased" in outputs
    assert "conflicts-resolved" in outputs
    assert "conflict-count" in outputs


@pytest.mark.integration
def test_auto_rebase_steps_exist():
    """Verify auto-rebase has required steps"""
    action_yml = Path("actions/auto-rebase/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-rebase action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])
    step_names = [s.get("name", s.get("id", "")) for s in steps]

    # Check for critical steps
    assert len(steps) > 0, "auto-rebase should have at least one step"
    assert any("Checkout PR" in name for name in step_names), "Should have checkout step"
    assert any("Rebase" in name for name in step_names), "Should have rebase step"
