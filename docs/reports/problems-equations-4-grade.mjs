#!/usr/bin/env node
/* Problems equations, set 4: what the engine's own graders do with each part (harness of
   docs/reviews/problems-1.3-c-scripts/grade-check.mjs). Loads app/js/engine/grade.js and the local Compute Engine, then
     numeric     answer inside its own band, every wrong[] outside it, every TYPED string graded as numeric.js grades it
                 (parseNum, within; a set through numSetGrade)
     expression  answer, every accept[] form and every TYPED string graded as expression.js grades it; no wrong[].tex grades correct
   node docs/reports/problems-equations-4-grade.mjs --local-cdn <pkgs>      (from the repo root) */
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

/* [item, part (1-based), typed text, expected] */
const TYPED = [
  ['p-rowing-current', 1, 'b-c=10', true], ['p-rowing-current', 1, 'c=b-10', true], ['p-rowing-current', 1, '10=b-c', true],
  ['p-rowing-current', 1, 'b=c+10', true], ['p-rowing-current', 1, '2b-2c=20', true], ['p-rowing-current', 1, 'b-10=c', true],
  ['p-rowing-current', 1, 'c-b=10', false], ['p-rowing-current', 1, 'b+c=10', false], ['p-rowing-current', 1, 'b-c=14', false],
  ['p-rowing-current', 1, 'b-c', false], ['p-rowing-current', 1, '10', false],
  ['p-rowing-current', 2, '12', true], ['p-rowing-current', 2, 'b = 12', false /* engine: a single numeric field does not drop 'b =' (backlog bullet) */], ['p-rowing-current', 2, '24', false],
  ['p-rowing-current', 3, '2', true], ['p-rowing-current', 3, '-2', false],
  ['p-rowing-current', 4, '3', true], ['p-rowing-current', 4, '3.0', true], ['p-rowing-current', 4, '2.33', false], ['p-rowing-current', 4, '2.63', false],
  ['p-seedling-trays', 1, 'x+8', true], ['p-seedling-trays', 1, 'y=x+8', true], ['p-seedling-trays', 1, '8+x', true],
  ['p-seedling-trays', 1, '8x', false], ['p-seedling-trays', 1, 'x-8', false],
  ['p-seedling-trays', 2, '18', true], ['p-seedling-trays', 2, '20', false],
  ['p-seedling-trays', 3, '62n', true], ['p-seedling-trays', 3, '2n\\times18+26n', true], ['p-seedling-trays', 3, '36n+26n', true],
  ['p-seedling-trays', 3, '18\\cdot2n+26\\cdot n', true], ['p-seedling-trays', 3, 'n\\left(36+26\\right)', true],
  ['p-seedling-trays', 3, '44n', false], ['p-seedling-trays', 3, '35n', false], ['p-seedling-trays', 3, '62', false],
  ['p-seedling-trays', 4, '10', true], ['p-seedling-trays', 4, '5', false],
  ['p-remote-cars', 1, '0, 7', true], ['p-remote-cars', 1, '7, 0', true], ['p-remote-cars', 1, 't = 0 or t = 7', true],
  ['p-remote-cars', 1, '7', false], ['p-remote-cars', 1, '7, 49', false],
  ['p-remote-cars', 2, '49', true], ['p-remote-cars', 2, '14', false],
  ['p-remote-cars', 3, '9', true], ['p-remote-cars', 3, '-9', false],
  ['p-remote-cars', 4, '18', true], ['p-remote-cars', 4, '63', false],
  ['p-salt-solutions', 1, '0.15x+0.4y=125', true], ['p-salt-solutions', 1, '3x+8y=2500', true],
  ['p-salt-solutions', 1, '15x+40y=12500', true], ['p-salt-solutions', 1, '0.4y+0.15x=125', true],
  ['p-salt-solutions', 1, '\\frac{15}{100}x+\\frac{40}{100}y=125', true], ['p-salt-solutions', 1, '0.15x+0.40y=0.25\\cdot500', true],
  ['p-salt-solutions', 1, '0.15x+0.4y=0.25(x+y)', false], ['p-salt-solutions', 1, '15x+40y=125', false],
  ['p-salt-solutions', 1, '0.15x+0.4y=0.25', false], ['p-salt-solutions', 1, '0.4x+0.15y=125', false], ['p-salt-solutions', 1, '0.15x+0.4y', false],
  ['p-salt-solutions', 2, '200', true], ['p-salt-solutions', 2, '300', false],
  ['p-salt-solutions', 3, '300', true], ['p-salt-solutions', 3, '45', false],
  ['p-salt-solutions', 4, '600', true], ['p-salt-solutions', 4, '600 g', false /* engine: trailing unit, BACKLOG-INBOX line 682 */], ['p-salt-solutions', 4, '240', false],
];

let checks = 0, fails = 0;
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('FAIL    ' + msg); } };

const gradeNumeric = (w, text) => {
  if (G.isSetSpec(w) && w.unordered === true) return !!G.numSetGrade(w, text).ok;
  const v = G.parseNum(text);
  return Number.isFinite(v) && G.within(v, w.answer, w.tol);
};
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo); } catch { return false; } };
  return [w.answer, ...(w.accept || [])].some(eq);
};

const set = JSON.parse(fs.readFileSync('app/content/courses/equations/problems-4.json', 'utf8'));
for (const it of set.items) it.parts.forEach((p, i) => {
  const w = p.widget, where = `${it.id} part ${i + 1}`;
  const typed = TYPED.filter((r) => r[0] === it.id && r[1] === i + 1);
  if (w.kind === 'numeric') {
    if (!(G.isSetSpec(w) && w.unordered)) {
      say(G.within(w.answer, w.answer, w.tol), `${where}: answer outside its own band`);
      for (const x of w.wrong || []) say(!G.within(x.value, w.answer, w.tol), `${where}: wrong "${x.id}" = ${x.value} is inside the answer band`);
    } else {
      for (const x of w.wrong || []) say(!gradeNumeric(w, x.value), `${where}: wrong set "${x.id}" grades correct`);
    }
    for (const r of typed) say(gradeNumeric(w, r[2]) === r[3], `${where}: typed "${r[2]}" ${r[3] ? 'refused' : 'accepted'}`);
  } else if (w.kind === 'expression') {
    say(gradeExpr(w, w.answer), `${where}: answer does not grade correct`);
    for (const a of w.accept || []) say(gradeExpr(w, a), `${where}: accept "${a}" does not grade correct`);
    for (const x of w.wrong || []) say(!gradeExpr(w, x.tex), `${where}: wrong "${x.id}" ${x.tex} grades correct`);
    for (const r of typed) say(gradeExpr(w, r[2]) === r[3], `${where}: typed "${r[2]}" ${r[3] ? 'refused' : 'accepted'}`);
  }
});
console.log(`grade-check equations 4: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
