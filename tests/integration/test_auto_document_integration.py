"""
Integration tests for auto-document action
Tests the action structure and basic functionality
"""

from pathlib import Path

import pytest
import yaml


@pytest.mark.integration
def test_auto_document_action_structure():
    """Test auto-document action has proper structure"""
    action_yml = Path("actions/auto-document/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-document action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"

    # Verify required inputs
    assert "source-path" in config["inputs"]
    assert "doc-path" in config["inputs"]
    assert "claude-model" in config["inputs"]


@pytest.mark.integration
def test_auto_document_default_values():
    """Test auto-document action has proper defaults"""
    action_yml = Path("actions/auto-document/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-document action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify default values
    source_path = config["inputs"]["source-path"]
    assert source_path["default"] == "."

    doc_path = config["inputs"]["doc-path"]
    assert doc_path["default"] == "README.md"


@pytest.mark.integration
def test_auto_document_steps_exist():
    """Verify auto-document has required steps"""
    action_yml = Path("actions/auto-document/action.yml")

    if not action_yml.exists():
        pytest.skip("auto-document action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])
    step_names = [s.get("name", s.get("id", "")) for s in steps]

    # Check for critical steps
    assert len(steps) > 0, "auto-document should have at least one step"
    assert any("Update Documentation" in name for name in step_names), "Should have documentation update step"
