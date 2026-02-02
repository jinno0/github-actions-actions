# Security Checklist for AI Actions

**Version:** 1.0
**Last Updated:** 2026-02-02
**Purpose:** Ensure all GitHub Actions follow security best practices

## Critical Security Patterns

### 1. CLI Availability Check ✅ REQUIRED

Every action MUST verify Claude CLI is available before attempting to use it.

```yaml
- name: Check Claude CLI availability
  shell: bash
  run: |
    # Check Claude CLI availability
    if ! command -v claude &> /dev/null; then
      echo "Error: Claude CLI not found"
      echo "Please install Claude Code CLI before using this action"
      exit 1
    fi

    # Verify Claude CLI is functional
    if ! claude --version &> /dev/null; then
      echo "Error: Claude CLI is not functional"
      exit 1
    fi

    echo "✓ Claude CLI verified"
```

**Status:** 4/13 actions compliant
**Required for:** All 13 actions

### 2. Path Validation ✅ REQUIRED

When accepting file paths as inputs, actions MUST validate:

```yaml
- name: Validate target path
  shell: bash
  run: |
    TARGET_PATH="${{ inputs.target-path }}"

    # Path validation - prevent path traversal
    if [[ "$TARGET_PATH" =~ \.\. ]]; then
      echo "Error: Path traversal detected in $TARGET_PATH"
      exit 1
    fi

    # Check for valid characters
    if [[ ! "$TARGET_PATH" =~ ^[a-zA-Z0-9_\-/]+$ ]]; then
      echo "Error: Invalid characters in path"
      exit 1
    fi

    # Resolve to absolute path and ensure it's within repository
    RESOLVED_PATH=$(cd "$GITHUB_WORKSPACE/$TARGET_PATH" && pwd)
    if [[ ! "$RESOLVED_PATH" =~ ^"$GITHUB_WORKSPACE" ]]; then
      echo "Error: Path outside repository not allowed"
      exit 1
    fi

    echo "✓ Path validated: $RESOLVED_PATH"
```

**Status:** Needs review for all actions accepting paths
**Required for:** Actions with path inputs (spec-to-code, auto-document, etc.)

### 3. Input Sanitization ✅ REQUIRED

```yaml
- name: Sanitize user input
  shell: bash
  run: |
    USER_INPUT="${{ inputs.user-instruction }}"

    # Remove null bytes and special characters
    SANITIZED=$(echo "$USER_INPUT" | tr -d '\0\r\n' | head -c 10000)

    # Log sanitized input length (not content for security)
    echo "Input length: ${#SANITIZED} characters"
```

### 4. GitHub Token Permissions 📋 DOCUMENTED

Each action MUST document required GitHub token scopes in its instruction file.

**Template:**
```markdown
## Prerequisites

### Required GitHub Token Scopes

This action requires the following GitHub token permissions:

- `repo:status` - To commit status checks
- `pull-requests:write` - To create PR comments
- `contents:write` - To push changes (if auto-fix enabled)
```

**Status:** 0/13 actions documented
**Required for:** All 13 actions

## Security Audit Results (2026-02-02)

### Actions with CLI Check ✅
1. action-fixer
2. spec-to-code
3. auto-refactor
4. release-notes-ai

### Actions Missing CLI Check ❌
1. _shared (helper, not critical)
2. auto-document
3. auto-merge
4. bulk-merge-prs
5. bulk-rebase-prs
6. lib (helper, not critical)
7. pr-review-enqueuer
8. publish-pr
9. review-and-merge
10. review-auto-merge

### Compliant Rate: 31% (4/13)

## Implementation Priority

### Phase 1: Critical (Week 1)
- [ ] Add CLI checks to remaining 9 production actions
- [ ] Add path validation to spec-to-code action
- [ ] Document token permissions for all actions

### Phase 2: High (Week 2)
- [ ] Add input sanitization to all actions accepting user input
- [ ] Security audit of all action.yml files for injection patterns
- [ ] Create security test suite

### Phase 3: Ongoing
- [ ] Quarterly security reviews
- [ ] Dependency scanning
- [ ] Vulnerability tracking

## Security Testing

### Manual Security Test

Run this script to verify security patterns:

```bash
#!/bin/bash
# test_security.sh

echo "Testing CLI availability checks..."

for action in actions/*/action.yml; do
  if grep -q "command -v claude" "$action"; then
    echo "✓ $(dirname $action): CLI check present"
  else
    echo "✗ $(dirname $action): CLI check MISSING"
  fi
done

echo ""
echo "Testing path validation..."

for action in actions/*/action.yml; do
  if grep -q "path validation\|path traversal" "$action"; then
    echo "✓ $(dirname $action): Path validation present"
  fi
done
```

## Vulnerability Reporting

If you discover a security vulnerability:

1. DO NOT open a public issue
2. Email security@[your-domain].com
3. Include details and reproduction steps
4. Wait for confirmation before disclosing

## References

- [GitHub Actions Security Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
