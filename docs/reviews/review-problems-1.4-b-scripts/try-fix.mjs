#!/usr/bin/env node
/* Second read, elimination and least-squares problem sets: the content fixes proposed in the review, tried on in-memory
   copies of the widgets with the real grader. Nothing is written.
     - `accept` forms for an answer typed as a number times a vector (findings 5, 8, 13)
     - a `normalised` wrong entry on three Gram-Schmidt parts (finding 12)
     - a second value, -10, for the `added` slip of p-hall-drone part 2 (finding 9)
   node docs/reviews/review-problems-1.4-b-scripts/try-fix.mjs --local-cdn <pkgs>      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const widget = (course, n, id, k) => JSON.parse(JSON.stringify(JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8')).items.find(i => i.id === id).parts[k - 1].widget));
const expr = (w, t) => { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null }; };
const num = (w, t) => { const r = G.numGrade(w, t); return { ok: !!r.ok, key: r.key || null }; };
let checks = 0, fails = 0;
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('FAIL ' + msg); } else console.log('ok   ' + msg); };

/* 1. accept forms: [course, set, item, part, accept to add, typed strings that must now pass, strings that must still be refused] */
const ACC = [
  ['elimination', 2, 'p-burning-ethanol', 3, ['\\frac{1}{3}(1, 3, 2, 3)', '(1, 3, 2, 3)/3'], ['\\frac{1}{3}(1,3,2,3)', '\\frac13\\left(1,3,2,3\\right)', '(1,3,2,3)/3'], ['(1,3,2,3)', '3(1,3,2,3)', '\\frac{1}{3}(1,3,2,1)']],
  ['least-squares', 1, 'p-hall-drone', 4, ['\\frac{1}{2}(7, -1, 2)', '0.5(7, -1, 2)'], ['\\frac12(7,-1,2)', '0.5(7,-1,2)', '\\frac{1}{2}\\left(7,-1,2\\right)'], ['(7,-1,2)', '\\frac12(7,1,2)']],
  ['least-squares', 2, 'p-solar-drone', 2, ['2(-2, -1, 1)'], ['2(-2,-1,1)', '2\\left(-2,-1,1\\right)'], ['(-2,-1,1)', '12(-2,-1,1)']],
  ['least-squares', 2, 'p-dye-mix', 2, ['\\frac{1}{7}(6, 2, -3)', '(6, 2, -3)/7'], ['\\frac17(6,2,-3)', '\\frac{1}{7}\\left(6,2,-3\\right)', '(6,2,-3)/7'], ['(6,2,-3)', '7(6,2,-3)', '\\frac17(6,2,3)']],
  ['least-squares', 3, 'p-ramp-ball', 2, ['0.1(5, -8, 3)', '\\frac{1}{10}(5, -8, 3)'], ['0.1(5,-8,3)', '\\frac{1}{10}(5,-8,3)', '\\frac{1}{10}\\left(5,-8,3\\right)'], ['(5,-8,3)', '9.8(5,-8,3)']],
];
for (const [c, n, id, k, add, pass, refuse] of ACC) {
  const w = widget(c, n, id, k);
  w.accept = [...(w.accept || []), ...add];
  for (const t of pass) say(expr(w, t).ok, `${id} ${k}: with the added accept forms, "${t}" is accepted`);
  for (const t of refuse) say(!expr(w, t).ok, `${id} ${k}: "${t}" is still refused (key ${expr(w, t).key})`);
  for (const x of w.wrong) say(expr(w, x.tex).key === x.id, `${id} ${k}: wrong "${x.id}" still lands on its key`);
  say(expr(w, w.answer).ok, `${id} ${k}: the key still grades correct`);
}

/* 2. a `normalised` wrong entry */
const NORM = [
  ['p-crystal-cell', 1, '(2/3, -2/3, -1/3)', ['(2/3,-2/3,-1/3)', '(\\frac23,-\\frac23,-\\frac13)']],
  ['p-crystal-cell', 3, '(1/3, 2/3, -2/3)', ['(1/3,2/3,-2/3)']],
  ['p-rotor-changes', 2, '(-1/2, 1/2, -1/2, 1/2)', ['(-1/2,1/2,-1/2,1/2)', '(-0.5,0.5,-0.5,0.5)']],
];
for (const [id, k, tex, typed] of NORM) {
  const w = widget('least-squares', 1, id, k);
  w.wrong = [...w.wrong, { id: 'normalised', tex }];
  for (const t of typed) say(expr(w, t).key === 'normalised', `${id} ${k}: "${t}" lands on normalised (got ${expr(w, t).key})`);
  for (const x of w.wrong) say(expr(w, x.tex).key === x.id, `${id} ${k}: wrong "${x.id}" lands on its key`);
  say(expr(w, w.answer).ok, `${id} ${k}: the key still grades correct`);
}

/* 3. p-hall-drone part 2: -10 as a second value of the `added` slip */
{
  const w = widget('least-squares', 1, 'p-hall-drone', 2);
  w.wrong = [...w.wrong, { id: 'added-solved', value: -10, tol: { abs: 0 } }];
  say(num(w, '-10').key === 'added-solved' && num(w, '10').key === 'added' && num(w, '2').ok && num(w, '-2').key === 'sign', 'p-hall-drone 2: -10, 10, 2 and -2 each land where they should');
}
console.log(`\ntry-fix: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
