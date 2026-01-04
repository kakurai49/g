# Phase1 Issue別チェックリスト（手動確認 + 自動確認 + コーテックス実装依頼プロンプト）

更新日: 2026-01-04

## このドキュメントの目的
- Phase1の各Issueについて **「実装チェックリスト」→「手動確認」→「自動確認」** を一枚にまとめる
- 自動確認は、GitHub Actions / pytest などで **回帰を防ぐための検証** を追加する
- 自動確認の実装をAI（コーテックス/Codex）へ依頼できるよう、**コピペ用の詳細プロンプト** を各Issueに付ける

## 前提（iPhone-first）
- 検証の中心は `/dev`（Dev Portal）と `/health` `/version`
- 可能な限り「GitHub → Actions → 自動デプロイ → iPhone Safariで確認」で完結させる

---

## 共通: 環境設定の一次チェック（詰まりポイント潰し）

### A. `.env`（実行時環境変数）
- [ ] `.env.example` をコピーして `.env` を作成
- [ ] `PORT`（既定8080）
- [ ] `GIT_SHA`（既定`unknown`。`/version`表示用）
- [ ] `APP_ENV`（既定`dev`。`/dev`表示用）
- [ ] `BUILD_TIME`（任意。`/version`表示用）
- [ ] **`.env` は compose ファイルと同じディレクトリに配置**（秘密情報はコミットしない）

### B. GitHub Secrets / Variables（自動デプロイを使う場合）
- [ ] 必須: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`
- [ ] 任意: `DEPLOY_PORT`（既定22）, `DEPLOY_PATH`（既定`/opt/g`）
- [ ] GHCRがプライベートの場合: `GHCR_USER`, `GHCR_TOKEN`

### C. ローカル（例外）での最低限の動作確認（PCが使える場合のみ）
- [ ] `docker compose up --build`
- [ ] `http://localhost:8080/dev` を開き、Health/Versionが表示される

### D. デプロイ後の一次確認（iPhone Safari）
- [ ] `https://<domain>/health` が200（JSON）になる
- [ ] `https://<domain>/version` が200で、commit SHAが表示される
- [ ] `https://<domain>/dev` を開き "Dev Portal" と `/health` `/version` のJSONが見える

### E. トラブルシュート（最短で切り分け）
- [ ] `/dev` が白画面: まず `curl`/ブラウザで `/health` `/version` が200か確認（200でなければAPI側/プロキシ）
- [ ] deploy workflowが動かない: secrets設定の有無と `deploy.yml` の `if` 条件を確認
- [ ] `/health` が落ちる: `.env` の `PORT`/`GIT_SHA` とコンテナログを確認

---

## 共通: 自動確認の基本セット（推奨）
- [ ] ruff（lint）
- [ ] pytest（unit/integration）+ coverage>=85
- [ ] docker smoke（compose起動 → `/health` 200）
- [ ] deploy後の外形スモーク（`BASE_URL` を使って `/health` などを確認）※S6-05で確定

---


# S1: iPhone中心の開発・デプロイ観点（GitHub→CI→デプロイ→iPhone確認）

### [P1-S1-01] リポジトリ骨格作成（単一サービス構成で開始）
- Labels: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:chore`

#### Done条件（仕様）
- `apps/api`（FastAPI想定）を作成
- `docker/` と `docker-compose.yml`（サーバ用）を作成
- `README.md`に「デプロイされるURL」「動作確認URL（/health等）」を先に書く

#### 実装チェックリスト
- [ ] `apps/api`（FastAPI想定）を作成
- [ ] `docker/` と `docker-compose.yml`（サーバ用）を作成
- [ ] `README.md`に「デプロイされるURL」「動作確認URL（/health等）」を先に書く

#### 手動確認（マニュアル）
- [ ] GitHub上でREADMEが入口になっていることを確認

#### 自動確認（Automated）
- [ ] CIで `apps/api/` と `deploy/`（または `docker-compose.yml`）の存在チェックを行う（ファイル/ディレクトリ構成の回帰防止）
- [ ] READMEに `/health` `/version` `/dev` の確認URLが含まれているかをCIで検証（簡易grep）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S1-01: リポジトリ骨格作成（単一サービス構成で開始）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `apps/api`（FastAPI想定）を作成
- `docker/` と `docker-compose.yml`（サーバ用）を作成
- `README.md`に「デプロイされるURL」「動作確認URL（/health等）」を先に書く

## 追加する自動確認（やること）
- CIで `apps/api/` と `deploy/`（または `docker-compose.yml`）の存在チェックを行う（ファイル/ディレクトリ構成の回帰防止）
- READMEに `/health` `/version` `/dev` の確認URLが含まれているかをCIで検証（簡易grep）

## 触る可能性が高いファイル（目安）
- scripts/verify_repo_layout.py（新規）
- .github/workflows/ci.yml（verify step追加）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S1-02] Issueテンプレ（Codex貼り付け前提）作成
- Labels: `phase:1`, `S1-devops`, `priority:p1`, `type:chore`

#### Done条件（仕様）
- `.github/ISSUE_TEMPLATE/feature.md` 等を作る
- テンプレに以下を含める
- Context / Scope / Done条件 / iPhone確認方法
- Codex Prompt欄（ここを丸ごと貼る運用）

#### 実装チェックリスト
- [ ] `.github/ISSUE_TEMPLATE/feature.md` 等を作る
- [ ] テンプレに以下を含める
- [ ] Context / Scope / Done条件 / iPhone確認方法
- [ ] Codex Prompt欄（ここを丸ごと貼る運用）

#### 手動確認（マニュアル）
- [ ] iPhoneのGitHubアプリ/ブラウザからIssue作成が楽になっている

#### 自動確認（Automated）
- [ ] CIで `.github/ISSUE_TEMPLATE/` 配下にテンプレが存在し、必須見出し（Context/Scope/Done/iPhone確認/Codex Prompt）が含まれるかを検証

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S1-02: Issueテンプレ（Codex貼り付け前提）作成

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `.github/ISSUE_TEMPLATE/feature.md` 等を作る
- テンプレに以下を含める
- Context / Scope / Done条件 / iPhone確認方法
- Codex Prompt欄（ここを丸ごと貼る運用）

## 追加する自動確認（やること）
- CIで `.github/ISSUE_TEMPLATE/` 配下にテンプレが存在し、必須見出し（Context/Scope/Done/iPhone確認/Codex Prompt）が含まれるかを検証

## 触る可能性が高いファイル（目安）
- scripts/verify_issue_templates.py（新規）
- .github/workflows/ci.yml（verify step追加）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S1-03] GitHub Actions: CI（lint + unit test）を追加
- Labels: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- PR作成でCIが走る
- 少なくとも `python -m compileall` / `pytest` / `ruff`（等）いずれかが動く

#### 実装チェックリスト
- [ ] PR作成でCIが走る
- [ ] 少なくとも `python -m compileall` / `pytest` / `ruff`（等）いずれかが動く

#### 手動確認（マニュアル）
- [ ] PR画面でChecksが緑になること
- [ ] GitHubのActions/Checks画面で対象workflowが成功していることを確認

#### 自動確認（Automated）
- [ ] `ci.yml`で ruff と pytest を実行し、coverage>=85 を強制する
- [ ] `docker compose` を使ったスモークテスト（コンテナ起動→ `/health` が200）をCIに含める

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S1-03: GitHub Actions: CI（lint + unit test）を追加

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- PR作成でCIが走る
- 少なくとも `python -m compileall` / `pytest` / `ruff`（等）いずれかが動く

## 追加する自動確認（やること）
- `ci.yml`で ruff と pytest を実行し、coverage>=85 を強制する
- `docker compose` を使ったスモークテスト（コンテナ起動→ `/health` が200）をCIに含める

## 触る可能性が高いファイル（目安）
- .github/workflows/ci.yml（新規または修正）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S1-04] GitHub Actions: Dockerイメージbuild & push（GHCR）
- Labels: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- mainマージでコンテナイメージがビルドされ、GHCRへpushされる
- タグに `sha` または `semver` を付ける（ロールバックに必要）

#### 実装チェックリスト
- [ ] mainマージでコンテナイメージがビルドされ、GHCRへpushされる
- [ ] タグに `sha` または `semver` を付ける（ロールバックに必要）

#### 手動確認（マニュアル）
- [ ] Actionsログでpush成功を確認（GHCRのPackages一覧でもOK）
- [ ] GitHubのActions/Checks画面で対象workflowが成功していることを確認

#### 自動確認（Automated）
- [ ] `docker.yml`で main マージ時にイメージをビルドし GHCR に push できることをActionsで保証
- [ ] タグに `latest` と `sha-<commit>`（または同等）を付けることをワークフロー内で保証（`GITHUB_SHA`利用）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S1-04: GitHub Actions: Dockerイメージbuild & push（GHCR）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- mainマージでコンテナイメージがビルドされ、GHCRへpushされる
- タグに `sha` または `semver` を付ける（ロールバックに必要）

## 追加する自動確認（やること）
- `docker.yml`で main マージ時にイメージをビルドし GHCR に push できることをActionsで保証
- タグに `latest` と `sha-<commit>`（または同等）を付けることをワークフロー内で保証（`GITHUB_SHA`利用）

## 触る可能性が高いファイル（目安）
- .github/workflows/docker.yml（新規または修正）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S1-05] サーバ側：コンテナ起動の最小セット（DBなしでもOK）を立てる
- Labels: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- サーバで `docker compose up -d` でアプリが立つ（最初はDB無しでも可）
- `/health` が200を返す

#### 実装チェックリスト
- [ ] サーバで `docker compose up -d` でアプリが立つ（最初はDB無しでも可）
- [ ] `/health` が200を返す

#### 手動確認（マニュアル）
- [ ] `https://<your-domain>/health` をSafariで開いてOK
- [ ] iPhone Safariで `https://<domain>/health` が200（JSON表示）になることを確認
- [ ] iPhone Safariで `https://<domain>/dev` を開き、Health/Versionが表示されることを確認

