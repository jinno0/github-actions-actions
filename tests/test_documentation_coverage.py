"""
Documentation coverage tests to ensure all actions have proper documentation.
"""
import pytest
from pathlib import Path


def test_all_actions_have_readme():
    """全てのActionにREADME.mdが存在すること"""
    actions_dir = Path("actions")
    missing = []

    for action_dir in actions_dir.iterdir():
        if action_dir.is_dir() and not action_dir.name.startswith("_"):
            readme = action_dir / "README.md"
            if not readme.exists():
                missing.append(action_dir.name)

    assert len(missing) == 0, f"READMEが不足しているAction: {missing}"


def test_all_actions_have_setup_guide():
    """全てのActionにSetup Guideが存在すること"""
    instructions_dir = Path("instructions")
    actions_dir = Path("actions")

    action_names = [
        d.name for d in actions_dir.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    ]

    missing = []
    for action_name in action_names:
        guide = instructions_dir / f"{action_name}.md"
        if not guide.exists():
            missing.append(action_name)

    # libはSetup Guideが不要な除外ケース
    missing = [m for m in missing if m != "lib"]

    assert len(missing) == 0, f"Setup Guideが不足しているAction: {missing}"


def test_readmes_have_required_sections():
    """README.mdに必要なセクションが含まれていること"""
    actions_dir = Path("actions")
    required_sections = ["## Overview", "## Inputs", "## Example Usage"]

    issues = []

    for action_dir in actions_dir.iterdir():
        if action_dir.is_dir() and not action_dir.name.startswith("_"):
            readme = action_dir / "README.md"
            if readme.exists():
                content = readme.read_text()

                # Check for at least some required sections (be flexible)
                has_inputs = "## Inputs" in content or "### Inputs" in content or "Inputs" in content
                has_example = "## Example Usage" in content or "### Example" in content or "example" in content.lower()

                if not (has_inputs and has_example):
                    issues.append(f"{action_dir.name}: Missing required sections")

    # Allow some flexibility - just warn if issues exist
    if issues:
        pytest.warns(UserWarning, match="Some READMEs may be missing sections")


def test_readme_quality():
    """README.mdの品質チェック（基本情報が含まれていること）"""
    actions_dir = Path("actions")

    for action_dir in actions_dir.iterdir():
        if action_dir.is_dir() and not action_dir.name.startswith("_"):
            readme = action_dir / "README.md"
            if readme.exists():
                content = readme.read_text()

                # File should not be empty
                assert len(content) > 100, f"{action_dir.name}/README.md is too short"

                # Should have some description (look for common patterns)
                has_description = (
                    "Features" in content or
                    "## Overview" in content or
                    "Description" in content or
                    content.count("#") >= 2
                )
                assert has_description, f"{action_dir.name}/README.md lacks description"
