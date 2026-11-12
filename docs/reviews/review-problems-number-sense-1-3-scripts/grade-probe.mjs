#!/usr/bin/env node
/* Second read, number-sense problems-1 to -3: what the engine's own numeric grader (numGrade in
   app/js/engine/grade.js, the call numeric.js makes) does with each typed part.
   For every numeric part: the key grades correct; every wrong[] value is refused and lands on its own id.
   Then the reader's rows: [set, item, part, typed text, expected], where expected is
     T = accepted, F = refused with the generic line, 'id' = refused on that wrong line, N = no number read.
   A row with a note is one the reader holds to be a fault in the content (FINDING, not a failure).
   With --fix the fixes of the review are applied to in-memory copies and their rows run instead.

   node docs/reviews/review-problems-number-sense-1-3-scripts/grade-probe.mjs [--fix] [--all]   (from the repo root) */
import fs from 'node:fs';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const ALL = argv.includes('--all'), FIX = argv.includes('--fix');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const grade = (w, t) => { const r = G.numGrade(w, t); return r.ok ? true : (r.key || (r.detail && r.detail.value == null ? 'N' : false)); };

const sets = {};
for (const n of [1, 2, 3]) sets[n] = JSON.parse(fs.readFileSync(`app/content/courses/number-sense/problems-${n}.json`, 'utf8'));
const part = (n, id, k) => sets[n].items.find((i) => i.id === id).parts[k - 1];

