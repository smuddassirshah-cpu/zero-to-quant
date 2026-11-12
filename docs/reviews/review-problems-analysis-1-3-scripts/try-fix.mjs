#!/usr/bin/env node
/* Second read, analysis problems-1 to -3: the content fix of finding 5 and the form tried for Engine note 1, on in-memory copies with the engine's graders.
   node docs/reviews/review-problems-analysis-1-3-scripts/try-fix.mjs --local-cdn <pkgs>      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return { ok: !!r.ok, key: r.key || null }; };
const expr = (w, t) => { try { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null }; } catch (e) { return { ok: false, key: 'THROW ' + e.message }; } };
const load = (n) => JSON.parse(fs.readFileSync(`app/content/courses/analysis/problems-${n}.json`, 'utf8'));
const part = (doc, id, k) => doc.items.find((x) => x.id === id).parts[k - 1];
let checks = 0, fails = 0;
const want = (label, r, ok, key = null) => { checks++; const good = r.ok === ok && (ok || r.key === key); if (!good) { fails++; console.log(`FAIL ${label}: ok=${r.ok} key=${r.key}`); } else console.log(`ok   ${label}: ${r.ok ? 'accepted' : 'refused on ' + r.key}`); };

/* Finding 5: p-alternating-quarters part 5. Narrow the s7 band and give the sum its own line. */
{
  const w = structuredClone(part(load(3), 'p-alternating-quarters', 5).widget);
  w.wrong.find((x) => x.id === 's7').tol = { abs: 0.00005 };
  w.wrong.push({ id: 'sum', value: 0.16, tol: { abs: 0.00004 } });
  for (const t of ['0.1597', '327/2048', '0.15967', '0.1596']) want(`f5 key form ${t}`, num(w, t), true);
  for (const t of ['0.16', '4/25', '0.160', '0.1600']) want(`f5 ${t}`, num(w, t), false, 'sum');
  for (const t of ['0.1601', '0.1600952', '0.16010']) want(`f5 ${t}`, num(w, t), false, 's7');
  want('f5 0.15625', num(w, '0.15625'), false, 's4');
  want('f5 0.4438', num(w, '0.4438'), false, 'sizes');
}

/* Engine note 1: the question retyped. Does "form": "simplified" refuse it and keep every right form? */
for (const [n, id, k, echo, rights] of [
  [1, 'p-climbing-fractions', 2, ['5-\\frac{5n-4}{n+1}'], ['\\frac{9}{n+1}', '9/(n+1)', '\\frac{9}{1+n}']],
  [2, 'p-sum-law-band', 1, ['3-\\frac{6n+1}{2n+5}', '\\left|\\frac{6n+1}{2n+5}-3\\right|'], ['\\frac{14}{2n+5}', '14/(2n+5)', '\\frac{14}{5+2n}']],
]) {
  const base = part(load(n), id, k).widget;
  for (const e of echo) { const r = expr(base, e); checks++; console.log(`now  ${id} ${k}: question retyped "${e}" is ${r.ok ? 'ACCEPTED' : 'refused on ' + r.key}`); }
  const w = structuredClone(base); w.form = 'simplified';
  // not a content fix: the form check does not see a number minus an uncombined fraction (review, Engine note 1)
  for (const e of echo) { const r = expr(w, e); checks++; console.log(`note ${id} ${k} with form simplified: retyped "${e}" is ${r.ok ? 'still ACCEPTED' : 'refused on ' + r.key}`); }
  for (const t of rights) want(`${id} ${k} with form simplified: "${t}"`, expr(w, t), true);
  for (const x of w.wrong) want(`${id} ${k} with form simplified: wrong ${x.id}`, expr(w, x.tex), false, x.id);
}
console.log(`try-fix: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
