#!/usr/bin/env node
/* Problems functions, set 4: what the engine's own graders do with each part (harness of
   docs/reports/problems-equations-4-grade.mjs). Loads app/js/engine/grade.js and the local Compute Engine, then
     numeric     answer inside its own band, every wrong[] outside it and landing on its own key (matchWrong),
                 every TYPED string graded as numeric.js grades it (parseNum, within; a set through numSetGrade)
     expression  answer and every accept[] form grade correct, every wrong[].tex grades wrong and is the first wrong[]
                 it equals (so its byKey line fires), every TYPED string graded as expression.js grades it
   node docs/reports/problems-functions-4-grade.mjs --local-cdn <pkgs>      (from the repo root) */
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
const T = true, F = false;

/* [item, part (1-based), typed text, expected] */
const TYPED = [
  ['p-photo-mount', 1, '22', T], ['p-photo-mount', 1, '22.0', T], ['p-photo-mount', 1, '24', F], ['p-photo-mount', 1, '20', F],
  ['p-photo-mount', 2, '1.5x+4', T], ['p-photo-mount', 2, '4+1.5x', T], ['p-photo-mount', 2, '1.5\\times x+4', T],
  ['p-photo-mount', 2, '\\frac{3}{2}x+4', T], ['p-photo-mount', 2, '3x/2+4', T], ['p-photo-mount', 2, 'y=1.5x+4', T],
  ['p-photo-mount', 2, '1.50x+4', T], ['p-photo-mount', 2, '1.5(x+4)', F], ['p-photo-mount', 2, '1.5x+6', F],
  ['p-photo-mount', 2, '1.5x+2', F], ['p-photo-mount', 2, '1.5x', F], ['p-photo-mount', 2, 'x+4', F],
  ['p-photo-mount', 3, '\\frac{x-4}{1.5}', T], ['p-photo-mount', 3, '(x-4)/1.5', T], ['p-photo-mount', 3, '\\frac{2}{3}(x-4)', T],
  ['p-photo-mount', 3, '\\frac{2x-8}{3}', T], ['p-photo-mount', 3, '(2x-8)/3', T], ['p-photo-mount', 3, '\\frac{x}{1.5}-\\frac{8}{3}', T],
  ['p-photo-mount', 3, 'y=\\frac{x-4}{1.5}', T], ['p-photo-mount', 3, '(x-4)\\div1.5', T],
  ['p-photo-mount', 3, '\\frac{x}{1.5}-4', F], ['p-photo-mount', 3, '\\frac{x+4}{1.5}', F], ['p-photo-mount', 3, '\\frac{x-6}{1.5}', F],
  ['p-photo-mount', 3, '1.5x-4', F], ['p-photo-mount', 3, '\\frac{1}{1.5x+4}', F],
  ['p-photo-mount', 4, '18', T], ['p-photo-mount', 4, '18.0', T], ['p-photo-mount', 4, '16.67', F], ['p-photo-mount', 4, '17', F],
  ['p-photo-mount', 4, '50.5', F],
  ['p-photo-mount', 5, '33', T], ['p-photo-mount', 5, '31', F], ['p-photo-mount', 5, '22', F],
  ['p-fountain-jet', 1, '5.4', T], ['p-fountain-jet', 1, '5.40', T], ['p-fountain-jet', 1, '27/5', T], ['p-fountain-jet', 1, '10.8', F],
  ['p-fountain-jet', 1, '5', F], ['p-fountain-jet', 1, '6', F],
  ['p-fountain-jet', 3, '7.5', T], ['p-fountain-jet', 3, '7.50', T], ['p-fountain-jet', 3, '15/2', T], ['p-fountain-jet', 3, '7 1/2', T],
  ['p-fountain-jet', 3, '4.8', F], ['p-fountain-jet', 3, '6', F], ['p-fountain-jet', 3, '8', F],
  ['p-fountain-jet', 4, '3.75, 11.25', T], ['p-fountain-jet', 4, '11.25, 3.75', T], ['p-fountain-jet', 4, '3.75 and 11.25', T],
  ['p-fountain-jet', 4, 'x = 3.75, x = 11.25', T], ['p-fountain-jet', 4, '15/4, 45/4', T],
  ['p-fountain-jet', 4, '3.75', F], ['p-fountain-jet', 4, '3.8, 11.3', F], ['p-fountain-jet', 4, '4.5, 10.5', F],
  ['p-car-park', 1, '9.25', T], ['p-car-park', 1, '£9.25', T], ['p-car-park', 1, '9.250', T], ['p-car-park', 1, '9.3', F],
  ['p-car-park', 1, '14.25', F],
  ['p-car-park', 2, '2.5t-2', T], ['p-car-park', 2, '-2+2.5t', T], ['p-car-park', 2, '2.50t-2', T], ['p-car-park', 2, '\\frac{5t}{2}-2', T],
  ['p-car-park', 2, '5t/2-2', T], ['p-car-park', 2, '2.5\\times t-2', T], ['p-car-park', 2, 'C=2.5t-2', T],
  ['p-car-park', 2, '3+2.5(t-2)', T], ['p-car-park', 2, '2.5t+1', F], ['p-car-park', 2, '2.5t-5', F], ['p-car-park', 2, '2.5t+3', F],
  ['p-car-park', 2, '2.5t', F], ['p-car-park', 2, '2.5x-2', F],
  ['p-car-park', 3, '5.9', T], ['p-car-park', 3, '5.90', T], ['p-car-park', 3, '59/10', T], ['p-car-park', 3, '6', F],
  ['p-car-park', 3, '4.3', F], ['p-car-park', 3, '7.1', F],
  ['p-car-park', 5, '10.25', T], ['p-car-park', 5, '£10.25', T], ['p-car-park', 5, '10.3', F], ['p-car-park', 5, '12.75', F],
  ['p-ticket-bonus', 1, '20', T], ['p-ticket-bonus', 1, '21', F], ['p-ticket-bonus', 1, '12,500', F],
  ['p-ticket-bonus', 2, '5n-100', T], ['p-ticket-bonus', 2, '-100+5n', T], ['p-ticket-bonus', 2, '5(n-20)', T],
  ['p-ticket-bonus', 2, '0.2(25n-500)', T], ['p-ticket-bonus', 2, '5\\times n-100', T], ['p-ticket-bonus', 2, 'B=5n-100', T],
  ['p-ticket-bonus', 2, '5n-2500', F], ['p-ticket-bonus', 2, '5n-500', F], ['p-ticket-bonus', 2, '5n', F], ['p-ticket-bonus', 2, '25n-500', F],
  ['p-ticket-bonus', 3, '\\frac{b+100}{5}', T], ['p-ticket-bonus', 3, '(b+100)/5', T], ['p-ticket-bonus', 3, '0.2b+20', T],
  ['p-ticket-bonus', 3, 'b/5+20', T], ['p-ticket-bonus', 3, '\\frac{100+b}{5}', T], ['p-ticket-bonus', 3, 'n=\\frac{b+100}{5}', T],
  ['p-ticket-bonus', 3, '\\frac{b}{5}+100', F], ['p-ticket-bonus', 3, '\\frac{b-100}{5}', F], ['p-ticket-bonus', 3, '5b-100', F],
  ['p-ticket-bonus', 3, '\\frac{x+100}{5}', F],
  ['p-ticket-bonus', 4, '28', T], ['p-ticket-bonus', 4, '28.0', T], ['p-ticket-bonus', 4, '32', F], ['p-ticket-bonus', 4, '38', F],
  ['p-ticket-bonus', 4, '21', F],
];

