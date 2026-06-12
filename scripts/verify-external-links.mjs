#!/usr/bin/env node
// verify-external-links.mjs — HEAD-checks every external URL in content/*.md
// Returns JSON with the full audit. Exit code 0 if all 200, 1 if any 404/5xx/timeout.
// Catches:
//   - 404 dead links
//   - 3xx redirect chains (follows them up to 3 hops, reports final status)
//   - timeout / network errors
//   - non-HTTP(S) schemes (mailto, ftp, etc.) — skipped
//
// Internal links (relative, /blog/*, same-origin) are NOT checked here. Those
// are the responsibility of seo-pack.mjs and verify-render.mjs.
//
// Usage: node scripts/verify-external-links.mjs [slug]   # single
//        node scripts/verify-external-links.mjs          # all content/*.md

import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter } from './lib/frontmatter.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const TIMEOUT_MS = 8000;
const MAX_REDIRECTS = 3;
const CONCURRENCY = 8;

function findExternalUrls(text) {
  const urlRe = /https?:\/\/[^\s)\]"'<>]+/g;
  const urls = new Set();
  let m;
  while ((m = urlRe.exec(text)) !== null) {
    let u = m[0].replace(/[.,;:!?)]+$/, '');
    urls.add(u);
  }
  return [...urls];
}

async function checkUrl(url) {
  const start = Date.now();
  let currentUrl = url;
  let redirects = 0;
  let lastStatus = 0;
  let lastContentType = '';
  let lastContentLength = 0;

  while (redirects <= MAX_REDIRECTS) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
    try {
      const res = await fetch(currentUrl, {
        method: 'HEAD',
        redirect: 'manual',
        signal: controller.signal,
        headers: { 'User-Agent': 'DayByDay-Blogposting-Verify/1.0' },
      });
      clearTimeout(timer);
      lastStatus = res.status;
      lastContentType = res.headers.get('content-type') || '';
      lastContentLength = parseInt(res.headers.get('content-length') || '0', 10);

      if ([301, 302, 303, 307, 308].includes(res.status) && redirects < MAX_REDIRECTS) {
        const loc = res.headers.get('location');
        if (!loc) break;
        currentUrl = new URL(loc, currentUrl).toString();
        redirects++;
        continue;
      }
      break;
    } catch (err) {
      clearTimeout(timer);
      return {
        url,
        final_url: currentUrl,
        status: 0,
        error: err.name === 'AbortError' ? 'timeout' : err.message,
        duration_ms: Date.now() - start,
        redirects,
      };
    }
  }

  return {
    url,
    final_url: currentUrl,
    status: lastStatus,
    content_type: lastContentType,
    content_length: lastContentLength,
    duration_ms: Date.now() - start,
    redirects,
  };
}

async function checkBatch(urls) {
  const results = [];
  for (let i = 0; i < urls.length; i += CONCURRENCY) {
    const slice = urls.slice(i, i + CONCURRENCY);
    const r = await Promise.all(slice.map(checkUrl));
    results.push(...r);
  }
  return results;
}

async function processFile(slug) {
  const fp = path.join(ROOT, 'content', `${slug}.md`);
  const raw = await readFile(fp, 'utf8');
  const { fm, body } = parseFrontmatter(raw);
  const allUrls = findExternalUrls(body);
  const sourceUrls = Array.isArray(fm.sources) ? fm.sources.map(s => typeof s === 'string' ? s : s.url).filter(Boolean) : [];
  const combined = [...new Set([...allUrls, ...sourceUrls])];
  return { slug, urls: combined };
}

async function main() {
  const arg = process.argv[2];
  const slugs = arg ? [arg] : (await readdir(path.join(ROOT, 'content')))
    .filter(f => f.endsWith('.md') && !f.startsWith('_'))
    .map(f => f.replace(/\.md$/, ''));

  const allTasks = await Promise.all(slugs.map(processFile));
  const urlToSlugs = new Map();
  for (const t of allTasks) {
    for (const u of t.urls) {
      if (!urlToSlugs.has(u)) urlToSlugs.set(u, new Set());
      urlToSlugs.get(u).add(t.slug);
    }
  }

  const uniqueUrls = [...urlToSlugs.keys()];
  const results = await checkBatch(uniqueUrls);

  const failed = results.filter(r => r.status === 0 || r.status >= 400 || r.status >= 300 && r.redirects === 0);
  const redirected = results.filter(r => r.redirects > 0 && r.status >= 200 && r.status < 400);
  const ok = results.filter(r => r.status >= 200 && r.status < 300);

  const report = {
    checked_at: new Date().toISOString(),
    files_processed: slugs.length,
    unique_urls: uniqueUrls.length,
    ok: ok.length,
    redirected: redirected.length,
    failed: failed.length,
    failures: failed.map(f => ({
      url: f.url,
      final_url: f.final_url,
      status: f.status,
      error: f.error,
      used_in: [...(urlToSlugs.get(f.url) || [])],
    })),
    redirects: redirected.map(r => ({
      url: r.url,
      final_url: r.final_url,
      status: r.status,
      hops: r.redirects,
      used_in: [...(urlToSlugs.get(r.url) || [])],
    })),
    ok_urls: ok.map(o => ({ url: o.url, status: o.status, duration_ms: o.duration_ms })),
  };
  console.log(JSON.stringify(report, null, 2));
  process.exit(failed.length > 0 ? 1 : 0);
}

await main();
