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
  echo "==> [$slug] verifying external links"
  if ! node scripts/verify-external-links.mjs "$slug"; then
    echo "    verify-external-links found broken external URLs. Fix or remove them, then retry."
    return 1
  fi
  echo "==> [$slug] rendering"
  node scripts/render-post.mjs "$slug"
  echo "==> [$slug] seo-pack validation"
  node scripts/seo-pack.mjs "$slug"
  echo "==> [$slug] verify-render (local)"
  node scripts/verify-render.mjs "$slug" --local
  echo "==> [$slug] verify-internal-links"
  node scripts/verify-internal-links.mjs "$slug"
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
      # Skip legacy sources that have not been rewritten by the pipeline.
      # Two markers indicate the source is still a skeleton:
      #   1) frontmatter `migration_state: "rendered"`
      #   2) literal placeholder `[BODY-TO-REWRITE]` in the body
      if grep -q '^migration_state:[[:space:]]*"rendered"' "$md"; then
        echo "  skip $slug (migration_state: rendered — legacy, not pipeline-ready)"
        continue
      fi
      if grep -q '\[BODY-TO-REWRITE\]' "$md"; then
        echo "  skip $slug (contains [BODY-TO-REWRITE] — legacy, not pipeline-ready)"
        continue
      fi
      render_one "$slug" || echo "Skipped $slug"
    fi
  done
elif [[ -n "${1:-}" ]]; then
  render_one "$1"
else
  echo "Usage: bash scripts/build-static.sh <slug> | --migrate | --all"
  exit 1
fi
