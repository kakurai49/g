# 1. Executive summary
- What this repository is: 単一の FastAPI サービスを中心に、Docker/Compose 実行・GH Actions CI/CD・最小運用スクリプトを同梱した小規模リポジトリ（軽量モノレポ風）である。**(Confirmed by code + config/scripts/tests)**
- Primary purpose: iPhone Safari で `/dev` を開いて、`/health` と `/version` の生存確認を行う「観測用MVP」を提供すること。**(Confirmed by code, Stated only in docs)**
- Intended users/operators: 開発者・運用者（Docker/GitHub Actions/SSH デプロイを扱える人）。エンドユーザー向け機能は見当たらない。**(Inferred from structure + docs)**
- Current maturity level: **partial implementation**。
- Bottom-line verdict: **runnable now**（ローカル Docker 実行とテストは成立）。ただし「実用的な業務機能」はほぼ未実装。**(Confirmed by code + config/scripts/tests, Uncertain for production runtime)**
- Confidence level: **中〜高（0.79）**。理由: API 実装・テスト・CI・Docker 周辺は実ファイルで裏付け済み。一方で本番デプロイ/Secrets 前提部分はこの調査では実環境未検証。

# 2. What this repository is trying to do
- apparent product/system/service:
  - FastAPI で `/health`, `/version`, `/dev`, `/` を提供する「運用確認用API + Dev Portal」。**(Confirmed by code)**
- business/technical problem:
  - 「ローカル開発環境なしでも、iPhone からデプロイ先の生存とバージョンを即確認したい」という運用上の可観測性課題に対処。**(Stated only in docs, Confirmed partially by code)**
- primary workflows:
  1. ローカルまたはサーバで起動。
  2. `/dev` にアクセス。
  3. フロント内 JS が `/health` `/version` を fetch。
  4. JSON を画面表示し生存確認。**(Confirmed by code + config/scripts/tests)**
- in-scope:
  - ヘルス/バージョン返却、簡易 HTML ポータル、Docker 化、CI/CD 基盤。
- out-of-scope:
  - 認証、DB 永続化、業務ドメインロジック、非同期処理、監査ログ、高度監視。**(Confirmed by absence in code, Inferred from structure)**

# 3. Repository map
- top-level
  - `apps/api/`（最重要）: 実行アプリ本体とテスト。
  - `.github/workflows/`（重要）: CI・Docker push・SSH deploy・backlog import。
  - `scripts/`（重要）: 起動補助/診断/ループ整合チェック。
  - `deploy/`（重要）: サーバ compose と Caddy テンプレート。
  - `docs/`（重要だが非権威）: 運用手順・設計メモ・改善ログ。
  - `backlog/`（補助）: issue 化用 Markdown。
- likely entrypoints
  - 実行: `apps/api/app/main.py`, `docker-compose.yml`, `apps/api/Dockerfile`
  - 検証: `Makefile`, `scripts/loop_check.py`, `apps/api/tests/*`
- infra/dev only
  - `scripts/dev-*.sh`, `scripts/doctor.sh`, `.github/workflows/*`, `deploy/*`
- dead/legacy/placeholder suspicion
  - 明確な「廃止」マーカーは少ないが、`backlog/phase1_issue_pack.md` は運用補助で実行系ではない。
  - `charaname_studio` パッケージは `__init__.py` のみで機能実体なし（compileall 対応痕跡に見える）。**(Confirmed by code, Inferred from structure)**

# 4. Architecture overview
- major modules/components
  1. FastAPI app (`app/main.py`)。
  2. Settings loader (`app/settings.py`)。
  3. Pytest suite (`tests/`)。
  4. Container/runtime definitions (`Dockerfile`, `docker-compose*.yml`)。
  5. CI/CD (`.github/workflows/*.yml`)。
- responsibility split
  - `main.py`: ルーティング + HTML組み立て + minimal business logic。
  - `settings.py`: env 読み込み・キャッシュ。
  - tests: endpoint/設定/HTML要素の回帰検証。
  - workflows: lint/test/smoke/build/deploy。
- runtime pieces
  - Uvicorn + FastAPI。
  - Browser fetch (same-origin) for `/dev` page。
- external dependencies/services
  - Python libs: `fastapi`, `uvicorn`, dev deps (`pytest`, `ruff`, `httpx`, etc.)。
  - GHCR (image registry), SSH target host (deploy), optional Caddy。
