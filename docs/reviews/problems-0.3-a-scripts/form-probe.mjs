#!/usr/bin/env node
/* What "form": "simplified" (expression.js formOk: size(json) <= size(simplify().json)) would do to the typed forms of the
   parts that ask for a simplest form. Used to judge whether a content fix closes findings on unsimplified answers.
   node docs/reviews/problems-0.3-a-scripts/form-probe.mjs --local-cdn <pkgs>      (from the repo root) */
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
const size = (j) => (Array.isArray(j) ? 1 + j.slice(1).reduce((a, x) => a + size(x), 0) : 1);
const simplified = (L) => { try { return G.withParsed(ce, L, [], (e) => { try { return size(e.json) <= size(e.simplify().json); } catch { return 'throws'; } }); } catch { return 'no parse'; } };

const ROWS = {
  'functions 4 p-car-park part 2 (want: first four pass, last three fail)': ['2.5t-2', '-2+2.5t', '\\frac{5}{2}t-2', '\\frac{5t}{2}-2', '3+2.5(t-2)', '3+2.5t-5', '2.5(t-2)+3'],
  'functions 4 p-ticket-bonus part 2 (want: first three pass, last fails)': ['5n-100', '-100+5n', '5(n-20)', '0.2(25n-500)'],
  'counting 3 p-sail-ring part 2 (want: first five pass, last fails)': ['\\frac{1}{2}r+\\frac{1}{2}s', '\\frac{1}{2}(r+s)', '(r+s)/2', '0.5r+0.5s', '\\frac{r+s}{2}', 'r+\\frac{1}{2}(s-r)'],
  'counting 3 p-sail-ring part 3 (want: first three pass, last fails)': ['\\frac{1}{3}r+\\frac{1}{3}s', '\\frac{1}{3}(r+s)', '(r+s)/3', '\\frac{2}{3}(\\frac{1}{2}r+\\frac{1}{2}s)'],
  'counting 3 p-sail-ring part 4 (want: first four pass, last two fail)': ['-\\frac{2}{3}r+\\frac{1}{3}s', '\\frac{1}{3}s-\\frac{2}{3}r', '(s-2r)/3', '\\frac{1}{3}(s-2r)', '-r+\\frac{1}{3}r+\\frac{1}{3}s', '\\frac{1}{3}r+\\frac{1}{3}s-r'],
  'other forms a learner may type for the simplified answer (want: all pass)': ['\\frac{5t-4}{2}', '2.50t-2', '2.5t-2.00', '-2+\\frac{5}{2}t', '2.5\\times t-2', '5\\times n-100', '\\frac{s-2r}{3}', '-\\frac{2r}{3}+\\frac{s}{3}', '\\frac{r+s}{3}', '\\frac{r}{3}+\\frac{s}{3}', '\\frac{1}{3}s+\\frac{1}{3}r', '\\frac{-2r+s}{3}'],
};
for (const [k, rows] of Object.entries(ROWS)) {
  console.log(k);
  for (const L of rows) console.log(`   ${String(simplified(L)).padEnd(8)} ${L}`);
}
