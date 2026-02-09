"""
Integration tests for review-and-merge action
Tests the action structure and basic functionality
"""

from pathlib import Path
from typing import Any, Dict

import pytest
import yaml

# Constants
ACTION_YML_PATH: str = "actions/review-and-merge/action.yml"
DEFAULT_CLAUDE_MODEL: str = "sonnet"
DEFAULT_LGTM_THRESHOLD: str = "7"
DEFAULT_AUTO_FIX: str = "true"  # String format as stored in YAML


@pytest.fixture
def action_config() -> Dict[str, Any]:
    """Load and return the review-and-merge action configuration"""
    action_yml = Path(ACTION_YML_PATH)

    if not action_yml.exists():
        pytest.skip("review-and-merge action not found")

    return yaml.safe_load(action_yml.read_text())


@pytest.mark.integration
def test_review_and_merge_action_structure(action_config):
    """Test review-and-merge action has proper structure"""
    # Verify required fields
    assert "name" in action_config
    assert "description" in action_config
    assert "runs" in action_config
    assert action_config["runs"]["using"] == "composite"


@pytest.mark.integration
def test_review_and_merge_inputs_defined(action_config):
    """Test review-and-merge action has proper inputs"""
    # Verify required inputs
    assert "github-token" in action_config["inputs"]
    assert "claude-model" in action_config["inputs"]
    assert "lgtm-threshold" in action_config["inputs"]


@pytest.mark.integration
def test_review_and_merge_outputs_defined(action_config):
    """Test review-and-merge action has proper outputs"""
    # Verify outputs are defined
    outputs = action_config.get("outputs", {})
    assert "verdict" in outputs
    assert "confidence" in outputs


@pytest.mark.integration
def test_review_and_merge_default_values(action_config):
    """Test review-and-merge action has proper default values"""
    # Verify default values
    assert action_config["inputs"]["claude-model"]["default"] == DEFAULT_CLAUDE_MODEL
    assert action_config["inputs"]["lgtm-threshold"]["default"] == DEFAULT_LGTM_THRESHOLD
    assert action_config["inputs"]["auto-fix"]["default"] == DEFAULT_AUTO_FIX


@pytest.mark.integration
def test_review_and_merge_steps_exist(action_config):
    """Verify review-and-merge has required steps"""
    steps = action_config.get("runs", {}).get("steps", [])

    # Check for critical steps
    assert len(steps) > 0, "review-and-merge should have at least one step"
    assert any("Review or Fix" in s.get("name", "") for s in steps), "Should have review step"
    assert any("Checkout" in s.get("name", "") for s in steps), "Should have checkout step"


@pytest.mark.integration
def test_review_and_merge_scripts_referenced(action_config):
    """Verify review-and-merge references required scripts"""
    steps = action_config.get("runs", {}).get("steps", [])

    # Check that scripts are referenced
    script_refs = []
    for step in steps:
        run_cmd = step.get("run", "")
        if "review-and-fix.sh" in run_cmd or "post-comment.sh" in run_cmd:
            script_refs.append(step.get("name", ""))

    assert len(script_refs) > 0, "Should reference shell scripts"
