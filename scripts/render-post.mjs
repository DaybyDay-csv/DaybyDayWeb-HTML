#!/usr/bin/env node
// render-post.mjs — converts content/<slug>.md to blog/<slug>.html using templates/post.html
// Pure node, no React, no JSX, no .map().

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter } from './lib/frontmatter.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function inlineMd(text) {
  let out = escapeHtml(text);
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/(^|[^*])\*([^*]+)\*(?!\*)/g, '$1<em>$2</em>');
  out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (m, text, url) => {
    const cleanUrl = url.replace(/^https?:\/\/(www\.)?daybydayconsulting\.com/, '').replace(/\.html$/, '').replace(/\/+$/, '');
    const finalUrl = cleanUrl.startsWith('/') || cleanUrl.startsWith('http') ? cleanUrl : `/${cleanUrl}`;
    return `<a href="${finalUrl}" rel="noopener noreferrer">${text}</a>`;
  });
  return out;
}

function mdToHtml(md) {
  const lines = md.split('\n');
  const out = [];
  let i = 0;
  let inList = null;
  let inTable = false;
  let tableHeader = null;
  let tableRows = [];

  function closeList() {
    if (inList) {
      out.push(`</${inList}>`);
      inList = null;
    }
  }
  function closeTable() {
    if (inTable) {
      let html = '<table><thead><tr>';
      for (const h of tableHeader) html += `<th>${inlineMd(h)}</th>`;
      html += '</tr></thead><tbody>';
      for (const row of tableRows) {
        html += '<tr>';
        for (const cell of row) html += `<td>${inlineMd(cell)}</td>`;
        html += '</tr>';
      }
      html += '</tbody></table>';
      out.push(html);
      inTable = false;
      tableHeader = null;
      tableRows = [];
    }
  }

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (trimmed.startsWith('<!-- ')) {
      i++;
      continue;
    }

    if (trimmed.startsWith('## ')) {
      closeList(); closeTable();
      out.push(`<h2>${inlineMd(trimmed.slice(3))}</h2>`);
      i++; continue;
    }
    if (trimmed.startsWith('### ')) {
      closeList(); closeTable();
      out.push(`<h3>${inlineMd(trimmed.slice(4))}</h3>`);
      i++; continue;
    }
    if (trimmed.startsWith('> ')) {
      closeList(); closeTable();
      const quoteLines = [];
      while (i < lines.length && lines[i].trim().startsWith('> ')) {
        quoteLines.push(lines[i].trim().slice(2));
        i++;
      }
      out.push(`<blockquote>${inlineMd(quoteLines.join(' '))}</blockquote>`);
      continue;
    }

    if (trimmed.startsWith('|') && trimmed.endsWith('|') && trimmed.length > 2) {
      const cells = trimmed.slice(1, -1).split('|').map(c => c.trim());
      const isSeparator = cells.every(c => /^:?-+:?$/.test(c));
      if (isSeparator) {
        i++; continue;
      }
      if (!inTable) {
        closeList();
        inTable = true;
        tableHeader = cells;
        tableRows = [];
      } else {
        tableRows.push(cells);
      }
      i++; continue;
    } else {
      closeTable();
    }

    if (/^[-*]\s+/.test(trimmed)) {
      if (inList !== 'ul') {
        closeList();
        inList = 'ul';
        out.push('<ul>');
      }
      out.push(`<li>${inlineMd(trimmed.replace(/^[-*]\s+/, ''))}</li>`);
      i++; continue;
    }
    if (/^\d+\.\s+/.test(trimmed)) {
      if (inList !== 'ol') {
        closeList();
        inList = 'ol';
        out.push('<ol>');
      }
      out.push(`<li>${inlineMd(trimmed.replace(/^\d+\.\s+/, ''))}</li>`);
      i++; continue;
    }
    closeList();

    if (trimmed === '') {
      i++; continue;
    }

    if (line.startsWith(':::') ) {
      const marker = line.trim();
      if (marker === ':::direct-answer' || marker === ':::pro-tip' || marker === ':::summary' || marker === ':::cifra') {
        const inner = [];
        i++;
        while (i < lines.length && !lines[i].trim().startsWith(':::')) {
          inner.push(lines[i]);
          i++;
        }
        i++;
        if (marker === ':::direct-answer') {
          out.push('<div class="direct-answer">' + inner.map(l => `<p>${inlineMd(l.replace(/^>\s*/, ''))}</p>`).join('') + '</div>');
        } else if (marker === ':::pro-tip') {
          out.push('<div class="pro-tip"><p>Pro tip</p>' + inner.map(l => `<p>${inlineMd(l.replace(/^>\s*/, ''))}</p>`).join('') + '</div>');
        } else if (marker === ':::summary') {
          out.push('<div class="summary-block">' + inner.map(l => `<p>${inlineMd(l.replace(/^>\s*/, ''))}</p>`).join('') + '</div>');
        } else if (marker === ':::cifra') {
          out.push(`<div class="cifra-que-abofetea">${inner.join(' ').trim()}</div>`);
        }
        continue;
      }
    }

    if (trimmed) {
      out.push(`<p>${inlineMd(trimmed)}</p>`);
    }
    i++;
  }
  closeList(); closeTable();
  return out.join('\n');
}

