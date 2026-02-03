# PR-001: テレメトリーダッシュボード作成

## Issue
- **ID**: ISS-005
- **Severity**: Medium (Quick Win)
- **Title**: Action使用状況の可視化不足

## Current State
- テレメトリー収集機能は実装済み（README.md:98-119）
- しかし、可視化・報告機能が不足している
- 各Actionの実行回数・成功率・エラー率が不明（C-020）

## Proposed Changes

### 1. テレメトリー集計スクリプト作成
**File**: `scripts/generate_telemetry_report.py`

```python
#!/usr/bin/env python3
"""
Generate telemetry report from collected metrics
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def load_metrics(metrics_dir: Path) -> dict:
    """Load metrics from JSON files"""
    metrics = defaultdict(lambda: {
        "total_runs": 0,
        "successes": 0,
        "failures": 0,
        "errors": []
    })
    
    for file in metrics_dir.glob("*.json"):
        data = json.loads(file.read_text())
        action_name = data.get("action_name", "unknown")
        metrics[action_name]["total_runs"] += 1
        if data.get("status") == "success":
            metrics[action_name]["successes"] += 1
        else:
            metrics[action_name]["failures"] += 1
            if "error" in data:
                metrics[action_name]["errors"].append(data["error"])
    
    return dict(metrics)

def generate_report(metrics: dict) -> str:
    """Generate markdown report"""
    report = ["# AI Actions Telemetry Report\n"]
    report.append(f"Generated: {datetime.now().isoformat()}\n\n")
    
    # Summary
    total_runs = sum(m["total_runs"] for m in metrics.values())
    total_successes = sum(m["successes"] for m in metrics.values())
    overall_success_rate = (total_successes / total_runs * 100) if total_runs > 0 else 0
    
    report.append("## Summary\n")
    report.append(f"- Total Runs: {total_runs}\n")
    report.append(f"- Overall Success Rate: {overall_success_rate:.1f}%\n\n")
    
    # Per-Action Breakdown
    report.append("## Per-Action Breakdown\n\n")
    for action_name, data in sorted(metrics.items(), key=lambda x: x[1]["total_runs"], reverse=True):
        if data["total_runs"] == 0:
            continue
        success_rate = (data["successes"] / data["total_runs"] * 100)
        report.append(f"### {action_name}\n")
        report.append(f"- Runs: {data['total_runs']}\n")
        report.append(f"- Success Rate: {success_rate:.1f}%\n")
        if data["failures"] > 0:
            report.append(f"- Failures: {data['failures']}\n")
        report.append("\n")
    
    return "".join(report)

if __name__ == "__main__":
    metrics_dir = Path("metrics")
    output_file = Path("docs/telemetry_report.md")
    
    metrics = load_metrics(metrics_dir)
    report = generate_report(metrics)
    
    output_file.write_text(report)
    print(f"Report generated: {output_file}")
```

### 2. CIワークフロー追加
**File**: `.github/workflows/generate-telemetry-report.yml`

```yaml
name: Generate Telemetry Report

on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight
  workflow_dispatch:

permissions:
  contents: write

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate report
        run: |
          python scripts/generate_telemetry_report.py
          
      - name: Commit report
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/telemetry_report.md
          git diff --staged --quiet || git commit -m "chore: update telemetry report"
          git push
```

### 3. ドキュメント更新
**File**: `docs/telemetry.md` (追記)

```markdown
## Telemetry Reports

Weekly telemetry reports are automatically generated and published to [telemetry_report.md](./telemetry_report.md).

### View Reports
- Latest Report: [telemetry_report.md](./telemetry_report.md)
- Historical: Git history of `docs/telemetry_report.md`
```

## Expected Outcomes

### Metrics
- ダッシュボード閲覧可能: 週次自動更新
- Action別実行回数・成功率可視化
- エラー傾向の把握

### Quality
- 運用上の意思決定がデータドリブンで可能に
- 人気のあるActionと使われていないActionを特定
- 改善の優先順位決定が容易に

## Verification

### Success Criteria
1. `python scripts/generate_telemetry_report.py` がエラーなく実行される
2. `docs/telemetry_report.md` が生成される
3. CIワークフローが成功する
4. レポートがMarkdown形式で正しく表示される

### Test Plan
```bash
# 1. スクリプト実行テスト
python scripts/generate_telemetry_report.py
cat docs/telemetry_report.md

# 2. 空メトリクスでのテスト
mv metrics metrics.bak
mkdir metrics
python scripts/generate_telemetry_report.py  # Should handle empty
mv metrics.bak metrics

# 3. CI手動実行
gh workflow run generate-telemetry-report.yml
```

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| メトリクスファイルが破損 | Low | Low | JSONバリデーション追加 |
| 空メトリクスでのエラー | Medium | Low | デフォルト値処理 |
| CIが古いレポートを上書き | Low | Low | Git historyで保持 |

## Rollback Plan

1. CIワークフローを削除:
   ```bash
   rm .github/workflows/generate-telemetry-report.yml
   ```

2. スクリプトを削除:
   ```bash
   rm scripts/generate_telemetry_report.py
   ```

3. ドキュメントを元に戻す:
   ```bash
   git checkout HEAD -- docs/telemetry.md
   ```

## Alternatives Considered

1. **Grafanaダッシュボード導入**
   - Rejected: インフラコストが高い、過剰機能

2. **Google Data Studio**
   - Rejected: 外部サービス依存、プライバシー懸念

3. **シェルスクリプトで実装**
   - Rejected: Pythonの方がメンテナンス性が高い

## Timeline

- 実装: 2-3日
- テスト: 1日
- デプロイ: 1日
- **Total: 4-5日**

## Dependencies

- メトリクス収集機能（既存）
- Python 3.x
- GitHub Actions CI

## Related Proposals

- PR-002: 受入率レポート（同様のパターン）
- PR-003: 導入追跡システム
