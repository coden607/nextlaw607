#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
fail() { printf 'Continuity preflight FAIL: %s\n' "$*" >&2; exit 1; }
pass() { printf 'Continuity preflight PASS: %s\n' "$*"; }
[ -f AGENTS.md ] || fail "AGENTS.md missing"
[ -f continuity.toml ] || fail "continuity.toml missing"
[ -f docs/nextlaw607-ny-criminal-intelligence.prd.md ] || fail "NY criminal PRD missing"
[ -f docs/nextlaw607-ny-criminal-continuity-architecture.md ] || fail "Continuity architecture contract missing"
grep -q "Continuity OS Universal Directives" AGENTS.md || fail "Continuity universal directives missing"
grep -q "NextLaw607 NY Criminal build contract" AGENTS.md || fail "NextLaw build contract missing"
grep -q "compress-token-spend" AGENTS.md || fail "compress-token-spend directive missing"
grep -q "legal-war-room" AGENTS.md || fail "legal-war-room directive missing"
if command -v continuity >/dev/null 2>&1; then
  continuity config-check continuity.toml
  pass "continuity.toml accepted by Continuity CLI"
else
  printf 'Continuity preflight NOTE: continuity CLI unavailable; static contract checks only.\n'
fi
SKILLS_ROOT="${CODEN607_SKILLS_ROOT:-$HOME/.coden607/skills}"
if [ -d "$SKILLS_ROOT" ]; then
  for skill in compress-token-spend route-with-jev route-interrupts maintain-second-brain isolate-agent-runs enforce-with-hooks run-software-factory legal-war-room; do
    [ -f "$SKILLS_ROOT/$skill/SKILL.md" ] || fail "canonical skill missing: $skill"
  done
  pass "required canonical skills available"
else
  printf 'Continuity preflight NOTE: canonical skill mount unavailable at %s; repository contract checks still enforced.\n' "$SKILLS_ROOT"
fi
pass "repository routing contract intact"
