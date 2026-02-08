# Improvement Roadmap

**Generated**: 2026-02-08T17:24:21Z
**Audit Run**: 2026-02-08T17:24:21Z
**Total Gaps**: 5
**Total Proposals**: 2

---

## Priority 1: CRITICAL (High Severity)

### [PR-006] Dry Run検証の実装（残り10 Actions）
**Gap**: GAP-003
**Effort**: 2-3 hours
**Impact**: HIGH - README.mdの主張「全てのAI ActionsはDry Runモードで自動検証される」を実現
**Status**: pending

#### Description
現在3/13 Actions (23%) にのみ実装されているDry Run検証を、残り10 Actionsにも実装する。

#### Implementation Order
1. **Simple (5 Actions)**: `publish-pr`, `auto-merge`, `review-auto-merge`, `auto-document`, `release-notes-ai`
2. **Medium (3 Actions)**: `action-fixer`, `auto-refactor`, `auto-rebase`
3. **Complex (2 Actions)**: `review-and-merge`, `spec-to-code`

#### Success Criteria
- [ ] 13/13 Actionsが `DRY_RUN` inputを持つ
- [ ] `pytest tests/ -k dry_run` が13個パス
- [ ] CF-004のverified_statusが passed になる

#### Related Files
- `.audit/proposal/changes/PR-006.md`

---

## Priority 2: LOW (Medium Severity)

### [PR-009] Test Coverage Decrease Investigation
**Gap**: ISS-MET-001
**Effort**: 15-30 minutes
**Impact**: LOW - 88.31%は目標値80%を超えているが、低下トレンドの調査
**Status**: pending

#### Description
テストカバレッジが92.97%から88.31%へ4.66%低下した原因を調査し、是正が必要か判断する。

#### Investigation Steps
1. `pytest --cov-report=term-missing` で詳細確認
2. 前回レポートと比較
3. 原因分類（テスト変更/コード追加/環境変化/一時的変動）
4. 是正の判断

#### Success Criteria
- [ ] 低下原因が特定されている
- [ ] 是正の有無が判断されている
- [ ] 必要な場合は回復アクション実行
- [ ] `.audit/analysis/gap.yml` の ISS-MET-001 が更新されている

#### Related Files
- `.audit/proposal/changes/PR-009.md`

---

## Priority 3: LOW (Low Severity - Ongoing)

### AIレビュー受入率のデータ収集継続
**Gap**: GAP-005
**Effort**: Ongoing
**Impact**: MEDIUM - ベースライン策定には20件以上のデータが必要
**Status**: in_progress (4/20件収集完了)

#### Description
AIレビュー受入率の品質メトリクス測定のため、20件以上のレビューデータ収集を継続する。

#### Current Status
- **Current**: 75.0% (3/4件 approved or modified)
- **Target**: >= 70%
- **Data Points**: 4/20 (20%)
- **Status**: achieved but insufficient data

#### Action
- 継続的なデータ収集
- 20件到達後、統計的に有意なベースライン値を算出
- README.mdのベースラインレポートを更新

#### Success Criteria
- [ ] 20件以上のレビューデータ収集
- [ ] ベースライン値の信頼区間を算出
- [ ] README.mdの「現在のベースライン」セクションを更新

---

## Priority 4: LOW (Low Severity - Optional)

### 導入数の把握
**Gap**: GAP-007
**Effort**: 1-2 hours
**Impact**: LOW - 採用状況の可視化
**Status**: pending

#### Description
実際の導入リポジトリ数を把握する。

#### Proposed Actions
1. ADOPTION.md の確認
2. GitHub APIを使用したリポジトリスキャン（ワークフロー使用状況）
3. 導入リポジトリの記録

#### Success Criteria
- [ ] 導入リポジトリ数を把握
- [ ] ADOPTION.mdを更新

---

## Priority 5: LOW (Low Severity - Investigation)

### Acceptance Rate Data Discrepancy Investigation
**Gap**: ISS-MET-002
**Effort**: 15 minutes
**Impact**: LOW - データ整合性の確認
**Status**: pending

#### Description
前回サイクルの feedback_to_auditor.yml と現在の metrics/review_metrics.json のデータ不一致を調査。

#### Discrepancy
- **Feedback reported**: 10 data points, 90% acceptance rate
- **Metrics file shows**: 4 data points, 75% acceptance rate
- **Difference**: 6 data points

#### Investigation Questions
1. feedback_to_auditor.yml の 90% は計算ミスか？
2. 実際の review_metrics.json のエントリ数は？
3. acceptance_rate の計算ロジックは正しいか？

#### Success Criteria
- [ ] 不一致の原因が特定されている
- [ ] 正しい値が意昧されている
- [ ] 必要に応じて計算ロジックを修正

---

## Summary Statistics

| Priority | Gap | Proposal | Effort | Status |
|----------|-----|----------|--------|--------|
| 1 | GAP-003 | PR-006 | 2-3 hours | pending |
| 2 | ISS-MET-001 | PR-009 | 15-30 min | pending |
| 3 | GAP-005 | Ongoing | Ongoing | in_progress |
| 4 | GAP-007 | Future | 1-2 hours | pending |
| 5 | ISS-MET-002 | Investigation | 15 min | pending |

**Total Implementation Effort**: 3.5-6 hours (excluding ongoing data collection)

---

## Next Actions (Recommended Order)

1. **Immediate**: PR-009の実行（15-30分）
   - カバレッジ低下の調査
   - 是正アクションの判断

2. **Short-term**: PR-006の実行（2-3時間）
   - Dry Run検証の実装
   - CF-004の達成

3. **Ongoing**: GAP-005のデータ収集継続
   - 20件到達まで継続
   - ベースライン値の策定

4. **Optional**: GAP-007, ISS-MET-002の調査
   - 低優先度のため、余裕があれば実施

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PR-006実装時に既存ワークフローへ影響 | Medium | Medium | `default: "false"` で既定動作を維持 |
| カバレッジ回復に時間がかかる | Low | Low | 88.31%は目標値80%を超えている |
| データ収集が遅延する | Medium | Low | 20件は数週間で達成可能 |

---

## Success Metrics

### Short-term (1 week)
- [ ] PR-009完了（カバレッジ調査）
- [ ] PR-006開始（Dry Run実装）

### Medium-term (2-4 weeks)
- [ ] PR-006完了（13/13 ActionsにDry Run実装）
- [ ] CF-004達成（Dry Run検証100%）
- [ ] GAP-003 resolved

### Long-term (1-2 months)
- [ ] GAP-005達成（20件のレビューデータ収集）
- [ ] ベースライン値の策定とREADME更新

---

## Notes

- PR-006は最大の課題（GAP-003）への対応であり、最も優先度が高い
- PR-009は軽微な調査タスクであり、すぐに実行可能
- GAP-005は継続的な活動であり、特定のPRを必要としない
- GAP-007とISS-MET-002は低優先度であり、他の課題解決後でよい
