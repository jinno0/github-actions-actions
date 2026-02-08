# PR-002: Automated Acceptance Rate Tracking and Dashboard

**Priority:** High
**Status:** Proposed
**Gap ID:** OG-001, SC-003
**Assumption Dependency:** ASM-003 (organization deployment), U-004 (unknown acceptance rate)

## Problem Statement

The repository has `scripts/calculate_acceptance_rate.py` but:
- It's not automated (requires manual execution)
- There's no scheduled workflow to run it periodically
- Acceptance rate trends are not tracked over time
- Success criterion "AIの提案に対する修正率が向上し続ける" cannot be measured

Current state shows 92.99% test coverage but no visibility into:
- Whether AI suggestions are actually being accepted
- If acceptance rate is improving over time
- Which actions have the highest/lowest acceptance rates

## Proposed Solution

Create a GitHub Actions workflow that:
1. Automatically runs acceptance rate calculation weekly
2. Stores historical data in a structured format
3. Creates a visualization/dashboard
4. Optionally commits trends back to the repository

### Implementation Components

#### 1. Weekly Workflow (`.github/workflows/track-acceptance-rate.yml`)

```yaml
name: Track Acceptance Rate

on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight
  workflow_dispatch:  # Allow manual trigger

permissions:
  contents: write
  pull-requests: read

jobs:
  track-acceptance:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install matplotlib pandas

      - name: Calculate Acceptance Rate
        id: calculate
        run: |
          python scripts/calculate_acceptance_rate.py \
            --org ${{ github.repository_owner }} \
            --output .audit/metrics/acceptance_rate.json \
            --plot .audit/metrics/acceptance_rate_trend.png

      - name: Update Historical Data
        run: |
          mkdir -p .audit/metrics
          timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
          echo "{\"timestamp\": \"$timestamp\", \"data\": $(cat .audit/metrics/acceptance_rate.json)}" >> \
            .audit/metrics/acceptance_rate_history.ndjson

      - name: Commit Metrics
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add .audit/metrics/
          git diff --quiet && git diff --staged --quiet || git commit -m "chore: update acceptance rate metrics [skip-ci]"
          git push
```

#### 2. Enhanced Script (`scripts/calculate_acceptance_rate_with_history.py`)

```python
#!/usr/bin/env python3
"""
Calculate and track AI suggestion acceptance rates over time.
Generates historical data and trend visualizations.
"""
import json
from pathlib import Path
from datetime import datetime
import argparse

def calculate_acceptance_rate(org: str, repo: str = None) -> dict:
    """Calculate current acceptance rate"""
    # Use existing calculate_acceptance_rate.py logic
    # Return structured data
    return {
        "overall_rate": 0.75,
        "by_action": {
            "review-and-merge": 0.82,
            "spec-to-code": 0.68,
            "auto-refactor": 0.71,
            # ...
        },
        "total_suggestions": 150,
        "accepted": 113,
        "rejected": 37
    }

def update_history(metrics: dict, history_file: Path):
    """Append new metrics to history"""
    history_file.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": metrics
    }

    with open(history_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def generate_trend_plot(history_file: Path, output_plot: Path):
    """Generate trend visualization"""
    import matplotlib.pyplot as plt
    import pandas as pd

    # Load history
    data = [json.loads(line) for line in history_file.read_text().splitlines()]
    df = pd.DataFrame([
        {
            "timestamp": d["timestamp"],
            "overall_rate": d["metrics"]["overall_rate"]
        }
        for d in data
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # Create plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['overall_rate'], marker='o', linewidth=2)
    plt.title('AI Suggestion Acceptance Rate Trend')
    plt.xlabel('Date')
    plt.ylabel('Acceptance Rate')
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_plot, dpi=300)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--org', required=True, help='GitHub organization')
    parser.add_argument('--output', required=True, help='Output JSON file')
    parser.add_argument('--plot', help='Output trend plot PNG')
    parser.add_argument('--history', default='.audit/metrics/acceptance_rate_history.ndjson')
    args = parser.parse_args()

    # Calculate current metrics
    metrics = calculate_acceptance_rate(args.org)

    # Save current metrics
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(metrics, indent=2))

    # Update history
    history_file = Path(args.history)
    update_history(metrics, history_file)

    # Generate plot if requested
    if args.plot:
        generate_trend_plot(history_file, Path(args.plot))

    print(f"Acceptance Rate: {metrics['overall_rate']:.2%}")
    print(f"History updated: {history_file}")

if __name__ == '__main__':
    main()
```

#### 3. Dashboard README (`.audit/metrics/README.md`)

```markdown
# Acceptance Rate Metrics

This directory contains automated tracking of AI suggestion acceptance rates.

## Files

- `acceptance_rate_history.ndjson` - Historical data (one JSON per line)
- `acceptance_rate_trend.png` - Visual trend plot
- `latest_acceptance_rate.json` - Most recent calculation

## Understanding Acceptance Rate

**Acceptance Rate** = (Accepted Suggestions) / (Total Suggestions)

A high acceptance rate indicates:
- AI suggestions are high quality
- Suggestions align with developer intent
- Actions are well-configured

## Trend Analysis

Check `acceptance_rate_trend.png` for visual trends:
- **Upward trend**: Improving AI suggestions
- **Stable**: Consistent quality
- **Downward trend**: May need prompt refinement

## Action-Level Breakdown

See `latest_acceptance_rate.json` for breakdown by action type:
- Identify which actions need prompt improvement
- Compare acceptance across different use cases
```

## Implementation Steps

1. Create `.github/workflows/track-acceptance-rate.yml`
2. Enhance `scripts/calculate_acceptance_rate.py` to support history tracking
3. Add `.audit/metrics/` to `.gitignore` (or commit if preferred)
4. Create `.audit/metrics/README.md`
5. Test workflow manually
6. Enable weekly schedule

## Verification Criteria

- [ ] Workflow runs successfully on `workflow_dispatch`
- [ ] Historical data is appended to `.audit/metrics/acceptance_rate_history.ndjson`
- [ ] Trend plot is generated
- [ ] Data is committed back to repository
- [ ] Weekly schedule is enabled
- [ ] `.audit/metrics/README.md` explains the metrics

## Expected Benefits

1. **Measurable Success**: Can track "AIの提案に対する修正率が向上し続ける" criterion
2. **Data-Driven Improvement**: Identify which actions need prompt refinement
3. **Transparency**: Organization can see AI quality trends
4. **Early Warning**: Detect quality degradation early

## Risks

- **Medium Risk**: Requires GitHub API access and permissions
- **Mitigation**: Use GitHub App token with minimal required scopes
- **Rollback**: Disable workflow and delete metrics directory

## Alternatives Considered

1. **External Dashboard (Grafana, etc.)**
   - **Rejected**: Overkill for single metric, adds infrastructure complexity

2. **Manual Execution Only**
   - **Rejected**: Forgetfulness leads to gaps in data

3. **Store in Database**
   - **Rejected**: JSON files are sufficient for this use case

## Dependencies

- `calculate_acceptance_rate.py` must work correctly
- GitHub API token with `pull-requests: read` permission
- Organization access via `gh` CLI or GitHub API

## Estimated Effort

- **Time**: 2-3 hours
- **Complexity**: Medium
- **Files Changed**: 3 (create workflow, enhance script, add README)

## Related Gaps

- Closes OG-001 (Acceptance Rate追跡)
- Addresses SC-003 (Acceptance Rate向上の測定)
- Validates U-004 (Acceptance Rateが未知)

## Related Unknowns

- Will reveal U-004 (current acceptance rate)
- Will provide data to validate ASM-003 (organization deployment success)
