#!/usr/bin/env node
/* Second read, problems 0.3 c: the engine on a power with a bracketed exponent typed as plain text, with and without the
   widget's text fallback (normExpr), on every geometric-rule part of the series sets; and shapeExactAngle on labelled forms.
   node docs/reviews/problems-0.3-c-scripts/probe.mjs --local-cdn <pkgs>      (from the repo root; prints a table, exits 0) */
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

const part = (course, n, id, i) => JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8')).items.find(x => x.id === id).parts[i - 1].widget;
const ROWS = [
  ['series', 1, 'p-pendulum-swings', 2, ['80*0.9^(n-1)', '80(0.9)^(n-1)', '80*(0.9)^(n-1)', '80x0.9^(n-1)', '80 x 0.9^(n-1)', '80×0.9^(n-1)', '80*0.9^{(n-1)}', '80\\cdot(0.9)^{(n-1)}', '80*.9^(n-1)', '80*(9/10)^(n-1)', '80\\cdot0.9^{n-1}cm']],
  ['series', 1, 'p-daily-tablet', 3, ['160*0.4^(n-1)', '160(0.4)^(n-1)', '160*(0.4)^(n-1)', '160×0.4^(n-1)', '400*0.4^n', '400(0.4)^n', '160*(2/5)^(n-1)']],
  ['series', 1, 'p-shop-orders', 4, ['64*1.5^(n-1)', '64(1.5)^(n-1)', '64*(1.5)^(n-1)', '64×1.5^(n-1)', '96*1.5^(n-2)', '96(1.5)^(n-2)', '64*(3/2)^(n-1)']],
  ['series', 2, 'p-app-users', 3, ['2*3^n-2', '2(3^n-1)', '2*(3^n-1)', '2×3^n-2', '4(3^n-1)/(3-1)', '(4(3^n-1))/2', '2*3^(n)-2']],
  ['series', 2, 'p-two-repayment-plans', 1, ['5n^2+45n', '5n²+45n', 'n/2*(100+10(n-1))', '(n/2)(100+10(n-1))', 'n/2(100+10(n-1))', 'n(100+10(n-1))/2']],
  ['series', 3, 'p-bracket-estimate', 2, ['1-21x+189x^2', '1-21x+189x²', '1 - 21x + 189x^2', '1-21x+189x^2+...', '1-21x+189x^2+\\dots']],
  ['trig', 1, 'p-hexagon-tile', 1, ['5sqrt(3)', '5√3', '5\\sqrt{3}cm', 'sqrt(75)', '5*3^(1/2)', '5\\cdot3^{0.5}']],
  ['trig', 3, 'p-garden-bed', 1, ['30sinC', '30 sin C', '30*sin(C)', '30sin(C)', 'sin(C)*30', '\\sin C\\cdot30', '\\sin(C)\\cdot30', '30\\sin C m^2', '30\\sin C^\\circ', '15\\cdot2\\sin C', '\\frac{5\\cdot12\\sin C}{2}', '30\\sin(180-C)', '30\\sin(180^\\circ-C)']],
  ['trig', 2, 'p-observation-wheel', 2, ['pi/10', '\\pi/10', '2pi/20', '2π/20', '0.1pi', '\\frac{\\pi}{10}rad', '18^\\circ', '\\frac{\\pi}{10}^{}']],
];
for (const [course, n, id, i, typed] of ROWS) {
  const w = part(course, n, id, i), fo = { functions: w.functions || [], integers: w.integers || [] };
  const forms = [w.answer, ...(w.accept || [])];
  console.log(`\n${course} ${n} ${id} part ${i}   key ${w.answer}   accept ${JSON.stringify(w.accept || [])}`);
  for (const t of typed) {
    let sym = false; try { sym = forms.some(f => !!G.exprEqual(ce, t, f, fo)); } catch { sym = false; }
    const text = forms.some(f => !!G.normExpr(t) && G.normExpr(t) === G.normExpr(f));
    console.log(`   ${(sym || text) ? 'correct' : 'WRONG  '}  ${t.padEnd(28)} exprEqual ${sym ? 'yes' : 'no '}  text fallback ${text ? 'yes' : 'no'}`);
  }
}
console.log('\nshapeExactAngle (form: "exact-angle", trig 3 p-quadratic-in-sine part 4):');
for (const t of ['\\frac{5\\pi}{6}', '5\\pi/6', '\\frac{5}{6}\\pi', 'x=\\frac{5\\pi}{6}', 'x = \\frac{5\\pi}{6}', '5pi/6', '5π/6', '\\frac{5\\pi}{6}\\text{ rad}', '\\frac{5 \\pi}{6}', '\\frac{5\\cdot\\pi}{6}', '\\frac{5\\times\\pi}{6}', '5\\cdot\\frac{\\pi}{6}', '5\\frac{\\pi}{6}', '\\frac{5\\pi}{6}^{}', '\\left(\\frac{5\\pi}{6}\\right)', '\\dfrac{5\\pi}{6}', '\\tfrac{5\\pi}{6}', '150^\\circ', '\\frac{150\\pi}{180}'])
  console.log(`   ${G.shapeExactAngle(t) ? 'shape ok ' : 'REFUSED  '} ${t}`);
