# PR-007: Test Coverage Recovery

**Status**: Proposed
**Priority**: High (GAP-002)
**Estimated Effort**: 5-8 hours
**Target Gap**: GAP-002 (テストカバレッジ78.15% → 80%+)

## 問題陈述

全体のテストカバレッジが78.15%で、目標値80%をわずかに下回っている。主要な原因は2つのスクリプトが0%カバレッジであること:

- `generate_review_quality_dashboard.py`: 128行、0%カバレッジ
- `test_data_collection.py`: 38行、0%カバレッジ

**現状**:
- 全体カバレッジ: 78.15% (869/1112 lines)
- 目標: >= 80%
- ギャップ: -1.85%
- 未カバー行数: 243行

**影響**:
- QA-001 (テストカバレッジ) 未達成
- CI/CDパイプラインでのカバレッジチェック失敗の可能性
- 新規スクリプト追加時にテストなしでマージされた事例（改善プロセスの問題）

## 提案内容

### アクション1: generate_review_quality_dashboard.py のテスト追加

**目標**: 128行中、少なくとも100行をカバーする
**期待効果**: カバレッジ78.15% → 82%+

#### テスト戦略

1. **メイン関数のテスト** (`generate_dashboard()`)
   - 正常系: メトリクスJSONを読み込み、ダッシュボードMarkdownを生成
   - 異常系: ファイル不存在、無効なJSON、権限エラー

2. **ヘルパー関数のテスト**
   - `calculate_acceptance_rate()`: 受入率計算、境界値テスト
   - `generate_outcome_breakdown()`: アウトカム集計
   - `format_trend_section()`: トレンドフォーマット

3. **モックとフィクスチャの活用**
   - `tmp_path` fixtureで一時ファイル作成
   - `capsys` でstdoutキャプチャ
   - テストデータ: `tests/fixtures/test_review_metrics.json`

#### テストファイル構成

```python
# tests/scripts/test_generate_review_quality_dashboard.py

import json
import pytest
from pathlib import Path
from scripts.generate_review_quality_dashboard import (
    generate_dashboard,
    calculate_acceptance_rate,
    generate_outcome_breakdown,
    format_trend_section
)

class TestCalculateAcceptanceRate:
    """受入率計算のテスト"""

    def test_all_approved(self):
        data = [
            {"outcome": "approved"},
            {"outcome": "approved"},
        ]
        rate = calculate_acceptance_rate(data)
        assert rate == 100.0

    def test_mixed_outcomes(self):
        data = [
            {"outcome": "approved"},
            {"outcome": "modified"},
            {"outcome": "rejected"},
        ]
        rate = calculate_acceptance_rate(data)
        assert rate == 33.33  # 1/3

    def test_empty_data(self):
        with pytest.raises(ValueError):
            calculate_acceptance_rate([])

class TestGenerateOutcomeBreakdown:
    """アウトカム集計のテスト"""

    def test_breakdown_counts(self):
        data = [
            {"outcome": "approved"},
            {"outcome": "approved"},
            {"outcome": "modified"},
        ]
        breakdown = generate_outcome_breakdown(data)
        assert breakdown["approved"] == 2
        assert breakdown["modified"] == 1
        assert breakdown["rejected"] == 0

class TestGenerateDashboard:
    """ダッシュボード生成の統合テスト"""

    def test_generate_dashboard_success(self, tmp_path, capsys):
        # 準備: テストデータの作成
        metrics_file = tmp_path / "test_metrics.json"
        metrics_file.write_text('[{"outcome": "approved"}]')

        output_file = tmp_path / "dashboard.md"

        # 実行
        generate_dashboard(str(metrics_file), str(output_file))

        # 検証
        assert output_file.exists()
        captured = capsys.readouterr()
        assert "Dashboard generated" in captured.out

    def test_generate_dashboard_file_not_found(self, tmp_path):
        metrics_file = tmp_path / "nonexistent.json"
        output_file = tmp_path / "dashboard.md"

        with pytest.raises(FileNotFoundError):
            generate_dashboard(str(metrics_file), str(output_file))

    def test_generate_dashboard_invalid_json(self, tmp_path):
        metrics_file = tmp_path / "invalid.json"
        metrics_file.write_text('{invalid json}')

        output_file = tmp_path / "dashboard.md"

        with pytest.raises(json.JSONDecodeError):
            generate_dashboard(str(metrics_file), str(output_file))
```

### アクション2: test_data_collection.py のテスト追加

**目標**: 38行中、少なくとも30行をカバーする
**期待効果**: カバレッジ78.15% → 81%+

#### テスト戦略

1. **データ収集関数のテスト**
   - 正常系: 有効なレビューデータの収集
   - 異常系: 無効なデータ、重複排除

2. **検証関数のテスト**
   - 必須フィールドのチェック
   - データ型の検証

#### テストファイル構成

