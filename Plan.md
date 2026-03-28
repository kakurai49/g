# Plan.md

## Goal
詳細な技術デューデリジェンス調査を実施し、ループ証跡とともに検証可能なリポジトリ成熟度/実行可能性の結論を記録する。

## Non-goals
- FastAPI エンドポイントの機能開発。
- CI アーキテクチャの再設計。
- 実行時負荷/性能ベンチマーク。

## Milestones

### M1. ループ基盤アーティファクトの追加
- Acceptance criteria:
  - `AGENTS.md`, `PLANS.md`, `Plan.md`, `docs/improvement/skills.md`, `docs/improvement/loop_requirements_checklist.md` が存在し、ループプロセスを相互参照している。
- Validation commands:
  - `make loop-check`
- Status: done

### M2. 再利用可能な検証スキル候補の追加
- Acceptance criteria:
  - `.agents/skills/run-required-validations/SKILL.md` が存在し、トリガー/非トリガー、入出力、ワークフロー、成功/失敗条件を含む。
  - 軽量な eval プロンプトセットが存在する。
- Validation commands:
  - `make loop-check`
- Status: done

### M3. 必須検証の実行とログ同期
- Acceptance criteria:
  - `make test`, `python -m compileall -q app charaname_studio tests`, `make loop-check` を実行済み。
  - 結果がこのファイルと最終レポートに反映されている。
- Validation commands:
  - `make test`
  - `python -m compileall -q app charaname_studio tests`
  - `make loop-check`
- Status: done

### M4. コード一次証跡によるリポジトリデューデリジェンス
- Acceptance criteria:
  - リポジトリの目的、アーキテクチャ、実行フロー、機能状態、実行可能性を具体的なファイル/コマンドで調査する。
  - ドキュメント/コード不一致と、実行時の未確定事項を明示的に特定する。
  - 証跡に基づく結論を持つ構造化された最終レポートを作成する。
- Validation commands:
  - `make test`
  - `cd apps/api && python -m compileall -q app charaname_studio tests`
  - `make loop-check`
- Status: done

## Validation result log
| UTC timestamp | Command | Exit code | Summary | Rerun |
|---|---|---:|---|---|
| 2026-03-28T06:54:11Z | `make test` | 0 | `apps/api` 経由で pytest + カバレッジゲートが成功（8 passed, 100% coverage）。 | no |
| 2026-03-28T06:54:18Z | `cd apps/api && python -m compileall -q app charaname_studio tests` | 0 | compileall は成功終了したが、`Can't list 'charaname_studio'` 警告を出力。 | yes |
| 2026-03-28T06:54:43Z | `cd apps/api && python -m compileall -q app charaname_studio tests` | 0 | `apps/api/charaname_studio/__init__.py` 追加後の再実行で警告が解消。 | no |
| 2026-03-28T06:54:50Z | `make loop-check` | 0 | 必須ループアーティファクトと順序ドキュメントを検出。 | no |
| 2026-03-28T07:16:23Z | `make test` | 2 | 調査前にアクティブな Python 環境で `httpx` 不足により失敗（`starlette.testclient` から `RuntimeError`）。`environment_or_setup_issue` に分類。 | yes |
| 2026-03-28T07:17:02Z | `python -m pip install -r apps/api/requirements.txt -r apps/api/requirements-dev.txt` | 0 | 不足していたテスト/実行時依存（`httpx`, `pytest-cov`, 推移的依存）をインストール。 | no |
| 2026-03-28T07:17:31Z | `make test` | 0 | pytest とカバレッジゲートが成功（8 passed, 100% coverage）。 | no |
| 2026-03-28T07:17:33Z | `cd apps/api && python -m compileall -q app charaname_studio tests` | 0 | compileall が警告なしで成功。 | no |
| 2026-03-28T07:17:35Z | `make loop-check` | 0 | ループアーティファクト整合性チェックが成功。 | no |
| 2026-03-28T07:21:45Z | `make test` | 0 | ドキュメント変更後の再実行が成功（8 passed, 100% coverage）。 | no |
| 2026-03-28T07:21:48Z | `cd apps/api && python -m compileall -q app charaname_studio tests` | 0 | ドキュメント変更後の再実行が成功。 | no |
| 2026-03-28T07:21:51Z | `make loop-check` | 0 | ドキュメント変更後の再実行が成功。 | no |

| 2026-03-28T09:20:41Z | `make test` | 2 | アクティブな Python 環境で `httpx` 不足のため `starlette.testclient` が `RuntimeError` を送出し失敗。`environment_or_setup_issue` に分類。 | yes |
| 2026-03-28T09:21:02Z | `python -m pip install -r apps/api/requirements.txt -r apps/api/requirements-dev.txt` | 0 | 不足依存（`httpx`, `pytest-cov` など）をインストールして環境を修復。 | no |
| 2026-03-28T09:21:31Z | `make test` | 0 | 翻訳変更後の再実行で pytest とカバレッジゲートが成功（8 passed, 100% coverage）。 | no |
| 2026-03-28T09:22:10Z | `cd apps/api && python -m compileall -q app charaname_studio tests` | 0 | 翻訳変更後の compileall が警告なしで成功。 | no |
| 2026-03-28T09:22:25Z | `make loop-check` | 0 | 翻訳変更後の loop-check が成功。 | no |

| 2026-03-28T09:24:40Z | `make test` | 0 | `docs/improvement` 更新後の再実行で pytest とカバレッジゲートが成功（8 passed, 100% coverage）。 | no |
| 2026-03-28T09:24:46Z | `cd apps/api && python -m compileall -q app charaname_studio tests` | 0 | `docs/improvement` 更新後の compileall が成功。 | no |
| 2026-03-28T09:24:52Z | `make loop-check` | 0 | `docs/improvement` 更新後の loop-check が成功。 | no |

## Defer log
- なし。

## Decision log
- 読み取り順序 `AGENTS.md` -> `PLANS.md` -> `Plan.md` 更新を適用。
- 必須検証を実行可能かつ反復可能にするため、ルート `Makefile` と `scripts/loop_check.py` を追加。
- 必須 compileall コマンドで想定パスをクリーンに解決できるよう `apps/api/charaname_studio/__init__.py` を追加。
- 高再利用ワークフロー 1 件（`run-required-validations`）を昇格し、より広いオーケストレーションはドキュメントに残した。
- このループではドキュメントを非権威と見なし、成熟度を結論づける前にコード/テスト/ワークフロー/スクリプトに対して主張を検証した。
- `environment_or_setup_issue` 1 件（ローカル依存セット不足）を解消し、停止して修正ポリシーに従って必須検証を再実行。

## Current status
指定された 3 ファイル（`AGENTS.md`, `PLANS.md`, `Plan.md`）の日本語翻訳を完了し、関連改善ログ更新後も必須検証 3 コマンドが成功。

## Next action
必要に応じて `docs/improvement/` 配下ドキュメントの言語統一方針（英語/日本語）を次 PR で決定する。
