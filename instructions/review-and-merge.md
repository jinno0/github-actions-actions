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
    ```

3.  **Customize Rules (Optional)**:
    You can provide specific review guidelines using the `custom-rules` input:
    ```yaml
    custom-rules: |
      - Check for security vulnerabilities.
      - Ensure variable naming follows camelCase.
    ```

## Usage

The action triggers automatically on Pull Request events (opened, synchronize, reopened) targeting the configured branches (default: `main`, `develop`).
