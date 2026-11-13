#!/usr/bin/env node
/* Delta read AD-1: the engine's own graders (app/js/engine/grade.js) on the parts three fix passes changed.
   BASE: every numeric and expression part of the changed items: the stored answer and each accept[] form grade correct;
   each wrong[] entry typed at its stored value is refused and lands on its own id, which has a byKey line.
   TYPED rows [typed, expected]: true (accepted), a wrong id, or null (generic refusal).
   node docs/reports/delta-ad-grade.mjs --local-cdn <pkgs>      (from the repo root) */
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
const num = (w, t) => { const r = w.answers ? G.numSetGrade(w, t) : G.numGrade(w, t); return r.ok ? true : (r.key || null); };
const expr = (w, t) => { let r; try { r = G.exprGrade(ce, w, t, t); } catch (e) { return 'THROW ' + e.message; } return r.ok ? true : (r.key || null); };

const ITEMS = {
  'analysis/problems-4': ['p-cubic-bracket'],
  'analysis/problems-5': ['p-root-sums', 'p-diamond-ball', 'p-accumulated-cubic'],
  'odes/problems-4': ['p-test-rig'],
  'vector-calc/problems-1': ['p-bead-semicircle', 'p-two-routes-cubic', 'p-cubic-potential'],
  'vector-calc/problems-2': ['p-triangle-flux', 'p-cycloid-arch'],
  'vector-calc/problems-3': ['p-saddle-roof', 'p-open-tank'],
};
const TYPED = {
  'p-root-sums': { 1: [['19.3060', true], ['19.306', true], ['16.3060', 'lower'], ['2.1451', 'ninth'], ['19.31', null]],
    2: [['\\frac{27}{n}', true], ['27/n', true], ['\\frac{3}{n}', 'unit-width'], ['\\frac{9}{n}', 'no-height']],
    3: [['18', true], ['27', 'no-coeff'], ['40.5', 'flip']], 4: [['1.3060', true], ['1.306', true], ['3', 'gap'], ['1.6940', 'lower']],
    5: [['541', true], ['540', 'equal'], ['61', 'unit-width'], ['181', 'no-height']] },
  'p-diamond-ball': { 1: [['0.55', true], ['-0.25', 'signs'], ['0.25', 'signs-size'], ['0.4272', 'straight'], ['0.4', 'largest']],
    2: [['0.45', true], ['0.55', 'whole'], ['0.5728', 'straight']],
    3: [['0.3182', true], ['0.31820', true], ['0.6364', 'times'], ['0.45', 'same'], ['0.225', 'half'], ['0.318', null]],
    4: [['0.225', true], ['0.9', 'times'], ['0.3182', 'root-two'], ['0.45', 'same']] },
  'p-accumulated-cubic': { 1: [['\\frac{x^3}{3}-6x^2+27x', true], ['\\frac{x(x-9)^2}{3}', true], ['\\frac13x^3-6x^2+27x', true], ['x^3-6x^2+27x', 'no-third'], ['2x-12', 'derivative']],
    2: [['3, 9', true], ['9, 3', true], ['0, 9', 'zeros-of-big-f'], ['3', 'count']], 3: [['180', true], ['36', 'critical'], ['2430', 'no-third']],
    5: [['1029', true], ['1028', 'round-down'], ['386', 'left-end'], ['15', 'no-bound']] },
  'p-test-rig': { 1: [['\\frac{24}{s+8}', true], ['24/(s+8)', true], ['\\frac{24}{s-8}', 'sign'], ['\\frac{1}{s+8}', 'no-factor']],
    2: [['\\frac{24}{(s+2)(s+4)(s+8)}', true], ['\\frac{24}{(s+8)(s^2+6s+8)}', true], ['\\frac{24}{(s-8)(s+2)(s+4)}', 'carried-sign'], ['\\frac{24}{(s+8)(s-2)(s-4)}', 'root-signs']],
    3: [['-3', true], ['3', 'sign'], ['2', 'other-pole']],
    4: [['2e^{-2t}-3e^{-4t}+e^{-8t}', true], ['e^{-8t}-3e^{-4t}+2e^{-2t}', true], ['2e^{2t}-3e^{4t}+e^{8t}', 'exp-sign'], ['2e^{-2t}+3e^{-4t}+e^{-8t}', 'carried-sign']],
    5: [['0.348', true], ['0.3481', true], ['0.366', 'u-value'], ['0.503', 'time'], ['0.5025', 'time'], ['0.216', 'at-one'], ['0.35', null]] },
  'p-bead-semicircle': { 3: [['252.89', true], ['42.15', 'no-speed'], ['3392.92', 'squared'], ['505.79', 'full-circle']], 4: [['36', true], ['72', 'position'], ['180', 'magnitude']],
    5: [['0.447', true], ['2.236', 'inverse'], ['0.142', 'no-integral'], ['0.894', 'full-circle']] },
  'p-two-routes-cubic': { 1: [['t^4+3t^3+3t^5', true], ['3t^5+t^4+3t^3', true], ['t^4+t^3+t', 'no-dot'], ['t^4+t^3+t^5', 'no-chain']],
    2: [['50.4', true], ['252/5', true], ['12.4', 'no-dot'], ['21.1', null]],
    3: [['50.667', true], ['152/3', true], ['208.904', 'ds'], ['10.667', 'p-only'], ['40', 'q-only'], ['20.667', 'no-four']],
    4: [['-0.2667', true], ['-4/15', true], ['0.2667', 'sign'], ['101.067', 'added']] },
  'p-cubic-potential': { 1: [['(16, 12)', true], ['(10, 12)', 'y-not-squared'], ['(12, 16)', 'swap']], 2: [['6y', true], ['12x^2', 'px'], ['6x', 'qy']],
    3: [['x^4+3xy^2', true], ['3xy^2+x^4', true], ['x^4+6xy^2', 'double'], ['x^4+3x^2y', 'wrong-var']], 4: [['69', true], ['70', 'end-only'], ['123', 'double']] },
  'p-triangle-flux': { 1: [['4x', true], ['2y-1', 'curl'], ['2x', 'only-p']], 2: [['36', true], ['27', 'curl'], ['108', 'rectangle'], ['18', 'only-p']],
    3: [['-18', true], ['18', 'sign'], ['0', 'tangent']], 4: [['54', true], ['18', 'add-edge'], ['36', 'all-out']] },
  'p-cycloid-arch': { 3: [['-\\frac{y^2}{2}', true], ['-y^2/2', true], ['-\\frac12y^2', true], ['\\frac{y^2}{2}', 'sign'], ['-y^2', 'no-half'], ['-\\frac{y^2}{2}+x', 'x-term'], ['x-\\frac{y^2}{2}', 'x-term'],
    ['-\\frac{y^2}{2}+1', 'constant'], ['1-\\frac{y^2}{2}', 'constant']], 5: [['0.833', true], ['5/6', true], ['1.2', 'inverse'], ['1.667', 'no-half']] },
};
let n = 0, bad = 0;
const check = (label, got, want) => { n++; if (got !== want) { bad++; console.log(`FAIL ${label}: got ${JSON.stringify(got)}, expected ${JSON.stringify(want)}`); } };
for (const [file, ids] of Object.entries(ITEMS)) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${file}.json`, 'utf8'));
  for (const id of ids) {
    const item = set.items.find((i) => i.id === id);
    item.parts.forEach((p, k) => {
      const w = p.widget; const lab = `${file} ${id} part ${k + 1}`;
      if (w.kind !== 'numeric' && w.kind !== 'expression') return;
      const gr = w.kind === 'numeric' ? num : expr;
      const by = (p.feedback && p.feedback.byKey) || {};
      if (w.answers) check(`${lab} key`, gr(w, w.answers.join(', ')), true); else check(`${lab} key`, gr(w, String(w.answer)), true);
      if (w.kind === 'expression') for (const a of w.accept || []) check(`${lab} accept ${a}`, gr(w, a), true);
      for (const x of w.wrong || []) { check(`${lab} wrong ${x.id}`, gr(w, String(x.tex ?? x.value)), x.id); check(`${lab} wrong ${x.id} has a line`, x.id in by, true); }
      if (w.answers) check(`${lab} count line`, 'count' in by, true);
      for (const [typed, want] of ((TYPED[id] || {})[k + 1] || [])) check(`${lab} typed ${typed}`, gr(w, typed), want);
    });
  }
}
console.log(`${n} checks, ${bad} failures`);
process.exit(bad ? 1 : 0);
