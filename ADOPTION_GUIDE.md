# AI Actions 導入ガイド (Adoption Guide)

このガイドは、あなたのチーム/リポジトリで AI Actions を導入するための完全なロードマップを提供します。

> **Note**: このドキュメントには組織固有のプレースホルダーが含まれています（例: `your-org`、GitHub URL等）。
> 実際の値に置き換えてから使用してください。

---

## 📋 Prerequisites Checklist (導入前チェックリスト)

導入を開始する前に、以下の前提条件を確認してください。

### 環境要件
- [ ] **Self-hosted Runner が利用可能**
  - GitHub組織またはリポジトリで self-hosted runner が設定されていること
  - Runner は Linux 環境であること（推奨: Ubuntu 20.04+）

- [ ] **Claude Code CLI がインストール済み**
  - Self-hosted runner 上に Claude Code CLI がインストールされていること
  - 詳細: [AGENTS.md](./AGENTS.md#実行環境と-claude-code-cli)

- [ ] **必要な権限が設定済み**
  - GitHub Token に以下の権限があること:
    - `contents: read` (最小限)
    - `pull-requests: write` (PR操作を行う場合)
    - `issues: write` (Issue操作を行う場合)
  - 詳細: 各 Action の `instructions/` ドキュメントを参照

- [ ] **対象リポジトリが特定済み**
  - 最初のパイロット導入先リポジトリを決定していること
  - 推奨: 低リスクかつ頻繁に更新されるリポジトリ

---

## 🚀 Quick Start (5分間セットアップ)

まずは1つの Action を試すところから始めましょう。

### Step 1: Action を選択する

初めて導入する場合は、以下の「初心者向け」Actions から始めることを推奨します:

| Action | 難易度 | 推奨理由 | リスク |
|--------|--------|----------|--------|
| `release-notes-ai` | ⭐ 低 | コード変更なし、リリースノート生成のみ | なし |
| `action-fixer` | ⭐ 低 | 失敗時に通知のみ、自動修正は Dry Run | 低 |
| `review-and-merge` | ⭐⭐ 中 | AIレビュー+自動マージ、但しDry Run可能 | 中 |

### Step 2: ワークフローをコピーする

例: `release-notes-ai` を導入する場合

```bash
# examples ディレクトリからコピー
cp examples/release-notes-ai-example.yml .github/workflows/release-notes.yml
```

**代替案: パイロットテンプレートの使用**

初めて導入する場合は、パイロットワークフローテンプレートの使用を推奨します:

```bash
# パイロットテンプレートをコピー
cp examples/pilot-workflow-template.yml .github/workflows/ai-actions-pilot.yml
```

このテンプレートにはすべてのベストプラクティスと Dry Run モードが事前設定されています。

### Step 3: 必要な入力を設定する

コピーしたワークフローファイルを開き、以下を設定:

```yaml
- name: Generate Release Notes
  uses: ./actions/release-notes-ai
  with:
    # 必須: Claude モデル名
    claude-model: claude-sonnet-4-5-20250929

    # 必須: GitHub Token (自動的に提供される)
    github_token: ${{ secrets.GITHUB_TOKEN }}

    # オプション: リリースノートの言語
    language: japanese  # japanese | english
```

### Step 4: Dry Run モードで実行する

初回は **Dry Run** モード（実際には変更を保存しない）で動作確認:

```yaml
with:
  dry_run: true  # Dry Run モード有効化
```

### Step 5: 実行結果を確認する

1. GitHub リポジトリの「Actions」タブを開く
2. ワークフローの実行ログを確認
3. エラーなく完了することを確認

---

## 📖 Step-by-Step Integration (各Actionの詳細導入手順)

### 1. release-notes-ai (リリースノート自動生成)

**概要**: コミット履歴から人間が読みやすいリリースノートを生成

#### Prerequisites
- なし（最も導入しやすい Action）

#### Setup Instructions
1. `examples/release-notes-ai-example.yml` を `.github/workflows/` にコピー
2. ワークフロートリガーを設定（例: `release: types: [published]`）
3. `with.model` で使用する Claude モデルを指定
4. `with.language` でリリースノートの言語を指定

#### Verification Steps
1. テスト用リリースを作成
2. Actions タブでワークフローが実行されることを確認
3. 生成されたリリースノートを確認

#### Troubleshooting
- **問題**: リリースノートが生成されない
  - **解決**: トリガーが正しく設定されているか確認（`release:` vs `push:`）

---

### 2. action-fixer (Workflow エラー自動修正)

**概要**: Workflow のエラーを検知し、AI が原因を特定して修正案を生成

#### Prerequisites
- Runner にファイル書き込み権限が必要
- `contents: write` 権限を持つ GitHub Token

#### Setup Instructions
1. `examples/action-fixer-example.yml` を `.github/workflows/` にコピー
2. トリガーを設定（例: `workflow_run: workflows: ["*"]`）
3. `with.github_token` で Token を指定
4. **重要**: `dry_run: true` で最初はテスト

#### Verification Steps
1. 意図的にエラーを含むワークフローを実行
2. `action-fixer` が起動し、エラーを検知することを確認
3. Dry Run モードでは修正案がログに出力されることを確認

#### Troubleshooting
- **問題**: 修正案が生成されない
  - **解決**: エラーログが十分に出力されているか確認

---

### 3. review-and-merge (AIレビュー+自動マージ)

**概要**: AI がコードをレビューし、問題がなければ自動マージ（Auto-Fix 機能付き）

#### Prerequisites
- PR の作成・編集権限 (`pull-requests: write`)
- CI テストがパスしたことを確認できる仕組み

#### Setup Instructions
1. `examples/review-and-merge-example.yml` を `.github/workflows/` にコピー
2. トリガーを PR に設定（`pull_request_target:` 推奨）
3. `with.model`, `with.github_token` を設定
4. CI パス後に実行されるように設定（`needs: ci-test` など）

#### Verification Steps
1. テスト用 PR を作成
2. CI テストがパスした後、`review-and-merge` が実行されることを確認
3. AI レビューコメントが PR に投稿されることを確認
4. 問題がなければマージされることを確認（または Auto-Fix される）

#### Troubleshooting
- **問題**: AI レビューが実行されない
  - **解決**: トリガーが `pull_request:` ではなく `pull_request_target:` であることを確認

---

### 4. spec-to-code (仕様書からコード生成)

**概要**: Markdown 仕様書からコードを自動生成

#### Prerequisites
- 仕様書を配置するディレクトリ（例: `specs/`）
- 生成されたコードをコミットする権限

#### Setup Instructions
1. `examples/spec-to-code-example.yml` を `.github/workflows/` にコピー
2. 仕様書ディレクトリを `with.specs_dir` で指定
3. 生成コードの出力先を `with.output_dir` で指定
4. **重要**: 最初は `dry_run: true` で動作確認

#### Verification Steps
1. `specs/` ディレクトリにテスト用仕様書を作成
2. ワークフローを実行
3. 生成されたコードを確認（Dry Run モードではログに表示）

#### Troubleshooting
- **問題**: 期待したコードが生成されない
  - **解決**: 仕様書のフォーマットが正しいか確認（テンプレート参照）

---

## 🧪 Pilot Implementation Guide (パイロット導入ガイド)

### Phase 1: パイロット計画 (1週間前)

1. **パイロットチームの選定**
   - 推奨: 3〜5人の開発チーム
   - 特性: 実験的変更にオープンなチーム

2. **パイロットActionの選定**
   - 初回: `release-notes-ai` または `action-fixer` (Dry Run)
   - 条件: 低リスクで効果が見えやすいもの

3. **成功指標の定義**
   - テスト導入前: 手動で作成していたリリースノートの作成時間
   - テスト導入後: AI 生成による時間短縮
   - 目標: 50%以上の時間短縮

### Phase 2: パイロット実行 (1〜2週間)

1. **週次ミーティング**で進捗確認
   - 問題発生の有無
   - チームからのフィードバック

2. **メトリクス収集**
   - ワークフロー実行回数
   - 成功/失敗回数
   - チームの満足度（1〜5段階評価）

### Phase 3: 結果評価と判断

| 成功率 | アクション |
|--------|----------|
| 80%以上 満足 | 全チームへ展開 |
| 50-80% 満足 | 改善後に全展開 |
| 50%未満 満足 | 問題分析、再設計 |

---

## ✅ Rollout Checklist (本番展開チェックリスト)

パイロットが成功したら、組織全体に展開します。

### チーム準備
- [ ] チームトレーニング実施済み
  - [ ] AI Actions の概要説明
  - [ ] 各 Action の使い方ハンズオン
  - [ ] トラブルシューティング方法共有

### 技術準備
- [ ] 全 Actions が Staging 環境でテスト済み
- [ ] 本番環境向けの設定値が決定済み
  - [ ] 使用する Claude モデル
  - [ ] Dry Run モードの有無
  - [ ] 通知先（Slack, Email など）

### リスク管理
- [ ] ロールバック計画が文書化済み
  - [ ] 各 Action を無効化する手順
  - [ ] 問題発生時のエスカレーション先
- [ ] 成功メトリクスが定義済み
  - [ ] 導入前後のベンチマーク
  - [ ] 定期的なレビュー予定

---

## 🔧 Troubleshooting (トラブルシューティング)

### 一般的な問題

#### 1. ワークフローが実行されない

**症状**: Actions タブにワークフローが表示されない

**原因**:
- ファイルが `.github/workflows/` に配置されていない
- YAML 構文エラー

**解決策**:
```bash
# 構文チェック
find .github/workflows -name "*.yml" -exec yamllint {} \;

# パス確認
ls -la .github/workflows/
```

#### 2. Claude Code CLI が見つからない

**症状**: `claude: command not found`

**原因**: Self-hosted runner に Claude Code CLI がインストールされていない

**解決策**:
```bash
# Runner にログインしてインストール
npm install -g @anthropic-ai/claude-code
```

#### 3. 権限エラー

**症状**: `Resource not accessible by integration`

**原因**: GitHub Token の権限不足

**解決策**:
1. リポジトリの Settings > Actions > General に移動
2. Workflow permissions で "Read and write permissions" を選択
3. 必要に応じて "Allow GitHub Actions to create pull requests" を有効化

### Action 固有の問題

#### release-notes-ai
- **問題**: リリースノートが空
  - **解決**: 対象期間にコミットがあるか確認

#### action-fixer
- **問題**: 誤検知（エラーがないのにエラーとみなす）
  - **解決**: `with.ignore_patterns` で無視するパターンを指定

#### review-and-merge
- **問題**: AI レビューが厳しすぎる
  - **解決**: `with.review_temperature` を調整（0.0〜1.0）

---

## 📞 How to Get Help (サポート)

### 問題報告

1. **既知の問題**: [GitHub Issues](https://github.com/your-org/github-actions-actions/issues)
2. **新規問題**: Issue テンプレートを使用して報告

### コンタクト

- **メンテナ**: [PURPOSE.md](./PURPOSE.md) を参照
- **Slackチャンネル**: `#ai-actions-support` (組織内)

### フィードバック

改善提案や機能リクエストは以下から:
- GitHub Discussions: [ディスカッションフォーラム]
- または、Pull Request を直接送信

---

## 📚 Additional Resources (追加資料)

- [AGENTS.md](./AGENTS.md) - 開発者向け詳細ガイド
- [PURPOSE.md](./PURPOSE.md) - プロジェクトの目的とロードマップ
- [examples/](./examples/) - 全 Action の利用例
- [instructions/](./instructions/) - 各 Action の詳細ドキュメント

---

## 📊 Adoption Registry (導入登録簿)

This registry tracks the adoption of AI Hub Actions across the organization.

### 統計 (Statistics)

- **Total Teams**: 0
- **Total Repositories**: 0
- **Most Used Actions**: TBD (awaiting adoption data)

### 導入チーム (Using Teams)

#### Team Template

- **Since**: YYYY-MM-DD
- **Repositories**: X
- **Actions in Use**:
  - action-name-1
  - action-name-2
- **Feedback**: Describe the team's experience (positive/negative/neutral)

*No teams have registered yet. Be the first to adopt AI Hub Actions!*

### ロールアウトタイムライン (Rollout Timeline)

| Date | Team | Repositories | Actions |
|------|------|--------------|---------|
| *Awaiting first adoption* | - | - | - |

### チーム登録方法 (How to Register Your Team)

To add your team to this registry:

1. Edit this file (`ADOPTION_GUIDE.md`)
2. Add your team information to the "導入チーム (Using Teams)" section
3. Update the statistics and timeline
4. Submit a PR with your changes

#### プライバシーオプション (Privacy Options)

Teams can choose their level of visibility:

- **Public**: Team name, repository names, and feedback visible
- **Anonymous**: Team identified as "Team X" with repository names omitted
- **Private**: Data used for statistics only, not individually listed

### フィードバック要約 (Feedback Summary)

#### Positive Aspects

*Awaiting user feedback*

#### Areas for Improvement

*Awaiting user feedback*

#### Common Use Cases

*Awaiting adoption data*

### 成功指標 (Success Metrics)

This registry helps track:

1. **Organizational Reach**: How many teams are using AI Hub Actions
2. **Action Popularity**: Which actions are most widely adopted
3. **User Satisfaction**: Collective feedback and experiences
4. **Impact Assessment**: Development workflow improvements

---

**Last Updated**: 2026-02-02
**Update Frequency**: Monthly or as new teams adopt
**Registry Maintainer**: TBD
**バージョン**: 1.0
