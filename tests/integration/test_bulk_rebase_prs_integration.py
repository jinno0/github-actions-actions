"""
Integration tests for bulk-rebase-prs action
Tests the action structure and basic functionality
"""

import pytest
import yaml
from pathlib import Path


@pytest.mark.integration
def test_bulk_rebase_prs_action_structure():
    """Test bulk-rebase-prs action has proper structure"""
    action_yml = Path("actions/bulk-rebase-prs/action.yml")

    if not action_yml.exists():
        pytest.skip("bulk-rebase-prs action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"

    # Verify required inputs
    assert "github-token" in config["inputs"]
    assert "limit" in config["inputs"]
    assert "merge-state-status" in config["inputs"]


@pytest.mark.integration
def test_bulk_rebase_prs_filter_options():
    """Test bulk-rebase-prs action has proper filter options"""
    action_yml = Path("actions/bulk-rebase-prs/action.yml")

    if not action_yml.exists():
        pytest.skip("bulk-rebase-prs action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify filter inputs
    assert "dry-run" in config["inputs"]
    assert "merge-state-status" in config["inputs"]

    # Verify defaults
    assert config["inputs"]["limit"]["default"] == "0"
    assert config["inputs"]["merge-state-status"]["default"] == "BEHIND"


@pytest.mark.integration
def test_bulk_rebase_prs_steps_exist():
    """Verify bulk-rebase-prs has required steps"""
    action_yml = Path("actions/bulk-rebase-prs/action.yml")

    if not action_yml.exists():
        pytest.skip("bulk-rebase-prs action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])

    # Check for critical steps
    assert len(steps) > 0, "bulk-rebase-prs should have at least one step"
    assert any("Bulk Rebase PRs" in s.get("name", "") for s in steps), "Should have bulk rebase step"
