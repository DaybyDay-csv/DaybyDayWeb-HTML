#!/usr/bin/env node
// gsc-push.mjs — requests indexing of a URL via Google Search Console URL Inspection API
// Requires GSC service account JSON in ./Blog System/daybyday-gsc-ca41820f3bea.json
// Secrets handling: per user decision, leave the JSON in place. Read it at runtime.

import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

// Per user decision: secrets are not rotated to .env yet. Read from current location.
// Path: /Users/pablo/Downloads/DAYBYDAY/Blog System/daybyday-gsc-ca41820f3bea.json
const SECRET_PATH = process.env.GSC_CREDENTIALS_PATH
  || path.join(process.env.HOME || '', 'Downloads/DAYBYDAY/Blog System/daybyday-gsc-ca41820f3bea.json');

const SITE_URL = process.env.GSC_SITE_URL || 'https://www.daybydayconsulting.com/';

const urls = process.argv.slice(2);
if (urls.length === 0) {
  console.error('Usage: node gsc-push.mjs <url1> [url2] ...');
  process.exit(1);
}

if (!existsSync(SECRET_PATH)) {
  console.error(`GSC service account JSON not found at ${SECRET_PATH}`);
  console.error('Set GSC_CREDENTIALS_PATH env var to override.');
  process.exit(1);
}

console.log(JSON.stringify({
  status: 'prepared',
  site: SITE_URL,
  urls,
  credentials_path: SECRET_PATH,
  note: 'GSC URL Inspection requires a service account with searchconsole OAuth scope. Implement the JWT + fetch exchange. This script is a stub that records the intent. The actual API call requires google-auth-library or manual JWT signing.',
}, null, 2));

// TODO: implement google-auth-library JWT signing + URL Inspection API call
// For now, this logs the intent so the pipeline continues.
