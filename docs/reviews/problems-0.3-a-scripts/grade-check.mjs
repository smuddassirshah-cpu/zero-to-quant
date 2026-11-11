#!/usr/bin/env node
/* Second read, problems 0.3 (a): what the engine's own graders do with each part of counting 1 to 3 and functions 4.
   Harness as problems-0.2-a-scripts/grade-check.mjs (app/js/engine/grade.js and the local Compute Engine), plus the
   vector "length" line (exprShapeLine) that the expression widget gives a wrong-sized vector.
   Every answer and accept[] form must grade correct, every wrong[] must grade wrong and land on its own key, and every TYPED
   row must grade as expected. A TYPED row with a 7th field is one the reader holds to be a fault: it prints as FINDING.
   --probe prints what every TYPED row does, without judging it.

   node docs/reviews/problems-0.3-a-scripts/grade-check.mjs --local-cdn <pkgs> [--probe]      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const probe = argv.includes('--probe');
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = {}; vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

const SETS = [['counting', 1], ['counting', 2], ['counting', 3], ['functions', 4]];
const T = true, F = false;
const C = 'counting', FN = 'functions';
const PM = (a, b) => `\\begin{pmatrix}${a}\\\\${b}\\end{pmatrix}`;
const RETYPE = 'the unsimplified line the question itself prints grades correct on a "simplest form" part';
/* [course, set, item, part (1-based), typed text, expected, finding?]
   A numeric field is a plain text input: a number with a unit word after it ("22 cm", "115°") does not parse, so the
   field does not submit it; those rows are expected false. A sum of vectors left unadded returns the "length" line. */
