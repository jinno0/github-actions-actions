# Auto Document Action

## 概要

`auto-document` は、Claude Code CLI を使用してコード変更に基づき自動的にドキュメントを更新する GitHub Action です。

## 機能

- ソースコードの分析に基づくドキュメントの自動更新
- カスタムプロンプトテンプレートのサポート
- 柔軟なソースパス・ドキュメントパスの指定

## Setup

1. **Copy Example Configuration**:
   Copy the workflow from [Auto Document Example](../examples/auto-document-example.yml).

2. **Configure your workflow**:
   Place the file in `.github/workflows/auto-document.yml`.

## 使用方法

### 基本的な使い方

```yaml
steps:
  - uses: ./actions/auto-document
    with:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 入力パラメータ

| パラメータ | 必須 | デフォルト値 | 説明 |
|-----------|------|-------------|------|
| `github-token` | ✓ | - | GitHub トークン |
| `source-path` | - | `.` | 分析対象のソースコードパス |
| `doc-path` | - | `README.md` | 更新対象のドキュメントパス |
| `claude-model` | - | `sonnet` | 使用する Claude モデル |
| `doc-prompt-template` | - | (組み込み) | カスタムプロンプトテンプレートのパス |

### 使用例

#### README.md の自動更新

```yaml
name: Update Documentation
on:
  push:
    branches: [main]

jobs:
  update-docs:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - uses: ./actions/auto-document
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          source-path: 'src/'
          doc-path: 'README.md'
```

#### カスタムテンプレートの使用

```yaml
steps:
  - uses: ./actions/auto-document
    with:
      github-token: ${{ secrets.GITHUB_TOKEN }}
      doc-prompt-template: '.github/templates/custom-doc-prompt.txt'
```

## 注意事項

- この Action は self-hosted runner 上で Claude Code CLI が利用可能であることを前提としています
- ドキュメントの更新内容は AI によって生成されるため、重要な変更については確認を推奨します
- カスタムテンプレートを使用する場合、`{SOURCE_PATH}` と `{DOC_PATH}` プレースホルダーを含める必要があります
