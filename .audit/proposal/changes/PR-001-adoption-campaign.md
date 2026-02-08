# PR-001: 採用加速キャンペーンの実施

**Priority:** P0 (Critical)  
**Gap:** GAP-001 (外部採用0件)  
**Estimated Effort:** High (4-6週)

## 背景

現在、外部採用数が0件であり、プロジェクトの存在意義「組織全体の開発効率と品質を向上させる」が達成されていない。ADOPTION.mdには「Current adopters: Seeking pilot projects」と記載されており、早急な採用推進が必要。

## 提案する変更

### 1. パイロットプログラムの立ち上げ

**ファイル:** `ADOPTION_GUIDE.md` に以下を追加

- パイロット申込みフォームのリンク
- パイロット導入の特典（無料セットアップサポート、優先的機能対応）
- パイロット期間の明記（1ヶ月）
- 成功事例としてのインタビュー承諾

### 2. 採用手順の簡素化

**ファイル:** 新規 `ADOPTION.md` の拡充

```markdown
## 5分で始めるクイックスタート

1. このリポジトリをfork
2. 利用したいActionのexampleをコピー
3. Self-hosted runnerにClaude CLIをインストール
4. ワークフローを実行

詳しくは [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md) を参照してください。
```

### 3. 採用状況の追跡

**ファイル:** 新規 `scripts/scan_adoption.py` の実装

- 組織内の全リポジトリをスキャン
- `.github/workflows/` からこのリポジトリのActionを参照しているものを検出
- ADOPTION.mdに自動生成されたリストを出力

**使用方法:**
```bash
python scripts/scan_adoption.py --org your-org --output ADOPTION.md
```

### 4. 採用事例テンプレートの作成

**ファイル:** 新規 `ADOPTION.md` にテンプレート追加

```markdown
## 採用事例

### [組織名/プロジェクト名]

- **導入アクション:** review-and-merge, auto-document
- **導入時期:** YYYY-MM
- **効果:** レビュー時間が50%削減、ドキュメント更新工数が80%削減
- **インタビュー:** [リンク]
```

## 期待される効果

- **短期 (1ヶ月):** 3件以上のパイロット導入
- **中期 (3ヶ月):** 5件以上の本格採用
- **長期 (6ヶ月):** 採用事例の公開と社会的証明の確立

## 成功基準

- ADOPTION.mdに5件以上の採用リストが記載される
- README.mdの採用数が更新される
- 少なくとも2件の採用事例インタビューが公開される

## リスク

- **採用が進まない:** パイロット申込みが少ない
  - 緩和策: GitHub Discussionsでアナウンス、直接DMで依頼
- **導入サポートの負荷:** パイロット導入のサポート工数
  - 緩和策: ドキュメントの充実、先着3件限定

## 検証方法

1. PR作成後、ADOPTION.mdの更新を確認
2. scan_adoption.pyを実行し、組織内導入状況を把握
3. 2週間後にパイロット申込み数を確認

## 次のアクション

1. ADOPTION.mdとADOPTION_GUIDE.mdの更新
2. scan_adoption.pyの実装とテスト
3. パイロット申込みフォームの作成 (Google Forms など)
4. 組織内でのアナウンス (Slack, Email, GitHub Discussions)

---

**依存関係:** なし  
**ブロッカー:** なし  
**関連PR:** PR-003 (組織内導入状況の可視化)
