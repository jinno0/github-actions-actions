# Agent Workflow Patterns

This document describes common workflow patterns used by agents in the Miyabi framework.

## Universal Workflow Pattern

All agents follow a similar workflow structure:

1. **Initial Assessment** - Analyze current state and requirements
2. **Execution** - Apply specialized expertise using available tools
3. **Validation** - Verify results meet quality standards
4. **Reporting** - Provide clear recommendations and next steps

## Type-Specific Workflows

Specific workflow implementations are documented in the template files:
- Code Review: `templates/workflows/code-review.md`
- Testing: `templates/workflows/testing.md`
- Deployment: `templates/workflows/deployment.md`
- Documentation: `templates/workflows/documentation.md`
- Security: `templates/workflows/security.md`
- General Purpose: `templates/workflows/general-purpose.md`

---

## Workflow Quality Standards

### Common Quality Criteria

All agent workflows should meet these standards:

1. **Clarity**: Steps are clearly defined and unambiguous
2. **Completeness**: All necessary phases are included
3. **Actionability**: Each step produces concrete results
4. **Measurability**: Progress and success can be measured
5. **Adaptability**: Workflow can handle edge cases
6. **Documentation**: Each step is properly documented

### Error Handling Patterns

```markdown
1. **Input Validation**
   - Verify all inputs before processing
   - Handle malformed or incomplete data
   - Provide clear error messages

2. **Exception Handling**
   - Catch and handle expected exceptions
   - Log unexpected errors appropriately
   - Implement graceful degradation

3. **Recovery Procedures**
   - Define rollback strategies
   - Implement retry mechanisms
   - Provide alternative approaches

4. **Error Reporting**
   - Generate clear error reports
   - Include context and debugging info
   - Suggest remediation steps
```

### Performance Optimization

```markdown
1. **Efficient Tool Usage**
   - Minimize unnecessary tool calls
   - Use appropriate tools for each task
   - Batch related operations

2. **Resource Management**
   - Monitor memory and CPU usage
   - Implement caching where appropriate
   - Clean up temporary resources

3. **Parallel Processing**
   - Identify independent tasks
   - Execute in parallel when possible
   - Coordinate parallel results
```

---

*This workflow patterns document is part of the agent-creator skill*