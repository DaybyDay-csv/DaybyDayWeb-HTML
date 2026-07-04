#!/usr/bin/env node
// update-blog-index.mjs — inserts the post card into the two blog listing pages
//
//   1. blog.html        (legacy static card list, .html URLs)
//   2. blog/index.html  (tailwind build served at /blog, clean URLs with trailing slash)
//
// Idempotent: if the slug is already present in a file, that file is left untouched.
// Usage: node scripts/update-blog-index.mjs <slug>

import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter } from './lib/frontmatter.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

function esc(s) {
  return String(s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

const slug = process.argv[2];
if (!slug) {
  console.error('Usage: node update-blog-index.mjs <slug>');
  process.exit(1);
}

const md = await readFile(path.join(ROOT, 'content', `${slug}.md`), 'utf8');
const { fm } = parseFrontmatter(md);
const title = fm.title || slug;
const desc = fm.meta_desc || '';
const category = fm.category || 'Estrategia';
const date = fm.article_date || new Date().toISOString().split('T')[0];
const mins = fm.reading_time || 8;

const result = { slug, updated: [], skipped: [] };

// ---- 1. blog.html (legacy cards) ----
{
  const file = path.join(ROOT, 'blog.html');
  let html = await readFile(file, 'utf8');
  if (html.includes(`/blog/${slug}.html`)) {
    result.skipped.push('blog.html (already listed)');
  } else {
    const card = [
      `        <a href="/blog/${slug}.html" class="blog-card">`,
      `          <div class="blog-card-meta">`,
      `            <span class="blog-card-category">${esc(category)}</span>`,
      `            <span class="blog-card-time">${mins} min</span>`,
      `            <span class="blog-card-date">${date}</span>`,
      `          </div>`,
      `          <h3 class="blog-card-title">${esc(title)}</h3>`,
      `          <p class="blog-card-desc">${esc(desc)}</p>`,
      `        </a>`,
      '',
    ].join('\n');
    const anchorRe = /([ \t]*<a href="\/blog\/[^"]+\.html" class="blog-card">)/;
    if (!anchorRe.test(html)) {
      console.error('blog.html: no blog-card anchor found — aborting for this file');
      result.skipped.push('blog.html (anchor not found)');
    } else {
      html = html.replace(anchorRe, card + '$1');
      await writeFile(file, html, 'utf8');
      result.updated.push('blog.html');
    }
  }
}

// ---- 2. blog/index.html (tailwind build) ----
{
  const file = path.join(ROOT, 'blog', 'index.html');
  let html = await readFile(file, 'utf8');
  if (html.includes(`/blog/${slug}/`) || html.includes(`/blog/${slug}"`)) {
    result.skipped.push('blog/index.html (already listed)');
  } else {
    const card =
      `<a class="block p-6 bg-gray-900 rounded-lg hover:bg-gray-800 transition" href="/blog/${slug}/">` +
      `<p class="text-xs text-blue-400 mb-2">${esc(category)}</p>` +
      `<h2 class="text-lg font-semibold text-white mb-2">${esc(title)}</h2>` +
      `<p class="text-sm text-gray-400 line-clamp-2">${esc(desc)}</p>` +
      `<p class="text-xs text-gray-500 mt-4">${date}<!-- --> • <!-- -->${mins} min</p></a>`;
    const anchor = '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">';
    const i = html.indexOf(anchor);
    if (i === -1) {
      console.error('blog/index.html: grid anchor not found — aborting for this file');
      result.skipped.push('blog/index.html (anchor not found)');
    } else {
      html = html.slice(0, i + anchor.length) + card + html.slice(i + anchor.length);
      await writeFile(file, html, 'utf8');
      result.updated.push('blog/index.html');
    }
  }
}

console.log(JSON.stringify(result, null, 2));
if (result.updated.length === 0 && result.skipped.some(s => s.includes('anchor not found'))) {
  process.exit(1);
}
