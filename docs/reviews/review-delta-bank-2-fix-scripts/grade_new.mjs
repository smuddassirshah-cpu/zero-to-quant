#!/usr/bin/env node
/* Fix pass of review-delta-bank-2: the engine's own numeric grader (app/js/engine/grade.js numGrade) on every typed answer
   whose item the fix pass changed (findings 1, 2, 4, 11, 12). Same rules as the reader's grade.mjs: the stored answer is
   accepted, every wrong[] value lands on its own id and has a line, no band touches another, each TYPED row is as expected.
   node docs/reviews/review-delta-bank-2-fix-scripts/grade_new.mjs      (from the repo root; exit 1 on a FAIL) */
import fs from 'node:fs';
import vm from 'node:vm';

const SHOW = process.argv.includes('--show');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return r.ok ? true : (r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null)); };

const items = {};
for (const f of fs.readdirSync('app/content/bank')) {
  if (!/^(statistics|finance|coding)-\d\.json$/.test(f)) continue;
  for (const it of JSON.parse(fs.readFileSync('app/content/bank/' + f, 'utf8')).items) items[it.id] = [f.replace('.json', ''), it];
}

const TYPED = {
  'collinear-features-inflation-factor': [['1.33', true], ['1.3333', true], ['1.333', true], ['4/3', true], ['1.34', null], ['1.3', null], ['2', 'one-minus-r'], ['2.00', 'one-minus-r'], ['1.15', 'standard-error-factor'], ['1.1547', 'standard-error-factor'],
    ['0.75', null], ['0.25', null], ['1.56', null], ['1.5625', null]],
  'sample-size-for-signal-sharpe-years': [['7.4', true], ['7.44', true], ['7.438', true], ['900/121', true], ['7.4 years', true], ['7.3', null], ['7.5', null], ['7', null], ['2.7', 'no-square'], ['2.73', 'no-square'], ['2.727', 'no-square'],
    ['3.3', 'aimed-at-two'], ['3.31', 'aimed-at-two'], ['3.306', 'aimed-at-two'], ['18.4', null], ['18.37', null]],
  'weak-signal-daily-edge': [['1.75', true], ['7/4', true], ['1.750', true], ['1.7', null], ['1.8', null], ['0.05', 'no-root'], ['0.0500', 'no-root'], ['0.79', 'annual-sharpe'], ['0.794', 'annual-sharpe'], ['0.7937', 'annual-sharpe'],
    ['1', null], ['1.00', null], ['0.63', null]],
  'op-payoff-short-strangle-loss': [['-3', true], ['-£3', true], ['£-3', true], ['-3.00', true], ['3', 'unsigned'], ['£3', 'unsigned'], ['3.00', 'unsigned'], ['-9', 'no-premium'], ['6', 'premium-only'], ['-6', null], ['-2', null]],
  'pf-types-round-half-even': [['-12', true], ['-10', 'all-towards-zero'], ['-11', 'half-up'], ['-13', 'half-away'], ['12', null], ['-14', null]],
};
let checks = 0, fails = 0, findings = 0;
const fail = (m) => { fails++; console.log('FAIL ' + m); };
for (const [id, rows] of Object.entries(TYPED)) {
  if (!items[id]) { fail('missing item ' + id); continue; }
  const [file, it] = items[id];
  const w = it.widget;
  checks++;
  if (num(w, String(w.answer)) !== true) fail(`${file}/${id}: stored answer ${w.answer} not accepted`);
  const keyTol = (w.tol && w.tol.abs) || 0;
  for (const x of w.wrong || []) {
    checks += 3;
    const got = num(w, String(x.value));
    if (got !== x.id) fail(`${file}/${id}: wrong value ${x.value} lands on ${got}, not ${x.id}`);
    if (!(it.feedback.byKey || {})[x.id]) fail(`${file}/${id}: wrong id ${x.id} has no byKey line`);
    const gap = Math.abs(x.value - w.answer) - keyTol - ((x.tol && x.tol.abs) || 0);
    if (gap <= 1e-12) fail(`${file}/${id}: band of ${x.id} touches the key band`);
    for (const y of w.wrong) {
      if (y === x) continue;
      if (Math.abs(x.value - y.value) - ((x.tol && x.tol.abs) || 0) - ((y.tol && y.tol.abs) || 0) < -1e-12) fail(`${file}/${id}: bands of ${x.id} and ${y.id} overlap`);
    }
  }
  for (const k of Object.keys(it.feedback.byKey || {})) { checks++; if (!(w.wrong || []).some(x => x.id === k)) fail(`${file}/${id}: byKey line ${k} has no wrong entry`); }
  for (const [typed, want, note] of rows) {
    checks++;
    const got = num(w, typed);
    if (note) { findings++; console.log(`FINDING ${file}/${id} typed "${typed}" -> ${got === true ? 'accepted' : got === null ? 'generic line' : got}: ${note}`); continue; }
    if (got !== want) fail(`${file}/${id} typed "${typed}" -> ${got}, expected ${want}`);
    else if (SHOW) console.log(`ok ${file}/${id} "${typed}" -> ${got}`);
  }
}
console.log(`${checks} checks over ${Object.keys(TYPED).length} items, ${fails} failures, ${findings} FINDING rows`);
process.exit(fails ? 1 : 0);
