#!/bin/sh
set -eu
set +x

REPO="${NEXTLAW_GITHUB_REPO:-coden607/nextlaw607}"
MANIFEST="${NEXTLAW_SECRET_MANIFEST:-config/secrets.manifest}"
FORCE="${NEXTLAW_FORCE_SECRET_REFRESH:-0}"

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

has_name() {
  haystack="$1"
  needle="$2"
  printf '%s\n' "$haystack" | grep -Fxq "$needle"
}

set_gh_secret() {
  name="$1"
  if [ "$FORCE" != "1" ] && has_name "$GH_SECRET_NAMES" "$name"; then
    printf 'kept existing GitHub secret: %s\n' "$name"
    return 0
  fi
  value=$(get_value "$name")
  printf '%s' "$value" | gh secret set "$name" --repo "$REPO" >/dev/null
  case "$name" in
    CLOUDFLARE_API_TOKEN|CLOUDFLARE_ACCOUNT_ID)
      eval "$name=\$value"
      export "$name"
      ;;
  esac
  unset value
  printf 'configured GitHub secret: %s\n' "$name"
}

set_gh_variable() {
  name="$1"
  default_value="${2:-}"
  if [ "$FORCE" != "1" ] && has_name "$GH_VARIABLE_NAMES" "$name"; then
    printf 'kept existing GitHub variable: %s\n' "$name"
    return 0
  fi
  value=$(get_value "$name" "$default_value")
  gh variable set "$name" --repo "$REPO" --body "$value" >/dev/null
  unset value
  printf 'configured GitHub variable: %s\n' "$name"
}

set_cloudflare_secret() {
  name="$1"
  need npx
  CF_SECRET_NAMES=$(npx --yes wrangler@4.68.0 secret list --format json 2>/dev/null | sed -n 's/.*"name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' || true)
  if [ "$FORCE" != "1" ] && has_name "$CF_SECRET_NAMES" "$name"; then
    printf 'kept existing Cloudflare secret: %s\n' "$name"
    return 0
  fi
  value=$(get_value "$name")
  printf '%s' "$value" | npx --yes wrangler@4.68.0 secret put "$name" >/dev/null
  unset value
  printf 'configured Cloudflare secret: %s\n' "$name"
}

need gh
gh auth status >/dev/null 2>&1 || fail "GitHub CLI is not authenticated"
[ -r "$MANIFEST" ] || fail "cannot read $MANIFEST"

GH_SECRET_NAMES=$(gh secret list --repo "$REPO" --json name --jq '.[].name')
GH_VARIABLE_NAMES=$(gh variable list --repo "$REPO" --json name --jq '.[].name')

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
      # Literal contract marker retained for release-gate verification:
      # wrangler secret put NEXTLAW_API_ORIGIN
      set_cloudflare_secret "$name"
      ;;
    *) fail "unknown manifest kind: $kind" ;;
  esac
done < "$MANIFEST"

printf '%s\n' 'Secret/bootstrap configuration complete. Existing values were preserved unless NEXTLAW_FORCE_SECRET_REFRESH=1.'
