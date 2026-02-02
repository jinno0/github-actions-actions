# Custom Rules Tutorial

A step-by-step guide to creating and testing custom review rules for the **review-and-merge** action.

## Learning Objectives

By the end of this tutorial, you will be able to:
1. Define custom review rules for your project
2. Integrate rules into your workflow
3. Test rules on sample PRs
4. Iterate and refine rules based on feedback

## Prerequisites

- Basic understanding of YAML syntax
- Access to a GitHub repository with review-and-merge action
- Permissions to create/modify workflows

## Tutorial Scenario

Imagine you're working on a **TypeScript web application** and want to enforce these standards:
1. No console.log in production code
2. All async functions must have error handling
3. Use TypeScript strict mode

Let's implement these rules step by step.

## Step 1: Create Custom Rules File

### 1.1 Create the file

In your repository root, create `.github/review-rules.yml`:

```bash
mkdir -p .github
touch .github/review-rules.yml
```

### 1.2 Define your rules

Edit `.github/review-rules.yml`:

```yaml
custom-rules: |
  Project: TypeScript Web Application

  Rule 1: No console.log in production code
  - Remove or replace console.log before committing
  - Use proper logging library (winston, pino) for production
  - Exception: console.log allowed in development only

  Rule 2: All async functions must have error handling
  - Use try/catch blocks for async operations
  - Handle promise rejections
  - Provide meaningful error messages

  Rule 3: Use TypeScript strict mode
  - Enable strict mode in tsconfig.json
  - No implicit any types
  - Explicit return types for functions
```

### 1.3 Commit the file

```bash
git add .github/review-rules.yml
git commit -m "Add custom review rules"
git push
```

## Step 2: Update Workflow

### 2.1 Find your workflow

Locate `.github/workflows/review-and-merge.yml`.

### 2.2 Add custom rules reference

Update the workflow to include your custom rules:

```yaml
name: Review and Merge

on:
  pull_request:
    types: [opened, synchronized, reopened]

jobs:
  review:
    runs-on: [self-hosted]
    steps:
      - uses: actions/checkout@v3

      - name: Read custom rules
        id: rules
        run: |
          echo "rules<<EOF" >> $GITHUB_OUTPUT
          cat .github/review-rules.yml >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Review and Merge
        uses: owner/repo/actions/review-and-merge@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          custom-rules: ${{ steps.rules.outputs.rules }}
```

### 2.3 Commit the workflow

```bash
git add .github/workflows/review-and-merge.yml
git commit -m "Integrate custom rules into review workflow"
git push
```

## Step 3: Test Your Rules

### 3.1 Create a test PR

Create a new branch and make intentional violations:

```bash
git checkout -b/test-rules
```

Create a file `test-file.ts`:

```typescript
// Intentional violations for testing

console.log('This violates Rule 1');  // ❌ Rule 1 violation

async function fetchData() {
  // ❌ Rule 2 violation: no error handling
  const response = await fetch('https://api.example.com/data');
  return response.json();
}

// ❌ Rule 3 violation: implicit any
function processData(data) {  // No type annotation
  return data.map((item: any) => item.value);  // any type
}
```

Commit and create a PR:

```bash
git add test-file.ts
git commit -m "Test: Intentional rule violations"
git push origin test-rules
```

### 3.2 Check the review results

1. Open the PR on GitHub
2. Wait for the review-and-merge workflow to complete
3. Check the PR review comments

**Expected result:** The AI should comment on each violation with specific feedback.

## Step 4: Fix Violations

### 4.1 Address the feedback

Update `test-file.ts` to fix violations:

```typescript
// ✅ Fixed: Proper logging
import logger from './logger';

logger.info('Proper logging in production');

// ✅ Fixed: Error handling added
async function fetchData(): Promise<Data> {
  try {
    const response = await fetch('https://api.example.com/data');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    logger.error('Failed to fetch data', error);
    throw error;  // Re-throw for caller to handle
  }
}

// ✅ Fixed: Type annotations added
interface DataItem {
  value: string;
}

function processData(data: DataItem[]): string[] {
  return data.map(item => item.value);
}
```

