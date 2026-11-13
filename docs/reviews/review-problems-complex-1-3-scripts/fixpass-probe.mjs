#!/usr/bin/env node
/* Fix pass on the second read of complex problems-1 to -3: a copy of grade-probe.mjs whose rows are fixpass-rows.json.
   Generic checks run over every typed part; the rows are the learner entries the fixes were written for.
   Second read, complex problems-1 to -3: what the engine's own graders do with each typed part.
   Loads app/js/engine/grade.js and the local Compute Engine (pattern: review-problems-1.4-c-scripts/grade-probe.mjs), then
     numeric     numGrade: the key grades correct, also with one more place, after a letter and "=", with a true minus sign
                 and with its unit; every wrong[] is refused on its own key and has a byKey line
     expression  exprGrade: the key and every accept[] grade correct; every wrong[].tex is refused on its own key and has a line
   and the reader's own strings (ROWS): T accepted, F refused on no wrong line, a wrong id = refused on that line,
   N = no number read. A row with a note is one the reader holds to be a fault (FINDING, not a failure).

   node docs/reviews/review-problems-complex-1-3-scripts/fixpass-probe.mjs --local-cdn <pkgs> [--all]      (from the repo root) */
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

const T = true, F = false, N = 'NOPARSE';
const NOTES = {
  SURD: 'a right answer in the form a + bi, with the surd and the i written beside a fraction or a decimal, is refused with the false line "not in the form a + bi" (finding 1)',
  DEC: 'the right value in decimals is refused with the generic line; the part does not say exact (finding 2)',
  NEG: 'the slip its own line describes (cosine and sine swapped gives 12 cos 120 = -6) does not reach the line (finding 3)',
  OWN: 'the value the learner\'s own answers to parts 2 and 3 (66.61 and 4665) give is refused with the generic line (finding 12)',
  VAR: 'the variance from the unrounded moments misses the `variance` band (finding 12)',
  CROSS: 'squaring each part with i^2 = -1 and no cross term, the slip the `square-parts` line describes, has no line (finding 7)',
  DEGS: 'the angle in degrees has no line in an exact-angle part (finding 5)',
  BAND: 'an exact answer of 0.5 with a band of 0.05 (finding 11)',
  UNIT: 'a one-letter unit after the number is not read, so Check stays unavailable; a `unit` on the widget reads it (finding 16, unit-probe.mjs)',
  PI: 'pi typed as a word is refused with the form line (engine note, raised by the author)',
};
/* ROWS[set][item][part] = [[text, expected, note?], ...]; expectations are the reader's; a row marked "?" is only printed */
const ROWS = JSON.parse(fs.readFileSync(new URL('./fixpass-rows.json', import.meta.url), 'utf8'));

let checks = 0, fails = 0, findings = 0, nNum = 0, nExpr = 0, nRows = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + (NOTES[note] || note) + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/complex/problems-${n}.json`, 'utf8'));
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
      if (w.unit) say(grade(w.unit === "£" ? w.unit + a : a + " " + w.unit).ok, null, `${where}: key with its unit ${w.unit} grades correct`);
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
      }
    } else return;
    const rows = ((ROWS[n] || {})[it.id] || {})[k] || [];
    for (const [text, want, note] of rows) {
      nRows++;
      const r = grade(text);
      const got = `${r.ok ? 'accepted' : 'refused'} (key ${r.key}${r.line ? ', line "' + r.line + '"' : ''})`;
      if (want === '?') { console.log(`EXPLORE ${where}: typed "${text}" is ${got}`); continue; }
      const good = want === true ? r.ok : want === false ? (!r.ok && r.key !== 'NOPARSE' && !(w.wrong || []).some((x) => x.id === r.key)) : (!r.ok && r.key === want);
      say(good, note, `${where}: typed "${text}" is ${got}, expected ${want === true ? 'accepted' : want === false ? 'refused on no wrong line' : 'refused on ' + want}`);
    }
  });
}
console.log(`grade-probe: ${checks} checks over ${nNum} numeric and ${nExpr} expression parts, ${nRows} reader rows, ${fails} failures, ${findings} findings`);
process.exit(fails ? 1 : 0);
