"""Pytest configuration and fixtures for AI Hub Actions testing."""

import os
import tempfile
import shutil
from pathlib import Path
import pytest
import subprocess


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test artifacts."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_pr_diff():
    """Sample PR diff for testing."""
    return """diff --git a/src/example.py b/src/example.py
index 1234567..abcdefg 100644
--- a/src/example.py
+++ b/src/example.py
@@ -1,5 +1,10 @@
 def hello():
-    print("Hello")
+    print("Hello World")
     return True
+
+def new_function():
+    return "new"
"""


@pytest.fixture
def sample_spec():
    """Sample Markdown spec for testing."""
    return """---
language: python
---

# Data Processing Function

## Requirements
- Read data from input
- Process data with transformations
- Return processed result

## Interface
```python
def process_data(input_data: dict) -> dict:
    pass
```

## Examples
```python
result = process_data({"value": 10})
```
"""


@pytest.fixture
def mock_repo(temp_dir):
    """Create a mock git repository for testing."""
    repo_path = Path(temp_dir) / "test-repo"
    repo_path.mkdir()

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_path,
        check=True,
        capture_output=True,
    )

    # Create initial commit
    (repo_path / "README.md").write_text("# Test Repo")
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=repo_path,
        check=True,
        capture_output=True,
    )

    yield repo_path
    shutil.rmtree(repo_path, ignore_errors=True)


@pytest.fixture
def action_path():
    """Get the path to the actions directory."""
    return Path(__file__).parent.parent / "actions"