function buildFaqBlock(faq) {
  if (!faq || !faq.length) return '';
  const items = faq.map(qa =>
    `<div class="faq-item"><h3 class="faq-q">${escapeHtml(qa.q)}</h3><p class="faq-a">${escapeHtml(qa.a)}</p></div>`
  ).join('\n');
  return `<section class="faq-section">\n  <h2 style="font-size:1.5rem;font-weight:700;margin-bottom:1.5rem;">Preguntas frecuentes</h2>\n${items}\n</section>`;
}

function buildRelatedLinks(links) {
  if (!links || !links.length) return '';
  return links.map(l => {
    let url = l.url.startsWith('http') ? l.url : (l.url.startsWith('/') ? l.url : `/${l.url}`);
    url = url.replace(/\.html$/, '').replace(/\/+$/, '');
    return `          <a href="${escapeHtml(url)}">${escapeHtml(l.anchor)}</a>`;
  }).join('\n');
}

function buildSourcesBlock(sources) {
  if (!sources || !sources.length) return '';
  const items = sources.map((s, i) => {
    const url = (typeof s === 'string' ? s : (s.url || '')).replace(/^https?:\/\/(www\.)?daybydayconsulting\.com/, '').replace(/\.html$/, '').replace(/\/+$/, '');
    const label = typeof s === 'string' ? new URL(s).hostname : (s.label || new URL(s.url).hostname);
    const rel = (typeof s === 'object' && s.rel) || 'noopener noreferrer';
    return `<li><a href="${escapeHtml(url)}" rel="${rel}" target="_blank">${escapeHtml(label)}</a></li>`;
  }).join('\n');
  return `<section class="sources-block">\n  <h2>Fuentes y datos</h2>\n  <p>Cada cifra y afirmación de este artículo se sostiene en una fuente verificable. Las que respaldan este post:</p>\n  <ul>\n${items}\n  </ul>\n</section>`;
}

function buildSchema(fm, faq) {
  const canonicalNoExt = String(fm.canonical || '').replace(/\.html$/, '').replace(/\/+$/, '');
  const article = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: fm.title,
    description: fm.meta_desc,
    datePublished: fm.published_at,
    dateModified: fm.published_at,
    author: {
      '@type': 'Person',
      name: 'Pablo Santirso',
      url: 'https://www.daybydayconsulting.com/'
    },
    publisher: {
      '@type': 'Organization',
      name: 'DayByDay Consulting',
      url: 'https://www.daybydayconsulting.com/'
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': canonicalNoExt
    }
  };
  const faqSchema = faq && faq.length ? {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faq.map(qa => ({
      '@type': 'Question',
      name: qa.q,
      acceptedAnswer: {
        '@type': 'Answer',
        text: qa.a
      }
    }))
  } : null;
  const ld = [article, faqSchema].filter(Boolean).map(o =>
    `<script type="application/ld+json">${JSON.stringify(o)}</script>`
  ).join('\n');
  return ld;
}

