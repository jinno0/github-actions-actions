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

## Inputs

- `source-path` (required): Path to the source code directory to analyze.
- `doc-path` (required): Path to the documentation file to update (e.g., `README.md`).
- `commit-message` (optional): Custom commit message for documentation updates. Default: "docs: update documentation".

## Troubleshooting

### Claude CLI not found
Ensure the self-hosted runner has the `claude` CLI installed and available in the system PATH. Verify by running `which claude` on the runner.

### Permission denied errors
Check that your workflow file includes the necessary permissions:
```yaml
permissions:
  contents: write
```

### Documentation not updating
- Verify the `source-path` and `doc-path` inputs are correct relative to your repository root.
- Check the action logs for any Claude CLI errors or parsing issues.
- Ensure the source code changes are triggering the workflow (check the `paths` filter in your workflow trigger).

### Large files or timeouts
If your documentation file is very large or the analysis is taking too long, consider:
1. Narrowing the `source-path` to specific subdirectories.
2. Using a more focused prompt template via the `prompt-template` input.