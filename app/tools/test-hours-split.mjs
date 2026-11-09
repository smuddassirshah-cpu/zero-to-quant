#!/usr/bin/env node
/* In-app hours shown apart from outside-study hours (session Y; AUTHORING section 14).
   1. js/hours.js on a small made-up curriculum: lesson, level, course, topic, stage and role figures, the allowances (review 20,
      homework 45, topic exam 60), stated minutes overriding them, the exam shared by lesson weight, outside floored at 0, splitLabel.
   2. The real content: every stage, topic and role set has both figures, they add up the way the contract says, and the app's
      ZQ.content (js/content.js over the manifest, as the browser loads it) gives the same figures as the node tools.
   3. The surfaces: readiness.json, docs/readiness.md and docs/curriculum.md carry both figures and no stored total alone; the screens call splitLabel.
   Usage: node tools/test-hours-split.mjs   Exit 0 when all pass, 1 on a failure. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { loadHours } from './hours-source.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CONTENT = path.join(APP, 'content');
const DOCS = path.join(APP, '..', 'docs');
const hours = createRequire(import.meta.url)('../js/hours.js');

let fails = 0, n = 0;
const ok = (cond, msg) => { n++; if (!cond) { fails++; console.log(`FAIL ${msg}`); } };
const near = (a, b, msg, eps = 1e-9) => ok(Math.abs(a - b) <= eps, `${msg}: ${a} against ${b}`);

/* ---- 1. A made-up curriculum: topic T1 (60 h) holds courses a (2 levels, 3 + 2 lessons) and b (1 level, 1 workshop of 60 min); topic T2 stores 0 ---- */
const cur = { stages: [{ id: 9, topics: [{ id: 'T1', hours: 60, courses: ['a', 'b'] }, { id: 'T2', hours: 0, courses: ['c'] }] }] };
const courses = {
  a: { topic: 'T1', levels: [{ n: 1, lessons: ['a1', 'a2', 'a3'] }, { n: 2, lessons: ['a4', 'a5'] }] },
  b: { topic: 'T1', levels: [{ n: 1, lessons: ['b1'] }] },
  c: { topic: 'T2', levels: [{ n: 1, lessons: ['c1'] }] },
};
const mins = { 'a/a1': 12, 'a/a2': 14, 'a/a3': 16, 'a/a4': 10, 'b/b1': 60, 'c/c1': 15 };   // a5 is not written: it counts SHORT_NORM (14)
const written = (c, l) => `${c}/${l}` in mins;
const H = hours.build({ curriculum: cur, courses, written, sessions: { 'b/b1': { session: 'workshop', minutes: 60 } }, minutes: (c, l) => mins[`${c}/${l}`] });
near(H.lessonApp('a', 'a1'), 12 / 60, 'a written lesson counts its own minutes');
near(H.lessonApp('a', 'a5'), 14 / 60, 'an unwritten lesson counts the short-lesson norm (14)');
near(H.lessonApp('b', 'b1'), 1, 'a workshop counts its true minutes');
near(H.levelApp('a', 1), (12 + 14 + 16 + 20 + 45) / 60, 'a level is its lessons plus the review and homework allowances');
near(H.levelApp('a', 2), (10 + 14 + 20 + 45) / 60, 'level 2 of course a');
near(H.levelApp('a', 9), 0, 'a level that does not exist is 0');
// topic T1 lesson weights: a = 5 lessons of weight 1, b = one workshop of 60 / 14
const wA = 5, wB = 60 / 14, W = wA + wB;
near(H.courseApp('a'), (12 + 14 + 16 + 20 + 45 + 10 + 14 + 20 + 45) / 60 + (60 / 60) * wA / W, 'a course adds its share of the topic exam (60 min allowance, by lesson weight)');
near(H.courseApp('b'), (60 + 20 + 45) / 60 + (60 / 60) * wB / W, 'course b share of the exam');
near(H.topicApp('T1'), H.courseApp('a') + H.courseApp('b'), 'a topic is the sum of its courses');
near(H.stageApp(9), H.topicApp('T1') + H.topicApp('T2'), 'a stage is the sum of its topics');
near(H.totalApp(), H.stageApp(9), 'the total is the sum of its stages');
near(H.topicOut('T1'), 60 - H.topicApp('T1'), 'outside is stored less in-app');
near(H.topicOut('T2'), 0, 'a topic that stores 0 has no outside hours: floored at 0');
near(H.courseOut('c'), 0, 'a course of a 0-hour topic has no outside hours');
near(H.lessonOut('a', 'a1'), 60 * 1 / W - 12 / 60, 'a lesson is its stored share less its own minutes');
near(H.stageOut(9), H.topicOut('T1') + H.topicOut('T2'), 'a stage outside is the sum of its topics');
const rs = H.roleSums((c) => (c === 'c' ? 'optional' : 'required'), ['required']);
ok(rs.app === Math.round(H.courseApp('a') + H.courseApp('b')) && rs.out === Math.round(H.courseOut('a') + H.courseOut('b')), `roleSums gives app and out (${JSON.stringify(rs)})`);
// stated minutes override the allowances
const H2 = hours.build({ curriculum: cur, courses, written, sessions: {}, minutes: (c, l) => mins[`${c}/${l}`], setMinutes: { 'a/review-1': 30, 'a/homework-1': 90 }, examMinutes: { 'topic-T1': 45 } });
near(H2.levelApp('a', 1), (12 + 14 + 16 + 30 + 90) / 60, 'a review and homework that state minutes replace the allowances');
near(H2.levelApp('a', 2), H.levelApp('a', 2), 'a level whose files state nothing keeps the allowances');
near(H2.courseApp('a') - H2.levelApp('a', 1) - H2.levelApp('a', 2), (45 / 60) * wA / (wA + 1), 'a stated exam length replaces the 60 minute allowance (b weighs 1 without the workshop session)');
// formats
ok(hours.splitLabel(150, 1650) === 'about 150 h in the app, about 1,650 h of outside study', `splitLabel long form (${hours.splitLabel(150, 1650)})`);
ok(hours.splitLabel(3.46, 48.2, { short: true }) === '3.5 h in the app, 48 h outside', `splitLabel short form (${hours.splitLabel(3.46, 48.2, { short: true })})`);
ok(hours.fmtH(9.96) === '10' && hours.fmtH(0.04) === '0' && hours.fmtH(1234.5) === '1,235', 'fmtH rounds to whole hours from 10 up and one decimal below');
ok(hours.REVIEW_MIN === 20 && hours.HOMEWORK_MIN === 45 && hours.EXAM_MIN === 60, 'the allowances are the documented ones');

