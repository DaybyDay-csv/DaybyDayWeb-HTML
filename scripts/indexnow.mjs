#!/usr/bin/env node
// indexnow.mjs — submits URLs to IndexNow API
// Reads API key from INDEXNOW_KEY env var (GitHub secret en CI).
// Sin key hace skip con exit 0: el gate de indexación nunca tumba una
// publicación.

const INDEXNOW_KEY = process.env.INDEXNOW_KEY || '';
const HOST = 'www.daybydayconsulting.com';

const urls = process.argv.slice(2);
if (urls.length === 0) {
  console.error('Usage: node indexnow.mjs <url1> [url2] ...');
  process.exit(1);
}

if (!INDEXNOW_KEY) {
  console.log(JSON.stringify({ submitted: 0, skipped: 'INDEXNOW_KEY not set', urls: urls.length }, null, 2));
  process.exit(0);
}

const fullUrls = urls.map(u => u.startsWith('http') ? u : `https://${HOST}${u.startsWith('/') ? '' : '/'}${u}`);

const body = {
  host: HOST,
  key: INDEXNOW_KEY,
  keyLocation: `https://${HOST}/${INDEXNOW_KEY}.txt`,
  urlList: fullUrls,
};

try {
  const res = await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  console.log(JSON.stringify({
    submitted: fullUrls.length,
    status: res.status,
    response: text.slice(0, 500),
  }, null, 2));
} catch (err) {
  console.error('IndexNow submission failed:', err.message);
  process.exit(1);
}
