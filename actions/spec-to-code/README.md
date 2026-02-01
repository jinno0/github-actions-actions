# Spec to Code

Generate production-ready code from Markdown specifications using Claude Code CLI with context-aware AI.

## Features

- **Markdown-to-Code**: Converts human-readable specs into executable code
- **Multi-Language Support**: Works with Python, TypeScript, JavaScript, Go, and more
- **Security-First**: Built-in path traversal protection and spec validation
- **Custom Templates**: Support for custom generation prompt templates
- **Base64 Encoding**: Safely handles specs with special characters

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `spec-path` | **Yes** | - | Path to the Markdown specification file |
| `output-dir` | No | `.` | Directory where code should be generated |
| `language` | No | `TypeScript` | Primary programming language |
| `claude-model` | No | `sonnet` | Claude model to use (sonnet/opus/haiku) |
| `gen-prompt-template` | No | Built-in | Path to custom generation prompt template |
| `github-token` | No | `${{ github.token }}` | GitHub token for API operations |

## Example Usage

### Basic Usage

```yaml
name: Generate from Spec
on:
  push:
    paths:
      - 'specs/**/*.md'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate Code from Spec
        uses: ./actions/spec-to-code
        with:
          spec-path: 'specs/user-auth.md'
          output-dir: 'src/auth'
          language: 'Python'
          claude-model: 'sonnet'

      - name: Commit Generated Code
        run: |
          git config user.name 'GitHub Actions Bot'
          git config user.email 'bot@github.com'
          git add .
          git diff --staged --quiet || git commit -m "Generate code from spec"
          git push
```

### Advanced Usage with Custom Template

```yaml
- name: Generate Code with Custom Rules
  uses: ./actions/spec-to-code
  with:
    spec-path: 'specs/payment-api.md'
    output-dir: 'src/payment'
    language: 'TypeScript'
    gen-prompt-template: '.github/templates/custom-gen.md'
    claude-model: 'opus'
```

## Spec File Format

Your specification should follow this structure:

```markdown
# User Authentication System

## Overview
Implement JWT-based authentication for the web application.

## Requirements
1. User registration with email validation
2. Secure password hashing (bcrypt)
3. JWT token generation and validation
4. Refresh token mechanism

## API Endpoints
- POST /auth/register - Register new user
- POST /auth/login - Authenticate user
- POST /auth/refresh - Refresh access token
- POST /auth/logout - Invalidate tokens

## Data Models
User: {
  id: UUID
  email: string
  password_hash: string
  created_at: timestamp
}

## Security Considerations
- Rate limiting on auth endpoints
- Password requirements: min 8 chars, 1 uppercase, 1 number
- Token expiration: 15 minutes (access), 7 days (refresh)
```

## Security Features

### Path Traversal Protection
The action validates that the output directory is within the workspace:
```yaml
# This will be rejected
output-dir: '../../../etc/passwd'

# This will work
output-dir: 'src/components'
```

### Spec Validation
- Checks spec file exists
- Validates file is readable
- Uses base64 encoding to handle special characters

## Custom Generation Templates

Create a custom template for your project:

```markdown
# .github/templates/custom-gen.md

You are generating code for a high-performance web application.

Requirements:
- Use async/await for all I/O operations
- Include comprehensive error handling
- Add JSDoc/TypeDoc comments
- Follow SOLID principles
- Include unit tests for all functions

Generate code that is production-ready and maintainable.
```

## Supported Languages

- **Python**: 3.8+
- **TypeScript**: 4.0+
- **JavaScript**: ES2020+
- **Go**: 1.19+
- **Rust**: 1.65+
- **Java**: 17+

## Best Practices

### 1. Keep Specs Focused
✅ Good: Single feature or module per spec
❌ Bad: Entire application in one spec

### 2. Be Specific
```markdown
# Good spec
Create a REST API endpoint that accepts user registration data:
- Email (required, must be valid format)
- Password (required, min 8 chars)
- Returns: 201 on success, 400 on validation error

# Vague spec
Create a user registration thing
```

### 3. Include Context
```markdown
# Add context for better code generation
Context:
- This is part of a microservices architecture
- Uses PostgreSQL for data persistence
- Must be compatible with existing auth service
- API version: v2
```

## Output

Generated code will be placed in the specified `output-dir`:
```
output-dir/
├── implementation.code  # Generated code
└── generation.log       # Generation metadata
```

## Troubleshooting

### Spec Not Found
```
Error: Spec file not found: specs/feature.md
```
**Solution**: Verify the spec path is relative to repository root

### Invalid Output Directory
```
Error: Output directory outside workspace
```
**Solution**: Use relative paths within your repository

### Generation Failed
```
Error: Code generation failed
```
**Solution**:
- Check spec syntax is valid Markdown
- Verify Claude Code CLI is installed
- Review spec for ambiguous requirements

## Requirements

- Claude Code CLI installed on runner
- GitHub token with `contents:write` scope
- Spec file must be valid Markdown

## See Also

- [Full workflow examples](../../examples/)
- [Usage guide](../../instructions/spec-to-code.md)
- [Spec best practices](../../docs/spec-format.md)
