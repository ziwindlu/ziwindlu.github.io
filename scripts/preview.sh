#!/usr/bin/env bash
# 本地常驻预览服务的启动/停止/状态。
# 用法：
#   scripts/preview.sh start     # 在 127.0.0.1 上后台启动 hugo server，写日志与 PID
#   scripts/preview.sh stop      # 停止
#   scripts/preview.sh restart   # 重启（换源重建后用）
#   scripts/preview.sh status    # 看状态与 HTTP 响应码
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-1313}"
DIR=".preview"
LOG="$DIR/hugo.log"
PIDFILE="$DIR/hugo.pid"
URL="http://127.0.0.1:${PORT}/"

mkdir -p "$DIR"

is_listening() { lsof -nP -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1; }

running_pid() {
  [ -f "$PIDFILE" ] || return 1
  local pid; pid="$(cat "$PIDFILE" 2>/dev/null || true)"
  [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null && echo "$pid"
}

http_code() { curl -sS -o /dev/null -w '%{http_code}' --max-time 5 "$URL" || echo "000"; }

start() {
  local pid
  if pid="$(running_pid)"; then
    echo "预览已在运行：pid=$pid → $URL"
    return 0
  fi
  while is_listening "$PORT"; do
    echo "端口 $PORT 被占用，试 $((PORT + 1))"
    PORT=$((PORT + 1))
    [ "$PORT" -gt 1400 ] && { echo "!! 找不到空闲端口"; exit 1; }
  done
  URL="http://127.0.0.1:${PORT}/"

  # 双 fork + setsid：脱离调用方的会话/进程组，调用方退出不会把它带走
  rm -f "$PIDFILE"
  python3 scripts/daemonize.py --pidfile "$PIDFILE" --log "$LOG" -- \
    hugo server \
      --bind 127.0.0.1 --port "$PORT" --baseURL "http://127.0.0.1:$PORT/" \
      --appendPort=false --renderToMemory --disableFastRender --logLevel warn
  echo "启动中：pid=$(cat "$PIDFILE" 2>/dev/null || echo '?') port=$PORT log=$PWD/$LOG"

  local code="000"
  for _ in $(seq 1 60); do
    code="$(http_code)"
    [ "$code" = "200" ] && break
    sleep 0.5
  done
  if [ "$code" = "200" ]; then
    echo "OK $URL → 200"
  else
    echo "!! 预览未就绪（HTTP $code），日志尾部："
    tail -30 "$LOG" || true
    exit 1
  fi
}

stop() {
  local pid
  if ! pid="$(running_pid)"; then
    echo "没有在跑的预览进程（$PIDFILE）"
    rm -f "$PIDFILE"
    return 0
  fi
  kill "$pid" 2>/dev/null || true
  for _ in $(seq 1 20); do
    kill -0 "$pid" 2>/dev/null || break
    sleep 0.2
  done
  kill -9 "$pid" 2>/dev/null || true
  rm -f "$PIDFILE"
  echo "已停止 pid=$pid"
}

status() {
  local pid
  if pid="$(running_pid)"; then
    echo "运行中 pid=$pid url=$URL http=$(http_code)"
  else
    echo "未运行（pid 文件：$PWD/$PIDFILE）"
  fi
}

case "${1:-status}" in
  start) start ;;
  stop) stop ;;
  restart) stop; start ;;
  status) status ;;
  *) echo "用法: $0 {start|stop|restart|status}"; exit 2 ;;
esac
