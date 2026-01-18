# Codex Skill

OpenAI Codex CLIを使用したコードレビュー・分析スキル。

## 機能

- **自動コードレビュー**: コードベース全体の包括的な分析
- **リアルタイム出力**: 進捗状況を表示しながら実行
- **ログ自動保存**: 全分析結果をタイムスタンプ付きで保存
- **ログ管理**: 古いログを自動削除（デフォルト: 最新10件）

## インストール

```bash
# Codex CLIがインストールされている必要があります
npm install -g @openai/codex
```

## 使用方法

### 基本使用

```bash
# コードレビュー（ログは自動保存）
python .claude/skills/codex/scripts/run_codex.py "Review this codebase for bugs"

# プロジェクトディレクトリを指定
python .claude/skills/codex/scripts/run_codex.py "Analyze architecture" --project-dir /path/to/project

# サンドボックス無効（慎重に使用）
python .claude/skills/codex/scripts/run_codex.py "Review code" --no-sandbox
```

### ログ保存先

ログは自動的に `.claude/skills/codex/logs/` に保存されます：

```
.claude/skills/codex/logs/
├── codex_20260118_123456.md  # タイムスタンプ付き
├── codex_20260118_234567.md
└── ...
```

### オプション

| オプション | 短縮形 | 説明 | デフォルト |
|---------|--------|------|----------|
| `--output` | `-o` | 出力ファイルパス | 自動生成 |
| `--project-dir` | - | 分析対象プロジェクト | 自動検出 |
| `--no-sandbox` | - | サンドボックス無効化 | 有効 |
| `--no-stream` | - | リアルタイム出力無効化 | 有効 |
| `--keep-logs` | - | 保存するログ数 | 10 |

### 使用例

```bash
# 出力ファイルを指定
python .claude/skills/codex/scripts/run_codex.py "Review code" \
  --output /path/to/custom_report.md

# 最新の5件のみログを保持
python .claude/skills/codex/scripts/run_codex.py "Analyze security" \
  --keep-logs 5

# 全ログを保持（削除なし）
python .claude/skills/codex/scripts/run_codex.py "Review code" \
  --keep-logs 0
```

## ログ形式

保存されるログファイルには、以下のメタデータが含まれます：

```markdown
# Codex Analysis Report

**Generated**: 2026-01-18T12:34:56
**Request**: Review this codebase for bugs
**Project**: /home/user/project

---

[分析結果がここに含まれます]
```

## 注意点

1. **実行時間**: 大規模なプロジェクトでは数十分かかる場合があります
2. **サンドボックス**: デフォルトでread-onlyモード（安全）
3. **ログサイズ**: 大規模な分析ではログファイルが大きくなる可能性があります
4. **Codex CLI**: 事前にインストールが必要です

## トラブルシューティング

### Codex CLIが見つからない

```bash
Error: Codex CLI not found. Please ensure it is installed and in your PATH.
```

**解決策**:
```bash
npm install -g @openai/codex
```

### ログが保存されない

**解決策**:
- `.claude/skills/codex/logs/` ディレクトリの書き込み権限を確認
- ディスク容量を確認

## ログのクリア

古いログは自動的に削除されますが、手動でクリアすることも可能：

```bash
# 全ログ削除
rm -rf .claude/skills/codex/logs/*

# 1週間以上前のログのみ削除
find .claude/skills/codex/logs/ -name "codex_*.md" -mtime +7 -delete
```
