#!/usr/bin/env node
// generate-hero.mjs — genera la imagen hero (1200×675 PNG) de un post desde su frontmatter.
// Diseño de marca determinista (SVG → PNG via sharp). Sin APIs de pago, apto para CI.
// Google AI optimization guide: las respuestas con IA incluyen imágenes → más superficie para aparecer.
// Usage: node scripts/generate-hero.mjs <slug> [--force]

import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter } from './lib/frontmatter.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const slug = process.argv[2];
const force = process.argv.includes('--force');
if (!slug) { console.error('Usage: node generate-hero.mjs <slug>'); process.exit(1); }

const outDir = path.join(ROOT, 'blog', 'img');
const outPath = path.join(outDir, `${slug}.png`);
if (!force) {
  try { await access(outPath); console.log(JSON.stringify({ slug, skipped: true, reason: 'hero ya existe' })); process.exit(0); } catch {}
}

const md = await readFile(path.join(ROOT, 'content', `${slug}.md`), 'utf8');
const { fm, body } = parseFrontmatter(md);
const title = String(fm.h1 || fm.title || slug);
const category = String(fm.category || 'Estrategia');

// La cifra destacada: primer :::cifra o primer número con € / % del body
let highlight = '';
const cifraMatch = body.match(/:::cifra\n([\s\S]*?)\n:::/);
if (cifraMatch) {
  const m = cifraMatch[1].match(/(?:[A-Za-zÁ-úñÑ()]+\s+){0,2}\d[\d.,-]*\s*(?:€|%|x\b|días|horas|conversiones)/);
  if (m) highlight = m[0].trim().slice(0, 34);
}

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// Word-wrap del título a ≤3 líneas
function wrap(text, maxChars) {
  const words = text.split(' ');
  const lines = [];
  let cur = '';
  for (const w of words) {
    if ((cur + ' ' + w).trim().length > maxChars && cur) { lines.push(cur.trim()); cur = w; }
    else cur = (cur + ' ' + w).trim();
  }
  if (cur) lines.push(cur.trim());
  return lines.slice(0, 3);
}
const lines = wrap(title, 30);
const fontSize = lines.length >= 3 ? 56 : 64;
const lineHeight = fontSize * 1.25;
const titleY = 300 - ((lines.length - 1) * lineHeight) / 2;
const titleSvg = lines.map((l, i) =>
  `<text x="80" y="${titleY + i * lineHeight}" font-family="Arial, Helvetica, sans-serif" font-size="${fontSize}" font-weight="800" fill="#ffffff">${esc(l)}</text>`
).join('\n');

const highlightSvg = highlight
  ? `<text x="80" y="${titleY + lines.length * lineHeight + 40}" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="700" fill="#818cf8">${esc(highlight)}</text>`
  : '';

const svg = `<svg width="1200" height="675" viewBox="0 0 1200 675" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b0d14"/>
      <stop offset="1" stop-color="#151a2e"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6366f1"/>
      <stop offset="1" stop-color="#8b5cf6"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="675" fill="url(#bg)"/>
  <circle cx="1050" cy="120" r="260" fill="#6366f1" opacity="0.08"/>
  <circle cx="1150" cy="560" r="180" fill="#8b5cf6" opacity="0.07"/>
  <rect x="80" y="96" width="72" height="6" rx="3" fill="url(#accent)"/>
  <text x="80" y="150" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="700" fill="#818cf8" letter-spacing="2">${esc(category.toUpperCase())}</text>
  ${titleSvg}
  ${highlightSvg}
  <text x="80" y="600" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#ffffff">DayByDay</text>
  <text x="222" y="600" font-family="Arial, Helvetica, sans-serif" font-size="24" fill="#94a3b8">· Growth Partner D2C</text>
  <rect x="80" y="616" width="1040" height="2" fill="#1e2440"/>
</svg>`;

await mkdir(outDir, { recursive: true });
let sharp;
try { sharp = (await import('sharp')).default; } catch (e) {
  console.error('sharp no instalado: npm install sharp'); process.exit(1);
}
await sharp(Buffer.from(svg)).png().toFile(outPath);
console.log(JSON.stringify({ slug, hero: `blog/img/${slug}.png`, lines: lines.length, highlight: highlight || null }));
