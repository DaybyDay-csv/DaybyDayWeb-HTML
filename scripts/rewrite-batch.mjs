#!/usr/bin/env node
// rewrite-batch.mjs — orchestrates the full pipeline gate sequence for one or more
// legacy slugs, against the 6 gates currently wired in main post-PR #11.
//
// Usage:
//   node scripts/rewrite-batch.mjs <slug1> [slug2 ...]      # specific list
//   node scripts/rewrite-batch.mjs --next 5                 # first 5 legacy with migration_state: rendered
//   node scripts/rewrite-batch.mjs --all                    # all legacy with migration_state: rendered
//   node scripts/rewrite-batch.mjs --status                 # print inventory only
//
// For each slug, runs the 6 gates in order:
//   1. qa-checklist.mjs                  (Hormozi voice, estructura, contenido, SEO)
//   2. verify-external-links.mjs         (every external source must be 200)
//   3. render-post.mjs                   (produces blog/<slug>.html)
//   4. seo-pack.mjs                      (meta tags, schemas, OG, hreflang, etc.)
//   5. verify-render.mjs <slug> --local  (verifies the rendered HTML)
//   6. verify-internal-links.mjs         (every internal href resolves)
//
// If all 6 gates pass, the source .md is updated: migration_state "rendered" → "good".
// The 2 stages that do NOT touch blog/<slug>.html (qa-checklist, verify-external-links,
// verify-internal-links) run first against the .md. Then the 3 rendering stages run.
// This matches the order in scripts/build-static.sh.
//
// Exit codes:
//   0 — all slugs in the batch passed all 6 gates
//   1 — usage error
//   2 — at least one slug failed at least one gate
//   3 — at least one slug triggered qa-checklist REESCRIBIR / REGENERAR (needs human)

import { readFile, writeFile, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter } from './lib/frontmatter.mjs';

const execFileP = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

// Gate order: matches build-static.sh render_one() exactly.
const GATES = [
  { name: 'qa-checklist', script: 'qa-checklist.mjs', args: (s) => [s], timeoutMs: 30_000 },
  { name: 'verify-external-links', script: 'verify-external-links.mjs', args: (s) => [s], timeoutMs: 120_000 },
  { name: 'render-post', script: 'render-post.mjs', args: (s) => [s], timeoutMs: 30_000 },
  { name: 'seo-pack', script: 'seo-pack.mjs', args: (s) => [s], timeoutMs: 30_000 },
  { name: 'verify-render', script: 'verify-render.mjs', args: (s) => [s, '--local'], timeoutMs: 30_000 },
  { name: 'verify-internal-links', script: 'verify-internal-links.mjs', args: (s) => [s], timeoutMs: 30_000 },
];

// Sanity check: all 6 gate scripts must exist and parse before we start.
for (const g of GATES) {
  const p = path.join(__dirname, g.script);
  if (!existsSync(p)) {
    console.error(`[FATAL] gate script missing: ${p}`);
    process.exit(1);
  }
}

async function listLegacySlugs() {
  const contentDir = path.join(ROOT, 'content');
  const files = (await readdir(contentDir)).filter(f => f.endsWith('.md') && !f.startsWith('_'));
  const legacy = [];
  for (const f of files) {
    const text = await readFile(path.join(contentDir, f), 'utf8');
    const { fm } = parseFrontmatter(text, { strict: true });
    if (fm.migration_state === 'rendered') {
      legacy.push(f.replace(/\.md$/, ''));
    }
  }
  return legacy;
}

async function markSlugGood(slug) {
  const mdPath = path.join(ROOT, 'content', `${slug}.md`);
  if (!existsSync(mdPath)) {
    throw new Error(`md not found: ${mdPath}`);
  }
  const text = await readFile(mdPath, 'utf8');
  // Read current state to give a meaningful reason when no change happens.
  const { fm } = parseFrontmatter(text, { strict: true });
  const current = fm.migration_state || '(absent)';
  if (current !== 'rendered') {
    return { changed: false, reason: `migration_state was "${current}", not "rendered" — no change made` };
  }
  const updated = text.replace(
    /^migration_state:\s*"rendered"\s*$/m,
    'migration_state: "good"'
  );
  await writeFile(mdPath, updated, 'utf8');
  return { changed: true, reason: 'promoted rendered → good' };
}

async function runGate(gate, slug) {
  const start = Date.now();
  const args = gate.args(slug);
  try {
    const { stdout, stderr } = await execFileP('node', [path.join(__dirname, gate.script), ...args], {
      timeout: gate.timeoutMs,
      maxBuffer: 10 * 1024 * 1024,
    });
    return {
      gate: gate.name,
      slug,
      exitCode: 0,
      durationMs: Date.now() - start,
      stdout,
      stderr,
      pass: true,
    };
  } catch (err) {
    const exitCode = typeof err.code === 'number' ? err.code : 1;
    return {
      gate: gate.name,
      slug,
      exitCode,
      durationMs: Date.now() - start,
      stdout: err.stdout || '',
      stderr: err.stderr || '',
      pass: false,
    };
  }
}

