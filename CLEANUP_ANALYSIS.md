# Universal Janitor - Cleanup Analysis

**Date**: 2026-02-02
**Target Repository**: github-actions-actions
**Analysis Method**: Random 3-file sampling

## Files Analyzed

1. **`.audit/proposal/changes/PR-001.md`** - Audit proposal document (already implemented)
2. **`.claude/skills/spec-flow-auto/scripts/generate_spec_from_prd.py`** - Python script (393 lines)
3. **`actions/review-and-merge/README.md`** - Action documentation

## 10 Cleanup Improvement Ideas

### 1. [Implemented Proposal Archiving]
- **Target**: `.audit/proposal/changes/PR-001.md`
- **Reason**: PR-001 is already implemented (ADOPTION_GUIDE.md and pilot-workflow-template.yml exist)
- **Expected Result**: Clear proposal lifecycle management
- **Action**: Move implemented proposals to `.audit/proposal/implemented/` directory

### 2. [Unused Script Evaluation] ✅ VERIFIED AS USED
- **Target**: `.claude/skills/spec-flow-auto/scripts/generate_spec_from_prd.py`
- **Reason**: 393-line generic spec generation script. Needs usage verification
- **Expected Result**: ~~Remove unused code~~ No action needed - actively used
- **Action**: ✅ VERIFIED - Referenced by enhanced_sdd_pipeline.py, validate_prd_spec_sync.py, run_sdd_pipeline.py, and SKILL.md. Keep as is.

### 3. [Documentation Deduplication] ✅ VERIFIED AS INTENTIONAL
- **Target**: `actions/review-and-merge/README.md` vs `instructions/review-and-merge.md`
- **Reason**: Potential content overlap between action README and instructions
- **Expected Result**: ~~Single source of truth~~ No action needed - Different purposes
- **Action**: ✅ VERIFIED - README.md (122 lines) is comprehensive reference; instructions/ (48 lines) is quick setup guide. This is intentional separation.

### 4. [Python Cache Cleanup]
- **Target**: `tests/**/__pycache__/`, `**/*.pyc`
- **Reason**: __pycache__ directories exist despite .gitignore rules
- **Expected Result**: Reduced repository size, faster clones
- **Action**: Remove from Git history (already ignored)

### 5. [Node Modules Log Exclusion]
- **Target**: `./node_modules/nwsapi/dist/lint.log`
- **Reason**: node_modules/ should not contain tracked files
- **Expected Result**: Clean repository
- **Action**: Verify .gitignore excludes node_modules/

### 6. [Test Coverage File Cleanup]
- **Target**: `.coverage`, `coverage.json`, `htmlcov/`
- **Reason**: Already in .gitignore but may be in Git history
- **Expected Result**: Reduced repository size
- **Action**: Remove from Git history if present

### 7. [Audit Directory Restructuring]
- **Target**: `.audit/proposal/changes/*.md` (PR-001, PR-003, PR-004, PR-005, PR-006)
- **Reason**: Need better status tracking (implemented/in-progress/pending)
- **Expected Result**: Clear proposal status management
- **Action**: Organize proposals by implementation status

### 8. [Skill Template Duplication Check]
- **Target**: `.claude/skills/agent-creator/templates/workflows/*.md`
- **Reason**: 6 workflow templates may have redundant content
- **Expected Result**: Reduced maintenance overhead
- **Action**: Review and consolidate duplicate templates

### 9. [Example File Completeness] ✅ VERIFIED COMPLETE
- **Target**: `examples/*-example.yml` (14 files)
- **Reason**: Verify all actions have corresponding examples
- **Expected Result**: ~~Create missing examples~~ All actions have examples
- **Action**: ✅ VERIFIED - All 13 actions have corresponding example files. Coverage is complete.

### 10. [Temporary Report Cleanup]
- **Target**: `.bmad/reports/`, `.bmad/workflows/*-report.md`
- **Reason**: Temporary files that should not be in repository
- **Expected Result**: Clean repository history
- **Action**: Ensure .gitignore covers all temporary patterns

## Immediate Actions Taken

1. ✅ Analysis completed
2. ✅ Created cleanup analysis document
3. ✅ Moved PR-001.md to `.audit/proposal/implemented/` (Item #1)
4. ✅ Verified generate_spec_from_prd.py is actively used (Item #2)
5. ✅ Verified example file completeness (Item #9)
6. ⏳ Remaining items prioritized below

## Priority Recommendations

**High Priority** (Quick wins):
- ✅ #1: Archive implemented PR-001 **[DONE]**
- ✅ #2: Evaluate unused script **[VERIFIED - KEEP]**
- ✅ #9: Verify example file completeness **[VERIFIED - COMPLETE]**
- #4: Clean Python cache from Git history (requires Git history rewrite)

**Medium Priority** (Impactful but requires care):
- ~~#2: Evaluate unused script~~ ✅ VERIFIED - NO ACTION NEEDED
- ~~#3: Documentation consolidation~~ ✅ VERIFIED - INTENTIONAL SEPARATION
- #7: Audit directory restructuring (partially done - created implemented/ directory)

**Low Priority** (Maintenance):
- #5, #6, #10: Git history cleanup
- #8: Template review

## Notes

- All `.audit/` contents are already in .gitignore (line 171) - PR-001 move tracked locally but not committed
- All `.bmad/reports/` and temporary files are in .gitignore (lines 79-115)
- Python cache files are in .gitignore (lines 124-160)
- Main issue is Git history contains files that are now ignored
- The .audit directory structure change (implemented/) improves local organization but won't be committed

## Next Steps

1. Get approval for high-priority items
2. Create systematic cleanup plan
3. Execute with proper testing
4. Update documentation to prevent future accumulation
