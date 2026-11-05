#!/usr/bin/env node
/* Unit tests for the met rule rewrite (PLAN 2c item 4; ENGINE-BACKLOG 528). Plain node, no browser: a minimal fake window and
   localStorage, the real js/state.js, js/content.js and js/prereq.js, and the real content/ files read through a fake fetch, as the app loads them.
   Run from anywhere: node app/tools/test-met-rule.mjs. One PASS or FAIL line per test, a summary line, exit code 1 on any failure. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CONTENT = path.join(APP, 'content');

const store = new Map();
globalThis.localStorage = { getItem: (k) => (store.has(k) ? store.get(k) : null), setItem: (k, v) => { store.set(k, String(v)); }, removeItem: (k) => { store.delete(k); }, clear: () => store.clear() };
globalThis.window = globalThis;
globalThis.ZQ = { emit: () => {}, on: () => {} };   // no sync on every mutation: the tests call prereq.sync() themselves
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
const reset = () => { store.clear(); S._reload(); };
const results = [];
const test = async (name, fn) => {
  reset();
  try { await fn(); results.push(true); console.log(`PASS ${name}`); }
  catch (e) { results.push(false); console.log(`FAIL ${name}: ${e && e.message ? e.message : e}`); }
};
const eq = (a, b, m) => { if (a !== b) throw new Error(`${m || 'value'}: expected ${b}, got ${a}`); };
const ok = (c, m) => { if (!c) throw new Error(m || 'assertion failed'); };
const saved = () => JSON.parse(S.export());

/* ---------- Fixtures from the real content ---------- */
const courses = C.allCourses();
const written = (cid, id) => C.exists(cid, id) !== false;
const fullLevels = [];
courses.forEach(c => (c.levels || []).forEach(lv => {
  if (lv.review && written(c.id, lv.review) && (lv.lessons || []).length && lv.lessons.every(id => written(c.id, id))) fullLevels.push({ cid: c.id, lv });
}));
ok(fullLevels.length > 20, 'expected many fully written levels in the content');

const reviewOf = ({ cid, lv }) => readJSON(`courses/${cid}/${lv.review}.json`);
const sitReview = (L, missed = [], extra = {}) => {
  const D = reviewOf(L);
  const rows = D.items.map((it, i) => ({ id: it.id || 'q' + i, ok: !missed.includes(i), difficulty: it.difficulty || 3, skills: it.skills || [], ref: { course: L.cid, lesson: L.lv.review, item: it.id || 'q' + i } }));
  S.reviewFinished({ course: L.cid, id: L.lv.review, results: rows, items: rows.length, ...extra });
  return D;
};
const gapsFor = (D, missed) => {
  const by = {}; D.items.forEach((it, i) => (it.skills || []).forEach(s => { const b = by[s] || (by[s] = [0, 0]); b[1]++; if (!missed.includes(i)) b[0]++; }));
  return S.floorGaps(by, [...new Set(D.items.flatMap(it => it.skills || []))], P.SKILL_FLOOR);
};
/* a fully written level with a 10-item review that has a pair of misses under the floor and another pair over it */
const findPairs = () => {
  for (const L of fullLevels) {
    const D = reviewOf(L); if (D.items.length !== 10) continue;
    let bad = null, good = null;
    for (let i = 0; i < 10; i++) for (let j = i + 1; j < 10; j++) { const g = gapsFor(D, [i, j]).length; if (g && !bad) bad = [i, j]; if (!g && !good) good = [i, j]; }
    if (bad && good) return { L, D, bad, good };
  }
  throw new Error('no 10-item review with both a below-floor and an at-floor pair of misses');
};
const needsExam = () => {   // a course with a topic and two levels whose reviews list different skills
  for (const L of fullLevels) {
    const co = C.course(L.cid); if (!co.topic) continue;
    const ea = new Set(reviewOf(L).items.flatMap(it => it.skills || []));
    for (const o of fullLevels.filter(x => x.cid === L.cid && x.lv.n !== L.lv.n)) {
      const eb = [...new Set(reviewOf(o).items.flatMap(it => it.skills || []))];
      if (eb.some(s => !ea.has(s))) return { A: L, B: o, topic: co.topic, ea: [...ea], eb };
    }
  }
  throw new Error('no course with two levels of different skills');
};
const firstLessonOf = (L) => ({ cid: L.cid, id: L.lv.lessons[0], doc: readJSON(`courses/${L.cid}/${L.lv.lessons[0]}.json`) });
const wide = (x) => { const d = firstLessonOf(x).doc; return (d.screens || []).filter(s => s.widget).length >= 6 && (d.quiz || []).length >= 4; };
/* what the player records: a screenGraded per gradable screen (revealed or not), the quiz, then lessonFinished with [first-try count, gradable] */
const playLesson = (cid, id, doc, { reveal, quizMiss = 1 }) => {
  const screens = doc.screens || [], quiz = doc.quiz || [];
  const idx = screens.map((s, i) => (s.widget ? i : -1)).filter(i => i >= 0);
  idx.forEach((i, k) => S.screenGraded({ course: cid, lesson: id, screen: i, ok: !reveal(k), firstTry: !reveal(k), revealed: reveal(k), skills: doc.skills || [] }));
  const rows = quiz.map((q, j) => ({ id: q.id || 'q' + j, ok: j >= quizMiss, difficulty: 2, skills: q.skills || doc.skills || [] }));
  S.quizFinished({ course: cid, lesson: id, results: rows, items: quiz.length, skills: doc.skills || [] });
  S.lessonFinished({ course: cid, lesson: id, firstTry: [idx.filter((_, k) => !reveal(k)).length, idx.length + quiz.length] });
  return { gradable: idx.length + quiz.length, n: idx.length, idx };
};

