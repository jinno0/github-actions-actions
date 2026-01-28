# Test Documentation
## AI Hub GitHub Actions Test Suite

**Document Version:** 1.0
**Created:** 2026-01-29
**Status:** ✅ Complete

---

## Overview

This document describes the test suite for AI Hub GitHub Actions, including security tests, functional tests, and integration tests for the implemented actions.

---

## Test Structure

```
tests/
├── conftest.py                          # Pytest fixtures and configuration
├── __init__.py                          # Test package initialization
├── test_review_and_merge/
│   ├── test_security.py                 # Security tests for review-and-merge
│   └── test_functional.py               # Functional tests for review-and-merge
└── test_spec_to_code/
    ├── test_security.py                 # Security tests for spec-to-code
    └── test_functional.py               # Functional tests for spec-to-code
```

---

## Running Tests

### Run All Tests
```bash
cd /home/jinno/github-actions-actions
pytest
```

### Run Specific Test File
```bash
pytest tests/test_review_and_merge/test_security.py
```

### Run Specific Test Class
```bash
pytest tests/test_review_and_merge/test_security.py::TestPathTraversal
```

### Run Specific Test
```bash
pytest tests/test_review_and_merge/test_security.py::TestPathTraversal::test_pr_diff_with_path_traversal
```

### Run with Coverage
```bash
pytest --cov=actions --cov-report=html
```

### Run Security Tests Only
```bash
pytest -m security
```

---

## Test Categories

### 1. Security Tests

#### Purpose
Verify that actions handle malicious input safely and don't introduce security vulnerabilities.

#### Coverage

**Story 1.1: review-and-merge**
- ✅ Path traversal protection
- ✅ Command injection prevention
- ✅ Resource limit enforcement
- ✅ Privilege escalation prevention
- ✅ Data exfiltration prevention
- ✅ Sandboxing verification

**Story 2.1: spec-to-code**
- ✅ Path traversal validation
- ✅ Command injection prevention
- ✅ Code injection handling
- ✅ Resource limit enforcement
- ✅ Privilege escalation prevention
- ✅ Data leakage prevention
- ✅ Template security

### 2. Functional Tests

#### Purpose
Verify that core functionality works as expected.

#### Coverage

**Story 1.1: review-and-merge**
- ✅ Review mode functionality
- ✅ Auto-fix mode functionality
- ✅ Git operations (commit, push)
- ✅ JSON output parsing
- ✅ Comment posting
- ✅ Error handling
- ✅ Input validation

**Story 2.1: spec-to-code**
- ✅ Action structure verification
- ✅ Required inputs validation
- ✅ Template functionality
- ✅ Spec validation
- ✅ Code generation logic
- ✅ Custom template support
- ✅ Output directory handling
- ✅ Error handling
- ✅ Multi-language support
- ✅ Spec format handling

### 3. Integration Tests (TODO)

#### Purpose
Verify end-to-end functionality with real dependencies.

#### Planned Coverage
- [ ] Full PR review workflow
- [ ] Full code generation workflow
- [ ] Error recovery scenarios
- [ ] Performance benchmarks

---

## Test Fixtures

### Available Fixtures

#### `temp_dir`
Creates a temporary directory for test artifacts. Automatically cleaned up after each test.

#### `sample_pr_diff`
Provides a sample PR diff for testing review functionality.

#### `sample_spec`
Provides a sample Markdown specification for testing code generation.

#### `mock_repo`
Creates a mock git repository with initial commit for testing git operations.

#### `action_path`
Returns the path to the actions directory.

---

## Test Results Summary

### Current Status
- **Total Tests:** 60+
- **Security Tests:** 13
- **Functional Tests:** 47
- **Integration Tests:** 0 (TODO)

### Coverage by Story

#### STORY-1.1: review-and-merge
| Category | Tests | Status |
|----------|-------|--------|
| Security | 6 | ✅ Complete |
| Functional | 23 | ✅ Complete |
| Integration | 0 | ⏳ TODO |
| **Total** | **29** | **77%** |

#### STORY-2.1: spec-to-code
| Category | Tests | Status |
|----------|-------|--------|
| Security | 7 | ✅ Complete |
| Functional | 24 | ✅ Complete |
| Integration | 0 | ⏳ TODO |
| **Total** | **31** | **77%** |

