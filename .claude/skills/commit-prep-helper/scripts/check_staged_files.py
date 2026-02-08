#!/usr/bin/env python3
"""
Check Staged Files

Gitのステージングされたファイルを検出し、変更内容を分析するスクリプト。
"""

import json
import os
import subprocess

# 定数定義
PACKAGE_FILES = {
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
}


def get_staged_files() -> list[str]:
    """Get list of staged files"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = result.stdout.strip().split("\n")
        return [f for f in files if f]  # 空文字列を除外
    except subprocess.CalledProcessError:
        return []


def get_file_diff_stats(file_path: str) -> dict:
    """Get diff statistics for staged file using --numstat"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--numstat", "--", file_path],
            capture_output=True,
            text=True,
            check=True,
        )

        if not result.stdout.strip():
            return {"added": 0, "removed": 0, "is_binary": False}

        # Parse numstat output: format: "added\tremoved\tfilename"
        # Binary files show as "-\t-\tfilename"
        lines = result.stdout.strip().split("\n")
        for line in lines:
            if line.strip():
                parts = line.split("\t")
                if len(parts) >= 2:
                    # Check for binary file marker
                    if parts[0] == "-" and parts[1] == "-":
                        return {"added": 0, "removed": 0, "is_binary": True}

                    added = int(parts[0]) if parts[0].isdigit() else 0
                    removed = int(parts[1]) if parts[1].isdigit() else 0
                    return {"added": added, "removed": removed, "is_binary": False}

        return {"added": 0, "removed": 0, "is_binary": False}
    except subprocess.CalledProcessError:
        return {"added": 0, "removed": 0, "is_binary": False}


def analyze_changes(files: list[str]) -> dict:
    """Analyze changes in staged files with improved diff parsing"""
    analysis = {
        "total_files": len(files),
        "file_types": {},
        "has_tests": False,
        "has_package_changes": False,
        "binary_files": [],
        "files_detail": [],
    }

    for file_path in files:
        file_ext = os.path.splitext(file_path)[1]

        # Check if file is binary and get diff stats in one call
        diff_stats = get_file_diff_stats(file_path)
        is_binary = diff_stats.get("is_binary", False)

        if is_binary:
            analysis["binary_files"].append(file_path)
            file_detail = {
                "path": file_path,
                "extension": file_ext,
                "is_binary": True,
                "added_lines": 0,
                "removed_lines": 0,
                "has_test": any(
                    p in file_path.lower() for p in ("test", "spec")
                ),
            }
            analysis["files_detail"].append(file_detail)
            analysis["file_types"][file_ext] = (
                analysis["file_types"].get(file_ext, 0) + 1
            )
            continue

        file_detail = {
            "path": file_path,
            "extension": file_ext,
            "is_binary": False,
            "added_lines": diff_stats["added"],
            "removed_lines": diff_stats["removed"],
            "has_test": any(
                p in file_path.lower() for p in ("test", "spec")
            ),
        }

        analysis["files_detail"].append(file_detail)
        analysis["file_types"][file_ext] = analysis["file_types"].get(file_ext, 0) + 1

        if file_detail["has_test"]:
            analysis["has_tests"] = True

        if os.path.basename(file_path) in PACKAGE_FILES:
            analysis["has_package_changes"] = True

    return analysis


def main():
    """Main function"""
    files = get_staged_files()

    if not files:
        print("No staged files found.")
        return

    analysis = analyze_changes(files)

    # Output JSON for other scripts to consume
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
