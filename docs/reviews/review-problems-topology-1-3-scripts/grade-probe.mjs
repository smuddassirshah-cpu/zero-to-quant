#!/usr/bin/env node
/* Second read, topology problems-1 to -3: the engine's own graders on each typed part.
   node docs/reviews/review-problems-topology-1-3-scripts/grade-probe.mjs <pkgs>      (from the repo root)
   Rows: T accepted, F refused on the generic line, an id = refused on that slip line. A 3-place rounding of a 4-place key is refused (F), as the stems ask. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const cdn = process.argv[2];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return { ok: !!r.ok, key: r.key || null }; };
const expr = (w, t) => { try { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null }; } catch (e) { return { ok: false, key: 'THROW ' + e.message }; } };
const T = true, F = false;
const ROWS = {
  'p-plotter-zone': { 1: [['\\frac{2}{3}\\varepsilon', T], ['\\frac{2\\epsilon}{3}', T], ['\\varepsilon\\div 1.5', T], ['0.6667\\varepsilon', F], ['\\frac{2}{3}', F]],
    2: [['8/3', T], ['2.667', F], ['2.67', F]], 3: [['1.193', F], ['5.9629', 'multiplied'], ['5.96292', F], ['0.8889', 'used-three']],
    4: [['1.265', T], ['1.2649', T], ['1.26', F]] },
  'p-cubic-band': { 1: [['6', T], ['6.0000', T]], 4: [['2.1962', T], ['2.196', F], ['2.2', F]] },
  'p-diagonal-sphere': { 1: [['1.609', T], ['1.6090', T], ['1.6091', T], ['1.61', F]], 3: [['0.0808', T], ['0.081', F]],
    4: [['0.0571', T], ['0.05713', T], ['0.1143', 'times-root'], ['0.11427', 'times-root'], ['0.1142', 'times-root']] },
  'p-reciprocal-room': { 1: [['4/15', T], ['0.2667', T], ['0.267', F]], 2: [['0.1', T], ['1/10', T], ['.1', T]],
    3: [['\\frac12-\\frac{1}{2+\\varepsilon}', T], ['\\frac{\\varepsilon}{2\\varepsilon+4}', T], ['\\frac{\\epsilon}{2(2+\\epsilon)}', T], ['\\frac{1}{2}\\cdot\\frac{\\varepsilon}{2+\\varepsilon}', T], ['0.1', F]],
    4: [['0.5', T], ['1/2', T]] },
  'p-bond-yield-map': { 1: [['\\frac{100-P}{P}', T], ['100P^{-1}-1', T], ['\\frac{100}{p}-1', T], ['y=\\frac{100}{P}-1', T], ['\\frac{100}{1+P}', F]],
    2: [['95.2381', T], ['95.24', F], ['98.0392', 'upper-end'], ['95', 'linear']], 3: [['0.0309', T], ['3/97', T], ['0.031', T], ['0.03', 'linear'], ['0.0300', 'linear']] },
  'p-quadratic-iteration': { 2: [['2/3', T], ['0.6667', T], ['0.667', F], ['0.67', F]], 5: [['1/3', T], ['0.3333', T], ['0.333', F]] },
  'p-input-output': { 4: [['8.2609', T], ['8.261', F], ['190/23', T], ['8.26', F]] },
  'p-cube-delta': { 3: [['\\frac{1}{12}\\varepsilon', T], ['\\frac{\\epsilon}{12}', T], ['\\varepsilon\\div 12', T], ['\\frac{\\varepsilon}{12.0}', T]], 4: [['5.7685', T], ['5.769', F], ['5.77', F], ['5.7735', 'slope-only']] },
};
let checks = 0, fails = 0, rows = 0;
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('ROW ' + msg); } };
for (const n of [1, 2, 3]) {
  const d = JSON.parse(fs.readFileSync(`app/content/courses/topology/problems-${n}.json`, 'utf8'));
  for (const it of d.items) it.parts.forEach((p, j) => {
    const w = p.widget, tag = `problems-${n} ${it.id} part ${j + 1}`;
    if (w.kind === 'choice') return;
    const run = w.kind === 'numeric' ? num : expr;
    if (w.kind === 'numeric') {
      const k = Number.isInteger(w.answer) ? String(w.answer) : w.answer.toFixed(4);
      say(run(w, k).ok, `${tag}: key ${k} refused`);
      say(run(w, k.replace('-', '−')).ok, `${tag}: key with a true minus refused`);
      for (const x of w.wrong || []) { const r = run(w, String(x.value)); say(!r.ok && r.key === x.id, `${tag}: wrong ${x.id} ${x.value} -> ${JSON.stringify(r)}`); }
    } else {
      for (const t of [w.answer, ...(w.accept || [])]) say(run(w, t).ok, `${tag}: form ${t} refused`);
      for (const x of w.wrong || []) { const r = run(w, x.tex); say(!r.ok && r.key === x.id, `${tag}: wrong ${x.id} -> ${JSON.stringify(r)}`); }
    }
    for (const [t, want] of ((ROWS[it.id] || {})[j + 1] || [])) {
      rows++;
      const r = run(w, t);
      const ok = want === true ? r.ok : want === false ? (!r.ok && !r.key) : (!r.ok && r.key === want);
      say(ok, `${tag}: "${t}" expected ${want}, got ${JSON.stringify(r)}`);
    }
  });
}
console.log(`grade-probe: ${checks} checks, ${rows} reader rows, ${fails} ROW line(s)`);
