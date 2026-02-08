"""
Integration tests for review-and-merge action
Tests the action structure and basic functionality
"""

from pathlib import Path

import pytest
import yaml


@pytest.mark.integration
def test_review_and_merge_action_structure():
    """Test review-and-merge action has proper structure"""
    action_yml = Path("actions/review-and-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-and-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"


@pytest.mark.integration
def test_review_and_merge_inputs_defined():
    """Test review-and-merge action has proper inputs"""
    action_yml = Path("actions/review-and-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-and-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required inputs
    assert "github-token" in config["inputs"]
    assert "claude-model" in config["inputs"]
    assert "lgtm-threshold" in config["inputs"]


@pytest.mark.integration
def test_review_and_merge_outputs_defined():
    """Test review-and-merge action has proper outputs"""
    action_yml = Path("actions/review-and-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-and-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify outputs are defined
    outputs = config.get("outputs", {})
    assert "verdict" in outputs
    assert "confidence" in outputs


@pytest.mark.integration
def test_review_and_merge_default_values():
    """Test review-and-merge action has proper default values"""
    action_yml = Path("actions/review-and-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-and-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify default values
    assert config["inputs"]["claude-model"]["default"] == "sonnet"
    assert config["inputs"]["lgtm-threshold"]["default"] == "7"
    assert config["inputs"]["auto-fix"]["default"] == "true"


@pytest.mark.integration
def test_review_and_merge_steps_exist():
    """Verify review-and-merge has required steps"""
    action_yml = Path("actions/review-and-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-and-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])

    # Check for critical steps
    assert len(steps) > 0, "review-and-merge should have at least one step"
    assert any("Review or Fix" in s.get("name", "") for s in steps), "Should have review step"
    assert any("Checkout" in s.get("name", "") for s in steps), "Should have checkout step"


@pytest.mark.integration
def test_review_and_merge_scripts_referenced():
    """Verify review-and-merge references required scripts"""
    action_yml = Path("actions/review-and-merge/action.yml")

    if not action_yml.exists():
        pytest.skip("review-and-merge action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])

    # Check that scripts are referenced
    script_refs = []
    for step in steps:
        run_cmd = step.get("run", "")
        if "review-and-fix.sh" in run_cmd or "post-comment.sh" in run_cmd:
            script_refs.append(step.get("name", ""))

    assert len(script_refs) > 0, "Should reference shell scripts"
