# PR-001: テストカバレッジ70%達成に向けた改善

**優先度**: Critical (P0)
**目標カバレッジ**: 21.29% → 70% (+48.71%)
**見積もりの作業規模**: Medium (2-3週間)

## 背景

**※この提案はASM-002（目標カバレッジ70%）という仮定に基づいています**

- pytest.iniで`--cov-fail-under=70`が設定されているが、現在のカバレッジは21.29%
- CIがカバレッジチェックで失敗し続けている状態
- 301個のテストケースは存在するが、各テストが狭い範囲のみをカバーしている
- 最もカバレッジが低いファイル: test_review_action.py (20%), test_spec_to_code_action.py (20%)

## 提案する改善アクション

### Phase 1: カバレッジ不足モジュールの特定と優先順位付け (2-3日)

**目的**: 限られたリソースで最大のカバレッジ向上を実現

```bash
# coverage.jsonから最もカバレッジが低いファイルtop10を抽出
python scripts/identify_low_coverage_files.py --threshold 30 --top 10

# 出力例:
# 1. tests/test_review_and_merge/test_review_action.py: 20% (+127 lines uncovered)
# 2. tests/test_spec_to_code/test_spec_to_code_action.py: 20% (+111 lines uncovered)
# 3. tests/test_generate_telemetry_report.py: 22% (+96 lines uncovered)
```

**期待される効果**: カバレッジ向上の「ボトルネック」を視覚化

### Phase 2: 統合テストの強化 (1週間)

**目的**: 実際のワークフロー実行パスをカバーし、エンドツーエンドでのカバレッジを向上

現在の問題点:
- 各テストが個々の関数やメソッドを単体でテストしている
- モックやフィクスチャが過度に使用され、実際のコードパスを通っていない

改善アクション:
1. 各Actionについて、実際のGitHub Actionsワークフロー実行をシミュレートする統合テストを追加
2. モックを最小限にし、実際のファイルシステム操作やプロセス実行をテスト

例:
```python
# tests/integration/test_review_and_merge_integration.py
def test_review_and_merge_full_workflow():
    """
    review-and-merge Actionの完全なワークフローをテスト
    1. PRの作成
    2. Claude Code CLIによるレビュー実行
    3. レビューコメントの投稿
    4. 条件を満たす場合の自動マージ
    """
    # 実際のaction.ymlを使用してテスト
    # ...
```

**期待される効果**: +15-25%カバレッジ向上

### Phase 3: エッジケーステストの追加 (3-5日)

**目的**: エラー処理、例外パス、境界値テストを追加

改善アクション:
1. 各Actionについて、以下のエッジケースをテスト:
   - 空入力、null入力
   - 不正なYAML構文
   - ネットワークエラー
   - ファイルシステムエラー
   - Claude CLI実行失敗

2. パラメータの境界値テスト:
   - 最大サイズのPR
   - 最大数のファイル
   - 特殊文字を含む入力

例:
```python
# tests/test_review_and_merge/test_edge_cases.py
def test_review_with_empty_diff():
    """差分が空のPRに対するレビュー"""

def test_review_with_malformed_yaml():
    """不正なYAMLを含むPRに対するレビュー"""

def test_review_with_cli_timeout():
    """Claude CLIがタイムアウトした場合のハンドリング"""
```

**期待される効果**: +10-15%カバレッジ向上

### Phase 4: テストリファクタリングとメンテナンス性向上 (2-3日)

**目的**: テストコードの重複を排除し、メンテナンス性を向上

改善アクション:
1. 共通フィクスチャの抽出 (conftest.pyの拡充)
2. テストヘルパー関数の作成
3. テストデータの共通化

**期待される効果**: テストの追加・修正が容易になり、将来的なカバレッジ維持に寄与

## 実装計画

### Week 1: Phase 1 + Phase 2の一部
- [ ] 低カバレッジファイルの特定
- [ ] 最も影響の大きいAction（review-and-merge, spec-to-code）の統合テスト追加

### Week 2: Phase 2の残り + Phase 3の一部
- [ ] 残りのActionの統合テスト追加
- [ ] エッジケーステストの追加（優先度の高いActionから）

### Week 3: Phase 3の残り + Phase 4
- [ ] 全Actionのエッジケーステスト完了
- [ ] テストリファクタリング
- [ ] 最終的なカバレッジ検証

## 成功基準

- [ ] pytest実行時のカバレッジが70%以上
- [ ] `python -m pytest --cov=. --cov-fail-under=70` が成功すること
- [ ] 全ての既存テストが依然としてパスすること（回帰なし）

## リスクと副作用

### リスク
- **テスト実行時間の増加**: 統合テスト追加により実行時間が2-3倍になる可能性
  - **緩和策**: pytestのマーカーを使用し、CIでは統合テストを並列実行

### 副作用
- **メンテナンスコストの増加**: テストコードの行数が増加
  - **許容範囲**: メンテナンス性向上（Phase 4）で相殺

## ロールバック計画

もし改善により既存機能が壊れた場合:
1. Gitで改善前の状態に戻す: `git revert <commit-hash>`
2. カバレッジ目標を一時的に50%に引き下げ（pytest.ini修正）

## 次のアクション

1. この提案をレビューし、Phase 1から開始することを承認
2. カバレッジ状況の可視化スクリプト（identify_low_coverage_files.py）を作成
3. 低カバレッジファイルtop10をチーム全体で共有し、改善の優先順位を合意

## 参考資料

- GAP-001: カバレッジ不足の詳細分析
- SOL-001-1〜3: 具体的なソリューション案
- .audit/analysis/as_is.yml: 現状のカバレッジデータ
