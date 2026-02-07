# Improvement Roadmap

**Generated:** 2026-02-07
**Target:** Test Coverage >= 80%, Core Functions Verified

## Overview

このロードマップは、`github-actions-actions` リポジトリの品質向上のために実施すべき改善を優先度順に示しています。

## Current State

- テストカバレッジ: 未測定
- Lintチェック: 未実施
- 動作検証: 手動
- ドキュメント整備: ✓ 完了

## Improvement Plan

### Phase 1: Quality Foundation (必須)

#### PR-001: Test Coverage Framework Setup
- **Priority:** High
- **Impact:** High
- **Risk:** Low
- **Estimated Time:** 30 min
- **Dependencies:** None

テストカバレッジの測定基盤を整える。

**Expected Outcome:**
- pytest-cov が導入される
- カバレッジレポートが自動生成される
- CIでカバレッジが可視化される

#### PR-002: Lint Framework Setup
- **Priority:** Medium
- **Impact:** Medium
- **Risk:** Low
- **Estimated Time:** 20 min
- **Dependencies:** None

Lintチェックの基盤を整える。

**Expected Outcome:**
- ruff が導入される
- pre-commit hook で自動チェックされる
- CIで品質ゲートが機能する

#### PR-003: Core Functions Verification Script
- **Priority:** High
- **Impact:** High
- **Risk:** Medium
- **Estimated Time:** 60 min
- **Dependencies:** PR-001

本質的機能の動作検証を自動化する。

**Expected Outcome:**
- 全Actionの検証スクリプトが作成される
- CIで自動検証が実行される
- 回帰テストが可能になる

### Phase 2: Quality Enhancement (将来実施)

- 型チェック (mypy) の導入
- 各Actionのユニットテスト追加
- 統合テストの追加
- パフォーマンス検証

### Phase 3: Automation & Documentation (将来実施)

- auto-document Actionの活用
- テストカバレッジ 80% 達成
- CI/CDパイプラインの最適化

## Execution Order

1. **PR-001** → カバレッジ測定基盤整備
2. **PR-002** → Lintチェック基盤整備 (PR-001と並列実行可)
3. **PR-003** → 動作検証スクリプト作成 (PR-001完了後)

## Success Criteria

- [ ] テストカバレッジが測定できている
- [ ] Lintエラーが 0 件
- [ ] 全Actionの動作検証が自動化されている
- [ ] CIで全チェックがパスする

## Estimated Total Time

**Phase 1 合計:** 約 2 時間 (並列実行時は約 1.5 時間)

## Next Steps

1. PR-001, PR-002, PR-003 を適用
2. テストカバレッジの現状を測定
3. カバレッジ 80% に向けたテスト追加計画を策定
