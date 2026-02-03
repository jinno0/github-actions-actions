"""
Integration tests for spec-to-code action
Tests the action structure and basic functionality
"""

import pytest
import yaml
from pathlib import Path


@pytest.mark.integration
def test_spec_to_code_action_structure():
    """Test spec-to-code action has proper structure"""
    action_yml = Path("actions/spec-to-code/action.yml")

    if not action_yml.exists():
        pytest.skip("spec-to-code action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify required fields
    assert "name" in config
    assert "description" in config
    assert "runs" in config
    assert config["runs"]["using"] == "composite"

    # Verify required inputs
    assert "spec-path" in config["inputs"]
    assert "output-dir" in config["inputs"]
    assert "language" in config["inputs"]


@pytest.mark.integration
def test_spec_to_code_required_inputs():
    """Test spec-to-code action has required inputs"""
    action_yml = Path("actions/spec-to-code/action.yml")

    if not action_yml.exists():
        pytest.skip("spec-to-code action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify spec-path is required
    assert config["inputs"]["spec-path"]["required"] == True


@pytest.mark.integration
def test_spec_to_code_default_values():
    """Test spec-to-code action has proper defaults"""
    action_yml = Path("actions/spec-to-code/action.yml")

    if not action_yml.exists():
        pytest.skip("spec-to-code action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify default values
    output_dir = config["inputs"]["output-dir"]
    assert output_dir["default"] == "."

    language = config["inputs"]["language"]
    assert language["default"] == "TypeScript"


@pytest.mark.integration
def test_spec_to_code_template_support():
    """Test spec-to-code action supports custom templates"""
    action_yml = Path("actions/spec-to-code/action.yml")

    if not action_yml.exists():
        pytest.skip("spec-to-code action not found")

    config = yaml.safe_load(action_yml.read_text())

    # Verify template input
    assert "gen-prompt-template" in config["inputs"]
    assert "claude-model" in config["inputs"]


@pytest.mark.integration
def test_spec_to_code_steps_exist():
    """Verify spec-to-code has required steps"""
    action_yml = Path("actions/spec-to-code/action.yml")

    if not action_yml.exists():
        pytest.skip("spec-to-code action not found")

    config = yaml.safe_load(action_yml.read_text())

    steps = config.get("runs", {}).get("steps", [])
    step_names = [s.get("name", s.get("id", "")) for s in steps]

    # Check for critical steps
    assert len(steps) > 0, "spec-to-code should have at least one step"
    assert any("Generate Code" in name for name in step_names), "Should have generation step"
    assert any("Validate Spec Path" in name for name in step_names), "Should have validation step"
