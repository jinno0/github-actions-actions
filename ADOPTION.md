# Adopters List

This repository is used in the following projects:

## 🚀 Quick Start (5分で始める)

1. **Fork this repository**
2. **Copy the example workflow** for the action you want to use
3. **Install Claude CLI** on your self-hosted runner: `npm install -g @anthropic-ai/claude-code`
4. **Run the workflow**

詳しくは [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md) を参照してください。

---

## 🎯 Pilot Program (パイロット募集)

現在、パイロットプロジェクトを募集しています！

### 特典
- ✅ **無料セットアップサポート**: 導入から初期設定まで手厚くサポート
- ✅ **優先的機能対応**: 新機能のリクエストを優先的に実装
- ✅ **成功事例としての紹介**: 導入事例としてブログ等で紹介

### 申込み方法
1. このリポジトリを fork
2. [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md) を参照して導入
3. あなたのリポジトリ情報を以下の「Adopters」セクションに追加
4. Pull Request を送信

---

## 📊 Known Adopters

If you're using these AI Actions in your repository, please add a link below!

### Internal Projects

| Repository | Team | Actions Used | Notes |
|------------|------|--------------|-------|
| *[example/repo-1](https://github.com/example/repo-1)* | Platform Team | All 13 actions | Pilot project |
| *[example/repo-2](https://github.com/example/repo-2)* | Backend Team | review-and-merge, auto-merge | Trial run |

### External Adopters

| Repository | Organization | Actions Used | Adopted | Effects |
|------------|--------------|--------------|---------|---------|
| *[your-org/repo](https://github.com/your-org/repo)* | Your Org | action-fixer, auto-document | YYYY-MM | Review time -50%, Doc update time -80% |

> **Note**: 外部採用事例は現在募集中です。パイロットプログラムに参加して、成功事例として紹介されませんか？

---

## 📈 Adoption Success Stories (採用事例)

### [組織名/プロジェクト名]

- **導入アクション**: review-and-merge, auto-document
- **導入時期**: YYYY-MM
- **効果**:
  - レビュー時間が **50%削減**
  - ドキュメント更新工数が **80%削減**
  - AIレビューの受入率: **75%** (初月) → **85%** (3ヶ月後)
- **インタビュー**: [リンク]

> "AI Actions 導入により、開発者はコードレビューとドキュメント更新に費やしていた時間を、本質的な設計と実装に使えるようになりました。" — チームリーダー

---

## 🔍 Tracking Adoption

導入状況のスキャンには `scripts/scan_adoption.py` を使用してください:

```bash
# 組織内の導入状況をスキャン
python scripts/scan_adoption.py --org your-org --output ADOPTION_SCAN.md

# ADOPTION.md を自動更新
python scripts/scan_adoption.py --org your-org --update-adoption-md
```

---

**Note:** This list is self-reported and may not be exhaustive. To add your repository:
1. Fork this repository
2. Add your repository to the table above
3. Submit a Pull Request

詳しくは [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md) と [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。
