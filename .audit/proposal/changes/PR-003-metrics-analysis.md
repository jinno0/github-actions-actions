# PR-003: 受入率メトリクスの実データ分析とダッシュボード作成

**提出者**: Repo Genesis Auditor (Run #2026-02-03T23:20:15Z)
**優先度**: 低
**種別**: 分析 & 改善
**推定工数**: 小（2-4時間）

---

## 概要

README.md:121-139で説明されているAIレビュー品質メトリクス（受入率）の実際のデータを分析し、現在の品質レベルと改善余地を評価します。また、定期的なメトリクス確認の仕組みを導入します。

## 問題の背景

### 現状
- **README.md**: 受入率追跡機能と目標値（>= 70%）が記載されている
- **スクリプト**: `scripts/calculate_acceptance_rate.py` が存在し実行可能
- **課題**: 実際の受入率の数値、トレンド、改善状況が不明

### 既存データ
- `scripts/calculate_acceptance_rate.py` が存在
- `metrics/acceptance_rate_30d.json` が存在することが確認されている

---

## 提案するアクション

### Phase 1: メトリクスデータの分析

#### ステップ 1: 現在の受入率を計算
```bash
cd /home/jinno/github-actions-actions
python3 scripts/calculate_acceptance_rate.py --output report --time-period 30d
```

#### ステップ 2: メトリクスの可視化
**新規ファイル**: `scripts/visualize_metrics.py`

**機能**:
- 受入率の時系列推移をグラフ化
- レビューアウトカム（approved/modified/rejected/needs_work）の割合を円グラフ化
- HTML形式のダッシュボードを生成

**実装例**:
```python
#!/usr/bin/env python3
"""
Visualize AI review quality metrics.
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import base64
from io import BytesIO

def generate_html_dashboard(metrics_data: dict, output_path: Path):
    """Generate HTML dashboard with embedded charts."""

    # Extract data
    acceptance_rate = metrics_data.get('acceptance_rate', 0)
    outcome_counts = metrics_data.get('outcome_counts', {})
    total_reviews = metrics_data.get('total_reviews', 0)
    time_series = metrics_data.get('time_series', [])

    # Generate simple bar chart using HTML/CSS (no external dependencies)
    outcome_bars = ""
    for outcome, count in outcome_counts.items():
        percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
        color = {
            'approved': '#28a745',
            'modified': '#ffc107',
            'rejected': '#dc3545',
            'needs_work': '#6c757d'
        }.get(outcome, '#17a2b8')

        outcome_bars += f"""
        <div style="margin-bottom: 10px;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>{outcome.title()}</span>
            <span>{count} ({percentage:.1f}%)</span>
          </div>
          <div style="background: #e9ecef; border-radius: 4px; height: 20px;">
            <div style="background: {color}; width: {percentage}%; height: 100%; border-radius: 4px;"></div>
          </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>AI Review Quality Metrics</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; margin-top: 30px; }}
        .metric {{ font-size: 48px; font-weight: bold; color: #28a745; }}
        .metric-label {{ font-size: 18px; color: #666; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; }}
        .target {{ font-size: 14px; color: #6c757d; }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🤖 AI Review Quality Metrics</h1>
        <p class="target">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="card">
          <div class="metric-label">Acceptance Rate (Target: ≥70%)</div>
          <div class="metric">{acceptance_rate:.1f}%</div>
        </div>

        <h2>Review Outcomes</h2>
        <div class="card">
          <p><strong>Total Reviews:</strong> {total_reviews}</p>
          {outcome_bars}
        </div>

        <h2>Time Series (Last 30 Days)</h2>
        <div class="card">
          <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #f8f9fa;">
              <th style="padding: 10px; text-align: left;">Date</th>
              <th style="padding: 10px; text-align: right;">Reviews</th>
              <th style="padding: 10px; text-align: right;">Acceptance Rate</th>
            </tr>
            {''.join([f'<tr><td style="padding: 8px; border-bottom: 1px solid #dee2e6;">{item["date"]}</td><td style="padding: 8px; border-bottom: 1px solid #dee2e6; text-align: right;">{item["count"]}</td><td style="padding: 8px; border-bottom: 1px solid #dee2e6; text-align: right;">{item["rate"]:.1f}%</td></tr>' for item in time_series[-7:]])}
          </table>
        </div>

        <h2>Interpretation</h2>
        <div class="card">
          <p><strong>What this means:</strong></p>
          <ul>
            <li>Acceptance rate < 70%: ⚠️ AIレビューの精度が目標に達していない。改善が必要。</li>
            <li>Acceptance rate ≥ 70%: ✅ AIレビューが有効に機能している。</li>
            <li>High 'modified' rate: 💡 AIの提案は有用だが、一部修正が必要。</li>
            <li>High 'rejected' rate: ⚠️ AIレビューの精度や関連性に問題がある可能性。</li>
          </ul>
        </div>
      </div>
    </body>
    </html>
    """

    output_path.write_text(html, encoding='utf-8')
    print(f"✅ Dashboard generated: {output_path}")

def main():
    metrics_file = Path("/home/jinno/github-actions-actions/metrics/acceptance_rate_30d.json")

    if not metrics_file.exists():
        print("❌ Metrics file not found. Run calculate_acceptance_rate.py first.")
        sys.exit(1)

    with open(metrics_file) as f:
        metrics_data = json.load(f)

    output_html = Path("/home/jinno/github-actions-actions/docs/metrics_dashboard.html")
    generate_html_dashboard(metrics_data, output_html)

    # Also copy to GitHub Pages or similar if configured
    print(f"✅ Open dashboard: file://{output_html}")

if __name__ == '__main__':
    main()
```

---

### Phase 2: CIへの統合

**新規ファイル**: `.github/workflows/update-metrics-dashboard.yml`

```yaml
name: 'Update Metrics Dashboard'

on:
  schedule:
    - cron: '0 6 * * *'  # Every day at 6 AM
  workflow_dispatch:

permissions:
  contents: read

jobs:
  update-dashboard:
    runs-on: self-hosted
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Calculate acceptance rate
        run: |
          python3 scripts/calculate_acceptance_rate.py \
            --output json \
            --time-period 30d \
            --metrics-file metrics/acceptance_rate_30d.json

      - name: Generate dashboard
        run: |
          python3 scripts/visualize_metrics.py

      - name: Commit changes
        run: |
          git config user.name 'GitHub Actions'
          git config user.email 'actions@github.com'

          if [[ -n $(git diff docs/metrics_dashboard.html) ]]; then
            git add docs/metrics_dashboard.html
            git commit -m "chore: Update metrics dashboard [skip ci]"
            git push
          fi
```

---

### Phase 3: README.mdへの反映

README.md:121-139のセクションに実際の数値を反映:

```markdown
## 📈 AIレビュー品質メトリクス

**review-and-merge** Action では、AIレビューの品質を測定するための**受入率（Acceptance Rate）**を追跡しています。これにより、AIレビューの有効性を定量的に評価できます。

### 現在の品質レベル

- **受入率**: XX.X%（目標: ≥70%）
- **総レビュー数**: XXX件
- **最新更新**: YYYY-MM-DD

📊 **詳細なダッシュボード**: [metrics_dashboard.html](metrics_dashboard.html) を参照してください。

### 品質メトリクスの概要
...
```

---

## 実行手順

### ステップ 1: データの確認と分析
```bash
cd /home/jinno/github-actions-actions

# 現在の受入率を計算
python3 scripts/calculate_acceptance_rate.py --output report --time-period 30d

# JSONで出力（後で使用）
python3 scripts/calculate_acceptance_rate.py --output json --time-period 30d > metrics/acceptance_rate_30d.json
```

### ステップ 2: 可視化スクリプトの作成と実行
```bash
# スクリプトを作成
# （上記の visualize_metrics.py を作成）

# 実行
python3 scripts/visualize_metrics.py

# ダッシュボードを確認
firefox docs/metrics_dashboard.html  # またはブラウザで開く
```

### ステップ 3: CIの設定
```bash
# ワークフローを作成
# （上記の .github/workflows/update-metrics-dashboard.yml を作成）

# Push
git add .github/workflows/update-metrics-dashboard.yml
git commit -m "Add metrics dashboard CI"
git push
```

### ステップ 4: READMEの更新
```markdown
# README.md:121-139 に実際の数値を反映
```

---

## 成功の基準

- [ ] 現在の受入率が計算されている
- [ ] `docs/metrics_dashboard.html` が生成されている
- [ ] ダッシュボードがブラウザで正しく表示される
- [ ] CIで定期的にダッシュボードが更新される
- [ ] README.mdで現在の品質レベルが公開されている

---

## 副作用とリスク

### 副作用
- **データのプライバシー**: レビュー内容は含まれないが、メトリクスデータにはリポジトリ名が含まれる可能性がある

### リスク
- **低受入率**: 受入率が70%を下回っている場合、READMEに公開する際にネガティブな印象を与える可能性
- **データ不足**: まだ十分なレビュー数がない場合、統計的な有意性が低い

### 対策
- 受入率が低い場合は「改善中」であることを明記
- レビュー数が少ない場合は「データ収集中」であることを明記

---

## ロールバック手順

```bash
cd /home/jinno/github-actions-actions

# スクリプトとワークフローの削除
rm scripts/visualize_metrics.py
rm .github/workflows/update-metrics-dashboard.yml
rm docs/metrics_dashboard.html

# READMEの復元
git checkout README.md
```

---

## 改善のアイデア（将来の拡張）

1. **アラート**: 受入率が閾値を下回った場合に通知を送信
2. **トレンド分析**: 受入率の推移を分析し、改善/悪化の傾向を把握
3. **Action別のメトリクス**: review-and-merge以外のActionでも同様のメトリクスを収集
4. **原因分析**: 'rejected'や'modified'の主要原因を分析

---

## 次のアクション

1. **データ確認**: `calculate_acceptance_rate.py` を実行し、現在の受入率を確認
2. **可視化スクリプト実装**: `visualize_metrics.py` を作成
3. **ダッシュボード生成**: 初回ダッシュボードを生成
4. **CI統合**: 定期更新用のワークフローを作成
5. **README更新**: 現在の品質レベルをREADMEに反映

---

## 参考資料

- README.md:121-139（AIレビュー品質メトリクスの説明）
- scripts/calculate_acceptance_rate.py（既存の計算スクリプト）
- .audit/analysis/gap.yml（CF-004: 受入率の実際の数値が不明）
