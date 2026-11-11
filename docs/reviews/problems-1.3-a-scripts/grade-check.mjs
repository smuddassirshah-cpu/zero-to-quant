#!/usr/bin/env node
/* Second read, problems 1.3 (a): what the engine's own graders do with each part.
   Loads app/js/engine/grade.js and the local Compute Engine (as tools/audit-plain-functions.mjs does), then for every part of the six sets:
     numeric     the answer and every typed string in TYPED below is graded as numeric.js grades it (parseNum, the "%" unit, within, numSetGrade);
                 each wrong[] value must fall outside the answer's band
     expression  the answer, every accept[] form and every typed string in TYPED is graded as expression.js grades it (exprEqual or
                 exprEqualUpToConstant, then the "factorised" shape); each wrong[].tex must not grade correct
   TYPED rows carry the result the reader expects (true accepted, false refused). A row marked `finding` is one the reader holds to be a fault
   in the content: it prints as FINDING and does not fail the run. Any other mismatch prints as FAIL and the exit code is 1.

   node docs/reviews/problems-1.3-a-scripts/grade-check.mjs --local-cdn <pkgs>      (from the repo root) */
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

/* [course, set, item, part (1-based), typed text, expected, finding?] */
const TYPED = [
  ['limits', 1, 'p-broker-schedule', 3, '0.4', true], ['limits', 1, 'p-broker-schedule', 3, '2/5', true],
  ['limits', 1, 'p-rational-features', 1, '5/3', true], ['limits', 1, 'p-rational-features', 1, '1.6667', true], ['limits', 1, 'p-rational-features', 1, '1.67', false],
  ['limits', 1, 'p-fit-the-constants', 4, '7/3', true], ['limits', 1, 'p-fit-the-constants', 4, '2.3333', true],
  ['limits', 1, 'p-print-wiggle', 1, '0.2', true], ['limits', 1, 'p-print-wiggle', 1, '1/5', true],
  ['limits', 2, 'p-fund-session', 2, '1, 2', true], ['limits', 2, 'p-fund-session', 2, '2,1', true], ['limits', 2, 'p-fund-session', 2, 't = 1 or t = 2', true], ['limits', 2, 'p-fund-session', 2, '1', false],
  ['limits', 2, 'p-fund-session', 4, '-1.5', true], ['limits', 2, 'p-fund-session', 4, '-3/2', true],
  ['limits', 2, 'p-perpetuity-slope', 2, '-2041', true], ['limits', 2, 'p-perpetuity-slope', 2, '-2040.82', true],
  ['limits', 2, 'p-perpetuity-slope', 2, '-2040', true, 'price kept to the penny: (102.04 - 100) / -0.001 = -2040'],
  ['limits', 3, 'p-relative-strength', 2, '0.0004', true], ['limits', 3, 'p-relative-strength', 2, '1/2500', true],
  ['limits', 3, 'p-relative-strength', 3, '2', true], ['limits', 3, 'p-relative-strength', 3, '2%', true], ['limits', 3, 'p-relative-strength', 3, '0.02', false],
  ['limits', 3, 'p-research-price', 4, '16.67', true], ['limits', 3, 'p-research-price', 4, '50/3', true],
  ['limits', 3, 'p-gas-season', 2, '-0.157', true],
  ['limits', 3, 'p-gas-season', 3, '-28.77', true], ['limits', 3, 'p-gas-season', 3, '-28.76', true],
  ['limits', 3, 'p-gas-season', 3, '-28.75', true, 'from part 2\'s own 3-place value: 5 - 215 * 0.157 = -28.755, rounded towards zero'],
  ['integrals', 1, 'p-falling-parabola', 1, '15.625', true], ['integrals', 1, 'p-falling-parabola', 1, '125/8', true],
  ['integrals', 1, 'p-desk-session', 4, '-5.33', true], ['integrals', 1, 'p-desk-session', 4, '-16/3', true],
  ['integrals', 1, 'p-desk-session', 5, '2.33', true], ['integrals', 1, 'p-desk-session', 5, '7/3', true],
  ['integrals', 2, 'p-area-function', 4, '20/3', true], ['integrals', 2, 'p-area-function', 4, '6.667', true],
  ['integrals', 2, 'p-turnover-decay', 3, '13.83', true],
  ['integrals', 2, 'p-turnover-decay', 3, '13.84', true, 'with e^-2 = 0.1353: 16 - 16 * 0.1353 = 13.8352'],
  ['integrals', 2, 'p-turnover-decay', 4, '2.77', true],
  ['integrals', 2, 'p-line-and-parabola', 1, '-1, 1.5', true], ['integrals', 2, 'p-line-and-parabola', 1, '3/2, -1', true],
  ['integrals', 2, 'p-line-and-parabola', 2, '125/24', true], ['integrals', 2, 'p-line-and-parabola', 2, '5.208', true],
  ['integrals', 2, 'p-line-and-parabola', 3, '19/6', true], ['integrals', 2, 'p-line-and-parabola', 3, '3.167', true],
  ['integrals', 2, 'p-line-and-parabola', 4, '67/8', true], ['integrals', 2, 'p-line-and-parabola', 4, '8.375', true],
  ['integrals', 3, 'p-order-size-tail', 2, '1/5', true], ['integrals', 3, 'p-order-size-tail', 4, '9.95', true],
  ['integrals', 3, 'p-time-to-fill', 2, '0.406', true], ['integrals', 3, 'p-time-to-fill', 4, '25', true],
  ['integrals', 3, 'p-log-return', 1, '-0.0719', true],
  ['integrals', 3, 'p-log-return', 1, '-0.0720', true, 'the explanation\'s own printed working: 0.5 * (-0.3466 + 0.2027) = -0.07195'],
  ['integrals', 3, 'p-log-return', 2, '-0.0452', true],
  ['integrals', 3, 'p-log-return', 3, '0.0017', true], ['integrals', 3, 'p-log-return', 3, '0.00167', true],
  ['integrals', 3, 'p-signal-average', 2, '3.459', true], ['integrals', 3, 'p-signal-average', 3, '0.865', true],
  ['integrals', 3, 'p-signal-average', 4, '2.967', true],
  ['integrals', 3, 'p-signal-average', 4, '2.968', true, 'the explanation\'s own printed working: 2 * (1.2131 + 0.2707) = 2.9676'],
  // expressions
  ['limits', 2, 'p-session-volume', 2, '3h+16', true],
  ['limits', 2, 'p-fund-session', 1, '6(t^2-3t+2)', true],
  ['limits', 2, 'p-inventory-penalty', 1, '4+\\frac{1}{2}h', true], ['limits', 2, 'p-inventory-penalty', 1, '\\frac{h}{2}+4', true],
  ['limits', 3, 'p-research-price', 3, '-(50-p)(3p-50)', true], ['limits', 3, 'p-research-price', 3, '(50-p)^2-2p(50-p)', false], ['limits', 3, 'p-research-price', 3, '3p^2-200p+2500', false],
  ['limits', 3, 'p-gas-season', 1, '-\\frac{\\pi}{20}\\sin\\left(\\frac{\\pi t}{6}\\right)', true],
  ['limits', 3, 'p-gas-season', 1, '-0.3\\cdot\\frac{\\pi}{6}\\sin\\left(\\frac{\\pi t}{6}\\right)', true],
  ['limits', 3, 'p-gas-season', 1, '-\\frac{0.3\\pi}{6}\\sin\\left(\\frac{\\pi t}{6}\\right)', true],
  ['limits', 3, 'p-gas-season', 1, '-\\frac{\\pi}{20}\\sin\\frac{\\pi t}{6}', true],
  ['limits', 3, 'p-gas-season', 1, '-0.157\\sin\\left(\\frac{\\pi t}{6}\\right)', false],
  ['limits', 3, 'p-gas-season', 1, '-0.3\\cos\\left(\\frac{\\pi t}{6}\\right)', false],
  ['integrals', 1, 'p-falling-parabola', 4, '27-\\frac{27}{n^3}\\cdot\\frac{n(n+1)(2n+1)}{6}', true],
  ['integrals', 1, 'p-falling-parabola', 4, '\\frac{9(4n+1)(n-1)}{2n^2}', true],
  ['integrals', 1, 'p-falling-parabola', 4, '18', false],
  ['integrals', 2, 'p-area-function', 3, '\\frac{t^3}{3}-3t^2+8t+C', true], ['integrals', 2, 'p-area-function', 3, '\\frac{t^3}{3}-3t^2+8t+5', true],
  ['integrals', 2, 'p-area-function', 3, 't^2-6t+8', false],
  ['integrals', 2, 'p-turnover-decay', 1, '-\\frac{16}{e^{0.5t}}', true], ['integrals', 2, 'p-turnover-decay', 1, '16-16e^{-0.5t}', true],
  ['integrals', 2, 'p-turnover-decay', 1, '-16e^{-0.5t}+C', true], ['integrals', 2, 'p-turnover-decay', 1, '-16e^{0.5t}', false],
  ['integrals', 2, 'p-etf-units', 2, '-x(x-3)^2', true], ['integrals', 2, 'p-etf-units', 2, '6x^2-x^3-9x+C', false], ['integrals', 2, 'p-etf-units', 2, '-t^3+6t^2-9t', false],
  ['integrals', 3, 'p-order-size-tail', 1, '\\frac{-1}{x^2+1}', true], ['integrals', 3, 'p-order-size-tail', 1, '\\frac{x^2}{1+x^2}', true],
  ['integrals', 3, 'p-order-size-tail', 1, '-\\frac{1}{u}', false],
  ['integrals', 3, 'p-time-to-fill', 1, '-e^{-x}(x+1)', true], ['integrals', 3, 'p-time-to-fill', 1, '-\\frac{x+1}{e^x}', true],
  ['integrals', 3, 'p-signal-average', 1, '-\\frac{4}{e^{t^2/8}}', true], ['integrals', 3, 'p-signal-average', 1, '-4e^{-t^2/8}+C', true],
  ['integrals', 3, 'p-signal-average', 1, '-4e^{-u}', false],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (ok) return; if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };

