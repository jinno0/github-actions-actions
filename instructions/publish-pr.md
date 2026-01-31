# Publish PR Action

## 概要

`publish-pr` は、ドラフトプルリクエストをレビュー準備完了（Ready for review）に変換する GitHub Action です。

## 機能

- ドラフト PR の自動公開
- `gh` CLI を使用したシンプルな操作

## 使用方法

### 基本的な使い方

```yaml
steps:
  - uses: ./actions/publish-pr
    with:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 入力パラメータ

| パラメータ | 必須 | デフォルト値 | 説明 |
|-----------|------|-------------|------|
| `github-token` | ✓ | - | リポジトリ権限を持つ GitHub トークン |

### 使用例

#### ワークフローでの自動公開

```yaml
name: Auto Publish PR
on:
  pull_request:
    types: [labeled, opened, synchronize]

jobs:
  publish:
    if: github.event.pull_request.draft == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./actions/publish-pr
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

#### ラベル付きで公開

```yaml
jobs:
  publish-when-approved:
    if: |
      contains(github.event.pull_request.labels.*.name, 'approved') &&
      github.event.pull_request.draft == true
    runs-on: ubuntu-latest
    steps:
      - uses: ./actions/publish-pr
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 注意事項

- この Action はドラフト PR に対してのみ機能します
- 既に公開されている PR に対しては何も行いません
- 適切な権限を持つ GitHub トークンが必要です
- プルリクエスト番号は `github.event.pull_request.number` から自動的に取得されます
