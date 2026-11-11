#!/usr/bin/env node
/* Delta read, fix passes of problems 1.3 c, 0.2 a, 0.3 a and 0.2 b: what the engine's own graders do with the changed items.
   Pattern: docs/reviews/delta-problems-1.3-ab-scripts/grade.mjs and docs/reviews/problems-0.2-b-scripts/grade-check.mjs
   (app/js/engine/grade.js with the local Compute Engine; the grading steps of numeric.js and expression.js, the shape check
   being expression.js formOk for "expanded", "factorised", "factorised-fully", "completed-square" and "simplified").
   For every part of the 42 changed items: the answer and each accept[] form grade correct, each wrong[] entry grades to its
   own id and has a byKey line, no wrong value sits in the answer band, no two bands of a part meet.
   TYPED rows (typed.mjs): [course, set, item, part, typed, expected, note?]; expected is true (accepted), false (refused, any
   line) or the key the typed value should be given ("form", "count" or a wrong[] id). A row with a note is one the reader
   records as a finding: it prints as FINDING and does not fail. --show prints what every typed row did.

   node docs/reviews/delta-problems-aa-2-scripts/grade.mjs --local-cdn <pkgs> [--show]      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { ITEMS, TYPED } from './typed.mjs';

const argv = process.argv.slice(2);
const SHOW = argv.includes('--show');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = {}; vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (finding) { findings++; console.log((ok ? 'FINDING ' : 'FAIL    ') + msg + '   [' + finding + ']'); if (!ok) fails++; return; } if (!ok) { fails++; console.log('FAIL    ' + msg); } };

const isSet = (w) => G.isSetSpec(w) && w.unordered === true;
const gradeNumeric = (w, text) => {
  if (isSet(w)) { const r = G.numSetGrade(w, text); return r.ok ? true : (r.key || null); }
  let v = G.parseNum(text);
  if (w.unit === '%' && !text.includes('%')) v = v / 100;
  if (!Number.isFinite(v)) return 'NOPARSE';
  if (G.within(v, +w.answer, w.tol)) return true;
  const m = G.matchWrong(v, w.wrong, { abs: 1e-9 });
  return m ? m.id : null;
};
const head = (j) => (Array.isArray(j) ? j[0] : null), args = (j) => (Array.isArray(j) ? j.slice(1) : []);
const hasSum = (j) => head(j) === 'Add' || head(j) === 'Subtract' || args(j).some(hasSum);
const size = (j) => (Array.isArray(j) ? 1 + args(j).reduce((a, x) => a + size(x), 0) : 1);
const isSumLike = (j) => head(j) === 'Add' || head(j) === 'Subtract';
const formOk = (w, L) => {
  if (!w.form) return true;
  try {
    return G.withParsed(ce, L, w.functions || [], (e) => {
      const j = e.json;
      if (w.form === 'expanded') return isSumLike(j) ? args(j).every((t) => !hasSum(t)) : !hasSum(j);
      if (w.form === 'factorised') return G.shapeFactorised(j);
      if (w.form === 'factorised-fully') return G.shapeFullyFactorised(j);
      if (w.form === 'completed-square') return G.shapeCompletedSquare(j);
      if (w.form === 'simplified') { try { return size(j) <= size(e.simplify().json); } catch { return true; } }
      throw new Error('form not modelled: ' + w.form);
    });
  } catch (err) { if (/not modelled/.test(err.message)) throw err; return true; }
};
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => {
    try { if (w.upToConstant ? G.exprEqualUpToConstant(ce, L, t, fo) : G.exprEqual(ce, L, t, fo)) return true; } catch { /* fall to text */ }
    return !!G.normExpr(L) && G.normExpr(L) === G.normExpr(t);
  };
  if ([w.answer, ...(w.accept || [])].some(eq)) return formOk(w, L) ? true : 'form';
  const x = (w.wrong || []).find((y) => y.tex && eq(y.tex));
  if (x) return x.id;
  try { if (G.exprShapeLine(ce, w.answer, L, fo.functions)) return 'length'; } catch { /* none */ }
  return null;
};

