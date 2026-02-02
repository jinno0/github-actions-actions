#!/usr/bin/env python3
"""
Goal Decomposer - 作業目標を中間目標に自動分解

Claude APIを使用して、任意の作業目標を実行可能な中間目標（サブゴール）に自動分解します。
分解結果はJSON形式で保存され、execute_steps.pyで使用できます。
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


def load_env_file():
    """
    .envファイルから環境変数を読み込む

    カレントディレクトリまたは親ディレクトリの.envファイルを読み込みます。
    """
    current = Path.cwd()

    # カレントディレクトリと親ディレクトリ（最大3階層）で.envファイルを探す
    # 通常、プロジェクトルートは2-3階層以内にあるため、これで十分
    for _ in range(3):
        env_file = current / ".env"
        if env_file.exists():
            try:
                with open(env_file, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            os.environ.setdefault(key.strip(), value.strip())
                return  # 読み込み成功
            except Exception:
                # 読み込み失敗は無視（別の場所の.envファイルを試す）
                # デバッグ時は以下のコメントを外して詳細を表示可能
                # import warnings
                # warnings.warn(f".env読み込み失敗: {env_file}: {e}")
                pass
        parent = current.parent
        if parent == current:  # ファイルシステムルートに到達
            break
        current = parent


# .envファイルを読み込み（環境変数の自動設定）
load_env_file()


def load_decomposition_strategies(skill_path: Path) -> str:
    """
    分解戦略ドキュメントを読み込む

    Args:
        skill_path: スキルのパス

    Returns:
        分解戦略のテキスト
    """
    strategies_file = skill_path / "references" / "decomposition_strategies.md"
    if strategies_file.exists():
        with open(strategies_file, encoding="utf-8") as f:
            return f.read()
    return ""


def load_goal_patterns(skill_path: Path) -> dict[str, Any]:
    """
    目標パターンを読み込む

    Args:
        skill_path: スキルのパス

    Returns:
        目標パターンの辞書
    """
    patterns_dir = skill_path / "assets" / "goal_patterns"
    patterns = {}

    if patterns_dir.exists():
        for pattern_file in patterns_dir.glob("*.json"):
            with open(pattern_file, encoding="utf-8") as f:
                patterns[pattern_file.stem] = json.load(f)

    return patterns


def create_decomposition_prompt(
    goal: str, strategies: str, patterns: dict[str, Any]
) -> str:
    """
    Claude APIに送信するプロンプトを作成する

    Args:
        goal: ユーザーの目標
        strategies: 分解戦略のテキスト
        patterns: 目標パターンの辞書

    Returns:
        プロンプト文字列
    """
    patterns_info = ""
    if patterns:
        patterns_info = "\n\n## 参考パターン\n\n"
        for name, pattern in patterns.items():
            patterns_info += f"### {name}\n{json.dumps(pattern, ensure_ascii=False, indent=2)}\n\n"

    prompt = f"""あなたは経験豊富なプロジェクトマネージーです。以下の作業目標を実行可能な中間目標（サブゴール）に分解してください。

# 目標
{goal}

# 分解の指針
{strategies}
{patterns_info}
# 出力形式

以下のJSON形式のみで出力してください（マークダウンなどの他のテキストは一切含めないでください）:

{{
  "original_goal": "元の目標",
  "decomposition_strategy": "使用した分解戦略の説明",
  "steps": [
    {{
      "step": 1,
      "title": "ステップのタイトル",
      "description": "具体的な説明（何を、どのように、なぜ）",
      "estimated_effort": "small|medium|large",
      "dependencies": []
    }}
  ]
}}

# 分解の品質基準
- 各ステップは具体的で実行可能であること
- ステップの完了条件が明確であること
- 依存関係が適切に定義されていること
- 推定作業量が現実的であること
- 全体として最終目標を達成できること
- ステップ数は3〜15個程度であること

