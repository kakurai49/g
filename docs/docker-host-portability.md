# Docker ホスト差し替えポータビリティ設計

現状は **ローカル PC = Docker ホスト** として運用しますが、将来的に **リモートサーバ = Docker ホスト** へ移行しても同じコマンド体系を維持する方針を明文化します。

## 基本方針
- Docker の接続先は **Docker context** で切り替える。
- 全ての compose 操作は `./scripts/compose.sh`（内部で `docker --context "$DOCKER_CONTEXT" compose` を呼ぶ）経由に統一。
- **コマンドは変えずに** `DOCKER_CONTEXT` の値だけ差し替えることで、ローカルでもリモートでも同じ手順を実行できる。

## Docker context の追加例（ssh 経由）
```bash
# リモートホストを context "remote" として登録
docker context create remote \
  --docker "host=ssh://<user>@<remote-host>"

# 確認
docker context ls
```

## 運用時の使い方
```bash
# ローカル（default context）で起動する場合
./scripts/compose.sh up -d

# リモートホストに切り替えて起動する場合
DOCKER_CONTEXT=remote ./scripts/compose.sh up -d
```
- すべての compose オプションはそのまま透過的に渡せます（例: `logs`, `pull`, `down` など）。
- context 未設定時は `default` とみなし、ローカル Docker デーモンに接続します。

## 移行チェックリスト（local → remote）
- [ ] リモートホストに Docker Engine + Compose plugin がインストールされている。
- [ ] `docker context create` でリモートを登録し、`docker --context remote info` が成功する。
- [ ] `.env` をリモート側にも配置（秘密は安全な経路で配布）。
- [ ] `DOCKER_CONTEXT=remote ./scripts/compose.sh pull` が成功する。
- [ ] `DOCKER_CONTEXT=remote ./scripts/compose.sh up -d --remove-orphans` で起動する。
- [ ] iPhone から `http(s)://<remote-host>:8080/dev` にアクセスして `/health` `/version` が確認できる。
- [ ] 不要になったローカルリソース（古い context、イメージ）を整理する。

## ヒント
- context 名は `remote` 以外でも任意。`DOCKER_CONTEXT` の値と一致させれば OK です。
- SSH 秘密鍵や `.env` は Git にコミットしないでください。
- ネットワーク遅延が大きい場合は、`logs -f` などストリーミング系操作が重くなるため、必要に応じて `--tail` を付与してください。
