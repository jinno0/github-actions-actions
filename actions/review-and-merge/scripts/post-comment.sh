#!/bin/bash
# Post Review Comment Script
# This script posts review comments to PRs

set -euo pipefail

# Inputs
PR_NUMBER="${1}"
VERDICT="${2}"
CONFIDENCE="${3}"
SUMMARY="${4}"
THRESHOLD="${5}"
COMMENT_TEMPLATE="${6}"
MODEL="${7}"

ACTION_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="${ACTION_PATH}/templates"

if [ -n "$COMMENT_TEMPLATE" ]; then
  # Validate path to prevent directory traversal
  if [[ "$COMMENT_TEMPLATE" == *".."*"."* ]] || [[ "$COMMENT_TEMPLATE" == *"/"*".."* ]]; then
    echo "::error::Path traversal detected in comment template path"
    exit 1
  fi
  # Resolve to absolute path and ensure it's within allowed directories
  RESOLVED_PATH=$(cd "$GITHUB_WORKSPACE" 2>/dev/null && cd "$(dirname "$COMMENT_TEMPLATE")" 2>/dev/null && pwd)/$(basename "$COMMENT_TEMPLATE") 2>/dev/null || echo ""
  if [ -z "$RESOLVED_PATH" ] || [[ ! "$RESOLVED_PATH" == "$GITHUB_WORKSPACE"* ]] && [[ ! "$RESOLVED_PATH" == "${ACTION_PATH}"* ]]; then
    echo "::error::Comment template path must be within workspace or action directory"
    exit 1
  fi
  if [ -f "$RESOLVED_PATH" ]; then
    TEMPLATE_FILE="$RESOLVED_PATH"
  else
    echo "::error::Comment template file not found: $COMMENT_TEMPLATE"
    exit 1
  fi
else
  TEMPLATE_FILE="${TEMPLATE_DIR}/comment_template.txt"
fi

if [ "$VERDICT" = "LGTM" ] && [ "$CONFIDENCE" -ge "$THRESHOLD" ]; then
  STATUS_MESSAGE="✅ This PR meets the LGTM threshold."
else
  STATUS_MESSAGE="❌ This PR requires changes."
fi

COMMENT=$(export VERDICT CONFIDENCE THRESHOLD SUMMARY STATUS_MESSAGE MODEL && \
           envsubst '$VERDICT $CONFIDENCE $THRESHOLD $SUMMARY $STATUS_MESSAGE $MODEL' < "$TEMPLATE_FILE")

gh pr comment $PR_NUMBER --body "$COMMENT"
