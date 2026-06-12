#!/usr/bin/env node
// qa-checklist.mjs — runs Checklist_PrePublicacion against a draft
// Outputs JSON with verdict: publicar | reescribir | regenerar
// Implements sections A (voz), B (estructura), C (contenido), D (lista negra), E (anti-IA), F (SEO), G (cierre)

import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter } from './lib/frontmatter.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

function splitSentences(text) {
  const stripped = text
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/\|[^\n]+\|/g, ' ')
    .replace(/```/g, ' ')
    .replace(/^>+\s*/gm, '')
    .replace(/^[-*]\s+/gm, '')
    .replace(/^\d+\.\s+/gm, '')
    .replace(/^#+\s+/gm, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/[*_`]/g, '');
  return stripped.split(/(?<=[.!?…])\s+|\n+/).map(s => s.trim()).filter(s => s.length > 0);
}

function wordCount(s) { return s.split(/\s+/).filter(Boolean).length; }

const BANNED_PHRASES = [
  /\bverdaderamente\b/i,
  /\bsinceramente\b/i,
  /\bhonestamente\b/i,
  /es importante destacar/i,
  /se podría considerar/i,
  /sería interesante explorar/i,
  /a nivel de/i,
  /en términos de/i,
  /\bholístico\b/i,
  /\bsinergia\b/i,
  /\btransversal\b/i,
  /como sabes/i,
  /como bien sabrás/i,
  /en el mundo actual/i,
  /en el panorama actual/i,
  /\bmuchos\b/i,
  /\bvarios\b/i,
  /\bdiversos\b/i,
  /\bnumerosos\b/i,
  /here'?s the thing/i,
  /but here'?s/i,
  /it'?s not\s+\w+, it'?s/i,
  /\bshift\b/i,
  /game[ -]changer/i,
  /revolutionize/i,
  /\bleverage\b/i,
  /\bsynergy\b/i,
  /what if i told you/i,
];

