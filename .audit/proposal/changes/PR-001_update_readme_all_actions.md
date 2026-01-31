# PR-001: Update README.md to Document All 13 Actions

## Summary
README.md currently documents only 6 of 13 available actions (46% coverage). This PR updates the README to include all 13 actions with consistent formatting and descriptions.

## Problem
- Users cannot discover 7 available actions from README
- Reduces discoverability and adoption
- Violates hub repository principle of visibility

## Proposed Changes

### 1. Update README.md Actions Table
Replace the current 6-action table with a complete 13-action table:

| Category | Action | Purpose | Documentation |
|----------|--------|---------|---------------|
| **Core Development** | review-and-merge | AIがコードをレビューし自動マージ（Auto-Fix標準装備） | [Guide](./instructions/review-and-merge.md) |
| | spec-to-code | Markdown仕様書からコードを自動生成 | [Guide](./instructions/spec-to-code.md) |
| | action-fixer | Workflowのエラーを検知し、AIが自動修正 | [Guide](./instructions/action-fixer.md) |
| | auto-refactor | 自然言語の指示に基づき、既存コードをリファクタリング | [Guide](./instructions/auto-refactor.md) |
| **Documentation** | auto-document | コードの変更を検知し、README等のドキュメントを自動更新 | [Guide](./instructions/auto-document.md) |
| | release-notes-ai | コミット履歴から人間が読みやすいリリースノートを生成 | [Guide](./instructions/release-notes-ai.md) |
| **Automation** | auto-merge | PRが条件を満たす場合に自動マージ | [Guide](./instructions/auto-merge.md) |
| | auto-rebase | PRの競合を自動的にリベースで解決 | [Guide](./instructions/auto-rebase.md) |
| **Bulk Operations** | bulk-merge-prs | 複数のPRを一括マージ | [Guide](./instructions/bulk-merge-prs.md) |
| | bulk-rebase-prs | 複数のPRを一括リベース | [Guide](./instructions/bulk-rebase-prs.md) |
| **Workflow** | pr-review-enqueuer | PRレビューをキューに登録して処理 | [Guide](./instructions/pr-review-enqueuer.md) |
| | review-auto-merge | レビュー完了後に自動マージ | [Guide](./instructions/review-auto-merge.md) |
| | publish-pr | PRを作成・公開するためのヘルパー | [Guide](./instructions/publish-pr.md) |

### 2. Add Category Sections
Organize actions by purpose (Core Development, Documentation, Automation, Bulk Operations, Workflow)

### 3. Update "🚀 提供している AI Actions" Section
Change from "主要な AI Actions (6件)" to "提供している AI Actions (13件)"

## Benefits
1. **Improved Discoverability**: Users can see all available actions
2. **Better Categorization**: Actions grouped by purpose
3. **Adoption**: Users more likely to try additional actions
4. **Transparency**: Accurate representation of repository contents

## Alternatives Considered
1. **Keep README focused on "main" 6 actions**
   - Rejected: Hub repository should document everything
   - Reason: Users need to discover all available tools

2. **Create separate ACTIONS.md file**
   - Rejected: Adds friction - users expect README to be comprehensive
   - Reason: README.md is the first file users read

3. **Mark 7 actions as "experimental" or "internal"**
   - Rejected: Cannot verify status without documentation
   - Reason: If they're in actions/, they should be documented

## Risks
- **Low**: Documentation update only, no code changes
- **Mitigation**: Review each action's instruction.md for accurate descriptions

## Testing
- Verify all 13 instruction.md files exist and are readable
- Check all links work
- Ensure consistent formatting

## Rollback
Revert README.md commit if descriptions are inaccurate

## Estimated Effort
15 minutes (read instructions/, update table, verify links)

## Success Criteria
- All 13 actions documented in README
- Links to all 13 instruction files work
- Categorization makes sense to users

## Related Issues
Closes ISS-001 (Critical documentation gap)