/* ---------- Tests, one per rule ---------- */
await test('rule 1: review pass defaults to 0.8 (7 of 10 does not pass, 8 of 10 does)', async () => {
  eq(P.PASS, 0.8, 'prereq PASS'); eq(S.rules.REVIEW_PASS, 0.8, 'state REVIEW_PASS'); eq(S.rules.MASTERY, 0.8, 'MASTERY');
  eq(P.SKILL_FLOOR, S.rules.SKILL_FLOOR, 'SKILL_FLOOR in prereq and state');
  const { L, D } = findPairs();
  const rows = (n) => D.items.map((it, i) => ({ id: it.id || 'q' + i, ok: i >= n, difficulty: 3, skills: [] }));   // no skill tags: the aggregate alone
  S.reviewFinished({ course: L.cid, id: L.lv.review, results: rows(3), items: 10 });
  eq(saved().reviews[`${L.cid}/${L.lv.review}`].passedAuto, false, '7 of 10 passedAuto');
  S.reviewFinished({ course: L.cid, id: L.lv.review, results: rows(2), items: 10 });
  eq(saved().reviews[`${L.cid}/${L.lv.review}`].passedAuto, true, '8 of 10 passedAuto');
  ok(/ZQ\.prereq \? ZQ\.prereq\.PASS : 0\.8/.test(fs.readFileSync(path.join(APP, 'js/screens/review.js'), 'utf8')), 'review screen fallback is 0.8');
});

await test('rule 2: 8 of 10 with one skill under the floor does not meet; at the floor on every skill it does; never removed', async () => {
  const { L, D, bad, good } = findPairs();
  sitReview(L, bad);
  ok(gapsFor(D, bad).length > 0, 'fixture has a gap');
  ok(!P.levelMet(L.cid, L.lv.n), 'below floor on a skill: not met');
  sitReview(L, good);
  ok(P.levelMet(L.cid, L.lv.n), 'at or above floor on every skill: met');
  sitReview(L, bad);
  ok(P.levelMet(L.cid, L.lv.n), 'a later weaker attempt never removes it');
});

await test('rule 2: the floor helper treats an absent or empty essential skill as below', async () => {
  eq(S.floorGaps({ a: [7, 10], b: [1, 2] }, ['a', 'b', 'c'], 0.7).join(','), 'b,c', 'gaps');
  eq(S.floorGaps({ a: [7, 10] }, ['a'], 0.7).length, 0, 'at the floor passes');
  eq(S.floorGaps({ a: [0, 0] }, ['a'], 0.7).length, 1, 'no rows is a gap');
});

