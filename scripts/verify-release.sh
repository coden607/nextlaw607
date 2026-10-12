#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
./scripts/verify.sh
python3 scripts/browser-evidence-check.py
printf '\nNextLaw607 release verification PASS\n'