function summarizeGate(result) {
  if (result.pass) {
    return `  PASS  ${result.gate.padEnd(24)} ${result.durationMs}ms`;
  }
  // For qa-checklist, interpret exit codes 2/3 as verdict signals, not plain failures.
  if (result.gate === 'qa-checklist' && (result.exitCode === 2 || result.exitCode === 3)) {
    const verdict = result.exitCode === 2 ? 'REGENERAR' : 'REESCRIBIR';
    return `  ${verdict.padEnd(7)} qa-checklist             ${result.durationMs}ms  (verdict: ${verdict})`;
  }
  return `  FAIL  ${result.gate.padEnd(24)} ${result.durationMs}ms  exit=${result.exitCode}`;
}

async function processSlug(slug) {
  const slugReport = { slug, gates: [], markedGood: false, needsHuman: false };
  for (const gate of GATES) {
    const r = await runGate(gate, slug);
    slugReport.gates.push(r);
    if (!r.pass) {
      // qa-checklist exit 2/3 = needs human, not a hard fail.
      if (gate.name === 'qa-checklist' && (r.exitCode === 2 || r.exitCode === 3)) {
        slugReport.needsHuman = true;
        // Still stop the chain for this slug — the source has banned phrases or
        // low scores and must be rewritten before re-running.
        return slugReport;
      }
      return slugReport;
    }
  }
  // All 6 passed — promote the .md.
  try {
    const m = await markSlugGood(slug);
    slugReport.markedGood = m.changed;
    slugReport.markReason = m.reason;
  } catch (err) {
    slugReport.markError = err.message;
  }
  return slugReport;
}

function printReport(reports) {
  console.log('');
  console.log('='.repeat(70));
  console.log('  REWRITE-BATCH REPORT');
  console.log('='.repeat(70));
  let pass = 0, fail = 0, human = 0;
  for (const r of reports) {
    console.log('');
    console.log(`[${r.slug}]`);
    for (const g of r.gates) {
      console.log(summarizeGate(g));
      if (!g.pass && g.gate === 'qa-checklist' && (g.exitCode === 2 || g.exitCode === 3)) {
        human++;
      } else if (!g.pass) {
        fail++;
      }
    }
    if (r.gates.every(g => g.pass)) {
      const markMsg = r.markedGood
        ? 'PROMOTED to migration_state: good'
        : `GATES PASSED (no promotion: ${r.markReason || r.markError || 'unknown'})`;
      console.log(`  → ${markMsg}`);
      pass++;
    } else if (r.needsHuman) {
      console.log('  → NEEDS HUMAN REWRITE (qa-checklist rejected the source)');
    } else {
      console.log('  → STOPPED at first failing gate; fix and re-run for this slug');
    }
  }
  console.log('');
  console.log('-'.repeat(70));
  console.log(`  ${pass} passed · ${fail} failed · ${human} need human rewrite · ${reports.length} total`);
  console.log('='.repeat(70));
}

// ---- CLI parsing ----

const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--status') {
  const all = await listLegacySlugs();
  console.log(`Legacy inventory: ${all.length} slugs with migration_state: "rendered"`);
  for (const s of all) console.log('  ' + s);
  process.exit(0);
}

let slugs = [];
if (args[0] === '--all') {
  slugs = await listLegacySlugs();
  console.log(`[rewrite-batch] --all: ${slugs.length} legacy slugs queued`);
} else if (args[0] === '--next') {
  const n = parseInt(args[1] || '5', 10);
  if (!Number.isFinite(n) || n < 1) {
    console.error('Usage: --next N (N must be a positive integer)');
    process.exit(1);
  }
  const all = await listLegacySlugs();
  slugs = all.slice(0, n);
  console.log(`[rewrite-batch] --next ${n}: ${slugs.length} legacy slugs queued`);
} else {
  slugs = args;
  console.log(`[rewrite-batch] explicit list: ${slugs.length} slugs`);
}

if (slugs.length === 0) {
  console.log('Nothing to do.');
  process.exit(0);
}

console.log('[rewrite-batch] gate order: ' + GATES.map(g => g.name).join(' → '));
console.log('');

const reports = [];
for (const slug of slugs) {
  console.log(`[rewrite-batch] processing ${slug} ...`);
  const r = await processSlug(slug);
  reports.push(r);
  for (const g of r.gates) console.log(summarizeGate(g));
  if (r.gates.every(g => g.pass)) {
    const markMsg = r.markedGood
      ? 'PROMOTED to migration_state: good'
      : `GATES PASSED (no promotion: ${r.markReason || r.markError || 'unknown'})`;
    console.log(`  → ${markMsg}`);
  } else if (r.needsHuman) {
    console.log('  → NEEDS HUMAN REWRITE');
  } else {
    console.log('  → STOPPED at first failure');
  }
  console.log('');
}

printReport(reports);

const anyFail = reports.some(r => !r.gates.every(g => g.pass) && !r.needsHuman);
const anyHuman = reports.some(r => r.needsHuman);

if (anyFail) process.exit(2);
if (anyHuman) process.exit(3);
process.exit(0);
