# GitHub Actions Actions - Project Overview

## Project Purpose

This repository provides a hub of **AI-native GitHub Actions** for improving development efficiency and quality across the entire organization. It focuses on **Composite Actions** that leverage the **Claude Code CLI** running on self-hosted runners to enable context-aware automation (review, fixes, documentation generation, etc.) that was previously impossible with regex or static analysis alone.

## Mission

Provide a trusted, single source of truth for common **Composite Actions** used across the organization's GitHub Actions workflows.

## Core Competencies

1. **AI-Powered Automation**: Leverage Claude Code CLI to process code with semantic understanding
2. **Self-hosted Advantage**: Flexible access to toolchains and resources outside containers
3. **Human-in-the-Loop**: AI suggests/prepares, humans make final decisions or set thresholds

## Current Phase

**Phase 3: Stabilization & Adoption (In Progress)**
- ✅ All core Actions implemented
- ✅ Examples and instructions created
- ⬜ Organization-wide adoption and feedback collection
- ✅ Documentation (README) completed

## Non-Goals (Anti-Patterns)

- ❌ Shell script wrappers (existing Actions are sufficient)
- ❌ Fully autonomous operation (AI hallucination risk)
- ❌ Tightly coupled to specific products (prioritize reusability)
- ❌ Reusable Workflow templates (belongs to github-actions-templates)
- ❌ Runner management (belongs to github-actions-hub)
- ❌ Docker/JavaScript actions (Composite Actions only)

## Key Principles (Immutable)

1. **Single Responsibility**: Each Action has exactly ONE clear purpose
2. **Organization-Wide Reusability**: All Actions must work in any repository
3. **Version Pinning**: Use tags (v1, v2), never @main
4. **Standard Structure**: Every Action has (1) action.yml, (2) example workflow, (3) instruction guide
5. **Template Files**: Prompts/messages in templates/, not hardcoded in action.yml

## Tech Stack

- **Primary**: GitHub Composite Actions (YAML)
- **Runtime**: Self-hosted runner with Claude Code CLI (`claude` command)
- **Helper**: GitHub CLI (`gh` command)
- **Language**: Bash/Shell for action logic
- **Python**: For testing and validation scripts