await test('rule 2: test-out applies the same floor to the skills it drew (5 of 6 right, one skill under it, fails)', async () => {
  const drawn = { a: [3, 3], b: [1, 2], c: [1, 1] };   // 5 of 6 right; skill b at 0.5
  ok(S.floorGaps(drawn, Object.keys(drawn), P.SKILL_FLOOR).includes('b'), 'b is under the floor');
  ok(/floorGaps\(drawn, Object\.keys\(drawn\), P\.SKILL_FLOOR\)/.test(fs.readFileSync(path.join(APP, 'js/screens/review.js'), 'utf8')), 'review.js test-out applies it');
});

await test('rule 3: more than 0.25 of gradable screens revealed means the lesson does not count; revealing alone never raises a skill', async () => {
  const { cid, id, doc } = firstLessonOf(fullLevels.find(wide));
  const total = (doc.screens || []).filter(s => s.widget).length + (doc.quiz || []).length, need = Math.floor(0.25 * total) + 1;
  const g = playLesson(cid, id, doc, { reveal: (k) => k < need, quizMiss: 0 });
  const r = S.lesson(cid, id);
  ok(r.done && r.mastered, 'finished and mastered as a raw record');
  ok(!S.lessonCounts(r), `revealed ${r.revealed.length} of ${g.gradable}: should not count`);
  ok(!P.lessonMet(cid, id), 'lessonMet false');
  eq(S.summary().lessonsDone, 0, 'progress figure');
  ok(!P.nodeOf(`${cid}/${id}`).done, 'node done false');
  ok(!P.lessonLocked(cid, id), 'a finished lesson is never locked');
  reset();   // reveal only, no quiz: no skill record at all
  (doc.screens || []).forEach((s, i) => { if (s.widget) S.screenGraded({ course: cid, lesson: id, screen: i, ok: false, revealed: true, skills: doc.skills || [] }); });
  eq(Object.keys(S.skills).length, 0, 'revealed screens create no skill record');
});

await test('rule 3: exactly at the cap counts; an honest replay of revealed screens restores the count', async () => {
  const { cid, id, doc } = firstLessonOf(fullLevels.find(wide));
  const total = (doc.screens || []).filter(s => s.widget).length + (doc.quiz || []).length;
  const atCap = Math.floor(0.25 * total);
  playLesson(cid, id, doc, { reveal: (k) => k < atCap, quizMiss: 0 });
  ok(S.lessonCounts(S.lesson(cid, id)), `${atCap} of ${total} revealed is within the cap`);
  reset();
  const g = playLesson(cid, id, doc, { reveal: () => true, quizMiss: 0 });
  ok(!S.lessonCounts(S.lesson(cid, id)), 'all revealed does not count');
  g.idx.forEach(i => S.screenGraded({ course: cid, lesson: id, screen: i, ok: true, firstTry: true, revealed: false }));
  ok(S.lessonCounts(S.lesson(cid, id)), 'replayed honestly: counts again');
});

await test('rule 4: a topic exam pass meets a level only when its essential skills are covered at the floor', async () => {
  const { A, B, topic, ea } = needsExam();
  await C.loadEssentials(A.cid);
  const rowsFor = (skills) => skills.map((s, i) => ({ id: 'x' + i, ok: true, difficulty: 3, skills: [s] }));
  const by = (rows) => Object.fromEntries(rows.map(r => [r.skills[0], [r.ok ? 1 : 0, 1]]));
  let rows = rowsFor(ea);
  S.examFinished({ id: 'topic-' + topic, score: rows.length, items: rows.length, passed: true, results: rows, bySkill: by(rows) });
  P.sync();
  ok(C.examPassedAuto('topic-' + topic), 'the exam counts as passed');
  ok(P.levelMet(A.cid, A.lv.n), 'covered level is met');
  ok(!reviewOf(B).items.flatMap(it => it.skills || []).every(s => ea.includes(s)) && !P.levelMet(B.cid, B.lv.n), 'a level with an uncovered skill is a badge, not met');
  reset();
  rows = rowsFor(ea); rows[0].ok = false;   // one essential skill at 0 of 1
  S.examFinished({ id: 'topic-' + topic, score: rows.length - 1, items: rows.length, passed: true, results: rows, bySkill: by(rows) });
  P.sync();
  ok(!P.levelMet(A.cid, A.lv.n), 'a pass with one essential skill under the floor does not meet');
});

