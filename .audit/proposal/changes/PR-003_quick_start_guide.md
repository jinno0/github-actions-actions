# PR-003: 15分で試せるクイックスタートガイドの作成

**優先度**: Medium (P2)
**作業規模**: Low (2-3日)
**依存関係**: なし

## 背景

**※この提案はASM-001（ターゲットユーザー）という仮定に基づいています**

- 現在のinstructions/は個別のActionの導入には役立つが、「全体像を把握して手軽に試す」用途には不親切
- ADOPTION_GUIDE.mdは組織全体での導入を想定しており、個人の試し使いにはハードルが高い
- 「まずは自分のリポジトリで何か一つ試してみたい」というユーザーのニーズに応えられていない
- 最もシンプルなAction（auto-merge等）の15分チュートリアルがあれば、導入障壁が大きく下がる

## 現状の問題点

1. **どこから始めればよいか分からない**: 13個のActionが並んでおり、初心者はどれから試すべきか迷う
2. **試行に時間がかかりすぎる**: self-hosted runnerのセットアップから始める必要がある
3. **成功体験を得られない**: 一つ試すまでに数時間要し、途中で挫折する可能性

## 提案する改善アクション

### ドキュメント構成の追加 (2日)

**QUICKSTART.md**の新規作成:

```markdown
# 15分で試す AI Actions クイックスタート

このガイドでは、最もシンプルな **auto-merge** Action を使って、
15分でAI Actionsの体験を試してみましょう。

## 前提条件

- GitHubアカウントがあること
- **Self-hosted runner** が設定済みであること
  （[詳細なセットアップ手順](./AGENTS.md#実行環境と-claude-code-cli)）

## Step 1: 試すリポジトリを準備 (3分)

まずは練習用に新しいリポジトリを作成しましょう:

1. GitHubで新しいリポジトリを作成（名前は何でもOK）
2. ローカルにクローン:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

## Step 2: auto-merge Actionを追加 (5分)

1. `.github/workflows/` ディレクトリを作成:
   ```bash
   mkdir -p .github/workflows
   ```

2. [examples/auto-merge.yml](../examples/auto-merge.yml) をコピー:
   ```bash
   # このリポジトリからコピー
   cp path/to/github-actions-actions/examples/auto-merge.yml \
      .github/workflows/auto-merge.yml
   ```

3. 中身を確認:
   ```yaml
   name: Auto Merge PRs
   on:
     pull_request:
         # ここで設定を確認
   ```

## Step 3: 動作を確認 (7分)

1. 変更をコミット:
   ```bash
   git add .github/workflows/auto-merge.yml
   git commit -m "Add auto-merge workflow"
   git push
   ```

2. PRを作成:
   - GitHubで「Pull request」をクリック
   - 適当なタイトルを入力（例: "Test auto-merge"）
   - 「Create pull request」をクリック

3. 自動マージを待つ:
   - PRが作成されると、自動的に `auto-merge` workflow が実行されます
   - 条件を満たしていれば、PRが自動的にマージされます

4. 結果を確認:
   - PRの「Checks」タブでworkflowの実行結果を確認
   - マージされていれば成功！ 🎉

## Step 4: 次のActionに挑戦 (5分)

成功したら、次はもっと高度なActionを試してみましょう:

- [**review-and-merge**](./instructions/review-and-merge.md): AIがコードをレビューして自動マージ
- [**auto-document**](./instructions/auto-document.md): コード変更を検知してREADMEを自動更新
- [**spec-to-code**](./instructions/spec-to-code.md): Markdown仕様書からコードを生成

## トラブルシューティング

### Q: workflowが実行されない
A: Self-hosted runnerがオンラインになっているか確認してください

### Q: PRが自動マージされない
A: auto-mergeの条件（CIパス、承認数など）を確認してください

### Q: もっと詳しく知りたい
A: [ADOPTION_GUIDE.md](./ADOPTION_GUIDE.md) で組織全体での導入手順を確認してください

## フィードバックをお待ちしています！

クイックスタートで分かりにくい点があれば、Issueを立ててください:
https://github.com/YOUR_ORG/github-actions-actions/issues
```

### 簡易版auto-mergeワークフローの作成 (1日)

**examples/auto-merge-simple.yml**の新規作成:

```yaml
name: Quick Start - Auto Merge

on:
  pull_request:
    types: [labeled, unlabeled, opened, synchronize, reopened]

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: self-hosted  # Self-hosted runnerで実行

    steps:
      - name: Check if PR should be auto-merged
        id: check
        run: |
          # 簡易版: 単純な条件で自動マージ
          if [[ "${{ github.event.label.name }}" == "auto-merge" ]]; then
            echo "should_merge=true" >> $GITHUB_OUTPUT
          fi

      - name: Auto-merge PR
        if: steps.check.outputs.should_merge == 'true'
        run: |
          gh pr merge ${{ github.event.pull_request.number }} \
            --squash \
            --subject "Auto-merge ${{ github.event.pull_request.title }}" \
            --body "Automatically merged by quick-start action"
        env:
          GH_TOKEN: ${{ github.token }}
```

## 成功基準

- [ ] QUICKSTART.mdが作成されている
- [ ] ドキュメントに沿って15分以内にauto-mergeが試せる
- [ ] トラブルシューティングセクションで主要な問題をカバーしている
- [ ] 次のステップ（他のAction）への導線がある

## リスクと副作用

### リスク
- **情報の陳腐化**: Actionsの仕様変更に合わせて頻繁に更新が必要
  - **緩和策**: 本ドキュメントは「auto-merge」にフォーカスし、変更頻度を低くする

### 副作用
- **サポート負荷の増加**: クイックスタートを試すユーザーからの問い合わせ増
  - **許容範囲**: 採用数の増加によるメリットが上回る

## 今後の改善

- [ ] ビデオチュートリアルの作成（スクリーンキャスト）
- [ ] インタラクティブなチュートリアル（GitHub Codespaces対応）
- [ ] 多言語対応（英語版）

## 参考資料

- GAP-005: ドキュメント親切性の不足
- SOL-005-1: クイックスタートガイドの作成
- examples/auto-merge.yml: 既存のauto-mergeワークフロー
