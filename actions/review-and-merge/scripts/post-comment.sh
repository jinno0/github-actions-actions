#!/bin/bash
# Post Review Comment Script
# This script posts review comments to PRs

set -e

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

if [ -n "$COMMENT_TEMPLATE" ] && [ -f "$COMMENT_TEMPLATE" ]; then
  TEMPLATE_FILE="$COMMENT_TEMPLATE"
else
  TEMPLATE_FILE="${TEMPLATE_DIR}/comment_template.txt"
fi

if [ "$VERDICT" = "LGTM" ] && [ "$CONFIDENCE" -ge "$THRESHOLD" ]; then
  STATUS_MESSAGE="✅ This PR meets the LGTM threshold."
else
  STATUS_MESSAGE="❌ This PR requires changes."
fi

COMMENT=$(sed -e "s#{VERDICT}#$VERDICT#g" \
              -e "s#{CONFIDENCE}#$CONFIDENCE#g" \
              -e "s#{THRESHOLD}#$THRESHOLD#g" \
              -e "s#{SUMMARY}#$SUMMARY#g" \
              -e "s#{STATUS_MESSAGE}#$STATUS_MESSAGE#g" \
              -e "s#{MODEL}#${MODEL}#g" \
              "$TEMPLATE_FILE")

gh pr comment $PR_NUMBER --body "$COMMENT"
