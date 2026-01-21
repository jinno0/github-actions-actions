# Cleanup Scripts

This directory contains utility scripts for maintaining the repository.

## cleanup_temp_files.py

### Purpose
Automatically removes temporary files, old reports, and build artifacts to prevent repository bloat.

### Usage

#### Basic Usage (24-hour default)
```bash
python3 .claude/scripts/cleanup_temp_files.py
```

#### Custom Age Threshold
```bash
# Remove files older than 7 days (168 hours)
python3 .claude/scripts/cleanup_temp_files.py --max-age-hours 168

# Remove files older than 30 days
python3 .claude/scripts/cleanup_temp_files.py --max-age-hours 720
```

#### Dry Run (Recommended First)
```bash
# See what would be deleted without actually deleting
python3 .claude/scripts/cleanup_temp_files.py --dry-run --max-age-hours 168
```

#### Verbose Mode
```bash
# See details about all scanned files
python3 .claude/scripts/cleanup_temp_files.py --verbose
```

### Protected Files
The following files are NEVER deleted:
- Core documentation: `README.md`, `PURPOSE.md`, `SYSTEM_CONSTITUTION.md`, `AGENTS.md`
- Important guides: `API_GUIDE.md`, `INTEGRATION_TESTING_GUIDE.md`, `MAINTENANCE_OPERATIONS_GUIDE.md`
- Project summaries: `IMPLEMENTATION_SUMMARY.md`
- Config files: `package.json`, `tsconfig.json`, `requirements.txt`, `pytest.ini`
- Build configs: `docker-compose.yml`, `.gitignore`

### Temporary File Patterns
The script looks for these patterns (case-sensitive):
- `*_SUMMARY.md`, `*_REPORT.md`, `*_RESULTS.md`
- `*_RECOMMENDATIONS.md`, `*_GUIDE.md` (except protected ones)
- `*_OPERATIONS*.md`, `IMPLEMENTATION_*.md`
- `COMMIT_*.md`, `CLEANUP_*.md`, `MAINTENANCE_*.md`
- `TEST_*.md`, `*_coverage.json`, `*_coverage.xml`
- `coverage*.json`, `test_results*.xml`

### Directories Targeted
- `archive/` - Old archived files
- `logs/` - Log files

### Directories Excluded
- `node_modules/` - npm dependencies
- `.git/` - Git repository
- `.next/` - Next.js build output (but should be in .gitignore)

### Automation (Cron)

#### Weekly Cleanup (Recommended)
Add to crontab (`crontab -e`):
```cron
# Run every Sunday at 2 AM, delete files older than 7 days
0 2 * * 0 cd /path/to/manga-mvv && python3 .claude/scripts/cleanup_temp_files.py --max-age-hours 168 >> /var/log/manga-mvv-cleanup.log 2>&1
```

#### Daily Cleanup (Aggressive)
```cron
# Run every day at 3 AM, delete files older than 3 days
0 3 * * * cd /path/to/manga-mvv && python3 .claude/scripts/cleanup_temp_files.py --max-age-hours 72 >> /var/log/manga-mvv-cleanup.log 2>&1
```

### Safety Tips
1. **Always run with `--dry-run` first** to see what will be deleted
2. **Check the protected files list** before running on a new project
3. **Keep backups** of critical data before aggressive cleanup
4. **Monitor logs** when running via cron to catch issues early

### Exit Codes
- `0` - Success
- `1` - Error (check stderr for details)

### Troubleshooting

#### Script reports "no files deleted"
- Run with `--verbose` to see why files are being skipped
- Check if `--max-age-hours` is too high
- Verify files match temporary patterns

#### Important files were deleted
1. Restore from git: `git checkout HEAD -- <file>`
2. Add file to `PROTECTED_FILES` set in the script
3. Submit issue to improve protected file list

### See Also
- [PROJECT STATUS](../../PROJECT_STATUS.md) - Repository health metrics
- [MAINTENANCE OPERATIONS GUIDE](../../docs/MAINTENANCE_OPERATIONS_GUIDE.md) - Detailed maintenance procedures
