# PROJECT_DIAGNOSIS

## Executive summary
- 本リポジトリは **単一 FastAPI サービス中心の small monorepo 風構成**（`apps/api` + `deploy` + `scripts` + `docs`）で、CI は `ruff + pytest(coverage>=85) + docker smoke` まで実装済みです。
- 一方で、Codex 自己改善ループの中核 artefact（`AGENTS.md`, `PLANS.md`, `Plan.md`, `.agents/skills`, `docs/improvement/*`）は未導入で、**初回 PR で loop を閉じるための運用ルールが欠落**しています。
- 指定コマンド検証では、`make test` / `make loop-check` は Makefile 不在で実行不能、`python -m compileall -q app charaname_studio tests` は repo root では対象パス不一致、`apps/api` では compile 自体は成功しました。pytest は `httpx` 未導入で失敗、`scripts/doctor.sh` は Docker 未導入で失敗。
- 結論として、**「初回 AGENTS 作成 PR で Plan 更新・skills ログ・checklist・検証まで同梱」自体は可能**ですが、実行前提（コマンド導線、PLANS 優先ルール、defer policy）を docs で先に固定しないと高確率で loop が中断します。

## Repo map

### Top-level
- `apps/api/`: FastAPI アプリ本体と Python テスト。
- `.github/workflows/`: CI/CD（CI, Docker push, Deploy, backlog issue import）。
- `scripts/`: docker context 抽象化ラッパー、doctor、dev 補助。
- `deploy/`: サーバ compose + Caddy + 手順。
- `docs/`: 運用・設計・セットアップ文書。
- `backlog/`: issue import 用のバックログ markdown。

### Repo type
- 物理的には single git repo。
- 構造は「アプリ + インフラ + 運用 docs」を同居させた **single-repo / multi-surface**。

## Tech stack and entrypoints
- Runtime: Python 3.11 想定（`apps/api/pyproject.toml` の `target-version = "py311"`）。
- App framework: FastAPI + Uvicorn。
- Lint/Test: Ruff, Pytest, Pytest-cov。
- Container: Docker, Docker Compose。
- CI/CD: GitHub Actions。

### Entrypoints
- API app: `apps/api/app/main.py` (`app = FastAPI()`)
- API routes: `/health`, `/version`, `/dev`, `/`
- Container command: `uvicorn app.main:app --host 0.0.0.0 --port 8080`（compose / Dockerfile で定義）

## How to run / build / test / lint / typecheck

### Documented commands (current)
- Run: `docker compose up --build`（`README.md`, `docs/usage.md`）
- Lint/Test (apps/api):
  - `ruff check .`
  - `pytest -q --cov=app --cov-report=term-missing --cov-fail-under=85`

### Required command checks (this diagnosis)
1. `make test`
   - 結果: 失敗（`No rule to make target 'test'`）
   - 分類: **missing instructions / missing docs**（実質は build tool 定義欠落）
   - 根因: Makefile 自体が存在しない。
2. `python -m compileall -q app charaname_studio tests`（repo root）
   - 結果: 終了コード 0 だが `Can't list 'app'` 等の警告。
   - 分類: **code/config inconsistency**（指定パスが現行 repo layout と不整合）
3. `make loop-check`
   - 結果: 失敗（`No rule to make target 'loop-check'`）
   - 分類: **missing instructions / missing docs**

### Additional safe checks
- `python -m compileall -q app tests`（`apps/api` で実行）: 成功
- `python -m ruff check .`（`apps/api`）: 成功
- `python -m pytest -q`（`apps/api`）: `httpx` 未導入で失敗
  - 分類: **environment/setup issue**
- `bash scripts/doctor.sh`: Docker コマンド未導入で失敗
  - 分類: **environment/setup issue**

## Architecture snapshot
- 単一サービス API が JSON endpoint (`/health`, `/version`) と HTML Dev Portal (`/dev`) を提供。
- Dev Portal 内の JS が同 origin で `/health` `/version` を fetch。
- 設定は env var 由来（`PORT`, `GIT_SHA`, `BUILD_TIME`, `APP_ENV`）。
- デプロイは GHCR push → optional SSH deploy（secrets gating）で構成。

## Current quality gates

