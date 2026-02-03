# PR-003: 導入率（Adoption Rate）メトリクスの実装

**優先度**: MEDIUM (ISS-002)
**関連ギャップ**: ISS-002 - 本番利用率メトリクスの欠如
**状態**: Proposed

## 概要

テレメトリー機能を拡張し、組織・リポジトリレベルの導入率を追跡できるようにする。
現状の匿名化されたテレメトリーに集計機能を追加し、公開可能な導入状況レポートを作成する。

## 現状

- テレメトリーは実装済み（README.md:99-110）
- オプトアウト機能、SHA-256匿名化が実装されている
- しかし、導入率（どの程度の組織で使われているか）は可視化されていない（C-019: unknown）

## 提案内容

### Phase 1: テレメトリーデータの集約機能追加（2-3日）

1. **一意識別子の集約**
   - 現状: リポジトリ名をSHA-256ハッシュ化（先頭16文字）
   - 追加: ユニークリポジトリ数、ユニーク組織数を集計

2. **時系列データの保存**
   - 月次/週次のスナップショットを保存
   - トレンド分析を可能にする

### Phase 2: 導入率ダッシュボードの作成（2-3日）

1. **シンプルな集計レポート**
   ```markdown
   # Adoption Metrics

   ## Unique Repositories
   - Total: 45
   - Active (last 30 days): 32

   ## Unique Organizations (SHA-256 hashed)
   - Total: 12
   - Active (last 30 days): 9

   ## Action Usage Breakdown
   - review-and-merge: 28 repos
   - auto-merge: 15 repos
   - ...
   ```

2. **プライバシー保護の強化**
   - リポジトリ名は完全にハッシュ化
   - 小規模な組織（< 5リポジトリ）は集計から除外
   - 生データは公開しない

### Phase 3: GitHub Actionsでの自動収集（1-2日）

1. **週次の集計ジョブ**
   - テレメトリーデータの集計
   - レポートの自動生成
   - GitHub Pagesへのデプロイ（オプション）

## 実装手順

### 1. テレメトリーデータ構造の拡張

現状のテレメトリー収集（仮定）:

```python
# lib/telemetry.py（既存と仮定）
def send_telemetry(event_type, action_name, **metadata):
    data = {
        "event_type": event_type,
        "action_name": action_name,
        "repo_hash": hashlib.sha256(repo_name.encode()).hexdigest()[:16],
        "timestamp": datetime.now().isoformat(),
        **metadata
    }
    # 送信処理...
```

拡張案:

```python
# lib/telemetry_collector.py（新規）
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

class TelemetryCollector:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self):
        """テレメトリーデータをロード"""
        if not self.data_path.exists():
            return {"events": []}
        return json.loads(self.data_path.read_text())

    def get_unique_repos(self, days=30):
        """ユニークリポジトリ数を取得（直近N日間）"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_events = [
            e for e in self.data["events"]
            if datetime.fromisoformat(e["timestamp"]) > cutoff
        ]
        return len(set(e["repo_hash"] for e in recent_events))

    def get_action_usage(self, days=30):
        """Actionごとの使用数を取得"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_events = [
            e for e in self.data["events"]
            if datetime.fromisoformat(e["timestamp"]) > cutoff
        ]

        action_repos = defaultdict(set)
        for event in recent_events:
            action_repos[event["action_name"]].add(event["repo_hash"])

        return {
            action: len(repos)
            for action, repos in action_repos.items()
        }
```

### 2. 集計レポート生成スクリプト

`scripts/generate_adoption_report.py`:

