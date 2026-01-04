# アーキテクチャ（Phase1 / S1）

- **W (Why):** ローカル環境を使わずに、iPhone Safari からサービスの健全性を即確認できる観測点を用意する。
- **E (End state):** デプロイ後に `/health` `/version` `/dev` へ到達でき、`/dev` でヘルスとバージョンの JSON が表示される。
- **S (Scope):** 単一 FastAPI サービス（apps/api）を Docker/Compose で提供。データ層は未導入だが将来拡張できる構成を維持。
- **A (Approach):** JSON エンドポイント + 静的 Dev Portal を FastAPI で提供し、CI（lint/test/coverage + docker smoke）と GHCR ビルド、SSH ベースの任意デプロイを自動化。
- **S (Signals):** iPhone で `/dev` にアクセスすると `/health` `/version` がライブ表示されること、CI が ruff + pytest + docker smoke でグリーン、GHCR に `latest` と `sha-*` が公開、secrets 無しの環境でデプロイが安全に skip されること。

Phase1 ではまず `/dev` を観測点として整備し、その周辺に CI/CD を敷設することで毎回 iPhone からの確認を可能にする。
