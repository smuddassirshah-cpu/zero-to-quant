#!/usr/bin/env node
/* Unit tests for the role readiness status and the oa-drill performance rule (PLAN 2c item 8; ENGINE-BACKLOG 564, 566, 568).
   Plain node, as test-met-rule.mjs: fake window and localStorage, the real js/state.js, content.js and prereq.js, the real content/ files.
   Run from anywhere: node app/tools/test-capstone.mjs. One PASS or FAIL line per test, a summary line, exit code 1 on any failure. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CONTENT = path.join(APP, 'content');
const store = new Map();
globalThis.localStorage = { getItem: (k) => (store.has(k) ? store.get(k) : null), setItem: (k, v) => { store.set(k, String(v)); }, removeItem: (k) => { store.delete(k); }, clear: () => store.clear() };
globalThis.window = globalThis;
globalThis.ZQ = { emit: () => {}, on: () => {} };
globalThis.fetch = async (url) => {
  const f = path.join(APP, String(url));
  if (!fs.existsSync(f)) return { status: 404, ok: false, json: async () => null };
  const text = fs.readFileSync(f, 'utf8');
  return { status: 200, ok: true, json: async () => JSON.parse(text) };
};
for (const f of ['state.js', 'content.js', 'prereq.js']) vm.runInThisContext(fs.readFileSync(path.join(APP, 'js', f), 'utf8'), { filename: f });
const { state: S, content: C, prereq: P } = globalThis.ZQ;
await C.ready;

const readJSON = (rel) => JSON.parse(fs.readFileSync(path.join(CONTENT, rel), 'utf8'));
const results = [];
const test = async (name, fn) => {
  store.clear(); S._reload(); C._setPerf({}); C._setCapstones([]);
  try { await fn(); results.push(true); console.log(`PASS ${name}`); }
  catch (e) { results.push(false); console.log(`FAIL ${name}: ${e && e.message ? e.message : e}`); }
};
const eq = (a, b, m) => { if (a !== b) throw new Error(`${m || 'value'}: expected ${b}, got ${a}`); };
const ok = (c, m) => { if (!c) throw new Error(m || 'assertion failed'); };

const written = (cid, id) => C.exists(cid, id) !== false;
const fullLevel = (cid, lv) => lv.review && written(cid, lv.review) && (lv.lessons || []).length && lv.lessons.every(id => written(cid, id));
const sitReview = (cid, lv) => {
  const D = readJSON(`courses/${cid}/${lv.review}.json`);
  const rows = D.items.map((it, i) => ({ id: it.id || 'q' + i, ok: true, difficulty: it.difficulty || 3, skills: it.skills || [], ref: { course: cid, lesson: lv.review, item: it.id || 'q' + i } }));
  S.reviewFinished({ course: cid, id: lv.review, results: rows, items: rows.length });
};
/* a course whose every level is fully written and has a review: a one-course "required" role */
const oneCourse = C.allCourses().find(c => (c.levels || []).length && c.levels.every(lv => fullLevel(c.id, lv)));
ok(oneCourse, 'expected a course with every level fully written');
const ROLE = 'trader';
C._setReadiness({ roles: { [ROLE]: { courses: { [oneCourse.id]: 'required' }, totals: {}, mocks: {} }, undecided: { courses: {}, totals: {}, mocks: {} } } });
const meetAll = () => { oneCourse.levels.forEach(lv => sitReview(oneCourse.id, lv)); P.sync(); };
const complete = { role: ROLE, project: 'my-book', repo: 'https://github.com/a/b', reviewer: 'Sam', date: '2026-11-05', rerun: 'pass', defence: 'notes', external: true };

