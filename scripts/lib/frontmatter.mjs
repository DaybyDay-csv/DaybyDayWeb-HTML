#!/usr/bin/env node
// lib/frontmatter.mjs — single source of truth for YAML-lite frontmatter parsing.
//
// Used by:
//   - scripts/render-post.mjs        (strict: throws on missing/malformed block)
//   - scripts/qa-checklist.mjs       (lenient: returns { fm: {}, body } on missing block)
//   - scripts/verify-external-links.mjs (lenient: same)
//
// Frontmatter shape (deliberately YAML-subset, not full YAML):
//   ---
//   key: value
//   quoted: "string value"
//   list: ["a", "b", "c"]
//   ---
//   <body>
//
// Quirk: legacy sources written by migrate-legacy.mjs may emit single-quoted
// JSON arrays. We try a tolerant single->double quote normalization before
// giving up. The relaxed branch is intentional and matches the original
// inline behavior of the three call sites; do not tighten it without
// re-running all 124 sources through the new parser.
//
// Usage:
//   import { parseFrontmatter } from './lib/frontmatter.mjs';
//   const { fm, body } = parseFrontmatter(text);                 // lenient
//   const { fm, body } = parseFrontmatter(text, { strict: true }); // throws

export function parseFrontmatter(text, opts = {}) {
  const strict = opts.strict === true;

  if (!text.startsWith('---')) {
    if (strict) throw new Error('Missing frontmatter (---) at top of file');
    return { fm: {}, body: text };
  }

  const end = text.indexOf('\n---', 3);
  if (end === -1) {
    if (strict) throw new Error('Unterminated frontmatter (no closing ---)');
    return { fm: {}, body: text };
  }

  const raw = text.slice(3, end).trim();
  const body = text.slice(end + 4).replace(/^\n/, '');
  const fm = {};

  for (const line of raw.split('\n')) {
    const m = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
    if (!m) continue;
    const key = m[1].trim();
    let value = m[2].trim();

    if (value.startsWith('[') && value.endsWith(']')) {
      try {
        value = JSON.parse(value);
      } catch {
        const normalized = value
          .replace(/'/g, '"')
          .replace(/\\"/g, '\u0001')
          .replace(/"/g, '\\"')
          .replace(/\u0001/g, '\\"');
        try {
          value = JSON.parse(normalized);
        } catch {
          value = [];
        }
      }
    } else if (value.startsWith('"') && value.endsWith('"')) {
      value = value.slice(1, -1);
    }

    fm[key] = value;
  }

  return { fm, body };
}
