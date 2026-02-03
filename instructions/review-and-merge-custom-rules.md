# Custom Rule Injection Guide

The **review-and-merge** action supports injecting custom review rules to tailor AI behavior to your project's specific standards and conventions.

## Overview

Custom rules allow you to:
- Enforce project-specific coding standards
- Add security requirements for your domain
- Specify architectural patterns and constraints
- Customize review focus areas

## Basic Usage

### Step 1: Define Your Rules

Create a custom rules file (e.g., `.github/review-rules.yml`):

```yaml
# Custom review rules for my project
custom-rules: |
  1. Always use TypeScript strict mode
  2. No console.log in production code
  3. All async functions must have error handling
  4. API responses must be validated with schemas
  5. No hardcoded credentials or secrets
```

### Step 2: Reference in Workflow

Update your `.github/workflows/review-and-merge.yml`:

```yaml
- name: Review and Merge
  uses: owner/repo/actions/review-and-merge@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    custom-rules: |
      1. Always use TypeScript strict mode
      2. No console.log in production code
      3. All async functions must have error handling
```

### Step 3: Run and Verify

Commit your changes and open a PR. The AI will review against your custom rules.

## Rule Categories

### 1. Style Rules

Enforce code style and formatting conventions:

```yaml
custom-rules: |
  - Use 2-space indentation (no tabs)
  - Prefer const over let when variable is not reassigned
  - Use template literals instead of string concatenation
  - Add JSDoc comments to all public functions
  - Limit line length to 100 characters
```

### 2. Security Rules

Enforce security best practices:

```yaml
custom-rules: |
  - No hardcoded credentials, API keys, or secrets
  - Use environment variables for sensitive data
  - Validate and sanitize all user inputs
  - Use parameterized queries to prevent SQL injection
  - Implement proper authentication and authorization checks
  - Don't expose error details to clients
  - Use HTTPS for all external API calls
```

### 3. Performance Rules

Enforce performance guidelines:

```yaml
custom-rules: |
  - Avoid nested loops (prefer O(n) algorithms)
  - Implement caching for expensive operations
  - Use pagination for large datasets
  - Lazy load non-critical resources
  - Debounce or throttle event handlers
  - Avoid unnecessary re-renders in React components
```

### 4. Architecture Rules

Enforce architectural patterns:

```yaml
custom-rules: |
  - Follow layered architecture (controllers → services → repositories)
  - Use dependency injection for service dependencies
  - Implement repository pattern for data access
  - Separate business logic from presentation logic
  - Use interfaces/contracts for service boundaries
  - Avoid circular dependencies
```

### 5. Testing Rules

Enforce testing standards:

```yaml
custom-rules: |
  - All new code must have unit tests
  - Test files must be co-located with source files
  - Use descriptive test names (should_... convention)
  - Mock external dependencies in tests
  - Achieve minimum 80% code coverage
  - Test error paths, not just happy paths
```

## Rule Templates by Language

### TypeScript/JavaScript

```yaml
custom-rules: |
  - Enable TypeScript strict mode (strictNullChecks, noImplicitAny)
  - Use explicit return types for functions
  - Prefer interface over type for object shapes
  - Use enum for fixed sets of values
  - Avoid using 'any' type
  - Use async/await instead of Promise chains
  - Handle promise rejections with try/catch
```

### Python

```yaml
custom-rules: |
  - Follow PEP 8 style guide
  - Use type hints for function parameters and returns
  - Write docstrings for all functions and classes
  - Use context managers (with statements) for resource management
  - Prefer list comprehensions over map/filter
  - Use f-strings for string formatting
  - Handle exceptions specifically, avoid bare except
```

### Go

```yaml
custom-rules: |
  - Follow effective Go guidelines
  - Handle errors explicitly, don't ignore them
  - Use goroutines for concurrent operations
  - Implement proper error wrapping with fmt.Errorf
  - Use channels for goroutine communication
  - Avoid package-level state
  - Implement proper defer for cleanup
```

## Advanced Usage

### Multi-line Rules with Examples

```yaml
custom-rules: |
  When reviewing API endpoints:
  - Ensure proper HTTP methods are used (GET, POST, PUT, DELETE)
  - Implement request validation with schemas
  - Return appropriate HTTP status codes
  - Include error messages in response body
  - Add rate limiting for public endpoints
  - Document endpoints with OpenAPI/Swagger
```

### Conditional Rules

```yaml
custom-rules: |
  For database operations:
  - Always use transactions for multi-step operations
  - Implement proper indexing for query performance
  - Use parameterized queries to prevent SQL injection
  - Add retry logic for transient failures
  - Log slow queries for optimization

  For frontend components:
  - Ensure responsive design for mobile devices
  - Implement loading states for async operations
  - Add error boundaries for error handling
  - Test accessibility with screen readers
```

### Framework-Specific Rules

#### Express.js

```yaml
custom-rules: |
  - Use middleware for cross-cutting concerns (auth, logging)
  - Implement proper error handling middleware
  - Validate request data with middleware (e.g., express-validator)
  - Use async/await in route handlers
  - Implement proper HTTP status codes
  - Set security headers (helmet middleware)
  - Rate limit authentication endpoints
```

#### Django

```yaml
custom-rules: |
  - Use Django ORM, avoid raw SQL
  - Implement proper model validation
  - Use Django's authentication system
  - Implement CSRF protection
  - Use select_related/prefetch_related for query optimization
  - Implement proper middleware order
  - Use Django's built-in security features
```

## Best Practices

### 1. Be Specific and Actionable

❌ Bad: "Write better code"

✅ Good: "Use TypeScript strict mode with noImplicitAny enabled"

### 2. Focus on High-Impact Rules

Prioritize rules that:
- Prevent security vulnerabilities
- Improve code maintainability
- Catch common bugs
- Enforce architectural consistency

### 3. Keep Rules Concise

Each rule should be one clear, testable statement.

### 4. Review and Update Regularly

Rules should evolve with your project. Review them quarterly.

### 5. Get Team Buy-In

Discuss rules with your team to ensure alignment.

## Examples Repository

See `examples/custom-rules/` for ready-to-use rule templates:
- `typescript-strict.yml` - TypeScript strict mode
- `security-best-practices.yml` - Security guidelines
- `python-style.yml` - Python PEP 8 compliance

## Troubleshooting

### Q: The AI is not enforcing my rules

**A:** Check that:
1. Rules are properly formatted in the YAML
2. Rules are specific and actionable
3. Rules don't contradict each other
4. You're using the latest version of the action

### Q: Too many rule violations

**A:** Consider:
1. Phasing in rules gradually
2. Marking some rules as warnings (future enforcement)
3. Providing migration documentation
4. Running linting tools separately

### Q: Rules conflict with existing code style

**A:**
1. Review if the rule is appropriate for your project
2. Update rules to match your conventions
3. Consider if legacy code needs exceptions

## Integration with Other Actions

Custom rules work great with:
- **action-fixer**: Automatically fix rule violations
- **auto-refactor**: Apply rule-based refactoring
- **spec-to-code**: Generate code that follows rules

## Next Steps

1. Start with basic rules from this guide
2. Customize for your project's needs
3. Test on a few PRs to tune the rules
4. Roll out to the entire team
5. Gather feedback and iterate

## Additional Resources

- [Main Setup Guide](./review-and-merge.md)
- [Example Workflow](../examples/review-and-merge-example.yml)
- [Custom Rule Examples](../examples/custom-rules/)

---

**Need Help?** Open an issue or discussion on GitHub.
