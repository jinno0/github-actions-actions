# Improvement Roadmap

## Overview
このロードマップは、`github-actions-actions` リポジトリの監査結果に基づく改善提案を優先順位順に並べたものです。

## Priority Levels

- **P0 (Critical)**: リポジトリの存在意義に関わる問題
- **P1 (High)**: 品質や信頼性に大きな影響を与える問題
- **P2 (Medium)**: 改善の余地があるが、すぐに対処する必要はない問題
- **P3 (Low)**: 文書化や整理レベルの問題

---

## Phase 1: Critical Issues (Week 1)

### ✅ COMPLETED: Documentation Inconsistencies Fix
**PR:** PR-001
**Gap:** GAP-001, GAP-002
**Effort:** 15分
**Status:** ✅ Completed (2026-02-08)

**Completed Actions:**
1. ✅ README.mdのテストカバレッジ目標値を70% → 80%に変更
2. ✅ README.mdのAIレビュー受入率セクションを更新（75.0%を反映）
3. ✅ ドキュメントと実際のデータの整合性を確保

**Results:**
- README.mdとpyproject.tomlの目標値が一致（80%）
- AIレビュー受入率の実測値が正しく反映（75.0%, 3/4件）

---

### ✅ COMPLETED: Core Function Verification
**PR:** PR-002
**Gap:** GAP-003, GAP-008
**Effort:** 1時間45分
**Status:** ✅ Completed (2026-02-08)

**Completed Actions:**
1. ✅ 全13個のActionでDry Run検証の実装状況を確認
2. ✅ Claude Code CLI統合の状況を確認
3. ✅ 検証スクリプトを作成し実行

**Results:**
- Dry Run検証: 3/13 Actionsのみ実装済み（pr-review-enqueuer, bulk-rebase-prs, bulk-merge-prs）
- Claude CLI統合: 7/13 Actionsが統合済み
- 10個のActionsでDry Run検証が未実装であることが判明

---

## Phase 2: Critical Resolution (Week 1-2)

### P0: Dry Run Verification Implementation
**PR:** PR-003
**Gap:** GAP-003
**Effort:** 2-3日 (Option 1) / 15分 (Option 2)
**Status:** 🔄 Proposed

**Actions:**
1. **Option 1 (Recommended)**: 未実装の10個のActionにDry Run検証を追加
   - action-fixer, review-and-merge, spec-to-code, auto-document, release-notes-ai
   - auto-rebase, review-auto-merge, auto-merge, auto-refactor, publish-pr
   - 各action.ymlにdry-run入力を追加
   - 各entrypoint.shにdry-runロジックを実装
2. **Option 2 (Quick Fix)**: README.mdの記載を「一部のAction（3/13）で実装」に修正

**Success Criteria:**
- Option 1: 全13個のActionsがDry Run検証をサポート
- Option 2: ドキュメントと実態が整合

**Dependencies:** なし

**Decision Required:** Option 1 (実装追加) または Option 2 (ドキュメント修正)

---

## Phase 3: High Priority Items (Week 2-3)

### P1: Claude CLI Integration Investigation
**PR:** PR-004
**Gap:** GAP-004
**Effort:** 2-3時間調査 + 1時間ドキュメント
**Status:** 🔄 Proposed

**Actions:**
1. Claude CLI統合がない6つのActionsの用途を調査
   - pr-review-enqueuer, bulk-rebase-prs, bulk-merge-prs, auto-merge, review-auto-merge, publish-pr
2. なぜこれらがClaude Codeを利用しない理由を文書化
3. docs/claude-cli-integration-status.mdを作成
4. 必要に応じてREADME.mdを更新

**Success Criteria:**
- 6つのActionsの用途とClaude CLI未使用の理由が明確
- ドキュメントが作成されている
- README.mdの記載が実態と整合

**Dependencies:** なし

---

### P2: Remaining Core Functions Verification
**PR:** PR-005
**Gap:** GAP-006
**Effort:** 3-4時間
**Status:** 🔄 Proposed

**Actions:**
1. CF-003 (カスタムレビュールール注入機能) の検証シナリオを作成
2. CF-006 (AIレビュー品質メトリクス追跡) の検証シナリオを作成
3. 検証スクリプトを実装し実行
4. 結果をintent.ymlに反映

**Success Criteria:**
- CF-003, CF-006の検証が完了
- 全6つのCore Functionsが検証済み

**Dependencies:** なし

---

## Phase 4: Medium Priority Items (Week 3-4)

### P2: AI Review Data Collection Enhancement
**Gap:** GAP-005
**Effort:** 継続的
**Status:** 🔄 Ongoing

