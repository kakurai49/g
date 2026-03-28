# skills operation log

## 2026-03-28 — bootstrap loop closure
- Trigger / 課題:
  - 初回自己改善ループ導入時に、必須artefactと検証の同一PR閉塞が未定義。
- Effective workflow / 有効だった手順:
  1. `PLANS.md` を先に定義して `Plan.md` の形式を固定。
  2. ループ土台ファイルを同一PRで追加。
  3. required 3 commands を実行し、結果を `Plan.md` に同期。
  4. checklist で閉塞条件を再確認して最終報告と一致させる。
- Commands used:
  - `make test`
  - `python -m compileall -q app charaname_studio tests` (from `apps/api`)
  - `make loop-check`
- Inputs / Outputs:
  - Input: repo with CI but without loop artifacts.
  - Output: standardized plan protocol + loop-check + operation log.
- Success criteria:
  - 3 required validations pass.
  - `AGENTS.md` 更新と同じPRに `Plan.md` / `skills.md` / checklist が揃う。
- Failure modes:
  - Make target missing.
  - compileall target path mismatch.
  - docs updated but validation log unsynced.
- Reuse signals:
  - PRごとに同じ3コマンドを走らせる。
  - 失敗分類を再利用できる。
- Promote judgment: promote
- Reason:
  - 入出力と成功条件が明確で、以後のPRで繰り返し使えるため。

## 2026-03-28 — repository due diligence execution
- Trigger / 課題:
  - リポジトリの成熟度・実行可能性・未実装領域を、docsを盲信せずコード/設定/テスト起点で監査する必要があった。
- Effective workflow / 有効だった手順:
  1. `README` / `apps/api` / `scripts` / `.github/workflows` を優先して一次証拠を収集。
  2. docs主張とコード実装の一致/不一致を照合。
  3. required validations を実行し、失敗時は分類→修正→再実行を適用。
  4. 最終報告では各結論に evidence label（code/config/docs/inferred/uncertain）を付与する。
- Commands used:
  - `make test`
  - `python -m pip install -r apps/api/requirements.txt -r apps/api/requirements-dev.txt`
  - `cd apps/api && python -m compileall -q app charaname_studio tests`
  - `make loop-check`
  - `rg --files`, `rg -n`, `sed -n`, `cat`
- Inputs / Outputs:
  - Input: FastAPI + Docker + GitHub Actions で構成された small monorepo 風リポジトリ。
  - Output: evidence-backed due diligence report + loop validation logs.
- Success criteria:
  - 主要結論がファイル/コマンドで裏取りされる。
  - required validations 3件が最終的に成功し、失敗時分類と再実行履歴が `Plan.md` に残る。
- Failure modes:
  - ローカル Python 環境で依存不足（今回の `httpx` 欠落）。
  - docs の期待と実装のズレを見落とす。
- Reuse signals:
  - 新規参加者の技術監査、買収DD、継続開発前の現状把握で再利用可能。
- Promote judgment: promote
- Reason:
  - 調査観点と検証手順が定型化でき、再現性の高い監査プロセスとして使えるため。

## 2026-03-28 — core loop documents Japanese translation
- Trigger / 課題:
  - ユーザー要求により `AGENTS.md` / `PLANS.md` / `Plan.md` を日本語化する必要があった。
- Effective workflow / 有効だった手順:
  1. 3ファイルの構造を維持したまま逐次翻訳。
  2. 用語（Goal/Non-goals/Milestones など）は既存運用との互換性を優先して必要箇所を英語のまま維持。
  3. required validations を実行し、環境エラー発生時は stop-and-fix で依存を補完して再実行。
- Commands used:
  - `make test`
  - `python -m pip install -r apps/api/requirements.txt -r apps/api/requirements-dev.txt`
  - `cd apps/api && python -m compileall -q app charaname_studio tests`
  - `make loop-check`
- Inputs / Outputs:
  - Input: 既存英語ベースのループ運用ドキュメント。
  - Output: 日本語化された 3 ファイル + 検証ログ更新。
- Success criteria:
  - 対象3ファイルが日本語として読める。
  - required validations 3件が最終的に成功。
- Failure modes:
  - 開発環境依存（`httpx` 未導入）で `make test` が失敗。
- Reuse signals:
  - 将来の多言語ドキュメント整備 PR で同手順を再利用可能。
- Promote judgment: promote
- Reason:
  - 翻訳作業でもループ規約（検証・ログ）を崩さず適用できることを確認できたため。
