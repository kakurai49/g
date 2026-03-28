# AGENTS.md

## リポジトリマップ
- `apps/api/`: FastAPI サービス（`app/`）と pytest スイート（`tests/`）。
- `docs/`: アーキテクチャ/運用ガイドと改善ログ。
- `scripts/`: 補助シェル/Python スクリプト。
- `.github/workflows/`: CI/CD 定義。
- `Makefile`: ローカル検証エントリーポイント（`make test`, `make loop-check`）。

## 必須実行順序（ループプロトコル）
1. `AGENTS.md` を読み、その後に **`PLANS.md`** を読む。
2. `PLANS.md` のルールに従って `Plan.md` を作成/更新する。
3. スコープを最小化した変更を実装する。
4. `docs/improvement/skills.md` と `docs/improvement/loop_requirements_checklist.md` を更新する。
5. 必須検証を実行し、結果を `Plan.md` に記録する。

## 必須検証コマンド
- `make test`
- `python -m compileall -q app charaname_studio tests`
- `make loop-check`

期待されるパスが解決されるよう、`python -m compileall -q app charaname_studio tests` は `apps/api/` から実行すること。

## 検証失敗カテゴリ（`Plan.md` への記録必須）
1. `code_or_test_failure`
2. `environment_or_setup_issue`
3. `missing_instructions_or_docs`
4. `code_config_inconsistency`

## 停止して修正 / 保留ルール
- デフォルト: 停止して修正し、同じコマンドを再実行する。
- 保留を許可するのは、この PR で解決できない `environment_or_setup_issue` のみ。
- すべての保留には、`Plan.md` に理由・解除条件・担当者を含めること。

## ループ/ブートストラップ PR の完了定義
`AGENTS.md` を作成/更新する PR は、同じ PR 内で次も更新すること:
- `PLANS.md`
- `Plan.md`
- `docs/improvement/skills.md`
- `docs/improvement/loop_requirements_checklist.md`
- 3 つの必須コマンドの検証ログ
