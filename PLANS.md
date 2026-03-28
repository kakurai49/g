# PLANS.md

このリポジトリにおける `Plan.md` の運用標準。

## 順序ルール
- `Plan.md` を作成または編集する前に、常にこのファイルを読むこと。

## `Plan.md` の必須セクション
1. Goal
2. Non-goals
3. Milestones（小さく、テスト可能な単位）
4. Acceptance criteria（マイルストーンごと）
5. Validation commands（マイルストーンごと）
6. Status（todo / in_progress / done / deferred）
7. Validation result log（`command`, `exit code`, `summary`, `rerun`）
8. Defer log（`reason`, `unblock condition`, `owner`）
9. Decision log
10. Current status
11. Next action

## マイルストーン粒度
- レビュー可能な変更セットごとに、1 マイルストーンを基本とする。
- 各マイルストーンを独立して検証可能に保つ。

## 検証記載標準
- 正確なコマンド文字列を記録する。
- UTC タイムスタンプと終了コードを記録する。
- 失敗した場合は、停止して修正し、再実行する。

## 停止して修正・再実行
- 必須検証が失敗している間は、次のマイルストーンに進まない。
- 修正後に同じコマンドを再実行し、両方の試行を記録する。

## 保留ポリシー
- 環境/セットアップ制約でブロックされた場合にのみ許可。
- 具体的な解除条件とフォローアップアクションを必ず含める。

## リビングドキュメント原則
- `Plan.md` は意図だけでなく、現在の実態を反映しなければならない。
- 各ループの最後に `Current status` と `Next action` を更新する。
