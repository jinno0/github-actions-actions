# PR-003: AIレビュー受入率の可視化と定期レポート

**関連するギャップ:** GAP-005
**優先度:** Medium
**推定作業時間:** 2-3時間

## 概要

AIレビュー品質の指標である「受入率（Acceptance Rate）」の目標値は >= 70% と設定されているが、
現在の実際の値が不明である。このPRでは受入率を計算し、定期レポートを生成する仕組みを整備する。

## 変更内容

### 1. scripts/calculate_acceptance_rate.py の動作確認

**ファイル:** `scripts/calculate_acceptance_rate.py`

**確認項目:**
- スクリプトが存在し、実行可能であること
- 必要な依存関係（PyGithub, pandas等）が揃っていること
- GitHub Tokenの認証が正常に動作すること

**実装手順:**
1. スクリプトのdry-runを実行: `python scripts/calculate_acceptance_rate.py --dry-run`
2. 必要に応じて依存関係を追加: `requirements.txt` または `pyproject.toml`
3. エラーが出る場合はデバッグし、修正

### 2. GitHub Actionsワークフローの作成

**ファイル:** `.github/workflows/weekly-acceptance-rate-report.yml`

**内容:** 毎週日曜日に受入率レポートを自動生成し、Issueとして投稿する

```yaml
name: Weekly Acceptance Rate Report

on:
  schedule:
    # 毎週日曜日 00:00 UTC
    - cron: '0 0 * * 0'
  workflow_dispatch:  # 手動実行も可能

permissions:
  contents: read
  issues: write

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Calculate acceptance rate
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          REPOSITORY: ${{ github.repository }}
        run: |
          python scripts/calculate_acceptance_rate.py \
            --output report \
            --time-period 7d \
            --create-issue

      - name: Upload metrics
        uses: actions/upload-artifact@v4
        with:
          name: acceptance-rate-report
          path: metrics/
```

### 3. metrics/ ディレクトリの初期化

**ディレクトリ:** `metrics/`

**内容:** 受入率レポートの保存場所

**実装手順:**
1. `metrics/` ディレクトリが存在することを確認
2. `README.md` でレポートの見方を説明
3. `metrics/README.md` を作成:

```markdown
# AI Review Quality Metrics

このディレクトリには、AIレビューの品質メトリクス（受入率）の定期レポートが保存されます。

## レポートファイル

- `acceptance-report-YYYY-MM-DD.json`: 生データ
- `acceptance-report-YYYY-MM-DD.md`: 人間が読める形式のサマリー

## メトリクスの定義

### 受入率（Acceptance Rate）

人間に受け入れられたAIレビューの割合。

\[
\text{受入率} = \frac{\text{approved + modifiedのレビュー数}}{\text{全レビュー数}} \times 100
\]

**アウトカムの定義:**
- `approved`: 人間がそのまま承認
- `modified`: 人間が一部修正したが、基本的に受け入れ
- `rejected`: 完全に拒否
- `needs_work`: 修正要求

**目標:** >= 70%

## 自動生成

毎週日曜日の00:00 UTCに、`.github/workflows/weekly-acceptance-rate-report.yml` によって
自動生成されます。
```

### 4. 手動実行方法のドキュメント化

**ファイル:** `README.md` の更新

**追加内容:**

```markdown
## 📈 AIレビュー品質メトリクスの確認方法

### 定期レポート

毎週日曜日に自動生成されます。過去のレポートは [`metrics/`](metrics/) ディレクトリを
参照してください。

### 手動でのレポート生成

開発環境で手動実行する場合:

\`\`\`bash
# 過去7日間のレポートを生成
python scripts/calculate_acceptance_rate.py --output report --time-period 7d

# 過去30日間のレポートを生成
python scripts/calculate_acceptance_rate.py --output report --time-period 30d

# Issueとして投稿
python scripts/calculate_acceptance_rate.py --output report --time-period 7d --create-issue
\`\`\`

### 現在の受入率

[![Acceptance Rate](https://img.shields.io/badge/Acceptance_Rate-Loading%20...-blue)](metrics/)
```

## 期待される効果

- 受入率のトレンドが可視化され、改善の方向性がデータドリブンで決められる
- チーム全体がAIレビューの品質を意識するようになる
- README.md:148の「ベースライン策定中」の状態から、定量的な目標管理へ移行できる

## 検証方法

1. **スクリプトのdry-run**
   ```bash
   python scripts/calculate_acceptance_rate.py --dry-run --time-period 7d
   ```

2. **ワークフローの手動実行**
   - GitHub Actions画面で `workflow_dispatch` を実行
   - Issueが正常に作成されることを確認

3. **メトリクスファイルの確認**
   ```bash
   ls -lh metrics/acceptance-report-*.json
   cat metrics/README.md
   ```

## 依存関係

- GitHub APIへのアクセス権限
- `scripts/calculate_acceptance_rate.py` が既に実装されていること
- 必要なPythonパッケージ（PyGithub等）がインストールされていること

## リスク評価

- **破壊的変更:** なし
- **副作用:** なし（レポート生成のみ）
- **プライバシー:** レビューコメントの内容は収集せず、統計情報のみを収集

## 注意事項

- レビューコメントの内容自体は収集しない（プライバシー配慮）
- リポジトリ名はハッシュ化して保存（README.md:124にあるテレメトリーと同様）
- 古いレポートは適宜アーカイブまたは削除（ストレージ節約）

## 参考資料

- README.md:141-170 (AIレビュー品質メトリクスのセクション)
- docs/quality_metrics.md
- `scripts/calculate_acceptance_rate.py`

## 成功基準

- [ ] `scripts/calculate_acceptance_rate.py` が正常に動作する
- [ ] `.github/workflows/weekly-acceptance-rate-report.yml` が作成される
- [ ] ワークフローが手動実行でき、Issueが正常に作成される
- [ ] `metrics/README.md` が作成され、メトリクスの定義が説明されている
- [ ] README.mdにメトリクス確認方法が記載される
- [ ] 次回の日曜日に自動レポートが生成される
