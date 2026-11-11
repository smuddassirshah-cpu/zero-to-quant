#!/usr/bin/env node
/* Sizes the open fault in quadratics problems-4 p-windy-ride part 4 (no `form`): which unsimplified entries pass now, and
   which pass under each candidate `form`. Also tries the proposed fix for p-storage-crate part 2 and the `whole` entry for
   p-windy-ride part 1. Prints a table; no exit gate.
   node docs/reviews/review-holes-0.1-0.2-scripts/windy-form.mjs --local-cdn <pkgs>     (from the repo root) */
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
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const gr = (w, t) => { const r = G.exprGrade(ce, w, t, t); return r.ok ? 'ok' : (r.key || 'no'); };

const set = JSON.parse(fs.readFileSync('app/content/courses/quadratics/problems-4.json', 'utf8'));
const windy = set.items.find(i => i.id === 'p-windy-ride'), crate = set.items.find(i => i.id === 'p-storage-crate');

const w4 = windy.parts[3].widget;
const typed = [
  ['\\frac{9v}{16(v-2)}', 'the key'], ['\\frac{9v}{16v-32}', 'accept'], ['\\frac{9v}{-32+16v}', 'right'], ['\\frac{9}{16}\\cdot\\frac{v}{v-2}', 'right, two fractions'],
  ['\\frac{9v}{16}\\cdot\\frac{1}{v-2}', 'right, two fractions'], ['0.5625\\frac{v}{v-2}', 'decimal'],
  ['\\frac{9}{v-2}\\div\\frac{16}{v}', 'the question typed back'], ['\\frac{\\frac{9}{v-2}}{\\frac{16}{v}}', 'fraction over fraction'],
  ['\\frac{9}{v-2}\\times\\frac{v}{16}', 'flipped, not multiplied'], ['\\frac{18v}{32(v-2)}', 'not lowest terms'], ['\\frac{9v^2}{16v(v-2)}', 'v not cancelled'],
  ['\\frac{9v(v-2)}{16(v-2)^2}', 'bracket not cancelled'], ['\\frac{144v}{256(v-2)}', 'not lowest terms'],
];
const forms = [undefined, 'simplified', 'factorised', 'fraction', 'expanded'];
console.log('p-windy-ride part 4: entry | ' + forms.map(f => f || 'no form (now)').join(' | '));
for (const [t, note] of typed) console.log(`  ${t.padEnd(44)} ${note.padEnd(26)} ` + forms.map(f => gr({ ...w4, form: f }, t).padEnd(6)).join(' '));

console.log('\np-windy-ride part 1 with a `whole` wrong entry (review-quadratics-4 finding 8):');
const w1 = windy.parts[0].widget, w1b = { ...w1, wrong: [...w1.wrong, { id: 'whole', tex: '\\frac{25v-32}{v(v-2)}' }] };
for (const t of ['25v-32', '\\frac{25v-32}{v(v-2)}', '\\frac{25v-32}{v^2-2v}', '\\frac{16(v-2)+9v}{v(v-2)}', '25v-18']) console.log(`  ${t.padEnd(32)} now ${gr(w1, t).padEnd(12)} with whole ${gr(w1b, t)}`);

console.log('\np-storage-crate part 2: form now "expanded"; with no form:');
const c2 = crate.parts[1].widget, c2b = { ...c2, form: undefined };
for (const t of ['x^2+2x-3', '(x+3)(x-1)', '(x-1)(x+3)', '\\frac{x^3+4x^2+x-6}{x+2}', '\\frac{(x+2)(x+3)(x-1)}{x+2}', 'x^2+2x+3']) console.log(`  ${t.padEnd(32)} now ${gr(c2, t).padEnd(8)} no form ${gr(c2b, t)}`);
