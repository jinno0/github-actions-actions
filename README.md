# AI Hub - GitHub Actions for AI-Native Development

このリポジトリは、GitHub組織全体の開発効率と品質を向上させるための「AIネイティブなGitHub Actions」を提供するハブです。
Self-hosted runner上で動作する **Claude Code CLI** を活用し、文脈を理解した高度な自動化（レビュー、修正、ドキュメント生成など）を実現します。

## 🚀 提供している AI Actions

現在、以下の6つの主要な AI Actions を提供しています。

| Action | 概要 | セットアップガイド |
|--------|------|-------------------|
| `review-and-merge` | AIがコードを自動修正し、そのまま自動マージ（Auto-Fix標準装備） | [Guide](./instructions/review-and-merge.md) |
| `spec-to-code` | Markdown仕様書からコードを自動生成 | [Guide](./instructions/spec-to-code.md) |
| `action-fixer` | Workflowのエラーを検知し、AIが自動修正 | [Guide](./instructions/action-fixer.md) |
| `auto-refactor` | 自然言語の指示に基づき、既存コードをリファクタリング | [Guide](./instructions/auto-refactor.md) |
| `auto-document` | コードの変更を検知し、README等のドキュメントを自動更新 | [Guide](./instructions/auto-document.md) |
| `release-notes-ai` | コミット履歴から人間が読みやすいリリースノートを生成 | [Guide](./instructions/release-notes-ai.md) |

## 🛠 使い方

全ての Action には、すぐに試せる**利用例（Examples）**と、詳細な**導入手順（Instructions）**が用意されています。

### 1. 利用例をコピーする
[examples/](./examples/) ディレクトリにある `.yml` ファイルを、あなたの方のリポジトリの `.github/workflows/` にコピーしてください。

### 2. 手順書を確認する
[instructions/](./instructions/) ディレクトリにある各 Action のドキュメントに従って、必要な権限や環境を設定してください。

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