- data stores
  - なし（DB 未導入）。**(Confirmed by code)**
- queues/events/schedulers
  - なし。
- frontend/backend split
  - フロントは `/dev` HTML 内インライン JS。別SPAなし。
- internal layering
  - 単層に近い。API層 + 設定層のみで service/repository 層分離なし。**(Confirmed by code)**

# 5. Core execution flows
## Flow A: health/version API 応答
- trigger/input: `GET /health` または `GET /version`。
- main files/functions/classes: `app.main.health`, `app.main.version`, `app.settings.get_settings`。
- sequence:
  1. endpoint が `get_settings()` 呼び出し。
  2. env から読み込まれた設定（またはキャッシュ）を取得。
  3. JSON payload を返却。
- validation/transformation:
  - `PORT` は `int()` 変換。
  - `build_time` は存在時のみ出力。
- persistence/external calls: なし。
- outputs/side effects: JSONレスポンスのみ。
- logging/metrics/error handling: 明示ログ/メトリクスなし、例外処理最小。
- weak points:
  - `PORT` が数値以外だと `int()` で起動時/実行時エラー化し得る。
  - ヘルスチェックは app 固定で依存先を監視しない。
- confidence: 高。**(Confirmed by code + tests)**

## Flow B: Dev Portal 描画とブラウザ内 fetch
- trigger/input: `GET /dev`。
- main files: `app.main.dev_portal`。
- sequence:
  1. サーバがHTML文字列を生成。
  2. ブラウザがJS `loadHealth/loadVersion` を実行。
  3. `/health` `/version` を fetch。
  4. 成功時 `<pre>` にJSON整形表示、失敗時エラーメッセージ表示。
- validation/transformation:
  - `response.ok` 判定のみ。
- persistence/external calls:
  - 外部通信なし（同一サービス内 fetch）。
- outputs/side effects:
  - ブラウザ画面に運用情報表示。
- logging/metrics/error handling:
  - クライアント側エラーメッセージのみ。サーバ側ログ強化なし。
- weak points:
  - 認証なしで `/dev` 公開される。
  - HTMLがインライン文字列で保守性低。
- confidence: 高。**(Confirmed by code + tests)**

## Flow C: CI→Docker smoke→(条件付き)deploy
- trigger/input: push/PR。
- main files: `.github/workflows/ci.yml`, `docker.yml`, `deploy.yml`。
- sequence:
  1. CIで shell syntax, Python lint/test。
  2. docker-smoke で image build→container起動→curl health/version/dev。
  3. main push で docker image push。
  4. secrets があれば deploy job が SSH/SCP で更新。
- validation/transformation:
  - pytest coverage gate 85%。
  - curl retry。
- persistence/external calls:
  - GHCR push、SSH先サーバ操作。
- outputs/side effects:
  - CI pass/fail、イメージ公開、サーバ更新。
- logging/metrics/error handling:
  - Actionsログのみ。
- weak points:
  - deploy は secrets 前提でこの調査では未実証。
  - release/versioning 戦略は簡易。
- confidence: 中。**(Confirmed by config/scripts/tests, Uncertain / requires runtime verification)**

