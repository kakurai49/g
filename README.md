# g

G理論学習システムのiPhone-firstなMVP。まずは FastAPI 単体で `/health` `/version` `/dev` を提供し、デプロイ後に iPhone Safari から疎通確認できることを目指します。

## エンドポイント
- `GET /health`: サービス状態とバージョンを返すJSON。
- `GET /version`: バージョンのみを返すJSON。
- `GET /dev`: Dev Portal。ブラウザ上で `/health` を fetch して結果とバージョンを表示。

## 動かし方（サーバ / ローカル）
1. `.env` を `.env.example` を参考に用意する（最低限 `GIT_SHA` と `PORT`）。
2. `docker compose up` を実行する。
3. `http://localhost:8080/dev` にアクセスして `/health` の結果が見えることを確認。

## iPhoneでの確認方法
- サーバにデプロイ後、iPhone Safari で `https://<domain>/dev` を開く。
- 画面上に "Dev Portal" と `/health` のレスポンス、バージョンが表示されていることを確認。

## 環境変数
- `GIT_SHA`: デプロイ時のコミットSHA。未設定の場合は `unknown` として表示されます。

## 開発メモ
- 依存は FastAPI + uvicorn のみ（開発用に pytest/httpx/ruff）。
- CI では `ruff check` と `pytest` を実行します。
