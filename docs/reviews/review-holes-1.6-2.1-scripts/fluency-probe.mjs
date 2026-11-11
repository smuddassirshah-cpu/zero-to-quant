#!/usr/bin/env node
/* Second read of the eight level 4 Fluency sets of testing and stat-learning: every draw goes through the engine's own
   numeric grader (grade.js numGrade).
     - the answer grades correct; each wrong value grades wrong and lands on its own key (FAIL if not)
     - the typed rows fluency-read.py wrote to <draws>/rows.json (the answer rounded as asked, with more places, one place
       short, with the prompt's unit after it, worked from rounded intermediates): a row that goes against the verdict
       the reader expects is counted per family and printed once as a FINDING candidate
   node docs/reviews/review-holes-1.6-2.1-scripts/fluency-probe.mjs <draws dir>      (from the repo root, after fluency-read.py) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const dir = process.argv[2];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const grade = (w, text) => { const r = G.numGrade(w, text); return { ok: !!r.ok, key: r.key || (r.detail.value == null ? 'NOPARSE' : null) }; };

let checks = 0, fails = 0; const find = {}, per = {};
for (const d of JSON.parse(fs.readFileSync(path.join(dir, 'rows.json'), 'utf8'))) {
  const w = d.spec, where = `${d.family} seed ${d.seed}`;
  per[d.family] = (per[d.family] || 0) + 1;
  checks++; if (!grade(w, String(w.answer)).ok) { fails++; console.log(`FAIL    ${where}: the answer ${w.answer} does not grade correct`); }
  for (const x of w.wrong) {
    checks++; const r = grade(w, String(x.value));
    if (r.ok || r.key !== x.id) { fails++; console.log(`FAIL    ${where}: wrong ${x.id} ${x.value} grades ok=${r.ok} key=${r.key}`); }
  }
  for (const [text, want, why] of d.rows) {
    checks++;
    const r = grade(w, text);
    if (r.ok !== want) { const k = `${d.family}: ${why} is ${r.ok ? 'accepted' : 'refused (key ' + r.key + ')'}`; (find[k] = find[k] || []).push(`"${text}"   [${d.prompt}]`); }
  }
}
console.log('rows that went against the reader (FINDING candidates), with the number of draws and one example:');
for (const [k, v] of Object.entries(find)) console.log(`  [${v.length} of ${per[k.split(':')[0]]}] ${k}\n        e.g. ${v[0]}`);
console.log(`fluency-probe: ${checks} checks, ${fails} failures, ${Object.keys(find).length} finding classes`);
process.exit(fails ? 1 : 0);
