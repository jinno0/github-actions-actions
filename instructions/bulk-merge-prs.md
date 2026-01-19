# Bulk Merge PRs

## 概要

CIが通っている複数のPull Requestを一括でマージします。

## Prerequisites

- GitHub Actionsの実行権限
- `pull-requests: write` 権限
- `contents: write` 権限

## Setup

1. ワークフローファイルを作成:
```yaml
name: Bulk Merge PRs

on:
  workflow_dispatch:

permissions:
  pull-requests: write
  contents: write

jobs:
  bulk-merge:
    runs-on: ubuntu-latest
    steps:
      - uses: jinno0/github-actions-actions/actions/bulk-merge-prs@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

2. 必要に応じてパラメータを調整

## Parameters

| パラメータ | 必須 | デフォルト | 説明 |
|-----------|------|----------|------|
| github-token | ✗ | ${{ github.token }} | GitHubトークン |
| limit | ✗ | '0' | 最大マージ数（0 = 全て） |
| merge-method | ✗ | 'squash' | マージ方法 |
| include-drafts | ✗ | 'true' | ドラフトPRを含む |
| dry-run | ✗ | 'false' | ドライラン実行 |

## merge-method の値

- `squash`: 全てのコミットを1つにまとめてマージ（デフォルト）
- `merge`: マージコミットを作成
- `rebase`: コミットをそのまま適用

## Usage

### 基本的な使い方

GitHubのActionsタブから手動実行します。

### 全てのマージ可能なPRをマージ

```yaml
- uses: jinno0/github-actions-actions/actions/bulk-merge-prs@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 最初の10件だけマージ

```yaml
- uses: jinno0/github-actions-actions/actions/bulk-merge-prs@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    limit: '10'
```

### ドライランで確認

```yaml
- uses: jinno0/github-actions-actions/actions/bulk-merge-prs@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    dry-run: 'true'
```

## マージされるPRの条件

- `mergeable == "MERGEABLE"` （コンフリクトなし）
- `mergeStateStatus == "CLEAN"` （CI全通過）
- ドラフトPRも対象（自動的にreadyにしてからマージ）

## マージされないPR

- **DIRTY**: マージコンフリクトあり
- **UNSTABLE**: CI失敗中
- **DRAFT**: ドラフト（`include-drafts: false`の場合）

## 推奨ワークフロー

1. まず `bulk-rebase-prs` で古いPRをリベース
2. CIが通るのを待つ
3. `bulk-merge-prs` で一括マージ
