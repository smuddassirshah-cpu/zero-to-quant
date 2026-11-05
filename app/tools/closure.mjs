#!/usr/bin/env node
/* Prerequisite closure report (ENGINE-BACKLOG 551; docs/AUTHORING.md, requires section). Read-only.
     node tools/closure.mjs --role trader|researcher|developer|strats|derivatives
     node tools/closure.mjs --target <course>/L<n> | <mock id>
     options: --json, --edges (cross-course edges inside the closure, with their why), --proposal-template <file>
   The closure is the set of levels reached by following gating requires (gate: false entries are left out) from the target, using the
   same edge set as the validator: a level's own requires or, when it has none, the previous level of its course, plus the lessonRequires
   of its lessons. A target <course>/L<n> counts what it requires, not itself (research-int/L1 gives 61, as the review). A mock id starts from the references in the mock's top-level requires.
   A role is the union of the closures of the mocks listed as present for it in content/readiness.json (derivatives = strats-deriv).
   Figures for trader: --target mock-superday-trader gives 107 levels, 35 courses, 470 mapped lessons (the review's F02 figure).
   --proposal-template writes every cross-course edge in course.json, whole content, as
   { "from": "<course>/L<n>", "ref": "...", "why": "<existing why or empty>", "action": "keep" } (plus "lesson" for a lessonRequires edge)
   for a content agent to fill; action is keep, cut or diagnostic. Courses: node 'unwritten' means a level of it with no written lesson. */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const { entriesOf } = createRequire(import.meta.url)('../js/prereq.js');   // the one requires normaliser
const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CONTENT = path.join(APP, 'content');
const read = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const argv = process.argv.slice(2);
const arg = (n) => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : null; };
const has = (n) => argv.includes(n);

const courses = {};
for (const id of fs.readdirSync(path.join(CONTENT, 'courses')).sort()) {
  const f = path.join(CONTENT, 'courses', id, 'course.json');
  if (fs.existsSync(f)) courses[id] = read(f);
}
const levelsOf = (c) => (courses[c] && courses[c].levels) || [];
const writtenIds = (c, lv) => (lv.lessons || []).filter(l => fs.existsSync(path.join(CONTENT, 'courses', c, l + '.json')));
const find = (ref) => {
  const m = /^([^/]+)\/(.+)$/.exec(ref);
  if (!m || !courses[m[1]]) return null;
  const lv = /^L\d+$/.test(m[2]) ? levelsOf(m[1]).find(x => x.n === +m[2].slice(1)) : levelsOf(m[1]).find(x => (x.lessons || []).includes(m[2]));
  return lv ? { c: m[1], lv } : null;
};
const key = (c, lv) => `${c}/L${lv.n}`;
/* every edge out of a level: { ref (entry), why, gate, lesson } */
const edgesOf = (c, lv) => {
  const ls = levelsOf(c), i = ls.indexOf(lv), out = [];
  if (Array.isArray(lv.requires)) entriesOf(lv.requires).forEach(e => out.push({ ...e }));
  else if (i > 0) out.push({ ref: key(c, ls[i - 1]), why: '', gate: true });
  const lr = courses[c].lessonRequires || {};
  (lv.lessons || []).forEach(l => { if (Array.isArray(lr[l])) entriesOf(lr[l]).forEach(e => out.push({ ...e, lesson: l })); });
  return out;
};

const walk = (starts, includeStarts) => {
  const seen = new Map(), cross = [], queue = [];
  const add = (hit, from) => { const k = key(hit.c, hit.lv); if (!seen.has(k)) { seen.set(k, hit); queue.push(hit); } };
  starts.forEach(r => { const h = find(r); if (h) add(h); });
  while (queue.length) {
    const cur = queue.shift();
    for (const e of edgesOf(cur.c, cur.lv)) {
      if (!e.gate) continue;
      const h = find(e.ref);
      if (!h) continue;
      if (h.c !== cur.c) cross.push({ from: key(cur.c, cur.lv), ref: e.ref, why: e.why, lesson: e.lesson });
      add(h);
    }
  }
  return { seen, cross };
};

