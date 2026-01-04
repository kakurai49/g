# サーバデプロイ手順

iPhone-first な運用を前提に、API をサーバで稼働させ `/dev` を iPhone Safari から確認するための手順をまとめます。

## 前提
- サーバに Docker と Docker Compose がインストール済み
- Docker コマンドを実行できる SSH アカウントを保有
- 任意: Caddy を使う場合はドメインが DNS でサーバを指していること

## サーバ上のディレクトリ構成（例: `/opt/g`）
```
/opt/g
├─ docker-compose.server.yml
├─ Caddyfile          # リバースプロキシを使う場合のみ
└─ .env               # 実行時の環境変数（コミットしない）
```

## `.env` の例
リポジトリ同梱の `.env.example` をベースにする:
```
GIT_SHA=dev
PORT=8080
APP_ENV=prod
# BUILD_TIME=2024-01-01T00:00:00Z
```

## 手動デプロイ手順
1. サーバにデプロイ用ディレクトリ（例: `/opt/g`）を作成。
2. `deploy/docker-compose.server.yml`、`deploy/Caddyfile`、`.env` をサーバへ配置。
3. GHCR がプライベートの場合はログイン:
   ```bash
   echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USER" --password-stdin
   ```
4. コンテナを取得して起動:
   ```bash
   docker compose -f docker-compose.server.yml pull
   docker compose -f docker-compose.server.yml up -d --remove-orphans
   ```
5. iPhone から `http://<host>:8080/dev`（またはドメイン）を開き、`/health` `/version` が Dev Portal に表示されることを確認。

## Caddy リバースプロキシ
- `deploy/Caddyfile` をテンプレートにドメインを差し替える。
- `api:8080` へリバースプロキシし、必要に応じて gzip や HSTS ヘッダを付与。
- `/dev` は現状公開のまま。運用情報を含むため将来フェーズで保護予定。

## GitHub Actions によるデプロイ
- ワークフロー: `.github/workflows/deploy.yml`
- トリガー: `main` への push、または `workflow_dispatch`
- 実行条件: `DEPLOY_HOST` と `DEPLOY_SSH_KEY` が設定されている場合のみ
- 手順概要:
  1. `deploy/docker-compose.server.yml` と `deploy/Caddyfile` を SCP でサーバにコピー
  2. GHCR がプライベートなら `GHCR_USER` / `GHCR_TOKEN` でログイン
  3. `docker compose pull` と `docker compose up -d --remove-orphans` を `DEPLOY_PATH` 内で実行
- secrets が未設定の場合はジョブがスキップされ、パイプラインは失敗しない。
