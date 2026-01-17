# Action Fixer Setup Guide

This action validates GitHub Actions workflow files and uses AI to suggest or apply fixes for errors.

## Prerequisites

- **Runner**: A self-hosted runner with the `claude` CLI installed.
- **Permissions**: `contents: write` to commit fixes.

## Setup Instructions

1.  **Create Workflow File**:
    Create a new file at `.github/workflows/fix-actions.yml`.

2.  **Copy Example Configuration**:
    Copy the content from the [Action Fixer Example](../examples/action-fixer-example.yml).

    ```yaml
    # Reference: examples/action-fixer-example.yml
    uses: owner/repo/actions/action-fixer@main
    with:
      workflow-path: '.github/workflows'
    ```

## Usage

This action is typically triggered manually (`workflow_dispatch`) when you encounter a workflow error, or it can be scheduled to run periodically to check for deprecated syntax.
