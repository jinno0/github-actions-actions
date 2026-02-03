# PR-001: テレメトリー実装状況の調査と整合性修正

**提出者**: Repo Genesis Auditor (Run #2026-02-03T23:20:15Z)
**優先度**: 高
**種別**: 調査 & 修正
**推定工数**: 小（2-4時間）

---

## 概要

README.md:98-119で詳細に説明されているテレメトリー機能（匿名化、オプトアウト可能）の実装が、実際のコードベースで見つからない問題を調査し、整合性を修正します。

## 問題の背景

### 現状
- **README.md**: テレメトリー機能の詳細な説明が存在（機能概要、プライバシー機能、収集データ、無効化方法）
- **実装コード**: `actions/` ディレクトリ内にテレメトリー関連の実装が見つからない（`grep -r 'telemetry' actions/` で該当なし）
- **不整合**: ドキュメントと実装の間に乖離が存在

### 可能な原因（仮説）
1. **未実装**: READMEが先行して記載され、実装が追いついていない
2. **別の場所で実装**: テレメトリー機能が`github-actions-hub`リポジトリ等で実装されている
3. **機能削除**: 以前実装されていたが、削除された際にREADMEの更新が漏れている
4. **オプション機能**: テレメトリーはオプション機能で、デフォルトでは無効化されている

---

## 提案するアクション

### Phase 1: 実装状況の調査（必須）

#### ステップ 1: 全リポジトリスキャン
```bash
# 全関連リポジトリでテレメトリー実装を検索
cd /home/jinno
find . -name "*.yml" -o -name "*.yaml" -o -name "*.py" | \
  xargs grep -l "telemetry\|DISABLE_TELEMETRY" 2>/dev/null
```

#### ステップ 2: 関連リポジトリの確認
- `github-actions-hub` リポジトリでテレメトリー実装を確認
- `github-actions-templates` リポジトリでも同様に確認

#### ステップ 3: Git履歴の調査
```bash
cd /home/jinno/github-actions-actions
git log --all --oneline --grep="telemetry"
git log --all -p -- "*telemetry*"
```

---

### Phase 2: 調査結果に基づく対応（いずれか一方）

#### シナリオA: テレメトリーが未実装の場合
**アクション**: README.mdからテレメトリー記述を削除または「計画中」と明記

**変更内容**:
```markdown
## 📊 テレメトリー（使用状況メトリクス）

⚠️ **現在開発中**: この機能は現在計画・開発中です。詳細が決まり次第、更新されます。

このプロジェクトでは、将来的にActions の使用状況を把握し、改善に役立てるための**匿名テレメトリー**を収集する予定です。
```

**影響範囲**: README.md:98-119
**リスク**: 低（ドキュメントの修正のみ）

---

#### シナリオB: テレメトリーが別リポジトリで実装されている場合
**アクション**: README.mdに「実装場所」への参照を追加

**変更内容**:
```markdown
## 📊 テレメトリー（使用状況メトリクス）

テレメトリー機能の実装と詳細は、[github-actions-hubリポジトリ](../github-actions-hub/)を参照してください。
```

**影響範囲**: README.md:98-119
**リスク**: 低（ドキュメントの修正のみ）

---

#### シナリオC: テレメトリーを実装する場合
**アクション**: 全Actionにテレメトリー機能を追加

**実装方針**:
1. **共有テンプレートの作成**: `actions/_shared/templates/telemetry_wrapper.txt`
2. **各Actionの修正**: テレメトリー収集ロジックを追加
3. **環境変数チェック**: `DISABLE_TELEMETRY` で無効化可能にする

**サンプル実装** (`actions/review-and-merge/action.yml`):
```yaml
- name: Collect telemetry
  if: env.DISABLE_TELEMETRY != 'true'
  run: |
    if [ -n "${{ github.action_path }}" ]; then
      bash "${{ github.action_path }}/../_shared/scripts/collect_telemetry.sh" \
        --action "${{ github.action }}" \
        --status "${{ job.status }}" \
        --duration "${{ steps.main.outputs.duration }}"
    fi
  shell: bash
```

**影響範囲**:
- 全13個の `action.yml`
- 新規: `actions/_shared/scripts/collect_telemetry.sh`
- 新規: `actions/_shared/templates/telemetry_wrapper.txt`

**リスク**: 中（全Actionへの変更が必要、破壊的変更にならないよう注意）

---

#### シナリオD: テレメトリー機能が削除された場合
**アクション**: README.mdからテレメトリー記述を完全に削除

**変更内容**:
- README.md:98-119 のセクション全体を削除
- 関連する `docs/telemetry.md` も削除（存在する場合）

**影響範囲**: README.md, docs/telemetry.md（存在すれば）
**リスク**: 低（ドキュメントの削除のみ）

---

## 実行手順

### ステップ 1: 調査の実行
1. 全リポジトリスキャンを実行
2. Git履歴を調査
3. 関連チームメンバーに確認（可能な場合）

### ステップ 2: 結果の記録
`.audit/config/telemetry_investigation_result.yml` に調査結果を記録:
```yaml
investigation_date: "2026-02-03"
findings:
  implementation_found: true/false
  location: "github-actions-hub" / "not-implemented" / "removed"
  evidence: ["git logのエビデンス", "チームメンバーの証言"]
recommendation: "scenario-A" / "scenario-B" / "scenario-C" / "scenario-D"
```

### ステップ 3: 対応の実施
調査結果に基づき、対応するシナリオのアクションを実行

### ステップ 4: 検証
```bash
# ドキュメントと実装の整合性を確認
grep -A 10 "テレメトリー" README.md
# 実装コードを確認
find actions -name "*telemetry*"
```

---

## 成功の基準

- [ ] テレメトリー実装の有無が明確になっている
- [ ] README.mdの記述が実際の実装と合致している
- [ ] ドキュメントとコードの間に矛盾が存在しない

---

## 副作用とリスク

### 副作用
- README.mdの変更のみの場合: 副作用なし
- テレメトリー実装の場合: Actionの実行時間が若干増加（数秒〜数十秒ミリ秒）

### リスク
- **情報の誤認**: 削除した場合、将来的にテレメトリーを追加する際に再度READMEを更新する必要がある
- **実装漏れ**: テレメトリーを実装する場合、一部のActionで実装漏れが発生するリスク

---

## ロールバック手順

### ドキュメント修正の場合
```bash
cd /home/jinno/github-actions-actions
git diff README.md  # 変更内容を確認
git checkout README.md  # 元に戻す
```

### テレメトリー実装の場合
```bash
# 実装した変更を全て取り消す
git checkout .
git clean -fd  # 新規ファイルを削除
```

---

## 次のアクション

1. **調査の実行**: Phase 1のスクリプトを実行し、実装状況を特定
2. **チーム確認**: 可能であれば、チームメンバーにテレメトリー機能の経緯を確認
3. **対応実施**: 調査結果に基づき、適切なシナリオのアクションを実行
4. **ドキュメント更新**: `.audit/config/intent.yml` の `ASM-001` を更新

---

## 参考資料

- README.md:98-119（テレメトリー記述）
- .audit/analysis/gap.yml（QA-003: テレメトリー実装の不一致）
- .audit/log/claims.ndjson（C-011: テレメトリー実装の有無が不明）