const used = new Set();
let nItems = 0, nParts = 0;
for (const [course, n, id] of ITEMS) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  const it = set.items.find((x) => x.id === id);
  if (!it) { fails++; console.log(`FAIL    no item ${course} ${n} ${id}`); continue; }
  nItems++;
  it.parts.forEach((p, i) => {
    nParts++;
    const w = p.widget, where = `${course} ${n} ${id} part ${i + 1}`, by = (p.feedback && p.feedback.byKey) || {};
    const typed = TYPED.filter((r) => r[0] === course && r[1] === n && r[2] === id && r[3] === i + 1);
    typed.forEach((r) => used.add(r));
    const judge = (grade) => {
      for (const r of typed) {
        const got = grade(w, r[4]);
        if (SHOW || r[5] === '?') console.log(`      ${where}: "${r[4]}" -> ${JSON.stringify(got)}`);
        if (r[5] === '?') continue;
        const ok = r[5] === false ? got !== true : got === r[5];
        say(ok, r[6], `${where}: typed "${r[4]}" -> ${JSON.stringify(got)}, expected ${JSON.stringify(r[5])}`);
      }
    };
    for (const x of w.wrong || []) say(!!by[x.id], null, `${where}: wrong "${x.id}" has no byKey line`);
    if (w.kind === 'numeric' && isSet(w)) {
      say(gradeNumeric(w, w.answers.join(', ')) === true, null, `${where}: set answer does not grade correct`);
      say(gradeNumeric(w, w.answers.slice().reverse().join(', ')) === true, null, `${where}: set answer reversed does not grade correct`);
      for (const x of w.wrong || []) say(gradeNumeric(w, String(x.value)) === x.id, null, `${where}: wrong "${x.id}" ${x.value} grades ${gradeNumeric(w, String(x.value))}`);
      say(!!by.count, null, `${where}: no "count" line`);
      judge(gradeNumeric);
    } else if (w.kind === 'numeric') {
      const band = (v, t) => { const a = (t && t.abs) || 0; return [v - a, v + a]; };
      say(G.within(+w.answer, +w.answer, w.tol), null, `${where}: answer outside its own band`);
      const bands = [['answer', band(+w.answer, w.tol)], ...(w.wrong || []).map((x) => [x.id, band(+x.value, x.tol || { abs: 1e-9 })])];
      for (let a = 0; a < bands.length; a++) for (let b = a + 1; b < bands.length; b++) say(bands[a][1][1] < bands[b][1][0] || bands[b][1][1] < bands[a][1][0], null, `${where}: bands "${bands[a][0]}" and "${bands[b][0]}" meet`);
      for (const x of w.wrong || []) say(gradeNumeric(w, String(x.value)) === x.id, null, `${where}: wrong "${x.id}" = ${x.value} grades ${gradeNumeric(w, String(x.value))}`);
      judge(gradeNumeric);
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer) === true, null, `${where}: answer does not grade correct (${gradeExpr(w, w.answer)})`);
      for (const a of w.accept || []) say(gradeExpr(w, a) === true, null, `${where}: accept "${a}" does not grade correct (${gradeExpr(w, a)})`);
      for (const x of w.wrong || []) say(gradeExpr(w, x.tex) === x.id, null, `${where}: wrong "${x.id}" ${x.tex} grades ${gradeExpr(w, x.tex)}`);
      if (w.form) say(!!by.form, null, `${where}: form "${w.form}" with no "form" line`);
      judge(gradeExpr);
    } else if (w.kind === 'choice') {
      say((w.options || []).filter((o) => o.correct).length === 1, null, `${where}: not exactly one correct option`);
      if (typed.length) { fails++; console.log(`FAIL    ${where}: typed rows on a choice part`); }
    }
  });
}
for (const r of TYPED) if (!used.has(r)) { fails++; console.log('FAIL    row not used: ' + r.slice(0, 5).join(' ')); }
console.log(`grade.mjs: ${nItems} items, ${nParts} parts, ${TYPED.length} typed rows; ${checks} checks, ${fails} failures, ${findings} finding rows`);
process.exit(fails ? 1 : 0);
