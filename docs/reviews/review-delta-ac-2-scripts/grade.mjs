#!/usr/bin/env node
/* Delta read AC-2: the engine's own graders (app/js/engine/grade.js: numGrade, and exprGrade with the local Compute
   Engine) on every numeric or expression item whose key, band or wrong[] the two fix passes changed. No browser.
     - the stored answer and each accept[] form of an expression grade correct
     - each wrong[] entry lands on its own id and has a byKey line; each byKey line has a wrong[] entry
     - numeric: no wrong band reaches the key band or another wrong band
     - TYPED rows [typed, expected, note?]: expected is true (accepted), a wrong id, or null (refused, generic line).
       A row with a note is one the review records: it prints FINDING and does not fail the run.
   node docs/reviews/review-delta-ac-2-scripts/grade.mjs --local-cdn <pkgs> [--show]      (from the repo root; exit 1 on FAIL) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const SHOW = argv.includes('--show');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return r.ok ? true : (r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null)); };
const expr = (w, t) => { let r; try { r = G.exprGrade(ce, w, t, t); } catch (e) { return 'THROW ' + e.message; } return r.ok ? true : (r.key || null); };

const DEC = 'the `decimal` band (0.0005, widened from the 0.00002 proposed) takes in other slips typed as decimals (finding 4)';
// [file under app/content, item id, part (1-based; 0 = no parts), rows]
const TYPED = [
  // ---- bank part 2, fix pass of review-delta-bank-2
  ['bank/statistics-2', 'collinear-features-inflation-factor', 0, [['1.33', true], ['1.3333', true], ['4/3', true], ['1.333', true], ['1.34', null], ['1.32', null], ['1.3', null],
    ['2', 'one-minus-r'], ['2.00', 'one-minus-r'], ['1.15', 'standard-error-factor'], ['1.155', 'standard-error-factor'], ['1.1547', 'standard-error-factor'], ['1.16', null],
    ['1.5625', null], ['1.56', null], ['2.5', null], ['1.25', null], ['0.75', null], ['4', null]]],
  ['bank/statistics-3', 'weak-signal-daily-edge', 0, [['1.75', true], ['7/4', true], ['1.750', true], ['1.74', null], ['1.76', null], ['1.8', null],
    ['0.05', 'no-root'], ['0.79', 'annual-sharpe'], ['0.794', 'annual-sharpe'], ['0.7937', 'annual-sharpe'], ['0.8', null], ['1', null], ['0.04', null], ['0.63', null], ['27.78', null]]],
  ['bank/statistics-1', 'sample-size-for-signal-sharpe-years', 0, [['7.4', true], ['7.44', true], ['7.438', true], ['900/121', true], ['7.4 years', true], ['7.3', null], ['7.5', null], ['7', null],
    ['2.7', 'no-square'], ['2.73', 'no-square'], ['2.727', 'no-square'], ['3.3', 'aimed-at-two'], ['3.31', 'aimed-at-two'], ['3.306', 'aimed-at-two'], ['18.4', null], ['4.3', null], ['8.2', null]]],
  ['bank/finance-3', 'op-payoff-short-strangle-loss', 0, [['-3', true], ['-£3', true], ['£-3', true], ['-3.00', true], ['−3', true], ['3', 'unsigned'], ['£3', 'unsigned'], ['3.00', 'unsigned'],
    ['-9', 'no-premium'], ['6', 'premium-only'], ['9', null], ['-6', null], ['-15', null]]],
  ['bank/coding-1', 'pf-types-round-half-even', 0, [['-12', true], ['−12', true], ['-10', 'all-towards-zero'], ['-11', 'half-up'], ['-13', 'half-away'], ['12', null], ['-14', null]]],
  ['bank/statistics-1', 'es-mle-waits-between-trades', 0, [['0.2', true], ['1/5', true], ['.2', true], ['0.20', true], ['5', 'mean-wait'], ['0.1667', 'five-gaps'], ['0.167', 'five-gaps'], ['1/6', 'five-gaps'], ['0.17', null]]],
  // ---- holes, fix pass of review-delta-holes
  ['courses/number-sense/problems-4', 'p-lawn-pond', 3, [['12', true], ['12 tins', true], ['11', 'rounded-down'], ['13', 'whole-courtyard'], ['11.2', null], ['11.20', null], ['9', null], ['10', null], ['8', null], ['144', null]]],
  ['courses/quadratics/problems-4', 'p-windy-ride', 4, [['9v', true], ['9*v', true], ['v9', true], ['9\\cdot v', true], ['(9v)', true], ['72', 'number'], ['144', 'not-flipped'], ['9', 'dropped-v'],
    ['\\frac{9v}{16(v-2)}', 'whole'], ['\\frac{9v}{16v-32}', 'whole'], ['9v/(16(v-2))', 'whole'], ['\\frac{72}{96}', null], ['0.75', null], ['96', null], ['16(v-2)', null], ['9\\cdot8', 'number'], ['9\\times 8', 'number']]],
  ['courses/testing/problems-4', 'p-disk-failures', 5, [['200', true], ['198', 'numerator'], ['0.95', 'efficiency-now'], ['199', null], ['201', null], ['100', null]]],
  ['exams/topic-2.1', 'e-odds-update', 0, [['16.7', true], ['16.7%', true], ['16.72', true], ['16.722', true], ['16.6', true], ['16.8', true], ['16.9', null], ['16.5', null], ['17', null],
    ['12', 'prob-times'], ['12.0', 'prob-times'], ['12.05', 'prob-times'], ['20.1', 'odds-as-prob'], ['20.08', 'odds-as-prob'], ['20', 'odds-as-prob'], ['68.9', 'sign'], ['68.88', 'sign'],
    ['0.167', 'decimal'], ['0.1672', 'decimal'], ['0.17', 'decimal'],
    ['0.201', null, DEC], ['0.2', null, DEC], ['0.2008', null, DEC], ['0.12', null, DEC], ['0.1205', null, DEC], ['0.15', null, DEC],
    ['0.689', null], ['0.4', null], ['40', null], ['21.5', null], ['24.6', null], ['27.3', null], ['28.6', null], ['83.3', null]]],
  ['exams/topic-0.2', 'e-diameter-ends', 0, [['(x-1)^2+(y-6)^2=289', true], ['(y-6)^2+(x-1)^2=289', true], ['289=(x-1)^2+(y-6)^2', true], ['(x-1)^2+(y-6)^2=17^2', true], ['(1-x)^2+(6-y)^2=289', true],
    ['x^2+y^2-2x-12y-252=0', true], ['x^2-2x+y^2-12y=252', true], ['x^2+y^2=2x+12y+252', true], ['(x-1)^2+(y-6)^2-289=0', true], ['x^2-2x+1+y^2-12y+36=289', true],
    ['\\left(x-1\\right)^2+\\left(y-6\\right)^2=289', true], ['(x-1)^{2}+(y-6)^{2}=289', true], ['2(x-1)^2+2(y-6)^2=578', true],
    ['(x+1)^2+(y+6)^2=289', 'signs'], ['(x-1)^2+(y-6)^2=17', 'radius-not-squared'], ['(x-1)^2+(y-6)^2=1156', 'full-diameter'], ['(x-1)^2+(y-6)^2=34^2', 'full-diameter'],
    ['(x-1)^2+(y-6)^2=169', null], ['x^2+y^2-2x-12y-132=0', null], ['(x-1)^2+(y-6)^2=34', null], ['(x-6)^2+(y-1)^2=289', null], ['x^2+y^2-2x-12y+252=0', null], ['x^2+y^2-2x-12y-252', null]]],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, note, msg) => {
  checks++;
  if (note) { findings++; console.log('FINDING ' + msg + ' | ' + note); return; }
  if (!ok) { fails++; console.log('FAIL    ' + msg); } else if (SHOW) console.log('ok      ' + msg);
};
const docs = {};
const doc = (f) => docs[f] || (docs[f] = JSON.parse(fs.readFileSync('app/content/' + f + '.json', 'utf8')));
for (const [file, id, part, rows] of TYPED) {
  const it = doc(file).items.find(i => i.id === id);
  if (!it) { say(false, null, `${file} ${id}: item missing`); continue; }
  const p = part ? it.parts[part - 1] : it, w = p.widget;
  const isExpr = w.kind === 'expression', grade = isExpr ? expr : num;
  const by = (p.feedback && p.feedback.byKey) || {};
  const where = `${file} ${id}${part ? ' part ' + part : ''}`;
  if (isExpr) {
    for (const a of [w.answer, ...(w.accept || [])]) say(grade(w, a) === true, null, `${where}: answer or accept "${a}" grades correct (got ${grade(w, a)})`);
    for (const x of w.wrong || []) { say(grade(w, x.tex) === x.id, null, `${where}: wrong ${x.id} "${x.tex}" lands on its id (got ${grade(w, x.tex)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`); }
  } else {
    const pct = w.unit === '%', typedOf = (v) => (pct ? String(+(v * 100).toFixed(6)) : String(v));
    say(grade(w, typedOf(w.answer)) === true, null, `${where}: answer ${typedOf(w.answer)} grades correct`);
    const kt = (w.tol && w.tol.abs) || 0;
    for (const x of w.wrong || []) {
      const xt = (x.tol && x.tol.abs) || 0;
      say(grade(w, typedOf(x.value)) === x.id, null, `${where}: wrong ${x.id} ${typedOf(x.value)} lands on its id (got ${grade(w, typedOf(x.value))})`);
      say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`);
      say(Math.abs(x.value - w.answer) - kt - xt > 1e-12, null, `${where}: band of ${x.id} is clear of the key band`);
      for (const y of w.wrong) if (y !== x) say(Math.abs(x.value - y.value) - xt - ((y.tol && y.tol.abs) || 0) > 1e-12, null, `${where}: bands of ${x.id} and ${y.id} are apart`);
    }
  }
  for (const k of Object.keys(by)) say((w.wrong || []).some(x => x.id === k) || k === 'form', null, `${where}: byKey line ${k} has a wrong entry`);
  for (const [typed, want, note] of rows) {
    const got = grade(w, typed);
    const txt = (v) => (v === true ? 'accepted' : v === null ? 'refused, generic line' : v === 'NOPARSE' ? 'not read' : 'refused, line "' + v + '"');
    say(got === want, note && got !== want ? note : null, `${where}: typed "${typed}" -> ${txt(got)}${got === want ? '' : '; expected ' + txt(want)}`);
  }
}
// the fix proposed in finding 4: the same widget with the `decimal` band at 0.00006
{
  const w = JSON.parse(JSON.stringify(doc('exams/topic-2.1').items.find(i => i.id === 'e-odds-update').widget));
  w.wrong.find(x => x.id === 'decimal').tol.abs = 0.00006;
  for (const [typed, want] of [['16.7', true], ['16.6', true], ['0.167', 'decimal'], ['0.1672', 'decimal'], ['0.16722', 'decimal'], ['0.17', 'decimal'], ['0.166', 'decimal'], ['0.168', 'decimal'],
    ['0.201', null], ['0.2', null], ['0.2008', null], ['0.12', null], ['0.1205', null], ['0.15', null], ['12', 'prob-times'], ['20.1', 'odds-as-prob'], ['68.9', 'sign']]) {
    const got = num(w, typed);
    say(got === want, null, `PROPOSED e-odds-update decimal band 0.00006: typed "${typed}" -> ${got}; expected ${want}`);
  }
}
console.log(`grade: ${checks} checks, ${fails} failures, ${findings} FINDING rows (recorded in the review)`);
process.exit(fails ? 1 : 0);
