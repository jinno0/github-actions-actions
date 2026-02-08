"""Example test file for pytest setup verification."""

from pathlib import Path


def test_repo_purpose():
    """Verify the repository purpose is documented."""
    readme = Path("README.md")
    assert readme.exists(), "README.md should exist"
    content = readme.read_text()
    assert "AI Hub" in content, "README should mention AI Hub"
    assert "GitHub Actions" in content, "README should mention GitHub Actions"


def test_purpose_file_exists():
    """Verify PURPOSE.md exists."""
    purpose = Path("PURPOSE.md")
    assert purpose.exists(), "PURPOSE.md should exist"
