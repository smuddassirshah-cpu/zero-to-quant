#!/usr/bin/env node
// precision-candidates.mjs: PLAN 2c item 9 (F08, N05). Lists every summary line in the
// precision-read courses that contains a quantifier a counterexample could break.
// Run from anywhere: node app/tools/precision-candidates.mjs [--json] [--courses a,b] [--words w,x]
// Fields read: summary.ideas[], summary.trap, summary.formula.note of each lesson file l*.json.
// Output: one line per candidate (file:line field words text), then counts by course and word.
// The five-word set (only, exactly when, any, always, never) reproduces the 69 lines of the
// course-correction review at 1e67d6f; "all" and "iff" are added for this read.
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
const arg = (k) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const COURSES = (arg('--courses') || 'ito,measure-prob,pdes,markov,limits-thm,random-vars,research-int').split(',');
const WORDS = (arg('--words') || 'only,exactly when,any,always,never,all,iff').split(',');
const FIVE = ['only', 'exactly when', 'any', 'always', 'never'];
const re = (w) => new RegExp(`\\b${w.replace(/ /g, '\\s+')}\\b`, 'i');

const rows = [];
for (const c of COURSES) {
  const dir = join(APP, 'content', 'courses', c);
  const files = readdirSync(dir).filter((f) => /^l\d+.*\.json$/.test(f)).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)));
  for (const f of files) {
    const raw = readFileSync(join(dir, f), 'utf8');
    const s = JSON.parse(raw).summary || {};
    const parts = (s.ideas || []).map((t, i) => [`ideas[${i}]`, t]);
    if (s.trap) parts.push(['trap', s.trap]);
    if (s.formula && typeof s.formula === 'object' && s.formula.note) parts.push(['formula.note', s.formula.note]);
    const lines = raw.split('\n');
    for (const [field, text] of parts) {
      const hit = WORDS.filter((w) => re(w).test(String(text)));
      if (!hit.length) continue;
      const enc = JSON.stringify(text).slice(1, -1);
      const line = lines.findIndex((l) => l.includes(enc)) + 1;
      rows.push({ id: rows.length + 1, course: c, file: `${c}/${f}`, line, field, words: hit, five: hit.some((w) => FIVE.includes(w)), text });
    }
  }
}

if (process.argv.includes('--json')) { console.log(JSON.stringify(rows, null, 1)); process.exit(0); }
for (const r of rows) console.log(`${String(r.id).padStart(3)} ${r.file}:${r.line} ${r.field} [${r.words.join(', ')}] ${r.text}`);
const by = (k) => rows.reduce((m, r) => { for (const v of [].concat(r[k])) m[v] = (m[v] || 0) + 1; return m; }, {});
console.log('== by course', JSON.stringify(by('course')));
console.log('== by word', JSON.stringify(by('words')));
console.log(`== candidates ${rows.length}; with the five-word set ${rows.filter((r) => r.five).length}`);
