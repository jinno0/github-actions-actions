# Testing Strategy

## Overview

This repository uses a **structural testing approach** for GitHub Actions. Tests validate the structure, syntax, and configuration of actions without executing them in a GitHub Actions runtime environment.

## Testing Approach

### Current Strategy: Structural/Smoke Tests

Our tests verify that actions are **properly structured** and **ready to execute**, but do not validate their runtime behavior. This is a deliberate choice based on:

1. **Runtime Requirements**: GitHub Actions require:
   - GitHub Actions runtime environment
   - GitHub API access
   - Repository context
   - Self-hosted runner with Claude CLI

2. **Test Environment**: Standard pytest environments don't provide:
   - GitHub Actions context (`github.*` variables)
   - GitHub API access
   - Repository checkout
   - Claude CLI installation

3. **Value Provided**: Structural tests catch:
   - YAML syntax errors
   - Missing required files
   - Incorrect action structure
   - Breaking changes to action interfaces

### What We Test

✅ **Tested** (Structural Validation):
- YAML syntax validity
- Required inputs are defined
- Optional inputs have defaults
- Template files exist
- Script files exist and are referenced
- Directory structure is correct
- Security patterns are present (path validation, CLI checks)
- Action uses composite run type
- Action uses bash shell

❌ **Not Tested** (Runtime Behavior):
- Actual action execution
- Real GitHub API interactions
- Claude CLI invocation
- File operations
- Error handling in practice
- Output values

## Test Structure

### Test Classes

Each action has two test classes:

1. **`Test[ActionName]Action`**: Unit tests
   - Test individual components
   - Validate structure
   - Check syntax

2. **`Test[ActionName]Integration`**: Integration tests
   - Validate YAML can be parsed
   - Check directory structure
   - Verify files are accessible

### Example Test

```python
class TestAutoDocumentAction:
    """Test suite for auto-document action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "auto-document" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    def test_action_required_inputs(self, action_path):
        """Test that all required inputs are defined."""
        action_file = action_path / "auto-document" / "action.yml"
        content = action_file.read_text()

        assert "github-token:" in content, "github-token should be defined"
        assert "required: true" in content, "github-token should be required"
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_auto_document/test_auto_document_action.py -v
```

### Run With Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

## Current Coverage

- **Test Count**: 168 tests (13 actions)
- **Coverage**: 97.51%
- **Test Types**: Structural/smoke tests only

## Known Limitations

### 1. No Functional Testing

**Issue**: Tests don't verify actions actually work when executed

**Impact**: Bugs in action logic won't be caught by tests

**Mitigation**:
- Manual testing before deployment
- Beta testing with select teams
- Monitoring in production

### 2. String-In-File Testing

**Issue**: Tests verify strings exist in files, not that they're used correctly

**Example**:
```python
# This test only checks that "claude" appears in the file
assert "claude" in content
```

**Impact**: Typos or incorrect usage might not be caught

**Mitigation**:
- Code review of action implementations
- Structural tests reduce surface area for bugs
- YAML validation catches syntax errors

### 3. No Runtime Environment

**Issue**: Tests run in standard Python environment, not GitHub Actions runtime

**Impact**: Runtime-specific issues won't be caught

**Mitigation**:
- Use [act](https://github.com/nektos/act) for local testing
- Test in staging environment before production
- Monitor first deployments carefully

## Roadmap: Future Improvements

### Phase 2: Integration Testing (Planned)

**Goal**: Add tests that execute actions in controlled environments

**Approach**:
1. Use `act` for local GitHub Actions execution
2. Mock GitHub API responses
3. Create test repositories
4. Verify action outputs

**Example**:
```python
@pytest.mark.integration
def test_auto_document_generates_docs(self, action_runner):
    """Test that auto-document actually generates documentation."""
    result = action_runner.run(
        action="auto-document",
        inputs={
            "source-path": "test_src",
            "doc-path": "test_docs/README.md"
        }
    )

    assert result.exit_code == 0
    assert (Path("test_docs/README.md").exists())
```

**Timeline**: Next quarter (after self-hosted runner infrastructure is ready)

### Phase 3: End-to-End Testing (Future)

**Goal**: Test complete workflows with real GitHub API

**Approach**:
1. Create test GitHub repositories
2. Execute actions via real GitHub API
3. Verify results
4. Cleanup test data

**Timeline**: When dedicated testing environment is available

## Contributing Tests

When adding tests for new actions:

1. **Follow Existing Patterns**: Use the same structure as existing tests
2. **Test Structure, Not Behavior**: Focus on YAML syntax, file existence, inputs/outputs
3. **Use Fixtures**: Leverage `action_path` fixture from conftest.py
4. **Document Intent**: Add docstrings explaining what each test validates
5. **Mark Tests**: Use pytest markers for categorization

### Template for New Tests

```python
"""Tests for the [action-name] GitHub Action."""

import pytest
from pathlib import Path


class Test[ActionName]Action:
    """Test suite for [action-name] action."""

    def test_action_yaml_exists(self, action_path):
        """Test that the action.yml file exists and is valid."""
        action_file = action_path / "[action-name]" / "action.yml"
        assert action_file.exists(), "action.yml should exist"
        content = action_file.read_text()
        assert "name:" in content
        assert "description:" in content
        assert "inputs:" in content

    # Add more structural tests here...


class Test[ActionName]Integration:
    """Integration tests for [action-name] action."""

    def test_action_yaml_syntax(self, action_path):
        """Test that action.yml has valid YAML syntax."""
        import yaml
        action_file = action_path / "[action-name]" / "action.yml"

        with open(action_file) as f:
            config = yaml.safe_load(f)

        assert config is not None
        assert "name" in config
        assert "inputs" in config
        assert "runs" in config
```

## Testing Philosophy

### Why Structural Testing?

1. **Fast Feedback**: Tests run in milliseconds without external dependencies
2. **High Coverage**: Achieves 97.51% coverage with minimal infrastructure
3. **Catches Common Errors**: Most issues are structural (YAML syntax, missing files)
4. **Maintainable**: Simple to understand and modify

### Trade-offs

| Aspect | Structural Tests | Functional Tests |
|--------|-----------------|------------------|
| Speed | ✅ Fast | ❌ Slow |
| Infrastructure | ✅ Minimal | ❌ Complex |
| Coverage | ⚠️ Structure only | ✅ End-to-end |
| Maintenance | ✅ Simple | ❌ Complex |
| Confidence | ⚠️ Medium | ✅ High |

### Our Choice

We prioritize **speed and maintainability** with structural tests, while recognizing we need **functional tests** for higher confidence. The roadmap outlines how we'll add functional testing incrementally.

## Questions?

See also:
- `README.md`: Repository overview
- `AGENTS.md`: Agent development guidelines
- `conftest.py`: Test fixtures and configuration
