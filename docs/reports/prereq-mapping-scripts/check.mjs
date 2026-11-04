// Usage (from repo root): node docs/reports/prereq-mapping-scripts/check.mjs [course/Ln]
// 1. parsed JSON differs from HEAD only in levels[].requires and top-level lessonRequires;
// 2. rule checks: stage order, same-stage later topic, strand (pure never gates non-pure), self/cycle, unwritten refs;
// 3. longest chain and, for the argument (default research-int/L3), the exact set of levels to finish.
import fs from 'fs'; import path from 'path'; import { execSync } from 'child_process';
import { loadCourses, stageOf, topicKey } from './lib.mjs';
const courses = loadCourses();
// 1 ---------------------------------------------------------------
let diffOk = true;
for (const c of Object.keys(courses)) {
  const head = JSON.parse(execSync(`git show HEAD:app/content/courses/${c}/course.json`, { encoding: 'utf8' }));
  const now = JSON.parse(JSON.stringify(courses[c]));
  delete now.lessonRequires; for (const lv of now.levels) delete lv.requires;
  if (JSON.stringify(head) !== JSON.stringify(now)) { diffOk = false; console.log('DIFF beyond requires:', c); }
  const hk = Object.keys(head).join(), nk = Object.keys(courses[c]).filter(k => k !== 'lessonRequires').join();
  if (hk !== nk) { diffOk = false; console.log('KEY ORDER changed:', c); }
}
console.log('parsed JSON differs from HEAD only in requires/lessonRequires:', diffOk);
// 2 ---------------------------------------------------------------
const written = {};
for (const c of Object.keys(courses)) {
  const dir = `app/content/courses/${c}`; const files = new Set(fs.readdirSync(dir).map(f => f.replace('.json', '')));
  written[c] = {}; for (const lv of courses[c].levels) written[c][lv.n] = lv.lessons.filter(l => files.has(l)).length;
}
const key = (c, n) => `${c}/L${n}`;
const deps = {}; const pureCourses = new Set(Object.keys(courses).filter(c => courses[c].strand === 'pure'));
let problems = 0, warns = 0; const unwritten = [];
for (const c of Object.keys(courses)) for (const lv of courses[c].levels) {
  const refs = lv.requires ?? (lv.n === 1 ? [] : [key(c, lv.n - 1)]);
  deps[key(c, lv.n)] = refs;
  for (const r of refs) {
    const m = r.match(/^([a-z-]+)\/L(\d+)$/); if (!m || !courses[m[1]] || !courses[m[1]].levels.find(l => l.n == m[2])) { console.log('BAD REF', key(c, lv.n), r); problems++; continue; }
    const rc = courses[m[1]];
    if (stageOf(rc.topic) > stageOf(courses[c].topic)) { console.log('LATER STAGE', key(c, lv.n), r); problems++; }
    else if (stageOf(rc.topic) === stageOf(courses[c].topic) && topicKey(rc.topic) > topicKey(courses[c].topic)) { console.log('later topic same stage', key(c, lv.n), r); warns++; }
    if (pureCourses.has(m[1]) && !pureCourses.has(c)) { console.log('PURE GATES NON-PURE', key(c, lv.n), r); problems++; }
    if (written[m[1]][m[2]] === 0) unwritten.push(`${key(c, lv.n)} -> ${r}`);
  }
}
console.log('rule problems:', problems, '| later-topic warnings:', warns);
console.log('references to levels with no written lesson (this worktree):', unwritten.length); unwritten.forEach(u => console.log('  ', u));
// 3 ---------------------------------------------------------------
const memo = {}, state = {};
function depth(k) {
  if (memo[k] != null) return memo[k];
  if (state[k] === 1) { console.log('CYCLE at', k); return 0; } state[k] = 1;
  let best = 1; for (const d of deps[k]) best = Math.max(best, 1 + depth(d)); state[k] = 2; return memo[k] = best;
}
let longest = ''; let ld = 0; for (const k of Object.keys(deps)) { const d = depth(k); if (d > ld) { ld = d; longest = k; } }
console.log(`longest chain: ${ld} levels, ending at ${longest}`);
const path_ = [longest]; { let k = longest; while (deps[k].length) { k = deps[k].reduce((a, b) => depth(a) >= depth(b) ? a : b); path_.push(k); } }
console.log('  ' + path_.reverse().join(' -> '));
function closure(k, seen = new Set()) { for (const d of deps[k]) if (!seen.has(d)) { seen.add(d); closure(d, seen); } return seen; }
const target = process.argv[2] || 'research-int/L3';
const cl = [...closure(target)].sort((a, b) => {
  const [ca, na] = a.split('/L'), [cb, nb] = b.split('/L');
  return topicKey(courses[ca].topic) - topicKey(courses[cb].topic) || ca.localeCompare(cb) || na - nb;
});
console.log(`${target}: direct = ${JSON.stringify(deps[target])}; whole closure = ${cl.length} levels`);
const by = {}; for (const k of cl) { const c = k.split('/L')[0]; (by[`${stageOf(courses[c].topic)} ${courses[c].topic}`] ||= []).push(k); }
for (const [t, ks] of Object.entries(by)) console.log(`  ${t}: ${ks.join(', ')}`);
// averages for the report
const counts = Object.values(deps).map(a => a.length);
console.log('levels:', Object.keys(deps).length, '| explicit requires:', Object.values(courses).reduce((s, c) => s + c.levels.filter(l => l.requires).length, 0), '| max direct refs:', Math.max(...counts));
