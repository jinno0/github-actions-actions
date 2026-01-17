# GitHub Actions - Organization Actions & Workflows

GitHub組織で共通利用するActionsとWorkflowsを管理するリポジトリ。

## Actions

### Review PR and Auto-Merge

Claude Code CLIを使用してPRをレビューし、LGTM（Looks Good To Me）と判定された場合に自動マージするActionです。

#### 使用方法

リポジトリのワークフローから参照：

```yaml
name: Review and Auto-Merge

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  pull-requests: write
  contents: write

jobs:
  review:
    runs-on: self-hosted
    steps:
      - uses: your-org/github-actions-actions/actions/review-and-merge@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          claude-model: sonnet          # 使用するClaudeモデル
          lgtm-threshold: '7'           # LGTM判定のしきい値 (1-10)
          merge-method: squash          # マージ方法 (squash/merge/rebase)
```

#### 必要要件

- **Self-hosted Runner**: Claude Code CLI (`claude`) がインストールされたrunner
- **Permissions**: `pull-requests: write`, `contents: write`

#### 入力パラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|-----------|------|-----------|------|
| `github-token` | ✓ | - | GitHubトークン |
| `claude-model` | | `sonnet` | 使用するClaudeモデル |
| `lgtm-threshold` | | `7` | LGTM判定の最低confidenceスコア (1-10) |
| `merge-method` | | `squash` | マージ方法 (`squash`, `merge`, `rebase`) |

#### 動作フロー

1. PRのdiffを取得
2. Claude Code CLIでコードレビューを実行
3. 結果をPRにコメントとして投稿
4. LGTM且つconfidenceがしきい値以上の場合、自動マージ

## Workflows

### Review and Auto-Merge PR

PR作成・更新時に自動レビューとマージを実行するワークフローです。

**トリガー条件:**
- PRがopened/synchronize/reopenedされたとき
- DraftでないPRのみ対象

**使用方法:**
このリポジトリでワークフローを有効化するには、Self-hosted Runnerを設定してください。

## セットアップ

### Self-hosted Runnerの設定

1. Claude Code CLIをインストールしたマシンを準備
2. OrganizationのSettings > Actions > Runners からrunnerを追加
3. ワークフローが`runs-on: self-hosted`で実行されるよう設定

### Claude Code CLIのインストール

```bash
npm install -g @anthropic-ai/claude-code
```

## ライセンス

TBD