async function renderPost(slug) {
  const mdPath = path.join(ROOT, 'content', `${slug}.md`);
  const htmlOut = path.join(ROOT, 'blog', `${slug}.html`);
  if (!existsSync(mdPath)) {
    throw new Error(`Source markdown not found: ${mdPath}`);
  }
  const raw = await readFile(mdPath, 'utf8');
  const { fm, body } = parseFrontmatter(raw, { strict: true });
  const tpl = await readFile(path.join(ROOT, 'templates', 'post.html'), 'utf8');

  const bodyHtml = mdToHtml(body);
  const faqBlock = buildFaqBlock(fm.faq);
  const relatedLinks = buildRelatedLinks(fm.internal_links);
  const sourcesBlock = buildSourcesBlock(fm.sources);
  const schema = buildSchema(fm, fm.faq);

  const wordCount = body.replace(/```[\s\S]*?```/g, ' ').split(/\s+/).filter(Boolean).length;

  let canonical = String(fm.canonical || `https://www.daybydayconsulting.com/blog/${slug}.html`);
  canonical = canonical.replace(/\.html$/, '').replace(/\/+$/, '');

  const replacements = {
    '{{TITLE}}': String(fm.title || ''),
    '{{META_DESC}}': String(fm.meta_desc || ''),
    '{{CANONICAL}}': canonical,
    '{{PUBLISHED_AT}}': String(fm.published_at || new Date().toISOString()),
    '{{CATEGORY}}': String(fm.category || 'Estrategia'),
    '{{H1}}': String(fm.h1 || fm.title || ''),
    '{{READING_TIME}}': String(fm.reading_time || Math.max(4, Math.round(wordCount / 220))),
    '{{ARTICLE_DATE}}': String(fm.article_date || (fm.published_at || '').slice(0, 10)),
    '{{BODY}}': bodyHtml,
    '{{FAQ_BLOCK}}': faqBlock,
    '{{SOURCES_BLOCK}}': sourcesBlock,
    '{{RELATED_LINKS}}': relatedLinks,
    '{{SCHEMA}}': schema,
    '{{CTA_TITLE}}': String(fm.cta_title || '¿Quieres aplicar esto en tu negocio?'),
    '{{CTA_DESC}}': String(fm.cta_desc || 'En 30 minutos analizamos tu situación y te decimos exactamente qué acciones tendrían más impacto.'),
    '{{CTA_HREF}}': String(fm.cta_href || '/contacto.html'),
    '{{CTA_LABEL}}': String(fm.cta_label || 'Solicitar diagnóstico gratuito'),
  };

  let out = tpl;
  for (const [k, v] of Object.entries(replacements)) {
    out = out.split(k).join(v);
  }

  await mkdir(path.dirname(htmlOut), { recursive: true });
  await writeFile(htmlOut, out, 'utf8');

  return {
    slug,
    outPath: htmlOut,
    wordCount,
    bodyLength: bodyHtml.length,
    hasFaq: !!(fm.faq && fm.faq.length),
    hasRelated: !!(fm.internal_links && fm.internal_links.length),
    schemaCount: (schema.match(/<script type="application\/ld\+json">/g) || []).length,
  };
}

const slug = process.argv[2];
if (!slug) {
  console.error('Usage: node render-post.mjs <slug>');
  process.exit(1);
}
try {
  const result = await renderPost(slug);
  console.log(JSON.stringify(result, null, 2));
} catch (err) {
  console.error('Render failed:', err.message);
  process.exit(1);
}
