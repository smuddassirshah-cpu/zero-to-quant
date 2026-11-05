#!/usr/bin/env node
// PLAN 2c item 11 content transform (ENGINE-BACKLOG 562). Removes the stored stage `hours` field from curriculum.json: a stage's hours are
// the sum of its topic hours (js/hours.js), and the engine already ignores the stored figure. Text edit only: each stage-level
// `"hours": N,` line (six spaces of indent, inside a stage and before its first topic) is deleted; topic hours and every other byte stay.
// Idempotent: run twice, same result.
//   node app/tools/apply-item11-content.mjs [--dir <content dir>] [--dry]
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const arg = (k) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const DIR = arg('--dir') || join(dirname(fileURLToPath(import.meta.url)), '..', 'content');
const DRY = process.argv.includes('--dry');
const f = join(DIR, 'curriculum.json');
const text = readFileSync(f, 'utf8');
const lines = text.split('\n');
const out = [];
let removed = 0, inTopics = false;
for (const line of lines) {
  if (/^ {4}\{\s*$/.test(line)) inTopics = false;           // a stage object opens
  else if (/^ {6}"topics":/.test(line)) inTopics = true;     // its topics follow; stage-level fields come before
  if (!inTopics && /^ {6}"hours":\s*\d+,?\s*$/.test(line)) { removed++; continue; }
  out.push(line);
}
const next = out.join('\n');
JSON.parse(next);   // still valid JSON, or throw before writing
if (!DRY && next !== text) writeFileSync(f, next);
console.log(`item 11: ${removed} stage hours line(s) ${DRY ? 'would be ' : ''}removed from curriculum.json${removed ? '' : ' (already absent)'}`);
