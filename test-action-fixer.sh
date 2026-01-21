#!/bin/bash
# Comprehensive test script for action-fixer
# Tests structure, templates, examples, and instructions

set -e

ACTION_NAME="action-fixer"
ACTION_PATH="actions/$ACTION_NAME"
EXAMPLE_PATH="examples/${ACTION_NAME}-example.yml"
INSTRUCTION_PATH="instructions/${ACTION_NAME}.md"

echo "=== Testing $ACTION_NAME ==="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASS=0
FAIL=0
WARN=0

# Test function
test_check() {
  local test_name="$1"
  local command="$2"
  local should_succeed="${3:-true}"

  echo -n "Testing: $test_name ... "

  if eval "$command" > /dev/null 2>&1; then
    if [ "$should_succeed" = "true" ]; then
      echo -e "${GREEN}PASS${NC}"
      PASS=$((PASS + 1))
    else
      echo -e "${RED}FAIL${NC} (should have failed but passed)"
      FAIL=$((FAIL + 1))
    fi
  else
    if [ "$should_succeed" = "false" ]; then
      echo -e "${GREEN}PASS${NC} (failed as expected)"
      PASS=$((PASS + 1))
    else
      echo -e "${RED}FAIL${NC}"
      FAIL=$((FAIL + 1))
    fi
  fi
}

# 1. Structure Tests
echo "### 1. Structure Tests"

test_check "action.yml exists" "[ -f '$ACTION_PATH/action.yml' ]"
test_check "templates directory exists" "[ -d '$ACTION_PATH/templates' ]"
test_check "template file exists" "[ -f '$ACTION_PATH/templates/fix_prompt.txt' ]"
test_check "example file exists" "[ -f '$EXAMPLE_PATH' ]"
test_check "instruction file exists" "[ -f '$INSTRUCTION_PATH' ]"

echo ""

# 2. YAML Syntax Tests
echo "### 2. YAML Syntax Tests"

test_check "action.yml valid YAML" "python3 -c 'import yaml; yaml.safe_load(open(\"$ACTION_PATH/action.yml\"))'"
test_check "example file valid YAML" "python3 -c 'import yaml; yaml.safe_load(open(\"$EXAMPLE_PATH\"))'"

echo ""

# 3. Template Validation
echo "### 3. Template Validation"

# Check for placeholder syntax
if grep -q '{[A-Z_]*}' "$ACTION_PATH/templates/fix_prompt.txt"; then
  echo -e "Testing: Template uses placeholder syntax ... ${GREEN}PASS${NC}"
  PASS=$((PASS + 1))
else
  echo -e "Testing: Template uses placeholder syntax ... ${YELLOW}WARN${NC} (no placeholders found)"
  WARN=$((WARN + 1))
fi

# Check for heredoc (should NOT be present)
if grep -q '<< EOF' "$ACTION_PATH/action.yml"; then
  echo -e "Testing: No heredoc in action.yml ... ${RED}FAIL${NC} (heredoc found)"
  FAIL=$((FAIL + 1))
else
  echo -e "Testing: No heredoc in action.yml ... ${GREEN}PASS${NC}"
  PASS=$((PASS + 1))
fi

echo ""

# 4. Content Validation
echo "### 4. Content Validation"

# Check action.yml has required fields
test_check "action.yml has 'name' field" "grep -q '^name:' '$ACTION_PATH/action.yml'"
test_check "action.yml has 'description' field" "grep -q '^description:' '$ACTION_PATH/action.yml'"
test_check "action.yml has 'inputs' section" "grep -q '^inputs:' '$ACTION_PATH/action.yml'"
test_check "action.yml has 'runs' section" "grep -q '^runs:' '$ACTION_PATH/action.yml'"

# Check example has required fields
test_check "example has 'on' trigger" "grep -q '^on:' '$EXAMPLE_PATH'"
test_check "example has 'jobs' section" "grep -q '^jobs:' '$EXAMPLE_PATH'"
test_check "example uses self-hosted runner" "grep -q 'runs-on: self-hosted' '$EXAMPLE_PATH'"

# Check instruction has required sections
test_check "instruction has Prerequisites" "grep -q 'Prerequisites' '$INSTRUCTION_PATH'"
test_check "instruction has Setup Instructions" "grep -q 'Setup' '$INSTRUCTION_PATH'"
test_check "instruction has Usage section" "grep -q 'Usage' '$INSTRUCTION_PATH'"

echo ""

# 5. Input Validation
echo "### 5. Input Validation"

# Check action.yml defines github-token
test_check "action.yml has github-token input" "grep -A2 'inputs:' '$ACTION_PATH/action.yml' | grep -q 'github-token:'"

# Check inputs have descriptions
INPUT_COUNT=$(grep -E '^\s+[a-z-]+:' "$ACTION_PATH/action.yml" | grep -A1 'inputs:' | tail -n +2 | wc -l)
if [ "$INPUT_COUNT" -gt 0 ]; then
  echo -e "Testing: Inputs have descriptions ... ${GREEN}PASS${NC} ($INPUT_COUNT inputs found)"
  PASS=$((PASS + 1))
else
  echo -e "Testing: Inputs have descriptions ... ${YELLOW}WARN${NC}"
  WARN=$((WARN + 1))
fi

echo ""

# 6. Best Practices Check
echo "### 6. Best Practices Check"

# Check for proper shell declaration
test_check "action.yml uses bash shell" "grep -q 'shell: bash' '$ACTION_PATH/action.yml'"

# Check for composite action type
test_check "action.yml is composite type" "grep -q \"using: 'composite'\" '$ACTION_PATH/action.yml'"

echo ""

# 7. Example Workflow Validation
echo "### 7. Example Workflow Validation"

# Extract job name from example
JOB_NAME=$(awk '/^jobs:/,/^[a-z]/ {if (/^[a-z-]+:/) {gsub(/[:\t]/, "", $1); print $1; exit}}' "$EXAMPLE_PATH")
if [ -n "$JOB_NAME" ]; then
  echo -e "Testing: Example has valid job name ... ${GREEN}PASS${NC} (job: $JOB_NAME)"
  PASS=$((PASS + 1))
else
  echo -e "Testing: Example has valid job name ... ${RED}FAIL${NC}"
  FAIL=$((FAIL + 1))
fi

# Check example references the action correctly
if grep -q "uses.*$ACTION_NAME" "$EXAMPLE_PATH"; then
  echo -e "Testing: Example uses the action ... ${GREEN}PASS${NC}"
  PASS=$((PASS + 1))
else
  echo -e "Testing: Example uses the action ... ${RED}FAIL${NC}"
  FAIL=$((FAIL + 1))
fi

echo ""

# Summary
echo "=== Test Summary ==="
echo -e "${GREEN}PASSED: $PASS${NC}"
echo -e "${YELLOW}WARNINGS: $WARN${NC}"
echo -e "${RED}FAILED: $FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
  echo -e "${GREEN}✅ All critical tests passed!${NC}"
  exit 0
else
  echo -e "${RED}❌ Some tests failed. Please review the output above.${NC}"
  exit 1
fi
