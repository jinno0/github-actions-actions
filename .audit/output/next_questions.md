# 確認事項と仮定の報告

対話ができないため、以下の仮定に基づいて監査を完了させました。
認識が異なる場合は `intent.yml` を修正してください。

---

## 適用した仮定

| ID | 項目 | 仮定した値 | 根拠 | 信頼度 |
|----|------|------------|------|--------|
| ASM-001 | ターゲットユーザー | GitHub Organizationを使用する企業や組織 | SYSTEM_CONSTITUTION.mdで「組織全体のGitHub Actions」に明記 | high |
| ASM-002 | 実行環境 | Self-hosted runnerを運用している環境 | README.mdで「Self-hosted runner上で動作するClaude Code CLI」を前提 | high |
| ASM-003 | テストカバレッジ | 92.99% (目標70%を達成) | coverage.jsonとpytest --covの両方が92.99%を報告。ISS-NEW-004解決済み | high |
| ASM-004 | AIレビュー受入率 | >= 70% (ただしレビューデータが0件のため未測定) | README.mdに目標値記載。ただしreview_metrics.jsonが存在せず、測定不能 | low (status: not_measurable) |
| ASM-005 | デプロイ形式 | Composite Actionsのみ | SYSTEM_CONSTITUTION.mdで「非Composite Action（Docker/JavaScript）は含まない」と明記 | high |
| ASM-006 | 採用実績 | **不明**（ADOPTION.mdのパイロットプロジェクトはプレースホルダー） | README.mdに「Current adopters: 2」と記載されているが、Executor feedbackによりプレースホルダーであることが判明 | high (status: rejected) |

---

## Critical: 仮定の否定と人間の入力が必要な事項

以下の仮定が**否定された**、または**人間の入力なしには解決不可能**です。

### ASM-006: 採用実績について (Rejected)

**仮定**: 「現在2件のパイロットプロジェクトで導入済み」  
**実際の状態**: ADOPTION.mdの記載はプレースホルダー (example/repo-1, example/repo-2)  
**ステータス**: ❌ **Rejected**

**原因**:
- README.mdには「Current adopters: 2」と記載されている
- しかし、ADOPTION.mdを確認すると、example/repo-1, example/repo-2 がプレースホルダーとして記載されている
- Executor feedback (2026-02-07T09:46:22Z) により、実際のパイロットプロジェクトが不明であることが確認された

**人間の入力が必要です**:

1. **実際のパイロットプロジェクトのリポジトリURLを提供してください**
   - 組織内で実際にこれらのAI Actionsを使用しているリポジトリは何ですか？
   - または、パイロットプロジェクトはまだ存在しないのでしょうか？

2. **パイロットプロジェクトの担当チームと連絡先**
   - 誰がこれらのActionsを使用していますか？
   - フィードバック収集の連絡先は誰ですか？

3. **採用開始日**
   - いつからパイロット運用を開始しましたか？

**推奨されるアクション**:

- **Option A**: 実際のパイロットプロジェクト情報を提供し、ADOPTION.mdを更新する
- **Option B**: パイロットプロジェクトがまだ存在しない場合、README.mdから「Current adopters: 2」の記載を削除し、「Seeking Pilot Projects」に変更する

---

## 質問（次回の精度向上のため）

### Critical (Human Input Required)

- [ ] **Q1**: 実際のパイロットプロジェクトは存在しますか？
  - はい → リポジトリURL、担当チーム、連絡先、採用開始日を提供してください
  - いいえ → README.mdとADOPTION.mdから「Current adopters: 2」の記載を削除してください

- [ ] **Q2**: review-and-merge Actionは実際にパイロットプロジェクトで実行されていますか？
  - はい → ワークフロー実行のURL、または実行履歴のスクリーンショットを提供してください
  - いいえ → どのActionもまだ本番実行されていないことになります

- [ ] **Q3**: review_metrics.jsonファイルを作成する計画はありますか？
  - REVIEW_METRICS_FILE環境変数の設定が必要です
  - 詳細は `docs/data_collection_diagnosis.md` を参照してください

### High Priority

- [ ] **Q4**: README.mdの「Current adopters: 2」記載をどうしますか？
  - 削除しますか？
  - 「Seeking Pilot Projects」に変更しますか？
  - example/repo-1, example/repo-2 を「例示」と明記しますか？

- [ ] **Q5**: 本番環境のOSは何ですか？
  - 今回はLinux (self-hosted runner)と仮定しました
  - macOSやWindows runnerも使用していますか？

- [ ] **Q6**: カスタムレビュールール機能は使用されていますか？
  - instructions/review-and-merge-custom-rules.md に詳細なドキュメントがあります
  - パイロットプロジェクトでカスタムルールは利用されていますか？

### Medium Priority

- [ ] **Q7**: テレメトリー収集は有効化されていますか？
  - DISABLE_TELEMETRY環境変数は設定されていますか？
  - metrics/telemetry/ ディレクトリにデータは保存されていますか？

- [ ] **Q8**: 13個のActionsのうち、最も頻繁に使用されているのはどれですか？
  - 使用頻度のデータはありますか？

- [ ] **Q9**: AIレビューの品質についてフィードバックはありますか？
  - 誤検知（false positive）の例はありますか？
  - 人間による修正頻度はどの程度ですか？

---

## 次回監査での改善予定

次回の監査（2026-02-14またはISS-NEW-002解決時）では、以下を優先的に確認します：

1. **ISS-NEW-002の解決状況**
   - 実際のパイロットプロジェクトが特定されているか
   - ADOPTION.mdが実際の情報で更新されているか

2. **ISS-NEW-001の実行準備**
   - パイロットプロジェクトでレビューデータ収集が有効化されているか
   - REVIEW_METRICS_FILE環境変数が設定されているか

3. **README.mdとの整合性**
   - 「Current adopters」記載がADOPTION.mdと整合しているか
   - 誤解を招く表現が修正されているか

---

## 自律実行の限界について

この監査により、以下の改善アクションは**人間の入力なしには実行不可能**であることが判明しました：

### ❌ 人間の入力が必要なアクション

1. **ISS-NEW-002**: パイロットプロジェクトの特定
   - 組織内のステークホルダーへの連絡が必要
   - リポジトリURL、担当チーム、連絡先の収集が必要

2. **README.mdの修正**: 「Current adopters」記載の削除または変更
   - プロダクトの戦略的意思決定が必要
   - 「採用実績なし」を公表するかどうかの判断が必要

### ✅ 自律的に実行可能なアクション（完了済み）

1. ✅ テストカバレッジの検証: 92.99% (目標70%達成)
2. ✅ Core Function Verification: 13個のActionsが適切に定義されていることを確認
3. ✅ ドキュメントカバー率の検証: 100% (全Actionにinstruction.mdが存在)
4. ✅ GAP-006の解決: テストカバレッジ測定値の不整合を解消

---

**End of Questions**

**Next Audit**: 2026-02-14 or when ISS-NEW-002 is resolved
