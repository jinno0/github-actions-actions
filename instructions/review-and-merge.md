# Review and Merge Setup Guide

This action uses AI (Claude Code CLI) to review pull requests and automatically fix code issues. It can operate in two modes: **Auto-Fix** (applies corrections directly) or **Review** (posts feedback as a comment).

## Prerequisites

- **Runner**: A self-hosted runner with the `claude` CLI installed.
- **Permissions**: `contents: write` and `pull-requests: write` to checkout PRs, commit fixes, and post comments.

## Setup Instructions

1. **Create Workflow File**:
   Create a new file at `.github/workflows/review-and-merge.yml`.

2. **Copy Example Configuration**:
   Copy the content from the [Review and Merge Example](../examples/review-and-merge-example.yml).

   ```yaml
   # Reference: examples/review-and-merge-example.yml
   uses: owner/repo/actions/review-and-merge@main
   with:
     github-token: ${{ secrets.GITHUB_TOKEN }}
     claude-model: 'sonnet'
     lgtm-threshold: '7'
     auto-fix: 'true'
   ```

## Usage

This action is triggered on `pull_request` events (opened, synchronized, or reopened). When triggered:

- **Auto-Fix Mode** (`auto-fix: 'true'`): Claude analyzes the PR diff, automatically fixes issues, and commits the changes back to the PR branch.
- **Review Mode** (`auto-fix: 'false'`): Claude posts a review comment with verdict (LGTM/REQUEST_CHANGES), confidence score, and summary.

### Customization

- **Custom Review Rules**: Use the `custom-rules` input to inject project-specific guidelines.
- **Custom Templates**: Use `review-prompt-template` or `comment-template` to override default prompts.
- **LGTM Threshold**: Adjust `lgtm-threshold` (1-10) to control auto-merge sensitivity.

### Integration with Auto-Merge

Typically used in a pipeline:
1. Publish draft PRs (optional)
2. Review and fix code
3. Auto-merge if LGTM threshold is met

See the full example workflow for details.
