#!/usr/bin/env node
/* Unit tests for the cumulative weekly review (ENGINE-BACKLOG 820 to 829; docs/AUTHORING.md section 16). Plain node, no browser: a fake window
   and localStorage, the real js/state.js, content.js, prereq.js, arith.js, gen.js and select.js, and the real content/ files read through a
   fake fetch, as the app loads them.
     Part A  the selection rules (ZQ.select.cumulative.build) on synthetic models, with and without Fluency families: tiers in order,
             at most four items from one course (the cap relaxes only when too few courses are met), neighbours from different courses,
             families weighted by wrong answers and by age, least recently seen first, determinism, no repeated generated prompt.
     Part B  the schedule in the state (ZQ.state.cumulative): first due seven days after the first met level, then seven days after the last
             review, postponing keeps it due, a left review is not a review.
     Part C  the live model on seeded states of the real content, without and with a Fluency set (the fixture, registered through the test
             hook): what is drawn, what is recorded (history row, per-level misses, redo queue, family counts, seen items).
   Run from anywhere: node app/tools/test-cumulative.mjs. One PASS or FAIL line per test, a summary line, exit 1 on any failure. */
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
for (const f of ['state.js', 'content.js', 'prereq.js', 'engine/arith.js', 'engine/gen.js', 'engine/select.js']) vm.runInThisContext(fs.readFileSync(path.join(APP, 'js', f), 'utf8'), { filename: f });
const { state: S, content: C, select: SEL, gen: GEN } = globalThis.ZQ;
await C.ready;

const DAY = 86400000;
const results = [];
const test = async (name, fn) => {
  store.clear(); S._reload(); S._setClock(null);
  try { await fn(); results.push(true); console.log(`PASS ${name}`); }
  catch (e) { results.push(false); console.log(`FAIL ${name}: ${e && e.message ? e.message : e}`); }
};
const eq = (a, b, m) => { if (a !== b) throw new Error(`${m || 'value'}: expected ${b}, got ${a}`); };
const ok = (c, m) => { if (!c) throw new Error(m || 'assertion failed'); };
const fixture = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/fluency/fluency-l3-opening-brackets.json'), 'utf8'));
const count = (list, f) => list.filter(f).length;
const perCourse = (picks) => { const m = {}; picks.forEach(p => { m[p.course] = (m[p.course] || 0) + 1; }); return m; };

/* ---------- Part A: the selection on synthetic models ---------- */
const NOW = 1_800_000_000_000;
const fakeItem = (uid) => ({ id: uid, uid, question: uid, widget: { kind: 'numeric', answer: 1 }, skills: [], ref: { course: 'x', lesson: 'l1', item: uid } });
const families = (courses, perCourseSets = 2, stats = {}) => courses.flatMap((c, ci) => fixture.families.slice(0, perCourseSets).map((f) => Object.assign({ course: c, n: 1, set: { id: `fluency-${c}`, lesson: 'l1', title: 't', families: [f] }, family: f, right: 0, wrong: 0, lastAt: 0 }, stats[`${c}/${f.id}`] || {})));
const pool = (courses, k, prefix, extra = () => ({})) => courses.flatMap((c) => Array.from({ length: k }, (_, i) => Object.assign({ uid: `${prefix}-${c}-${i}`, course: c, n: 1, item: fakeItem(`${prefix}-${c}-${i}`) }, extra(c, i))));
const COURSES6 = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6'];

