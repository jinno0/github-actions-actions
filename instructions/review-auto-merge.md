# AI Review and Auto-Merge Workflow

This workflow provides automated Pull Request review and merging using Claude Code CLI.

## Prerequisites

- **Self-hosted runner**: Required with `claude` CLI installed and configured
- **Permissions**:
  - `contents: write` - For committing auto-fixes and merging
  - `pull-requests: write` - For posting review comments
  - `checks: read` - For verifying CI status

## Setup Instructions

1. **Ensure self-hosted runner is available**
   - The workflow uses `runs-on: self-hosted` for the AI review job
   - Claude Code CLI must be installed on the runner

2. **Create or update the workflow file**
   - Location: `.github/workflows/review-auto-merge.yml`
   - The workflow is already created in this repository

3. **Customize settings (optional)**

   Adjust the LGTM threshold:
   ```yaml
   lgtm-threshold: '7'  # 1-10 scale (default: 7)
   ```

   Choose Claude model:
   ```yaml
   claude-model: sonnet  # or 'opus', 'haiku'
   ```

   Toggle auto-fix mode:
   ```yaml
   auto-fix: 'true'  # Auto-fix and commit issues (default: true)
   auto-fix: 'false' # Review-only mode with comments
   ```

## How It Works

### 1. AI Review Job (`ai-review`)
- Runs on **self-hosted** runner
- Uses `actions/review-and-merge` composite action
- Performs:
  - Fetches PR diff
  - Runs Claude Code CLI for analysis
  - **Auto-fix mode**: Directly edits files and commits fixes
  - **Review mode**: Posts JSON verdict with comments

Outputs:
- `verdict`: "LGTM" or "REQUEST_CHANGES"
- `confidence`: 1-10 score
- `made-changes`: true/false

### 2. Wait for CI Job (`wait-for-ci`)
- Waits up to **30 minutes** for CI checks to complete
- Checks every 30 seconds
- Outputs whether CI passed or failed

### 3. Auto-Merge Job (`auto-merge`)
- Only runs if:
  - AI review verdict is "LGTM"
  - CI checks passed
  - No changes were made (auto-fix already pushed)

- **Merge retry logic**:
  - Up to 10 attempts
  - Tries all methods: squash → merge → rebase
  - 5 second delay between attempts

- **Failure handling**:
  - Creates GitHub comment with failure details
  - Exits with error if all attempts fail

## Usage

The workflow triggers automatically on:
- PR opened
- PR synchronized (new commit pushed)
- PR reopened
- PR marked as ready for review

## Example Scenarios

### Scenario 1: Perfect PR
1. PR opened → AI reviews → LGTM
2. CI passes
3. PR auto-merged using squash

### Scenario 2: Issues Found (Auto-Fix)
1. PR opened → AI finds issues
2. AI fixes and commits to branch
3. CI runs on new commit
4. Workflow re-triggers
5. AI reviews → LGTM
6. PR auto-merged

### Scenario 3: Issues Found (Review Mode)
1. PR opened → AI reviews → REQUEST_CHANGES
2. Review comment posted with issues
3. Author fixes and pushes
4. Workflow re-triggers
5. Repeat until LGTM

### Scenario 4: CI Failure
1. PR opened → AI reviews → LGTM
2. CI fails
3. Merge is blocked
4. Author must fix CI

## Troubleshooting

### Workflow not running
- Check if self-hosted runner is online: `gh auth status` and runner settings
- Verify workflow file is in `.github/workflows/`

### AI review fails
- Check runner logs for Claude CLI errors
- Verify `claude` CLI is installed: `which claude`
- Test manually: `claude --help`

### Merge fails despite LGTM
- Check branch protection rules
- Verify PR is mergeable (no conflicts)
- Check GitHub token permissions

### CI timeout
- Default is 30 minutes, can be adjusted in `wait-for-ci` job
- Increase `TIMEOUT` value if needed

## Custom Rules

You can add custom review guidelines:

```yaml
- name: AI Review and Fix
  uses: ./actions/review-and-merge
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    custom-rules: |
      - No console.log statements in production code
      - All functions must have JSDoc comments
      - Use TypeScript strict mode
```

## Related Files

- **Action implementation**: `actions/review-and-merge/action.yml`
- **Templates**: `actions/review-and-merge/templates/`
- **Example usage**: `examples/review-and-merge-example.yml`
