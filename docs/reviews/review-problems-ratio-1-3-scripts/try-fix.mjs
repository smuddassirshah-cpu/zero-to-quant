#!/usr/bin/env node
/* Second read, ratio problems-1 to -3: the content fixes of the review tried on in-memory copies with the engine's own grader
   (numGrade of app/js/engine/grade.js). Nothing is written.

   node docs/reviews/review-problems-ratio-1-3-scripts/try-fix.mjs      (from the repo root) */
import fs from 'node:fs';
import vm from 'node:vm';

const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return r.ok ? 'OK' : r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : 'generic'); };
const load = (n) => JSON.parse(fs.readFileSync(`app/content/courses/ratio/problems-${n}.json`, 'utf8'));
const widget = (doc, id, k) => doc.items.find(i => i.id === id).parts[k - 1].widget;
let checks = 0, fails = 0;
const want = (w, text, exp, what) => { checks++; const got = num(w, text); if (got !== exp) { fails++; console.log(`FAIL ${what}: "${text}" expected ${exp}, got ${got}`); } };

const s1 = load(1), s2 = load(2), s3 = load(3);

/* finding 1: p-platform-fee part 4, wider bands for two slips */
{ const w = widget(s1, 'p-platform-fee', 4);
  w.wrong.find(x => x.id === 'one-place').tol = { abs: 0.002 };
  w.wrong.find(x => x.id === 'upside-down').tol = { abs: 0.006 };
  for (const [t, e] of [['82', 'OK'], ['81.6', 'OK'], ['81', 'OK'], ['8', 'one-place'], ['8.2', 'one-place'], ['8.16', 'one-place'], ['122', 'upside-down'], ['123', 'upside-down'], ['122.5', 'upside-down'], ['0.29', 'account-base'], ['0.3', 'account-base'], ['10', 'generic'], ['120', 'generic'], ['83', 'generic']]) want(w, t, e, 'fee part 4'); }

/* findings 2 and 7: bands that end exactly on the rounded slip, widened to 0.001 */
{ const w = widget(s1, 'p-phone-rise', 4);
  for (const id of ['upside-down', 'saving']) w.wrong.find(x => x.id === id).tol = { abs: 0.001 };
  for (const [t, e] of [['37.3', 'OK'], ['267.8', 'upside-down'], ['267.7', 'upside-down'], ['268', 'generic'], ['62.7', 'saving'], ['62.6', 'saving'], ['63', 'generic'], ['40', 'old-price']]) want(w, t, e, 'phone part 4');
  const v = widget(s2, 'p-laptop-sale', 3);
  v.wrong.find(x => x.id === 'sale-base').tol = { abs: 0.001 };
  for (const [t, e] of [['-6.5', 'OK'], ['-7.0', 'sale-base'], ['-7', 'sale-base'], ['-6.9', 'sale-base'], ['-6.95', 'sale-base'], ['6.5', 'sign'], ['-5', 'added'], ['-6.7', 'generic'], ['-7.2', 'generic']]) want(v, t, e, 'laptop part 3'); }

/* finding 5: p-phone-rise part 4 with a £14.00 deal */
{ const w = widget(load(1), 'p-phone-rise', 4);
  w.answer = 0.4357; w.accept = '43.6%';
  w.wrong = [{ id: 'old-price', value: 0.4667, tol: { abs: 0.001 } }, { id: 'upside-down', value: 2.295, tol: { abs: 0.001 } }, { id: 'saving', value: 0.5643, tol: { abs: 0.001 } }];
  for (const [t, e] of [['43.6', 'OK'], ['43.57', 'OK'], ['43.6%', 'OK'], ['43.5', 'OK'], ['44', 'generic'], ['46.7', 'old-price'], ['46.67', 'old-price'], ['229.5', 'upside-down'], ['56.4', 'saving'], ['56.43', 'saving'], ['37.3', 'generic']]) want(w, t, e, 'phone part 4, £14.00'); }

/* finding 8: p-laptop-sale part 1, a line for 15% off again */
{ const w = widget(s2, 'p-laptop-sale', 1);
  w.wrong.push({ id: 'off-again', value: 476.85, tol: { abs: 0.005 } });
  for (const [t, e] of [['660', 'OK'], ['476.85', 'off-again'], ['645.15', 'added'], ['476.9', 'generic']]) want(w, t, e, 'laptop part 1'); }

/* finding 13: p-print-run with four presses for 15 hours */
{ const a = widget(s3, 'p-print-run', 1), b = widget(s3, 'p-print-run', 2);
  a.wrong = [{ id: 'direct', value: 30, tol: { abs: 0 } }, { id: 'subtracted', value: 11, tol: { abs: 0 } }];
  b.wrong.find(x => x.id === 'direct').value = 3360; b.wrong.find(x => x.id === 'direct').tol = { abs: 0 };
  for (const [t, e] of [['7.5', 'OK'], ['7.5 hours', 'OK'], ['30', 'direct'], ['11', 'subtracted'], ['19.2', 'generic'], ['9', 'generic']]) want(a, t, e, 'print part 1');
  for (const [t, e] of [['840', 'OK'], ['3360', 'direct'], ['3,360', 'direct'], ['105', 'one-press'], ['2150.40', 'generic']]) want(b, t, e, 'print part 2'); }

/* finding 15: a unit on the franc and euro boxes */
{ const c = widget(s3, 'p-coffee-suppliers', 1); c.unit = 'CHF';
  for (const [t, e] of [['27.50', 'OK'], ['27.5', 'OK'], ['27.50 CHF', 'OK'], ['27.50 francs', 'OK'], ['29.40', 'german'], ['0.04', 'upside-down'], ['25', 'generic']]) want(c, t, e, 'coffee part 1 with unit CHF');
  for (const k of [1, 3]) { const v = widget(s3, 'p-villa-split', k); v.unit = '€';
    const key = String(v.answer);
    for (const [t, e] of [[key, 'OK'], ['€' + key, 'OK'], [key + ' euros', 'OK'], [key + '.00', 'OK']]) want(v, t, e, `villa part ${k} with unit €`);
    for (const x of v.wrong) want(v, String(x.value), x.id, `villa part ${k} with unit €`); } }

console.log(`${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
