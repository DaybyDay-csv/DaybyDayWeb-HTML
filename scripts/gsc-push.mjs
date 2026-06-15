#!/usr/bin/env node
// gsc-push.mjs — requests indexing of URLs via Google Search Console URL Inspection API
// Requires GSC service account JSON with webmasters scope, added as owner in GSC.
//
// Usage:
//   node scripts/gsc-push.mjs /blog/smart-bidding-google-ads-d2c.html [more urls...]
//   GSC_SITE_URL=https://www.daybydayconsulting.com/ node scripts/gsc-push.mjs /blog/foo.html

import { readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { GoogleAuth } from 'google-auth-library';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const SECRET_PATH = process.env.GSC_CREDENTIALS_PATH
  || path.join(process.env.HOME || '', 'Downloads/DAYBYDAY/Blog System/daybyday-gsc-ca41820f3bea.json');

const SITE_URL = process.env.GSC_SITE_URL || 'https://www.daybydayconsulting.com/';

const urls = process.argv.slice(2);
if (urls.length === 0) {
  console.error('Usage: node gsc-push.mjs <url1> [url2 ...]');
  process.exit(1);
}

if (!existsSync(SECRET_PATH)) {
  console.error(`GSC service account JSON not found at ${SECRET_PATH}`);
  console.error('Set GSC_CREDENTIALS_PATH env var to override.');
  process.exit(1);
}

const LOG_PATH = path.join(ROOT, 'logs/gsc-push.log.jsonl');

async function logResult(record) {
  await import('node:fs/promises').then(fs => fs.mkdir(path.dirname(LOG_PATH), { recursive: true }));
  await writeFile(LOG_PATH, JSON.stringify(record) + '\n', { flag: 'a' });
}

async function pushUrl(auth, siteUrl, urlPath) {
  const url = urlPath.startsWith('http') ? urlPath : `https://www.daybydayconsulting.com${urlPath.startsWith('/') ? '' : '/'}${urlPath}`;
  const fullUrl = encodeURI(url);
  const apiUrl = `https://searchconsole.googleapis.com/v1/urlInspection/index:inspect`;
  const body = {
    inspectionUrl: fullUrl,
    siteUrl: siteUrl,
    languageCode: 'es-ES',
  };

  const client = await auth.getClient();
  const res = await client.request({
    url: apiUrl,
    method: 'POST',
    data: body,
  });

  return res.data;
}

async function main() {
  const auth = new GoogleAuth({
    keyFile: SECRET_PATH,
    scopes: ['https://www.googleapis.com/auth/webmasters'],
  });

  const results = [];
  for (const u of urls) {
    const start = Date.now();
    try {
      const data = await pushUrl(auth, SITE_URL, u);
      const inspection = data.inspectionResult || {};
      const verdict = inspection.verdict || 'UNKNOWN';
      const coverage = inspection.coverageState || 'UNKNOWN';
      const indexed = inspection.indexingState || inspection.inspectionResultLink?.from || 'UNKNOWN';
      const record = {
        ok: true,
        url: u,
        verdict,
        coverage,
        indexingState: indexed,
        lastCrawlTime: inspection.lastCrawlTime || null,
        pageFetchState: inspection.pageFetchState || null,
        duration_ms: Date.now() - start,
        at: new Date().toISOString(),
      };
      results.push(record);
      console.log(JSON.stringify(record, null, 2));
    } catch (err) {
      const record = {
        ok: false,
        url: u,
        error: err.message || String(err),
        code: err.code || err.response?.status || null,
        duration_ms: Date.now() - start,
        at: new Date().toISOString(),
      };
      results.push(record);
      console.log(JSON.stringify(record, null, 2));
    }
    await logResult(results[results.length - 1]);
  }

  const summary = {
    pushed: results.length,
    ok: results.filter(r => r.ok).length,
    failed: results.filter(r => !r.ok).length,
    indexedAlready: results.filter(r => r.ok && (r.coverage === 'Indexed' || r.coverage === 'indexed')).length,
    submitted: results.filter(r => r.ok && r.verdict === 'PASS' && r.coverage !== 'Indexed' && r.coverage !== 'indexed').length,
    at: new Date().toISOString(),
  };
  console.log('\n=== GSC PUSH SUMMARY ===');
  console.log(JSON.stringify(summary, null, 2));
}

main().catch(err => {
  console.error('GSC push failed:', err.message);
  process.exit(1);
});