# 6. Feature inventory
| Feature / capability | Evidence | Status | Why this status | Confidence | How to verify |
|---|---|---|---|---|---|
| `GET /health` | `apps/api/app/main.py`, `apps/api/tests/test_health.py` | implemented | 実装とテストが一致 | High | `curl http://localhost:8080/health` |
| `GET /version` | `apps/api/app/main.py`, `apps/api/tests/test_version.py` | implemented | build_time 条件分岐までテスト済み | High | `curl http://localhost:8080/version` |
| `GET /dev` Dev Portal | `apps/api/app/main.py`, `apps/api/tests/test_dev_portal.py` | mostly implemented | 表示と fetch あり。認証やテンプレート分離なし | High | ブラウザで `/dev` を開く |
| Root redirect `/ -> /dev` | `apps/api/app/main.py`, `apps/api/tests/test_dev_portal.py` | implemented | リダイレクト検証あり | High | `curl -I http://localhost:8080/` |
| Settings env load/cache | `apps/api/app/settings.py`, `apps/api/tests/test_settings.py` | implemented | 既定値/上書き値を検証 | High | pytest 実行 |
| Local Docker起動 | `docker-compose.yml`, `apps/api/Dockerfile` | mostly implemented | compose定義あり。実ホスト差分は未検証 | Medium | `docker compose up --build` |
| CI lint/test/smoke | `.github/workflows/ci.yml` | implemented | ジョブ定義は具体的 | Medium | GitHub Actions run |
| GHCR image push | `.github/workflows/docker.yml` | implemented | build/push steps 明示 | Medium | main push で action確認 |
| SSH deploy | `.github/workflows/deploy.yml`, `deploy/*` | partial | 設定はあるが secrets/接続先依存、未検証 | Medium-Low | secrets設定後に dispatch |
| DB-backed business feature | 全体検索でDB/migration不在 | planned/doc-only ではなく out-of-scope | 実装/設計痕跡がほぼ無い | High | `rg -n "sql|alembic|migration|database"` |
| ループ検証プロトコル | `Makefile`, `scripts/loop_check.py`, `AGENTS.md` | implemented | required 3コマンド運用が定義 | High | `make loop-check` |

# 7. Runability assessment
- likely local startup commands
  - `docker compose up --build`（repo root）。
  - 代替: `cd apps/api && uvicorn app.main:app --host 0.0.0.0 --port 8080`。
- likely production/deployment entrypoints
  - GH Actions `docker.yml` + `deploy.yml`。
  - サーバ手動: `deploy/docker-compose.server.yml`。
- package/build toolchain
  - Python 3.11, pip, FastAPI/Uvicorn, pytest/ruff。
- required services
  - ローカルは Docker のみでも可。
  - deploy は SSH 到達可能サーバ + Docker + (任意)Caddy。
