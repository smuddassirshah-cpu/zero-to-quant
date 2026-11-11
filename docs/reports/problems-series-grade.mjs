/* Engine graders on every part of series problems 1 to 3, plus typed strings. Run from repo root:
   node docs/reports/problems-series-grade.mjs --local-cdn <pkgs> */
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
  [1, 'p-theatre-rows', 1, '36', true], [1, 'p-theatre-rows', 1, '39', false],
  [1, 'p-theatre-rows', 2, '3n+15', true], [1, 'p-theatre-rows', 2, '15+3n', true], [1, 'p-theatre-rows', 2, '18+3(n-1)', true], [1, 'p-theatre-rows', 2, 'u_n=3n+15', true],
  [1, 'p-theatre-rows', 2, '18+3n', false], [1, 'p-theatre-rows', 2, '3n', false], [1, 'p-theatre-rows', 2, '18n+3', false],
  [1, 'p-theatre-rows', 3, '90', true], [1, 'p-theatre-rows', 3, '93', false],
  [1, 'p-theatre-rows', 4, '10', true], [1, 'p-theatre-rows', 4, '9', false], [1, 'p-theatre-rows', 4, '13', false],
  [1, 'p-pendulum-swings', 2, '80\\cdot0.9^{n-1}', true], [1, 'p-pendulum-swings', 2, '80*0.9^{(n-1)}', true], [1, 'p-pendulum-swings', 2, '\\frac{800}{9}\\cdot0.9^n', true],
  [1, 'p-pendulum-swings', 2, '80*(0.9)^(n-1)', true], [1, 'p-pendulum-swings', 2, '80\\cdot(0.9)^{n-1}', true], [1, 'p-pendulum-swings', 2, '80*0.9^(n-1)', true], [1, 'p-pendulum-swings', 2, '80*(0.9)^n', false], [1, 'p-pendulum-swings', 2, '80\\cdot0.9^n', false], [1, 'p-pendulum-swings', 2, '88-8n', false], [1, 'p-pendulum-swings', 2, '72^{n-1}', false],
  [1, 'p-pendulum-swings', 3, '47.2', true], [1, 'p-pendulum-swings', 3, '47.24', true], [1, 'p-pendulum-swings', 3, '47.2392', true], [1, 'p-pendulum-swings', 3, '47.3', false], [1, 'p-pendulum-swings', 3, '42.5', false],
  [1, 'p-pendulum-swings', 4, '8', true], [1, 'p-pendulum-swings', 4, '7', false],
  [1, 'p-daily-tablet', 1, '374.4', true], [1, 'p-daily-tablet', 1, '374.40', true], [1, 'p-daily-tablet', 1, '374', false], [1, 'p-daily-tablet', 1, '336', false],
  [1, 'p-daily-tablet', 2, '400', true], [1, 'p-daily-tablet', 2, '600', false],
  [1, 'p-daily-tablet', 3, '160\\cdot0.4^{n-1}', true], [1, 'p-daily-tablet', 3, '160*0.4^{(n-1)}', true], [1, 'p-daily-tablet', 3, '400\\cdot0.4^n', true], [1, 'p-daily-tablet', 3, '160\\left(\\frac{2}{5}\\right)^{n-1}', true],
  [1, 'p-daily-tablet', 3, '160(0.4)^(n-1)', true], [1, 'p-daily-tablet', 3, '160*(0.4)^(n-1)', true], [1, 'p-daily-tablet', 3, '160\\cdot(0.4)^{n-1}', true], [1, 'p-daily-tablet', 3, '160(0.4)^n', false], [1, 'p-daily-tablet', 3, '160*(0.6)^(n-1)', false], [1, 'p-daily-tablet', 3, '160\\cdot0.4^n', false], [1, 'p-daily-tablet', 3, '160\\cdot0.6^{n-1}', false],
  [1, 'p-daily-tablet', 4, '5', true], [1, 'p-daily-tablet', 4, '4', false],
  [1, 'p-shop-orders', 1, '60', true], [1, 'p-shop-orders', 1, '120', false],
  [1, 'p-shop-orders', 2, '1.5', true], [1, 'p-shop-orders', 2, '3/2', true], [1, 'p-shop-orders', 2, '2.25', false],
  [1, 'p-shop-orders', 4, '64\\cdot1.5^{n-1}', true], [1, 'p-shop-orders', 4, '96\\cdot1.5^{n-2}', true], [1, 'p-shop-orders', 4, '64*1.5^{(n-1)}', true], [1, 'p-shop-orders', 4, '64\\left(\\frac{3}{2}\\right)^{n-1}', true],
  [1, 'p-shop-orders', 4, '64(1.5)^(n-1)', true], [1, 'p-shop-orders', 4, '64*(1.5)^(n-1)', true], [1, 'p-shop-orders', 4, '64\\cdot(1.5)^{n-1}', true], [1, 'p-shop-orders', 4, '64(1.5)^n', false], [1, 'p-shop-orders', 4, '96*(1.5)^(n-1)', false], [1, 'p-shop-orders', 4, '96\\cdot1.5^{n-1}', false], [1, 'p-shop-orders', 4, '60n-24', false],
  [1, 'p-shop-orders', 5, '8', true], [1, 'p-shop-orders', 5, '7', false],
  [2, 'p-tin-display', 1, '53', true], [2, 'p-tin-display', 1, '58', false], [2, 'p-tin-display', 1, '50', false], [2, 'p-tin-display', 2, '305', true], [2, 'p-tin-display', 2, '610', false], [2, 'p-tin-display', 2, '265', false], [2, 'p-tin-display', 2, '330', false],
  [2, 'p-tin-display', 3, '7', true], [2, 'p-tin-display', 3, '6', false], [2, 'p-tin-display', 3, '10', false], [2, 'p-tin-display', 4, '266', true], [2, 'p-tin-display', 4, '228', false], [2, 'p-tin-display', 4, '243', false], [2, 'p-tin-display', 4, '305', false],
  [2, 'p-app-users', 1, '972', true], [2, 'p-app-users', 2, '1456', true], [2, 'p-app-users', 2, '1,456', true], [2, 'p-app-users', 2, '1458', false],
  [2, 'p-app-users', 3, '2\\cdot3^n-2', true], [2, 'p-app-users', 3, '2(3^n-1)', true], [2, 'p-app-users', 3, '\\frac{4(3^n-1)}{2}', true], [2, 'p-app-users', 3, '2*3^n-2', true], [2, 'p-app-users', 3, 'S_n=2\\cdot3^n-2', true],
  [2, 'p-app-users', 3, '4\\cdot3^n-4', false], [2, 'p-app-users', 3, '2\\cdot3^{n-1}-2', false], [2, 'p-app-users', 3, '2\\cdot3^n', false],
  [2, 'p-app-users', 4, '10', true], [2, 'p-app-users', 4, '11', false],
  [2, 'p-bouncing-ball', 1, '7.42', true], [2, 'p-bouncing-ball', 1, '7.424', true], [2, 'p-bouncing-ball', 1, '7.43', false], [2, 'p-bouncing-ball', 1, '7.5', false],
  [2, 'p-bouncing-ball', 2, '19.85', true], [2, 'p-bouncing-ball', 2, '19.84', true], [2, 'p-bouncing-ball', 2, '19.8488', true], [2, 'p-bouncing-ball', 2, '19.86', false], [2, 'p-bouncing-ball', 2, '19.83', false],
  [2, 'p-bouncing-ball', 3, '7.5', true], [2, 'p-bouncing-ball', 3, '15/2', true], [2, 'p-bouncing-ball', 3, '12.5', false],
  [2, 'p-bouncing-ball', 4, '20', true], [2, 'p-bouncing-ball', 4, '12.5', false],
  [2, 'p-two-repayment-plans', 1, '5n^2+45n', true], [2, 'p-two-repayment-plans', 1, '\\frac{n}{2}(100+10(n-1))', true], [2, 'p-two-repayment-plans', 1, '5n(n+9)', true],
  [2, 'p-two-repayment-plans', 1, 'n/2*(2*50+10(n-1))', true], [2, 'p-two-repayment-plans', 1, '\\frac{n(10n+90)}{2}', true],
  [2, 'p-two-repayment-plans', 1, '5n^2+50n', false], [2, 'p-two-repayment-plans', 1, '10n+40', false],
  [2, 'p-two-repayment-plans', 2, '21', true], [2, 'p-two-repayment-plans', 2, '20', false],
  [2, 'p-two-repayment-plans', 3, '2000', true], [2, 'p-two-repayment-plans', 3, '2,000', true], [2, 'p-two-repayment-plans', 3, '£2,000', true], [2, 'p-two-repayment-plans', 3, '1800', false],
  [2, 'p-two-repayment-plans', 4, '1781', true], [2, 'p-two-repayment-plans', 4, '1782', true], [2, 'p-two-repayment-plans', 4, '1781.16', true], [2, 'p-two-repayment-plans', 4, '£1,781', true], [2, 'p-two-repayment-plans', 4, '1780', false], [2, 'p-two-repayment-plans', 4, '1757', false],
  [2, 'p-two-repayment-plans', 5, '1219', true], [2, 'p-two-repayment-plans', 5, '1218', true], [2, 'p-two-repayment-plans', 5, '1,219', true], [2, 'p-two-repayment-plans', 5, '1000', false], [2, 'p-two-repayment-plans', 5, '1220', false],
  [3, 'p-pizza-toppings', 1, '330', true], [3, 'p-pizza-toppings', 1, '7920', false], [3, 'p-pizza-toppings', 1, '44', false], [3, 'p-pizza-toppings', 1, '1320', false],
  [3, 'p-pizza-toppings', 2, '660', true], [3, 'p-pizza-toppings', 2, '330', false],
  [3, 'p-pizza-toppings', 3, '495', true], [3, 'p-pizza-toppings', 3, '341', false], [3, 'p-pizza-toppings', 3, '660', false], [3, 'p-pizza-toppings', 3, '11880', false],
  [3, 'p-pizza-toppings', 4, '4096', true], [3, 'p-pizza-toppings', 4, '4095', false], [3, 'p-pizza-toppings', 4, '2048', false],
  [3, 'p-bracket-estimate', 1, '189', true], [3, 'p-bracket-estimate', 1, '-189', false],
  [3, 'p-bracket-estimate', 2, '1-21x+189x^2', true], [3, 'p-bracket-estimate', 2, '189x^2-21x+1', true], [3, 'p-bracket-estimate', 2, '1-21x+189x^{2}', true],
  [3, 'p-bracket-estimate', 2, '1+21x+189x^2', false], [3, 'p-bracket-estimate', 2, '1-21x', false], [3, 'p-bracket-estimate', 2, '(1-3x)^7', false],
  [3, 'p-bracket-estimate', 3, '0.8089', true], [3, 'p-bracket-estimate', 3, '0.80890', true], [3, 'p-bracket-estimate', 3, '0.809', false], [3, 'p-bracket-estimate', 3, '0.8080', false],
  [3, 'p-bracket-estimate', 4, '-945', true], [3, 'p-bracket-estimate', 4, '945', false],
  [3, 'p-bracket-estimate', 5, '0.80796', true], [3, 'p-bracket-estimate', 5, '0.80795', true], [3, 'p-bracket-estimate', 5, '0.80798', false], [3, 'p-bracket-estimate', 5, '0.807983', false], [3, 'p-bracket-estimate', 5, '0.807955', true], [3, 'p-bracket-estimate', 5, '0.80799', false], [3, 'p-bracket-estimate', 5, '0.8080', false], [3, 'p-bracket-estimate', 5, '0.80985', false],
  [3, 'p-gym-membership', 1, '1.06165', true], [3, 'p-gym-membership', 1, '1.06168', false], [3, 'p-gym-membership', 1, '1.0617', false],
  [3, 'p-gym-membership', 2, '0.9419', true], [3, 'p-gym-membership', 2, '0.94189', true], [3, 'p-gym-membership', 2, '0.94190', true], [3, 'p-gym-membership', 2, '0.9418', false], [3, 'p-gym-membership', 2, '0.942', false],
  [3, 'p-gym-membership', 3, '1162', true], [3, 'p-gym-membership', 3, '1161', true], [3, 'p-gym-membership', 3, '£1,162', true], [3, 'p-gym-membership', 3, '1161.89', true], [3, 'p-gym-membership', 3, '1200', false], [3, 'p-gym-membership', 3, '1160', false],
  [3, 'p-gym-membership', 4, '12', true], [3, 'p-gym-membership', 4, '11', true], [3, 'p-gym-membership', 4, '£12', true], [3, 'p-gym-membership', 4, '50', false], [3, 'p-gym-membership', 4, '13', false],
  [3, 'p-powers-of-eleven', 1, '14641', true], [3, 'p-powers-of-eleven', 1, '14,641', true], [3, 'p-powers-of-eleven', 1, '10001', false],
  [3, 'p-powers-of-eleven', 2, '161051', true], [3, 'p-powers-of-eleven', 2, '161,051', true], [3, 'p-powers-of-eleven', 2, '15101051', false],
  [3, 'p-powers-of-eleven', 3, '1.61051', true], [3, 'p-powers-of-eleven', 3, '1.6105', false], [3, 'p-powers-of-eleven', 4, '0.11051', true], [3, 'p-powers-of-eleven', 4, '0.1105', false],
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
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo) || (!!G.normExpr(L) && G.normExpr(L) === G.normExpr(t)); } catch { return false; } };
  return [w.answer, ...(w.accept || [])].some(eq);
};
for (const n of [1, 2, 3]) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/series/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${n} ${it.id} p${i + 1}`;
    const typed = T.filter((r) => r[0] === n && r[1] === it.id && r[2] === i + 1);
    if (w.kind === 'numeric') {
      say(G.within(w.answer, w.answer, w.tol), `${where}: answer outside band`);
      for (const x of w.wrong || []) say(!G.within(x.value, w.answer, w.tol), `${where}: wrong ${x.id} inside answer band`);
      for (const x of w.wrong || []) for (const y of w.wrong || []) if (x !== y) say(!G.within(x.value, y.value, y.tol || w.tol), `${where}: wrong ${x.id} inside ${y.id}`);
      for (const x of w.wrong || []) { const k = wrongKey(w, String(x.value)); say(k === x.id, `${where}: wrong ${x.id} value ${x.value} lands on ${k}`); }
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
