/* Engine graders on every part of exp-log problems 1 to 3, plus typed strings. Run from repo root:
   node docs/reports/problems-exp-log-grade.mjs --local-cdn <pkgs> */
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

/* [set, item, part, typed, expected] */
const T = [
  [1, 'p-yeast-culture', 1, '3000\\cdot2^n', true], [1, 'p-yeast-culture', 1, '3000*2^n', true], [1, 'p-yeast-culture', 1, '2^n\\cdot3000', true],
  [1, 'p-yeast-culture', 1, '1500\\cdot2^{n+1}', true], [1, 'p-yeast-culture', 1, '3000\\cdot2n', false], [1, 'p-yeast-culture', 1, '3000^n', false],
  [1, 'p-yeast-culture', 2, '750', true], [1, 'p-yeast-culture', 2, '-12000', false],
  [1, 'p-yeast-culture', 3, '4243', true], [1, 'p-yeast-culture', 3, '4242', true], [1, 'p-yeast-culture', 3, '4242.64', true], [1, 'p-yeast-culture', 3, '4500', false], [1, 'p-yeast-culture', 3, '4241', false],
  [1, 'p-yeast-culture', 4, '2.5', true], [1, 'p-yeast-culture', 4, '5/2', true], [1, 'p-yeast-culture', 4, '-1.5', false],
  [1, 'p-laptop-value', 1, '0.75', true], [1, 'p-laptop-value', 1, '3/4', true],
  [1, 'p-laptop-value', 2, '675', true], [1, 'p-laptop-value', 2, '£675', true], [1, 'p-laptop-value', 2, '675.00', true],
  [1, 'p-laptop-value', 3, '379.69', true], [1, 'p-laptop-value', 3, '379.6875', true], [1, 'p-laptop-value', 3, '379.7', false],
  [1, 'p-laptop-value', 4, '68.36', true], [1, 'p-laptop-value', 4, '68.36%', true], [1, 'p-laptop-value', 4, '68.4', false], [1, 'p-laptop-value', 4, '100', false], [1, 'p-laptop-value', 4, '0.6836', false],
  [1, 'p-rare-coin', 1, '1.5625', true], [1, 'p-rare-coin', 1, '25/16', true], [1, 'p-rare-coin', 1, '1.56', false],
  [1, 'p-rare-coin', 2, '1.25', true], [1, 'p-rare-coin', 2, '5/4', true],
  [1, 'p-rare-coin', 3, '25', true], [1, 'p-rare-coin', 3, '25%', true], [1, 'p-rare-coin', 3, '0.25', false],
  [1, 'p-rare-coin', 4, '1398', true], [1, 'p-rare-coin', 4, '1397', true], [1, 'p-rare-coin', 4, '1397.54', true], [1, 'p-rare-coin', 4, '1397.5', true], [1, 'p-rare-coin', 4, '1399', false], [1, 'p-rare-coin', 4, '1396', false], [1, 'p-rare-coin', 4, '1406', false],
  [1, 'p-curve-point', 1, '4', true], [1, 'p-curve-point', 2, '0.5', true], [1, 'p-curve-point', 2, '1/2', true],
  [1, 'p-curve-point', 3, '5.5', true], [1, 'p-curve-point', 3, '11/2', true], [1, 'p-curve-point', 4, '-5.5', true], [1, 'p-curve-point', 4, '-11/2', true],
  [2, 'p-fault-search', 1, '11', true], [2, 'p-fault-search', 2, '16', true], [2, 'p-fault-search', 3, '19', true],
  [2, 'p-forty-doublings', 1, '12.0412', true], [2, 'p-forty-doublings', 1, '12.04120', true], [2, 'p-forty-doublings', 1, '12.04', false],
  [2, 'p-forty-doublings', 2, '12', true], [2, 'p-forty-doublings', 3, '1.10', true], [2, 'p-forty-doublings', 3, '1.1', true], [2, 'p-forty-doublings', 3, '1.0995', true], [2, 'p-forty-doublings', 3, '1.09', false],
  [2, 'p-forty-doublings', 4, '14', true], [2, 'p-forty-doublings', 4, '13', false], [2, 'p-forty-doublings', 4, '10', false],
  [2, 'p-drawdown-recovery', 1, '32000', true], [2, 'p-drawdown-recovery', 1, '32,000', true],
  [2, 'p-drawdown-recovery', 2, '56.25', true], [2, 'p-drawdown-recovery', 2, '56.25%', true], [2, 'p-drawdown-recovery', 2, '56.3', false],
  [2, 'p-drawdown-recovery', 3, '4.28', true], [2, 'p-drawdown-recovery', 3, '4.2764', true], [2, 'p-drawdown-recovery', 3, '4.2767', true], [2, 'p-drawdown-recovery', 3, '4.27', false], [2, 'p-drawdown-recovery', 3, '4.29', false], [2, 'p-drawdown-recovery', 3, '5.80', false],
  [2, 'p-drawdown-recovery', 4, '5', true], [2, 'p-drawdown-recovery', 4, '4', false], [2, 'p-drawdown-recovery', 4, '6', false],
  [2, 'p-app-users', 1, '2000\\cdot1.3^n', true], [2, 'p-app-users', 1, '2000*1.3^n', true], [2, 'p-app-users', 1, '2000\\left(\\frac{13}{10}\\right)^n', true],
  [2, 'p-app-users', 1, '2000\\cdot1.03^n', false], [2, 'p-app-users', 1, '2000\\cdot1.3n', false],
  [2, 'p-app-users', 3, '12.27', true], [2, 'p-app-users', 3, '12.273', true], [2, 'p-app-users', 3, '12.3', false],
  [2, 'p-app-users', 4, '13', true],
  [3, 'p-savings-doubling', 1, '2400e^{0.055t}', true], [3, 'p-savings-doubling', 1, '2400\\exp(0.055t)', true], [3, 'p-savings-doubling', 1, '2400e^{\\frac{5.5t}{100}}', true],
  [3, 'p-savings-doubling', 1, '2400\\cdot e^{0.055}\\cdot t', false], [3, 'p-savings-doubling', 1, '2400\\cdot1.055^t', false], [3, 'p-savings-doubling', 1, '2400e^{0.55t}', false],
  [3, 'p-savings-doubling', 2, '12.60', true], [3, 'p-savings-doubling', 2, '12.6', true], [3, 'p-savings-doubling', 2, '12.59', false],
  [3, 'p-savings-doubling', 3, '37.80', true], [3, 'p-savings-doubling', 3, '37.81', true], [3, 'p-savings-doubling', 3, '37.8', true], [3, 'p-savings-doubling', 3, '37.79', false],
  [3, 'p-savings-doubling', 4, '6788', true], [3, 'p-savings-doubling', 4, '6787', true], [3, 'p-savings-doubling', 4, '6788.23', true], [3, 'p-savings-doubling', 4, '6786.73', true], [3, 'p-savings-doubling', 4, '6786', false], [3, 'p-savings-doubling', 4, '6790', false],
  [3, 'p-weekly-target', 1, '0.043', true], [3, 'p-weekly-target', 2, '41.76', true], [3, 'p-weekly-target', 2, '41.7575', true], [3, 'p-weekly-target', 2, '41.75', false],
  [3, 'p-weekly-target', 3, '0.0747', true], [3, 'p-weekly-target', 3, '0.0748', true], [3, 'p-weekly-target', 3, '0.07472', true], [3, 'p-weekly-target', 3, '0.0746', false], [3, 'p-weekly-target', 3, '0.0749', false],
  [3, 'p-weekly-target', 4, '0.0249', true], [3, 'p-weekly-target', 4, '0.02493', true], [3, 'p-weekly-target', 4, '0.02490', true], [3, 'p-weekly-target', 4, '0.024908', true], [3, 'p-weekly-target', 4, '0.0248', false], [3, 'p-weekly-target', 4, '0.0250', false], [3, 'p-weekly-target', 4, '0.0259', false],
  [3, 'p-weekly-target', 5, '2.52', true], [3, 'p-weekly-target', 5, '2.521', true], [3, 'p-weekly-target', 5, '2.51', false], [3, 'p-weekly-target', 5, '0.0249', false], [3, 'p-weekly-target', 5, '2.52%', true], [3, 'p-weekly-target', 5, '2.53', false], [3, 'p-weekly-target', 5, '2.49', false],
  [3, 'p-log-chart-line', 1, '27.47', true], [3, 'p-log-chart-line', 1, '27.47%', true], [3, 'p-log-chart-line', 1, '27.5', false], [3, 'p-log-chart-line', 1, '27.46', false],
  [3, 'p-log-chart-line', 2, '2.52', true], [3, 'p-log-chart-line', 2, '2.5233', true],
  [3, 'p-log-chart-line', 3, '45', true], [3, 'p-log-chart-line', 3, '45.07', true], [3, 'p-log-chart-line', 3, '£45', true],
  [3, 'p-log-chart-line', 4, '6', true], [3, 'p-log-chart-line', 4, '6.0', true],
  [3, 'p-monthly-deposit', 1, '1.0491', true], [3, 'p-monthly-deposit', 1, '1.04907', true], [3, 'p-monthly-deposit', 1, '1.049', false], [3, 'p-monthly-deposit', 1, '1.0492', false],
  [3, 'p-monthly-deposit', 2, '4.79', true], [3, 'p-monthly-deposit', 2, '4.79%', true], [3, 'p-monthly-deposit', 2, '4.80', false],
  [3, 'p-monthly-deposit', 3, '0.2395', true], [3, 'p-monthly-deposit', 3, '0.23952', true], [3, 'p-monthly-deposit', 3, '0.24', false],
  [3, 'p-monthly-deposit', 4, '7624', true], [3, 'p-monthly-deposit', 4, '7623.68', true], [3, 'p-monthly-deposit', 4, '7623.84', true], [3, 'p-monthly-deposit', 4, '7623', false], [3, 'p-monthly-deposit', 4, '£7,624', true],
];