#### 自動確認（Automated）
- [ ] CIで `docker compose up -d` → `curl http://localhost:<port>/health` が200 を確認（docker smoke）
- [ ] composeファイルの静的検証: `docker compose config` が成功すること

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S1-05: サーバ側：コンテナ起動の最小セット（DBなしでもOK）を立てる

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- サーバで `docker compose up -d` でアプリが立つ（最初はDB無しでも可）
- `/health` が200を返す

## 追加する自動確認（やること）
- CIで `docker compose up -d` → `curl http://localhost:<port>/health` が200 を確認（docker smoke）
- composeファイルの静的検証: `docker compose config` が成功すること

## 触る可能性が高いファイル（目安）
- apps/api/tests/test_devportal.py（新規）
- docker-compose.yml または composeファイル（必要に応じて）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S1-06] 自動デプロイ（GitHub Actions→サーバ反映）を確立
- Labels: `phase:1`, `S1-devops`, `area:infra`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- 方式A：GitHub ActionsからSSHでサーバに入って `docker compose pull && up -d`
- 方式B：サーバがWebHook受けてpull/upする
- 方式C：サーバにself-hosted runnerを置いてdeploy jobを実行する

#### 実装チェックリスト
- [ ] 方式A：GitHub ActionsからSSHでサーバに入って `docker compose pull && up -d`
- [ ] 方式B：サーバがWebHook受けてpull/upする
- [ ] 方式C：サーバにself-hosted runnerを置いてdeploy jobを実行する

#### 手動確認（マニュアル）
- [ ] mainマージ後に `/version` が新しいcommit SHAを表示する
- [ ] GitHubのActions/Checks画面で対象workflowが成功していることを確認

#### 自動確認（Automated）
- [ ] `deploy.yml`が secrets 未設定時に安全にskipされることを `if:` 条件で担保（回帰防止）
- [ ] secrets がある場合のみデプロイし、完了後に `/version` が期待値を返すスモークを入れる（S6-05と共通化可）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S1-06: 自動デプロイ（GitHub Actions→サーバ反映）を確立

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 方式A：GitHub ActionsからSSHでサーバに入って `docker compose pull && up -d`
- 方式B：サーバがWebHook受けてpull/upする
- 方式C：サーバにself-hosted runnerを置いてdeploy jobを実行する

## 追加する自動確認（やること）
- `deploy.yml`が secrets 未設定時に安全にskipされることを `if:` 条件で担保（回帰防止）
- secrets がある場合のみデプロイし、完了後に `/version` が期待値を返すスモークを入れる（S6-05と共通化可）

## 触る可能性が高いファイル（目安）
- .github/workflows/deploy.yml（修正）
- deploy/docker-compose.server.yml（参照）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S1-07] 先に“確認用Web”を作る（Dev Portal最小）
- Labels: `phase:1`, `S1-devops`, `area:web`, `area:api`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- `/` または `/dev` に 超簡易ページを出す（HTMLでOK）
- そのページが JS fetch で `/health` を叩き結果を表示する
- `/version`（commit SHA/ビルド時刻）も表示する

#### 実装チェックリスト
- [ ] `/` または `/dev` に 超簡易ページを出す（HTMLでOK）
- [ ] そのページが JS fetch で `/health` を叩き結果を表示する
- [ ] `/version`（commit SHA/ビルド時刻）も表示する
- [ ] `/dev` ページから `/health` と `/version` 取得失敗時の表示（エラー文言）も用意する（後続S6で強化してもOK）

#### 手動確認（マニュアル）
- [ ] iPhoneでページを開き、「API疎通OK」「version表示」が見える
- [ ] iPhone Safariで `https://<domain>/health` が200（JSON表示）になることを確認
- [ ] iPhone Safariで `https://<domain>/dev` を開き、Health/Versionが表示されることを確認

#### 自動確認（Automated）
- [ ] pytestで `/dev` が200を返し、HTML内に `/health` と `/version` を取得するスクリプト/表示要素が含まれることを検証（簡易文字列チェック）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S1-07: 先に“確認用Web”を作る（Dev Portal最小）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `/` または `/dev` に 超簡易ページを出す（HTMLでOK）
- そのページが JS fetch で `/health` を叩き結果を表示する
- `/version`（commit SHA/ビルド時刻）も表示する

## 追加する自動確認（やること）
- pytestで `/dev` が200を返し、HTML内に `/health` と `/version` を取得するスクリプト/表示要素が含まれることを検証（簡易文字列チェック）

