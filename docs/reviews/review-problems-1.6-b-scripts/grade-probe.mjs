#!/usr/bin/env node
/* Second read, testing problems-1 to -3: what the engine's own numeric grader (app/js/engine/grade.js numGrade) does with
   each typed part and with strings a learner would really type.
     - every answer must grade correct; every wrong[] must grade wrong and land on its own key, with a byKey line (FAIL if not)
     - every TYPED row [set, item, part (1-based), text, expected (true accepted, false refused, the wrong id it must land on, or 'NONE' for refused on no wrong line),
       finding?] must grade as expected; a row with a 6th field is one the reader holds to be a fault (printed, not a failure)
   node docs/reviews/review-problems-1.6-b-scripts/grade-probe.mjs [--all]     (from the repo root) */
import fs from 'node:fs';
import vm from 'node:vm';

const ALL = process.argv.includes('--all');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const grade = (w, text) => { const r = G.numGrade(w, text); return { ok: !!r.ok, key: r.key || (r.detail.value == null ? 'NOPARSE' : null) }; };

const T = true, F = false;
const UNIT = 'the question names the unit but the part has no `unit`, so the one-letter unit is not read';
const SHORT = 'the slip rounded to 2 places misses its own line (band 0.001 beside an answer asked as "a decimal")';
const TOLD = 'the slip worked without the rounded value the question hands over misses its line';
const TYPED = [
  // problems-1
  [1, 'p-cereal-boxes', 2, '3', T], [1, 'p-cereal-boxes', 2, '3 g', T], [1, 'p-cereal-boxes', 2, '3g', T], [1, 'p-cereal-boxes', 2, '3.0', T], [1, 'p-cereal-boxes', 2, '18/6', T], [1, 'p-cereal-boxes', 2, '3 grams', T],
  [1, 'p-cereal-boxes', 2, '0.5', 'over-n'], [1, 'p-cereal-boxes', 2, '9', 'variance'], [1, 'p-cereal-boxes', 2, '18', F],
  [1, 'p-cereal-boxes', 3, '-2.3', T], [1, 'p-cereal-boxes', 3, '−2.3', T], [1, 'p-cereal-boxes', 3, '-2.30', T], [1, 'p-cereal-boxes', 3, 'z=-2.3', T], [1, 'p-cereal-boxes', 3, 'z = -2.3', T], [1, 'p-cereal-boxes', 3, '-23/10', T],
  [1, 'p-cereal-boxes', 3, '2.3', 'sign'], [1, 'p-cereal-boxes', 3, '-0.38', 'over-sd'], [1, 'p-cereal-boxes', 3, '-0.383', 'over-sd'], [1, 'p-cereal-boxes', 3, '-13.8', 'carried'], [1, 'p-cereal-boxes', 3, '-2.29', F], [1, 'p-cereal-boxes', 3, '-0.77', F],
  [1, 'p-cereal-boxes', 4, '0.0107', T], [1, 'p-cereal-boxes', 4, '.0107', T], [1, 'p-cereal-boxes', 4, '1.07%', T], [1, 'p-cereal-boxes', 4, '0.01072', T], [1, 'p-cereal-boxes', 4, 'p=0.0107', T], [1, 'p-cereal-boxes', 4, '0.011', F], [1, 'p-cereal-boxes', 4, '0.01', F],
  [1, 'p-cereal-boxes', 4, '0.0214', 'two-sided'], [1, 'p-cereal-boxes', 4, '0.9893', 'upper-tail'],
  [1, 'p-phone-battery', 1, '18', T], [1, 'p-phone-battery', 1, '18 hours', T], [1, 'p-phone-battery', 1, '144/8', T], [1, 'p-phone-battery', 1, '18.0', T], [1, 'p-phone-battery', 1, '18 h', T, UNIT], [1, 'p-phone-battery', 1, '18h', T, UNIT],
  [1, 'p-phone-battery', 1, '20.57', 'n-minus-one'], [1, 'p-phone-battery', 1, '20.6', F],
  [1, 'p-phone-battery', 2, '2', T], [1, 'p-phone-battery', 2, '2.0', T], [1, 'p-phone-battery', 2, '2 hours', T], [1, 'p-phone-battery', 2, 's=2', T], [1, 'p-phone-battery', 2, '1.87', 'divide-by-n'], [1, 'p-phone-battery', 2, '4', 'variance'], [1, 'p-phone-battery', 2, '3.4', 'carried'],
  [1, 'p-phone-battery', 3, '-2.121', T], [1, 'p-phone-battery', 3, '-2.1213', T], [1, 'p-phone-battery', 3, '−2.121', T], [1, 'p-phone-battery', 3, 't=-2.121', T], [1, 'p-phone-battery', 3, '-2.122', T], [1, 'p-phone-battery', 3, '-2.12', F], [1, 'p-phone-battery', 3, '-2.1', F],
  [1, 'p-phone-battery', 3, '2.121', 'sign'], [1, 'p-phone-battery', 3, '-1.984', 'root-seven'], [1, 'p-phone-battery', 3, '-0.75', 'over-s'], [1, 'p-phone-battery', 3, '-2.268', 'carried'],
  [1, 'p-phone-battery', 5, '19.34', T], [1, 'p-phone-battery', 5, '19.340', T], [1, 'p-phone-battery', 5, '19.33995', T], [1, 'p-phone-battery', 5, '19.34 hours', T], [1, 'p-phone-battery', 5, '19.3', F], [1, 'p-phone-battery', 5, '19.35', F], [1, 'p-phone-battery', 5, '19.33', F],
  [1, 'p-phone-battery', 5, '19.16', 'normal'], [1, 'p-phone-battery', 5, '19.67', 'two-sided'], [1, 'p-phone-battery', 5, '16.66', 'wrong-side'], [1, 'p-phone-battery', 5, '21.79', 'sd-not-se'],
  [1, 'p-wine-taster', 1, '0.0032', T], [1, 'p-wine-taster', 1, '13/4096', T], [1, 'p-wine-taster', 1, '0.00317', T], [1, 'p-wine-taster', 1, '0.003174', T], [1, 'p-wine-taster', 1, '0.32%', T], [1, 'p-wine-taster', 1, '0.003', F],
  [1, 'p-wine-taster', 1, '12/4096', 'eleven-only'], [1, 'p-wine-taster', 1, '0.0029', 'eleven-only'], [1, 'p-wine-taster', 1, '1/4096', 'twelve-only'], [1, 'p-wine-taster', 1, '0.0002', 'twelve-only'],
  [1, 'p-wine-taster', 2, '0.0193', T], [1, 'p-wine-taster', 2, '79/4096', T], [1, 'p-wine-taster', 2, '0.01929', T], [1, 'p-wine-taster', 2, '1.93%', T], [1, 'p-wine-taster', 2, '0.02', F],
  [1, 'p-wine-taster', 2, '0.019', 'NONE', 'the right answer cut to 3 places is exactly the `carried` value 0.0190, so it is told "You added 66 to 12"'],
  [1, 'p-wine-taster', 2, '78/4096', 'carried'], [1, 'p-wine-taster', 2, '66/4096', 'exactly-ten'], [1, 'p-wine-taster', 2, '0.0161', 'exactly-ten'],
  [1, 'p-wine-taster', 3, '0.0730', T], [1, 'p-wine-taster', 3, '0.073', T], [1, 'p-wine-taster', 3, '299/4096', T], [1, 'p-wine-taster', 3, '0.072998', T], [1, 'p-wine-taster', 3, '7.3%', T], [1, 'p-wine-taster', 3, '0.07', F],
  [1, 'p-wine-taster', 3, '0.0537', 'exactly-nine'], [1, 'p-wine-taster', 3, '220/4096', 'exactly-nine'], [1, 'p-wine-taster', 3, '0.0698', 'carried'], [1, 'p-wine-taster', 3, '286/4096', 'carried'], [1, 'p-wine-taster', 3, '0.0727', F],
  [1, 'p-wine-taster', 4, '10', T], [1, 'p-wine-taster', 4, '10 right', T], [1, 'p-wine-taster', 4, '10 trials', T], [1, 'p-wine-taster', 4, '9', 'nine'], [1, 'p-wine-taster', 4, '11', 'eleven'], [1, 'p-wine-taster', 4, '12', F],
  [1, 'p-pizza-delivery', 1, '1.75', T], [1, 'p-pizza-delivery', 1, '7/4', T], [1, 'p-pizza-delivery', 1, '1.750', T], [1, 'p-pizza-delivery', 1, 'z=1.75', T], [1, 'p-pizza-delivery', 1, '1.8', F],
  [1, 'p-pizza-delivery', 1, '0.44', 'over-sd'], [1, 'p-pizza-delivery', 1, '0.4375', 'over-sd'], [1, 'p-pizza-delivery', 1, '7', 'over-n'], [1, 'p-pizza-delivery', 1, '16.75', 'no-null'],
  [1, 'p-pizza-delivery', 2, '0.0401', T], [1, 'p-pizza-delivery', 2, '4.01%', T], [1, 'p-pizza-delivery', 2, '0.04006', T], [1, 'p-pizza-delivery', 2, '0.04', F], [1, 'p-pizza-delivery', 2, '0.040', F],
  [1, 'p-pizza-delivery', 2, '0.0802', 'two-sided'], [1, 'p-pizza-delivery', 2, '0.0801', 'two-sided', TOLD], [1, 'p-pizza-delivery', 2, '0.9599', 'lower-tail'],
  [1, 'p-pizza-delivery', 3, '1.458', T], [1, 'p-pizza-delivery', 3, '1.4583', T], [1, 'p-pizza-delivery', 3, '35/24', T], [1, 'p-pizza-delivery', 3, 't=1.458', T], [1, 'p-pizza-delivery', 3, '1.46', F], [1, 'p-pizza-delivery', 3, '1.459', F],
  [1, 'p-pizza-delivery', 3, '2.1', 'flipped'], [1, 'p-pizza-delivery', 3, '0.365', 'over-s'], [1, 'p-pizza-delivery', 3, '0.3646', 'over-s'],
  // problems-2
  [2, 'p-fertiliser-trials', 1, '2.25', T], [2, 'p-fertiliser-trials', 1, '9/4', T], [2, 'p-fertiliser-trials', 1, '2.250', T], [2, 'p-fertiliser-trials', 1, '2.3', F], [2, 'p-fertiliser-trials', 1, '0.375', 'over-sd'], [2, 'p-fertiliser-trials', 1, '0.38', 'over-sd'], [2, 'p-fertiliser-trials', 1, '13.5', 'over-n'],
  [2, 'p-fertiliser-trials', 2, '0.7274', T], [2, 'p-fertiliser-trials', 2, '72.74%', T], [2, 'p-fertiliser-trials', 2, '0.72741', T], [2, 'p-fertiliser-trials', 2, '0.727', F], [2, 'p-fertiliser-trials', 2, '0.73', F], [2, 'p-fertiliser-trials', 2, '0.2726', 'beta'], [2, 'p-fertiliser-trials', 2, '0.05', 'alpha'],
  [2, 'p-fertiliser-trials', 3, '0.9257', T], [2, 'p-fertiliser-trials', 3, '0.92569', T], [2, 'p-fertiliser-trials', 3, '92.57%', T], [2, 'p-fertiliser-trials', 3, '0.926', F], [2, 'p-fertiliser-trials', 3, '0.5291', 'both'], [2, 'p-fertiliser-trials', 3, '1.4548', 'added'], [2, 'p-fertiliser-trials', 3, '0.4709', 'carried'],
  [2, 'p-fertiliser-trials', 4, '0.9379', T], [2, 'p-fertiliser-trials', 4, '93.79%', T], [2, 'p-fertiliser-trials', 4, '0.93785', T], [2, 'p-fertiliser-trials', 4, '0.938', F], [2, 'p-fertiliser-trials', 4, '0.0621', 'beta'], [2, 'p-fertiliser-trials', 4, '0.7274', 'unchanged'],
  [2, 'p-tyre-brands', 1, '0.1587', T], [2, 'p-tyre-brands', 1, '0.15875', T], [2, 'p-tyre-brands', 1, '0.1588', T], [2, 'p-tyre-brands', 1, '0.1587 mm', T], [2, 'p-tyre-brands', 1, '0.159', F], [2, 'p-tyre-brands', 1, '0.16', F],
  [2, 'p-tyre-brands', 1, '0.2221', 'sum-se'], [2, 'p-tyre-brands', 1, '0.2222', 'sum-se'], [2, 'p-tyre-brands', 1, '0.0252', 'variance'], [2, 'p-tyre-brands', 1, '0.153', 'same-n'], [2, 'p-tyre-brands', 1, '0.1530', 'same-n'],
  [2, 'p-tyre-brands', 2, '2.520', T], [2, 'p-tyre-brands', 2, '2.52', T], [2, 'p-tyre-brands', 2, '2.5198', T], [2, 'p-tyre-brands', 2, '2.5205', T], [2, 'p-tyre-brands', 2, 't=2.520', T], [2, 'p-tyre-brands', 2, '2.5', F], [2, 'p-tyre-brands', 2, '2.51', F], [2, 'p-tyre-brands', 2, '-2.520', F],
  [2, 'p-tyre-brands', 2, '1.801', 'carried'], [2, 'p-tyre-brands', 2, '15.873', 'over-variance'], [2, 'p-tyre-brands', 2, '2.614', F],
  [2, 'p-tyre-brands', 3, '0.0118', T], [2, 'p-tyre-brands', 3, '1.18%', T], [2, 'p-tyre-brands', 3, '0.0117', T], [2, 'p-tyre-brands', 3, '0.012', F], [2, 'p-tyre-brands', 3, '0.0059', 'one-sided'], [2, 'p-tyre-brands', 3, '0.9882', 'inside'],
  [2, 'p-running-shoes', 1, '-4', T], [2, 'p-running-shoes', 1, '−4', T], [2, 'p-running-shoes', 1, '-4 s', T], [2, 'p-running-shoes', 1, '-4s', T], [2, 'p-running-shoes', 1, '-4 seconds', T], [2, 'p-running-shoes', 1, '-36/9', T], [2, 'p-running-shoes', 1, '4', 'sign'], [2, 'p-running-shoes', 1, '-4.5', 'n-minus-one'],
  [2, 'p-running-shoes', 2, '3', T], [2, 'p-running-shoes', 2, '3 s', T], [2, 'p-running-shoes', 2, '3.0', T], [2, 'p-running-shoes', 2, '9', 'variance'], [2, 'p-running-shoes', 2, '2.828', 'divide-by-n'], [2, 'p-running-shoes', 2, '3.046', 'carried'],
  [2, 'p-running-shoes', 2, '2.83', 'divide-by-n', SHORT], [2, 'p-running-shoes', 2, '3.05', 'carried', SHORT],
  [2, 'p-running-shoes', 3, '-4', T], [2, 'p-running-shoes', 3, '-4.0', T], [2, 'p-running-shoes', 3, '−4', T], [2, 'p-running-shoes', 3, 't=-4', T], [2, 'p-running-shoes', 3, '4', 'sign'], [2, 'p-running-shoes', 3, '-1.333', 'over-sd'], [2, 'p-running-shoes', 3, '-3.771', 'root-eight'], [2, 'p-running-shoes', 3, '-4.243', 'carried'],
  [2, 'p-running-shoes', 3, '-1.33', 'over-sd', SHORT], [2, 'p-running-shoes', 3, '-4.24', 'carried', SHORT], [2, 'p-running-shoes', 3, '-3.77', 'root-eight'], [2, 'p-running-shoes', 3, '-4/3', 'over-sd'], [2, 'p-running-shoes', 3, '-4.5', F],
  [2, 'p-running-shoes', 5, '25', T], [2, 'p-running-shoes', 5, '25 runners', T], [2, 'p-running-shoes', 5, 'n=25', T], [2, 'p-running-shoes', 5, '24.72', 'not-rounded'], [2, 'p-running-shoes', 5, '24.7', 'not-rounded'], [2, 'p-running-shoes', 5, '24', 'rounded-down'],
  [2, 'p-running-shoes', 5, '13', 'no-square'], [2, 'p-running-shoes', 5, '12.36', 'no-square'], [2, 'p-running-shoes', 5, '22', 'carried'], [2, 'p-running-shoes', 5, '21.97', 'carried'], [2, 'p-running-shoes', 5, '26', F], [2, 'p-running-shoes', 5, '12', F],
  [2, 'p-blood-screen', 1, '0.0359', T], [2, 'p-blood-screen', 1, '3.59%', T], [2, 'p-blood-screen', 1, '0.03593', T], [2, 'p-blood-screen', 1, '0.036', F], [2, 'p-blood-screen', 1, '0.9641', 'lower'], [2, 'p-blood-screen', 1, '0.0718', 'two-tail'], [2, 'p-blood-screen', 1, '0.6554', 'disease-curve'],
  [2, 'p-blood-screen', 1, '0.0719', 'two-tail', TOLD],
  [2, 'p-blood-screen', 2, '0.3446', T], [2, 'p-blood-screen', 2, '34.46%', T], [2, 'p-blood-screen', 2, '0.34458', T], [2, 'p-blood-screen', 2, '0.345', F], [2, 'p-blood-screen', 2, '0.6554', 'power'], [2, 'p-blood-screen', 2, '0.9641', 'healthy-curve'],
  [2, 'p-blood-screen', 3, '483', T], [2, 'p-blood-screen', 3, '482.9', T], [2, 'p-blood-screen', 3, '483.2', T], [2, 'p-blood-screen', 3, '483 patients', T], [2, 'p-blood-screen', 3, '482', F], [2, 'p-blood-screen', 3, '484', F],
  [2, 'p-blood-screen', 3, '131', 'true-only'], [2, 'p-blood-screen', 3, '352', 'false-only'], [2, 'p-blood-screen', 3, '421', 'beta-not-power'], [2, 'p-blood-screen', 3, '420.7', 'beta-not-power'],
  [2, 'p-blood-screen', 4, '0.27', T], [2, 'p-blood-screen', 4, '27%', T], [2, 'p-blood-screen', 4, '0.271', T], [2, 'p-blood-screen', 4, '0.2714', T], [2, 'p-blood-screen', 4, '131.1/483', T], [2, 'p-blood-screen', 4, '0.3', F], [2, 'p-blood-screen', 4, '0.28', F],
  [2, 'p-blood-screen', 4, '0.73', 'flipped'], [2, 'p-blood-screen', 4, '0.66', 'power'], [2, 'p-blood-screen', 4, '0.6554', 'power'], [2, 'p-blood-screen', 4, '0.16', 'carried'], [2, 'p-blood-screen', 4, '0.31', F],
  // problems-3
  [3, 'p-gene-screen', 1, '0.8715', T], [3, 'p-gene-screen', 1, '87.15%', T], [3, 'p-gene-screen', 1, '0.87149', T], [3, 'p-gene-screen', 1, '0.871', F], [3, 'p-gene-screen', 1, '0.87', F], [3, 'p-gene-screen', 1, '2', 'expected'], [3, 'p-gene-screen', 1, '0.1285', 'no-complement'], [3, 'p-gene-screen', 1, '0.05', 'single'],
  [3, 'p-gene-screen', 2, '0.0488', T], [3, 'p-gene-screen', 2, '4.88%', T], [3, 'p-gene-screen', 2, '0.04880', T], [3, 'p-gene-screen', 2, '0.049', F], [3, 'p-gene-screen', 2, '0.05', 'bound'], [3, 'p-gene-screen', 2, '0.9512', 'no-complement'], [3, 'p-gene-screen', 2, '0.8715', 'carried'],
  [3, 'p-gene-screen', 3, '2', T], [3, 'p-gene-screen', 3, '2 genes', T], [3, 'p-gene-screen', 3, '8', 'unadjusted'], [3, 'p-gene-screen', 3, '5', 'bh'], [3, 'p-gene-screen', 3, '3', F],
  [3, 'p-gene-screen', 4, '5', T], [3, 'p-gene-screen', 4, '5 genes', T], [3, 'p-gene-screen', 4, '3', 'first-fail'], [3, 'p-gene-screen', 4, '2', 'bonferroni'], [3, 'p-gene-screen', 4, '8', 'unadjusted'], [3, 'p-gene-screen', 4, '4', F],
  [3, 'p-fund-managers', 1, '2.7', T], [3, 'p-fund-managers', 1, '2.70', T], [3, 'p-fund-managers', 1, '27/10', T], [3, 'p-fund-managers', 1, 't=2.7', T], [3, 'p-fund-managers', 1, '0.3', 'over-root'], [3, 'p-fund-managers', 1, '8.1', 'times-t'],
  [3, 'p-fund-managers', 2, '0.0035', T], [3, 'p-fund-managers', 2, '0.35%', T], [3, 'p-fund-managers', 2, '0.00347', T], [3, 'p-fund-managers', 2, '0.003', F], [3, 'p-fund-managers', 2, '0.004', F], [3, 'p-fund-managers', 2, '0.007', 'two-sided'], [3, 'p-fund-managers', 2, '0.0070', 'two-sided'], [3, 'p-fund-managers', 2, '0.9965', 'lower'],
  [3, 'p-fund-managers', 2, '0.0069', 'two-sided', TOLD],
  [3, 'p-fund-managers', 3, '5', T], [3, 'p-fund-managers', 3, '5 managers', T], [3, 'p-fund-managers', 3, '3', 'first-fail'], [3, 'p-fund-managers', 3, '2', 'bonferroni'], [3, 'p-fund-managers', 3, '6', 'unadjusted'], [3, 'p-fund-managers', 3, '4', F],
  [3, 'p-checkout-designs', 1, '0.0953', T], [3, 'p-checkout-designs', 1, '9.53%', T], [3, 'p-checkout-designs', 1, '0.09534', T], [3, 'p-checkout-designs', 1, '0.095', F], [3, 'p-checkout-designs', 1, '0.1', 'bonferroni'], [3, 'p-checkout-designs', 1, '0.10', 'bonferroni'], [3, 'p-checkout-designs', 1, '0.004', 'single'], [3, 'p-checkout-designs', 1, '0.9047', 'no-complement'],
  [3, 'p-checkout-designs', 2, '0.002050', T], [3, 'p-checkout-designs', 2, '0.00205', T], [3, 'p-checkout-designs', 2, '0.0020496', T], [3, 'p-checkout-designs', 2, '2.05e-3', T], [3, 'p-checkout-designs', 2, '0.205%', T], [3, 'p-checkout-designs', 2, '0.002049', F],
  [3, 'p-checkout-designs', 2, '0.0020', 'bonferroni'], [3, 'p-checkout-designs', 2, '0.002', 'bonferroni'], [3, 'p-checkout-designs', 2, '0.0021', F], [3, 'p-checkout-designs', 2, '0.05', 'no-root'], [3, 'p-checkout-designs', 2, '0.7226', 'power-25'],
  [3, 'p-checkout-designs', 4, '0.5330', T], [3, 'p-checkout-designs', 4, '0.533', T], [3, 'p-checkout-designs', 4, '53.3%', T], [3, 'p-checkout-designs', 4, '0.53302', T], [3, 'p-checkout-designs', 4, '0.53', F], [3, 'p-checkout-designs', 4, '0.03', 'single'], [3, 'p-checkout-designs', 4, '0.75', 'bonferroni'], [3, 'p-checkout-designs', 4, '0.467', 'no-complement'],
  [3, 'p-biomarker-field', 1, '17.29', T], [3, 'p-biomarker-field', 1, '17.290', T], [3, 'p-biomarker-field', 1, '17.29 finds', T], [3, 'p-biomarker-field', 1, '17.3', F], [3, 'p-biomarker-field', 1, '17', F], [3, 'p-biomarker-field', 1, '18.2', 'all-400'], [3, 'p-biomarker-field', 1, '8.645', 'one-sided'], [3, 'p-biomarker-field', 1, '8.65', 'one-sided'],
  [3, 'p-biomarker-field', 2, '0.490', T], [3, 'p-biomarker-field', 2, '0.49', T], [3, 'p-biomarker-field', 2, '49%', T], [3, 'p-biomarker-field', 2, '0.4899', T], [3, 'p-biomarker-field', 2, '17.29/35.29', T], [3, 'p-biomarker-field', 2, '0.5', F],
  [3, 'p-biomarker-field', 2, '0.51', 'true-share'], [3, 'p-biomarker-field', 2, '0.043', 'over-400'], [3, 'p-biomarker-field', 2, '0.464', 'no-power'], [3, 'p-biomarker-field', 2, '0.503', F],
  [3, 'p-biomarker-field', 3, '1.026', T], [3, 'p-biomarker-field', 3, '1.0260', T], [3, 'p-biomarker-field', 3, '1.03', F], [3, 'p-biomarker-field', 3, '1.08', 'all-400'], [3, 'p-biomarker-field', 3, '17.29', 'old-bar'],
  [3, 'p-biomarker-field', 4, '0.079', T], [3, 'p-biomarker-field', 4, '7.9%', T], [3, 'p-biomarker-field', 4, '0.0788', T], [3, 'p-biomarker-field', 4, '1.026/13.026', T], [3, 'p-biomarker-field', 4, '0.08', F], [3, 'p-biomarker-field', 4, '0.054', 'old-power'], [3, 'p-biomarker-field', 4, '0.921', 'true-share'], [3, 'p-biomarker-field', 4, '0.083', 'carried'],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const seen = new Set();
let typedParts = 0;
for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/testing/problems-${n}.json`, 'utf8'));
  for (const it of doc.items) {
    it.parts.forEach((p, i) => {
      const k = i + 1, w = p.widget, where = `problems-${n} ${it.id} ${k}`;
      if (w.kind !== 'numeric') return;
      typedParts++;
      const by = (p.feedback && p.feedback.byKey) || {};
      say(grade(w, String(w.answer)).ok, null, `${where}: answer ${w.answer} grades correct`);
      for (const x of w.wrong || []) {
        const r = grade(w, String(x.value));
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} lands on its key (got ok=${r.ok} key=${r.key})`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
      }
      const rows = TYPED.filter(r => r[0] === n && r[1] === it.id && r[2] === k);
      say(rows.length >= 4, null, `${where}: at least four typed rows (${rows.length})`);
      for (const r of rows) {
        seen.add(r);
        let res; try { res = grade(w, r[3]); } catch (e) { res = { ok: null, key: 'THROW ' + e.message }; }
        const want = r[4];
        const good = want === true ? res.ok === true : want === false ? res.ok === false : want === 'NONE' ? (res.ok === false && res.key === null) : (res.ok === false && res.key === want);
        say(good, r[5], `${where}: typed "${r[3]}" is ${res.ok ? 'accepted' : 'refused'} (key ${res.key}), expected ${want === true ? 'accepted' : want === false ? 'refused' : 'refused on ' + want}`);
      }
    });
  }
}
for (const r of TYPED) if (!seen.has(r)) { fails++; console.log('FAIL    row never used: ' + r.slice(0, 4).join(' ')); }
console.log(`grade-probe: ${checks} checks over ${typedParts} typed parts, ${fails} failures, ${findings} findings (rows the reader holds to be faults)`);
process.exit(fails ? 1 : 0);
