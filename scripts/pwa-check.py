#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from nextlaw607.release_checks import pwa_issues
issues = pwa_issues(ROOT)
if issues:
    print("\n".join(issues))
    raise SystemExit(1)
print("PWA structure check PASS")
