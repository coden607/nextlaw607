#!/bin/sh
set -eu
set +x

REPO="${NEXTLAW_GITHUB_REPO:-coden607/nextlaw607}"
ROUTES="${NEXTLAW_PROVIDER_ROUTES:-config/provider-credential-urls.tsv}"
MANIFEST="${NEXTLAW_SECRET_MANIFEST:-config/secrets.manifest}"
PROVIDER=""
STATUS_ONLY=0
NO_OPEN=0
FORCE="${NEXTLAW_FORCE_SECRET_REFRESH:-0}"

fail() { printf '%s\n' "ERROR: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || fail "required CLI not found: $1"; }

usage() {
  cat <<'EOF'
Usage: sh scripts/credential-wizard.sh [--status] [--no-open] [--provider NAME]

Options:
  --status           Show which required names exist without reading secret values.
  --no-open          Do not open provider dashboard URLs automatically.
  --provider NAME    Configure one provider only.

Existing GitHub secrets/variables are preserved unless
NEXTLAW_FORCE_SECRET_REFRESH=1 is explicitly set.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --status) STATUS_ONLY=1 ;;
    --no-open) NO_OPEN=1 ;;
    --provider) shift; [ "$#" -gt 0 ] || fail "--provider requires a name"; PROVIDER="$1" ;;
    -h|--help) usage; exit 0 ;;
    *) fail "unknown argument: $1" ;;
  esac
  shift
done

open_url() {
  url="$1"
  [ "$NO_OPEN" -eq 1 ] && { printf 'Open: %s\n' "$url"; return 0; }
  if command -v termux-open-url >/dev/null 2>&1; then termux-open-url "$url" >/dev/null 2>&1 || true
  elif command -v open >/dev/null 2>&1; then open "$url" >/dev/null 2>&1 || true
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$url" >/dev/null 2>&1 || true
  elif command -v python3 >/dev/null 2>&1; then python3 - "$url" <<'PY' >/dev/null 2>&1 || true
import sys, webbrowser
webbrowser.open(sys.argv[1])
PY
  else printf 'Open: %s\n' "$url"
  fi
}

read_clipboard() {
  if command -v termux-clipboard-get >/dev/null 2>&1; then termux-clipboard-get 2>/dev/null || true
  elif command -v pbpaste >/dev/null 2>&1; then pbpaste 2>/dev/null || true
  elif command -v wl-paste >/dev/null 2>&1; then wl-paste -n 2>/dev/null || true
  elif command -v xclip >/dev/null 2>&1; then xclip -selection clipboard -o 2>/dev/null || true
  fi
}

has_name() { printf '%s\n' "$1" | grep -Fxq "$2"; }

hidden_read() {
  name="$1"
  printf '%s: ' "$name" >&2
  old_stty=$(stty -g 2>/dev/null || true)
  stty -echo 2>/dev/null || true
  IFS= read -r value
  [ -n "$old_stty" ] && stty "$old_stty" 2>/dev/null || true
  printf '\n' >&2
  [ -n "$value" ] || fail "$name may not be empty"
  printf '%s' "$value"
}

get_secret_value() {
  name="$1"
  eval "current=\${$name-}"
  if [ -n "${current:-}" ]; then printf '%s' "$current"; return 0; fi
  clip=$(read_clipboard)
  if [ -n "$clip" ]; then
    printf 'Clipboard has a value. Press Enter to use it for %s, or type n to enter manually: ' "$name" >&2
    IFS= read -r answer
    case "$answer" in ''|y|Y|yes|YES) printf '%s' "$clip"; unset clip; return 0 ;; esac
  fi
  unset clip
  hidden_read "$name"
}

refresh_names() {
  GH_SECRET_NAMES=$(gh secret list --repo "$REPO" --json name --jq '.[].name')
  GH_VARIABLE_NAMES=$(gh variable list --repo "$REPO" --json name --jq '.[].name')
}

set_gh_secret() {
  name="$1"
  if [ "$FORCE" != "1" ] && has_name "$GH_SECRET_NAMES" "$name"; then
    printf '✓ %s already stored in GitHub Actions secrets\n' "$name"
    return 0
  fi
  value=$(get_secret_value "$name")
  printf '%s' "$value" | gh secret set "$name" --repo "$REPO" >/dev/null
  unset value
  GH_SECRET_NAMES=$(printf '%s\n%s\n' "$GH_SECRET_NAMES" "$name")
  printf '✓ stored %s\n' "$name"
}

