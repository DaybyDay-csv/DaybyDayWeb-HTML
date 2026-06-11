#!/usr/bin/env node
// update-llms-txt.mjs — appends/updates a new post entry in llms.txt

import { readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const slug = process.argv[2];
if (!slug) { console.error('Usage: node update-llms-txt.mjs <slug>'); process.exit(1); }

const mdPath = path.join(ROOT, 'content', `${slug}.md`);
const raw = await readFile(mdPath, 'utf8');
const fmMatch = raw.match(/^---([\s\S]*?)\n---/);
if (!fmMatch) { console.error('Missing frontmatter'); process.exit(1); }
const fm = {};
for (const line of fmMatch[1].split('\n')) {
  const m = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
  if (m) fm[m[1]] = m[2].replace(/^"|"$/g, '').trim();
}
const url = `https://www.daybydayconsulting.com/blog/${slug}.html`;
const summary = (fm.llms_summary || fm.meta_desc || '').slice(0, 200);

const llmsPath = path.join(ROOT, 'llms.txt');
let llms = await readFile(llmsPath, 'utf8');

const entryMarker = `<!-- auto:${slug} -->`;
const newEntry = `${entryMarker}\n- [${fm.title}](${url}) — ${summary}\n<!-- /auto -->`;

if (llms.includes(entryMarker)) {
  const re = new RegExp(`${entryMarker}[\\s\\S]*?<!-- /auto -->`, 'g');
  llms = llms.replace(re, newEntry);
} else {
  if (!llms.includes('## Posts recientes')) {
    llms = llms.trimEnd() + '\n\n## Posts recientes\n\n';
  }
  llms = llms.trimEnd() + '\n' + newEntry + '\n';
}

await writeFile(llmsPath, llms, 'utf8');
console.log(JSON.stringify({ updated: true, url, slug, summary }, null, 2));