let checks = 0, fails = 0;
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('FAIL ' + msg); } };
const gradeNumeric = (w, text) => {
  const pct = w.unit === '%';
  let v = G.parseNum(text); if (pct && !text.includes('%')) v /= 100; else if (pct) v = G.parseNum(text.replace('%', '')) / 100;
  return Number.isFinite(v) && G.within(v, w.answer, w.tol);
};
const wrongKey = (w, text) => {
  const pct = w.unit === '%';
  let v = G.parseNum(text.replace('%', '')); if (pct) v /= 100;
  for (const x of w.wrong || []) if (G.within(v, x.value, x.tol || w.tol)) return x.id;
  return null;
};
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo); } catch { return false; } };
  return [w.answer, ...(w.accept || [])].some(eq);
};
for (const n of [1, 2, 3]) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/exp-log/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${n} ${it.id} p${i + 1}`;
    const typed = T.filter((r) => r[0] === n && r[1] === it.id && r[2] === i + 1);
    if (w.kind === 'numeric') {
      say(G.within(w.answer, w.answer, w.tol), `${where}: answer outside band`);
      for (const x of w.wrong || []) say(!G.within(x.value, w.answer, w.tol), `${where}: wrong ${x.id} inside answer band`);
      for (const x of w.wrong || []) for (const y of w.wrong || []) if (x !== y) say(!G.within(x.value, y.value, y.tol || w.tol), `${where}: wrong ${x.id} inside ${y.id}`);
      for (const r of typed) say(gradeNumeric(w, r[3]) === r[4], `${where}: typed "${r[3]}" ${r[4] ? 'refused' : 'accepted'} (wrong key ${wrongKey(w, r[3])})`);
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer), `${where}: answer not correct`);
      for (const a of w.accept || []) say(gradeExpr(w, a), `${where}: accept ${a} not correct`);
      for (const x of w.wrong || []) say(!gradeExpr(w, x.tex), `${where}: wrong ${x.id} ${x.tex} grades correct`);
      for (const r of typed) say(gradeExpr(w, r[3]) === r[4], `${where}: typed "${r[3]}" ${r[4] ? 'refused' : 'accepted'}`);
    }
  });
}
console.log(`grade: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
