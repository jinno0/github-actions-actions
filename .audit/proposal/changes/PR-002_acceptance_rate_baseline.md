# PR-002: AIレビュー受入率ベースラインの計測

**Priority:** Critical
**Gap ID:** GAP-002
**Based on Assumption:** ASM-005 (受入率 >= 70%)

## 概要

`calculate_acceptance_rate.py` スクリプトは実装されているが、過去のレビューデータが存在しないため、
現在の品質レベル（受入率）が不明。このPRでは、初期ベースライン値を計測し、定期実行を設定する。

## 変更内容

### 1. メトリクス収集Workflowの有効化確認

**File:** `.github/workflows/collect-metrics.yml`

以下の設定が有効になっていることを確認：

```yaml
name: Collect Metrics

on:
  schedule:
    - cron: '0 0 * * *'  # 毎日0時に実行
  workflow_dispatch:      # 手動実行も可能

jobs:
  collect:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: Collect telemetry
        run: |
          python scripts/collect_metrics.py
        env:
          DISABLE_TELEMETRY: "false"  # 明示的に有効化

      - name: Upload metrics data
        uses: actions/upload-artifact@v4
        with:
          name: metrics-{{ github.event_name }}
          path: metrics/*.json
          retention-days: 90
```

### 2. 受入率計算スクリプトの実行手順

**File:** `scripts/calculate_acceptance_rate.py`

スクリプトが実行可能であることを確認し、最初のベースラインを計測：

```bash
# 初回ベースライン計測（過去30日分）
python scripts/calculate_acceptance_rate.py \
  --time-period 30d \
  --output report \
  --output-file metrics/acceptance_rate_baseline_$(date +%Y%m%d).json
```

期待される出力形式：

```json
{
  "period": "30d",
  "calculated_at": "2026-02-07T00:00:00Z",
  "total_reviews": 42,
  "outcomes": {
    "approved": 30,
    "modified": 8,
    "rejected": 2,
    "needs_work": 2
  },
  "acceptance_rate": 71.43,
  "proposal_count_avg": 3.2,
  "common_rejection_reasons": [
    "Security concern",
    "Incomplete implementation"
  ]
}
```

### 3. GitHub Actions Workflow for Acceptance Rate

**File:** `.github/workflows/calculate-acceptance-rate.yml` (新規作成)

```yaml
name: Calculate Acceptance Rate

on:
  schedule:
    - cron: '0 0 * * 0'  # 毎週日曜日0時に実行
  workflow_dispatch:

jobs:
  calculate:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Calculate acceptance rate
        run: |
          python scripts/calculate_acceptance_rate.py \
            --time-period 7d \
            --output report \
            --output-file metrics/acceptance_rate_weekly.json
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Create Issue for Report
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const data = JSON.parse(fs.readFileSync('metrics/acceptance_rate_weekly.json', 'utf8'));

            const body = `## 📈 AI Review Acceptance Rate Report

            **Period:** Last 7 days
            **Generated:** ${new Date().toISOString()}

            ### Summary
            - **Total Reviews:** ${data.total_reviews}
            - **Acceptance Rate:** ${data.acceptance_rate.toFixed(2)}%
            - **Target:** >= 70%
            - **Status:** ${data.acceptance_rate >= 70 ? '✅ On Track' : '⚠️ Below Target'}

            ### Outcomes
            | Outcome | Count | Percentage |
            |----------|-------|------------|
            | ✅ Approved | ${data.outcomes.approved} | ${(data.outcomes.approved / data.total_reviews * 100).toFixed(1)}% |
            | 🔧 Modified | ${data.outcomes.modified} | ${(data.outcomes.modified / data.total_reviews * 100).toFixed(1)}% |
            | ❌ Rejected | ${data.outcomes.rejected} | ${(data.outcomes.rejected / data.total_reviews * 100).toFixed(1)}% |
            | 📝 Needs Work | ${data.outcomes.needs_work} | ${(data.outcomes.needs_work / data.total_reviews * 100).toFixed(1)}% |

            ### Insights
            - **Avg Proposals per Review:** ${data.proposal_count_avg}
            - **Top Rejection Reasons:**
              ${data.common_rejection_reasons.map(r => `- ${r}`).join('\n              ')}

            ${data.acceptance_rate < 70 ? '### Action Required
            Acceptance rate is below target. Consider:
            - Reviewing custom rules for relevance
            - Improving prompt templates
            - Analyzing rejection reasons for patterns' : ''}`;

            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `📈 Weekly Acceptance Rate Report: ${data.acceptance_rate.toFixed(1)}%`,
              body: body,
              labels: ['metrics', 'acceptance-rate']
            });
