# PR-001: 機能的テスト（Integration Testing）の導入

**優先度**: HIGH (ISS-001)
**関連ギャップ**: ISS-001 - 機能的テストの欠如
**状態**: Proposed

## 概要

TESTING.mdのPhase 2で計画されている統合テストを導入し、Actionsの実行時動作を検証する。
現状の構造的テスト（97.51%カバレッジ）に加え、actツールを使用した機能的テストを実装する。

## 現状

- 構造的テストのみ実装済み（YAML構文、ファイル存在確認）
- 機能的テストは未実装
- TESTING.md:156-186でPhase 2統合テストが計画されているが未着手

## 提案内容

### Phase 1: actツールのセットアップ（1-2日）

1. **actのインストールと検証**
   - GitHub Actionsをローカルで実行するためのactツールをセットアップ
   - `.github/workflows/` にテスト用workflowを作成

2. **テスト環境の構築**
   - Mock GitHub APIレスポンスの準備
   - テスト用GitHub Tokenのモック化

### Phase 2: 基本的な統合テスト実装（3-5日）

1. **各Actionの smoke test**
   ```python
   # tests/integration/test_review_and_merge_smoke.py
   @pytest.mark.integration
   def test_review_and_merge_smoke(action_runner):
       """review-and-merge actionが正常に実行されること"""
       result = action_runner.run(
           action="review-and-merge",
           inputs={
               "github-token": "${{ secrets.GITHUB_TOKEN }}",
               "claude-model": "sonnet"
           }
       )
       assert result.exit_code == 0
   ```

2. **出力値の検証**
   - 各Actionのoutputsが正しく設定されることを確認
   - エラーハンドリングの検証

### Phase 3: GitHub APIモックの強化（2-3日）

1. **GitHub APIレスポンスのモック化**
   - PR情報のモック
   - Issue情報のモック
   - Repository情報のモック

2. **Claude CLI呼び出しのモック化**
   - Claude CLIを実際に呼び出さず、テスト用レスポンスを返す
   - コマンドライン引数の検証

### Phase 4: カバレッジ目標の設定（1日）

- 構造的テスト: 97.51% (維持)
- 統合テスト: 新規で50%以上のActionをカバー
- 目標: 全13 Actionsのうち、少なくとも7つで統合テストを実装

## 実装手順

### 1. プロジェクト構造の変更

```
tests/
├── unit/              # 既存の構造的テスト（移動なし）
├── integration/       # 新規：統合テスト
│   ├── conftest.py   # act runnerのfixture
│   ├── test_review_and_merge_integration.py
│   ├── test_auto_merge_integration.py
│   └── ...
└── fixtures/          # 新規：テストデータ
    ├── mock_github_api.py
    └── sample_prs/
```

### 2. 依存関係の追加

`requirements.txt` または `pyproject.toml` に追加:

```
pytest>=8.0.0
pytest-mock>=3.12.0
responses>=0.24.0  # GitHub APIモック用
```

### 3. conftest.pyの拡張

```python
# tests/integration/conftest.py
import pytest
import subprocess
from pathlib import Path

@pytest.fixture
def action_runner(tmp_path):
    """actを使用してActionを実行するRunner"""
    class ActionRunner:
        def run(self, action, inputs):
            # actコマンド構築
            cmd = [
                "act",
                "-W", f".github/workflows/test-{action}.yml",
                "--container-architecture", "linux/amd64",
                "--bind" # 必要に応じて
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result
    return ActionRunner()
```

### 4. 最初の統合テスト実装

`review-and-merge` actionから開始（最も重要なActionのため）:

```python
# tests/integration/test_review_and_merge_integration.py
import pytest
import yaml
from pathlib import Path

@pytest.mark.integration
def test_review_and_merge_action_structure():
    """review-and-merge actionの基本構造を検証"""
    action_yml = Path("actions/review-and-merge/action.yml")
    config = yaml.safe_load(action_yml.read_text())

    assert config["runs"]["using"] == "composite"
    assert "github-token" in config["inputs"]

@pytest.mark.integration
def test_review_and_merge_steps_exist():
    """action.ymlで定義されたstepsが存在することを確認"""
    action_yml = Path("actions/review-and-merge/action.yml")
    config = yaml.safe_load(action_yml.read_text())

    step_names = [s.get("name", s.get("id", "")) for s in config["runs"]["steps"]]
    assert "Checkout PR" in step_names
    assert "Review" in step_names
```

## 期待効果

1. **品質向上**: 実行時のバグを早期発見
2. **信頼性向上**: 構造的テストだけでは検知できない問題を検出
3. **ドキュメント化**: 統合テストがActionsの使用例として機能
4. **リファクタリングの安全性**: 既存機能の動作保証

## 副作用とリスク

1. **実行時間の増加**: 統合テストは構造的テストより遅い
   - 対策: CIで統合テストを分離、タグ付けで実行制御
2. **メンテナンスコスト**: モックの更新が必要
   - 対策: モックを最小限に、安定したインターフェースに依存
3. **学習コスト**: 開発者がactに慣れる必要がある
   - 対策: ドキュメント作成、ワークショップ開催

## 検証方法

1. テストが通過すること: `pytest tests/integration/ -v`
2. カバレッジレポートで統合テストカバレッジが計測されること
3. CIで統合テストが自動実行されること

## ロールバック計画

- 統合テストは既存の構造的テストに影響を与えない
- 問題発生時は、統合テストを `.gitignore` で除外して元の状態に戻す可能性

## 関連ファイル

- 変更: `TESTING.md` (Phase 2 statusを更新)
- 新規: `tests/integration/conftest.py`
- 新規: `tests/integration/test_review_and_merge_integration.py`
- 新規: `requirements-dev.txt` (依存関係追加)

## 次のアクション

1. 本提案のレビューと承認
2. actツールのインストールと基本検証
3. 最初の統合テスト（review-and-merge）の実装
4. ドキュメント更新（TESTING.md）

---

**作成日**: 2025-02-03
**作成者**: Repo Genesis Auditor (run-initial)
**仮定に基づく**: なし（事実に基づく提案）