await test('A: an empty model gives nothing, and never hangs', () => {
  eq(SEL.cumulative.build({ now: NOW, levels: [], families: [], unseen: [], review: [] }, { seed: 1 }).length, 0);
});
await test('A: with no Fluency sets it is authored items alone, unseen first', () => {
  const m = { now: NOW, levels: [], families: [], unseen: pool(COURSES6, 2, 'u'), review: pool(COURSES6, 8, 'r', (c, i) => ({ lastSeen: i })) };
  const p = SEL.cumulative.build(m, { seed: 3 });
  eq(p.length, 20, 'items');
  eq(count(p, (x) => x.tier === 1), 0, 'no generated item without a set');
  eq(count(p, (x) => x.tier === 2), 12, 'every unseen authored item (12) is taken before any review item');
  eq(count(p, (x) => x.tier === 3), 8, 'review items fill the rest');
  ok(Object.values(perCourse(p)).every((v) => v <= 4), `at most four from one course: ${JSON.stringify(perCourse(p))}`);
});
await test('A: with Fluency families, generated items come first and fill the set when the courses allow it', () => {
  const m = { now: NOW, levels: [], families: families(COURSES6), unseen: pool(COURSES6, 5, 'u'), review: pool(COURSES6, 5, 'r') };
  const p = SEL.cumulative.build(m, { seed: 4 });
  eq(p.length, 20);
  eq(count(p, (x) => x.tier === 1), 20, 'all twenty are generated while six courses have families (6 x 4 = 24 places)');
  ok(Object.values(perCourse(p)).every((v) => v <= 4), `cap: ${JSON.stringify(perCourse(p))}`);
  ok(p.every((x) => x.gen && x.gen.prompt && x.gen.widget), 'each generated entry carries its drawn item');
  eq(new Set(p.map((x) => x.gen.prompt)).size, 20, 'no generated prompt repeats');
});
await test('A: when families run short, authored items fill the set (tier 2 then tier 3)', () => {
  const m = { now: NOW, levels: [], families: families(['c1', 'c2'], 1), unseen: pool(COURSES6, 1, 'u'), review: pool(COURSES6, 6, 'r') };
  const p = SEL.cumulative.build(m, { seed: 5 });
  eq(p.length, 20);
  eq(count(p, (x) => x.tier === 1), 8, 'two courses, four each');
  eq(count(p, (x) => x.tier === 2), 4, 'the unseen items of the four other courses (the two with generated items are full)');
  ok(count(p, (x) => x.tier === 3) === 8, 'the rest from review items');
  ok(Object.values(perCourse(p)).every((v) => v <= 4), `cap: ${JSON.stringify(perCourse(p))}`);
});
await test('A: the cap of four relaxes only when too few courses are met', () => {
  const three = SEL.cumulative.build({ now: NOW, families: [], unseen: [], review: pool(['c1', 'c2', 'c3'], 30, 'r') }, { seed: 6 });
  eq(three.length, 20, 'three courses still make twenty items');
  ok(Object.values(perCourse(three)).every((v) => v <= 8), `relaxed in steps: ${JSON.stringify(perCourse(three))}`);
  const one = SEL.cumulative.build({ now: NOW, families: [], unseen: [], review: pool(['c1'], 30, 'r') }, { seed: 6 });
  eq(one.length, 20, 'one course fills the set when nothing else is met');
  const six = SEL.cumulative.build({ now: NOW, families: [], unseen: [], review: pool(COURSES6, 30, 'r') }, { seed: 6 });
  ok(Object.values(perCourse(six)).every((v) => v <= 4), `six courses never need to relax: ${JSON.stringify(perCourse(six))}`);
  const short = SEL.cumulative.build({ now: NOW, families: [], unseen: [], review: pool(['c1', 'c2'], 3, 'r') }, { seed: 6 });
  eq(short.length, 6, 'fewer items than twenty in the pool gives all of them, no padding');
});
await test('A: neighbours come from different courses when that is possible', () => {
  const m = { now: NOW, families: families(COURSES6), unseen: [], review: [] };
  for (let seed = 0; seed < 20; seed++) {
    const p = SEL.cumulative.build(m, { seed });
    p.forEach((x, i) => { if (i) ok(x.course !== p[i - 1].course, `seed ${seed}: items ${i} and ${i + 1} are both from ${x.course}`); });
  }
});
await test('A: families with more wrong answers are drawn more often', () => {
  const m = { now: NOW, families: [], unseen: [], review: [] };
  const base = families(['c1', 'c2'], 1).map((f) => Object.assign(f, { lastAt: NOW - 3 * DAY, right: 10, wrong: 0 }));
  base[0].right = 2; base[0].wrong = 18;   // c1's family is the one the learner gets wrong
  let a = 0, b = 0;
  for (let seed = 0; seed < 200; seed++) { SEL.cumulative.build({ ...m, families: base.map((f) => ({ ...f })) }, { seed, n: 3 }).forEach((x) => { if (x.course === 'c1') a++; else b++; }); }
  ok(a > b * 1.4, `the weak family should be drawn clearly more often (${a} against ${b})`);
});
await test('A: families practised longer ago are drawn more often', () => {
  const base = families(['c1', 'c2'], 1).map((f) => Object.assign(f, { right: 5, wrong: 5, lastAt: NOW - 1 * DAY }));
  base[1].lastAt = NOW - 60 * DAY;
  let a = 0, b = 0;
  for (let seed = 0; seed < 200; seed++) SEL.cumulative.build({ now: NOW, families: base.map((f) => ({ ...f })), unseen: [], review: [] }, { seed, n: 3 }).forEach((x) => { if (x.course === 'c1') a++; else b++; });
  ok(b > a * 1.4, `the stale family should be drawn clearly more often (${a} against ${b})`);
});
await test('A: review items come least recently seen first', () => {
  const m = { now: NOW, families: [], unseen: [], review: pool(['c1'], 10, 'r', (c, i) => ({ lastSeen: 100 - i })) };   // r-c1-9 is the oldest (91), r-c1-0 the newest (100)
  const p = SEL.cumulative.build(m, { seed: 7, n: 4 });
  eq(p.map((x) => x.uid).sort().join(), ['r-c1-6', 'r-c1-7', 'r-c1-8', 'r-c1-9'].join(), 'the four least recently seen');
});
await test('A: the same model and seed give the same review, another seed another', () => {
  const m = { now: NOW, families: families(COURSES6), unseen: pool(COURSES6, 4, 'u'), review: pool(COURSES6, 6, 'r') };
  const key = (p) => p.map((x) => x.uid + (x.gen ? x.gen.prompt : '')).join('|');
  eq(key(SEL.cumulative.build(m, { seed: 11 })), key(SEL.cumulative.build(m, { seed: 11 })), 'same seed');
  ok(key(SEL.cumulative.build(m, { seed: 11 })) !== key(SEL.cumulative.build(m, { seed: 12 })), 'another seed');
});
await test('A: a family that cannot be drawn is skipped, not a hang', () => {
  const bad = families(['c1'], 1); bad[0].family = Object.assign({}, bad[0].family, { where: ['a > 1000'] });
  const m = { now: NOW, families: bad, unseen: [], review: pool(['c1', 'c2', 'c3', 'c4', 'c5'], 5, 'r') };
  const p = SEL.cumulative.build(m, { seed: 2 });
  eq(p.length, 20);
  eq(count(p, (x) => x.tier === 1), 0);
});

