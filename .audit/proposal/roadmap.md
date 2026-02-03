# Improvement Roadmap
version: "2.0"
generated_at: "2026-02-04T02:20:00Z"
generated_by: "audit-run-001"

## Overview

このロードマップは、Repo Genesis Auditの結果に基づき、github-actions-actionsリポジトリの改善を段階的に実行するための計画です。

## Priority Matrix

```
High Impact + Low Effort  → Phase 1 (Quick Wins)
High Impact + High Effort → Phase 2 (Strategic)
Low Impact + Low Effort   → Phase 3 (Maintenance)
Low Impact + High Effort  → Deprioritize
```

## Phase 1: Quick Wins (1-2 weeks)

### Goal
運用メトリクスの可視化と低コストな改善で即座に価値を提供する

### Actions

#### 1. テレメトリーダッシュボード作成
- **Issue**: ISS-005 (Action使用状況の可視化不足)
- **Effort**: Low (2-3日)
- **Impact**: Medium (運用上の意思決定が可能になる)
- **Proposed by**: PR-001

#### 2. 受入率レポート自動化
- **Issue**: ISS-003 (受入率実測値が不明)
- **Effort**: Low (1-2日)
- **Impact**: Medium (品質目標の達成状況を可視化)
- **Proposed by**: PR-002

#### 3. 導入リポジトリ追跡システム
- **Issue**: ISS-004 (導入状況の追跡不足)
- **Effort**: Low (1日)
- **Impact**: Medium (成功条件の評価が可能に)
- **Proposed by**: PR-003

## Phase 2: Strategic Investments (2-4 weeks)

### Goal
技術的債務を解消し、長期的な品質基盤を構築する

### Actions

#### 1. テストカバレッジ改善（70%達成）
- **Issue**: ISS-001 (カバレッジ23.06% → 70%)
- **Effort**: High (2-3週間)
- **Impact**: High (pytestがパスする、回帰リスク低減)
- **Proposed by**: PR-004

#### 2. テンプレート標準完全準拠
- **Issue**: ISS-002 (6/13 Actionsにtemplates/不足)
- **Effort**: Medium (1週間)
- **Impact**: High (メンテナンス性向上、カスタマイズ性向上)
- **Proposed by**: PR-005

## Phase 3: Future Enhancements (1-2 months)

### Goal
機能検証と高度な品質保証を実装する

### Actions

#### 1. Runtime Testing実装
- **Issue**: ISS-006 (機能検証未実装)
- **Effort**: High (1-2ヶ月)
- **Impact**: Medium (実行時のバグ検出)
- **Proposed by**: PR-006

#### 2. E2E Testing with act
- **Issue**: ISS-006拡張
- **Effort**: High (2週間)
- **Impact**: Medium (GitHub Actions Runtimeシミュレーション)
- **Proposed by**: PR-007

## Execution Timeline

```
Week 1-2:  Phase 1 (Quick Wins)
Week 3-6:  Phase 2 (Strategic)  
Week 7-10: Phase 3 (Future)
```

## Risk Management

### High Risk Items
1. **テストカバレッジ70%達成** (PR-004)
   - Risk: 既存テストのリファクタリングが必要な可能性
   - Mitigation: テスト可能なコードから優先的に追加

2. **テンプレート移行** (PR-005)
   - Risk: Actionのロジック変更が必要な可能性
   - Mitigation: 各Actionごとに慎重にテスト実施

## Success Criteria

各Phase完了時に以下を確認：

### Phase 1
- [ ] テレメトリーダッシュボードが閲覧可能
- [ ] 受入率レポートが自動生成される
- [ ] 導入リポジトリ数が追跡可能

### Phase 2
- [ ] pytest --covがパスする（>= 70%）
- [ ] 全Action（13/13）がtemplates/を持つ

### Phase 3
- [ ] actで全Actionを実行可能
- [ ] E2Eテストがパスする

## Dependencies

```
PR-004 (Coverage) → 必須前提条件なし
PR-005 (Templates) → 必須前提条件なし
PR-001〜003 → 必須前提条件なし
PR-006〜007 → PR-004完了推奨（テスト基盤整備済みのため）
```

## Resource Requirements

### Human Resources
- Phase 1: 1開発者 × 2週間
- Phase 2: 1-2開発者 × 4週間
- Phase 3: 1開発者 × 2ヶ月

### Infrastructure
- テレメトリーデータストレージ (既存)
- actツールのインストール (Phase 3)
- テスト用GitHubリポジトリ (Phase 3, オプション)

## Rollback Plan

各PRにはロールバック手順を含める：
- PR-001〜003: ダッシュボード/レポートを削除
- PR-004: テストファイルを削除
- PR-005: 元のaction.ymlに戻す（git revert）
- PR-006〜007: 新規テストファイルを削除
