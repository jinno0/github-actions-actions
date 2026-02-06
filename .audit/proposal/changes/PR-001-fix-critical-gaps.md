# PR-001: Critical Gapsの修正

**関連するギャップ:**
- GAP-001: review-and-merge Actionの例ファイル欠落
- GAP-002: spec-to-code Actionのscripts/ディレクトリ欠落
- GAP-003: action-fixer Actionのscripts/ディレクトリ欠落

**優先度:** Critical
**推定作業時間:** 2-3時間

## 概要

3つのActionで重要なファイルまたはディレクトリが欠落しており、Actionの実行または利用に支障を
出ている。このPRではこれらのCriticalなギャップを修正する。

## 変更内容

### 1. examples/review-and-merge.yml の作成

**ファイル:** `examples/review-and-merge.yml`

**内容:** review-and-merge Actionの使用例ワークフロー

**実装手順:**
1. `examples/` ディレクトリに `review-and-merge.yml` を作成
2. `instructions/review-and-merge.md` の内容を参考にワークフローを記述
3. 必要な入力パラメータ（claude-model, lgtm-threshold, auto-fix等）を設定
4. コメントで各パラメータの説明を追加

**期待される効果:**
- 利用者が `examples/review-and-merge.yml` を `.github/workflows/` にコピーするだけで導入可能になる
- README.md:50-53の「全てのActionには利用例がある」という主張と整合する

**検証方法:**
- 作成した.ymlファイルのYAML構文チェック: `yamllint examples/review-and-merge.yml`
- action.ymlで参照されている全てのinputsが設定されていることを確認

### 2. actions/spec-to-code/scripts/ の調査と修正

**ディレクトリ:** `actions/spec-to-code/scripts/`

**問題:** action.yml内でscripts/を参照しているが、ディレクトリが存在しない

**実装手順:**
1. `actions/spec-to-code/action.yml` を確認し、どのスクリプトファイルを参照しているか調査
2. 以下のいずれかの対応:
   - パターンA: スクリプトが別の場所にある場合 → シンボリックリンクを作成またはaction.ymlのパスを修正
   - パターンB: スクリプト自体が未実装の場合 → スクリプトを作成（他のActionのscripts/を参考）
   - パターンC: composite actionでrunステップに直接コマンドがある場合 → scripts/ディレクトリ不要と判断し、action.ymlを修正
3. spec-to-codeのREADME.mdと整合性が取れていることを確認

**期待される効果:**
- spec-to-code Actionが正常に実行されるようになる
- 「Markdown仕様書からコードを生成できる」という機能が動作する

**検証方法:**
- `actions/spec-to-code/action.yml` のYAML構文チェック
- スクリプトが存在する場合: 実行権限の確認 (`chmod +x scripts/*.sh` など)
- action.ymlの `runs.steps[].with` や `runs.using` の設定値が正しいことを確認

### 3. actions/action-fixer/scripts/ の調査と修正

**ディレクトリ:** `actions/action-fixer/scripts/`

**問題:** action.yml内でscripts/を参照しているが、ディレクトリが存在しない

**実装手順:**
1. `actions/action-fixer/action.yml` を確認し、スクリプトの参照状況を調査
2. spec-to-codeと同様の3パターンのいずれかを判断し対応
3. 必要に応じてYAML検証・修正スクリプトを作成

**期待される効果:**
- action-fixer Actionが正常に実行されるようになる
- 「ワークフローのエラーを検知・修正」という機能が動作する

**検証方法:**
- YAML構文チェック
- スクリプトの実行権限確認
- テストケース `tests/test_action_fixer/` がパスすることを確認

## テスト計画

1. **YAML構文検証**
   ```bash
   yamllint examples/review-and-merge.yml
   yamllint actions/spec-to-code/action.yml
   yamllint actions/action-fixer/action.yml
   ```

2. **Action構造検証**
   ```bash
   pytest tests/integration/test_action_structure.py::TestActionStructure::test_all_actions_have_action_yml -v
   ```

3. **各Actionの個別テスト**
   ```bash
   pytest tests/test_action_fixer/ -v
   pytest tests/test_spec_to_code/ -v
   ```

## ロールバック手順

もし変更により問題が発生した場合:
1. 作成したファイルを削除: `rm examples/review-and-merge.yml`
2. 作成したscripts/を削除: `rm -rf actions/spec-to-code/scripts/ actions/action-fixer/scripts/`
3. 修正したaction.ymlをgit checkoutで戻す: `git checkout actions/*/action.yml`

## リスク評価

- **破壊的変更:** なし（新規ファイル追加、または不足ファイルの追加のみ）
- **副作用:** なし（既存のワークフローに影響しない）
- **依存関係:** なし（他のActionや機能に依存しない）

## 参考資料

- `instructions/review-and-merge.md`
- `instructions/spec-to-code.md`
- `instructions/action-fixer.md`
- `examples/` 内の他のActionの.ymlファイル

## 成功基準

- [ ] examples/review-and-merge.yml が作成され、YAML構文チェックがパスする
- [ ] actions/spec-to-code/scripts/ が存在し、action.ymlとの整合性が取れている
- [ ] actions/action-fixer/scripts/ が存在し、action.ymlとの整合性が取れている
- [ ] 関連するテストケースが全てパスする
- [ ] `.audit/verification/verify_core_functions.py` のCF-001, CF-002, CF-004が全てPASSになる
