# 使い方と運用マニュアル

Phase1/S1 の iPhone-first ワークフローで、ローカルセットアップ無しでも `/dev` から疎通とバージョンを確認できるようにするための手順をまとめます。

## 1. 前提
- Docker / Docker Compose が利用できること
- Python 実行環境は不要（テスト実行時のみ必要）
- デプロイ確認は iPhone Safari から行う

## 2. リポジトリ構成（抜粋）
```
apps/api          # FastAPI 本体
├─ app/main.py    # エンドポイント実装 (/health, /version, /dev, /)
├─ app/settings.py# 環境変数読み込み
└─ tests/         # pytest + httpx などによるテスト

.github/workflows # CI/CD (ci.yml, docker.yml, deploy.yml)
deploy/           # サーバ用 compose/Caddy テンプレ + 手順
```

## 3. 環境変数の準備
1. `.env.example` を `.env` にコピー。
2. 必要に応じて値を更新:
   - `GIT_SHA`（コミット SHA。無ければ `unknown`）
   - `PORT`（デフォルト 8080）
   - `APP_ENV`（`dev` / `prod` など表示用）
   - `BUILD_TIME`（任意。`/version` に表示）

## 4. ローカル実行
```bash
docker compose up --build
```
ブラウザで `http://localhost:8080/dev` を開き、Health/Version が表示されることを確認。

## 5. iPhone での確認
1. デプロイ環境の `https://<domain>/dev` を iPhone Safari で開く。
2. 画面に "Dev Portal" が表示され、`/health` `/version` の JSON が描画されていることを確認。
3. エラー表示が無いことを確認。

## 6. テストと lint
```bash
cd apps/api
ruff check .
pytest -q --cov=app --cov-report=term-missing --cov-fail-under=85
```

## 7. CI/CD の流れ
- `ci.yml`: ruff -> pytest(coverage>=85) -> docker smoke テスト。
- `docker.yml`: GHCR に `latest` と `sha-<commit>` タグでビルド＆プッシュ。
- `deploy.yml`: secrets が揃っていればサーバに SSH/SCP し、compose pull/up を実行（無ければ skip）。

## 8. サーバデプロイ
- 手動手順は `deploy/README.md` を参照。
- GitHub Actions で自動デプロイする場合は `DEPLOY_HOST` / `DEPLOY_USER` / `DEPLOY_SSH_KEY` などの secrets を設定。
- デプロイ後は必ず `/dev` を iPhone から確認。

## 9. トラブルシュートのヒント
- `/health` が落ちる場合: `.env` の `PORT`/`GIT_SHA` 設定やコンテナ起動ログを確認。
- `/dev` が白画面の場合: CORS/プロキシ設定を確認し、`/health` `/version` が 200 を返すか `curl` でチェック。
- deploy ワークフローが動かない場合: secrets 設定の有無と `deploy.yml` の `if` 条件を確認。
