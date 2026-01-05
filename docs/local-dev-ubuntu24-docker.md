# Ubuntu 24.04 でのローカル開発用 Docker/Compose セットアップ

この手順では **単一の Ubuntu 24.04 PC を Docker ホスト** として使いつつ、将来 Docker ホストを差し替えても同じコマンドで動かせる構成を整えます。スマホ（iPhone）からの確認を想定し、LAN 内の IP でアクセスする流れも記載しています。

## 前提
- Ubuntu 24.04（sudo 可能なユーザー）
- `.env` はコミットしない。雛形として `.env.example` を利用
- `docker-compose.yml` がリポジトリ直下にあること

## Docker Engine + Compose plugin の導入（コピペ手順）
既存の古いパッケージを削除し、Docker 公式リポジトリからインストールします。

```bash
# 1) 古いパッケージを削除
sudo apt-get remove docker docker-engine docker.io containerd runc || true

# 2) 依存とリポジトリ設定
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 3) Docker Engine と Compose plugin をインストール
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

> sudo 無し運用は任意です。`docker` グループは実質 root 権限となるため、追加する場合はリスクを理解した上で運用してください。

## デーモン確認と疎通チェック
```bash
# systemd でデーモン状態を確認
sudo systemctl status docker

# hello-world で疎通確認
sudo docker run --rm hello-world
```
`hello-world` のメッセージが表示されれば Engine/ネットワークが正常です。

## 環境変数ファイルの用意
リポジトリ直下で `.env.example` を `.env` にコピーし、必要に応じて値を編集します。

```bash
cp .env.example .env
```
> `.env` は Git にコミットしないでください。`.gitignore` に登録済みです。

## compose 起動（ホスト差し替え対応版）
Docker ホストの指定を `DOCKER_CONTEXT` 環境変数に集約するため、**常に専用スクリプトを経由**します。

```bash
# 例: ローカルホストに対して起動
./scripts/doctor.sh
./scripts/compose.sh up -d --build

# 停止
./scripts/compose.sh down
```
- `DOCKER_CONTEXT` を未設定（空）の場合、`default` を利用します。
- 将来リモートホストへ移行しても、`DOCKER_CONTEXT=remote ./scripts/compose.sh up -d` のように **環境変数を変えるだけ**で同じコマンド体系を使えます。

## iPhone からの確認方法（同一 LAN を想定）
1. Docker を動かしている PC の IP を確認: `hostname -I | awk '{print $1}'`
2. iPhone Safari で `http://<上で確認したIP>:8080/dev` を開く。
3. 画面に `/health` と `/version` の内容が表示されれば OK。

外部公開前でも、同一 LAN 内なら IP:PORT でアクセスできます。ポートや FW 設定が閉じている場合は OS のファイアウォール設定を確認してください。

## よくある詰まりと対処
- **`docker: command not found`**: 上記のインストール手順を再実行する。
- **`permission denied while trying to connect to the Docker daemon socket`**: `sudo docker ...` で動くか確認。sudo なし運用をしたい場合は `docker` グループに追加するが、権限リスクに注意。
- **`hello-world` が失敗する**: `sudo systemctl status docker` でデーモン稼働を確認し、`sudo systemctl restart docker` で再起動を試す。
- **`./scripts/compose.sh` がリモートを掴まない**: `DOCKER_CONTEXT` が意図通りか `echo $DOCKER_CONTEXT` で確認し、`docker context ls` で登録状況を確認する。
- **アプリが外部から見えない**: `docker-compose.yml` のポート (`8080:8080`) を確認し、iPhone が同一ネットワークにいるかチェックする。

### 実際に解消した手順メモ（daemon/socket への接続権限）
以下の流れで `permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock` を解消できた実績があります。

1. デーモンが停止している場合があるため、まず起動する  
   ```bash
   sudo systemctl start docker
   ```
2. sudo なしで使いたいユーザーを `docker` グループに追加する  
   ```bash
   sudo usermod -aG docker "$USER"
   ```
3. グループを反映するため新しいログインセッションを開始する（`newgrp docker` でも可）
4. グループに入ったことを確認する  
   ```bash
   id   # groups に docker が含まれることを確認
   ```
5. 権限が反映された状態で疎通を確認する  
   ```bash
   docker ps
   ```
   ソケットの所有者が `root:docker` でパーミッション `srw-rw----` になっていることも `ls -l /var/run/docker.sock` で確認すると安心です。必要に応じて `sudo systemctl restart docker` で再起動して反映させます。

### 再起動後も Docker を自動起動させる
PC を再起動した際に Docker デーモンが自動で立ち上がるよう、`enable` を設定しておくと便利です。
```bash
sudo systemctl enable docker
```
