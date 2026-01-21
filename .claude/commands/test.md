---
description: プロジェクト全体のテストを実行
---

# テスト実行

プロジェクト全体のテスト（Python + TypeScript）を実行します。

## 実行内容

1. **Pythonテスト (Pytest)**
   ```bash
   cd api && pytest
   ```
   - 全APIエンドポイントのテスト
   - モデル・CRUD操作のテスト
   - ページ構成・パネル配置のテスト

2. **TypeScript型チェック**
   ```bash
   cd web && npm run typecheck
   ```
   - Strict mode有効
   - 全TypeScriptファイル検証
   - エラー0件が目標

3. **Vitestテストスイート** (web/ 配下)
   ```bash
   cd web && npm test
   ```

## 期待される結果

✅ **Python**: 全テストパス
✅ **TypeScript**: エラー0件
✅ **Tests**: 全テストパス

## テスト対象

### Python (api/)
- `tests/test_page_composition_api.py`: ページ構成API
- `tests/test_*.py`: CRUD・認証・その他エンドポイント

### TypeScript (web/)
- Next.jsコンポーネント・ページ
- ユーティリティ関数

## カバレッジ確認

```bash
# Python
cd api && pytest --cov=.

# TypeScript
cd web && npm run test:coverage
```

## 失敗時の対処

### Pythonテスト失敗
```bash
# 詳細モードで実行
cd api && pytest -v

# 特定のテストファイルのみ
cd api && pytest tests/test_page_composition_api.py

# 特定のテストメソッドのみ
cd api && pytest tests/test_page_composition_api.py::TestPageComposition::test_compose_page_success
```

### TypeScriptエラー
```bash
# エラー詳細確認
cd web && npm run typecheck

# 型定義確認
cd web && cat tsconfig.json
```

### TypeScriptテスト失敗
```bash
# 詳細モードで実行
cd web && npm test -- --reporter=verbose

# 特定のテストファイルのみ
cd web && npm test -- path/to/test.spec.ts
```

---

実行完了後、全テストが合格していることを確認してください。
