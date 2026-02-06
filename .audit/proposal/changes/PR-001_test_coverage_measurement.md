# PR-001: テストカバレッジ計測の実装

**Priority:** Critical
**Gap ID:** GAP-001
**Based on Assumption:** ASM-002 (テストカバレッジ >= 70%)

## 概要

現在32個のテストファイルが存在するが、実際のカバレッジ率が計測されていない。
このPRでは、pytest-covを使用してカバレッジ率を可視化し、CIで自動生成するようにする。

## 変更内容

### 1. pytest.ini の更新

**File:** `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*

# カバレッジ設定
addopts =
    --cov=actions
    --cov=scripts
    --cov=tests
    --cov-report=term-missing
    --cov-report=html:.htmlcov
    --cov-report=json:.coverage.json
    --cov-fail-under=70

# カバレッジ除外パス
[coverage:run]
omit =
    */__pycache__/*
    */.venv/*
    */venv/*
    */.tox/*
    */tests/test_*.py
    actions/_shared/*
    actions/lib/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

### 2. GitHub Actions Workflow の更新

**File:** `.github/workflows/test-all-actions.yml`

```yaml
# 既存のジョブにカバレッジレポートステップを追加
- name: Generate coverage report
  run: |
    pytest --cov=actions --cov=scripts --cov-report=term-missing --cov-report=xml
  continue-on-error: true

- name: Upload coverage to PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const coverage = JSON.parse(fs.readFileSync('.coverage.json', 'utf8'));
      const total = coverage.totals.percent_covered;

      const output = `## 📊 Coverage Report

      **Total Coverage:** ${total.toFixed(2)}%

      ${total >= 70 ? '✅' : '❌'} Target: 70%

      ${total < 70 ? '⚠️ Coverage is below target. Please add tests.' : ''}`;

      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: output
      });
```

### 3. README.md の更新

**File:** `README.md`

以下のセクションを追加：

```markdown
## 📊 テストカバレッジ

このプロジェクトでは、テストカバレッジ >= 70% を目標としています。

### カバレッジレポートの確認方法

```bash
# ローカルでカバレッジを計測
pytest --cov=actions --cov=scripts --cov-report=html

# HTMLレポートを開く
open .htmlcov/index.html  # macOS
xdg-open .htmlcov/index.html  # Linux
```

### CIでのカバレッジチェック

PRを作成すると、自動的にカバレッジレポートがコメントされます。
```

## 実装手順

1. `pytest.ini` を作成・更新
2. `.github/workflows/test-all-actions.yml` にカバレッジステップを追加
3. `README.md` にカバレッジセクションを追加
4. ローカルで `pytest --cov` を実行して動作確認
5. テストPRを作成してCIでのカバレッジレポート動作を確認

## 期待される効果

- ✅ カバレッジ率が可視化され、品質のベースラインが明確になる
- ✅ PRごとにカバレッジ変動が追跡できる
- ✅ ASM-002 (カバレッジ >= 70%) の仮定が検証される
- ✅ カバレッジ不足が早期に検知できる

## ロールバック手順

1. `pytest.ini` の `addopts` から `--cov*` を削除
2. `.github/workflows/test-all-actions.yml` のカバレッジステップを削除
3. README.md のカバレッジセクションを削除

## 検証方法

```bash
# 1. カバレッジ計測が実行できるか
pytest --cov=actions --cov=scripts --cov-report=term-missing

# 2. カバレッジレポートが生成されるか
test -f .coverage.json && echo "✅ JSON report generated"
test -f .htmlcov/index.html && echo "✅ HTML report generated"

# 3. カバレッジ率が取得できるか
python -c "import json; data=json.load(open('.coverage.json')); print(f\"Coverage: {data['totals']['percent_covered']:.2f}%\")"
```

## 副作用とリスク

- **リスク:** pytestの実行時間が10-20%増加する可能性
- **緩和策:** CIでは並列実行を検討する
- **リスク:** カバレッジが70%を大きく下回る場合、PRブロックの摩擦が増える
- **緩和策:** 最初は `--cov-fail-under=0` で様子を見て、徐々に閾値を上げる

## 関連ファイル

- `pytest.ini` (新規作成または更新)
- `.github/workflows/test-all-actions.yml` (更新)
- `README.md` (更新)
- `.coverage.json` (生成物、.gitignoreに追加済みか確認)
- `.htmlcov/` (生成物、.gitignoreに追加済みか確認)

## 参考情報

- pytest-covドキュメント: https://pytest-cov.readthedocs.io/
- Coverage.pyドキュメント: https://coverage.readthedocs.io/
