---
name: codex
description: >
  OpenAI Codex CLIを使用したコードレビュー、分析、コードベースへの質問を実行するスキル。
  使用場面: (1) コードレビュー依頼時、(2) コードベース全体の分析、(3) 実装に関する質問、
  (4) バグの調査、(5) リファクタリング提案、(6) 解消が難しい問題の調査。
  トリガー: "codex", "コードレビュー", "レビューして", "分析して", "/codex"
---

# Codex

OpenAI Codex CLIを使用してコードレビュー・分析・質問回答を実行するスキル。

## 概要

このスキルは、OpenAI Codex CLIのラッパーを提供し、以下のタスクを自動化します:

- コードレビューと品質分析
- バグやパフォーマンス問題の調査
- アーキテクチャと設計の分析
- セキュリティ脆弱性の検出
- リファクタリング提案
- コードベースに関する質問回答

## クイックスタート

### 基本的な使い方

ユーザーが次のようなリクエストをした場合に使用します:

- 「このコードをレビューして」
- 「バグを調査して」
- 「アーキテクチャを分析して」
- 「このプロジェクトについて質問に答えて」

### 実行手順

1. **リクエストを理解**: ユーザーの目的を特定（レビュー、分析、調査など）
2. **Codexを実行**: `scripts/run_codex.py` を使用してCodex CLIを実行
3. **結果を報告**: Codexの出力をユーザーに提示

### 使用例

```bash
# コードレビュー（プロジェクトルートから実行）
python .claude/skills/codex/scripts/run_codex.py "Review this codebase for potential security vulnerabilities"

# バグ調査
python .claude/skills/codex/scripts/run_codex.py "Investigate why the authentication is failing"

# アーキテクチャ分析
python .claude/skills/codex/scripts/run_codex.py "Analyze the architecture and suggest improvements"

# サンドボックスを無効化（慎重に使用）
python .claude/skills/codex/scripts/run_codex.py "Review code" --no-sandbox

# ログ保持時間をカスタマイズ（例: 48時間）
python .claude/skills/codex/scripts/run_codex.py "Review code" --max-age-hours 48
```

## 主要ユースケース

### 1. コードレビュー

ユーザーが以下のようなリクエストをしたときに使用:

- 「コードレビューを実施して」
- 「このプロジェクトの問題点を指摘して」
- 「セキュリティレビューをして」
- 「コード品質を評価して」

**推奨リクエストパターン** (`references/request_patterns.md` 参照):

```
"Review this codebase for:
1. Potential bugs and edge cases
2. Code quality issues
3. Performance concerns
4. Security vulnerabilities
5. Best practices violations

Provide specific file locations and suggestions for improvement."
```

### 2. バグ調査

ユーザーが以下のような問題を報告したときに使用:

- 「認証でエラーが発生する」
- 「パフォーマンスが悪い」
- 「特定の機能が動かない」

**調査手順**:

1. 問題の詳細をユーザーから聞き出す
2. Codexで根本原因を調査
3. 影響範囲を特定
4. 修正提案を提示

### 3. アーキテクチャ分析

ユーザーが以下を求めたときに使用:

- 「アーキテクチャを分析して」
- 「設計上の問題点を教えて」
- 「スケーラビリティを評価して」

**分析ポイント**:

- 設計パターンの識別
- 結合度の評価
- 拡張性の確認
- 単一障害点の特定

### 4. リファクタリング提案

ユーザーが以下を求めたときに使用:

- 「リファクタリング提案をして」
- 「コードを改善したい」
- 「モダン化の機会を教えて」

**提案内容**:

- コード重複の排除
- 可読性の改善
- 設計パターンの適用
- 最新言語機能の活用

### 5. 学習と理解

ユーザーが以下を求めたときに使用:

- 「このコードは何をするもの？」
- 「どのような設計パターンが使われている？」
- 「ドキュメントを生成して」

## スクリプト

### run_codex.py

メインスクリプト。Codex CLIを実行するラッパー。

**機能**:

- プロジェクトルートの自動検出
- Codex CLIの実行
- 結果の整形と出力
- ログファイルの自動クリーンアップ（24時間経過で削除）

**使用方法**:

```bash
# 基本形式（プロジェクトルートから実行）
python .claude/skills/codex/scripts/run_codex.py "<request>"

# プロジェクトディレクトリを指定
python .claude/skills/codex/scripts/run_codex.py "<request>" --project-dir /path/to/project

# サンドボックスを無効化（慎重に使用）
python .claude/skills/codex/scripts/run_codex.py "<request>" --no-sandbox

# ログ保持時間をカスタマイズ（デフォルト: 24時間）
python .claude/skills/codex/scripts/run_codex.py "<request>" --max-age-hours 48
```

**注意点**:

- デフォルトで `--sandbox read-only` モードを使用（安全）
- 実行タイムアウトは10分に設定
- 大規模なプロジェクトでは時間がかかる可能性がある
- ログファイルは自動的にクリーンアップされる（24時間経過で削除）

## ログ管理

### ログファイルの保存場所

ログファイルは `.claude/skills/codex/logs/` ディレクトリに保存されます。

ファイル名形式: `codex_YYYYMMDD_HHMMSS.md`

### 自動クリーンアップ

スクリプト実行後、自動的に古いログファイルが削除されます:

