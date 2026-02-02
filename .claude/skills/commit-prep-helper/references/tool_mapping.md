# プロジェクトタイプ別ツール設定

プロジェクトの種類に応じて使用するLint/Testツールのマッピング。

## プロジェクトタイプ検出アルゴリズム

### 検出優先順位
1. `package.json` 存在 → Node.js/TypeScript
2. `requirements.txt` または `pyproject.toml` 存在 → Python
3. `Cargo.toml` 存在 → Rust
4. `go.mod` 存在 → Go
5. `pom.xml` または `build.gradle` 存在 → Java
6. その他 → Unknown

## Node.js/TypeScript プロジェクト

### Lintツール
```json
{
  "eslint": {
    "command": "npx eslint",
    "options": ["--format=json"],
    "files": ".",
    "priority": 1
  },
  "prettier": {
    "command": "npx prettier",
    "options": ["--check"],
    "files": ".",
    "priority": 2
  }
}
```

### テストフレームワーク
```json
{
  "jest": {
    "command": "npx jest",
    "options": ["--coverage", "--passWithNoTests"],
    "config_files": ["jest.config.js", "jest.config.json", "package.json"],
    "priority": 1
  },
  "vitest": {
    "command": "npx vitest run",
    "options": ["--coverage"],
    "config_files": ["vitest.config.js", "vitest.config.ts", "vite.config.js"],
    "priority": 2
  },
  "mocha": {
    "command": "npx mocha",
    "options": ["--recursive"],
    "config_files": ["mocha.opts"],
    "priority": 3
  }
}
```

### ファイル拡張子
- JavaScript: `.js`, `.jsx`
- TypeScript: `.ts`, `.tsx`
- 設定ファイル: `.json`, `.js`, `.ts`
- ドキュメント: `.md`

## Python プロジェクト

### Lintツール
```json
{
  "black": {
    "command": "python -m black",
    "options": ["--check"],
    "files": ".",
    "priority": 1
  },
  "flake8": {
    "command": "flake8",
    "options": [],
    "files": ".",
    "priority": 2
  },
  "pylint": {
    "command": "pylint",
    "options": [],
    "files": ".",
    "priority": 3
  }
}
```

### テストフレームワーク
```json
{
  "pytest": {
    "command": "python -m pytest",
    "options": ["-v", "--cov=.", "--cov-report=term-missing"],
    "config_files": ["pytest.ini", "pyproject.toml", "setup.cfg"],
    "priority": 1
  },
  "unittest": {
    "command": "python -m unittest",
    "options": ["discover"],
    "config_files": [],
    "priority": 2
  }
}
```

### ファイル拡張子
- Python: `.py`
- 設定ファイル: `.ini`, `.cfg`, `.toml`
- ドキュメント: `.md`, `.rst`

## 実行順序

### 品質チェックの標準フロー
1. **Lintチェック** (優先度: 高)
   - コードスタイルと構文チェック
   - フォーマット検証

2. **テスト実行** (優先度: 高)
   - ユニットテスト実行
   - カバレッジ測定

3. **コードレビュー** (優先度: 中)
   - 静的解析
   - セキュリティチェック

### 各ツールのタイムアウト設定
- Lintツール: 30秒
- テストフレームワーク: 5分
- コードレビュー: 1分