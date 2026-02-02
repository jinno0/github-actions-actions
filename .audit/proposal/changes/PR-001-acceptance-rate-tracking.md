# PR-001: Implement Acceptance Rate Tracking System

**Priority:** Critical (GAP-001)
**Effort:** Medium
**Impact:** High

## Summary

PURPOSE.mdで定義されている成功条件「AIの提案に対する修正率（Acceptance Rate）が向上し続ける」を測定するための仕組みを実装する。

現在、AIが生成したコード変更や提案が実際に採用されたかどうかを追跡する仕組みがなく、AIの品質改善サイクルを回せていない。

## Problem Statement

### Current Situation
- PURPOSE.md:71でAcceptance Rateの継続的向上が成功条件として定義されている
- しかし、Acceptance Rateを測定・追跡する実装が存在しない
- AIの提案品質が向上しているかどうかを客観的に証明できない

### Impact
- AIの改善サイクル（PDCA）を回せない
- 投資対効果（ROI）を測定できない
- どのActionが効果的か、どの改善が品質向上に寄与したか不明

## Proposed Solution

### Phase 1: Basic Metrics Collection (本PR)

#### 1.1 メトリクス収集ワークフローの拡張

**File:** `.github/workflows/aggregate-metrics.yml`

```yaml
name: Aggregate Quality Metrics

on:
  schedule:
    - cron: '0 0 * * *'  # 毎日0時に実行
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: read

jobs:
  collect-metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Collect PR metrics
        uses: actions/github-script@v7
        with:
          script: |
            const { data: pulls } = await github.rest.pulls.list({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'closed',
              sort: 'updated',
              direction: 'desc',
              per_page: 100
            });

            const metrics = pulls.map(pr => ({
              number: pr.number,
              title: pr.title,
              merged_at: pr.merged_at,
              created_at: pr.created_at,
              additions: pr.additions,
              deletions: pr.deletions,
              reviews: pr.review_comments,
              ai_reviewed: pr.labels.some(l => l.name === 'ai-reviewed'),
              ai_fixed: pr.labels.some(l => l.name === 'ai-fixed')
            }));

            console.log(JSON.stringify(metrics, null, 2));
```

#### 1.2 review-and-merge Actionの拡張

**File:** `actions/review-and-merge/action.yml`

**変更点:**
- `outputs` に `suggestions_count` を追加
- `outputs` に `suggestions_accepted` を追加（後続の手動追跡用）

```yaml
outputs:
  verdict:
    description: 'Review verdict (LGTM or REQUEST_CHANGES)'
    value: ${{ steps.review.outputs.verdict }}
  confidence:
    description: 'Confidence score (1-10)'
    value: ${{ steps.review.outputs.confidence }}
  suggestions_count:
    description: 'Number of suggestions made by AI'
    value: ${{ steps.review.outputs.suggestions_count }}
```

#### 1.3 メトリクス保存用のディレクトリ構造

```
metrics/
├── acceptance_rate.json       # Acceptance Rateの時系列データ
├── pr_metrics.json           # 個別PRのメトリクス
└── action_metrics.json       # Action別の集計
```

### Phase 2: Automated Acceptance Rate Calculation (Future PR)

**File:** `scripts/calculate-acceptance-rate.py`

- GitHub APIを使用して、review-and-mergeでレビューしたPRの最終状態を追跡
- LGTM vs REQUEST_CHANGESの割合を計算
- AIの提案した修正が実際に採用されたかを追跡

**ロジック:**
1. review-and-mergeが実行されたPRを特定（label: `ai-reviewed`）
2. PRがマージされたか、closed（拒否）されたかを集計
3. `Acceptance Rate = merged / (merged + closed) * 100`

### Phase 3: Dashboard & Visualization (Future PR)

- GitHub Pagesまたは外部ツールでダッシュボードを作成
- Acceptance Rateの推移をグラフ化
- Action別、期間別のドライバン分析

## Implementation Plan

### Step 1: メトリクス収集の基盤整備（本PR）
1. `.github/workflows/aggregate-metrics.yml` を作成
2. review-and-mergeのoutputsを拡張
3. `metrics/` ディレクトリと初期JSONファイルを作成

### Step 2: データ収集の開始（本PR）
1. ワークフローを手動実行し、データが正しく収集されることを確認
2. 1週間ほどデータを蓄積

### Step 3: 自動計算の実装（次回PR）
1. `scripts/calculate-acceptance-rate.py` を実装
2. GitHub API認証の設定（PATまたはApp）
3. 定期実行のスケジュール設定

## Testing Strategy

### Structural Tests
- `tests/test_metrics_collection/` ディレクトリを作成
- `test_aggregate_workflow_exists.py`: aggregate-metrics.ymlが存在すること
- `test_metrics_directory_structure.py`: metrics/ディレクトリが正しい構造であること

### Integration Tests
- モックのGitHub APIレスポンスを使用してテスト
- 実際のself-hosted runnerでテスト（手動実行）

### Manual Testing
1. ワークフローを手動実行
2. `metrics/` ディレクトリにJSONファイルが生成されることを確認
3. JSONの構造が正しいことを確認

## Rollback Plan

- ワークフローの削除：`.github/workflows/aggregate-metrics.yml` を削除
- Actionへの変更：review-and-mergeのoutputs追加のみなので、既存機能に影響しない
- メトリクスファイル：`metrics/` ディレクトリを削除

## Success Criteria

1. ✅ `.github/workflows/aggregate-metrics.yml` が存在し、有効なYAMLである
2. ✅ review-and-merge Actionに `suggestions_count` outputが追加されている
3. ✅ `metrics/` ディレクトリが作成され、初期データファイルが存在
4. ✅ ワークフローを実行すると、PRメトリクスが収集される
5. ✅ 構造的テストがパスする

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| GitHub API rate limit | Medium | キャッシュを実装、取得頻度を調整 |
| PATの管理 | High | GitHub Appを使用、またはsecretsで管理 |
| 誤ったメトリクス定義 | Medium | ステークホルダーと定義を合意 |

## Dependencies

- GitHub API（既に使用済み）
- GitHub Actions（既に使用済み）
- Python 3.x（スクリプト実行用）

## Related Issues

- Closes GAP-001: Acceptance Rate追跡機能の不在
- Addresses PURPOSE.md:71の成功条件

## Notes

- まずはシンプルな収集から始め、徐々に自動化を進める
- プライバシーに配慮し、PRの内容自体は保存しない（メタデータのみ）
- 将来的には、AIモデルのバージョン別、プロジェクト別のドリルダウンも検討

---

**Acceptance Criteria:**
1. メトリクス収集ワークフローが実行可能であること
2. 収集したデータがJSON形式で保存されること
3. 全ての構造的テストがパスすること
4. README.mdにメトリクスについてのセクションが追加されること
