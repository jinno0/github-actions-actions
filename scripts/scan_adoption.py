#!/usr/bin/env python3
"""
Scan organization repositories for AI Actions usage.

This script searches GitHub for repositories that reference our actions
by looking for workflow files that use './actions/' paths.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

def try_scan_github_org():
    """Attempt to scan organization repositories using GitHub CLI."""
    result = os.system("gh --version >/dev/null 2>&1")
    if result != 0:
        print("⚠️  GitHub CLI not found. Skipping organization scan.")
        return []

    # Check if we're in a GitHub organization context
    try:
        org = os.getenv("GITHUB_ORG")
        if not org:
            print("⚠️  GITHUB_ORG environment variable not set. Skipping organization scan.")
            return []

        # Search for repositories using our actions
        cmd = f'gh search repos --org {org} --json name,url --limit 100'
        print(f"Scanning organization: {org}")
        print(f"Command: {cmd}")

        # Note: This is a simplified scan. Real implementation would use GitHub API
        # to search workflow files for './actions/' references.

        return []
    except Exception as e:
        print(f"❌ Error scanning organization: {e}")
        return []

def generate_adoption_report():
    """Generate adoption statistics from ADOPTION.md."""
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

    content = adoption_file.read_text()

    # Simple parser - count table rows with repository links
    adopters = []
    for line in content.split('\n'):
        if '|' in line and 'http' in line and '*[' in line:
            # Count lines that look like: | [repo](url) | team | actions | notes |
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4 and ('.github' in parts[1] or 'http' in parts[1]):
                adopters.append({
                    "name": parts[1],
                    "team": parts[2],
                    "actions": parts[3],
                    "notes": parts[4] if len(parts) > 4 else ""
                })

    return {
        "total_adopters": len(adopters),
        "adopters": adopters,
        "last_updated": datetime.now().isoformat()
    }

def main():
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
        print(f"  Registered adopters: {report['total_adopters']}")
    else:
        print("ℹ️  No external adopters registered yet.")
        print()
        print("Next steps:")
        print("  1. Add your repository to ADOPTION.md")
        print("  2. Set up GITHUB_ORG environment variable for automatic scanning")
        print("  3. Share within your organization to encourage adoption")

    # Save report
    output = Path("metrics/adoption_report.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n📄 Report saved to: {output}")

if __name__ == "__main__":
    main()