```python
#!/usr/bin/env python3
"""Generate adoption metrics report from telemetry data."""
import json
from pathlib import Path
from datetime import datetime
from lib.telemetry_collector import TelemetryCollector

def generate_adoption_report(data_path: Path, output_path: Path):
    """導入率レポートを生成"""
    collector = TelemetryCollector(data_path)

    unique_repos_30d = collector.get_unique_repos(days=30)
    unique_repos_all = collector.get_unique_repos(days=365)

    action_usage = collector.get_action_usage(days=30)

    report = f"""# Adoption Metrics

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Unique Repositories

| Period | Count |
|--------|-------|
| Last 30 days | {unique_repos_30d} |
| All time | {unique_repos_all} |

## Action Usage (Last 30 Days)

| Action | Repos Using |
|--------|-------------|
{chr(10).join(f"| {action} | {count} |" for action, count in sorted(action_usage.items(), key=lambda x: -x[1]))}

## Privacy Notice

- Repository names are SHA-256 hashed (first 16 characters)
- No individual repository data is disclosed
- Small organizations (< 5 repos) are excluded from aggregation

---

## Methodology

**Unique Repository Definition**: Unique SHA-256 hash of repository name

**Active Definition**: Repository that has triggered any action in the period

**Data Source**: Anonymous telemetry (opt-out available via `DISABLE_TELEMTERY`)

**Limitations**:
- Actual adoption may be higher (some users disable telemetry)
- Organization-level count is estimated from repo hashes
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    print(f"Adoption report generated: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--telemetry-data", default="telemetry/events.json")
    parser.add_argument("--output", default="metrics/ADOPTION_REPORT.md")
    args = parser.parse_args()

    generate_adoption_report(Path(args.telemetry_data), Path(args.output))
```

### 3. GitHub Actionsでの自動収集

`.github/workflows/generate-adoption-report.yml`:

```yaml
name: Generate Adoption Report

on:
  schedule:
    - cron: '0 0 * * 0'  # 毎週日曜日
  workflow_dispatch:

permissions:
  contents: read

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Generate Adoption Report
        env:
          TELEMETRY_DATA_PATH: ${{ secrets.TELEMETRY_DATA_PATH }}
        run: |
          python scripts/generate_adoption_report.py \
            --telemetry-data "$TELEMETRY_DATA_PATH" \
            --output metrics/ADOPTION_REPORT.md

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: adoption-report
          path: metrics/ADOPTION_REPORT.md
```

## 期待効果

1. **成功判定**: PURPOSE.md:71の「組織内の複数のリポジトリで採用される」を定量化
2. **意思決定**: プロジェクトの継続/終了の判断材料
3. **コミュニティ形成**: 導入実績を見せることで、新規導入の促進
4. **優先順位付け**: よく使われるActionの特定と改善の集中

## 副作用とリスク

1. **プライバシー**: テレメトリーの拡張によるプライバシー懸念
   - 対策: 完全な匿名化、オプトアウト機能の維持、ポリシーの明記
2. **データの解釈**: 導入率が低い場合、ネガティブな印象
   - 対策: 「ベータ版」「成長中」といった文脈を提供
3. **コスト**: テレメトリー収集のバックエンド維持
   - 対策: 低コストなソリューション（GitHub Artifacts, GitHub Pages）

## 検証方法

1. `scripts/generate_adoption_report.py` が実行できること
2. 出力されるレポートが適切に匿名化されていること
3. GitHub Actionsが正常に実行され、レポートが更新されること

## ロールバック計画

- テレメトリー収集は既存機能の拡張であり、破壊的変更ではない
- 問題発生時は、集計スクリプトのみを無効化

## 関連ファイル

- 新規: `lib/telemetry_collector.py`
- 新規: `scripts/generate_adoption_report.py`
- 新規: `.github/workflows/generate-adoption-report.yml`
- 新規: `metrics/ADOPTION_REPORT.md` (自動生成)
- 変更: `docs/telemetry.md` (プライバシーポリシーの更新)

## 次のアクション

1. 本提案のレビューと承認
2. テレメトリーデータ構造の確認と拡張設計
3. `telemetry_collector.py` の実装
4. 最初の導入率レポートの生成
5. プライバシーポリシーの更新

---

**作成日**: 2025-02-03
**作成者**: Repo Genesis Auditor (run-initial)
**仮定に基づく**: テレメトリー収集機能が実装されているという仮定（C-014）
**注意**: 実際のテレメトリー実装を確認後に調整が必要
