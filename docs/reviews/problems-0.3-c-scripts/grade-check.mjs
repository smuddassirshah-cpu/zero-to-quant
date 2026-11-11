#!/usr/bin/env node
/* Second read, problems 0.3 c: what the engine's own graders do with each part of series 1 to 3 and trig 1 to 3.
   Harness as problems-0.2-b-scripts/grade-check.mjs (app/js/engine/grade.js and the local Compute Engine); the numeric
   path is the widget's (parseNum, within, matchWrong with the 1e-9 fallback, numSetGrade), the expression path is the
   widget's equal() (exprEqual, then the normExpr text fallback) and its form check for "exact-angle".
   Every answer and accept[] form must grade correct; every wrong[] must grade wrong and land on its own key; every
   feedback line printed after "correct" that ends in a number must be accepted; every TYPED row must grade as expected.
   A TYPED row whose note starts with "F" is one the reader holds to be a fault: it prints as FINDING when it happens.
   --show prints what every typed row did.

   node docs/reviews/problems-0.3-c-scripts/grade-check.mjs --local-cdn <pkgs> [--show]      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { TYPED } from './typed.mjs';

const argv = process.argv.slice(2);
const SHOW = argv.includes('--show');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = {}; vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

const SETS = [['series', 1], ['series', 2], ['series', 3], ['trig', 1], ['trig', 2], ['trig', 3]];
let checks = 0, fails = 0, findings = 0, rows = 0;
const say = (ok, finding, msg) => { checks++; if (ok) return; if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };

const isSet = (w) => G.isSetSpec(w) && w.unordered === true;
const gradeNumeric = (w, text) => {
  if (isSet(w)) { const r = G.numSetGrade(w, text); if (r.detail && r.detail.value === null) return { ok: false, key: 'NOPARSE' }; return { ok: !!r.ok, key: r.key }; }
  const v = G.parseNum(text);
  if (!Number.isFinite(v)) return { ok: false, key: 'NOPARSE' };
  if (G.within(v, +w.answer, w.tol)) return { ok: true, key: null };
  const m = G.matchWrong(v, w.wrong, { abs: 1e-9 }); return { ok: false, key: m ? m.id : null };
};
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo) || (!!G.normExpr(L) && G.normExpr(L) === G.normExpr(t)); } catch { return false; } };
  const same = [w.answer, ...(w.accept || [])].some(eq);
  if (same) return (w.form === 'exact-angle' ? G.shapeExactAngle(L) : true) ? { ok: true, key: null } : { ok: false, key: 'form' };
  const x = (w.wrong || []).find(x => x.tex && eq(x.tex));
  return { ok: false, key: x ? x.id : null };
};

for (const [course, n] of SETS) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${course} ${n} ${it.id} part ${i + 1}`, by = (p.feedback && p.feedback.byKey) || {};
    const typed = TYPED.filter((r) => r[0] === course && r[1] === n && r[2] === it.id && r[3] === i + 1);
    const grade = w.kind === 'numeric' ? (t) => gradeNumeric(w, t) : w.kind === 'expression' ? (t) => gradeExpr(w, t) : null;
    if (!grade) return;
    if (w.kind === 'numeric') {
      const key = isSet(w) ? w.answers.join(', ') : String(w.answer);
      say(grade(key).ok, null, `${where}: the key ${key} is not correct`);
      /* the number the accept line opens with, and each "is also accepted" number */
      const acc = String(w.accept || '');
      for (const m of acc.matchAll(/(^|\(|or )(-?\d[\d.]*(?:\/\d+)?)(?= to \d|,| is also|\)|$| \()/g)) say(grade(m[2]).ok, null, `${where}: accept line names ${m[2]}, which is refused`);
      for (const x of w.wrong || []) {
        const r = grade(String(x.value));
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} grades ${r.ok ? 'correct' : 'to key ' + r.key}`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has no byKey line`);
      }
    } else {
      say(grade(w.answer).ok, null, `${where}: the key ${w.answer} is not correct`);
      for (const a of w.accept || []) say(grade(a).ok, null, `${where}: accept ${a} is not correct`);
      for (const x of w.wrong || []) {
        const r = grade(x.tex);
        say(!r.ok && r.key === x.id, !r.ok && r.key ? 'two wrong entries are one expression' : null, `${where}: wrong "${x.id}" ${x.tex} grades ${r.ok ? 'correct' : 'to key ' + r.key}`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has no byKey line`);
      }
    }
    for (const r of typed) {
      rows++;
      const res = grade(r[4]), note = r[6] || '';
      if (SHOW) console.log(`      ${where}: "${r[4]}" -> ${res.ok ? 'correct' : 'wrong'} (key ${res.key})`);
      if (note === 'NOPARSE') { say(res.key === 'NOPARSE', null, `${where}: typed "${r[4]}" was read after all (${res.ok ? 'correct' : 'wrong'})`); continue; }
      if (note.startsWith('F key ')) { say(res.key !== note.slice(6), note.slice(2), `${where}: typed "${r[4]}" is told "${note.slice(6)}": ${by[note.slice(6)]}`); continue; }
      say(res.ok === r[5], note.startsWith('F') ? note.slice(2) : null, `${where}: typed "${r[4]}" ${r[5] ? 'refused' : 'accepted'} (key ${res.key})`);
    }
  });
}
console.log(`grade-check: ${checks} checks (${rows} typed rows), ${fails} failures, ${findings} rows held to be faults`);
process.exit(fails ? 1 : 0);
