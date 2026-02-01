# PR-003: Add README for action-fixer

## Status
**Proposed** | **Impact**: High | **Effort**: Medium | **Time**: 30 minutes

## Problem Statement
The `action-fixer` action lacks a README file, making it difficult for users to:
- Understand what the action does
- Learn how to use it quickly
- Find examples and best practices

## Gap Analysis
- **Current State**: No README exists for action-fixer
- **Target State**: Comprehensive README following the template established in PR-001
- **Reference**: ASM-003, GAP-001

## Proposed Solution

### Files to Create
1. `actions/action-fixer/README.md`

### README Structure (based on PR-001 template)

```markdown
# Action Fixer

## 概要 (Overview)
AIがGitHub Actions Workflowのエラーを自動検知・修正するアクションです。

## 機能 (Features)
- YAML構文エラーの自動修正
- インデントの整形
- 非推奨構文の検出と修正提案
- Dry Runモードによる安全な検証

## 前提条件 (Prerequisites)
- Self-hosted runner上でClaude Code CLIが実行可能であること
- Workflowファイルへの書き込み権限

## 使用方法 (Usage)

### Basic Usage

\`\`\`yaml
name: Action Fixer
on:
  workflow_dispatch:
  push:
    paths:
      - '.github/workflows/**/*.yml'
      - '.github/workflows/**/*.yaml'

permissions:
  contents: write

jobs:
  fix-workflows:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Fix Workflow Errors
        uses: ./.github/actions/action-fixer
        with:
          workflow-path: '.github/workflows'
          dry-run: false
          auto-commit: true
\`\`\`

### Dry Run Mode

\`\`\`yaml
- name: Check Workflows (Dry Run)
  uses: ./.github/actions/action-fixer
  with:
    workflow-path: '.github/workflows'
    dry-run: true
\`\`\`

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| \`workflow-path\` | Yes | - | チェック対象のWorkflowファイルパス |
| \`dry-run\` | No | false | trueの場合、修正提案のみを行いファイルは変更しない |
| \`auto-commit\` | No | false | trueの場合、修正を自動コミットする |

## Outputs

| Output | Description |
|--------|-------------|
| \`fixes-applied\` | 適用した修正数 |
| \`errors-found\` | 検出したエラー数 |
| \`fixes-summary\` | 修正内容のサマリー |

## 詳細手順
詳細な導入手順については、[instructions/action-fixer.md](../../instructions/action-fixer.md)を参照してください。

## 使用例 (Examples)
[examples/action-fixer.yml](../../examples/action-fixer.yml)を参照してください。

## 注意事項
- **Commit権限が必要**: 修正を自動コミットする場合、\`permissions: contents: write\` が必要です
- **AIのハルシネーション**: 提案された修正をそのまま適用せず、必ず確認してください
- **バックアップ**: 大きな変更を適用する前に、ブランチのバックアップを作成してください

## トラブルシューティング

### 修正が適用されない
- \`permissions\` が正しく設定されているか確認してください
- \`workflow-path\` が正しいパスを指しているか確認してください

### Dry Runでエラーが出る
- YAMLファイルの構文が壊れている可能性があります
- 手動で構文を確認してください

## ライセンス
このプロジェクトの一部として、同じライセンスが適用されます。
```

## Expected Impact
- **Users**: Can quickly understand and adopt action-fixer
- **Documentation Coverage**: +7.7 percentage points (4→5/13)
- **Quality**: Consistent with existing READMEs

## Verification Plan
1. Create README.md file
2. Verify YAML examples are valid
3. Check all links work (instructions, examples)
4. Ensure consistency with PR-001 template

## Rollback Plan
```bash
git revert <commit-hash>
rm actions/action-fixer/README.md
```

## Related Issues
- GAP-001: Complete action documentation
- ASM-003: 100% documentation coverage target

## References
- instructions/action-fixer.md
- examples/action-fixer.yml
- actions/review-and-merge/README.md (template reference)
