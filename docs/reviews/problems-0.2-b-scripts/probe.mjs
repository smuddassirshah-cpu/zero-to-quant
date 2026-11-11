#!/usr/bin/env node
/* Probe for the proposed fixes: grade typed strings against an ad hoc expression spec with the engine's own graders.
   node docs/reviews/problems-0.2-b-scripts/probe.mjs --local-cdn <pkgs>      (from the repo root)
   Each row: [label, spec, typed, expected ok, expected key]. Exit 1 on any mismatch. */
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

const head = (j) => (Array.isArray(j) ? j[0] : null), args = (j) => (Array.isArray(j) ? j.slice(1) : []);
const hasSum = (j) => head(j) === 'Add' || head(j) === 'Subtract' || args(j).some(hasSum);
const size = (j) => (Array.isArray(j) ? 1 + args(j).reduce((a, x) => a + size(x), 0) : 1);
const isSumLike = (j) => head(j) === 'Add' || head(j) === 'Subtract';
const formOk = (w, L) => {
  if (!w.form) return true;
  try {
    return G.withParsed(ce, L, [], (e) => {
      const j = e.json;
      if (w.form === 'expanded') return isSumLike(j) ? args(j).every(t => !hasSum(t)) : !hasSum(j);
      if (w.form === 'factorised') return G.shapeFactorised(j);
      if (w.form === 'factorised-fully') return G.shapeFullyFactorised(j);
      if (w.form === 'completed-square') return G.shapeCompletedSquare(j);
      if (w.form === 'simplified') { try { return size(j) <= size(e.simplify().json); } catch { return true; } }
      throw new Error('form not modelled');
    });
  } catch (err) { if (/not modelled/.test(err.message)) throw err; return true; }
};
const grade = (w, L) => {
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, {}) || (!!G.normExpr(L) && G.normExpr(L) === G.normExpr(t)); } catch { return false; } };
  if ([w.answer, ...(w.accept || [])].some(eq)) return formOk(w, L) ? { ok: true, key: null } : { ok: false, key: 'form' };
  const x = (w.wrong || []).find(x => x.tex && eq(x.tex));
  return { ok: false, key: x ? x.id : null };
};

const SALT = { answer: '0.15x+0.4y=125', accept: ['3x+8y=2500'], wrong: [{ id: 'both-letters', tex: '0.15x+0.4y=0.25(x+y)' }, { id: 'per-cent', tex: '15x+40y=125' }] };
const ROWS = [
  // would form "simplified" close the uncollected line on the two "expanded and simplified" parts? It lets the brackets through.
  ['cinema 1 with form simplified', { answer: 'x^2+11x+24', form: 'simplified' }, 'x^2+8x+3x+24', false, 'form'],
  ['cinema 1 with form simplified', { answer: 'x^2+11x+24', form: 'simplified' }, '(x+3)(x+8)', true, null],
  ['cinema 1 with form simplified', { answer: 'x^2+11x+24', form: 'simplified' }, 'x^2+11x+24', true, null],
  // finding on salt part 1: a wrong[] entry catches the two-letter right-hand side and gives it its own line
  ['salt 1 with wrong both-letters', SALT, '0.15x+0.4y=0.25(x+y)', false, 'both-letters'],
  ['salt 1 with wrong both-letters', SALT, '15x+40y=25(x+y)', false, 'both-letters'],
  ['salt 1 with wrong both-letters', SALT, '\\frac{0.15x+0.4y}{x+y}=0.25', false, null],
  ['salt 1 with wrong both-letters', SALT, '0.15x+0.4y=125', true, null],
  ['salt 1 with wrong both-letters', SALT, '15x+40y=125', false, 'per-cent'],
];
let bad = 0;
for (const [label, w, L, ok, key] of ROWS) {
  const r = grade(w, L);
  const fine = r.ok === ok && r.key === key;
  if (!fine) bad++;
  console.log(`${fine ? 'ok  ' : 'DIFF'} ${label}: "${L}" -> ${r.ok ? 'correct' : 'wrong'} (key ${r.key})`);
}
console.log(`probe: ${ROWS.length} rows, ${bad} not as expected`);
process.exit(bad ? 1 : 0);
