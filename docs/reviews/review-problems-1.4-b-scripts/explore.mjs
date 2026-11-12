#!/usr/bin/env node
/* Second read, elimination and least-squares problems-1 to -3: print what the engine's graders do with any strings.
   Usage (repo root): node docs/reviews/review-problems-1.4-b-scripts/explore.mjs --local-cdn <pkgs> <course> <n> <item> <part> "text" ["text" ...]
   With no text, prints the stored answer, accept forms and wrong entries as graded. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const rest = argv.filter((a, i) => a !== '--local-cdn' && argv[i - 1] !== '--local-cdn');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const [course, n, item, part, ...texts] = rest;
const doc = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
const w = doc.items.find(i => i.id === item).parts[part - 1].widget;
const grade = (t) => {
  try {
    if (w.kind === 'numeric') { const r = G.numGrade(w, t); return `${r.ok ? 'ACCEPTED' : 'refused '} key ${r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null)}`; }
    const r = G.exprGrade(ce, w, t, t); return `${r.ok ? 'ACCEPTED' : 'refused '} key ${r.key || null}${r.line ? ' line "' + r.line + '"' : ''}`;
  } catch (e) { return 'THROW ' + e.message; }
};
const list = texts.length ? texts : [String(w.answer), ...(w.accept && Array.isArray(w.accept) ? w.accept : []), ...(w.wrong || []).map(x => x.tex != null ? x.tex : String(x.value))];
for (const t of list) console.log(`${grade(t).padEnd(34)} ${t}`);
