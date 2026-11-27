#!/usr/bin/env node
/* The optional AI strand (course.json strand "ai"; ENGINE-BACKLOG 1218, docs/AUTHORING.md "strand").
   An ai course never touches the quant path. Each exclusion is proved on the fixture course tools/fixtures/mini-app/content/courses/ai-sample
   (topic 1.12, stage 1, the only topic whose courses are all ai):
     validator    accepts "ai", rejects an unknown strand, rejects a topic mixing ai and other courses, accepts no readiness row (or an "optional" one), keeps ai out of stage papers and stage draws, lets ai require quant and never the reverse
     hours.js     a stage, the total and a role's sums leave the ai topic out; H.ai() reports it alone; with no ai course nothing moves
     content.js   strand, badge, "Quant path only" and the AI switch hide it, pathTopics leaves it out of the stage count, Today's plan skips it unless aiToday
     census and curriculum-hours  every existing figure unchanged, one AI line
   Run: node tools/test-strand-ai.mjs. One FAIL line per failure, exit 1. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import vm from 'node:vm';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { openHarness, TOOLS, APP, MINI } from './lib/validate-harness.mjs';
import { loadHours } from './hours-source.mjs';

let fails = 0, n = 0;
const ok = (c, m, d = '') => { n++; if (!c) { fails++; console.log(`FAIL ${m}${d ? '  ' + d : ''}`); } };
const near = (a, b, m) => ok(Math.abs(a - b) < 1e-9, m, `${a} against ${b}`);
const rd = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const hours = createRequire(import.meta.url)('../js/hours.js');
const CONTENT = path.join(MINI, 'content');

/* ---- 1. The validator ---- */
{
  const h = openHarness({ name: 'strand-ai' });
  const base = h.validate();
  ok(base.code === 0 && /\b0 errors\b/.test(base.out), 'the fixture with an ai course: 0 errors', base.errors.slice(0, 3).join(' | '));
  const cf = h.path('content/courses/ai-sample/course.json'), d = rd(cf);
  const put = (x) => fs.writeFileSync(cf, JSON.stringify(x, null, 2));
  put({ ...d, strand: 'ml' });
  let r = h.validate(); ok(r.errors.some((l) => /strand must be "quant", "pure" or "ai"/.test(l)), 'an unknown strand is rejected', r.errors.join('|'));
  put({ ...d, strandNote: undefined });
  r = h.validate(); ok(r.errors.some((l) => /strandNote/.test(l)), 'strand "ai" needs a strandNote like the other strands');
  h.reset();
  const curF = h.path('content/curriculum.json'), cur = rd(curF);
  const st1 = cur.stages.find((s) => s.id === 1), t112 = st1.topics.find((t) => t.id === '1.12'), t18 = st1.topics.find((t) => t.id === '1.8');
  t112.courses.push(...t18.courses); t18.courses = [];
  cur.courses[t112.courses[1]].topic = '1.12';
  fs.writeFileSync(curF, JSON.stringify(cur, null, 2));
  const moved = rd(h.path(`content/courses/${t112.courses[1]}/course.json`)); moved.topic = '1.12';
  fs.writeFileSync(h.path(`content/courses/${t112.courses[1]}/course.json`), JSON.stringify(moved, null, 2));
  r = h.validate(); ok(r.errors.some((l) => /only AI-strand courses \(strand "ai"\) or none of them/.test(l)), 'a topic mixing ai and other courses is an error', r.errors.slice(0, 4).join('|'));
  h.reset();
  const rf = h.path('content/readiness.json'), rj = rd(rf);
  rj.roles.trader.courses["ai-sample"] = "required";
  fs.writeFileSync(rf, JSON.stringify(rj, null, 2));
  r = h.validate(); ok(r.errors.some((l) => /roles\.trader\.courses\.ai-sample.*must be "optional"/.test(l)), "readiness.json rejects a non-optional ai row", r.errors.slice(0, 3).join('|'));
  h.reset();
  const ex = { id: 'stage-1', stage: 1, parts: [{ kind: 'paper', name: 'Paper', minutes: 30, pass: 0.5, items: [{ id: 'x1', skills: ['ai-loss'], question: 'q' }, { id: 'x2', skills: ['at-complexity'], question: 'q' }] }] };
  fs.writeFileSync(h.path('content/exams/stage-1.json'), JSON.stringify(ex));
  r = h.validate();
  ok(r.errors.some((l) => /unknown skill "ai-loss"/.test(l)), 'a stage paper cannot test an ai skill', r.errors.slice(0, 3).join('|'));
  ok(!r.errors.some((l) => /unknown skill "at-complexity"/.test(l)), 'a quant skill is still allowed in a stage paper');
  /* follow-up (ENGINE-BACKLOG 1260 to 1262): the readiness exemption, the requires direction, the stage-exam draw check */
  h.reset();
  r = h.validate(); ok(r.code === 0 && !r.errors.some((l) => /ai-sample/.test(l) && /readiness/.test(l)), 'an ai course with no readiness row in any role: 0 errors', r.errors.slice(0, 3).join('|'));
  const rj2 = rd(rf); rj2.roles.trader.courses['ai-sample'] = 'optional'; fs.writeFileSync(rf, JSON.stringify(rj2, null, 2));
  r = h.validate(); ok(r.code === 0, 'a readiness row for an ai course is accepted when "optional"', r.errors.slice(0, 3).join('|'));
  rj2.roles.trader.courses['ai-sample'] = 'required'; fs.writeFileSync(rf, JSON.stringify(rj2, null, 2));
  r = h.validate(); ok(r.errors.some((l) => /roles\.trader\.courses\.ai-sample.*must be "optional"/.test(l)), 'a "required" row for an ai course is an error', r.errors.slice(0, 3).join('|'));
  h.reset();
  const dropLevel = rd(cf); dropLevel.levels = dropLevel.levels.slice(0, 2); put(dropLevel);
  r = h.validate(); ok(r.errors.some((l) => /3 to 5 levels \(found 2\)/.test(l)), 'an ai course keeps the 3 to 5 level rule');
  h.reset();
  const withReq = rd(cf); withReq.levels[1].requires = [{ ref: 'first-python/L1', why: 'Loops come before gradient descent.' }]; put(withReq);
  r = h.validate(); ok(r.code === 0, 'an ai course may require a quant course level (and a quant course needs no edge into ai)', r.errors.slice(0, 3).join('|'));
  h.reset();
  const fpf = h.path('content/courses/first-python/course.json'), fp = rd(fpf);
  fp.levels[1].requires = [{ ref: 'ai-sample/L1', why: 'Fitting first.' }]; fs.writeFileSync(fpf, JSON.stringify(fp, null, 2));
  r = h.validate(); ok(r.errors.some((l) => /ai-sample\/L1.*non-AI course never requires it/.test(l)), 'a quant course requiring an ai level is an error', r.errors.slice(0, 3).join('|'));
  h.reset();
  const stageDraw = (from) => ({ id: 'stage-1', stage: 1, parts: [{ kind: 'paper', name: 'Paper', minutes: 30, pass: 0.5, items: [], draw: [{ from, n: 1 }] }] });
  fs.writeFileSync(h.path('content/bank/ai-scratch.json'), JSON.stringify({ id: 'ai-scratch', name: 'Scratch', items: [{ id: 'a1', difficulty: 2, skills: ['ai-loss'], tags: ['t'] }] }));
  fs.writeFileSync(h.path('content/exams/stage-1.json'), JSON.stringify(stageDraw('bank/ai-scratch')));
  r = h.validate(); ok(r.errors.some((l) => /bank\/ai-scratch.*draws bank\/ai-scratch\/a1 from the AI strand/.test(l)), 'a stage exam drawing a bank item with an ai skill is an error', r.errors.slice(0, 3).join('|'));
  fs.writeFileSync(h.path('content/exams/mock-ai.json'), JSON.stringify({ ...stageDraw('bank/ai-scratch'), id: 'mock-ai' }));
  fs.rmSync(h.path('content/exams/stage-1.json'));
  r = h.validate(); ok(!r.errors.some((l) => /from the AI strand/.test(l)), 'the draw rule applies to stage exams only');
  fs.rmSync(h.path('content/exams/mock-ai.json')); fs.rmSync(h.path('content/bank/ai-scratch.json'));
  fs.writeFileSync(h.path('content/drills/ai-drill.json'), JSON.stringify({ ...rd(h.path('content/drills/dsa-missing-seq.json')), id: 'ai-drill', course: 'ai-sample', skills: ['ai-loss'] }));
  fs.writeFileSync(h.path('content/exams/stage-1.json'), JSON.stringify(stageDraw('drills/ai-drill')));
  r = h.validate(); ok(r.errors.some((l) => /draws drills\/ai-drill from the AI strand/.test(l)), 'a stage exam drawing an ai course drill is an error', r.errors.slice(0, 3).join('|'));
  h.close();
}