const gradeNumeric = (w, text) => {
  if (G.isSetSpec(w) && w.unordered === true) return !!G.numSetGrade(w, text).ok;
  const pct = w.unit === '%';
  let v = G.parseNum(text); if (pct && !text.includes('%')) v /= 100;
  return Number.isFinite(v) && G.within(v, w.answer, w.tol);
};
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!(w.upToConstant ? G.exprEqualUpToConstant(ce, L, t, fo) : G.exprEqual(ce, L, t, fo)); } catch { return false; } };
  const same = [w.answer, ...(w.accept || [])].some(eq);
  if (!same) return false;
  if (w.form === 'factorised') { try { return !!G.shapeFactorised(ce.parse(L).json); } catch { return true; } }
  return true;
};

for (const course of ['limits', 'integrals']) for (const n of [1, 2, 3]) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${course} ${n} ${it.id} part ${i + 1}`;
    const typed = TYPED.filter((r) => r[0] === course && r[1] === n && r[2] === it.id && r[3] === i + 1);
    if (w.kind === 'numeric') {
      if (!G.isSetSpec(w)) {
        say(G.within(w.answer, w.answer, w.tol), null, `${where}: answer outside its own band`);
        for (const x of w.wrong || []) say(!G.within(x.value, w.answer, w.tol), null, `${where}: wrong "${x.id}" = ${x.value} is inside the answer band`);
        for (const x of w.wrong || []) for (const y of w.wrong || []) if (x !== y) say(!G.within(x.value, y.value, y.tol || w.tol) || (w.wrong.indexOf(x) < w.wrong.indexOf(y)), null, `${where}: wrong "${x.id}" is shadowed by "${y.id}"`);
      } else for (const x of w.wrong || []) say(!G.numSetGrade(w, String(x.value)).ok, null, `${where}: set wrong "${x.id}" grades correct`);
      for (const r of typed) say(gradeNumeric(w, r[4]) === r[5], r[6], `${where}: typed "${r[4]}" ${r[5] ? 'refused' : 'accepted'}`);
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer), null, `${where}: answer does not grade correct`);
      for (const a of w.accept || []) say(gradeExpr(w, a), null, `${where}: accept "${a}" does not grade correct`);
      for (const x of w.wrong || []) say(!gradeExpr(w, x.tex), null, `${where}: wrong "${x.id}" ${x.tex} grades correct`);
      for (const r of typed) say(gradeExpr(w, r[4]) === r[5], r[6], `${where}: typed "${r[4]}" ${r[5] ? 'refused' : 'accepted'}`);
    }
  });
}
/* --accept-lines: the accept line "Any form equal to X" on a numeric part. Can the field take X as typed? (review finding 6) */
if (argv.includes('--accept-lines')) {
  for (const s of ['2ln4', '2ln(4)', '2\\ln 4', 'sqrt(99)', '√99', '3e^-2', '3e^{-2}', '4(1-e^-2)', '1-e^-2', '20/3', '-16/3', '201/24'])
    console.log(`parseNum(${JSON.stringify(s)}) = ${G.parseNum(s)}`);
}
console.log(`grade-check: ${checks} checks, ${fails} failures, ${findings} findings (rows the reader holds to be content faults)`);
process.exit(fails ? 1 : 0);
