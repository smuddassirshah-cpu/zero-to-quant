#!/usr/bin/env node
/* ENGINE-BACKLOG 621: for every exam in content, the minutes the Learn chip shows (ZQ.content.examMinutes, read from the
   manifest) equal the minutes the exam screen runs (a paper's `minutes`, or 60 when absent, summed over the papers; the
   top-level `minutes` for a single-paper exam). Also checks that learn.js reads the helper, not the hours-based guess.
   Usage: node tools/test-exam-minutes.mjs   Exit 0 when all pass, 1 on a failure. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CONTENT = path.join(APP, 'content');
const win = { ZQ: {} };
const fetchStub = async (url) => {
  const f = path.join(CONTENT, String(url).replace(/^content\//, '').split('?')[0]);
  if (!fs.existsSync(f)) return { ok: false, status: 404, json: async () => null };
  return { ok: true, status: 200, json: async () => JSON.parse(fs.readFileSync(f, 'utf8')) };
};
const ctx = vm.createContext({ window: win, fetch: fetchStub, console, document: undefined, setTimeout, clearTimeout });
vm.runInContext(fs.readFileSync(path.join(APP, 'js/content.js'), 'utf8'), ctx);
await win.ZQ.content.ready;
const C = win.ZQ.content;

// What exam.js runs (screens/exam.js run(): one paper from the top level, or the paper parts)
const runs = (doc) => (Array.isArray(doc.parts) ? doc.parts.filter(p => p.kind === 'paper') : [doc]).reduce((a, p) => a + (+p.minutes || 60), 0);

let fails = 0, n = 0;
for (const f of fs.readdirSync(path.join(CONTENT, 'exams')).filter(x => x.endsWith('.json'))) {
  const id = f.replace(/\.json$/, '');
  const doc = JSON.parse(fs.readFileSync(path.join(CONTENT, 'exams', f), 'utf8'));
  const want = runs(doc);
  const got = typeof C.examMinutes === 'function' ? C.examMinutes(id) : undefined;
  n++;
  if (got !== want) { fails++; console.log(`FAIL ${id}: chip ${got}, exam runs ${want}`); }
}
const learn = fs.readFileSync(path.join(APP, 'js/screens/learn.js'), 'utf8');
if (!/C\.examMinutes\('topic-'/.test(learn)) { fails++; console.log('FAIL learn.js examChip does not read C.examMinutes'); }
console.log(fails ? `${fails} failed of ${n} exams` : `All passed (${n} exams)`);
process.exit(fails ? 1 : 0);
