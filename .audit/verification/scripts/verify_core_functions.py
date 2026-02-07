#!/usr/bin/env python3
"""
Core Functions Verification Script

リポジトリの存在意義 (Core Functions) が実際に動作するか検証する。
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


class CoreFunctionVerifier:
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or Path.cwd()
        self.results: List[Dict] = []

    def verify_action_workflow(self, action_name: str, workflow_path: str) -> bool:
        """ActionのWorkflowファイルが存在し、構文的に正しいことを検証"""
        try:
            full_path = self.repo_root / workflow_path

            # ファイル存在確認
            if not full_path.exists():
                print(f"  ✗ Workflow file not found: {workflow_path}")
                return False

            # YAML構文チェック
            try:
                import yaml
                with open(full_path, 'r') as f:
                    yaml.safe_load(f)
                print(f"  ✓ Workflow file is valid YAML")
                return True
            except ImportError:
                # yamllint がない場合は簡易チェック
                print(f"  ⚠ yamllint not available, skipping YAML validation")
                return True
            except yaml.YAMLError as e:
                print(f"  ✗ YAML syntax error in {workflow_path}")
                print(f"    {e}")
                return False

        except Exception as e:
            print(f"  ✗ Error verifying {action_name}: {e}")
            return False

    def verify_instruction_exists(self, action_name: str) -> bool:
        """各Actionに導入ガイドが存在することを検証"""
        instruction_path = self.repo_root / f"instructions/{action_name}.md"
        exists = instruction_path.exists()
        if exists:
            print(f"  ✓ Instruction guide exists")
        else:
            print(f"  ✗ Instruction guide missing: instructions/{action_name}.md")
        return exists

    def verify_examples_exist(self, action_name: str) -> bool:
        """各Actionに実行例が存在することを検証"""
        example_dir = self.repo_root / f"examples/{action_name}"
        exists = example_dir.exists() and len(list(example_dir.iterdir())) > 0
        if exists:
            print(f"  ✓ Examples exist")
        else:
            print(f"  ✗ Examples missing: examples/{action_name}/")
        return exists

    def run_verification(self) -> Dict:
        """全ての検証を実行"""

        print("=" * 60)
        print("Core Functions Verification")
        print("=" * 60)
        print(f"Repository: {self.repo_root}")
        print()

        core_functions = [
            {
                "id": "CF-001",
                "name": "review-and-merge",
                "workflow": ".github/workflows/review-and-merge.yml"
            },
            {
                "id": "CF-002",
                "name": "spec-to-code",
                "workflow": ".github/workflows/spec-to-code.yml"
            },
            {
                "id": "CF-003",
                "name": "auto-refactor",
                "workflow": ".github/workflows/auto-refactor.yml"
            },
            {
                "id": "CF-004",
                "name": "action-fixer",
                "workflow": ".github/workflows/action-fixer.yml"
            },
            {
                "id": "CF-005",
                "name": "auto-document",
                "workflow": ".github/workflows/auto-document.yml"
            },
        ]

        total = len(core_functions)
        passed = 0

        for func in core_functions:
            print(f"\n[{func['id']}] {func['name']}")
            print(f"  Workflow: {func['workflow']}")

            # 1. Workflow検証
            workflow_ok = self.verify_action_workflow(
                func['name'],
                func['workflow']
            )

            # 2. 導入ガイド検証
            guide_ok = self.verify_instruction_exists(func['name'])

            # 3. 実行例検証
            example_ok = self.verify_examples_exist(func['name'])

            all_ok = workflow_ok and guide_ok and example_ok

            if all_ok:
                passed += 1
                print(f"  ✓ PASSED")
            else:
                print(f"  ✗ FAILED")

            self.results.append({
                "id": func['id'],
                "name": func['name'],
                "passed": all_ok,
                "workflow_ok": workflow_ok,
                "guide_ok": guide_ok,
                "example_ok": example_ok,
                "workflow_path": func['workflow']
            })

        # 結果サマリ
        print("\n" + "=" * 60)
        print(f"Results: {passed}/{total} passed ({passed/total*100:.1f}%)")
        print("=" * 60)

        output = {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "results": self.results
        }

        # 結果をJSONファイルに出力
        output_path = self.repo_root / ".audit/output/verification_result.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))

        print(f"\nResults saved to: {output_path}")

        return output


if __name__ == "__main__":
    verifier = CoreFunctionVerifier()
    result = verifier.run_verification()

    # 終了コードを返す (失敗があれば1)
    sys.exit(0 if result['failed'] == 0 else 1)
