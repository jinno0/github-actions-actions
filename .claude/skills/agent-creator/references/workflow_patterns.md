# Agent Workflow Patterns

This document describes common workflow patterns used by agents in the Miyabi framework.

## Universal Workflow Pattern

All agents follow a similar workflow structure:

1. **Initial Assessment** - Analyze current state and requirements
2. **Execution** - Apply specialized expertise using available tools
3. **Validation** - Verify results meet quality standards
4. **Reporting** - Provide clear recommendations and next steps

## Type-Specific Workflow Patterns

### Code Review Workflow

**Phase Distribution**: Architecture (25%) → Code Quality (20%) → Security (20%) → Performance (15%) → Testing (10%) → Documentation (10%)

**Key Focus Areas**:
- SOLID principles, modularity, dependency management
- Code smells, error handling, naming conventions
- OWASP Top 10, dependency security, input validation
- Algorithmic complexity, resource management, scalability
- Test coverage, edge cases, integration testing
- API consistency, documentation completeness

### Deployment Workflow

**Phases**: Pre-deployment Validation → Execution → Health Check → Rollback Management → Post-deployment Tasks

**Key Focus Areas**:
- Test coverage, build artifacts, environment configs, rollback procedures
- Pipeline execution, progress monitoring, failure handling
- Health checks, performance metrics, user workflows
- Rollback triggers, impact analysis, monitoring updates
- Stakeholder notification, documentation, next deployment planning

### Testing Workflow

**Phases**: Test Planning → Test Execution → Test Analysis → Quality Validation → Reporting

**Key Focus Areas**:
- Requirements analysis, test types, success criteria
- Unit/integration/E2E tests, security, performance, accessibility
- Results analysis, root cause identification, gap assessment
- Code quality standards, security vulnerabilities, performance benchmarks
- Comprehensive reports, improvement recommendations, action plans

### Documentation Workflow

**Phases**: Documentation Analysis → Content Generation → Structure Organization → Quality Assurance → Maintenance Planning

**Key Focus Areas**:
- Codebase analysis, documentation gaps, audience needs
- API docs, README files, technical guides, tutorials
- Logical organization, consistent formatting, navigation
- Technical accuracy, completeness, example validation
- Update workflows, review cycles, user feedback

### Security Workflow

**Phases**: Security Scanning → Threat Analysis → Compliance Validation → Risk Assessment → Security Reporting

**Key Focus Areas**:
- Code scans, OWASP Top 10, dependency security, secret scanning
- Threat identification, attack surface assessment, incident response
- Regulatory compliance, security policies, audit requirements
- Risk categorization, remediation recommendations, exploitability estimation
- Security reports, improvement recommendations, metrics establishment

### General Purpose Workflow

**Phases**: Requirement Analysis → Information Gathering → Problem Decomposition → Execution & Coordination → Synthesis & Reporting

**Key Focus Areas**:
- Task objectives, constraints, success criteria, resource planning
- Research, codebase analysis, context gathering, validation
- Task decomposition, dependency identification, contingency planning
- Systematic execution, agent coordination, issue handling
- Result synthesis, report generation, recommendations, knowledge sharing

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