# PR-003: Implement Organizational Adoption Tracking

**Priority**: 3 (Medium - Phase 3 completion)
**Status**: Proposed
**Estimated Effort**: Medium (4-6 hours)

## Problem

PURPOSE.md Phase 3 states:
> 組織内プロジェクトへの導入とフィードバック収集

Current status: **Unknown** which repositories are using these actions.

Without adoption tracking:
- Cannot measure success condition: "組織内の複数のリポジトリで採用される"
- Cannot prioritize action improvements based on actual usage
- Cannot demonstrate value to organization
- Cannot collect systematic feedback

## Proposed Solution

### Approach A: Telemetry-Based Tracking (Recommended)

Enhance existing telemetry system to track adoption.

#### Implementation

**File: `scripts/track_adoption.py`**

```python
#!/usr/bin/env python3
"""
Track organizational adoption of AI Hub Actions

Uses telemetry data to identify which repositories are using which actions.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def analyze_telemetry_data(telemetry_dir: Path) -> dict:
    """Analyze telemetry to extract adoption metrics"""
    # Parse telemetry logs
    # Extract unique repository hashes
    # Count action usage per repository
    # Generate adoption report
    pass

def generate_adoption_report(output_path: Path):
    """Generate adoption tracking report"""
    metrics = analyze_telemetry_data(Path("metrics/telemetry/"))

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_repositories": metrics["unique_repo_count"],
        "active_repositories_30d": metrics["active_30d"],
        "action_usage": {
            "review-and-merge": metrics["actions"]["review_and_merge"]["repos"],
            "spec-to-code": metrics["actions"]["spec_to_code"]["repos"],
            # ... all 13 actions
        },
        "most_used_actions": metrics["top_actions"],
        "recent_adoptions": metrics["new_repos_30d"]
    }

    output_path.write_text(json.dumps(report, indent=2))
```

**Update: `docs/telemetry.md`**

Add section on adoption tracking:

```markdown
## Adoption Tracking

Telemetry data is used to track organizational adoption:

- Repository counts (anonymized)
- Action usage patterns
- Active repositories over time

This helps us understand which actions provide the most value.
```

### Approach B: Manual Registration (Alternative)

Create `ADOPTION_REGISTRY.md` for manual tracking:

```markdown
# Adopting Repositories

This file tracks which repositories are using AI Hub Actions.

## Registered Adopters

| Repository | Actions Used | Contact | Notes |
|------------|--------------|---------|-------|
| repo-1 | review-and-merge, auto-merge | @user1 | Production since 2025-01 |
| repo-2 | spec-to-code | @user2 | Pilot testing |

## To Register

Add your repository to this table via PR.
```

**Recommendation**: Start with Approach A, use Approach B as fallback if telemetry insufficient.

### Action 1: Generate Initial Adoption Report

```bash
cd /home/jinno/github-actions-actions
python scripts/track_adoption.py --output .audit/metrics/adoption-report-2026-02-04.json
```

### Action 2: Update PURPOSE.md with Adoption Status

Add to "Current Status" section:

```markdown
### Phase 3: Stabilization & Adoption (In Progress)
- ✅ 各Actionの検証用ワークフローの作成 (`examples/`)
- ✅ 各Actionの導入ガイドの作成 (`instructions/`)
- 🔄 組織内プロジェクトへの導入とフィードバック収集
  - 現在の導入リポジトリ数: [X]（最新: YYYY-MM-DD）
  - 導入状況レポート: [link to .audit/metrics/adoption-report-*.json]
- ✅ ドキュメント（README）の整備
```

### Action 3: Create Automated Adoption Tracking Workflow

Add `.github/workflows/update-adoption-metrics.yml`:

```yaml
name: Update Adoption Metrics
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  track:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v3
      - name: Generate adoption report
        run: |
          python scripts/track_adoption.py \
            --output metrics/adoption-latest.json
      - name: Commit report
        run: |
          git config user.name "Adoption Tracker"
          git config user.email "adoption-tracker@ai-hub"
          git add metrics/adoption-latest.json
          git commit -m "chore: Update adoption metrics [skip ci]"
          git push
```

## Benefits

1. **Success Measurement**: Can track "複数のリポジトリで採用される" goal
2. **Prioritization**: Focus improvements on most-used actions
3. **Demonstration**: Show value to stakeholders with concrete numbers
4. **Feedback Loop**: Identify which repositories to solicit feedback from

## Risks

- **Risk**: Telemetry data may be insufficient (no recent runs)
  - **Mitigation**: Use Approach B (manual registration) as supplement
- **Risk**: Low adoption numbers may discourage team
  - **Mitigation**: Frame as "baseline for growth", emphasize Phase 3 is "In Progress"
- **Risk**: Privacy concerns about tracking
  - **Mitigation**: Use anonymized hashes only, emphasize opt-out capability

## Verification

**Success Criteria**:
- [ ] `scripts/track_adoption.py` exists and runs without errors
- [ ] Initial adoption report generated in `.audit/metrics/`
- [ ] PURPOSE.md updated with current adoption status
- [ ] Automated workflow created for weekly tracking
- [ ] docs/telemetry.md updated with adoption section

**Validation Method**:
```bash
# Verify script exists and is executable
ls -la scripts/track_adoption.py

# Generate initial report
python scripts/track_adoption.py --output test-report.json
cat test-report.json | jq .

# Verify PURPOSE.md updated
grep -A 5 "導入とフィードバック収集" PURPOSE.md | grep "導入リポジトリ数"
```

## Rollback

If tracking causes concerns:
```bash
# Remove tracking script
rm scripts/track_adoption.py

# Remove workflow
rm .github/workflows/update-adoption-metrics.yml

# Revert PURPOSE.md changes
git checkout HEAD -- PURPOSE.md

# Keep generated reports as historical data
```

## Alternatives Considered

1. **Don't track adoption (rely on word-of-mouth)**
   - **Rejected**: Cannot measure Phase 3 completion or success
2. **Require all repositories to register before using**
   - **Rejected**: Creates friction, reduces adoption
3. **Use external analytics service**
   - **Rejected**: Unnecessary dependency, telemetry sufficient

## Related Gaps

- Addresses: GAP-004 (Organizational adoption status unknown)

## Related Success Conditions

- Measures: "組織内の複数のリポジトリでこれらのActionsが採用される" (PURPOSE.md:70)
- Supports: Phase 3 completion criteria