const TYPED = [
  // counting 1: whole-number counts
  [C, 1, 'p-tulip-bed', 4, '6720', T], [C, 1, 'p-tulip-bed', 4, '6,720', T], [C, 1, 'p-tulip-bed', 4, '6 720', T], [C, 1, 'p-tulip-bed', 3, '1,680', T],
  [C, 1, 'p-tulip-bed', 1, '70.0', T], [C, 1, 'p-tulip-bed', 2, '4!', F], [C, 1, 'p-team-photo', 1, '5,040', T], [C, 1, 'p-team-photo', 1, '7!', F],
  [C, 1, 'p-team-photo', 4, '192', T], [C, 1, 'p-five-a-side', 3, '9', T], [C, 1, 'p-five-a-side', 3, '-8', F], [C, 1, 'p-ice-cream-van', 4, '12,740', T],
  [C, 1, 'p-ice-cream-van', 3, '2,548', T],
  // counting 2: chances as a fraction or a decimal to 3 places
  [C, 2, 'p-signal-flags', 4, '5/7', T], [C, 2, 'p-signal-flags', 4, '75/105', T], [C, 2, 'p-signal-flags', 4, '0.714', T], [C, 2, 'p-signal-flags', 4, '0.7143', T],
  [C, 2, 'p-signal-flags', 4, '0.71', F], [C, 2, 'p-signal-flags', 4, '0.7', F],
  [C, 2, 'p-leisure-centre', 3, '17/80', T], [C, 2, 'p-leisure-centre', 3, '0.2125', T], [C, 2, 'p-leisure-centre', 3, '0.213', T], [C, 2, 'p-leisure-centre', 3, '0.212', T], [C, 2, 'p-leisure-centre', 3, '0.21', F],
  [C, 2, 'p-leisure-centre', 4, '0.043', T], [C, 2, 'p-leisure-centre', 4, '136/3160', T], [C, 2, 'p-leisure-centre', 4, '17/395', T], [C, 2, 'p-leisure-centre', 4, '0.0430', T], [C, 2, 'p-leisure-centre', 4, '0.045', F], [C, 2, 'p-leisure-centre', 4, '0.04', F],
  [C, 2, 'p-balloon-blocks', 5, '11/21', T], [C, 2, 'p-balloon-blocks', 5, '660/1260', T], [C, 2, 'p-balloon-blocks', 5, '0.524', T], [C, 2, 'p-balloon-blocks', 5, '0.52', F],
  [C, 2, 'p-balloon-blocks', 1, '1,260', T], [C, 2, 'p-quiz-team', 5, '31/33', T], [C, 2, 'p-quiz-team', 5, '310/330', T], [C, 2, 'p-quiz-team', 5, '0.939', T], [C, 2, 'p-quiz-team', 5, '0.94', F],
  // counting 3: vectors typed as (across, up)
  [C, 3, 'p-orienteering', 1, '(9,12)', T], [C, 3, 'p-orienteering', 1, '(9, 12)', T], [C, 3, 'p-orienteering', 1, '\\left(9,12\\right)', T], [C, 3, 'p-orienteering', 1, PM(9, 12), T],
  [C, 3, 'p-orienteering', 1, '(12,9)', F], [C, 3, 'p-orienteering', 1, '(9,12,0)', F], [C, 3, 'p-orienteering', 1, '9,12', T], [C, 3, 'p-orienteering', 1, '[9,12]', T],
  [C, 3, 'p-orienteering', 1, '(9.0,12.0)', T], [C, 3, 'p-orienteering', 1, '(900,1200)', F], [C, 3, 'p-orienteering', 1, '\\binom{9}{12}', F],
  [C, 3, 'p-orienteering', 2, '(-12,16)', T], [C, 3, 'p-orienteering', 2, '(−12, 16)', T], [C, 3, 'p-orienteering', 2, PM(-12, 16), T], [C, 3, 'p-orienteering', 2, '(16,-12)', F],
  [C, 3, 'p-orienteering', 3, '(-3,28)', T], [C, 3, 'p-orienteering', 3, '(9,12)+(-12,16)', F], [C, 3, 'p-orienteering', 3, '(9-12,12+16)', T],
  [C, 3, 'p-orienteering', 4, '3500', T], [C, 3, 'p-orienteering', 4, '3,500', T], [C, 3, 'p-orienteering', 4, '3500 m', F], [C, 3, 'p-orienteering', 4, '3500m', F], [C, 3, 'p-orienteering', 4, '3.5', F],
  [C, 3, 'p-orienteering', 5, '684', T], [C, 3, 'p-orienteering', 5, '683.97', T], [C, 3, 'p-orienteering', 5, '684 m', F], [C, 3, 'p-orienteering', 5, '680', F], [C, 3, 'p-orienteering', 5, '6.84', F],
  [C, 3, 'p-power-line', 1, '(6,4)', T], [C, 3, 'p-power-line', 1, '(3,2)', F], [C, 3, 'p-power-line', 2, '(15,10)', T], [C, 3, 'p-power-line', 2, '2.5(6,4)', F],
  [C, 3, 'p-power-line', 3, '2.5', T], [C, 3, 'p-power-line', 3, '5/2', T], [C, 3, 'p-power-line', 3, '2 1/2', T], [C, 3, 'p-power-line', 3, 'k=2.5', F],
  [C, 3, 'p-power-line', 5, '1803', T], [C, 3, 'p-power-line', 5, '1802', T], [C, 3, 'p-power-line', 5, '1802.78', T], [C, 3, 'p-power-line', 5, '1,803', T], [C, 3, 'p-power-line', 5, '1800', F], [C, 3, 'p-power-line', 5, '18.03', F],
  [C, 3, 'p-grain-merchant', 1, '10', T], [C, 3, 'p-grain-merchant', 1, '£10', T], [C, 3, 'p-grain-merchant', 2, '(40,70)', T], [C, 3, 'p-grain-merchant', 2, PM(40, 70), T], [C, 3, 'p-grain-merchant', 2, '(60,40)+(-20,30)', F],
  [C, 3, 'p-grain-merchant', 3, '-145', T], [C, 3, 'p-grain-merchant', 3, '−145', T], [C, 3, 'p-grain-merchant', 3, '-£145', T], [C, 3, 'p-grain-merchant', 3, '£-145', T], [C, 3, 'p-grain-merchant', 3, '145', F],
  [C, 3, 'p-grain-merchant', 4, '115', T], [C, 3, 'p-grain-merchant', 4, '114.7', T], [C, 3, 'p-grain-merchant', 4, '115°', F], [C, 3, 'p-grain-merchant', 4, '114', F], [C, 3, 'p-grain-merchant', 4, '116', F],
  // counting 3: expressions in r and s
  [C, 3, 'p-sail-ring', 1, 's-r', T], [C, 3, 'p-sail-ring', 1, '-r+s', T], [C, 3, 'p-sail-ring', 1, 'S-R', T], [C, 3, 'p-sail-ring', 1, '-(r-s)', T],
  [C, 3, 'p-sail-ring', 1, 'r-s', F], [C, 3, 'p-sail-ring', 1, 'RS=s-r', T],
  [C, 3, 'p-sail-ring', 2, '\\frac{1}{2}r+\\frac{1}{2}s', T], [C, 3, 'p-sail-ring', 2, '\\frac{r+s}{2}', T], [C, 3, 'p-sail-ring', 2, '\\frac{1}{2}(r+s)', T], [C, 3, 'p-sail-ring', 2, '0.5(r+s)', T],
  [C, 3, 'p-sail-ring', 2, '\\frac{r}{2}+\\frac{s}{2}', T], [C, 3, 'p-sail-ring', 2, '\\frac{s+r}{2}', T], [C, 3, 'p-sail-ring', 2, 'r+\\frac{1}{2}(s-r)', T], [C, 3, 'p-sail-ring', 2, '\\frac{1}{2}r+\\frac{1}{2}s+0', T],
  [C, 3, 'p-sail-ring', 2, '\\frac{1}{2}rs', F], [C, 3, 'p-sail-ring', 2, 'r+s', F],
  [C, 3, 'p-sail-ring', 3, '\\frac{1}{3}r+\\frac{1}{3}s', T], [C, 3, 'p-sail-ring', 3, '\\frac{r+s}{3}', T], [C, 3, 'p-sail-ring', 3, '\\frac{1}{3}(r+s)', T],
  [C, 3, 'p-sail-ring', 3, '\\frac{2}{3}(\\frac{1}{2}r+\\frac{1}{2}s)', F, RETYPE], [C, 3, 'p-sail-ring', 3, '\\frac{2}{3}\\times\\frac{1}{2}(r+s)', T],
  [C, 3, 'p-sail-ring', 3, '0.33r+0.33s', F], [C, 3, 'p-sail-ring', 3, '0.333r+0.333s', F],
  [C, 3, 'p-sail-ring', 4, '-\\frac{2}{3}r+\\frac{1}{3}s', T], [C, 3, 'p-sail-ring', 4, '\\frac{1}{3}s-\\frac{2}{3}r', T], [C, 3, 'p-sail-ring', 4, '\\frac{s-2r}{3}', T], [C, 3, 'p-sail-ring', 4, '\\frac{1}{3}(s-2r)', T],
  [C, 3, 'p-sail-ring', 4, '-r+\\frac{1}{3}r+\\frac{1}{3}s', F, 'the route before the r terms are collected grades correct on a "simplest form" part'], [C, 3, 'p-sail-ring', 4, '\\frac{1}{3}r+\\frac{1}{3}s-r', T], [C, 3, 'p-sail-ring', 4, '-\\frac{2r}{3}+\\frac{s}{3}', T],
  [C, 3, 'p-sail-ring', 4, '\\frac{2}{3}r+\\frac{1}{3}s', F],
  [C, 3, 'p-sail-ring', 5, '2/3', T], [C, 3, 'p-sail-ring', 5, '0.667', T], [C, 3, 'p-sail-ring', 5, '0.6667', T], [C, 3, 'p-sail-ring', 5, '0.67', F], [C, 3, 'p-sail-ring', 5, '0.666', F],
  // functions 4
  [FN, 4, 'p-photo-mount', 1, '22', T], [FN, 4, 'p-photo-mount', 1, '22 cm', F], [FN, 4, 'p-photo-mount', 1, '22cm', F], [FN, 4, 'p-photo-mount', 1, '22.0', T],
  [FN, 4, 'p-photo-mount', 2, '1.5x+4', T], [FN, 4, 'p-photo-mount', 2, '4+1.5x', T], [FN, 4, 'p-photo-mount', 2, '\\frac{3x+8}{2}', T], [FN, 4, 'p-photo-mount', 2, 'm(e(x))=1.5x+4', F],
  [FN, 4, 'p-photo-mount', 2, '1.5\\times x+4', T], [FN, 4, 'p-photo-mount', 2, 'x+4', F], [FN, 4, 'p-photo-mount', 2, '1.5x+6', F], [FN, 4, 'p-photo-mount', 2, 'y=1.5x+4', T],
  [FN, 4, 'p-photo-mount', 3, '\\frac{x-4}{1.5}', T], [FN, 4, 'p-photo-mount', 3, '(x-4)/1.5', T], [FN, 4, 'p-photo-mount', 3, '\\frac{2}{3}(x-4)', T], [FN, 4, 'p-photo-mount', 3, '\\frac{x-4}{\\frac{3}{2}}', T],
  [FN, 4, 'p-photo-mount', 3, '(x-4)\\div1.5', T], [FN, 4, 'p-photo-mount', 3, 'f^{-1}(x)=\\frac{x-4}{1.5}', F], [FN, 4, 'p-photo-mount', 3, '\\frac{2x}{3}-\\frac{8}{3}', T],
  [FN, 4, 'p-photo-mount', 3, '0.67x-2.67', F], [FN, 4, 'p-photo-mount', 3, '1.5x+4', F], [FN, 4, 'p-photo-mount', 3, '\\frac{y-4}{1.5}', F],
  [FN, 4, 'p-photo-mount', 4, '18', T], [FN, 4, 'p-photo-mount', 4, '18 cm', F], [FN, 4, 'p-photo-mount', 5, '33', T], [FN, 4, 'p-photo-mount', 5, '33 cm', F],
  [FN, 4, 'p-fountain-jet', 1, '5.4', T], [FN, 4, 'p-fountain-jet', 1, '5.40', T], [FN, 4, 'p-fountain-jet', 1, '5.4 m', F], [FN, 4, 'p-fountain-jet', 1, '27/5', T], [FN, 4, 'p-fountain-jet', 1, '5', F],
  [FN, 4, 'p-fountain-jet', 3, '7.5', T], [FN, 4, 'p-fountain-jet', 3, '15/2', T], [FN, 4, 'p-fountain-jet', 3, '7.5 m', F],
  [FN, 4, 'p-fountain-jet', 4, '3.75, 11.25', T], [FN, 4, 'p-fountain-jet', 4, '11.25, 3.75', T], [FN, 4, 'p-fountain-jet', 4, '3.75 and 11.25', T], [FN, 4, 'p-fountain-jet', 4, '3.75 m, 11.25 m', F],
  [FN, 4, 'p-fountain-jet', 4, 'x = 3.75, x = 11.25', T], [FN, 4, 'p-fountain-jet', 4, '15/4, 45/4', T], [FN, 4, 'p-fountain-jet', 4, '3.75', F], [FN, 4, 'p-fountain-jet', 4, '3.8, 11.3', F],
  [FN, 4, 'p-car-park', 1, '9.25', T], [FN, 4, 'p-car-park', 1, '£9.25', T], [FN, 4, 'p-car-park', 1, '9.3', F], [FN, 4, 'p-car-park', 1, '925', F],
  [FN, 4, 'p-car-park', 2, '2.5t-2', T], [FN, 4, 'p-car-park', 2, '-2+2.5t', T], [FN, 4, 'p-car-park', 2, 'C(t)=2.5t-2', T], [FN, 4, 'p-car-park', 2, '\\frac{5t-4}{2}', F], [FN, 4, 'p-car-park', 2, '2.50t-2', T],
  [FN, 4, 'p-car-park', 2, '3+2.5(t-2)', F, RETYPE], [FN, 4, 'p-car-park', 2, '3+2.5t-5', F, 'a line of the working, not yet collected, grades correct on an "as simply as possible" part'],
  [FN, 4, 'p-car-park', 2, '2.5(t-2)+3', F, RETYPE],
  [FN, 4, 'p-car-park', 3, '5.9', T], [FN, 4, 'p-car-park', 3, '5.90', T], [FN, 4, 'p-car-park', 3, '59/10', T], [FN, 4, 'p-car-park', 3, '5.9 hours', F], [FN, 4, 'p-car-park', 3, '5.54', F],
  [FN, 4, 'p-car-park', 5, '10.25', T], [FN, 4, 'p-car-park', 5, '£10.25', T], [FN, 4, 'p-car-park', 5, '10.3', F],
  [FN, 4, 'p-ticket-bonus', 1, '20', T], [FN, 4, 'p-ticket-bonus', 1, '20 tickets', F],
  [FN, 4, 'p-ticket-bonus', 2, '5n-100', T], [FN, 4, 'p-ticket-bonus', 2, '5(n-20)', T], [FN, 4, 'p-ticket-bonus', 2, 'B(T(n))=5n-100', F], [FN, 4, 'p-ticket-bonus', 2, '-100+5n', T],
  [FN, 4, 'p-ticket-bonus', 2, '0.2(25n-500)', F, 'the composite before it is simplified grades correct on an "as simply as possible" part'],
  [FN, 4, 'p-ticket-bonus', 2, '\\max(0.2(25n-500),0)', F], [FN, 4, 'p-ticket-bonus', 2, '5n-500', F],
  [FN, 4, 'p-ticket-bonus', 3, '\\frac{b+100}{5}', T], [FN, 4, 'p-ticket-bonus', 3, '(b+100)/5', T], [FN, 4, 'p-ticket-bonus', 3, 'n=\\frac{b+100}{5}', T], [FN, 4, 'p-ticket-bonus', 3, '0.2(b+100)', T],
  [FN, 4, 'p-ticket-bonus', 3, '\\frac{b}{5}+20', T], [FN, 4, 'p-ticket-bonus', 3, '0.2b+20', T], [FN, 4, 'p-ticket-bonus', 3, '(b+100)\\div5', T], [FN, 4, 'p-ticket-bonus', 3, '5n-100', F], [FN, 4, 'p-ticket-bonus', 3, '\\frac{B+100}{5}', T],
  [FN, 4, 'p-ticket-bonus', 4, '28', T], [FN, 4, 'p-ticket-bonus', 4, '28 tickets', F], [FN, 4, 'p-ticket-bonus', 4, '32', F],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (ok) return; if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };

const isSet = (w) => G.isSetSpec(w) && w.unordered === true;
const gradeNumeric = (w, text) => {
  if (isSet(w)) { const r = G.numSetGrade(w, text); return { ok: !!r.ok, key: r.key }; }
  const v = G.parseNum(text);
  if (!Number.isFinite(v)) return { ok: false, key: 'NOPARSE' };
  if (G.within(v, w.answer, w.tol)) return { ok: true, key: null };
  const m = G.matchWrong(v, w.wrong, w.tol); return { ok: false, key: m ? m.id : null };
};
const size = (j) => (Array.isArray(j) ? 1 + j.slice(1).reduce((a, x) => a + size(x), 0) : 1);
const formOk = (w, L) => {
  if (!w.form) return true;
  if (w.form !== 'simplified') throw new Error('form not modelled: ' + w.form);
  try { return G.withParsed(ce, L, w.functions || [], (e) => { try { return size(e.json) <= size(e.simplify().json); } catch { return true; } }); } catch { return true; }
};
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo) || (!!G.normExpr(L) && G.normExpr(L) === G.normExpr(t)); } catch { return false; } };
  const same = [w.answer, ...(w.accept || [])].some(eq);
  if (same) return formOk(w, L) ? { ok: true, key: null } : { ok: false, key: 'form' };
  const x = (w.wrong || []).find(x => x.tex && eq(x.tex));
  if (x) return { ok: false, key: x.id };
  let sl = null; try { sl = G.exprShapeLine(ce, w.answer, L, fo.functions); } catch { sl = null; }
  return { ok: false, key: sl ? 'length' : null };
};

