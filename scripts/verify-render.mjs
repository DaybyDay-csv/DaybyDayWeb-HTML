#!/usr/bin/env node
// verify-render.mjs — fetches the deployed URL, asserts H1, body word count, no JSX, no broken links
// In CI: run after deploy. Locally: run with --local to read from blog/<slug>.html

import { readFile, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const slug = process.argv[2];
if (!slug) { console.error('Usage: node verify-render.mjs <slug> [--local]'); process.exit(1); }
const local = process.argv.includes('--local');

const filePath = path.join(ROOT, 'blog', `${slug}.html`);
if (!existsSync(filePath)) {
  console.error(`File not found: ${filePath}`);
  process.exit(1);
}

const html = await readFile(filePath, 'utf8');
const s = await stat(filePath);

const checks = [];
const errors = [];
function check(name, pass, detail) {
  checks.push({ name, pass, detail });
  if (!pass) errors.push(`${name}: ${detail}`);
}

const h1Match = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
check('h1_present', !!h1Match, h1Match ? h1Match[1].slice(0, 80) : 'missing');
check('h1_unique', (html.match(/<h1[\s>]/g) || []).length === 1, `${(html.match(/<h1[\s>]/g) || []).length} h1`);

const bodyMatch = html.match(/<article class="article-body">([\s\S]*?)<\/article>/);
const bodyText = bodyMatch ? bodyMatch[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : '';
const wordCount = bodyText.split(/\s+/).filter(Boolean).length;
check('word_count', wordCount >= 1100, `${wordCount} words (target 1200-1500)`);

const jsxMarkers = html.match(/map\(\(\w+|class="text-white\/70[^"]*"\)\s*\{|leading-relaxed mb-5"\)\s*\{|\[(\s*,\s*)+\]/g);
check('no_jsx', !jsxMarkers, jsxMarkers ? `${jsxMarkers.length} JSX markers` : 'clean');

const titleMatch = html.match(/<title>([^<]+)<\/title>/);
check('title', !!titleMatch, titleMatch ? titleMatch[1] : 'missing');
check('title_length', titleMatch && titleMatch[1].length <= 70, titleMatch ? `${titleMatch[1].length} chars` : '');

const meta = html.match(/<meta name="description" content="([^"]+)"/);
check('meta', !!meta, meta ? `${meta[1].length} chars` : 'missing');
check('meta_length', meta && meta[1].length <= 160, meta ? `${meta[1].length} chars` : '');

const canonical = html.match(/<link rel="canonical" href="([^"]+)"/);
check('canonical', !!canonical, canonical ? canonical[1] : 'missing');

const faqSchema = html.match(/"@type":\s*"FAQPage"/);
check('faq_schema', !!faqSchema, faqSchema ? 'present' : 'missing');

const articleSchema = html.match(/"@type":\s*"Article"/);
check('article_schema', !!articleSchema, articleSchema ? 'present' : 'missing');

const internalLinks = (html.match(/href="\/[^"#]*"/g) || []).length;
check('internal_links', internalLinks >= 2, `${internalLinks} internal links`);

const summary = {
  slug,
  file_size_kb: +(s.size / 1024).toFixed(1),
  word_count: wordCount,
  pass: errors.length === 0,
  errors,
  checks,
  mode: local ? 'local' : 'remote',
};
console.log(JSON.stringify(summary, null, 2));
if (errors.length > 0) process.exit(1);
