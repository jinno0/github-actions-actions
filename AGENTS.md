# AGENTS.md - AIエージェントへの指示

このファイルは、AIエージェント（Claude Code等）がこのリポジトリで作業する際に最初に読むべき指示です。

## 実行環境と Claude Code CLI

このリポジトリにおける複雑なロジックや高度な自動化タスク（例：PRの自動レビューやコードの自動修正）は、**self-hosted runner 上で動作する Claude Code CLI (`claude` コマンド)** によって処理されることを前提としています。

- **実装例**: `actions/review-and-merge/action.yml` では、GitHub Actions から `claude` コマンドを呼び出して PR のレビューと自動マージを行っています。
- **権限**: self-hosted runner 上で実行されるため、ファイルシステムへのアクセスや外部コマンドの実行が許可されています。

## 自動埋め込み仕組み（重要）

AIエージェントは、タスク実行時に**最新のプロジェクト情報が自動的にプロンプトに埋め込まれます**：

### 埋め込まれる情報

1. **PURPOSE.mdの最新セクション**（現在のステータス、最大50行）
   - 「現在のステータス」セクションを自動抽出
   - プロジェクトの現在のフェーズ・優先順位を把握

2. **TASKS.mdの最新N行**（最新50行）
   - 今日〜今週のTODO・メモを自動抽出
   - 現在の作業コンテキストを把握

3. **仕組み**: `tools/harness/run_task.py` が実行時に読み込んでプロンプトに埋め込みます

### メリット

- ✅ **プロンプト肥大化防止**: 全文ではなく「必要な部分だけ」埋め込み
- ✅ **常に最新情報**: 実行時に動的に読み込むので、古い情報を見る心配がない
- ✅ **WORKTREE問題解決**: TASKS.mdがworktreeにない場合でも、内容を伝達可能
- ✅ **スリム化**: 過去の情報は埋め込みず、現在の情報だけに集中

## 必読ファイル（この順で読むこと）

自動埋め込みに加えて、以下のファイルも直接読んでください。

### 1. PURPOSE.md（必須・全文）

- **内容**: このプロジェクトの大目標・非目標・成功条件・今期の優先順位
- **目的**: プロジェクトの全体像と方向性を理解する（プロンプトには最新セクションのみ埋め込み）
- **更新頻度**: 低（月に1回〜数ヶ月に1回）
- **位置**: リポジトリルート

### 2. TASKS.md（推奨・全文）

- **内容**: 今日〜今週の細かいToDo・メモ・コマンド履歴
- **目的**: 現在の作業コンテキストと優先順位を理解する（プロンプトには最新50行のみ埋め込み）
- **注意**: 存在しない場合は無視してOK（ローカルファイル）
- **更新頻度**: 高（毎日〜毎週）
- **位置**: リポジトリルート（.gitignore済み）

### 3. SYSTEM_CONSTITUTION.md（必須）

- **内容**: Layer0: 憲法（変更不可の絶対ルール）
- **目的**: 何が禁止されているか、何が必須かを理解する
- **更新頻度**: 極低（基本的に不変）

### 4. hub/runtime.yml（必須）

- **内容**: 実行設定（時間上限、テストコマンド）
- **目的**: 実行時の制約を理解する

### 5. hub/policy/policy.current.md（必須）

- **内容**: コーディング方針（進化対象）
- **目的**: どの順序で作業するか、何を優先するかを理解する
- **更新頻度**: 中（評価結果に基づいて更新）

### 6. README.md（推奨）

## 読み込み時の注意点

1. **PURPOSE.mdを最優先**: このプロジェクトの「なぜ」「何を」「どう」を理解する
2. **TASKS.mdは補助**: 現在の優先順位を把握するだけ（詳細はPURPOSE.mdを参照）
3. **憲法は絶対**: SYSTEM_CONSTITUTION.md のルールは破ってはならない

## タスク実行時のワークフロー

