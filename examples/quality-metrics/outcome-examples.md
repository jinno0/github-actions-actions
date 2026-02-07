# Acceptance Outcome Examples

Real examples from AI reviews to illustrate categorization.

**Purpose:** This document provides concrete examples to help developers consistently categorize AI review outcomes.

## Accepted Examples

### Example 1: Security Improvement

**AI Review:**
```markdown
### Security: Add input validation

The `user_input` parameter should be validated to prevent command injection.

Suggestion:
```python
import re
if not re.match(r'^[a-zA-Z0-9_-]+$', user_input):
    raise ValueError("Invalid input format")
```
```

**Developer Response:**
> "Applied suggestion. Added the validation check as recommended."

**Outcome:** ✅ Accepted

**Rationale:** The review was applied exactly as suggested without modifications.

---

### Example 2: Code Clarity

**AI Review:**
```markdown
### Clarity: Extract magic number

The value `86400` appears multiple times. Consider extracting to a constant.

Suggestion:
```python
SECONDS_PER_DAY = 86400
```
```

**Developer Response:**
> "Good catch. Added the constant at the top of the file."

**Outcome:** ✅ Accepted

---

## Modified Examples

### Example 1: Style Correction (Team Convention)

**AI Review:**
```markdown
### Naming: Improve variable clarity

Rename variable `temp` to `temporary_file_path` for better readability.
```

**Developer Response:**
> "Applied with a small change: used `tmp_path` instead to match our team's naming convention."

**Outcome:** 📝 Modified

**Rationale:** The core suggestion was accepted, but the specific name was adjusted for team consistency.

---

### Example 2: Partial Implementation

**AI Review:**
```markdown
### Error Handling: Add exception handling

Wrap the file operations in try-except to handle `FileNotFoundError`.

Suggestion:
```python
try:
    with open(file_path) as f:
        data = f.read()
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    return None
```

**Developer Response:**
> "Applied, but also added `PermissionError` handling since we've seen that in production."

**Outcome:** 📝 Modified

**Rationale:** The suggestion was implemented with an additional, related improvement.

---

## Rejected Examples

### Example 1: Incorrect Context

**AI Review:**
```markdown
### Error Handling: Add file check

Add `os.path.exists()` check before opening the file to prevent errors.

Suggestion:
```python
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File does not exist: {file_path}")
```

**Developer Response:**
> "Not applicable - file existence is guaranteed by the caller contract (see function documentation at line 42). Adding this check would be redundant."

**Outcome:** ❌ Rejected

**Rationale:** The AI misunderstood the context; the check is unnecessary.

---

### Example 2: Already Implemented

**AI Review:**
```markdown
### Performance: Cache result

The `calculate_metric()` function is called multiple times. Consider caching the result.

Suggestion:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_metric(key):
    # ...
```

**Developer Response:**
> "This is already implemented at line 15 using `@lru_cache`. Please verify existing code before suggesting changes."

**Outcome:** ❌ Rejected

---

### Example 3: Conflicts with Requirements

**AI Review:**
```markdown
### Security: Remove debug logging

The `logger.debug()` calls expose sensitive information. Remove them.

Suggestion:
```python
# Remove these lines:
- logger.debug(f"Processing user {user_id}")
- logger.debug(f"Token: {auth_token}")
```

**Developer Response:**
> "Cannot remove - these debug logs are required for troubleshooting production issues per https://docs.example.com/logging-requirements. Will add masking for sensitive fields instead."

**Outcome:** ❌ Rejected

**Rationale:** The suggestion conflicts with documented requirements.

---

## Needs Work Examples

### Example 1: Useful Direction, Wrong Implementation

**AI Review:**
```markdown
### Performance: Use async operations

The synchronous file operations are blocking. Consider using async/await.

Suggestion:
```python
async def process_files(files):
    for file in files:
        await async_read_file(file)
```

**Developer Response:**
> "Good direction, but this won't work with our current event loop architecture. Rewrote using `asyncio.gather()` for proper concurrency. See revised implementation in the PR."

**Outcome:** 🔧 Needs Work

**Rationale:** The concept was valuable, but the implementation needed significant rework (not just minor tweaks).

---

### Example 2: Incomplete Solution

**AI Review:**
```markdown
### Error Handling: Add timeout

Network operations should have timeouts to prevent hanging.

Suggestion:
```python
response = requests.get(url, timeout=30)
```

**Developer Response:**
> "Applied the timeout concept, but also added:
> 1. Retry logic with exponential backoff
> 2. Circuit breaker pattern
> 3. Proper exception handling for timeout errors
>
> The single-line suggestion wasn't production-ready."

**Outcome:** 🔧 Needs Work

**Rationale:** The suggestion identified a real issue but provided an incomplete solution requiring substantial expansion.

---

### Example 3: Alternative Approach Required

**AI Review:**
```markdown
### Architecture: Extract to function

The validation logic is duplicated. Extract to a helper function.

Suggestion:
```python
def validate_input(data):
    # validation logic here
```

**Developer Response:**
> "Valid observation, but instead of a simple function, I've created a `Validator` class to support:
> - Multiple validation rules
> - Custom error messages
> - Reusable validation strategies
>
> This better fits our architecture and provides more flexibility."

**Outcome:** 🔧 Needs Work

**Rationale:** The AI correctly identified duplication, but a different architectural approach was more appropriate.

---

## Decision Flowchart

Use this flowchart to categorize ambiguous cases:

```
┌─────────────────────────────┐
│ Did you apply the review?    │
└─────────────┬───────────────┘
              │
     ┌────────┴────────┐
     │                 │
    NO                YES
     │                 │
     ▼                 ▼
┌─────────┐    ┌──────────────┐
│ Rejected│    │ Any changes? │
└─────────┘    └──────┬───────┘
                      │
              ┌───────┴────────┐
              │                │
             NO              YES
              │                │
              ▼                ▼
         ┌─────────┐    ┌──────────────┐
         │Accepted │    │ Minor tweaks? │
         └─────────┘    └──────┬───────┘
                               │
                       ┌───────┴────────┐
                       │                │
                      YES              NO
                       │                │
                       ▼                ▼
                  ┌─────────┐    ┌──────────────┐
                  │Modified │    │Needs Work    │
                  └─────────┘    └──────────────┘
```

**"Minor tweaks" criteria:**
- Typos/grammar
- Variable/function renaming
- Style adjustments
- Small additions (<5 lines of code)

**"Needs Work" criteria:**
- Logic changes
- Alternative implementations
- Partial application only
- Major expansions

---

**Last Updated:** 2026-02-07
**Maintained by:** DevOps Team
**Questions?** Open an issue with the `quality-metrics` label
