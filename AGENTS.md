# AGENTS.md — instructions for any AI agent working in this repo

If you are an AI agent (Claude Code, opencode, n8n agent, GitHub Actions bot, anything) that writes, audits, edits, or reviews content in this repository, read this file fully before producing output.

## Voice and tone — read these skills FIRST

This repo uses an internal doctrine for writing that is non-negotiable. Before you write a single sentence for a blog post, social caption, ad, or landing page, clone and read:

```
https://github.com/DaybyDay-csv/daybyday-skills
```

Read in this order:

1. `tono-humano/SKILL.md` — voice, banned phrases, anti-IA structures (the floor)
2. `ethical-conversion-system/SKILL.md` — orchestrator (7-phase pipeline)
3. `direct-response-copy-engine/SKILL.md` — doctrine (Schwartz, Masterson, Dry)
4. `copy-estilo-jesus/SKILL.md` — frameworks F1-F6 + ethical guardrail
5. `mecanicas-atencion-hooks/SKILL.md` — hook mechanics

If you cannot reach the `daybyday-skills` repo (network failure, missing auth), **stop and tell the user**. Do not write copy without these skills loaded.

## The absolute rules (recap)

- **No bold, italic, or underline in body prose.** Headers and tables are fine.
- **No fake antithesis** ("No es X, es Y") unless both sides carry real weight.
- **No anaphora stacks.** No staccato triplets. No rhetorical-question hooks.
- **Always read the draft aloud.** Coach-in-a-BMW = rewrite. Friend-in-a-cafe = ship.
- **Invitation over pressure.** No fake urgency, no manufactured guilt.
- **Rule of One.** One idea, one reader, one promise, one action. If you find yourself writing a third promise, cut to the strongest.

## What this repo does

This is the DayByDay production website (HTML + JS + CSS, no React). It hosts:

- Marketing pages (index, servicios, contacto, problema, resultados, etc.)
- Blog at `/blog/<slug>.html` (125 posts, ~94 already Hormozi-style)
- A 6-gate build pipeline under `scripts/` that renders `.md` → `.html`, validates SEO, and pushes to IndexNow + Google Search Console
- `SKILL_BLOGPOSTING.md` — the operator guide for end-to-end blog post creation (read this in addition to the doctrine skills above)

## What you must NOT do

- **Do not edit `scripts/build-static.sh`, `scripts/rewrite-batch.mjs`, or any file under `scripts/lib/` without a passing CI run + manual review.** These are the canonical pipeline; changes break the gates for every post.
- **Do not commit to `main` directly.** All content goes through feature branches + PR. The CI pipeline runs on PRs.
- **Do not introduce new dependencies in `package.json`** without checking the `cloudflare.toml` build constraints (the site is static, no Node runtime in production).
- **Do not invent customer numbers, testimonials, or proof.** All stats come from the four anchor figures in `llms.txt`: 3,2M€ generated, 264.712€ managed, 31.555 conversions, 88,95M impressions. If you need a stat that is not in this set, ask the user.
- **Do not write a blog post without reading `SKILL_BLOGPOSTING.md`** (the operator guide for the DayByDay voice specifically) **and** the doctrine skills above.

## Pipeline gates — what runs in CI

The pipeline in `scripts/rewrite-batch.mjs` runs these in order:

1. `qa-checklist.mjs` — voice, structure, content, banned phrases, anti-IA patterns, SEO, closing
2. `verify-external-links.mjs` — every external source URL returns 200
3. `render-post.mjs` — produces `blog/<slug>.html` from `templates/post.html`
4. `seo-pack.mjs` — meta, schema, OG, hreflang
5. `verify-render.mjs <slug> --local` — render sanity check
6. `verify-internal-links.mjs` — internal href resolution

Then if all 6 pass:

7. `update-llms-txt.mjs` — append to `llms.txt`
8. `update-sitemap.mjs` — regenerate `sitemap.xml` (once per batch)
9. `indexnow.mjs` — Bing/Yandex/Seznam push
10. `gsc-push.mjs` — Google URL Inspection API push (optional)

After all pass, the source `.md` is flipped from `migration_state: "rendered"` to `"good"`.

## How to write a new post (for an AI agent)

1. Read `SKILL_BLOGPOSTING.md` AND the doctrine skills (linked above).
2. Receive the positioning thesis from the user.
3. Derive the keyword pack and external sources. Verify every URL with HEAD.
4. Pick the archetype from the 5 in `SKILL_BLOGPOSTING.md` STEP 3.
5. Write the post (1.2-1.5K words, Hormozi voice, tuteo, 4-12 word sentences).
6. Write the `.md` to `content/<slug>.md` with full frontmatter (`primary_keyword`, `secondary_keywords`, `faq[]`, `sources[]`, `migration_state: "rendered"`).
7. **Do not run the gates yourself.** Commit to a feature branch and open a PR. The CI runs the pipeline.

## Hardcoded paths you should know about

- `scripts/gsc-push.mjs` reads `GSC_CREDENTIALS_PATH` (default: `~/Downloads/DAYBYDAY/Blog System/daybyday-gsc-ca41820f3bea.json`). Override with env var in CI.
- Templates: `templates/post.html` is the single post template. Don't fork it; extend it.
- Static assets are at root. Anything you add gets deployed to `daybydayconsulting.com`.