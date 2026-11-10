#!/usr/bin/env node
/* Audit for ENGINE-BACKLOG 836 (plain-text function names in graded answers; docs/AUTHORING.md `expression`).
   Before the fix a plain-text `ln(97)/ln(4)` was read as the letters l, n, (97) and so equalled 97/4. This lists every expression `answer`,
   `accept[]`, set `answers[]` and `wrong[].tex` in app/content (lessons, quizzes, exams, bank, homework, and Fluency families, drawn on five
   seeds each) whose text holds ln, log, exp, sin, cos, tan or sqrt directly before a bracket, and says what the fix did to it:

     CHANGED    the grader before the fix read the text as something else (a product of letters), so for answer/accept the entry took a wrong
                value, and for a wrong[] entry it never matched the slip it names
     DEAD       before the fix the entry could not do its job: an answer/accept whose intended value no form of the widget accepted (a correct
                typed answer was refused), a wrong[] whose own intended slip did not route to it, or text that did not parse at all
     STILL-DEAD as DEAD, and the entry does not read after the fix either (a text-mode spelling such as `**` or `e^(3x)`): content to repair, not
                an engine fault
     WRONG-OK   a wrong[] value of the same widget that the grader before the fix graded CORRECT and the grader after the fix does not
     same       no change in meaning

   Entries printed as CHANGED, DEAD or WRONG-OK are the ones whose grading was wrong before the fix. Content is read, never written.

   node tools/audit-plain-functions.mjs --local-cdn <pkgs> [--before <grade.js>] [--quiet]
   --before   the grade.js to compare with; default is the one in commit 657ce91c (git show, read only).
   The grade.js after the fix is app/js/engine/grade.js, which must export plainFns. Exit 0; 2 on a setup problem. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { gen, loadSet } from './fluency-rules.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const argv = process.argv.slice(2);
const arg = (k) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? path.resolve(argv[i + 1]) : null; };
const die = (m) => { console.error('audit-plain-functions: ' + m); process.exit(2); };
const cdn = arg('--local-cdn') || (process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null);
const ceFile = cdn && path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
if (!ceFile || !fs.existsSync(ceFile)) die('give --local-cdn <pkgs> (or ZQ_LOCAL_CDN) with the local Compute Engine');
let beforeSrc;
if (arg('--before')) beforeSrc = fs.readFileSync(arg('--before'), 'utf8');
else { try { beforeSrc = execFileSync('git', ['show', '657ce91c:app/js/engine/grade.js'], { cwd: APP, encoding: 'utf8', maxBuffer: 1 << 26 }); } catch { die('cannot read grade.js of commit 657ce91c; give --before <grade.js>'); } }

const load = (src) => {
  const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
  g.window = g; g.globalThis = g; vm.createContext(g);
  vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
  const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
  g.ZQ = {}; vm.runInContext(src, g);
  return { G: g.ZQ.grade, ce };
};
const B = load(beforeSrc), A = load(fs.readFileSync(path.join(APP, 'js/engine/grade.js'), 'utf8'));
if (typeof A.G.plainFns !== 'function') die('app/js/engine/grade.js does not export plainFns');
const eqB = (a, b, o) => { try { return !!B.G.exprEqual(B.ce, a, b, o); } catch { return false; } };
const eqA = (a, b, o) => { try { return !!A.G.exprEqual(A.ce, a, b, o); } catch { return false; } };

const RE = /(?<![A-Za-z\\])(ln|log|exp|sin|cos|tan|sqrt)\s*\(/;
const files = [];
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).forEach((e) => { const p = path.join(d, e.name); if (e.isDirectory()) walk(p); else if (e.name.endsWith('.json') && e.name !== 'manifest.json') files.push(p); });
walk(path.join(APP, 'content'));

/* widgets: { where, w: { answer, answers, accept, wrong: [{ id, tex }], functions, integers }, raw: [role, text, ...] entries holding a name } */
const widgets = [];
const widgetOf = (v, wrong) => ({ answer: v.answer, answers: v.answers, accept: v.accept, wrong: (wrong || []).filter((x) => x && typeof x.tex === 'string'), functions: v.functions || [], integers: v.integers || [] });
const entriesOf = (w) => [
  ...(typeof w.answer === 'string' ? [['answer', w.answer]] : []), ...(w.answers || []).filter((x) => typeof x === 'string').map((x) => ['answer', x]),
  ...(w.accept || []).filter((x) => typeof x === 'string').map((x) => ['accept', x]), ...w.wrong.map((x) => ['wrong:' + x.id, x.tex]),
];
const find = (v, file, p) => {
  if (Array.isArray(v)) v.forEach((x, i) => find(x, file, `${p}[${i}]`));
  else if (v && typeof v === 'object') {
    if (v.kind === 'expression' && (typeof v.answer === 'string' || Array.isArray(v.answers))) widgets.push({ where: `${path.relative(APP, file)} ${p}`, w: widgetOf(v, v.wrong) });
    Object.entries(v).forEach(([k, x]) => find(x, file, `${p}.${k}`));
  }
};
files.filter((f) => !/fluency-[^/]*\.json$/.test(f)).forEach((f) => { try { find(JSON.parse(fs.readFileSync(f, 'utf8')), f, ''); } catch { /* not content JSON */ } });
/* Fluency families: the templates are drawn (five seeds), each draw is a widget */
const fluencyFiles = files.filter((f) => /fluency-[^/]*\.json$/.test(f));
for (const f of fluencyFiles) {
  let doc; try { doc = JSON.parse(fs.readFileSync(f, 'utf8')); } catch { continue; }
  for (const fam of doc.families || []) {
    if (!fam.widget || fam.widget.kind !== 'expression') continue;
    const raw = [fam.widget.answer, ...(fam.widget.answers || []), ...(fam.widget.accept || []), ...(fam.wrong || []).map((x) => x.tex)].filter((x) => typeof x === 'string');
    if (!raw.some((t) => RE.test(t))) continue;
    if (gen.checkFamily(fam).length) continue;
    const r = gen.sample(fam, { seeds: 5, set: doc.id });
    (r.items || []).forEach((it) => widgets.push({ where: `${path.relative(APP, f)} family ${fam.id} seed ${it.seed}`, fluency: fam.id, w: widgetOf(it.widget, it.wrong) }));
  }
}