## 触る可能性が高いファイル（目安）
- apps/api/tests/test_devportal.py（新規）
- docker-compose.yml または composeファイル（必要に応じて）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S1-08] リバースプロキシ + HTTPS（または暫定でも良い）
- Labels: `phase:1`, `S1-devops`, `area:infra`, `priority:p1`, `type:feature`

#### Done条件（仕様）
- `https://` でアクセスできる（Let’s Encrypt/Caddy等）
- 最低限 `/health` と `/dev` が外から見える

#### 実装チェックリスト
- [ ] `https://` でアクセスできる（Let’s Encrypt/Caddy等）
- [ ] 最低限 `/health` と `/dev` が外から見える
- [ ] Caddy等の設定で `/health` と `/dev` を外部公開し、HTTP→HTTPSリダイレクトを設定する

#### 手動確認（マニュアル）
- [ ] Safariで警告なしに開ける
- [ ] iPhone Safariで `https://<domain>/health` が200（JSON表示）になることを確認
- [ ] iPhone Safariで `https://<domain>/dev` を開き、Health/Versionが表示されることを確認

#### 自動確認（Automated）
- [ ] deploy後のスモークで `https://<domain>/health` と `https://<domain>/dev` が200 かを確認（`BASE_URL` をActionsのSecret/Variableで受け取る）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S1-08: リバースプロキシ + HTTPS（または暫定でも良い）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `https://` でアクセスできる（Let’s Encrypt/Caddy等）
- 最低限 `/health` と `/dev` が外から見える

## 追加する自動確認（やること）
- deploy後のスモークで `https://<domain>/health` と `https://<domain>/dev` が200 かを確認（`BASE_URL` をActionsのSecret/Variableで受け取る）

## 触る可能性が高いファイル（目安）
- deploy/Caddyfile（参照/修正）
- .github/workflows/deploy.yml（https smoke追加）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S1-09] 環境変数の管理方針を固定（Secrets含む）
- Labels: `phase:1`, `S1-devops`, `priority:p1`, `type:docs`

#### Done条件（仕様）
- GitHub Secretsに入れるもの（SSH鍵等）
- サーバに置く `.env` の場所
- READMEに「ここを変える」を明記

#### 実装チェックリスト
- [ ] GitHub Secretsに入れるもの（SSH鍵等）
- [ ] サーバに置く `.env` の場所
- [ ] READMEに「ここを変える」を明記

#### 手動確認（マニュアル）
- [ ] READMEに運用手順がある
- [ ] `.env.example` から `.env` を作り、composeと同じディレクトリに配置できていることを確認
- [ ] GitHub Secrets（DEPLOY_HOST/DEPLOY_USER/DEPLOY_SSH_KEY等）が設定されていることを確認

#### 自動確認（Automated）
- [ ] CIで `.env.example` が存在し、必須キー（PORT/GIT_SHA/APP_ENV/BUILD_TIME）が含まれることを検証
- [ ] READMEまたは運用ドキュメントにGitHub Secrets一覧と `.env` 配置方針が書かれているかをCIで軽く検証（見出し/キーワードチェック）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S1-09: 環境変数の管理方針を固定（Secrets含む）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- GitHub Secretsに入れるもの（SSH鍵等）
- サーバに置く `.env` の場所
- READMEに「ここを変える」を明記

## 追加する自動確認（やること）
- CIで `.env.example` が存在し、必須キー（PORT/GIT_SHA/APP_ENV/BUILD_TIME）が含まれることを検証
- READMEまたは運用ドキュメントにGitHub Secrets一覧と `.env` 配置方針が書かれているかをCIで軽く検証（見出し/キーワードチェック）

## 触る可能性が高いファイル（目安）
- .env.example（確認）
- README.md / docs/operations.md（方針追記）
- scripts/verify_env_docs.py（新規）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

# S2: 教材取り込み・閲覧観点（理論MDを取り込み、Webで読める）

### [P1-S2-01] 教材ファイル配置とメタ情報整備
- Labels: `phase:1`, `S2-content`, `area:infra`, `priority:p0`, `type:chore`

#### Done条件（仕様）
- `docs/source/` に理論MDを配置（リポジトリに入れる）
- ファイル名・版（v1.1等）をメタとして扱えるようにする

#### 実装チェックリスト
- [ ] `docs/source/` に理論MDを配置（リポジトリに入れる）
- [ ] ファイル名・版（v1.1等）をメタとして扱えるようにする

#### 手動確認（マニュアル）
- [ ] GitHubでファイルが見える
- [ ] Dev Portal（`/dev`）で `chunks: N` 等、教材取り込み状況が観測できることを確認

#### 自動確認（Automated）
- [ ] CIで `docs/source/` 配下に理論MDが存在すること（最低1ファイル）と、ファイル名が規約（例: snake/kebab）に沿うかを検証（任意）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S2-01: 教材ファイル配置とメタ情報整備

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `docs/source/` に理論MDを配置（リポジトリに入れる）
- ファイル名・版（v1.1等）をメタとして扱えるようにする

## 追加する自動確認（やること）
- CIで `docs/source/` 配下に理論MDが存在すること（最低1ファイル）と、ファイル名が規約（例: snake/kebab）に沿うかを検証（任意）

## 触る可能性が高いファイル（目安）
- apps/api/tests/（API/統合テスト追加）
- migrations/（テーブル/拡張）
- docs/source/（教材）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S2-02] DBスキーマ：doc_chunks（教材チャンク）作成
- Labels: `phase:1`, `S2-content`, `area:db`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- `doc_chunks`（本文、doc_id、章/節、順序、hash、embedding列は後でもOK）
- migrationで作れる

#### 実装チェックリスト
- [ ] `doc_chunks`（本文、doc_id、章/節、順序、hash、embedding列は後でもOK）
- [ ] migrationで作れる

#### 手動確認（マニュアル）
- [ ] Dev Portalに「DB接続OK」表示（S6側で作ってもOK）
- [ ] Dev Portal（`/dev`）で `chunks: N` 等、教材取り込み状況が観測できることを確認

#### 自動確認（Automated）
- [ ] GitHub ActionsでPostgreSQLサービスを立て、migration適用後に `doc_chunks` テーブルが存在することをテスト

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S2-02: DBスキーマ：doc_chunks（教材チャンク）作成

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `doc_chunks`（本文、doc_id、章/節、順序、hash、embedding列は後でもOK）
- migrationで作れる

## 追加する自動確認（やること）
- GitHub ActionsでPostgreSQLサービスを立て、migration適用後に `doc_chunks` テーブルが存在することをテスト

## 触る可能性が高いファイル（目安）
- apps/api/tests/（API/統合テスト追加）
- migrations/（テーブル/拡張）
- docs/source/（教材）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S2-03] “サーバで完結”する取り込み（起動時ブートストラップ）
- Labels: `phase:1`, `S2-content`, `area:api`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- アプリ起動時に `doc_chunks` が空なら自動で取り込み

#### 実装チェックリスト
- [ ] アプリ起動時に `doc_chunks` が空なら自動で取り込み
- [ ] 取り込み対象のMD（`docs/source/`）の走査・チャンク分割・hash計算を実装する

#### 手動確認（マニュアル）
- [ ] `/dev` に「chunks: N」などの表示が出る
- [ ] Dev Portal（`/dev`）で `chunks: N` 等、教材取り込み状況が観測できることを確認

