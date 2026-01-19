# Bulk Rebase PRs

## 概要

複数のPull Requestを一括で最新のブランチに対してリベースします。

## Prerequisites

- GitHub Actionsの実行権限
- `pull-requests: write` 権限

## Setup

1. ワークフローファイルを作成:
```yaml
name: Bulk Rebase PRs

on:
  workflow_dispatch:

permissions:
  pull-requests: write

jobs:
  bulk-rebase:
    runs-on: ubuntu-latest
    steps:
      - uses: jinno0/github-actions-actions/actions/bulk-rebase-prs@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

2. 必要に応じてパラメータを調整

## Parameters

| パラメータ | 必須 | デフォルト | 説明 |
|-----------|------|----------|------|
| github-token | ✗ | ${{ github.token }} | GitHubトークン |
| limit | ✗ | '0' | 最大処理数（0 = 全て） |
| merge-state-status | ✗ | 'BEHIND' | フィルタするステータス |
| dry-run | ✗ | 'false' | ドライラン実行 |

## merge-state-status の値

- `BEHIND`: ベースブランチより古いPR（デフォルト）
- `CLEAN`: マージ可能
- `DIRTY`: コンフリクトあり
- `UNKNOWN`: 状態不明
- `UNSTABLE`: CI失敗中
- 空文字: 全てのBEHIND PR

## Usage

### 基本的な使い方

GitHubのActionsタブから手動実行します。

### 全ての古いPRをリベース

```yaml
- uses: jinno0/github-actions-actions/actions/bulk-rebase-prs@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    merge-state-status: 'BEHIND'
```

### 最初の10件だけ処理

```yaml
- uses: jinno0/github-actions-actions/actions/bulk-rebase-prs@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    limit: '10'
```

### ドライランで確認

```yaml
- uses: jinno0/github-actions-actions/actions/bulk-rebase-prs@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    dry-run: 'true'
```