AIエージェントがタスクを実行する際は、以下の手順を守ってください：

1. **コンテキスト理解**
   - PURPOSE.md を読む（大目標・今期の優先順位）
   - TASKS.md を読む（現在のTODO・制約）
   - SYSTEM_CONSTITUTION.md を読む（絶対ルール）

2. **方針決定**
   - hub/policy/policy.current.md を参照
   - 「テスト優先か実装優先か」「どこから触るか」を決定

3. **実行**
   - hub/templates/prompt_task.md に従って作業
   - 最小差分で変更を加える

4. **検証**
   - テストを実行
   - 変更内容を要約

5. **出力**
   - Summary, Decision trace, Files changed, Test result を記録

## 人間へのフィードバック

AIエージェントは以下の場合に人間に報告してください：

- PURPOSE.md に矛盾するタスクが与えられた場合
- TASKS.md に記載された制約とタスクが競合する場合
- SYSTEM_CONSTITUTION.md に違反する変更を求められた場合


# GitHub Actions 開発ノウハウ

このリポジトリで GitHub Actions を開発・保守する際のノウハウとベストプラクティスです。

## テンプレートファイルの切り出し方

action.yml 内にプロンプトや文章をハードコーディングするのではなく、テンプレートファイルとして切り出します。

### 背景

- **メンテナンス性**: 文章修正時に action.yml を編集する必要がなくなる
- **カスタマイズ性**: ユーザーが独自テンプレートを提供できる
- **可読性**: action.yml がスッキリし、ロジックと文章が分離される

### 実装パターン

#### 1. テンプレートファイルの作成

`actions/{action-name}/templates/{prompt_name}.txt` を作成：

```
actions/review-and-merge/templates/review_prompt.txt
```

プレースホルダーには `{VARIABLE_NAME}` 形式を使用：

```text
You are reviewing a GitHub Pull Request.

PR Number: {PR_NUMBER}
PR Title: {PR_TITLE}

Verdict: {VERDICT}
```

#### 2. action.yml での input 定義

```yaml
inputs:
  prompt-template:
    description: 'Path to custom prompt template (optional, uses built-in template if not specified)'
    required: false
    default: ''
```

#### 3. action.yml での使用

```yaml
run: |
  PROMPT_TEMPLATE="${{ inputs.prompt-template }}"

  # Use custom template if provided, otherwise use built-in
  if [ -n "$PROMPT_TEMPLATE" ] && [ -f "$PROMPT_TEMPLATE" ]; then
    TEMPLATE_FILE="$PROMPT_TEMPLATE"
  else
    TEMPLATE_FILE="${{ github.action_path }}/templates/review_prompt.txt"
  fi

  # Read template and replace placeholders
  PROMPT=$(sed -e "s/{PR_NUMBER}/$PR_NUMBER/g" \
              -e "s/{PR_TITLE}/$PR_TITLE/g" \
              -e "s/{VERDICT}/$VERDICT/g" \
              "$TEMPLATE_FILE")

  echo "$PROMPT" > /tmp/final_prompt.txt
```

### セキュリティ上の注意

プレースホルダー置換には `sed` を使用しています。ユーザー入力をテンプレートに埋め込む場合は、コマンドインジェクションを防ぐため、以下の点に注意：

1. **変数は二重引用符で囲む**: `"$VARIABLE"`
2. **特殊文字のエスケープが必要な場合は検討する**
3. **外部入力はバリデーションする**

## YAML 構文の注意点

### 避けるべきパターン: heredoc

**❌ 良くない例:**

```yaml
run: |
  cat << EOF > /tmp/prompt.txt
You are reviewing code.
PR: $PR_NUMBER
EOF
```

**問題点:**
- YAML パーサーによってはインデントが厳密になりエラーになる
- YAML 内の `|` (literal style scalar) と bash の heredoc が干渉する

**✅ 良い例:**

