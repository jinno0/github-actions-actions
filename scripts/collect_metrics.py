#!/usr/bin/env python3
"""
Collect and send anonymous usage metrics for GitHub Actions.

This script collects anonymous telemetry data about Action executions to help
measure adoption and identify issues. All data is anonymized and opt-out.

Privacy Features:
- Repository names are hashed (SHA-256, first 16 chars)
- Opt-out mechanism via DISABLE_TELEMETRY environment variable
- Only essential metrics collected
- No code or sensitive data transmitted

Usage:
    python scripts/collect_metrics.py <action_name> <status> <duration_ms> [error_type]

Environment Variables:
    DISABLE_TELEMETRY: Set to "true" to disable metrics collection
    GITHUB_REPOSITORY: Automatically set in GitHub Actions (hashed for privacy)
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path


def is_telemetry_disabled() -> bool:
    """Check if telemetry is disabled via environment variable."""
    return os.getenv("DISABLE_TELEMETRY", "").lower() == "true"


def anonymize_repository(repo: str) -> str:
    """
    Anonymize repository name using SHA-256 hash.

    Args:
        repo: Repository name (e.g., "owner/repo")

    Returns:
        First 16 characters of SHA-256 hash
    """
    if repo == "unknown":
        return repo

    hash_obj = hashlib.sha256(repo.encode('utf-8'))
    return hash_obj.hexdigest()[:16]


def collect_metrics(
    action_name: str,
    status: str,
    duration_ms: int,
    error_type: str = None
) -> dict:
    """
    Collect metrics for Action execution.

    Args:
        action_name: Name of the Action (e.g., "review-and-merge")
        status: Execution status ("success", "failure", "error")
        duration_ms: Execution duration in milliseconds
        error_type: Optional error type or message

    Returns:
        Dictionary containing collected metrics
    """
    # Check opt-out
    if is_telemetry_disabled():
        return {"status": "skipped", "reason": "telemetry_disabled"}

    # Get repository context (anonymous)
    repo = os.getenv("GITHUB_REPOSITORY", "unknown")
    repo_id = anonymize_repository(repo)

    # Get runner OS
    runner_os = os.getenv("RUNNER_OS", "unknown")

    # Get Claude CLI version (if available)
    claude_version = os.getenv("CLAUDE_CLI_VERSION", "unknown")

    metrics = {
        "action_name": action_name,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": status,
        "duration_ms": duration_ms,
        "repository_anonymous_id": repo_id,
        "runner_os": runner_os,
        "claude_cli_version": claude_version,
    }

    if error_type:
        metrics["error_type"] = error_type[:200]  # Limit error message length

    return metrics


def send_metrics(metrics: dict) -> bool:
    """
    Send metrics to collection endpoint.

    Currently, this is a placeholder implementation. In production, you would:
    1. Send to a metrics collection service (e.g., Google Analytics, self-hosted)
    2. Queue for batch sending to reduce overhead
    3. Handle network errors gracefully

    For now, metrics are logged to a file for manual inspection.

    Args:
        metrics: Dictionary containing metrics to send

    Returns:
        True if sending succeeded, False otherwise
    """
    if metrics.get("status") == "skipped":
        return True

    try:
        # Create metrics directory if it doesn't exist
        metrics_dir = Path("metrics/telemetry")
        metrics_dir.mkdir(parents=True, exist_ok=True)

        # Write metrics to log file (append mode)
        log_file = metrics_dir / "telemetry.log"
        with open(log_file, "a") as f:
            f.write(json.dumps(metrics) + "\n")

        return True

    except Exception as e:
        # Silently fail to avoid breaking Actions
        print(f"Warning: Failed to send metrics: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 4:
        print(
            f"Usage: {sys.argv[0]} <action_name> <status> <duration_ms> [error_type]",
            file=sys.stderr
        )
        sys.exit(1)

    action_name = sys.argv[1]
    status = sys.argv[2]

    try:
        duration_ms = int(sys.argv[3])
    except ValueError:
        print(f"Error: duration_ms must be an integer, got '{sys.argv[3]}'", file=sys.stderr)
        sys.exit(1)

    error_type = sys.argv[4] if len(sys.argv) > 4 else None

    # Validate status
    valid_statuses = ["success", "failure", "error"]
    if status not in valid_statuses:
        print(f"Warning: Invalid status '{status}', must be one of {valid_statuses}", file=sys.stderr)
        status = "error"

    # Collect and send metrics
    metrics = collect_metrics(action_name, status, duration_ms, error_type)

    if metrics.get("status") != "skipped":
        send_metrics(metrics)

    # Always exit successfully to avoid breaking Actions
    sys.exit(0)


if __name__ == "__main__":
    main()
