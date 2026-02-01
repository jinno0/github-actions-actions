#!/bin/bash
# Shared script for validating and resolving template paths
# Usage: source this script and call validate_template_path
#
# Arguments:
#   $1 - Template path input (can be empty for built-in)
#   $2 - Built-in template file path
#   $3 - Variable name to store the result
#
# Returns:
#   0 on success, sets the result variable to the validated template file path
#   1 on error (exits with error message)

validate_template_path() {
    local TEMPLATE_INPUT="$1"
    local BUILTIN_TEMPLATE="$2"
    local RESULT_VAR="$3"

    # If no custom template provided, use built-in
    if [ -z "$TEMPLATE_INPUT" ]; then
        eval "$RESULT_VAR=\"$BUILTIN_TEMPLATE\""
        return 0
    fi

    # Validate path to prevent directory traversal
    if [[ "$TEMPLATE_INPUT" == *".."*"."* ]] || [[ "$TEMPLATE_INPUT" == *"/"*".."* ]]; then
        echo "::error::Path traversal detected in template path"
        return 1
    fi

    # Resolve to absolute path and ensure it's within allowed directories
    local RESOLVED_PATH
    RESOLVED_PATH=$(cd "$GITHUB_WORKSPACE" 2>/dev/null && cd "$(dirname "$TEMPLATE_INPUT")" 2>/dev/null && pwd)/$(basename "$TEMPLATE_INPUT")" 2>/dev/null || echo ""

    if [ -z "$RESOLVED_PATH" ] || [[ ! "$RESOLVED_PATH" == "$GITHUB_WORKSPACE"* ]]; then
        echo "::error::Template path must be within workspace directory"
        return 1
    fi

    if [ -f "$RESOLVED_PATH" ]; then
        eval "$RESULT_VAR=\"$RESOLVED_PATH\""
        return 0
    else
        echo "::error::Template file not found: $TEMPLATE_INPUT"
        return 1
    fi
}

check_claude_cli() {
    if ! command -v claude &> /dev/null; then
        echo "::error::Claude CLI not found. Please install Claude CLI first."
        echo "  Visit https://claude.ai/ for installation instructions."
        return 1
    fi
    return 0
}
