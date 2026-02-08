"""
Centralized environment variable configuration.

This module provides a single source of truth for accessing environment variables,
ensuring the "one information = one variable = one variable name" principle.

All environment variable access should go through these functions to maintain
consistency across the codebase.
"""

import os


def is_telemetry_disabled() -> bool:
    """
    Check if telemetry is disabled via environment variable.

    Returns:
        True if DISABLE_TELEMETRY is set to "true" (case insensitive), False otherwise
    """
    return os.getenv("DISABLE_TELEMETRY", "").lower() == "true"


def get_github_repository() -> str:
    """
    Get the GitHub repository name from environment.

    Returns:
        Repository name in format "owner/repo", or "unknown" if not set
    """
    return os.getenv("GITHUB_REPOSITORY", "unknown")


def get_repository_from_components() -> str | None:
    """
    Build repository name from REPO_OWNER and REPO_NAME environment variables.

    This is an alternative method to get the repository identifier when
    GITHUB_REPOSITORY is not available.

    Returns:
        Repository name in format "owner/repo", or None if components are missing
    """
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")

    if repo_owner and repo_name:
        return f"{repo_owner}/{repo_name}"
    return None


def get_repository_identifier() -> str:
    """
    Get repository identifier from available environment variables.

    Tries GITHUB_REPOSITORY first, then falls back to REPO_OWNER/REPO_NAME combination.

    Returns:
        Repository name in format "owner/repo", or "unknown" if not available
    """
    # Try GITHUB_REPOSITORY first
    repo = get_github_repository()
    if repo != "unknown":
        return repo

    # Fall back to REPO_OWNER and REPO_NAME
    repo_from_components = get_repository_from_components()
    if repo_from_components:
        return repo_from_components

    return "unknown"


def get_runner_os() -> str:
    """
    Get the GitHub Actions runner operating system.

    Returns:
        Runner OS (e.g., "Linux", "Windows", "macOS"), or "unknown" if not set
    """
    return os.getenv("RUNNER_OS", "unknown")


def get_claude_cli_version() -> str:
    """
    Get the Claude CLI version from environment.

    Returns:
        Version string, or "unknown" if not set
    """
    return os.getenv("CLAUDE_CLI_VERSION", "unknown")
