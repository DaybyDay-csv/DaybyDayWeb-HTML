#!/usr/bin/env bash
# build-static.sh — entrypoint for the blogposting pipeline
# Usage:
#   bash scripts/build-static.sh <slug>     # render + validate + push a single new post
#   bash scripts/build-static.sh --migrate   # inventory the legacy 69 broken posts
#   bash scripts/build-static.sh --all      # render every content/*.md that doesn't have a matching blog/<slug>.html

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ "${1:-}" == "--migrate" ]]; then
  echo "==> Migrating legacy posts"
  node scripts/migrate-legacy.mjs
  exit $?
fi

render_one() {
  local slug="$1"
  echo ""
  echo "==> [$slug] running qa-checklist"
  if ! node scripts/qa-checklist.mjs "$slug"; then
    local rc=$?
    if [[ $rc -eq 2 ]]; then
      echo "    qa-checklist returned REGENERAR (banned phrases or severe issues). Fix the source."
    elif [[ $rc -eq 3 ]]; then
      echo "    qa-checklist returned REESCRIBIR (some blocks to fix)."
    fi
    return $rc
  fi
  echo "==> [$slug] rendering"
  node scripts/render-post.mjs "$slug"
  echo "==> [$slug] seo-pack validation"
  node scripts/seo-pack.mjs "$slug"
  echo "==> [$slug] verify-render (local)"
  node scripts/verify-render.mjs "$slug" --local
  echo "==> [$slug] update-llms-txt"
  node scripts/update-llms-txt.mjs "$slug"
  echo "==> [$slug] update-sitemap"
  node scripts/update-sitemap.mjs
  echo "==> [$slug] indexnow"
  node scripts/indexnow.mjs "/blog/$slug.html"
  echo "==> [$slug] gsc-push"
  node scripts/gsc-push.mjs "/blog/$slug.html"
  echo ""
  echo "==> [$slug] DONE"
}

if [[ "${1:-}" == "--all" ]]; then
  for md in content/*.md; do
    [[ "$(basename "$md")" == _* ]] && continue
    slug=$(basename "$md" .md)
    if [[ ! -f "blog/$slug.html" ]]; then
      render_one "$slug" || echo "Skipped $slug"
    fi
  done
elif [[ -n "${1:-}" ]]; then
  render_one "$1"
else
  echo "Usage: bash scripts/build-static.sh <slug> | --migrate | --all"
  exit 1
fi
