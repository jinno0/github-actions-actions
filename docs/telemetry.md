# Telemetry and Privacy Policy

**Last Updated**: 2026-02-03
**Version**: 1.0

## Overview

This project collects anonymous usage telemetry to help us understand how Actions are being used and identify areas for improvement. We take privacy seriously and have designed our telemetry system with the following principles:

- **Opt-out by default**: You can disable telemetry at any time
- **Anonymous**: Repository names are hashed before collection
- **Minimal**: We only collect essential metrics
- **Transparent**: This document explains exactly what we collect

## What We Collect

### Per Execution Metrics

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `action_name` | string | Name of the Action executed | `"review-and-merge"` |
| `timestamp` | string | ISO 8601 timestamp (UTC) | `"2026-02-03T08:00:00Z"` |
| `status` | string | Execution status | `"success"`, `"failure"`, `"error"` |
| `duration_ms` | integer | Execution duration in milliseconds | `1234` |
| `repository_anonymous_id` | string | First 16 chars of SHA-256 hash of repo name | `"a1b2c3d4e5f6g7h8"` |
| `runner_os` | string | Operating system of the runner | `"Linux"`, `"macOS"`, `"Windows"` |
| `claude_cli_version` | string | Version of Claude CLI (if available) | `"1.2.3"` |
| `error_type` | string | Error message (only on failure, max 200 chars) | `"File not found"` |

### What We DON'T Collect

- ❌ Code snippets or file contents
- ❌ Repository names (stored as hashes only)
- ❌ Personal information (PII)
- ❌ Access tokens or credentials
- ❌ IP addresses
- ❌ Sensitive business data

## How We Use This Data

Collected metrics are used to:

1. **Measure Adoption**: Track how many teams use each Action
2. **Identify Issues**: Detect failing Actions quickly
3. **Prioritize Improvements**: Focus development on high-impact areas
4. **Demonstrate Value**: Show impact to stakeholders

### Example Analysis

```
Q1 2026 Metrics Summary:
- Total executions: 1,234
- Most used Actions: review-and-merge (45%), auto-refactor (30%)
- Average success rate: 97%
- Top error: "Claude CLI not found" (12 occurrences)
```

## Privacy Features

### Anonymization

Repository names are anonymized using SHA-256 hashing:

```python
# Before hashing
repository = "acme-corp/main-project"

# After hashing (first 16 chars)
repository_anonymous_id = "a1b2c3d4e5f6g7h8"
```

**Important**: Hashing is one-way. It's computationally infeasible to recover the original repository name from the hash.

### Opt-Out Mechanism

You can disable telemetry collection by setting the `DISABLE_TELEMETRY` environment variable:

```yaml
# In your GitHub Actions workflow
env:
  DISABLE_TELEMETRY: "true"
```

Or globally in your self-hosted runner configuration:

```bash
# In runner's environment
export DISABLE_TELEMETRY="true"
```

### Data Retention

Telemetry data is currently stored in `metrics/telemetry/telemetry.log` within this repository. Future versions may:

- Send data to an external analytics service (e.g., Google Analytics 4)
- Implement automatic data retention (e.g., delete logs after 90 days)
- Aggregate data for public dashboards

Any changes to data handling will be documented in this file.

## Security Considerations

### Data in Transit

Currently, telemetry is written to a local file. If external transmission is implemented:

- All data will be sent over HTTPS/TLS 1.3
- No sensitive data is transmitted
- Data is aggregated before sending (when possible)

### Data at Rest

Telemetry logs are stored in `metrics/telemetry/`:
- **Access**: Repository maintainers only
- **Permissions**: Controlled via GitHub repository settings
- **Backup**: Included in git repository (ensure `.gitignore` is configured appropriately)

### Recommendations for Production Use

If you fork or deploy this project:

1. **Review telemetry settings**: Decide if you want to keep telemetry enabled
2. **Configure storage**: Consider external analytics (GA4, Mixpanel, self-hosted)
3. **Set retention policies**: Don't keep logs indefinitely
4. **Document changes**: Update this file with your privacy practices

## Compliance

### GDPR (EU General Data Protection Regulation)

- **Lawful Basis**: Legitimate Interest for product improvement
- **Data Controller**: Repository maintainers
- **Data Subject Rights**: Users can opt-out at any time
- **Data Minimization**: Only essential metrics collected

### California Consumer Privacy Act (CCPA)

- **Opt-Out**: Available via `DISABLE_TELEMETRY` environment variable
- **No Sale**: Data is never sold to third parties

## Questions or Concerns?

If you have questions about telemetry or privacy:

1. Check this document first
2. Review `scripts/collect_metrics.py` source code
3. Open a GitHub Issue with the `privacy` label

## Changes to This Policy

We may update this policy as we improve the telemetry system. Significant changes will be:

- Announced in the project changelog
- Tagged with the updated date
- Reviewed for privacy implications

---

**Version History**:
- **v1.0** (2026-02-03): Initial telemetry policy
