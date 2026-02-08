# PR-004: Claude CLI Integration Investigation & Documentation

**Status:** Proposed
**Priority:** P1 - HIGH
**Estimated Effort:** 2-3 hours investigation + 1 hour documentation
**Gap ID:** GAP-004

---

## Problem Statement

**Current State:**
- README.md:3-4 claims: "Claude Code CLIを活用し、コードの文脈を理解した高度な自動化を実現する"
- Actual implementation: 7/13 (54%) Actions have Claude CLI integration
- 6/13 Actions do NOT use Claude Code CLI

**Actions WITH Claude CLI (7/13):**
1. action-fixer
2. review-and-merge
3. spec-to-code
4. auto-document
5. release-notes-ai
6. auto-rebase
7. auto-refactor

**Actions WITHOUT Claude CLI (6/13):**
1. pr-review-enqueuer
2. bulk-rebase-prs
3. bulk-merge-prs
4. auto-merge
5. review-auto-merge
6. publish-pr

**Impact:**
- Medium: README.md's value proposition may not align with actual implementation
- Users may be confused when some Actions don't use Claude Code CLI
- Need to understand WHY these 6 Actions don't use Claude CLI

---

## Investigation Plan

### Phase 1: Understand the 6 Actions' Purpose

**Research Questions:**
1. What is the primary function of each of the 6 Actions?
2. Do they require AI/code understanding capabilities?
3. Are they utility/wrapper functions that don't need AI?
4. Is the lack of Claude CLI integration by design or an oversight?

**Investigation Method:**
```bash
# For each action without Claude CLI
for action in pr-review-enqueuer bulk-rebase-prs bulk-merge-prs auto-merge review-auto-merge publish-pr; do
  echo "=== Investigating $action ==="
  echo "README:"
  cat actions/$action/README.md 2>/dev/null || echo "No README"
  echo "---"
  echo "action.yml purpose:"
  grep -A 5 "description:" actions/$action/action.yml
  echo "---"
  echo "entrypoint analysis:"
  head -50 actions/$action/entrypoint.sh | grep -E "(claude|ai|llm)" || echo "No AI keywords found"
  echo "---"
done
```

**Expected Findings:**
- Hypothesis 1: These are utility actions (PR enqueueing, bulk operations) that don't require AI
- Hypothesis 2: These are lower-level infrastructure actions
- Hypothesis 3: These are actions that could benefit from Claude CLI but haven't been integrated yet

### Phase 2: Document Findings

**Create Documentation:** `docs/claude-cli-integration-status.md`

```markdown
# Claude CLI Integration Status

## Overview
This document explains which Actions use Claude Code CLI and why.

## Actions WITH Claude CLI (7/13)
These actions require code understanding and AI capabilities:
- [list each with purpose]

## Actions WITHOUT Claude CLI (6/13)
These actions do NOT use Claude Code CLI because:
- [explain reasons for each]

### pr-review-enqueuer
- **Purpose**: [investigation finding]
- **Why no Claude CLI**: [investigation finding]

### bulk-rebase-prs
- **Purpose**: [investigation finding]
- **Why no Claude CLI**: [investigation finding]

[... and so on for all 6 actions]

## Design Philosophy
[Explain the pattern: which actions need AI vs which don't]
```

### Phase 3: Update README.md (If Needed)

**Option A: If the 6 actions are utilities by design**
```markdown
# Add to README.md after line 4:

## Action Categories

### AI-Native Actions (7/13)
These Actions use Claude Code CLI for code understanding and intelligent automation:
- action-fixer, review-and-merge, spec-to-code, auto-document, release-notes-ai, auto-rebase, auto-refactor

### Utility Actions (6/13)
These Actions provide workflow orchestration and don't require AI:
- pr-review-enqueuer, bulk-rebase-prs, bulk-merge-prs, auto-merge, review-auto-merge, publish-pr
```

**Option B: If some of the 6 actions SHOULD use Claude CLI**
- Create follow-up issue to add Claude CLI integration
- Prioritize based on user value

---

## Proposed Solution

### Step 1: Investigation (2 hours)

**Task:** Create investigation script and analyze all 6 Actions

**Output:** Investigation findings document with:
- Purpose of each action
- Whether Claude CLI integration is needed
- Current implementation approach

### Step 2: Documentation (1 hour)

**Task:** Create `docs/claude-cli-integration-status.md`

**Content:**
- Clear explanation of which Actions use Claude CLI and why
- Design philosophy behind the categorization
- Examples of when to use each type

### Step 3: README Update (30 minutes)

**Task:** Update README.md based on findings

**Approach:**
- If by design: Add "Action Categories" section
- If oversight: Create follow-up issues for integration

---

## Success Criteria

- [ ] All 6 Actions investigated and documented
- [ ] Clear rationale documented for why each does/doesn't use Claude CLI
- [ ] `docs/claude-cli-integration-status.md` created
- [ ] README.md updated to reflect actual state
- [ ] No confusion about which Actions use AI

---

## Expected Outcomes

**Best Case (Design Intent):**
- The 6 Actions are utilities by design (orchestration, bulk operations)
- Documentation clarifies this distinction
- User understanding improves
- No code changes needed

**Medium Case (Partial Oversight):**
- Some of the 6 Actions could benefit from Claude CLI
- Create follow-up issues for integration
- Prioritize based on user value

**Worst Case (Major Inconsistency):**
- README.md's main value proposition is misleading
- Need broader discussion about project direction
- May require repositioning of the repository

---

## Related Issues

- Gap: GAP-004
- Core Function: CF-002 (partial)
- Question: UNK-003 in next_questions.md
