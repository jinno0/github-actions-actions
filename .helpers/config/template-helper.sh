#!/bin/bash
# Shared template helper script for consistent placeholder replacement across all actions
# This follows the "1情報 = 1変数 = 1変数名" principle by standardizing template handling

# Function to load and process template files
# Usage: process_template <template_file> <output_file> <placeholder_1> <value_1> [<placeholder_2> <value_2> ...]
process_template() {
  local template_file="$1"
  local output_file="$2"
  shift 2

  if [ ! -f "$template_file" ]; then
    echo "Error: Template file not found: $template_file" >&2
    return 1
  fi

  # Start with template content
  local content
  content=$(cat "$template_file")

  # Replace each placeholder with its value
  while [ $# -ge 2 ]; do
    local placeholder="$1"
    local value="$2"
    shift 2

    # Escape special characters in value for sed
    local escaped_value
    escaped_value=$(printf '%s\n' "$value" | sed 's/[&/\]/\\&/g')

    # Replace placeholder
    content=$(printf '%s' "$content" | sed -e "s/{${placeholder}}/${escaped_value}/g")
  done

  # Write output
  printf '%s\n' "$content" > "$output_file"
}

# Function to find template file with fallback to built-in
# Usage: find_template_file <custom_template_path> <action_path> <default_template_name>
find_template_file() {
  local custom_template="$1"
  local action_path="$2"
  local default_template="$3"

  # Use custom template if provided and exists
  if [ -n "$custom_template" ] && [ -f "$custom_template" ]; then
    printf '%s\n' "$custom_template"
    return 0
  fi

  # Fall back to built-in template
  local built_in_template="${action_path}/templates/${default_template}"
  if [ -f "$built_in_template" ]; then
    printf '%s\n' "$built_in_template"
    return 0
  fi

  echo "Error: Neither custom template ($custom_template) nor built-in template ($built_in_template) found" >&2
  return 1
}
