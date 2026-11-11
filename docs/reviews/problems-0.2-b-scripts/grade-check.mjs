#!/usr/bin/env node
/* Second read, problems 0.2 (b): what the engine's own graders do with each part of quadratics 1 to 3 and equations 4.
   Harness as problems-0.2-a-scripts/grade-check.mjs (app/js/engine/grade.js and the local Compute Engine). The shape check is
   the expression widget's formOk (app/js/engine/widgets/expression.js) for "expanded", "factorised", "factorised-fully",
   "completed-square" and "simplified". Typed rows live in typed.mjs.
   Every answer and accept[] form must grade correct, every wrong[] must grade wrong and land on its own key, and every TYPED
   row must grade as expected. A TYPED row with a 7th field is one the reader holds to be a fault: it prints as FINDING.
   --show prints what every typed row did.

   node docs/reviews/problems-0.2-b-scripts/grade-check.mjs --local-cdn <pkgs>      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { TYPED } from './typed.mjs';

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

const SETS = [['quadratics', 1], ['quadratics', 2], ['quadratics', 3], ['equations', 4]];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (ok) return; if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };

const isSet = (w) => G.isSetSpec(w) && w.unordered === true;
const gradeNumeric = (w, text) => {
  if (isSet(w)) { const r = G.numSetGrade(w, text); return { ok: !!r.ok, key: r.key }; }
  const pct = w.unit === '%';
  let v = G.parseNum(text); if (pct && !text.includes('%')) v /= 100;
  if (!Number.isFinite(v)) return { ok: false, key: 'NOPARSE' };
  if (G.within(v, w.answer, w.tol)) return { ok: true, key: null };
  const m = G.matchWrong(v, w.wrong, w.tol); return { ok: false, key: m ? m.id : null };
};
/* the widget's shape check (expression.js formOk), for the three forms these sets use */
const head = (j) => (Array.isArray(j) ? j[0] : null), args = (j) => (Array.isArray(j) ? j.slice(1) : []);
const hasSum = (j) => head(j) === 'Add' || head(j) === 'Subtract' || args(j).some(hasSum);
const size = (j) => (Array.isArray(j) ? 1 + args(j).reduce((a, x) => a + size(x), 0) : 1);
const isSumLike = (j) => head(j) === 'Add' || head(j) === 'Subtract';
const formOk = (w, L) => {
  if (!w.form) return true;
  try {
    return G.withParsed(ce, L, w.functions || [], (e) => {
      const j = e.json;
      if (w.form === 'expanded') return isSumLike(j) ? args(j).every(t => !hasSum(t)) : !hasSum(j);
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
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo) || (!!G.normExpr(L) && G.normExpr(L) === G.normExpr(t)); } catch { return false; } };
  const same = [w.answer, ...(w.accept || [])].some(eq);
  if (same) return formOk(w, L) ? { ok: true, key: null } : { ok: false, key: 'form' };
  const x = (w.wrong || []).find(x => x.tex && eq(x.tex));
  return { ok: false, key: x ? x.id : null };
};

for (const [course, n] of SETS) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${course} ${n} ${it.id} part ${i + 1}`, by = (p.feedback && p.feedback.byKey) || {};
    const typed = TYPED.filter((r) => r[0] === course && r[1] === n && r[2] === it.id && r[3] === i + 1);
    const row = (r, res) => { if (SHOW) console.log(`      ${where}: "${r[4]}" -> ${res.ok ? 'correct' : 'wrong'} (key ${res.key})`); say(res.ok === r[5], r[6], `${where}: typed "${r[4]}" ${r[5] ? 'refused' : 'accepted'} (key ${res.key})`); };
    const wrongs = (grade) => {
      for (const x of w.wrong || []) {
        const r = grade(x);
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value ?? x.tex} grades ${r.ok ? 'correct' : 'to key ' + r.key}`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has no byKey line`);
      }
    };
    if (w.kind === 'numeric' && isSet(w)) {
      say(gradeNumeric(w, w.answers.join(', ')).ok, null, `${where}: set answer does not grade correct`);
      say(gradeNumeric(w, w.answers.slice().reverse().join(', ')).ok, null, `${where}: set answer reversed does not grade correct`);
      wrongs((x) => gradeNumeric(w, String(x.value)));
      say(!!by.count, null, `${where}: no "count" line`);
      for (const r of typed) row(r, gradeNumeric(w, r[4]));
    } else if (w.kind === 'numeric') {
      say(G.within(w.answer, w.answer, w.tol), null, `${where}: answer outside its own band`);
      wrongs((x) => gradeNumeric(w, String(x.value)));
      for (const x of w.wrong || []) { const t = (x.tol && x.tol.abs) || 0; if (t > 0 && Math.abs(x.value) > 0 && t > 0.2 * Math.abs(x.value)) console.log(`NOTE    ${where}: wrong "${x.id}" = ${x.value} has band ±${t}, wider than 20% of the value`); }
      for (const r of typed) row(r, gradeNumeric(w, r[4]));
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer).ok, null, `${where}: answer does not grade correct (${JSON.stringify(gradeExpr(w, w.answer))})`);
      for (const a of w.accept || []) say(gradeExpr(w, a).ok, null, `${where}: accept "${a}" does not grade correct (${JSON.stringify(gradeExpr(w, a))})`);
      wrongs((x) => gradeExpr(w, x.tex));
      if (w.form) say(!!by.form, null, `${where}: form "${w.form}" with no "form" line`);
      for (const r of typed) row(r, gradeExpr(w, r[4]));
    }
  });
}
console.log(`grade-check: ${checks} checks, ${fails} failures, ${findings} findings (rows the reader holds to be faults)`);
process.exit(fails ? 1 : 0);
