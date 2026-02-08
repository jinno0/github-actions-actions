"""
Integration tests for bulk-merge-prs action
Tests the action structure and basic functionality
"""

from pathlib import Path

import pytest
import yaml


@pytest.mark.integration
def test_bulk_merge_prs_action_structure():
    """Test bulk-merge-prs action has proper structure"""
    action_yml = Path("actions/bulk-merge-prs/action.yml")

    if not action_yml.exists():
        pytest.skip("bulk-merge-prs action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"


@pytest.mark.integration
def test_bulk_merge_prs_inputs():
    """Verify bulk-merge-prs has required inputs"""
    action_yml = Path("actions/bulk-merge-prs/action.yml")

    if not action_yml.exists():
        pytest.skip("bulk-merge-prs action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Check for critical inputs
    assert "github-token" in config["inputs"]
    assert "merge-method" in config["inputs"]
