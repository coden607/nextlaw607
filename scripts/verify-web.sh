#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
if command -v tsc >/dev/null 2>&1; then
  (cd apps/web && tsc -p tsconfig.json)
elif [ -x apps/web/node_modules/.bin/tsc ]; then
  (cd apps/web && ./node_modules/.bin/tsc -p tsconfig.json)
else
  echo "TypeScript compiler missing; run npm --prefix apps/web install" >&2
  exit 1
fi
node apps/web/tests/run.mjs
