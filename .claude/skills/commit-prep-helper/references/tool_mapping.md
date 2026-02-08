# プロジェクトタイプ別ツール設定

プロジェクトの種類に応じて使用するLint/Testツールのマッピング。

## プロジェクトタイプ検出アルゴリズム

### 検出優先順位
1. `requirements.txt` または `pyproject.toml` 存在 → Python
2. `package.json` 存在 → Node.js/TypeScript
3. その他 → Unknown

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