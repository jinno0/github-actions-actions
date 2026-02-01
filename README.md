# AI Hub - GitHub Actions for AI-Native Development

このリポジトリは、GitHub組織全体の開発効率と品質を向上させるための「AIネイティブなGitHub Actions」を提供するハブです。
Self-hosted runner上で動作する **Claude Code CLI** を活用し、文脈を理解した高度な自動化（レビュー、修正、ドキュメント生成など）を実現します。

## 🚀 提供している AI Actions

現在、以下の AI Actions を提供しています（全13件）。

### コア開発ワークフロー (Core Development)

| Action | 概要 | セットアップガイド |
|--------|------|-------------------|
| `review-and-merge` | AIがコードをレビューし自動マージ（Auto-Fix標準装備） | [Guide](./instructions/review-and-merge.md) |
| `spec-to-code` | Markdown仕様書からコードを自動生成 | [Guide](./instructions/spec-to-code.md) |
| `action-fixer` | Workflowのエラーを検知し、AIが自動修正 | [Guide](./instructions/action-fixer.md) |
| `auto-refactor` | 自然言語の指示に基づき、既存コードをリファクタリング | [Guide](./instructions/auto-refactor.md) |

### ドキュメント自動化 (Documentation)

| Action | 概要 | セットアップガイド |
|--------|------|-------------------|
| `auto-document` | コードの変更を検知し、README等のドキュメントを自動更新 | [Guide](./instructions/auto-document.md) |
| `release-notes-ai` | コミット履歴から人間が読みやすいリリースノートを生成 | [Guide](./instructions/release-notes-ai.md) |

### PR マージ自動化 (Automation)

| Action | 概要 | セットアップガイド |
|--------|------|-------------------|
| `auto-merge` | PRが条件を満たす場合に自動マージ（squash/merge/rebase対応） | [Guide](./instructions/auto-merge.md) |
| `auto-rebase` | PRの競合をAIが自動解決しながらリベース | [Guide](./instructions/auto-rebase.md) |
| `review-auto-merge` | AIレビュー後、CIパス時に自動マージ（リトライ機能付き） | [Guide](./instructions/review-auto-merge.md) |
| `publish-pr` | ドラフトPRを自動的にレビュー準備完了に変更 | [Guide](./instructions/publish-pr.md) |

### 一括操作 (Bulk Operations)

| Action | 概要 | セットアップガイド |
|--------|------|-------------------|
| `bulk-merge-prs` | 複数のPRを一括マージ | [Guide](./instructions/bulk-merge-prs.md) |
| `bulk-rebase-prs` | 複数のPRを一括リベース | [Guide](./instructions/bulk-rebase-prs.md) |

### ワークフロー補助 (Workflow Helpers)

| Action | 概要 | セットアップガイド |
|--------|------|-------------------|
| `pr-review-enqueuer` | PRをスキャンし、AIレビューキューに自動登録 | [Guide](./instructions/pr-review-enqueuer.md) |

## 🛠 使い方

全ての Action には、すぐに試せる**利用例（Examples）**と、詳細な**導入手順（Instructions）**が用意されています。

### 1. 利用例をコピーする
[examples/](./examples/) ディレクトリにある `.yml` ファイルを、あなたの方のリポジトリの `.github/workflows/` にコピーしてください。

### 2. 手順書を確認する
[instructions/](./instructions/) ディレクトリにある各 Action のドキュメントに従って、必要な権限や環境を設定してください。

### 3. 組織での導入を計画している方へ
チーム全体で導入を進める場合は、[**ADOPTION_GUIDE.md**](./ADOPTION_GUIDE.md) を参照してください。パイロット導入から本番展開までの完全なロードマップを提供しています。

## 🏗 前提条件

これらの Action を利用するには、**Self-hosted Runner** 上で **Claude Code CLI** が実行可能である必要があります。

詳細な環境要件や仕組みについては、[AGENTS.md](./AGENTS.md#実行環境と-claude-code-cli) を参照してください。

## 📜 開発者向けガイド

このリポジトリに新しい Action を追加したり、既存のものを改善したりする場合は、[AGENTS.md](./AGENTS.md) を必ず確認してください。
テンプレートの切り出し方や、YAML構文の注意点、必須となる構成要素（Action/Example/Instruction）について定義されています。

## 🧪 検証・テスト

全ての AI Actions は **Dry Run モード** で自動検証されます。PR 作成時や Main ブランチへの Push 時に、構造チェック・YAML 構文・モック実行が行われます。

開発者向けの詳細なテスト方法については、[AGENTS.md](./AGENTS.md#dry-run-検証testing) を参照してください。

## 🎯 プロジェクトの目的

詳細なロードマップや現在のステータスについては、[PURPOSE.md](./PURPOSE.md) を参照してください。

## ⚖️ 憲法

このリポジトリの不変の原則については、[SYSTEM_CONSTITUTION.md](./SYSTEM_CONSTITUTION.md) を参照してください。