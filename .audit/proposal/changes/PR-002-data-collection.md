# PR-002: AI Review Data Collection Setup

**Priority**: P0 (Critical)
**Gap Addressed**: GAP-001 (AIレビュー品質データの欠如)
**Estimated Effort**: 1-2 weeks
**Risk Level**: Low

---

## Summary

このPRは、AIレビューの品質メトリクス（受入率）を測定するためのデータ収集プロセスを確立する。

**目的**: `metrics/review_metrics.json` を生成し、AIレビュー受入率のベースライン値を算出する。

---

## Background

### Current Situation
- README.md:176 で「AIレビュー受入率 >= 70%」と目標設定
- **しかし**、`metrics/review_metrics.json` が存在しない（C-006）
- 受入率を計測できない（README.md:174-191）

### Why This Matters
- プロジェクトの**核心的品質指標**が測定できない
- AIの提案品質を評価できない
- 改善サイクルを回せない

### Dependencies
- **PR-001** が完了していること（パイロットプロジェクトが必要）

---

## Proposed Changes

### 1. acceptance_tracker.py の動作確認と修正

**File**: `actions/lib/acceptance_tracker.py`

**Issue**:
- カバレッジ88.89%で、一部のロジックが未検証
- Missing lines: [95, 108, 155-157, 196-197, 251-253]

**Action**:
1. 未カバレッジ部分のコードレビュー
2. バグがあれば修正
3. モックデータを使用したテスト追加

### 2. review_metrics.json 生成のテスト

**Script**: `scripts/test_data_collection.py`

```python
#!/usr/bin/env python3
"""
テスト用のレビューデータ収集スクリプト
"""
import json
from pathlib import Path

def generate_test_metrics():
    """テスト用のレビューメトリクスを生成"""

    test_data = {
        "version": "1.0",
        "collection_period": {
            "start": "2026-02-08T00:00:00Z",
            "end": "2026-02-08T23:59:59Z"
        },
        "reviews": [
            {
                "pr_number": 1,
                "repo_id": "test-repo",
                "outcome": "approved",
                "suggestions_count": 3,
                "accepted_suggestions": 2,
                "timestamp": "2026-02-08T12:00:00Z"
            },
            {
                "pr_number": 2,
                "repo_id": "test-repo",
                "outcome": "modified",
                "suggestions_count": 5,
                "accepted_suggestions": 3,
                "timestamp": "2026-02-08T13:00:00Z"
            }
        ]
    }

    output_path = Path("metrics/review_metrics.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(test_data, indent=2))

    print(f"✅ Test metrics generated: {output_path}")

if __name__ == "__main__":
    generate_test_metrics()
```

### 3. calculate_acceptance_rate.py の実行テスト

**Command**:
```bash
python scripts/calculate_acceptance_rate.py \
  --time-period 7d \
  --output report \
  --baseline
```

**Expected Output**:
```
=== AI Review Acceptance Rate Report ===
Collection Period: 2026-02-01 ~ 2026-02-08

Total Reviews: 0
Acceptance Rate: N/A (insufficient data)

Status: ⚠️ Data collection in progress
Minimum required: 20 reviews
Current: 0 reviews
```

### 4. CIへのデータ収集チェック追加

**Workflow**: `.github/workflows/check-data-collection.yml`

```yaml
name: Check Data Collection

on:
  schedule:
    - cron: '0 9 * * 1'  # 毎週月曜9時
  workflow_dispatch:

jobs:
  check-data:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Check review metrics
        run: |
          if [ ! -f metrics/review_metrics.json ]; then
            echo "⚠️ review_metrics.json not found"
            echo "Data collection has not started yet"
            exit 0  # 失敗させない（パイロット段階）
          fi

          python scripts/calculate_acceptance_rate.py \
            --time-period 7d \
            --output report
```

---

## Success Criteria

- [ ] `actions/lib/acceptance_tracker.py` が正常に動作する
- [ ] `metrics/review_metrics.json` が生成される
- [ ] `calculate_acceptance_rate.py` がエラーなく実行できる
- [ ] CIでデータ収集チェックが動作する

---

## Testing Plan

### Unit Testing
1. モックデータでの `acceptance_tracker.py` テスト
2. エッジケースのテスト（空データ、不正フォーマット）

### Integration Testing
1. パイロットプロジェクトで実際のPRを作成
2. `metrics/review_metrics.json` の生成を確認
3. `calculate_acceptance_rate.py` の実行を確認

**Target**: エラー0件、データ収集成功率100%

### Rollback Plan
データ収集に問題がある場合：
1. acceptance_tracker.py のロールバック
2. エラーログの収集と分析
3. バグ修正後に再実行

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| データ収集が始まらない | Medium | High | PR-001の成功を前提にする |
| メトリクス計算ロジックのバグ | Low | Medium | モックデータで事前検証 |
| プライバシー問題 | Low | Medium | 匿名化処理の確認 |

---

## Implementation Steps

### Step 1: コードレビューとテスト (Day 1-2)
1. `acceptance_tracker.py` の未カバレッジ部分をレビュー
2. モックデータでのテスト追加
3. バグがあれば修正

### Step 2: 生成スクリプトの作成 (Day 3)
1. `test_data_collection.py` の作成
2. ローカルで実行テスト
3. `metrics/review_metrics.json` の生成を確認

### Step 3: CIワークフローの追加 (Day 4)
1. `check-data-collection.yml` の作成
2. CIでの実行テスト
3. スケジュール実行の確認

### Step 4: パイロットでの検証 (Week 2)
1. パイロットプロジェクトでPRを作成
2. データ収集の動作確認
3. 最初のレポート生成

---

## Post-Deployment Actions

### Week 1
1. 毎日のデータ収集確認
2. エラーログの監視
3. 必要に応じて修正

### Week 2-4
1. 週次レポートの生成
2. 受入率の推移を監視
3. 20件のデータが集まり次第、ベースライン値算出

### Month 2
1. ベースラインレポートの公開
2. 目標（>= 70%）との比較
3. 改善アクションの検討

---

## Data Collection Diagnosis

**Known Issue**: `docs/data_collection_diagnosis.md` で診断されている通り、データ収集プロセスに問題がある可能性がある。

**Action**:
1. 診断ドキュメントの詳細確認
2. 問題点の特定
3. 修正プランの作成

---

## Related Issues/PRs

- **Depends on**: PR-001（パイロット導入）
- **Blocks**: PR-003（テレメトリー収集）
- **Related**: GAP-001, GAP-003

---

## Additional Notes

### 仮定（Assumption）
この提案は以下の仮定に基づいている：
- **ASM-003**: AIレビュー受入率 >= 70% という目標
- **C-006**: 現時点でレビューデータが存在しない

### 成功の定義
- 20件以上のレビューデータが収集される
- 受入率のベースライン値が算出できる
- 目標（>= 70%）との比較が可能になる

### 次のアクション
データ収集が成功したら、次は：
1. **PR-003**: テレメトリー収集の有効化
2. **PR-005**: Claude CLI互換性テスト

---

## Approval Checklist

- [ ] PR-001が完了している
- [ ] acceptance_tracker.py のコードレビュー完了
- [ ] テストスクリプトが動作することを確認
- [ ] CIワークフローがレビューされている
