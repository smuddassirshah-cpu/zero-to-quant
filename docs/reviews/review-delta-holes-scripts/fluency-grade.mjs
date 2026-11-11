#!/usr/bin/env node
/* Delta read, Fluency: the engine's graders on the draws of draw.sh.
   add-tops, subtract-tops, quotient (exprGrade): the answer passes; each wrong entry lands on its id; the whole fraction with
   the bottom multiplied out lands on "whole"; a top with a common factor taken out, and a factorised quotient, get the form line.
   volatility-se, assign-and-update (numGrade, bands from the family file): the 2- or 4-place answer passes, the same with a % sign
   lands on "percent-sign".  two-by-two, poisson-ratio-test: the 2-place answer and the neighbours 0.04 either side pass, 0.06 fail.
   node docs/reviews/review-delta-holes-scripts/fluency-grade.mjs <draws dir> --local-cdn <pkgs>      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
const argv = process.argv.slice(2), dir = argv[0], cdn = argv[argv.indexOf('--local-cdn') + 1];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const expr = (w, t) => { let r; try { r = G.exprGrade(ce, w, t, t); } catch (e) { return 'THROW'; } return r.ok ? true : (r.key || null); };
const num = (w, t) => { const r = G.numGrade(w, t); return r.ok ? true : (r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null)); };
const EXPR_N = 40; // expression draws graded a family (the Compute Engine is slow); numeric families use all 200
const all = (f) => JSON.parse(fs.readFileSync(path.join(dir, f + '.json'), 'utf8')).items;
const draws = (f) => all(f).slice(0, ['add-tops', 'subtract-tops', 'quotient'].includes(f) ? EXPR_N : 1e9);
const fam = (set, id) => JSON.parse(fs.readFileSync('app/content/courses/' + set + '.json', 'utf8')).families.find(f => f.id === id);
let checks = 0, fails = 0; const tally = {};
const say = (ok, msg) => { checks++; if (!ok) { fails++; if (fails < 25) console.log('FAIL    ' + msg); } };
const count = (k, hit) => { tally[k] = tally[k] || [0, 0]; tally[k][1]++; if (hit) tally[k][0]++; };
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
const lin = (v, m, c) => `${m === 1 ? '' : m === -1 ? '-' : m}${v}${c < 0 ? c : '+' + c}`;

for (const f of ['add-tops', 'subtract-tops']) for (const it of draws(f)) {
  const w = { kind: 'expression', answer: it.answer, form: it.form, wrong: it.wrong };
  say(expr(w, it.answer) === true, `${f}: answer ${it.answer}`);
  for (const x of it.wrong) say(expr(w, x.tex) === x.id, `${f}: wrong ${x.id} ${x.tex} -> ${expr(w, x.tex)}`);
  const { p, q, a, b, v } = it.vars, s = f === 'add-tops' ? 1 : -1, m = p + s * q, c0 = p * b + s * q * a;
  const open = `\\frac{${it.answer}}{${v}^2${a + b < 0 ? a + b : '+' + (a + b)}${v}${a * b < 0 ? a * b : '+' + a * b}}`;
  if (a + b !== 0) say(expr(w, open) === 'whole', `${f}: whole with the bottom multiplied out ${open} -> ${expr(w, open)}`);
  const unw = `${p}(${v}${b < 0 ? b : '+' + b})${s > 0 ? '+' : '-'}${q}(${v}${a < 0 ? a : '+' + a})`;
  say(expr(w, unw) === 'form', `${f}: the top left in brackets ${unw} -> ${expr(w, unw)}`);
  const k = gcd(m, c0);
  if (k > 1 && m !== 0) { const t = `${k}(${lin(v, m / k, c0 / k)})`; count(`${f}: a top with the common factor taken out, inner coefficient ${Math.abs(m / k) === 1 ? '1, such as 3(x-4)' : 'above 1, such as 2(4x-13)'}: refused with the form line`, expr(w, t) === 'form'); }
}
for (const it of draws('quotient')) {
  const w = { kind: 'expression', answer: it.answer, form: it.form, wrong: it.wrong };
  say(expr(w, it.answer) === true, `quotient: answer ${it.answer}`);
  for (const x of it.wrong) { const r = expr(w, x.tex); say(r === x.id || x.tex === it.answer, `quotient: wrong ${x.id} ${x.tex} -> ${r}`); }
}
const numFam = [['testing/fluency-l15-sharpness-of-the-peak', 'volatility-se', 4, true], ['stat-learning/fluency-l16-groups-nobody-labelled', 'assign-and-update', 2, true],
  ['testing/fluency-l18-counts-against-expectations', 'two-by-two', 2, false], ['testing/fluency-l17-ratio-of-likelihoods', 'poisson-ratio-test', 2, false]];
for (const [set, id, dp, pct] of numFam) {
  const F = fam(set, id);
  for (const it of draws(id)) {
    const w = { kind: 'numeric', answer: it.answer, tol: it.tol, wrong: it.wrong.map(x => ({ ...x, tol: (F.wrong.find(y => y.id === x.id) || {}).tol })) };
    const t = (+it.answer).toFixed(dp);
    say(num(w, t) === true, `${id}: ${t} accepted (got ${num(w, t)})`);
    for (const x of w.wrong) say(num(w, String(x.value)) === x.id, `${id}: wrong ${x.id} ${x.value} -> ${num(w, String(x.value))}`);
    if (pct) { say(num(w, t + '%') === 'percent-sign', `${id}: "${t}%" -> ${num(w, t + '%')}`); say(num(w, t + ' %') === 'percent-sign', `${id}: "${t} %" -> ${num(w, t + ' %')}`); }
    else {
      say(num(w, (+t + 0.04).toFixed(2)) === true && num(w, (+t - 0.04).toFixed(2)) === true, `${id}: 0.04 either side of ${t} accepted`);
      say(num(w, (+t + 0.06).toFixed(2)) !== true && num(w, (+t - 0.06).toFixed(2)) !== true, `${id}: 0.06 either side of ${t} refused`);
    }
  }
}
for (const [k, [h, n]] of Object.entries(tally)) console.log(`   ${k}: ${h} of ${n} draws`);
console.log(`fluency-grade: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