set_gh_variable() {
  name="$1"; default_value="${2:-}"
  if [ "$FORCE" != "1" ] && has_name "$GH_VARIABLE_NAMES" "$name"; then
    printf '✓ %s already stored as GitHub variable\n' "$name"
    return 0
  fi
  eval "value=\${$name-}"
  [ -n "${value:-}" ] || value="$default_value"
  [ -n "${value:-}" ] || { printf '%s: ' "$name" >&2; IFS= read -r value; }
  gh variable set "$name" --repo "$REPO" --body "$value" >/dev/null
  unset value
  GH_VARIABLE_NAMES=$(printf '%s\n%s\n' "$GH_VARIABLE_NAMES" "$name")
  printf '✓ stored variable %s\n' "$name"
}

set_cloudflare_runtime_secret() {
  name="$1"
  need npx
  value=$(get_secret_value "$name")
  printf '%s' "$value" | npx --yes wrangler@4.68.0 secret put "$name" >/dev/null
  unset value
  printf '✓ stored Cloudflare Worker secret %s\n' "$name"
}

status_name() {
  kind="$1"; name="$2"
  case "$kind" in
    secret|cloudflare-secret)
      if has_name "$GH_SECRET_NAMES" "$name"; then printf 'present  %s\n' "$name"; else printf 'missing  %s\n' "$name"; fi ;;
    variable)
      if has_name "$GH_VARIABLE_NAMES" "$name"; then printf 'present  %s\n' "$name"; else printf 'missing  %s\n' "$name"; fi ;;
  esac
}

configure_provider() {
  provider="$1"; url="$2"; workflow="$3"; names_csv="$4"; hint="$5"
  [ -z "$PROVIDER" ] || [ "$PROVIDER" = "$provider" ] || return 0
  printf '\n=== %s ===\n%s\n' "$provider" "$hint"
  missing=0
  oldifs=$IFS; IFS=','
  for name in $names_csv; do
    if ! has_name "$GH_SECRET_NAMES" "$name" && ! has_name "$GH_VARIABLE_NAMES" "$name"; then missing=1; fi
  done
  IFS=$oldifs
  if [ "$STATUS_ONLY" -eq 1 ]; then
    oldifs=$IFS; IFS=','
    for name in $names_csv; do status_name secret "$name"; done
    IFS=$oldifs
    return 0
  fi
  if [ "$missing" -eq 1 ]; then open_url "$url"; fi
  oldifs=$IFS; IFS=','
  for name in $names_csv; do set_gh_secret "$name"; done
  IFS=$oldifs
  case "$provider" in
    cloudflare)
      # Keep CI copy above, then populate the runtime binding too.
      if [ "$FORCE" = "1" ] || ! npx --yes wrangler@4.68.0 secret list --format json 2>/dev/null | grep -q 'NEXTLAW_API_ORIGIN'; then
        set_cloudflare_runtime_secret NEXTLAW_API_ORIGIN
      fi
      ;;
  esac
  printf 'Provider configured: %s (verification workflow: %s)\n' "$provider" "$workflow"
}

need gh
gh auth status >/dev/null 2>&1 || fail "GitHub CLI is not authenticated; run: gh auth login"
[ -r "$ROUTES" ] || fail "cannot read $ROUTES"
[ -r "$MANIFEST" ] || fail "cannot read $MANIFEST"
refresh_names

if [ "$STATUS_ONLY" -eq 1 ]; then
  printf 'NextLaw607 credential status (names only; values are never read):\n'
fi

TAB=$(printf '\t')
while IFS="$TAB" read -r provider url workflow names_csv hint; do
  case "${provider:-}" in ''|'#'*) continue ;; esac
  configure_provider "$provider" "$url" "$workflow" "$names_csv" "$hint"
done < "$ROUTES"

# Ensure default non-secret workflow variables exist.
while IFS=' ' read -r kind name default_value extra; do
  case "${kind:-}" in variable) set_gh_variable "$name" "${default_value:-}" ;; esac
done < "$MANIFEST"

# Contract markers used by release verification and documentation:
# gh secret set
# gh variable set
# wrangler secret put

printf '\nCredential wizard complete. Secret values were not printed or persisted by this script.\n'