#### 自動確認（Automated）
- [ ] テスト用DBを空で起動し、アプリ起動時ブートストラップで `doc_chunks` にレコードが入ることを統合テスト
- [ ] 二重取り込み防止（hash）をユニットテスト（同一入力で件数が増えない）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S2-03: “サーバで完結”する取り込み（起動時ブートストラップ）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- アプリ起動時に `doc_chunks` が空なら自動で取り込み

## 追加する自動確認（やること）
- テスト用DBを空で起動し、アプリ起動時ブートストラップで `doc_chunks` にレコードが入ることを統合テスト
- 二重取り込み防止（hash）をユニットテスト（同一入力で件数が増えない）

## 触る可能性が高いファイル（目安）
- apps/api/tests/（API/統合テスト追加）
- migrations/（テーブル/拡張）
- docs/source/（教材）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S2-04] 教材閲覧API（章・節一覧 / チャンク取得）
- Labels: `phase:1`, `S2-content`, `area:api`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- `GET /api/docs`（章/節のツリー or リスト）
- `GET /api/docs/{doc_id}/chunks?section=...`

#### 実装チェックリスト
- [ ] `GET /api/docs`（章/節のツリー or リスト）
- [ ] `GET /api/docs/{doc_id}/chunks?section=...`

#### 手動確認（マニュアル）
- [ ] Dev Portalから叩ける or ブラウザでJSONが見える
- [ ] Dev Portal（`/dev`）で `chunks: N` 等、教材取り込み状況が観測できることを確認

#### 自動確認（Automated）
- [ ] pytestで `GET /api/docs` と `GET /api/docs/{doc_id}/chunks` の200とレスポンススキーマを検証

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S2-04: 教材閲覧API（章・節一覧 / チャンク取得）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `GET /api/docs`（章/節のツリー or リスト）
- `GET /api/docs/{doc_id}/chunks?section=...`

## 追加する自動確認（やること）
- pytestで `GET /api/docs` と `GET /api/docs/{doc_id}/chunks` の200とレスポンススキーマを検証

## 触る可能性が高いファイル（目安）
- apps/api/tests/（API/統合テスト追加）
- migrations/（テーブル/拡張）
- docs/source/（教材）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S2-05] Web：教材ビューア（最低限）
- Labels: `phase:1`, `S2-content`, `area:web`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- iPhoneで読みやすい表示（レスポンシブ）
- 章/節を選ぶと本文が表示される（最初はチャンク連結でOK）

#### 実装チェックリスト
- [ ] iPhoneで読みやすい表示（レスポンシブ）
- [ ] 章/節を選ぶと本文が表示される（最初はチャンク連結でOK）

#### 手動確認（マニュアル）
- [ ] Safariで普通に読める
- [ ] Dev Portal（`/dev`）で `chunks: N` 等、教材取り込み状況が観測できることを確認

#### 自動確認（Automated）
- [ ] 最低限、Webビューアのページが200を返し、章/節の選択UI要素が含まれることを検証（HTML文字列チェック）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S2-05: Web：教材ビューア（最低限）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- iPhoneで読みやすい表示（レスポンシブ）
- 章/節を選ぶと本文が表示される（最初はチャンク連結でOK）

## 追加する自動確認（やること）
- 最低限、Webビューアのページが200を返し、章/節の選択UI要素が含まれることを検証（HTML文字列チェック）

## 触る可能性が高いファイル（目安）
- apps/api/tests/（API/統合テスト追加）
- migrations/（テーブル/拡張）
- docs/source/（教材）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

# S3: 検索観点（キーワード/ベクトルで目的箇所に辿れる）

### [P1-S3-01] キーワード検索（SQL）を先に作る
- Labels: `phase:1`, `S3-search`, `area:api`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- `GET /api/search/keyword?q=...` が `doc_chunks` を返す（TopN）
- 結果に章/節/スニペット/チャンクIDが含まれる

#### 実装チェックリスト
- [ ] `GET /api/search/keyword?q=...` が `doc_chunks` を返す（TopN）
- [ ] 結果に章/節/スニペット/チャンクIDが含まれる

#### 手動確認（マニュアル）
- [ ] Web検索画面 or Dev Portalで結果が出る
- [ ] iPhone Safariで検索→結果表示→該当箇所へ遷移ができることを確認

#### 自動確認（Automated）
- [ ] pytestで `GET /api/search/keyword?q=...` が200を返し、結果に必要フィールド（章/節/スニペット/チャンクID）が含まれることを検証

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S3-01: キーワード検索（SQL）を先に作る

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `GET /api/search/keyword?q=...` が `doc_chunks` を返す（TopN）
- 結果に章/節/スニペット/チャンクIDが含まれる

## 追加する自動確認（やること）
- pytestで `GET /api/search/keyword?q=...` が200を返し、結果に必要フィールド（章/節/スニペット/チャンクID）が含まれることを検証

## 触る可能性が高いファイル（目安）
- apps/api/app/search.py（例）
- apps/api/tests/test_search.py（新規）
- migrations/（pgvector採用時）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S3-02] pgvector（または代替）の導入判断と採用
- Labels: `phase:1`, `S3-search`, `area:db`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- PostgreSQL + pgvector を使うなら extension有効化まで完了

#### 実装チェックリスト
- [ ] PostgreSQL + pgvector を使うなら extension有効化まで完了
- [ ] 採用方針（pgvector or 代替）を README または docs に明記する

#### 手動確認（マニュアル）
- [ ] `/dev` に「vector-ready: true」表示（表示はS6でも可）
- [ ] iPhone Safariで検索→結果表示→該当箇所へ遷移ができることを確認

#### 自動確認（Automated）
- [ ] 採用方針に応じた自動検証を用意: pgvector採用なら `CREATE EXTENSION vector` がmigrationに含まれること、代替なら代替方式がdocsに明記されていること

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S3-02: pgvector（または代替）の導入判断と採用

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- PostgreSQL + pgvector を使うなら extension有効化まで完了

## 追加する自動確認（やること）
- 採用方針に応じた自動検証を用意: pgvector採用なら `CREATE EXTENSION vector` がmigrationに含まれること、代替なら代替方式がdocsに明記されていること

## 触る可能性が高いファイル（目安）
- apps/api/app/search.py（例）
- apps/api/tests/test_search.py（新規）
- migrations/（pgvector採用時）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S3-03] embedding生成（doc_chunks用）
- Labels: `phase:1`, `S3-search`, `area:llm`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- 取り込み時 or バッチで embedding を埋める
- 失敗時のリトライ/ログがある

#### 実装チェックリスト
- [ ] 取り込み時 or バッチで embedding を埋める
- [ ] 失敗時のリトライ/ログがある

#### 手動確認（マニュアル）
- [ ] `/dev` に「embedded: N/M」表示
- [ ] iPhone Safariで検索→結果表示→該当箇所へ遷移ができることを確認

#### 自動確認（Automated）
- [ ] embedding生成処理をユニットテスト（外部LLMはモック/スタブ）。失敗時にリトライされ、ログ/例外が整形されることを検証
- [ ] 取り込み時に embedding が埋まっている割合 `embedded: N/M` を返す計算ロジックをテスト（S6の/healthでも可）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S3-03: embedding生成（doc_chunks用）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 取り込み時 or バッチで embedding を埋める
- 失敗時のリトライ/ログがある

