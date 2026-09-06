#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nextlaw607.release_checks import browser_evidence_issues


def main() -> int:
    metadata = json.loads((ROOT / ".continuity" / "verification.json").read_text(encoding="utf-8"))
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    issues = browser_evidence_issues(ROOT, metadata=metadata, revision=revision)
    if issues:
        for issue in issues:
            print(f"browser evidence: FAIL: {issue}")
        return 1
    print("browser evidence: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
