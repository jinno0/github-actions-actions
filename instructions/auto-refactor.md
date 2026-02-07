# Auto Refactor Setup Guide

This action automatically refactors code based on natural language instructions using Claude Code CLI.

## Prerequisites

- **Runner**: A self-hosted runner with the `claude` CLI installed.
- **Permissions**: `pull-requests: write` to create a PR with the refactored code.

## Setup Instructions

1.  **Create Workflow File**:
    Create a new file at `.github/workflows/auto-refactor.yml`.

2.  **Copy Example Configuration**:
    Copy the content from the [Auto Refactor Example](../examples/auto-refactor-example.yml).

    ```yaml
    # Reference: examples/auto-refactor-example.yml
    uses: owner/repo/actions/auto-refactor@main
    with:
      path: 'src/legacy-module'
      instruction: 'Convert to modern syntax and add types'
    ```

## Usage

This action is best used with `workflow_dispatch` inputs, allowing you to specify the target path and instructions dynamically for each run. It creates a Pull Request with the changes.

## See Also

For comprehensive documentation including features, inputs, examples, and best practices, see the [Auto Refactor README](../actions/auto-refactor/README.md).
