# Codex Request Patterns

## Effective Request Templates

This document provides tested request templates for common code review and analysis scenarios.

## Code Review Patterns

### General Code Review

```
"Review this codebase for:
1. Potential bugs and edge cases
2. Code quality issues
3. Performance concerns
4. Security vulnerabilities
5. Best practices violations

Provide specific file locations and suggestions for improvement."
```

### Focused Review (Specific Module)

```
"Review the authentication module (src/auth/) for:
- SQL injection vulnerabilities
- Session management issues
- Password handling security
- Error information disclosure"
```

### Architecture Review

```
"Analyze the architecture of this application:
1. Identify architectural patterns used
2. Evaluate separation of concerns
3. Check for tight coupling issues
4. Suggest improvements for scalability
5. Identify potential single points of failure"
```

## Bug Investigation Patterns

### General Bug Investigation

```
"Investigate the following issue: [describe issue]
1. Identify the root cause
2. Locate all affected code sections
3. Explain why the bug occurs
4. Suggest fixes with priority ranking"
```

### Performance Investigation

```
"Investigate performance issues:
1. Identify potential bottlenecks
2. Find inefficient algorithms or database queries
3. Locate memory leaks or excessive allocations
4. Suggest optimization opportunities"
```

### Integration Issue Investigation

```
"Investigate why the integration between [component A] and [component B] is failing:
1. Check API contract compliance
2. Verify data flow and transformations
3. Identify version compatibility issues
4. Check error handling"
```

## Refactoring Patterns

### Code Quality Refactoring

```
"Identify refactoring opportunities to improve:
1. Code readability
2. Maintainability
3. DRY principle adherence
4. Naming conventions
5. Function/class complexity

For each issue, provide:
- Current code location
- Problem description
- Suggested refactoring approach"
```

### Modernization Refactoring

```
"Identify opportunities to modernize this codebase:
1. Outdated patterns that can be replaced
2. Deprecated API usage
3. Opportunities to use modern language features
4. Library updates that would benefit the code"
```

## Security Review Patterns

### OWASP Top 10 Review

```
"Review this codebase for OWASP Top 10 vulnerabilities:
1. Injection (SQL, NoSQL, OS command, LDAP)
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities (XXE)
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. Using Components with Known Vulnerabilities
10. Insufficient Logging & Monitoring"
```

### Specific Security Concern

```
"Review for [specific security concern]:
1. Identify all vulnerable code paths
2. Assess severity and exploitability
3. Check for existing mitigations
4. Recommend security improvements"
```

## Learning & Understanding Patterns

### Code Explanation

```
"Explain the following code:
1. What is the purpose of this component?
2. How does it work?
3. What are the key design decisions?
4. What are the dependencies and interactions?

Focus on: [specific file or directory]"
```

### Design Pattern Identification

```
"Identify design patterns used in this codebase:
1. List all design patterns found
2. Explain where and how each is used
3. Evaluate if patterns are applied correctly
4. Suggest pattern improvements where applicable"
```

### Documentation Generation

```
"Generate documentation for [component]:
1. Purpose and functionality
2. Public API/Interface
3. Usage examples
4. Dependencies and requirements
5. Configuration options"
```

## Testing Patterns

### Test Coverage Analysis

```
"Analyze test coverage:
1. Identify untested critical paths
2. Find areas lacking edge case tests
3. Check for missing error handling tests
4. Suggest test cases to add"
```

### Test Quality Review

```
"Review test quality:
1. Check for brittle or flaky tests
2. Identify test code duplication
3. Evaluate test organization and structure
4. Suggest improvements for test maintainability"
```

## Customization Guidelines

### Creating Effective Requests

1. **Be Specific**: Narrow the scope for better results
   - Instead of: "Review the code"
   - Use: "Review the user authentication flow for security issues"

2. **Provide Context**: Give background information
   - "This is a Django web application with PostgreSQL"
   - "The codebase handles financial transactions"

3. **Specify Output Format**: Request structured output
   - "Provide results in a table with columns: File, Issue, Severity, Suggestion"
   - "Group findings by category: Security, Performance, Maintainability"

4. **Set Priorities**: Indicate what matters most
   - "Focus on security vulnerabilities over style issues"
   - "Prioritize performance bottlenecks in the API layer"

### Iterative Refinement

1. Start with a broad request
2. Review the results
3. Ask follow-up questions based on findings
4. Drill down into specific areas of concern

## Language-Specific Patterns

### Python

```
"Review this Python code for:
1. PEP 8 style compliance
2. Pythonic idioms (list comprehensions, context managers, etc.)
3. Exception handling best practices
4. Type hints usage
5. Common Python anti-patterns"
```

### JavaScript/TypeScript

```
"Review this JavaScript/TypeScript code for:
1. Async/await patterns and Promise handling
2. Memory leaks (event listeners, closures)
3. TypeScript type safety
4. ES6+ feature utilization
5. Common JS vulnerabilities (XSS, prototype pollution)"
```

### Go

```
"Review this Go code for:
1. Error handling patterns
2. Goroutine and channel usage
3. Resource cleanup (defer)
4. Interface design
5. Common Go idioms"
```
