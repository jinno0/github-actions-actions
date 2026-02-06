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

## 🎨 カスタマイズ

AI Actionsはプロジェクトに合わせてカスタマイズ可能です：

### カスタムレビュールール (review-and-merge)
**review-and-merge** アクションでは、プロジェクト固有のコーディング規約やセキュリティ要件をAIレビューに反映できます：

- 📖 **[カスタムルール導入ガイド](./instructions/review-and-merge-custom-rules.md)** - 詳しい設定方法と例
- 🔧 **[ルールテンプレート](./examples/custom-rules/)** - TypeScript/Python/React等のテンプレート
- 📚 **[チュートリアル](./examples/custom-rules-tutorial.md)** - ステップバイステップで学べるガイド

**対応言語・フレームワーク:**
- TypeScript (厳格モード)
- Python (PEP 8準拠)
- React (ベストプラクティス)
- セキュリティ (共通脆弱性の防止)

### テンプレートと設定のカスタマイズ
各Actionは、カスタムプロンプトやテンプレートを注入可能です。詳しくは各Actionのセットアップガイドを参照してください。

## 🏗 前提条件

これらの Action を利用するには、**Self-hosted Runner** 上で **Claude Code CLI** が実行可能である必要があります。

詳細な環境要件や仕組みについては、[AGENTS.md](./AGENTS.md#実行環境と-claude-code-cli) を参照してください。

## 📜 開発者向けガイド

このリポジトリに新しい Action を追加したり、既存のものを改善したりする場合は、[AGENTS.md](./AGENTS.md) を必ず確認してください。
テンプレートの切り出し方や、YAML構文の注意点、必須となる構成要素（Action/Example/Instruction）について定義されています。

## 🧪 検証・テスト

全ての AI Actions は **Dry Run モード** で自動検証されます。PR 作成時や Main ブランチへの Push 時に、構造チェック・YAML 構文・モック実行が行われます。

開発者向けの詳細なテスト方法については、[AGENTS.md](./AGENTS.md#dry-run-検証testing) を参照してください。

### 📊 テストカバレッジ

このプロジェクトでは、テストカバレッジ >= 70% を目標としています。

#### カバレッジレポートの確認方法

```bash
# ローカルでカバレッジを計測
pytest --cov=actions --cov=scripts --cov-report=html

# HTMLレポートを開く
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

#### CIでのカバレッジチェック

PRを作成すると、自動的にカバレッジレポートがコメントされます。
現在のカバレッジ率: **計測中** (ベースライン策定中)

## 📊 テレメトリー（使用状況メトリクス）

このプロジェクトでは、Actions の使用状況を把握し、改善に役立てるための**匿名テレメトリー**を収集しています。プライバシーを重視し、以下の機能を提供しています：

### プライバシー機能
- ✅ **オプトアウト可能**: `DISABLE_TELEMETRY` 環境変利亚で無効化
- ✅ **匿名化**: リポジトリ名は SHA-256 ハッシュ（先頭16文字）で保存
- ✅ **最小限の収集**: 必須メトリクスのみ（コードや機密情報は収集しない）

### 収集するデータ
- Action 名、実行ステータス、実行時間
- Runner OS、Claude CLI バージョン
- エラー発生時のエラーメッセージ（最大200文字）

### 無効化する方法
```yaml
# ワークフローで無効化
env:
  DISABLE_TELEMETRY: "true"
```

詳細なプライバシーポリシーについては、[docs/telemetry.md](./docs/telemetry.md) を参照してください。

## 📈 AIレビュー品質メトリクス

**review-and-merge** Action では、AIレビューの品質を測定するための**受入率（Acceptance Rate）**を追跡しています。

### 現在のベースライン

- **受入率:** 計測中 (データ収集段階)
- **目標:** >= 70%
- **ステータス:** 📊 ベースライン策定中

### 品質メトリクスの概要

- **受入率（Acceptance Rate）**: 人間に受け入れられたAIレビューの割合（目標: >= 70%）
- **レビューアウトカム**: approved（承認）/modified（修正あり）/rejected（拒否）/needs_work（修正要求）
- **提案数**: 1回のレビューあたりの平均提案数
- **一般的な拒否理由**: AIレビューが拒否される主な理由

### メトリクスの確認方法

```bash
# 品質メトリクスレポートを生成
python scripts/calculate_acceptance_rate.py --output report --time-period 7d
```

### 定期レポート

毎週日曜日に自動的に受入率レポートが生成され、Issueとして投稿されます。
過去のレポートは [`metrics/`](metrics/) ディレクトリを参照してください。

詳細な品質メトリクスのドキュメントについては、[docs/quality_metrics.md](./docs/quality_metrics.md) を参照してください。

## 🚀 Adoption

Are you using these AI Actions in your repository? We'd love to hear from you!

- **Add your repository:** Edit [ADOPTION.md](ADOPTION.md) and submit a PR
- **Share feedback:** Open an [Adoption Report](https://github.com/your-org/github-actions-actions/issues/new?template=adoption_report.yml)

Current adopters: [See ADOPTION.md](ADOPTION.md) (2 pilot projects)

## 🎯 プロジェクトの目的

詳細なロードマップや現在のステータスについては、[PURPOSE.md](./PURPOSE.md) を参照してください。

## ⚖️ 憲法

このリポジトリの不変の原則については、[SYSTEM_CONSTITUTION.md](./SYSTEM_CONSTITUTION.md) を参照してください。