const ANTI_IA_PATTERNS = [
  { name: 'anaphora', re: /([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+ \w+[\.,])(\s*\1){2,}/g },
  { name: 'false_negative', re: /no (es|se trata de) [^,.;]+, (es|se trata de)/i },
  { name: 'reversal_framing', re: /la mayoría (de las? |de los? )?\w+ (piensa|cree|opina|asume)[^.]*\. (la verdad|la realidad|lo cierto)/i },
  { name: 'staccato', re: /(\b\w+[\.,]\s*){2,}\b\w+[\.,]\s*$/m },
  { name: 'rhetorical_open', re: /^[¿][^?]{0,40}\?\s*$/m },
  { name: 'i_seen', re: /i'?ve seen (this|it) (play out|happen|all the time)/i },
  { name: 'i_see_constantly', re: /i see this constantly/i },
  { name: 'most_opener', re: /^\s*Most /m },
];

function runChecks(slug) {
  return (async () => {
    const md = await readFile(path.join(ROOT, 'content', `${slug}.md`), 'utf8');
    const { fm, body } = parseFrontmatter(md);
    const sentences = splitSentences(body);
    const words = body.split(/\s+/).filter(Boolean);

    // A · VOZ
    const A = {};
    const sentenceLengths = sentences.map(wordCount);
    A.avg_sentence_length = sentenceLengths.length
      ? +(sentenceLengths.reduce((a, b) => a + b, 0) / sentenceLengths.length).toFixed(1)
      : 0;
    A.median_sentence_length = sentenceLengths.length
      ? sentenceLengths.sort((a, b) => a - b)[Math.floor(sentenceLengths.length / 2)]
      : 0;
    A.tuteo_violations = (body.match(/\b(usted|el lector|uno debe|nosotros como)\b/gi) || []).length;
    A.adverb_mente_count = (body.match(/\b\w+mente\b/gi) || []).length;
    A.score = 5;
    if (A.avg_sentence_length > 14) A.score -= 2;
    else if (A.avg_sentence_length > 12) A.score -= 1;
    if (A.tuteo_violations > 0) A.score -= 1;
    if (A.adverb_mente_count > 2) A.score -= 1;

    // B · ESTRUCTURA
    const B = {};
    B.has_epigrafe_or_quote = /(^> |^##\s+)/m.test(body);
    B.has_promise = /##\s+(lo que vas a aprender|en este post|qué vas a)/i.test(body);
    B.has_authority_drop = /(\d+[.,]?\d*)\s*(%|€|\$|x|veces|M€|K€|semanas|meses|días|años|clientes|cuentas)/.test(body);
    B.has_framework_named = /(método|framework|modelo|sistema|regla)\s+[A-ZÁÉÍÓÚÑ]{2,}/.test(body) || /##\s+los \d+ \w+/i.test(body) || /##\s+los tres /i.test(body) || /##\s+las \d+ /i.test(body);
    B.has_real_example = /(caso|cliente|cuenta|empresa).{0,200}\d/.test(body);
    B.has_pro_tip = /:::pro-tip|pro tip|:::cifra/i.test(body);
    B.has_action_step = /##\s+(acción|action step|próximos?\s+\d+ minutos|en los próximos)/i.test(body);
    B.has_recap = /(cubrimos|en este post (hemos visto|cubrimos|aprendiste)|recap|resumen)/i.test(body);
    B.score = 0;
    if (B.has_epigrafe_or_quote) B.score++;
    if (B.has_promise) B.score++;
    if (B.has_authority_drop) B.score++;
    if (B.has_framework_named) B.score++;
    if (B.has_real_example) B.score++;
    if (B.has_pro_tip) B.score++;
    if (B.has_action_step) B.score++;
    if (B.has_recap) B.score++;

    // C · CONTENIDO
    const C = {};
    const numbersFound = (body.match(/\b\d+(?:[.,]\d+)?(?:\s*[\$€%xMKB]|\s*(?:veces|días|semanas|meses|años|horas|minutos|cuentas|clientes|pedidos|euros))?/g) || []);
    C.concrete_numbers = new Set(numbersFound).size;
    C.uses_3plus_retoricos = [
      /más \w+ → más \w+/i.test(body),
      /aunque tengas [^,.;]+, no /i.test(body),
      /:::cifra/.test(body),
      /\?\s*\n+/.test(body) && /\?/.test(body.split('\n')[0] || ''),
      /\btres\b.*\btres\b.*\btres\b/i.test(body),
      /spoiler|zas|pum|boom/i.test(body)
    ].filter(Boolean).length >= 3;
    C.has_vulnerability = /(cagada|fallo|perdí|error|equivoc|cuesta|costó|aprendí|trocé)/i.test(body);
    C.has_authority = /\b\d{2,}\b/.test(body) && /(cliente|cuenta|caso|empresa)/i.test(body);
    C.has_utility = B.has_action_step;
    C.score = 0;
    if (C.concrete_numbers >= 3) C.score++;
    if (C.uses_3plus_retoricos) C.score++;
    if (C.has_vulnerability) C.score++;
    if (C.has_authority) C.score++;
    if (C.has_utility) C.score++;

    // D · LISTA NEGRA
    const D = { hits: [] };
    for (const re of BANNED_PHRASES) {
      const m = body.match(re);
      if (m) D.hits.push({ phrase: m[0], context: m.index });
    }
    D.count = D.hits.length;

    // E · ANTI-IA
    const E = { hits: [] };
    for (const p of ANTI_IA_PATTERNS) {
      const m = body.match(p.re);
      if (m) E.hits.push({ pattern: p.name, sample: m[0].slice(0, 80) });
    }
    const enConclusion = /(^|\n)\s*en conclusión[:\s]/i.test(body) || /(^|\n)\s*en resumen[:\s]/i.test(body) || /(^|\n)\s*en definitiva[:\s]/i.test(body);
    if (enConclusion) E.hits.push({ pattern: 'en_conclusion', sample: 'opening with "en conclusión/resumen/definitiva"' });
    E.count = E.hits.length;
    E.score = 5;
    E.score -= Math.min(E.count, 5);

    // F · SEO
    const F = {};
    F.title_length = (fm.title || '').length;
    F.meta_length = (fm.meta_desc || '').length;
    F.slug = fm.slug || slug;
    F.slug_kebab = /^[a-z0-9-]+$/.test(F.slug) && !F.slug.includes('--');
    F.keyword_in_h1 = !fm.primary_keyword || (fm.h1 || fm.title || '').toLowerCase().includes(String(fm.primary_keyword).toLowerCase().split(' ')[0]);
    F.score = 0;
    if (F.title_length > 0 && F.title_length <= 60) F.score++;
    if (F.meta_length > 0 && F.meta_length <= 155) F.score++;
    if (F.slug_kebab) F.score++;
    if (F.keyword_in_h1) F.score++;

    // G · CIERRE
    const G = {};
    G.has_cliffhanger = /próxim[oa]\s+(post|artículo|semana)|la semana que viene|en el siguiente|cubrimos \d+/i.test(body);
    G.passes = G.has_cliffhanger;

    // Verdict
    let verdict = 'publicar';
    const issues = [];
    if (D.count > 0) { verdict = 'regenerar'; issues.push(`${D.count} banned phrase hits`); }
    if (A.score < 4) { if (verdict === 'publicar') verdict = 'reescribir'; issues.push(`voice score ${A.score}/5`); }
    if (B.score < 7) { if (verdict === 'publicar') verdict = 'reescribir'; issues.push(`structure score ${B.score}/9`); }
    if (C.score < 4) { if (verdict === 'publicar') verdict = 'reescribir'; issues.push(`content score ${C.score}/5`); }
    if (E.count > 0) { if (verdict === 'publicar') verdict = 'reescribir'; issues.push(`${E.count} anti-IA hits`); }
    if (F.score < 4) { if (verdict === 'publicar') verdict = 'reescribir'; issues.push(`SEO score ${F.score}/4`); }
    if (!G.passes) { if (verdict === 'publicar') verdict = 'reescribir'; issues.push('cliffhanger missing'); }
    if (words.length < 1100 || words.length > 1700) {
      if (verdict === 'publicar') verdict = 'reescribir';
      issues.push(`word count ${words.length} (target 1200-1500)`);
    }

    const result = {
      slug,
      word_count: words.length,
      verdict,
      issues,
      scores: { voz: A, estructura: B, contenido: C, lista_negra: D, anti_ia: E, seo: F, cierre: G },
      blocks_to_rewrite: [
        ...(A.score < 4 ? ['A · voz'] : []),
        ...(B.score < 7 ? ['B · estructura'] : []),
        ...(C.score < 4 ? ['C · contenido'] : []),
        ...(D.count > 0 ? ['D · lista negra'] : []),
        ...(E.count > 0 ? ['E · anti-IA'] : []),
        ...(F.score < 4 ? ['F · SEO'] : []),
        ...(!G.passes ? ['G · cierre'] : []),
      ],
    };
    return result;
  })();
}

const slug = process.argv[2];
if (!slug) {
  console.error('Usage: node qa-checklist.mjs <slug>');
  process.exit(1);
}
const r = await runChecks(slug);
console.log(JSON.stringify(r, null, 2));
if (r.verdict === 'regenerar') process.exit(2);
if (r.verdict === 'reescribir') process.exit(3);
