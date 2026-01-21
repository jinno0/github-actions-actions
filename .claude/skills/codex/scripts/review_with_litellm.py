#!/usr/bin/env python3
"""
LiteLLM-based code review script.
Alternative to Codex when landlock/sandbox issues prevent file access.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess
import json

# Setup common library access
def find_claude_lib():
    current = Path(__file__).resolve()
    for _ in range(8):
        claude_lib = current / '.claude' / 'lib'
        if claude_lib.exists():
            return str(claude_lib)
        current = current.parent
        if current == current.parent:
            break
    return None

claude_lib_path = find_claude_lib()
if claude_lib_path:
    sys.path.insert(0, claude_lib_path)
    from env_utils import setup_python_path, load_env_files
    setup_python_path()
    load_env_files()

def get_logs_dir():
    script_dir = Path(__file__).parent.parent
    logs_dir = script_dir / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir

def read_project_files():
    """Read key project files for context."""
    project_root = Path.cwd()
    files_to_read = [
        'PURPOSE.md',
        'SYSTEM_CONSTITUTION.md',
        'README.md',
        'AGENTS.md',
    ]

    content = {}
    for file_path in files_to_read:
        full_path = project_root / file_path
        if full_path.exists():
            content[file_path] = full_path.read_text(encoding='utf-8')
        else:
            content[file_path] = f"[File not found: {file_path}]"

    return content

def get_source_files():
    """Get list of source code files."""
    project_root = Path.cwd()
    source_files = []

    # Python files
    for py_file in project_root.rglob('*.py'):
        # Skip venv, node_modules, etc.
        if 'venv' not in str(py_file) and 'node_modules' not in str(py_file):
            source_files.append(str(py_file.relative_to(project_root)))

    return source_files[:50]  # Limit to 50 files

def call_litellm(prompt: str, model: str = None) -> str:
    """Call LiteLLM API for code review."""
    import requests

    # Get API URL from env
    api_url = os.environ.get('LITELLM_API_URL', 'http://localhost:4000')
    api_key = os.environ.get('LITELLM_API_KEY', '')

    # Default model
    if not model:
        model = os.environ.get('LITELLM_MODEL', 'gpt-4')

    # Prepare request
    url = f"{api_url}/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
    }
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    data = {
        'model': model,
        'messages': [
            {
                'role': 'system',
                'content': 'You are an expert code reviewer. Analyze the provided code and give practical, specific recommendations with file locations.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.3,
        'max_tokens': 8000,
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        result = response.json()

        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error calling LiteLLM: {e}"

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Review codebase with LiteLLM')
    parser.add_argument('--model', help='LiteLLM model to use')
    parser.add_argument('--output', '-o', type=Path, help='Output log file')
    args = parser.parse_args()

    # Generate output file path
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = get_logs_dir() / f'litellm_review_{timestamp}.md'

    print(f"[LOG] Review will be saved to: {output_file}", file=sys.stderr)

    # Read project files
    print("[LOG] Reading project files...", file=sys.stderr)
    project_files = read_project_files()

    # Get source file list
    print("[LOG] Getting source file list...", file=sys.stderr)
    source_files = get_source_files()

    # Build prompt
    prompt = f"""Review this manga-mvv project comprehensively:

## Project Context

### PURPOSE.md
{project_files.get('PURPOSE.md', '[Not found]')}

### SYSTEM_CONSTITUTION.md (first 2000 chars)
{project_files.get('SYSTEM_CONSTITUTION.md', '[Not found]')[:2000]}...

### README.md (first 2000 chars)
{project_files.get('README.md', '[Not found]')[:2000]}...

## Source Files (first 50)
{chr(10).join(source_files[:20])}  # Show first 20

Please analyze:
1. **Project Overview**: Understanding of mission and architecture
2. **Code Quality**: Structure, patterns, technical debt
3. **Architecture**: Provider abstraction, Docker-first approach
4. **Potential Issues**: Security, performance, scalability, error handling
5. **Improvement Suggestions**: Prioritized actionable recommendations

Focus on practical, specific recommendations with file locations.
"""

    # Call LiteLLM
    print("[LOG] Calling LiteLLM API...", file=sys.stderr)
    result = call_litellm(prompt, args.model)

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# LiteLLM Code Review Report\n\n")
        f.write(f"**Generated**: {datetime.now().isoformat()}\n")
        f.write(f"**Model**: {args.model or 'default'}\n")
        f.write(f"**Project**: {Path.cwd()}\n\n")
        f.write("---\n\n")
        f.write(result)

    print(f"[LOG] Review complete: {output_file}", file=sys.stderr)
    print(result)

if __name__ == '__main__':
    main()