/* ---- 1b. Learn and Review show the strand at topic level (the badge, as for Pure maths) ---- */
{
  const learn = fs.readFileSync(path.join(APP, 'js/screens/learn.js'), 'utf8'), review = fs.readFileSync(path.join(APP, 'js/screens/review.js'), 'utf8');
  ok((learn.match(/strandBadge\(C\.topicStrand\(t\)/g) || []).length >= 2, 'Learn badges a topic heading and its exam chip by topicStrand');
  ok(/strandBadge\(C\(\)\.topicStrand\(t\)/.test(review), 'Review badges a topic exam row by topicStrand');
}

/* ---- 2. hours.js ---- */
{
  const cur = { stages: [{ id: 9, topics: [{ id: 'Q', hours: 60, courses: ['q'] }, { id: 'A', hours: 40, courses: ['a'] }] }] };
  const courses = { q: { topic: 'Q', levels: [{ n: 1, lessons: ['q1', 'q2'] }] }, a: { topic: 'A', strand: 'ai', levels: [{ n: 1, lessons: ['a1'] }] } };
  const H = hours.build({ curriculum: cur, courses, written: () => true, minutes: () => 14 });
  const noAi = hours.build({ curriculum: cur, courses: { ...courses, a: { ...courses.a, strand: undefined } }, written: () => true, minutes: () => 14 });
  ok(H.aiTopic(cur.stages[0].topics[1]) && !H.aiTopic(cur.stages[0].topics[0]), 'a topic whose courses are all ai is an ai topic');
  near(H.stage(9), 60, 'stage hours leave the ai topic out'); near(H.total(), 60, 'total hours leave it out');
  near(H.stageApp(9), H.topicApp('Q'), 'stage in-app leaves it out'); near(H.stageOut(9), H.topicOut('Q'), 'stage outside leaves it out');
  near(H.totalApp(), H.topicApp('Q'), 'total in-app leaves it out');
  near(H.ai().app, H.topicApp('A'), 'ai() reports its in-app hours'); near(H.ai().hours, 40, 'ai() reports its stored hours'); ok(H.ai().topics === 1, 'ai() counts its topics');
  const rs = H.roleSums(() => 'required', ['required']);
  near(rs.app, Math.round(H.courseApp('q')), 'a role sum leaves the ai course out');
  ok(noAi.ai().topics === 0 && noAi.stage(9) === 100 && noAi.roleSums(() => 'required', ['required']).app === Math.round(noAi.courseApp('q') + noAi.courseApp('a')), 'with no ai course every figure is as before');
  near(hours.stageHours(cur.stages[0]), 100, 'stageHours without a skip is the plain sum'); near(hours.stageHours(cur.stages[0], H.aiTopic), 60, 'stageHours with a skip leaves the topic out');
}

/* ---- 3. content.js ---- */
{
  const win = { ZQ: { state: { settings: {} } } };
  const fetchStub = async (url) => {
    const f = path.join(CONTENT, String(url).replace(/^content\//, '').split('?')[0]);
    if (!fs.existsSync(f)) return { ok: false, status: 404, json: async () => null };
    return { ok: true, status: 200, json: async () => JSON.parse(fs.readFileSync(f, 'utf8')) };
  };
  const ctx = vm.createContext({ window: win, fetch: fetchStub, console, document: undefined, setTimeout, clearTimeout });
  for (const f of ['js/hours.js', 'js/content.js']) vm.runInContext(fs.readFileSync(path.join(APP, f), 'utf8'), ctx);
  await win.ZQ.content.ready;
  const C = win.ZQ.content, S = win.ZQ.state.settings;
  const ids = () => C.courses().map((c) => c.id), topics = () => C.stages().flatMap((s) => s.topics.map((t) => t.id));
  ok(C.course('ai-sample').strand === 'ai', 'course() reports strand "ai"');
  ok(C.topicStrand(C.topic('1.12')) === 'ai' && C.topicStrand(C.topic('1.8')) !== 'ai', 'a topic of ai courses has strand "ai"');
  const b = C.strandBadge('ai', C.course('ai-sample').strandNote);
  ok(/is-ai/.test(b) && />AI strand</.test(b) && /aria-label="AI strand\./.test(b), 'the badge reads "AI strand"', b);
  ok(ids().includes('ai-sample') && topics().includes('1.12'), 'shown by default');
  S.aiStrand = false; ok(!ids().includes('ai-sample') && !topics().includes('1.12'), 'the AI switch off hides the course and its topic');
  ok(C.course('ai-sample') && C.topic('1.12'), 'a hidden ai course is still found by id (links and resume points keep working)');
  S.aiStrand = true; S.quantOnly = true; ok(!ids().includes('ai-sample') && !topics().includes('1.12'), '"Quant path only" hides it too');
  ok(ids().includes('first-python'), '"Quant path only" keeps quant courses');
  S.quantOnly = false;
  const s1 = C.stages().find((s) => s.id === 1);
  ok(!C.pathTopics(s1).some((t) => t.id === '1.12') && C.pathTopics(s1).length === s1.topics.length - 1, 'the stage topic count leaves the ai topic out');
  const st = C.stage(1); const sum = st.topics.filter((t) => t.id !== '1.12').reduce((a, t) => a + t.hours, 0);
  near(st.hours, sum, 'the stage hours exclude the ai topic');
  near(st.hoursApp, st.topics.filter((t) => t.id !== '1.12').reduce((a, t) => a + t.hoursApp, 0), 'the stage in-app hours exclude it');
  const all = C.allCourses();
  ok(!C.readiness.plan(all, 'Undecided').some((c) => c.id === 'ai-sample'), 'Today\'s plan leaves ai out by default');
  S.aiToday = true; ok(C.readiness.plan(all, 'Undecided').some((c) => c.id === 'ai-sample'), 'Today\'s plan offers it once the learner opts in');
  S.aiStrand = false; ok(!C.aiToday(), 'the Today opt-in does nothing while the strand is hidden');
  S.aiStrand = true; S.aiToday = false;
  ok(!C.readiness.roleState('trader').levels.missing.some((m) => m.course === 'ai-sample'), 'role readiness never counts it');
}

/* ---- 4. census and curriculum-hours on a scratch root: figures unchanged, one AI line ---- */
{
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-strand-ai-'));
  const clone = (drop) => {
    fs.rmSync(path.join(root, 'app'), { recursive: true, force: true });
    fs.mkdirSync(path.join(root, 'app', 'tools'), { recursive: true });
    fs.cpSync(path.join(APP, 'js'), path.join(root, 'app', 'js'), { recursive: true });
    for (const f of ['census.mjs', 'curriculum-hours.mjs', 'hours-source.mjs']) fs.copyFileSync(path.join(TOOLS, f), path.join(root, 'app', 'tools', f));
    fs.cpSync(CONTENT, path.join(root, 'app', 'content'), { recursive: true });
    fs.mkdirSync(path.join(root, 'docs'), { recursive: true });
    if (drop) {
      const cf = path.join(root, 'app', 'content', 'curriculum.json'), c = rd(cf);
      c.stages.find((s) => s.id === 1).topics = c.stages.find((s) => s.id === 1).topics.filter((t) => t.id !== '1.12'); delete c.courses['ai-sample'];
      fs.writeFileSync(cf, JSON.stringify(c)); fs.rmSync(path.join(root, 'app', 'content', 'courses', 'ai-sample'), { recursive: true });
    }
  };
  const run = (f) => execFileSync('node', [path.join(root, 'app', 'tools', f)], { encoding: 'utf8' });
  clone(true); const cBaseAll = run('census.mjs'), hBase = run('curriculum-hours.mjs');
  clone(false); const cAi = run('census.mjs'), hAi = run('curriculum-hours.mjs');
  const aiLine = cAi.split('\n').filter((l) => /^AI strand/.test(l));
  ok(aiLine.length === 1 && /courses 1, topics 1/.test(aiLine[0]), 'census prints one AI line', aiLine.join('|'));
  ok(cAi.split('\n').filter((l) => !/^AI strand|Courses:|^  |Topics with no topic exam|Topic exams:|^Exams|Topic exam pass/.test(l)).join('\n').replace(/Stage 1:.*\n/, '') === cBaseAll.split('\n').filter((l) => !/^AI strand|Courses:|^  |Topics with no topic exam|Topic exams:|^Exams|Topic exam pass/.test(l)).join('\n').replace(/Stage 1:.*\n/, ''),
    'census totals, stage figures and hours are the same with and without the ai course');
  ok(/Stage 1: lessons \d+\/\d+ \(missing \d+\), courses (\d+)/.exec(cAi)[1] === /Stage 1: lessons \d+\/\d+ \(missing \d+\), courses (\d+)/.exec(cBaseAll)[1], 'the stage course count leaves the ai course out');
  ok(!/AI strand/.test(cBaseAll) && !/AI strand/.test(hBase), 'with no ai course neither tool prints an AI line');
  ok(/^AI strand \(optional/m.test(hAi) && (hAi.match(/^\| 1\. .*$/m) || [''])[0] === (hBase.match(/^\| 1\. .*$/m) || [''])[0], 'curriculum-hours: a stage row is the same, one AI line follows the table');
  ok(hAi.replace(/^AI strand.*\n\n/m, '').split('\n').filter((l) => !/^\| 1\.12|^\| \d/.test(l) || /^\| \d\. /.test(l)).join('\n') === hBase.split('\n').filter((l) => !/^\| 1\.12|^\| \d/.test(l) || /^\| \d\. /.test(l)).join('\n'), 'curriculum-hours: nothing else moves');
  fs.rmSync(root, { recursive: true, force: true });
}

console.log(`${fails ? 'FAIL' : 'PASS'}: ${n - fails}/${n} checks`);
process.exit(fails ? 1 : 0);
