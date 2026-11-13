#!/usr/bin/env node
/* Second read, odes problems-1 to -3: what the engine's own graders do with each typed part (pattern:
   review-problems-analysis-1-3-scripts/grade-probe.mjs). For every numeric and expression part, through the real widget files as tools/grade-all.mjs boots them: the key and each accept grade
   correct, each wrong[] is refused on its own line. Then the reader's own strings (ROWS): T accepted, F refused on no wrong
   line, an id = refused on that wrong line ('count' is the engine's own line for too few values). Numeric fields are plain text, so no TeX rows. Exit 1 on any row that differs from the expectation.

   node docs/reviews/review-problems-odes-1-3-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const ALL = argv.includes('--all');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
/* the fake DOM and the real widget files, as tools/grade-all.mjs boots them */
const stubEl = (html = '') => {
  const memo = new Map();
  const el = {
    _html: html, value: '', hidden: false, textContent: '', innerHTML: '', readOnly: false, className: '', children: [], dataset: {},
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    addEventListener() {}, removeEventListener() {}, setAttribute() {}, getAttribute() { return null; }, append() {}, prepend() {}, focus() {}, remove() {}, insertAdjacentHTML() {},
    querySelector(sel) { if (!memo.has(sel)) memo.set(sel, stubEl()); return memo.get(sel); },
    querySelectorAll() { return []; },
  };
  el.parentElement = html ? null : { classList: el.classList };
  return el;
};
const g = { console, setTimeout, clearTimeout, requestAnimationFrame: (f) => f(), document: { addEventListener() {}, querySelector() { return null; }, createElement: () => stubEl(), head: stubEl() }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { h: (html) => stubEl(String(html)), esc: (x) => String(x), sound() {}, icon: () => '', mathify() {} };
for (const f of ['js/engine/grade.js', 'js/engine/widgets/_base.js', 'js/engine/widgets/expression.js', 'js/engine/widgets/numeric.js']) vm.runInContext(fs.readFileSync(path.join('app', f), 'utf8'), g, { filename: f });
g.ZQ.grade.inline = (x) => String(x);
g.ZQ.grade.maths = () => Promise.resolve({ mathlive: false, ce });
const kinds = g.ZQ.widgets.kinds;
const tick = () => new Promise((r) => setTimeout(r, 0));
const typed = async (spec, text) => {
  const w = kinds[spec.kind](stubEl(), spec, { change() {} });
  w.set(text); await tick();
  const r = await w.grade();
  return { ok: !!r.ok, key: r.key == null ? null : r.key };
};
const fmt = (spec, v) => (spec.unit === '%' ? String(+(+v * 100).toPrecision(15)) : String(v));   // a percentage is typed as 25 for 0.25

const T = true, F = false;
/* ROWS[set][item][part] = [[text, expected], ...] */
const ROWS = {
  1: {
    'p-lending-members': {
      1: [['2, 6', T], ['6, 2', T], ['m = 2, m = 6', T], ['-6, -2', 'signs'], ['8, 0', 'no-constant'], ['2', 'count'], ['2, 4', F]],
      3: [['4', T], ['k = 4', T], ['1', 'no-quarter'], ['0.25', F], ['-4', F]],
      4: [['1/7', T], ['0.1429', T], ['0.14286', T], ['0.143', F], ['0.14', F], ['7', 'inverted'], ['0.2', 'over-m'], ['1/5', 'over-m'], ['1/8', 'gap'], ['0.125', 'gap']],
      5: [['0.761', T], ['0.7611', T], ['0.76', F], ['0.762', F], ['-0.212', 'inverted'], ['-0.2118', 'inverted'], ['3.045', 'no-quarter'], ['3.0445', 'no-quarter'], ['0.677', 'over-m'], ['0.795', 'gap'], ['0.7945', 'gap'], ['0.794', F]],
    },
    'p-moving-target': {
      1: [['e^{1.25t}', T], ['e^{\\frac{5t}{4}}', T], ['\\exp(1.25t)', T], ['\\mu=e^{1.25t}', T], ['e^{-1.25t}', 'sign'], ['e^{1.25}', 'no-t'], ['1.25t', F], ['2e^{1.25t}', F]],
      2: [['2.52+0.6t+2.48e^{-1.25t}', T], ['2.48e^{-1.25t}+0.6t+2.52', T], ['\\frac{63}{25}+\\frac{3}{5}t+\\frac{62}{25}e^{-\\frac{5}{4}t}', T], ['r=2.52+0.6t+2.48e^{-1.25t}', T],
        ['0.6t+2.52+\\frac{2.48}{e^{1.25t}}', T], ['3+0.6t+2e^{-1.25t}', 'no-lag'], ['3.48+0.6t+1.52e^{-1.25t}', 'sign'], ['2.52+0.6t', 'no-start'], ['2.52+0.6t+2.48e^{1.25t}', F], ['2.5+0.6t+2.5e^{-1.25t}', F]],
      3: [['0.5545', T], ['0.55452', T], ['0.555', F], ['0.55', F], ['0.8', 'mean-life'], ['0.8664', 'times'], ['0.866', F]],
      4: [['1.314', T], ['1.3138', T], ['1.31', F], ['1.135', 'no-chain'], ['1.142', 'no-lag'], ['0.922', 'sign'], ['3.788', F]],
    },
    'p-rising-pension': {
      1: [['0.04B+2000e^{0.02t}', T], ['2000e^{0.02t}+0.04B', T], ['\\frac{B}{25}+2000e^{\\frac{t}{50}}', T], ["B'=0.04B+2000e^{0.02t}", T], ['0.04B+2000', 'flat'], ['2000e^{0.02t}', 'no-interest'],
        ['0.02B+2000e^{0.04t}', 'swapped'], ['0.04B+2000(1.02)^t', F], ['4B+2000e^{2t}', F]],
      2: [['e^{-0.04t}', T], ['e^{-\\frac{t}{25}}', T], ['\\frac{1}{e^{0.04t}}', T], ['e^{0.04t}', 'sign'], ['e^{0.02t}', 'forcing'], ['e^{-0.02t}', F]],
      3: [['100000(e^{0.04t}-e^{0.02t})', T], ['100000e^{0.04t}-100000e^{0.02t}', T], ['10^5(e^{t/25}-e^{t/50})', T], ['B=100000(e^{0.04t}-e^{0.02t})', T], ['100000e^{0.02t}(e^{0.02t}-1)', T],
        ['-100000e^{0.02t}', 'no-c'], ['50000(e^{0.04t}-1)', 'flat'], ['100000(e^{0.02t}-e^{0.04t})', 'sign-int'], ['100000(e^{0.04t}-1)', F]],
      4: [['27042', T], ['27,042', T], ['£27,042', T], ['27042.19', T], ['27042.2', T], ['27043', F], ['27040', F], ['27000', F], ['24591', 'flat'], ['24591.23', 'flat'], ['22140', 'no-interest']],
    },
  },
  2: {
    'p-hedge-overshoot': {
      1: [['-2+5i, -2-5i', T], ['-2-5i, -2+5i', T], ['-2\\pm 5i', T], ['r=-2+5i, r=-2-5i', T], ['2+5i, 2-5i', 'sign'], ['-4+10i, -4-10i', 'no-half'], ['-2+5i', 'count'], ['-2+10i, -2-10i', F]],
      2: [['2', T], ['x_p = 2', T], ['58', 'no-divide'], ['29', F]],
      3: [['-0.8', T], ['-4/5', T], ['−0.8', T], ['0', 'no-decay'], ['0.8', 'sign'], ['-2', F]],
      4: [['0.6283', T], ['0.62832', T], ['0.628', F], ['0.63', F], ['1.2566', 'period'], ['0.5834', 'omega0']],
      5: [['28.46', T], ['28.46%', T], ['28.461', T], ['0.2846', F], ['28.5', F], ['28', F], ['-28.46', 'sign'], ['-8.10', 'period'], ['-8.1', 'period'], ['8.10', F], ['128.46', F]],
    },
    'p-cash-buffer': {
      1: [['-2+i, -2-i', T], ['-2\\pm i', T], ['2+i, 2-i', 'sign'], ['-4+2i, -4-2i', 'no-half'], ['-2+2i, -2-2i', F]],
      2: [['1.25', T], ['5/4', T], ['0', 'no-damping'], ['-1.25', 'sign'], ['2.5', F]],
      3: [['-3.75', T], ['-15/4', T], ['-1.25', 'no-decay'], ['1.25', 'sign'], ['3.75', 'drop-sign'], ['-2.5', F]],
      4: [['1.088', T], ['1.0879', T], ['1.09', F], ['1.196', 'no-decay'], ['1.25', 'steady'], ['1.304', 'sign'], ['1.412', F]],
    },
    'p-tracking-gap': {
      1: [['10', T], ['b = 10', T], ['5', 'omega0'], ['100', 'no-root'], ['-10', F]],
      2: [['-5', T], ['r = -5', T], ['5', 'sign'], ['-10', 'no-half']],
      3: [['6', T], ['-4', 'no-r'], ['-14', 'sign'], ['2', F]],
      4: [['0.4104', T], ['0.41043', T], ['0.410', F], ['0.41', F], ['0', 'no-r'], ['-0.4104', 'sign'], ['0.1642', 'no-t']],
    },
  },
  3: {
    'p-yield-gaps': {
      1: [['5', T], ['-19', 'bc-sign'], ['-5', F], ['-6', F]],
      2: [['-1, -5', T], ['-5, -1', T], ['1, 5', 'trace-sign'], ['-1', 'count'], ['-2, -3', F]],
      4: [['-1', T], ['c_1 = -1', T], ['4', 'identity'], ['5', 'swapped'], ['1', 'drop-sign']],
      5: [['3', T], ['3.0', T], ['3/1', T], ['1', 'fast'], ['1/3', 'inverted'], ['0.333', 'inverted'], ['0.5', 'start'], ['1/2', 'start'], ['0', F]],
    },
    'p-liquidity-arbitrage': {
      1: [['(2,4)', T], ['(2, 4)', T], ['\\left(2,4\\right)', T], ['(4,2)', 'swapped'], ['(6,0)', 'boundary'], ['(0,0)', F], ['(2,3)', F]],
      2: [['[[-2,-2],[4,0]]', T], ['[[-2, -2], [4, 0]]', T], ['\\begin{pmatrix}-2&-2\\\\4&0\\end{pmatrix}', T], ['[[0,-2],[4,0]]', 'no-product'], ['[[-2,4],[-2,0]]', 'transpose'], ['[[-2,-2],[4,1]]', F], ['[[2,2],[-4,0]]', F]],
      3: [['-28', T], ['36', 'delta-sign'], ['-4', 'no-four'], ['28', 'drop-sign'], ['-32', F]],
      5: [['2.375', T], ['2.3748', T], ['2.37', F], ['2.38', F], ['2.221', 'centre'], ['1.187', 'no-half'], ['6.283', F]],
    },
    'p-trend-signal': {
      1: [['[[0,1],[5,-4]]', T], ['\\begin{pmatrix}0&1\\\\5&-4\\end{pmatrix}', T], ['[[0,1],[-5,4]]', 'signs'], ['[[0,1],[-4,5]]', 'swapped'], ['[[0,1],[4,-5]]', F], ['[[1,0],[5,-4]]', F]],
      2: [['-5', T], ['5', 'sign'], ['-4', 'trace'], ['0', F]],
      3: [['1, -5', T], ['-5, 1', T], ['-1, 5', 'trace-sign'], ['1, 5', F]],
      4: [['-5', T], ['1', 'unstable'], ['5', 'sign'], ['0', F]],
    },
  },
};

let n = 0, bad = 0, mine = 0;
const out = (ok, s) => { n += 1; if (!ok) bad += 1; if (!ok || ALL) console.log((ok ? 'ok   ' : 'DIFF ') + s); };
for (const set of [1, 2, 3]) {
  const S = JSON.parse(fs.readFileSync(`app/content/courses/odes/problems-${set}.json`, 'utf8'));
  for (const it of S.items) {
    for (const [i, p] of it.parts.entries()) {
      const w = p.widget, tag = `${set} ${it.id} part ${i + 1}`;
      if (w.kind !== 'numeric' && w.kind !== 'expression') continue;
      const gr = (spec, txt) => typed(spec, txt);
      const keyText = w.answers ? w.answers.join(', ') : w.kind === 'numeric' ? fmt(w, w.answer) : String(w.answer);
      let r = await gr(w, keyText); out(r.ok, `${tag} key ${keyText} -> ${JSON.stringify(r)}`);
      for (const a of w.accept || []) { r = await gr(w, a); out(r.ok, `${tag} accept ${a} -> ${JSON.stringify(r)}`); }
      for (const wr of w.wrong || []) {
        const txt = wr.tex != null ? wr.tex : typeof wr.value === 'string' ? wr.value : fmt(w, wr.value);
        r = await gr(w, txt); out(!r.ok && r.key === wr.id, `${tag} wrong ${wr.id} ${txt} -> ${JSON.stringify(r)}`);
        out(!!(p.feedback.byKey || {})[wr.id], `${tag} wrong ${wr.id} has a byKey line`);
      }
      const rows = ((ROWS[set] || {})[it.id] || {})[i + 1] || [];
      for (const [txt, exp] of rows) {
        r = await gr(w, txt); mine += 1;
        const ok = exp === true ? r.ok : exp === false ? (!r.ok && !r.key) : (!r.ok && r.key === exp);
        out(ok, `${tag} reader "${txt}" expected ${exp} -> ${JSON.stringify(r)}`);
      }
    }
  }
}
console.log(`${n - bad} of ${n} checks as expected (${mine} reader rows)`);
process.exit(bad ? 1 : 0);