await test('rule 5: a missed quiz item queues for redo even when the quiz reached mastery', async () => {
  const { cid, id } = firstLessonOf(fullLevels[0]);
  const rows = [0, 1, 2, 3, 4].map(j => ({ id: 'q' + j, ok: j !== 4, difficulty: 2, skills: ['s'] }));
  const out = S.quizFinished({ course: cid, lesson: id, results: rows, items: 5 });
  ok(out.mastered, '4 of 5 is mastered');
  eq(out.redo.length, 1, 'one redo from the result');
  eq(S.redo.list().length, 1, 'one redo in the queue');
});

/* ---------- Acceptance scenarios ---------- */
await test('acceptance: a learner who opens every lesson, reveals every screen and scores 4 of 5 on quizzes ends with zero levels met', async () => {
  let lessons = 0;
  for (const c of courses) for (const lv of c.levels || []) for (const id of lv.lessons || []) {
    if (!written(c.id, id)) continue;
    const doc = readJSON(`courses/${c.id}/${id}.json`);
    playLesson(c.id, id, doc, { reveal: () => true, quizMiss: Math.max(1, Math.round((doc.quiz || []).length * 0.2)) });
    lessons++;
  }
  P.sync();
  let met = 0, counted = 0;
  courses.forEach(c => (c.levels || []).forEach(lv => { if (P.levelMet(c.id, lv.n)) met++; (lv.lessons || []).forEach(id => { if (written(c.id, id) && S.lessonCounts(S.lesson(c.id, id))) counted++; }); }));
  ok(lessons > 100, `played ${lessons} lessons`);
  eq(met, 0, 'levels met');
  eq(counted, 0, 'lessons counted as done');
  eq(S.summary().lessonsDone, 0, 'progress lessonsDone');
});

await test('acceptance: sat cold, 8 of 10 aggregate with a skill under the floor does not meet; at the floor on every skill it does', async () => {
  const { L, bad, good } = findPairs();
  sitReview(L, bad); P.sync();
  ok(!P.levelMet(L.cid, L.lv.n), 'under the floor on one skill');
  reset();
  sitReview(L, good); P.sync();
  ok(P.levelMet(L.cid, L.lv.n), 'at the floor on every skill');
});

