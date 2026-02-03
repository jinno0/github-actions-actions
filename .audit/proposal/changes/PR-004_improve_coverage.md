# PR-004: テストカバレッジ70%達成

## Issue
- **ID**: ISS-001
- **Severity**: Critical
- **Title**: テストカバレッジが目標70%を46.94%下回っている

## Current State
- 現在のカバレッジ: 23.06%
- 目標カバレッジ: 70% (pytest.ini:22)
- pytestは必ず失敗する（--cov-fail-under=70）
- 281 testsが存在するが、構造検証に偏っている

## Root Cause Analysis

### カバレッジが低い理由
1. **構造検証のみ**: テストがYAML構文とファイル存在確認に集中
2. **未テストのモジュール**: scripts/以下のユーティリティ
3. **未カバーな分岐**: action.ymlの条件分岐
4. **Helper関数未テスト**: tests/conftest.pyのフィクスチャ

### カバレッジレポートの詳細（pytest coverageより）
```
tests/test_calculate_acceptance_rate.py                             118     87    26%
tests/test_collect_metrics.py                                       129     95    26%
tests/test_*.py                                                    ~2000   ~1500   ~23%
-----------------------------------------------------------------------------------------------
TOTAL                                                              2268   1745    23%
```

## Proposed Changes

### Phase 1: 既存コードのテスト追加 (1週間)

#### 1. scripts/のテスト追加
**Files to create**:
- `tests/test_scripts/test_generate_telemetry_report.py`
- `tests/test_scripts/test_calculate_acceptance_rate.py`
- `tests/test_scripts/test_collect_metrics.py`

**Example**:
```python
# tests/test_scripts/test_calculate_acceptance_rate.py
import pytest
from pathlib import Path
from scripts.calculate_acceptance_rate import calculate_acceptance_rate

def test_calculate_acceptance_rate_normal():
    """Test normal acceptance rate calculation"""
    # テストデータ準備
    reviews = [
        {"outcome": "approved"},
        {"outcome": "approved"},
        {"outcome": "rejected"}
    ]
    result = calculate_acceptance_rate(reviews)
    assert result == 66.67

def test_calculate_acceptance_rate_empty():
    """Test with empty review list"""
    result = calculate_acceptance_rate([])
    assert result == 0.0
```

#### 2. tests/conftest.pyのフィクスチャテスト
**File to create**: `tests/test_conftest.py`

```python
import pytest
from pathlib import Path

def test_action_path_fixture(action_path):
    """Test that action_path fixture returns correct path"""
    assert action_path.exists()
    assert (action_path / "review-and-merge").exists()

def test_sample_data_fixture(sample_data):
    """Test that sample_data fixture returns valid data"""
    assert isinstance(sample_data, dict)
```

### Phase 2: テスト可能なActionコードの抽出 (1週間)

#### 問題
action.yml自体は直接テストできない（composite action）

#### 解決策
テスト可能なロジックをスクリプトとして抽出：

**例**: `actions/review-and-merge/scripts/verdict.py`
```python
def determine_verdict(confidence: int, threshold: int) -> str:
    """Determine review verdict based on confidence"""
    if confidence >= threshold:
        return "LGTM"
    return "REQUEST_CHANGES"
```

**テスト**:
```python
# tests/test_verdict.py
def test_determine_verdict_lgtm():
    assert determine_verdict(8, 7) == "LGTM"

def test_determine_verdict_request_changes():
    assert determine_verdict(5, 7) == "REQUEST_CHANGES"
```

### Phase 3: エッジケースのテスト追加 (3-5日)

#### 対象
- 空ファイル
- 不正なYAML
- 不足のinputs
- テンプレートファイル不在

**例**:
```python
def test_action_with_missing_template(action_path):
    """Test action behavior when template is missing"""
    # モック環境でテンプレートを削除して実行
    # エラーハンドリングを検証
```

## Expected Outcomes

### Metrics
- カバレッジ: 23.06% → 70% (+46.94%)
- pytestがパスするようになる
- 回帰リスク低減

### Quality
- リファクタリングが安全にできるようになる
- バグ早期発見
- コード品質の可視化

## Verification Plan

### 週次マイルストーン
```
Week 1, Day 1-2: scripts/のテスト追加（+15% coverage）
Week 1, Day 3-4: conftest.pyのテスト追加（+5% coverage）
Week 1, Day 5: 進捗確認と調整

Week 2, Day 1-3: ロジック抽出とテスト（+20% coverage）
Week 2, Day 4-5: エッジケーステスト（+10% coverage）

Total expected: +50% → 73% (目標達成)
```

### 進捗測定
```bash
# 毎日実行してカバレッジ推移を記録
pytest --cov=. --cov-report=term-missing | tee coverage_log.txt
```

### 成功基準
1. `pytest --cov=. --cov-fail-under=70` がパスする
2. 全ての新しいテストがパスする
3. カバレッジレポートで未カバーの重要なパスがない

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| テスト追加が70%に到達しない | Medium | High | ロジック抽出で補完、pytest.ini調整も検討 |
| 既存Actionの動作を壊す | Low | High | 機能変更はせずテストのみ追加 |
| テスト作成に時間がかかりすぎる | Medium | Medium | 優先順位付け：scripts/ → conftest → actions |
| モックが複雑になりすぎる | Medium | Low | 構造検証に留める、機能テストはPhase 3へ |

## Rollback Plan

1. 新規テストファイルを削除:
   ```bash
   git checkout HEAD -- tests/test_scripts/ tests/test_conftest.py
   ```

2. 抽出したスクリプトを削除:
   ```bash
   rm actions/*/scripts/*.py
   ```

3. 元のaction.ymlに戻す（変更した場合）:
   ```bash
   git checkout HEAD -- actions/*/action.yml
   ```

## Alternatives Considered

1. **pytest.iniで基準値を60%に下げる**
   - Rejected: 本質的な解決になっていない
   - Fallback: どうしても70%が達成できない場合の最終手段

2. **特定のディレクトリをカバレッジ対象外にする**
   - Partially Accepted: examples/, docs/ は除外
   - Implementation: .coveragerc で設定

3. **機能テストを優先する**
   - Rejected: 機能テストはPhase 3（ISS-006）
   - Reason: 構造テストのカバレッジ向上を先に行う

## Timeline

- Phase 1: 1週間（scripts/ + conftest.py）
- Phase 2: 1週間（ロジック抽出）
- Phase 3: 3-5日（エッジケース）
- **Total: 2-3週間**

## Dependencies

- pytest.iniの設定（既存）
- テストデータ（既存）
- Python 3.x

## Related Proposals

- PR-006: 機能検証実装（次のPhase）
- PR-002: 受入率レポート（calculate_acceptance_rate.py使用）

## Success Metrics

### Primary
- pytest --cov がパスする（>= 70%）

### Secondary
- 回帰バグ検知数の増加
- リファクタリングの実施回数の増加
- テスト実行時間の増加は許容範囲内（< 5分）

## Note

このPRはCritical優先度であるため、他のPRよりも優先して実施すること。
カバレッジ70%未達の場合、CIが常に失敗し続けるため、開発効率に悪影響を与える。
