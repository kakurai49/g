# オペレーション（Phase1 / S1）

## 環境変数
- `PORT`（既定: 8080）— API の待受ポート
- `GIT_SHA`（既定: `unknown`）— `/health` と `/version` に表示するコミット SHA
- `BUILD_TIME`（任意）— ビルド時刻。設定されていれば `/version` に表示
- `APP_ENV`（既定: `dev`）— `/dev` に表示する環境ラベル

`.env.example` を雛形として `.env` を用意し、秘密情報はコミットしない。実行時 `.env` は compose ファイルと同じディレクトリに置く。

## GitHub Secrets / Variables
- 必須: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`
- 任意: `DEPLOY_PORT`（既定 22）, `DEPLOY_PATH`（既定 `/opt/g`）
- GHCR がプライベートの場合: `GHCR_USER`, `GHCR_TOKEN`

## デプロイフロー（GitHub Actions）
1. `main` への push で `docker.yml`（ビルド＆プッシュ）と `deploy.yml`（secrets がある場合のみ実行）が起動。
2. `deploy.yml` は `deploy/docker-compose.server.yml` と `deploy/Caddyfile` を SSH/SCP でサーバへ送信。
3. サーバ側で `docker compose pull` と `docker compose up -d --remove-orphans` を `DEPLOY_PATH` 内で実行。
4. iPhone Safari から `https://<domain>/dev` を開き、`/health` と `/version` の結果が表示されるか確認。

## セーフティ
- `/dev` は運用情報を含むため公開範囲に注意（後続フェーズで保護予定）。
- `.env` や SSH 鍵はコミットしない。認証情報は GitHub Secrets に保存。
- デプロイ用 secrets が無い場合、`deploy.yml` は安全に skip される。