**Actions:**
1. 継続的なAIレビューデータの収集
2. 目標: 20件以上のデータ収集（現状: 4/20件, 20%）
3. 統計的に有意なベースライン値の確立

**Success Criteria:**
- 20件以上のレビューデータが収集されている
- ベースライン値が安定している

**Dependencies:** なし

---

### P2: Adoption Status Investigation
**Gap:** GAP-007
**Effort:** 1-2時間
**Status:** 📋 Pending

**Actions:**
1. ADOPTION.mdファイルの確認
2. GitHub APIによるOrganization内リポジトリのスキャン
3. 導入数の調査と報告

**Success Criteria:**
- 実際の導入数が把握できている
- ミッション達成度が測定可能

**Dependencies:** なし

---

## Phase 5: Continuous Improvement (Week 4+)

### P3: Non-Goals Clarification
**Gap:** (legacy)
**Effort:** 1時間
**Status:** 📋 Pending

**Actions:**
1. 非目標の判断基準を明確化
2. 具体的な例を追加
3. チーム内で合意を形成

**Success Criteria:**
- 非目標の境界条件が明確になっている
- ドキュメントに反映されている

**Dependencies:** なし

---

## Summary Table

| PR | Gap | Priority | Phase | Effort | Status | Dependencies |
|----|-----|----------|-------|--------|--------|--------------|
| PR-001 | GAP-001, GAP-002 | P1 | Phase 1 | 15分 | ✅ Completed | なし |
| PR-002 | GAP-003, GAP-008 | P0 | Phase 1 | 1時間45分 | ✅ Completed | なし |
| PR-003 | GAP-003 | P0 | Phase 2 | 2-3日/15分 | 🔄 Proposed | なし |
| PR-004 | GAP-004 | P1 | Phase 3 | 3-4時間 | 🔄 Proposed | なし |
| PR-005 | GAP-006 | P2 | Phase 3 | 3-4時間 | 🔄 Proposed | なし |
| - | GAP-005 | P2 | Phase 4 | 継続的 | 🔄 Ongoing | なし |
| - | GAP-007 | P2 | Phase 4 | 1-2時間 | 📋 Pending | なし |
| - | (legacy) | P3 | Phase 5 | 1時間 | 📋 Pending | なし |

**Total Estimated Effort:** ~3-5日 (PR-003のOptionによる)

---

## Progress Tracking

### Completed (2 PRs)
- ✅ PR-001: Documentation inconsistencies fix
- ✅ PR-002: Core function verification

### Proposed (3 PRs)
- 🔄 PR-003: Dry Run verification implementation
- 🔄 PR-004: Claude CLI integration investigation
- 🔄 PR-005: Remaining core functions verification

### Ongoing Tasks
- 🔄 GAP-005: AI review data collection (4/20件)

---

## Success Metrics

### Short-term (1 month)
- [x] ドキュメントの不一致が解消されている (PR-001)
- [x] Core Functionsの検証が実施されている (PR-002)
- [ ] Dry Run検証の実装不足が解消されている (PR-003)
- [ ] Claude CLI統合の整合性が確保されている (PR-004)
- [ ] 全てのCore Functionsが検証されている (PR-005)

### Medium-term (3 months)
- [ ] AIレビューデータが20件以上収集されている (GAP-005)
- [ ] 導入プロジェクト数が把握されている (GAP-007)
- [ ] AIレビュー受入率が70%以上で安定している

### Long-term (6 months)
- [ ] 組織内の複数リポジトリで採用されている（成功条件達成）
- [ ] AI Actionsが開発業務の標準ツールとして定着している
- [ ] 継続的な改善が行われている

---

## Next Steps

### Immediate Actions (This Week)
1. **Decision Required**: PR-003の対応方針を決定
   - Option 1: Dry Run検証を10個のActionsに実装（推奨、2-3日）
   - Option 2: README.mdを修正（15分）

2. **Investigation**: PR-004の調査を実施
   - 6つのActionsの用途を調査
   - Claude CLI未使用の理由を文書化

### Short-term Actions (Next 2 Weeks)
3. **Verification**: PR-005を実施
   - CF-003, CF-006の検証シナリオを作成
   - 検証スクリプトを実行

4. **Data Collection**: AIレビューデータの収集を継続
   - 目標: 20件以上

### Medium-term Actions (Next Month)
5. **Adoption Survey**: 導入数の調査を実施
   - ADOPTION.mdの確認
   - Organization内リポジトリのスキャン

---

**Last Updated:** 2026-02-08T19:35:00Z
**Audit Run:** 2026-02-08T19:35:00Z
**Overall Status:** 2/5 PRs completed, 3/5 PRs proposed
