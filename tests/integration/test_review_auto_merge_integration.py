"""
Integration tests for review-auto-merge action
Tests the action structure and basic functionality
"""

import pytest
import yaml
from pathlib import Path


@pytest.mark.integration
def test_review_auto_merge_action_structure():
    """Test review-auto-merge action has proper structure"""
    action_yml = Path("actions/review-auto-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-auto-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"

    # Verify required inputs
    assert "github-token" in config["inputs"]
    assert "max-attempts" in config["inputs"]


@pytest.mark.integration
def test_review_auto_merge_outputs_defined():
    """Test review-auto-merge action has proper outputs"""
    action_yml = Path("actions/review-auto-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-auto-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify outputs are defined
    outputs = config.get("outputs", {})
    assert "merged" in outputs


@pytest.mark.integration
def test_review_auto_merge_retry_logic():
    """Test review-auto-merge action has retry configuration"""
    action_yml = Path("actions/review-auto-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-auto-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify max-attempts input
    assert "max-attempts" in config["inputs"]
    assert config["inputs"]["max-attempts"]["default"] == "5"


@pytest.mark.integration
def test_review_auto_merge_steps_exist():
    """Verify review-auto-merge has required steps"""
    action_yml = Path("actions/review-auto-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-auto-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])

    # Check for critical steps
    assert len(steps) > 0, "review-auto-merge should have at least one step"
    assert any("Merge PR" in s.get("name", "") for s in steps), "Should have merge step"
