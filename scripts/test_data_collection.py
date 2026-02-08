#!/usr/bin/env python3
"""
テスト用のレビューデータ収集スクリプト

このスクリプトは、AIレビューのデータ収集機能をテストするために
ダミーのレビューデータを生成します。

使用方法:
    python scripts/test_data_collection.py
"""

import json
from datetime import datetime, timedelta
from pathlib import Path


def generate_test_metrics():
    """テスト用のレビューメトリクスを生成 - フラットリスト形式"""

    # 過去30日間のデータを生成
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # calculate_acceptance_rate.py はフラットな配列を期待する
    test_data = [
            {
                "pr_number": 1,
                "repo_id": "test-repo-1",
                "outcome": "approved",
                "suggestions_count": 3,
                "accepted_suggestions": 2,
                "timestamp": (end_date - timedelta(days=1)).strftime("%Y-%m-%dT12:00:00Z"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.85
            },
            {
                "pr_number": 2,
                "repo_id": "test-repo-1",
                "outcome": "modified",
                "suggestions_count": 5,
                "accepted_suggestions": 3,
                "timestamp": (end_date - timedelta(days=2)).strftime("%Y-%m-%dT13:00:00Z"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.75
            },
            {
                "pr_number": 3,
                "repo_id": "test-repo-2",
                "outcome": "approved",
                "suggestions_count": 2,
                "accepted_suggestions": 2,
                "timestamp": (end_date - timedelta(days=3)).strftime("%Y-%m-%dT14:00:00Z"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.90
            },
            {
                "pr_number": 4,
                "repo_id": "test-repo-1",
                "outcome": "rejected",
                "suggestions_count": 4,
                "accepted_suggestions": 0,
                "timestamp": (end_date - timedelta(days=5)).strftime("%Y-%m-%dT15:00:00Z"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.60,
                "rejection_reasons": ["Low quality suggestions"]
            },
            {
                "pr_number": 5,
                "repo_id": "test-repo-2",
                "outcome": "approved",
                "suggestions_count": 6,
                "accepted_suggestions": 5,
                "timestamp": (end_date - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.88
            },
            {
                "pr_number": 6,
                "repo_id": "test-repo-1",
                "outcome": "approved",
                "suggestions_count": 4,
                "accepted_suggestions": 4,
                "timestamp": (end_date - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.92
            },
            {
                "pr_number": 7,
                "repo_id": "test-repo-2",
                "outcome": "modified",
                "suggestions_count": 7,
                "accepted_suggestions": 4,
                "timestamp": (end_date - timedelta(days=12)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.78
            },
            {
                "pr_number": 8,
                "repo_id": "test-repo-1",
                "outcome": "approved",
                "suggestions_count": 3,
                "accepted_suggestions": 3,
                "timestamp": (end_date - timedelta(days=15)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.95
            },
            {
                "pr_number": 9,
                "repo_id": "test-repo-2",
                "outcome": "approved",
                "suggestions_count": 5,
                "accepted_suggestions": 5,
                "timestamp": (end_date - timedelta(days=18)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.87
            },
            {
                "pr_number": 10,
                "repo_id": "test-repo-1",
                "outcome": "modified",
                "suggestions_count": 6,
                "accepted_suggestions": 4,
                "timestamp": (end_date - timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "reviewer": "ai-reviewer",
                "confidence_score": 0.82
            }
    ]

    output_path = Path("metrics/review_metrics.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # フラットな配列として保存
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2)

    # 統計を計算
    total = len(test_data)
    approved = sum(1 for r in test_data if r["outcome"] == "approved")
    modified = sum(1 for r in test_data if r["outcome"] == "modified")
    rejected = sum(1 for r in test_data if r["outcome"] == "rejected")
    acceptance_rate = ((approved + modified) / total * 100) if total > 0 else 0

    print(f"✅ Test metrics generated: {output_path}")
    print(f"   Total reviews: {total}")
    print(f"   Approved: {approved}, Modified: {modified}, Rejected: {rejected}")
    print(f"   Acceptance rate: {acceptance_rate:.1f}%")
    print(f"   Period: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

    return output_path


def main():
    """メイン関数"""
    print("=== Test Data Collection Script ===\n")
    print("Generating test review metrics...")

    try:
        _ = generate_test_metrics()
        print("\n✅ Success!")
        print("\nNext steps:")
        print("  1. Run: python scripts/calculate_acceptance_rate.py --time-period 30d --output report")
        print("  2. Verify the acceptance rate calculation")
        print("  3. Check that the report generates correctly")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
