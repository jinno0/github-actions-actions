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

### Actions Fixer

GitHub Actionsのワークフローやアクションのエラーをチェックし、一般的な問題を自動修正するActionです。

#### 使用方法

リポジトリのワークフローから参照：

```yaml
name: Validate and Fix Workflows

on:
  pull_request:
    paths:
      - '.github/**'
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Workflows
        uses: your-org/github-actions-actions/actions/action-fixer@main
        with:
          fail-on-error: 'true'
          auto-fix: 'false'
```

#### 入力パラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|-----------|------|-----------|------|
| `fail-on-error` | | `true` | エラー発見時にジョブを失敗させるか |
| `auto-fix` | | `false` | 自動修正を適用してPRを作成するか |
| `commit-message` | | `fix: correct workflow validation issues` | 自動修正時のコミットメッセージ |

#### 検出・修正する問題

| 問題 | 説明 | 自動修正 |
|------|------|----------|
| YAML構文エラー | yamllintとPython yamlモジュールで検証 | ✅ |
| 破損したxargsコマンド | `xargs -I {} sh -c` の問題を検出 | ✅ |
| 欠落したruns-on | ジョブにruns-onがない場合を検出 | ❌ |
| 非推奨アクション | `@v1`, `@v2` などの古いバージョンを検出 | ❌ |
| 権限設定の欠如 | permissionsがない場合を警告 | ❌ |

#### 動作フロー

1. YAML構文の検証
2. 一般的なワークフローの問題をチェック
3. auto-fixが有効な場合、問題を自動修正
4. 修正内容でPRを自動作成（auto-fix=trueの場合）

## ライセンス

TBD
