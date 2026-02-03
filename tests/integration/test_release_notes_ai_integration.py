"""
Integration tests for release-notes-ai action
Tests the action structure and basic functionality
"""

import pytest
import yaml
from pathlib import Path


@pytest.mark.integration
def test_release_notes_ai_action_structure():
    """Test release-notes-ai action has proper structure"""
    action_yml = Path("actions/release-notes-ai/action.yml")

    if not action_yml.exists():
        pytest.skip("release-notes-ai action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"

    # Verify required inputs
    assert "base-ref" in config["inputs"]
    assert "head-ref" in config["inputs"]
    assert "output-file" in config["inputs"]


@pytest.mark.integration
def test_release_notes_ai_default_values():
    """Test release-notes-ai action has proper defaults"""
    action_yml = Path("actions/release-notes-ai/action.yml")

    if not action_yml.exists():
        pytest.skip("release-notes-ai action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify default values
    base_ref = config["inputs"]["base-ref"]
    assert base_ref["default"] == "main"

    head_ref = config["inputs"]["head-ref"]
    assert head_ref["default"] == "HEAD"

    output_file = config["inputs"]["output-file"]
    assert output_file["default"] == "RELEASE_NOTES.md"


@pytest.mark.integration
def test_release_notes_ai_template_support():
    """Test release-notes-ai action supports custom templates"""
    action_yml = Path("actions/release-notes-ai/action.yml")

    if not action_yml.exists():
        pytest.skip("release-notes-ai action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify template input
    assert "release-prompt-template" in config["inputs"]
    assert "claude-model" in config["inputs"]


@pytest.mark.integration
def test_release_notes_ai_steps_exist():
    """Verify release-notes-ai has required steps"""
    action_yml = Path("actions/release-notes-ai/action.yml")

    if not action_yml.exists():
        pytest.skip("release-notes-ai action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])

    # Check for critical steps
    assert len(steps) > 0, "release-notes-ai should have at least one step"
    assert any("Generate Release Notes" in s.get("name", "") for s in steps), "Should have generation step"
