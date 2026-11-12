#!/usr/bin/env node
/* Does a `unit` on a numeric widget let the learner type the unit the question names? (finding 16)
   node docs/reviews/review-problems-complex-1-3-scripts/unit-probe.mjs      (from the repo root; needs no Compute Engine) */
import fs from 'node:fs';
import vm from 'node:vm';

const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const CASES = [
  [{ kind: 'numeric', answer: 2.819, tol: { abs: 0.001 } }, ['2.819', '2.819 amps', '2.819 A', '2.819A']],
  [{ kind: 'numeric', answer: 2.819, tol: { abs: 0.001 }, unit: 'A' }, ['2.819', '2.819 amps', '2.819 A', '2.819A']],
  [{ kind: 'numeric', answer: 4.243, tol: { abs: 0.001 } }, ['4.243 metres', '4.243 m']],
  [{ kind: 'numeric', answer: 4.243, tol: { abs: 0.001 }, unit: 'm' }, ['4.243', '4.243 metres', '4.243 m', '4.243m']],
  [{ kind: 'numeric', answer: 0.5, tol: { abs: 0.005 }, unit: 'm²' }, ['0.5', '0.5 m²', '0.5 m^2', '0.5 square metres']],
];
for (const [w, ts] of CASES) for (const t of ts) {
  const r = G.numGrade(w, t);
  console.log(`unit ${JSON.stringify(w.unit || null).padEnd(5)} typed "${t}": ${r.ok ? 'accepted' : 'refused'}${r.ok ? '' : ' (' + (r.key || (r.detail && r.detail.value == null ? 'no number read' : 'no line')) + ')'}`);
}
