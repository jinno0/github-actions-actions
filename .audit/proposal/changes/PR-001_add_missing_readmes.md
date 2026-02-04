# PR-001: Add Missing README.md for Actions

**Priority:** HIGH
**Gap ID:** GAP-002
**Estimated Effort:** 2-4 hours

---

## Summary

9つのActionにREADME.mdが不足しているため、ドキュメント網羅性を100%にするためのPRです。

---

## Problem

検証の結果、以下のActionにREADME.mdが存在しません:

- action-fixer
- pr-review-enqueuer
- bulk-rebase-prs
- release-notes-ai
- auto-rebase
- review-auto-merge
- auto-merge
- bulk-merge-prs
- publish-pr

この状態では、利用者が各Actionの概要や使用方法を把握できません。

---

## Proposed Changes

### 1. README.mdの作成

各ActionのディレクトリにREADME.mdを作成します。

#### テンプレート構成

```markdown
# {Action Name}

## Overview
{Actionの概要}

## Prerequisites
- Self-hosted Runner with Claude Code CLI
- ...

## Inputs
| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| ... | ... | ... | ... |

## Outputs
| Output | Description |
|--------|-------------|
| ... | ... |

## Usage Example
\`\`\`yaml
steps:
  - uses: ./actions/{action-name}
    with:
      ...
\`\`\`

## Setup Guide
詳細な導入手順については [instructions/{action-name}.md](../../instructions/{action-name}.md) を参照してください。
```

### 2. 自動化チェックの追加

CIにドキュメント網羅性チェックを追加します。

#### 新規テストファイル: `tests/test_documentation_coverage.py`

\`\`\`python
import pytest
from pathlib import Path

def test_all_actions_have_readme():
    \"\"\"全てのActionにREADME.mdが存在すること\"\"\"
    actions_dir = Path("actions")
    missing = []

    for action_dir in actions_dir.iterdir():
        if action_dir.is_dir() and not action_dir.name.startswith("_"):
            readme = action_dir / "README.md"
            if not readme.exists():
                missing.append(action_dir.name)

    assert len(missing) == 0, f"READMEが不足しているAction: {missing}"

def test_all_actions_have_setup_guide():
    \"\"\"全てのActionにSetup Guideが存在すること\"\"\"
    instructions_dir = Path("instructions")
    actions_dir = Path("actions")

    action_names = [
        d.name for d in actions_dir.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    ]

    missing = []
    for action_name in action_names:
        guide = instructions_dir / f"{action_name}.md"
        if not guide.exists():
            missing.append(action_name)

    # libはSetup Guideが不要な除外ケース
    missing = [m for m in missing if m != "lib"]

    assert len(missing) == 0, f"Setup Guideが不足しているAction: {missing}"
\`\`\`

---

## Success Criteria

- [ ] 全てのActionにREADME.mdが存在する
- [ ] README.mdには概要、Inputs、Outputs、使用例が含まれている
- [ ] CIでドキュメント網羅性がチェックされる
- [ ] `pytest tests/test_documentation_coverage.py` がパスする

---

## Rollback Plan

問題がある場合は、作成したREADME.mdを削除してください。

```bash
git rm actions/*/README.md
```

---

## Related Issues

- Gap ID: GAP-002
- Issue: ISS-002