for (const [course, n] of SETS) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  const seen = new Set();
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${course} ${n} ${it.id} part ${i + 1}`, by = (p.feedback && p.feedback.byKey) || {};
    const typed = TYPED.filter((r) => r[0] === course && r[1] === n && r[2] === it.id && r[3] === i + 1);
    typed.forEach(r => seen.add(r));
    const row = (r, res) => {
      if (probe) { console.log(`${res.ok === r[5] ? '  ' : '!!'} ${where}: "${r[4]}" -> ${res.ok ? 'correct' : 'wrong'} (key ${res.key}), expected ${r[5]}`); return; }
      say(res.ok === r[5], r[6], `${where}: typed "${r[4]}" ${r[5] ? 'refused' : 'accepted'} (key ${res.key})`);
    };
    const wrongs = (grade) => {
      for (const x of w.wrong || []) {
        const r = grade(x);
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value ?? x.tex} grades ${r.ok ? 'correct' : 'to key ' + r.key}`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has no byKey line`);
      }
    };
    if (w.kind === 'numeric' && isSet(w)) {
      say(gradeNumeric(w, w.answers.join(', ')).ok, null, `${where}: set answer does not grade correct`);
      say(gradeNumeric(w, w.answers.slice().reverse().join(', ')).ok, null, `${where}: set answer reversed does not grade correct`);
      wrongs((x) => gradeNumeric(w, String(x.value)));
      say(!!by.count, null, `${where}: no "count" line`);
      for (const r of typed) row(r, gradeNumeric(w, r[4]));
    } else if (w.kind === 'numeric') {
      say(G.within(w.answer, w.answer, w.tol), null, `${where}: answer outside its own band`);
      wrongs((x) => gradeNumeric(w, String(x.value)));
      for (const x of w.wrong || []) { const t = (x.tol && x.tol.abs) || 0; if (t > 0 && Math.abs(x.value) > 0 && t > 0.2 * Math.abs(x.value)) console.log(`NOTE    ${where}: wrong "${x.id}" = ${x.value} has band ±${t}, wider than 20% of the value`); }
      for (const r of typed) row(r, gradeNumeric(w, r[4]));
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer).ok, null, `${where}: answer does not grade correct (${JSON.stringify(gradeExpr(w, w.answer))})`);
      for (const a of w.accept || []) say(gradeExpr(w, a).ok, null, `${where}: accept "${a}" does not grade correct (${JSON.stringify(gradeExpr(w, a))})`);
      wrongs((x) => gradeExpr(w, x.tex));
      if (w.form) say(!!by.form, null, `${where}: form "${w.form}" with no "form" line`);
      for (const r of typed) row(r, gradeExpr(w, r[4]));
    }
  });
  for (const r of TYPED) if (r[0] === course && r[1] === n && !seen.has(r)) { fails++; console.log('FAIL    no such part for row ' + JSON.stringify(r.slice(0, 5))); }
}
console.log(`grade-check: ${checks} checks, ${fails} failures, ${findings} findings (rows the reader holds to be faults)`);
process.exit(fails ? 1 : 0);