### In CI
- Shell script syntax check (`bash -n scripts/*.sh`)
- Ruff check
- Pytest + coverage threshold (85)
- Docker build/run/curl smoke test

### Missing/weak gates
- `typecheck`（mypy/pyright 等）は未定義
- `format` の公式コマンド未定義
- loop-check 相当の「運用 artefact 完整性検証」未定義

## Loop closure gaps
1. `AGENTS.md` が未配置（root / nested ともに無し）
2. `PLANS.md` / `Plan.md` が未配置
3. `.agents/skills` が未配置
4. `docs/improvement/skills.md` が未配置
5. `docs/improvement/loop_requirements_checklist.md` が未配置
6. `make test`, `make loop-check` 導線未提供
7. 「validation rerun / defer policy」の明文化なし

## Risk hotspots
- **運用 docs の期待コマンドと実際の実行可能性のズレ**: repo root での検証コマンドが不整合。
- **環境依存が強い入口**: Docker 未導入だと `scripts/doctor.sh` で止まる。
- **Python version drift**: CI は 3.11、ローカル実行は 3.10 になりやすく再現差分の温床。
- **docs 肥大化と鮮度劣化リスク**: `docs/phase1_issue_checklist_prompts.md` が巨大で、現在のコード範囲外の項目も多い。

## Documentation audit

### Good
- README / usage / operations / architecture / deploy が揃い、Phase1 の操作導線は比較的明確。
- Docker host portability の設計意図がドキュメント化されている。

### Gaps
- onboarding を 1 本化した「最短導線（5分起動 + 検証）」がない。
- loop 導入 docs（PLANS first rule, Plan update protocol, defer rule）がない。
- `docs/improvement/*` を置くディレクトリ構造が未作成。

## AGENTS / PLANS / skills audit
- `AGENTS.md`: 未検出
- nested AGENTS: 未検出
- `PLANS.md`: 未検出
- `Plan.md`: 未検出
- `.agents/skills`: 未検出
- 判断: Codex運用の最小 map と task protocol が未定義で、自己改善ループ開始前状態。

## Readiness scorecard (0-5)
- build reproducibility: **3/5**（Docker中心で再現しやすいが、ローカル Python 版差分あり）
- testability: **3/5**（CIは明確、ローカルは依存不足時の導線不足）
- doc quality: **3/5**（量は十分、loop運用面が欠落）
- observability: **2/5**（`/health` `/version` の基本のみ）
- skillability: **2/5**（反復作業はあるが skill 管理構造未導入）
- automation readiness: **3/5**（CI/CDあり、運用 automation は限定的）
- loop closure readiness: **1/5**（必要 artefact 群が未配置）

## Evidence appendix

### Inspected files
- `README.md`
- `docs/architecture.md`, `docs/usage.md`, `docs/operations.md`, `docs/local-dev-ubuntu24-docker.md`, `docs/docker-host-portability.md`
- `.github/workflows/ci.yml`, `docker.yml`, `deploy.yml`, `backlog-issue-import.yml`
- `apps/api/app/main.py`, `apps/api/app/settings.py`
- `apps/api/tests/*.py`, `apps/api/pyproject.toml`, `requirements*.txt`
- `scripts/*.sh`, `docker-compose.yml`, `deploy/README.md`, `.env.example`

### Executed commands
- `make test`
- `python -m compileall -q app charaname_studio tests` (repo root)
- `make loop-check`
- `python --version && pip --version`
- `python -m compileall -q app tests` (apps/api)
- `python -m pytest -q` (apps/api)
- `python -m ruff check .` (apps/api)
- `bash scripts/doctor.sh`
- `rg --files` / `rg -n` / `find` / `sed`

### Key outputs
- `make test`: `No rule to make target 'test'`
- `make loop-check`: `No rule to make target 'loop-check'`
- root compileall: `Can't list 'app'`, `Can't list 'charaname_studio'`, `Can't list 'tests'`
- pytest: `starlette.testclient module requires the httpx package`
- doctor: `docker コマンドが見つかりません`

### Unresolved unknowns
- 実開発者環境で Python 3.11 + deps が標準化済みか
- `make` ベース運用を今後導入する意思があるか
- `Plan.md` の保管場所（root固定か docs 配下か）の組織合意
