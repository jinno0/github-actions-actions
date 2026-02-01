# PR-003: Update README.md to Reflect Implementation Status

## Priority
**MEDIUM** - Documentation accuracy

## Problem Statement
README.mdでは13 Actionsを「提供している」と明言しているが、実際にテスト付きで実装完了しているのは2つのみ。ドキュメントと実装の不一致がある。

### Evidence
- **README.md:8**: "現在、以下の AI Actions を提供しています（全13件）。"
- **Reality**: 2 actions have tests, 11 actions are partially implemented
- **Gap**: Documentation claims completion, implementation is incomplete

## Impact Assessment

### User Trust Risk
- Users may try to use incomplete actions
- Failed implementations damage repository reputation
- Violates PURPOSE.md success criteria

### Development Team Risk
- Misleading documentation creates confusion
- New contributors may not know priorities
- Unclear what needs to be implemented

## Proposed Solution

### Option A: Add Implementation Status (Recommended)

Add a status column to the action table:

```markdown
## 🚀 提供している AI Actions

| Status | Action | 概要 | セットアップガイド |
|--------|--------|------|-------------------|
| ✅ 完了 | `review-and-merge` | AIがコードをレビューし自動マージ | [Guide](./instructions/review-and-merge.md) |
| ✅ 完了 | `spec-to-code` | Markdown仕様書からコードを自動生成 | [Guide](./instructions/spec-to-code.md) |
| 🚧 WIP | `action-fixer` | Workflowのエラーを検知し、AIが自動修正 | [Guide](./instructions/action-fixer.md) |
| 🚧 WIP | `auto-refactor` | 自然言語の指示に基づき、既存コードをリファクタリング | [Guide](./instructions/auto-refactor.md) |
| ⏸️ 計画 | `auto-document` | コードの変更を検知し、README等のドキュメントを自動更新 | [Guide](./instructions/auto-document.md) |
| ...
```

**Legend**:
- ✅ 完了: Tests implemented and passing
- 🚧 WIP: Partially implemented (action.yml exists, missing tests/scripts)
- ⏸️ 計画: Planned (action.yml skeleton only)

### Option B: Separate Sections

Split into "Production Ready" and "In Development":

```markdown
## 🚀 提供している AI Actions

### Production Ready (Ready for Organization-wide Adoption)

| Action | 概要 | セットアップガイド |
|--------|------|-------------------|
| `review-and-merge` | AIがコードをレビューし自動マージ | [Guide](./instructions/review-and-merge.md) |
| `spec-to-code` | Markdown仕様書からコードを自動生成 | [Guide](./instructions/spec-to-code.md) |

### In Development (Use with Caution)

| Action | ステータス | 概要 | セットアップガイド |
|--------|----------|------|-------------------|
| `action-fixer` | 🚧 WIP | Workflowのエラーを検知し、AIが自動修正 | [Guide](./instructions/action-fixer.md) |
...
```

### Option C: Add Progress Bar

Add a visual progress indicator:

```markdown
## 📊 Development Progress

**Overall Completion**: 2/13 actions (15.4%) | **Target**: 80% by end of Q2

```text
[████░░░░░░░░░░░░░░░░] 15.4%
```

### Production Ready ✅
- review-and-merge
- spec-to-code

### In Development 🚧
- action-fixer (partial)
- auto-refactor (partial)
- [...9 more actions]
```

## Recommendation

**Adopt Option A** with the following implementation status mapping:

| Action | Status | Justification |
|--------|--------|---------------|
| review-and-merge | ✅ 完了 | Tests exist and passing |
| spec-to-code | ✅ 完了 | Tests exist and passing |
| action-fixer | 🚧 WIP | Has templates, missing tests |
| auto-refactor | ⏸️ 計画 | action.yml only |
| auto-document | ⏸️ 計画 | action.yml only |
| release-notes-ai | ⏸️ 計画 | action.yml only |
| auto-merge | 🚧 WIP | Has action.yml, basic structure |
| auto-rebase | ⏸️ 計画 | action.yml only |
| review-auto-merge | ⏸️ 計画 | action.yml only |
| publish-pr | ⏸️ 計画 | action.yml only |
| bulk-merge-prs | ⏸️ 計画 | action.yml only |
| bulk-rebase-prs | ⏸️ 計画 | action.yml only |
| pr-review-enqueuer | ⏸️ 計画 | action.yml only |

## Implementation Steps

### Step 1: Update README.md table
- Add Status column
- Mark each action with appropriate status
- Add legend explaining status meanings

### Step 2: Add progress section
- Add overall progress bar
- Link to verification results
- Show test coverage percentage

### Step 3: Update PURPOSE.md
- Reflect current Phase 2 status as "PARTIALLY_COMPLETED"
- Update Phase 3 status to "BLOCKED until coverage reaches 80%"

## Expected Outcome

### Success Criteria
- ✅ README.md accurately reflects implementation status
- ✅ Users can identify which actions are production-ready
- ✅ Development team has clear priorities

### Behavioral Changes
- Users will only adopt "✅ 完了" actions
- Contributors will focus on completing "🚧 WIP" actions first
- Transparency increases trust in project

## Risk Assessment

### Low Risk
- Pure documentation change
- No code changes required
- Reduces user confusion

### Potential Concerns
- "🚧 WIP" status may discourage early adopters
- **Mitigation**: Add note "Feedback welcome on WIP actions"

## Estimated Effort
- **Implementation**: 30 minutes
- **Review**: 15 minutes
- **Total**: 45 minutes

## Related Issues
- Addresses: GAP-003 (implementation completeness)
- Addresses: RISK-002 (reputation risk from documentation mismatch)
- Supports: PURPOSE.md Phase 3 transparency

## Dependencies
- **Requires**: Verification results from `.audit/output/verification_result.json`
- **Enables**: Accurate communication with stakeholders

## Rollback Plan

If status tracking becomes too burdensome:
1. Revert to simple list
2. Remove status column
3. Maintain separate STATUS.md file instead

## References
- Source: `.audit/analysis/gap.yml -> GAP-003`
- Source: `.audit/analysis/as_is.yml -> actions inventory`
- Verification: `.audit/output/verification_result.json`

## Future Enhancement

After PR-002 and PR-003 are complete, add CI badge to README:
```markdown
![Test Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)
![Actions Status](https://img.shields.io/badge/actions-5%2F13%20ready-orange)
```