# estimated_effort の目安
- small: 30分〜2時間
- medium: 2時間〜4時間
- large: 4時間〜1日

それでは、目標を分解してください。JSONのみを出力してください。"""

    return prompt


def decompose_with_claude(prompt: str) -> dict[str, Any]:
    """
    Claude APIを使用して目標を分解する

    Args:
        prompt: プロンプト

    Returns:
        分解結果

    Raises:
        RuntimeError: API呼び出しに失敗した場合
    """
    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "anthropic パッケージがインストールされていません。"
            "pip install anthropic でインストールしてください。"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY 環境変数が設定されていません。"
            ".envファイルに設定してください。"
        )

    client = anthropic.Anthropic(api_key=api_key)

    print("\n🎯 目標を分解中...")

    try:
        # モデルは環境変数から取得（デフォルト: claude-sonnet-4-20250514）
        model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-20250514")
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.content[0].text

        # JSONのみを抽出（マークダウンコードブロックなどが含まれる場合に対応）
        content = content.strip()

        # ```jsonと```を削除
        if content.startswith("```"):
            lines = content.split("\n")
            if lines[0].startswith("```json"):
                lines = lines[1:]  # 最初の```jsonを削除
            elif lines[0].startswith("```"):
                lines = lines[1:]  # 最初の```を削除
            if lines[-1].startswith("```"):
                lines = lines[:-1]  # 最後の```を削除
            content = "\n".join(lines)

        result = json.loads(content)
        return result

    except Exception as e:
        raise RuntimeError(f"Claude API の呼び出しに失敗しました: {e}")


def print_decomposition_summary(result: dict[str, Any]):
    """
    分解結果のサマリーを表示する

    Args:
        result: 分解結果
    """
    print("\n" + "=" * 60)
    print("📋 目標分解サマリー")
    print("=" * 60)

    print(f"\n元の目標: {result['original_goal']}")
    print(f"中間目標数: {len(result['steps'])}")

    if "decomposition_strategy" in result:
        print(f"分解戦略: {result['decomposition_strategy']}")

    print("\n中間目標:")
    for step in result["steps"]:
        deps_str = ""
        if step.get("dependencies"):
            deps_str = f" (依存: {', '.join(map(str, step['dependencies']))})"
        print(
            f"  {step['step']}. {step['title']} [{step['estimated_effort']}]{deps_str}"
        )
        print(f"     {step['description']}")


def save_decomposition(result: dict[str, Any], output_file: str):
    """
    分解結果を保存する

    Args:
        result: 分解結果
        output_file: 出力ファイルパス
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 分解結果を保存しました: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="作業目標をAIで中間目標に自動分解します"
    )
    parser.add_argument("goal", help="作業目標の説明")
    parser.add_argument(
        "-o",
        "--output",
        default="decomposed_goal.json",
        help="出力ファイルパス（デフォルト: decomposed_goal.json）",
    )
    parser.add_argument(
        "--show-only",
        action="store_true",
        help="結果を表示するのみで保存しない（プレビュー用）",
    )

    args = parser.parse_args()

    # スキルのパスを取得
    skill_path = Path(__file__).parent.parent

    # 分解戦略とパターンを読み込み
    strategies = load_decomposition_strategies(skill_path)
    patterns = load_goal_patterns(skill_path)

    # プロンプトを作成
    prompt = create_decomposition_prompt(args.goal, strategies, patterns)

    # Claude APIで分解
    try:
        result = decompose_with_claude(prompt)
    except RuntimeError as e:
        print(f"❌ エラー: {e}", file=sys.stderr)
        sys.exit(1)

    # サマリーを表示
    print_decomposition_summary(result)

    # 保存
    if not args.show_only:
        save_decomposition(result, args.output)
        print(f"\n次のステップ: execute_steps.py {args.output}")
    else:
        print("\n（--show-only モード: ファイルは保存されませんでした）")


if __name__ == "__main__":
    main()
