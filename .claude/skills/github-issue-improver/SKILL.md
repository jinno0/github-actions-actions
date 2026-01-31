---
name: github-issue-improver
description: >
  自動的にGitHub Issueを分析し、構造化された内容に改善するスキル。
  雑なIssueや情報不足のIssueをAIが作業しやすい形式に自動補完・加筆訂正する。
  タイトルの標準化、本文の構造化、適切なラベル付与、不足情報の指摘を行う。
  「このIssueを改善して」「Issue内容を整えて」といった依頼で使用。
---

# GitHub Issue Improver

## Overview

このスキルはGitHub Issueの品質を自動的に改善します。雑な記述のIssueを分析し、構造化されたAIが作業しやすい形式に変換します。Issueの種類を自動分類し、適切なテンプレートを適用して不足情報を指摘します。

## Quick Start

### 基本的な使い方

```bash
# 環境設定
export GITHUB_TOKEN="ghp_xxx"

# 単一のIssueを改善（コメントとして提案）
python scripts/issue_improver.py --repo owner/repo --issue 123

# Issueを直接更新
python scripts/issue_improver.py --repo owner/repo --issue 123 --mode update --update-title --update-body --update-labels

# 複数のIssueを一括改善
python scripts/issue_improver.py --repo owner/repo --issues 123 124 125 --mode comment

# JSONファイルから一括適用
python scripts/apply_improvements.py --repo owner/repo apply --improvements-file improvements.json
```

詳細は `--help` オプションを参照してください。

## Core Capabilities

### 1. Issue自動分析
- **種類分類**: bug, feature, documentation, test, refactorなどを自動判定
- **重要度評価**: critical, high, medium, lowの優先度を自動設定
- **コンポーネント抽出**: frontend, backend, apiなどの関連コンポーネントを特定
- **品質スコアリング**: Issueの品質を0-1のスコアで評価

### 2. 標準化されたタイトル生成
- Coventional Commitsスタイルのプレフィックス付与
```
元: login fails
改善: Fix: Login fails with invalid credentials
```

### 3. 構造化された本文生成
- 種類に応じたテンプレート自動適用
- 不足情報の指摘と入力枠の追加
- マークダウン形式での整形

**バグ報告の例:**
```markdown
## Bug Description
[自動生成された説明]

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
[ここに期待される動作を記述]

## Actual Behavior
[ここに実際の動作を記述]

## Environment
- OS:
- Browser:
- Version:
```

**機能要望の例:**
```markdown
## Feature Description
[自動生成された説明]

## Use Case
[ユーザーストーリーを記述]

## Acceptance Criteria
- [ ]
- [ ]
- [ ]

## Proposed Solution
[解決策の提案]
```

### 4. 適切なラベル付与
- 種類ラベル: `bug`, `feature`, `documentation`
- 優先度ラベル: `priority: critical`, `priority: high`
- エリアラベル: `area: frontend`, `area: backend`

### 5. 不足情報の指摘
- 再現手順の欠如
- 期待する動作の記述漏れ
- 環境情報の不足
- 受け入れ条件の未設定

## Workflow

### 改善モード

**Commentモード（推奨）**: 改善提案をコメントとして追加
```bash
python scripts/issue_improver.py --repo owner/repo --issue 123 --mode comment
```

**Updateモード**: Issueを直接更新
```bash
python scripts/issue_improver.py --repo owner/repo --issue 123 --mode update --update-title --update-body
```

**バッチ処理**: 複数のIssueを一括処理
```bash
python scripts/issue_improver.py --repo owner/repo --issues 123 124 125 --mode comment
```

## Scripts

- **issue_improver.py**: メインの改善スクリプト（詳細は `--help` を参照）
- **issue_analyzer.py**: Issue内容を分析し、改善案を生成
- **github_client.py**: GitHub APIとの連携処理
- **apply_improvements.py**: JSONファイルからの改善適用とテンプレート生成

```bash
# 改善テンプレートを生成
python scripts/apply_improvements.py --repo owner/repo template --issues 123 124 125

# JSONファイルから改善を適用
python scripts/apply_improvements.py --repo owner/repo apply --improvements-file improvements.json
```

## References

### references/issue_templates.md
Issue種類ごとのテンプレートと品質ガイドライン。
- バグ報告、機能要望、ドキュメント更新のテンプレート
- タイトル命名規則
- ラベル付けガイドライン
- 品質チェックリスト

## Use Cases

- **新規Issueの品質向上**: 新しく作られた雑なIssueを改善
- **バックログの一括整理**: 古い未整理Issueを一括改善
- **Issueテンプレートの適用**: プロジェクトでIssue標準化を実施
- **CI/CD連携**: GitHub Actionsでの自動実行が可能

---

このスキルを使うことで、GitHub Issueの品質が大幅に向上し、開発チームの作業効率が改善されます。特にAIによるIssue処理の前処理として最適です。