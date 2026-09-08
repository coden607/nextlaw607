from __future__ import annotations

import json
import os
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


def test_readiness_cli_prefers_explicit_exact_revision_over_synthetic_ci_sha() -> None:
    env = os.environ.copy()
    env["GITHUB_SHA"] = "synthetic-merge-sha"
    env["NEXTLAW_EXACT_REVISION"] = "feature-head-sha"
    result = subprocess.run(
        [sys.executable, "scripts/production-readiness-check.py"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )

    assert json.loads(result.stdout)["revision"] == "feature-head-sha"


def test_ci_publishes_exact_revision_readiness_report() -> None:
    workflow = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "production-readiness-report:" in workflow
    assert "scripts/production-readiness-check.py" in workflow
    assert "production-readiness-${{ github.event.pull_request.head.sha || github.sha }}" in workflow
    assert "NEXTLAW_EXACT_REVISION: ${{ github.event.pull_request.head.sha || github.sha }}" in workflow