/* ---------- Proposal template: every cross-course edge in the content ---------- */
const tpl = arg('--proposal-template');
if (tpl) {
  const rows = [];
  for (const c of Object.keys(courses)) for (const lv of levelsOf(c)) for (const e of edgesOf(c, lv)) {
    const h = find(e.ref);
    if (h && h.c !== c) rows.push({ from: key(c, lv), ...(e.lesson ? { lesson: e.lesson } : {}), ref: e.ref, why: e.why || '', action: e.gate ? 'keep' : 'diagnostic' });
  }
  fs.writeFileSync(path.resolve(tpl), JSON.stringify(rows, null, 2) + '\n');
  console.log(`wrote ${rows.length} cross-course edges to ${tpl}`);
  process.exit(0);
}

/* ---------- Target ---------- */
const role = arg('--role'), target = arg('--target');
if (!role && !target) { console.error('usage: closure.mjs --role trader|researcher|developer|strats|derivatives | --target <course>/L<n>|<mock id> [--json] [--edges] | --proposal-template <file>'); process.exit(2); }
const mockRefs = (id) => { const f = path.join(CONTENT, 'exams', id + '.json'); if (!fs.existsSync(f)) return null; return entriesOf(read(f).requires).filter(e => e.gate).map(e => e.ref); };
let label, starts;
if (role) {
  const rk = role === 'derivatives' ? 'strats-deriv' : role, R = read(path.join(CONTENT, 'readiness.json')).roles[rk];
  if (!R) { console.error(`unknown role ${role}`); process.exit(2); }
  const ms = (R.mocks && R.mocks.present) || [];
  starts = [...new Set(ms.flatMap(m => mockRefs(m) || []))];
  label = `role ${role} (union of the mocks ${ms.filter(m => (mockRefs(m) || []).length).join(', ') || 'none'})`;
} else if (/^[^/]+\/L\d+$/.test(target)) {
  const h = find(target);
  if (!h) { console.error(`${target} is not a level`); process.exit(2); }
  starts = edgesOf(h.c, h.lv).filter(e => e.gate).map(e => e.ref); label = `level ${target} (what it requires, not itself)`;
}
else { starts = mockRefs(target); if (!starts) { console.error(`${target} is not a mock file`); process.exit(2); } label = `mock ${target}`; }

const { seen, cross } = walk(starts);
const hits = [...seen.values()];
const byCourse = new Map();
hits.forEach(h => (byCourse.get(h.c) || byCourse.set(h.c, []).get(h.c)).push(h.lv));
const mapped = hits.reduce((a, h) => a + (h.lv.lessons || []).length, 0);
const written = hits.reduce((a, h) => a + writtenIds(h.c, h.lv).length, 0);
const unwritten = [...byCourse.keys()].map(c => ({ course: c, name: courses[c].name || c, levels: hits.filter(h => h.c === c && !writtenIds(c, h.lv).length).map(h => h.lv.n).sort((a, b) => a - b) }))
  .filter(u => u.levels.length);
const result = { target: label, levels: hits.length, courses: byCourse.size, mappedLessons: mapped, writtenLessons: written, closureCourses: [...byCourse.keys()].sort(), unwrittenCourses: unwritten };
const edges = [];
const seenEdge = new Set();
cross.forEach(e => { const k = `${e.from}>${e.ref}>${e.lesson || ''}`; if (!seenEdge.has(k)) { seenEdge.add(k); edges.push(e); } });
if (has('--edges')) result.edges = edges;
if (has('--json')) { console.log(JSON.stringify(result, null, 1)); process.exit(0); }
console.log(`Target: ${label}`);
console.log(`Levels ${result.levels}; courses ${result.courses}; mapped lessons ${mapped}; written lessons ${written}`);
console.log(`Courses in the closure: ${result.closureCourses.join(', ')}`);
console.log(`Unwritten courses reached: ${unwritten.length ? unwritten.map(u => `${u.course} (levels ${u.levels.join(', ')})`).join(', ') : 'none'}`);
if (has('--edges')) {
  console.log(`\nCross-course edges in the closure (${edges.length}, ${edges.filter(e => !e.why).length} without why)`);
  edges.forEach(e => console.log(`  ${e.from}${e.lesson ? ` [${e.lesson}]` : ''} -> ${e.ref}${e.why ? `: ${e.why}` : ''}`));
}
