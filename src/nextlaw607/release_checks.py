from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, List, Optional

_SECRET_ASSIGNMENT = re.compile(r"(?im)^\s*(OPENAI_API_KEY|COURTLISTENER_API_TOKEN|ANTHROPIC_API_KEY|GITHUB_TOKEN)\s*=\s*([^\s#]+)")
_SECRET_PREFIXES = ("sk-", "ghp_", "github_pat_", "xoxb-", "xoxp-")
_REQUIRED_ARCH_PATHS = ("apps/web", "services/api", "src/nextlaw607", "tests")


def _candidate_paths(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in {".git", "node_modules", ".venv", "__pycache__", "dist"} for part in rel.parts):
            continue
        yield rel


def secret_issues(root: Path, *, paths: Optional[Iterable[Path]] = None) -> List[str]:
    root = Path(root)
    issues: List[str] = []
    for rel in paths if paths is not None else _candidate_paths(root):
        path = root / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in _SECRET_ASSIGNMENT.finditer(text):
            value = match.group(2).strip().strip('"\'')
            if value:
                issues.append(f"{rel}: non-empty {match.group(1)} assignment")
        lowered = text.lower()
        for prefix in _SECRET_PREFIXES:
            if prefix.lower() in lowered and not str(rel).endswith("release_checks.py"):
                issues.append(f"{rel}: possible secret prefix {prefix}")
    return sorted(set(issues))


def architecture_issues(root: Path) -> List[str]:
    root = Path(root)
    return [f"missing architecture path: {rel}" for rel in _REQUIRED_ARCH_PATHS if not (root / rel).is_dir()]


def pwa_issues(root: Path) -> List[str]:
    root = Path(root)
    web = root / "apps" / "web"
    issues: List[str] = []
    manifest = web / "manifest.webmanifest"
    service_worker = web / "sw.js"
    index = web / "index.html"
    main = web / "src" / "main.ts"
    for path in (manifest, service_worker, index):
        if not path.is_file():
            issues.append(f"missing PWA file: {path.relative_to(root)}")
    if manifest.is_file():
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            issues.append("invalid PWA manifest JSON")
        else:
            for key in ("name", "start_url", "display"):
                if not payload.get(key):
                    issues.append(f"manifest missing {key}")
    registration_text = ""
    for path in (index, main):
        if path.is_file():
            registration_text += path.read_text(encoding="utf-8")
    if "serviceWorker.register" not in registration_text:
        issues.append("service worker is not registered")
    if index.is_file() and 'rel="manifest"' not in index.read_text(encoding="utf-8"):
        issues.append("manifest link missing from index.html")
    return issues
