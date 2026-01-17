# Auto Document Setup Guide

This action keeps your documentation (like README.md) in sync with your source code by analyzing changes and updating the docs automatically.

## Prerequisites

- **Runner**: A self-hosted runner with the `claude` CLI installed.
- **Permissions**: `contents: write` to commit the documentation updates.

## Setup Instructions

1.  **Create Workflow File**:
    Create a new file at `.github/workflows/auto-doc.yml`.

2.  **Copy Example Configuration**:
    Copy the content from the [Auto Document Example](../examples/auto-document-example.yml).

    ```yaml
    # Reference: examples/auto-document-example.yml
    uses: owner/repo/actions/auto-document@main
    with:
      source-path: 'src'
      doc-path: 'README.md'
    ```

## Usage

Configure the workflow to run on `push` to main branches, restricted to specific paths (e.g., `src/**`) to trigger updates whenever the code changes.