const out = [], counts = { entries: 0, changed: 0, dead: 0, still: 0, wrongOk: 0, bad: 0 };
const seenLine = new Set();
for (const { where, w, fluency } of widgets) {
  const o = { functions: w.functions, integers: w.integers };
  const all = [...(typeof w.answer === 'string' ? [w.answer] : []), ...(w.answers || []), ...(w.accept || [])].filter((x) => typeof x === 'string');
  for (const [role, text] of entriesOf(w)) {
    if (!RE.test(text)) continue;
    const intended = A.G.plainFns(text);
    const selfOk = eqB(text, text, o);
    const same = selfOk && eqB(text, intended, o);
    let status = 'same', why = '';
    if (!same) {
      status = 'CHANGED';
      if (!selfOk) { status = 'DEAD'; why = 'did not parse before the fix'; }
      else if (role === 'answer' || role === 'accept') {
        if (!all.some((f) => eqB(intended, f, o))) { status = 'DEAD'; why = 'the intended value was refused before the fix (the entry took a different value)'; }
        else why = 'the entry took a different (wrong) value before the fix; the intended value was accepted by another form';
      } else if (!eqB(intended, text, o)) { status = 'DEAD'; why = 'the slip it names did not route to it before the fix'; }
    }
    if (status !== 'same' && !eqA(text, text, o)) { status = status === 'DEAD' ? 'STILL-DEAD' : status; why += (why ? '; ' : '') + 'and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)'; }
    const key = `${fluency ? where.replace(/ seed \d+$/, '') : where}|${role}|${text}|${status}`;
    if (seenLine.has(key)) continue;
    seenLine.add(key);
    counts.entries++;
    if (status !== 'same') { counts[status === 'DEAD' ? 'dead' : status === 'STILL-DEAD' ? 'still' : 'changed']++; counts.bad++; }
    out.push(`${status.padEnd(7)} ${where.replace(/ seed \d+$/, '')}  ${role}  ${JSON.stringify(text)}${why ? '  [' + why + ']' : ''}`);
  }
  /* a wrong[] value of this widget that was graded correct before and is not now (needs a function name somewhere in the widget) */
  if (![...all, ...w.wrong.map((x) => x.tex)].some((t) => RE.test(t))) continue;
  for (const x of w.wrong) {
    const before = all.some((f) => eqB(x.tex, f, o)), after = all.some((f) => eqA(x.tex, f, o));
    if (before && !after) {
      const key = `${fluency ? where.replace(/ seed \d+$/, '') : where}|${x.id}|wrongok`;
      if (seenLine.has(key)) continue;
      seenLine.add(key); counts.wrongOk++; counts.bad++;
      out.push(`WRONG-OK ${where.replace(/ seed \d+$/, '')}  wrong:${x.id}  ${JSON.stringify(x.tex)}  [graded correct before the fix, not after]`);
    }
  }
}
const quiet = argv.includes('--quiet');
out.filter((l) => !quiet || !l.startsWith('same')).forEach((l) => console.log(l));
console.log(`expression widgets read: ${widgets.length} (Fluency families count once per draw); entries with a function name: ${counts.entries}; same ${counts.entries - counts.changed - counts.dead - counts.still}, CHANGED ${counts.changed}, DEAD ${counts.dead} (read after the fix), STILL-DEAD ${counts.still}, WRONG-OK ${counts.wrongOk}`);
console.log(`entries whose grading was wrong before the fix: ${counts.bad}`);
process.exit(0);
