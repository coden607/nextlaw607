#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
./scripts/verify-python.sh
./scripts/verify-web.sh
python3 scripts/browser-evidence-check.py
python3 - <<'PY'
import json
for path in ['package.json','apps/web/package.json','apps/web/manifest.webmanifest','.continuity/verification.json']:
    with open(path, encoding='utf-8') as handle:
        json.load(handle)
print('JSON manifests valid')
PY
printf '\nNextLaw607 verification PASS\n'
