#!/usr/bin/env node
/* Second read, level-4 problem sets: what the engine's own graders do with each typed part.
   Loader as docs/reviews/review-problems-linear-maps-1-3-scripts/grade-probe.mjs (app/js/engine/grade.js, local Compute Engine).
   For every numeric and expression part: the key and each accept[] grade correct, each wrong[] is refused on its own key.
   Then the reader's rows (rows.json: { item: { part: [[text, expected, note?]] } }): "T" accepted, "F" refused on no
   wrong line, any other string = refused on that byKey id. A row with a note is one the reader holds to be a fault
   (printed as FINDING, not counted as a failure).

   node docs/reviews/review-problems-linear-maps-4-scripts/grade-probe.mjs --file <set.json> --rows <rows.json> --local-cdn <pkgs> [--all] */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const arg = (n) => argv[argv.indexOf(n) + 1];
const ALL = argv.includes('--all');
const cdn = arg('--local-cdn');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const grader = (w) => (t) => {
  try {
    const set = G.isSetSpec(w);
    const r = w.kind === 'numeric' ? (set ? G.numSetGrade(w, t) : G.numGrade(w, t)) : (set ? G.exprSetGrade(ce, w, t) : G.exprGrade(ce, w, t, t));
    return { ok: !!r.ok, key: r.key || null, line: r.line };
  } catch (e) { return { ok: false, key: 'THROW ' + e.message }; }
};

const doc = JSON.parse(fs.readFileSync(arg('--file'), 'utf8'));
const ROWS = JSON.parse(fs.readFileSync(arg('--rows'), 'utf8'));
let checks = 0, fails = 0, findings = 0, nRows = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
for (const it of doc.items) it.parts.forEach((p, i) => {
  const k = i + 1, w = p.widget, where = `${it.id} ${k}`;
  if (w.kind !== 'numeric' && w.kind !== 'expression') return;
  const grade = grader(w), by = (p.feedback && p.feedback.byKey) || {};
  const key = G.isSetSpec(w) ? w.answers.join(', ') : String(w.answer);
  say(grade(key).ok, null, `${where}: key ${key} grades correct`);
  for (const a of (Array.isArray(w.accept) ? w.accept : [])) say(grade(a).ok, null, `${where}: accept "${a}" grades correct`);
  for (const x of w.wrong || []) {
    const t = String(x.tex != null ? x.tex : x.value), r = grade(t);
    say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${t} lands on its key (got ok=${r.ok} key=${r.key})`);
    say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
  }
  const rows = (ROWS[it.id] || {})[k] || [];
  if (!rows.length) { fails++; console.log(`FAIL    ${where}: no reader rows`); }
  for (const [text, exp, note] of rows) {
    nRows++;
    const r = grade(text);
    const good = exp === 'T' ? r.ok : exp === 'F' ? (!r.ok && !(r.key && by[r.key] && r.key !== 'count')) : (!r.ok && r.key === exp);
    say(good, note || null, `${where}: "${text}" expected ${exp}, got ok=${r.ok} key=${r.key}`);
  }
});
console.log(`${checks} checks (${nRows} reader rows), ${fails} failures, ${findings} rows held to be faults`);
process.exit(fails ? 1 : 0);
