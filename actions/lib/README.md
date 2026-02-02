# Actions Library

Shared libraries and utilities for GitHub Actions.

## Acceptance Tracking

### Overview

The `acceptance_tracker.py` module provides acceptance rate tracking for AI-generated suggestions across all GitHub Actions.

### Usage

```python
from actions.lib.acceptance_tracker import AcceptanceTracker

# Initialize tracker for an action
tracker = AcceptanceTracker("action-name")

# Record suggestion outcomes
tracker.record_suggestion("made")
tracker.record_suggestion("accepted")  # or "rejected" or "modified"

# Get acceptance rate
rate = tracker.get_acceptance_rate()

# Export and persist metrics
metrics = tracker.export_metrics()
tracker.save_to_file("metrics/action-metrics.json")
```

### Integration Guide

To integrate acceptance tracking into a GitHub Action:

#### Step 1: Import the Tracker

Add to your action script:
```python
import sys
sys.path.insert(0, 'actions/lib')
from acceptance_tracker import AcceptanceTracker
```

#### Step 2: Initialize Tracker

```python
tracker = AcceptanceTracker(os.getenv("GITHUB_ACTION", "unknown-action"))
```

#### Step 3: Record Outcomes

```python
# When AI generates a suggestion
tracker.record_suggestion("made")

# After user decision (detected via PR comments, reactions, etc.)
# - Accepted without changes
tracker.record_suggestion("approved")

# - Rejected
tracker.record_suggestion("rejected")

# - Accepted with modifications
tracker.record_suggestion("modified")
```

#### Step 4: Persist Metrics

```python
# Save to centralized metrics location
metrics_dir = os.environ.get("GITHUB_WORKSPACE", ".")
metrics_file = os.path.join(metrics_dir, "metrics", f"{action_name}-metrics.json")
os.makedirs(os.path.dirname(metrics_file), exist_ok=True)
tracker.save_to_file(metrics_file)
```

### Integration Examples

#### Example 1: review-and-merge Action

```yaml
- name: Track review suggestions
  if: always()
  env:
    OUTCOME: ${{ steps.ai-review.outputs.outcome }}
  run: |
    python - <<'EOF'
    import os, json
    import sys
    sys.path.insert(0, 'actions/lib')
    from acceptance_tracker import AcceptanceTracker

    tracker = AcceptanceTracker("review-and-merge")
    tracker.record_suggestion("made")

    if os.getenv("OUTCOME") == "approved":
        tracker.record_suggestion("accepted")
    elif os.getenv("OUTCOME") == "rejected":
        tracker.record_suggestion("rejected")
    else:
        tracker.record_suggestion("modified")

    tracker.save_to_file("metrics/review-and-merge-metrics.json")
    EOF
```

#### Example 2: spec-to-code Action

```python
# In spec-to-code implementation
from actions.lib.acceptance_tracker import AcceptanceTracker

def track_code_generation(tracker, pr_merged, commit_count):
    """Track code generation acceptance"""
    tracker.record_suggestion("made")

    if pr_merged and commit_count == 1:
        # Code accepted without modification
        tracker.record_suggestion("accepted")
    elif pr_merged and commit_count > 1:
        # Code accepted with modifications
        tracker.record_suggestion("modified")
    else:
        # Code rejected (PR not merged)
        tracker.record_suggestion("rejected")

    return tracker.export_metrics()
```

#### Example 3: action-fixer Action

```python
# In action-fixer implementation
from actions.lib.acceptance_tracker import AcceptanceTracker

def track_fix_suggestion(tracker, fix_applied, modified_before_apply):
    """Track fix suggestion acceptance"""
    tracker.record_suggestion("made")

    if fix_applied and not modified_before_apply:
        tracker.record_suggestion("accepted")
    elif fix_applied and modified_before_apply:
        tracker.record_suggestion("modified")
    else:
        tracker.record_suggestion("rejected")

    return tracker.get_acceptance_rate()
```

#### Example 4: auto-refactor Action

```python
# In auto-refactor implementation
from actions.lib.acceptance_tracker import AcceptanceTracker

def track_refactor_suggestion(tracker, refactor_accepted):
    """Track refactor suggestion acceptance"""
    tracker.record_suggestion("made")

    if refactor_accepted:
        # Check if PR was merged with modifications
        # This can be detected by comparing commit counts
        tracker.record_suggestion("accepted")  # or "modified"
    else:
        tracker.record_suggestion("rejected")

    return tracker.export_metrics()
```

### Detecting Outcomes

To determine if a suggestion was accepted, rejected, or modified:

#### For Pull Request-Based Actions

```python
def detect_pr_outcome(github_token, pr_number):
    """Detect PR outcome using GitHub API"""
    from github import Github

    g = Github(github_token)
    repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))
    pr = repo.get_pull(pr_number)

    if pr.merged:
        # Check if there were commits after the suggestion
        # If only 1 commit, it was accepted as-is
        # If >1 commits, it was modified
        commits = list(pr.get_commits())
        return "modified" if len(commits) > 1 else "accepted"
    elif pr.closed:
        return "rejected"
    else:
        return "pending"
```

#### For Comment-Based Actions

```python
def detect_comment_outcome(comment_body):
    """Detect outcome from comment reactions or keywords"""
    body_lower = comment_body.lower()

    if "+1" in body_lower or "approved" in body_lower or "accept" in body_lower:
        return "accepted"
    elif "-1" in body_lower or "rejected" in body_lower or "decline" in body_lower:
        return "rejected"
    elif "modified" in body_lower or "adjusted" in body_lower:
        return "modified"
    else:
        return "unknown"
```

### Testing Your Integration

```python
# Test acceptance tracking
import tempfile
import os

def test_tracking():
    tracker = AcceptanceTracker("test-action")

    # Simulate workflow
    tracker.record_suggestion("made")
    tracker.record_suggestion("accepted")

    # Verify
    assert tracker.get_acceptance_rate() == 100.0

    # Test persistence
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name

    try:
        tracker.save_to_file(temp_file)

        # Load and verify
        tracker2 = AcceptanceTracker.from_file("test-action", temp_file)
        assert tracker2.metrics["suggestions_accepted"] == 1
    finally:
        os.unlink(temp_file)
```

### Best Practices

1. **Always record "made" before recording the outcome**
2. **Use consistent action names** (match the GitHub Action name)
3. **Persist metrics after each workflow run**
4. **Handle errors gracefully** (tracking failures shouldn't break the action)
5. **Test integration locally** before deploying
6. **Review metrics regularly** to identify quality issues

### Troubleshooting

#### Metrics Not Appearing

- Verify metrics directory exists
- Check file permissions
- Ensure tracker.save_to_file() is called
- Review workflow logs for errors

#### Incorrect Acceptance Rates

- Verify outcome detection logic
- Check that "made" is recorded before outcome
- Review metrics JSON file for data integrity
- Test with known scenarios

#### Performance Issues

- Use asynchronous tracking where possible
- Batch metric writes instead of writing continuously
- Consider using GitHub Actions artifacts for large metrics files

## Additional Utilities

Future utilities will be added to this directory as the need arises.

## Contributing

When adding new utilities:

1. Create appropriate subdirectories for organization
2. Include comprehensive tests
3. Add documentation to this README
4. Follow existing code patterns
5. Update relevant action integrations
