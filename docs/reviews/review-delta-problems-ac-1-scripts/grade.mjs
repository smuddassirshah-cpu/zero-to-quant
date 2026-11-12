#!/usr/bin/env node
/* Delta read AC-1: what the engine's own graders (app/js/engine/grade.js: numGrade for numeric parts, exprGrade with
   the local Compute Engine for expression parts) do with every changed part of the three fix passes.
     - the stored answer and each accept[] form grade correct; each wrong[] entry typed at its stored value is refused,
       lands on its own id and has a byKey line (FAIL if not). A wrong matrix typed whole is the known engine fault
       and is counted, not failed.
     - TYPED rows [typed, expected, note?]: expected is true (accepted), a wrong id, null (generic refusal) or
       "NOPARSE". A row with a note is one the review records: when it misbehaves it prints FINDING and does not fail.
   node docs/reviews/review-delta-problems-ac-1-scripts/grade.mjs --local-cdn <pkgs> [--show]     (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const SHOW = argv.includes('--show');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return r.ok ? true : (r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null)); };
const expr = (w, t) => { let r; try { r = G.exprGrade(ce, w, t, t); } catch (e) { return 'THROW ' + e.message; } return r.ok ? true : (r.key || null); };

const EL = 'elimination', LS = 'least-squares', EG = 'eigen', TS = 'testing';
// [course, item, part (1-based), rows]
const TYPED = [
  // ---- fix pass 1.4 b
  [EL, 'p-courier-rounds', 1, [['[[0,1,0],[1,0,0],[0,0,1]]', true]]],
  [EL, 'p-courier-rounds', 2, [['[[1,0,0],[0,1,0],[0,2,1]]', true]]],
  [EL, 'p-courier-rounds', 3, [['(15,18,9)', true], ['(15, 18, 9)', true], ['(18,15,15)', 'unswapped'], ['(15,18,81)', 'signs'], ['(14,15,9)', null], ['(18,15,9)', null], ['(15,18,45)', null]]],
  [EL, 'p-courier-rounds', 4, [['(2,4,3)', true], ['(6,0,9)', 'no-divide'], ['(3,4,2)', 'reversed'], ['(-10,6,9)', null]]],
  [EL, 'p-courier-rounds', 5, [['30', true], ['30 minutes', true], ['31', 'reversed'], ['29', null]]],
  [EL, 'p-tilted-gantry', 1, [['-4', true], ['4', 'sign'], ['0', 'zero']]],
  [EL, 'p-tilted-gantry', 2, [['(-2,2)', true], ['(2,-2)', 'sign']]],
  [EL, 'p-tilted-gantry', 3, [['8', true], ['12', 'half-step'], ['-4', 'sign'], ['4', null], ['6', null], ['16', null], ['-8', null]]],
  [EL, 'p-tilted-gantry', 4, [['(6,0,1)', true], ['(6, 0, 1)', true], ['(4,2,0)', 'no-motor-3'], ['(2,4,1)', 'sign'], ['(4,-1,1)', null], ['(0,3,1)', null]]],
  [EL, 'p-futures-packages', 1, [['2', true], ['3', 'columns']]],
  [EL, 'p-futures-packages', 2, [['(-1,1,1)', true], ['(1,-1,1)', 'sign']]],
  [EL, 'p-futures-packages', 3, [['-3', true], ['3', 'sign'], ['2', 'stale-rhs'], ['1', null]]],
  [EL, 'p-futures-packages', 4, [['(5,3,0)', true], ['(5,-3,0)', 'sign'], ['(4,3,0)', null]]],
  [EL, 'p-futures-packages', 5, [['(3,5,2)', true], ['(7,1,2)', 'sign'], ['(-2,2,2)', 'nullspace-only'], ['(2,5,2)', null], ['(6,1,2)', null]]],
  [EL, 'p-vinyl-cutter', 1, [['40', true], ['80', 'plus'], ['60', 'diagonal'], ['50', null], ['70', null], ['8', null]]],
  [EL, 'p-vinyl-cutter', 2, [['6', true], ['-6', 'sign'], ['12', 'factor']]],
  [EL, 'p-vinyl-cutter', 3, [['4', true], ['12', 'row']]],
  [EL, 'p-vinyl-cutter', 4, [['(2,-1)', true], ['(2,1)', 'sign'], ['(2,-3)', 'perpendicular']]],
  [LS, 'p-gas-hubs', 1, [['30', true], ['5', 'count'], ['10', 'sum'], ['100', 'sum-squared'], ['15', null], ['25', null]]],
  [LS, 'p-gas-hubs', 2, [['(3,-2)', true], ['(3, -2)', true], ['(-1,-1)', 'diagonal'], ['(-2,3)', 'swapped'], ['(3,2)', 'no-sign'], ['(1,-2)', null]]],
  [LS, 'p-gas-hubs', 3, [['(2,-1.5)', true], ['(2,-3/2)', true], ['(2,-\\frac{3}{2})', true], ['(-1,-5/6)', 'diagonal'], ['(-1,-\\frac{5}{6})', 'diagonal'], ['(2,1.5)', 'no-sign'], ['(0.5,-1.5)', null],
    ['(-1,-0.83)', 'diagonal', 'the `diagonal` slip typed as a decimal, as "Give exact decimals" asks (5/6 has no exact decimal): generic line']]],
  [LS, 'p-gas-hubs', 4, [['(1,-0.5)', true], ['(1,-1/2)', true], ['(1,-.5)', true], ['(5,-3.5)', 'added'], ['(-1,0.5)', 'reversed'], ['(0.5,-0.5)', null]]],
  [LS, 'p-gas-hubs', 5, [['0.333', true], ['0.3333', true], ['1/3', true], ['0.33', null], ['0.334', null], ['0.667', 'ratio'], ['0.6667', 'ratio'], ['0.6', 'added-sse'], ['0.600', 'added-sse'], ['0.964', 'hub-n'], ['0.9639', 'hub-n'], ['0.938', null]]],
  // ---- fix pass 1.4 c
  [EG, 'p-river-gauges', 1, [['2', true], ['2.0', true], ['1', 'multiplier-one'], ['-1', 'multiplier-two'], ['8', null]]],
  [EG, 'p-river-gauges', 2, [['0.375', true], ['.375', true], ['3/8', true], ['0.38', null], ['0.37', null], ['0.25', 'one-step'], ['0.5', 'big-multiplier'], ['0.125', 'added'], ['-0.375', null]]],
  [EG, 'p-river-gauges', 3, [['(-0.125,-0.25,1)', true], ['(-1/8,-1/4,1)', true], ['(-\\frac18,-\\frac14,1)', true], ['(-.125,-.25,1)', true], ['(0.125,0.25,1)', 'sign'], ['(-0.25,-0.125,1)', 'swapped'], ['(-0.25,-0.25,1)', 'no-b'],
    ['(-1,-2,8)', null], ['(1,2,-8)', null], ['(-0.13,-0.25,1)', null]]],
  [EG, 'p-river-gauges', 4, [['0.125', true], ['.125', true], ['1/8', true], ['0.13', null], ['0.5', 'c-only'], ['1.625', 'sign'], ['0.375', 'boundary'], ['0', null], ['0.25', null]]],
  [EG, 'p-river-gauges', 5, [['0.75', true], ['.75', true], ['3/4', true], ['0.25', 'unexplained'], ['0.875', 'not-scaled'], ['0.375', null]]],
  [EG, 'p-tank-thermometers', 5, [['1.89', true], ['1.890', true], ['189/100', true], ['1.9', null], ['1.88', null], ['1.90', null], ['1.78', 'no-eigenvalue'], ['1.778', 'no-eigenvalue'], ['0.22', 'd-only'], ['0.223', 'd-only'], ['0.2233', 'd-only'],
    ['1.335', 'no-cov'], ['1.33', 'no-cov'], ['1.34', 'no-cov'], ['1.76', null], ['1.71', null]]],
  [EG, 'p-crab-sizes', 5, [['1.265', true], ['1.2649', true], ['1.26491', true], ['1.2650', true], ['1.26', null], ['1.27', null], ['1.264', null], ['1.266', null], ['0.08', 'variance'], ['0.080', 'variance'], ['1.131', 'total'], ['1.1314', 'total'], ['2.53', 'pc2-sd'], ['2.530', 'pc2-sd'], ['2.5298', 'pc2-sd'], ['1.13', null]]],
  // ---- fix pass delta AB-1
  [TS, 'p-gene-screen', 1, [['0.001667', true], ['1/600', true], ['0.1', 'unadjusted'], ['6', 'times-m'], ['0.000833', 'five-percent'], ['0.00167', null]]],
  [TS, 'p-gene-screen', 2, [['1', true], ['1 gene', true], ['8', 'unadjusted'], ['6', 'bh'], ['5', null], ['0', null]]],
  [TS, 'p-gene-screen', 3, [['6', true], ['6 genes', true], ['2', 'first-fail'], ['1', 'bonferroni'], ['8', 'unadjusted'], ['4', 'count-passes'], ['5', null], ['3', null], ['7', null]]],
  [TS, 'p-gene-screen', 4, [['0.096', true], ['.096', true], ['0.0960', true], ['q=0.096', true], ['0.0959', null], ['0.0961', null], ['0.095', null], ['0.0948', null], ['0.576', 'no-divide'], ['0.108', 'rank-five'], ['0.1080', 'rank-five'], ['0.01', 'bar'], ['0.0100', 'bar'], ['0.10', null], ['0.11', null], ['0.1065', null], ['0.474', null]]],
];

let checks = 0, fails = 0, findings = 0, known = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (SHOW) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const docs = {};
const find = (course, id) => {
  for (const f of fs.readdirSync('app/content/courses/' + course).filter(x => /^problems-\d+\.json$/.test(x))) {
    const d = docs[course + f] || (docs[course + f] = JSON.parse(fs.readFileSync(`app/content/courses/${course}/${f}`, 'utf8')));
    const it = d.items.find(i => i.id === id);
    if (it) return it;
  }
  throw new Error('no item ' + id);
};
for (const [course, id, part, rows] of TYPED) {
  const p = find(course, id).parts[part - 1], w = p.widget;
  const isExpr = w.kind === 'expression';
  const grade = isExpr ? expr : num;
  const by = (p.feedback && p.feedback.byKey) || {};
  const where = `${course} ${id} ${part}`;
  if (isExpr) {
    for (const a of [w.answer, ...(w.accept || [])]) say(grade(w, a) === true, null, `${where}: answer or accept "${a}" grades correct (got ${grade(w, a)})`);
    for (const x of w.wrong || []) {
      if (/pmatrix/.test(x.tex)) { known++; say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`); continue; }
      say(grade(w, x.tex) === x.id, null, `${where}: wrong ${x.id} "${x.tex}" lands on its id (got ${grade(w, x.tex)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`);
    }
  } else {
    const shown = String(w.answer);
    say(grade(w, shown) === true, null, `${where}: answer ${shown} grades correct (got ${grade(w, shown)})`);
    for (const x of w.wrong || []) {
      const t = String(x.value);
      say(grade(w, t) === x.id, null, `${where}: wrong ${x.id} ${t} lands on its id (got ${grade(w, t)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`);
    }
  }
  for (const [typed, want, note] of rows) {
    const got = grade(w, typed);
    say(got === want, note, `${where}: typed "${typed}" -> ${got === true ? 'accepted' : got === null ? 'refused, generic line' : got === 'NOPARSE' ? 'not read (field will not submit)' : 'refused, line "' + got + '"'}; expected ${want === true ? 'accepted' : want === null ? 'generic refusal' : want}`);
  }
}
console.log(`grade: ${checks} checks, ${fails} failures, ${findings} FINDING rows (recorded in the review); ${known} wrong matrices not typed (known engine fault)`);
process.exit(fails ? 1 : 0);
