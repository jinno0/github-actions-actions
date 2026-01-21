---
description: 統合审批屏幕 - QA、Deploy、PR、CodeReviewなど
---

# Approve Command - 統合审批屏幕

承認が必要な操作のための統合UI画面を提供します。

## 使用方法

```bash
/approve [type] [id]
```

## パラメータ

- `type` (必須): 承認タイプ
  - `qa`: QAレビュー承認
  - `deploy`: デプロイ承認
  - `pr`: プルリクエスト承認
  - `code-review`: コードレビュー承認
  - `hotfix`: ホットフィックス承認
  - `release`: リリース承認

- `id` (オプション): 承認対象ID（省略時はリスト表示）

## 実行内容

### 1. 承認画面の起動

```typescript
// Reactコンポーネントで承認画面を起動
const approvalScreen = await ApprovalScreen.launch({
  type: 'deploy',
  id: 'deploy-123'
});
```

### 2. 承認タイプ別のUI

#### QA承認画面
```typescript
interface QAApprovalData {
  id: string;
  title: string;
  description: string;
  testResults: TestResult[];
  coverage: number;
  criticalIssues: number;
  reviewer: string;
  status: 'pending' | 'approved' | 'rejected';
  createdAt: Date;
  deadline?: Date;
}
```

#### デプロイ承認画面
```typescript
interface DeployApprovalData {
  id: string;
  environment: 'staging' | 'production';
  version: string;
  changes: Change[];
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  approvals: Approval[];
  checklist: ChecklistItem[];
  rollbackPlan: string;
  estimatedDowntime: number;
}
```

#### PR承認画面
```typescript
interface PRApprovalData {
  id: string;
  title: string;
  description: string;
  author: string;
  reviewers: Reviewer[];
  changes: FileChange[];
  conflicts: Conflict[];
  checks: StatusCheck[];
  discussion: Comment[];
  mergeable: boolean;
}
```

### 3. 承認フロー

```mermaid
graph TD
    A[/approve実行] --> B{タイプ指定}
    B -->|qa| C[QA承認画面]
    B -->|deploy| D[デプロイ承認画面]
    B -->|pr| E[PR承認画面]
    B -->|省略| F[承認待ちリスト]

    C --> G[詳細情報表示]
    D --> H[リスク評価表示]
    E --> I[変更内容表示]

    G --> J[承認/拒否選択]
    H --> J
    I --> J

    J -->|承認| K[承認処理実行]
    J -->|拒否| L[拒否理由入力]
    J -->|保留| M[コメント追加]

    K --> N[結果通知]
    L --> N
    M --> N
```

## UIコンポーネント構成

### メイン承認画面
ApprovalScreenコンポーネントを作成し、承認タイプに応じたUIを表示する。

### 共通UI要素
- **StatusBadge**: 状態表示
- **RiskIndicator**: リスクレベル表示
- **ApproverAvatar**: 承認者アバター
- **Timeline**: 承認履歴タイムライン
- **CommentSection**: コメントセクション
- **Checklist**: チェックリスト

### レスポンシブデザイン
モバイル用コンパクト表示とデスクトップ用詳細表示を用意する。

## 承認ロジック

### 1. 承認権限チェック
ユーザーの権限、必要なロール、利益相反をチェックすること。

### 2. 承認処理実行
データベース更新、通知送信、後続処理トリガー、ログ記録を行うこと。

### 3. 承認後のアクション
承認タイプに応じた後続処理を実行する:
- `qa`: デプロイパイプライン起動
- `deploy`: デプロイ実行
- `pr`: プルリクエストマージ
- `hotfix`: ホットフィックス適用
- `release`: リリース公開

## 承認リスト表示

### ダッシュボード機能
未処理の承認リストをカード形式で表示する。

### フィルタリング機能
タイプ、ステータス、優先度で承認をフィルタリング・検索できるようにする。

## 通知システム

### 1. 承認要求通知
Slack等で承認要求を通知し、承認ボタンを表示する。

