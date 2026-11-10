#!/usr/bin/env node
/* Runtime tests for level problem sets (ENGINE-BACKLOG 845 to 851; author side docs/AUTHORING.md section 5), in the pattern of tools/test-fluency.mjs.
     Part A (plain node, a fake window and the real js/state.js, content.js, prereq.js, arith.js, gen.js, select.js, hours.js, with the real content read through a fake fetch):
             the loader and registry (problemsFor, problemsList, the default 40 minutes), the save (ZQ.state.problems.finished: the homework-scale XP on the first
             finish only, part credit counted in items, a partial attempt is no attempt, nothing else moves: reviews, homework, met levels, the redo queue, the
             performance record), the lock (a problem set is held by its level), the hours (in-app minutes count the set, the stored hours and the census figure
             do not), and the weekly review's pool (met levels only, an item with parts in the right shape, long-form and code parts left out, a miss queued
             and resolved again from its ref).
     Part B (Playwright, Chromium; needs --local-cdn for the maths grader): the weekly review's problem-set items played in the real set player: every part
             graded with its own feedback, an item with parts right only when every part is, the result recorded by weeklyFinish.
   Usage: node tools/test-problems.mjs [--local-cdn <pkgs>] [--unit-only]
   Exit 0 pass, 1 failure, 2 setup problem. */
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';
import { spawn, execSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);
const val = (k) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : null; };
const localCdn = val('--local-cdn') ? path.resolve(val('--local-cdn')) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const unitOnly = argv.includes('--unit-only');
const CHROMIUM = '/opt/pw-browsers/chromium';
const fixture = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/problems/problems-fixture-3.json'), 'utf8'));
const results = [];
const fails = [];
const record = (name, ok, detail = '') => { results.push(ok); if (!ok) fails.push(name); console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : ': ' + detail}`); };
const eq = (a, b, m) => { if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error(`${m || 'value'}: expected ${JSON.stringify(b)}, got ${JSON.stringify(a)}`); };
const ok = (c, m) => { if (!c) throw new Error(m || 'assertion failed'); };

/* ---------- Part A ---------- */
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
for (const f of ['hours.js', 'state.js', 'content.js', 'prereq.js', 'engine/arith.js', 'engine/gen.js', 'engine/select.js']) vm.runInThisContext(fs.readFileSync(path.join(APP, 'js', f), 'utf8'), { filename: f });
const { state: S, content: C, select: SEL, prereq: P } = globalThis.ZQ;
await C.ready;
const reg = (doc = fixture) => { C._setProblems([]); C._addProblems([{ course: doc.course, doc }]); };
const test = async (name, fn) => {
  store.clear(); S._reload(); S._setClock(null); C._setProblems([]); C._setFluency([]);   // no real Fluency set: its generated items would fill the review before the unseen pool (ENGINE-BACKLOG 835)
  try { await fn(); record(name, true); } catch (e) { record(name, false, e && e.message ? e.message : String(e)); }
};
const partsOf = (it) => it.parts.length;
const snap = () => JSON.stringify({ reviews: S.reviews, homework: S.homework, met: S.prereq.get().met, redo: S.redo.list(), perf: S.perf.get() });
const results4 = (list) => list.map((it, j) => ({ id: it.id, ok: true, difficulty: it.difficulty, skills: it.skills, ref: { course: 'equations', lesson: 'problems-3', item: it.id } }));

await test('A: the registry lists a problem set by level, with 40 minutes where the file states none', async () => {
  eq(C.problemsFor('equations', 3), null, 'no file, no set');
  C._addProblems([{ course: 'equations', doc: fixture }]);
  const row = C.problemsFor('equations', 3);
  ok(row && row.id === 'problems-3' && row.level === 3 && row.items === 3 && row.minutes === 30, JSON.stringify(row));
  const bare = JSON.parse(JSON.stringify(fixture)); delete bare.minutes; bare.level = 2; bare.id = 'problems-2';
  C._addProblems([{ course: 'equations', doc: bare }]);
  eq(C.problemsFor('equations', 2).minutes, 40, 'the default allowance');
  eq(C.problemsList().length, 2);
  eq(C.problemsFor('equations', 1), null, 'a level with no set has none');
  const doc = await C.problems('equations', 'problems-3');
  eq(doc.items.length, 3); doc.items.length = 0;
  eq((await C.problems('equations', 'problems-3')).items.length, 3, 'the registered document is copied, never shared');
  eq(await C.problems('equations', 'problems-1'), null);
});
await test('A: a problem set is held by its level, so it locks and unlocks with the level', () => {
  const lv = P.levelHolding('equations', 'problems-3');
  ok(lv && lv.n === 3, 'levelHolding finds level 3');
  eq(P.levelHolding('equations', 'problems-9'), null, 'a level that is not on the map holds nothing');
  eq(P.itemLocked('equations', 'problems-3'), P.levelLocked('equations', 3), 'locked exactly when the level is');
});
await test('A: the first finish earns the homework scale (50 and 5 an item right), a repeat earns none', () => {
  const list = fixture.items, rows = results4(list);
  const a = S.problems.finished({ course: 'equations', id: 'problems-3', results: rows, items: 3, seconds: 600 });
  eq(a.xp, 50 + 5 * 3, 'XP on the first finish'); eq(S.xp, 65);
  eq(a.record.attempts, 1); eq(a.record.best, 3); eq(a.record.n, 3);
  const b = S.problems.finished({ course: 'equations', id: 'problems-3', results: rows, items: 3, seconds: 600 });
  eq(b.xp, 0, 'no XP on a repeat'); eq(S.xp, 65); eq(b.record.attempts, 2);
  eq(S.rules.XP.homework, 50, 'the scale is the homework one'); eq(S.rules.XP.homeworkItem, 5);
  ok(S.mp > 0, 'the first finish earns mastery points as a homework does');
  const mp = S.mp;
  S.problems.finished({ course: 'equations', id: 'problems-3', results: rows, items: 3 });
  eq(S.mp, mp, 'a repeat adds no mastery points');
});
await test('A: part credit is counted in items; best keeps the highest; a miss earns no item XP', () => {
  const rows = results4(fixture.items);
  rows[0] = { ...rows[0], ok: false, credit: 2 / 3 };   // 2 of 3 parts right: not right, credit two thirds
  rows[1] = { ...rows[1], ok: false, credit: 1 / 3 };
  const a = S.problems.finished({ course: 'equations', id: 'problems-3', results: rows, items: 3 });
  eq(a.record.lastScore, 2, 'one item and two thirds and a third of an item: 1 + 0.7 + 0.3, to one place');
  eq(a.xp, 50 + 5 * 1, 'only the item right earns item XP');
  const b = S.problems.finished({ course: 'equations', id: 'problems-3', results: results4(fixture.items), items: 3 });
  eq(b.record.best, 3); eq(b.record.lastScore, 3);
  const c = S.problems.finished({ course: 'equations', id: 'problems-3', results: rows, items: 3 });
  eq(c.record.best, 3, 'a worse attempt leaves the best');
  eq(S.problems.get('equations', 'problems-3').attempts, 3);
  eq(S.problems.get('equations', 'problems-9'), null);
});
await test('A: a partial attempt is not an attempt and earns nothing', () => {
  const a = S.problems.finished({ course: 'equations', id: 'problems-3', results: [], items: 3, seconds: 120, partial: true });
  eq(a.xp, 0); eq(a.record.attempts, 0); eq(S.xp, 0);
  const b = S.problems.finished({ course: 'equations', id: 'problems-3', results: results4(fixture.items), items: 3 });
  eq(b.xp, 65, 'the first real finish still earns the first-finish XP');
});
await test('A: nothing else moves: reviews, homework, met levels, the redo queue and the performance record', () => {
  const before = snap();
  const rows = results4(fixture.items); rows[2].ok = false;
  S.problems.finished({ course: 'equations', id: 'problems-3', results: rows, items: 3 });
  eq(snap(), before);
  eq(S.redo.list().length, 0, 'a miss joins no redo queue');
});
await test('A: the save survives export and import, and an old save with no problems block loads', () => {
  S.problems.finished({ course: 'equations', id: 'problems-3', results: results4(fixture.items), items: 3 });
  const text = S.export(); S.reset(); S.import(text);
  eq(S.problems.get('equations', 'problems-3').attempts, 1);
  const d = JSON.parse(S.export()); delete d.problems; S.import(JSON.stringify(d));
  eq(S.problems.get('equations', 'problems-3'), null); eq(Object.keys(S.problems.list()).length, 0);
  S.problems.finished({ course: 'equations', id: 'problems-3', results: results4(fixture.items), items: 3 });
  eq(S.problems.get('equations', 'problems-3').attempts, 1);
});

/* the hours: in-app minutes count the set; the stored hours, and so the census figure, do not */
const { loadHours } = await import('./hours-source.mjs');
await test('A: in-app hours count the set (stated minutes, else 40); stored hours do not move', () => {
  const { hours, cur } = loadHours(path.join(APP, 'content'));
  const cid = 'equations';
  const mk = (problemsMinutes) => hours.build({ curriculum: cur, courses: Object.fromEntries(Object.keys(JSON.parse(fs.readFileSync(path.join(APP, 'content/curriculum.json'), 'utf8')).courses).map((c) => [c, JSON.parse(fs.readFileSync(path.join(APP, 'content/courses', c, 'course.json'), 'utf8'))])), written: () => true, sessions: {}, minutes: (c, l) => { try { return JSON.parse(fs.readFileSync(path.join(APP, 'content/courses', c, l + '.json'), 'utf8')).minutes; } catch { return undefined; } }, setMinutes: {}, examMinutes: {}, problemsMinutes });
  const none = mk({}), withSet = mk({ 'equations/problems-3': 30 }), dflt = mk({ 'equations/problems-3': hours.PROBLEMS_MIN });
  eq(hours.PROBLEMS_MIN, 40, 'the allowance is 40');
  const near = (a, b) => Math.abs(a - b) < 1e-9;
  ok(near(withSet.levelApp(cid, 3) - none.levelApp(cid, 3), 30 / 60), 'the level gains the stated minutes');
  ok(near(dflt.levelApp(cid, 3) - none.levelApp(cid, 3), 40 / 60), 'the default is 40 minutes');
  ok(near(withSet.levelApp(cid, 2), none.levelApp(cid, 2)), 'a level with no set gains nothing');
  ok(near(withSet.courseApp(cid) - none.courseApp(cid), 0.5), 'the course gains the same');
  const tid = JSON.parse(fs.readFileSync(path.join(APP, 'content/courses/equations/course.json'), 'utf8')).topic;
  ok(near(withSet.topicApp(tid) - none.topicApp(tid), 0.5), 'the topic gains the same');
  eq(withSet.topic(tid), none.topic(tid), 'the stored topic hours are unchanged');
  eq(withSet.course(cid), none.course(cid), 'the stored course hours are unchanged');
  eq(withSet.total(), none.total(), 'the stored total is unchanged');
  ok(withSet.topicOut(tid) <= none.topicOut(tid) + 1e-9, 'outside hours can only fall');
});

/* the weekly review's pool */
const metEq = () => S.prereq.mark(['equations/L3'], 'test');
await test('A: problem-set items of a met level join the weekly review; an unmet level adds none', async () => {
  reg();
  const none = await SEL.weeklyReview({ n: 60, seed: 5 });
  eq(none.length, 0, 'no level met, nothing drawn');
  metEq();
  const items = await SEL.weeklyReview({ n: 80, seed: 5 });
  const mine = items.filter((it) => String(it.uid).startsWith('equations/problems-3/'));
  eq(mine.length, 3, 'all three problems are in the pool of a met level');
  ok(mine.every((it) => it.weekly && it.weekly.tier === 2 && it.weekly.course === 'equations' && it.weekly.n === 3), 'unseen authored items of that level');
  ok(mine.every((it) => Array.isArray(it.parts) && it.parts.length === 3 && !it.widget && it.skills.length && it.ref.lesson === 'problems-3' && it.source.includes('problem set')), 'each keeps its parts, skills, ref and source');
  eq(partsOf(mine[0]), 3);
});
await test('A: a problem-set item already served by a weekly review is not drawn again; the others still are', async () => {
  reg(); metEq();
  const first = (await SEL.weeklyReview({ n: 80, seed: 6 })).filter((it) => String(it.uid).startsWith('equations/problems-3/'));
  eq(first.length, 3);
  const res = first.map(() => ({ ok: true }));
  SEL.weeklyFinish(first, res);
  const again = (await SEL.weeklyReview({ n: 80, seed: 7 })).filter((it) => String(it.uid).startsWith('equations/problems-3/') && it.weekly.tier === 2);
  eq(again.length, 0, 'served items leave the unseen pool');
});
await test('A: a code or long-form part keeps the item out of the weekly review, as everywhere', async () => {
  const doc = JSON.parse(JSON.stringify(fixture));
  doc.items[1].parts[2].widget = { kind: 'code', language: 'python', starter: 'x', tests: [], solution: 'x' };
  reg(doc); metEq();
  const mine = (await SEL.weeklyReview({ n: 80, seed: 8 })).filter((it) => String(it.uid).startsWith('equations/problems-3/'));
  eq(mine.map((it) => it.id).sort(), ['pf-phone', 'pf-plumber']);
});
await test('A: a missed problem-set item joins the redo queue and resolves again from its ref, with its parts', async () => {
  reg(); metEq();
  const items = (await SEL.weeklyReview({ n: 80, seed: 9 })).filter((it) => String(it.uid).startsWith('equations/problems-3/'));
  const res = items.map((it, j) => ({ ok: j !== 1 }));
  const r = SEL.weeklyFinish(items, res);
  eq(r.queued, 1);
  const q = S.redo.list();
  eq(q.length, 1); eq(q[0].ref.lesson, 'problems-3'); eq(q[0].ref.course, 'equations');
  const back = await SEL.resolve(q[0].ref, q[0].kind);
  ok(back && Array.isArray(back.parts) && back.parts.length === 3 && back.uid === q[0].id, 'the redo session finds the item with its parts');
  ok(/problem set/.test(SEL.source(q[0].ref)), `its source reads "${SEL.source(q[0].ref)}"`);
  const session = await SEL.redoSession();
  eq(session.length, 0, 'nothing is due the same day');
  const inDays = Date.now() + 8 * 86400000; S._setClock(() => inDays);
  const due = await SEL.redoSession();
  eq(due.length, 1); ok(due[0].parts && due[0].redo, 'due after seven days, as a playable item with parts');
});

/* ---------- Part B ---------- */
const loadPlaywright = async () => {
  try { return await import('playwright'); } catch { /* not local */ }
  const roots = [];
  try { roots.push(execSync('npm root -g', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()); } catch { /* no npm */ }
  (process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).forEach((p) => roots.push(p));
  for (const r of roots) { const f = path.join(r, 'playwright', 'index.mjs'); if (fs.existsSync(f)) return import(pathToFileURL(f).href); }
  console.error('test-problems: Playwright is not installed (npm i -g playwright)'); process.exit(2);
};
const freePort = () => new Promise((res, rej) => { const s = net.createServer(); s.unref(); s.on('error', rej); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); });
const MIME = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm' };
const cdnFile = (u) => { let m; if ((m = u.pathname.match(/^\/npm\/(@[^/]+\/[^@/]+|[^@/]+)@([^/]+)\/(.*)$/))) return path.join(localCdn, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package', m[3]); return null; };

const browser = async () => {
  const { chromium } = await loadPlaywright();
  const port = await freePort();
  const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', APP], { stdio: 'ignore' });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i++) { try { if ((await fetch(base + '/index.html')).ok) break; } catch { /* not up */ } await new Promise((r) => setTimeout(r, 100)); }
  const b = await chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
  try {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 860 } });
    await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
      const f = cdnFile(new URL(route.request().url()));
      if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
      return route.fulfill({ status: 404, body: '' });
    });
    await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, (r) => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
    const page = await ctx.newPage();
    page.on('pageerror', (e) => record('B: no uncaught error in the page', false, String(e).slice(0, 200)));
    await page.goto(base + '/#today');
    await page.waitForFunction(() => window.ZQ && ZQ.widgets && ZQ.grade && ZQ.player && ZQ.select, null, { timeout: 30000 });
    await page.evaluate(() => ZQ.content.ready);
    await page.evaluate((d) => { ZQ.content._setFluency([]); ZQ.content._setProblems([]); ZQ.content._addProblems([{ course: d.course, doc: d }]); ZQ.state.prereq.mark(['equations/L3'], 'test'); }, fixture);
    const run = async (wrongFirst) => page.evaluate(async (wrong) => {
      const all = await ZQ.select.weeklyReview({ n: 80, seed: 11 });
      const items = all.filter((it) => String(it.uid).startsWith('equations/problems-3/'));
      if (!items.length) return { error: 'no problem-set item in the weekly review' };
      const host = document.createElement('div'); document.body.appendChild(host);
      let done = null;
      const set = ZQ.player.runSet(host, { title: 'Weekly review', items, mode: 'set', track: 'maths', onDone: (r) => { done = r; } });
      const log = [];
      for (let guard = 0; guard < 80 && !done; guard++) {
        const c = ZQ.test.current();
        if (c.kind === 'done') break;
        if (c.state === 'idle' || c.state === 'engaged') {
          const missThis = wrong && c.screenIndex === 0 && c.part === 0;
          const applied = missThis ? ZQ.test.answerWrong() : ZQ.test.answerCorrect();
          const r = await ZQ.test.check();
          log.push({ item: c.screenIndex, part: c.part, parts: c.parts, applied, ok: r ? !!r.ok : null, text: (document.querySelector('.lsn-verdict') || {}).innerText || '' });
        }
        await ZQ.test.continue();
        await new Promise((r) => setTimeout(r, 60));
      }
      const res = set.results ? set.results() : [];
      const fin = ZQ.select.weeklyFinish(items, res);
      set.destroy(); host.remove();
      return { n: items.length, log, res: res.map((r) => (r ? { ok: !!r.ok, credit: r.credit, right: r.right, of: r.of } : null)), fin: { right: fin.right, authored: fin.authored, queued: fin.queued }, seen: Object.keys(ZQ.state.cumulative.seen()).filter((u) => u.startsWith('equations/problems-3/')).length, redo: ZQ.state.redo.list().map((x) => x.ref.lesson) };
    }, wrongFirst);
    const maths = await page.evaluate(() => ZQ.grade.maths().then((m) => !!(m && m.ce && m.mathlive)));
    if (!maths) { console.log('note: the Compute Engine or MathLive did not load (give --local-cdn <pkgs>); the expression part cannot be graded, so part B is skipped'); return; }
    const a = await run(true);
    if (a.error) record('B: the weekly review plays a problem set in the real player', false, a.error);
    else {
      record('B: every part of each problem is asked in turn (3 problems, 3 parts each)', a.log.length === 9 && a.log.every((x) => x.parts === 3), JSON.stringify(a.log.map((x) => [x.item, x.part])));
      const first = a.log[0];
      record('B: a wrong first part is graded wrong and shows its own feedback', first && first.applied && first.ok === false && first.text.length > 12, JSON.stringify(first));
      record('B: the next part still opens and grades on its own', a.log[1] && a.log[1].ok === true && a.log[1].part === 1, JSON.stringify(a.log[1]));
      record('B: the problem with a wrong part is not right and carries its part credit', a.res[0] && a.res[0].ok === false && Math.abs(a.res[0].credit - 2 / 3) < 1e-9 && a.res[0].right === 2 && a.res[0].of === 3, JSON.stringify(a.res[0]));
      record('B: the other problems are right', a.res.slice(1).every((r) => r && r.ok), JSON.stringify(a.res));
      record('B: weeklyFinish records the three problems, queues the miss once and remembers all three', a.fin.authored === 3 && a.fin.right === 2 && a.fin.queued === 1 && a.seen === 3 && a.redo.length === 1 && a.redo[0] === 'problems-3', JSON.stringify(a));
    }
    await page.evaluate(() => { ZQ.state.cumulative.record({ score: 0, n: 0, seen: [] }); const d = ZQ.state.doc.cumulative; d.seen = {}; ZQ.state.doc.redo.length = 0; });
    const c = await run(false);
    record('B: with every part right all three problems are right and the weekly review counts them', !c.error && c.res.every((r) => r && r.ok && r.credit === 1) && c.fin.right === 3 && c.fin.queued === 0, JSON.stringify(c));
    await ctx.close();
  } finally { await b.close(); proc.kill(); }
};

if (!unitOnly) {
  if (!localCdn || !fs.existsSync(path.join(localCdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'))) console.log('note: no local Compute Engine (give --local-cdn <pkgs>); part B is skipped if the maths grader cannot load');
  try { await browser(); } catch (e) { console.error(e); record('B: the browser part ran', false, String(e.message || e).split('\n')[0]); }
}
const bad = results.filter((x) => !x).length;
console.log(`test-problems: ${results.length - bad}/${results.length} passed${bad ? `, ${bad} FAILED` : ''}`);
process.exit(bad ? 1 : 0);
