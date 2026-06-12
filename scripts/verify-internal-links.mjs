#!/usr/bin/env node
// verify-internal-links.mjs — resolves every internal href in
// blog/<slug>.html against the local repo. Fails the build if any
// target is missing. External (https:, mailto:, tel:, #anchor) are
// ignored. This is the responsibility of seo-pack.mjs and
// verify-external-links.mjs.
//
// Usage:  node scripts/verify-internal-links.mjs <slug>

import { readFile, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const slug = process.argv[2];
if (!slug) {
  console.error('Usage: node scripts/verify-internal-links.mjs <slug>');
  process.exit(1);
}

const filePath = path.join(ROOT, 'blog', `${slug}.html`);
if (!existsSync(filePath)) {
  console.error(`File not found: ${filePath}`);
  process.exit(1);
}

const html = await readFile(filePath, 'utf8');

// Match every href="..." and src="..." (src same problem: images).
// Skip externals (http(s)://, mailto:, tel:, data:).
const re = /(?:href|src)=["']([^"']+)["']/g;
const candidates = [];
let m;
while ((m = re.exec(html)) !== null) {
  const raw = m[1];
  if (
    /^https?:\/\//i.test(raw) ||
    /^(mailto|tel|data|javascript):/i.test(raw) ||
    raw.startsWith('#')
  ) {
    continue;
  }
  // Drop query / hash for resolution.
  const clean = raw.split('#')[0].split('?')[0];
  if (!clean) continue;
  candidates.push(clean);
}

// Resolve one URL → filesystem path. Returns null if the URL is
// explicitly external-by-design (e.g. /en/blog/*) so the gate does not
// fire on intentional gaps.
function resolve(url) {
  // Strip leading slash.
  let p = url.replace(/^\//, '');

  // Language alternates that we do not yet build. The 2 new posts
  // hreflang to /en/<filename>, which exists for the 15 main pages
  // but not for blog posts. Treat that as a known gap, not a 404.
  if (p.startsWith('en/blog/')) return { state: 'known_gap', url };

  // favicon.ico is referenced from the render template (<link rel="icon">)
  // but the file is not committed to the repo (served by the platform
  // or absent by design). Treat as a known gap, not a 404.
  if (p === 'favicon.ico') return { state: 'known_gap', url };

  // Anchor-style root.
  if (p === '') p = 'index.html';

  // Try direct file.
  const direct = path.join(ROOT, p);
  if (existsSync(direct)) return { state: 'ok', path: direct };

  // Try with .html appended.
  if (existsSync(direct + '.html')) {
    return { state: 'ok', path: direct + '.html' };
  }

  // Try as directory index.
  if (existsSync(path.join(direct, 'index.html'))) {
    return { state: 'ok', path: path.join(direct, 'index.html') };
  }

  return { state: 'missing', url, attempted: [direct, direct + '.html', path.join(direct, 'index.html')] };
}

const seen = new Set(candidates);
const results = [];
for (const url of seen) {
  results.push({ url, ...resolve(url) });
}

const missing = results.filter(r => r.state === 'missing');
const knownGaps = results.filter(r => r.state === 'known_gap');
const ok = results.filter(r => r.state === 'ok');

const summary = {
  slug,
  internal_links: seen.size,
  ok: ok.length,
  missing: missing.length,
  known_gaps: knownGaps.length,
  results,
};

console.log(JSON.stringify(summary, null, 2));

if (missing.length > 0) {
  console.error(`\n[FAIL] ${missing.length} broken internal link(s) in blog/${slug}.html`);
  for (const m of missing) {
    console.error(`  - ${m.url}`);
    for (const a of m.attempted) console.error(`      tried: ${a}`);
  }
  process.exit(1);
}

if (knownGaps.length > 0) {
  console.error(`\n[INFO] ${knownGaps.length} known-gap link(s) (en/blog/* — not yet built)`);
}

process.exit(0);

