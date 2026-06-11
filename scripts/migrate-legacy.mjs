#!/usr/bin/env node
// migrate-legacy.mjs — inventory the 123 blog posts, classify each as:
//   state-good     : no JSX .map() placeholders, no "coming soon" stub, renders cleanly
//   state-rendered : JSX placeholders present (table/list never populated), needs body rewrite
//   state-stub     : subdir index.html with "coming soon" placeholder, needs full rewrite
// For each non-good post, extracts:
//   - existing H2 titles (skeleton)
//   - existing FAQ Q&A pairs
//   - existing internal links
//   - existing meta description from <head>
//   - existing canonical
// Writes content/<slug>.md skeleton with [BODY-TO-REWRITE] markers under each H2
// so the human-grade Hormozi voice can be re-applied post-by-post.

import { readFile, writeFile, readdir, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

function htmlDecode(s) {
  return s
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&aacute;/g, 'á').replace(/&eacute;/g, 'é').replace(/&iacute;/g, 'í').replace(/&oacute;/g, 'ó').replace(/&uacute;/g, 'ú')
    .replace(/&Aacute;/g, 'Á').replace(/&Eacute;/g, 'É').replace(/&Iacute;/g, 'Í').replace(/&Oacute;/g, 'Ó').replace(/&Uacute;/g, 'Ú')
    .replace(/&ntilde;/g, 'ñ').replace(/&Ntilde;/g, 'Ñ');
}