/* ---------- Performance task (ENGINE-BACKLOG 529): an extra AND on every route to met ---------- */
const withTask = (L, kind = 'code', gates = true) => { C._setPerf({ [`${L.cid}/L${L.lv.n}`]: { file: `courses/${L.cid}/homework-${L.lv.n}.json`, item: 'perf-item', kind, how: kind === 'code' ? 'auto' : 'self', ...(gates ? { gates: true } : {}) } }); return `${L.cid}/L${L.lv.n}`; };
const perfRow = (kind, ok, how) => ({ id: 'perf-item', ok, how, perf: kind, difficulty: 4, skills: [] });
const submitPerf = (L, kind, ok, how) => S.homeworkSubmitted({ course: L.cid, level: L.lv.n, id: `homework-${L.lv.n}`, results: [perfRow(kind, ok, how)], items: 1 });
await test('performance: a level with a task is not met by a review pass at the floor until the task is passed', async () => {
  const { L, good } = findPairs();
  withTask(L);
  sitReview(L, good); P.sync();
  ok(!P.levelMet(L.cid, L.lv.n), 'review at the floor, task not passed: not met');
  ok(P.perfNeeded(L.cid, L.lv) && !P.perfPassed(L.cid, L.lv), 'perfNeeded and not passed');
  eq(P.nodeOf(`${L.cid}/L${L.lv.n}`).perf.passed, false, 'node fact says not passed');
  submitPerf(L, 'code', false, 'auto'); P.sync();
  ok(!P.levelMet(L.cid, L.lv.n), 'a failed attempt does not meet it');
  submitPerf(L, 'code', true, 'auto'); P.sync();
  ok(P.levelMet(L.cid, L.lv.n), 'task passed and review at the floor: met');
  const rec = saved().perf[`${L.cid}/L${L.lv.n}`];
  ok(rec && rec.how === 'auto' && rec.kind === 'code' && rec.item === 'perf-item', 'stored as { item, kind, how: auto }');
  submitPerf(L, 'code', false, 'auto');
  ok(P.levelMet(L.cid, L.lv.n) && saved().perf[`${L.cid}/L${L.lv.n}`].how === 'auto', 'a later miss never removes it');
  C._setPerf({});
});
await test('performance: the task alone meets nothing, and a self mark is stored how: self', async () => {
  const { L } = findPairs();
  withTask(L, 'derivation');
  submitPerf(L, 'derivation', true, 'self'); P.sync();
  eq(saved().perf[`${L.cid}/L${L.lv.n}`].how, 'self', 'self mark recorded as self');
  ok(!P.levelMet(L.cid, L.lv.n), 'a self mark never meets a level alone (no review pass)');
  sitReview(L, []); P.sync();
  ok(P.levelMet(L.cid, L.lv.n), 'with the review pass as well it is met');
  C._setPerf({});
});
await test('performance: a level without a task is unchanged (review pass meets it, a perf row elsewhere is ignored)', async () => {
  const { L, good } = findPairs();
  C._setPerf({});
  sitReview(L, good); P.sync();
  ok(P.levelMet(L.cid, L.lv.n), 'no task: met by the review as before');
  ok(P.perfPassed(L.cid, L.lv) && !P.perfNeeded(L.cid, L.lv), 'perfPassed is true when there is no task');
});
await test('performance: a task on a level the verb rule does not match is practice only and never gates met (549)', async () => {
  const { L, good } = findPairs();
  const key = withTask(L, 'derivation', false);   // a manifest row without gates: the validator did not rule-match the level
  ok(!P.perfNeeded(L.cid, L.lv) && P.perfPassed(L.cid, L.lv), 'an ungated task is not needed and counts as passed');
  eq(P.nodeOf(key).perf, null, 'the node carries no performance fact');
  sitReview(L, good); P.sync();
  ok(P.levelMet(L.cid, L.lv.n), 'the review pass alone meets the level, no self mark awaited');
  withTask(L, 'derivation', true);   // the same row on a rule-matched level gates again
  ok(P.perfNeeded(L.cid, L.lv) && !P.perfPassed(L.cid, L.lv), 'a gated task is needed until passed');
  C._setPerf({});
});
await test('performance: a code task row in the review file records the pass (level from review-<n>)', async () => {
  const { L, D } = findPairs();
  withTask(L);
  const rows = D.items.map((it, i) => ({ id: it.id || 'q' + i, ok: true, difficulty: 3, skills: it.skills || [], ...(i === 0 ? { perf: 'code', how: 'auto' } : {}) }));
  S.reviewFinished({ course: L.cid, id: L.lv.review, results: rows, items: rows.length }); P.sync();
  ok(saved().perf[`${L.cid}/L${L.lv.n}`], 'recorded');
  ok(P.levelMet(L.cid, L.lv.n), 'review passed and task passed: met');
  C._setPerf({});
});
await test('performance: test-out is a badge until the task is passed, then the level is met', async () => {
  const { L } = findPairs();
  const key = withTask(L);
  S.prereq.testout({ key, score: 6, items: 6, passed: true }); P.sync();
  ok(S.prereq.get().testouts[key].passed, 'test-out recorded');
  ok(!P.levelMet(L.cid, L.lv.n), 'test-out passed, task not passed: not met');
  submitPerf(L, 'code', true, 'auto'); P.sync();
  ok(P.levelMet(L.cid, L.lv.n), 'task passed: the test-out now meets it');
  C._setPerf({});
});
await test('performance: a topic exam pass is a badge for a level with a task until the task is passed', async () => {
  const { A, topic, ea } = needsExam();
  await C.loadEssentials(A.cid);
  const key = withTask(A);
  const rows = ea.map((s, i) => ({ id: 'x' + i, ok: true, difficulty: 3, skills: [s] }));
  S.examFinished({ id: 'topic-' + topic, score: rows.length, items: rows.length, passed: true, results: rows, bySkill: Object.fromEntries(rows.map(r => [r.skills[0], [1, 1]])) });
  P.sync();
  ok(C.examPassedAuto('topic-' + topic), 'exam counts as passed');
  ok(!P.levelMet(A.cid, A.lv.n), 'covered, but the task is not passed: not met');
  submitPerf(A, 'code', true, 'auto'); P.sync();
  ok(P.levelMet(A.cid, A.lv.n), `task passed (${key}): met`);
  C._setPerf({});
});

const pass = results.filter(Boolean).length;
console.log(`${pass === results.length ? 'PASS' : 'FAIL'} summary: ${pass} of ${results.length} tests passed`);
process.exit(pass === results.length ? 0 : 1);
