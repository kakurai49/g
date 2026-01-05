# `.env` 設置場所と接続構成のマニュアル（ローカル／サーバ）

このドキュメントでは、`.env` をどこに置くか、何と何をどう接続するか、ローカル／サーバでの実行手順をまとめる。

## 1. 配置の原則
- **ローカル開発**: リポジトリ直下に `.env` を置く。`docker-compose.yml` が `./.env` を読むため、`docker compose up` を実行するカレントディレクトリに `.env` を配置する。
- **サーバ本番**: サーバ上のデプロイ用ディレクトリ（例: `/opt/g`）直下に `.env` を置く。`deploy/docker-compose.server.yml` が同じ場所の `.env` を参照する。
- `.env` はリポジトリの `.env.example` をコピーして作成し、リポジトリにはコミットしない。

## 2. `.env` に設定する主な項目
- `GIT_SHA`: 表示用のコミット SHA（無ければ `unknown` など）
- `PORT`: API の待受ポート（デフォルト 8080）
- `APP_ENV`: 表示用の環境ラベル（`dev` / `prod` など）
- `BUILD_TIME`: 任意。指定すると `/version` にビルド時刻が表示される

## 3. 接続構成（ポートと経路）
1. FastAPI コンテナ（サービス名: `api`）はコンテナ内ポート `8080` で待ち受け。
2. Docker Compose がコンテナの 8080 をホストの 8080 に公開する（`8080:8080`）。
3. サーバでリバースプロキシを使う場合、Caddy などが外部の 80/443 を受けて `api:8080` へプロキシする。
4. クライアント（ローカル PC や iPhone）はブラウザから `http://localhost:8080/dev`（ローカル）またはドメインの `/dev`（本番）へアクセスし、`/health` `/version` の結果を Dev Portal で確認する。

## 4. ローカル環境での手順
1. `.env.example` を `.env` にコピーして値を設定する。
2. `docker compose up --build` を実行する。
3. ブラウザで `http://localhost:8080/dev` を開き、Health/Version が表示されれば完了。

## 5. サーバ環境での手順（手動デプロイ例）
1. サーバに `/opt/g` などのディレクトリを用意し、`deploy/docker-compose.server.yml` と `deploy/Caddyfile`（必要なら）を配置する。
2. `.env.example` を基にサーバ上で `.env` を作成し、同ディレクトリに置く。
3. GHCR がプライベートな場合は `docker login`（`GHCR_USER`/`GHCR_TOKEN`）を行う。
4. `docker compose -f docker-compose.server.yml pull` と `docker compose -f docker-compose.server.yml up -d --remove-orphans` を実行する。
5. iPhone Safari などから `http://<host>:8080/dev`（またはドメイン）を開き、`/health` `/version` が表示されることを確認する。

## 6. GitHub Actions を用いた自動デプロイの流れ
- `docker.yml`: GHCR に `api` イメージを `latest`/`sha-*` タグでビルド＆プッシュ。
- `deploy.yml`: `DEPLOY_HOST` `DEPLOY_USER` `DEPLOY_SSH_KEY` などの secrets が揃っている場合にサーバへ SSH/SCP し、`docker compose pull/up` を実行。
- secrets が無い場合はジョブがスキップされる設計。

## 7. セキュリティと運用上の注意
- `.env` や SSH 鍵などの秘密情報はリポジトリにコミットしない。
- `/dev` には運用情報が含まれるため公開範囲に注意し、必要に応じてリバースプロキシ側でアクセス制御を検討する。
- Python 実行環境は基本不要で、Docker があればローカル確認できる（テスト実行時のみ Python 環境が必要）。
