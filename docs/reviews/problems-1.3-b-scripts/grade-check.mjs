#!/usr/bin/env node
/* Second read, problems 1.3 (b): what the engine's own graders do with each part of the taylor and multivar sets 1 to 3.
   Pattern: docs/reviews/problems-1.3-a-scripts/grade-check.mjs. Loads app/js/engine/grade.js and the local Compute Engine, then per part:
     numeric     the answer and every typed string in TYPED is graded as numeric.js grades it (parseNum, within, numSetGrade, then matchWrong
                 in listed order with each entry's own tol); each wrong[] value must fall outside the answer's band
     expression  the answer, every accept[] form and every typed string is graded as expression.js grades it (exprEqual, then the
                 "expanded" shape); each wrong[].tex must not grade correct
   TYPED rows: [course, set, item, part, typed, expected, finding?]. `expected` is true (accepted), false (refused) or a string, the wrong[]
   key the reader expects the typed value to be given. A row with a `finding` text is one the reader holds to be a content fault: it prints
   as FINDING and does not fail the run. Any other mismatch prints FAIL and the exit code is 1.

   node docs/reviews/problems-1.3-b-scripts/grade-check.mjs --local-cdn <pkgs>      (from the repo root) */
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

const T = 'taylor', M = 'multivar';
const TYPED = [
  // taylor 1
  [T, 1, 'p-cube-root-27', 1, '\\frac{x}{27}+2', true], [T, 1, 'p-cube-root-27', 1, '\\frac{x+54}{27}', true], [T, 1, 'p-cube-root-27', 1, '3+\\frac{1}{27}\\left(x-27\\right)', true],
  [T, 1, 'p-cube-root-27', 1, '3+\\frac{0.81}{27}', false], [T, 1, 'p-cube-root-27', 1, '3+\\frac{x-27}{9}', 'slope-ninth'],
  [T, 1, 'p-cube-root-27', 2, '3.03', true], [T, 1, 'p-cube-root-27', 2, '3.0300', true],
  [T, 1, 'p-cube-root-27', 3, '-0.0003', true], [T, 1, 'p-cube-root-27', 3, '-0.00030', true], [T, 1, 'p-cube-root-27', 3, '-0.00037', 'h-not-squared'],
  [T, 1, 'p-cube-root-27', 4, '3.0297', true], [T, 1, 'p-cube-root-27', 4, '3.03', false],
  [T, 1, 'p-newton-cubic', 1, '1.25', true], [T, 1, 'p-newton-cubic', 1, '5/4', true],
  [T, 1, 'p-newton-cubic', 2, '1.2143', true], [T, 1, 'p-newton-cubic', 2, '17/14', true],
  [T, 1, 'p-newton-cubic', 4, '1.213412', true], [T, 1, 'p-newton-cubic', 4, '1.213411', false], [T, 1, 'p-newton-cubic', 4, '1.2134121', true],
  [T, 1, 'p-loss-limit', 1, '96.37', true], [T, 1, 'p-loss-limit', 1, '£96.37', true], [T, 1, 'p-loss-limit', 2, '-354.43', true],
  [T, 1, 'p-loss-limit', 3, '1418', true], [T, 1, 'p-loss-limit', 3, '1417.72', true], [T, 1, 'p-loss-limit', 3, '£1,418', true], [T, 1, 'p-loss-limit', 3, '1417', true],
  [T, 1, 'p-loss-limit', 4, '35.3', true], [T, 1, 'p-loss-limit', 4, '35.27', true], [T, 1, 'p-loss-limit', 4, '35.2', false],
  [T, 1, 'p-loan-rate', 1, '10076.02', true], [T, 1, 'p-loan-rate', 1, '10,076.02', true],
  [T, 1, 'p-loan-rate', 2, '-18880.40', true], [T, 1, 'p-loan-rate', 2, '-18,880.4', true],
  [T, 1, 'p-loan-rate', 3, '1.874', true], [T, 1, 'p-loan-rate', 4, '0.05403', true], [T, 1, 'p-loan-rate', 4, '0.054026', true],
  [T, 1, 'p-loan-rate', 5, '0.054052', true], [T, 1, 'p-loan-rate', 5, '0.054051', false],
  // taylor 2
  [T, 2, 'p-three-halves', 2, '3/16', true], [T, 2, 'p-three-halves', 2, '0.1875', true],
  [T, 2, 'p-three-halves', 4, '-1/128', true], [T, 2, 'p-three-halves', 4, '-0.00781', true],
  [T, 2, 'p-three-halves', 5, '9.2295', true], [T, 2, 'p-three-halves', 5, '9.23', false],
  [T, 2, 'p-square-geometric', 3, 'k+1', true], [T, 2, 'p-square-geometric', 3, '1+k', true], [T, 2, 'p-square-geometric', 3, 'k', 'k-only'],
  [T, 2, 'p-square-geometric', 3, '\\frac{1}{k+1}', 'reciprocal'], [T, 2, 'p-square-geometric', 3, '(k+1)!', 'no-factorial'],
  [T, 2, 'p-square-geometric', 5, '1.234', true], [T, 2, 'p-square-geometric', 5, '1.2340', true], [T, 2, 'p-square-geometric', 5, '1.2346', false],
  [T, 2, 'p-eight-coupon', 1, '103.39', true], [T, 2, 'p-eight-coupon', 2, '1557.43', true], [T, 2, 'p-eight-coupon', 2, '1,557.43', true],
  [T, 2, 'p-eight-coupon', 3, '15.06', true], [T, 2, 'p-eight-coupon', 4, '98.19', true], [T, 2, 'p-eight-coupon', 5, '98.37', true],
  [T, 2, 'p-eight-coupon', 5, '98.36', false],
  [T, 2, 'p-log-two', 2, '0.6885', true], [T, 2, 'p-log-two', 2, '0.68854', true], [T, 2, 'p-log-two', 2, '0.6931', false],
  [T, 2, 'p-log-two', 3, '-1/8', true], [T, 2, 'p-log-two', 3, '-0.125', true], [T, 2, 'p-log-two', 4, '1/24', true], [T, 2, 'p-log-two', 4, '0.0417', true],
  [T, 2, 'p-log-two', 5, '0.73733', true], [T, 2, 'p-log-two', 5, '0.74194', false],
  // taylor 3
  [T, 3, 'p-doubling-coefficients', 1, '1.28', true], [T, 3, 'p-doubling-coefficients', 1, '32/25', true],
  [T, 3, 'p-doubling-coefficients', 3, '1/2', true], [T, 3, 'p-doubling-coefficients', 3, '0.5', true],
  [T, 3, 'p-two-months', 1, '0.0768', true],
  [T, 3, 'p-two-months', 2, '17.1', true], [T, 3, 'p-two-months', 2, '17.07', true], [T, 3, 'p-two-months', 2, '17.0', false],
  [T, 3, 'p-two-months', 2, '0.000171', 'unscaled'], [T, 3, 'p-two-months', 2, '0.0001707', 'unscaled'],
  [T, 3, 'p-two-months', 2, '0.0000853', null, 'the 3! slip typed unscaled is told "That is the bound itself ... so type 17.1"'],
  [T, 3, 'p-two-months', 2, '0.000512', null, 'r^3 typed unscaled is told "That is the bound itself ... so type 17.1"'],
  [T, 3, 'p-two-months', 2, '0.0032', null, 'the last kept term typed unscaled is told "That is the bound itself ... so type 17.1"'],
  [T, 3, 'p-two-months', 3, '-0.05125', true],
  [T, 3, 'p-two-months', 4, '4.86', true], [T, 3, 'p-two-months', 4, '4.8598', true],
  [T, 3, 'p-two-months', 4, '4.85', true, 'with M kept as 2.33: 2.33 * 0.000125 / 6 = 4.854e-5'],
  [T, 3, 'p-two-months', 4, '0.0000417', null, 'the M = 2 slip typed unscaled is told "That is the bound itself ... so type 4.86"'],
  [T, 3, 'p-two-months', 4, '0.0000486', 'unscaled'],
  [T, 3, 'p-two-months', 5, '21.9', true], [T, 3, 'p-two-months', 5, '21.93', true],
  [T, 3, 'p-two-months', 5, '0.0001221', null, 'the subtracted bounds typed unscaled are told "That is the bound itself ... so type 21.9"'],
  [T, 3, 'p-tail-bound', 1, '1.49067', true], [T, 3, 'p-tail-bound', 2, '0.0016', true], [T, 3, 'p-tail-bound', 2, '0.00160', true],
  [T, 3, 'p-tail-bound', 3, '0.08', true], [T, 3, 'p-tail-bound', 3, '2/25', true],
  [T, 3, 'p-tail-bound', 4, '11.59', true], [T, 3, 'p-tail-bound', 4, '11.594', true], [T, 3, 'p-tail-bound', 4, '11.58', false],
  [T, 3, 'p-tail-bound', 4, '11.60', true, 'from a_4 = 10.67 (the part\'s own first-term entry) or 0.001067 (part 2\'s explanation): 10.67 / 0.92 = 11.598'],
  [T, 3, 'p-tail-bound', 4, '0.0016', null, 'the Lagrange bound typed unscaled is told "That is the bound itself ... so type 11.59"'],
  [T, 3, 'p-tail-bound', 4, '0.0010667', null, 'a_4 typed unscaled is told "That is the bound itself ... so type 11.59"'],
  [T, 3, 'p-tail-bound', 5, '1.49183', true], [T, 3, 'p-tail-bound', 5, '1.49182', false],
  [T, 3, 'p-big-gain', 1, '1.8', true], [T, 3, 'p-big-gain', 2, '0.33493', true],
  [T, 3, 'p-big-gain', 3, '0.00205', true], [T, 3, 'p-big-gain', 3, '0.002048', true],
  [T, 3, 'p-big-gain', 4, '1.0281', true], [T, 3, 'p-big-gain', 4, '1.02808', true], [T, 3, 'p-big-gain', 4, '1.0296', false],
  // multivar 1
  [M, 1, 'p-stretched-bowl', 2, '\\left(18,6\\right)', true], [M, 1, 'p-stretched-bowl', 2, '(18, 6)', true], [M, 1, 'p-stretched-bowl', 2, '(6,18)', 'swapped'],
  [M, 1, 'p-stretched-bowl', 3, '-0.03', true], [M, 1, 'p-stretched-bowl', 3, '-0.0300', true], [M, 1, 'p-stretched-bowl', 3, '-0.0303', true],
  [M, 1, 'p-stretched-bowl', 4, '-0.0303', true], [M, 1, 'p-stretched-bowl', 4, '-0.03031', true], [M, 1, 'p-stretched-bowl', 4, '-0.03', 'linear'],
  [M, 1, 'p-mixed-both-ways', 1, '3x^2y-2y^2', true], [M, 1, 'p-mixed-both-ways', 1, '3yx^2-2y^2', true], [M, 1, 'p-mixed-both-ways', 1, 'y\\left(3x^2-2y\\right)', true],
  [M, 1, 'p-mixed-both-ways', 2, '-4y+3x^2', true], [M, 1, 'p-mixed-both-ways', 2, '3x^2-4y-4x', 'carried-both'],
  [M, 1, 'p-mixed-both-ways', 5, '10.8', true], [M, 1, 'p-mixed-both-ways', 5, '10.78', true],
  [M, 1, 'p-dollar-holding', 4, '-\\frac{2000}{X^2}', true], [M, 1, 'p-dollar-holding', 4, '\\frac{-2000}{X^{2}}', true], [M, 1, 'p-dollar-holding', 4, '-2000X^{-2}', true],
  [M, 1, 'p-dollar-holding', 4, '-1280', false], [M, 1, 'p-dollar-holding', 4, '-\\frac{2000P}{X^2}', 'gave-vx'],
  [M, 1, 'p-dollar-holding', 5, '-12.8', true], [M, 1, 'p-dollar-holding', 5, '-12.80', true],
  // multivar 2
  [M, 2, 'p-slopes-around', 1, '\\left(12,9\\right)', true], [M, 2, 'p-slopes-around', 3, '-4.2', true], [M, 2, 'p-slopes-around', 3, '-21/5', true],
  [M, 2, 'p-slopes-around', 4, '\\left(0.6,-0.8\\right)', true], [M, 2, 'p-slopes-around', 4, '(\\frac{3}{5},-\\frac{4}{5})', true],
  [M, 2, 'p-slopes-around', 4, '(-0.6,0.8)', 'other-way'], [M, 2, 'p-slopes-around', 4, '(9,-12)', 'not-unit'], [M, 2, 'p-slopes-around', 4, '(3,-4)', false],
  [M, 2, 'p-two-book-risk', 1, '\\left(0.6,0.8\\right)', true], [M, 2, 'p-two-book-risk', 1, '\\left(\\frac{3}{5},\\frac{4}{5}\\right)', true],
  [M, 2, 'p-two-book-risk', 2, '\\frac{3}{5}x+\\frac{4}{5}y', true], [M, 2, 'p-two-book-risk', 2, '5+0.6\\left(x-3\\right)+0.8\\left(y-4\\right)', true],
  [M, 2, 'p-two-book-risk', 2, '0.8y+0.6x', true], [M, 2, 'p-two-book-risk', 2, '5+0.6x+0.8y', 'no-shift'],
  [M, 2, 'p-two-book-risk', 3, '4.88', true], [M, 2, 'p-two-book-risk', 3, '4.89', 'exact'], [M, 2, 'p-two-book-risk', 3, '4.9', 'unit-slopes'],
  [M, 2, 'p-two-book-risk', 4, '0.0118', true], [M, 2, 'p-two-book-risk', 4, '0.01183', true], [M, 2, 'p-two-book-risk', 4, '0.012', false],
  [M, 2, 'p-two-book-risk', 5, '0.0030', true], [M, 2, 'p-two-book-risk', 5, '0.003', true], [M, 2, 'p-two-book-risk', 5, '0.00295', true], [M, 2, 'p-two-book-risk', 5, '0.0029', true],
  [M, 2, 'p-fit-descent', 1, '\\left(-8,4\\right)', true], [M, 2, 'p-fit-descent', 2, '\\left(0.8,-0.4\\right)', true], [M, 2, 'p-fit-descent', 2, '(4/5,-2/5)', true],
  [M, 2, 'p-fit-descent', 3, '-0.72', true], [M, 2, 'p-fit-descent', 4, '0.25', true], [M, 2, 'p-fit-descent', 4, '1/4', true], [M, 2, 'p-fit-descent', 5, '24', true],
  // multivar 3
  [M, 3, 'p-two-level-points', 1, '0, 1', true], [M, 3, 'p-two-level-points', 1, '1,0', true], [M, 3, 'p-two-level-points', 1, 'x = 0 or x = 1', true],
  [M, 3, 'p-two-level-points', 1, '1', false], [M, 3, 'p-two-level-points', 1, '0, -1', false],
  [M, 3, 'p-two-level-points', 2, '36\\left(2x-1\\right)', true], [M, 3, 'p-two-level-points', 2, '12x\\cdot6-36', true], [M, 3, 'p-two-level-points', 2, '72x', 'no-mixed'],
  [M, 3, 'p-capital-limit', 1, '\\left(7,3\\right)', true], [M, 3, 'p-capital-limit', 1, '(3,7)', 'swapped'],
  [M, 3, 'p-capital-limit', 5, '52', true], [M, 3, 'p-capital-limit', 5, '51.875', true], [M, 3, 'p-capital-limit', 5, '51.88', true], [M, 3, 'p-capital-limit', 5, '51.9', true],
  [M, 3, 'p-min-variance-pair', 1, '0.1w^2-0.05w+0.04', true], [M, 3, 'p-min-variance-pair', 1, '0.04-0.05w+0.1w^2', true],
  [M, 3, 'p-min-variance-pair', 1, '\\frac{1}{10}w^2-\\frac{1}{20}w+\\frac{1}{25}', true],
  [M, 3, 'p-min-variance-pair', 1, '0.09w^2+0.04\\left(1-w\\right)^2+0.03w\\left(1-w\\right)', false],
  [M, 3, 'p-min-variance-pair', 1, '0.13w^2-0.08w+0.04', 'no-cross'],
  [M, 3, 'p-min-variance-pair', 2, '0.25', true], [M, 3, 'p-min-variance-pair', 2, '1/4', true],
  [M, 3, 'p-min-variance-pair', 3, '0.1837', true], [M, 3, 'p-min-variance-pair', 3, '0.18', false], [M, 3, 'p-min-variance-pair', 4, '0.0675', true],
  [M, 3, 'p-min-variance-pair', 5, '0.0351', true], [M, 3, 'p-min-variance-pair', 5, '0.03511', true], [M, 3, 'p-min-variance-pair', 5, '0.0344', 'sigma-lambda'],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (ok) return; if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };

/* returns true (correct) or the wrong[] key or null */
const gradeNumeric = (w, text) => {
  if (G.isSetSpec(w)) { const r = G.numSetGrade(w, text); return r.ok ? true : (r.key || null); }
  const v = G.parseNum(text);
  if (!Number.isFinite(v)) return null;
  if (G.within(v, +w.answer, w.tol)) return true;
  const m = G.matchWrong(v, w.wrong, { abs: 1e-9 });
  return m ? m.id : null;
};
const head = (j) => (Array.isArray(j) ? j[0] : null);
const args = (j) => (Array.isArray(j) ? j.slice(1) : []);
const hasSum = (j) => head(j) === 'Add' || head(j) === 'Subtract' || args(j).some(hasSum);
const isSumLike = (j) => head(j) === 'Add' || head(j) === 'Subtract';
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo); } catch { return false; } };
  if ([w.answer, ...(w.accept || [])].some(eq)) {
    if (w.form === 'expanded') { let ok = true; try { ok = G.withParsed(ce, L, fo.functions, (e) => (isSumLike(e.json) ? args(e.json).every((t) => !hasSum(t)) : !hasSum(e.json))); } catch { ok = true; } return ok ? true : 'form'; }
    return true;
  }
  const x = (w.wrong || []).find((y) => y.tex && eq(y.tex));
  return x ? x.id : null;
};

