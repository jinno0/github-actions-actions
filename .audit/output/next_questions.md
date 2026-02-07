# 確認事項と仮定の報告

対話ができないため、以下の仮定に基づいて監査を完了させました。
認識が異なる場合は `.audit/config/intent.yml` を修正してください。

---

## 適用した仮定

| ID | 項目 | 仮定した値 | 根拠 | 自信度 |
|----|------|------------|------|--------|
| ASM-001 | ターゲットユーザー | GitHub Organizationを使用する企業や組織 | SYSTEM_CONSTITUTION.mdで「組織全体のGitHub Actions」に明記 | high |
| ASM-002 | 実行環境 | Self-hosted runnerを運用している環境 | README.mdで「Self-hosted runner上で動作するClaude Code CLI」を前提 | high |
| ASM-003 | テストカバレッジ目標 | >= 70% | README.mdに「このプロジェクトでは、テストカバレッジ >= 70% を目標」と明記 | high |
| ASM-004 | AIレビュー受入率目標 | >= 70% | README.mdにAIレビューの受入率目標として「>= 70%」と記載 | high |
| ASM-005 | デプロイ方式 | Composite Actionsのみ | SYSTEM_CONSTITUTION.mdで「非Composite Action（Docker/JavaScript）は含まない」と明記 | high |
| ASM-006 | 導入実績 | 2 pilot projects | README.mdに「Current adopters: (2 pilot projects)」と記載 | high |

**全ての仮定は「high confidence（高信頼度）」であり、ドキュメントの明示的な記述に基づいています。**

---

## 質問（次回の精度向上のため）

### 高優先度（GAP解消に必要）

1. **[C-201] AIレビュー受入率の実際の数値**
   - **現在の認識:** READMEに「計測中 (データ収集段階)」と記載されているのみ
   - **確認したい点:** 
     - 現在の受入率は何%か？
     - 過去30日間の推移はどうなっているか？
     - 目標の70%に対して、現状は上回っているか下回っているか？
   - **確認方法:** `python scripts/calculate_acceptance_rate.py --time-period 30d`

2. **[C-203] 2件のパイロットプロジェクトからの具体的なフィードバック内容**
   - **現在の認識:** 導入実績はあるが、フィードバックの詳細が不明
   - **確認したい点:**
     - どのActionsをどのくらい使っているか？
     - 時間の節約効果などの定量評価はあるか？
     - 困っている点や改善要望は何か？
     - AIレビューの品質に満足しているか？
   - **確認方法:** パイロットプロジェクトの担当者へのインタビュー、ADOPTION.mdの確認

3. **[C-204] 各Actionの実際の使用頻度**
   - **現在の認識:** テレメトリー機能は実装済みだが、集計結果が未公開
   - **確認したい点:**
     - どのActionが最も使われているか？
     - 逆に、全く使われていないActionはあるか？
     - 使用頻度に時間的な傾向はあるか？
   - **確認方法:** `python scripts/aggregate_metrics.py` の実行結果確認

### 中優先度（改善計画に役立つ）

4. **[C-202] テレメトリー収集状況（有効/無効の比率）**
   - **確認したい点:**
     - オプトアウト率は何%か？
     - テレメトリー収集に参加しているリポジトリ数は？
   - **確認方法:** `python scripts/generate_telemetry_report.py`

5. **[C-207] AIレビューの誤検知（false positive）の発生頻度**
   - **確認したい点:**
     - 「rejected」や「needs_work」になる主な理由は何か？
     - 誤検知の傾向はあるか？（特定のパターンで誤検知が多い等）
   - **確認方法:** レビューアウトカムの詳細分析

### 低優先度（補完情報）

6. **[C-205] 本番環境でのClaude Code CLIのバージョン分布**
   - **確認したい点:** どのバージョンのClaude CLIが最も使われているか？
   - **確認方法:** テレメトリーデータ内のCLIバージョン情報

7. **パイロット導入における具体的な成功事例**
   - **確認したい点:** 
     - カスタムレビュールールを導入しているか？
     - 導入プロセスで困った点はあったか？
     - 他のチームへのアドバイスは？

---

## 不明点の扱い

今回の監査では、以下の**7つの不明点（unknowns）**を特定しました：

- **C-201:** AIレビュー受入率の実際の数値
- **C-202:** テレメトリー収集状況（有効/無効の比率）
- **C-203:** 2件のパイロットプロジェクトからの具体的なフィードバック内容
- **C-204:** 各Actionの実際の使用頻度
- **C-205:** 本番環境でのClaude Code CLIのバージョン分布
- **C-206:** パイロット導入における課題や改善要望の詳細
- **C-207:** AIレビューの誤検知（false positive）の発生頻度

これらの不明点は**技術的な欠陥ではなく、観測データの不足**です。`.audit/proposal/roadmap.md`に記載した改善策を実行することで、これらの不明点を解消できます。

---

## 次回監査時の改善方法

次回14_repo_genesis_auditorを実行する際は、以下のファイルを更新しておくと、より精度の高い監査が可能です：

1. **`.audit/config/intent.yml`**
   - 仮定（assumptions）が正しければそのまま
   - 認識が異なる場合は値を修正
   - 新たに分かった品質目標を追加

2. **実行結果の記録**
   - `scripts/calculate_acceptance_rate.py` の結果を `metrics/` に保存
   - テレメトリーレポートを `metrics/` に保存
   - フィードバックを `ADOPTION.md` または専用Issueに記録

3. **改善実施の記録**
   - `.audit/proposal/roadmap.md` の各フェーズ完了時に✅チェック
   - 実施した改善の結果を記録

---

**Generated:** 2026-02-07T13:26:48
**Process:** Non-blocking autonomous audit completed
**Next Step:** Review assumptions, clarify unknowns, execute roadmap
