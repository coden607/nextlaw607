#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from nextlaw607.release_readiness import assess_production_readiness


def main() -> int:
    parser = argparse.ArgumentParser(description="Report fail-closed NextLaw607 production readiness")
    parser.add_argument("--require-ready", action="store_true", help="exit nonzero when required components are not verified")
    args = parser.parse_args()

    manifest = json.loads(Path("config/production-stack.json").read_text(encoding="utf-8"))
    result = assess_production_readiness(manifest)
    payload = {
        "schema_version": 1,
        "revision": os.environ.get("GITHUB_SHA", "unknown"),
        "ready": result.ready,
        "blockers": list(result.blockers),
    }
    print(json.dumps(payload, sort_keys=True))
    return 1 if args.require_ready and not result.ready else 0


if __name__ == "__main__":
    raise SystemExit(main())
