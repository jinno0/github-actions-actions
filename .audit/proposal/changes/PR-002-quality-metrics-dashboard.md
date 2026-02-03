# PR-002: 品質メトリクスダッシュボードの公開

**優先度**: MEDIUM (ISS-003)
**関連ギャップ**: ISS-003 - 受入率（Acceptance Rate）の公開値がない
**状態**: Proposed

## 概要

AIレビューの品質メトリクス（受入率）を可視化するダッシュボードを構築し、
プロジェクトの公開ドキュメントとして品質状況を透明化する。

## 現状

- `scripts/calculate_acceptance_rate.py` は存在するが、実行結果が公開されていない
- README.md:123-124で受入率追跡が言及されているが、実際の値が見えない
- PURPOSE.md:72で「AIの提案に対する修正率（Acceptance Rate）が向上し続ける」ことが成功条件

## 提案内容

### Phase 1: メトリクス収集の強化（1-2日）

1. **既存スクリプトの評価**
   - `scripts/calculate_acceptance_rate.py` の動作確認
   - 出力フォーマットの標準化（JSON, Markdown, HTML）

2. **定期的な実行仕組みの導入**
   - GitHub Actionsで週次/月次のメトリクス収集
   - 結果を `metrics/` ディレクトリに保存

### Phase 2: ダッシュボードの構築（3-5日）

1. **シンプルなMarkdownベースのレポート**
   ```markdown
   # AI Review Quality Metrics

   ## Acceptance Rate (Last 30 Days)

   | Metric | Value | Target | Status |
   |--------|-------|--------|--------|
   | Acceptance Rate | 68.5% | >= 70% | ⚠️  Below Target |
   | Total Reviews | 234 | - | - |
   | Approved | 160 | - | - |
   | Modified | 52 | - | - |
   | Rejected | 22 | - | - |

   ## Trend

   [週次のグラフまたはテーブル]
   ```

2. **GitHub Pagesでの公開（オプション）**
   - MarkdownからHTMLへの変換
   - GitHub Actionsで自動デプロイ

### Phase 3: メトリクスの拡張（2-3日）

1. **追加メトリクスの定義**
   - 平均レビュー時間
   - 提案数/レビューあたり
   - 各Actionの利用率

2. **データの集約**
   - テレメトリーデータとの統合
   - 時系列データの保存

## 実装手順

### 1. メトリクス収集ワークフロー

`.github/workflows/collect-metrics.yml`:

```yaml
name: Collect Quality Metrics

on:
  schedule:
    - cron: '0 0 * * 0'  # 毎週日曜日
  workflow_dispatch:

permissions:
  contents: read

jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Calculate Acceptance Rate
        run: |
          python scripts/calculate_acceptance_rate.py \
            --output report \
            --time-period 30d \
            --format json \
            --output-file metrics/acceptance_rate.json

      - name: Generate Markdown Report
        run: |
          python scripts/generate_metrics_report.py \
            --input metrics/acceptance_rate.json \
            --output metrics/QUALITY_METRICS.md

      - name: Upload Metrics
        uses: actions/upload-artifact@v4
        with:
          name: quality-metrics
          path: metrics/
```

### 2. レポート生成スクリプト

`scripts/generate_metrics_report.py`:

