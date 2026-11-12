#!/usr/bin/env node
/* Second read, vectors problems-1 to -3: what the engine's own graders do with each typed part.
   Loads app/js/engine/grade.js and the local Compute Engine, then
     numeric     numGrade: the answer grades correct; every wrong[] is refused on its own key and has a byKey line; TYPED rows
     expression  exprGrade (the call expression.js makes): the answer and every accept[] grade correct; every wrong[].tex is refused
                 on its own key and has a byKey line; then a fixed list of other ways to type the same vector or matrix (FORMS) and
                 of near misses (the entries reversed, the matrix transposed, a flat row where a matrix is meant)
   TYPED rows: [set, item, part (1-based), text, expected (true accepted, false refused, a wrong id, or 'NONE' for refused on no
   wrong line), finding?]; a row with a 6th field is one the reader holds to be a fault (printed, not a failure).
   A FORMS result against the reader prints as FORM and is counted; the review decides which of those are faults.

   node docs/reviews/review-problems-1.4-a-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const ALL = argv.includes('--all');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

const num = (w, text) => { const r = G.numGrade(w, text); return { ok: !!r.ok, key: r.key || (r.detail.value == null ? 'NOPARSE' : null) }; };
const expr = (w, L) => { try { const r = G.exprGrade(ce, w, L, L); return { ok: !!r.ok, key: r.key || null, line: r.line }; } catch (e) { return { ok: false, key: 'THROW ' + e.message }; } };

/* the entries of a stored answer: "(a, b, c)" gives [[a], [b], [c]] read as a vector; a pmatrix gives its rows */
const entries = (ans) => {
  const m = /\\begin\{pmatrix\}(.*)\\end\{pmatrix\}/.exec(ans);
  if (m) return { matrix: true, rows: m[1].split('\\\\').map(r => r.split('&').map(s => s.trim())) };
  return { matrix: false, v: ans.replace(/^\(|\)$/g, '').split(',').map(s => s.trim()) };
};
const lb = '\\left\\lbrack', rb = '\\right\\rbrack';
const vecForms = (v) => ({
  'round, no space': [`(${v.join(',')})`, true],
  'round, MathLive \\left( \\right)': [`\\left(${v.join(',')}\\right)`, true],
  'square brackets': [`[${v.join(', ')}]`, true],
  'square, MathLive \\lbrack': [`${lb}${v.join(',')}${rb}`, true],
  'angle brackets': [`\\langle ${v.join(', ')}\\rangle`, true],
  'column pmatrix': [`\\begin{pmatrix}${v.join('\\\\')}\\end{pmatrix}`, true],
  'row pmatrix': [`\\begin{pmatrix}${v.join('&')}\\end{pmatrix}`, true],
  'column bmatrix': [`\\begin{bmatrix}${v.join('\\\\')}\\end{bmatrix}`, true],
  'no brackets': [v.join(', '), true],
  'semicolons': [`(${v.join('; ')})`, true],
  'curly braces (a set, not a vector)': [`\\left\\lbrace ${v.join(',')}\\right\\rbrace`, false],
  'entries reversed': [`(${[...v].reverse().join(', ')})`, v.join() === [...v].reverse().join()],
  'one entry short': [v.length > 2 ? `(${v.slice(0, -1).join(', ')})` : `${v[0]}`, false],
});
const matForms = (rows) => {
  const T = rows[0].map((_, j) => rows.map(r => r[j]));
  const sym = JSON.stringify(T) === JSON.stringify(rows);
  return {
    'as asked [[a, b], [c, d]]': [`[[${rows.map(r => r.join(', ')).join('], [')}]]`, true],
    'as asked, no spaces': [`[[${rows.map(r => r.join(',')).join('],[')}]]`, true],
    'as asked, MathLive \\lbrack': [`${lb}${rows.map(r => `${lb}${r.join(',')}${rb}`).join(',')}${rb}`, true],
    'round ((a, b), (c, d))': [`((${rows.map(r => r.join(', ')).join('), (')}))`, true],
    'round, MathLive \\left(': [`\\left(${rows.map(r => `\\left(${r.join(',')}\\right)`).join(',')}\\right)`, true],
    'square outside, round rows': [`[(${rows.map(r => r.join(', ')).join('), (')})]`, true],
    'bmatrix': [`\\begin{bmatrix}${rows.map(r => r.join('&')).join('\\\\')}\\end{bmatrix}`, true],
    'pmatrix, spaced': [`\\begin{pmatrix} ${rows.map(r => r.join(' & ')).join(' \\\\ ')} \\end{pmatrix}`, true],
    'rows split by semicolon [a, b; c, d]': [`[${rows.map(r => r.join(', ')).join('; ')}]`, true],
    'rows with no outer bracket [a, b], [c, d]': [`[${rows.map(r => r.join(', ')).join('], [')}]`, true],
    'transposed': [`[[${T.map(r => r.join(', ')).join('], [')}]]`, sym],
    'flat row (a, b, c, d)': [`(${rows.flat().join(', ')})`, false],
  };
};