### 2. 承認完了通知
承認者、要求者、関連チームに結果を通知する。

## セキュリティ機能

### 1. 二要素認証
高リスク承認には2FAを必須化すること。

### 2. 承認履歴の追跡
監査証跡として以下を記録する:
- 承認ID、ユーザーID、アクション種別
- タイムスタンプ、IPアドレス、User-Agent
- セッションID

## 統合機能

### 1. 既存システムとの連携
- **QAシステム連携**: テスト結果を承認画面に表示
- **CI/CD連携**: 承認後にデプロイパイプラインを起動

### 2. APIエンドポイント
- `POST /api/approvals/{approval_id}/approve`: 承認処理
- `POST /api/approvals/{approval_id}/reject`: 拒否処理

## 実行例

### QA承認
```bash
/approve qa qa-2024-001

# 期待されるUI:
# ┌─────────────────────────────────────┐
# │ QA承認: v2.1.0 リリーステスト      │
# ├─────────────────────────────────────┤
# │ テストカバレッジ: 92% ✅           │
# │ クリティカル問題: 0件 ✅           │
# │ レビュアー: 山田太郎               │
# │                                     │
# │ [詳細を表示] [承認] [拒否]          │
# └─────────────────────────────────────┘
```

### デプロイ承認
```bash
/approve deploy deploy-123

# 期待されるUI:
# ┌─────────────────────────────────────┐
# │ 本番環境デプロイ承認                │
# │ バージョン: v1.2.3                 │
# │ リスクレベル: 高🔴                 │
# │                                     │
# │ ✓ テスト完了                        │
# │ ✓ ロールバック計画                  │
# │ ⚠ データベース移行を含む           │
# │                                     │
# │ [変更確認] [承認] [拒否]            │
# └─────────────────────────────────────┘
```

### 承認リスト
```bash
/approve

# 期待されるUI:
# ┌─────────────────────────────────────┐
# │ 承認待ち (3件)                      │
# ├─────────────────────────────────────┤
# │ 🔴 高優先度                         │
# │ • 本番デプロイ (deploy-123)         │
# │ • ホットフィックス (hotfix-456)     │
# │                                     │
# │ 🟡 中優先度                         │
# │ • PRレビュー (pr-789)               │
# │                                     │
# │ [全て表示]                          │
# └─────────────────────────────────────┘
```

## 設定

### 環境変数
```bash
# .env
APPROVAL_WEBHOOK_URL=https://hooks.slack.com/...
APPROVAL_2FA_REQUIRED=true
APPROVAL_MAX_PENDING_DAYS=7
APPROVAL_AUTO_REMINDER_HOURS=24
```

### 承認ポリシー設定
```yaml
# approval_config.yml
approval_policies:
  deploy:
    required_approvers: 2
    risk_assessment: true
    two_factor_auth: true

  qa:
    required_approvers: 1
    minimum_coverage: 80
    critical_issues_threshold: 0

  pr:
    required_approvers: 2
    auto_merge: false
    conflict_check: true
```

## 拡張機能

### 1. 承認テンプレート
承認依頼のテンプレート（タイトル、説明、チェックリスト）を用意する。

### 2. 自動承認ルール
低リスク変更、信頼済み担当者、テスト合格等の条件で自動承認できるようにする。

### 3. 承認Analytics
平均承認時間、承認率、ボトルネック分析などのメトリクスを収集する。

## トラブルシューティング

トラブルシューティングは実装時に問題が発生してから追記する。

## 関連ドキュメント

- [DEPLOY.md](../../DEPLOYMENT.md) - デプロイ手順
- [qa_review.md](../../docs/QA_REVIEW_GUIDELINES.md) - QAレビュー基準
- [src/components/approval/](../../src/computer_use_web/src/components/approval/) - UIコンポーネント
- [src/core/approval/](../../src/core/approval/) - バックエンドロジック

---

🤖 このコマンドは統合审批システムによって管理されます。
