#!/usr/bin/env python3
"""
Clean up temporary files (MD, JSON) older than specified age.

This script removes temporary report files, archive files, and other
generated artifacts to prevent repository bloat.
"""

import argparse
import time
from pathlib import Path


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


# Files that should NEVER be deleted (critical project files)
PROTECTED_FILES = {
    'README.md',
    'CONTRIBUTING.md',
    'CHANGELOG.md',
    'LICENSE',
    'PURPOSE.md',
    'SYSTEM_CONSTITUTION.md',
    'AGENTS.md',
    'TASKS.md',
    # Important guides that should never be auto-deleted
    'spec_workflow_guide.md',
    'SKILL.md',
    'CLAUDE.md',
    'package.json',
    'package-lock.json',
    'requirements.txt',
    'pyproject.toml',
    'tsconfig.json',
    '.gitignore',
}


# Patterns that indicate temporary/generated files
TEMP_PATTERNS = [
    '*_SUMMARY.md',
    '*_REPORT.md',
    '*_RESULTS.md',
    '*_RECOMMENDATIONS.md',
    '*_OPERATIONS*.md',
    'IMPLEMENTATION_*.md',
    'COMMIT_*.md',
    'CLEANUP_*.md',
    'MAINTENANCE_*.md',
    'TEST_*.md',
    '*_coverage.json',
    '*_coverage.xml',
    'coverage*.json',
    'test_results*.xml',
    'TEMP_*.md',
    'TMP_*.md',
    'DRAFT_*.md',
    'OLD_*.md',
    'BAK_*.md',
    '*_backup.md',
    '*_temp.md',
]


def should_delete_file(file_path: Path, temp_patterns: list) -> bool:
    """
    Determine if a file should be deleted based on its name and location.

    Args:
        file_path: Path to the file
        temp_patterns: List of glob patterns for temporary files

    Returns:
        bool: True if file should be deleted
    """
    # Never delete protected files
    if file_path.name in PROTECTED_FILES:
        return False

    # Check if it matches temporary patterns
    for pattern in temp_patterns:
        if file_path.match(pattern):
            return True

    # Check if it's in an archive directory
    if 'archive' in file_path.parts:
        return True

    # Check if it's in logs directory
    if 'logs' in file_path.parts:
        return True

    return False


def cleanup_temp_files(
    project_dir: Path,
    max_age_hours: int = 24,
    dry_run: bool = False,
    verbose: bool = False
) -> dict:
    """
    Clean up temporary files older than specified age.

    Args:
        project_dir: Project root directory
        max_age_hours: Maximum age in hours (default: 24)
        dry_run: If True, only report what would be deleted
        verbose: If True, print detailed information

    Returns:
        dict: Statistics about cleanup operation
    """
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600

    stats = {
        'scanned': 0,
        'deleted': 0,
        'skipped': 0,
        'total_size_mb': 0.0,
    }

    # Scan for MD and JSON files
    for ext in ['*.md', '*.json']:
        for file_path in project_dir.rglob(ext):
            stats['scanned'] += 1

            # Skip if in .git or node_modules
            if '.git' in file_path.parts or 'node_modules' in file_path.parts:
                stats['skipped'] += 1
                continue

            # Skip protected files
            if file_path.name in PROTECTED_FILES:
                stats['skipped'] += 1
                if verbose:
                    print(f"[SKIP] Protected: {file_path.relative_to(project_dir)}")
                continue

            # Check if file should be deleted
            if not should_delete_file(file_path, TEMP_PATTERNS):
                stats['skipped'] += 1
                continue

            # Check file age
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                file_size_mb = file_path.stat().st_size / (1024 * 1024)
                stats['total_size_mb'] += file_size_mb
                stats['deleted'] += 1

                rel_path = file_path.relative_to(project_dir)
                age_hours = file_age / 3600

                if dry_run:
                    print(f"[DRYRUN] Would delete: {rel_path} (age: {age_hours:.1f}h, size: {file_size_mb:.2f}MB)")
                else:
                    file_path.unlink()
                    print(f"[DELETE] {rel_path} (age: {age_hours:.1f}h, size: {file_size_mb:.2f}MB)")
            else:
                stats['skipped'] += 1
                if verbose:
                    age_hours = file_age / 3600
                    rel_path = file_path.relative_to(project_dir)
                    print(f"[TOO_RECENT] {rel_path} (age: {age_hours:.1f}h)")

    return stats


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Clean up temporary files older than specified age'
    )
    parser.add_argument(
        '--project-dir',
        type=Path,
        help='Project directory (default: auto-detect)',
        default=None
    )
    parser.add_argument(
        '--max-age-hours',
        type=int,
        help='Maximum age of files in hours (default: 24)',
        default=24
    )
    parser.add_argument(
        '--dry-run',
        help='Only report what would be deleted without actually deleting',
        action='store_true'
    )
    parser.add_argument(
        '--verbose', '-v',
        help='Print detailed information about all scanned files',
        action='store_true'
    )

    args = parser.parse_args()

    # Auto-detect project directory if not specified
    if args.project_dir is None:
        project_dir = find_project_root()
    else:
        project_dir = args.project_dir

    print(f"[CLEANUP] Project directory: {project_dir}")
    print(f"[CLEANUP] Maximum age: {args.max_age_hours} hours")
    print(f"[CLEANUP] Mode: {'DRY RUN' if args.dry_run else 'DELETE'}")
    print()

    # Run cleanup
    stats = cleanup_temp_files(
        project_dir=project_dir,
        max_age_hours=args.max_age_hours,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    # Print summary
    print()
    print("=" * 60)
    print("CLEANUP SUMMARY")
    print("=" * 60)
    print(f"Scanned:     {stats['scanned']} files")
    print(f"Deleted:     {stats['deleted']} files")
    print(f"Skipped:     {stats['skipped']} files")
    print(f"Freed space: {stats['total_size_mb']:.2f} MB")
    print("=" * 60)

    if args.dry_run:
        print("\nThis was a DRY RUN. No files were actually deleted.")
        print("Run without --dry-run to perform the actual cleanup.")


if __name__ == '__main__':
    main()
