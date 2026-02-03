# PR-002: 導入状況の可視化と進捗レポートの作成

**提出者**: Repo Genesis Auditor (Run #2026-02-03T23:20:15Z)
**優先度**: 中
**種別**: 新規機能追加
**推定工数**: 中（4-8時間）

---

## 概要

PURPOSE.mdの成功条件（「組織内の複数のリポジトリで採用」）とPhase 3の進捗（「組織内プロジェクトへの導入とフィードバック収集」）を追跡するための仕組みを導入し、導入状況を可視化します。

## 問題の背景

### 現状
- **PURPOSE.md**: 成功条件で「組織内の複数のリポジトリで採用されること」を掲げている
- **Phase 3**: 「組織内プロジェクトへの導入とフィードバック収集」が進行中
- **課題**: 具体的な導入数、どのリポジトリで使用されているか、ユーザーフィードバックなどの情報が公開されていない

### 影響
- Phase 3の進捗評価が困難
- 成功条件の達成状況が不明
- 改善の優先順位決定に必要なデータが不足

---

## 提案するアクション

### Phase 1: 導入状況の追跡機能の実装

#### ステップ 1: 導入状況スクリプトの作成
**新規ファイル**: `scripts/track_adoption.py`

**機能**:
- 組織内の全リポジトリをスキャン
- `.github/workflows/` 内で `github-actions-actions` を参照しているリポジトリを検出
- 使用されているActionの種類と頻度を集計
- 結果をJSON/Markdown形式で出力

**実装例**:
```python
#!/usr/bin/env python3
"""
Track adoption of github-actions-actions across organization repositories.
"""
import os
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def scan_repositories(org_root: Path) -> dict:
    """Scan all repositories under organization root."""
    repos = []
    for repo_path in org_root.iterdir():
        if not repo_path.is_dir() or repo_path.name.startswith('.'):
            continue

        workflows_dir = repo_path / '.github' / 'workflows'
        if not workflows_dir.exists():
            continue

        usage = analyze_workflows(workflows_dir)
        if usage:
            repos.append({
                'name': repo_path.name,
                'path': str(repo_path),
                'usage': usage
            })

    return repos

def analyze_workflows(workflows_dir: Path) -> dict:
    """Analyze workflow files for github-actions-actions usage."""
    actions_used = defaultdict(int)

    for workflow_file in workflows_dir.glob('*.yml'):
        content = workflow_file.read_text()

        # Check for references to github-actions-actions
        if 'github-actions-actions' in content:
            # Extract action names
            pattern = r'uses:.*github-actions-actions/(\w+)'
            for match in re.finditer(pattern, content):
                action_name = match.group(1)
                actions_used[action_name] += 1

    return dict(actions_used) if actions_used else None

def generate_report(repos: list, output_format: str = 'markdown') -> str:
    """Generate adoption report."""
    total_repos = len(repos)
    action_counts = defaultdict(int)

    for repo in repos:
        for action, count in repo['usage'].items():
            action_counts[action] += count

    if output_format == 'markdown':
        report = [
            "# AI Actions 導入状況レポート",
            f"\n**生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n## サマリー",
            f"- **導入リポジトリ数**: {total_repos}",
            f"- **利用Action種類**: {len(action_counts)}",
            f"\n## Action別使用状況",
            f"\n| Action | 使用回数 |",
            f"|--------|----------|"
        ]

        for action, count in sorted(action_counts.items(), key=lambda x: -x[1]):
            report.append(f"| {action} | {count} |")

        report.append(f"\n## 導入リポジトリ一覧")
        for repo in repos:
            actions_str = ', '.join(repo['usage'].keys())
            report.append(f"- **{repo['name']}**: {actions_str}")

        return '\n'.join(report)

    return json.dumps({
        'generated_at': datetime.now().isoformat(),
        'total_repos': total_repos,
        'action_counts': dict(action_counts),
        'repositories': repos
    }, indent=2)

def main():
    org_root = Path('/home/jinno')  # Adjust to your organization root

    print("🔍 Scanning repositories for github-actions-actions usage...")
    repos = scan_repositories(org_root)

    if not repos:
        print("⚠️  No repositories found using github-actions-actions")
        return

    # Generate markdown report
    report_md = generate_report(repos, 'markdown')
    output_md = Path('/home/jinno/github-actions-actions/docs/adoption_report.md')
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(report_md, encoding='utf-8')

    # Generate JSON report
    report_json = generate_report(repos, 'json')
    output_json = Path('/home/jinno/github-actions-actions/metrics/adoption_status.json')
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(report_json, encoding='utf-8')

    print(f"✅ Report generated:")
    print(f"   - Markdown: {output_md}")
    print(f"   - JSON: {output_json}")

if __name__ == '__main__':
    main()
```

---

#### ステップ 2: CIへの統合
**新規ファイル**: `.github/workflows/generate-adoption-report.yml`

```yaml
name: 'Generate Adoption Report'

on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight
  workflow_dispatch:

permissions:
  contents: read

jobs:
  generate-report:
    runs-on: self-hosted
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Generate adoption report
        run: |
          python3 scripts/track_adoption.py

      - name: Upload report
        run: |
          git config user.name 'GitHub Actions'
          git config user.email 'actions@github.com'

          if [[ -n $(git diff docs/adoption_report.md) ]]; then
            git add docs/adoption_report.md metrics/adoption_status.json
            git commit -m "chore: Update adoption report [skip ci]"
            git push
          fi
```

---

### Phase 2: README.mdへの追跡結果の反映

#### 変更内容
README.mdに「導入状況」セクションを追加:

```markdown
## 📊 導入状況

組織内での利用状況を公開しています。詳細なレポートは[こちら](docs/adoption_report.md)を参照してください。

- **導入リポジトリ数**: XX件
- **利用Action種類**: XX種
- **最新更新**: YYYY-MM-DD
```

---

### Phase 3: PURPOSE.mdの更新

#### 変更内容
PURPOSE.md:25の進捗を更新:

```yaml
### Phase 3: Stabilization & Adoption (In Progress)
- ✅ 各Actionの検証用ワークフローの作成 (`examples/`)
- ✅ 各Actionの導入ガイドの作成 (`instructions/`)
- ⬜ 組織内プロジェクトへの導入とフィードバック収集
  - ✅ 導入状況追跡スクリプトの実装
  - ⬜ 定期的なレポート生成と公開
- ✅ ドキュメント（README）の整備
```

---

## 実行手順

### ステップ 1: スクリプトの作成
1. `scripts/track_adoption.py` を作成
2. 実行権限を付与: `chmod +x scripts/track_adoption.py`

### ステップ 2: 手動実行テスト
```bash
cd /home/jinno/github-actions-actions
python3 scripts/track_adoption.py
```

### ステップ 3: 結果の確認
```bash
cat docs/adoption_report.md
cat metrics/adoption_status.json
```

### ステップ 4: CIの設定
1. `.github/workflows/generate-adoption-report.yml` を作成
2. GitHub ActionsにPush

### ステップ 5: READMEとPURPOSE.mdの更新
1. README.mdに導入状況セクションを追加
2. PURPOSE.mdを更新

---

## 成功の基準

- [ ] `scripts/track_adoption.py` がエラーなく実行できる
- [ ] 組織内の導入状況が `docs/adoption_report.md` に出力される
- [ ] CIで定期的にレポートが更新される
- [ ] README.mdで導入状況が公開されている
- [ ] PURPOSE.mdの進捗が更新されている

---

## 副作用とリスク

### 副作用
- **プライバシー**: 全リポジトリをスキャンするため、リポジトリ名が公開される
- **実行時間**: 組織内のリポジトリ数によるが、スキャンに数分〜数十分かかる可能性

### リスク
- **スキャン権限**: 組織の全リポジトリにアクセスできる必要がある
- **誤検出**: `github-actions-actions` という文字列を含むコメントや他の記述も検出する可能性

### 対策
- スキャン対象を `.github/workflows/` の `.yml` ファイルに限定
- 実行権限の適切な設定（CIで実行する場合）

---

## ロールバック手順

### スクリプトの削除
```bash
cd /home/jinno/github-actions-actions
rm scripts/track_adoption.py
rm .github/workflows/generate-adoption-report.yml
git checkout README.md PURPOSE.md
```

### 生成されたレポートの削除
```bash
rm docs/adoption_report.md
rm metrics/adoption_status.json
```

---

## 改善のアイデア（将来の拡張）

1. **フィードバック収集**: 各リポジトリのメンテナにアンケートを送信
2. **アクティビティ追跡**: 実際にActionが実行された回数を追跡
3. **バージョン追跡**: 各リポジトリがどのバージョンのActionを使用しているかを追跡
4. **グラフ化**: 時系列での導入数の推移をグラフ化

---

## 次のアクション

1. **スクリプト実装**: `scripts/track_adoption.py` を作成
2. **手動テスト**: ローカルでスクリプトを実行し、結果を確認
3. **CI統合**: 定期実行用のワークフローを作成
4. **ドキュメント更新**: README.mdとPURPOSE.mdを更新
5. **初回レポート公開**: 最初の導入状況レポートを生成

---

## 参考資料

- PURPOSE.md:25（Phase 3の進捗）
- .audit/analysis/gap.yml（Phase 3: 導入状況の可視化不足）
- .audit/log/claims.ndjson（C-012: 実際のプロダクト利用状況が不明）
