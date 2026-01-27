#!/bin/bash
# Review and Fix Script for Claude Code CLI
# This script handles PR review and auto-fixing using Claude Code CLI

set -e

# Inputs (passed as environment variables)
PR_NUMBER="${1}"
MODEL="${2}"
THRESHOLD="${3}"
REVIEW_PROMPT_TEMPLATE="${4}"
CUSTOM_RULES="${5}"
AUTO_FIX="${6}"
COMMENT_TEMPLATE="${7}"

# Derived paths
ACTION_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="${ACTION_PATH}/templates"

echo "Running Claude Code CLI..."
echo "Model: $MODEL"
echo "Auto Fix: $AUTO_FIX"

if [ "$AUTO_FIX" = "true" ]; then
  # --- AUTO FIX MODE ---
  echo "Entering Auto-Fix mode..."
  TEMPLATE_FILE="${TEMPLATE_DIR}/fix_prompt.txt"
  cat "$TEMPLATE_FILE" > /tmp/fix_prompt.txt

  if [ -n "$CUSTOM_RULES" ]; then
    echo -e "\nAdditional Rules:\n$CUSTOM_RULES" >> /tmp/fix_prompt.txt
  fi

  echo '' >> /tmp/fix_prompt.txt
  cat /tmp/pr_diff.patch >> /tmp/fix_prompt.txt

  if claude --dangerously-skip-permissions --model "$MODEL" < /tmp/fix_prompt.txt > /tmp/claude_output.txt 2>&1; then
     echo "Claude fix execution completed"
  else
     echo "Claude execution failed"
     exit 1
  fi

  if git diff --quiet; then
    echo "No changes made by Claude."
    SUMMARY="Analyzed code, no fixes needed."
    MADE_CHANGES="false"
  else
    echo "Changes detected. Committing..."
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git config user.name "github-actions[bot]"
    git add .
    git commit -m "fix: auto-correction by Claude Code"
    git push
    SUMMARY="Applied auto-fixes based on code analysis."
    MADE_CHANGES="true"
  fi

  VERDICT="LGTM"
  CONFIDENCE="10"

else
  # --- REVIEW MODE ---
  echo "Entering Review mode..."
  if [ -n "$REVIEW_PROMPT_TEMPLATE" ] && [ -f "$REVIEW_PROMPT_TEMPLATE" ]; then
    REVIEW_PROMPT_FILE="$REVIEW_PROMPT_TEMPLATE"
  else
    REVIEW_PROMPT_FILE="${TEMPLATE_DIR}/review_prompt.txt"
  fi

  cat "$REVIEW_PROMPT_FILE" > /tmp/review_prompt.txt

  if [ -n "$CUSTOM_RULES" ]; then
    echo -e "\nAdditional Rules for this Review:\n$CUSTOM_RULES" >> /tmp/review_prompt.txt
  fi

  echo '' >> /tmp/review_prompt.txt
  cat /tmp/pr_diff.patch >> /tmp/review_prompt.txt

  if claude --dangerously-skip-permissions --model "$MODEL" < /tmp/review_prompt.txt > /tmp/claude_response.json 2>&1; then
    echo "Claude review completed"
  else
    echo '{"verdict":"REQUEST_CHANGES","confidence":1,"summary":"Claude CLI error"}' > /tmp/claude_response.json
  fi

  if grep -q '"verdict"[[:space:]]*:[[:space:]]*"LGTM"' /tmp/claude_response.json; then
    VERDICT="LGTM"
  else
    VERDICT="REQUEST_CHANGES"
  fi
  CONFIDENCE=$(grep -oP '"confidence"[[:space:]]*:[[:space:]]*\K\d+' /tmp/claude_response.json || echo "1")
  SUMMARY=$(grep -oP '"summary"[[:space:]]*:[[:space:]]*"\K[^"].*' /tmp/claude_response.json || echo "No summary")
  MADE_CHANGES="false"
fi

# Set output variables for GitHub Actions
echo "verdict=$VERDICT" >> $GITHUB_OUTPUT
echo "confidence=$CONFIDENCE" >> $GITHUB_OUTPUT
echo "summary=$SUMMARY" >> $GITHUB_OUTPUT
echo "made_changes=$MADE_CHANGES" >> $GITHUB_OUTPUT
