#!/usr/bin/env node
/* Runs typed answers through the real numeric grader (app/js/engine/grade.js, no browser).
   Usage: node probe.mjs <probes.json>
   probes.json: [ { "file": "statistics-1", "id": "<item id>", "text": "34/3", "want": "ok" | "no" | "<wrong id>" | "any-no", "note": "..." } ]
   "no" means refused with no wrong line; "any-no" means refused (with or without a line).
   Prints one line per probe whose outcome differs from `want`, then a summary. Exit 1 when any differ. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..', '..', '..', 'app');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(APP, 'js', 'engine', 'grade.js'), 'utf8'), g);
const G = g.ZQ.grade;
const probes = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const cache = {};
const item = (file, id) => {
  cache[file] = cache[file] || JSON.parse(fs.readFileSync(path.join(APP, 'content', 'bank', file + '.json'), 'utf8'));
  return cache[file].items.find(i => i.id === id);
};
let bad = 0;
for (const p of probes) {
  const it = item(p.file, p.id);
  if (!it) { console.log('MISSING', p.file, p.id); bad++; continue; }
  const r = G.numGrade(it.widget, p.text);
  const got = r.ok ? 'ok' : (r.key || 'no');
  const pass = p.want === 'any-no' ? !r.ok : got === p.want;
  if (!pass) { bad++; console.log(`DIFF ${p.file}/${p.id} typed "${p.text}" -> ${got}, wanted ${p.want}${p.note ? ' (' + p.note + ')' : ''}`); }
}
console.log(`${probes.length} probes, ${bad} differ`);
process.exit(bad ? 1 : 0);
