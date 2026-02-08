# PR-003: Add Shell Script Testing Framework

**Priority:** Medium
**Status:** Proposed
**Gap ID:** TG-001, I-003, U-005
**Assumption Dependency:** I-003 (shell scripts are untested), ASM-002 (coverage target 80%)

## Problem Statement

Current test coverage is 92.99%, but this only covers Python scripts (`scripts/` and `actions/lib/`).
The actual action implementations (shell scripts in `actions/*/scripts/`) have **zero test coverage**.

Evidence:
- Only 2 Python files exist in `actions/` directory
- 15 action directories exist, most using shell scripts
- pytest coverage report shows only `scripts/` and `actions/lib/`
- No shell script test framework is configured

This creates a **coverage illusion**:
- We think we have 92.99% coverage
- But the actual action logic (shell scripts) is untested
- Quality guarantees don't extend to production code

## Proposed Solution

Introduce **BATS (Bash Automated Testing System)** to test shell scripts.

### Why BATS?

1. **GitHub Actions Native**: GitHub uses BATS internally
2. **Simple Syntax**: Tests are written in bash, easy to learn
3. **Good CI Integration**: Works well with GitHub Actions
4. **Active Community**: Well-maintained and documented

### Implementation

#### 1. Add BATS to Project (`tests/bats/`)

```bash
tests/bats/
├── actions/
│   ├── review-and-merge.bats
│   ├── spec-to-code.bats
│   ├── auto-refactor.bats
│   ├── auto-document.bats
│   └── action-fixer.bats
├── lib/
│   └── helpers.bash
└── README.md
```

#### 2. Install BATS (`scripts/install-test-tools.sh`)

```bash
#!/bin/bash
# Install BATS and helper libraries

# Install BATS core
git clone --depth 1 https://github.com/bats-core/bats-core.git /tmp/bats
sudo /tmp/bats/install.sh /usr/local

# Install BATS support libraries
git clone --depth 1 https://github.com/bats-core/bats-assert.git /tmp/bats-assert
sudo /tmp/bats-assert/install.sh /usr/local

git clone --depth 1 https://github.com/bats-core/bats-file.git /tmp/bats-file
sudo /tmp/bats-file/install.sh /usr/local

echo "BATS installed successfully"
```

#### 3. Example Test (`tests/bats/actions/action-fixer.bats`)

```bash
#!/usr/bin/env bats

load 'lib/bats-assert/load'
load 'lib/bats-file/load'
load 'lib/helpers'

setup() {
  # Setup test fixtures
  TEST_DIR=$(mktemp -d)
  export TEST_DIR
}

teardown() {
  # Cleanup
  rm -rf "$TEST_DIR"
}

@test "action-fixer: detects invalid YAML syntax" {
  # Create invalid workflow
  cat > "$TEST_DIR/invalid.yml" <<EOF
name: Test
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout
  # Missing closing bracket
EOF

  # Run action-fixer script
  run bash actions/action-fixer/scripts/fix.sh "$TEST_DIR/invalid.yml"

  # Should detect error
  assert_output --partial "syntax error"
  assert_failure
}

@test "action-fixer: fixes common errors" {
  cat > "$TEST_DIR/fixable.yml" <<EOF
name: Test
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps: []
EOF

  run bash actions/action-fixer/scripts/fix.sh "$TEST_DIR/fixable.yml" --fix

  assert_success
  assert_file_exist "$TEST_DIR/fixable.yml.fixed"
}

@test "action-fixer: validates with yamllint" {
  cat > "$TEST_DIR/valid.yml" <<EOF
name: Test
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "test"
EOF

  run bash actions/action-fixer/scripts/validate.sh "$TEST_DIR/valid.yml"

  assert_success
}
```

#### 4. GitHub Actions Workflow (`.github/workflows/test-shell-scripts.yml`)

```yaml
name: Test Shell Scripts

on:
  push:
    paths:
      - 'actions/**/scripts/**'
      - 'tests/bats/**'
  pull_request:
  workflow_dispatch:

jobs:
  bats-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install BATS
        run: |
          bash scripts/install-test-tools.sh

      - name: Run BATS tests
        run: |
          bats --report-formatter junit tests/bats/

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: bats-test-results
          path: report.xml

  coverage-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install BATS and bashcov
        run: |
          bash scripts/install-test-tools.sh
          gem install bashcov

      - name: Run with coverage
        run: |
          bashcov -- bats tests/bats/

      - name: Generate Coverage Report
        run: |
          bashcov report --format HTML --output bashcov/html

      - name: Upload Coverage
        uses: actions/upload-artifact@v3
        with:
          name: bash-coverage
          path: bashcov/html
```

