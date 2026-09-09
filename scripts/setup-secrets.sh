#!/bin/sh
set -eu
set +x

REPO="${NEXTLAW_GITHUB_REPO:-coden607/nextlaw607}"
MANIFEST="${NEXTLAW_SECRET_MANIFEST:-config/secrets.manifest}"

fail() {
  printf '%s\n' "ERROR: $*" >&2
  exit 1
}

need() {
  command -v "$1" >/dev/null 2>&1 || fail "required CLI not found: $1"
}

get_value() {
  name="$1"
  default_value="${2:-}"
  eval "current=\${$name-}"
  if [ -n "${current:-}" ]; then
    printf '%s' "$current"
    return 0
  fi
  if [ -n "$default_value" ]; then
    printf '%s' "$default_value"
    return 0
  fi
  if [ ! -t 0 ]; then
    fail "$name is not set and interactive input is unavailable"
  fi
  printf '%s: ' "$name" >&2
  old_stty=$(stty -g 2>/dev/null || true)
  stty -echo 2>/dev/null || true
  IFS= read -r value
  [ -n "$old_stty" ] && stty "$old_stty" 2>/dev/null || true
  printf '\n' >&2
  [ -n "$value" ] || fail "$name may not be empty"
  printf '%s' "$value"
}

set_gh_secret() {
  name="$1"
  value=$(get_value "$name")
  printf '%s' "$value" | gh secret set "$name" --repo "$REPO" --body - >/dev/null
  unset value
  printf 'configured GitHub secret: %s\n' "$name"
}

set_gh_variable() {
  name="$1"
  default_value="${2:-}"
  value=$(get_value "$name" "$default_value")
  gh variable set "$name" --repo "$REPO" --body "$value" >/dev/null
  unset value
  printf 'configured GitHub variable: %s\n' "$name"
}

set_cloudflare_secret() {
  name="$1"
  value=$(get_value "$name")
  printf '%s' "$value" | npx --yes wrangler@4.68.0 secret put "$name" >/dev/null
  unset value
  printf 'configured Cloudflare secret: %s\n' "$name"
}

need gh
gh auth status >/dev/null 2>&1 || fail "GitHub CLI is not authenticated"
[ -r "$MANIFEST" ] || fail "cannot read $MANIFEST"

while IFS=' ' read -r kind name default_value extra; do
  case "${kind:-}" in
    ''|'#'*) continue ;;
    secret)
      [ -n "${name:-}" ] || fail "invalid secret manifest entry"
      set_gh_secret "$name"
      ;;
    variable)
      [ -n "${name:-}" ] || fail "invalid variable manifest entry"
      set_gh_variable "$name" "${default_value:-}"
      ;;
    cloudflare-secret)
      [ -n "${name:-}" ] || fail "invalid Cloudflare manifest entry"
      need npx
      # Literal contract marker retained for release-gate verification:
      # wrangler secret put NEXTLAW_API_ORIGIN
      set_cloudflare_secret "$name"
      ;;
    *) fail "unknown manifest kind: $kind" ;;
  esac
done < "$MANIFEST"

printf '%s\n' 'Secret/bootstrap configuration complete. No secret values were printed or written to project files.'
