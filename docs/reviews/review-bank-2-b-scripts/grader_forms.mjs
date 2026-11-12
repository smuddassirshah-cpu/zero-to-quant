#!/usr/bin/env node
/* Second reader, bank part 2 (b): the real grader (app/js/engine/grade.js numGrade) on every typed answer of the eight files.
   For each numeric item: the key in sensible forms must pass, each stored wrong value must show its own line, and the
   hand-listed "one step short" answers must be refused; the report says which line each lands on.
   Usage: node docs/reviews/review-bank-2-b-scripts/grader_forms.mjs            (prints surprises only; -v for every row) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '../../../app');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; g.ZQ = {}; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(APP, 'js/engine/grade.js'), 'utf8'), g);
const G = g.ZQ.grade;
const verbose = process.argv.includes('-v');

/* one step short (or the commonest near answer) per item: [typed text, what it is] */
const SHORT = {
  'fi-interest-monthly-to-annual': [['0.5', 'the monthly rate'], ['6.2', 'one place fewer'], ['0.0617', 'a decimal in a per cent field']],
  'fi-bonds-duration-move': [['-175', 'duration times 25, in basis points'], ['-0.0175', 'a decimal in a per cent field'], ['1.75', 'no minus sign']],
  'fi-forwards-six-month-fair': [['82.02', 'rounded down'], ['82', 'whole pounds']],
  'fi-equity-growing-dividend': [['0.05', 'r less g'], ['57.69', '3/1.04 over 0.05, shrinking the dividend']],
  'op-parity-price-the-put': [['50.97', 'the discounted strike'], ['4.1', 'one place'], ['4.07', 'key']],
  'op-strategies-bull-spread-breakeven': [['4', 'the net cost'], ['114', 'upper strike plus cost']],
  'op-greeks-second-order-estimate': [['1', 'the change, not the new price'], ['1.00', 'the change']],
  'tp-riskneutral-one-step-with-rate': [['0.5', 'the up probability'], ['4.76', 'q of 1/3 then discounted'], ['14.29', '15 over 1.05']],
  'tp-multistep-american-put-two-step': [['5.24', 'the wait value at 90'], ['10', 'the exercise value at 90'], ['2.38', '0.25 times 10 over 1.05, the up node dropped']],
  'ms-book-sweep-four-hundred': [['4009', 'the total cost'], ['10.02', 'two places'], ['10.023', 'three places']],
  'ms-costs-effective-spread': [['0.001', 'the fraction, not basis points'], ['0.1', 'in per cent'], ['2.5', 'fill against the ask']],
  'gv-risk-one-day-var': [['36000', 'one standard deviation'], ['83,736', 'with a comma'], ['83736.00', 'with pence'], ['83.736', 'in thousands']],
  'option-estimate-short-dated-call': [['4.79', 'the Black-Scholes value the feedback prints'], ['4.8', 'one place'], ['12', '150 times 0.32 times 0.25, no 0.4']],
  'fi-interest-three-payments-pv': [['1288.5', 'one place'], ['1,288.55', 'comma'], ['1388.89', 'undiscounted first payment (payments at the start of each year: 1391.63)'], ['1391.63', 'annuity due']],
  'fi-bonds-zero-coupon-yield': [['5', 'whole'], ['5.0', 'one place'], ['27.63', 'the five-year gain in per cent'], ['4.33', 'gain over five']],
  'fi-forwards-rich-forward': [['202', 'the fair forward'], ['5', 'quote less spot'], ['-3', 'the wrong side of the trade']],
  'fi-forwards-futures-daily-loss': [['-20000', 'a signed loss'], ['40', 'the points'], ['20,000', 'comma']],
  'op-strategies-covered-call-at-fifty': [['10', 'the share rise'], ['3', '5 less 2']],
  'op-strategies-butterfly-best-case': [['100', 'the share price of the peak']],
  'op-parity-call-under-its-floor': [['0.5', 'one place'], ['95.5', 'cash in hand']],
  'gamma-pnl-break-even-move': [['1.06', 'no half, two places'], ['1.1', 'no half, one place'], ['2.25', 'squared move'], ['1.50', 'two places']],
  'digital-option-at-the-money': [['0.47', 'two places'], ['-0.075', 'd2'], ['0.4701', 'key'], ['0.5299', 'N(d1)'], ['0.53', 'N(d1) to two places']],
  'tp-multistep-two-step-call': [['22.5', 'the top payoff'], ['4.4', 'one place'], ['40/9', 'the fraction'], ['0.1975', 'q squared']],
  'ms-book-weighted-mid': [['100.02', 'two places'], ['100.0160', 'four places']],
  'ms-costs-impact-four-times-size': [['2', 'the multiplier']],
  'ms-mm-spread-less-drift': [['600', 'in pence'], ['0.6', 'pence per share'], ['6.00', 'with pence']],
  'gv-risk-two-desks': [['1.73', 'two places'], ['1.7321', 'four places'], ['1732051', 'in pounds'], ['1.5', 'root of 1 + 1 + 0.5 squared... no: 1 + 1 + 0.25'], ['1.581', 'correlation without the 2']],
  'fi-interest-loan-payment': [['4021.1', 'one place'], ['4,021.15', 'comma'], ['4436.67', 'compound interest split three ways'], ['3655.59', 'payments at the start of each year']],
  'fi-bonds-three-year-coupon': [['105.6', 'one place'], ['105.55', 'key']],
  'fi-bonds-pound-per-basis-point': [['-4410', 'a signed loss'], ['4,410', 'comma'], ['441', 'duration 0.45']],
  'fi-forwards-geared-loss': [['-24%', 'with the sign'], ['-20', 'no interest'], ['-0.24', 'a decimal in a per cent field'], ['-28', 'interest on the whole 200,000']],
  'fi-forwards-currency-forward': [['1.27', 'two places'], ['1.2743', 'key'], ['1.3125', 'dollars grown, not divided']],
  'op-payoff-short-strangle-loss': [['3', 'a loss with no minus sign'], ['-£3', 'pound after minus'], ['£-3', 'pound before minus']],
  'op-strategies-one-by-two-breakeven': [['10', 'the peak payoff']],
  'op-parity-implied-forward': [['2.14', 'the forward less the strike'], ['102.1', 'one place (the not-compounded slip)'], ['102.14', 'key']],
  'op-greeks-vol-move-pnl': [['1,800', 'comma'], ['0.36', 'one option']],
  'tp-bs-at-the-money-delta': [['0.6', 'one place'], ['0.5793', 'four places'], ['0.2', 'd1']],
  'tp-multistep-monthly-up-factor': [['1.09', 'two places'], ['0.0866', 'the exponent'], ['1.0905', 'key']],
  'ms-book-who-gets-filled': [['350', 'what is left after C'], ['450', 'the whole order']],
  'ms-costs-shortfall-with-unfilled': [['360', 'the filled cost alone'], ['1,190', 'comma'], ['830', '800 plus 30']],
  'tp-bs-vega-rule': [['20', 'per unit of vol'], ['19.92', 'per unit of vol, exact'], ['0.2', 'one place'], ['0.1992', 'exact']],
  'fi-interest-one-year-forward-rate': [['5.0', 'one place'], ['5.01', 'key'], ['5.0097', 'four places'], ['5.00', 'the linear slip']],
  'fi-bonds-duration-and-convexity': [['-7.60', 'two places'], ['-8.4', 'convexity with the wrong sign'], ['0.4', 'the convexity term']],
  'fi-equity-combine-two-sharpes': [['1', 'whole'], ['1.00', 'two places']],
  'fi-forwards-implied-rate': [['3.9605', 'four places'], ['1.98', 'the half-year log return'], ['2', 'the half-year gain']],
  'digital-option-from-two-calls': [['0.55', 'key'], ['£0.55', 'pound sign'], ['55p', 'pence'], ['0.6', 'one place']],
  'op-strategies-protective-put-floor': [['-13', 'a signed loss'], ['£13', 'pound sign'], ['113', '110 plus 3']],
  'op-greeks-put-delta-from-call': [['−0.38', 'a typographic minus'], ['-.38', 'no leading zero']],
  'tp-multistep-lookback-two-step': [['64', 'the sum of the highs'], ['£16', 'pound sign']],
  'ms-book-opening-auction': [['10.1', 'the price, not the volume'], ['900', 'shares bid at 10.1']],
  'ms-orders-immediate-or-cancel': [['300', 'the cancelled part']],
  'ms-costs-participation-time': [['15000', 'the hourly rate'], ['4 hours', 'unit word'], ['4h', 'unit letter']],
  'option-estimate-straddle-implied-move': [['5', 'the move in pounds'], ['10%', 'per cent sign'], ['10.03', 'the Black-Scholes figure the feedback prints'], ['8', 'no factor']],
};

