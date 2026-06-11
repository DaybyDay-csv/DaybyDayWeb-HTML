#!/usr/bin/env node
// seo-pack.mjs — validates meta/title/slug/H-hierarchy/FAQ schema on the rendered HTML
// Operates on blog/<slug>.html

import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const slug = process.argv[2];
if (!slug) { console.error('Usage: node seo-pack.mjs <slug>'); process.exit(1); }

const html = await readFile(path.join(ROOT, 'blog', `${slug}.html`), 'utf8');

const checks = [];
const errors = [];

function check(name, pass, detail) {
  checks.push({ name, pass, detail });
  if (!pass) errors.push(`${name}: ${detail}`);
}

const title = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || '';
check('title_present', title.length > 0, title.length ? `${title.length} chars` : 'missing');
check('title_length', title.length > 0 && title.length <= 60, `${title.length} chars (max 60)`);

const meta = (html.match(/<meta name="description" content="([^"]+)"/) || [])[1] || '';
check('meta_present', meta.length > 0, meta.length ? `${meta.length} chars` : 'missing');
check('meta_length', meta.length > 0 && meta.length <= 155, `${meta.length} chars (max 155)`);

const canonical = (html.match(/<link rel="canonical" href="([^"]+)"/) || [])[1] || '';
check('canonical_present', canonical.length > 0, canonical || 'missing');
check('canonical_https', canonical.startsWith('https://'), canonical);

const h1Count = (html.match(/<h1[\s>]/g) || []).length;
check('h1_unique', h1Count === 1, `${h1Count} h1 tags`);

const h2Count = (html.match(/<h2[\s>]/g) || []).length;
check('h2_min', h2Count >= 3, `${h2Count} h2 tags`);

const faqSchemaCount = (html.match(/"@type":\s*"FAQPage"/g) || []).length;
check('faq_schema', faqSchemaCount === 1, `${faqSchemaCount} FAQPage schema blocks`);

const articleSchemaCount = (html.match(/"@type":\s*"Article"/g) || []).length;
check('article_schema', articleSchemaCount === 1, `${articleSchemaCount} Article schema blocks`);

const ogTitle = (html.match(/<meta property="og:title" content="([^"]+)"/) || [])[1] || '';
const ogDesc = (html.match(/<meta property="og:description" content="([^"]+)"/) || [])[1] || '';
check('og_title', ogTitle.length > 0, ogTitle || 'missing');
check('og_description', ogDesc.length > 0, ogDesc || 'missing');

const hasHreflang = /<link rel="alternate" hreflang=/.test(html);
check('hreflang', hasHreflang, hasHreflang ? 'present' : 'missing');

const jsxMarkers = (html.match(/map\(\(\w+|class="text-white\/70|leading-relaxed mb-5".*\[/g) || []).length;
check('no_jsx_leftover', jsxMarkers === 0, `${jsxMarkers} JSX patterns found`);

const internalLinkCount = (html.match(/href="\/[^"]+"/g) || []).length;
check('internal_links_min', internalLinkCount >= 2, `${internalLinkCount} internal links`);

const bodyMatch = html.match(/<article class="article-body">([\s\S]*?)<\/article>/);
const bodyText = bodyMatch ? bodyMatch[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : '';
const wordCount = bodyText.split(/\s+/).filter(Boolean).length;
check('word_count', wordCount >= 1100 && wordCount <= 1700, `${wordCount} words (target 1200-1500)`);

const summary = {
  slug,
  pass: errors.length === 0,
  errors,
  checks,
  word_count: wordCount,
};
console.log(JSON.stringify(summary, null, 2));
if (errors.length > 0) process.exit(1);
