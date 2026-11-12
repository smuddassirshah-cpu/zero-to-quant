#!/usr/bin/env node
/* Second read, vectors problems-2 and -3: the nine matrix parts ask for the matrix "row by row, as [[a, b], [c, d]]".
   This probe grades, with exprGrade and the Compute Engine as expression.js does, for each matrix part:
     - every wrong[].tex retyped in the asked form, plain and as MathLive writes it (\left\lbrack ... \right\rbrack): which key and line?
     - the right matrix in the asked form with one entry written another way (a fraction, a trailing zero, a sum, a product)
     - any other wrong matrix in the asked form: which line?
   It prints one row per string; nothing is asserted (the review reads the table).

   node docs/reviews/review-problems-1.4-a-scripts/matrix-forms.mjs --local-cdn <pkgs>      (from the repo root) */
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
const grade = (w, L) => { try { const r = G.exprGrade(ce, w, L, L); return `${r.ok ? 'ACCEPTED' : 'refused '} key ${String(r.key).padEnd(10)}${r.line ? ' line "' + r.line + '"' : ''}`; } catch (e) { return 'THROW ' + e.message; } };

const rowsOf = (tex) => /\\begin\{pmatrix\}(.*)\\end\{pmatrix\}/.exec(tex)[1].split('\\\\').map(r => r.split('&').map(s => s.trim()));
const asked = (rows) => `[[${rows.map(r => r.join(', ')).join('], [')}]]`;
const lb = '\\left\\lbrack', rb = '\\right\\rbrack';
const mathlive = (rows) => `${lb}${rows.map(r => `${lb}${r.join(',')}${rb}`).join(',')}${rb}`;

/* right matrices with an entry written another way: [set, item, part, text] */
const RIGHT = [
  [2, 'p-italic-letters', 1, '[[1, \\frac{1}{4}], [0, 1]]'], [2, 'p-italic-letters', 1, '[[1, 0.250], [0, 1]]'], [2, 'p-italic-letters', 1, '[[1, .25], [0, 1]]'], [2, 'p-italic-letters', 1, '[[1, 2/8], [0, 1]]'],
  [2, 'p-italic-letters', 3, '[[1.5, \\frac{3}{8}], [0, 1]]'], [2, 'p-italic-letters', 3, '[[1.50, 0.375], [0, 1]]'], [2, 'p-italic-letters', 3, '[[1.5, 1.5\\times0.25], [0, 1]]'], [2, 'p-italic-letters', 3, '[[\\frac{3}{2}, 0.375], [0, 1]]'],
  [2, 'p-site-plan', 1, '[[\\frac{4}{5}, -\\frac{3}{5}], [\\frac{3}{5}, \\frac{4}{5}]]'], [2, 'p-site-plan', 1, '[[0.80, -0.60], [0.60, 0.80]]'], [2, 'p-site-plan', 1, '[[.8, -.6], [.6, .8]]'],
  [2, 'p-site-plan', 2, '[[1.0, 0], [0, 1.0]]'], [2, 'p-site-plan', 2, '[[0.64+0.36, 0], [0, 1]]'],
  [3, 'p-goat-feed', 1, '[[\\frac{2}{5}, \\frac{1}{10}], [\\frac{1}{5}, \\frac{3}{10}]]'], [3, 'p-goat-feed', 1, '[[0.40, 0.10], [0.20, 0.30]]'], [3, 'p-goat-feed', 1, '[[.4, .1], [.2, .3]]'],
  [3, 'p-goat-feed', 3, '[[3.0, -1], [-2, 4]]'], [3, 'p-goat-feed', 3, '[[\\frac{0.3}{0.1}, -1], [-2, 4]]'],
  [3, 'p-colour-sensor', 2, '[[\\frac{7}{5}, -\\frac{3}{5}], [-\\frac{2}{5}, \\frac{8}{5}]]'], [3, 'p-colour-sensor', 2, '[[1.40, -0.60], [-0.40, 1.60]]'], [3, 'p-colour-sensor', 2, '[[1.4, -.6], [-.4, 1.6]]'],
  [3, 'p-engraver-dial', 1, '[[2k+6, k+2], [5, 2]]'], [3, 'p-engraver-dial', 1, '[[6+2k, k+2], [5, 2]]'], [3, 'p-engraver-dial', 1, '[[2k+6, 2+k], [5, 2]]'], [3, 'p-engraver-dial', 1, '[[2(k+3), k+2], [5, 2]]'],
  [3, 'p-engraver-dial', 1, '[[2(3+k), 2+k], [5, 2]]'], [3, 'p-engraver-dial', 1, '[[6+k\\cdot2, 2+k], [5, 2]]'], [3, 'p-engraver-dial', 1, '[[6+2k, 2+1k], [5, 2]]'], [3, 'p-engraver-dial', 1, '\\begin{pmatrix}2(k+3)&k+2\\\\5&2\\end{pmatrix}'],
  [3, 'p-engraver-dial', 4, '[[2.0, -3], [-5, 8]]'], [3, 'p-engraver-dial', 4, '[[\\frac{2}{1}, -3], [-5, 8]]'],
];
/* wrong matrices no `wrong` entry names: the line a learner reads */
const OTHER = [
  [2, 'p-italic-letters', 1, '[[1, 0.5], [0, 1]]'], [2, 'p-site-plan', 1, '[[0.8, -0.6], [0.6, -0.8]]'], [3, 'p-goat-feed', 3, '[[4, -1], [-2, 3]]'], [3, 'p-engraver-dial', 4, '[[8, 3], [5, 2]]'],
];

let total = 0, onKey = 0, asLength = 0, rightTotal = 0, rightRefused = 0;
for (const n of [2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/vectors/problems-${n}.json`, 'utf8'));
  for (const it of doc.items) it.parts.forEach((p, i) => {
    const w = p.widget;
    if (w.kind !== 'expression' || !/pmatrix/.test(w.answer)) return;
    console.log(`\n== problems-${n} ${it.id} part ${i + 1}`);
    for (const x of w.wrong || []) {
      const rows = rowsOf(x.tex);
      for (const [name, text] of [['stored pmatrix', x.tex], ['asked form', asked(rows)], ['MathLive form', mathlive(rows)], ['bare \\lbrack', mathlive(rows).replace(/\\left|\\right/g, '')], ['round brackets', asked(rows).replace(/\[/g, '(').replace(/\]/g, ')')]]) {
        const r = grade(w, text);
        console.log(`  wrong ${x.id.padEnd(11)} ${name.padEnd(15)} ${r}`);
        if (name !== 'stored pmatrix') { total++; if (r.includes(`key ${x.id}`)) onKey++; if (r.includes('key length')) asLength++; }
      }
    }
    for (const r of RIGHT.filter(r => r[0] === n && r[1] === it.id && r[2] === i + 1)) { const res = grade(w, r[3]); rightTotal++; if (!res.startsWith('ACCEPTED')) rightRefused++; console.log(`  right   ${r[3].padEnd(62)} ${res}`); }
    for (const r of OTHER.filter(r => r[0] === n && r[1] === it.id && r[2] === i + 1)) console.log(`  other   ${r[3].padEnd(62)} ${grade(w, r[3])}`);
  });
}
console.log(`\nmatrix-forms: ${total} wrong matrices retyped in the form asked; ${onKey} land on their own key, ${asLength} get the key "length"; ${rightTotal} right matrices with an entry written another way, ${rightRefused} refused`);
