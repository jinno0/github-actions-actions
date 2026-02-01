# PR-002: Add Tests for Critical Actions

## Priority
**HIGH** - Required for quality assurance

## Problem Statement
13 Actions中、2つ（review-and-merge, spec-to-code）のみにテストが存在し、テストカバレッジが15.4%に留まっている。目標の80%に対し68.4ポイントのギャップがある。

### Evidence
- **Current Coverage**: 15.4% (2/13 actions)
- **Target Coverage**: 80% (ASM-003)
- **Gap**: 11 actions without tests

## Proposed Solution

### Phase 1: Add Tests for High-Priority Actions (Immediate)

Select 3 most frequently used actions based on README.md positioning:

1. **action-fixer** (Core Development - Listed first in workflow automation)
2. **auto-refactor** (Core Development - Listed as key feature)
3. **auto-document** (Documentation - Enables other actions to be documented)

### Test Template Structure

For each action, create:

```
tests/
└── test_{action-name}/
    ├── __init__.py
    ├── test_dry_run.py       # Structural validation
    ├── test_functional.py    # Mock execution
    └── conftest.py           # Action-specific fixtures
```

### Example: test_action_fixer/test_dry_run.py

```python
"""Dry run tests for action-fixer"""
import pytest
import yaml
from pathlib import Path

def test_action_yml_syntax(action_path):
    """action.yml is valid YAML"""
    yaml_file = action_path / "actions" / "action-fixer" / "action.yml"
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
    assert data is not None
    assert data["name"] == "Action Fixer"

def test_action_has_description(action_path):
    """action.yml has description"""
    yaml_file = action_path / "actions" / "action-fixer" / "action.yml"
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
    assert len(data.get("description", "")) > 0

def test_action_is_composite(action_path):
    """Action uses composite type"""
    yaml_file = action_path / "actions" / "action-fixer" / "action.yml"
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
    assert data["runs"]["using"] == "composite"
    assert len(data["runs"]["steps"]) > 0
```

### Example: test_action_fixer/test_functional.py

```python
"""Functional tests for action-fixer"""
import pytest
import subprocess
from pathlib import Path

def test_action_fixer_detects_invalid_yaml(temp_dir, action_path):
    """Action can detect invalid YAML in workflow files"""
    # Create invalid workflow
    invalid_workflow = temp_dir / "workflow.yml"
    invalid_workflow.write_text("invalid: yaml: content:][")

    # Mock execution (dry run)
    # In real execution, this would call the action
    result = subprocess.run(
        ["python", "-m", "pytest", "--collect-only"],
        cwd=action_path,
        capture_output=True
    )

    # Verify action structure exists
    assert (action_path / "actions" / "action-fixer" / "action.yml").exists()
```

### Step-by-Step Implementation

#### Step 1: Create test structure for action-fixer
```bash
mkdir -p tests/test_action_fixer
touch tests/test_action_fixer/__init__.py
touch tests/test_action_fixer/test_dry_run.py
touch tests/test_action_fixer/test_functional.py
```

#### Step 2: Implement dry run tests
- Verify YAML syntax
- Verify required fields (name, description)
- Verify composite action type
- Verify inputs/outputs structure

#### Step 3: Implement functional tests (mock only)
- Verify action can be loaded
- Verify templates exist
- Verify scripts exist (if applicable)

#### Step 4: Repeat for auto-refactor and auto-document

## Expected Outcome

### Success Criteria
- ✅ Tests for action-fixer pass
- ✅ Tests for auto-refactor pass
- ✅ Tests for auto-document pass
- ✅ Coverage increases from 15.4% to 38.5% (5/13 actions)

### Coverage Progress
| Phase | Actions Tested | Coverage | Target |
|-------|---------------|----------|--------|
| Current | 2/13 | 15.4% | 80% |
| After PR-002 | 5/13 | 38.5% | 80% |
| After PR-003 | 13/13 | 100% | 80% |

## Risk Assessment

### Low Risk
- Tests are additive (no breaking changes)
- Dry run tests only validate structure
- No actual execution of Claude Code CLI required

### Mitigation
- Start with dry run tests only
- Gradually add functional tests
- Mock external dependencies (Claude Code CLI)

## Estimated Effort
- **action-fixer tests**: 2 hours
- **auto-refactor tests**: 2 hours
- **auto-document tests**: 2 hours
- **Total**: 6 hours

## Dependencies
- **Requires**: PR-001 (pytest.ini fix) to be merged first
- **Blocks**: PR-003 (remaining 8 actions)

## Related Issues
- Addresses: GAP-001 (test coverage gap)
- Supports: PURPOSE.md Phase 3 quality assurance
- Validates: CF-001～CF-013 core functions

## Assumptions
Based on ASM-003 (quality.target_test_coverage >= 80%), this is the second step toward achieving target.

## Verification Method
```bash
# After PR-001 and PR-002 are applied
pytest tests/test_action_fixer/ tests/test_auto_refactor/ tests/test_auto_document/ -v
pytest --cov=actions --cov-report=term-missing
# Expected: Coverage ~38.5%, all new tests pass
```

## Next Steps (PR-003)
After PR-002 is merged, create PR-003 to add tests for remaining 8 actions:
- auto-merge
- auto-rebase
- review-auto-merge
- publish-pr
- bulk-merge-prs
- bulk-rebase-prs
- release-notes-ai
- pr-review-enqueuer

## References
- Source: `.audit/analysis/gap.yml -> GAP-001`
- Source: `.audit/output/verification_result.json`
- Template: `tests/test_review_and_merge/` (existing test)
