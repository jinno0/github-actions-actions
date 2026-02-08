"""
Integration tests for pr-review-enqueuer action
Tests the action structure and basic functionality
"""

from pathlib import Path

import pytest
import yaml


@pytest.mark.integration
def test_pr_review_enqueuer_action_structure():
    """Test pr-review-enqueuer action has proper structure"""
    action_yml = Path("actions/pr-review-enqueuer/action.yml")

    if not action_yml.exists():
        pytest.skip("pr-review-enqueuer action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"

    # Verify required inputs
    assert "github-token" in config["inputs"]
    assert "pr-filter" in config["inputs"]


@pytest.mark.integration
def test_pr_review_enqueuer_outputs_defined():
    """Test pr-review-enqueuer action has proper outputs"""
    action_yml = Path("actions/pr-review-enqueuer/action.yml")

    if not action_yml.exists():
        pytest.skip("pr-review-enqueuer action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify outputs are defined
    outputs = config.get("outputs", {})
    assert "prs-reviewed" in outputs
    assert "prs-skipped" in outputs


@pytest.mark.integration
def test_pr_review_enqueuer_filter_options():
    """Test pr-review-enqueuer action has proper filter options"""
    action_yml = Path("actions/pr-review-enqueuer/action.yml")

    if not action_yml.exists():
        pytest.skip("pr-review-enqueuer action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify filter inputs
    assert "pr-filter" in config["inputs"]
    assert "label-filter" in config["inputs"]
    assert "age-threshold" in config["inputs"]
    assert "exclude-labels" in config["inputs"]

    # Verify defaults
    assert config["inputs"]["pr-filter"]["default"] == "all"


@pytest.mark.integration
def test_pr_review_enqueuer_steps_exist():
    """Verify pr-review-enqueuer has required steps"""
    action_yml = Path("actions/pr-review-enqueuer/action.yml")

    if not action_yml.exists():
        pytest.skip("pr-review-enqueuer action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])

    # Check for critical steps
    assert len(steps) > 0, "pr-review-enqueuer should have at least one step"
    assert any("Scan and enqueue" in s.get("name", "") for s in steps), "Should have scan step"