const places = (q) => { const m = /to (\d) decimal places?/.exec(q || ''); return m ? +m[1] : null; };
let rows = 0, bad = 0;
const out = (tag, id, typed, r, note) => { rows++; if (tag !== 'ok') bad++; if (verbose || tag !== 'ok') console.log(`${tag.padEnd(9)} ${id.padEnd(42)} ${String(typed).padEnd(12)} -> ${r.ok ? 'CORRECT' : r.key ? 'wrong:' + r.key : Number.isFinite(r.detail.value) ? 'generic' : 'NOT A NUMBER'}  ${note || ''}`); };
const summary = [];
for (const fam of ['finance', 'coding']) for (const n of [1, 2, 3, 4]) {
  const file = JSON.parse(fs.readFileSync(path.join(APP, 'content/bank', `${fam}-${n}.json`), 'utf8'));
  for (const it of file.items) {
    const w = it.widget; if (w.kind !== 'numeric') continue;
    const pct = w.unit === '%', k = pct ? 100 : 1, a = +w.answer * k, dp = places(it.question);
    const base = dp == null ? G.fmtNum(+(a).toFixed(6)) : a.toFixed(dp);
    const forms = new Set([base, G.fmtNum(a)]);
    if (/pound|£/.test(it.question + (w.label || ''))) forms.add('£' + base);
    if (pct) forms.add(base + '%');
    if (dp != null) forms.add(a.toFixed(dp + 1)), forms.add(a.toFixed(dp + 2));
    if (Math.abs(a) >= 1000) forms.add(Number(base).toLocaleString('en-GB', { minimumFractionDigits: dp || 0 }));
    for (const f of forms) { const r = G.numGrade(w, f); out(r.ok ? 'ok' : 'KEY-FORM', it.id, f, r, 'a form of the key'); }
    /* the figure feedback.correct and accept print */
    for (const src of [it.feedback.correct, w.accept]) {
      const m = /(-?£?-?[\d,]+(?:\.\d+)?)%?/.exec(String(src || '').replace(/^Correct\.\s*/, '').replace(/[A-Za-z ]*?(?=-?£?\d)/, ''));
      if (m) { const t = m[1]; const r = G.numGrade(w, t); out(r.ok ? 'ok' : 'PRINTED', it.id, t, r, 'printed in feedback or accept: ' + String(src).slice(0, 50)); }
    }
    for (const x of w.wrong || []) {
      const t = G.fmtNum(+x.value * k); const r = G.numGrade(w, t);
      out(!r.ok && r.key === x.id ? 'ok' : 'WRONG-ID', it.id, t, r, 'stored wrong ' + x.id);
    }
    if (dp != null && dp > 0) { const t = a.toFixed(dp - 1); const r = G.numGrade(w, t); summary.push([it.id, t, 'one place fewer', r]); }
    for (const [t, what] of SHORT[it.id] || []) { const r = G.numGrade(w, t); summary.push([it.id, t, what, r]); }
    if (fam === 'finance' && !SHORT[it.id]) console.log('NO-SHORT  ' + it.id);
  }
}
console.log(`\n${rows} graded forms, ${bad} surprises\n\nNear answers and where they land:`);
for (const [id, t, what, r] of summary) console.log(`${id.padEnd(42)} ${t.padEnd(10)} ${(r.ok ? 'CORRECT' : r.key ? 'wrong:' + r.key : Number.isFinite(r.detail.value) ? 'generic' : 'NOT A NUMBER').padEnd(24)} ${what}`);