/* ---------- Part B: the schedule ---------- */
const clockAt = (t) => S._setClock(() => t);
await test('B: nothing is due while no level is met', () => {
  clockAt(NOW);
  const st = S.cumulative.status();
  eq(st.dueAt, null, 'no due date'); eq(st.due, false, 'not due'); eq(SEL.cumulativeStatus().eligible, false, 'not eligible');
});
await test('B: the first review is due seven days after the first level was met', () => {
  clockAt(NOW); S.prereq.mark(['algebra/L1'], 'test');
  clockAt(NOW + 3 * DAY); S.prereq.mark(['equations/L1'], 'test');   // a later level does not move the date
  clockAt(NOW + 6.9 * DAY); eq(S.cumulative.status().due, false, 'not yet at 6.9 days');
  clockAt(NOW + 7 * DAY); const st = S.cumulative.status();
  eq(st.due, true, 'due at seven days'); eq(st.dueAt, NOW + 7 * DAY, 'the date'); eq(SEL.cumulativeStatus().eligible, true);
  clockAt(NOW + 9.5 * DAY); eq(S.cumulative.status().overdueDays, 2, 'two days over');
});
await test('B: after a review the next is due seven days after it was finished', () => {
  clockAt(NOW); S.prereq.mark(['algebra/L1'], 'test');
  clockAt(NOW + 10 * DAY); eq(S.cumulative.status().due, true);
  S.cumulative.record({ score: 15, n: 20, byLevel: { 'algebra/L1': 5 }, levels: ['algebra/L1'], fluency: 8, authored: 12, seen: ['u1'] });
  eq(S.cumulative.status().due, false, 'cleared');
  clockAt(NOW + 16.9 * DAY); eq(S.cumulative.status().due, false, 'not at 6.9 days');
  clockAt(NOW + 17 * DAY); eq(S.cumulative.status().due, true, 'due again at seven days');
  const h = S.cumulative.history();
  eq(h.length, 1); eq(h[0].score, 15); eq(h[0].n, 20); eq(h[0].byLevel['algebra/L1'], 5); eq(h[0].at, NOW + 10 * DAY);
  ok(S.cumulative.seen().u1, 'the served item is remembered');
});
await test('B: postponing keeps it due and changes nothing else', () => {
  clockAt(NOW); S.prereq.mark(['algebra/L1'], 'test');
  clockAt(NOW + 8 * DAY);
  const a = S.cumulative.status(); eq(a.postponedToday, false);
  S.cumulative.postpone();
  const b = S.cumulative.status();
  eq(b.due, true, 'still due'); eq(b.postponedToday, true, 'marked for today'); eq(b.dueAt, a.dueAt, 'the due date does not move'); eq(S.cumulative.history().length, 0);
  clockAt(NOW + 9 * DAY + 3600000); eq(S.cumulative.status().postponedToday, false, 'the next day it is plainly due'); eq(S.cumulative.status().due, true);
});
await test('B: a review left part way is not a review: it stays due and what was served is remembered', () => {
  clockAt(NOW); S.prereq.mark(['algebra/L1'], 'test');
  clockAt(NOW + 8 * DAY);
  const row = S.cumulative.record({ score: 3, n: 20, byLevel: {}, levels: [], fluency: 0, authored: 4, seen: ['a', 'b'], partial: true });
  eq(row, null, 'no history row'); eq(S.cumulative.status().due, true, 'still due'); eq(S.cumulative.status().last, null);
  ok(S.cumulative.seen().a && S.cumulative.seen().b, 'seen kept');
});
await test('B: the history keeps 100 reviews and seen 3000 uids; export and import keep both', () => {
  clockAt(NOW); S.prereq.mark(['algebra/L1'], 'test');
  for (let i = 0; i < 105; i++) { clockAt(NOW + (i + 1) * 8 * DAY); S.cumulative.record({ score: i, n: 20, seen: [`u${i}`] }); }
  eq(S.cumulative.history().length, 100); eq(S.cumulative.history()[0].score, 5, 'the oldest five dropped');
  S.cumulative.record({ score: 1, n: 20, seen: Array.from({ length: 3100 }, (_, i) => `bulk${i}`) });
  eq(Object.keys(S.cumulative.seen()).length, 3000, 'seen capped');
  const text = S.export(); S.reset(); S.import(text);
  eq(S.cumulative.history().length, 100, 'history survives export and import');
});
await test('B: an old save with no cumulative block loads with an empty one', () => {
  const d = JSON.parse(S.export()); delete d.cumulative; S.import(JSON.stringify(d));
  eq(S.cumulative.history().length, 0); eq(S.cumulative.status().due, false);
});

