#!/usr/bin/env node
/* Second read, problems 1.3 (c): what the engine's own graders do with each part of limits 4 and 5, integrals 4, multivar 4 and 5.
   Same harness as problems-1.3-a-scripts/grade-check.mjs: loads app/js/engine/grade.js and the local Compute Engine, then
     numeric     answer inside its own band, every wrong[] outside it, no wrong[] shadowed by an earlier one, every TYPED string graded
                 as numeric.js grades it (parseNum, within)
     expression  answer, every accept[] form and every TYPED string graded as expression.js grades it; each wrong[].tex must not
                 grade correct
   A TYPED row marked with a 7th field is one the reader holds to be a content fault: it prints as FINDING and does not fail the run.

   node docs/reviews/problems-1.3-c-scripts/grade-check.mjs --local-cdn <pkgs> [--accept-lines]      (from the repo root) */
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

const SETS = [['limits', 4], ['limits', 5], ['integrals', 4], ['multivar', 4], ['multivar', 5]];

/* [course, set, item, part (1-based), typed text, expected, finding?] */
const TYPED = [
  // limits 4
  ['limits', 4, 'p-spread-quote', 1, '\\frac{900}{(2+s)^2}-\\frac{1800s}{(2+s)^3}', true],
  ['limits', 4, 'p-spread-quote', 1, '\\frac{900(2+s)^2-1800s(2+s)}{(2+s)^4}', true],
  ['limits', 4, 'p-spread-quote', 1, '\\frac{900(2-s)}{(s+2)^3}', true],
  ['limits', 4, 'p-spread-quote', 1, '\\frac{900}{(2+s)^2}', false],
  ['limits', 4, 'p-spread-quote', 3, '112.5', true], ['limits', 4, 'p-spread-quote', 3, '225/2', true],
  ['limits', 4, 'p-spread-quote', 5, '8.33', true], ['limits', 4, 'p-spread-quote', 5, '25/3', true], ['limits', 4, 'p-spread-quote', 5, '8.3', false],
  ['limits', 4, 'p-signal-decay', 4, '122.74', true], ['limits', 4, 'p-signal-decay', 4, '122.7', false],
  ['limits', 4, 'p-barbell-hedge', 1, '500e^{-5u}-400e^{-8u}-100e^{-2u}', true],
  ['limits', 4, 'p-barbell-hedge', 1, '-\\frac{100}{e^{2u}}-\\frac{400}{e^{8u}}+\\frac{500}{e^{5u}}', true, 'engine: 400e^{-8u} evaluates to 0 at u = 2.9 where 400/e^{8u} does not (probe-e8u.mjs); a correct form is refused'],
  ['limits', 4, 'p-barbell-hedge', 1, '50e^{-2u}+50e^{-8u}-100e^{-5u}', false],
  ['limits', 4, 'p-barbell-hedge', 4, '43', true], ['limits', 4, 'p-barbell-hedge', 4, '42.81', true], ['limits', 4, 'p-barbell-hedge', 4, '£43', true],
  ['limits', 4, 'p-barbell-hedge', 4, '42', false], ['limits', 4, 'p-barbell-hedge', 4, '0.04281', false],
  ['limits', 4, 'p-barbell-hedge', 4, '45', false], // (1/2) V''(0) u^2: refused, rightly, but with the generic line only (finding 3)
  ['limits', 4, 'p-level-annuity', 2, '\\frac{10re^{-10r}+e^{-10r}-1}{r^2}', true],
  ['limits', 4, 'p-level-annuity', 2, '\\frac{10e^{-10r}}{r}-\\frac{1-e^{-10r}}{r^2}', true],
  ['limits', 4, 'p-level-annuity', 2, '\\frac{10r+1-e^{10r}}{r^2e^{10r}}', true],
  ['limits', 4, 'p-level-annuity', 2, '\\frac{10e^{-10r}}{1}', false],
  ['limits', 4, 'p-level-annuity', 4, '9', true], ['limits', 4, 'p-level-annuity', 4, '9.00', true],
  ['limits', 4, 'p-level-annuity', 5, '9.0635', true], ['limits', 4, 'p-level-annuity', 5, '9.06346', true], ['limits', 4, 'p-level-annuity', 5, '9.06', false],
  // limits 5
  ['limits', 5, 'p-camera-pan', 1, '\\frac{1}{30}\\cdot\\frac{1}{1+\\left(\\frac{x}{30}\\right)^2}', true],
  ['limits', 5, 'p-camera-pan', 1, '\\frac{30}{x^2+900}', true],
  ['limits', 5, 'p-camera-pan', 1, '\\frac{1}{30+\\frac{x^2}{30}}', true],
  ['limits', 5, 'p-camera-pan', 1, '\\frac{1}{30}', false],
  ['limits', 5, 'p-camera-pan', 2, '0.24', true], ['limits', 5, 'p-camera-pan', 2, '6/25', true],
  ['limits', 5, 'p-camera-pan', 3, '0.524', true], ['limits', 5, 'p-camera-pan', 3, '0.5236', true], ['limits', 5, 'p-camera-pan', 3, '0.523', false],
  ['limits', 5, 'p-camera-pan', 4, '15.7', true], ['limits', 5, 'p-camera-pan', 4, '15.68', true], ['limits', 5, 'p-camera-pan', 4, '15.6', false],
  ['limits', 5, 'p-app-adoption', 5, '3.2', true], ['limits', 5, 'p-app-adoption', 5, '16/5', true],
  ['limits', 5, 'p-impact-curve', 1, '\\frac{2}{500}\\cdot\\frac{1}{1+\\frac{q^2}{250000}}', true],
  ['limits', 5, 'p-impact-curve', 1, '\\frac{1000}{q^2+250000}', true],
  ['limits', 5, 'p-impact-curve', 1, '\\frac{1}{250}', false], ['limits', 5, 'p-impact-curve', 1, '\\frac{1000}{250000+q}', false],
  ['limits', 5, 'p-impact-curve', 2, '0.4', true], ['limits', 5, 'p-impact-curve', 2, '2/5', true],
  ['limits', 5, 'p-impact-curve', 4, '325', true], ['limits', 5, 'p-impact-curve', 4, '324.61', true], ['limits', 5, 'p-impact-curve', 4, '324', false],
  // integrals 4
  ['integrals', 4, 'p-impact-kernel', 2, '2\\ln\\left(\\frac{1+u}{2+u}\\right)', true],
  ['integrals', 4, 'p-impact-kernel', 2, '2\\ln(1+u)-2\\ln(2+u)+C', true],
  ['integrals', 4, 'p-impact-kernel', 2, '2\\ln|1+u|-2\\ln|2+u|', true],
  ['integrals', 4, 'p-impact-kernel', 2, '\\ln\\frac{(1+u)^2}{(2+u)^2}', true],
  ['integrals', 4, 'p-impact-kernel', 2, '2\\ln\\frac{2+2u}{2+u}', true],
  ['integrals', 4, 'p-impact-kernel', 2, '-2\\ln\\frac{2+u}{1+u}', true],
  ['integrals', 4, 'p-impact-kernel', 2, '\\frac{2}{1+u}-\\frac{2}{2+u}', false],
  ['integrals', 4, 'p-impact-kernel', 3, '0.811', true], ['integrals', 4, 'p-impact-kernel', 3, '0.81', false],
  ['integrals', 4, 'p-impact-kernel', 4, '1.386', true],
  ['integrals', 4, 'p-impact-kernel', 5, '0.585', true],
  ['integrals', 4, 'p-impact-kernel', 5, '0.586', false], // the restated 0.811 / 1.386 gives 0.5851, so 0.585 is the only 3 dp value
  ['integrals', 4, 'p-flared-mouth', 1, '6.283', true], ['integrals', 4, 'p-flared-mouth', 2, '1.645', true],
  ['integrals', 4, 'p-flared-mouth', 3, '4.935', true], ['integrals', 4, 'p-flared-mouth', 4, '0.707', true],
  ['integrals', 4, 'p-dish-and-spindle', 2, '2.048', true], ['integrals', 4, 'p-dish-and-spindle', 3, '0.141', true],
  ['integrals', 4, 'p-dish-and-spindle', 4, '15', true], ['integrals', 4, 'p-dish-and-spindle', 4, '14.55', true], ['integrals', 4, 'p-dish-and-spindle', 4, '14', false],
  ['integrals', 4, 'p-rubber-seal', 1, '1.571', true], ['integrals', 4, 'p-rubber-seal', 2, '0', true],
  ['integrals', 4, 'p-rubber-seal', 3, '59.22', true], ['integrals', 4, 'p-rubber-seal', 5, '5.07', true],
  // multivar 4
  ['multivar', 4, 'p-weighted-rectangle', 1, '\\frac{1}{2}y^2', true], ['multivar', 4, 'p-weighted-rectangle', 1, '\\frac{x^2y^2}{2}', false],
  ['multivar', 4, 'p-weighted-rectangle', 2, '3/4', true], ['multivar', 4, 'p-weighted-rectangle', 2, '0.75', true],
  ['multivar', 4, 'p-weighted-rectangle', 3, '\\frac{3}{4}x\\cdot\\frac{8x^3}{3}', true], ['multivar', 4, 'p-weighted-rectangle', 3, '\\frac{xy^3}{4}', false],
  ['multivar', 4, 'p-weighted-rectangle', 4, '2/5', true], ['multivar', 4, 'p-weighted-rectangle', 4, '0.4', true],
  ['multivar', 4, 'p-corner-sprinkler', 1, '\\sqrt{9-x^2}', true], ['multivar', 4, 'p-corner-sprinkler', 1, '\\sqrt{(3-x)(3+x)}', true],
  ['multivar', 4, 'p-corner-sprinkler', 1, '(9-x^2)^{0.5}', true], ['multivar', 4, 'p-corner-sprinkler', 1, '\\sqrt{9}-x', false],
  ['multivar', 4, 'p-corner-sprinkler', 1, '-\\sqrt{9-x^2}', false], ['multivar', 4, 'p-corner-sprinkler', 1, '\\sqrt{x^2-9}', false],
  ['multivar', 4, 'p-corner-sprinkler', 2, '(9-r^2)r', true], ['multivar', 4, 'p-corner-sprinkler', 2, '(9-r^2)r\\,dr\\,d\\theta', false],
  ['multivar', 4, 'p-corner-sprinkler', 3, '20.25', true], ['multivar', 4, 'p-corner-sprinkler', 3, '81/4', true],
  ['multivar', 4, 'p-corner-sprinkler', 4, '31.81', true], ['multivar', 4, 'p-corner-sprinkler', 4, '31.8', false],
  ['multivar', 4, 'p-corner-sprinkler', 5, '1.62', true], ['multivar', 4, 'p-corner-sprinkler', 5, '1.6236', true],
  ['multivar', 4, 'p-drone-landing', 1, '5.0133', true], ['multivar', 4, 'p-drone-landing', 1, '5.01', false],
  ['multivar', 4, 'p-drone-landing', 2, '8\\pi', true], ['multivar', 4, 'p-drone-landing', 2, '\\left(\\sqrt{8\\pi}\\right)^2', true],
  ['multivar', 4, 'p-drone-landing', 2, '25.13', false], ['multivar', 4, 'p-drone-landing', 2, '\\pi', false],
  ['multivar', 4, 'p-drone-landing', 3, '\\frac{1}{8\\pi}', true], ['multivar', 4, 'p-drone-landing', 3, '\\frac{0.125}{\\pi}', true],
  ['multivar', 4, 'p-drone-landing', 3, '(8\\pi)^{-1}', true], ['multivar', 4, 'p-drone-landing', 3, '\\frac{\\pi}{8}', false],
  ['multivar', 4, 'p-drone-landing', 4, '0.3935', true], ['multivar', 4, 'p-drone-landing', 4, '0.39', false],
  ['multivar', 4, 'p-drone-landing', 5, '4.29', true],
  // multivar 5
  ['multivar', 5, 'p-three-strategies', 1, '4/3', true], ['multivar', 5, 'p-three-strategies', 1, '1.3333', true], ['multivar', 5, 'p-three-strategies', 1, '1.33', false],
  ['multivar', 5, 'p-three-strategies', 2, '-1/6', true], ['multivar', 5, 'p-three-strategies', 2, '-0.1667', true],
  ['multivar', 5, 'p-three-strategies', 4, '3/4', true], ['multivar', 5, 'p-three-strategies', 5, '2.125', true], ['multivar', 5, 'p-three-strategies', 5, '17/8', true],
  ['multivar', 5, 'p-dome-tent', 2, '2-\\frac{(2u)^2+4v^2}{2}', true], ['multivar', 5, 'p-dome-tent', 2, '2-2u^2-2v^2', true],
  ['multivar', 5, 'p-dome-tent', 2, '2-\\frac{x^2+4y^2}{2}', false],
  ['multivar', 5, 'p-dome-tent', 3, '2\\pi', true], ['multivar', 5, 'p-dome-tent', 3, '6.28', false],
  ['multivar', 5, 'p-dome-tent', 4, '\\frac{4\\pi}{3}', true], ['multivar', 5, 'p-dome-tent', 4, '\\frac{8\\pi}{6}', true],
  ['multivar', 5, 'p-dome-tent', 5, '2/3', true], ['multivar', 5, 'p-dome-tent', 5, '0.6667', true], ['multivar', 5, 'p-dome-tent', 5, '0.667', false],
  ['multivar', 5, 'p-triangle-field', 2, '32/15', true], ['multivar', 5, 'p-triangle-field', 2, '2.1333', true],
  ['multivar', 5, 'p-triangle-field', 3, '8/15', true], ['multivar', 5, 'p-triangle-field', 3, '0.5333', true],
  ['multivar', 5, 'p-triangle-field', 4, '2.3704', true], ['multivar', 5, 'p-triangle-field', 4, '64/27', true],
  ['multivar', 5, 'p-triangle-field', 5, '0.225', true], ['multivar', 5, 'p-triangle-field', 5, '9/40', true],
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
  return [w.answer, ...(w.accept || [])].some(eq);
};

