#!/usr/bin/env node
/* Delta read, fix passes of problems 0.3 b and 0.3 c: what the engine's own graders do with the 24 changed items.
   Pattern: docs/reviews/delta-problems-aa-2-scripts/grade.mjs. app/js/engine/grade.js with the local Compute Engine; the
   grading steps of numeric.js (parseNum, within, matchWrong with the 1e-9 fallback, numSetGrade) and of expression.js
   (exprEqual, then the normExpr text fallback, then the shape check: "simplified" with expression.js's own exprForms.reducible,
   "exact-angle" with shapeExactAngle).
   For every part of the changed items: the answer and each accept[] form grade correct, each wrong[] entry grades to its own
   id and has a byKey line. TYPED rows: [course, set, item, part, typed, expected, note?]; expected is true (accepted), false
   (refused, any line), null (refused with the generic line) or the key the typed value should be given ("form", "count" or a
   wrong[] id). A row with a note is one the reader records as a finding: it prints as FINDING and does not fail.

   node docs/reviews/delta-problems-aa-3-scripts/grade.mjs --local-cdn <pkgs> [--show]      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

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
g.ZQ.widgets = { register() {}, dataPanel() { return null; } }; g.ZQ.h = () => ({}); g.ZQ.esc = (x) => x;
vm.runInContext(fs.readFileSync('app/js/engine/widgets/expression.js', 'utf8'), g);

const X = 'exp-log', S = 'series', T = 'trig';
const ITEMS = [
  [X, 1, 'p-yeast-culture'], [X, 1, 'p-rare-coin'], [X, 1, 'p-curve-point'], [X, 2, 'p-forty-doublings'], [X, 2, 'p-drawdown-recovery'], [X, 2, 'p-app-users'],
  [X, 3, 'p-savings-doubling'], [X, 3, 'p-weekly-target'], [X, 3, 'p-log-chart-line'], [X, 3, 'p-monthly-deposit'],
  [S, 1, 'p-pendulum-swings'], [S, 1, 'p-daily-tablet'], [S, 1, 'p-shop-orders'], [S, 2, 'p-tin-display'], [S, 3, 'p-pizza-toppings'], [S, 3, 'p-bracket-estimate'],
  [T, 1, 'p-hexagon-tile'], [T, 1, 'p-lake-markers'], [T, 1, 'p-desk-lamp'], [T, 2, 'p-water-wheel'], [T, 3, 'p-two-angles'], [T, 3, 'p-quadratic-in-sine'],
  [T, 3, 'p-daylight-model'], [T, 3, 'p-garden-bed'],
];
const rows = (course, n, id, part, list) => list.map(([typed, expected, note]) => [course, n, id, part, typed, expected, note]);
const TYPED = [
  // ---------------- fix pass 0.3 b ----------------
  ...rows(X, 1, 'p-rare-coin', 4, [['1397', true], ['1398', true], ['£1,398', true], ['1397.54', true], ['1397.5', true], ['1399', false], ['1396', false]]),
  ...rows(X, 2, 'p-forty-doublings', 4, [['14', true], ['14.0', true], ['13', 'rounded-down'], ['4', 'tenfold-steps'], ['54', 'total'], ['10', null], ['13.15', null], ['15', null]]),
  ...rows(X, 2, 'p-drawdown-recovery', 3, [['4.28', true], ['4.2764', true], ['4.277', true], ['4.27', false], ['4.29', false], ['2.14', 'no-power'], ['0.23', 'inverted'], ['5.11', 'simple'],
    ['3.22', 'carried'], ['1.41', 'divided-numbers'], ['5.80', null], ['4.3', null]]),
  ...rows(X, 2, 'p-drawdown-recovery', 4, [['5', true], ['4', 'rounded-down'], ['7', 'with-falls'], ['6', null], ['4.28', null]]),
  ...rows(X, 2, 'p-app-users', 1, [['2000\\cdot1.3^{n}', true], ['2000(1.3)^n', true], ['2000*1.3^n', true], ['2000\\cdot0.3^{n}', 'rate-only'], ['2000+600n', 'steady']]),
  ...rows(X, 2, 'p-app-users', 3, [['12.27', true], ['12.269', true], ['12.26', false], ['12.28', false], ['80', 'simple'], ['83.33', null], ['19.23', 'divided'], ['1.38', 'joined'], ['-2.67', 'rate-only']]),
  ...rows(X, 3, 'p-savings-doubling', 4, [['2606.4', 'years'], ['2606', 'years'], ['2607', 'years']]),
  ...rows(X, 3, 'p-weekly-target', 3, [['0.0747', true], ['0.0748', true], ['0.07472', true], ['0.0746', false], ['0.0749', false], ['-0.0747', 'inverted'], ['−0.0747', 'inverted'], ['-0.0748', 'inverted'],
    ['0.0776', 'simple'], ['0.1178', 'from-monday'], ['3.24', 'difference']]),
  ...rows(X, 3, 'p-weekly-target', 4, [['0.0249', true], ['0.02490', true], ['0.024908', true], ['0.0250', true], ['0.0248', true], ['0.0251', false], ['0.0247', false], ['0.4212', 'cube-root'],
    ['0.2241', 'times-three'], ['0.0259', 'carried'], ['0.025867', 'carried']]),
  ...rows(X, 3, 'p-weekly-target', 5, [['2.52', true], ['2.52%', true], ['2.521', true], ['2.51', false], ['2.53', false], ['2.49', 'log-as-simple'], ['2.59', 'simple-split'], ['0.0252', 'decimal'],
    ['0.02521', 'decimal'], ['0.0249', null], ['0.0259', null], ['102.52', 'e-power']]),
  ...rows(X, 3, 'p-monthly-deposit', 2, [['4.79', true], ['4.79%', true], ['0.0479', 'decimal'], ['0.04793', 'decimal'], ['0.048', null], ['0.0491', null]]),
  // ---------------- fix pass 0.3 c: series ----------------
  ...rows(S, 1, 'p-pendulum-swings', 2, [['80\\cdot0.9^{n-1}', true], ['80\\cdot(0.9)^{n-1}', true], ['80(0.9)^{n-1}', true], ['80*(0.9)^(n-1)', true], ['80*0.9^(n-1)', true], ['80(0.9)^(n-1)', true],
    ['80\\times0.9^{n-1}', true], ['80\\cdot\\left(\\frac{9}{10}\\right)^{n-1}', true], ['80*(0.9)^n', false], ['72\\cdot0.9^{n-2}', true], ['80(9/10)^(n-1)', null]]),
  ...rows(S, 1, 'p-daily-tablet', 3, [['160\\cdot0.4^{n-1}', true], ['160(0.4)^{n-1}', true], ['160\\cdot(0.4)^{n-1}', true], ['160(0.4)^(n-1)', true], ['160*(0.4)^(n-1)', true], ['160*0.4^(n-1)', true],
    ['400\\cdot0.4^{n}', true], ['160(0.4)^n', false], ['160*(0.6)^(n-1)', false], ['g_n=160\\cdot0.4^{n-1}', true], ['160(2/5)^(n-1)', null]]),
  ...rows(S, 1, 'p-shop-orders', 4, [['64\\cdot1.5^{n-1}', true], ['64(1.5)^{n-1}', true], ['64\\cdot(1.5)^{n-1}', true], ['64(1.5)^(n-1)', true], ['64*(1.5)^(n-1)', true], ['64*1.5^(n-1)', true],
    ['96\\cdot1.5^{n-2}', true], ['96*(1.5)^(n-2)', null, 'finding 3: true, refused in the plain-text field'], ['64\\cdot1.5^{n}', 'month-two-start'], ['64(1.5)^n', 'month-two-start'], ['64*1.5^n', 'month-two-start'], ['96\\cdot1.5^{n-1}', 'month-two-start'], ['96*(1.5)^(n-1)', null],
    ['60n-24', 'arith'], ['64\\left(\\frac{3}{2}\\right)^{n-1}', true], ['\\frac{128}{3}\\cdot1.5^{n}', true],
    ['96*1.5^(n-2)', true], ['96(1.5)^(n-2)', null, 'finding 3: true, refused in the plain-text field'], ['96(1.5)^{n-2}', true], ['96\\cdot(1.5)^{n-2}', true]]),
  ...rows(S, 1, 'p-daily-tablet', 3, [['400*0.4^n', true], ['400(0.4)^n', true]]),
  ...rows(T, 1, 'p-desk-lamp', 5, [['20sqrt(3)-15', true], ['20\\sqrt{3}-\\frac{30}{2}', true, 'finding 4: an unworked line passes']]),
  ...rows(S, 2, 'p-tin-display', 1, [['53', true], ['58', 'n-steps'], ['50', 'step-only'], ['27', null]]),
  ...rows(S, 2, 'p-tin-display', 2, [['305', true], ['610', 'no-halve'], ['265', 'last-only'], ['330', 'n-steps'], ['192', null]]),
  ...rows(S, 2, 'p-tin-display', 3, [['7', true], ['6', 'subtract'], ['10', 'top'], ['8', null]]),
  ...rows(S, 2, 'p-tin-display', 4, [['266', true], ['228', 'six-rows'], ['243', 'four-left'], ['305', 'full'], ['160', null]]),
  ...rows(S, 3, 'p-pizza-toppings', 1, [['330', true], ['7920', 'ordered'], ['7,920', 'ordered'], ['44', 'times'], ['1320', 'three-orders'], ['56', null]]),
  ...rows(S, 3, 'p-pizza-toppings', 2, [['660', true], ['330', 'one-size'], ['165', null], ['792', null]]),
  ...rows(S, 3, 'p-pizza-toppings', 3, [['495', true], ['341', 'one-more'], ['660', 'doubled'], ['11880', 'ordered'], ['84', null]]),
  ...rows(S, 3, 'p-pizza-toppings', 4, [['4096', true], ['4,096', true], ['4095', 'no-plain'], ['2048', 'row-eleven'], ['512', null]]),
  ...rows(S, 3, 'p-bracket-estimate', 5, [['0.80796', true], ['0.80795', true], ['0.807955', true], ['0.80798', 'calculator'], ['0.807983', 'calculator'], ['0.80797', null], ['0.80794', null],
    ['0.809845', 'added'], ['0.80985', 'added'], ['0.7144', 'square']]),
  // ---------------- fix pass 0.3 c: trig ----------------
  ...rows(T, 1, 'p-hexagon-tile', 1, [['4\\sqrt{3}', true], ['4\\sqrt3', true], ['\\sqrt{48}', true], ['4\\cdot\\sqrt{3}', true], ['4\\times\\sqrt{3}', true], ['\\sqrt{3}\\cdot4', true], ['sqrt(48)', true],
    ['4sqrt(3)', true], ['4*sqrt(3)', true], ['\\sqrt{8^2-4^2}', 'form'], ['\\sqrt{64-16}', 'form'], ['8\\sin(60^\\circ)', 'form'], ['\\frac{8\\sqrt{3}}{2}', 'form'], ['2\\sqrt{12}', 'form'], ['\\frac{12}{\\sqrt{3}}', true],
    ['6.93', false], ['6.928', false], ['\\sqrt{80}', 'added'], ['4\\sqrt{5}', 'added'], ['8\\sqrt{3}', 'whole-side'], ['\\sqrt{192}', 'whole-side'], ['4\\sqrt{2}', 'half-square'], ['\\sqrt{32}', 'half-square'], ['4', false], ['5\\sqrt{3}', false]]),
  ...rows(T, 1, 'p-hexagon-tile', 2, [['8\\sqrt{3}', true], ['\\sqrt{192}', true], ['8\\sqrt3', true], ['2\\cdot4\\sqrt{3}', 'form'], ['2\\times4\\sqrt{3}', 'form'], ['4\\sqrt{3}+4\\sqrt{3}', 'form'], ['4\\sqrt{12}', 'form'], ['13.86', false],
    ['4\\sqrt{3}', 'half'], ['\\sqrt{48}', 'half'], ['8', 'side'], ['16', 'long'], ['10\\sqrt{3}', false]]),
  ...rows(T, 1, 'p-hexagon-tile', 3, [['256', true], ['88', 'root-as-three'], ['174.85', 'root-left'], ['175', 'root-left'], ['200', 'cd-unsquared'], ['192', null], ['400', null]]),
  ...rows(T, 1, 'p-hexagon-tile', 4, [['30', true], ['60', 'angle-d'], ['26.57', 'tan'], ['27', 'tan'], ['0.5', 'half'], ['1/2', 'half'], ['0.50', 'half'], ['0.5236', 'radians'], ['0.52', 'radians'], ['0.524', 'radians'],
    ['1', 'radians'], ['0.46', 'radians'], ['0.87', 'radians', 'finding 5: the cosine is told radians'], ['0.866', 'radians', 'finding 5'], ['0.58', 'radians', 'finding 5: the tangent is told radians'], ['31', null]]),
  ...rows(T, 1, 'p-desk-lamp', 1, [['20\\sqrt{3}', true], ['\\sqrt{1200}', true], ['20\\sqrt3', true], ['40\\times\\frac{\\sqrt{3}}{2}', 'form'], ['40\\cdot\\frac{\\sqrt{3}}{2}', 'form'], ['\\frac{40\\sqrt{3}}{2}', 'form'],
    ['40\\sin(60^\\circ)', 'form'], ['10\\sqrt{12}', 'form'], ['34.64', false], ['20', 'sin-30'], ['40\\sqrt{3}', 'no-half'], ['20\\sqrt{2}', 'half-square']]),
  ...rows(T, 1, 'p-desk-lamp', 3, [['36.9', true], ['36.87', true], ['36.8', false], ['37', false], ['53.1', 'flipped'], ['48.6', 'sine'], ['0.75', 'ratio-tan'], ['3/4', 'ratio-tan'], ['0.6', 'ratio-sin'], ['3/5', 'ratio-sin'],
    ['0.64', 'radians'], ['0.644', 'radians'], ['0.6435', 'radians'], ['0.65', null], ['0.8', null], ['0.7', null]]),
  ...rows(T, 1, 'p-desk-lamp', 5, [['20\\sqrt{3}-15', true], ['-15+20\\sqrt{3}', true], ['20\\sqrt3-15', true], ['\\sqrt{1200}-15', true], ['5(4\\sqrt{3}-3)', 'form', 'finding 4: a worked exact value refused'], ['40\\sin(60^\\circ)-30\\sin(30^\\circ)', 'form'],
    ['20\\sqrt{3}-30\\cdot\\frac{1}{2}', 'form'], ['19.64', false], ['20\\sqrt{3}+15', 'above'], ['5\\sqrt{3}', 'cos-30'], ['20\\sqrt{3}-15\\sqrt{3}', 'cos-30'], ['20\\sqrt{3}-30', 'whole-arm']]),
  ...rows(T, 3, 'p-two-angles', 1, [['-45/53', true], ['-0.849', true], ['-0.8491', true], ['−45/53', true], ['-0.85', false], ['-0.88', false], ['45/53', 'sign'], ['0.849', 'sign'], ['25/53', 'one-minus'], ['2025/2809', 'no-root'], ['-15/17', null]]),
  ...rows(T, 3, 'p-two-angles', 3, [['0.2694', true], ['357/1325', true], ['0.269', false], ['0.27', false], ['0.7449', 'sign'], ['987/1325', 'sign'], ['0.8083', 'sum-of-sines'], ['-0.9630', 'cos-formula'], ['0.2047', null]]),
  ...rows(T, 3, 'p-two-angles', 4, [['-0.9630', true], ['-0.963', true], ['-1276/1325', true], ['-0.96', false], ['-0.6672', 'plus'], ['0.6672', 'sign'], ['0.9630', null], ['0.2694', null]]),
  ...rows(T, 3, 'p-two-angles', 5, [['164.4', true], ['164.37', true], ['164.3', false], ['164', false], ['15.6', 'principal'], ['15.63', 'principal'], ['195.6', 'third'], ['344.4', 'fourth'], ['168.2', null]]),
  ...rows(T, 3, 'p-quadratic-in-sine', 4, [['\\frac{5\\pi}{6}', true], ['\\frac{5}{6}\\pi', true], ['5\\pi/6', true], ['x=\\frac{5\\pi}{6}', false], ['150', 'degrees'], ['\\frac{150\\pi}{180}', 'form'], ['\\frac{\\pi}{2}', 'middle'], ['\\frac{5\\pi}{12}', 'half'], ['2.618', false]]),
  ...rows(T, 3, 'p-daylight-model', 4, [['2, 10', true], ['10, 2', true], ['t = 2, t = 10', true], ['2', 'count'], ['7, 11', 'no-shift'], ['11, 7', 'no-shift'], ['4, 8', 'above'], ['8, 4', 'above'], ['2, 8', null], ['1, 5', null]]),
  ...rows(T, 3, 'p-daylight-model', 5, [['8', true], ['4', 'outside'], ['9', 'counted'], ['5', null]]),
  ...rows(T, 3, 'p-garden-bed', 1, [['65\\sin C', true], ['65\\sin(C)', true], ['65sin(C)', true], ['\\frac{1}{2}\\times10\\times13\\sin C', true], ['\\frac{1}{2}\\cdot10\\cdot13\\sin C', true], ['65\\sin{C}', true], ['\\frac{130\\sin C}{2}', true],
    ['130\\sin C', 'no-half'], ['65\\cos C', 'cos'], ['65C', 'angle'], ['30\\sin C', false], ['65\\sin c', true]]),
  ...rows(T, 3, 'p-garden-bed', 2, [['22.62, 157.38', true], ['157.38, 22.62', true], ['22.62', 'count'], ['22.6, 157.4', false], ['11.09, 168.91', 'no-half'], ['22.62, 337.38', 'cos-rule'], ['337.38, 22.62', 'cos-rule'], ['36.87, 143.13', null]]),
  ...rows(T, 3, 'p-garden-bed', 3, [['-12/13', true], ['-0.923', true], ['-0.9231', true], ['-0.92', false], ['12/13', 'sign'], ['0.923', 'sign'], ['8/13', 'one-minus'], ['-144/169', 'no-root'], ['-0.852', 'no-root'], ['-0.8', null], ['-5/13', null]]),
  ...rows(T, 3, 'p-garden-bed', 4, [['22.56', true], ['22.561', true], ['22.6', false], ['22.57', false], ['5.39', 'sign'], ['5.385', 'sign'], ['16.40', 'pythagoras'], ['16.4', 'pythagoras'], ['509', 'no-root'], ['19.72', 'no-two'], ['16.28', null]]),
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (finding) { findings++; console.log((ok ? 'FINDING ' : 'FAIL    ') + msg + '   [' + finding + ']'); if (!ok) fails++; return; } if (!ok) { fails++; console.log('FAIL    ' + msg); } };

const isSet = (w) => Array.isArray(w.answers);
const gradeNumeric = (w, text) => {
  if (isSet(w)) { const r = G.numSetGrade(w, text); return r.ok ? true : (r.key || null); }
  let v = G.parseNum(text);
  if (w.unit === '%' && !text.includes('%')) v = v / 100;
  if (!Number.isFinite(v)) return 'NOPARSE';
  if (G.within(v, +w.answer, w.tol)) return true;
  const m = G.matchWrong(v, w.wrong, { abs: 1e-9 });
  return m ? m.id : null;
};
const size = (j) => (Array.isArray(j) ? 1 + j.slice(1).reduce((a, x) => a + size(x), 0) : 1);
const formOk = (w, L) => {
  if (!w.form) return true;
  if (w.form === 'exact-angle') return !!G.shapeExactAngle(L);
  if (w.form === 'fraction') return !!G.shapeFraction(L);
  if (w.form !== 'simplified') throw new Error('form not modelled: ' + w.form);
  try {
    return G.withParsed(ce, L, w.functions || [], (e) => {
      const j = e.json;
      const constant = !(e.unknowns || []).filter((v) => v !== 'iota').length;
      if (constant && g.ZQ.widgets.exprForms.reducible(j)) return false;
      try { return size(j) <= size(e.simplify().json); } catch { return true; }
    });
  } catch { return true; }
};
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => {
    try { if (G.exprEqual(ce, L, t, fo)) return true; } catch { /* fall to text */ }
    return !!G.normExpr(L) && G.normExpr(L) === G.normExpr(t);
  };
  if ([w.answer, ...(w.accept || [])].some(eq)) return formOk(w, L) ? true : 'form';
  const x = (w.wrong || []).find((y) => y.tex && eq(y.tex));
  if (x) return x.id;
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
      const k = w.unit === '%' ? 100 : 1;
      say(gradeNumeric(w, G.fmtNum(+w.answer * k)) === true, null, `${where}: answer outside its own band`);
      for (const x of w.wrong || []) { const got = gradeNumeric(w, G.fmtNum(+x.value * k)); say(got === x.id, null, `${where}: wrong "${x.id}" = ${x.value} grades ${got}`); }
      judge(gradeNumeric);
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer) === true, null, `${where}: answer does not grade correct (${gradeExpr(w, w.answer)})`);
      for (const a of w.accept || []) say(gradeExpr(w, a) === true, null, `${where}: accept "${a}" does not grade correct (${gradeExpr(w, a)})`);
      for (const x of w.wrong || []) say(gradeExpr(w, x.tex) === x.id, null, `${where}: wrong "${x.id}" ${x.tex} grades ${gradeExpr(w, x.tex)}`);
      judge(gradeExpr);
    } else if (w.kind === 'choice') {
      say((w.options || []).filter((o) => o.correct).length === 1, null, `${where}: not exactly one correct option`);
      for (const o of w.options || []) say(!!o.correct || !!o.why, null, `${where}: option ${o.id} has no why`);
      if (typed.length) { fails++; console.log(`FAIL    ${where}: typed rows on a choice part`); }
    }
  });
}
for (const r of TYPED) if (!used.has(r)) { fails++; console.log('FAIL    row not used: ' + r.slice(0, 5).join(' ')); }
console.log(`grade.mjs: ${nItems} items, ${nParts} parts, ${TYPED.length} typed rows; ${checks} checks, ${fails} failures, ${findings} finding rows`);
process.exit(fails ? 1 : 0);
