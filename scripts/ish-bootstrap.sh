#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

if command -v apk >/dev/null 2>&1; then
  apk add --no-cache python3 nodejs npm git ca-certificates
fi

npm --prefix apps/web install --no-audit --no-fund

PYTHONPATH="$ROOT/src:$ROOT" python3 - <<'PY'
from services.api.fallback import dispatch
status, body = dispatch("GET", "/status/live", None)
assert status == 200 and body == {"status": "live"}
status, body = dispatch("POST", "/api/live", {"mode": "search", "user_goal": "protect my rights"})
assert status == 200 and body.get("verified_authority") is False
print("NextLaw607 fallback API smoke PASS")
PY

npm --prefix apps/web run build
printf '\nNextLaw607 iSH bootstrap PASS\nRun: ./scripts/dev.sh\nOpen: http://127.0.0.1:4173\n'
