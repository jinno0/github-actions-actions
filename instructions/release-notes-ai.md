# AI Release Notes Setup Guide

This action generates comprehensive, human-readable release notes from commit history and merged PRs.

## Prerequisites

- **Runner**: A self-hosted runner with the `claude` CLI and `gh` CLI installed.
- **Permissions**: `contents: write` to update Releases.

## Setup Instructions

1.  **Create Workflow File**:
    Create a new file at `.github/workflows/release-notes.yml`.

2.  **Copy Example Configuration**:
    Copy the content from the [Release Notes Example](../examples/release-notes-ai-example.yml).

    ```yaml
    # Reference: examples/release-notes-ai-example.yml
    uses: owner/repo/actions/release-notes-ai@main
    with:
      base-ref: 'v1.0.0'
      head-ref: 'v1.1.0'
      output-file: 'RELEASE_NOTES.md'
    ```

## Usage

Typically triggered by a tag push (`v*`). The workflow calculates the previous tag automatically (as shown in the example) and generates notes for the diff.
