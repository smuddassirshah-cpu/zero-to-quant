#!/usr/bin/env node
/* Delta read of the two holes fix passes: what the engine's own graders (app/js/engine/grade.js: numGrade for numeric parts
   and table cells, exprGrade with the local Compute Engine for expression parts) do with every changed part.
     - the answer and each accept[] form of an expression grade correct; each wrong[] entry grades wrong and lands on its own
       id, and has a byKey line (FAIL if not)
     - TYPED rows [typed, expected, note?]: expected is true (accepted), a wrong id or "form" (refused with that line),
       null (refused with the generic line) or "NOPARSE" (the field does not read it and will not submit).
       A row with a note is one the reader records in the review: it prints as FINDING and does not fail the run.
   node docs/reviews/review-delta-holes-scripts/grade.mjs --local-cdn <pkgs> [--show]      (from the repo root) */
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

const NS = 'courses/number-sense/problems-4', QD = 'courses/quadratics/problems-4', SL = 'courses/stat-learning/problems-4', TS = 'courses/testing/problems-4';
const E01 = 'exams/topic-0.1', E02 = 'exams/topic-0.2', E16 = 'exams/topic-1.6', E21 = 'exams/topic-2.1';
const UNIT = 'engine: a unit with a caret or in words stops the field (deferred by the fix pass, in the inbox)';
// [file, item, part (1-based; 0 = an item with no parts; "0.1" = first editable cell of a table), rows]
const TYPED = [
  [NS, 'p-hall-tiles', 1, [['120', true], ['120 cm', true], ['120cm', true], ['24', 'missing-prime'], ['1800', 'lcm'], ['1,800', 'lcm'], ['60', null], ['1.2 m', 'NOPARSE']]],
  [NS, 'p-hall-tiles', 2, [['16', true], ['16 sides', true], ['3', 'indices-multiplied'], ['8', 'indices-added'], ['36', 'lcm-carried'], ['15', null]]],
  [NS, 'p-hall-tiles', 3, [['15', true], ['15 tiles', true], ['8', 'rows-added'], ['375', 'small-tile-carried'], ['16', null]]],
  [NS, 'p-hall-tiles', 4, [['21.6', true], ['21.60', true], ['21.6 m²', true], ['21.6m²', true], ['108/5', true], ['2160', 'hundred'], ['216000', 'cm-squared'], ['216,000', 'cm-squared'],
    ['21.6 m^2', true, UNIT], ['21.6 square metres', true, UNIT], ['21.6 m2', true, UNIT], ['22', null], ['21.7', null]]],
  [NS, 'p-lawn-pond', 1, [['19.63', true], ['19.64', true], ['19.625', true], ['19.635', true], ['19.63 m²', true], ['19.6', null], ['19.66', null], ['78.54', 'diameter'], ['78.5', 'diameter'], ['15.71', 'circumference'], ['15.7', 'circumference']]],
  [NS, 'p-lawn-pond', 2, [['134.37', true], ['134.36', true], ['134.365', true], ['134.38', true], ['134.37 m²', true], ['134.4', null], ['138.29', 'circumference-carried'], ['30.37', 'perimeter'], ['154', null]]],
  [NS, 'p-lawn-pond', 3, [['9', true], ['9 tins', true], ['8', 'rounded-down'], ['10', 'circumference-carried'], ['11', 'whole-courtyard'], ['8.96', null]]],
  [NS, 'p-meshing-gears', 4, [['45', true], ['45 m', true], ['45m', true], ['45.24', true], ['45.2', true], ['90', 'radius'], ['4524', 'centimetres'], ['4524 cm', 'centimetres'], ['46', null]]],
  [NS, 'p-cycle-commute', 4, [['20', true], ['20 km/h', true], ['20km/h', true], ['20 kmh', true], ['20 km an hour', true, 'the question\'s own words for the unit ("km an hour") typed after the number']]],
  [NS, 'p-cycle-commute', 5, [['5.56', true], ['5.56 m/s', true], ['5.56m/s', true], ['5.556', true], ['5.6', null], ['5.56 metres a second', true, 'the question\'s own words for the unit typed after the number']]],
  [QD, 'p-park-pond', 1, [['10', true], ['10 m', true], ['10m', true], ['10 metres', true], ['14', 'added'], ['100', 'no-root']]],
  [QD, 'p-windy-ride', 1, [['25v-32', true], ['-32+25v', true], ['\\frac{25v-32}{v(v-2)}', 'whole'], ['\\frac{25v-32}{v^2-2v}', 'whole'], ['\\frac{16(v-2)+9v}{v(v-2)}', 'whole'], ['(25v-32)/(v(v-2))', 'whole'],
    ['16(v-2)+9v', 'form'], ['25v-18', 'own-bottoms'], ['25', 'tops-added']]],
  [QD, 'p-windy-ride', 3, [['8', true], ['8 km/h', true], ['8km/h', true], ['8/7', 'small-root'], ['1.14', 'small-root'], ['6', null], ['8 km an hour', true, 'the question\'s own words for the unit typed after the number']]],
  [QD, 'p-windy-ride', 4, [['9v', true], ['9*v', true], ['9\\cdot v', true], ['9\\times v', true], ['v9', true], ['v\\cdot9', true], ['(9v)', true], ['9 v', true],
    ['144', 'not-flipped'], ['9', 'dropped-v'], ['\\frac{9v}{16(v-2)}', 'whole'], ['\\frac{9v}{16v-32}', 'whole'], ['9v/(16(v-2))', 'whole'], ['\\frac{9}{v-2}\\div\\frac{16}{v}', 'whole'],
    ['\\frac{9}{v-2}\\times\\frac{v}{16}', 'whole'], ['\\frac{\\frac{9}{v-2}}{\\frac{16}{v}}', 'whole'], ['\\frac{18v}{32(v-2)}', 'whole'],
    ['16(v-2)', null], ['16v-32', null], ['18v', null], ['9v^2', null], ['72', null], ['9v-18', null], ['v', null], ['\\frac{9v}{16}', null], ['\\frac{9}{16}', null],
    ['\\frac{18v}{2}', true], ['3\\cdot3v', true]]],
  [QD, 'p-windy-ride', 5, [['0.75', true], ['.75', true], ['3/4', true], ['0.750', true], ['1.33', 'upside-down'], ['-0.75', 'small-root'], ['0.8', null]]],
  [QD, 'p-storage-crate', 2, [['x^2+2x-3', true], ['-3+2x+x^2', true], ['x^2-3+2x', true], ['(x+3)(x-1)', 'form'], ['(x-1)(x+3)', 'form'], ['x^2+2x+3', 'constant-sign'], ['x^2+6x+13', 'sign'], ['\\frac{x^3+4x^2+x-6}{x+2}', 'form']]],
  [QD, 'p-storage-crate', 5, [['89.375', true], ['89.375 m³', true], ['89.375m³', true], ['89.38', null], ['37.125', 'x-is-height'], ['35.75', 'base-only'], ['89.375 m^3', true, UNIT], ['89.375 cubic metres', true, UNIT]]],
  [E02, 'e-diameter-ends', 0, [['(x-1)^2+(y-6)^2=169', true], ['(y-6)^2+(x-1)^2=169', true], ['169=(x-1)^2+(y-6)^2', true], ['(x-1)^2+(y-6)^2=13^2', true], ['(1-x)^2+(6-y)^2=169', true],
    ['x^2+y^2-2x-12y-132=0', true], ['x^2-2x+y^2-12y=132', true], ['x^2+y^2=2x+12y+132', true], ['(x-1)^2+(y-6)^2-169=0', true], ['x^2-2x+1+y^2-12y+36=169', true],
    ['\\left(x-1\\right)^2+\\left(y-6\\right)^2=169', true], ['(x-1)^{2}+(y-6)^{2}=169', true], ['(x - 1)^2 + (y - 6)^2 = 169', true],
    ['2(x-1)^2+2(y-6)^2=338', true], ['\\sqrt{(x-1)^2+(y-6)^2}=13', null],
    ['(x+1)^2+(y+6)^2=169', 'signs'], ['(x-1)^2+(y-6)^2=13', 'radius-not-squared'], ['(x-1)^2+(y-6)^2=676', 'full-diameter'], ['(x-1)^2+(y-6)^2=26^2', 'full-diameter'],
    ['(x-1)^2+(y-6)^2', null], ['(x-1)^2+(y-6)^2=r^2', null], ['x^2+y^2=169', null], ['(x-6)^2+(y-1)^2=169', null], ['(x-1)^2+(y-6)^2=26', null], ['(x+4)^2+(y+6)^2=169', null],
    ['(x-1)^2+(y-6)^2=144', null], ['(x-1)+(y-6)=13', null], ['13', null], ['169', null], ['x^2+y^2-2x-12y+37=169', true], ['x^2+y^2-2x-12y-132', null],
    ['(x+1)^2+(y+6)^2=13', null], ['(x+1)^2+(y+6)^2=676', null]]],
  [E01, 'e-pit-area', 0, [['199', true], ['199 m²', true], ['198.94', true], ['198.9', true], ['199.04', true], ['201', 'rounded-radius'], ['201.06', 'rounded-radius'], ['200', null], ['796', 'diameter-as-radius'], ['1963', 'half-round'],
    ['7854', 'edge-as-radius'], ['199 square metres', true, UNIT + '; the question itself says "square metre"']]],
  [E01, 'e-feed-updates', 0, [['351000', true], ['351,000', true], ['369000', 'six-fifty'], ['369,000', 'six-fifty'], ['324000', 'six-hours'], ['5850', 'minutes-only']]],
  [E01, 'e-plan-hall', 0, [['234', true], ['234 m²', true], ['234m²', true], ['117', 'scale-once'], ['58.5', 'plan-area'], ['234 square metres', true, UNIT + '; the question itself says "square metres"']]],
  [SL, 'p-one-unit', 1, [['7', true], ['7 h', true], ['7h', true], ['7 hours', true], ['7 hrs', true], ['9', 'no-hidden-bias'], ['6', 'no-output-bias']]],
  [SL, 'p-one-unit', 4, [['0.596', true], ['.596', true], ['0.5960', true], ['w_1=0.596', true], ['149/250', true], ['0.6', null], ['0.60', null], ['0.404', 'uphill'], ['48.5', 'no-rate'], ['0.518', 'carried'],
    ['0.98', null], ['0.512', null], ['0.532', null], ['0.096', null]]],
  [SL, 'p-one-unit', 5, [['1.678', true], ['1.6779', true], ['1.6778', true], ['1.68', null], ['1.677', null], ['2', 'old-knot'], ['-1.678', 'sign'], ['−1.678', 'sign'], ['1.931', 'carried'], ['1.9305', 'carried'],
    ['16.78', null], ['16.8', null], ['16.78 km', null]]],
  [SL, 'p-order-sizes', 1, [['18', true], ['18.0', true], ['18%', 'percent-sign'], ['18 %', 'percent-sign'], ['0.18', 'percent-sign'], ['13', 'all-orders'], ['16', 'kept-centre'], ['22', 'six-misassigned']]],
  [SL, 'p-order-sizes', 2, [['22', true], ['22%', 'percent-sign'], ['22 %', 'percent-sign'], ['18', 'no-reassign'], ['13', 'all-orders']]],
  [SL, 'p-order-sizes', 3, [['40', true], ['226', 'not-settled'], ['91', 'carried'], ['12', 'unsquared'], ['6.67', 'averaged'], ['20', null]]],
  [SL, 'p-spam-filter', 4, [['0.667', true], ['.667', true], ['0.6667', true], ['0.6666', true], ['2/3', true], ['0.67', null], ['0.666', null], ['0.7', null], ['1.5', 'gave-norm'], ['1.333', 'street-width'],
    ['1.3333', 'street-width'], ['4/3', 'street-width'], ['1.33', null], ['0.4', 'unchanged'], ['0.24', null], ['0.444', null]]],
  [TS, 'p-disk-failures', 5, [['200', true], ['200.0', true], ['200 gaps', true], ['n=200', true], ['n = 200', true], ['198', 'numerator'], ['0.95', 'efficiency-now'], ['199', null], ['201', null], ['100', null],
    ['≥200', true, 'the question says "at least": a learner may type the answer as a bound'], ['>=200', true, 'the same'], ['n≥200', true, 'the same'], ['at least 200', true, 'the same'], ['n >= 200', true, 'the same']]],
  [E16, 's-pareto-losses', 2, [['2.5', true], ['5/2', true], ['2.50', true], ['80/32', true], ['0.4', 'upside-down'], ['3.5', 'exponent'], ['-2.5', 'sign'], ['−2.5', 'sign'], ['1.5', null]]],
  [E16, 's-pareto-losses', 3, [['0.0781', true], ['0.078125', true], ['0.07813', true], ['5/64', true], ['0.0782', true], ['0.078', null], ['0.0780', null], ['0.08', null], ['0.2795', 'sd'], ['12.8', 'info'], ['0.03125', 'theta-not-squared'],
    ['0.0313', 'theta-not-squared'], ['0.0312', 'theta-not-squared']]],
  [E16, 's-pool-rates', '0.1', [['6.04', true], ['6.041', true], ['6.042', true], ['6.0406', true], ['6.00', 'pearson'], ['6', 'pearson'], ['6.0', 'pearson'], ['3.02', 'no-two'], ['-6.04', 'sign'], ['6.05', null], ['6.03', null]]],
  [E16, 's-pool-rates', '0.2', [['1', true], ['2', 'model-size']]],
  [E21, 'e-odds-update', 0, [['21.5', true], ['21.5%', true], ['21.5 %', true], ['21.46', true], ['21.4', true], ['21.6', true], ['21.3', null], ['21.7', null], ['21', null], ['22', null], ['24.6', 'prob-times'], ['24.6%', 'prob-times'],
    ['27.3', 'odds-as-prob'], ['27.3%', 'odds-as-prob'], ['0.215', true, 'the probability typed as a fraction of 1 in a field whose unit is %'], ['0.2146', true, 'the same']]],
  [E21, 'e-spline-slope', 0, [['2.5', true], ['2.5 bp', true]]],
  [E21, 'e-kmeans-spreads', 0, [['91', true]]],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (SHOW) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const docs = {};
const doc = (f) => docs[f] || (docs[f] = JSON.parse(fs.readFileSync('app/content/' + f + '.json', 'utf8')));
for (const [file, id, part, rows] of TYPED) {
  const it = doc(file).items.find(i => i.id === id);
  let p = it, w;
  const pn = String(part).split('.');
  if (+pn[0] > 0) p = it.parts[+pn[0] - 1];
  w = p.widget;
  if (pn.length === 2) { const cells = []; for (const row of w.rows) for (const c of row) if (c && c.edit) cells.push(c); w = cells[+pn[1] - 1]; }
  const isExpr = w.kind === 'expression';
  const grade = isExpr ? expr : num;
  const by = (p.feedback && p.feedback.byKey) || {};
  const where = `${file.replace(/^(courses|exams)\//, '')} ${id} ${part}`;
  if (isExpr) {
    for (const a of [w.answer, ...(w.accept || [])]) say(grade(w, a) === true, null, `${where}: answer or accept "${a}" grades correct (got ${grade(w, a)})`);
    for (const x of w.wrong || []) { say(grade(w, x.tex) === x.id, null, `${where}: wrong ${x.id} "${x.tex}" lands on its id (got ${grade(w, x.tex)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`); }
    if (w.form) say(!!by.form, null, `${where}: form "${w.form}" has a byKey.form line`);
  } else {
    const shown = w.unit === '%' ? String(+(w.answer * 100).toFixed(6)) : String(w.answer);
    say(grade(w, shown) === true, null, `${where}: answer ${shown} grades correct (got ${grade(w, shown)})`);
    for (const x of w.wrong || []) { const t = w.unit === '%' ? String(+(x.value * 100).toFixed(6)) : String(x.value); say(grade(w, t) === x.id, null, `${where}: wrong ${x.id} ${t} lands on its id (got ${grade(w, t)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`); }
  }
  for (const [typed, want, note] of rows) {
    const got = grade(w, typed);
    say(got === want, note, `${where}: typed "${typed}" -> ${got === true ? 'accepted' : got === null ? 'refused, generic line' : got === 'NOPARSE' ? 'not read (field will not submit)' : 'refused, line "' + got + '"'}; expected ${want === true ? 'accepted' : want === null ? 'generic refusal' : want}`);
  }
}
console.log(`grade: ${checks} checks, ${fails} failures, ${findings} FINDING rows (recorded in the review)`);
process.exit(fails ? 1 : 0);