let checks = 0, fails = 0;
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('FAIL    ' + msg); } };

const gradeNumeric = (w, text) => {
  if (G.isSetSpec(w) && w.unordered === true) return !!G.numSetGrade(w, text).ok;
  const v = G.parseNum(text);
  return Number.isFinite(v) && G.within(v, w.answer, w.tol);
};
const fo = (w) => ({ functions: w.functions || [], integers: w.integers || [] });
const eq = (w, a, b) => { try { return !!G.exprEqual(ce, a, b, fo(w)); } catch { return false; } };
const gradeExpr = (w, L) => [w.answer, ...(w.accept || [])].some((k) => eq(w, L, k));

const set = JSON.parse(fs.readFileSync('app/content/courses/functions/problems-4.json', 'utf8'));
for (const it of set.items) it.parts.forEach((p, i) => {
  const w = p.widget, where = `${it.id} part ${i + 1}`;
  const typed = TYPED.filter((r) => r[0] === it.id && r[1] === i + 1);
  if (w.kind === 'numeric') {
    if (!(G.isSetSpec(w) && w.unordered)) {
      say(G.within(w.answer, w.answer, w.tol), `${where}: answer outside its own band`);
      for (const x of w.wrong || []) {
        say(!G.within(x.value, w.answer, w.tol), `${where}: wrong "${x.id}" = ${x.value} is inside the answer band`);
        const m = G.matchWrong(x.value, w.wrong, w.tol);
        say(m && m.id === x.id, `${where}: wrong "${x.id}" lands on ${m && m.id}`);
      }
    } else {
      say(gradeNumeric(w, w.answers.join(', ')), `${where}: the key set does not grade correct`);
      for (const x of w.wrong || []) say(!gradeNumeric(w, x.value), `${where}: wrong set "${x.id}" grades correct`);
    }
    for (const r of typed) say(gradeNumeric(w, r[2]) === r[3], `${where}: typed "${r[2]}" ${r[3] ? 'refused' : 'accepted'}`);
  } else if (w.kind === 'expression') {
    say(gradeExpr(w, w.answer), `${where}: answer does not grade correct`);
    for (const a of w.accept || []) say(gradeExpr(w, a), `${where}: accept "${a}" does not grade correct`);
    for (const x of w.wrong || []) {
      say(!gradeExpr(w, x.tex), `${where}: wrong "${x.id}" ${x.tex} grades correct`);
      const first = (w.wrong || []).find((y) => eq(w, x.tex, y.tex));
      say(first && first.id === x.id, `${where}: wrong "${x.id}" lands on ${first && first.id}`);
    }
    for (const r of typed) say(gradeExpr(w, r[2]) === r[3], `${where}: typed "${r[2]}" ${r[3] ? 'refused' : 'accepted'}`);
  } else {
    say(w.options.filter((o) => o.correct).length === 1, `${where}: not exactly one keyed option`);
  }
});
console.log(`grade-check functions 4: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