```yaml
run: |
  echo 'You are reviewing code.' > /tmp/prompt.txt
  echo "PR: $PR_NUMBER" >> /tmp/prompt.txt
```

または、テンプレートファイルを使用：

```yaml
run: |
  sed -e "s/{PR_NUMBER}/$PR_NUMBER/g" \
      "${{ github.action_path }}/templates/prompt.txt" > /tmp/final.txt
```

### プレースホルダーの命名規則

- **中括弧を使用**: `{VARIABLE_NAME}`
- **大文字スネークケース**: `{SOURCE_PATH}`, `{DOC_PATH}`
- **説明的な名前**: `{CURRENT_CONTENT}` ではなく `{FILE_CONTENT}`

## 既存の実装例

以下の action でテンプレートファイルを使用しています：

| Action | テンプレートファイル | プレースホルダー例 |
|--------|---------------------|-------------------|
| `action-fixer` | `templates/fix_prompt.txt` | `{FILE}`, `{ISSUES}`, `{CURRENT_CONTENT}` |
| `auto-document` | `templates/doc_prompt.txt` | `{SOURCE_PATH}`, `{DOC_PATH}` |
| `auto-refactor` | `templates/refactor_prompt.txt` | `{TARGET_PATH}`, `{INSTRUCTION}` |
| `release-notes-ai` | `templates/release_prompt.txt` | `{GIT_LOG}`, `{PRS}`, `{OUTPUT}` |
| `review-and-merge` | `templates/review_prompt.txt`, `templates/comment_template.txt` | `{VERDICT}`, `{CONFIDENCE}`, `{SUMMARY}` |
| `spec-to-code` | `templates/gen_prompt.txt` | `{LANG}`, `{SPEC_CONTENT}`, `{OUTPUT_DIR}` |

## 新しい action を作成する際の手順

1. **テンプレートファイルの作成**
   ```bash
   mkdir -p actions/new-action/templates
   # actions/new-action/templates/prompt.txt を作成
   ```

2. **action.yml の作成**
   - inputs に `{template-name}-template` を追加
   - `run:` ブロックでテンプレート読み込みロジックを実装

3. **YAML 構文チェック**
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('actions/new-action/action.yml'))"
   ```

4. **テンプレート置換のテスト**
   ```bash
   # プレースホルダー置換が正しく動作するか確認
   sed -e "s/{VAR}/value/g" template.txt
   ```

## 参考リソース

- [GitHub Actions: Composite actions](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- [YAML仕様](https://yaml.org/spec/)
- 既存の実装: `actions/review-and-merge/` が参考実装

## Action構造標準（Standard Action Structure）

新しい Action を作成または既存の Action を整備する際は、必ず以下の3つの構成要素をセットで用意してください。これにより、開発者と利用者の双方がスムーズに利用できるようになります。

### 1. Action 実装 (`actions/{name}/`)
- **`action.yml`**: Action の定義ファイル。
- **`templates/`**: プロンプトや通知メッセージのテンプレートファイル。`.yml` にハードコーディングせず、必ずここから読み込むこと。

### 2. 利用例 (`examples/{name}-example.yml`)
- ユーザーがコピー＆ペーストしてすぐに使える完全なワークフローファイル。
- `examples/` ディレクトリ直下に配置する。
- 必要な `permissions` や `runs-on: self-hosted` を明記すること。

### 3. 利用ガイド (`instructions/{name}.md`)
- `examples/` のワークフローを参照し、セットアップ手順を解説するドキュメント。
- `instructions/` ディレクトリ直下に配置する。
- 以下の項目を含めること：
    - **Prerequisites**: 前提条件（Runner, Token権限など）
    - **Setup Instructions**: 具体的な導入手順
    - **Usage**: 使い方やトリガーの説明

### 構成例

```text
root/
├── actions/
│   └── my-awesome-action/
│       ├── action.yml
│       └── templates/
│           └── prompt.txt
├── examples/
│   └── my-awesome-action-example.yml
└── instructions/
    └── my-awesome-action.md