const T = true, F = false;
const MAT = 'a wrong matrix typed in the form the question asks for never reaches its `wrong` line: key "length", line "That is a single value. The answer has 2 rows and 2 columns."';
const RIGHTM = 'a right matrix in the asked form with one entry written another way is refused, with the same "single value" line';
const SCAL = 'the right answer as a scalar times a vector or matrix (the form the working gives) is refused';
const DEC = 'a "Give a percentage" part refuses the same value typed as the decimal the working gives, with the generic line';
const TYPED = [
  // problems-1
  [1, 'p-charging-robot', 1, 'a=2, b=3', F], [1, 'p-charging-robot', 1, '(3, 2)', 'swapped'], [1, 'p-charging-robot', 1, '(2, 3, 0)', 'length'],
  [1, 'p-charging-robot', 2, '30', T], [1, 'p-charging-robot', 2, '30.0', T], [1, 'p-charging-robot', 2, '5', 'unweighted'], [1, 'p-charging-robot', 2, '10', 'only-u'], [1, 'p-charging-robot', 2, '15', 'only-v'], [1, 'p-charging-robot', 2, '6', F],
  [1, 'p-charging-robot', 3, '45', T], [1, 'p-charging-robot', 3, '45°', T], [1, 'p-charging-robot', 3, '45 degrees', T], [1, 'p-charging-robot', 3, '45.0', T], [1, 'p-charging-robot', 3, '44.9', T], [1, 'p-charging-robot', 3, '0.785', 'radians'], [1, 'p-charging-robot', 3, '0.79', 'radians'],
  [1, 'p-charging-robot', 3, '\\pi/4', F], [1, 'p-charging-robot', 3, '89', 'no-root'], [1, 'p-charging-robot', 3, '135', F], [1, 'p-charging-robot', 3, '46', F],
  [1, 'p-charging-robot', 4, '12.04', T], [1, 'p-charging-robot', 4, '12.04 m', T], [1, 'p-charging-robot', 4, '12.04m', T], [1, 'p-charging-robot', 4, '12.042', T], [1, 'p-charging-robot', 4, '12.04 metres', T], [1, 'p-charging-robot', 4, '12.0', F], [1, 'p-charging-robot', 4, '12', F], [1, 'p-charging-robot', 4, '12.1', F],
  [1, 'p-charging-robot', 4, '12.03', T], [1, 'p-charging-robot', 4, '12.06', F], [1, 'p-charging-robot', 4, '9.22', 'no-cross'], [1, 'p-charging-robot', 4, '13.03', 'path'], [1, 'p-charging-robot', 4, '5', 'minus'], [1, 'p-charging-robot', 4, '145', 'no-root'],
  [1, 'p-active-bets', 2, '-0.55', T], [1, 'p-active-bets', 2, '-0.55%', T], [1, 'p-active-bets', 2, '−0.55', T], [1, 'p-active-bets', 2, '-0.550', T], [1, 'p-active-bets', 2, '-0.55 %', T], [1, 'p-active-bets', 2, '-0.6', F], [1, 'p-active-bets', 2, '-0.0055', T, DEC],
  [1, 'p-active-bets', 2, '0.55', 'flipped'], [1, 'p-active-bets', 2, '0.95', 'fund'], [1, 'p-active-bets', 2, '1.5', 'benchmark'], [1, 'p-active-bets', 2, '1.50%', 'benchmark'],
  [1, 'p-active-bets', 3, '0.1871', T], [1, 'p-active-bets', 3, '0.18708', T], [1, 'p-active-bets', 3, '0.187', T], [1, 'p-active-bets', 3, '0.19', F], [1, 'p-active-bets', 3, '0.1870', T], [1, 'p-active-bets', 3, '18.71%', T], [1, 'p-active-bets', 3, '0.035', 'no-root'], [1, 'p-active-bets', 3, '0.3', 'abs-sum'], [1, 'p-active-bets', 3, '0', 'sum'],
  [1, 'p-active-bets', 4, '130', T], [1, 'p-active-bets', 4, '130°', T], [1, 'p-active-bets', 4, '129.9', T], [1, 'p-active-bets', 4, '129.89', T], [1, 'p-active-bets', 4, '130 degrees', T], [1, 'p-active-bets', 4, '50', 'acute'], [1, 'p-active-bets', 4, '50.1', 'acute'], [1, 'p-active-bets', 4, '2.267', 'radians'], [1, 'p-active-bets', 4, '2.27', 'radians'], [1, 'p-active-bets', 4, '129', F], [1, 'p-active-bets', 4, '131', F],
  [1, 'p-drone-crosswind', 1, '(3/5, 4/5)', T], [1, 'p-drone-crosswind', 1, '(\\frac{3}{5},\\frac{4}{5})', T], [1, 'p-drone-crosswind', 1, '(.6, .8)', T], [1, 'p-drone-crosswind', 1, '(0.60, 0.80)', T], [1, 'p-drone-crosswind', 1, '\\frac{1}{5}(3,4)', T, SCAL],
  [1, 'p-drone-crosswind', 1, '(3, 4)', 'not-unit'], [1, 'p-drone-crosswind', 1, '(0.8, 0.6)', 'swapped'], [1, 'p-drone-crosswind', 1, '(12, 16)', 'whole'], [1, 'p-drone-crosswind', 1, '(-0.6, -0.8)', F],
  [1, 'p-drone-crosswind', 2, '-4', T], [1, 'p-drone-crosswind', 2, '−4', T], [1, 'p-drone-crosswind', 2, '-4 km/h', T], [1, 'p-drone-crosswind', 2, '-4km/h', T], [1, 'p-drone-crosswind', 2, '-4.0', T], [1, 'p-drone-crosswind', 2, '-4 kmh', T], [1, 'p-drone-crosswind', 2, '-4 km per hour', F],
  [1, 'p-drone-crosswind', 2, '4', 'sign'], [1, 'p-drone-crosswind', 2, '-80', 'not-unit'], [1, 'p-drone-crosswind', 2, '-20', 'three-four'], [1, 'p-drone-crosswind', 2, '-5.8', 'swapped'], [1, 'p-drone-crosswind', 2, '-6', 'swapped'], [1, 'p-drone-crosswind', 2, '-5', F],
  [1, 'p-drone-crosswind', 3, '7', T], [1, 'p-drone-crosswind', 3, '7 km/h', T], [1, 'p-drone-crosswind', 3, '7.0', T], [1, 'p-drone-crosswind', 3, '-7', F], [1, 'p-drone-crosswind', 3, '8.06', 'wind-speed'], [1, 'p-drone-crosswind', 3, '8', 'wind-speed'], [1, 'p-drone-crosswind', 3, '9', 'added'], [1, 'p-drone-crosswind', 3, '49', 'no-root'],
  [1, 'p-drone-crosswind', 4, '24', T], [1, 'p-drone-crosswind', 4, '24 km/h', T], [1, 'p-drone-crosswind', 4, '24.0', T], [1, 'p-drone-crosswind', 4, '25', 'no-cancel'], [1, 'p-drone-crosswind', 4, '18', 'subtracted'], [1, 'p-drone-crosswind', 4, '576', 'no-root'], [1, 'p-drone-crosswind', 4, '20', F],
  [1, 'p-drone-crosswind', 5, '60', T], [1, 'p-drone-crosswind', 5, '60 minutes', T], [1, 'p-drone-crosswind', 5, '60 min', T], [1, 'p-drone-crosswind', 5, '60 mins', T], [1, 'p-drone-crosswind', 5, '60.0', T], [1, 'p-drone-crosswind', 5, '1 hour', 'hours'], [1, 'p-drone-crosswind', 5, '1', 'hours'],
  [1, 'p-drone-crosswind', 5, '50', 'no-wind'], [1, 'p-drone-crosswind', 5, '43', 'tailwind'], [1, 'p-drone-crosswind', 5, '42.86', 'tailwind'], [1, 'p-drone-crosswind', 5, '48', 'air-only'], [1, 'p-drone-crosswind', 5, '3600', F],
  [1, 'p-stress-hedge', 1, '-2.2', T], [1, 'p-stress-hedge', 1, '-2.2%', T], [1, 'p-stress-hedge', 1, '−2.2', T], [1, 'p-stress-hedge', 1, '-2.20', T], [1, 'p-stress-hedge', 1, '-0.022', T, DEC], [1, 'p-stress-hedge', 1, '2.2', F], [1, 'p-stress-hedge', 1, '-2', F], [1, 'p-stress-hedge', 1, '-3', 'unweighted'], [1, 'p-stress-hedge', 1, '-1', 'equal'],
  [1, 'p-stress-hedge', 2, '0.11', T], [1, 'p-stress-hedge', 2, '.11', T], [1, 'p-stress-hedge', 2, '11/100', T], [1, 'p-stress-hedge', 2, '11%', T], [1, 'p-stress-hedge', 2, 'h=0.11', T], [1, 'p-stress-hedge', 2, '0.1', F], [1, 'p-stress-hedge', 2, '-0.11', F], [1, 'p-stress-hedge', 2, '-0.55', 'sign'], [1, 'p-stress-hedge', 2, '0.275', 'gold-only'], [1, 'p-stress-hedge', 2, '0.28', 'gold-only'], [1, 'p-stress-hedge', 2, '0.18', 'equity-only'],
  [1, 'p-stress-hedge', 3, '-1.46', T], [1, 'p-stress-hedge', 3, '-1.46%', T], [1, 'p-stress-hedge', 3, '-1.460', T], [1, 'p-stress-hedge', 3, '-0.0146', T, DEC], [1, 'p-stress-hedge', 3, '-1.5', F], [1, 'p-stress-hedge', 3, '-0.8', 'old'], [1, 'p-stress-hedge', 3, '-0.14', 'shift-added'], [1, 'p-stress-hedge', 3, '1.46', F],
  [1, 'p-stress-hedge', 4, '-0.73', T], [1, 'p-stress-hedge', 4, '-0.73%', T], [1, 'p-stress-hedge', 4, '−0.73', T], [1, 'p-stress-hedge', 4, '-0.0073', T, DEC], [1, 'p-stress-hedge', 4, '-0.7', F], [1, 'p-stress-hedge', 4, '-1.5', 'unhedged'], [1, 'p-stress-hedge', 4, '-1.46', 'no-half'], [1, 'p-stress-hedge', 4, '0.73', F],
  // problems-2
  [2, 'p-italic-letters', 1, '[[1, \\frac{1}{4}], [0, 1]]', T], [2, 'p-italic-letters', 1, '[[1, 1/4], [0, 1]]', T], [2, 'p-italic-letters', 1, '[[1.0, 0.250], [0, 1]]', T], [2, 'p-italic-letters', 1, '[[1, 0], [0.25, 1]]', 'rows', MAT], [2, 'p-italic-letters', 1, '[[1, 0.25], [0, 0]]', F],
  [2, 'p-italic-letters', 2, '(4.0, 8)', T], [2, 'p-italic-letters', 2, '(2, 8.5)', 'rows'], [2, 'p-italic-letters', 2, '(2.25, 8)', 'once'], [2, 'p-italic-letters', 2, '(8, 4)', F],
  [2, 'p-italic-letters', 3, '[[3/2, 3/8], [0, 1]]', T], [2, 'p-italic-letters', 3, '[[1.5, 0.25], [0, 1]]', 'order', MAT], [2, 'p-italic-letters', 3, '[[1.5, 0], [0, 1]]', 'entrywise', MAT], [2, 'p-italic-letters', 3, '[[1.5, 0.38], [0, 1]]', F],
  [2, 'p-italic-letters', 4, '6', T], [2, 'p-italic-letters', 4, '6.0', T], [2, 'p-italic-letters', 4, 'x=6', T], [2, 'p-italic-letters', 4, '(6, 8)', F], [2, 'p-italic-letters', 4, '5', 'order'], [2, 'p-italic-letters', 4, '4', 'slant-only'], [2, 'p-italic-letters', 4, '3', 'widen-only'], [2, 'p-italic-letters', 4, '8', F],
  [2, 'p-site-plan', 1, '[[4/5, -3/5], [3/5, 4/5]]', T], [2, 'p-site-plan', 1, '[[0.8, −0.6], [0.6, 0.8]]', T], [2, 'p-site-plan', 1, '[[0.8, 0.6], [-0.6, 0.8]]', 'clockwise', MAT], [2, 'p-site-plan', 1, '[[0.6, -0.8], [0.8, 0.6]]', 'swapped', MAT], [2, 'p-site-plan', 1, '[[\\cos\\theta, -\\sin\\theta], [\\sin\\theta, \\cos\\theta]]', F],
  [2, 'p-site-plan', 2, 'I', F], [2, 'p-site-plan', 2, '[[1.0, 0.0], [0.0, 1.0]]', T], [2, 'p-site-plan', 2, '[[0.28, -0.96], [0.96, 0.28]]', 'square', MAT], [2, 'p-site-plan', 2, '[[0.64, -0.36], [-0.36, 0.64]]', 'entrywise', MAT], [2, 'p-site-plan', 2, '1', 'length'],
  [2, 'p-site-plan', 3, '(10.0, -5.0)', T], [2, 'p-site-plan', 3, '(10, −5)', T], [2, 'p-site-plan', 3, '(7.6, 8.2)', 'forward'], [2, 'p-site-plan', 3, '(8.2, -7.6)', 'swapped'], [2, 'p-site-plan', 3, '(-5, 10)', F],
  [2, 'p-site-plan', 4, '126.9', T], [2, 'p-site-plan', 4, '126.9°', T], [2, 'p-site-plan', 4, '126.87', T], [2, 'p-site-plan', 4, '126.9 degrees', T], [2, 'p-site-plan', 4, '127', F], [2, 'p-site-plan', 4, '126.8', F], [2, 'p-site-plan', 4, '90', 'plan-angle'], [2, 'p-site-plan', 4, '36.9', 'theta'],
  [2, 'p-site-plan', 4, '53.1', 'NONE', 'the acute angle between the pipe (a line) and the axis, from the right ground step (-6, 8), is told "That turns the step the wrong way, with R^T"'],
  [2, 'p-site-plan', 4, '-233.1', F], [2, 'p-site-plan', 4, '2.214', F],
  [2, 'p-factor-risk', 2, '(1.04, 0.250)', T], [2, 'p-factor-risk', 2, '(26/25, 1/4)', T], [2, 'p-factor-risk', 2, '(3, 0.9)', 'unweighted'], [2, 'p-factor-risk', 2, '(1, 0.3)', 'equal'], [2, 'p-factor-risk', 2, '(0.25, 1.04)', F], [2, 'p-factor-risk', 2, '(1.0, 0.3)', 'equal'],
  [2, 'p-factor-risk', 3, '(0.02415, 0.00472)', T], [2, 'p-factor-risk', 3, '(0.0242, 0.0047)', T, 'no rounding is asked and the entries are compared exactly, so four places are refused'], [2, 'p-factor-risk', 3, '(0.024, 0.005)', F], [2, 'p-factor-risk', 3, '(2.415\\times10^{-2}, 4.72\\times10^{-3})', T],
  [2, 'p-factor-risk', 3, '(0.0234, 0.0016)', 'diagonal'], [2, 'p-factor-risk', 3, '(0.00472, 0.02415)', 'wrong-order'], [2, 'p-factor-risk', 3, '(2.415%, 0.472%)', F],
  [2, 'p-factor-risk', 4, '0.02630', T], [2, 'p-factor-risk', 4, '0.0263', T], [2, 'p-factor-risk', 4, '0.026296', T], [2, 'p-factor-risk', 4, '0.02629', T], [2, 'p-factor-risk', 4, '0.02631', T], [2, 'p-factor-risk', 4, '0.026', F], [2, 'p-factor-risk', 4, '2.63%', T],
  [2, 'p-factor-risk', 4, '0.02474', 'diagonal'], [2, 'p-factor-risk', 4, '0.024736', 'diagonal'], [2, 'p-factor-risk', 4, '1.1441', 'no-f'], [2, 'p-factor-risk', 4, '0.02887', 'sum'],
  [2, 'p-factor-risk', 5, '16.2', T], [2, 'p-factor-risk', 5, '16.2%', T], [2, 'p-factor-risk', 5, '16.22', T], [2, 'p-factor-risk', 5, '16.20', T], [2, 'p-factor-risk', 5, '0.162', T, DEC], [2, 'p-factor-risk', 5, '16', F], [2, 'p-factor-risk', 5, '16.3', F], [2, 'p-factor-risk', 5, '15.7', 'diagonal'], [2, 'p-factor-risk', 5, '2.63', 'no-root'], [2, 'p-factor-risk', 5, '2.6', 'no-root'],
  [2, 'p-bakery-costs', 1, '(23.60, 6.40, 4.40)', T], [2, 'p-bakery-costs', 1, '(118/5, 32/5, 22/5)', T], [2, 'p-bakery-costs', 1, '(18, 9.2, 8.6)', 'swapped'], [2, 'p-bakery-costs', 1, '(0.8, 0.3, 0.25)', 'one-each'], [2, 'p-bakery-costs', 1, '(23.6, 6.4)', 'length'],
  [2, 'p-bakery-costs', 2, '54.88', T], [2, 'p-bakery-costs', 2, '£54.88', T], [2, 'p-bakery-costs', 2, '54.88 pounds', T], [2, 'p-bakery-costs', 2, '54.880', T], [2, 'p-bakery-costs', 2, '54.9', F], [2, 'p-bakery-costs', 2, '55', F], [2, 'p-bakery-costs', 2, '5488p', F], [2, 'p-bakery-costs', 2, '79.8', 'swapped'], [2, 'p-bakery-costs', 2, '79.80', 'swapped'], [2, 'p-bakery-costs', 2, '34.4', 'unpriced'],
  [2, 'p-bakery-costs', 4, '1.74', T], [2, 'p-bakery-costs', 4, '£1.74', T], [2, 'p-bakery-costs', 4, '1.740', T], [2, 'p-bakery-costs', 4, '174p', F], [2, 'p-bakery-costs', 4, '1.7', F], [2, 'p-bakery-costs', 4, '0.85', 'loaf'], [2, 'p-bakery-costs', 4, '0.7', 'unpriced'], [2, 'p-bakery-costs', 4, '0.70', 'unpriced'],
  [2, 'p-bakery-costs', 5, '77.30', T], [2, 'p-bakery-costs', 5, '77.3', T], [2, 'p-bakery-costs', 5, '£77.30', T], [2, 'p-bakery-costs', 5, '77', F], [2, 'p-bakery-costs', 5, '54.88', 'this-week'], [2, 'p-bakery-costs', 5, '104', 'swapped'], [2, 'p-bakery-costs', 5, '2.59', 'one-each'], [2, 'p-bakery-costs', 5, '77.31', F],
  // problems-3
  [3, 'p-goat-feed', 1, '[[2/5, 1/10], [1/5, 3/10]]', T], [3, 'p-goat-feed', 1, '[[.4, .1], [.2, .3]]', T], [3, 'p-goat-feed', 1, '[[0.4, 0.2], [0.1, 0.3]]', 'transposed', MAT], [3, 'p-goat-feed', 1, '[[4, 1], [2, 3]]', F],
  [3, 'p-goat-feed', 2, '0.1', T], [3, 'p-goat-feed', 2, '.1', T], [3, 'p-goat-feed', 2, '1/10', T], [3, 'p-goat-feed', 2, '0.10', T], [3, 'p-goat-feed', 2, '0.14', 'added'], [3, 'p-goat-feed', 2, '-0.1', 'flipped'], [3, 'p-goat-feed', 2, '10', F],
  [3, 'p-goat-feed', 3, '[[3.0, -1.0], [-2.0, 4.0]]', T], [3, 'p-goat-feed', 3, '10[[0.3, -0.1], [-0.2, 0.4]]', T, SCAL], [3, 'p-goat-feed', 3, '[[0.3, -0.1], [-0.2, 0.4]]', 'no-divide', MAT], [3, 'p-goat-feed', 3, '[[3, 1], [2, 4]]', 'no-negate', MAT],
  [3, 'p-goat-feed', 3, '[[3, -2], [-1, 4]]', 'transposed', MAT], [3, 'p-goat-feed', 3, '[[0.03, -0.01], [-0.02, 0.04]]', 'times-det', MAT], [3, 'p-goat-feed', 3, '[[4, -1], [-2, 3]]', F],
  [3, 'p-goat-feed', 4, '(25 kg, 30 kg)', F], [3, 'p-goat-feed', 4, 'm=25, h=30', F], [3, 'p-goat-feed', 4, '(11, 43)', 'transposed'], [3, 'p-goat-feed', 4, '(2.5, 3)', 'no-divide'], [3, 'p-goat-feed', 4, '(30, 25)', 'swapped'],
  [3, 'p-paint-tints', 1, '2', T], [3, 'p-paint-tints', 1, 'k=2', T], [3, 'p-paint-tints', 1, '2.0', T], [3, 'p-paint-tints', 1, '-2', 'plus'], [3, 'p-paint-tints', 1, '4.5', 'mixed'], [3, 'p-paint-tints', 1, '9/2', 'mixed'], [3, 'p-paint-tints', 1, '0.5', F], [3, 'p-paint-tints', 1, '32', F],
  [3, 'p-paint-tints', 2, '1', T], [3, 'p-paint-tints', 2, '1.0', T], [3, 'p-paint-tints', 2, '2', 'full'], [3, 'p-paint-tints', 2, '0', 'zero'], [3, 'p-paint-tints', 2, '-1', F],
  [3, 'p-paint-tints', 4, '3', T], [3, 'p-paint-tints', 4, '3 litres', T], [3, 'p-paint-tints', 4, 'q=3', T], [3, 'p-paint-tints', 4, '3.0', T], [3, 'p-paint-tints', 4, '7.5', 'q-only'], [3, 'p-paint-tints', 4, '0', 'p-only'], [3, 'p-paint-tints', 4, '5', F],
  [3, 'p-paint-tints', 5, '(4.0, 2.0)', T], [3, 'p-paint-tints', 5, '(144/36, 72/36)', T], [3, 'p-paint-tints', 5, '(2, 4)', 'swapped'], [3, 'p-paint-tints', 5, '(144, 72)', 'no-divide'], [3, 'p-paint-tints', 5, '(4, -2)', F],
  [3, 'p-colour-sensor', 1, '0.5', T], [3, 'p-colour-sensor', 1, '1/2', T], [3, 'p-colour-sensor', 1, '.5', T], [3, 'p-colour-sensor', 1, '0.50', T], [3, 'p-colour-sensor', 1, '50%', T], [3, 'p-colour-sensor', 1, '0.62', 'added'], [3, 'p-colour-sensor', 1, '0.56', 'diagonal'], [3, 'p-colour-sensor', 1, '-0.5', F], [3, 'p-colour-sensor', 1, '2', F],
  [3, 'p-colour-sensor', 2, '[[7/5, -3/5], [-2/5, 8/5]]', T], [3, 'p-colour-sensor', 2, '[[1.40, -0.60], [-0.40, 1.60]]', T], [3, 'p-colour-sensor', 2, '2[[0.7, -0.3], [-0.2, 0.8]]', T, SCAL],
  [3, 'p-colour-sensor', 2, '[[0.7, -0.3], [-0.2, 0.8]]', 'no-divide', MAT], [3, 'p-colour-sensor', 2, '[[0.35, -0.15], [-0.1, 0.4]]', 'times-det', MAT], [3, 'p-colour-sensor', 2, '[[1.4, 0.6], [0.4, 1.6]]', 'no-negate', MAT], [3, 'p-colour-sensor', 2, '[[1.6, -0.6], [-0.4, 1.4]]', F],
  [3, 'p-colour-sensor', 3, '-42', T], [3, 'p-colour-sensor', 3, '−42', T], [3, 'p-colour-sensor', 3, '-42.0', T], [3, 'p-colour-sensor', 3, '140', 'matrix-product'], [3, 'p-colour-sensor', 3, '-52', 'entry-10'], [3, 'p-colour-sensor', 3, '182', 'entry-00'], [3, 'p-colour-sensor', 3, '42', F], [3, 'p-colour-sensor', 3, '112', F],
  [3, 'p-colour-sensor', 4, '(140.0, 60.0)', T], [3, 'p-colour-sensor', 4, '(70, 30)', 'no-divide'], [3, 'p-colour-sensor', 4, '(125, 75)', 'forward'], [3, 'p-colour-sensor', 4, '(130, 70)', 'column-sums'], [3, 'p-colour-sensor', 4, '(60, 140)', F],
  [3, 'p-engraver-dial', 1, '[[2k+6, k+2], [5, 2]]', T], [3, 'p-engraver-dial', 1, '[[2(k+3), 2+k], [5, 2]]', T, RIGHTM], [3, 'p-engraver-dial', 1, '[[6+2k, 2+k], [3+2, 1+1]]', T, RIGHTM], [3, 'p-engraver-dial', 1, '[[7, 3k+1], [5, 2k+1]]', 'order', MAT], [3, 'p-engraver-dial', 1, '[[6, k], [2, 1]]', 'entrywise', MAT], [3, 'p-engraver-dial', 1, '[[6+2k, 2+k], [5, 1]]', F],
  [3, 'p-engraver-dial', 2, '2-k', T], [3, 'p-engraver-dial', 2, '-k+2', T], [3, 'p-engraver-dial', 2, '2 - k', T], [3, 'p-engraver-dial', 2, '-(k-2)', T], [3, 'p-engraver-dial', 2, '2(6+2k)-5(2+k)', 'form'], [3, 'p-engraver-dial', 2, '12+4k-10-5k', 'form'],
  [3, 'p-engraver-dial', 2, '22+9k', 'added'], [3, 'p-engraver-dial', 2, 'k-2', 'flipped'], [3, 'p-engraver-dial', 2, '2k-2', F], [3, 'p-engraver-dial', 2, 'd=2-k', T],
  [3, 'p-engraver-dial', 3, '2', T], [3, 'p-engraver-dial', 3, 'k=2', T], [3, 'p-engraver-dial', 3, '2.0', T], [3, 'p-engraver-dial', 3, '-2.44', 'added'], [3, 'p-engraver-dial', 3, '-22/9', 'added'], [3, 'p-engraver-dial', 3, '0', F],
  [3, 'p-engraver-dial', 3, '-2', 'NONE', 'the sign slip k = -2 (from 2 + k = 0) falls in the `added` band of 0.5 and is told "That solves 22 + 9k = 0"'],
  [3, 'p-engraver-dial', 4, '[[2.0, -3.0], [-5.0, 8.0]]', T], [3, 'p-engraver-dial', 4, '[[2, 3], [5, 8]]', 'no-negate', MAT], [3, 'p-engraver-dial', 4, '[[8, -3], [-5, 2]]', 'unswapped', MAT], [3, 'p-engraver-dial', 4, '[[3, -4], [-5, 7]]', 'order', MAT], [3, 'p-engraver-dial', 4, '[[8, 3], [5, 2]]', F],
  [3, 'p-engraver-dial', 5, '(2.0, 1.0)', T], [3, 'p-engraver-dial', 5, '(9, -11)', 'order'], [3, 'p-engraver-dial', 5, '(188, 119)', 'forward'], [3, 'p-engraver-dial', 5, '(116, -71)', 'unswapped'], [3, 'p-engraver-dial', 5, '(1, 2)', F], [3, 'p-engraver-dial', 5, '(7, 5)', F],
];

