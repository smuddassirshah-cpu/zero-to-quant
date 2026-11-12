#!/usr/bin/env node
/* Second read, proof problems-1 to -3: finding 3 (a threshold typed with its % sign) on in-memory copies with the engine's own
   numeric grader: the entry is read as a hundredth, and no `accept` string changes that, so the fix is a sentence in the question.
   node docs/reviews/review-problems-proof-1-3-scripts/try-fix.mjs      (from the repo root) */
import fs from 'node:fs';
import vm from 'node:vm';

const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const num = (w, t) => { const r = g.ZQ.grade.numGrade(w, t); return { ok: !!r.ok, key: r.key || null }; };
let checks = 0, fails = 0;
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('FAIL ' + msg); } };
const doc = JSON.parse(fs.readFileSync('app/content/courses/proof/problems-1.json', 'utf8'));
const it = doc.items.find((x) => x.id === 'p-fund-thresholds');
for (const [k, key] of [[2, 2], [3, 6]]) {
  const w = JSON.parse(JSON.stringify(it.parts[k].widget));
  say(!num(w, key + '%').ok && num(w, key + '%').key === null, `part ${k + 1} as it stands refuses ${key}% on the generic line (read as ${key / 100})`);
  w.accept = key + '%';
  say(!num(w, key + '%').ok, `part ${k + 1}: an accept string does not change that, so the fix is a sentence in the question`);
  for (const t of [String(key), 't = ' + key, key + ' per cent', key + ' percent']) console.log(`part ${k + 1} "${t}": ${num(w, t).ok ? 'accepted' : 'refused'}`);
  say(num(w, String(key)).ok && num(w, 't = ' + key).ok, `part ${k + 1} takes ${key} and t = ${key}`);
}
console.log(`${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
