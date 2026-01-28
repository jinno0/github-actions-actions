# Code Review Workflow

When performing code reviews, follow this systematic approach:

1. **Architecture & Design Analysis** (25% weight)
   - Evaluate overall architecture and design patterns
   - Check for SOLID principles adherence
   - Assess modularity and maintainability
   - Identify potential architectural improvements

2. **Code Quality Assessment** (20% weight)
   - Review code readability and style consistency
   - Check for code smells and anti-patterns
   - Evaluate error handling and edge cases
   - Assess naming conventions and documentation

3. **Security & Dependencies** (20% weight)
   - Scan for OWASP Top 10 vulnerabilities
   - Check dependency security and versions
   - Validate input sanitization and data validation
   - Review authentication and authorization

4. **Performance & Scalability** (15% weight)
   - Analyze algorithmic complexity
   - Check for performance bottlenecks
   - Evaluate memory usage and resource management
   - Assess scalability considerations

5. **Testing Coverage** (10% weight)
   - Review test coverage and quality
   - Check for missing edge case tests
   - Evaluate test structure and maintainability
   - Assess integration testing

6. **Documentation & API Design** (10% weight)
   - Review API design and consistency
   - Check documentation completeness and clarity
   - Evaluate inline code comments
   - Assess user-facing documentation

Provide specific, actionable feedback with:
- Exact file paths and line numbers
- Concrete improvement suggestions
- Code examples where helpful
- Priority levels (Critical/High/Medium/Low)
