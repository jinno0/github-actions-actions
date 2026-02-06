# PR-003: 組織導入状況の追跡機能

**Priority:** High
**Gap ID:** GAP-004

## 概要

PURPOSE.md の成功条件に「組織内の複数のリポジトリで採用」とあるが、
導入数やフィードバックを収集する仕組みがない。このPRでは、導入リポジトリを
追跡し、フィードバックを収集する仕組みを追加する。

## 変更内容

### 1. 導入リポジトリ登録ファイル

**File:** `ADOPTION.md` (新規作成)

```markdown
# Adopters List

This repository is used in the following projects:

## Known Adopters

If you're using these AI Actions in your repository, please add a link below!

### External Projects

| Repository | Team | Actions Used | Notes |
|------------|------|--------------|-------|
| [Your Repo](https://github.com/org/repo) | Team Name | review-and-merge, auto-merge | Using for CI/CD automation |

### Internal Projects

| Repository | Team | Actions Used | Notes |
|------------|------|--------------|-------|
| [example/repo-1](https://github.com/example/repo-1) | Platform Team | All 13 actions | Pilot project |
| [example/repo-2](https://github.com/example/repo-2) | Backend Team | review-and-merge, spec-to-code | Trial run |

## How to Register Your Repository

1. Fork this repository
2. Edit `ADOPTION.md` to add your repository
3. Submit a PR with title: "Add adoption: [your-repo-name]"

## Adoption Statistics

- **Total Adopters:** 2
- **Most Used Actions:** review-and-merge (2), auto-merge (2)
- **Last Updated:** 2026-02-07

---

**Note:** This list is self-reported and may not be exhaustive.
```

### 2. 導入状況スキャンスクリプト

**File:** `scripts/scan_adoption.py` (新規作成)

```python
#!/usr/bin/env python3
"""
Scan organization repositories for AI Actions usage.

This script searches GitHub for repositories that reference our actions
by looking for workflow files that use './actions/' paths.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

def try_scan_github_org():
    """Attempt to scan organization repositories using GitHub CLI."""
    result = os.system("gh --version >/dev/null 2>&1")
    if result != 0:
        print("⚠️  GitHub CLI not found. Skipping organization scan.")
        return []

    # Check if we're in a GitHub organization context
    try:
        org = os.getenv("GITHUB_ORG")
        if not org:
            print("⚠️  GITHUB_ORG environment variable not set. Skipping organization scan.")
            return []

        # Search for repositories using our actions
        cmd = f'gh search repos --org {org} --json name,url --limit 100'
        print(f"Scanning organization: {org}")
        print(f"Command: {cmd}")

        # Note: This is a simplified scan. Real implementation would use GitHub API
        # to search workflow files for './actions/' references.

        return []
    except Exception as e:
        print(f"❌ Error scanning organization: {e}")
        return []

def generate_adoption_report():
    """Generate adoption statistics from ADOPTION.md."""
    adoption_file = Path("ADOPTION.md")

    if not adoption_file.exists():
        print("⚠️  ADOPTION.md not found. Creating template...")
        return {
            "total_adopters": 0,
            "internal_projects": 0,
            "external_projects": 0,
            "most_used_actions": [],
            "last_updated": datetime.now().isoformat()
        }

    content = adoption_file.read_text()

    # Parse adopters from markdown table
    # This is a simplified parser. Real implementation would use a proper markdown parser.
    adopters = []
    for line in content.split('\n'):
        if '|' in line and 'http' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4 and parts[1].startswith('['):
                adopters.append({
                    "name": parts[1],
                    "team": parts[2],
                    "actions": parts[3],
                    "notes": parts[4] if len(parts) > 4 else ""
                })

    return {
        "total_adopters": len(adopters),
        "adopters": adopters,
        "last_updated": datetime.now().isoformat()
    }

def main():
    print("🔍 AI Actions Adoption Scanner")
    print("=" * 50)
    print()

    # Try to scan organization (requires gh CLI and GITHUB_ORG)
    repos = try_scan_github_org()

    # Generate report from ADOPTION.md
    report = generate_adoption_report()

    print(f"📊 Adoption Statistics:")
    print(f"  Total Adopters: {report['total_adopters']}")
    print(f"  Last Updated: {report['last_updated']}")
    print()

    if report['total_adopters'] > 0:
        print("✅ Adoption tracking is working!")
    else:
        print("ℹ️  No adopters registered yet.")
        print()
        print("Next steps:")
        print("  1. Add your repository to ADOPTION.md")
        print("  2. Set up GITHUB_ORG environment variable for automatic scanning")
        print("  3. Create an issue to encourage adoption")

    # Save report
    output = Path("metrics/adoption_report.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n📄 Report saved to: {output}")

if __name__ == "__main__":
    main()
```

