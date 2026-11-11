#!/usr/bin/env node
/* Second read, holes 1.6 and 2.1: what the engine's own numeric grader (app/js/engine/grade.js numGrade) does with each
   typed part of testing problems-4, stat-learning problems-4 and the new exam items (numeric widgets and editable table
   cells), and with strings a learner would really type.
     - every answer must grade correct; every wrong[] must grade wrong and land on its own key, with a byKey line (FAIL if not)
     - every TYPED row [file, item, part (1-based, 0 for an item with no parts; a table cell is part.cell, e.g. 1.2 or 0.1),
       text, expected, finding?] must grade as expected; a row with a 6th field is one the reader holds to be a fault
   node docs/reviews/review-holes-1.6-2.1-scripts/grade-probe.mjs [--all]     (from the repo root) */
import fs from 'node:fs';
import vm from 'node:vm';

const ALL = process.argv.includes('--all');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const grade = (w, text) => { const r = G.numGrade(w, text); return { ok: !!r.ok, key: r.key || (r.detail.value == null ? 'NOPARSE' : null) }; };

const TS = 'app/content/courses/testing/problems-4.json', SL = 'app/content/courses/stat-learning/problems-4.json';
const E1 = 'app/content/exams/topic-1.6.json', E2 = 'app/content/exams/topic-2.1.json';
const EXAM_NEW = { [E1]: ['s-uniform-moments', 's-chi-order-mix', 's-pool-rates', 's-pareto-losses'], [E2]: ['e-spline-slope', 'e-kmeans-spreads', 'e-unit-gradient'] };
const T = true, F = false;
const UNIT = 'a unit typed after the number is not read: the field shows its help line and will not submit (no `unit` on the part)';
const PCT = 'a per cent sign typed after a value the prose gives in per cent';
const TYPED = [
  // testing problems-4
  [TS, 'p-disk-failures', 1, '0.4', T], [TS, 'p-disk-failures', 1, '.4', T], [TS, 'p-disk-failures', 1, '0.40', T], [TS, 'p-disk-failures', 1, '2/5', T],
  [TS, 'p-disk-failures', 1, '0.4 failures a day', T, UNIT], [TS, 'p-disk-failures', 1, '0.4 a day', T, UNIT], [TS, 'p-disk-failures', 1, '0.025', F], [TS, 'p-disk-failures', 1, '40', F],
  [TS, 'p-disk-failures', 2, '250', T], [TS, 'p-disk-failures', 2, '250.0', T], [TS, 'p-disk-failures', 2, '40/0.16', T], [TS, 'p-disk-failures', 2, '16', F],
  [TS, 'p-disk-failures', 3, '0.0632', T], [TS, 'p-disk-failures', 3, '0.06325', T], [TS, 'p-disk-failures', 3, '0.063246', T], [TS, 'p-disk-failures', 3, '0.0633', F], [TS, 'p-disk-failures', 3, '0.063', F], [TS, 'p-disk-failures', 3, '0.06', F],
  [TS, 'p-disk-failures', 4, '0.004', T], [TS, 'p-disk-failures', 4, '1/250', T], [TS, 'p-disk-failures', 4, '0.0040', T], [TS, 'p-disk-failures', 4, '4e-3', T], [TS, 'p-disk-failures', 4, '0.00399', T], [TS, 'p-disk-failures', 4, '0.0041', F],
  [TS, 'p-disk-failures', 5, '0.95', T], [TS, 'p-disk-failures', 5, '19/20', T], [TS, 'p-disk-failures', 5, '38/40', T], [TS, 'p-disk-failures', 5, '0.9499', T], [TS, 'p-disk-failures', 5, '0.94989', T],
  [TS, 'p-disk-failures', 5, '95%', T, 'an efficiency typed as a percentage, as the explanation itself speaks ("only by 5%")'], [TS, 'p-disk-failures', 5, '0.952', F], [TS, 'p-disk-failures', 5, '0.9524', F],
  [TS, 'p-website-signups', 2, '4.5', T], [TS, 'p-website-signups', 2, '9/2', T], [TS, 'p-website-signups', 2, '54/12', T], [TS, 'p-website-signups', 2, '4.50', T], [TS, 'p-website-signups', 2, '4.5 sign-ups', T, UNIT],
  [TS, 'p-website-signups', 3, '0.375', T], [TS, 'p-website-signups', 3, '3/8', T], [TS, 'p-website-signups', 3, '0.38', F], [TS, 'p-website-signups', 3, '0.3750', T],
  [TS, 'p-website-signups', 4, '0.0833', T], [TS, 'p-website-signups', 4, '1/12', T], [TS, 'p-website-signups', 4, '0.08333', T], [TS, 'p-website-signups', 4, '0.083', F], [TS, 'p-website-signups', 4, '0.0834', F], [TS, 'p-website-signups', 4, '8.33%', T, 'an efficiency typed as a percentage'],
  [TS, 'p-website-signups', 5, '50', T], [TS, 'p-website-signups', 5, '50 hours', T], [TS, 'p-website-signups', 5, 'n=50', T], [TS, 'p-website-signups', 5, '49', F], [TS, 'p-website-signups', 5, '51', F], [TS, 'p-website-signups', 5, '38', F],
  [TS, 'p-bakery-loaves', 1, '28', T], [TS, 'p-bakery-loaves', 1, '28 loaves', T], [TS, 'p-bakery-loaves', 1, '28.0', T],
  [TS, 'p-bakery-loaves', 2, '7.143', T], [TS, 'p-bakery-loaves', 2, '50/7', T], [TS, 'p-bakery-loaves', 2, '7.1429', T], [TS, 'p-bakery-loaves', 2, '7.14', F], [TS, 'p-bakery-loaves', 2, '7.142', F], [TS, 'p-bakery-loaves', 2, '7.144', F], [TS, 'p-bakery-loaves', 2, '7.242', F],
  [TS, 'p-bakery-loaves', 3, '2', T], [TS, 'p-bakery-loaves', 3, '6', F],
  [TS, 'p-bakery-loaves', 4, '0.0281', T], [TS, 'p-bakery-loaves', 4, '0.02811', T], [TS, 'p-bakery-loaves', 4, '0.028108', T], [TS, 'p-bakery-loaves', 4, '0.028', F], [TS, 'p-bakery-loaves', 4, '0.0282', F], [TS, 'p-bakery-loaves', 4, '2.81%', T, 'a p-value typed as a percentage'],
  [TS, 'p-night-admissions', 1, '3.8', T], [TS, 'p-night-admissions', 1, '19/5', T], [TS, 'p-night-admissions', 1, '3.80', T], [TS, 'p-night-admissions', 1, '3.8 a night', T, UNIT],
  [TS, 'p-night-admissions', 2, '1.966', T], [TS, 'p-night-admissions', 2, '1.9655', T], [TS, 'p-night-admissions', 2, '1.9656', T], [TS, 'p-night-admissions', 2, '1.9664', T], [TS, 'p-night-admissions', 2, '1.97', F], [TS, 'p-night-admissions', 2, '1.965', F], [TS, 'p-night-admissions', 2, '1.936', F],
  [TS, 'p-night-admissions', 3, '0.6164', T], [TS, 'p-night-admissions', 3, '0.61644', T], [TS, 'p-night-admissions', 3, '0.616', F], [TS, 'p-night-admissions', 3, '0.6165', F], [TS, 'p-night-admissions', 3, '0.62', F],
  [TS, 'p-night-admissions', 4, '1.298', T], [TS, 'p-night-admissions', 4, '1.2978', T], [TS, 'p-night-admissions', 4, '1.2979', T], [TS, 'p-night-admissions', 4, '1.30', F], [TS, 'p-night-admissions', 4, '1.297', F], [TS, 'p-night-admissions', 4, 'z=1.298', T],
  [TS, 'p-night-admissions', 5, '20', T], [TS, 'p-night-admissions', 5, '20 nights', T], [TS, 'p-night-admissions', 5, '19.54', F], [TS, 'p-night-admissions', 5, '10', F],
  // stat-learning problems-4
  [SL, 'p-spam-filter', 1, '0.4', T], [SL, 'p-spam-filter', 1, '2/5', T], [SL, 'p-spam-filter', 1, '0.40', T], [SL, 'p-spam-filter', 1, '1/2.5', T],
  [SL, 'p-spam-filter', 2, '0.08', T], [SL, 'p-spam-filter', 2, '2/25', T], [SL, 'p-spam-filter', 2, '0.080', T], [SL, 'p-spam-filter', 2, '.08', T], [SL, 'p-spam-filter', 2, '0.8', F],
  [SL, 'p-spam-filter', 5, '2.24', T], [SL, 'p-spam-filter', 5, '2.236', T], [SL, 'p-spam-filter', 5, '2.2361', T], [SL, 'p-spam-filter', 5, 't=2.24', T], [SL, 'p-spam-filter', 5, '2.23', F], [SL, 'p-spam-filter', 5, '2.2', F], [SL, 'p-spam-filter', 5, '2.25', F],
  [SL, 'p-spam-filter', 5, '2.239', T],
  [SL, 'p-order-sizes', 1, '18', T], [SL, 'p-order-sizes', 1, '18%', T, PCT], [SL, 'p-order-sizes', 1, '18 %', T, PCT], [SL, 'p-order-sizes', 1, '18.0', T],
  [SL, 'p-order-sizes', 2, '22', T], [SL, 'p-order-sizes', 2, '22%', T, PCT],
  [SL, 'p-order-sizes', 3, '40', T], [SL, 'p-order-sizes', 3, '226', F], [SL, 'p-order-sizes', 3, '20', F],
  [SL, 'p-order-sizes', 4, '38.4', T], [SL, 'p-order-sizes', 4, '38.40', T], [SL, 'p-order-sizes', 4, '38.4 bp', T], [SL, 'p-order-sizes', 4, '38.4bp', T], [SL, 'p-order-sizes', 4, '192/5', T], [SL, 'p-order-sizes', 4, '38', F],
  [SL, 'p-order-sizes', 5, '12.4', T], [SL, 'p-order-sizes', 5, '12.4 bp', T], [SL, 'p-order-sizes', 5, '26', F], [SL, 'p-order-sizes', 5, '-12.4', F],
  [SL, 'p-one-unit', 1, '7', T], [SL, 'p-one-unit', 1, '7 hours', T], [SL, 'p-one-unit', 1, '7 h', T, UNIT], [SL, 'p-one-unit', 1, '3', F],
  [SL, 'p-one-unit', 2, '4.5', T], [SL, 'p-one-unit', 2, '9/2', T], [SL, 'p-one-unit', 2, '4.50', T], [SL, 'p-one-unit', 2, '-4.5', F],
  [SL, 'p-one-unit', 3, '-48', T], [SL, 'p-one-unit', 3, '−48', T], [SL, 'p-one-unit', 3, '- 48', T], [SL, 'p-one-unit', 3, '-48.0', T], [SL, 'p-one-unit', 3, '-24', F],
  [SL, 'p-one-unit', 4, '0.98', T], [SL, 'p-one-unit', 4, '.98', T], [SL, 'p-one-unit', 4, '49/50', T], [SL, 'p-one-unit', 4, 'w_1=0.98', T], [SL, 'p-one-unit', 4, '0.48', F],
  [SL, 'p-one-unit', 5, '1.020', T], [SL, 'p-one-unit', 5, '1.02', T], [SL, 'p-one-unit', 5, '1.0204', T], [SL, 'p-one-unit', 5, '50/49', T], [SL, 'p-one-unit', 5, '1.021', F, 'no fault: 1.021 is a wrong rounding; row kept to show the band'],
  [SL, 'p-one-unit', 5, '10.2', F], [SL, 'p-one-unit', 5, '10.2 km', F], [SL, 'p-one-unit', 5, '1.0', F],
  [SL, 'p-renewals', 1, '129', T], [SL, 'p-renewals', 1, '129 parameters', T], [SL, 'p-renewals', 1, '113', F], [SL, 'p-renewals', 1, '128', F],
  [SL, 'p-renewals', 3, '1.95', T], [SL, 'p-renewals', 3, '1.952', T], [SL, 'p-renewals', 3, '1.9518', T], [SL, 'p-renewals', 3, '1.96', F], [SL, 'p-renewals', 3, '2.0', F], [SL, 'p-renewals', 3, '1.9', F],
  [SL, 'p-renewals', 4, '1182', T], [SL, 'p-renewals', 4, '1,182', T], [SL, 'p-renewals', 4, '1182 rows', T], [SL, 'p-renewals', 4, '1181.25', F], [SL, 'p-renewals', 4, '1200', F],
  // topic-1.6 new items
  [E1, 's-uniform-moments', 0, '0.6', T], [E1, 's-uniform-moments', 0, '0.60', T], [E1, 's-uniform-moments', 0, '.6', T], [E1, 's-uniform-moments', 0, '0.599', T], [E1, 's-uniform-moments', 0, '0.5990', T], [E1, 's-uniform-moments', 0, '3/5', T],
  [E1, 's-uniform-moments', 0, '0.6 ticks', T], [E1, 's-uniform-moments', 0, '0.60 ticks', T], [E1, 's-uniform-moments', 0, '0.59', F], [E1, 's-uniform-moments', 0, '0.61', F], [E1, 's-uniform-moments', 0, '0.35', F], [E1, 's-uniform-moments', 0, '0.346', F],
  [E1, 's-chi-order-mix', 1.1, '5.23', T], [E1, 's-chi-order-mix', 1.1, '5.2267', T], [E1, 's-chi-order-mix', 1.1, '5.227', T], [E1, 's-chi-order-mix', 1.1, '392/75', T], [E1, 's-chi-order-mix', 1.1, '5.22', F], [E1, 's-chi-order-mix', 1.1, '5.2', F], [E1, 's-chi-order-mix', 1.1, '5.24', F],
  [E1, 's-chi-order-mix', 1.1, '4.928', F], [E1, 's-chi-order-mix', 1.2, '2', T], [E1, 's-chi-order-mix', 1.2, '1', F],
  [E1, 's-pool-rates', 0.1, '6.04', T], [E1, 's-pool-rates', 0.1, '6.0406', T], [E1, 's-pool-rates', 0.1, '6.041', T], [E1, 's-pool-rates', 0.1, '6.042', T], [E1, 's-pool-rates', 0.1, '6.05', F], [E1, 's-pool-rates', 0.1, '6.03', F],
  [E1, 's-pool-rates', 0.1, '6.00', F], [E1, 's-pool-rates', 0.1, '6', F], [E1, 's-pool-rates', 0.1, '3.02', F], [E1, 's-pool-rates', 0.1, '-6.04', F],
  [E1, 's-pool-rates', 0.2, '1', T], [E1, 's-pool-rates', 0.2, '0', F],
  [E1, 's-pareto-losses', 2, '2.5', T], [E1, 's-pareto-losses', 2, '5/2', T], [E1, 's-pareto-losses', 2, '2.50', T], [E1, 's-pareto-losses', 2, '80/32', T], [E1, 's-pareto-losses', 2, '3.5', F],
  [E1, 's-pareto-losses', 3, '0.0781', T], [E1, 's-pareto-losses', 3, '0.078125', T], [E1, 's-pareto-losses', 3, '0.07813', T], [E1, 's-pareto-losses', 3, '5/64', T], [E1, 's-pareto-losses', 3, '0.078', F], [E1, 's-pareto-losses', 3, '0.08', F], [E1, 's-pareto-losses', 3, '0.0782', T],
  [E1, 's-pareto-losses', 3, '0.0780', F],
  // topic-2.1 new items
  [E2, 'e-spline-slope', 0, '2.5', T], [E2, 'e-spline-slope', 0, '2.50', T], [E2, 'e-spline-slope', 0, '5/2', T], [E2, 'e-spline-slope', 0, '2.5 bp', T], [E2, 'e-spline-slope', 0, '2.5bp', T], [E2, 'e-spline-slope', 0, '2.5 bp a year', T, 'the placeholder\'s own words typed after the number'],
  [E2, 'e-spline-slope', 0, '2.5 basis points', T, UNIT], [E2, 'e-spline-slope', 0, '1', F], [E2, 'e-spline-slope', 0, '-1', F],
  [E2, 'e-kmeans-spreads', 0, '91', T], [E2, 'e-kmeans-spreads', 0, '91.0', T], [E2, 'e-kmeans-spreads', 0, '91 bp squared', T, 'the placeholder\'s own words typed after the number'], [E2, 'e-kmeans-spreads', 0, '91 bp^2', T, UNIT], [E2, 'e-kmeans-spreads', 0, '91 bp²', T, UNIT],
  [E2, 'e-kmeans-spreads', 0, '77', F], [E2, 'e-kmeans-spreads', 0, '13', F], [E2, 'e-kmeans-spreads', 0, '288.83', F],
  [E2, 'e-unit-gradient', 0, '-2.4', T], [E2, 'e-unit-gradient', 0, '−2.4', T], [E2, 'e-unit-gradient', 0, '-12/5', T], [E2, 'e-unit-gradient', 0, '-2.40', T], [E2, 'e-unit-gradient', 0, '-1.2', F], [E2, 'e-unit-gradient', 0, '0', F],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const seen = new Set();

for (const file of [TS, SL, E1, E2]) {
  const doc = JSON.parse(fs.readFileSync(file, 'utf8'));
  const short = file.replace('app/content/', '');
  for (const it of doc.items) {
    if (EXAM_NEW[file] && !EXAM_NEW[file].includes(it.id)) continue;
    const parts = it.parts ? it.parts.map((p, i) => [i + 1, p]) : [[0, it]];
    for (const [n, p] of parts) {
      const by = (p.feedback && p.feedback.byKey) || {};
      let specs = [];
      if (p.widget.kind === 'numeric') specs = [[n, p.widget]];
      else if (p.widget.kind === 'table') { let c = 0; for (const row of p.widget.rows) for (const cell of row) if (cell && cell.edit) { c++; specs.push([+(n + '.' + c), cell]); } }
      for (const [tag, w] of specs) {
        const where = `${short} ${it.id} ${tag}`;
        say(grade(w, String(w.answer)).ok, null, `${where}: answer ${w.answer} grades correct`);
        for (const x of w.wrong || []) {
          const r = grade(w, String(x.value));
          say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} lands on its key (got ok=${r.ok} key=${r.key})`);
          say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
        }
        for (const r of TYPED.filter(r => r[0] === file && r[1] === it.id && r[2] === tag)) {
          seen.add(r);
          let res; try { res = grade(w, r[3]); } catch (e) { res = { ok: null, key: 'THROW ' + e.message }; }
          say(res.ok === r[4], r[5], `${where}: typed "${r[3]}" is ${res.ok ? 'accepted' : 'refused'} (key ${res.key}), expected ${r[4] ? 'accepted' : 'refused'}`);
          if (ALL && !res.ok) console.log(`          key for "${r[3]}": ${res.key}`);
        }
      }
    }
  }
}
for (const r of TYPED) if (!seen.has(r)) { fails++; console.log('FAIL    row never used: ' + r.slice(1, 4).join(' ')); }
const used = new Set(TYPED.map(r => r[0] + r[1] + r[2]));
console.log(`grade-probe: ${checks} checks over ${used.size} parts, ${fails} failures, ${findings} findings (rows the reader holds to be faults)`);
process.exit(fails ? 1 : 0);
