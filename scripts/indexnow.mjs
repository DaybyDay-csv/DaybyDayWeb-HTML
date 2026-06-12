#!/usr/bin/env node
// indexnow.mjs — submits URLs to IndexNow API
// Reads API key + URLs from env or hard-coded fallback (rotated by user)
//
// TODO(rotate-indexnow-key): the literal fallback below is a temporary
// measure pending rotation to a .env-loaded secret. Action items:
//   1) Generate a new IndexNow key at https://www.indexnow.org/
//   2) Store it as INDEXNOW_KEY in .env (already gitignored)
//   3) Remove the || '<hardcoded-fallback>' fallback in this file
//   4) Make the script exit 1 if process.env.INDEXNOW_KEY is undefined
// This must happen before the repo is shared with anyone outside the
// founder's workstation, since the key is currently readable to anyone
// with repo access.

const INDEXNOW_KEY = process.env.INDEXNOW_KEY || 'd3b6f1c2a8e54a7f9c1b0d2e3f4a5b6c';
const HOST = 'www.daybydayconsulting.com';

const urls = process.argv.slice(2);
if (urls.length === 0) {
  console.error('Usage: node indexnow.mjs <url1> [url2] ...');
  process.exit(1);
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
  console.error(
    '[indexnow] NOTE: API key is hardcoded. See scripts/indexnow.mjs TODO(rotate-indexnow-key).'
  );
} catch (err) {
  console.error('IndexNow submission failed:', err.message);
  process.exit(1);
}