await test('capstone (a): every required level met but no external record is not ready', async () => {
  meetAll();
  const s = C.readiness.status(ROLE);
  eq(s.levels.met, s.levels.total, 'all levels met'); ok(s.levels.total > 0, 'has levels');
  ok(!s.ready, 'not ready'); ok(s.missing.includes('Capstone not recorded'), `missing says so (${s.missing})`);
  ok(!/^ready/i.test(C.readiness.verdict(ROLE)), `verdict is not Ready (${C.readiness.verdict(ROLE)})`);
});
await test('capstone (a2): an empty record is "not done" and levels unmet is not ready', async () => {
  C._setCapstones([{ role: ROLE, project: '', repo: '', reviewer: '', date: '', rerun: '', defence: '', external: false }]);
  ok(!C.readiness.status(ROLE).ready, 'empty record, no levels: not ready');
  meetAll();
  ok(!C.readiness.status(ROLE).ready, 'empty record, levels met: still not ready');
  eq(C.readiness.status(ROLE).missing[0], 'Capstone not recorded', 'empty record reads as not recorded');
});
await test('capstone (b): every required level met and a complete external record is ready', async () => {
  meetAll(); C._setCapstones([complete]);
  const s = C.readiness.status(ROLE);
  ok(s.ready && s.capstoneDone && !s.missing.length, 'ready'); eq(C.readiness.verdict(ROLE), 'Ready', 'verdict');
});
await test('capstone (b2): a complete record with levels unmet is not ready', async () => {
  C._setCapstones([complete]);
  const s = C.readiness.status(ROLE);
  ok(!s.ready && s.capstoneDone, 'record done, levels not');
  ok(/required levels not met/.test(s.missing[0]), `says levels (${s.missing})`);
});
await test('capstone (c): an incomplete external record (blank reviewer, or rerun not pass, or external false) is not ready', async () => {
  meetAll();
  for (const bad of [{ reviewer: '' }, { rerun: 'fail' }, { rerun: '' }, { external: false }, { repo: '' }, { date: '  ' }]) {
    C._setCapstones([{ ...complete, ...bad }]);
    ok(!C.readiness.status(ROLE).ready, `not ready with ${JSON.stringify(bad)}`);
  }
  C._setCapstones([{ ...complete, reviewer: '' }]);
  eq(C.readiness.status(ROLE).missing[0], 'Capstone incomplete', 'says incomplete');
});
await test('capstone: undecided and a missing file are never ready', async () => {
  ok(!C.readiness.status('undecided').ready, 'undecided'); ok(C.readiness.verdict('undecided') === '', 'no verdict for undecided');
  eq(C.readiness.capstones().length, 0, 'missing file is an empty list');
});

/* ---------- oa drill and the code performance task ---------- */
const ci = C.course('coding-int');
const oaIds = C.drills().filter(d => d.course === 'coding-int' && String(d.id).startsWith('oa-')).map(d => d.id);
const other = C.drills().find(d => !String(d.id).startsWith('oa-'));
ok(ci && oaIds.length >= 2, 'expected oa drills mapped to coding-int');
const L1 = ci.levels.find(l => l.n === 1);
const taskFor = (kind, n = 1) => C._setPerf({ [`coding-int/L${n}`]: { file: 'courses/coding-int/homework-1.json', item: 'perf-item', kind, how: kind === 'code' ? 'auto' : 'self', gates: true } });

await test('drill (d): a verified oa drill satisfies the mapped coding-int code task, an unverified one does not', async () => {
  taskFor('code'); sitReview('coding-int', L1); P.sync();
  ok(fullLevel('coding-int', L1), 'fixture level written');
  ok(P.perfNeeded('coding-int', L1), 'task needed'); ok(!P.perfPassed('coding-int', L1), 'not passed'); ok(!P.levelMet('coding-int', 1), 'review alone does not meet');
  S.drills.draft(oaIds[0], 'x = 1');   // unverified draft
  ok(!P.perfPassed('coding-int', L1), 'a draft does not count'); ok(!P.levelMet('coding-int', 1), 'unverified: not met');
  S.drills.verified(oaIds[0], 'def f(): pass');
  ok(P.perfPassed('coding-int', L1), 'verified oa drill passes the task'); ok(P.levelMet('coding-int', 1), 'level met');
});
await test('drill (d2): a verified non-oa drill, a non-code task, or another level does not count', async () => {
  taskFor('code'); sitReview('coding-int', L1); P.sync();
  if (other) { S.drills.verified(other.id, 'x'); ok(!P.perfPassed('coding-int', L1), `non-oa drill ${other.id} does not count`); }
  C._setPerf({}); taskFor('derivation');
  S.drills.verified(oaIds[0], 'x'); ok(!P.perfPassed('coding-int', L1), 'a derivation task is not met by a drill');
  C._setPerf({}); taskFor('code', 2);
  const L2 = ci.levels.find(l => l.n === 2);
  if (L2) ok(P.perfPassed('coding-int', L2), 'with no level field an oa drill maps to the lowest level that has a gated code task');
});
await test('drill (d3): an explicit level on the drill row maps it to that level', async () => {
  const L2 = ci.levels.find(l => l.n === 2);
  ok(L2, 'coding-int has level 2');
  taskFor('code', 1); C._setPerf({ ...{ 'coding-int/L1': { kind: 'code', gates: true, item: 'a' }, 'coding-int/L2': { kind: 'code', gates: true, item: 'b' } } });
  const meta = {}; oaIds.forEach((id, i) => { meta[id] = i === 0 ? { level: 2, pack: 'oa' } : { pack: 'oa' }; }); C._setDrillMeta(meta);
  S.drills.verified(oaIds[0], 'x');
  ok(P.perfPassed('coding-int', L2), 'level 2 passes with its mapped drill'); ok(!P.perfPassed('coding-int', L1), 'level 1 does not');
  C._setDrillMeta({});
});

const pass = results.filter(Boolean).length;
console.log(`${pass === results.length ? 'PASS' : 'FAIL'} summary: ${pass} of ${results.length} tests passed`);
process.exit(pass === results.length ? 0 : 1);