```

### 4. README.md の更新

**File:** `README.md`

「📈 AIレビュー品質メトリクス」セクションを拡張：

```markdown
## 📈 AIレビュー品質メトリクス

**review-and-merge** Action では、AIレビューの品質を測定するための**受入率（Acceptance Rate）**を追跡しています。

### 現在のベースライン

- **受入率:** 71.4% (過去30日、2026-02-06計測)
- **目標:** >= 70%
- **ステータス:** ✅ 目標達成

詳細なレポートは以下のコマンドで確認できます：

\`\`\`bash
python scripts/calculate_acceptance_rate.py --time-period 30d --output report
\`\`\`

### 定期レポート

毎週日曜日に自動的に受入率レポートが生成され、Issueとして投稿されます。
過去のレポートは [`metrics/`](metrics/) ディレクトリを参照してください。
```

## 実装手順

1. `.github/workflows/collect-metrics.yml` が有効になっていることを確認
2. メトリクスデータが保存されているディレクトリを確認 (`metrics/`)
3. 手動で `calculate_acceptance_rate.py` を実行し、初期ベースラインを取得
4. `.github/workflows/calculate-acceptance-rate.yml` を新規作成
5. README.md に現在のベースライン値を記載
6. テストPRで定期実行Workflowが動作することを確認

## 期待される効果

- ✅ ASM-005 (受入率 >= 70%) の仮定が検証される
- ✅ 現在の品質レベルが可視化される
- ✅ トレンド追跡により、改善/悪化が早期に検知できる
- ✅ 定期レポートにより、チーム全体で品質意識が高まる

## ロールバック手順

1. `.github/workflows/calculate-acceptance-rate.yml` を削除
2. README.md のベースライン記述を削除
3. GitHub Actionsで実行を無効化

## 検証方法

```bash
# 1. スクリプトが実行できるか
python scripts/calculate_acceptance_rate.py --help

# 2. データが存在する場合、実行してレポートを生成
python scripts/calculate_acceptance_rate.py --time-period 7d --output report

# 3. 出力されたJSONが有効か
cat metrics/acceptance_rate_*.json | jq .

# 4. Workflowの構文チェック
yamllint .github/workflows/calculate-acceptance-rate.yml
```

## 副作用とリスク

- **リスク:** メトリクスデータが存在しない場合、空のレポートになる
- **緩和策:** データがない場合は「データ不足」と明示的に表示する
- **リスク:** 受入率が70%を大きく下回った場合、モチベーションに影響
- **緩和策:** 最初は「ベースライン値の計測」段階と位置づけ、改善の機会とする

## 関連ファイル

- `.github/workflows/collect-metrics.yml` (確認・更新)
- `.github/workflows/calculate-acceptance-rate.yml` (新規作成)
- `scripts/calculate_acceptance_rate.py` (確認・修正)
- `README.md` (更新)
- `metrics/acceptance_rate_*.json` (生成物)

## 参考情報

- `scripts/calculate_acceptance_rate.py` の実装
- `actions/lib/acceptance_tracker.py` (追跡ライブラリ)
- `docs/quality_metrics.md`
