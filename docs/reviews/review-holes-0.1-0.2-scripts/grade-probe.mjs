#!/usr/bin/env node
/* Second read, holes 0.1 and 0.2: what the engine's own graders (app/js/engine/grade.js: numGrade, numSetGrade, exprGrade,
   with the local Compute Engine) do with each typed part of number-sense problems-4, quadratics problems-4 and the new exam
   items, and with strings a learner would really type.
     - every answer and accept[] form must grade correct; every wrong[] must grade wrong and land on its own key (FAIL if not)
     - every TYPED row [file, item, part (1-based, 0 for an item with no parts), text, expected, finding?] must grade as
       expected; a row with a 6th field is one the reader holds to be a fault and prints as FINDING
   node docs/reviews/review-holes-0.1-0.2-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]     (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ALL = argv.includes('--all');
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

export const grade = (w, text) => {
  if (w.kind === 'expression') { const r = G.exprGrade(ce, w, text, text); return { ok: !!r.ok, key: r.key || null }; }
  if (G.isSetSpec(w)) { const r = G.numSetGrade(w, text); return { ok: !!r.ok, key: r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null) }; }
  const r = G.numGrade(w, text); return { ok: !!r.ok, key: r.key || (r.detail.value == null ? 'NOPARSE' : null) };
};

const NS = 'app/content/courses/number-sense/problems-4.json', QD = 'app/content/courses/quadratics/problems-4.json';
const E1 = 'app/content/exams/topic-0.1.json', E2 = 'app/content/exams/topic-0.2.json';
const EXAM_NEW = { [E1]: ['e-feed-updates', 'e-plan-hall', 'e-pit-area', 'e-partner-number', 'e-five-counts'], [E2]: ['e-two-desks', 'e-cubic-remainder'] };
const T = true, F = false;
const UNIT = 'a unit typed after the number: the field shows its help line and will not submit (no `unit` on the part)';
const TYPED = [
  // number-sense problems-4
  [NS, 'p-hall-tiles', 1, '108', T], [NS, 'p-hall-tiles', 1, '108 cm', T], [NS, 'p-hall-tiles', 1, '108cm', T], [NS, 'p-hall-tiles', 1, '1.08', F], [NS, 'p-hall-tiles', 1, '36', F],
  [NS, 'p-hall-tiles', 2, '12', T], [NS, 'p-hall-tiles', 2, '11', F],
  [NS, 'p-hall-tiles', 3, '20', T], [NS, 'p-hall-tiles', 3, '20 tiles', T],
  [NS, 'p-hall-tiles', 4, '23.328', T], [NS, 'p-hall-tiles', 4, '23.328 m^2', T, UNIT], [NS, 'p-hall-tiles', 4, '23.328 m²', T, UNIT], [NS, 'p-hall-tiles', 4, '23.33', F], [NS, 'p-hall-tiles', 4, '23.3', F], [NS, 'p-hall-tiles', 4, '233280', F],
  [NS, 'p-lawn-pond', 1, '28.27', T], [NS, 'p-lawn-pond', 1, '28.26', T], [NS, 'p-lawn-pond', 1, '28.29', T], [NS, 'p-lawn-pond', 1, '28.274', T], [NS, 'p-lawn-pond', 1, '28.3', F], [NS, 'p-lawn-pond', 1, '28', F],
  [NS, 'p-lawn-pond', 1, '9\\pi', F], [NS, 'p-lawn-pond', 1, '28.27 m²', T, UNIT], [NS, 'p-lawn-pond', 1, '113.04', F], [NS, 'p-lawn-pond', 1, '113.14', F], [NS, 'p-lawn-pond', 1, '18.84', F], [NS, 'p-lawn-pond', 1, '18.86', F],
  [NS, 'p-lawn-pond', 2, '79.73', T], [NS, 'p-lawn-pond', 2, '79.74', T], [NS, 'p-lawn-pond', 2, '79.71', T], [NS, 'p-lawn-pond', 2, '79.726', T], [NS, 'p-lawn-pond', 2, '79.7', F], [NS, 'p-lawn-pond', 2, '89.16', F], [NS, 'p-lawn-pond', 2, '89.14', F],
  [NS, 'p-lawn-pond', 3, '4', T], [NS, 'p-lawn-pond', 3, '4 boxes', T], [NS, 'p-lawn-pond', 3, '3.99', F], [NS, 'p-lawn-pond', 3, '3.9865', F],
  [NS, 'p-cycle-commute', 1, '32', T], [NS, 'p-cycle-commute', 1, '32 minutes', T], [NS, 'p-cycle-commute', 2, '27', T],
  [NS, 'p-cycle-commute', 4, '20', T], [NS, 'p-cycle-commute', 4, '20 km/h', T], [NS, 'p-cycle-commute', 4, '20kmh', T], [NS, 'p-cycle-commute', 4, '0.33', F], [NS, 'p-cycle-commute', 4, '1/3', F], [NS, 'p-cycle-commute', 4, '16.88', F], [NS, 'p-cycle-commute', 4, '16.9', F],
  [NS, 'p-cycle-commute', 5, '5.56', T], [NS, 'p-cycle-commute', 5, '5.556', T], [NS, 'p-cycle-commute', 5, '50/9', T], [NS, 'p-cycle-commute', 5, '5.56 m/s', T], [NS, 'p-cycle-commute', 5, '5.55', F], [NS, 'p-cycle-commute', 5, '5.6', F], [NS, 'p-cycle-commute', 5, '333.33', F],
  [NS, 'p-meshing-gears', 1, '144', T], [NS, 'p-meshing-gears', 2, '8', T], [NS, 'p-meshing-gears', 3, '30', T], [NS, 'p-meshing-gears', 3, '1/2', F],
  [NS, 'p-meshing-gears', 4, '45', T], [NS, 'p-meshing-gears', 4, '45 m', T, UNIT], [NS, 'p-meshing-gears', 4, '45.24', T], [NS, 'p-meshing-gears', 4, '45.22', T], [NS, 'p-meshing-gears', 4, '46', F], [NS, 'p-meshing-gears', 4, '4524 cm', F], [NS, 'p-meshing-gears', 4, '4522', F], [NS, 'p-meshing-gears', 4, '4526', F], [NS, 'p-meshing-gears', 4, '90.48', F],
  // quadratics problems-4
  [QD, 'p-park-pond', 1, '10', T], [QD, 'p-park-pond', 1, '10 m', T, UNIT], [QD, 'p-park-pond', 1, '\\sqrt{100}', F],
  [QD, 'p-park-pond', 2, '(x+2)^2+(y-3)^2=100', T], [QD, 'p-park-pond', 2, '(x+2)^2+(y-3)^2=10^2', T], [QD, 'p-park-pond', 2, '(y-3)^2+(x+2)^2=100', T], [QD, 'p-park-pond', 2, '100=(x+2)^2+(y-3)^2', T],
  [QD, 'p-park-pond', 2, 'x^2+4x+y^2-6y=87', T], [QD, 'p-park-pond', 2, '(x-(-2))^2+(y-3)^2=100', T], [QD, 'p-park-pond', 2, '\\left(x+2\\right)^2+\\left(y-3\\right)^2=100', T],
  [QD, 'p-park-pond', 2, '(x+2)^{2}+(y-3)^{2}=100', T], [QD, 'p-park-pond', 2, '\\sqrt{(x+2)^2+(y-3)^2}=10', F], [QD, 'p-park-pond', 2, '(x+2)^2+(y-3)^2', F], [QD, 'p-park-pond', 2, '(x+2)^2+(y-3)^2=r^2', F],
  [QD, 'p-park-pond', 2, '(x+2)^2+(y-3)^2=10', F], [QD, 'p-park-pond', 2, '(x-2)^2+(y-3)^2=100', F], [QD, 'p-park-pond', 2, '(x+2)^2+(y-3)^2=\\sqrt{100}', F], [QD, 'p-park-pond', 2, '(x+2)^2-(y-3)^2=100', F],
  [QD, 'p-park-pond', 3, '4, -10', T], [QD, 'p-park-pond', 3, '-10 and 4', T], [QD, 'p-park-pond', 3, 'x=4, x=-10', T], [QD, 'p-park-pond', 3, 'x = 4 or x = -10', T], [QD, 'p-park-pond', 3, '4', F], [QD, 'p-park-pond', 3, '11, -3', F], [QD, 'p-park-pond', 3, '4, 10', F],
  [QD, 'p-park-pond', 3, '-3 \\pm 7', T],
  [QD, 'p-park-pond', 4, '14', T], [QD, 'p-park-pond', 4, 'a=14', T], [QD, 'p-park-pond', 4, '14\\sqrt{2}', F], [QD, 'p-park-pond', 4, '19.8', F], [QD, 'p-park-pond', 4, '7', F],
  [QD, 'p-park-pond', 5, '19.14', T], [QD, 'p-park-pond', 5, '19.142', T], [QD, 'p-park-pond', 5, 'c=19.14', T], [QD, 'p-park-pond', 5, '19.1', F], [QD, 'p-park-pond', 5, '19.15', F], [QD, 'p-park-pond', 5, '19', F], [QD, 'p-park-pond', 5, '-9.14', F], [QD, 'p-park-pond', 5, '14.14', F],
  [QD, 'p-windy-ride', 1, '25v-32', T], [QD, 'p-windy-ride', 1, '-32+25v', T], [QD, 'p-windy-ride', 1, '(25v-32)', T], [QD, 'p-windy-ride', 1, '16(v-2)+9v', F], [QD, 'p-windy-ride', 1, '16v-32+9v', F], [QD, 'p-windy-ride', 1, '25v+32', F],
  [QD, 'p-windy-ride', 1, '\\frac{25v-32}{v(v-2)}', F], [QD, 'p-windy-ride', 1, '\\frac{16(v-2)+9v}{v(v-2)}', F],
  [QD, 'p-windy-ride', 2, '8, 1.14', T], [QD, 'p-windy-ride', 2, '1.14, 8', T], [QD, 'p-windy-ride', 2, '8, 8/7', T], [QD, 'p-windy-ride', 2, '8.00, 1.14', T], [QD, 'p-windy-ride', 2, '8 and 1.143', T], [QD, 'p-windy-ride', 2, 'v=8, v=1.14', T],
  [QD, 'p-windy-ride', 2, '8, 1.1', F], [QD, 'p-windy-ride', 2, '8, 1.15', F], [QD, 'p-windy-ride', 2, '8', F], [QD, 'p-windy-ride', 2, '8.54, 0.6', F],
  [QD, 'p-windy-ride', 3, '8', T], [QD, 'p-windy-ride', 3, '8 km/h', T], [QD, 'p-windy-ride', 3, '8/7', F], [QD, 'p-windy-ride', 3, '1.14', F], [QD, 'p-windy-ride', 3, '6', F],
  [QD, 'p-windy-ride', 4, '\\frac{9v}{16(v-2)}', T], [QD, 'p-windy-ride', 4, '\\frac{9v}{16v-32}', T], [QD, 'p-windy-ride', 4, '\\frac{9v}{-32+16v}', T], [QD, 'p-windy-ride', 4, '\\frac{9}{16}\\cdot\\frac{v}{v-2}', T],
  [QD, 'p-windy-ride', 4, '\\frac{9}{v-2}\\div\\frac{16}{v}', F, 'the division of the question typed back, not simplified, grades correct'],
  [QD, 'p-windy-ride', 4, '\\frac{\\frac{9}{v-2}}{\\frac{16}{v}}', F, 'a fraction over a fraction, the question itself, grades correct'],
  [QD, 'p-windy-ride', 4, '\\frac{9}{v-2}\\times\\frac{v}{16}', F, 'the flipped product, two fractions not one, grades correct'],
  [QD, 'p-windy-ride', 4, '\\frac{18v}{32(v-2)}', F, 'a fraction not in lowest terms grades correct'],
  [QD, 'p-windy-ride', 4, '\\frac{9v^2}{16v(v-2)}', F, 'a fraction with v left on top and bottom grades correct'],
  [QD, 'p-windy-ride', 4, '\\frac{9v}{16v-2}', F], [QD, 'p-windy-ride', 4, '\\frac{16(v-2)}{9v}', F], [QD, 'p-windy-ride', 4, '\\frac{144}{v(v-2)}', F], [QD, 'p-windy-ride', 4, '\\frac{9(v-2)}{16v}', F], [QD, 'p-windy-ride', 4, '0.75', F],
  [QD, 'p-windy-ride', 5, '0.75', T], [QD, 'p-windy-ride', 5, '.75', T], [QD, 'p-windy-ride', 5, '3/4', T], [QD, 'p-windy-ride', 5, '0.8', F], [QD, 'p-windy-ride', 5, '1.33', F], [QD, 'p-windy-ride', 5, '4/3', F], [QD, 'p-windy-ride', 5, '1.5', F],
  [QD, 'p-storage-crate', 1, '0', T], [QD, 'p-storage-crate', 1, 'V(-2)=0', F],
  [QD, 'p-storage-crate', 2, 'x^2+2x-3', T], [QD, 'p-storage-crate', 2, '(x^2+2x-3)', T], [QD, 'p-storage-crate', 2, '-3+2x+x^2', T], [QD, 'p-storage-crate', 2, 'x^{2}+2x-3', T],
  [QD, 'p-storage-crate', 2, '(x+3)(x-1)', T, 'the quotient typed in factorised form is refused; the question names no form'],
  [QD, 'p-storage-crate', 2, '\\frac{x^3+4x^2+x-6}{x+2}', F], [QD, 'p-storage-crate', 2, 'x^2+2x+3', F], [QD, 'p-storage-crate', 2, 'x^2+6x+13', F], [QD, 'p-storage-crate', 2, 'x^2+2x', F],
  [QD, 'p-storage-crate', 3, '(x+2)(x+3)(x-1)', T], [QD, 'p-storage-crate', 3, '(x-1)(x+3)(x+2)', T], [QD, 'p-storage-crate', 3, '(x+2)(x-1)(x+3)', T], [QD, 'p-storage-crate', 3, 'V(x)=(x+2)(x+3)(x-1)', T],
  [QD, 'p-storage-crate', 3, '(2+x)(3+x)(-1+x)', T], [QD, 'p-storage-crate', 3, '(x+2)(x^2+2x-3)', F], [QD, 'p-storage-crate', 3, 'x^3+4x^2+x-6', F], [QD, 'p-storage-crate', 3, '(x+2)(x+3)', F], [QD, 'p-storage-crate', 3, '(x^2+5x+6)(x-1)', F],
  [QD, 'p-storage-crate', 4, 'x-1', T], [QD, 'p-storage-crate', 4, '(x-1)', T], [QD, 'p-storage-crate', 4, '-1+x', T], [QD, 'p-storage-crate', 4, 'h=x-1', T],
  [QD, 'p-storage-crate', 4, '\\frac{(x+2)(x+3)(x-1)}{x^2+5x+6}', F], [QD, 'p-storage-crate', 4, '\\frac{(x+2)(x+3)(x-1)}{(x+2)(x+3)}', F], [QD, 'p-storage-crate', 4, '\\frac{x-1}{1}', T], [QD, 'p-storage-crate', 4, 'x+1', F],
  [QD, 'p-storage-crate', 5, '89.375', T], [QD, 'p-storage-crate', 5, '89.375 m^3', T, UNIT], [QD, 'p-storage-crate', 5, '715/8', T], [QD, 'p-storage-crate', 5, '89 3/8', T], [QD, 'p-storage-crate', 5, '89.38', F], [QD, 'p-storage-crate', 5, '89.4', F], [QD, 'p-storage-crate', 5, '35.75', F],
  // topic-0.1 new items
  [E1, 'e-feed-updates', 0, '351000', T], [E1, 'e-feed-updates', 0, '351,000', T], [E1, 'e-feed-updates', 0, '351 000', T], [E1, 'e-feed-updates', 0, '3.51e5', T], [E1, 'e-feed-updates', 0, '351000 updates', T],
  [E1, 'e-feed-updates', 0, '369000', F], [E1, 'e-feed-updates', 0, '5850', F], [E1, 'e-feed-updates', 0, '97.5', F], [E1, 'e-feed-updates', 0, '98', F], [E1, 'e-feed-updates', 0, '97', F],
  [E1, 'e-plan-hall', 0, '234', T], [E1, 'e-plan-hall', 0, '234 m^2', T, UNIT], [E1, 'e-plan-hall', 0, '234m²', T, UNIT], [E1, 'e-plan-hall', 0, '234 square metres', T, UNIT], [E1, 'e-plan-hall', 0, '234 sq m', T, UNIT], [E1, 'e-plan-hall', 0, '14.625', F], [E1, 'e-plan-hall', 0, '2340000', F],
  [E1, 'e-pit-area', 0, '199', T], [E1, 'e-pit-area', 0, '198.94', T], [E1, 'e-pit-area', 0, '199.04', T], [E1, 'e-pit-area', 0, '198.86', T], [E1, 'e-pit-area', 0, '199 m²', T, UNIT], [E1, 'e-pit-area', 0, '198', F], [E1, 'e-pit-area', 0, '200', F],
  [E1, 'e-pit-area', 0, '796', F], [E1, 'e-pit-area', 0, '795.77', F], [E1, 'e-pit-area', 0, '1963', F], [E1, 'e-pit-area', 0, '1964', F], [E1, 'e-pit-area', 0, '1962.5', F], [E1, 'e-pit-area', 0, '7854', F], [E1, 'e-pit-area', 0, '7850', F], [E1, 'e-pit-area', 0, '625/\\pi', F],
  [E1, 'e-partner-number', 0, '56', T], [E1, 'e-partner-number', 0, '1344', F], [E1, 'e-five-counts', 0, '3', T], [E1, 'e-five-counts', 0, '3 trades', T], [E1, 'e-five-counts', 0, '1', F],
  // topic-0.2 new items
  [E2, 'e-two-desks', 0, '3', T], [E2, 'e-two-desks', 0, '3 hours', T], [E2, 'e-two-desks', 0, 'x=3', T], [E2, 'e-two-desks', 0, '3h', F], [E2, 'e-two-desks', 0, '-2', F], [E2, 'e-two-desks', 0, '6', F], [E2, 'e-two-desks', 0, '3, -2', F],
  [E2, 'e-cubic-remainder', 1, '3', T], [E2, 'e-cubic-remainder', 1, 'k=3', T], [E2, 'e-cubic-remainder', 1, '15', F], [E2, 'e-cubic-remainder', 1, '-3', F], [E2, 'e-cubic-remainder', 1, '27', F],
  [E2, 'e-cubic-remainder', 2, '(x-2)(x+2)(x+3)', T], [E2, 'e-cubic-remainder', 2, '(x+3)(x-2)(x+2)', T], [E2, 'e-cubic-remainder', 2, '(x+2)(x+3)(x-2)', T], [E2, 'e-cubic-remainder', 2, 'p(x)=(x-2)(x+2)(x+3)', T],
  [E2, 'e-cubic-remainder', 2, '(2-x)(-2-x)(x+3)', T], [E2, 'e-cubic-remainder', 2, '(x+3)(x^2-4)', F], [E2, 'e-cubic-remainder', 2, '(x-2)(x^2+5x+6)', F], [E2, 'e-cubic-remainder', 2, 'x^3+3x^2-4x-12', F],
  [E2, 'e-cubic-remainder', 2, '(x-2)(x+2)(x-3)', F], [E2, 'e-cubic-remainder', 2, '(x-2)(x+2)', F], [E2, 'e-cubic-remainder', 2, 'x^2(x+3)-4(x+3)', F],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };

for (const file of [NS, QD, E1, E2]) {
  const doc = JSON.parse(fs.readFileSync(file, 'utf8'));
  const short = file.replace('app/content/', '');
  for (const it of doc.items) {
    if (EXAM_NEW[file] && !EXAM_NEW[file].includes(it.id)) continue;
    const parts = it.parts ? it.parts.map((p, i) => [i + 1, p]) : [[0, it]];
    for (const [n, p] of parts) {
      const w = p.widget, where = `${short} ${it.id}${n ? ' part ' + n : ''}`, by = (p.feedback && p.feedback.byKey) || {};
      if (!w || (w.kind !== 'numeric' && w.kind !== 'expression')) continue;
      if (w.kind === 'numeric' && G.isSetSpec(w)) {
        say(grade(w, w.answers.join(', ')).ok, null, `${where}: set answer grades correct`);
        say(grade(w, w.answers.slice().reverse().join(', ')).ok, null, `${where}: set answer reversed grades correct`);
        say(!!by.count, null, `${where}: has a "count" line`);
      } else if (w.kind === 'numeric') {
        say(grade(w, String(w.answer)).ok, null, `${where}: answer ${w.answer} grades correct`);
      } else {
        for (const a of [w.answer, ...(w.accept || [])]) { const r = grade(w, a); say(r.ok, null, `${where}: "${a}" grades correct (${JSON.stringify(r)})`); }
        if (w.form) say(!!by.form, null, `${where}: form "${w.form}" has a "form" line`);
      }
      for (const x of w.wrong || []) {
        const r = grade(w, String(x.value ?? x.tex));
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value ?? x.tex} lands on its key (got ok=${r.ok} key=${r.key})`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
      }
      for (const k of Object.keys(by)) if (!/^(form|count|length|r\d+c\d+)$/.test(k)) say((w.wrong || []).some(x => x.id === k), null, `${where}: byKey "${k}" has a wrong entry`);
      for (const r of TYPED.filter(r => r[0] === file && r[1] === it.id && r[2] === n)) {
        let res; try { res = grade(w, r[3]); } catch (e) { res = { ok: null, key: 'THROW ' + e.message }; }
        say(res.ok === r[4], r[5], `${where}: typed "${r[3]}" is ${res.ok ? 'accepted' : 'refused'} (key ${res.key}), expected ${r[4] ? 'accepted' : 'refused'}`);
      }
    }
  }
}
const used = new Set(TYPED.map(r => r[0] + r[1] + r[2]));
console.log(`grade-probe: ${checks} checks over ${used.size} parts, ${fails} failures, ${findings} findings (rows the reader holds to be faults)`);
process.exit(fails ? 1 : 0);
