# g

iPhone-first な FastAPI MVP。デプロイ後は iPhone Safari から `/dev` を開き、`/health` `/version` の結果を確認することを前提としています。

## エンドポイント
- `GET /health` — `{ status, service, version, time, checks }`（UTC ISO8601）
- `GET /version` — `{ service, version, build_time? }`
- `GET /dev` — Dev Portal（内部で `/health` `/version` を fetch し画面表示）
- `GET /` — `/dev` へリダイレクト

## クイックスタート（ローカル／サーバ）
1. `.env.example` をコピーして `.env` を用意（最低でも `GIT_SHA` `PORT` `APP_ENV` を設定）。
2. `docker compose up --build` を実行。
3. ブラウザで `http://localhost:8080/dev` を開き、health/version が表示されることを確認。

## iPhone 確認手順
- デプロイ後、iPhone Safari で `https://<domain>/dev` を開く。
- 画面に "Dev Portal" が表示され、`/health` `/version` の JSON が描画されていることを確認。
- エラー表示が無いことを確認。

## GitHub Actions
- `ci.yml`: ruff + pytest（coverage >= 85%）+ docker smoke テスト。
- `docker.yml`: GHCR へ `latest` と `sha-<commit>` タグでイメージを build/push。
- `deploy.yml`: サーバへ SSH で compose pull/up を実行（secrets 未設定時は安全に skip）。

## デプロイ（サーバ）
- `deploy/docker-compose.server.yml` をサーバに配置し、GHCR イメージで起動。
- HTTPS が必要な場合は `deploy/Caddyfile` を参考にリバースプロキシを構成。
- 詳細手順・環境変数やシークレットの扱いは `deploy/README.md` と `docs/operations.md` を参照。

## 追加ドキュメント
- `docs/architecture.md`: W/E/S/A(S) 観点の設計メモ（日本語）
- `docs/operations.md`: 環境変数・シークレット・デプロイ運用（日本語）
- `docs/usage.md`: 全体の使い方・運用フローまとめ（日本語）