for (const course of [T, M]) for (const n of [1, 2, 3]) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${course} ${n} ${it.id} part ${i + 1}`;
    const typed = TYPED.filter((r) => r[0] === course && r[1] === n && r[2] === it.id && r[3] === i + 1);
    const judge = (grade) => { for (const r of typed) { const got = grade(w, r[4]); const want = r[5] === false ? [null, ...((w.wrong || []).map((x) => x.id)), 'count', 'form'] : [r[5]]; say(want.includes(got) && (r[5] !== false || got !== true), r[6], `${where}: typed "${r[4]}" graded ${JSON.stringify(got)}, reader expects ${JSON.stringify(r[5])}`); } };
    if (w.kind === 'numeric') {
      if (!G.isSetSpec(w)) {
        say(G.within(+w.answer, +w.answer, w.tol), null, `${where}: answer outside its own band`);
        for (const x of w.wrong || []) say(!G.within(+x.value, +w.answer, w.tol), null, `${where}: wrong "${x.id}" = ${x.value} is inside the answer band`);
        (w.wrong || []).forEach((x, a) => { const m = G.matchWrong(+x.value, w.wrong, { abs: 1e-9 }); say(m === x, null, `${where}: wrong "${x.id}" = ${x.value} is caught first by "${m && m.id}"`); });
      } else for (const x of w.wrong || []) say(!G.numSetGrade(w, String(x.value)).ok, null, `${where}: set wrong "${x.id}" grades correct`);
      judge(gradeNumeric);
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer) === true, null, `${where}: answer does not grade correct`);
      for (const a of w.accept || []) say(gradeExpr(w, a) === true, null, `${where}: accept "${a}" does not grade correct`);
      for (const x of w.wrong || []) say(gradeExpr(w, x.tex) === x.id, null, `${where}: wrong "${x.id}" ${x.tex} grades ${gradeExpr(w, x.tex)}`);
      judge(gradeExpr);
    }
  });
}
/* --probe: forms the reader was unsure of; printed, not judged */
if (argv.includes('--probe')) {
  const probe = [[T, 2, 'p-square-geometric', 3, '\\frac{(k+1)!}{k!}'], [M, 1, 'p-dollar-holding', 4, '-\\frac{2000}{x^2}'], [M, 2, 'p-two-book-risk', 2, 'z=0.6x+0.8y'],
    [M, 1, 'p-stretched-bowl', 2, '18,6'], [M, 2, 'p-slopes-around', 4, '(0.6;-0.8)'], [M, 2, 'p-slopes-around', 4, '\\left(\\frac35,-\\frac45\\right)'], [M, 3, 'p-capital-limit', 1, 'x=7,y=3'],
    [M, 3, 'p-min-variance-pair', 1, '\\frac{2w^2-w}{20}+0.04'], [M, 3, 'p-min-variance-pair', 1, '0.1w^2-0.05w+\\frac{1}{25}'], [M, 1, 'p-stretched-bowl', 2, '(18x,2y)']];
  for (const [c, n, id, part, L] of probe) {
    const set = JSON.parse(fs.readFileSync(`app/content/courses/${c}/problems-${n}.json`, 'utf8'));
    const w = set.items.find((x) => x.id === id).parts[part - 1].widget;
    console.log(`probe ${c} ${n} ${id} part ${part}: "${L}" -> ${JSON.stringify(gradeExpr(w, L))}`);
  }
  for (const s of ['-0.00030', '35.3 bp', '£1,418', '17.1e-5', '1.2143.', '60°', '0.6885 ']) console.log(`parseNum(${JSON.stringify(s)}) = ${G.parseNum(s)}`);
}
console.log(`grade-check: ${checks} checks, ${fails} failures, ${findings} findings (rows the reader holds to be content faults)`);
process.exit(fails ? 1 : 0);
