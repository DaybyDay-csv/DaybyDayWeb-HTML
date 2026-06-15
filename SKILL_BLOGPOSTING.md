---
name: daybyday-blogposting
description: 
  Full-pipeline blogposting system for DayByDay. Operates the static-export pipeline (Markdown → blog/<slug>.html) end-to-end. Covers research, writing, QA against the Hormozi checklist, SEO/GEO/AEO/AVO packaging, llms.txt + sitemap updates, IndexNow + GSC indexation. Trigger when the user says "publish a new post", "write a post about [positioning point]", "run the blog pipeline", or "next article". Always trigger as the full pipeline driver — no manual steps.
---

# DayByDay Blogposting System

## Purpose

End-to-end operator for the DayByDay blog. Owns the full lifecycle of a post: from positioning brief to live URL to indexation receipt. Single source of truth is `content/<slug>.md`; output is `blog/<slug>.html` rendered through `templates/post.html`. No React, no JSX, no `.map()` placeholders ever land on disk.

## STEP 1 — INTAKE

Receive the positioning thesis (e.g. "qué es un Growth Partner"). Ask nothing else. Derive everything else from the existing `llms.txt`, `growth-partner.html`, the three public cases (Universidad, Garett, Aras), and the verified metrics (3,2M€, 264.712€, 31.555, 88,95M, CPA 4,8€ Garett).

## STEP 2 — RESEARCH

- Pull keyword pack: primary + 3 secondary + 3 long-tail + 3 FAQ.
- Verify all candidate external URLs with HEAD request; only keep 200s.
- Classify search intent: informational / commercial / comparison.
- Find 3-7 authoritative external sources for the chiffres, methodologies, or definitions cited in the body. These must be:
  - Authoritative (industry body, primary research, official documentation, Wikipedia, established publisher).
  - Verifiable (live URL, not behind a paywall or a 404).
  - Relevant to a *specific claim* in the body, not generic anchors.

Output: `content/<slug>.md` frontmatter with `primary_keyword`, `secondary_keywords`, `faq[]`, and `sources[]` (an array of `{label, url}` objects). The renderer emits these as a "Fuentes y datos" block at the end of the article body, before the FAQ. Inline citations are optional but recommended for the strongest claims.

## STEP 3 — OUTLINE

Map the positioning point to one of the 5 archetypes in `Plantillas_Estructura_Post.md`:

| Positioning | Archetype |
|---|---|
| "¿Qué es X?" | #2 Framework con nombre (adapted) |
| Audit a problem | #1 Diagnóstico |
| Counterintuitive claim | #3 Contraintuitivo |
| Result numbers | #4 Caso de estudio |
| Own failure | #5 Lección |

Confirm: 9-block structure (epígrafe, escena, promesa, drop autoridad, framework, ejemplo real, pro tip, action step, recap+cliffhanger) — labeled internally, not visible to reader.

## STEP 4 — WRITE

Voice: Hormozi. Tuteo, 4-12 word sentences, no "verdaderamente", no "mayoría", no anaphora, no "no es X, es Y", no "shift", no "leverage", no "synergy". ≥3 cifras concretas per post. ≥3 retóricos del repertorio. 1.2-1.5K words.

Read aloud test: debe sonar a operador, no a coach ni a IA.

## STEP 5 — QA GATE (block publish if not green)

Run `node scripts/qa-checklist.mjs <slug>`. JSON output must report `verdict: publicar` with empty `issues` array. If `verdict: regenerar` → fix banned phrases. If `verdict: reescribir` → fix listed `blocks_to_rewrite`, re-run.

Required scores:
- A · voz ≥ 4/5
- B · estructura ≥ 7/9
- C · contenido ≥ 4/5
- D · lista negra = 0 hits
- E · anti-IA = 0 hits
- F · SEO = 4/4
- G · cierre = cliffhanger present
- word count 1200-1500 (tolerance 1100-1700)

## STEP 5.5 — EXTERNAL LINKS GATE (block publish if not green)

Every external URL cited in the body or in the `sources[]` frontmatter field must HEAD-respond with 200 (or 3xx that resolves to 200 within 3 hops). Run `node scripts/verify-external-links.mjs <slug>`. The script reports `failed: 0` to pass. If it reports any failure, the URL is either 404, 5xx, or times out — fix the source by either removing the citation or replacing it with a verified alternative.

Known limitations:
- `support.google.com/*` returns 404 to the verify script's `User-Agent` (Google bot detection). This is a false positive. Skip these and document them in the post if you must cite Google Support.

## STEP 6 — RENDER + SEO PACK

`node scripts/render-post.mjs <slug>` → emits `blog/<slug>.html`.
`node scripts/seo-pack.mjs <slug>` → must return `pass: true`.
`node scripts/verify-render.mjs <slug> --local` → must return `pass: true`.

If any fails, abort and report. Do not push.

## STEP 7 — INDEXATION INFRASTRUCTURE

This step is **automated** as part of `scripts/rewrite-batch.mjs` and `scripts/build-static.sh` — no manual run needed. After all 6 gates pass for a slug, the pipeline runs in this order:

- `node scripts/update-llms-txt.mjs <slug>` → appends/replaces the post entry.
- `node scripts/update-sitemap.mjs` → regenerates sitemap.xml with real `lastmod` and tiered priorities. **Runs only on the final slug of a batch** to avoid redundant regenerations.
- `node scripts/indexnow.mjs /blog/<slug>.html` → submits to IndexNow (status 202 expected; Bing, Yandex, Seznam accept it).
- `node scripts/gsc-push.mjs /blog/<slug>.html` → POSTs to Google Search Console URL Inspection API. Real JWT signing via `google-auth-library` + service account. **Optional step**: a 403 (no GSC access) reports WARN, not FAIL, so the rest of the pipeline succeeds even before the service account is added to GSC.

**To skip the indexation phase for a run:** pass `--no-index` to `rewrite-batch.mjs`. Useful for dry runs or when the indexation will be run separately.

**To enable GSC push end-to-end (no WARN):** add `hermes-blogpost@daybyday-gsc.iam.gserviceaccount.com` (or current service account) as Owner in Search Console for `https://www.daybydayconsulting.com/`. The script will detect access and report PASS instead of WARN.

## STEP 8 — REPORT BACK

Always end with a single message containing:
1. Live URL.
2. Final QA JSON (all green).
3. IndexNow submission receipt.
4. SEO pack + verify-render results.
5. The 2 internal links placed.
6. The full article text (final review pass).
7. Next-post hook (cliffhanger resolved into next positioning point).

## ESCALATION RULES

Stop and call for human input if:
- Primary keyword volume can't be validated (no GSC data + no autocomplete fallback).
- A claim needs a source you can't verify live.
- A 2xx response from an external URL has changed meaning.
- The migration script (`scripts/migrate-legacy.mjs`) needs to overwrite a non-skeleton file.

Never:
- Touch secrets under `Blog System/*.json` (per user decision, deferred to manual rotation).
- Commit to main branch (use the `feat/static-pipeline` worktree).
- Push to the live site from this skill (deploy is separate).
- Use synonyms of banned phrases to dodge the checklist.
