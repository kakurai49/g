#!/usr/bin/env bash
set -u
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR%/scripts}"
cd "$PROJECT_ROOT"

CONTEXT="${DOCKER_CONTEXT:-default}"
STATUS=0

print_ok() {
  printf '[OK] %s
' "$1"
}

print_ng() {
  printf '[NG] %s
' "$1"
  STATUS=1
}

print_info() {
  printf '[INFO] %s
' "$1"
}

if ! command -v docker >/dev/null 2>&1; then
  print_ng "docker コマンドが見つかりません。docs/local-dev-ubuntu24-docker.md を参照してインストールしてください。"
  echo "全てのチェックは docker が導入されてから再実行してください。"
  exit 1
else
  print_ok "docker コマンドを検出しました。"
fi

if docker --context "$CONTEXT" info >/dev/null 2>&1; then
  print_ok "docker --context \"$CONTEXT\" info が成功しました。デーモンと疎通しています。"
else
  print_ng "docker --context \"$CONTEXT\" info に失敗しました。Docker デーモンや context 設定を確認してください。"
  print_info "ローカルの場合: sudo systemctl status docker / restart docker。リモートの場合: docker context ls で設定を確認。"
fi

if docker --context "$CONTEXT" compose version >/dev/null 2>&1; then
  print_ok "docker compose plugin が利用可能です。"
else
  print_ng "docker compose plugin が見つからないか実行に失敗しました。インストール状態を確認してください。"
fi

if [ -f .env ]; then
  print_ok ".env を検出しました。"
else
  print_ng ".env が見つかりません。必要に応じて 'cp .env.example .env' を実行し、値を設定してください。"
fi

if [ "$STATUS" -eq 0 ]; then
  print_info "次のステップ例: ./scripts/compose.sh up -d --build でサービスを起動し、ブラウザで http://localhost:8080/dev を確認。"
  exit 0
else
  echo "---"
  print_info "問題が解決したら再度 ./scripts/doctor.sh を実行してください。"
  exit 1
fi
