from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_readiness_cli_reports_blockers_without_masking_other_ci_evidence() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/production-readiness-check.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["ready"] is False
    assert "cloudflare" in payload["blockers"]
    assert "citation-firewall" in payload["blockers"]


def test_readiness_cli_can_fail_closed_for_an_actual_release_attempt() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/production-readiness-check.py", "--require-ready"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert '"ready": false' in result.stdout


def test_ci_publishes_exact_revision_readiness_report() -> None:
    workflow = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "production-readiness-report:" in workflow
    assert "scripts/production-readiness-check.py" in workflow
    assert "production-readiness-${{ github.sha }}" in workflow
