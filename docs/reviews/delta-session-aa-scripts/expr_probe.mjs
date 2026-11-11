/* Delta read, session AA: review (d) finding A8, left as an engine item by the fix pass.
   Would the content fix the reader proposed (extra slips spelt with a root) have worked on the real grade.js?
   Usage (from the repo root): node docs/reviews/delta-session-aa-scripts/expr_probe.mjs <pkgs> */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const cdn = path.resolve(process.argv[2]);
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const C = g.ComputeEngine.ComputeEngine || g.ComputeEngine, ce = new C();
g.ZQ = {};
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const eq = (a, b) => !!g.ZQ.grade.exprEqual(ce, a, b);

const rows = [
  ['key', '(1-2s)^{-2}', '\\frac{1}{(1-2s)^2}'],
  ['key', '(1-2s)^{-2}', '\\frac{1}{1-4s+4s^2}'],
  ['slip one as stored', '(1-2s)^{-1/2}', '\\frac{1}{\\sqrt{1-2s}}'],
  ['slip one, root spelling stored', '\\frac{1}{\\sqrt{1-2s}}', '\\frac{1}{\\sqrt{1-2s}}'],
  ['slip one, root stored, power typed', '\\frac{1}{\\sqrt{1-2s}}', '(1-2s)^{-1/2}'],
  ['slip added as stored', '4(1-2s)^{-1/2}', '\\frac{4}{\\sqrt{1-2s}}'],
  ['slip added, root spelling stored', '\\frac{4}{\\sqrt{1-2s}}', '\\frac{4}{\\sqrt{1-2s}}'],
  ['root slip must not match the key', '(1-2s)^{-2}', '\\frac{1}{\\sqrt{1-2s}}'],
  ['root slips must not match each other', '\\frac{4}{\\sqrt{1-2s}}', '\\frac{1}{\\sqrt{1-2s}}'],
  ['ticket-stages rates slip', '\\frac{1}{(1-s)(1-0.5s)}', '\\frac{1}{(1-s)(1-\\frac{s}{2})}'],
  ['ticket-stages key', '\\frac{1}{(1-s)(1-2s)}', '\\frac{0.5}{(1-s)(0.5-s)}'],
  ['ticket-stages rates slip is not the key', '\\frac{1}{(1-s)(1-2s)}', '\\frac{1}{(1-s)(1-0.5s)}'],
];
/* engine probe: expressions that are pure imaginary at the sample points (the grader reads only the real part) */
const pairs = [['\\sqrt{1-2s}', '2\\sqrt{1-2s}'], ['\\sqrt{1-2s}', '\\frac{1}{\\sqrt{1-2s}}'], ['\\frac{1}{\\sqrt{1-2s}}', '\\frac{1}{\\sqrt{1-3s}}'], ['\\sqrt{x-5}', '3\\sqrt{x-5}'], ['\\sqrt{x}', '3\\sqrt{x}'], ['\\sqrt{1-x^2}', '2\\sqrt{1-x^2}'], ['\\ln(1-2s)', '2\\ln(1-2s)'], ['(1-2s)^{-1/2}', '4(1-2s)^{-1/2}']];
for (const [a, b] of pairs) rows.push(['engine probe', a, b]);
for (const [name, stored, typed] of rows) console.log(`${eq(stored, typed) ? 'equal  ' : 'unequal'} | ${name} | ${stored} | ${typed}`);
