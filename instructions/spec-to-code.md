# Spec to Code Setup Guide

This action generates source code from Markdown specification files using Claude Code CLI.

## Prerequisites

- **Runner**: A self-hosted runner with the `claude` CLI installed.
- **Specs**: A directory (e.g., `specs/`) containing Markdown files that describe the desired code.

## Setup Instructions

1.  **Create Workflow File**:
    Create a new file at `.github/workflows/generate-code.yml`.

2.  **Copy Example Configuration**:
    Copy the content from the [Spec to Code Example](../examples/spec-to-code-example.yml).

    ```yaml
    # Reference: examples/spec-to-code-example.yml
    uses: owner/repo/actions/spec-to-code@main
    with:
      spec-path: 'specs/my-feature.md'
      output-dir: 'src'
      language: 'TypeScript'
    ```

3.  **Configure Trigger**:
    The example is configured to run on `push` to the `specs/` directory or manually via `workflow_dispatch`.

## Usage

1.  Create a Markdown file in `specs/` describing the feature.
2.  Push the file or manually trigger the workflow.
3.  The Action will generate the code and commit it back to the repository.