```

### 自動化ルール
AIエージェントは、Action を新規作成または大幅に修正した場合、上記の `examples/` と `instructions/` も同期して更新（または作成）しなければならない。

## Dry Run 検証（Testing）

このリポジトリでは、すべての Action が **Dry Run モード** で自動検証されます。

### CI による自動検証

`.github/workflows/test-all-actions.yml` が以下のタイミングで実行されます：

- **PR 作成時**: `actions/**/*.yml` や `actions/**/templates/**` を変更した場合
- **Main ブランチへの Push**: 変更をマージした場合
- **手動実行**: GitHub Actions の UI から特定の Action または全 Action をテスト可能

### 検証内容

Dry Run テストでは以下を検証します：

1. **構造チェック**:
   ```bash
   # action.yml が存在するか
   # templates/*.txt が存在するか
   # examples/{name}-example.yml が存在するか
   # instructions/{name}.md が存在するか
   ```

2. **YAML 構文チェック**:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('action.yml'))"
   ```

3. **モック実行**:
   - Claude CLI をモック化（`/usr/local/bin/claude` にシミュレーションスクリプトを配置）
   - Action の実行フローをシミュレート
   - 実際の commit/push は行わない

### Dry Run の実装方法

各 Action は、Dry Run 時に以下の動作を期待されます：

- **検証モード検出**: 環境変数 `DRY_RUN=true` をチェック（実装推奨）
- **commit/push のスキップ**: 実際の Git 操作は行わない
- **ログ出力**: 実行するであろう操作をログに出力

例（action.yml での実装パターン）：

```yaml
run: |
  DRY_RUN="${{ inputs.dry-run }}"

  if [ "$DRY_RUN" = "true" ]; then
    echo "[DRY RUN] Would commit: $COMMIT_MSG"
    echo "[DRY RUN] Would push to: $BRANCH"
  else
    git add .
    git commit -m "$COMMIT_MSG"
    git push
  fi
```

### ローカルでのテスト

PR を作成する前に、以下のコマンドでローカルテストを実行してください：

```bash
# 1. YAML 構文チェック
find actions -name 'action.yml' -exec python3 -c "import yaml; yaml.safe_load(open('{}'))" \;

# 2. 構造チェック
for action in actions/*/; do
  name=$(basename "$action")
  echo "Checking $name:"
  echo "  action.yml: $([ -f "$action/action.yml" ] && echo '✓' || echo '✗')"
  echo "  templates/: $(ls "$action/templates/" 2>/dev/null | wc -l) files"
  echo "  example: $([ -f "examples/${name}-example.yml" ] && echo '✓' || echo '✗')"
  echo "  instruction: $([ -f "instructions/${name}.md" ] && echo '✓' || echo '✗')"
done

# 3. プレースホルダーの検証（オプション）
grep -r "{[A-Z_]*}" actions/*/templates/ --color=always
```

### CI で検証が失敗した場合

1. **ログを確認**: どのステップで失敗したか確認
2. **エラーメッセージを読む**: YAML 構文エラーやファイル不在エラーを修正
3. **ローカルで再現**: 上記のコマンドで同じエラーを再現
4. **修正して Push**: 修正後、CI が再実行されます

### 新しい Action を追加する際のチェックリスト

Action を新規作成した場合、以下を確認してください：

- [ ] `actions/{name}/action.yml` が存在し、YAML 構文が正しい
- [ ] `actions/{name}/templates/*.txt` が存在する
- [ ] `examples/{name}-example.yml` が存在し、`runs-on: self-hosted` を含む
- [ ] `instructions/{name}.md` が存在し、Prerequisites/Setup/Usage を含む
- [ ] プレースホルダーが `{VARIABLE_NAME}` 形式で統一されている
- [ ] heredoc (`<< EOF`) を使用していない
- [ ] CI がパスすることを確認（GitHub Actions のログを確認）
