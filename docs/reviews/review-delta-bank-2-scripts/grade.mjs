#!/usr/bin/env node
/* Delta read of the two bank part 2 fix passes: what the engine's own numeric grader (app/js/engine/grade.js numGrade)
   does with every changed typed answer.
     - automatic, for each listed item: the stored answer grades correct; every wrong[] value grades wrong and lands on
       its own id; every wrong id has a feedback.byKey line; no wrong band touches the key band (FAIL if not)
     - TYPED rows [typed, expected, note?]: expected is true (accepted), a wrong id (refused with that line),
       null (refused with the generic line) or "NOPARSE" (the field does not read it).
       A row with a note is one the review records: it prints as FINDING and does not fail the run.
   node docs/reviews/review-delta-bank-2-scripts/grade.mjs [--show]      (from the repo root) */
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

const LOSS = 'a right size typed without the minus sign the question asks for gets the generic line, which points at the method';
const TYPED = {
  // ---- statistics: graded answers changed
  'es-bayes-seven-in-ten': [['5/7', true], ['10/14', true], ['0.7143', true], ['.7143', true], ['0.714', true], ['0.7142', true], ['0.71', null], ['0.7', 'no-prior'], ['7/10', 'no-prior'],
    ['2/3', 'one-each'], ['0.6667', 'one-each'], ['0.667', 'one-each'], ['9/14', null], ['0.6429', null], ['0.75', null]],
  'rg-inference-overall-f': [['3.75', true], ['15/4', true], ['3.750', true], ['3.81', 'df-61'], ['3.8125', 'df-61'], ['3.8', null], ['0.25', 'no-df'], ['1/4', 'no-df'], ['5.71', null], ['0.05', null], ['3.7', null]],
  'ts-acf-noise-band': [['0.0784', true], ['.0784', true], ['0.07840', true], ['0.078', null], ['0.08', 'rule-of-two'], ['0.0800', 'rule-of-two'], ['0.04', 'no-multiplier'], ['1/25', 'no-multiplier'],
    ['0.0031', 'divided-by-n'], ['0.003136', 'divided-by-n'], ['0.003', null], ['0.098', null], ['0.1', null], ['0.1568', null]],
  'rg-inference-t-from-r-squared': [['2.5', true], ['2.50', true], ['5/2', true], ['-2.5', null], ['2.6', 'used-n'], ['2.60', 'used-n'], ['2.598', 'used-n'], ['2.24', 'no-one-minus'], ['2.236', 'no-one-minus'],
    ['6.25', 'no-root'], ['5', null], ['2.4', null], ['2.51', null]],
  'collinear-features-inflation-factor': [['1.56', true], ['1.5625', true], ['1.563', true], ['25/16', true], ['1.57', null], ['1.6', null], ['2.5', 'one-minus-r'], ['1.25', 'standard-error-factor'], ['5/4', 'standard-error-factor'],
    ['0.64', null], ['0.36', null], ['5.26', null]],
  'measurement-error-noisy-regressor': [['0.98', true], ['.98', true], ['49/50', true], ['0.980', true], ['1.4', 'no-attenuation'], ['2', 'wrong-way'], ['2.00', 'wrong-way'], ['0.7', null], ['0.75', null], ['1', null]],
  'sample-size-for-signal-sharpe-years': [['18.4', true], ['18.37', true], ['18.367', true], ['900/49', true], ['18.3', null], ['18', null], ['18.5', null], ['4.3', 'no-square'], ['4.29', 'no-square'], ['4.2857', 'no-square'],
    ['8.2', 'aimed-at-two'], ['8.16', 'aimed-at-two'], ['8.163', 'aimed-at-two'], ['18.4 years', true]],
  'weak-signal-daily-edge': [['1', true], ['1.00', true], ['1.0', true], ['0.04', 'no-root'], ['0.63', 'annual-sharpe'], ['0.635', 'annual-sharpe'], ['0.64', null], ['25', null], ['2', null], ['0.99', null]],
  // ---- statistics: bands and slips changed
  'dl-clt-mean-of-hundred': [['0.023', true], ['0.0228', true], ['0.02275', true], ['.023', true], ['0.02', null], ['0.024', null], ['0.421', 'no-root'], ['0.4207', 'no-root'], ['0.42', null],
    ['0.046', 'both-tails'], ['0.0455', 'both-tails'], ['0.045', 'both-tails'], ['0.977', null], ['2', null]],
  'ht-errors-sample-for-power': [['197', true], ['196', 'rounded-down'], ['196.2', null], ['97', 'no-power'], ['155', 'one-sided'], ['393', 'two-groups'], ['392', null], ['198', null], ['14', null]],
  'rg-inference-new-observation': [['2.04', true], ['2.0396', true], ['2.4', 'added-errors'], ['2.40', 'added-errors'], ['2', 'noise-only'], ['0.4', 'fitted-mean'], ['4.16', null], ['2.03', null], ['2.05', null]],
  'es-intervals-poll-margin': [['4.8', true], ['4.80', true], ['4.801', true], ['4.9', 'used-half'], ['4.90', 'used-half'], ['4.899', 'used-half'], ['2.4', 'no-multiplier'], ['2.45', 'no-multiplier'], ['0.048', null], ['5', null]],
  // ---- statistics: text only (the key must still behave)
  'power-one-sided-shift': [['0.6387', true], ['.6387', true], ['0.3613', 'miss-rate'], ['0.516', 'two-sided'], ['0.64', null], ['0.6368', null], ['0.6406', null]],
  'es-intervals-two-desk-gap': [['0.016', true], ['.016', true], ['16', null], ['0.246', 'one-mean'], ['1.584', 'upper-end'], ['0.02', null]],
  'es-mle-waits-between-trades': [['0.2', true], ['1/5', true], ['.2', true], ['5', 'mean-wait'], ['0.1667', 'five-gaps'], ['1/6', 'five-gaps'], ['0.17', null]],
  'shrinkage-mse-best-multiplier': [['0.75', true], ['3/4', true], ['1', 'unbiased'], ['0.5', 'equal-split'], ['2.25', null]],
  // ---- finance: re-authored
  'op-parity-price-the-put': [['6.85', true], ['6.8494', true], ['6.849', true], ['£6.85', true], ['6.84', null], ['6.9', null], ['8.1', 'undiscounted'], ['8.10', 'undiscounted'], ['£8.10', 'undiscounted'],
    ['1.35', 'signs-swapped'], ['1.3506', 'signs-swapped'], ['82.75', null], ['2.75', null], ['-6.85', null], ['4.07', null]],
  'fi-forwards-currency-forward': [['0.8811', true], ['0.881078', true], ['.8811', true], ['0.88108', true], ['0.881', null], ['0.8812', null], ['0.8394', 'rates-swapped'], ['0.839426', 'rates-swapped'], ['0.8815', 'added-gap'],
    ['0.8987', null], ['1.135', null], ['0.86', null], ['1.2743', null], ['£0.8811', true], ['0.8811 pounds', true]],
  'ms-costs-shortfall-with-unfilled': [['825', true], ['£825', true], ['825.00', true], ['225', 'filled-only'], ['800', 'no-commission'], ['200', 'filled-cost'], ['£200', 'filled-cost'], ['600', null], ['1600', null], ['775', null], ['-825', null], ['1190', null]],
  'op-strategies-bull-spread-breakeven': [['44', true], ['£44', true], ['44.00', true], ['47', 'one-premium'], ['50', 'both-premiums'], ['4', null], ['46', null], ['104', null]],
  'op-payoff-short-strangle-loss': [['-3', true], ['−3', true], ['-£3', true], ['-3.00', true], ['-9', 'no-premium'], ['6', 'premium-only'], ['£6', 'premium-only'], ['3', null, LOSS], ['£3', null, LOSS], ['9', null]],
  'op-strategies-butterfly-best-case': [['8', true], ['£8', true], ['10', 'ignored-cost'], ['2', 'gave-cost'], ['20', null], ['6', null], ['7', null]],
  'ms-book-weighted-mid': [['800', true], ['800 shares', true], ['900', 'size-wanted'], ['100', 'size-now'], ['1000', null], ['100.016', null]],
  // ---- finance: the three loss items
  'fi-forwards-futures-daily-loss': [['20000', true], ['20,000', true], ['£20,000', true], ['-20000', 'signed'], ['-20,000', 'signed'], ['−20000', 'signed'], ['-£20,000', 'signed'], ['£-20,000', 'signed'],
    ['2000', 'one-contract'], ['400', 'points-times-contracts'], ['40', null], ['-2000', null], ['20k', 'NOPARSE']],
  'fi-bonds-pound-per-basis-point': [['4410', true], ['4,410', true], ['£4,410', true], ['4410.4', true], ['-4410', 'signed'], ['-4,410', 'signed'], ['−4410', 'signed'], ['-£4,410', 'signed'], ['4500', 'face-not-price'], ['44100', 'ten-basis-points'],
    ['441', null], ['-4500', null], ['4400', null]],
  'op-strategies-protective-put-floor': [['13', true], ['£13', true], ['13.00', true], ['-13', 'signed'], ['−13', 'signed'], ['-£13', 'signed'], ['10', 'no-premium'], ['7', 'took-off-premium'], ['110', null], ['123', null], ['-10', null]],
  // ---- finance: the step-short lines
  'tp-bs-vega-rule': [['0.2', true], ['0.20', true], ['0.1992', true], ['0.199', true], ['£0.20', true], ['0.4', 'no-time'], ['0.1', 'used-t'], ['20', 'per-unit-vol'], ['19.92', 'per-unit-vol'], ['19.9', 'per-unit-vol'], ['0.19', null], ['0.21', null]],
  'gv-risk-one-day-var': [['83736', true], ['83,736', true], ['£83,736', true], ['59220', 'used-1-645'], ['264796', 'ten-day'], ['36000', 'one-sd'], ['36,000', 'one-sd'], ['83700', null], ['-83736', null]],
  'fi-forwards-rich-forward': [['3', true], ['£3', true], ['-1', 'no-dividend'], ['7', 'dividend-twice'], ['202', 'fair-value'], ['£202', 'fair-value'], ['205', null], ['206', null]],
  'op-greeks-second-order-estimate': [['5', true], ['5.00', true], ['£5.00', true], ['4.9', 'delta-only'], ['4.90', 'delta-only'], ['5.1', 'no-half'], ['1', 'change-only'], ['1.00', 'change-only'], ['0.1', null], ['0.9', null]],
  'ms-book-opening-auction': [['550', true], ['550 shares', true], ['500', 'cleared-high'], ['850', 'all-sells'], ['10.1', 'gave-price'], ['10.10', 'gave-price'], ['£10.10', 'gave-price'], ['900', null], ['250', null]],
  'ms-mm-spread-less-drift': [['6', true], ['£6', true], ['6.00', true], ['10', 'ignored-move'], ['14', 'added-move'], ['600', 'in-pence'], ['0.6', null]],
  'op-parity-implied-forward': [['102.14', true], ['102.1429', true], ['102.143', true], ['102.1', 'not-compounded'], ['102.10', 'not-compounded'], ['100.1', 'gave-spot'], ['2.14', 'gap-only'], ['2.1429', 'gap-only'], ['2.1', null], ['102.15', null], ['102', null]],
  'tp-multistep-two-step-call': [['4.44', true], ['40/9', true], ['4.4444', true], ['£4.44', true], ['5.625', 'even-chances'], ['5.63', 'even-chances'], ['5.62', 'even-chances'], ['10', 'q-once'], ['22.5', 'top-payoff'], ['22.50', 'top-payoff'], ['4/9', null], ['4.4', null], ['4.45', null]],
  'ms-book-who-gets-filled': [['150', true], ['250', 'time-first'], ['300', 'filled-in-full'], ['350', 'left-after-c'], ['200', null], ['100', null]],
  // ---- coding: the three typed reasoning items
  'pf-functions-default-list': [['5', true], ['3', 'fresh-dict'], ['4', 'count-of-x'], ['6', null], ['2', null]],
  'pf-classes-shared-class-list': [['8', true], ['7', 'own-list'], ['9', 'shared-cap'], ['2', null], ['6', null]],
  'pf-types-round-half-even': [['-12', true], ['−12', true], ['-10', 'all-towards-zero'], ['-11', 'half-up'], ['12', null], ['-9', null], ['4', null]],
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
