#!/usr/bin/env node
/* Delta read, stat-learning L4 fix pass: what the engine's own numeric grader (app/js/engine/grade.js) does with
   the changed numeric widgets. For each: the answer grades correct, each wrong[] entry (old and new) grades to
   its own id and has a byKey line, the old stored values no longer fire, and a list of typed strings a learner
   might enter lands where the reader expects. Rows with a note print as FINDING (reported, not failures).

   node docs/reviews/delta-stat-learning-4-scripts/grade.mjs        (from the repo root) */
import fs from 'node:fs';
import vm from 'node:vm';

const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = {}; vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const C = 'app/content/courses/stat-learning/';
const load = (f) => JSON.parse(fs.readFileSync(C + f, 'utf8'));
const isSet = (w) => G.isSetSpec(w) && w.unordered === true;
const grade = (w, text) => {
  if (isSet(w)) { const r = G.numSetGrade(w, text); return r.ok ? true : (r.key || null); }
  const v = G.parseNum(text);
  if (!Number.isFinite(v)) return 'NOPARSE';
  if (G.within(v, +w.answer, w.tol)) return true;
  const m = G.matchWrong(v, w.wrong, { abs: 1e-9 });
  return m ? m.id : null;
};
let checks = 0, fails = 0, findings = 0;
const say = (ok, msg, note) => { checks++; if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); return; } if (!ok) fails++; console.log((ok ? 'ok   ' : 'FAIL ') + msg); };

const l16 = load('l16-groups-nobody-labelled.json'), l17 = load('l17-a-small-network.json'), l18 = load('l18-bending-the-line.json'), hw = load('homework-4.json');
const pick = hw.items.find((i) => i.id === 'h-pick-learner');
// [label, screen or item, typed, expected (true, null for the generic line, or a wrong id), note?]
const ROWS = [
  ['l16 s1', l16.screens[1], '12, 34', true], ['l16 s1', l16.screens[1], '34, 12', true],
  ['l16 s1', l16.screens[1], '11, 29.8', 'half'], ['l16 s1', l16.screens[1], '29.8, 11', 'half'],
  ['l16 s1 old value', l16.screens[1], '11, 29', null], ['l16 s1', l16.screens[1], '10, 25.6', 'stay'],
  ['l16 s2', l16.screens[2], '64', true], ['l16 s2', l16.screens[2], '16', 'unsq'], ['l16 s2 old value', l16.screens[2], '12', null],
  ['l16 s2', l16.screens[2], '8', 'onegroup'], ['l16 s2', l16.screens[2], '10.67', 'var'],
  ['l17 q2', l17.quiz[1], '5', true], ['l17 q2', l17.quiz[1], '-1', 'order'], ['l17 q2', l17.quiz[1], '6', 'dropped'], ['l17 q2', l17.quiz[1], '3', 'first'],
  ['l17 q2 first entry of the wrong order', l17.quiz[1], '1', null],
  ['l18 s3', l18.screens[3], '7', true], ['l18 s3', l18.screens[3], '3', 'interior'], ['l18 s3', l18.screens[3], '5', 'knots'], ['l18 s3', l18.screens[3], '9', 'nine'], ['l18 s3', l18.screens[3], '6', 'noconst'],
  ['l18 s3 both asked values typed', l18.screens[3], '3, 7', 'ANY', 'the question asks two things; see what a learner who types both gets'],
  ['h-pick-learner', pick, '1.21', true], ['h-pick-learner', pick, '1.209', true], ['h-pick-learner', pick, '1.2087', true],
  ['h-pick-learner', pick, '2.42', 'besttest'], ['h-pick-learner', pick, '1.61', 'tie'], ['h-pick-learner', pick, '3.6', 'coin'], ['h-pick-learner', pick, '3.60', 'coin'], ['h-pick-learner', pick, '2.01', 'valscore'],
  ['h-pick-learner, standard error rounded to 0.025', pick, '1.20', null, 'refused with the generic line'],
  ['h-pick-learner, standard error rounded to 0.025', pick, '1.2', null, 'refused with the generic line'],
  ["h-pick-learner, standard error from the learner's own 0.59", pick, '1.22', null, 'refused with the generic line'],
  ['h-pick-learner, validation score on its own 200 rows', pick, '1.42', null],
];
for (const [label, item, typed, want, note] of ROWS) {
  const got = grade(item.widget, typed);
  if (want === 'ANY') { say(true, `${label}: "${typed}" -> ${got === true ? 'correct' : got === null ? 'generic line' : got}`, note); continue; }
  say(got === want, `${label}: "${typed}" -> ${got === true ? 'correct' : got === null ? 'generic line' : got}` + (got === want ? '' : ` (expected ${want})`), got === want ? note : undefined);
}
for (const [label, item] of [['l16 s1', l16.screens[1]], ['l16 s2', l16.screens[2]], ['l17 q2', l17.quiz[1]], ['l18 s3', l18.screens[3]], ['h-pick-learner', pick]]) {
  for (const w of item.widget.wrong || []) {
    say(grade(item.widget, String(w.value)) === w.id, `${label}: wrong '${w.id}' (${w.value}) grades to its own id`);
    say(typeof (item.feedback.byKey || {})[w.id] === 'string', `${label}: wrong '${w.id}' has a byKey line`);
  }
}
console.log(`${checks} checks, ${fails} failures, ${findings} FINDING rows`);
process.exit(fails ? 1 : 0);