- **デフォルト**: 24時間経過したログを削除
- **カスタマイズ**: `--max-age-hours` オプションで調整可能

**使用例**:

```bash
# 12時間経過したログを削除
python .claude/skills/codex/scripts/run_codex.py "Review code" --max-age-hours 12

# クリーンアップを無効化（0を指定）
python .claude/skills/codex/scripts/run_codex.py "Review code" --max-age-hours 0
```

### クリーンアップのログ出力

削除されたファイルは標準エラー出力に記録されます:

```
[CLEANUP] Removed codex_20260115_143022.md (age: 28.5 hours)
[CLEANUP] Removed codex_20260114_091545.md (age: 52.3 hours)
[CLEANUP] Removed 2 old log file(s)
```

## リファレンス

### usage_guide.md

Codex CLIの使用方法とオプションの詳細。

**内容**:

- 基本的なコマンド構造
- 利用可能なオプション一覧
- サンドボックスモードの説明
- ベストプラクティス
- 制限事項

参照タイミング:
- コマンドオプションを確認したいとき
- サンドボックスモードの使い方を知りたいとき
- トラブルシューティングが必要なとき

### request_patterns.md

効果的なCodexリクエストのテンプレート集。

**内容**:

- コードレビューパターン
- バグ調査パターン
- リファクタリングパターン
- セキュリティレビューパターン
- 学習・理解パターン
- 言語別パターン（Python, JavaScript/TypeScript, Go）

参照タイミング:
- 効果的なリクエストを作成したいとき
- 特定の目的に合ったテンプレートを探しているとき
- 過去に成功したリクエストパターンを参照したいとき

## ワークフロー

### 典型的なコードレビューフロー

1. ユーザーが「レビューして」と依頼
2. レビューの目的と範囲を確認
3. `request_patterns.md` から適切なテンプレートを選択
4. `run_codex.py` を実行
5. 結果を要約してユーザーに報告

### 典型的なバグ調査フロー

1. ユーザーが問題を報告
2. 再現手順やエラーメッセージを詳細に聞き出す
3. `request_patterns.md` の調査パターンを参照
4. Codexで根本原因を調査
5. 調査結果と修正提案を提示

### 典型的なアーキテクチャ分析フロー

1. ユーザーが「分析して」と依頼
2. 分析の焦点（パフォーマンス、スケーラビリティなど）を確認
3. 適切な分析パターンを使用してCodexを実行
4. 結果を解釈し、改善提案をまとめる

## 制約と注意点

### Codex CLIの要件

- **前提**: Codex CLIがインストールされている必要があります
- **パス**: `codex` コマンドがPATHに含まれている必要があります
- **バージョン**: 最新バージョンの使用を推奨

### 実行環境

- **プロジェクトディレクトリ**: デフォルトでカレントディレクトリのプロジェクトルートを自動検出
- **サンドボックス**: デフォルトで読み取り専用モード（安全）
- **タイムアウト**: 10分に設定（大規模プロジェクト向け）

### 制限事項

- 大規模なコードベースでは時間がかかる可能性がある
- 読み取り専用サンドボックスではファイルを変更できない
- 実行時間はプロジェクトサイズとリクエストの複雑さに依存

## ベストプラクティス

1. **具体的なリクエスト**: 曖昧な表現を避け、具体的に
   - 良い例: 「認証モジュールのSQLインジェクション脆弱性をレビュー」
   - 悪い例: 「コードをレビュー」

2. **コンテキストの提供**: 分析範囲を明示
   - 「APIエンドポイントのエラーハンドリングを確認」
   - 「ユーザー認証フローで...」

3. **読み取り優先**: 最初は必ず `--sandbox read-only` を使用
   - ファイルの誤変更を防止
   - 本番コードベースでの安全な分析

4. **反復的アプローチ**:
   - 最初は広範なリクエスト
   - 結果に基づいて特定の領域を深掘り
   - フォローアップ質問で詳細を取得

## 拡張

### 新しいリクエストパターンの追加

`references/request_patterns.md` に新しいパターンを追加できます:

1. 成功したリクエストを記録
2. テンプレートとしてドキュメント化
3. カテゴリー別に整理

### スクリプトのカスタマイズ

`scripts/run_codex.py` は拡張可能です:

- 異なるサンドボックスモードのサポート
- 結果のフォーマット変更
- 追加の前処理/後処理ロジック
- 結果のキャッシング

## トラブルシューティング

### Codex CLIが見つからない

```
Error: Codex CLI not found. Please ensure it is installed and in your PATH.
```

**解決策**:
- Codex CLIがインストールされているか確認: `which codex`
- インストール手順: Codexの公式ドキュメントを参照

### 実行タイムアウト

```
Error: Codex execution timed out after 10 minutes
```

**解決策**:
- より具体的なリクエストに変更
- 特定のディレクトリに焦点を当てる
- プロジェクトの一部を分析

### パーミッションエラー

**解決策**:
- プロジェクトディレクトリの読み取り権限を確認
- `.git` ディレクトリにアクセス可能か確認

## 関連スキル

このスキルは以下のタスクに適しています:

- **code-review**: より詳細なコードレビューが必要な場合
- **stepwise-executor**: 段階的な問題解決が必要な場合
- **refactoring-expert**: リファクタリングの専門的な支援が必要な場合