## 追加する自動確認（やること）
- embedding生成処理をユニットテスト（外部LLMはモック/スタブ）。失敗時にリトライされ、ログ/例外が整形されることを検証
- 取り込み時に embedding が埋まっている割合 `embedded: N/M` を返す計算ロジックをテスト（S6の/healthでも可）

## 触る可能性が高いファイル（目安）
- apps/api/app/search.py（例）
- apps/api/tests/test_search.py（新規）
- migrations/（pgvector採用時）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S3-04] ベクトル検索API
- Labels: `phase:1`, `S3-search`, `area:api`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- `GET /api/search/vector?q=...` で近傍チャンクTopKが返る
- スコアと参照メタが返る

#### 実装チェックリスト
- [ ] `GET /api/search/vector?q=...` で近傍チャンクTopKが返る
- [ ] スコアと参照メタが返る

#### 手動確認（マニュアル）
- [ ] “観測関数 o_S” と検索すると関連節が出る、など
- [ ] iPhone Safariで検索→結果表示→該当箇所へ遷移ができることを確認

#### 自動確認（Automated）
- [ ] pytestで `GET /api/search/vector?q=...` が200を返し、スコア順に並ぶことを検証（固定データ+ダミーembeddingで）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S3-04: ベクトル検索API

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `GET /api/search/vector?q=...` で近傍チャンクTopKが返る
- スコアと参照メタが返る

## 追加する自動確認（やること）
- pytestで `GET /api/search/vector?q=...` が200を返し、スコア順に並ぶことを検証（固定データ+ダミーembeddingで）

## 触る可能性が高いファイル（目安）
- apps/api/app/search.py（例）
- apps/api/tests/test_search.py（新規）
- migrations/（pgvector採用時）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S3-05] ハイブリッド検索（keyword + vectorの簡易合成）
- Labels: `phase:1`, `S3-search`, `area:api`, `priority:p1`, `type:feature`

#### Done条件（仕様）
- `GET /api/search?q=...` で統合結果が返る
- 単純なスコア合成でOK（Phase1は完成度より導線）

#### 実装チェックリスト
- [ ] `GET /api/search?q=...` で統合結果が返る
- [ ] 単純なスコア合成でOK（Phase1は完成度より導線）

#### 手動確認（マニュアル）
- [ ] “集合被覆”などでそれっぽい節へ辿れる
- [ ] iPhone Safariで検索→結果表示→該当箇所へ遷移ができることを確認

#### 自動確認（Automated）
- [ ] pytestで hybrid 検索（例: `/api/search?q=...`）が keyword と vector の結果を統合し、重複を除き、上位Nを返すことを検証

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S3-05: ハイブリッド検索（keyword + vectorの簡易合成）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `GET /api/search?q=...` で統合結果が返る
- 単純なスコア合成でOK（Phase1は完成度より導線）

## 追加する自動確認（やること）
- pytestで hybrid 検索（例: `/api/search?q=...`）が keyword と vector の結果を統合し、重複を除き、上位Nを返すことを検証

## 触る可能性が高いファイル（目安）
- apps/api/app/search.py（例）
- apps/api/tests/test_search.py（新規）
- migrations/（pgvector採用時）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S3-06] Web：検索UI（結果→教材ビューアへジャンプ）
- Labels: `phase:1`, `S3-search`, `area:web`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- 検索→結果一覧→クリックで該当箇所表示

#### 実装チェックリスト
- [ ] 検索→結果一覧→クリックで該当箇所表示

#### 手動確認（マニュアル）
- [ ] Safariだけで検索とジャンプができる
- [ ] iPhone Safariで検索→結果表示→該当箇所へ遷移ができることを確認

#### 自動確認（Automated）
- [ ] E2E最小: 検索ページが200、検索クエリで結果一覧が描画され、クリックで教材ビューアへ遷移できるURLが生成されることを検証（HTML/URL生成のテスト）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S3-06: Web：検索UI（結果→教材ビューアへジャンプ）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 検索→結果一覧→クリックで該当箇所表示

## 追加する自動確認（やること）
- E2E最小: 検索ページが200、検索クエリで結果一覧が描画され、クリックで教材ビューアへ遷移できるURLが生成されることを検証（HTML/URL生成のテスト）

## 触る可能性が高いファイル（目安）
- apps/api/app/search.py（例）
- apps/api/tests/test_search.py（新規）
- migrations/（pgvector採用時）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

# S4: RAG Q&A観点（質問→根拠→回答の導線）

### [P1-S4-01] Ollama接続ラッパー（タイムアウト/エラー整形）
- Labels: `phase:1`, `S4-rag`, `area:llm`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- Ollamaの接続先をenvで指定できる
- タイムアウト時に分かりやすいエラーが返る

#### 実装チェックリスト
- [ ] Ollamaの接続先をenvで指定できる
- [ ] タイムアウト時に分かりやすいエラーが返る

#### 手動確認（マニュアル）
- [ ] `/dev` に「ollama: reachable/unreachable」表示
- [ ] iPhone Safari（Dev PortalまたはQ&A画面）から質問を投げ、回答と根拠が返ることを確認

#### 自動確認（Automated）
- [ ] Ollamaラッパーをユニットテスト（httpxのモック）。タイムアウト/接続不可/非200の時に、呼び出し側が扱える例外/エラー形式で返ることを検証

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S4-01: Ollama接続ラッパー（タイムアウト/エラー整形）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- Ollamaの接続先をenvで指定できる
- タイムアウト時に分かりやすいエラーが返る

## 追加する自動確認（やること）
- Ollamaラッパーをユニットテスト（httpxのモック）。タイムアウト/接続不可/非200の時に、呼び出し側が扱える例外/エラー形式で返ることを検証

## 触る可能性が高いファイル（目安）
- apps/api/app/qa.py（例）
- apps/api/tests/test_qa.py（新規）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S4-02] RAGプロンプトテンプレ（根拠必須・捏造抑制）
- Labels: `phase:1`, `S4-rag`, `area:llm`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- 参照チャンクをコンテキストに入れる
- 回答に「根拠チャンクID（または章/節）」を必ず含める形式にする

#### 実装チェックリスト
- [ ] 参照チャンクをコンテキストに入れる
- [ ] 回答に「根拠チャンクID（または章/節）」を必ず含める形式にする
- [ ] プロンプトテンプレをコード上で一元管理し、APIから参照する（散在を防ぐ）

#### 手動確認（マニュアル）
- [ ] Q&Aで根拠が見える
- [ ] iPhone Safari（Dev PortalまたはQ&A画面）から質問を投げ、回答と根拠が返ることを確認

#### 自動確認（Automated）
- [ ] RAGプロンプトテンプレが「根拠必須」「引用元を列挙」などの要件を満たすことをユニットテスト（文字列チェック）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S4-02: RAGプロンプトテンプレ（根拠必須・捏造抑制）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 参照チャンクをコンテキストに入れる
- 回答に「根拠チャンクID（または章/節）」を必ず含める形式にする

## 追加する自動確認（やること）
- RAGプロンプトテンプレが「根拠必須」「引用元を列挙」などの要件を満たすことをユニットテスト（文字列チェック）

## 触る可能性が高いファイル（目安）
- apps/api/app/qa.py（例）
- apps/api/tests/test_qa.py（新規）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S4-03] RAG回答API（retrieval→回答→根拠返却）
- Labels: `phase:1`, `S4-rag`, `area:api`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- `POST /api/qa`（question）→（answer, citations[]）
- citationsにチャンクID/見出し/スニペット/スコアを含む

