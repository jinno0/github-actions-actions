# Pilot Adoption Guide

AI Actionsのパイロット導入の手引きです。

## 対象

- Self-hosted Runnerを運用しているリポジトリ
- 活発にPRが作成されているリポジトリ（週5件以上）
- Claude Code CLIがインストールされている環境

## 手順

### 1. review-and-merge Actionの導入

\`examples/review-and-merge-example.yml\` を参照して、ワークフローを追加してください。

基本的なワークフロー例:

\`\`\`yaml
name: AI Review
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  review:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: AI Review and Fix
        uses: ./actions/review-and-merge
        with:
          claude-model: 'sonnet'
          lgtm-threshold: '7'
          auto-fix: 'true'
\`\`\`

### 2. カスタムルールの作成（オプション）

プロジェクト固有のコーディング規約がある場合は、カスタムルールを作成してください。

詳細は \`instructions/review-and-merge-custom-rules.md\` を参照してください。

例:
\`\`\`yaml
- uses: ./actions/review-and-merge
  with:
    custom-rules: |
      - Follow Python PEP 8 style guidelines
      - Include docstrings for all functions
      - Maintain test coverage above 80%
      - All new code must have tests
\`\`\`

### 3. メトリクス収集の開始

導入後、1週間程度でデータが蓄積されます。

#### 手動での受入率レポート生成

\`\`\`bash
# 受入率レポートの生成（過去7日間）
python scripts/calculate_acceptance_rate.py --output report.md --time-period 7d
\`\`\`

#### 自動メトリクス収集の有効化

以下のワークフローが自動的にメトリクスを収集します:

- **Daily Metrics**: \`collect-metrics.yml\` - 毎日0時に実行
- **Weekly Report**: \`generate-quality-report.yml\` - 毎週月曜日9時に実行

これらのワークフローはGitHub Actionsで自動的に実行されます。

### 4. フィードバックの収集

以下の情報を記録してください:

#### 定量的データ
- AIレビューの提案数
- 人間によるレビュー結果（approved/modified/rejected）
- 実行時間
- メモリ使用量

#### 定性的データ
- 開発者のフィードバック
- 有用だと思ったレビューの例
- 改善が必要と思ったレビューの例
- 誤検知の例

## 成功基準

- ✅ AIレビューの受入率が70%以上であること
- ✅ 開発者がAIレビューを有用と感じていること
- ✅ 実行時間が30分以内であること
- ✅ 既存のテストがすべてパスすること

## 監視方法

### 短期的（最初の1週間）

1. **実行状況の確認**
   \`\`\`bash
   # ワークフローの実行状況を確認
   gh run list --workflow=AI+Review --limit 10
   \`\`\`

2. **エラーの確認**
   \`\`\`bash
   # 失敗した実行を確認
   gh run list --workflow=AI+Review --status=failure
   \`\`\`

### 中期的（最初の1ヶ月）

1. **受入率の追跡**
   \`\`\`bash
   # 週次レポートを生成
   python scripts/calculate_acceptance_rate.py --output weekly_report.md --time-period 7d
   \`\`\`

2. **トレンドの分析**
   \`\`\`bash
   # テレメトリーレポートを生成
   python scripts/generate_adoption_report.py --output trends.md
   \`\`\`

## トラブルシューティング

### Claude CLIが見つからない

\`\`\`
Error: Claude CLI not found
\`\`\`

**解決策**:
1. Self-hosted RunnerにClaude Code CLIをインストール
2. \`which claude\` でパスを確認
3. ワークフローでPATHを設定

### レビューが実行されない

\`\`\`
No review comments posted
\`\`\`

**解決策**:
1. GitHubトークンの権限を確認（\`pull-requests:write\`が必要）
2. ワークフローのトリガー条件を確認
3. ログでエラーを確認

### 受入率が低い

**目標**: 70%以上

**改善策**:
1. カスタムルールを調整
2. LGTM閾値を下げる（例: 7→6）
3. レビュープロンプトテンプレートをカスタマイズ
4. 開発者にフィードバックを収集

### 実行時間が長い

**目標**: 30分以内

**改善策**:
1. より高速なモデルを使用（haiku）
2. PRのサイズ制限を設ける
3. 差分のみをレビュー
4. Runnerのスペックを確認

## 次のステップ

パイロット導入の結果を \`ADOPTION_GUIDE.md\` に反映してください。

以下の情報を記録:

1. 導入リポジトリと期間
2. 受入率と実行時間のデータ
3. 開発者からのフィードバック
4. 遇到した問題と解決策
5. 推奨される設定

## サポートとフィードバック

問題が発生した場合やフィードバックがある場合は:

1. GitHub Issuesを作成
2. テレメトリーデータを添付（可能であれば）
3. 再現手順を詳細に記述

---

**最終更新**: 2026-02-04
**バージョン**: 1.0
