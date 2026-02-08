# PR-002: AIレビュー品質の向上

**Priority:** P0 (Critical)  
**Gap:** GAP-002 (AIレビュー受入率60% < 目標70%)  
**Estimated Effort:** Medium (2-4週)

## 背景

AIレビューの受入率が60%で目標70%未達。サンプル数も10件で統計的に有意ではない（目標20件）。レビュー品質の向上とデータ収集の強化が必要。

## 現状分析

**現在のメトリクス:**
- 受入率: 60% (6/10件)
- 平均提案数: 4.0件
- 平均信頼度スコア: 0.78

**問題推測:**
1. プロンプトの品質が最適化されていない
2. コンテキスト不足（関連ファイルの考慮不足）
3. 提案の粒度が大きすぎる（一度に多数の改善提案）

## 提案する変更

### 1. レビューデータ収集の強化

**ファイル:** `metrics/review_metrics.json` のフォーマット拡張

現在のフィールドに加え、以下を追加:
```json
{
  "rejection_reasons": ["string"],
  "suggestion_categories": ["security", "performance", "style", "logic"],
  "files_touched": 5,
  "lines_changed": 150,
  "review_duration_seconds": 45
}
```

### 2. AIレビュープロンプトの改善

**ファイル:** `actions/review-and-merge/templates/review_prompt.txt` の最適化

**改善点:**
- 提案の優先順位付け（Critical > High > Medium > Low）
- 一度のレビューで最大3つの提案に制限
- 各提案に「なぜ重要か」を明記
- 安全性の提案を優先

**変更例:**
```diff
- コードの問題点を全て列挙してください
+ 優先度順に最大3つの重要な問題を挙げてください
+ それぞれについて、以下を含めてください:
+   - 問題の重要性（なぜ修正が必要か）
+   - 具体的な修正案
+   - 関連するベストプラクティス
```

### 3. レビュー品質ダッシュボードの作成

**ファイル:** 新規 `scripts/generate_review_quality_dashboard.py`

**機能:**
- 受入率の推移グラフ
- 拒否理由の分類と集計
- 提案カテゴリの傾向分析
- 信頼度スコアと受入率の相関

**出力:** `metrics/review_quality_dashboard.md`

```markdown
# AI Review Quality Dashboard

## 受入率推移

| 週 | 受入率 | サンプル数 |
|----|--------|-----------|
| 2026-02-01 | 60% | 10 |
| 2026-02-08 | 65% | 15 |

## 拒否理由トップ5

1. 既に対応済み (40%)
2. 提案が抽象的すぎる (25%)
3. 優先度が低い (20%)
4. 誤検知 (10%)
5. その他 (5%)
```

### 4. A/Bテストフレームワークの実装

**ファイル:** 新規 `actions/review-and-merge/ab_test_config.yml`

```yaml
experiments:
  - name: "limited_suggestions"
    description: "提案数を5個から3個に制限"
    variants:
      - name: "control"
        suggestions_limit: 5
      - name: "treatment"
        suggestions_limit: 3
    metric: "acceptance_rate"
    min_sample_size: 20
```

**実行方法:**
```bash
python scripts/analyze_ab_test.py --experiment limited_suggestions
```

## 期待される効果

- **短期 (2週):** レビューデータが10件 → 20件に増加
- **中期 (4週):** 受入率が60% → 70%以上に改善
- **長期 (8週):** 統計的に有意なベースライン値の策定

## 成功基準

- レビューサンプル数が20件以上
- 受入率が70%以上
- 主要な拒否理由が「既に対応済み」または「優先度の低い」に集約

## リスク

- **プロンプト変更の副作用:** 受入率がさらに低下する可能性
  - 緩和策: A/Bテストで徐々にロールアウト
- **データ収集のコスト:** レビューデータの収集に時間がかかる
  - 緩和策: 複数プロジェクトで同時に収集

## 検証方法

1. プロンプト変更後、A/Bテストを開始
2. 2週間ごとに受入率を測定
3. 拒否理由のトレンドを分析
4. 目標達成後、ベースラインを更新

## 次のアクション

1. review_metrics.jsonのフィールド拡張
2. review_prompt.txtのA/Bテスト準備
3. generate_review_quality_dashboard.pyの実装
4. 複数プロジェクトでのデータ収集開始

---

**依存関係:** PR-003 (組織内導入状況の可視化 - データ収集対象の特定)  
**ブロッカー:** なし  
**関連PR:** PR-001 (採用加速 - より多くのデータ収集源を確保)