#### 実装チェックリスト
- [ ] `POST /api/qa`（question）→（answer, citations[]）
- [ ] citationsにチャンクID/見出し/スニペット/スコアを含む

#### 手動確認（マニュアル）
- [ ] Dev Portalから投げてJSONが返る
- [ ] iPhone Safari（Dev PortalまたはQ&A画面）から質問を投げ、回答と根拠が返ることを確認

#### 自動確認（Automated）
- [ ] pytestで `POST /api/qa` が200を返し、`answer` と `citations[]` を返すことを検証（LLM部分はスタブ）
- [ ] citationsの各要素にチャンクID/見出し/スニペット/スコアが含まれることをスキーマテスト

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S4-03: RAG回答API（retrieval→回答→根拠返却）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `POST /api/qa`（question）→（answer, citations[]）
- citationsにチャンクID/見出し/スニペット/スコアを含む

## 追加する自動確認（やること）
- pytestで `POST /api/qa` が200を返し、`answer` と `citations[]` を返すことを検証（LLM部分はスタブ）
- citationsの各要素にチャンクID/見出し/スニペット/スコアが含まれることをスキーマテスト

## 触る可能性が高いファイル（目安）
- apps/api/app/qa.py（例）
- apps/api/tests/test_qa.py（新規）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S4-04] qa_log保存（質問・回答・参照）
- Labels: `phase:1`, `S4-rag`, `area:db`, `priority:p1`, `type:feature`

#### Done条件（仕様）
- 質問と回答と参照チャンクがDBに残る
- 後で一覧できるAPI（簡易）を用意

#### 実装チェックリスト
- [ ] 質問と回答と参照チャンクがDBに残る
- [ ] 後で一覧できるAPI（簡易）を用意

#### 手動確認（マニュアル）
- [ ] “履歴”が見える（簡易でOK）
- [ ] iPhone Safari（Dev PortalまたはQ&A画面）から質問を投げ、回答と根拠が返ることを確認

#### 自動確認（Automated）
- [ ] qa_log への保存を統合テスト（API呼び出し→DBに1件増える）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S4-04: qa_log保存（質問・回答・参照）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 質問と回答と参照チャンクがDBに残る
- 後で一覧できるAPI（簡易）を用意

## 追加する自動確認（やること）
- qa_log への保存を統合テスト（API呼び出し→DBに1件増える）

## 触る可能性が高いファイル（目安）
- apps/api/app/qa.py（例）
- apps/api/tests/test_qa.py（新規）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S4-05] Web：Q&A UI（チャット風＋根拠展開）
- Labels: `phase:1`, `S4-rag`, `area:web`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- 質問→回答
- 根拠をタップで展開、タップで教材表示へジャンプ

#### 実装チェックリスト
- [ ] 質問→回答
- [ ] 根拠をタップで展開、タップで教材表示へジャンプ

#### 手動確認（マニュアル）
- [ ] Safariで“質問→根拠→教材”が一筆書きで辿れる
- [ ] iPhone Safari（Dev PortalまたはQ&A画面）から質問を投げ、回答と根拠が返ることを確認

#### 自動確認（Automated）
- [ ] Web Q&A画面が200で表示され、送信すると回答と根拠が表示されるUI要素が存在することをテスト（HTMLチェック + APIモック）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S4-05: Web：Q&A UI（チャット風＋根拠展開）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 質問→回答
- 根拠をタップで展開、タップで教材表示へジャンプ

## 追加する自動確認（やること）
- Web Q&A画面が200で表示され、送信すると回答と根拠が表示されるUI要素が存在することをテスト（HTMLチェック + APIモック）

## 触る可能性が高いファイル（目安）
- apps/api/app/qa.py（例）
- apps/api/tests/test_qa.py（新規）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

# S5: 練習問題観点（問題を解いて学習ログが溜まる）

### [P1-S5-01] exercises / attempts スキーマ作成
- Labels: `phase:1`, `S5-exercise`, `area:db`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- `exercises`（問題本文、形式、選択肢、正解、解説、tags）
- `attempts`（exercise_id、回答、正誤、日時）

#### 実装チェックリスト
- [ ] `exercises`（問題本文、形式、選択肢、正解、解説、tags）
- [ ] `attempts`（exercise_id、回答、正誤、日時）

#### 手動確認（マニュアル）
- [ ] `/dev`でテーブル準備OK表示（または簡易APIで確認）
- [ ] iPhone Safariで演習一覧→解答→採点→解説→履歴更新が一連でできることを確認

#### 自動確認（Automated）
- [ ] migration適用後に `exercises` と `attempts` テーブルが存在することをテスト（PostgreSQLサービス）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S5-01: exercises / attempts スキーマ作成

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `exercises`（問題本文、形式、選択肢、正解、解説、tags）
- `attempts`（exercise_id、回答、正誤、日時）

## 追加する自動確認（やること）
- migration適用後に `exercises` と `attempts` テーブルが存在することをテスト（PostgreSQLサービス）

## 触る可能性が高いファイル（目安）
- apps/api/app/exercises.py（例）
- apps/api/tests/test_exercises.py（新規）
- migrations/（schema）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S5-02] 初期問題セット（10〜30問）をseedとして投入
- Labels: `phase:1`, `S5-exercise`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- 添付理論のコア（W/E/S/A(S)、観測関数、同値類、集合被覆など）を含む
- seed手段が「サーバで完結」する
- 起動時seed / 管理API / GitHub Actions手動workflow のどれか

#### 実装チェックリスト
- [ ] 添付理論のコア（W/E/S/A(S)、観測関数、同値類、集合被覆など）を含む
- [ ] seed手段が「サーバで完結」する
- [ ] 起動時seed / 管理API / GitHub Actions手動workflow のどれか

#### 手動確認（マニュアル）
- [ ] Webで問題一覧が見える
- [ ] iPhone Safariで演習一覧→解答→採点→解説→履歴更新が一連でできることを確認

#### 自動確認（Automated）
- [ ] seed実行後に `exercises` が最低10件以上入ることをテスト（起動時seed/管理API/手動workflowのいずれかに合わせる）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S5-02: 初期問題セット（10〜30問）をseedとして投入

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 添付理論のコア（W/E/S/A(S)、観測関数、同値類、集合被覆など）を含む
- seed手段が「サーバで完結」する
- 起動時seed / 管理API / GitHub Actions手動workflow のどれか

## 追加する自動確認（やること）
- seed実行後に `exercises` が最低10件以上入ることをテスト（起動時seed/管理API/手動workflowのいずれかに合わせる）

## 触る可能性が高いファイル（目安）
- apps/api/app/exercises.py（例）
- apps/api/tests/test_exercises.py（新規）
- migrations/（schema）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S5-03] 演習API（一覧・取得・解答送信）
- Labels: `phase:1`, `S5-exercise`, `area:api`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- `GET /api/exercises`
- `GET /api/exercises/{id}`
- `POST /api/exercises/{id}/attempt`

#### 実装チェックリスト
- [ ] `GET /api/exercises`
- [ ] `GET /api/exercises/{id}`
- [ ] `POST /api/exercises/{id}/attempt`

