# Claude CLI Version Testing Guide

This document provides guidelines for testing Claude Code CLI version compatibility with AI Actions.

## Testing Checklist for New CLI Versions

Before updating the minimum CLI version in documentation or CI:

### 1. Pre-Testing Preparation
- [ ] Create a feature branch for testing
- [ ] Note the new CLI version to test
- [ ] Identify any breaking changes in CLI changelog

### 2. Test Execution
- [ ] Run full test suite: `pytest --cov=. --cov-report=term-missing`
- [ ] Execute dry-run workflow: `.github/workflows/test-with-dry-run.yml`
- [ ] Test each action manually with representative example:
  - [ ] review-and-merge
  - [ ] spec-to-code
  - [ ] action-fixer
  - [ ] auto-refactor
  - [ ] auto-document
  - [ ] release-notes-ai
  - [ ] auto-merge
  - [ ] auto-rebase
  - [ ] review-auto-merge
  - [ ] publish-pr
  - [ ] bulk-merge-prs
  - [ ] bulk-rebase-prs
  - [ ] pr-review-enqueuer
- [ ] Verify no breaking changes in CLI API
- [ ] Check for deprecation warnings

### 3. Validation Criteria
- [ ] All tests pass (455 tests, 0 failures)
- [ ] Coverage remains >= 92%
- [ ] All actions pass dry-run validation
- [ ] No new errors or warnings in action execution
- [ ] Performance is comparable to previous version

### 4. Documentation Update
- [ ] Update README.md with new minimum version
- [ ] Update version pinning in CI workflows
- [ ] Update this document with test results
- [ ] Add entry to CHANGELOG (if exists)

## Version Upgrade Process

### Step 1: Development Testing
```bash
# Install new CLI version in development environment
npm install -g @anthropic-ai/claude-code@<new-version>

# Run test suite
pytest --cov=. --cov-report=term-missing

# Execute dry-run workflow
gh workflow run test-with-dry-run.yml
```

### Step 2: Documentation Updates
- Update version in README.md "Claude Code CLI バージョン" section
- Update pinned versions in `.github/workflows/test-with-dry-run.yml`
- Update version pinning examples in representative example workflows

### Step 3: Validation
- Monitor CI results for all workflows
- Check for any user-reported issues
- Verify telemetry shows no increase in errors

### Step 4: Rollout
- Merge documentation changes
- Monitor for issues for 1 week
- Update minimum version requirement if stability confirmed

## Current CLI Version Status

**Last Tested**: 2026-02-08
**Tested Version**: Latest Stable (unspecified)
**Status**: ✅ All actions passing

**Known Issues**: None

## Rollback Plan

If new CLI version causes issues:
```bash
# Revert documentation changes
git revert <commit-hash>

# Pin to previous known-good version in CI
npm install -g @anthropic-ai/claude-code@<previous-version>

# Report issue to Claude Code CLI repository
# Include: CLI version, error messages, reproduction steps
```

## Reporting Issues

When reporting CLI compatibility issues, include:
1. Claude CLI version: `claude --version`
2. Action name and version
3. Error message or unexpected behavior
4. Minimal reproduction case
5. Whether issue occurs in dry-run mode

## Version History

| Date | CLI Version | Status | Notes |
|------|-------------|--------|-------|
| 2026-02-08 | Latest Stable | ✅ Tested | Baseline established, version requirements documented |

---

**Last Updated**: 2026-02-08
**Maintained By**: Repository Maintainers
