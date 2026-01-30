#!/usr/bin/env python3
"""
Codex CLI wrapper for code review and analysis.

This script wraps the OpenAI Codex CLI to perform automated code reviews,
analysis, and Q&A on codebases.
"""

import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import time

# Setup common library access for Miyabi skills (dynamic discovery)
def find_claude_lib():
    current = Path(__file__).resolve()
    for _ in range(8):  # Search up to 8 levels
        claude_lib = current / '.claude' / 'lib'
        if claude_lib.exists():
            return str(claude_lib)
        current = current.parent
        if current == current.parent:  # Filesystem root reached
            break
    return None  # Not found

claude_lib_path = find_claude_lib()
if claude_lib_path:
    sys.path.insert(0, claude_lib_path)
    from env_utils import setup_python_path, load_env_files

    # Initialize environment
    setup_python_path()
    load_env_files()


def find_project_root():
    """
    Find the project root directory by looking for common indicators.

    Returns:
        Path: The project root directory
    """
    current = Path.cwd()

    # Look for common project indicators
    indicators = ['.git', 'package.json', 'requirements.txt', 'pyproject.toml', 'Cargo.toml', 'go.mod']

    for _ in range(10):  # Maximum 10 levels up
        for indicator in indicators:
            if (current / indicator).exists():
                return current
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent

    # Fallback to current directory
    return Path.cwd()


def get_logs_dir() -> Path:
    """
    Get the logs directory for the codex skill.

    Returns:
        Path: The logs directory path
    """
    script_dir = Path(__file__).parent.parent
    logs_dir = script_dir / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def cleanup_old_logs(logs_dir: Path, max_age_hours: int = 24) -> None:
    """
    Remove log files older than the specified age.

    Args:
        logs_dir: Directory containing log files
        max_age_hours: Maximum age of log files in hours (default: 24)
    """
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600

    log_files = logs_dir.glob('codex_*.md')
    removed_count = 0

    for log_file in log_files:
        file_age = current_time - log_file.stat().st_mtime
        if file_age > max_age_seconds:
            log_file.unlink()
            removed_count += 1
            age_hours = file_age / 3600
            print(f"[CLEANUP] Removed {log_file.name} (age: {age_hours:.1f} hours)", file=sys.stderr)

    if removed_count > 0:
        print(f"[CLEANUP] Removed {removed_count} old log file(s)", file=sys.stderr)


def read_project_context(project_dir: str) -> str:
    """
    Read key project files to provide context to Codex.

    Args:
        project_dir: The project directory

    Returns:
        str: Formatted project context
    """
    project_path = Path(project_dir)
    context_parts = []

    # Read key files
    key_files = [
        'PURPOSE.md',
        'SYSTEM_CONSTITUTION.md',
        'README.md',
        'AGENTS.md',
    ]

    for filename in key_files:
        file_path = project_path / filename
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            # Truncate if too long
            if len(content) > 5000:
                content = content[:5000] + "\n... [truncated]"
            context_parts.append(f"## {filename}\n{content}")

    # Get Python file list
    py_files = list(project_path.rglob('*.py'))
    py_files = [f for f in py_files if 'venv' not in str(f) and 'node_modules' not in str(f)]

    context_parts.append(f"\n## Source Files (total: {len(py_files)})")
    for py_file in py_files[:30]:  # First 30 files
        rel_path = py_file.relative_to(project_path)
        context_parts.append(f"- {rel_path}")

    return "\n\n".join(context_parts)