```python
# tests/scripts/test_test_data_collection.py

import pytest
from scripts.test_data_collection import (
    collect_review_data,
    validate_review_entry,
    deduplicate_entries
)

class TestValidateReviewEntry:
    """レビューエントリ検証のテスト"""

    def test_valid_entry(self):
        entry = {
            "pr_number": 1,
            "outcome": "approved",
            "timestamp": "2026-02-09T12:00:00Z"
        }
        assert validate_review_entry(entry) is True

    def test_missing_required_field(self):
        entry = {"pr_number": 1}  # outcome が欠落
        assert validate_review_entry(entry) is False

    def test_invalid_outcome(self):
        entry = {
            "pr_number": 1,
            "outcome": "invalid_outcome",
            "timestamp": "2026-02-09T12:00:00Z"
        }
        assert validate_review_entry(entry) is False

class TestDeduplicateEntries:
    """重複排除のテスト"""

    def test_remove_duplicates_by_pr_number(self):
        entries = [
            {"pr_number": 1, "outcome": "approved"},
            {"pr_number": 2, "outcome": "modified"},
            {"pr_number": 1, "outcome": "approved"},  # 重複
        ]
        unique = deduplicate_entries(entries)
        assert len(unique) == 2
        assert all(e["pr_number"] != 1 for e in unique[1:])
```

### アクション3: CI/CDパイプラインの強化

**目標**: 今後、テストなしのスクリプトがマージされないようにする

#### .github/workflows/test.yml の更新

```yaml
name: Test Coverage Check

on:
  pull_request:
    paths:
      - 'scripts/**/*.py'
      - 'actions/**/*.py'

jobs:
  coverage-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest --cov=actions --cov=scripts --cov-report=json --cov-fail-under=80

      - name: Check for new untested files
        run: |
          python scripts/check_new_files_coverage.py
```

#### 新規スクリプト: scripts/check_new_files_coverage.py

```python
#!/usr/bin/env python3
"""
新しいPythonファイルがテストなしで追加されていないかチェック
"""

import subprocess
import sys
from pathlib import Path

def get_new_python_files():
    """git diffで新規追加されたPythonファイルを取得"""
    result = subprocess.run(
        ['git', 'diff', '--name-only', '--diff-filter=A', 'origin/main', 'HEAD'],
        capture_output=True,
        text=True
    )
    return [f for f in result.stdout.split('\n') if f.endswith('.py')]

def check_test_exists(py_file):
    """Pythonファイルに対応するテストファイルが存在するか"""
    path = Path(py_file)

    # テスト対象外のディレクトリ
    if any(excluded in str(path) for excluded in ['tests/', '.venv/', '__pycache__']):
        return True

    # 対応するテストファイルのパス
    if 'scripts/' in str(path):
        test_file = Path('tests') / 'scripts' / path.name.replace('.py', '_test.py')
    elif 'actions/' in str(path):
        test_file = Path('tests') / 'actions' / path.name.replace('.py', '_test.py')
    else:
        return True  # その他のディレクトリは対象外

    return test_file.exists()

def main():
    new_files = get_new_python_files()
    untested = []

    for py_file in new_files:
        if not check_test_exists(py_file):
            untested.append(py_file)

    if untested:
        print(f"❌ ERROR: {len(untested)} new Python file(s) without tests:")
        for f in untested:
            print(f"  - {f}")
        print("\nPlease add tests for new files before merging.")
        sys.exit(1)

    print("✅ All new Python files have corresponding tests.")
    sys.exit(0)

if __name__ == '__main__':
    main()
```

## 期待される効果

**即時効果**:
- テストカバレッジ: 78.15% → 82%+ (目標達成)
- CI/CDパイプライン: カバレッジチェックパス
- QA-001: 達成

**中期効果**:
- テストなしの新規ファイル追加防止
- コード品質の維持・向上
- リファクタリングの安全性確保

**長期効果**:
- 技術的負債の蓄積防止
- 開発速度の向上（回帰バグの減少）

## 実行計画

**Phase 1: generate_review_quality_dashboard.py のテスト (3-5時間)**
1. テストファイル作成: `tests/scripts/test_generate_review_quality_dashboard.py`
2. フィクスチャ準備: `tests/fixtures/test_review_metrics.json`
3. テスト実装と実行
4. カバレッジ確認

**Phase 2: test_data_collection.py のテスト (2-3時間)**
1. テストファイル作成: `tests/scripts/test_test_data_collection.py`
2. テスト実装と実行
3. カバレッジ確認

**Phase 3: CI/CDパイプライン強化 (1-2時間)**
1. `.github/workflows/test.yml` の更新
2. `scripts/check_new_files_coverage.py` の作成
3. PRでテスト

## 成功判定基準

- [ ] 全体テストカバレッジ >= 80%
- [ ] `generate_review_quality_dashboard.py` カバレッジ >= 75%
- [ ] `test_data_collection.py` カバレッジ >= 75%
- [ ] 新規スクリプト追加チェックがPRで動作
- [ ] すべてのテストがパス (460+ tests)

## リスクと対策

| リスク | 確率 | 影響 | 対策 |
|--------|------|------|------|
| テスト作成時間が延長する | 中 | 低 | 最小限のテストから開始。段階的にカバレッジ向上。 |
| CI/CDパイプラインの誤検知 | 低 | 中 | 明確な除外ルールを設定。レビューで確認。 |
| 既存コードのリファクタリングが必要 | 低 | 低 | テスト可能な範囲のみ実施。大幅な変更は別PR。 |

## 次のアクション

1. **本提案の承認**
2. **generate_review_quality_dashboard.py のテスト実装開始**
3. **カバレッジ計測と確認**
4. **PR作成とレビュー**

---

**関連ファイル**:
- `.audit/analysis/gap.yml` (GAP-002)
- `scripts/generate_review_quality_dashboard.py`
- `scripts/test_data_collection.py`
- `.audit/config/intent.yml` (QA-001)