let checks = 0, fails = 0, findings = 0, forms = 0;
const say = (ok, finding, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const seen = new Set();
const formTable = {};
let nNum = 0, nExpr = 0;
for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/vectors/problems-${n}.json`, 'utf8'));
  for (const it of doc.items) {
    it.parts.forEach((p, i) => {
      const k = i + 1, w = p.widget, where = `problems-${n} ${it.id} ${k}`;
      const by = (p.feedback && p.feedback.byKey) || {};
      let grade;
      if (w.kind === 'numeric') {
        nNum++; grade = (t) => num(w, t);
        say(grade(String(w.unit === '%' ? +(w.answer * 100).toFixed(8) : w.answer)).ok, null, `${where}: answer ${w.answer} grades correct`);
        for (const x of w.wrong || []) {
          const r = grade(String(w.unit === '%' ? +(x.value * 100).toFixed(8) : x.value));
          say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} lands on its key (got ok=${r.ok} key=${r.key})`);
          say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
        }
      } else if (w.kind === 'expression') {
        nExpr++; grade = (t) => expr(w, t);
        say(grade(w.answer).ok, null, `${where}: answer grades correct`);
        for (const a of w.accept || []) say(grade(a).ok, null, `${where}: accept "${a}" grades correct`);
        for (const x of w.wrong || []) {
          const r = grade(x.tex);
          say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.tex} lands on its key (got ok=${r.ok} key=${r.key})`);
          say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
        }
        const e = entries(w.answer);
        if (e.matrix || /^\(.*,.*\)$/.test(w.answer)) {
          const fm = e.matrix ? matForms(e.rows) : vecForms(e.v);
          for (const [name, [text, want]] of Object.entries(fm)) {
            const r = grade(text);
            checks++;
            const tag = (e.matrix ? 'matrix: ' : 'vector: ') + name;
            formTable[tag] = formTable[tag] || { want, ok: 0, no: [], keys: new Set() };
            if (r.ok) formTable[tag].ok++; else { formTable[tag].no.push(`${n}.${it.id.slice(2)}.${k}`); formTable[tag].keys.add(String(r.key)); }
            if (r.ok !== want) { forms++; if (ALL) console.log(`FORM    ${where}: ${name} "${text}" is ${r.ok ? 'accepted' : 'refused'} (key ${r.key}), wanted ${want ? 'accepted' : 'refused'}`); }
          }
        }
      } else return;
      const rows = TYPED.filter(r => r[0] === n && r[1] === it.id && r[2] === k);
      for (const r of rows) {
        seen.add(r);
        const res = grade(r[3]);
        const want = r[4];
        const good = want === true ? res.ok === true : want === false ? res.ok === false : want === 'NONE' ? (res.ok === false && res.key === null) : (res.ok === false && res.key === want);
        say(good, r[5], `${where}: typed "${r[3]}" is ${res.ok ? 'accepted' : 'refused'} (key ${res.key}), expected ${want === true ? 'accepted' : want === false ? 'refused' : 'refused on ' + want}`);
      }
    });
  }
}
for (const r of TYPED) if (!seen.has(r)) { fails++; console.log('FAIL    row never used: ' + r.slice(0, 4).join(' ')); }
console.log('\nOther ways to type the answer (expression parts): accepted on how many parts, refused on which, with which keys');
for (const [tag, v] of Object.entries(formTable)) console.log(`  ${tag.padEnd(48)} wanted ${v.want ? 'accepted' : 'refused '}  accepted ${String(v.ok).padStart(2)}  refused ${String(v.no.length).padStart(2)}${v.no.length ? '  keys ' + [...v.keys].join(',') : ''}${ALL && v.no.length ? '  ' + v.no.join(' ') : ''}`);
console.log(`grade-probe: ${checks} checks over ${nNum} numeric and ${nExpr} expression parts, ${fails} failures, ${findings} findings (rows the reader holds to be faults), ${forms} form results against the reader`);
process.exit(fails ? 1 : 0);
