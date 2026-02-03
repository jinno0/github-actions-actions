---
description: Agent実行用Issueを対話的に作成
---

# Create Issue Command

Agent実行用のIssueをテンプレートベースで対話的に作成します。

## 使用方法

```bash
/create-issue
```

このコマンドを実行すると、対話的にIssue作成のための情報を収集します。

## 対話フロー

### 1. Issue タイトル

```
Issue タイトルを入力してください:
例) ユーザー認証機能の実装
```

### 2. Issue タイプ選択

```
Issue タイプを選択してください:
1. 🆕 feature (新機能)
2. 🐛 bug (バグ修正)
3. ♻️  refactor (リファクタリング)
4. 📝 docs (ドキュメント)
5. ⚡ performance (パフォーマンス改善)
6. 🔒 security (セキュリティ)
7. 🧪 test (テスト追加)

選択 (1-7):
```

### 3. 要件入力

```
要件を入力してください (完了したら空行):
- ログイン画面の実装
- JWT認証の実装
- ユーザーモデルの作成
- ユニットテスト作成
<Enter>
```

### 4. 技術スタック (オプション)

```
使用する技術スタックを入力してください (任意):
例) React, TypeScript, Firebase Auth
```

### 5. 制約事項 (オプション)

```
制約事項があれば入力してください (任意):
例) パスワードリセット機能は別Issueで実装
```

### 6. Agent実行設定

```
Agent自動実行を有効にしますか? (y/n):
```

- `y`: 🤖agent-execute ラベルを自動付与（作成後すぐにAgentが実行開始）
- `n`: 手動でラベルを追加するまでAgent実行しない

### 7. 優先度設定

```
優先度を選択してください:
1. 🔴 High (高)
2. 🟡 Medium (中)
3. 🟢 Low (低)

選択 (1-3):
```

### 8. 担当者指定 (オプション)

```
担当者を指定しますか? (GitHubユーザー名、空でスキップ):
```

## 生成されるIssue

### Issue Body テンプレート

```markdown
# [タイプ] タイトル

## 📋 要件

- [ ] 要件1
- [ ] 要件2
- [ ] 要件3

## 🛠️ 技術スタック

- React
- TypeScript
- Firebase Auth

## ⚠️ 制約事項

- パスワードリセット機能は別Issueで実装

## 📊 成功条件

- [ ] TypeScript エラー: 0件
- [ ] テストカバレッジ: ≥80%
- [ ] 品質スコア: ≥80点
- [ ] セキュリティスキャン: 脆弱性0件

## 🤖 Agent実行設定

- **自動実行**: 有効
- **優先度**: High
- **期待実行時間**: 3-5分

---

**ラベル**: 🤖agent-execute, 🆕feature, 🔴priority-high

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## 実行例

コマンドを実行すると対話的に情報を入力し、最後にIssueが作成されます。詳細な対話フローは上記「対話フロー」セクションを参照してください。

## ラベル自動付与

Issue タイプに応じて自動的にラベルが付与されます:

| タイプ | ラベル |
|--------|--------|
| feature | 🆕feature, enhancement |
| bug | 🐛bug |
| refactor | ♻️refactor |
| docs | 📝documentation |
| performance | ⚡performance |
| security | 🔒security |
| test | 🧪test |

優先度に応じたラベル:

| 優先度 | ラベル |
|--------|--------|
| High | 🔴priority-high |
| Medium | 🟡priority-medium |
| Low | 🟢priority-low |

Agent自動実行:

| 設定 | ラベル |
|------|--------|
| 有効 | 🤖agent-execute |

## 設定

### .claude/settings.local.json

```json
{
  "issueCreation": {
    "defaultPriority": "medium",
    "autoExecuteByDefault": true,
    "defaultLabels": ["🤖agent-execute"],
    "requireApproval": false,
    "templates": {
      "feature": ".github/ISSUE_TEMPLATE/feature.md",
      "bug": ".github/ISSUE_TEMPLATE/bug.md"
    }
  }
}
```

## トラブルシューティング

### `gh` コマンドが見つからない場合

```bash
# GitHub CLI インストール
brew install gh  # macOS
# または
npm install -g @github/cli

# 認証
gh auth login
```

### Issue作成権限エラー

GitHub Token に `repo` スコープが必要です。`.env` ファイルの `GITHUB_TOKEN` を確認してください。

### Agent が自動実行されない場合

- 🤖agent-execute ラベルが付与されているか確認
- GitHub Actions Workflow が有効か確認
- ANTHROPIC_API_KEY が Secrets に設定されているか確認

## 関連ドキュメント

- [.github/ISSUE_TEMPLATE/agent-task.md](../../.github/ISSUE_TEMPLATE/agent-task.md) - Issue Template
- [docs/AGENT_OPERATIONS_MANUAL.md](../../docs/AGENT_OPERATIONS_MANUAL.md) - Agent運用マニュアル
- [GitHub CLI Documentation](https://cli.github.com/manual/)

---

🤖 このコマンドは対話的にIssueを作成し、Agent実行を効率化します。
