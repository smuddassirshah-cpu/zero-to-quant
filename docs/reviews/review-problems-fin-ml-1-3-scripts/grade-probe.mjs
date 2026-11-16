#!/usr/bin/env node
/* Second read, fin-ml problems 1 to 3: what the engine's own numeric grader (app/js/engine/grade.js, numGrade) does with
   strings a learner would type. Rows: [set, item, part (1-based), text, expected ok, expected key or null, finding?].
   A row with a 7th field is one the reader holds to be a fault of the content; it prints as FINDING and does not fail.
   node docs/reviews/review-problems-fin-ml-1-3-scripts/grade-probe.mjs      (from anywhere) */
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync(path.join(ROOT, 'app/js/engine/grade.js'), 'utf8'), g);
const G = g.ZQ.grade;
const grade = (w, text) => { const r = G.numGrade(w, text); return { ok: !!r.ok, key: r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null) }; };
const sets = {}; for (const n of [1, 2, 3]) sets[n] = JSON.parse(fs.readFileSync(path.join(ROOT, `app/content/courses/fin-ml/problems-${n}.json`), 'utf8'));
const T = true, F = false;
const ROWS = [
  [1, 'p-index-fund-day', 1, '2.4', T, null], [1, 'p-index-fund-day', 1, '2.4%', T, null], [1, 'p-index-fund-day', 1, '1.2', F, 'no-root'], [1, 'p-index-fund-day', 1, '4.8%', F, 'times-h'],
  [1, 'p-index-fund-day', 2, '0', T, null], [1, 'p-index-fund-day', 2, '-1', F, null], [1, 'p-index-fund-day', 2, '+1', F, 'sign-only'],
  [1, 'p-index-fund-day', 3, '61.95', T, null], [1, 'p-index-fund-day', 3, '£61.95', T, null], [1, 'p-index-fund-day', 3, '61.952', T, null], [1, 'p-index-fund-day', 3, '59.90', F, 'root-h'],
  [1, 'p-index-fund-day', 5, '-3.28', T, null], [1, 'p-index-fund-day', 5, '-3.28%', T, null], [1, 'p-index-fund-day', 5, '-3.28125', T, null], [1, 'p-index-fund-day', 5, '-3.2', F, 'at-barrier'], [1, 'p-index-fund-day', 5, '3.28', F, 'no-sign'], [1, 'p-index-fund-day', 5, '2', F, 'day-four'],
  [1, 'p-copper-breakout', 2, '0.4167', T, null], [1, 'p-copper-breakout', 2, '5/12', T, null], [1, 'p-copper-breakout', 3, '2/3', T, null], [1, 'p-copper-breakout', 4, '0.8', T, null], [1, 'p-copper-breakout', 4, '0.80', T, null], [1, 'p-copper-breakout', 4, '4/5', T, null], [1, 'p-copper-breakout', 5, '8/11', T, null], [1, 'p-copper-breakout', 5, '0.7273', T, null], [1, 'p-copper-breakout', 5, '0.7333', F, 'mean'],
  [1, 'p-silver-windows', 2, '11/18', T, null], [1, 'p-silver-windows', 3, '2.5583', T, null], [1, 'p-silver-windows', 3, '2.5584', T, null], [1, 'p-silver-windows', 4, '0.57', T, null], [1, 'p-silver-windows', 4, '0.5700', T, null], [1, 'p-silver-windows', 5, '0.310', T, null], [1, 'p-silver-windows', 5, '0.31', T, null], [1, 'p-silver-windows', 5, '0.3095', T, null], [1, 'p-silver-windows', 5, '0.306', F, 'unweighted'],
  [1, 'p-bond-sign-model', 3, '40.9', T, null], [1, 'p-bond-sign-model', 4, '0.0764', T, null], [1, 'p-bond-sign-model', 4, '0.0774', F, 'base-p'], [1, 'p-bond-sign-model', 5, '0.46', T, null], [1, 'p-bond-sign-model', 5, '0.45', F, null],
  [2, 'p-gold-frac-weights', 1, '-0.11375', T, null], [2, 'p-gold-frac-weights', 1, '-0.1138', F, null], [2, 'p-gold-frac-weights', 2, '-0.0626', T, null], [2, 'p-gold-frac-weights', 2, '-0.0625625', T, null], [2, 'p-gold-frac-weights', 4, '2.379', T, null], [2, 'p-gold-frac-weights', 4, '2.378', T, null], [2, 'p-gold-frac-weights', 4, '2.366', F, 'reversed'],
  [2, 'p-retail-relative-volume', 2, '0.75', T, null], [2, 'p-retail-relative-volume', 2, '3/4', T, null], [2, 'p-retail-relative-volume', 3, '-0.035', T, null], [2, 'p-retail-relative-volume', 3, '-0.038', F, 'population'],
  [2, 'p-q3-earnings-join', 1, '6', T, null], [2, 'p-q3-earnings-join', 1, '6%', T, null], [2, 'p-q3-earnings-join', 1, '11', F, 'quarter-end'], [2, 'p-q3-earnings-join', 2, '0.6', T, null], [2, 'p-q3-earnings-join', 2, '3/5', T, null], [2, 'p-q3-earnings-join', 3, '1', T, null], [2, 'p-q3-earnings-join', 3, '1.0', T, null],
  [2, 'p-shipping-z', 1, '2.08', T, null], [2, 'p-shipping-z', 1, '1.70', F, 'population'], [2, 'p-shipping-z', 2, '1.12', T, null], [2, 'p-shipping-z', 2, '12.02', F, 'no-mean'],
  [2, 'p-shipping-z', 2, '12.01', F, 'no-mean', '25 over the unrounded sd 2.0817 is 12.01: the slip gets the generic line (finding)'],
  [2, 'p-shipping-z', 3, '25.33', T, null], [2, 'p-shipping-z', 3, '£25.33', T, null], [2, 'p-shipping-z', 4, '-0.07', T, null], [2, 'p-shipping-z', 4, '-0.09', F, 'population'],
  [3, 'p-five-day-sizing', 1, '0.28', T, null], [3, 'p-five-day-sizing', 1, '0.34', F, 'kelly'], [3, 'p-five-day-sizing', 2, '1.3', T, null], [3, 'p-five-day-sizing', 2, '1.25', F, 'raw-sizes'], [3, 'p-five-day-sizing', 3, '3900', T, null], [3, 'p-five-day-sizing', 3, '£3,900', T, null], [3, 'p-five-day-sizing', 4, '9', T, null], [3, 'p-five-day-sizing', 4, '9 bp', T, null],
  [3, 'p-trial-log-dsr', 2, '0.53', T, null], [3, 'p-trial-log-dsr', 2, '0.62', F, 'runs'], [3, 'p-trial-log-dsr', 3, '0.0286', T, null], [3, 'p-trial-log-dsr', 3, '0.0282', F, 'normal'], [3, 'p-trial-log-dsr', 4, '0.954', T, null], [3, 'p-trial-log-dsr', 4, '0.955', T, null], [3, 'p-trial-log-dsr', 4, '0.933', F, 'runs'],
  [3, 'p-futures-net-psr', 2, '0.60', T, null], [3, 'p-futures-net-psr', 2, '0.6', T, null], [3, 'p-futures-net-psr', 3, '0.0370', T, null], [3, 'p-futures-net-psr', 3, '0.0480', F, 'annual'],
  [3, 'p-futures-net-psr', 3, '0.0479', F, 'annual', 'the annual 0.60 the byKey line names gives 0.0479: generic line (finding)'],
  [3, 'p-futures-net-psr', 4, '0.848', T, null], [3, 'p-futures-net-psr', 4, '0.851', F, 'normal'],
  [3, 'p-futures-net-psr', 4, '0.850', F, 'normal', '0.038 over the normal error 0.0366 is 1.038 and gives 0.850: marked right (finding)'],
  [3, 'p-futures-net-psr', 4, '0.984', F, 'gross'], [3, 'p-futures-net-psr', 4, '0.985', F, 'gross'],
  [3, 'p-calibrated-kelly', 1, '0.176', T, null], [3, 'p-calibrated-kelly', 2, '0.129', T, null], [3, 'p-calibrated-kelly', 3, '0.0127', T, null], [3, 'p-calibrated-kelly', 3, '0.0267', F, 'raw-p'], [3, 'p-calibrated-kelly', 3, '-0.0369', F, 'even-payout'],
  [3, 'p-calibrated-kelly', 3, '-0.0371', F, 'even-payout', 'the stated stake 0.176 in ln(1 + f) gives -0.0371: generic line (finding)'],
  [3, 'p-calibrated-kelly', 4, '0.875', T, null], [3, 'p-calibrated-kelly', 4, '0.876', T, null], [3, 'p-calibrated-kelly', 4, '0.873', T, null], [3, 'p-calibrated-kelly', 4, '0.733', F, 'stake-ratio'],
];
let fail = 0, find = 0;
for (const [n, id, k, text, ok, key, why] of ROWS) {
  const p = sets[n].items.find((i) => i.id === id).parts[k - 1];
  const r = grade(p.widget, text);
  const good = r.ok === ok && (ok || r.key === key);
  if (good) continue;
  if (why) { find++; console.log(`FINDING ${n} ${id} part ${k} '${text}': ok=${r.ok} key=${r.key}; ${why}`); }
  else { fail++; console.log(`FAIL ${n} ${id} part ${k} '${text}': ok=${r.ok} key=${r.key}, expected ok=${ok} key=${key}`); }
}
console.log(`${ROWS.length} rows, ${fail} failures, ${find} findings`);
process.exit(fail ? 1 : 0);