/* ---------- Part C: the live model on the real content ---------- */
const courses = C.allCourses();
const written = (cid, id) => C.exists(cid, id) !== false;
const fullLevels = [];
courses.forEach(c => (c.levels || []).forEach(lv => { if (lv.review && written(c.id, lv.review) && (lv.lessons || []).length && lv.lessons.every(id => written(c.id, id))) fullLevels.push({ cid: c.id, lv }); }));
ok(fullLevels.length > 20, 'expected many fully written levels in the content');
const onePerCourse = (k, skip = new Set()) => { const seen = new Set(), out = []; for (const l of fullLevels) { if (seen.has(l.cid) || skip.has(l.cid)) continue; seen.add(l.cid); out.push(l); if (out.length === k) break; } return out; };
const metKeys = (list) => list.map(({ cid, lv }) => `${cid}/L${lv.n}`);
const practiceOk = (it) => !(it.kind === 'longform' || (it.widget && (it.widget.kind === 'longform' || it.widget.kind === 'code')));

await test('C: the review draws twenty items from met levels only, at most four a course, no code or long-form', async () => {
  const six = onePerCourse(6); S.prereq.mark(metKeys(six), 'test');
  const items = await SEL.weeklyReview({ seed: 21 });
  eq(items.length, 20, 'twenty items');
  const cs = new Set(six.map((l) => l.cid));
  ok(items.every((it) => cs.has(it.weekly.course)), 'every item is from a met course');
  ok(Object.values(perCourse(items.map((it) => ({ course: it.weekly.course })))).every((v) => v <= 4), 'at most four from a course');
  ok(items.every(practiceOk), 'no long-form or code item');
  eq(count(items, (it) => it.weekly.tier === 1), 0, 'no Fluency set written: no generated item');
  ok(items.every((it) => it.ref && it.skills), 'every authored item resolves with a ref');
  eq(new Set(items.map((it) => it.uid)).size, 20, 'no item twice');
  const again = await SEL.weeklyReview({ seed: 21 });
  eq(again.map((it) => it.uid).join(), items.map((it) => it.uid).join(), 'the same seed gives the same review');
});
await test('C: with no level met there is nothing to review', async () => {
  const items = await SEL.weeklyReview({ seed: 1 });
  eq(items.length, 0);
});
await test('C: a Fluency set of a met level is drawn first, four items at most from its course', async () => {
  const eqLv = fullLevels.find((l) => l.cid === 'equations' && l.lv.lessons.includes('l3-opening-brackets'));
  ok(eqLv, 'the fixture lesson is in a fully written equations level');
  const six = [eqLv, ...onePerCourse(6, new Set(['equations']))];
  S.prereq.mark(metKeys(six), 'test');
  C._addFluency([{ course: 'equations', doc: fixture }]);
  const items = await SEL.weeklyReview({ seed: 22 });
  eq(items.length, 20);
  eq(count(items, (it) => it.weekly.tier === 1), 4, 'four generated items: the cap for the one course with a set');
  ok(items.filter((it) => it.weekly.tier === 1).every((it) => it.weekly.course === 'equations' && it.fluency && it.widget && it.feedback), 'the generated items are runSet items of the set');
  eq(count(items, (it) => it.weekly.course === 'equations'), 4, 'four from equations in all');
  const fl = items.filter((it) => it.weekly.tier === 1);
  eq(new Set(fl.map((it) => it.question)).size, fl.length, 'distinct generated prompts');
  C._setFluency([]);
});
await test('C: a set whose lesson is not in a met level is not drawn', async () => {
  const six = onePerCourse(6, new Set(['equations'])); S.prereq.mark(metKeys(six), 'test');
  C._addFluency([{ course: 'equations', doc: fixture }]);
  const items = await SEL.weeklyReview({ seed: 23 });
  eq(count(items, (it) => it.weekly.tier === 1), 0);
  C._setFluency([]);
});
await test('C: finishing records the history row, per-level misses, the redo queue, family counts and the seen items', async () => {
  const eqLv = fullLevels.find((l) => l.cid === 'equations' && l.lv.lessons.includes('l3-opening-brackets'));
  const six = [eqLv, ...onePerCourse(6, new Set(['equations']))];
  S.prereq.mark(metKeys(six), 'test');
  C._addFluency([{ course: 'equations', doc: fixture }]);
  const items = await SEL.weeklyReview({ seed: 24 });
  const gens = items.map((it, j) => [it, j]).filter(([it]) => it.weekly.tier === 1), auth = items.map((it, j) => [it, j]).filter(([it]) => it.weekly.tier !== 1);
  const res = items.map(() => ({ ok: true }));
  const missAuth = auth.slice(0, 3).map(([, j]) => j), missGen = gens.slice(0, 2).map(([, j]) => j);
  [...missAuth, ...missGen].forEach((j) => { res[j] = { ok: false }; });
  const r = SEL.weeklyFinish(items, res);
  eq(r.right, 20 - 5, 'score'); eq(r.row.score, 15); eq(r.row.n, 20); eq(r.fluency, 4); eq(r.authored, 16);
  eq(Object.values(r.row.byLevel).reduce((a, b) => a + b, 0), 5, 'five misses by level');
  eq(S.redo.list().length, 3, 'the three authored misses are in the redo queue; the generated ones cannot be');
  ok(S.redo.list().every((x) => missAuth.some((j) => items[j].uid === x.id)), 'with their own ids');
  const f = S.fluency.get('equations', fixture.id);
  ok(f && Object.values(f.families).reduce((a, x) => a + x.right + x.wrong, 0) === 4 && Object.values(f.families).reduce((a, x) => a + x.wrong, 0) === 2, `family counts: ${JSON.stringify(f)}`);
  eq(f.attempts, 0, 'a weekly review is not a Fluency attempt'); eq(f.passedAt, null);
  eq(Object.keys(S.cumulative.seen()).length, 16, 'the sixteen authored uids are remembered');
  eq(S.cumulative.history().length, 1); eq(S.cumulative.status().due, false);
  /* the authored items served are not unseen next time */
  const next = await SEL.weeklyReview({ seed: 25 });
  const tier2 = next.filter((it) => it.weekly.tier === 2).map((it) => it.uid);
  ok(tier2.every((u) => !S.cumulative.seen()[u]), 'tier 2 takes only items never served');
  C._setFluency([]);
});
await test('C: leaving part way records the answered items without making a review', async () => {
  const six = onePerCourse(6); S.prereq.mark(metKeys(six), 'test');
  const items = await SEL.weeklyReview({ seed: 26 });
  const res = items.map(() => undefined); res[0] = { ok: false }; res[1] = { ok: true };
  const r = SEL.weeklyFinish(items, res, { partial: true });
  eq(r.row, null, 'no history row'); eq(S.cumulative.history().length, 0); eq(S.redo.list().length, 1, 'the one miss is queued');
  eq(Object.keys(S.cumulative.seen()).length, 2);
});
await test('C: a weekly review moves no gate: the met levels and lessons are as they were', async () => {
  const six = onePerCourse(6); S.prereq.mark(metKeys(six), 'test');
  const before = JSON.stringify({ met: S.prereq.get().met, lessons: S.lessons, reviews: S.reviews, exams: S.exams, perf: S.perf.get() });
  const items = await SEL.weeklyReview({ seed: 27 });
  SEL.weeklyFinish(items, items.map(() => ({ ok: false })));
  eq(JSON.stringify({ met: S.prereq.get().met, lessons: S.lessons, reviews: S.reviews, exams: S.exams, perf: S.perf.get() }), before);
});

const failed = results.filter((x) => !x).length;
console.log(`test-cumulative: ${results.length - failed} of ${results.length} passed`);
process.exit(failed ? 1 : 0);
