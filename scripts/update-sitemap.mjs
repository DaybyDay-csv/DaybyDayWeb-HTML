#!/usr/bin/env node
// update-sitemap.mjs — regenerates sitemap.xml with all blog/*.html + adds new post with real lastmod

import { readFile, writeFile, readdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const STATIC_PAGES = [
  { loc: '/', priority: 1.0, changefreq: 'weekly' },
  { loc: '/problema.html', priority: 0.9, changefreq: 'monthly' },
  { loc: '/como-trabajamos.html', priority: 0.9, changefreq: 'monthly' },
  { loc: '/resultados.html', priority: 0.9, changefreq: 'monthly' },
  { loc: '/growth-partner.html', priority: 0.9, changefreq: 'monthly' },
  { loc: '/lo-que-cubre.html', priority: 0.9, changefreq: 'monthly' },
  { loc: '/contacto.html', priority: 0.9, changefreq: 'monthly' },
  { loc: '/blog.html', priority: 0.8, changefreq: 'weekly' },
  { loc: '/meta-ads.html', priority: 0.85, changefreq: 'monthly' },
  { loc: '/google-ads.html', priority: 0.85, changefreq: 'monthly' },
  { loc: '/tiktok-ads.html', priority: 0.8, changefreq: 'monthly' },
  { loc: '/linkedin-ads.html', priority: 0.8, changefreq: 'monthly' },
  { loc: '/automatizacion.html', priority: 0.85, changefreq: 'monthly' },
  { loc: '/analytics.html', priority: 0.85, changefreq: 'monthly' },
  { loc: '/agentic-ai.html', priority: 0.85, changefreq: 'monthly' },
  { loc: '/growth-strategy.html', priority: 0.85, changefreq: 'monthly' },
  { loc: '/servicios.html', priority: 0.6, changefreq: 'monthly' },
];

const TECH_PAGES = [
  '/tech/meta-ads.html',
  '/tech/google-ads-tech.html',
  '/tech/tiktok-ads.html',
  '/tech/linkedin-ads.html',
  '/tech/shopify.html',
  '/tech/ga4.html',
  '/tech/gtm.html',
  '/tech/gsc.html',
  '/tech/n8n.html',
  '/tech/capi.html',
  '/tech/azure.html',
  '/tech/dsp.html',
];

const PILLARS = new Set([
  'que-es-un-growth-partner',
  'growth-partner-vs-agencia-paid-media',
  'agencia-vs-inhouse',
  'que-es-paid-media',
  'cac-vs-ltv-ecommerce',
  'metodologia-day-by-day',
  'kpis-ecommerce-d2c',
]);

const baseUrl = 'https://www.daybydayconsulting.com';

async function lastmodFor(filePath) {
  try {
    const s = await stat(filePath);
    return s.mtime.toISOString().slice(0, 10);
  } catch {
    return new Date().toISOString().slice(0, 10);
  }
}

function urlEntry(loc, priority, changefreq, lastmod) {
  return `  <url><loc>${baseUrl}${loc}</loc><changefreq>${changefreq}</changefreq><priority>${priority}</priority><lastmod>${lastmod}</lastmod></url>`;
}

async function buildSitemap() {
  const lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'];

  const today = new Date().toISOString().slice(0, 10);

  for (const p of STATIC_PAGES) {
    const fp = path.join(ROOT, p.loc.slice(1));
    const lm = existsSync(fp) ? await lastmodFor(fp) : today;
    lines.push(urlEntry(p.loc, p.priority, p.changefreq, lm));
  }

  for (const t of TECH_PAGES) {
    const fp = path.join(ROOT, t.slice(1));
    if (existsSync(fp)) {
      const lm = await lastmodFor(fp);
      lines.push(urlEntry(t, 0.65, 'monthly', lm));
    }
  }

  const blogDir = path.join(ROOT, 'blog');
  const blogFiles = (await readdir(blogDir)).filter(f => f.endsWith('.html')).sort();
  const seen = new Set();
  for (const f of blogFiles) {
    if (seen.has(f)) continue;
    seen.add(f);
    const slug = f.replace(/\.html$/, '');
    const fp = path.join(blogDir, f);
    const lm = await lastmodFor(fp);
    let priority = 0.55;
    if (PILLARS.has(slug)) priority = 0.8;
    else if (slug.startsWith('agencia') || slug.startsWith('metodologia')) priority = 0.7;
    lines.push(urlEntry(`/blog/${f}`, priority, 'monthly', lm));
  }

  lines.push('</urlset>');
  return lines.join('\n');
}

const xml = await buildSitemap();
await writeFile(path.join(ROOT, 'sitemap.xml'), xml, 'utf8');
const urlCount = (xml.match(/<url>/g) || []).length;
console.log(JSON.stringify({ updated: true, url_count: urlCount }, null, 2));
