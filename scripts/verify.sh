#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
./scripts/verify-python.sh
./scripts/verify-web.sh
python3 - <<'PY'
import json
from pathlib import Path
from nextlaw607.stack_contract import validate_stack_manifest

for path in ['package.json','apps/web/package.json','apps/web/manifest.webmanifest','.continuity/verification.json','config/production-stack.json']:
    with open(path, encoding='utf-8') as handle:
        json.load(handle)

manifest = json.loads(Path('config/production-stack.json').read_text(encoding='utf-8'))
contract = validate_stack_manifest(manifest)
print(f'JSON manifests valid; production stack contract covers {len(contract.components)} components')
PY
printf '\nNextLaw607 verification PASS\n'
