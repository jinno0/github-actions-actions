---
allowed-tools: Bash, Write, TodoWrite
description: Create a new GitHub repository with proper setup including directory creation, git initialization, and remote configuration
category: workflow
argument-hint: "<repository-name>"
---

# GitHub Repository Setup

Create a new GitHub repository named "$ARGUMENTS" with proper directory structure and git setup. Creates a **private** repository by default.

## Commands to execute:

```bash
mkdir "$ARGUMENTS" && cd "$ARGUMENTS" && \
git init && \
gh repo create "$ARGUMENTS" --private && \
echo "# $ARGUMENTS\n\nA new repository created with GitHub CLI." > README.md && \
git add README.md && \
git commit -m "Initial commit" && \
git remote add origin "git@github.com:$(gh api user --jq .login)/$ARGUMENTS.git" && \
git branch -M main && \
git push -u origin main
```

This will create the directory, initialize git, create the GitHub repository, add a README, make an initial commit, and push to GitHub.