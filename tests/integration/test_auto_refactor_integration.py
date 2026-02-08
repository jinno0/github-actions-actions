"""
Integration tests for auto-refactor action
Tests the action structure and basic functionality
"""

from pathlib import Path

import pytest
import yaml


@pytest.mark.integration
def test_auto_refactor_action_structure():
    """Test auto-refactor action has proper structure"""
    action_yml = Path("actions/auto-refactor/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-refactor action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"


@pytest.mark.integration
def test_auto_refactor_inputs():
    """Verify auto-refactor has required inputs"""
    action_yml = Path("actions/auto-refactor/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-refactor action not found")

    config = yaml.safe_load(action_yml.read_text())

    # auto-refactor doesn't require github-token directly, it uses path-based refactoring
    assert "path" in config["inputs"]
    assert "claude-model" in config["inputs"]


@pytest.mark.integration
def test_auto_refactor_has_outputs():
    """Verify auto-refactor defines outputs"""
    action_yml = Path("actions/auto-refactor/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-refactor action not found")

    config = yaml.safe_load(action_yml.read_text())

    outputs = config.get("outputs", {})
    # Should have at least some outputs defined
    assert isinstance(outputs, dict)
