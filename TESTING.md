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

**Note**: Coverage is measured only for `actions/` and `scripts/` directories.

```bash
# Measure coverage for actions/ and scripts/ only
pytest tests/ --cov=actions --cov=scripts --cov-report=html
```

## Current Coverage

### Phase 1: Structural Testing (Completed ✅)
- **Test Count**: 279 tests (13 actions)
- **Coverage**: 94.49%
- **Test Types**: Structural/smoke tests

### Phase 2: Integration Testing (Completed ✅)
- **Integration Test Files**: 13 files covering all 13 actions
- **Coverage**: 100% action-level coverage achieved (13/13 actions)
- **Current Status**: ✅ Complete
- **Test Files**:
  - `test_action_structure.py` - Generic action structure validation
  - `test_mock_claude.py` - Claude CLI mocking infrastructure
  - `test_review_and_merge_integration.py` - Review action validation
  - `test_auto_merge_integration.py` - Auto-merge action validation
  - `test_action_fixer_integration.py` - Action fixer validation
  - `test_auto_refactor_integration.py` - Auto-refactor validation
  - `test_bulk_merge_prs_integration.py` - Bulk merge validation
  - `test_publish_pr_integration.py` - Publish PR validation
  - `test_auto_rebase_integration.py` - Auto rebase validation [NEW]
  - `test_auto_document_integration.py` - Auto document validation [NEW]
  - `test_bulk_rebase_prs_integration.py` - Bulk rebase PRs validation [NEW]
  - `test_pr_review_enqueuer_integration.py` - PR review enqueuer validation [NEW]
  - `test_release_notes_ai_integration.py` - Release notes AI validation [NEW]
  - `test_review_auto_merge_integration.py` - Review auto merge validation [NEW]
  - `test_spec_to_code_integration.py` - Spec to code validation [NEW]

## Integration Test Coverage Definition

To ensure consistent quality metrics, we define integration test coverage as follows:

### Primary Metric: Action-Level Coverage

**Definition**: Percentage of Actions that have dedicated integration test files.

**Calculation**:
```
Action-Level Coverage = (Actions with integration test files / Total Actions) × 100%
```

**Example**:
- Actions with integration test files: 13
- Total Actions: 13
- Action-Level Coverage: (13/13) × 100% = 100%

**Files counted**:
- `tests/integration/test_{action_name}_integration.py`
- `tests/integration/test_action_structure.py` (covers all actions)

**Status**: ✅ **100% achieved** (13/13 actions)

### Secondary Metric: Field-Level Coverage

**Definition**: Percentage of YAML fields validated per action (future metric).

**Calculation**:
```
Field-Level Coverage = (Validated fields / Total critical fields) × 100%
```

**Critical fields include**:
- `name`
- `description`
- `inputs` (required and optional)
- `outputs` (if defined)
- `runs.using`
- `runs.steps`

**Example**:
- Validated fields: 6
- Total critical fields: 6
- Field-Level Coverage: (6/6) × 100% = 100%

**Status**: ⏳ **Not yet tracked** (future enhancement)

### Overall Coverage Calculation

**Overall Integration Test Coverage** is currently defined as **Action-Level Coverage**.

**Future**: When field-level tracking is implemented, overall coverage will be calculated as a weighted average:
```
Overall Coverage = (Action-Level × 0.7) + (Field-Level × 0.3)
```

**Rationale**: Action-level coverage is prioritized (70%) to ensure every action has basic integration tests, while field-level coverage (30%) provides depth of validation.

### Why This Definition?

**Chosen for**:
1. **Simplicity**: Easy to measure and understand
2. **Actionability**: Directly correlates to test files we create
3. **Consistency**: Matches our current reporting (53.8% → 100%)
4. **Alignment**: Aligns with TESTING.md Phase 2 goals

**Alternative not chosen**: "Percentage of YAML lines validated"
- **Reason**: Too granular, harder to measure, less meaningful

### Reporting Template

When reporting integration test coverage, use this format:

```markdown
### Integration Test Coverage

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Action-Level Coverage | 100% (13/13) | >= 50% | ✅ Achieved |
| Field-Level Coverage | N/A | TBD | ⏳ Future |
| Overall Coverage | 100% | >= 50% | ✅ Achieved |

**Actions with integration tests**:
- ✅ review-and-merge
- ✅ auto-merge
- ✅ action-fixer
- ✅ auto-refactor
- ✅ bulk-merge-prs
- ✅ publish-pr
- ✅ auto-rebase
- ✅ auto-document
- ✅ bulk-rebase-prs
- ✅ pr-review-enqueuer
- ✅ release-notes-ai
- ✅ review-auto-merge
- ✅ spec-to-code
```

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

### Phase 2: Integration Testing (Completed ✅)

**Goal**: Add tests that execute actions in controlled environments

**Status**: 100% action-level coverage achieved (13 of 13 actions)

**Coverage Definition**:
- Action-Level: 100% (13/13 actions have integration test files) ✅
- Field-Level: Not yet tracked (future enhancement)
- Overall: 100% (based on action-level coverage) ✅

See [Integration Test Coverage Definition](#integration-test-coverage-definition) above for details.

**Approach**:
1. ✅ Use YAML structure validation
2. ✅ Verify action inputs and outputs
3. ✅ Validate composite step structure
4. ⏳ Use `act` for local GitHub Actions execution (future - Phase 2b)
5. ⏳ Mock GitHub API responses (future - Phase 2b)

**Completed Actions**:
- ✅ review-and-merge
- ✅ auto-merge
- ✅ action-fixer
- ✅ auto-refactor
- ✅ bulk-merge-prs
- ✅ publish-pr
- ✅ auto-rebase
- ✅ auto-document
- ✅ bulk-rebase-prs
- ✅ pr-review-enqueuer
- ✅ release-notes-ai
- ✅ review-auto-merge
- ✅ spec-to-code
- ✅ Generic structure tests (all actions)

**Timeline**: Initial integration tests completed 2026-02-03; Full coverage achieved 2026-02-03

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
