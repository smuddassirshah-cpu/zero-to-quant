#!/usr/bin/env node
/* Second read, linear-maps problems-1 to -3: the two `wrong` entries proposed in finding 9, tried on in-memory copies
   with the engine's own grader (loader as grade-probe.mjs). Nothing is written.
   node docs/reviews/review-problems-linear-maps-1-3-scripts/try-fix.mjs --local-cdn <pkgs>   (from the repo root) */
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
const grade = (w, t) => { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null }; };
const load = (n) => JSON.parse(fs.readFileSync(`app/content/courses/linear-maps/problems-${n}.json`, 'utf8'));
const part = (n, id, k) => load(n).items.find((i) => i.id === id).parts[k - 1];

let checks = 0, fails = 0;
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('FAIL ' + msg); } else console.log('ok   ' + msg); };
const tryAdd = (n, id, k, entry, typed) => {
  const w = part(n, id, k).widget;
  const before = w.wrong.map((x) => [x.id, x.tex]);
  w.wrong.push(entry);
  for (const t of typed) { const r = grade(w, t); say(!r.ok && r.key === entry.id, `${n} ${id} ${k}: "${t}" lands on new line ${entry.id} (got ok=${r.ok} key=${r.key})`); }
  for (const [i, tex] of before) { const r = grade(w, tex); say(!r.ok && r.key === i, `${n} ${id} ${k}: old wrong ${i} still lands`); }
  say(grade(w, w.answer).ok, `${n} ${id} ${k}: key still correct`);
  for (const a of w.accept || []) say(grade(w, a).ok, `${n} ${id} ${k}: accept ${a} still correct`);
};
tryAdd(2, 'p-futures-exposure', 4, { id: 'carried-entrywise', tex: '(\\frac{29}{6}, \\frac{35}{6})' }, ['(29/6, 35/6)', '(\\frac{29}{6},\\frac{35}{6})']);
tryAdd(3, 'p-currency-duals', 4, { id: 'carried-three', tex: '(57, 46)' }, ['(57, 46)', '(57,46)']);
console.log(`\ntry-fix: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
