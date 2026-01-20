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

これらの Action を利用するには、以下の環境が必要です。

- **Self-hosted Runner**: 組織またはリポジトリで設定されたセルフホストランナー。
- **Claude Code CLI**: ランナー上で `claude` コマンドが実行可能であること。
- **GitHub CLI**: `gh` コマンドが実行可能であること。

詳細なセットアップ方法は、各 Action のガイドを参照してください。

## 📜 開発者向けガイド

このリポジトリに新しい Action を追加したり、既存のものを改善したりする場合は、[AGENTS.md](./AGENTS.md) を必ず確認してください。
テンプレートの切り出し方や、YAML構文の注意点、必須となる構成要素（Action/Example/Instruction）について定義されています。

## 🧪 検証・テスト

全ての AI Actions は **Dry Run モード** で自動検証されます。

### 自動テスト（CI）

このリポジトリでは、以下のタイミングで自動テストが実行されます：

- **PR 作成時**: Actions やテンプレートを変更した場合
- **Main ブランチへの Push**: 変更をマージした場合
- **手動実行**: GitHub Actions の UI からいつでも実行可能

### テスト内容

 Dry Run テストでは以下を検証します：

- ✅ **構造チェック**: `action.yml`、テンプレートファイル、例ワークフロー、説明ドキュメントが存在するか
- ✅ **YAML 構文**: 全ての YAML ファイルの構文が正しいか
- ✅ **プレースホルダー**: テンプレート内の `{VARIABLE}` 形式のプレースホルダーが正しく定義されているか
- ✅ **モック実行**: Claude CLI をモック化して、Action の実行フローをシミュレート

**重要**: Dry Run モードでは実際の commit/push は行われません。PR マージ直前までの挙動を検証します。

### 手動でテストを実行する

```bash
# YAML 構文チェック
find actions -name 'action.yml' -exec python3 -c "import yaml; yaml.safe_load(open('{}'))" \;

# 構造チェック
for action in actions/*/; do
  name=$(basename "$action")
  echo "Checking $name:"
  echo "  action.yml: $([ -f "$action/action.yml" ] && echo '✓' || echo '✗')"
  echo "  example: $([ -f "examples/${name}-example.yml" ] && echo '✓' || echo '✗')"
  echo "  instruction: $([ -f "instructions/${name}.md" ] && echo '✓' || echo '✗')"
done
```

## 🎯 プロジェクトの目的

詳細なロードマップや現在のステータスについては、[PURPOSE.md](./PURPOSE.md) を参照してください。

## ⚖️ 憲法

このリポジトリの不変の原則については、[SYSTEM_CONSTITUTION.md](./SYSTEM_CONSTITUTION.md) を参照してください。