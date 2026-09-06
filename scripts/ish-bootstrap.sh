#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
command -v apk >/dev/null 2>&1 && apk add --no-cache python3 py3-pip nodejs npm git ca-certificates || true
python3 -m venv .venv 2>/dev/null || true
if [ -f .venv/bin/activate ]; then . .venv/bin/activate; fi
python -m pip install --upgrade pip
python -m pip install -e . fastapi uvicorn httpx pytest
npm --prefix apps/web install --no-audit --no-fund
./scripts/verify.sh
printf '\nInstalled. Run: ./scripts/dev.sh\n'
