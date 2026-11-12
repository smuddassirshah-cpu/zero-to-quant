#!/usr/bin/env node
/* Second read, vectors: does the content-side fix proposed for finding 1 work? On an in-memory copy of each matrix part, every
   wrong entry gets a twin with the same id and its tex retyped in the asked form [[a, b], [c, d]]. Each wrong matrix is then
   graded as the learner would type it (plain and in MathLive's \left\lbrack form, and with a decimal entry as a fraction).
   No content file is written.

   node docs/reviews/review-problems-1.4-a-scripts/try-fix.mjs --local-cdn <pkgs>      (from the repo root) */
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
const rowsOf = (tex) => /\\begin\{pmatrix\}(.*)\\end\{pmatrix\}/.exec(tex)[1].split('\\\\').map(r => r.split('&').map(s => s.trim()));
const asked = (rows) => `[[${rows.map(r => r.join(', ')).join('], [')}]]`;
const lb = '\\left\\lbrack', rb = '\\right\\rbrack';
const mathlive = (rows) => `${lb}${rows.map(r => `${lb}${r.join(',')}${rb}`).join(',')}${rb}`;
const frac = (s) => ({ '0.25': '\\frac{1}{4}', '0.5': '\\frac{1}{2}', '-0.6': '-\\frac{3}{5}', '0.6': '\\frac{3}{5}', '0.8': '\\frac{4}{5}', '0.3': '\\frac{3}{10}', '-0.1': '-\\frac{1}{10}', '0.2': '\\frac{1}{5}', '0.4': '\\frac{2}{5}' }[s] || s);

let n = 0, hit = 0, fracN = 0, fracHit = 0;
for (const set of [2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/vectors/problems-${set}.json`, 'utf8'));
  for (const it of doc.items) it.parts.forEach((p, i) => {
    const w = p.widget;
    if (w.kind !== 'expression' || !/pmatrix/.test(w.answer)) return;
    const fixed = { ...w, wrong: [...w.wrong, ...w.wrong.map(x => ({ id: x.id, tex: asked(rowsOf(x.tex)) }))] };
    for (const x of w.wrong) {
      const rows = rowsOf(x.tex);
      for (const text of [asked(rows), mathlive(rows)]) { const r = G.exprGrade(ce, fixed, text, text); n++; if (!r.ok && r.key === x.id) hit++; else console.log(`MISS problems-${set} ${it.id} ${i + 1} ${x.id}: "${text}" -> ok=${r.ok} key=${r.key}`); }
      const fr = rows.map(r => r.map(frac));
      if (JSON.stringify(fr) !== JSON.stringify(rows)) { const text = asked(fr); const r = G.exprGrade(ce, fixed, text, text); fracN++; if (!r.ok && r.key === x.id) fracHit++; else console.log(`miss (fraction entries) problems-${set} ${it.id} ${i + 1} ${x.id}: "${text}" -> key=${r.key}`); }
    }
    const r = G.exprGrade(ce, fixed, w.accept[0], w.accept[0]);
    if (!r.ok) console.log(`BROKEN problems-${set} ${it.id} ${i + 1}: the right answer no longer grades correct`);
  });
}
console.log(`try-fix: with a twin in the asked form, ${hit} of ${n} wrong matrices typed in that form land on their own key; ${fracHit} of ${fracN} do with decimal entries typed as fractions`);

/* finding 2: engraver part 1 with one more accept form, the factorised entry */
const eng = JSON.parse(fs.readFileSync('app/content/courses/vectors/problems-3.json', 'utf8')).items.find(i => i.id === 'p-engraver-dial').parts[0].widget;
const eng2 = { ...eng, accept: [...eng.accept, '[[2(k+3), 2+k], [5, 2]]'] };
let engOk = 0;
const typed = ['[[2(k+3), k+2], [5, 2]]', '[[2(3+k), 2+k], [5, 2]]', `${lb}${lb}2\\left(k+3\\right),k+2${rb},${lb}5,2${rb}${rb}`, '[[(k+3)2, 2+k], [5, 2]]', '[[2(k+3), 2+k], [5, 2]]'];
for (const t of typed) { const before = G.exprGrade(ce, eng, t, t).ok, after = G.exprGrade(ce, eng2, t, t).ok; if (after) engOk++; console.log(`engraver 1 "${t}": now ${before ? 'accepted' : 'refused'}, with the extra accept form ${after ? 'accepted' : 'refused'}`); }
for (const x of eng.wrong) { const t = asked(rowsOf(x.tex)); if (G.exprGrade(ce, eng2, t, t).ok) { console.log(`BROKEN: wrong ${x.id} accepted`); engOk = -99; } }
console.log(`try-fix: engraver part 1, ${engOk} of ${typed.length} factorised typings accepted with the extra accept form`);
process.exit(hit === n ? 0 : 1);
