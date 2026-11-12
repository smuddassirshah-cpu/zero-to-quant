#!/usr/bin/env node
/* Delta read AC-3: what the engine's own graders (app/js/engine/grade.js: numGrade, numSetGrade, and exprGrade with the
   local Compute Engine) do with every changed part of the four fix passes, typed as a learner types.
     - the stored answer and each accept[] form grade correct; each wrong[] entry typed at its stored value is refused,
       lands on its own id and has a byKey line (FAIL if not).
     - TYPED rows [typed, expected, note?]: expected is true (accepted), a wrong id, null (generic refusal) or
       "NOPARSE". A row with a note is one the review records: when it misbehaves it prints FINDING and does not fail.
   node docs/reviews/review-delta-ac-3-scripts/grade.mjs --local-cdn <pkgs> [--show]     (from the repo root) */
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
const numSet = (w, t) => { const r = G.numSetGrade(w, t); return r.ok ? true : (r.key || null); };
const expr = (w, t) => { let r; try { r = G.exprGrade(ce, w, t, t); } catch (e) { return 'THROW ' + e.message; } return r.ok ? true : (r.key || null); };

const R1 = 'courses/ratio/problems-1', R2 = 'courses/ratio/problems-2', R3 = 'courses/ratio/problems-3', E4 = 'courses/eigen/problems-4';
const N1 = 'courses/number-sense/problems-1', N2 = 'courses/number-sense/problems-2', N3 = 'courses/number-sense/problems-3', S3 = 'exams/stage-3';
const NOTE_14 = 'finding 4.1: 14 is accepted where the nearest whole number is asked';
const NOTE_523 = 'finding 4.2: the exact value to 2 places gets the generic line';
const NOTE_CHF = 'finding 1.2: the currency code typed before the number, as the item writes it, is not read';
const NOTE_EUR = 'finding 1.3: the euro sign typed after the number is not read';
const NOTE_DEG = 'finding 3.1: °C typed on a field whose unit is degrees is not read';
const NOTE_R2 = 'finding 4.3: the gap over the model\'s MSE is accepted';
// [file, item id or index path, part (1-based, 0 for the node itself), rows]
const TYPED = [
  // ---- 1. ratio
  [R1, 'p-phone-rise', 4, [['43.6', true], ['43.6%', true], ['43.57', true], ['43.6 %', true], ['37.3', null], ['44', null], ['46.7', 'old-price'], ['46.67', 'old-price'], ['229.5', 'upside-down'], ['229.5%', 'upside-down'], ['56.4', 'saving'], ['56.43', 'saving'], ['40', null]]],
  [R1, 'p-platform-fee', 3, [['8370.60', true], ['£8,370.60', true], ['8429.40', 'added']]],
  [R1, 'p-platform-fee', 4, [['82', true], ['82%', true], ['81.6', true], ['8', 'one-place'], ['8.2', 'one-place'], ['8.16', 'one-place'], ['122', 'upside-down'], ['123', 'upside-down'], ['122.5', 'upside-down'], ['0.29', 'account-base'], ['0.3', 'account-base'], ['80', null]]],
  [R2, 'p-laptop-sale', 1, [['660', true], ['£660.00', true], ['476.85', 'off-again'], ['£476.85', 'off-again'], ['645.15', 'added'], ['477', null]]],
  [R2, 'p-laptop-sale', 3, [['-6.5', true], ['-6.5%', true], ['6.5', 'sign'], ['-5', 'added'], ['-7', 'sale-base'], ['-7.0', 'sale-base'], ['-6.95', 'sale-base'], ['-6.9', 'sale-base'], ['-6.6', null]]],
  [R3, 'p-partners-profit', 1, [['15', true], ['15 parts', true], ['12', null], ['60', 'thousands'], ['30', 'halved']]],
  [R3, 'p-partners-profit', 2, [['5120', true], ['£5,120', true], ['5,120', true], ['640', 'one-part'], ['3200', 'equal'], ['4000', null]]],
  [R3, 'p-partners-profit', 3, [['14250', true], ['£14,250', true], ['8550', 'own-parts'], ['42750', 'one-part-share'], ['11400', null]]],
  [R3, 'p-partners-profit', 4, [['1400', true], ['£1,400', true], ['1586.67', 'old-parts'], ['£1,586.67', 'old-parts'], ['2975', 'equal'], ['1700', null]]],
  [R3, 'p-print-run', 1, [['7.5', true], ['7.5 hours', true], ['7.5 h', true], ['30', 'direct'], ['11', 'subtracted'], ['19.2', null], ['9', null]]],
  [R3, 'p-print-run', 2, [['840', true], ['£840', true], ['3360', 'direct'], ['£3,360', 'direct'], ['105', 'one-press'], ['2150.4', null]]],
  [R3, 'p-print-run', 3, [['23.33', true], ['£23.33', true], ['42.86', 'upside-down'], ['0.02', 'per-leaflet']]],
  [R3, 'p-coffee-suppliers', 1, [['27.50', true], ['27.5', true], ['CHF 27.50', true, NOTE_CHF], ['27.50 CHF', true], ['CHF27.50', true, NOTE_CHF], ['27.50 francs', true], ['29.40', 'german'], ['29.4', 'german']]],
  [R3, 'p-villa-split', 1, [['540', true], ['€540', true], ['540 €', true, NOTE_EUR], ['540€', true, NOTE_EUR], ['540 euros', true], ['405', 'unchanged'], ['303.75', 'direct']]],
  [R3, 'p-villa-split', 3, [['630', true], ['€630', true], ['630 €', true, NOTE_EUR], ['540', 'equal'], ['360', 'four-nights'], ['€360', 'four-nights']]],
  // ---- 2. eigen
  [E4, 'p-linked-lagoons', 1, [['-5', true], ['5', 'sign'], ['-3', 'unchanged'], ['-1', 'reversed'], ['-4', null], ['-2', null]]],
  [E4, 'p-linked-lagoons', 2, [['-5, -2', true], ['-2, -5', true], ['-5 and -2', true], ['5, 2', 'sign'], ['-7, 10', 'trace-det'], ['-4, -3', 'a-diagonal'], ['-5, 2', null]]],
  [E4, 'p-linked-lagoons', 3, [['(2,-1)', true], ['(2, -1)', true], ['(2,-5)', 'inverse'], ['(2,-3)', 'unmoved'], ['(4,-1)', null], ['(3,-1)', null]]],
  [E4, 'p-linked-lagoons', 4, [['(3,1)', true], ['(1,3)', 'swapped'], ['(5,-3)', 'w-coords'], ['(3,2)', null]]],
  [E4, 'p-linked-lagoons', 5, [['0.819', true], ['0.819 kg', true], ['0.413', 'coefficients-only'], ['0.419', 'u1-only'], ['0.176', 'rates-swapped'], ['0.291', 'carried']]],
  [E4, 'p-machine-stops', 1, [['0, -0.5', true], ['-0.5, 0', true], ['0, -1/2', true], ['0 and -0.5', true], ['0, -.5', true], ['0, 0.5', 'sign'], ['0.5, 0', 'sign'], ['-0.1, -0.4', 'diagonal'], ['0, -0.8', null], ['-0.2, -0.6', null]]],
  [E4, 'p-machine-stops', 2, [['(0.8,0.2)', true], ['(0.8, 0.2)', true], ['(4/5,1/5)', true], ['(.8,.2)', true], ['(0.2,0.8)', 'swapped'], ['(4,1)', 'unscaled'], ['(0.75,0.25)', null], ['(0.25,0.75)', null], ['(3,1)', null]]],
  [E4, 'p-machine-stops', 4, [['0.266', true], ['0.2657', true], ['.266', true], ['0.816', 'running-chance'], ['0.066', 'no-steady'], ['0.308', 'restart-rate'], ['0.685', 'one-hour'], ['0.318', null], ['0.27', null]]],
  [E4, 'p-machine-stops', 5, [['8.76', true], ['8.76 hours', true], ['8.764', true], ['5.99', 'running-start'], ['9.21', 'no-coefficient'], ['10.96', 'restart-rate'], ['2.19', 'multiplied'], ['5.40', null], ['8.8', null]]],
  // ---- 3. number-sense
  [N1, 'p-garden-beds', 1, [['5', true], ['5 beds', true], ['80', 'flipped'], ['15', 'three-quarters'], ['8', null], ['4', null]]],
  [N1, 'p-rye-loaves', 1, [['25/6', true], ['4 1/6', true], ['4.1667', true], ['1/6', 'multiplied'], ['6/25', 'wrong-flip'], ['0.24', 'wrong-flip'], ['10/3', null], ['4', null]]],
  [N1, 'p-rye-loaves', 2, [['4', true], ['4 loaves', true], ['5', 'rounded-up'], ['0', 'carried'], ['3', null]]],
  [N1, 'p-rye-loaves', 3, [['1/30', true], ['1/30 kg', true], ['19/30', 'one-loaf'], ['1', 'tops-bottoms'], ['1/6', 'loaf-sixth'], ['1/12', null]]],
  [N1, 'p-rye-loaves', 4, [['1/25', true], ['0.04', true], ['6/150', true], ['1/36', 'multiplied'], ['25', 'flipped'], ['19/25', 'carried'], ['1/10', null]]],
  [N1, 'p-two-printers', 3, [['7/9', true], ['7/9 hours', true], ['7/9 of an hour', true], ['46 2/3', 'minutes'], ['140/3', 'minutes']]],
  [N1, 'p-two-printers', 4, [['320/3', true], ['106 2/3', true], ['106 2/3 minutes', true], ['1 7/9', 'hours'], ['16/9', 'hours'], ['46 2/3', 'rest-only']]],
  [N1, 'p-squash-jugs', 1, [['16', true], ['16/36', 'whole-fraction'], ['4/9', 'whole-fraction'], ['4', 'top-kept']]],
  [N1, 'p-squash-jugs', 3, [['1/3', true], ['1/3 litres', true], ['1/3 litre', true]]],
  [N2, 'p-moor-weather', 1, [['1.3', true], ['1.3 °C', true], ['1.3°C', true], ['1.3 degrees', true], ['-8.5', 'subtracted'], ['-8.5 °C', 'subtracted'], ['8.5°C', 'start-sign']]],
  [N2, 'p-moor-weather', 2, [['-6.3', true], ['-6.3 degrees', true], ['-6.3 °C', true, NOTE_DEG], ['-6.3°C', true, NOTE_DEG], ['6.3 degrees', 'sign'], ['3.5', 'carried']]],
  [N2, 'p-moor-weather', 3, [['-0.7', true], ['-0.7 degrees', true], ['-0.7 °C', true, NOTE_DEG], ['0.7', 'sign'], ['-56.7', 'times']]],
  [N2, 'p-moor-weather', 4, [['-7.8', true], ['-7.8 °C', true], ['-7.8°C', true], ['−7.8 °C', true], ['-2.8 °C', 'change-only']]],
  [N2, 'p-golf-card', 3, [['0.278', true], ['.278', true], ['0.2780', true], ['0.2778', 'unrounded'], ['0.27778', 'unrounded'], ['5/18', 'unrounded'], ['0.2777', 'unrounded'], ['0.277', 'truncated'], ['3.6', 'flipped'], ['0.28', null], ['0.279', null], ['0.27', null]]],
  [N2, 'p-taxi-split', 1, [['2.8333', true], ['£2.8333', true], ['2.8333 pounds', true]]],
  [N2, 'p-taxi-split', 2, [['2.83', true], ['£2.83', true], ['2.83 pounds', true], ['2.830', true], ['2.833', 'unrounded'], ['2.8333', 'unrounded'], ['£2.8333', 'unrounded'], ['17/6', 'unrounded'], ['2.84', 'rounded-up'], ['2.8', 'one-dp'], ['283', 'pence'], ['2.82', null]]],
  [N2, 'p-taxi-split', 3, [['-2', true], ['-2p', true], ['-2 p', true], ['-2 pence', true], ['2p', 'sign'], ['-0.02', 'pounds'], ['4', 'carried-up']]],
  [N2, 'p-taxi-split', 4, [['2.85', true], ['£2.85', true], ['285', 'pence'], ['2.83', 'same'], ['2.81', 'wrong-way']]],
  [N3, 'p-cube-tub', 1, [['12', true], ['12 cubes', true], ['13', 'rounded-up'], ['46', 'square-root'], ['47', 'square-root'], ['46.57', 'square-root'], ['723', 'thirds'], ['11', null]]],
  [N3, 'p-cube-tub', 2, [['441', true], ['441 cubes', true], ['2025', 'squared'], ['2,025', 'squared'], ['-28', 'carried-up'], ['2133', 'times-three'], ['169', null]]],
  [N3, 'p-cube-tub', 3, [['21', true], ['21 cubes', true], ['220.5', 'halved'], ['220', 'halved'], ['221', 'halved'], ['110.25', 'quartered'], ['110', 'quartered'], ['13', null]]],
  [N3, 'p-stationery-bill', 2, [['203.80', true], ['£203.80', true], ['203.8', true]]],
  [N3, 'p-comet-probe', 1, [['30000', true], ['30,000', true], ['30000 hours', true], ['30,000 hours', true]]],
  [N3, 'p-comet-probe', 3, [['3', true], ['3 years', true], ['3.33', 'unrounded'], ['3.3', 'unrounded'], ['3.333', 'unrounded'], ['4', 'carried']]],
  [N3, 'p-comet-probe', 4, [['3.4', true], ['3.4 years', true], ['3.42', true], ['3.3', 'nine-thousand']]],
  // ---- 4. bands pass, part B
  ['courses/series/problems-2', 'items[2]', 1, [['7.42', true], ['7.43', true], ['7.4244', true], ['7.41', null], ['7.44', null], ['7.45', 'ten'], ['7.37', 'eight'], ['7.5', 'forever'], ['7.50', 'forever']]],
  ['courses/integrals/problems-4', 'items[2]', 2, [['2.048', true], ['2.049', true], ['2.0485', true], ['2.047', null], ['2.05', null], ['0.326', 'no-2pi'], ['0.141', 'disc']]],
  ['courses/integrals/problems-4', 'items[2]', 4, [['15', true], ['14.55', true], ['14.6', true], ['14', null, NOTE_14], ['13', null], ['16', null], ['8', 'square-integral'], ['0.07', 'inverse']]],
  [S3, 'r-turnover-cost', 0, [['0.79', true], ['0.79%', true], ['0.78', true], ['0.7857', true], ['0.8', null], ['0.80', null], ['0.77', null], ['0.39', 'twice'], ['1.1', 'no-turnover']]],
  [S3, 'r-small-share', 2, [['1.07', true], ['1.07%', true], ['1.06', true], ['1.0655', true], ['1.05', null], ['1.08', null], ['1', 'big-only'], ['6.9', 'equal-weighted']]],
  [S3, 'r-oos-power', 1, [['1.41', true], ['1.42', true], ['1.4142', true], ['1.4', null], ['1.40', null], ['1.43', null], ['2', 'halved-only'], ['2.83', 'full-mean']]],
  ['exams/topic-0.2', 'e-formula', 0, [['2.77', true], ['2.76', true], ['2.7656', true], ['2.75', null], ['2.78', null], ['5.53', 'no-2a'], ['1.27', 'sign-b']]],
  // ---- part C
  [S3, 'r-t-bar', 1, [['2.75', true], ['2.76', true], ['2.754', true], ['2.7607', true], ['2.74', null], ['2.77', null], ['2.8', null], ['2.81', null], ['0.15', 'no-root'], ['0.8', 'years'], ['0.80', 'years']]],
  [S3, 'r-best-of-twenty', 0, [['0.23', true], ['0.22', true], ['0.225', true], ['.23', true], ['0.21', null], ['0.24', null], ['0.2', null], ['0.25', 'added-chances'], ['0.01', 'one-variant'], ['0.0127', 'one-variant']]],
  // ---- part D
  ['courses/ds/review-4', 'r4-height', 0, [['3', true], ['4', 'nodes'], ['5', null]]],
  ['courses/estimation/homework-3', 'h-laplace', 0, [['(n+1)/(n+2)', true], ['\\frac{n+1}{n+2}', true], ['1', 'mle'], ['(n+1)/(n+1)', 'mle'], ['\\frac{n+1}{n+1}', 'mle'], ['n/n', 'mle'], ['n/(n+2)', 'no-prior-head'], ['n/(n+1)', null]]],
  ['courses/limits/homework-5', 'h-arctan-recip', 0, [['-1/(1+x^2)', true], ['-\\frac{1}{1+x^2}', true], ['1/(1+x^2)', 'sign'], ['1/(1+1/x^2)', 'no-chain'], ['x^2/(1+x^2)', 'no-chain'], ['\\frac{x^2}{1+x^2}', 'no-chain'], ['\\frac{x^2}{x^2+1}', 'no-chain'], ['-x^2/(1+x^2)', null]]],
  ['courses/multivar/homework-5', 'h-parallelogram', 0, [['9', true], ['3', 'noJ'], ['27', null]]],
  ['courses/markov/l20-when-stopping-fails', 'screens[5]', 0, [['0', true], ['£0', true], ['1', 'win'], ['£1', 'win'], ['1.00', 'win'], ['0.999', 'most'], ['0.9990', 'most'], ['1023/1024', 'most'], ['-1023', 'loss'], ['-£1,023', 'loss']]],
  ['courses/multivar/l4-chain-two-inputs', 'screens[8]', 0, [['140', true], ['£140', true], ['0', 'rates'], ['0.14', 'per-option'], ['£0.14', 'per-option'], ['280', 'delta-only'], ['-140', 'vega-only'], ['420', 'sign']]],
  ['courses/numerics/l12-stiff-equations', 'screens[0]', 0, [['8.24', true], ['8.24%', true], ['8.2393', true], ['5.2253', 'exact'], ['5.2253%', 'exact'], ['5.225', 'exact'], ['5.2222', 'small'], ['5.2222%', 'small'], ['5.23', 'exact', NOTE_523], ['5.22', null]]],
  ['courses/stat-learning/review-2', 'r-test-r2', 0, [['-0.0222', true], ['-0.022', true], ['-0.02222', true], ['0.0222', 'pos'], ['0.022', 'pos'], ['0.02222', 'pos'], ['0.0217', 'flip'], ['0.02174', 'flip'], ['0.02', null], ['-0.0217', null, NOTE_R2], ['-0.02174', null, NOTE_R2]]],
  ['courses/taylor/l2-how-wrong', 'screens[10]', 0, [['500', true], ['£500', true], ['0', 'zero'], ['£0', 'zero'], ['0.5', 'per-contract'], ['0.50', 'per-contract'], ['£0.50', 'per-contract'], ['1000', 'no-half'], ['100', 'not-squared']]],
  ['courses/trees/l13-rules-of-thumb', 'screens[7]', 0, [['4.29', true], ['£4.29', true], ['4.3', true], ['8', 'rule'], ['8.00', 'rule'], ['£8.00', 'rule'], ['7.97', 'atm'], ['£7.97', 'atm'], ['7.966', 'atm'], ['7.98', 'atm'], ['7.96', 'atm']]],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (SHOW) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const docs = {};
const load = (f) => docs[f] || (docs[f] = JSON.parse(fs.readFileSync(`app/content/${f}.json`, 'utf8')));
const byId = (d, id) => {
  if (Array.isArray(d)) { for (const v of d) { const r = byId(v, id); if (r) return r; } return null; }
  if (d && typeof d === 'object') { if (d.id === id) return d; for (const v of Object.values(d)) { const r = byId(v, id); if (r) return r; } }
  return null;
};
const byPath = (d, p) => { for (const tok of p.match(/[A-Za-z_]+|\[\d+\]/g)) d = tok[0] === '[' ? d[+tok.slice(1, -1)] : d[tok]; return d; };
for (const [file, where0, part, rows] of TYPED) {
  const node = /\[/.test(where0) ? byPath(load(file), where0) : byId(load(file), where0);
  if (!node) throw new Error('no node ' + file + ' ' + where0);
  const p = part ? node.parts[part - 1] : node, w = p.widget;
  const isExpr = w.kind === 'expression', isSet = Array.isArray(w.answers);
  const grade = isExpr ? expr : isSet ? numSet : num;
  const by = (p.feedback && p.feedback.byKey) || {};
  const where = `${file.replace('courses/', '')} ${where0}${part ? ' part ' + part : ''}`;
  if (isExpr) {
    for (const a of [w.answer, ...(w.accept || [])]) say(grade(w, a) === true, null, `${where}: answer or accept "${a}" grades correct (got ${grade(w, a)})`);
    for (const x of w.wrong || []) { say(grade(w, x.tex) === x.id, null, `${where}: wrong ${x.id} "${x.tex}" lands on its id (got ${grade(w, x.tex)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`); }
  } else {
    const shown = isSet ? w.answers.join(', ') : String(w.unit === '%' ? +(w.answer * 100).toPrecision(10) : w.answer);
    say(grade(w, shown) === true, null, `${where}: answer ${shown} grades correct (got ${grade(w, shown)})`);
    for (const x of w.wrong || []) {
      const t = typeof x.value === 'string' ? x.value : String(w.unit === '%' ? +(x.value * 100).toPrecision(10) : x.value);
      say(grade(w, t) === x.id, null, `${where}: wrong ${x.id} ${t} lands on its id (got ${grade(w, t)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`);
    }
  }
  for (const [typed, want, note] of rows) {
    const got = grade(w, typed);
    say(got === want, note, `${where}: typed "${typed}" -> ${got === true ? 'accepted' : got === null ? 'refused, generic line' : got === 'NOPARSE' ? 'not read (field will not submit)' : 'refused, line "' + got + '"'}; expected ${want === true ? 'accepted' : want === null ? 'generic refusal' : want}`);
  }
}
// PROPOSED (finding 3.1): the two change-of-temperature fields with unit "°C" read every form
for (const [part, forms] of [[2, ['-6.3', '-6.3 °C', '-6.3°C', '-6.3 degrees', '-6.3 degrees C']], [3, ['-0.7', '-0.7 °C', '-0.7°C', '-0.7 degrees']]]) {
  const w = { ...byId(load(N2), 'p-moor-weather').parts[part - 1].widget, unit: '°C' };
  for (const t of forms) say(num(w, t) === true, null, `PROPOSED moor part ${part} with unit °C: typed "${t}" accepted (got ${num(w, t)})`);
}
// PROPOSED (finding 4.3): stat-learning r-test-r2 with key tol 0.0003 and a wrong entry for the model's MSE underneath
{
  const w0 = byId(load('courses/stat-learning/review-2'), 'r-test-r2').widget;
  const w = { ...w0, tol: { abs: 0.0003 }, wrong: [...w0.wrong, { id: 'model-base', value: -0.0217, tol: { abs: 0.00015 } }] };
  for (const [t, want] of [['-0.0222', true], ['-0.022', true], ['-0.02222', true], ['-0.0217', 'model-base'], ['-0.02174', 'model-base'], ['-0.0218', 'model-base'], ['0.0222', 'pos'], ['0.0217', 'flip'], ['-0.02', null], ['-0.0225', true]]) say(num(w, t) === want, null, `PROPOSED r-test-r2: typed "${t}" -> ${num(w, t)}, expected ${want}`);
}
// PROPOSED (finding 4.1): integrals dish part 4 keyed at 15 +- 0.5
{
  const w0 = byPath(load('courses/integrals/problems-4'), 'items[2]').parts[3].widget;
  const w = { ...w0, answer: 15, tol: { abs: 0.5 } };
  for (const [t, want] of [['15', true], ['14.55', true], ['14.6', true], ['14.5', true], ['14', null], ['16', null], ['14.4', null], ['8', 'square-integral'], ['0.07', 'inverse']]) say(num(w, t) === want, null, `PROPOSED dish part 4: typed "${t}" -> ${num(w, t)}, expected ${want}`);
}
// PROPOSED (finding 4.2): numerics l12 with one more wrong entry, `exact-rounded` 0.0523 +- 0.00002
{
  const w0 = byPath(load('courses/numerics/l12-stiff-equations'), 'screens[0]').widget;
  const w = { ...w0, wrong: [...w0.wrong, { id: 'exact-rounded', value: 0.0523, tol: { abs: 0.00002 } }] };
  for (const [t, want] of [['8.24', true], ['5.2253', 'exact'], ['5.225', 'exact'], ['5.23', 'exact-rounded'], ['5.23%', 'exact-rounded'], ['5.2222', 'small'], ['5.222', 'small'], ['5.22', null], ['5.24', null]]) say(num(w, t) === want, null, `PROPOSED l12: typed "${t}" -> ${num(w, t)}, expected ${want}`);
}
console.log(`grade: ${checks} checks, ${fails} failures, ${findings} FINDING rows (recorded in the review)`);
process.exit(fails ? 1 : 0);
