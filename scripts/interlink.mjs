#!/usr/bin/env node
// interlink.mjs — given a slug, finds 2 best contextual internal links from existing blog posts + strategic pages
// Reads blog.html to enumerate the catalog, ranks by keyword overlap

import { readFile, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const slug = process.argv[2];
if (!slug) { console.error('Usage: node interlink.mjs <slug>'); process.exit(1); }

const sourceMd = path.join(ROOT, 'content', `${slug}.md`);
if (!existsSync(sourceMd)) { console.error(`Missing source: ${sourceMd}`); process.exit(1); }
const source = await readFile(sourceMd, 'utf8');
const sourceText = source.toLowerCase();

// Strategic pages (always candidates)
const STRATEGIC = [
  { url: '/growth-partner.html', anchor: 'qué es un Growth Partner' },
  { url: '/meta-ads.html', anchor: 'Meta Ads para D2C' },
  { url: '/google-ads.html', anchor: 'Google Ads para D2C' },
  { url: '/automatizacion.html', anchor: 'automatización de marketing' },
  { url: '/analytics.html', anchor: 'analytics y atribución' },
  { url: '/agentic-ai.html', anchor: 'agentic AI' },
  { url: '/problema.html', anchor: 'los tres bloqueos típicos del founder D2C' },
  { url: '/resultados.html', anchor: 'casos reales de DayByDay' },
];

// Index blog posts
const blogDir = path.join(ROOT, 'blog');
const blogFiles = (await readdir(blogDir)).filter(f => f.endsWith('.html'));
const candidates = [];
for (const f of blogFiles) {
  if (f === `${slug}.html`) continue;
  const fullPath = path.join(blogDir, f);
  const html = await readFile(fullPath, 'utf8');
  const titleMatch = html.match(/<title>([^<]+)<\/title>/);
  const descMatch = html.match(/<meta name="description" content="([^"]+)"/);
  const h1Match = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
  const title = (titleMatch && titleMatch[1]) || (h1Match && h1Match[1]) || f;
  const desc = descMatch ? descMatch[1] : '';
  const url = `/blog/${f.replace(/\.html$/, '')}`;
  const text = (title + ' ' + desc).toLowerCase();
  let overlap = 0;
  const sourceWords = new Set(sourceText.match(/[a-záéíóúñ]{5,}/g) || []);
  for (const w of sourceWords) {
    if (text.includes(w)) overlap++;
  }
  if (overlap > 0) {
    candidates.push({ url, title, desc, overlap });
  }
}
candidates.sort((a, b) => b.overlap - a.overlap);

const top = candidates.slice(0, 2);
const output = {
  slug,
  recommended_internal_links: top,
  strategic_alternatives: STRATEGIC,
  note: 'Top 2 by lexical overlap with source. Strategic pages available as fallbacks if no good blog match.',
};
console.log(JSON.stringify(output, null, 2));
