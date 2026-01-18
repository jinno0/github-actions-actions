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
from datetime import datetime
import glob
import shutil

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


def cleanup_old_logs(logs_dir: Path, keep_count: int = 10) -> None:
    """
    Remove old log files, keeping only the most recent ones.

    Args:
        logs_dir: Directory containing log files
        keep_count: Number of recent logs to keep (default: 10)
    """
    log_files = sorted(
        logs_dir.glob('codex_*.md'),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    # Remove logs beyond the keep count
    for old_log in log_files[keep_count:]:
        old_log.unlink()
        print(f"[CLEANUP] Removed old log: {old_log.name}", file=sys.stderr)


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

    # Generate default output file path if not specified
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = get_logs_dir() / f'codex_{timestamp}.md'

    # Build the command
    cmd = [
        'codex',
        'exec',
        '--full-auto'
    ]

    if sandbox:
        cmd.extend(['--sandbox', 'read-only'])

    cmd.extend(['--cd', project_dir, request])

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
        '--keep-logs',
        type=int,
        help='Number of recent logs to keep (default: 10)',
        default=10
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
    if args.keep_logs > 0:
        logs_dir = get_logs_dir()
        cleanup_old_logs(logs_dir, keep_count=args.keep_logs)


if __name__ == '__main__':
    main()
