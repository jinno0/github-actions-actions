# Auto Rebase PR with AI

PR（Pull Request）を自動的にリベースし、マージコンフリクトが発生した場合に Claude Code CLI を使って解決する GitHub Action です。

## 前提条件

### Self-hosted Runner
この Action は **self-hosted runner** での動作を前提としています。

- リポジトリまたは Organization で self-hosted runner が設定されている必要があります
- Runner には書き込み権限が必要です

### Claude Code CLI
Runner に **Claude Code CLI** (`claude` コマンド) がインストールされている必要があります。

```bash
# Claude Code CLI のインストール例
npm install -g @anthropic-ai/claude-code
```

### Permissions
以下の権限が必要です：
- `pull-requests: write` - PR の操作とコメントの投稿
- `contents: write` - ブランチの force push

## セットアップ手順

### 1. Self-hosted Runner のセットアップ

まだ self-hosted runner を設定していない場合：

```bash
# Runner の登録トークンを取得
gh api /repos/YOUR_ORG/YOUR_REPO/actions/runners/registration-token

# 出力されたトークンを使って runner をセットアップ
# （GitHub のドキュメントに従ってください）
```

### 2. Claude Code CLI のインストール

Runner 上で Claude Code CLI をインストールし、認証を設定します：

```bash
npm install -g @anthropic-ai/claude-code
claude auth login
```

### 3. ワークフローの配置

`examples/auto-rebase-example.yml` を `.github/workflows/` にコピーします：

```bash
cp examples/auto-rebase-example.yml .github/workflows/auto-rebase.yml
```

## 使い方

### 基本的な使い方

PR が作成・更新されると、自動的に以下が行われます：

1. ベースブランチの最新を取得
2. リベースを試みる
3. コンフリクトが発生した場合、Claude Code CLI が解決を試みる
4. 解決後、force push してリベースを完了させる

### 手動実行

ワークフローは手動で実行することもできます：

1. GitHub 上でリポジトリを開く
2. **Actions** タブに移動
3. **Auto Rebase PR** ワークフローを選択
4. **Run workflow** をクリック
5. 対象の PR を選択して実行

### Inputs

| Input | 説明 | 必須 | デフォルト値 |
|-------|------|------|--------------|
| `github-token` | GitHub トークン | ✅ | `${{ secrets.GITHUB_TOKEN }}` |
| `claude-model` | 使用する Claude モデル | - | `sonnet` |
| `rebase-strategy` | リベース戦略（interactive / force） | - | `interactive` |
| `conflict-resolution-prompt-template` | カスタムプロンプトテンプレートのパス | - | （内蔵テンプレート使用） |

### Outputs

| Output | 説明 |
|--------|------|
| `rebased` | リベースが成功したか（`true` / `false`） |
| `conflicts-resolved` | コンフリクトが AI で解決されたか（`true` / `false`） |
| `conflict-count` | 発生したコンフリクトの数 |

## 仕組み

### リベースの流れ

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PR チェックアウト                                           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. ベースブランチの最新を取得                                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. リベース実行                                                │
└─────────────────────────────────────────────────────────────┘
                           ↓
                    ┌──────┴──────┐
                    │ コンフリクト？ │
                    └──────┬──────┘
                     No   │    Yes
           ┌─────────────┘         └─────────────┐
           ↓                                    ↓
┌─────────────────────┐          ┌───────────────────────────┐
│ ✅ リベース完了        │          │ ⚠️ Claude Code CLI で解決  │
│ force push          │          │ - コンフリクトファイルを解析 │
└─────────────────────┘          │ - 適切な解決策を適用        │
                                 └───────────────────────────┘
                                          ↓
                                 ┌────────────────┐
                                 │ 解決成功？       │
                                 └────────┬───────┘
                                 Yes     │    No
                      ┌─────────────┘         └─────────────┐
                      ↓                                         ↓
          ┌─────────────────────┐              ┌─────────────────────┐
          │ ✅ rebase --continue │              │ ❌ rebase --abort  │
          │ force push          │              │ 元の状態に復元        │
          └─────────────────────┘              └─────────────────────┘
```

### コンフリクト解決の原則

Claude Code CLI は以下の原則に従ってコンフリクトを解決します：

1. **一貫性**: 周囲のコードと一致するスタイルを維持
2. **意味**: 両方のブランチの意味を保持
3. **最小限の変更**: 必要最小限の変更で解決
4. **安全性**: 不確実な場合はシステム安定性を優先

## カスタマイズ

### カスタムプロンプトテンプレート

独自のコンフリクト解決ルールを指定したい場合、カスタムプロンプトテンプレートを作成できます：

1. リポジトリ内にテンプレートファイルを作成（例: `.github/conflict-prompt.txt`）
2. プレースホルダーを使用：
   - `{BASE_BRANCH}` - ベースブランチ名
   - `{CURRENT_BRANCH}` - 現在のブランチ名
   - `{PR_NUMBER}` - PR 番号

3. ワークフローで指定：

```yaml
- name: Auto Rebase with AI
  uses: ./actions/auto-rebase
  with:
    conflict-resolution-prompt-template: '.github/conflict-prompt.txt'
```

### 例: プロジェクト特有のルール

```
You are resolving merge conflicts for our Node.js project.

## Project-Specific Rules
1. Never remove TypeScript type definitions
2. Always prefer package.json updates from {BASE_BRANCH}
3. For test files, prefer the version with better coverage
4. Keep import paths consistent with the project's monorepo structure
...
```

## トラブルシューティング

### ワークフローが queued のまま

**原因**: self-hosted runner が利用できない

**解決策**:
- Runner がオンラインであることを確認
- Runner ラベルが正しく設定されているか確認
- Organization レベルの runner を使用している場合、ワークフローで `runs-on: self-hosted` を指定

### コンフリクト解決に失敗する

**原因**: Claude Code CLI が適切にインストール・認証されていない

**解決策**:
```bash
# Runner 上で CLI が動作するか確認
claude --version
claude auth status
```

### Force push が拒否される

**原因**: プッシュ権限の問題

**解決策**:
- `contents: write` 権限が付与されているか確認
- ブランチ保護ルールで force push が制限されていないか確認

## 完全なワークフロー例

```yaml
name: Auto Rebase PR

on:
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number }}
  cancel-in-progress: false

permissions:
  pull-requests: write
  contents: write

jobs:
  auto-rebase:
    runs-on: self-hosted

    steps:
      - name: Auto Rebase with AI
        uses: ./actions/auto-rebase
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          claude-model: 'sonnet'
```

