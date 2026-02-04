# PR-002: Collect AI Review Acceptance Rate Metrics

**Priority:** CRITICAL
**Gap ID:** GAP-001, GAP-004
**Estimated Effort:** 4-8 hours (setup) + 2-4 weeks (data collection)

---

## Summary

AIレビューの受入率を測定するためのデータ収集を開始するPRです。

---

## Problem

- `calculate_acceptance_rate.py` スクリプトは存在するが、実際の運用データがない
- 目標値70%に対する達成状況を証明できない
- AIレビューの有効性を示せない

---

## Proposed Changes

### 1. テレメトリー収集の有効化

既存の `collect_metrics.py` をCI/CDで定期的に実行するように設定します。

#### 新規ワークフロー: `.github/workflows/collect-metrics.yml`

\`\`\`yaml
name: Collect Metrics

on:
  schedule:
    # 毎日0時に実行
    - cron: '0 0 * * *'
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: read

jobs:
  collect:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: Collect Metrics
        run: |
          python scripts/collect_metrics.py --output .audit/metrics/
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Upload Metrics
        uses: actions/upload-artifact@v4
        with:
          name: metrics-${{ github.run_number }}
          path: .audit/metrics/
          retention-days: 90
\`\`\`

### 2. 受入率計算レポートの自動生成

週次レポートを生成するワークフローを追加します。

#### 新規ワークフロー: `.github/workflows/generate-quality-report.yml`

\`\`\`yaml
name: Generate Quality Report

on:
  schedule:
    # 毎週月曜日9時に実行
    - cron: '0 9 * * 1'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  report:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4

      - name: Calculate Acceptance Rate
        run: |
          python scripts/calculate_acceptance_rate.py \
            --output .audit/output/acceptance_rate_report.md \
            --time-period 7d
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: acceptance-rate-report-${{ github.run_number }}
          path: .audit/output/acceptance_rate_report.md
          retention-days: 90

      - # レポートをブランチにコミット（オプション）
        name: Commit Report
        if: github.ref == 'refs/heads/main'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .audit/output/acceptance_rate_report.md
          git commit -m "chore: update acceptance rate report" || exit 0
          git push
\`\`\`

### 3. パイロット導入のセットアップ

パイロット導入のためのドキュメントを作成します。

#### 新規ドキュメント: `docs/pilot_adoption_guide.md`

\`\`\`markdown
# Pilot Adoption Guide

AI Actionsのパイロット導入の手引きです。

## 対象

- Self-hosted Runnerを運用しているリポジトリ
- 活発にPRが作成されているリポジトリ（週5件以上）

## 手順

### 1. review-and-merge Actionの導入

\`examples/review-and-merge-example.yml\` を参照して、ワークフローを追加してください。

### 2. カスタムルールの作成（オプション）

プロジェクト固有のコーディング規約がある場合は、カスタムルールを作成してください。

詳細は \`instructions/review-and-merge-custom-rules.md\` を参照してください。

### 3. メトリクス収集の開始

導入後、1週間程度でデータが蓄積されます。

\`\`\`bash
# 受入率レポートの生成
python scripts/calculate_acceptance_rate.py --output report.md --time-period 7d
\`\`\`

### 4. フィードバックの収集

以下の情報を記録してください:

- AIレビューの提案数
- 人間によるレビュー結果（approved/modified/rejected）
- 実行時間
- 開発者のフィードバック

## 成功基準

- AIレビューの受入率が70%以上であること
- 開発者がAIレビューを有用と感じていること
- 実行時間が30分以内であること

## 次のステップ

パイロット導入の結果を \`ADOPTION_GUIDE.md\` に反映してください。
\`\`\`

---

## Success Criteria

- [ ] メトリクス収集ワークフローが動作している
- [ ] 週次レポートが自動生成されている
- [ ] パイロット導入ガイドが作成されている
- [ ] 少なくとも1つのリポジトリでパイロット導入が開始されている

---

## Rollback Plan

問題がある場合は、ワークフローを無効化してください。

\`\`\`bash
gh workflow disable collect-metrics.yml
gh workflow disable generate-quality-report.yml
\`\`\`

---

## Related Issues

- Gap ID: GAP-001, GAP-004
- Issue: ISS-001
- Assumption: ASM-002