/* ---- 2. The real content ---- */
const { H: HR, cur: curR, setMinutes, examMinutes } = loadHours(CONTENT);
let stageApp = 0, stageOut = 0;
for (const s of curR.stages) {
  const a = HR.stageApp(s.id), o = HR.stageOut(s.id);
  near(a, s.topics.reduce((x, t) => x + HR.topicApp(t.id), 0), `stage ${s.id} in-app is the sum of its topics`, 1e-6);
  near(o, s.topics.reduce((x, t) => x + HR.topicOut(t.id), 0), `stage ${s.id} outside is the sum of its topics`, 1e-6);
  ok(a > 0 && o >= 0, `stage ${s.id} has in-app and non-negative outside hours (${a.toFixed(1)}, ${o.toFixed(1)})`);
  ok(a + o + 1e-6 >= HR.stage(s.id), `stage ${s.id}: in-app plus outside is at least the stored hours (outside is floored, never raised)`);
  for (const t of s.topics) {
    ok(HR.topicOut(t.id) >= 0 && HR.topicApp(t.id) >= 0, `topic ${t.id} figures are not negative`);
    if (t.hours > 0) ok(Math.abs(HR.topicApp(t.id) + HR.topicOut(t.id) - t.hours) < 1e-6 || HR.topicOut(t.id) === 0, `topic ${t.id}: in-app plus outside is the stored ${t.hours} h`);
    const cs = (t.courses || []);
    near(HR.topicApp(t.id), cs.reduce((x, c) => x + HR.courseApp(c), 0), `topic ${t.id} in-app is the sum of its courses`, 1e-6);
  }
  stageApp += a; stageOut += o;
}
near(HR.totalApp(), stageApp, 'total in-app', 1e-6); near(HR.totalOut(), stageOut, 'total outside', 1e-6);
ok(Object.keys(examMinutes).length >= 20, `topic exam minutes read from the exam files (${Object.keys(examMinutes).length})`);
ok(Object.keys(setMinutes).length === 0 || Object.values(setMinutes).every((m) => m > 0), 'review and homework minutes, where stated, are positive');
// the lesson figure for a real written lesson is its authored minutes
const algebra = JSON.parse(fs.readFileSync(path.join(CONTENT, 'courses', 'algebra', 'l1-symmetries.json'), 'utf8'));
near(HR.lessonApp('algebra', 'l1-symmetries'), algebra.minutes / 60, 'a real lesson counts its authored minutes');