#### 手動確認（マニュアル）
- [ ] Dev Portalまたはブラウザで動作
- [ ] iPhone Safariで演習一覧→解答→採点→解説→履歴更新が一連でできることを確認

#### 自動確認（Automated）
- [ ] pytestで `GET /api/exercises` `GET /api/exercises/{id}` `POST /api/exercises/{id}/attempt` の基本動作とレスポンススキーマを検証

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S5-03: 演習API（一覧・取得・解答送信）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `GET /api/exercises`
- `GET /api/exercises/{id}`
- `POST /api/exercises/{id}/attempt`

## 追加する自動確認（やること）
- pytestで `GET /api/exercises` `GET /api/exercises/{id}` `POST /api/exercises/{id}/attempt` の基本動作とレスポンススキーマを検証

## 触る可能性が高いファイル（目安）
- apps/api/app/exercises.py（例）
- apps/api/tests/test_exercises.py（新規）
- migrations/（schema）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S5-04] 自動採点（Phase1は“確実に判定できる形式”に限定）
- Labels: `phase:1`, `S5-exercise`, `area:api`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- 選択式：完全一致
- 短答：正規化（空白/全半角/大小）＋許容解リスト

#### 実装チェックリスト
- [ ] 選択式：完全一致
- [ ] 短答：正規化（空白/全半角/大小）＋許容解リスト

#### 手動確認（マニュアル）
- [ ] 解いたら即結果が出て履歴に残る
- [ ] iPhone Safariで演習一覧→解答→採点→解説→履歴更新が一連でできることを確認

#### 自動確認（Automated）
- [ ] 採点ロジックをユニットテスト（選択式/短答の正規化/許容解）
- [ ] 誤答時の返却（正解・解説・正誤フラグ）がUI側で扱える形式になっているかをテスト

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S5-04: 自動採点（Phase1は“確実に判定できる形式”に限定）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 選択式：完全一致
- 短答：正規化（空白/全半角/大小）＋許容解リスト

## 追加する自動確認（やること）
- 採点ロジックをユニットテスト（選択式/短答の正規化/許容解）
- 誤答時の返却（正解・解説・正誤フラグ）がUI側で扱える形式になっているかをテスト

## 触る可能性が高いファイル（目安）
- apps/api/app/exercises.py（例）
- apps/api/tests/test_exercises.py（新規）
- migrations/（schema）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S5-05] Web：演習UI（解く→採点→解説）
- Labels: `phase:1`, `S5-exercise`, `area:web`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- iPhoneで解ける入力UI（ボタン中心）
- 採点と解説が表示される

#### 実装チェックリスト
- [ ] iPhoneで解ける入力UI（ボタン中心）
- [ ] 採点と解説が表示される

#### 手動確認（マニュアル）
- [ ] Safariだけで完結して練習できる
- [ ] iPhone Safariで演習一覧→解答→採点→解説→履歴更新が一連でできることを確認

#### 自動確認（Automated）
- [ ] 演習UIのページが200で表示され、問題取得→解答送信→採点結果表示に必要なDOMが揃っていることをテスト（HTMLチェック）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S5-05: Web：演習UI（解く→採点→解説）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- iPhoneで解ける入力UI（ボタン中心）
- 採点と解説が表示される

## 追加する自動確認（やること）
- 演習UIのページが200で表示され、問題取得→解答送信→採点結果表示に必要なDOMが揃っていることをテスト（HTMLチェック）

## 触る可能性が高いファイル（目安）
- apps/api/app/exercises.py（例）
- apps/api/tests/test_exercises.py（新規）
- migrations/（schema）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S5-06] 学習履歴（直近N件）表示
- Labels: `phase:1`, `S5-exercise`, `priority:p1`, `type:feature`

#### Done条件（仕様）
- 正答率、最近間違えた問題、など最低限の履歴が見える

#### 実装チェックリスト
- [ ] 正答率、最近間違えた問題、など最低限の履歴が見える

#### 手動確認（マニュアル）
- [ ] “復習”ができる状態
- [ ] iPhone Safariで演習一覧→解答→採点→解説→履歴更新が一連でできることを確認

#### 自動確認（Automated）
- [ ] 履歴API/画面で直近N件が取得でき、正答率などの集計が壊れないことをテスト（固定データで）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S5-06: 学習履歴（直近N件）表示

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 正答率、最近間違えた問題、など最低限の履歴が見える

## 追加する自動確認（やること）
- 履歴API/画面で直近N件が取得でき、正答率などの集計が壊れないことをテスト（固定データで）

## 触る可能性が高いファイル（目安）
- apps/api/app/exercises.py（例）
- apps/api/tests/test_exercises.py（新規）
- migrations/（schema）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

# S6: 品質・運用観点（壊れにくく、原因が追える/安全）

### [P1-S6-01] /health を“複合ヘルスチェック”にする（DB/LLM）
- Labels: `phase:1`, `S6-quality`, `area:api`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- DB疎通、Ollama疎通、doc_chunks件数、などを返す
- Dev Portalがこの結果を見て表示できる

#### 実装チェックリスト
- [ ] DB疎通、Ollama疎通、doc_chunks件数、などを返す
- [ ] Dev Portalがこの結果を見て表示できる

#### 手動確認（マニュアル）
- [ ] `/dev`で状態が一目で分かる
- [ ] iPhone Safariの `/dev` で、問題が起きたときに次の行動が分かる表示になっていることを確認

#### 自動確認（Automated）
- [ ] `/health` のレスポンスに DB/LLM疎通・doc_chunks件数などが含まれることをテスト（外部依存はモック/スタブ、DBは実サービス）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S6-01: /health を“複合ヘルスチェック”にする（DB/LLM）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- DB疎通、Ollama疎通、doc_chunks件数、などを返す
- Dev Portalがこの結果を見て表示できる

## 追加する自動確認（やること）
- `/health` のレスポンスに DB/LLM疎通・doc_chunks件数などが含まれることをテスト（外部依存はモック/スタブ、DBは実サービス）

## 触る可能性が高いファイル（目安）
- apps/api/app/main.py（/health等）
- apps/api/tests/test_ops.py（新規/追加）
- .github/workflows/deploy.yml（S6-05）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S6-02] リクエストログとrequest_id（原因追跡の最小）
- Labels: `phase:1`, `S6-quality`, `priority:p1`, `type:feature`

#### Done条件（仕様）
- すべてのAPIにrequest_id付与
- 例外時にrequest_id付きで返す

#### 実装チェックリスト
- [ ] すべてのAPIにrequest_id付与
- [ ] 例外時にrequest_id付きで返す

#### 手動確認（マニュアル）
- [ ] エラー画面にrequest_idが出る
- [ ] iPhone Safariの `/dev` で、問題が起きたときに次の行動が分かる表示になっていることを確認

#### 自動確認（Automated）
- [ ] すべてのAPIレスポンスに `request_id` が付くこと、例外時も同様であることをテスト（FastAPI TestClient）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S6-02: リクエストログとrequest_id（原因追跡の最小）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- すべてのAPIにrequest_id付与
- 例外時にrequest_id付きで返す

## 追加する自動確認（やること）
- すべてのAPIレスポンスに `request_id` が付くこと、例外時も同様であることをテスト（FastAPI TestClient）