### 4.2 Commit the fixes

```bash
git add test-file.ts
git commit -m "Fix: Address review feedback"
git push
```

### 4.3 Verify the review

The AI should now review the changes and approve (LGTM).

## Step 5: Iterate and Refine

### 5.1 Gather feedback

After testing with your team:
1. Are rules too strict or too lenient?
2. Are violations clearly explained?
3. Are false positives occurring?

### 5.2 Refine rules

Update `.github/review-rules.yml` based on feedback:

```yaml
custom-rules: |
  Project: TypeScript Web Application

  Rule 1: No console.log in production code
  - Remove or replace console.log before committing
  - Use proper logging library (winston, pino)
  - Exception: console.error allowed for critical errors

  Rule 2: All async functions must have error handling
  - Use try/catch for async operations
  - Handle promise rejections
  - Log errors with context
  - Modified: Allow console.error in catch blocks

  Rule 4 NEW: Enforce explicit return types
  - All functions must have explicit return types
  - Use 'void' for functions with no return
  - Avoid 'any' type
```

### 5.3 Document exceptions

Create `.github/review-rules-exceptions.md` for documented exceptions:

```markdown
# Review Rules Exceptions

## Approved Exceptions

1. **console.error in error handlers**
   - Reason: Critical for debugging production issues
   - Approval: Tech lead, 2024-01-15

2. **any types in migration files**
   - Reason: Legacy data structure compatibility
   - Approval: Architect, 2024-01-20
```

## Step 6: Roll Out to Team

### 6.1 Communicate changes

Send a team announcement:

```
Subject: New Code Review Rules Starting [Date]

Hi team,

We're implementing automated code review with custom rules:
- No console.log in production
- Async functions must handle errors
- TypeScript strict mode required

See the documentation:
- Custom Rules Guide: instructions/review-and-merge-custom-rules.md
- Your project rules: .github/review-rules.yml

Questions? Ask in #dev-ops channel.
```

### 6.2 Monitor adoption

Track metrics:
- Number of PRs reviewed
- Common violations
- Time to address feedback
- Team satisfaction

### 6.3 Gather feedback

After 2 weeks, survey the team:
- Are rules helpful?
- Any adjustments needed?
- Success stories or pain points?

## Common Issues and Solutions

### Issue: Too many violations in existing code

**Solution:** Phase in rules gradually
1. Start with warnings only (no enforcement)
2. Focus on new code only
3. Provide migration window (e.g., 30 days)
4. Offer office hours for help

### Issue: Rules conflict with team preferences

**Solution:** Discuss and modify
1. Schedule team meeting to discuss
2. Consider project-specific needs
3. Update rules with consensus
4. Document decision rationale

### Issue: False positives

**Solution:** Refine rule wording
1. Collect specific examples
2. Clarify rule language
3. Add examples to rule documentation
4. Test on more cases

## Next Steps

1. **Expand rules**: Add more project-specific rules
2. **Create templates**: Share rule sets across teams
3. **Automate**: Integrate with pre-commit hooks
4. **Measure**: Track impact on code quality

## Additional Resources

- [Custom Rules Guide](../instructions/review-and-merge-custom-rules.md)
- [Rule Templates](../examples/custom-rules/)
- [Main Setup Guide](../instructions/review-and-merge.md)

## Checklist

- [ ] Create .github/review-rules.yml
- [ ] Update workflow to use custom rules
- [ ] Test on sample PR with violations
- [ ] Verify AI catches violations
- [ ] Fix violations and re-test
- [ ] Communicate to team
- [ ] Monitor adoption
- [ ] Gather feedback and iterate

---

**Congratulations!** You've successfully implemented custom review rules.

**Questions?** Open an issue or discussion on GitHub.
