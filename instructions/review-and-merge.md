# Review and Auto-Merge Setup Guide

This action uses Claude Code CLI to review Pull Requests and automatically merge them if they meet the quality threshold.

## Prerequisites

- **Runner**: A self-hosted runner with the `claude` CLI installed and configured.
- **Permissions**: The workflow requires `contents: write`, `pull-requests: write`, and `checks: write`.

## Setup Instructions

1.  **Create Workflow File**:
    Create a new file at `.github/workflows/review-and-merge.yml`.

2.  **Copy Example Configuration**:
    Copy the content from the [Review and Merge Example](../examples/review-and-merge-example.yml).

    ```yaml
    # Reference: examples/review-and-merge-example.yml
    uses: owner/repo/actions/review-and-merge@main
    with:
      github-token: ${{ secrets.GITHUB_TOKEN }}
      lgtm-threshold: '7'  # Adjust sensitivity (1-10)
      # auto-fix: 'true'   # Uncomment to enable auto-correction and merge
    ```

3.  **Customize Rules (Optional)**:
    You can provide specific review guidelines using the `custom-rules` input:
    ```yaml
    custom-rules: |
      - Check for security vulnerabilities.
      - Ensure variable naming follows camelCase.
    ```

## Auto-Fix Mode (Enabled by default)

By default (`auto-fix: 'true'`), the action will:
1.  Analyze the code changes.
2.  **Automatically apply fixes** to the files if issues are found (using AI).
3.  Commit and push the fixes to the branch.
4.  Merge the PR automatically.

If you want to only receive review comments without automatic code changes, set `auto-fix: 'false'`.

**Note**: In auto-fix mode, detailed review comments are skipped in favor of direct code correction.

## Automatic Rebase and Conflict Resolution

Before merging, the action will automatically:

1. **Check if the PR branch is behind** the base branch (`main`, `develop`, etc.)
2. **Rebase the branch** if it's behind, using `git rebase origin/<base-branch>`
3. **Attempt automatic conflict resolution** if rebase fails:
   - Detects conflicted files using `git status --short | grep "^UU"`
   - Resolves conflicts by preferring the base branch version (`git checkout --theirs`)
   - Continues the rebase after resolution
   - Force pushes with `--force-with-lease` for safety

4. **Push all changes at once** (auto-fix commits and/or rebased commits)

If conflicts cannot be resolved automatically, the action will:
- Abort the rebase cleanly
- Post an error: `Could not automatically resolve merge conflicts. Manual intervention required.`
- Exit with error status, preventing the merge

In review mode (`auto-fix: 'false'`), the action will also report whether:
- The branch was **automatically rebased** before merge
- **Conflicts were resolved** automatically

This ensures that PRs are always up-to-date with the base branch before merging, reducing merge conflicts.

## Usage

The action triggers automatically on Pull Request events (opened, synchronize, reopened) targeting the configured branches (default: `main`, `develop`).