const T = true, F = false, N = 'N';
let ROWS;
if (!FIX) {
  ROWS = [
    // set 1: fractions typed as fractions, mixed numbers, unreduced forms, decimals
    [1, 'p-garden-beds', 1, '8 beds', T], [1, 'p-garden-beds', 2, '13/20', T], [1, 'p-garden-beds', 2, '26/40', T], [1, 'p-garden-beds', 2, '0.65', T],
    [1, 'p-garden-beds', 2, '3/9', 'tops-bottoms'], [1, 'p-garden-beds', 2, '1/3', 'tops-bottoms'], [1, 'p-garden-beds', 2, '3/20', 'tops-kept'],
    [1, 'p-garden-beds', 3, '7/20', T], [1, 'p-garden-beds', 3, '2/3', 'carried'], [1, 'p-garden-beds', 3, '7', 'beds'],
    [1, 'p-garden-beds', 4, '7/40', T], [1, 'p-garden-beds', 4, '3.5/20', T], [1, 'p-garden-beds', 4, '7/10', 'doubled'], [1, 'p-garden-beds', 4, '17/20', 'added-half'], [1, 'p-garden-beds', 4, '1/3', 'carried'],
    [1, 'p-rye-loaves', 1, '10/3', T], [1, 'p-rye-loaves', 1, '3 1/3', T], [1, 'p-rye-loaves', 1, '20/6', T], [1, 'p-rye-loaves', 1, '3.333', T], [1, 'p-rye-loaves', 1, '3.33', F],
    [1, 'p-rye-loaves', 1, '5/24', 'multiplied'], [1, 'p-rye-loaves', 1, '3/10', 'wrong-flip'], [1, 'p-rye-loaves', 1, '6/20', 'wrong-flip'],
    [1, 'p-rye-loaves', 2, '3 loaves', T], [1, 'p-rye-loaves', 2, '4', 'rounded-up'], [1, 'p-rye-loaves', 2, '0', 'carried'], [1, 'p-rye-loaves', 2, '3 1/3', F],
    [1, 'p-rye-loaves', 3, '1/12', T], [1, 'p-rye-loaves', 3, '1/12 kg', T], [1, 'p-rye-loaves', 3, '2/24', T], [1, 'p-rye-loaves', 3, '7/12', 'one-loaf'], [1, 'p-rye-loaves', 3, '2/2', 'tops-bottoms'], [1, 'p-rye-loaves', 3, '1/3', 'loaf-third'],
    [1, 'p-rye-loaves', 4, '1/10', T], [1, 'p-rye-loaves', 4, '6/60', T], [1, 'p-rye-loaves', 4, '0.1', T], [1, 'p-rye-loaves', 4, '5/72', 'multiplied'], [1, 'p-rye-loaves', 4, '10', 'flipped'], [1, 'p-rye-loaves', 4, '7/10', 'carried'],
    [1, 'p-two-printers', 1, '17/24', T], [1, 'p-two-printers', 1, '4/11', 'tops-bottoms'], [1, 'p-two-printers', 1, '3/24', 'multiplied'], [1, 'p-two-printers', 1, '1/8', 'multiplied'],
    [1, 'p-two-printers', 2, '7/24', T], [1, 'p-two-printers', 2, '7/11', 'carried'], [1, 'p-two-printers', 2, '7', 'count'],
    [1, 'p-two-printers', 3, '7/9', T], [1, 'p-two-printers', 3, '56/72', T], [1, 'p-two-printers', 3, '7/9 hours', T], [1, 'p-two-printers', 3, '21/192', 'multiplied'], [1, 'p-two-printers', 3, '9/7', 'flipped'], [1, 'p-two-printers', 3, '1 2/7', 'flipped'], [1, 'p-two-printers', 3, '7/8', 'printer-b'],
    [1, 'p-two-printers', 3, '46 2/3', F, 'finding 5: the time in minutes, one step ahead, has no line'],
    [1, 'p-two-printers', 4, '320/3', T], [1, 'p-two-printers', 4, '106 2/3', T], [1, 'p-two-printers', 4, '106 2/3 minutes', T], [1, 'p-two-printers', 4, '106.667', T], [1, 'p-two-printers', 4, '106.67', F],
    [1, 'p-two-printers', 4, '46 2/3', 'rest-only'], [1, 'p-two-printers', 4, '140/3', 'rest-only'], [1, 'p-two-printers', 4, '177 7/9', 'hundred'], [1, 'p-two-printers', 4, '137 1/7', 'carried-flipped'],
    [1, 'p-two-printers', 4, '1 7/9', F, 'finding 5: the right time left in hours has no line'], [1, 'p-two-printers', 4, '16/9', F, 'finding 5: the right time left in hours has no line'],
    [1, 'p-squash-jugs', 1, '16', T], [1, 'p-squash-jugs', 1, '4', 'top-kept'], [1, 'p-squash-jugs', 1, '31', 'added'],
    [1, 'p-squash-jugs', 1, '16/36', F, 'finding 4: the renamed fraction typed whole has no line'],
    [1, 'p-squash-jugs', 3, '1/3', T], [1, 'p-squash-jugs', 3, '12/36', T], [1, 'p-squash-jugs', 3, '1/3 litre', T], [1, 'p-squash-jugs', 3, '1/3 l', N, 'finding 8: a one-letter unit is not read without the unit field'], [1, 'p-two-printers', 3, '7/9 h', N, 'finding 8: a one-letter unit is not read without the unit field'], [1, 'p-squash-jugs', 3, '43/36', 'added'], [1, 'p-squash-jugs', 3, '16/27', 'divided'],
    [1, 'p-squash-jugs', 4, '31/48', T], [1, 'p-squash-jugs', 4, '6/19', 'tops-bottoms'], [1, 'p-squash-jugs', 4, '217/144', 'carried'],
    [1, 'p-squash-jugs', 5, '31/72', T], [1, 'p-squash-jugs', 5, '62/144', T], [1, 'p-squash-jugs', 5, '93/96', 'multiplied'], [1, 'p-squash-jugs', 5, '31/32', 'multiplied'], [1, 'p-squash-jugs', 5, '31/36', 'shares-added'],
    // set 2: signs, units, more places
    [2, 'p-moor-weather', 1, '1.3', T], [2, 'p-moor-weather', 1, '1.3 °C', N, 'finding 8: the unit the question names is not read, so Check stays unavailable'], [2, 'p-moor-weather', 1, '1.3°C', N, 'finding 8: the unit the question names is not read'], [2, 'p-moor-weather', 1, '1.3 degrees', T], [2, 'p-moor-weather', 1, '+1.3', T], [2, 'p-moor-weather', 1, '1.30', T],
    [2, 'p-moor-weather', 1, '-8.5', 'subtracted'], [2, 'p-moor-weather', 1, '−8.5', 'subtracted'], [2, 'p-moor-weather', 1, '8.5', 'start-sign'],
    [2, 'p-moor-weather', 2, '-6.3', T], [2, 'p-moor-weather', 2, '−6.3', T], [2, 'p-moor-weather', 2, '-6.3 degrees', T], [2, 'p-moor-weather', 2, '6.3', 'sign'], [2, 'p-moor-weather', 2, '-3.7', 'added'], [2, 'p-moor-weather', 2, '3.5', 'carried'],
    [2, 'p-moor-weather', 3, '-0.7', T], [2, 'p-moor-weather', 3, '-.7', T], [2, 'p-moor-weather', 3, '-7/10', T], [2, 'p-moor-weather', 3, '0.7', 'sign'], [2, 'p-moor-weather', 3, '-56.7', 'times'],
    [2, 'p-moor-weather', 4, '-7.8', T], [2, 'p-moor-weather', 4, '-7.8 °C', N, 'finding 8: the unit the question names is not read'], [2, 'p-moor-weather', 4, '7.8', 'sign'], [2, 'p-moor-weather', 4, '-2.2', 'minus-minus'], [2, 'p-moor-weather', 4, '-2.8', 'change-only'],
    [2, 'p-golf-card', 1, '-1', T], [2, 'p-golf-card', 1, '−1', T], [2, 'p-golf-card', 1, '1', 'sign'], [2, 'p-golf-card', 1, '0', 'eagle-one'], [2, 'p-golf-card', 1, '11', 'no-signs'],
    [2, 'p-golf-card', 2, '-2', T], [2, 'p-golf-card', 2, '2', 'sign'], [2, 'p-golf-card', 2, '-3', 'plus-as-minus'], [2, 'p-golf-card', 2, '-8', 'total'],
    [2, 'p-golf-card', 3, '0.278', T], [2, 'p-golf-card', 3, '.278', T], [2, 'p-golf-card', 3, '0.277', 'truncated'], [2, 'p-golf-card', 3, '3.6', 'flipped'], [2, 'p-golf-card', 3, '0.28', F],
    [2, 'p-golf-card', 3, '5/18', T, 'finding 10: the fraction of the question typed back is marked correct on a "write as a decimal" part'],
    [2, 'p-golf-card', 3, '0.2778', T, 'finding 10: four places pass where three are asked'],
    [2, 'p-taxi-split', 1, '2.8333', T], [2, 'p-taxi-split', 1, '£2.8333', T], [2, 'p-taxi-split', 1, '2.83333', T], [2, 'p-taxi-split', 1, '2.833', F], [2, 'p-taxi-split', 1, '2.83', F],
    [2, 'p-taxi-split', 1, '0.3529', 'flipped'], [2, 'p-taxi-split', 1, '2.5', 'remainder'], [2, 'p-taxi-split', 1, '17/6', T],
    [2, 'p-taxi-split', 2, '2.83', T], [2, 'p-taxi-split', 2, '£2.83', T], [2, 'p-taxi-split', 2, '2.84', 'rounded-up'], [2, 'p-taxi-split', 2, '2.8', 'one-dp'],
    [2, 'p-taxi-split', 2, '2.8333', T, 'finding 10: the value the question gives, typed back unrounded, is marked correct on the rounding part'],
    [2, 'p-taxi-split', 2, '283', F, 'finding 11: the share in pence has no line'],
    [2, 'p-taxi-split', 3, '-2', T], [2, 'p-taxi-split', 3, '-2p', N, 'finding 8: the unit the question names is not read'], [2, 'p-taxi-split', 3, '-2 pence', T], [2, 'p-taxi-split', 3, '2', 'sign'], [2, 'p-taxi-split', 3, '-0.02', 'pounds'], [2, 'p-taxi-split', 3, '4', 'carried-up'],
    [2, 'p-taxi-split', 4, '2.85', T], [2, 'p-taxi-split', 4, '£2.85', T], [2, 'p-taxi-split', 4, '2.83', 'same'], [2, 'p-taxi-split', 4, '2.81', 'wrong-way'], [2, 'p-taxi-split', 4, '0.02', 'shortfall'],
    [2, 'p-taxi-split', 4, '285', F, 'finding 11: the payment in pence has no line'],
    // set 3: thousands commas, standard form, money
    [3, 'p-cube-tub', 1, '11', T], [3, 'p-cube-tub', 1, '12', 'rounded-up'], [3, 'p-cube-tub', 1, '38.7', 'square-root'], [3, 'p-cube-tub', 1, '39', 'square-root'], [3, 'p-cube-tub', 1, '500', 'thirds'], [3, 'p-cube-tub', 1, '11.4', F],
    [3, 'p-cube-tub', 2, '169', T], [3, 'p-cube-tub', 2, '1379', 'squared'], [3, 'p-cube-tub', 2, '1,379', 'squared'], [3, 'p-cube-tub', 2, '-228', 'carried-up'], [3, 'p-cube-tub', 2, '1467', 'times-three'],
    [3, 'p-cube-tub', 3, '13', T], [3, 'p-cube-tub', 3, '84.5', 'halved'], [3, 'p-cube-tub', 3, '85', 'halved'], [3, 'p-cube-tub', 3, '42.25', 'quartered'], [3, 'p-cube-tub', 3, '42', 'quartered'],
    [3, 'p-stationery-bill', 1, '220', T], [3, 'p-stationery-bill', 1, '£220', T], [3, 'p-stationery-bill', 1, '1000', 'bracket-first'], [3, 'p-stationery-bill', 1, '1,000', 'bracket-first'], [3, 'p-stationery-bill', 1, '200', 'no-delivery'],
    [3, 'p-stationery-bill', 2, '203.80', T], [3, 'p-stationery-bill', 2, '203.8', T], [3, 'p-stationery-bill', 2, '£203.80', T], [3, 'p-stationery-bill', 2, '925.30', 'bracket'], [3, 'p-stationery-bill', 2, '184.30', 'boxes-only'],
    [3, 'p-stationery-bill', 3, '190.80', T], [3, 'p-stationery-bill', 3, '190.8', T], [3, 'p-stationery-bill', 3, '6.50', 'delivery-share'],
    [3, 'p-stationery-bill', 3, '67.93', 'intended', 'finding 12: a calculator that works left to right shows 67.93; its line says the calculator divides only the 19.50'],
    
    [3, 'p-stationery-bill', 4, '67.93', T], [3, 'p-stationery-bill', 4, '£67.93', T], [3, 'p-stationery-bill', 4, '190.80', 'calculator'], [3, 'p-stationery-bill', 4, '308.43', 'carried-bracket'], [3, 'p-stationery-bill', 4, '73.33', 'estimate'], [3, 'p-stationery-bill', 4, '67.9333', T],
    [3, 'p-comet-probe', 1, '30000', T], [3, 'p-comet-probe', 1, '30,000', T], [3, 'p-comet-probe', 1, '30 000', T], [3, 'p-comet-probe', 1, '30,000 hours', T],
    [3, 'p-comet-probe', 1, '300000', 'kept-point'], [3, 'p-comet-probe', 1, '300,000', 'kept-point'], [3, 'p-comet-probe', 1, '3000000000000', 'added-indices'], [3, 'p-comet-probe', 1, '3000', 'short'],
    [3, 'p-comet-probe', 2, '9000', T], [3, 'p-comet-probe', 2, '9,000', T], [3, 'p-comet-probe', 2, '8000', 'truncated'], [3, 'p-comet-probe', 2, '8800', 'two-sf'], [3, 'p-comet-probe', 2, '8,800', 'two-sf'],
    [3, 'p-comet-probe', 3, '3', T], [3, 'p-comet-probe', 3, '3 years', T], [3, 'p-comet-probe', 3, '0.3', 'inverted'], [3, 'p-comet-probe', 3, '4', 'carried'],
    [3, 'p-comet-probe', 3, '3.3', F, 'finding 14: the quotient left unrounded gets the generic line, which names the step the learner took'],
    [3, 'p-comet-probe', 3, '3.33', F, 'finding 14: the quotient left unrounded gets the generic line, which names the step the learner took'],
    [3, 'p-comet-probe', 4, '3.4', T], [3, 'p-comet-probe', 4, '3.4 years', T], [3, 'p-comet-probe', 4, '3.42', T], [3, 'p-comet-probe', 4, '3.3', 'nine-thousand'], [3, 'p-comet-probe', 4, '3.33', 'nine-thousand'], [3, 'p-comet-probe', 4, '34.2', 'carried'], [3, 'p-comet-probe', 4, '1250', 'days'], [3, 'p-comet-probe', 4, '1,250', 'days'], [3, 'p-comet-probe', 4, '3', F],
  ];
} else {
  // the fixes of the review, applied to in-memory copies (values from proposed.py)
  const setW = (n, id, k, f) => f(part(n, id, k).widget);
  setW(2, 'p-golf-card', 3, (w) => { w.tol = { abs: 0.0001 }; w.wrong.push({ id: 'unrounded', value: 0.277778, tol: { abs: 0.0001 } }); });
  setW(2, 'p-taxi-split', 2, (w) => { w.tol = { abs: 0.0005 }; w.wrong.push({ id: 'unrounded', value: 2.8333, tol: { abs: 0.0005 } }, { id: 'pence', value: 283, tol: { abs: 0 } }); });
  setW(2, 'p-taxi-split', 4, (w) => { w.wrong.push({ id: 'pence', value: 285, tol: { abs: 0 } }); });
  setW(3, 'p-comet-probe', 3, (w) => { w.wrong.push({ id: 'unrounded', value: 3.33, tol: { abs: 0.04 } }); });
  setW(1, 'p-squash-jugs', 1, (w) => { w.wrong.push({ id: 'whole-fraction', value: 0.444444, tol: { abs: 0.0005 } }); });
  setW(1, 'p-two-printers', 3, (w) => { w.wrong.push({ id: 'minutes', value: 46.666667, tol: { abs: 0.0005 } }); });
  setW(1, 'p-two-printers', 4, (w) => { w.wrong.push({ id: 'hours', value: 1.777778, tol: { abs: 0.0005 } }); });
  const U = [[2, 'p-moor-weather', 1, '°C'], [2, 'p-moor-weather', 2, 'degrees'], [2, 'p-moor-weather', 3, 'degrees'], [2, 'p-moor-weather', 4, '°C'], [2, 'p-taxi-split', 1, '£'], [2, 'p-taxi-split', 2, '£'], [2, 'p-taxi-split', 3, 'p'], [2, 'p-taxi-split', 4, '£'],
    [1, 'p-garden-beds', 1, 'beds'], [1, 'p-rye-loaves', 2, 'loaves'], [1, 'p-rye-loaves', 3, 'kg'], [1, 'p-two-printers', 3, 'hours'], [1, 'p-two-printers', 4, 'minutes'], [1, 'p-squash-jugs', 3, 'litres'], [1, 'p-squash-jugs', 4, 'litres'],
    [3, 'p-cube-tub', 1, 'cubes'], [3, 'p-cube-tub', 2, 'cubes'], [3, 'p-cube-tub', 3, 'cubes'], [3, 'p-stationery-bill', 1, '£'], [3, 'p-stationery-bill', 2, '£'], [3, 'p-stationery-bill', 3, '£'], [3, 'p-stationery-bill', 4, '£'],
    [3, 'p-comet-probe', 1, 'hours'], [3, 'p-comet-probe', 2, 'hours'], [3, 'p-comet-probe', 3, 'years'], [3, 'p-comet-probe', 4, 'years']];
  for (const [n, id, k, u] of U) part(n, id, k).widget.unit = u;
  setW(1, 'p-garden-beds', 1, (w) => { w.answer = 5; w.wrong = [{ id: 'flipped', value: 80, tol: { abs: 0 } }, { id: 'three-quarters', value: 15, tol: { abs: 0 } }]; });
  // finding 15, the cube tub with 2,169 cubes
  setW(3, 'p-cube-tub', 1, (w) => { w.answer = 12; w.wrong = [{ id: 'rounded-up', value: 13, tol: { abs: 0 } }, { id: 'square-root', value: 46, tol: { abs: 1 } }, { id: 'thirds', value: 723, tol: { abs: 0 } }]; });
  setW(3, 'p-cube-tub', 2, (w) => { w.answer = 441; w.wrong = [{ id: 'squared', value: 2025, tol: { abs: 0 } }, { id: 'carried-up', value: -28, tol: { abs: 0 } }, { id: 'times-three', value: 2133, tol: { abs: 0 } }]; });
  setW(3, 'p-cube-tub', 3, (w) => { w.answer = 21; w.wrong = [{ id: 'halved', value: 220.5, tol: { abs: 0.5 } }, { id: 'quartered', value: 110.25, tol: { abs: 0.25 } }]; });
  // finding 2, the rye loaves with a fifth of a kilogram a loaf
  setW(1, 'p-rye-loaves', 1, (w) => { w.answer = 4.166667; w.wrong = [{ id: 'multiplied', value: 0.166667, tol: { abs: 0.0005 } }, { id: 'wrong-flip', value: 0.24, tol: { abs: 0.0005 } }]; });
  setW(1, 'p-rye-loaves', 2, (w) => { w.answer = 4; w.wrong = [{ id: 'rounded-up', value: 5, tol: { abs: 0 } }, { id: 'carried', value: 0, tol: { abs: 0 } }]; });
  setW(1, 'p-rye-loaves', 3, (w) => { w.answer = 0.033333; w.wrong = [{ id: 'one-loaf', value: 0.633333, tol: { abs: 0.0005 } }, { id: 'tops-bottoms', value: 1, tol: { abs: 0.0005 } }, { id: 'loaf-sixth', value: 0.166667, tol: { abs: 0.0005 } }]; });
  setW(1, 'p-rye-loaves', 4, (w) => { w.answer = 0.04; w.wrong = [{ id: 'multiplied', value: 0.027778, tol: { abs: 0.0005 } }, { id: 'flipped', value: 25, tol: { abs: 0.0005 } }, { id: 'carried', value: 0.76, tol: { abs: 0.0005 } }]; });
  ROWS = [
    [2, 'p-moor-weather', 1, '1.3', T], [2, 'p-moor-weather', 1, '1.3 °C', T], [2, 'p-moor-weather', 1, '1.3°C', T], [2, 'p-moor-weather', 1, '-8.5 °C', 'subtracted'], [2, 'p-moor-weather', 4, '-7.8 °C', T], [2, 'p-moor-weather', 4, '\u22127.8°C', T], [2, 'p-moor-weather', 2, '-6.3 degrees', T], [2, 'p-moor-weather', 2, '-6.3', T],
    [2, 'p-taxi-split', 3, '-2p', T], [2, 'p-taxi-split', 3, '-2 p', T], [2, 'p-taxi-split', 3, '-2 pence', T], [2, 'p-taxi-split', 3, '-2', T], [2, 'p-taxi-split', 3, '2p', 'sign'], [2, 'p-taxi-split', 1, '£2.8333', T], [2, 'p-taxi-split', 1, '2.8333', T],
    [1, 'p-squash-jugs', 3, '1/3 l', N], [1, 'p-squash-jugs', 3, '1/3 litre', T], [1, 'p-squash-jugs', 3, '1/3 litres', T], [1, 'p-squash-jugs', 3, '1/3', T], [1, 'p-two-printers', 3, '7/9 h', T], [1, 'p-two-printers', 4, '106 2/3 min', T], [1, 'p-rye-loaves', 3, '1/30 kg', T], [3, 'p-comet-probe', 1, '30,000 h', T], [3, 'p-comet-probe', 4, '3.4 years', T], [3, 'p-stationery-bill', 2, '£203.80', T], [3, 'p-stationery-bill', 2, '203.80', T],
    [2, 'p-golf-card', 3, '0.278', T], [2, 'p-golf-card', 3, '.278', T], [2, 'p-golf-card', 3, '5/18', 'unrounded'], [2, 'p-golf-card', 3, '0.2778', 'unrounded'], [2, 'p-golf-card', 3, '0.27778', 'unrounded'], [2, 'p-golf-card', 3, '0.277', 'truncated'], [2, 'p-golf-card', 3, '3.6', 'flipped'], [2, 'p-golf-card', 3, '0.28', F],
    [2, 'p-taxi-split', 2, '2.83', T], [2, 'p-taxi-split', 2, '£2.83', T], [2, 'p-taxi-split', 2, '2.8333', 'unrounded'], [2, 'p-taxi-split', 2, '2.833', 'unrounded'], [2, 'p-taxi-split', 2, '17/6', 'unrounded'], [2, 'p-taxi-split', 2, '2.84', 'rounded-up'], [2, 'p-taxi-split', 2, '2.8', 'one-dp'], [2, 'p-taxi-split', 2, '283', 'pence'], [2, 'p-taxi-split', 2, '283 pence', 'pence'],
    [2, 'p-taxi-split', 4, '2.85', T], [2, 'p-taxi-split', 4, '285', 'pence'], [2, 'p-taxi-split', 4, '2.83', 'same'],
    [3, 'p-comet-probe', 3, '3', T], [3, 'p-comet-probe', 3, '3.3', 'unrounded'], [3, 'p-comet-probe', 3, '3.33', 'unrounded'], [3, 'p-comet-probe', 3, '3.333', 'unrounded'], [3, 'p-comet-probe', 3, '10/3', 'unrounded'], [3, 'p-comet-probe', 3, '0.3', 'inverted'], [3, 'p-comet-probe', 3, '4', 'carried'], [3, 'p-comet-probe', 3, '3.4', F],
    [1, 'p-squash-jugs', 1, '16', T], [1, 'p-squash-jugs', 1, '16/36', 'whole-fraction'], [1, 'p-squash-jugs', 1, '4/9', 'whole-fraction'], [1, 'p-squash-jugs', 1, '4', 'top-kept'], [1, 'p-squash-jugs', 1, '31', 'added'],
    [1, 'p-two-printers', 3, '7/9', T], [1, 'p-two-printers', 3, '46 2/3', 'minutes'], [1, 'p-two-printers', 3, '140/3', 'minutes'], [1, 'p-two-printers', 3, '9/7', 'flipped'],
    [1, 'p-two-printers', 4, '106 2/3', T], [1, 'p-two-printers', 4, '1 7/9', 'hours'], [1, 'p-two-printers', 4, '16/9', 'hours'], [1, 'p-two-printers', 4, '46 2/3', 'rest-only'],
    [3, 'p-stationery-bill', 3, '190.80', T], [3, 'p-stationery-bill', 3, '67.93', 'intended'], [3, 'p-stationery-bill', 3, '67.9333', 'intended'], [3, 'p-stationery-bill', 3, '6.50', 'delivery-share'],
    [1, 'p-garden-beds', 1, '5', T], [1, 'p-garden-beds', 1, '5 beds', T], [1, 'p-garden-beds', 1, '80', 'flipped'], [1, 'p-garden-beds', 1, '15', 'three-quarters'], [1, 'p-garden-beds', 1, '8', F],
    [3, 'p-cube-tub', 1, '12', T], [3, 'p-cube-tub', 1, '13', 'rounded-up'], [3, 'p-cube-tub', 1, '46.6', 'square-root'], [3, 'p-cube-tub', 1, '723', 'thirds'], [3, 'p-cube-tub', 1, '11', F],
    [3, 'p-cube-tub', 2, '441', T], [3, 'p-cube-tub', 2, '2,025', 'squared'], [3, 'p-cube-tub', 2, '-28', 'carried-up'], [3, 'p-cube-tub', 2, '2,133', 'times-three'],
    [3, 'p-cube-tub', 3, '21', T], [3, 'p-cube-tub', 3, '220.5', 'halved'], [3, 'p-cube-tub', 3, '110', 'quartered'],
    [1, 'p-rye-loaves', 1, '25/6', T], [1, 'p-rye-loaves', 1, '4 1/6', T], [1, 'p-rye-loaves', 1, '1/6', 'multiplied'], [1, 'p-rye-loaves', 1, '6/25', 'wrong-flip'],
    [1, 'p-rye-loaves', 2, '4', T], [1, 'p-rye-loaves', 2, '5', 'rounded-up'], [1, 'p-rye-loaves', 2, '0', 'carried'],
    [1, 'p-rye-loaves', 3, '1/30', T], [1, 'p-rye-loaves', 3, '19/30', 'one-loaf'], [1, 'p-rye-loaves', 3, '1/1', 'tops-bottoms'], [1, 'p-rye-loaves', 3, '1/6', 'loaf-sixth'],
    [1, 'p-rye-loaves', 4, '1/25', T], [1, 'p-rye-loaves', 4, '0.04', T], [1, 'p-rye-loaves', 4, '1/36', 'multiplied'], [1, 'p-rye-loaves', 4, '25', 'flipped'], [1, 'p-rye-loaves', 4, '19/25', 'carried'],
  ];
}

