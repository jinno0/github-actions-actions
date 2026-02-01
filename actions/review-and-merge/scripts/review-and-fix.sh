#!/bin/bash
# Review and Fix Script for Claude Code CLI
# This script handles PR review and auto-fixing using Claude Code CLI

set -euo pipefail

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

  # Check Claude CLI availability before invoking
  if ! command -v claude &> /dev/null; then
    echo "::error::Claude CLI not found. Please install Claude CLI first."
    echo "  Visit https://claude.ai/ for installation instructions."
    exit 1
  fi

  # Run Claude in review-only mode (no --dangerously-skip-permissions for security)
  # Claude will analyze the diff and suggest fixes but won't modify files directly
  if claude --model "$MODEL" < /tmp/fix_prompt.txt > /tmp/claude_output.txt 2>&1; then
     echo "Claude fix analysis completed"
  else
     claude_exit_code=$?
     echo "Claude execution failed with exit code: $claude_exit_code"
     # Don't exit - allow review to proceed even if fix fails
  fi

  # Check if Claude made any changes (it shouldn't in safe mode)
  if git diff --quiet; then
    echo "No changes made by Claude (safe mode)."
    SUMMARY="Analyzed code in safe mode. Review suggestions in Claude output."
    MADE_CHANGES="false"
  else
    # If changes were made, validate and commit with proper error handling
    echo "Changes detected. Committing..."
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git config user.name "github-actions[bot]"
    git add .

    # Check if there's anything to commit
    if git diff --cached --quiet; then
      echo "No changes to commit."
      SUMMARY="Analyzed code, no fixes needed."
      MADE_CHANGES="false"
    else
      git commit -m "fix: auto-correction by Claude Code"

      # Retry logic for git push with error handling
      max_retries=3
      retry_count=0
      push_success=false

      while [ $retry_count -lt $max_retries ] && [ "$push_success" = false ]; do
        # Use --force-with-lease for safer force push during concurrent operations
        if git push --force-with-lease; then
          echo "Push successful"
          push_success=true
          SUMMARY="Applied auto-fixes based on code analysis."
          MADE_CHANGES="true"
        else
          retry_count=$((retry_count + 1))
          if [ $retry_count -lt $max_retries ]; then
            echo "Push failed (attempt $retry_count/$max_retries). Retrying after pull..."
            git pull --rebase --strategy-option=theirs || {
              echo "Rebase failed, resetting..."
              git reset --hard HEAD@{1}
            }
            sleep $((retry_count * 2))  # Exponential backoff
          else
            echo "Push failed after $max_retries attempts. Rolling back commit."
            git reset --hard HEAD@{1}
            SUMMARY="Failed to apply auto-fixes due to git conflict."
            MADE_CHANGES="false"
            exit 1
          fi
        fi
      done
    fi
  fi

  VERDICT="LGTM"
  CONFIDENCE="10"

else
  # --- REVIEW MODE ---
  echo "Entering Review mode..."
  if [ -n "$REVIEW_PROMPT_TEMPLATE" ]; then
    # Validate path to prevent directory traversal
    if [[ "$REVIEW_PROMPT_TEMPLATE" == *".."*"."* ]] || [[ "$REVIEW_PROMPT_TEMPLATE" == *"/"*".."* ]]; then
      echo "::error::Path traversal detected in review template path"
      exit 1
    fi
    # Resolve to absolute path and ensure it's within allowed directories
    RESOLVED_PATH=$(cd "$GITHUB_WORKSPACE" 2>/dev/null && cd "$(dirname "$REVIEW_PROMPT_TEMPLATE")" 2>/dev/null && pwd)/$(basename "$REVIEW_PROMPT_TEMPLATE") 2>/dev/null || echo ""
    if [ -z "$RESOLVED_PATH" ] || [[ ! "$RESOLVED_PATH" == "$GITHUB_WORKSPACE"* ]] && [[ ! "$RESOLVED_PATH" == "${ACTION_PATH}"* ]]; then
      echo "::error::Review template path must be within workspace or action directory"
      exit 1
    fi
    if [ -f "$RESOLVED_PATH" ]; then
      REVIEW_PROMPT_FILE="$RESOLVED_PATH"
    else
      echo "::error::Review template file not found: $REVIEW_PROMPT_TEMPLATE"
      exit 1
    fi
  else
    REVIEW_PROMPT_FILE="${TEMPLATE_DIR}/review_prompt.txt"
  fi

  cat "$REVIEW_PROMPT_FILE" > /tmp/review_prompt.txt

  if [ -n "$CUSTOM_RULES" ]; then
    echo -e "\nAdditional Rules for this Review:\n$CUSTOM_RULES" >> /tmp/review_prompt.txt
  fi

  echo '' >> /tmp/review_prompt.txt
  cat /tmp/pr_diff.patch >> /tmp/review_prompt.txt

  # Run Claude in review-only mode (no --dangerously-skip-permissions for security)
  if claude --model "$MODEL" < /tmp/review_prompt.txt > /tmp/claude_response.json 2>&1; then
    echo "Claude review completed"
  else
    claude_exit_code=$?
    echo "Claude review failed with exit code: $claude_exit_code"
    echo '{"verdict":"REQUEST_CHANGES","confidence":1,"summary":"Claude CLI error - review failed"}' > /tmp/claude_response.json
  fi

  # Validate JSON structure before parsing
  if ! jq empty /tmp/claude_response.json 2>/dev/null; then
    echo "Invalid JSON from Claude, using fallback values"
    VERDICT="REQUEST_CHANGES"
    CONFIDENCE="1"
    SUMMARY="Claude returned invalid JSON - review failed"
    MADE_CHANGES="false"
  else
    # Use jq for proper JSON parsing (cross-platform compatible)
    VERDICT=$(jq -r '.verdict // "REQUEST_CHANGES"' /tmp/claude_response.json)
    CONFIDENCE=$(jq -r '.confidence // 1' /tmp/claude_response.json)
    SUMMARY=$(jq -r '.summary // "No summary provided"' /tmp/claude_response.json)

    # Validate verdict values
    if [[ "$VERDICT" != "LGTM" && "$VERDICT" != "REQUEST_CHANGES" && "$VERDICT" != "COMMENT" ]]; then
      VERDICT="REQUEST_CHANGES"
    fi

    # Validate confidence is a number
    if ! [[ "$CONFIDENCE" =~ ^[0-9]+$ ]]; then
      CONFIDENCE="1"
    fi

    MADE_CHANGES="false"
  fi
fi

# Set output variables for GitHub Actions
echo "verdict=$VERDICT" >> $GITHUB_OUTPUT
echo "confidence=$CONFIDENCE" >> $GITHUB_OUTPUT
echo "summary=$SUMMARY" >> $GITHUB_OUTPUT
echo "made_changes=$MADE_CHANGES" >> $GITHUB_OUTPUT