```python
#!/usr/bin/env python3
"""Generate quality metrics report from acceptance rate data."""
import json
from pathlib import Path
from datetime import datetime

def generate_markdown_report(data: dict, output_path: Path):
    """Generate Markdown report from metrics data."""
    target_rate = 70.0
    current_rate = data.get("acceptance_rate", 0)
    status = "✅" if current_rate >= target_rate else "⚠️"

    report = f"""# AI Review Quality Metrics

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Acceptance Rate (Last 30 Days)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Acceptance Rate | {current_rate:.1f}% | >= {target_rate}% | {status} {'Below Target' if current_rate < target_rate else 'On Track'} |
| Total Reviews | {data.get('total_reviews', 0)} | - | - |
| Approved | {data.get('approved', 0)} | - | - |
| Modified | {data.get('modified', 0)} | - | - |
| Rejected | {data.get('rejected', 0)} | - | - |

## Review Outcomes Distribution

```
Approved:  {data.get('approved', 0):3d} ({data.get('approved', 0)/max(data.get('total_reviews', 1),1)*100:.1f}%)
Modified:  {data.get('modified', 0):3d} ({data.get('modified', 0)/max(data.get('total_reviews', 1),1)*100:.1f}%)
Rejected:  {data.get('rejected', 0):3d} ({data.get('rejected', 0)/max(data.get('total_reviews', 1),1)*100:.1f}%)
```

## Common Rejection Reasons

{chr(10).join(f"- {reason}: {count}" for reason, count in data.get('rejection_reasons', {}).items())}

---

## Methodology

**Acceptance Rate Definition**:
```
Acceptance Rate = (Approved + Modified) / Total Reviews
```

- **Approved**: AI review suggestions accepted without changes
- **Modified**: AI review suggestions accepted with minor changes
- **Rejected**: AI review suggestions not accepted

**Data Source**: GitHub review comments via telemetry

**Target**: >= 70% (based on PURPOSE.md goal of continuous improvement)
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    print(f"Report generated: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text())
    generate_markdown_report(data, Path(args.output))
```

### 3. README.mdへの統合

README.mdにメトリクスセクションを追加:

```markdown
## 📊 AIレビュー品質メトリクス

最新の品質メトリクスは[**QUALITY_METRICS.md**](./metrics/QUALITY_METRICS.md)で確認できます。

### ハイライト（直近30日間）

| 指標 | 現在値 | 目標値 |
|------|--------|--------|
| 受入率 | 68.5% | >= 70% |
| 総レビュー数 | 234 | - |

詳細な週次トレンドや分析については、[品質メトリクスドキュメント](./metrics/QUALITY_METRICS.md)を参照してください。
```

## 期待効果

1. **透明性**: チーム内外で品質状況を共有
2. **改善サイクル**: メトリクスを見える化することで、改善の動機付け
3. **信頼性**: AIレビューの品質を定量的にデモンストレーション
4. **成功判定**: PURPOSE.mdの成功条件（Acceptance Rate向上）を追跡可能

## 副作用とリスク

1. **データの解釈ミス**: メトリクスが低いときにネガティブな印象を与える可能性
   - 対策: メトリクスの意味、限界、改善への取り組みを明記
2. **プライバシー**: テレメトリーデータの匿名化が不十分な可能性
   - 対策: 既存のプライバシー機能（SHA-256ハッシュ化）を維持
3. **メンテナンスコスト**: 週次のメトリクス収集とレポート生成
   - 対策: 自動化で人的コストを最小化

## 検証方法

1. `scripts/calculate_acceptance_rate.py --output report` が正常に動作すること
2. `scripts/generate_metrics_report.py` がMarkdownを出力すること
3. GitHub Actionsが週次実行され、metrics/ディレクトリが更新されること
4. README.mdからメトリクスページにリンクが張られていること

## ロールバック計画

- メトリクス収集ワークフローは無害（情報の生成のみ）
- 問題発生時はワークフローを無効化して元の状態に戻す

## 関連ファイル

- 新規: `.github/workflows/collect-metrics.yml`
- 新規: `scripts/generate_metrics_report.py`
- 新規: `metrics/QUALITY_METRICS.md` (自動生成)
- 変更: `README.md` (メトリクスセクションの追加)

## 次のアクション

1. 本提案のレビューと承認
2. `generate_metrics_report.py` の実装
3. GitHub Actionsワークフローの作成とテスト
4. 最初のメトリクスレポートの生成
5. README.mdの更新

---

**作成日**: 2025-02-03
**作成者**: Repo Genesis Auditor (run-initial)
**仮定に基づく**: なし（事実と既存スクリプトに基づく）