- required env vars/secrets
  - 実行時: `PORT`, `GIT_SHA`, `APP_ENV`, optional `BUILD_TIME`。
  - deploy: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY` 等。
- required datasets/assets/models
  - なし。
- docker/compose/devcontainer/nix/make/task support
  - Docker/Compose/Make はあり。
  - devcontainer/nix/taskfile は見当たらない。
- database migration story
  - 存在しない（DB層なし）。
- seed/bootstrap story
  - `.env.example` のみ。seed dataなし。
- what probably works immediately
  - endpoint応答、`/dev` 表示、pytest 実行、loop-check。
- what likely fails immediately
  - Python直実行は依存未導入環境で失敗し得る（`httpx` 等）。
  - deploy は secrets未設定で job skip（失敗ではない）。
- what might fail later at runtime
  - `/dev` 公開による情報露出。
  - `PORT` 不正値で設定変換失敗。
  - サーバ compose の GHCR private pull 認証失敗。**(Uncertain / requires runtime verification)**

# 8. Testing and reliability
- tests existence/shape
  - pytest 4ファイル、主にAPIレスポンスと設定読み込み。
- coverage patterns
  - ルーティング/設定には直接的。統合E2Eや負荷はなし。
- CI/CD evidence
  - ruff, pytest with coverage gate, docker smoke が定義。
- lint/typecheck/build gates
  - Ruff gateあり。mypy/pyright 等の型チェックはなし。
- observability hooks
  - 構造化ログ/メトリクス/トレーシングなし。
- reliability risks
  - 可観測性不足、`/dev` 無保護、ヘルスが依存先非監視。
- mismatch between tested paths and actual core flows
  - `/dev` のHTML文字列と fetch 断片はテストされるが、実ブラウザでの動作保証は限定的。
  - deploy フローはリポジトリ内テストなし。**(Confirmed by config/scripts/tests + Uncertain runtime)**

# 9. Gaps, risks, and incompleteness
- TODO/FIXME/HACK markers
  - 明示マーカーはほぼ無し（`rg` で顕著な該当なし）。
- placeholder implementations
  - `apps/api/charaname_studio/__init__.py` が空に近く機能実体なし。
- dead code
  - 断定できる dead code は少ないが、将来拡張用と見られる最小パッケージが存在。
- feature flags hiding incomplete work
  - 明示フラグなし。
- missing docs for critical setup
  - docs は比較的揃うが、production hardening 手順は薄い。
- missing env examples
  - `.env.example` あり（最小）。
- missing migrations/sample data
  - DBを使わないため該当なし。
- broken references
  - docsは `.env.example` を参照し実在。大きな破断は未検出。
- docs/code mismatch
  - docs は「将来 `/dev` 保護予定」と明記、コード上は未実装（意図的未完了）。
  - docsで iPhone-first を強調するが、iPhone 固有処理はなく一般Web挙動。
- abandoned subtrees
  - `backlog/` は運用用で実行と分離、放棄とは断定不可。
- missing production-hardening elements
  - 認証、rate limit、structured logging、監視、依存先ヘルス、リトライ方針、SLO/SLA、設定検証強化が不足。

# 10. Practical verdict
- Can this repo run today?
  - **はい（ローカル実行は可能）**。Dockerまたは適切なPython依存導入で起動可能。
- What can it do today?
  - `/health` `/version` `/dev` を提供し、最小CI/CDでビルド・スモーク・配布準備まで実施できる。
- What can it definitely not do yet?
  - 実業務向けAPI/DB処理、認証付き管理UI、堅牢な運用監視。
- Top blockers
  1. 機能スコープが観測MVP止まり。
  2. 本番運用ハードニング不足。
  3. deployフローの実地検証証跡不足。
- Shortest path to getting value
  - 監視用エンドポイント公開サービスとして利用し、CI/CD雛形として再利用する。
- Shortest path to making it genuinely usable
  1. 具体的ドメイン機能（1ユースケース）を追加。
  2. DB/migration と認証導入。
  3. `/dev` 制限（認証/IP制限）。
  4. 構造化ログ・メトリクス・アラート。
  5. deploy のステージング実証を CI に組み込む。

Runtime checks still needed:
- 実際の `docker compose up --build` 後に `/dev` が期待どおり動くか（この調査ではコード中心確認）。
- GH Actions `docker.yml` と `deploy.yml` が target 環境で成功するか。
- Caddy 経由 HTTPS 配備時のヘッダ/証明書動作。

# 11. Evidence appendix
- `apps/api/app/main.py` — API/Dev Portal の中核実装（purpose, architecture, execution）。
- `apps/api/app/settings.py` — env 読み込みとキャッシュ（execution, runability）。
- `apps/api/tests/test_health.py` — `/health` 契約確認（testing）。
- `apps/api/tests/test_version.py` — `/version` と build_time 条件確認（testing）。
- `apps/api/tests/test_dev_portal.py` — `/dev` と root redirect の最小保証（testing）。
- `apps/api/tests/test_settings.py` — 設定既定値/環境値検証（testing, runability）。
- `apps/api/Dockerfile` — コンテナ実行条件（runability, deployment）。
- `docker-compose.yml` — ローカル起動定義（runability）。
- `deploy/docker-compose.server.yml` — サーバ起動定義（runability, deployment）。
- `.github/workflows/ci.yml` — lint/test/smoke の品質ゲート（testing, reliability）。
- `.github/workflows/docker.yml` — GHCR publish（deployment readiness）。
- `.github/workflows/deploy.yml` — 条件付き SSH deploy（deployment）。
- `scripts/doctor.sh` — 環境前提チェック（runability）。
- `Makefile` + `scripts/loop_check.py` — ループ検証の強制（process reliability）。
- `README.md`, `docs/architecture.md`, `docs/operations.md`, `docs/usage.md` — 目的と運用主張（docs claims, mismatch checks）。

Useful verification commands:
- `docker compose up --build`
- `curl -sS http://localhost:8080/health | jq .`
- `curl -sS http://localhost:8080/version | jq .`
- `curl -sS http://localhost:8080/dev | head -n 40`
- `cd apps/api && pytest -q --cov=app --cov-report=term-missing --cov-fail-under=85`
- `make loop-check`
- `rg -n "TODO|FIXME|HACK|stub|placeholder|alembic|migration|database"`

FINAL VERDICT:
- Repo type: FastAPI + Docker + GitHub Actions の運用観測MVPリポジトリ
- Current state: partial implementation
- Runs today?: runnable now（ローカル）
- Main value today: デプロイ先生存確認用の最小API/PortalとCI/CD雛形
- Main blocker: ドメイン機能と本番ハードニングの不足
- Recommended next action: 1つの実業務ユースケースをDB/認証付きで縦に実装し、stagingでdeploy実証を追加
