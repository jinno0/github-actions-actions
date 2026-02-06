# PR-002: Action README.mdの追加

**関連するギャップ:** GAP-004
**優先度:** Low
**推定作業時間:** 3-4時間

## 概要

7つのAction (auto-merge, auto-rebase, review-auto-merge, publish-pr, pr-review-enqueuer,
bulk-merge-prs, bulk-rebase-prs) で `actions/xxx/README.md` が欠落している。
このPRでは各ActionにREADME.mdを追加し、ドキュメントの一貫性を向上させる。

## 変更内容

### 対象Action

1. `actions/auto-merge/README.md`
2. `actions/auto-rebase/README.md`
3. `actions/review-auto-merge/README.md`
4. `actions/publish-pr/README.md`
5. `actions/pr-review-enqueuer/README.md`
6. `actions/bulk-merge-prs/README.md`
7. `actions/bulk-rebase-prs/README.md`

### README.mdのテンプレート構造

各READMEには以下のセクションを含める:

```markdown
# [Action Name]

## 概要
このActionの機能を1-2文で説明

## 前提条件
- Self-hosted runner with Claude Code CLI
- 必要な権限（contents:write, pull-requests:write など）

## 入力パラメータ (Inputs)

| パラメータ | 必須 | デフォルト値 | 説明 |
|-----------|------|------------|------|
| ... | ... | ... | ... |

## 出力 (Outputs)

| 出力 | 説明 |
|------|------|
| ... | ... |

## 使用例

\`\`\`yaml
- uses: ./actions/[action-name]
  with:
    param: value
\`\`\`

## 導入方法

1. examples/ のワークフローファイルをコピー
2. 詳細は instructions/[action-name].md を参照

## 注意事項

- 特定の制約や注意点

## トラブルシューティング

### よくある問題

**問題:** エラーメッセージ
**原因:** 原因
**解決策:** 解決方法
```

### 実装手順

各Actionに対して:

1. `instructions/[action-name].md` を読み、機能と使用方法を把握
2. `actions/[action-name]/action.yml` を読み、inputs/outputsを確認
3. 既存のREADME（review-and-merge, spec-to-code等）をテンプレートとして使用
4. 上記テンプレート構造に従ってREADME.mdを作成
5. `examples/` のワークフローファイルの内容を反映

## 期待される効果

- `actions/` ディレクトリで各ActionのREADMEを直接見つけられるようになる
- 利用者が `instructions/` と `actions/` を行き来する手間が減る
- ドキュメントの一貫性が向上し、プロフェッショナルな印象を与える

## 検証方法

1. **READMEの存在確認**
   ```bash
   for action in auto-merge auto-rebase review-auto-merge publish-pr pr-review-enqueuer bulk-merge-prs bulk-rebase-prs; do
     [ -f actions/$action/README.md ] && echo "✓ $action" || echo "✗ $action"
   done
   ```

2. **READMEの内容確認**
   - action.ymlで定義されたinputsが全て説明されているか
   - 使用例が含まれているか
   - instructions/への参照が含まれているか

3. **リンク切れチェック**
   - README内の相対パスが正しいか確認

## 優先順位の根拠

この変更はCriticalではない理由:
- `instructions/*.md` ですでに導入ガイドが提供されている
- 利用者は `instructions/` を参照すれば機能する
- ただし、`actions/` 直下にREADMEがないのは不整合（README.md:89でAGENTS.md参照あり）

## ロールバック手順

作成したREADME.mdを削除:
```bash
rm actions/auto-merge/README.md
rm actions/auto-rebase/README.md
rm actions/review-auto-merge/README.md
rm actions/publish-pr/README.md
rm actions/pr-review-enqueuer/README.md
rm actions/bulk-merge-prs/README.md
rm actions/bulk-rebase-prs/README.md
```

## リスク評価

- **破壊的変更:** なし
- **副作用:** なし（README追加のみ）
- **ドキュメント整合性:** 向上（instructions/とactions/の二重管理になるが、内容は同期させる）

## 参考資料

- 既存の `actions/review-and-merge/README.md`
- 既存の `actions/spec-to-code/README.md`
- `AGENTS.md` (README.md:89で参照されている)

## 成功基準

- [ ] 7つのAction全てにREADME.mdが作成される
- [ ] 各READMEがaction.ymlと整合している
- [ ] 各READMEがinstructions/*.mdと内容が一致している
- [ ] README内のリンクが全て有効
