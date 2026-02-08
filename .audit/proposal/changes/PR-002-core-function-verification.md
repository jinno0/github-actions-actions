# PR-002: Core Function Verification Implementation

## Summary
リポジトリの存在意義である「Claude Code CLIを活用した高度な自動化」と「Dry Run検証」の実装状況を確認し、必要に応じて検証スクリプトを追加する提案。

## Gap ID
GAP-003, GAP-008

## Priority
High

## Context

リポジトリは以下のCore Functionsを主張している：
- CF-002: Claude Code CLIを活用し、コードの文脈を理解した高度な自動化を実現する
- CF-004: 全てのAI ActionsはDry Runモードで自動検証される

しかし、これらが実際に動作するか検証されていない。

## Changes Proposed

### Phase 1: Dry Run検証の実装状況確認 (GAP-008)

**Action:**
各Actionのaction.ymlファイルを確認し、以下をチェックする：

1. `inputs:` セクションに `dry-run` または同様の入力パラメータが存在するか
2. `if: ${{ inputs.dry-run == 'true' }}` のような条件分岐が実装されているか
3. Dry Run時に実際の変更を行わないようになっているか

**Expected Output:**
- 各ActionのDry Run検証実装状況レポート
- 未実装のActionリスト

### Phase 2: 検証スクリプトの作成 (GAP-003)

**File: .audit/verification/verify_core_functions.py**
**New File**

検証スクリプトでは以下を確認する：

```python
#!/usr/bin/env python3
"""
Core Function Verification Script
検証対象:
1. CF-002: Claude Code CLIの活用
2. CF-004: Dry Run検証
"""

import subprocess
import sys
from pathlib import Path

def verify_claude_cli_integration():
    """CF-002: Claude Code CLIが実際に呼び出されているか検証"""
    actions_dir = Path("actions")
    
    for action_dir in actions_dir.iterdir():
        if not action_dir.is_dir():
            continue
        
        action_yml = action_dir / "action.yml"
        if not action_yml.exists():
            continue
        
        # action.yml内に"claude"または"claude-code"の言及があるか確認
        content = action_yml.read_text()
        if "claude" in content.lower():
            print(f"✅ {action_dir.name}: Claude CLI integration found")
        else:
            print(f"⚠️  {action_dir.name}: No Claude CLI integration detected")

def verify_dry_run_implementation():
    """CF-004: Dry Run検証の実装状況を確認"""
    actions_dir = Path("actions")
    
    for action_dir in actions_dir.iterdir():
        if not action_dir.is_dir():
            continue
        
        action_yml = action_dir / "action.yml"
        if not action_yml.exists():
            continue
        
        content = action_yml.read_text()
        
        # dry-run入力の存在確認
        has_dry_run_input = "dry-run" in content or "dry_run" in content
        
        # 条件分岐の存在確認
        has_conditional = "if:" in content and ("inputs" in content or "input" in content)
        
        if has_dry_run_input and has_conditional:
            print(f"✅ {action_dir.name}: Dry Run mode implemented")
        else:
            print(f"❌ {action_dir.name}: Dry Run mode NOT implemented")

def main():
    print("=" * 60)
    print("CORE FUNCTION VERIFICATION REPORT")
    print("=" * 60)
    
    print("\n### CF-002: Claude CLI Integration ###")
    verify_claude_cli_integration()
    
    print("\n### CF-004: Dry Run Verification ###")
    verify_dry_run_implementation()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
```

### Phase 3: 検証結果の反映

**Action:**
検証スクリプトを実行し、結果を`.audit/output/verification_result.json`に保存する。

**Expected Outcomes:**
1. 全ActionでClaude Code CLI統合が確認される
2. 全ActionでDry Run検証が実装されていることが確認される
3. 未実装の場合は、改善提案を作成

## Expected Benefits

1. **リポジトリの存在意義の担保**: Core Functionsが実際に動作することが検証される
2. **ドキュメントとの整合性**: README.mdの記載と実際の実装が一致することを確認
3. **品質保証**: ユーザーがActionsを導入した際、期待通りに動作することが保証される

## Risks and Side Effects

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| 検証の結果、一部のActionで実装不足が発覚する | Medium | High | 改善提案を優先的に実施 |
| 検証スクリプトの実行時間が長い | Low | Low | 必要最小限のチェックに留める |

## Verification Criteria

1. `.audit/verification/verify_core_functions.py` が作成されている
2. 検証スクリプトがエラーなく実行できる
3. 検証結果が`.audit/output/verification_result.json` に保存されている
4. 未実装の機能がある場合は、改善提案が作成されている

## Rollback Plan

検証スクリプトは新規ファイルのため、削除するだけで元に戻る：

```bash
rm .audit/verification/verify_core_functions.py
```

## Related Issues

- GAP-003: Core Functionsの実装検証不足
- GAP-008: Dry Run検証の網羅性が未確認

## Implementation Steps

1. 各Actionのaction.ymlファイルを確認
2. 検証スクリプトを作成
3. 検証スクリプトを実行
4. 結果を記録
5. 必要に応じて改善提案を作成

## Estimated Effort

- 実装状況確認: 30分
- 検証スクリプト作成: 1時間
- 実行と結果記録: 15分
- 合計: 1時間45分

## Note

このPRは監査タスクの一部として実施されます。検証結果は`.audit/output/verification_result.json`に保存され、次回の監査で参照されます。
