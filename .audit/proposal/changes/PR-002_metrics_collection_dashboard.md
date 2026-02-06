# PR-002: AIレビュー受入率メトリクスの定期的収集とダッシュボード構築

**優先度**: High (P1)
**作業規模**: Medium (1週間)
**依存関係**: なし

## 背景

**※この提案はASM-003（目標受入率70%）という仮定に基づいています**

- README.mdでAIレビュー受入率（Acceptance Rate）目標70%が記載されている
- しかし、実際の受入率データは収集・可視化されていない（C-017: 不明）
- `scripts/calculate_acceptance_rate.py` は存在するが、定期的な実行・レポート生成の仕組みがない
- 品質改善のPDCAサイクルを回すための「計測」機能が不足している

## 現状の問題点

1. **データ収集が手動**: 誰かが手動でスクリプトを実行しないとメトリクスが更新されない
2. **トレンドが見えない**: 時系列での受入率の変化を追跡できない
3. **チーム全体で共有されていない**: メトリクスが個人のローカル環境にとどまっている

## 提案する改善アクション

### Phase 1: GitHub Actions workflowによる定期収集 (2-3日)

**目的**: 週次で自動的に受入率を計算し、レポートを生成する

実装:
```yaml
# .github/workflows/collect-acceptance-rate.yml
name: Collect AI Review Acceptance Rate

on:
  schedule:
    # 毎週月曜日9:00 JSTに実行
    - cron: '0 0 * * 1'
  workflow_dispatch:  # 手動実行も可能

permissions:
  contents: read
  pull-requests: read

jobs:
  collect-metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Calculate acceptance rate (last 7 days)
        run: |
          python scripts/calculate_acceptance_rate.py \
            --output report \
            --time-period 7d \
            --output-file .audit/metrics/acceptance_rate_weekly.json

      - name: Calculate acceptance rate (last 30 days)
        run: |
          python scripts/calculate_acceptance_rate.py \
            --output report \
            --time-period 30d \
            --output-file .audit/metrics/acceptance_rate_monthly.json

      - name: Upload metrics as artifacts
        uses: actions/upload-artifact@v4
        with:
          name: acceptance-rate-metrics-${{ github.run_number }}
          path: .audit/metrics/
          retention-days: 90

      - name: Comment on tracking issue (if rate < 70%)
        if: ${{ steps.check_rate.outputs.rate < 70 }}
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: 123,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '⚠️ AIレビュー受入率が70%を下回っています: ${{ steps.check_rate.outputs.rate }}%'
            })
```

**期待される効果**:
- 週次で自動的に最新のメトリクスが収集される
- 過去90日間のレポートがartifactsとして保存される
- 目標未達の場合は自動的に通知される

### Phase 2: メトリクスダッシュボードの作成 (2-3日)

**目的**: 受入率のトレンドを視覚的に確認できるダッシュボードを構築

実装:
```python
# scripts/generate_metrics_dashboard.py
"""
AIレビュー受入率のダッシュボードを生成するスクリプト
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def generate_dashboard():
    metrics_dir = Path(".audit/metrics")
    weekly_files = sorted(metrics_dir.glob("acceptance_rate_weekly_*.json"))

    # 過去12週間のデータをプロット
    dates = []
    acceptance_rates = []

    for file in weekly_files[-12:]:
        data = json.loads(file.read_text())
        dates.append(datetime.fromisoformat(data["timestamp"]))
        acceptance_rates.append(data["acceptance_rate"])

    # グラフ描画
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, acceptance_rates, marker='o', linewidth=2, markersize=8)
    ax.axhline(y=70, color='r', linestyle='--', label='Target (70%)')
    ax.set_ylim(0, 100)
    ax.set_ylabel('Acceptance Rate (%)')
    ax.set_title('AI Review Acceptance Rate - Last 12 Weeks')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # x軸のフォーマット
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('.audit/metrics/acceptance_rate_dashboard.png', dpi=150)
    print(f"ダッシュボードを生成しました: .audit/metrics/acceptance_rate_dashboard.png")

if __name__ == "__main__":
    generate_dashboard()
```

**期待される効果**:
- 受入率のトレンドを一目で確認できる
- 品質改善の取り組みの効果を定量的に評価できる

### Phase 3: トラッキングIssueの作成と運用 (1日)

**目的**: メトリクスの可視化と継続的な改善サイクルを回す

実装:
1. GitHub Issueを作成: "Track AI Review Acceptance Rate"
2. 毎週のworkflow実行結果をコメントとして投稿
3. 過去のコメントからトレンドを確認可能にする

Issueテンプレート:
```markdown
## AIレビュー受入率トラッキング

**目標**: 70%以上
**現状**: 最新の値は週次レポートを参照

### 週次レポート

<!-- 各週のレポートがここに追加されていく -->

### 改善アクション

- 受入率が70%未満の場合: レビュープロンプトの改善を検討
- 受入率が低下傾向の場合: 新しい導入プロジェクトでの事例を収集
```

## 成功基準

- [ ] 週次で自動的にacceptance_rate_*.jsonが生成されている
- [ ] 過去12週間のトレンドグラフが生成されている
- [ ] トラッキングIssueでメトリクスがチーム全体で共有されている
- [ ] 目標70%未達の場合、自動的に通知が届く

## リスクと副作用

### リスク
- **GitHub APIレート制限**: 大量のPRを取得する場合に制限に達する可能性
  - **緩和策**: 過去30日分のみを取得し、キャッシュを活用

### 副作用
- **通知ノイズ**: 70%未達の通知が頻繁に来るとストレスになる可能性
  - **緩和策**: 通知頻度を月次に変更、または閾値を調整

## ロールバック計画

もし過剰な通知が問題になる場合:
1. workflowファイルを無効化: `workflow disable` コマンド
2. 通知閾値を50%に引き下げ

## 今後の改善（Phase 4+）

- [ ] 他のメトリクス（レビュー提案数、平均修正時間）も収集
- [ ] メトリクスをSlack/Teamsに通知
- [ ] CIパイプラインに統合し、PRごとのレビュー品質を計測

## 参考資料

- GAP-002: メトリクス収集の詳細分析
- QA-002: AIレビュー受入率の品質目標
- scripts/calculate_acceptance_rate.py: 既存の計算スクリプト