/* The browser path: js/content.js over the manifest, with hours.js loaded first as index.html does */
const win = { ZQ: {} };
const fetchStub = async (url) => {
  const f = path.join(CONTENT, String(url).replace(/^content\//, '').split('?')[0]);
  if (!fs.existsSync(f)) return { ok: false, status: 404, json: async () => null };
  return { ok: true, status: 200, json: async () => JSON.parse(fs.readFileSync(f, 'utf8')) };
};
const ctx = vm.createContext({ window: win, fetch: fetchStub, console, document: undefined, setTimeout, clearTimeout });
vm.runInContext(fs.readFileSync(path.join(APP, 'js/hours.js'), 'utf8'), ctx);
vm.runInContext(fs.readFileSync(path.join(APP, 'js/content.js'), 'utf8'), ctx);
await win.ZQ.content.ready;
const C = win.ZQ.content;
ok(C.hours && typeof C.hours.courseApp === 'function', 'ZQ.content.hours is the model');
for (const s of C.stages()) {
  near(s.hoursApp, HR.stageApp(s.id), `app: stage ${s.id} in-app equals the tools' figure`, 0.01);
  near(s.hoursOut, HR.stageOut(s.id), `app: stage ${s.id} outside equals the tools' figure`, 0.01);
  for (const t of s.topics) near(t.hoursApp, HR.topicApp(t.id), `app: topic ${t.id} in-app equals the tools' figure`, 0.01);
}
const manifest = JSON.parse(fs.readFileSync(path.join(CONTENT, 'manifest.json'), 'utf8'));
ok(manifest.lessonMinutes && manifest.lessonMinutes['algebra/l1-symmetries'] === algebra.minutes, 'manifest.lessonMinutes carries every lesson\'s minutes (run node tools/validate.mjs)');
ok(manifest.setMinutes && typeof manifest.setMinutes === 'object', 'manifest.setMinutes exists');

/* ---- 3. The surfaces ---- */
const readiness = JSON.parse(fs.readFileSync(path.join(CONTENT, 'readiness.json'), 'utf8'));
for (const [role, r] of Object.entries(readiness.roles)) {
  const t = r.totals;
  for (const k of ['required', 'recommended', 'header']) ok(Number.isInteger(t[k].hoursInApp) && Number.isInteger(t[k].hoursOutside), `readiness.json ${role} ${k} has hoursInApp and hoursOutside`);
  ok(Math.abs(t.header.hoursInApp - (t.required.hoursInApp + t.recommended.hoursInApp)) <= 0 && Math.abs(t.header.hoursOutside - (t.required.hoursOutside + t.recommended.hoursOutside)) <= 0, `readiness.json ${role}: the header is required plus recommended`);
  ok(t.header.hoursInApp + t.header.hoursOutside >= t.header.hours - 3, `readiness.json ${role}: in-app plus outside covers the stored ${t.header.hours} h (within rounding)`);
}
const trader = readiness.roles.trader.totals.header;
console.log(`Trader route: ${trader.total} lessons, ${hours.splitLabel(trader.hoursInApp, trader.hoursOutside)}`);
ok(trader.hoursInApp > 0 && trader.hoursOutside > trader.hoursInApp, 'the trader route has more outside study than in-app hours');
const md = fs.readFileSync(path.join(DOCS, 'readiness.md'), 'utf8');
ok(!/\| Hours total \|/.test(md) && !/Hours written \|/.test(md), 'readiness.md shows no stored-total column');
ok((md.match(/\| Hours in the app \| Hours of outside study \|/g) || []).length === 6, 'readiness.md has the two hours columns in each of the six role tables');
const cmd = fs.readFileSync(path.join(DOCS, 'curriculum.md'), 'utf8');
ok(/\| Stage \| In the app \| Outside study \|/.test(cmd) && /\| Topic \| Name \| In the app \| Outside study \|/.test(cmd), 'curriculum.md tables give both figures');
ok(!/^## Stage \d: [^\n]*\(\d[\d,]* hours\)/m.test(cmd), 'curriculum.md stage headings do not show the stored total alone');
const learn = fs.readFileSync(path.join(APP, 'js/screens/learn.js'), 'utf8');
ok(/splitLabel/.test(learn) && !/\$\{fmt\(s\.hours\)\}|hrs\(t\.hours\)\}\<\/span\><\/h2>|hrs\(s2\.hours\)/.test(learn), 'learn.js shows hours through splitLabel (header, stage, topic)');
ok(/hoursInApp/.test(learn), 'learn.js reads the role header\'s in-app figure');
ok(/splitLabel/.test(fs.readFileSync(path.join(APP, 'js/screens/course.js'), 'utf8')), 'the course page shows both figures');
ok(/splitLabel/.test(fs.readFileSync(path.join(APP, 'js/screens/setup.js'), 'utf8')), 'setup shows both figures on the stage rows');

console.log(fails ? `${fails} failed of ${n}` : `All passed (${n} checks)`);
process.exit(fails ? 1 : 0);