let checks = 0, fails = 0, notes = 0;
const say = (okFlag, msg) => { checks++; if (!okFlag) { fails++; console.log('FAIL ' + msg); } else if (ALL) console.log('ok   ' + msg); };
for (const n of [1, 2, 3]) for (const it of sets[n].items) it.parts.forEach((p, i) => {
  const w = p.widget; if (w.kind !== 'numeric') return;
  const at = `problems-${n} ${it.id} part ${i + 1}`;
  say(grade(w, String(w.answer)) === true, `${at}: key ${w.answer} accepted`);
  for (const x of w.wrong) say(grade(w, String(x.value)) === x.id, `${at}: wrong ${x.id} (${x.value}) lands on its own line, got ${grade(w, String(x.value))}`);
});
for (const [n, id, k, text, want, note] of ROWS) {
  const got = grade(part(n, id, k).widget, text);
  say(got === want, `problems-${n} ${id} part ${k}: "${text}" expected ${want}, got ${got}`);
  if (note) { notes++; console.log(`FINDING problems-${n} ${id} part ${k}: "${text}" -> ${got === true ? 'accepted' : got === false ? 'generic line' : got}: ${note}`); }
}
console.log(`grade-probe${FIX ? ' --fix' : ''}: ${checks} checks, ${ROWS.length} reader rows, ${fails} failures, ${notes} rows held to be faults`);
process.exit(fails ? 1 : 0);