for (const [course, n] of SETS) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${course} ${n} ${it.id} part ${i + 1}`;
    const typed = TYPED.filter((r) => r[0] === course && r[1] === n && r[2] === it.id && r[3] === i + 1);
    if (w.kind === 'numeric') {
      say(G.within(w.answer, w.answer, w.tol), null, `${where}: answer outside its own band`);
      for (const x of w.wrong || []) say(!G.within(x.value, w.answer, w.tol), null, `${where}: wrong "${x.id}" = ${x.value} is inside the answer band`);
      for (const x of w.wrong || []) for (const y of w.wrong || []) if (x !== y) say(!G.within(x.value, y.value, y.tol || w.tol) || (w.wrong.indexOf(x) < w.wrong.indexOf(y)), null, `${where}: wrong "${x.id}" is shadowed by "${y.id}"`);
      /* a wrong[] band wide enough to swallow other plausible entries: band wider than 20% of its own value and of the answer's band */
      for (const x of w.wrong || []) { const t = (x.tol && x.tol.abs) || 0; if (t > 0 && Math.abs(x.value) > 0 && t > 0.2 * Math.abs(x.value)) console.log(`NOTE    ${where}: wrong "${x.id}" = ${x.value} has band ±${t}, wider than 20% of the value`); }
      for (const r of typed) say(gradeNumeric(w, r[4]) === r[5], r[6], `${where}: typed "${r[4]}" ${r[5] ? 'refused' : 'accepted'}`);
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer), null, `${where}: answer does not grade correct`);
      for (const a of w.accept || []) say(gradeExpr(w, a), null, `${where}: accept "${a}" does not grade correct`);
      for (const x of w.wrong || []) say(!gradeExpr(w, x.tex), null, `${where}: wrong "${x.id}" ${x.tex} grades correct`);
      for (const r of typed) say(gradeExpr(w, r[4]) === r[5], r[6], `${where}: typed "${r[4]}" ${r[5] ? 'refused' : 'accepted'}`);
    }
  });
}
/* --accept-lines: an accept line "Any form equal to X" on a numeric part. Can the field take X as typed? */
if (argv.includes('--accept-lines')) {
  for (const s of ['2ln(3/2)', '2ln(1.5)', '2\\ln\\frac{3}{2}', '2ln2', '2 ln 2', 'ln4', '2pi', '2π', '2\\pi', 'pi^2/6', 'π^2/6', '\\frac{\\pi^2}{6}', 'pi^2/2',
    'sqrt(2)/2', '√2/2', '1/sqrt(2)', '2pi(2+ln3-4ln2)', 'pi(5/3+4ln(2/3))', 'pi/2', '6pi^2', '50/pi^2', 'ln(1.5)/ln(2)', '81pi/8', '4/3', '-1/6', '64/27'])
    console.log(`parseNum(${JSON.stringify(s)}) = ${G.parseNum(s)}`);
}
console.log(`grade-check: ${checks} checks, ${fails} failures, ${findings} findings (rows the reader holds to be content faults)`);
process.exit(fails ? 1 : 0);