#### 5. Update `pytest.ini` or Create `Makefile`

```makefile
# Makefile

.PHONY: test test-all test-python test-shell lint

test: test-python test-shell

test-python:
	pytest

test-shell:
	bats tests/bats/

test-all:
	@echo "Running Python tests..."
	$(MAKE) test-python
	@echo "Running Shell tests..."
	$(MAKE) test-shell

coverage-python:
	pytest --cov=. --cov-report=html --cov-report=term

coverage-shell:
	bashcov -- bats tests/bats/
	@bashcov report

coverage-all:
	@echo "Python coverage:"
	$(MAKE) coverage-python
	@echo ""
	@echo "Shell coverage:"
	$(MAKE) coverage-shell

lint:
	ruff check .
	bats --formatter pretty tests/bats/ --dry-run
```

### Target Coverage Goals

```yaml
# .audit/config/intent.yml (update)
quality_attributes:
  - id: "QA-004"
    name: "シェルスクリプトのテストカバレッジ"
    target: ">= 70%"
    verification:
      type: "measurement"
      command: "make coverage-shell"
      criteria:
        operator: ">="
        value: 70
        unit: "%"
      interpretation:
        success_means: "アクション本体のシェルスクリプトの70%以上がテストされている"
        failure_means: "重要なロジックが未検証"
```

## Implementation Steps

1. **Install BATS Locally**
   - Run `scripts/install-test-tools.sh` locally
   - Verify with `bats --version`

2. **Create First Test**
   - Start with `action-fixer` (smallest scope)
   - Create `tests/bats/actions/action-fixer.bats`
   - Implement 2-3 basic tests

3. **Add CI Workflow**
   - Create `.github/workflows/test-shell-scripts.yml`
   - Run on every PR
   - Add test result upload

4. **Expand Coverage**
   - Add tests for each action (one per week)
   - Aim for 70% coverage minimum
   - Prioritize high-risk actions (review-and-merge, spec-to-code)

5. **Update Documentation**
   - Add BATS testing guide to `CONTRIBUTING.md`
   - Document test-writing patterns

## Verification Criteria

- [ ] BATS is installed and working (`bats --version`)
- [ ] At least 5 tests written for `action-fixer`
- [ ] CI workflow runs successfully
- [ ] Coverage report is generated
- [ ] Initial shell script coverage is > 50%
- [ ] Makefile targets work (`make test`, `make coverage`)

## Expected Benefits

1. **True Coverage**: Real 92.99% (or close) including shell scripts
2. **Bug Detection**: Catch shell script errors before production
3. **Refactoring Safety**: Can modify shell scripts with confidence
4. **Documentation**: Tests serve as usage examples
5. **Quality Gate**: Prevent regressions in action logic

## Risks

- **Medium Risk**: Learning curve for team unfamiliar with BATS
- **Mitigation**: Provide good documentation and examples
- **Time**: Initial test writing takes time
- **Rollback**: Remove BATS tests and workflow

## Alternatives Considered

1. **Convert shell scripts to Python**
   - **Rejected**: Huge effort, shell is native to GitHub Actions

2. **Use ShellCheck only (static analysis)**
   - **Rejected**: Doesn't test actual behavior, only syntax

3. **Manual testing only**
   - **Rejected**: Not scalable, error-prone

4. **Other shell test frameworks (shunit2, etc.)**
   - **Rejected**: BATS is more modern and GitHub-friendly

## Estimated Effort

- **Initial Setup**: 4 hours
- **Per Action Test Suite**: 2-3 hours each
- **Total (for 6 core actions)**: 16-22 hours
- **Ongoing Maintenance**: Minimal

## Dependencies

- BATS core
- bats-assert (for better assertions)
- bats-file (for file assertions)
- bashcov (for coverage - Ruby gem)

## Related Gaps

- Closes TG-001 (shell script testing gap)
- Validates I-003 (coverage illusion)
- Addresses U-005 (shell coverage unknown)

## Related Assumptions

- Will validate/contradict ASM-002 (80% coverage target)
- May require adjusting QA-001 if shell coverage is low
