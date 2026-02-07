# PR-001: Pilot Project Adoption Kickoff

**Priority**: P0 (Critical)
**Gap Addressed**: GAP-004 (Phase 3の導入が進んでいない)
**Estimated Effort**: 1-2 weeks
**Risk Level**: Medium

---

## Summary

このPRは、AI Actionsのパイロット導入を開始するための最初のステップである。

**目的**: 2-3件のパイロットプロジェクトを選定し、`review-and-merge` Actionの導入を開始する。

---

## Background

### Current Situation
- ✅ 13個のAI Actionsが実装完了
- ✅ テストカバレッジ92.99%
- ✅ ドキュメント100%カバレッジ
- ❌ 採用事例0件（PURPOSE.md:22-27, ADOPTION.md）

### Why This Matters
技術的完成度は高いが、**実際に使われないと意味がない**。

- AIレビューの品質（受入率 >= 70%）を測定できない
- 実運用でのフィードバックが得られない
- プロジェクトの成功条件を検証できない

### Dependencies
- PR-002が完了するまでは、レビューデータ収集が不完全になる可能性がある

---

## Proposed Changes

### 1. ADOPTION.md の更新
```markdown
## Pilot Projects

### Active Pilots (2026-02-08 ~)

1. **[プロジェクト名A]**
   - Started: 2026-02-15
   - Team: [チーム名]
   - Actions: review-and-merge
   - Status: 🟡 Onboarding
   - Notes: [初期フィードバック]

2. **[プロジェクト名B]**
   - Started: 2026-02-20
   - Team: [チーム名]
   - Actions: review-and-merge, auto-document
   - Status: 🟢 Active
   - Notes: [運用上のノウハウ]
```

### 2. パイロット導入ワークショップ資料の作成
**File**: `docs/pilot-workshop.md`

**内容**:
1. AI Actionsとは？（10分）
2. `review-and-merge` の使い方（20分）
3. 最初のPRでの実演（15分）
4. Q&A（15分）

**目標**: 参加者が「試してみたい」と思うこと

### 3. オンボーディングチェックリストの作成
**File**: `docs/pilot-onboarding-checklist.md`

**項目**:
- [ ] GitHub Actions runnerの設定確認
- [ ] Claude CLIのインストール（`npm install -g @anthropic-ai/claude-code`）
- [ ] `review-and-merge` workflowの設置
- [ ] 最初のPRでのテスト
- [ ] チームメンバーへの共有
- [ ] フィードバックチャネルの設定

---

## Success Criteria

- [ ] 2-3件のパイロットプロジェクトが選定される
- [ ] ADOPTION.md にパイロットプロジェクトが登録される
- [ ] 少なくとも1件で最初のAIレビューが実行される
- [ ] フィードバック収集プロセスが確立される

---

## Testing Plan

### Manual Testing
1. チームメンバー1人でワークショップ資料を試す
2. オンボーディングチェックリストの項目を検証
3. 最初のAIレビュー実行までの所要時間を計測

**Target**: オンボーディング <= 30分

### Rollback Plan
パイロット導入がうまくいかない場合：
1. ワークフローファイルを削除
2. ADOPTION.md からプロジェクトを削除
3. フィードバックを収集し、プロセス改善

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| チームがAIレビューに抵抗感 | Medium | High | Human-in-the-loop設計を強調 |
| Claude CLIインストールでトラブル | Low | Medium | インストールガイドの事前配布 |
| AIレビュー品質が低い | Medium | High | 拒否権は人間にあることを説明 |
| パイロットプロジェクトが見つからない | Low | Critical | チームリーダーへの事前根回し |

---

## Implementation Steps

### Step 1: 準備 (Day 1-2)
1. パイロットプロジェクトの候補リスト作成
   - 条件: 活発な開発、レビューチームがある
   - サイズ: 小〜中規模（5-20人）
2. チームリーダーへの導入提案
3. ワークショップ資料の作成

### Step 2: ワークショップ実施 (Day 3-5)
1. 各プロジェクトでワークショップ（1時間）
2. オンボーディングサポート
3. 最初のAIレビュー実演

### Step 3: フォローアップ (Week 2)
1. フィードバック収集
2. トラブルシューティング
3. ADOPTION.md の更新

---

## Post-Deployment Actions

1. **Week 1**: 毎日のチェックイン（最初の1週間）
2. **Week 2-4**: 週次フィードバック会議
3. **Month 2**: パイロット結果の評価と拡大判断

---

## Related Issues/PRs

- **Depends on**: None
- **Blocks**: PR-002（レビューデータ収集）
- **Related**: GAP-001, GAP-003

---

## Additional Notes

### 仮定（Assumption）
この提案は以下の仮定に基づいている：
- **ASM-001**: ターゲットユーザーは「GitHub組織の開発チーム・DevOpsエンジニア」である
- **C-101**: 実際の運用実績が不足している

### 次のアクション
パイロット導入が成功したら、次は：
1. **PR-002**: レビューデータ収集の開始
2. **PR-003**: テレメトリー収集の有効化
3. **PR-004**: actツール導入

---

## Approval Checklist

- [ ] パイロットプロジェクトが承認されている
- [ ] ワークショップ資料がレビューされている
- [ ] チームリーダーから了承を得ている
- [ ] ADOPTION_GUIDE.md の手順を確認している