def run_codex(request: str, project_dir: str = None, sandbox: bool = True,
              stream_output: bool = True, output_file: Path = None) -> str:
    """
    Run Codex CLI with the specified request.

    Args:
        request: The request/question to ask Codex
        project_dir: The project directory to analyze (default: auto-detect)
        sandbox: Whether to run in sandbox mode (default: True)
        stream_output: Whether to stream output in real-time (default: True)
        output_file: Path to save output log (default: auto-generated timestamped file)

    Returns:
        str: The output from Codex (empty if streaming)
    """
    # Auto-detect project directory if not specified
    if project_dir is None:
        project_dir = str(find_project_root())

    # Read project context
    print("[LOG] Reading project context...", file=sys.stderr)
    project_context = read_project_context(project_dir)

    # Build enhanced request
    enhanced_request = f"""# Project Context

{project_context}

# Review Request

{request}

Please provide a comprehensive review with specific file references and line numbers where applicable."""

    # Generate default output file path if not specified
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = get_logs_dir() / f'codex_{timestamp}.md'

    # Build the command
    cmd = ['codex', 'exec']

    if sandbox:
        cmd.extend(['--sandbox', 'danger-full-access'])
    else:
        cmd.extend(['--dangerously-bypass-approvals-and-sandbox'])

    cmd.extend(['--cd', project_dir, enhanced_request])

    # Print log location
    print(f"[LOG] Output will be saved to: {output_file}", file=sys.stderr)

    # Execute the command
    try:
        if stream_output:
            # Stream output in real-time to both stdout and file
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1  # Line buffered
            )

            # Stream output line by line
            output_lines = []
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"# Codex Analysis Report\n\n")
                f.write(f"**Generated**: {datetime.now().isoformat()}\n")
                f.write(f"**Request**: {request}\n")
                f.write(f"**Project**: {project_dir}\n\n")
                f.write("---\n\n")

                for line in process.stdout:
                    # Print to stdout
                    print(line, end='', flush=True)
                    # Write to file
                    f.write(line)
                    # Flush file immediately
                    f.flush()
                    # Store for return
                    output_lines.append(line)

            process.wait()

            if process.returncode != 0:
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n**ERROR**: Codex exited with code {process.returncode}\n")
                raise subprocess.CalledProcessError(process.returncode, cmd)

            print(f"\n[LOG] Analysis complete: {output_file}", file=sys.stderr)

            return ''.join(output_lines)
        else:
            # Capture output (original behavior)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=600  # 10 minute timeout
            )

            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Codex Analysis Report\n\n")
                f.write(f"**Generated**: {datetime.now().isoformat()}\n")
                f.write(f"**Request**: {request}\n")
                f.write(f"**Project**: {project_dir}\n\n")
                f.write("---\n\n")
                f.write(result.stdout)

            print(f"[LOG] Analysis complete: {output_file}", file=sys.stderr)

            return result.stdout

    except subprocess.CalledProcessError as e:
        error_msg = f"Error running Codex: {e}"
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n**ERROR**: {error_msg}\n")
        return error_msg
    except subprocess.TimeoutExpired:
        error_msg = "Error: Codex execution timed out after 10 minutes"
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n**ERROR**: {error_msg}\n")
        return error_msg
    except FileNotFoundError:
        error_msg = "Error: Codex CLI not found. Please ensure it is installed and in your PATH."
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n**ERROR**: {error_msg}\n")
        return error_msg


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Run Codex CLI for code review and analysis'
    )
    parser.add_argument(
        'request',
        help='The request/question to ask Codex'
    )
    parser.add_argument(
        '--project-dir',
        help='Project directory to analyze (default: auto-detect)',
        default=None
    )
    parser.add_argument(
        '--no-sandbox',
        help='Disable sandbox mode',
        action='store_true'
    )
    parser.add_argument(
        '--no-stream',
        help='Disable real-time output streaming (print all at end)',
        action='store_true'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output log file path (default: auto-generated timestamped file in logs/)',
        default=None
    )
    parser.add_argument(
        '--max-age-hours',
        type=int,
        help='Maximum age of log files in hours (default: 24)',
        default=24
    )

    args = parser.parse_args()

    # Run Codex
    run_codex(
        request=args.request,
        project_dir=args.project_dir,
        sandbox=not args.no_sandbox,
        stream_output=not args.no_stream,
        output_file=args.output
    )

    # Cleanup old logs
    if args.max_age_hours > 0:
        logs_dir = get_logs_dir()
        cleanup_old_logs(logs_dir, max_age_hours=args.max_age_hours)


if __name__ == '__main__':
    main()
