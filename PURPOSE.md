# AI Hub - PURPOSE

## Mission (Mission)

組織全体の開発効率と品質を向上させるための「AIネイティブなGitHub Actions」および「標準化ツール」を提供するハブとなること。
特に、**Self-hosted runner上で動作するClaude Code CLI**を活用し、従来の正規表現や静的解析では不可能な、文脈を理解した高度な自動化（レビュー、修正、ドキュメント生成など）を実現する。

## Current Status (2026-01-17)

### Phase 1: Foundation & POC
- ✅ Self-hosted runner + Claude Code CLI の基本動作検証完了 (`review-and-merge`)
- ✅ 基本的なActions Lint/Fixの提供 (`action-fixer`)

## Core Competencies

1.  **AI-Powered Automation**
    - Claude Code CLIを活用し、コードの意味を理解した処理を行う。
    - コンテキスト（関連ファイル、履歴）を踏まえた判断。
2.  **Self-hosted Advantage**
    - コンテナ外のツールチェーンやリソースへの柔軟なアクセス。
    - コスト効率とパフォーマンスの最適化。
3.  **Human-in-the-Loop**
    - AIはあくまで提案・準備を行い、最終決定権（マージ、デプロイ）は人間が持つ、または人間が設定した閾値に基づく。

## Action Candidates (Roadmap)

### 1. Development Support
- **`review-and-merge`** (Existing)
    - PRの内容をAIがレビューし、LGTMなら自動マージ。
    - 改善点: レビュー精度の向上、カスタムルールの注入機能。
- **`spec-to-code`** (Proposed)
    - Issueや仕様書（Markdown）から、雛形コードやテストコードを生成する。

### 2. Maintenance & Quality
- **`action-fixer`** (Existing -> Enhanced)
    - 現状: 静的解析によるWorkflowファイルの修正。
    - 将来: エラーログを解析し、AIが修正パッチを提案する機能の追加。
- **`auto-refactor`** (Proposed)
    - 指定されたファイルやディレクトリに対して、可読性向上や最新構文への書き換えをAIが実行。
    - Trigger: `refactor` ラベル付与やコメントコマンド `/refactor`。

### 3. Documentation
- **`auto-document`** (Proposed)
    - コードの変更を検知し、READMEやAPIドキュメント、JSDoc/Docstringを自動更新・生成。
- **`release-notes-ai`** (Proposed)
    - コミットログとPRの内容をAIが要約し、わかりやすいリリースノートを生成。

## 非目標（What we are NOT）

- ❌ 単なるシェルスクリプトのラッパー（既存のActionsで十分なもの）
- ❌ 完全に無人での運用（AIのハルシネーションリスクを考慮）
- ❌ 特定プロダクトに強く結合しすぎたロジック（再利用性を重視）

## 成功条件

- ✅ 組織内の複数のリポジトリでこれらのActionsが採用される。
- ✅ 「AIに任せられる雑務」が増え、人間が本質的な設計や意思決定に集中できる時間が増加する。
- ✅ AIの提案に対する修正率（Acceptance Rate）が向上し続ける。