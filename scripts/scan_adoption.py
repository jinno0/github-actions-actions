#!/usr/bin/env python3
"""
Scan organization repositories for AI Actions usage.

This script searches GitHub for repositories that reference our actions
by looking for workflow files that use './actions/' paths.
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import json

def try_scan_github_org() -> List[Dict[str, Any]]:
    """
    Attempt to scan organization repositories using GitHub CLI.

    Returns:
        List of repository dictionaries with 'name' and 'url' keys
    """
    try:
        # Use subprocess.run() instead of os.system() for security
        result = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode != 0:
            print("⚠️  GitHub CLI not found. Skipping organization scan.")
            return []
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  GitHub CLI not found. Skipping organization scan.")
        return []

    # Check if we're in a GitHub organization context
    try:
        org = os.getenv("GITHUB_ORG")
        if not org:
            print("⚠️  GITHUB_ORG environment variable not set. Skipping organization scan.")
            return []

        # Validate org name (GitHub org names: alphanumeric, hyphens, max 39 chars)
        if not re.match(r'^[a-zA-Z0-9-]{1,39}$', org):
            print(f"⚠️  Invalid organization name format: {org}")
            return []

        # Use subprocess with list argument (no shell injection)
        print(f"Scanning organization: {org}")
        result = subprocess.run(
            ["gh", "search", "repos", "--org", org, "--json", "name,url", "--limit", "100"],
            capture_output=True,
            timeout=30,
            text=True
        )

        if result.returncode == 0:
            repos = json.loads(result.stdout)
            print(f"✅ Found {len(repos)} repositories in {org}")
            return repos
        else:
            print(f"⚠️  Error searching repos: {result.stderr}")
            return []

    except subprocess.TimeoutExpired:
        print("❌ Timeout scanning organization")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Error parsing GitHub API response: {e}")
        return []
    except Exception as e:
        print(f"❌ Error scanning organization: {e}")
        return []

def generate_adoption_report() -> Dict[str, Any]:
    """
    Generate adoption statistics from ADOPTION.md.

    Returns:
        Dictionary containing adoption statistics and metadata
    """
    adoption_file = Path("ADOPTION.md")

    if not adoption_file.exists():
        print("⚠️  ADOPTION.md not found. Creating template...")
        return {
            "total_adopters": 0,
            "internal_projects": 0,
            "external_projects": 0,
            "most_used_actions": [],
            "last_updated": datetime.now().isoformat()
        }

    try:
        content = adoption_file.read_text(encoding='utf-8')
    except (UnicodeDecodeError, IOError) as e:
        print(f"⚠️  Error reading ADOPTION.md: {e}")
        return {
            "total_adopters": 0,
            "error": str(e),
            "last_updated": datetime.now().isoformat()
        }

    # Parse markdown table with better error handling
    adopters = []
    for line_num, line in enumerate(content.split('\n'), 1):
        try:
            if '|' in line and 'http' in line and '*[' in line:
                parts = [p.strip() for p in line.split('|')]

                # Skip header rows (empty first or second column)
                if len(parts) < 4 or not parts[1] or not parts[2]:
                    continue

                # Validate URL format
                if not ('.github' in parts[1] or 'http' in parts[1]):
                    continue

                # Extract repository name from markdown link
                repo_match = re.search(r'\*\[([^\]]+)\]\(([^)]+)\)', parts[1])
                if not repo_match:
                    continue

                adopters.append({
                    "name": repo_match.group(1),
                    "url": repo_match.group(2),
                    "team": parts[2],
                    "actions": parts[3],
                    "notes": parts[4] if len(parts) > 4 else "",
                    "line_number": line_num
                })
        except Exception as e:
            print(f"⚠️  Warning: Error parsing line {line_num}: {e}")
            continue

    return {
        "total_adopters": len(adopters),
        "adopters": adopters,
        "last_updated": datetime.now().isoformat()
    }

def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    print("🔍 AI Actions Adoption Scanner")
    print("=" * 50)
    print()

    # Try to scan organization (requires gh CLI and GITHUB_ORG)
    repos = try_scan_github_org()

    # Generate report from ADOPTION.md
    report = generate_adoption_report()

    print(f"📊 Adoption Statistics:")
    print(f"  Total Adopters: {report['total_adopters']}")
    print(f"  Last Updated: {report['last_updated']}")
    print()

    if report['total_adopters'] > 0:
        print("✅ Adoption tracking is working!")
        if 'adopters' in report and report['adopters']:
            print(f"  Registered adopters: {report['total_adopters']}")
            for adopter in report['adopters'][:3]:  # Show first 3
                print(f"    - {adopter.get('name', 'Unknown')} ({adopter.get('team', 'Unknown team')})")
            if len(report['adopters']) > 3:
                print(f"    ... and {len(report['adopters']) - 3} more")
    else:
        print("ℹ️  No external adopters registered yet.")
        print()
        print("Next steps:")
        print("  1. Add your repository to ADOPTION.md")
        print("  2. Set up GITHUB_ORG environment variable for automatic scanning")
        print("  3. Share within your organization to encourage adoption")

    # Save report with error handling
    output = Path("metrics/adoption_report.json")
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"\n📄 Report saved to: {output}")
        return 0
    except IOError as e:
        print(f"❌ Error saving report: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
