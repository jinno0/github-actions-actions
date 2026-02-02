#!/usr/bin/env python3
"""
Stepwise Executor Runner - 統合実行コマンド

目標の分解から実行、進捗管理までを一貫して行う統合コマンドです。
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def find_skill_root() -> Path:
    """
    スキルのルートディレクトリを見つける

    Returns:
        スキルのルートディレクトリのパス
    """
    current = Path(__file__).resolve().parent
    # scripts/ の親がスキルルート
    return current.parent


def load_env_file():
    """
    .envファイルから環境変数を読み込む
    """
    current = Path.cwd()
    for _ in range(5):
        env_file = current / ".env"
        if env_file.exists():
            try:
                with open(env_file, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            os.environ.setdefault(key.strip(), value.strip())
                return
            except Exception:
                pass
        parent = current.parent
        if parent == current:
            break
        current = parent


def generate_workflow_id(goal: str) -> str:
    """
    ワークフローIDを生成する

    Args:
        goal: 目標

    Returns:
        ワークフローID（タイムスタンプベース）
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 目標から簡略名を抽出（先頭20文字、英数字とアンダーバーのみ）
    simplified = "".join(c if c.isalnum() or c == "_" else "_" for c in goal[:20])
    return f"{timestamp}_{simplified}"


def run_decompose(goal: str, output: str, skill_root: Path) -> bool:
    """
    目標分解を実行する

    Args:
        goal: 目標
        output: 出力ファイルパス
        skill_root: スキルルートディレクトリ

    Returns:
        成功したかどうか
    """
    script = skill_root / "scripts" / "decompose_goal.py"
    cmd = [sys.executable, str(script), goal, "-o", output]

    print(f"\n🎯 目標を分解中: {goal}")
    print(f"コマンド: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 目標分解に失敗しました: {e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Pythonが見つかりません: {sys.executable}", file=sys.stderr)
        return False


def run_execute(goal_file: str, progress_file: str, skill_root: Path, interactive: bool, resume: bool) -> bool:
    """
    ステップ実行を行う

    Args:
        goal_file: 目標ファイルパス
        progress_file: 進捗ファイルパス
        skill_root: スキルルートディレクトリ
        interactive: インタラクティブモード
        resume: 再開モード

    Returns:
        成功したかどうか
    """
    script = skill_root / "scripts" / "execute_steps.py"
    cmd = [sys.executable, str(script), goal_file, "-p", progress_file]

    if interactive:
        cmd.append("-i")
    if resume:
        cmd.append("--resume")

    print("\n🚀 ステップ実行中...")
    print(f"コマンド: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=False, capture_output=False)
        return True
    except FileNotFoundError:
        print(f"❌ Pythonが見つかりません: {sys.executable}", file=sys.stderr)
        return False


def run_track(progress_file: str, skill_root: Path, export_report: str = None):
    """
    進捗追跡を行う

    Args:
        progress_file: 進捗ファイルパス
        skill_root: スキルルートディレクトリ
        export_report: レポート出力先（オプション）
    """
    script = skill_root / "scripts" / "track_progress.py"
    cmd = [sys.executable, str(script), progress_file]

    if export_report:
        cmd.extend(["-e", export_report])

    print("\n📊 進捗を表示中...")
    print(f"コマンド: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True, capture_output=False)
    except subprocess.CalledProcessError as e:
        print(f"❌ 進捗表示に失敗しました: {e}", file=sys.stderr)
    except FileNotFoundError:
        print(f"❌ Pythonが見つかりません: {sys.executable}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="目標の分解から実行、進捗管理までを一貫して行う統合コマンド"
    )
    parser.add_argument("goal", help="作業目標の説明")

    parser.add_argument(
        "-w",
        "--workflow-id",
        help="ワークフローID（指定しない場合は自動生成）",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="インタラクティブモード（各ステップで入力を求める）",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="既存の進捗から再開する",
    )
    parser.add_argument(
        "--decompose-only",
        action="store_true",
        help="目標分解のみ行う（実行しない）",
    )
    parser.add_argument(
        "--track-only",
        action="store_true",
        help="進捗表示のみ行う",
    )
    parser.add_argument(
        "--no-track",
        action="store_true",
        help="実行後に進捗表示を行わない",
    )
    parser.add_argument(
        "-e",
        "--export-report",
        help="実行後にMarkdownレポートを出力する",
    )

    args = parser.parse_args()

    # .envファイルを読み込み
    load_env_file()

    skill_root = find_skill_root()

    # ワークフローIDの生成
    workflow_id = args.workflow_id or generate_workflow_id(args.goal)

    # ワークフローディレクトリの作成
    workflow_dir = Path.cwd() / ".stepwise" / workflow_id
    workflow_dir.mkdir(parents=True, exist_ok=True)

    goal_file = workflow_dir / "goal.json"
    progress_file = workflow_dir / "progress.json"
    report_file = workflow_dir / "report.md" if args.export_report else args.export_report

    # 進捗表示のみモード
    if args.track_only:
        if not progress_file.exists():
            print(f"❌ 進捗ファイルが見つかりません: {progress_file}", file=sys.stderr)
            sys.exit(1)
        run_track(str(progress_file), skill_root, str(report_file) if report_file else None)
        return

    # 既存の進捗から再開
    if args.resume:
        if not goal_file.exists():
            print(f"❌ 目標ファイルが見つかりません: {goal_file}", file=sys.stderr)
            sys.exit(1)
        if not progress_file.exists():
            print(f"❌ 進捗ファイルが見つかりません: {progress_file}", file=sys.stderr)
            sys.exit(1)
        run_execute(str(goal_file), str(progress_file), skill_root, args.interactive, True)
        if not args.no_track:
            run_track(str(progress_file), skill_root, str(report_file) if report_file else None)
        return

    # 目標分解
    if not goal_file.exists():
        success = run_decompose(args.goal, str(goal_file), skill_root)
        if not success:
            sys.exit(1)

        # 目標分解のみモード
        if args.decompose_only:
            print(f"\n✅ 目標分解が完了しました: {goal_file}")
            print(f"次のステップ: python3 {__file__} --resume")
            return
    else:
        print(f"ℹ️  既存の目標ファイルを使用します: {goal_file}")

    # ステップ実行
    run_execute(str(goal_file), str(progress_file), skill_root, args.interactive, False)

    # 進捗表示
    if not args.no_track:
        run_track(str(progress_file), skill_root, str(report_file) if report_file else None)

    print(f"\n📂 ワークフローディレクトリ: {workflow_dir}")
    print(f"進捗の再表示: python3 {__file__} --track-only -w {workflow_id}")


if __name__ == "__main__":
    main()