---

## Known Issues and Limitations

### Current Limitations

1. **No Real Claude CLI Testing**
   - Tests verify structure but don't invoke actual Claude CLI
   - Integration tests needed for end-to-end validation

2. **No Network Testing**
   - All tests run offline
   - Network-dependent features not tested

3. **Mock-Only Git Operations**
   - Git operations tested with mock repositories
   - Real GitHub API interactions not tested

4. **No Performance Testing**
   - No benchmarks for large diffs/specs
   - No concurrency testing

### Future Enhancements

1. **Integration Tests**
   - Test with real Claude CLI
   - Test with real GitHub repositories
   - Test error scenarios with network failures

2. **Performance Tests**
   - Benchmark large PR reviews
   - Benchmark large spec generation
   - Concurrent execution tests

3. **End-to-End Tests**
   - Complete workflow automation tests
   - Multi-action orchestration tests

---

## Test Maintenance

### Adding New Tests

1. Create test file in appropriate directory
2. Use descriptive test names
3. Group tests into logical classes
4. Use fixtures for common setup
5. Mark tests with appropriate markers

### Example Test Structure

```python
"""Test description."""

import pytest
from pathlib import Path


class TestFeature:
    """Feature description."""

    def test_specific_behavior(self, temp_dir):
        """Test that specific behavior works correctly."""
        # Arrange
        test_data = "example"

        # Act
        result = process(test_data)

        # Assert
        assert result == expected
```

---

## Continuous Integration

### GitHub Actions Workflow

Test suite should run on:
- Every pull request
- Every push to main branch
- Nightly builds

### Required Dependencies

```bash
# Install test dependencies
pip install pytest pytest-cov

# Install additional dependencies
pip install pyyaml
```

---

## Test Data Management

### Test Artifacts
- Temporary files stored in `/tmp` during tests
- Automatically cleaned up after test run
- No persistent state between tests

### Mock Data
- Sample PR diffs in `conftest.py`
- Sample specs in `conftest.py`
- Mock repositories created per test

---

## Security Considerations

### Test Security
- Tests don't require real credentials
- No access to production systems
- No network calls to external services
- Mock data only, no real secrets

### Safe Testing Practices
- Use test-specific repositories
- Never test on production data
- Clean up test artifacts
- Verify no data leakage

---

## Troubleshooting

### Common Issues

#### Tests Fail to Find Actions
**Problem:** `FileNotFoundError: action.yml not found`

**Solution:** Run tests from repository root:
```bash
cd /home/jinno/github-actions-actions
pytest
```

#### Tests Skip Unexpectedly
**Problem:** Tests marked as skipped

**Solution:** Verify all dependencies are installed:
```bash
pip install -r requirements-dev.txt
```

#### Fixture Errors
**Problem:** `fixture 'temp_dir' not found`

**Solution:** Verify `conftest.py` exists in `tests/` directory

---

## References

### Related Documentation
- [CODE_REVIEW_FINDINGS.md](.bmad/CODE_REVIEW_FINDINGS.md) - Issues found during code review
- [PRD.md](.bmad/prd/product-requirements-document.md) - Product requirements
- [ARCHITECTURE.md](.bmad/architecture/architecture-decision-document.md) - Architecture decisions

### Test Frameworks
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

---

## Appendix

### Test Command Reference

```bash
# Basic usage
pytest                                    # Run all tests
pytest -v                                 # Verbose output
pytest -s                                 # Show print statements
pytest --tb=long                          # Full tracebacks

# Selection
pytest tests/test_review_and_merge/       # Run specific directory
pytest -k "security"                      # Run tests matching keyword
pytest -m "security"                      # Run marked tests

# Output
pytest --html=report.html                 # Generate HTML report
pytest --cov=actions                      # Coverage report
pytest --junitxml=results.xml             # JUnit XML output

# Debugging
pytest -pdb                               # Drop into debugger on failure
pytest --trace                            # Trace test execution
pytest -l                                 # Show local variables on failure
```

---

**Document Status:** ✅ Complete
**Next Review:** After integration tests implementation
**Maintainer:** AI Hub Development Team