function extractTitle(html) {
  const m = html.match(/<title>([^<]+)<\/title>/);
  return m ? htmlDecode(m[1].replace(/\s*\|\s*DayByDay Consulting\s*$/, '').trim()) : '';
}
function extractMeta(html, name) {
  const m = html.match(new RegExp(`<meta name="${name}" content="([^"]+)"`));
  return m ? htmlDecode(m[1]) : '';
}
function extractCanonical(html) {
  const m = html.match(/<link rel="canonical" href="([^"]+)"/);
  return m ? m[1] : '';
}
function extractH1(html) {
  const m = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
  return m ? htmlDecode(m[1].trim()) : '';
}
function extractArticleDate(html) {
  const m = html.match(/<span class="article-date">([^<]+)<\/span>/);
  return m ? m[1].trim() : '';
}
function extractReadingTime(html) {
  const m = html.match(/<span class="reading-time">(\d+)\s*min/);
  return m ? parseInt(m[1], 10) : 8;
}
function extractCategory(html) {
  const m = html.match(/<span class="category-badge">([^<]+)<\/span>/);
  return m ? htmlDecode(m[1].trim()) : 'Estrategia';
}
function hasJsxMap(html) {
  return /map\(\(\s*(row|item)/.test(html) || /\bmap\(\(row/.test(html);
}
function hasComingSoon(html) {
  return /coming soon|contenido completocoming/i.test(html);
}
function extractH2s(html) {
  const matches = [...html.matchAll(/<h2[^>]*>([^<]+)<\/h2>/g)];
  return matches.map(m => htmlDecode(m[1].trim())).filter(h => !h.startsWith('Artículos relacionados') && !h.startsWith('Preguntas frecuentes'));
}
function extractFaq(html) {
  const faq = [];
  const re = /<div class="faq-item">[\s\S]*?<h3[^>]*>([^<]+)<\/h3>[\s\S]*?<p[^>]*>([\s\S]+?)<\/p>[\s\S]*?<\/div>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    faq.push({ q: htmlDecode(m[1].trim()), a: htmlDecode(m[2].trim().replace(/<[^>]+>/g, '')) });
  }
  return faq;
}
function extractInternalLinks(html) {
  const seen = new Set();
  const links = [];
  const re = /<a href="(\/[^"#]+)">([^<]+)<\/a>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (seen.has(m[1])) continue;
    if (m[1].includes('blog.html') || m[1].includes('contacto') || m[1].endsWith('problema.html')) continue;
    if (m[1].includes('css/') || m[1].includes('js/') || m[1].includes('favicon')) continue;
    seen.add(m[1]);
    links.push({ url: m[1], anchor: htmlDecode(m[2].trim()).slice(0, 80) });
    if (links.length >= 4) break;
  }
  return links;
}

function skeletonMd(slug, meta) {
  const h2s = meta.h2s.length ? meta.h2s : ['Cuerpo del artículo'];
  const h2Section = h2s.map(h => `## ${h}\n\n[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.\n`).join('\n');
  const faqSection = meta.faq.length ? `\n## Preguntas frecuentes (mantener)\n\n${meta.faq.map(qa => `### ${qa.q}\n\n${qa.a}\n`).join('\n')}` : '';
  const linksSection = meta.internal_links.length ? `\n## Artículos relacionados (revisar, mantener 2 mejores)\n\n${meta.internal_links.map(l => `- [${l.anchor}](${l.url})`).join('\n')}` : '';
  return `---
title: "${meta.title}"
h1: "${meta.h1 || meta.title}"
slug: ${slug}
meta_desc: "${(meta.meta_desc || '').replace(/"/g, '\\"')}"
canonical: "${meta.canonical}"
category: "${meta.category}"
article_date: "${meta.article_date}"
reading_time: ${meta.reading_time}
published_at: "${meta.published_at || meta.article_date}T00:00:00+02:00"
primary_keyword: "${meta.primary_keyword || meta.title.split(' ').slice(0, 3).join(' ').toLowerCase()}"
secondary_keywords: ${JSON.stringify(meta.secondary_keywords || [])}
faq: ${JSON.stringify(meta.faq || [])}
internal_links: ${JSON.stringify((meta.internal_links || []).slice(0, 2))}
cta_title: "${(meta.cta_title || '¿Quieres aplicar esto en tu negocio?').replace(/"/g, '\\"')}"
cta_desc: "${(meta.cta_desc || 'En 30 minutos analizamos tu situación y te decimos exactamente qué acciones tendrían más impacto.').replace(/"/g, '\\"')}"
cta_href: "${meta.cta_href || '/contacto.html'}"
cta_label: "${meta.cta_label || 'Solicitar diagnóstico gratuito'}"
llms_summary: "${(meta.meta_desc || '').replace(/"/g, '\\"').slice(0, 200)}"
migration_state: "${meta.state}"
---

> Epígrafe pendiente. Una frase pegadiza + fecha, opcional pero recomendado.

${h2Section}

:::pro-tip
Pro tip pendiente: un giro contraintuitivo que el lector no espera. Etiquetarlo como "Pro tip" para que el renderer lo destaque visualmente.
:::

## Acción de hoy

Acción concreta ejecutable en menos de 30 minutos. Con número concreto (minutos, pasos, herramienta). Que el lector pueda hacerla esta misma tarde.

## Recap + cliffhanger

Cubrimos [3 cosas concretas del post]. La semana que viene: [tema del siguiente post con gancho concreto].
${faqSection}
${linksSection}
`;
}

async function classifyAndMigrate() {
  const blogDir = path.join(ROOT, 'blog');
  const contentDir = path.join(ROOT, 'content');
  await mkdir(contentDir, { recursive: true });

  const allFiles = (await readdir(blogDir)).filter(f => f.endsWith('.html')).sort();
  const inventory = { good: [], rendered: [], stub: [] };

  for (const f of allFiles) {
    const slug = f.replace(/\.html$/, '');
    const fpath = path.join(blogDir, f);
    const html = await readFile(fpath, 'utf8');

    const title = extractTitle(html);
    const meta_desc = extractMeta(html, 'description');
    const canonical = extractCanonical(html);
    const h1 = extractH1(html);
    const article_date = extractArticleDate(html);
    const reading_time = extractReadingTime(html);
    const category = extractCategory(html);
    const h2s = extractH2s(html);
    const faq = extractFaq(html);
    const internal_links = extractInternalLinks(html);

    let state;
    if (hasComingSoon(html)) state = 'stub';
    else if (hasJsxMap(html)) state = 'rendered';
    else state = 'good';

    const meta = { title, h1, meta_desc, canonical, category, article_date, reading_time, h2s, faq, internal_links, state };
    const mdPath = path.join(contentDir, `${slug}.md`);
    if (existsSync(mdPath)) {
      const existing = await readFile(mdPath, 'utf8');
      if (!existing.includes('[BODY-TO-REWRITE]') && !existing.includes('migration_state: "stub"')) {
        if (state === 'good') inventory.good.push(slug);
        else if (state === 'rendered') inventory.rendered.push(slug);
        else inventory.stub.push(slug);
        continue;
      }
    }
    const md = skeletonMd(slug, meta);
    await writeFile(mdPath, md, 'utf8');

    if (state === 'good') inventory.good.push(slug);
    else if (state === 'rendered') inventory.rendered.push(slug);
    else inventory.stub.push(slug);
  }

  const report = {
    total: allFiles.length,
    good: inventory.good.length,
    rendered_needs_body: inventory.rendered.length,
    stub_needs_full_rewrite: inventory.stub.length,
    rendered_slugs: inventory.rendered,
    stub_slugs: inventory.stub,
  };
  console.log(JSON.stringify(report, null, 2));
  await writeFile(path.join(contentDir, '_inventory.json'), JSON.stringify(report, null, 2), 'utf8');
}

await classifyAndMigrate();
