#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

cleanup(){
  [ -n "${API_PID:-}" ] && kill "$API_PID" 2>/dev/null || true
  [ -n "${WEB_PID:-}" ] && kill "$WEB_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

if python3 -c 'import fastapi, uvicorn' >/dev/null 2>&1; then
  PYTHONPATH="${PYTHONPATH:-}:$ROOT/src:$ROOT" python3 -m uvicorn services.api.main:app --host 0.0.0.0 --port "${NEXTLAW_API_PORT:-8000}" & API_PID=$!
else
  PYTHONPATH="${PYTHONPATH:-}:$ROOT/src:$ROOT" NEXTLAW_API_PORT="${NEXTLAW_API_PORT:-8000}" python3 scripts/api_fallback.py & API_PID=$!
fi
(
  cd apps/web
  if command -v tsc >/dev/null 2>&1; then tsc -p tsconfig.json; else ./node_modules/.bin/tsc -p tsconfig.json; fi
  PORT="${NEXTLAW_WEB_PORT:-4173}" NEXTLAW_API_ORIGIN="http://127.0.0.1:${NEXTLAW_API_PORT:-8000}" node server.mjs
) & WEB_PID=$!

echo "NextLaw607 API: http://127.0.0.1:${NEXTLAW_API_PORT:-8000}"
echo "NextLaw607 PWA: http://127.0.0.1:${NEXTLAW_WEB_PORT:-4173}"
wait "$API_PID" "$WEB_PID"