## 触る可能性が高いファイル（目安）
- apps/api/app/main.py（/health等）
- apps/api/tests/test_ops.py（新規/追加）
- .github/workflows/deploy.yml（S6-05）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S6-03] エラー表示の統一（iPhoneで困らない文言）
- Labels: `phase:1`, `S6-quality`, `priority:p1`, `type:feature`

#### Done条件（仕様）
- “何が足りないか”（DB未接続、Ollama未起動等）がUIに出る

#### 実装チェックリスト
- [ ] “何が足りないか”（DB未接続、Ollama未起動等）がUIに出る

#### 手動確認（マニュアル）
- [ ] 詰まったときに次の行動が分かる
- [ ] iPhone Safariの `/dev` で、問題が起きたときに次の行動が分かる表示になっていることを確認

#### 自動確認（Automated）
- [ ] 代表的な障害（DB未接続/Ollama未起動）を疑似的に発生させ、UI/APIのエラーメッセージが統一形式で返ることをテスト

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S6-03: エラー表示の統一（iPhoneで困らない文言）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- “何が足りないか”（DB未接続、Ollama未起動等）がUIに出る

## 追加する自動確認（やること）
- 代表的な障害（DB未接続/Ollama未起動）を疑似的に発生させ、UI/APIのエラーメッセージが統一形式で返ることをテスト

## 触る可能性が高いファイル（目安）
- apps/api/app/main.py（/health等）
- apps/api/tests/test_ops.py（新規/追加）
- .github/workflows/deploy.yml（S6-05）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S6-04] 最低限のアクセス制御（パスワード1個でも良い）
- Labels: `phase:1`, `S6-quality`, `priority:p1`, `type:feature`

#### Done条件（仕様）
- `/dev` や 管理系API（seed/ingestなど）に簡易認証

#### 実装チェックリスト
- [ ] `/dev` や 管理系API（seed/ingestなど）に簡易認証

#### 手動確認（マニュアル）
- [ ] 外部から丸見えになっていない
- [ ] iPhone Safariの `/dev` で、問題が起きたときに次の行動が分かる表示になっていることを確認

#### 自動確認（Automated）
- [ ] 認証が無い場合に `/dev` と管理系APIが 401/403 になること、正しい認証情報で200になることをテスト

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S6-04: 最低限のアクセス制御（パスワード1個でも良い）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- `/dev` や 管理系API（seed/ingestなど）に簡易認証

## 追加する自動確認（やること）
- 認証が無い場合に `/dev` と管理系APIが 401/403 になること、正しい認証情報で200になることをテスト

## 触る可能性が高いファイル（目安）
- apps/api/app/main.py（/health等）
- apps/api/tests/test_ops.py（新規/追加）
- .github/workflows/deploy.yml（S6-05）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S6-05] スモークテスト（デプロイ後に自動実行）
- Labels: `phase:1`, `S6-quality`, `area:infra`, `priority:p0`, `type:feature`

#### Done条件（仕様）
- デプロイworkflowの最後に
- `/health` が200
- `GET /api/docs` が動く
- `GET /api/exercises` が動く

#### 実装チェックリスト
- [ ] デプロイworkflowの最後に
- [ ] `/health` が200
- [ ] `GET /api/docs` が動く
- [ ] `GET /api/exercises` が動く
- [ ] スモークの失敗時にどのURL/どのステップで落ちたかActionsログに出す

#### 手動確認（マニュアル）
- [ ] Actions結果が緑なら最低限OKと言える
- [ ] iPhone Safariの `/dev` で、問題が起きたときに次の行動が分かる表示になっていることを確認

#### 自動確認（Automated）
- [ ] deploy workflow の最後にスモーク（`/health` 200, `/api/docs` OK, `/api/exercises` OK）を自動実行し、失敗時にログで原因が分かるようにする

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S6-05: スモークテスト（デプロイ後に自動実行）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- デプロイworkflowの最後に
- `/health` が200
- `GET /api/docs` が動く
- `GET /api/exercises` が動く

## 追加する自動確認（やること）
- deploy workflow の最後にスモーク（`/health` 200, `/api/docs` OK, `/api/exercises` OK）を自動実行し、失敗時にログで原因が分かるようにする

## 触る可能性が高いファイル（目安）
- apps/api/app/main.py（/health等）
- apps/api/tests/test_ops.py（新規/追加）
- .github/workflows/deploy.yml（S6-05）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---

### [P1-S6-06] docs/architecture.md（W/E/S/A(S)で書く）
- Labels: `phase:1`, `S6-quality`, `priority:p0`, `type:docs`

#### Done条件（仕様）
- 「iPhone中心のE」「Phase1のS1〜S6」「Issues=A(S)」を書き切る
- Phase2以降の拡張ポイント（obligationタグやset cover導入）をメモ

#### 実装チェックリスト
- [ ] 「iPhone中心のE」「Phase1のS1〜S6」「Issues=A(S)」を書き切る
- [ ] Phase2以降の拡張ポイント（obligationタグやset cover導入）をメモ
- [ ] READMEから `docs/architecture.md` へのリンクを追加する

#### 手動確認（マニュアル）
- [ ] README→architectureへの導線があり、見てすぐ分かる
- [ ] iPhone Safariの `/dev` で、問題が起きたときに次の行動が分かる表示になっていることを確認

#### 自動確認（Automated）
- [ ] CIで `docs/architecture.md` が存在し、READMEからリンクされていることを検証（リンク切れ防止）

#### コーテックス実装依頼プロンプト（自動確認の追加）
```text
あなたはこのリポジトリの実装担当（AI）です。以下のIssueについて、**自動確認（Automated Verification）** を実装してください。

## 対象Issue
- P1-S6-06: docs/architecture.md（W/E/S/A(S)で書く）

## 背景
- Phase1は iPhone-first（ローカルPC前提を最小化）。GitHub Actions と `/dev` を観測点にして、Issueを進めるたびに iPhone で確認できる状態を維持する。

## 前提 / 制約（重要）
- 既存のCI方針を崩さない: ruff + pytest（coverage>=85）+ docker smoke。
- 外部依存（PostgreSQL/Ollama等）は、CIでは service container かモックで扱い、テストがタイムアウトで不安定にならないようにする。
- テストは落ちたときに原因が分かるメッセージを出す（assertメッセージ/ログ）。

## IssueのDone条件（仕様）
- 「iPhone中心のE」「Phase1のS1〜S6」「Issues=A(S)」を書き切る
- Phase2以降の拡張ポイント（obligationタグやset cover導入）をメモ

## 追加する自動確認（やること）
- CIで `docs/architecture.md` が存在し、READMEからリンクされていることを検証（リンク切れ防止）

## 触る可能性が高いファイル（目安）
- apps/api/app/main.py（/health等）
- apps/api/tests/test_ops.py（新規/追加）
- .github/workflows/deploy.yml（S6-05）

## 実装の指針
- 可能なものは `apps/api/tests/` に pytest を追加して検証する（FastAPI TestClient / httpx）。
- workflow変更が必要なら `.github/workflows/` を最小差分で修正し、ログにURL/ステップ名が残るようにする。
- `BASE_URL` など環境依存がある場合は GitHub Actions の Secrets/Variables から受け取れるようにする。

## 受け入れ基準
- PR作成でCIが走り、上記の自動確認が実行される。
- 条件を満たさない場合、CIがfailし、ログだけで原因特定できる。
- 既存CI（lint/test/coverage/docker smoke）を含め、すべてグリーン。
```

---