### 3. 導入促進Issueテンプレート

**File:** `.github/ISSUE_TEMPLATE/adoption_report.yml` (新規作成)

```yaml
name: Adoption Report
description: Report your adoption of AI Actions
title: "[Adoption] Use AI Actions in my repository"
labels: ["adoption", "user-feedback"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for adopting AI Actions! Please fill out this form to help us track usage and improve our tools.

  - type: input
    id: repository
    attributes:
      label: Repository URL
      description: Link to your repository
      placeholder: https://github.com/org/repo
    validations:
      required: true

  - type: input
    id: team
    attributes:
      label: Team/Organization
      description: Your team or organization name
      placeholder: Platform Team
    validations:
      required: true

  - type: checkboxes
    id: actions
    attributes:
      label: Which actions are you using?
      description: Select all that apply
      options:
        - label: review-and-merge
        - label: spec-to-code
        - label: auto-refactor
        - label: auto-document
        - label: release-notes-ai
        - label: action-fixer
        - label: auto-merge
        - label: auto-rebase
        - label: bulk-merge-prs
        - label: bulk-rebase-prs
        - label: pr-review-enqueuer
        - label: publish-pr
        - label: review-auto-merge

  - type: textarea
    id: experience
    attributes:
      label: How is your experience?
      description: Tell us about your experience using these actions
      placeholder: We've been using review-and-merge for 2 weeks and it's been great...
    validations:
      required: false

  - type: textarea
    id: feedback
    attributes:
      label: Feedback or suggestions
      description: Any feedback or suggestions for improvement?
      placeholder: It would be great if...
    validations:
      required: false
```

### 4. README.md の更新

**File:** `README.md`

以下のセクションを追加：

```markdown
## 🚀 Adoption

Are you using these AI Actions in your repository? We'd love to hear from you!

- **Add your repository:** Edit [ADOPTION.md](ADOPTION.md) and submit a PR
- **Share feedback:** Open an [Adoption Report](https://github.com/your-org/github-actions-actions/issues/new?template=adoption_report.yml)

Current adopters: [See ADOPTION.md](ADOPTION.md)
```

## 実装手順

1. `ADOPTION.md` を作成
2. `scripts/scan_adoption.py` を作成し、実行権限を付与
3. `.github/ISSUE_TEMPLATE/adoption_report.yml` を作成
4. README.md にAdoptionセクションを追加
5. `python scripts/scan_adoption.py` を実行して動作確認
6. (オプション) Organizationのメンバーに導入を促すアナウンスを行う

## 期待される効果

- ✅ 導入リポジトリが可視化される
- ✅ PURPOSE.md の成功条件（組織内採用）の進捗が測れる
- ✅ ユーザーフィードバックが収集できる
- ✅ 社内的な成功事例が蓄積され、他チームへの導入が容易になる

## ロールバック手順

1. `ADOPTION.md` を削除
2. `scripts/scan_adoption.py` を削除
3. `.github/ISSUE_TEMPLATE/adoption_report.yml` を削除
4. README.md のAdoptionセクションを削除

## 検証方法

```bash
# 1. スクリプトが実行できるか
python scripts/scan_adoption.py

# 2. レポートが生成されるか
cat metrics/adoption_report.json | jq .

# 3. ADOPTION.md が有効なMarkdownか
grep -q "## Adopters List" ADOPTION.md && echo "✅ Valid structure"

# 4. Issueテンプレートが有効か
yamllint .github/ISSUE_TEMPLATE/adoption_report.yml
```

## 副作用とリスク

- **リスク:** 導入数が0の場合、公開していることが逆にネガティブな印象を与える可能性
- **緩和策:** 最初は「Pilot Projects」として内部プロジェクトのみをリストアップする
- **リスク:** メンテナンスの手間が増える（ADOPTION.mdの更新）
- **緩和策:** Issueテンプレートによる自己申告制にし、定期的にマージする

## 関連ファイル

- `ADOPTION.md` (新規作成)
- `scripts/scan_adoption.py` (新規作成)
- `.github/ISSUE_TEMPLATE/adoption_report.yml` (新規作成)
- `README.md` (更新)
- `metrics/adoption_report.json` (生成物)

## 参考情報

- `ADOPTION_GUIDE.md` (既存ドキュメント)
- `PURPOSE.md` の成功条件セクション
