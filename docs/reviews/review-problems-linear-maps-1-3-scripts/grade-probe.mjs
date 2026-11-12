#!/usr/bin/env node
/* Second read, linear-maps problems-1 to -3: what the engine's own graders do with each typed part.
   Loader as docs/reviews/review-problems-1.4-c-scripts/grade-probe.mjs (app/js/engine/grade.js and the local Compute Engine).
     numeric     numGrade: the key, with one more place, after a letter and "=", with a true minus sign;
                 every wrong[] refused on its own key, with a byKey line
     expression  exprGrade: the key and every accept[] correct; every wrong[].tex refused on its own key, with a line;
                 for a matrix part, each wrong matrix also typed whole in the [[a, b], [c, d]] form the question asks for
   then the reader's own strings (ROWS): T accepted, F refused on no wrong line, an id = refused on that line.
   A row with a note is one the reader holds to be a fault (FINDING, not a failure).

   node docs/reviews/review-problems-linear-maps-1-3-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]   (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const ALL = argv.includes('--all');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return { ok: !!r.ok, key: r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null), line: r.line }; };
const expr = (w, t) => { try { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null, line: r.line }; } catch (e) { return { ok: false, key: 'THROW ' + e.message }; } };

const T = true, F = false;
const LABEL = 'the right values typed with the letters the question names (a = 2, b = 5) are refused with the generic line';
const MATW = 'a wrong matrix typed whole in the form the question asks for does not reach its line';
/* ROWS[set][item][part] = [[text, expected, note?], ...] */
const ROWS = JSON.parse(fs.readFileSync(new URL('./rows.json', import.meta.url), 'utf8'), (k, v) => v === 'T' ? T : v === 'F' ? F : v);

const texToList = (tex) => {
  const m = /\\begin\{pmatrix\}(.*)\\end\{pmatrix\}/.exec(tex);
  if (!m) return null;
  const cell = (c) => c.trim().replace(/-\\t?frac\{(\d+)\}\{(\d+)\}/, '-$1/$2').replace(/\\t?frac\{(-?\d+)\}\{(\d+)\}/, '$1/$2');
  return '[' + m[1].split('\\\\').map((r) => '[' + r.split('&').map(cell).join(', ') + ']').join(', ') + ']';
};

let checks = 0, fails = 0, findings = 0, nNum = 0, nExpr = 0, nRows = 0, nMat = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/linear-maps/problems-${n}.json`, 'utf8'));
  for (const it of doc.items) it.parts.forEach((p, i) => {
    const k = i + 1, w = p.widget, where = `${n} ${it.id} ${k}`;
    const by = (p.feedback && p.feedback.byKey) || {};
    let grade;
    if (w.kind === 'numeric') {
      nNum++; grade = (t) => num(w, t);
      const a = String(w.answer);
      say(grade(a).ok, null, `${where}: key ${a} grades correct`);
      say(grade(a.includes('.') ? a + '0' : a + '.0').ok, null, `${where}: key with one more place grades correct`);
      say(grade('x = ' + a).ok, null, `${where}: key after a letter and = grades correct`);
      if (w.answer < 0) say(grade(a.replace('-', '−')).ok, null, `${where}: key with a true minus sign grades correct`);
      for (const x of w.wrong || []) {
        const r = grade(String(x.value));
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} lands on its key (got ok=${r.ok} key=${r.key})`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
      }
    } else if (w.kind === 'expression') {
      nExpr++; grade = (t) => expr(w, t);
      say(grade(w.answer).ok, null, `${where}: key grades correct`);
      for (const a of w.accept || []) say(grade(a).ok, null, `${where}: accept "${a}" grades correct`);
      for (const x of w.wrong || []) {
        const r = grade(x.tex);
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.tex} lands on its key (got ok=${r.ok} key=${r.key})`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
        const typed = texToList(x.tex);
        if (typed) {
          const r2 = grade(typed);
          say(!r2.ok && r2.key === x.id, MATW, `${where}: wrong "${x.id}" typed ${typed} lands on its key (got ok=${r2.ok} key=${r2.key}, line "${String(r2.line || '').slice(0, 70)}")`);
          say(!r2.ok, null, `${where}: wrong "${x.id}" typed ${typed} is refused`);
        }
      }
      if (/pmatrix/.test(w.answer)) nMat++;
    } else return;
    const rows = ((ROWS[n] || {})[it.id] || {})[k] || [];
    if (!rows.length) { fails++; console.log(`FAIL    ${where}: no reader rows`); }
    for (const [text, want, note0] of rows) {
      const note = note0 === 'LABEL' ? LABEL : note0;
      nRows++;
      const r = grade(text);
      const good = want === true ? r.ok : want === false ? (!r.ok && r.key === null) : (!r.ok && r.key === want);
      say(good, note, `${where}: "${text}" expected ${want === true ? 'accepted' : want === false ? 'refused, no line' : 'line ' + want}, got ok=${r.ok} key=${r.key}${r.line ? ' line "' + String(r.line).slice(0, 80) + '"' : ''}`);
    }
  });
}
console.log(`\ngrade-probe: ${checks} checks (${nNum} numeric, ${nExpr} expression of which ${nMat} matrix; ${nRows} reader rows), ${fails} failures, ${findings} rows held to be faults`);
process.exit(fails ? 1 : 0);
