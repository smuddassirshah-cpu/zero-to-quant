#!/usr/bin/env node
/* Delta read, fix passes of problems 1.3 a and b: what the engine's own graders do with the changed parts.
   Pattern: docs/reviews/problems-1.3-b-scripts/grade-check.mjs (same loader, same grading steps as numeric.js and expression.js).
   For every part of the 17 changed items: the answer and each accept[] form grade correct, each wrong[] entry grades to its own id.
   TYPED rows: [course, set, item, part, typed, expected, note?]; expected is true (accepted), false (refused, any line) or the wrong[] id
   the typed value should be given. A row with a note is one the reader records as a finding: it prints as FINDING and does not fail.

   node docs/reviews/delta-problems-1.3-ab-scripts/grade.mjs --local-cdn <pkgs>      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = {}; vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

const L = 'limits', I = 'integrals', T = 'taylor', M = 'multivar';
const ITEMS = [[L, 2, 'p-perpetuity-slope'], [L, 2, 'p-inventory-penalty'], [L, 3, 'p-relative-strength'], [I, 1, 'p-falling-parabola'], [I, 2, 'p-turnover-decay'],
  [I, 3, 'p-order-size-tail'], [I, 3, 'p-time-to-fill'], [I, 3, 'p-log-return'], [I, 3, 'p-signal-average'], [T, 1, 'p-cube-root-27'], [T, 1, 'p-newton-cubic'],
  [T, 1, 'p-loss-limit'], [T, 1, 'p-loan-rate'], [T, 3, 'p-two-months'], [T, 3, 'p-tail-bound'], [M, 2, 'p-two-book-risk'], [M, 3, 'p-min-variance-pair']];
const EDGE = 'the accept line prints this value as inside the band';
const TYPED = [
  // limits 2: the penny route and the 4-place route
  [L, 2, 'p-perpetuity-slope', 2, '-2041', true], [L, 2, 'p-perpetuity-slope', 2, '-2040', true], [L, 2, 'p-perpetuity-slope', 2, '-2040.82', true],
  [L, 2, 'p-perpetuity-slope', 2, '-2,041', true], [L, 2, 'p-perpetuity-slope', 2, '-2042', false], [L, 2, 'p-perpetuity-slope', 2, '-2039', false],
  [L, 2, 'p-perpetuity-slope', 2, '2041', 'sign'], [L, 2, 'p-perpetuity-slope', 2, '2040', 'sign'], [L, 2, 'p-perpetuity-slope', 2, '2.04', 'no-divide'],
  [L, 2, 'p-perpetuity-slope', 2, '2', 'no-divide'], [L, 2, 'p-perpetuity-slope', 2, '-2000', false], [L, 2, 'p-perpetuity-slope', 2, '-2500', false],
  [L, 2, 'p-inventory-penalty', 1, '4+\\frac{1}{2}h', true], [L, 2, 'p-inventory-penalty', 1, '\\frac{h}{2}+4', true],
  // limits 3
  [L, 3, 'p-relative-strength', 1, '2.1', true], [L, 3, 'p-relative-strength', 1, '2.10', true], [L, 3, 'p-relative-strength', 1, '21/10', true],
  [L, 3, 'p-relative-strength', 1, '30', 'no-chain'], [L, 3, 'p-relative-strength', 1, '0.07', 'no-thirty'], [L, 3, 'p-relative-strength', 1, '2.4', false],
  [L, 3, 'p-relative-strength', 2, '0.0004', true], [L, 3, 'p-relative-strength', 2, '1/2500', true], [L, 3, 'p-relative-strength', 2, '-0.0004', 'swapped'],
  [L, 3, 'p-relative-strength', 2, '0.6', 'no-square'], [L, 3, 'p-relative-strength', 2, '0.028', 'rates'], [L, 3, 'p-relative-strength', 2, '0.019', 'no-chain'],
  [L, 3, 'p-relative-strength', 2, '0.0192', false],
  [L, 3, 'p-relative-strength', 3, '2', true], [L, 3, 'p-relative-strength', 3, '2%', true], [L, 3, 'p-relative-strength', 3, '2.0', true],
  [L, 3, 'p-relative-strength', 3, '0.02', 'decimal'], [L, 3, 'p-relative-strength', 3, '0.020', 'decimal'], [L, 3, 'p-relative-strength', 3, '12', 'added'],
  [L, 3, 'p-relative-strength', 3, '7', 'share-only'], [L, 3, 'p-relative-strength', 3, '0.04', 'raw'], [L, 3, 'p-relative-strength', 3, '0.03', false],
  [L, 3, 'p-relative-strength', 3, '0.0004', false],
  // integrals 1
  [I, 1, 'p-falling-parabola', 1, '12.75', true], [I, 1, 'p-falling-parabola', 1, '51/4', true], [I, 1, 'p-falling-parabola', 1, '18.75', 'left-ends'],
  [I, 1, 'p-falling-parabola', 1, '25.5', 'no-width'], [I, 1, 'p-falling-parabola', 1, '15.625', false],
  [I, 1, 'p-falling-parabola', 2, '18.75', true], [I, 1, 'p-falling-parabola', 2, '6.75', 'subtracted'], [I, 1, 'p-falling-parabola', 2, '15.75', 'no-length'],
  [I, 1, 'p-falling-parabola', 3, '240', true], [I, 1, 'p-falling-parabola', 3, '241', 'strict'], [I, 1, 'p-falling-parabola', 3, '120', 'no-length'],
  [I, 1, 'p-falling-parabola', 3, '239', false],
  [I, 1, 'p-falling-parabola', 4, '16-\\frac{12}{n}-\\frac{4}{n^{2}}', true], [I, 1, 'p-falling-parabola', 4, '\\frac{4(n-1)(4n+1)}{n^2}', true],
  [I, 1, 'p-falling-parabola', 4, '\\frac{4\\left(4n^2-3n-1\\right)}{n^2}', true], [I, 1, 'p-falling-parabola', 4, '24-\\frac{8n^2+12n+4}{n^2}', true],
  [I, 1, 'p-falling-parabola', 4, '16', false], [I, 1, 'p-falling-parabola', 4, '16-\\frac{12}{n}', false], [I, 1, 'p-falling-parabola', 4, '16+\\frac{12}{n}-\\frac{4}{n^2}', 'left-ends'],
  [I, 1, 'p-falling-parabola', 4, '4-\\frac{12}{n}-\\frac{4}{n^2}', 'once'], [I, 1, 'p-falling-parabola', 4, '8n-6-\\frac{2}{n}', 'no-width'],
  [I, 1, 'p-falling-parabola', 4, '18-\\frac{27}{2n}-\\frac{9}{2n^2}', false],
  [I, 1, 'p-falling-parabola', 5, '16', true], [I, 1, 'p-falling-parabola', 5, '24', 'no-squares'], [I, 1, 'p-falling-parabola', 5, '12.75', 'stopped'],
  [I, 1, 'p-falling-parabola', 5, '4', 'once'], [I, 1, 'p-falling-parabola', 5, '18', false],
  // integrals 2 and 3: the widened bands and the accept lines
  [I, 2, 'p-turnover-decay', 3, '13.83', true], [I, 2, 'p-turnover-decay', 3, '13.84', true], [I, 2, 'p-turnover-decay', 3, '13.8352', true],
  [I, 2, 'p-turnover-decay', 3, '13.82', false, EDGE], [I, 2, 'p-turnover-decay', 3, '13.85', false], [I, 2, 'p-turnover-decay', 3, '-2.17', 'no-c'],
  [I, 2, 'p-turnover-decay', 3, '3.46', 'times-k'], [I, 2, 'p-turnover-decay', 3, '1.08', 'rate'],
  [I, 2, 'p-turnover-decay', 4, '2.77', true], [I, 2, 'p-turnover-decay', 4, '2.775', true], [I, 2, 'p-turnover-decay', 4, '2.765', false, EDGE],
  [I, 3, 'p-order-size-tail', 4, '9.95', true], [I, 3, 'p-order-size-tail', 4, '9.945', true], [I, 3, 'p-order-size-tail', 4, '9.955', false, EDGE], [I, 3, 'p-order-size-tail', 4, '10', 'drop-one'],
  [I, 3, 'p-time-to-fill', 2, '0.406', true], [I, 3, 'p-time-to-fill', 2, '0.4065', true], [I, 3, 'p-time-to-fill', 2, '0.4055', false, EDGE],
  [I, 3, 'p-log-return', 1, '-0.0719', true], [I, 3, 'p-log-return', 1, '-0.0720', true], [I, 3, 'p-log-return', 1, '-0.07195', true],
  [I, 3, 'p-log-return', 1, '-0.0718', false, EDGE], [I, 3, 'p-log-return', 1, '-0.0721', false], [I, 3, 'p-log-return', 1, '-0.1438', 'full-ends'],
  [I, 3, 'p-log-return', 1, '-0.0323', 'midpoint'], [I, 3, 'p-log-return', 1, '-0.1733', 'lost-strip'],
  [I, 3, 'p-signal-average', 2, '3.459', true], [I, 3, 'p-signal-average', 2, '3.4585', true], [I, 3, 'p-signal-average', 2, '3.4595', false, EDGE],
  [I, 3, 'p-signal-average', 3, '0.865', true], [I, 3, 'p-signal-average', 3, '0.8645', true], [I, 3, 'p-signal-average', 3, '0.8655', false, EDGE],
  [I, 3, 'p-signal-average', 4, '2.967', true], [I, 3, 'p-signal-average', 4, '2.968', true], [I, 3, 'p-signal-average', 4, '2.9676', true],
  [I, 3, 'p-signal-average', 4, '2.966', false, EDGE], [I, 3, 'p-signal-average', 4, '2.969', false], [I, 3, 'p-signal-average', 4, '3.509', 'full-ends'],
  [I, 3, 'p-signal-average', 4, '1.484', 'no-h'], [I, 3, 'p-signal-average', 4, '3.713', 'midpoint'],
  // taylor 1: the fourth root
  [T, 1, 'p-cube-root-27', 1, '\\frac{x}{32}+\\frac{3}{2}', true], [T, 1, 'p-cube-root-27', 1, '\\frac{x+48}{32}', true], [T, 1, 'p-cube-root-27', 1, '2+0.03125(x-16)', true],
  [T, 1, 'p-cube-root-27', 1, '2+\\frac{1}{32}\\left(x-16\\right)', true], [T, 1, 'p-cube-root-27', 1, '2+\\frac{x-16}{8}', 'slope-eighth'],
  [T, 1, 'p-cube-root-27', 1, '\\frac{x}{8}', 'slope-eighth'], [T, 1, 'p-cube-root-27', 1, '2+\\frac{x-16}{4}', 'slope-quarter'], [T, 1, 'p-cube-root-27', 1, '3+\\frac{x-27}{27}', false],
  [T, 1, 'p-cube-root-27', 1, '2+\\frac{0.32}{32}', false], [T, 1, 'p-cube-root-27', 1, '2.01', false],
  [T, 1, 'p-cube-root-27', 2, '2.01', true], [T, 1, 'p-cube-root-27', 2, '2.0100', true], [T, 1, 'p-cube-root-27', 2, '2.04', 'eighth'], [T, 1, 'p-cube-root-27', 2, '2.08', 'quarter'],
  [T, 1, 'p-cube-root-27', 2, '2.51', 'whole-x'], [T, 1, 'p-cube-root-27', 2, '2.0099', false],
  [T, 1, 'p-cube-root-27', 3, '-0.000075', true], [T, 1, 'p-cube-root-27', 3, '-0.00015', 'no-half'], [T, 1, 'p-cube-root-27', 3, '-0.000150', 'no-half'],
  [T, 1, 'p-cube-root-27', 3, '-0.000234', 'h-not-squared'], [T, 1, 'p-cube-root-27', 3, '0.000075', 'sign'], [T, 1, 'p-cube-root-27', 3, '-0.000074', false],
  [T, 1, 'p-cube-root-27', 3, '-0.0003', false],
  [T, 1, 'p-cube-root-27', 4, '2.009925', true], [T, 1, 'p-cube-root-27', 4, '2.010075', 'sign'], [T, 1, 'p-cube-root-27', 4, '2.00985', 'no-half'],
  [T, 1, 'p-cube-root-27', 4, '2.039925', 'eighth-carried'], [T, 1, 'p-cube-root-27', 4, '2.009926', false], [T, 1, 'p-cube-root-27', 4, '2.01', false],
  [T, 1, 'p-loss-limit', 3, '1418', true], [T, 1, 'p-loss-limit', 3, '1417.72', true], [T, 1, 'p-loss-limit', 3, '0.0354', 'one-lot'], [T, 1, 'p-loss-limit', 3, '0.04', 'one-lot'],
  [T, 1, 'p-loss-limit', 3, '0.035', 'one-lot'], [T, 1, 'p-loss-limit', 3, '0.35', false], [T, 1, 'p-loss-limit', 3, '0.14', false],
  [T, 1, 'p-loss-limit', 3, '0', false],
  [T, 1, 'p-loss-limit', 2, '-354.43', true], [T, 1, 'p-loan-rate', 2, '-18880.40', true],
  // taylor 3
  [T, 3, 'p-two-months', 2, '17.1', true], [T, 3, 'p-two-months', 2, '17.07', true], [T, 3, 'p-two-months', 2, '0.0001707', 'unscaled'], [T, 3, 'p-two-months', 2, '0.000171', 'unscaled'],
  [T, 3, 'p-two-months', 2, '0.00017', 'unscaled'], [T, 3, 'p-two-months', 2, '0.0000853', false], [T, 3, 'p-two-months', 2, '0.000512', false], [T, 3, 'p-two-months', 2, '0.0032', false],
  [T, 3, 'p-two-months', 2, '8.5', 'factorial'], [T, 3, 'p-two-months', 2, '16.1', false],
  [T, 3, 'p-two-months', 4, '4.86', true], [T, 3, 'p-two-months', 4, '4.85', true], [T, 3, 'p-two-months', 4, '4.854', true], [T, 3, 'p-two-months', 4, '4.87', true],
  [T, 3, 'p-two-months', 4, '4.84', false], [T, 3, 'p-two-months', 4, '4.17', 'wrong-end'], [T, 3, 'p-two-months', 4, '14.58', 'two-factorial'], [T, 3, 'p-two-months', 4, '2.08', 'no-m'],
  [T, 3, 'p-two-months', 4, '0.0000486', 'unscaled'], [T, 3, 'p-two-months', 4, '0.000049', 'unscaled'], [T, 3, 'p-two-months', 4, '0.0000485', 'unscaled'],
  [T, 3, 'p-two-months', 4, '0.0000417', false], [T, 3, 'p-two-months', 4, '0.0001458', false], [T, 3, 'p-two-months', 4, '4.33', false],
  [T, 3, 'p-two-months', 5, '21.9', true], [T, 3, 'p-two-months', 5, '21.93', true], [T, 3, 'p-two-months', 5, '17.1', 'first-only'], [T, 3, 'p-two-months', 5, '12.2', 'subtracted'],
  [T, 3, 'p-two-months', 5, '21.2', 'wrong-end'], [T, 3, 'p-two-months', 5, '0.000219', 'unscaled'], [T, 3, 'p-two-months', 5, '0.00022', 'unscaled'],
  [T, 3, 'p-two-months', 5, '0.0001221', false], [T, 3, 'p-two-months', 5, '0.0001707', false], [T, 3, 'p-two-months', 5, '11.8', false],
  [T, 3, 'p-tail-bound', 4, '11.59', true], [T, 3, 'p-tail-bound', 4, '11.60', true], [T, 3, 'p-tail-bound', 4, '11.6', true], [T, 3, 'p-tail-bound', 4, '11.598', true],
  [T, 3, 'p-tail-bound', 4, '11.58', false], [T, 3, 'p-tail-bound', 4, '11.61', false], [T, 3, 'p-tail-bound', 4, '10.67', 'first-term'], [T, 3, 'p-tail-bound', 4, '11.85', 'over-four'],
  [T, 3, 'p-tail-bound', 4, '16', 'lagrange'], [T, 3, 'p-tail-bound', 4, '0.0011594', 'unscaled'], [T, 3, 'p-tail-bound', 4, '0.00116', 'unscaled'],
  [T, 3, 'p-tail-bound', 4, '0.0010667', false], [T, 3, 'p-tail-bound', 4, '0.0016', false], [T, 3, 'p-tail-bound', 4, '0.0011852', false],
  // multivar 3
  [M, 3, 'p-min-variance-pair', 1, '0.1625w^2-0.065w+0.0625', true], [M, 3, 'p-min-variance-pair', 1, '\\frac{13}{80}w^2-\\frac{13}{200}w+\\frac{1}{16}', true],
  [M, 3, 'p-min-variance-pair', 1, '0.0625-0.065w+0.1625w^2', true], [M, 3, 'p-min-variance-pair', 1, '0.16w^2+0.0625(1-w)^2+0.06w(1-w)', 'form'],
  [M, 3, 'p-min-variance-pair', 1, '0.2225w^2-0.125w+0.0625', 'no-cross'], [M, 3, 'p-min-variance-pair', 1, '0.1925w^2-0.095w+0.0625', 'half-cross'],
  [M, 3, 'p-min-variance-pair', 1, '0.1w^2-0.05w+0.04', false], [M, 3, 'p-min-variance-pair', 1, '0.1625w^2+0.065w+0.0625', false],
  [M, 3, 'p-min-variance-pair', 2, '0.2', true], [M, 3, 'p-min-variance-pair', 2, '1/5', true], [M, 3, 'p-min-variance-pair', 2, '0.4', 'no-two'], [M, 3, 'p-min-variance-pair', 2, '0.8', 'gave-b'],
  [M, 3, 'p-min-variance-pair', 2, '0.2809', 'carried'], [M, 3, 'p-min-variance-pair', 2, '0.281', 'carried'], [M, 3, 'p-min-variance-pair', 2, '0.25', false],
  [M, 3, 'p-min-variance-pair', 3, '0.2366', true], [M, 3, 'p-min-variance-pair', 3, '0.056', 'variance'], [M, 3, 'p-min-variance-pair', 3, '0.28', 'weighted'],
  [M, 3, 'p-min-variance-pair', 3, '0.25', 'carried-half'], [M, 3, 'p-min-variance-pair', 3, '0.237', false], [M, 3, 'p-min-variance-pair', 3, '23.66', false],
  [M, 3, 'p-min-variance-pair', 4, '0.112', true], [M, 3, 'p-min-variance-pair', 4, '0.056', 'variance'], [M, 3, 'p-min-variance-pair', 4, '0.064', 'no-cross'], [M, 3, 'p-min-variance-pair', 4, '0.0675', false],
  [M, 3, 'p-min-variance-pair', 5, '0.05824', true], [M, 3, 'p-min-variance-pair', 5, '0.0582', true], [M, 3, 'p-min-variance-pair', 5, '0.0583', true], [M, 3, 'p-min-variance-pair', 5, '0.05826', true],
  [M, 3, 'p-min-variance-pair', 5, '0.05712', 'sigma-lambda'], [M, 3, 'p-min-variance-pair', 5, '0.0571', 'sigma-lambda'], [M, 3, 'p-min-variance-pair', 5, '0.056', 'no-change'],
  [M, 3, 'p-min-variance-pair', 5, '0.168', 'whole-lambda'], [M, 3, 'p-min-variance-pair', 5, '0.058', false], [M, 3, 'p-min-variance-pair', 5, '0.0584', false],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (finding) { findings++; console.log((ok ? 'FINDING ' : 'FAIL    ') + msg + '   [' + finding + ']'); if (!ok) fails++; return; } if (!ok) { fails++; console.log('FAIL    ' + msg); } };

const gradeNumeric = (w, text) => {
  let v = G.parseNum(text);
  if (w.unit === '%' && !text.includes('%')) v = v / 100;
  if (!Number.isFinite(v)) return null;
  if (G.within(v, +w.answer, w.tol)) return true;
  const m = G.matchWrong(v, w.wrong, { abs: 1e-9 });
  return m ? m.id : null;
};
const head = (j) => (Array.isArray(j) ? j[0] : null);
const args = (j) => (Array.isArray(j) ? j.slice(1) : []);
const hasSum = (j) => head(j) === 'Add' || head(j) === 'Subtract' || args(j).some(hasSum);
const isSumLike = (j) => head(j) === 'Add' || head(j) === 'Subtract';
const gradeExpr = (w, Lx) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, Lx, t, fo); } catch { return false; } };
  if ([w.answer, ...(w.accept || [])].some(eq)) {
    if (w.form === 'expanded') { let ok = true; try { ok = G.withParsed(ce, Lx, fo.functions, (e) => (isSumLike(e.json) ? args(e.json).every((t) => !hasSum(t)) : !hasSum(e.json))); } catch { ok = true; } return ok ? true : 'form'; }
    return true;
  }
  const x = (w.wrong || []).find((y) => y.tex && eq(y.tex));
  return x ? x.id : null;
};

const used = new Set();
for (const [course, n, id] of ITEMS) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  const it = set.items.find((x) => x.id === id);
  it.parts.forEach((p, i) => {
    const w = p.widget, where = `${course} ${n} ${id} part ${i + 1}`;
    const typed = TYPED.filter((r) => r[0] === course && r[1] === n && r[2] === id && r[3] === i + 1);
    typed.forEach((r) => used.add(r));
    const judge = (grade) => {
      for (const r of typed) {
        const got = grade(w, r[4]);
        const ok = r[5] === false ? got !== true : got === r[5];
        say(ok, r[6], `${where}: typed "${r[4]}" -> ${JSON.stringify(got)}, expected ${JSON.stringify(r[5])}`);
      }
    };
    if (w.kind === 'numeric' && !G.isSetSpec(w)) {
      say(G.within(+w.answer, +w.answer, w.tol), null, `${where}: answer outside its own band`);
      for (const x of w.wrong || []) say(!G.within(+x.value, +w.answer, w.tol), null, `${where}: wrong "${x.id}" = ${x.value} is inside the answer band`);
      (w.wrong || []).forEach((x) => { const m = G.matchWrong(+x.value, w.wrong, { abs: 1e-9 }); say(m === x, null, `${where}: wrong "${x.id}" = ${x.value} is caught first by "${m && m.id}"`); });
      judge(gradeNumeric);
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer) === true, null, `${where}: answer does not grade correct`);
      for (const a of w.accept || []) say(gradeExpr(w, a) === true, null, `${where}: accept "${a}" does not grade correct`);
      for (const x of w.wrong || []) say(gradeExpr(w, x.tex) === x.id, null, `${where}: wrong "${x.id}" ${x.tex} grades ${gradeExpr(w, x.tex)}`);
      judge(gradeExpr);
    }
  });
}
for (const r of TYPED) if (!used.has(r)) { fails++; console.log('FAIL    row not used: ' + r.slice(0, 5).join(' ')); }
console.log(`grade.mjs: ${checks} checks, ${fails} failures, ${findings} finding rows`);
process.exit(fails ? 1 : 0);
