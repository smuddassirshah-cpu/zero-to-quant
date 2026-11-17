#!/usr/bin/env node
/* Screen states test (docs/PLAN.md section 13, items 3, 4 and 6; docs/reports/definition-of-done-ai.md gaps 1, 2 and 4).
   1. Every route the router knows (the ids registered with ZQ.screen in js/screens/*, with real params) renders on an empty state and on a
      populated state, at 1280 x 860 and 440 x 956: no uncaught error, no console error other than blocked cdn.jsdelivr.net requests, and a
      non-empty #app. Empty: a fresh profile with setup finished (a route that needs setup is also visited on a truly empty profile and must
      land on #setup); #setup itself runs from truly empty. Populated: built by real use (one lesson, one level review and one problem set
      played through the ZQ.test hooks) plus the mutators for what play does not reach in a minute (an exam attempt with a miss, a fluency
      result, a redo item), so progress, XP, MP, streak, mastery, the redo queue, problem-set saves and exam attempts are all present.
   2. An unwritten lesson (tools/fixtures/mini-app, served as the app's content with a manifest the validator writes): the course map says
      "Not yet written" and its #lesson, #review and #homework routes show a card, not an error.
   3. Export, then import into a fresh browser context: the re-export deep-equals the first export (all keys), also after a reload, and a
      wrong version is refused without touching the state.
   Usage: node tools/test-screen-states.mjs [--local-cdn <dir>] [--only <text>]   Exit 0 when all pass, 1 on a failure, 2 on a setup problem. */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert';
import { execSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const CHROMIUM = '/opt/pw-browsers/chromium';
const argv = process.argv.slice(2);
const li = argv.indexOf('--local-cdn');
const localCdn = li >= 0 && argv[li + 1] && !argv[li + 1].startsWith('--') ? path.resolve(argv[li + 1]) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const oi = argv.indexOf('--only');
const only = oi >= 0 ? argv[oi + 1] : null;
const die = (m) => { console.error('test-screen-states: ' + m); process.exit(2); };
const T0 = Date.now();

const loadPlaywright = async () => {
  try { return await import('playwright'); } catch { /* not local */ }
  const roots = [];
  try { roots.push(execSync('npm root -g', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()); } catch { /* no npm */ }
  (process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).forEach(p => roots.push(p));
  for (const r of roots) { const f = path.join(r, 'playwright', 'index.mjs'); if (fs.existsSync(f)) return import(pathToFileURL(f).href); }
  die('Playwright is not installed (npm i -g playwright)');
};

/* A static server for app/, optionally with /content/ taken from another folder (the mini fixture) */
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2', '.ico': 'image/x-icon' };
const serve = (contentDir) => new Promise((resolve) => {
  const srv = http.createServer((req, res) => {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (p.endsWith('/')) p += 'index.html';
    const root = contentDir && p.startsWith('/content/') ? contentDir : APP;
    const f = path.join(root, contentDir && p.startsWith('/content/') ? p.slice('/content'.length) : p);
    if (!f.startsWith(root) || !fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'cache-control': 'no-cache' });
    res.end(fs.readFileSync(f));
  });
  srv.listen(0, '127.0.0.1', () => resolve({ base: `http://127.0.0.1:${srv.address().port}`, close: () => new Promise(r => srv.close(r)) }));
});
const cdnFile = (u) => {
  let m;
  if (!localCdn) return null;
  if ((m = u.pathname.match(/^\/pyodide\/v([\d.]+)\/full\/(.*)$/))) return path.join(localCdn, `pyodide-${m[1]}`, 'package', m[2]);
  if ((m = u.pathname.match(/^\/npm\/(@[^/]+\/[^@/]+|[^@/]+)@([^/]+)\/(.*)$/))) return path.join(localCdn, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package', m[3]);
  return null;
};
const CDN_MIME = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm' };

const VIEWPORTS = [['desktop', { width: 1280, height: 860 }], ['440', { width: 440, height: 956 }]];
const COURSE = 'number-sense', LESSON = 'l1-what-a-fraction-measures';

const main = async () => {
  const { chromium } = await loadPlaywright();
  const real = await serve(null);
  const browser = await chromium.launch();
  const fails = [];
  const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + String(detail).slice(0, 300)}`); if (!ok) fails.push(name); };
  const wanted = (name) => !only || name.includes(only);

  /* a fresh context (so a fresh localStorage), with the CDN served locally and the fonts stubbed; console errors and page errors collected */
  const open = async (base, viewport) => {
    const ctx = await browser.newContext({ viewport });
    await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
      if (!localCdn) return route.continue();   // CI: the real jsDelivr
      const f = cdnFile(new URL(route.request().url()));
      if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': CDN_MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
      return route.abort('blockedbyclient');
    });
    await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 200)));
    page.on('console', m => {
      if (m.type() !== 'error') return;
      const u = (m.location() && m.location().url) || '';
      if (/cdn\.jsdelivr\.net/.test(u) || /cdn\.jsdelivr\.net/.test(m.text())) return;   // blocked in a sandbox; not ours
      errors.push('console: ' + m.text().slice(0, 200));
    });
    page.on('requestfailed', r => { if (!/cdn\.jsdelivr\.net/.test(r.url())) errors.push('requestfailed: ' + r.url().slice(0, 120)); });
    const ready = async () => { await page.waitForFunction(() => window.ZQ && ZQ.state && ZQ.content && ZQ.content.resumeStands && document.querySelector('#app'), null, { timeout: 30000 }); await page.waitForTimeout(300); };
    await page.goto(base + '/#today');
    await ready();
    return { ctx, page, errors, ready };
  };
  /* go to a route and wait until #app has text that has stopped changing */
  const visit = async (page, route) => {
    await page.evaluate((r) => { delete window.ZQ.test; ZQ.go(r); }, route);
    let last = '', stable = 0;
    for (let i = 0; i < 100 && stable < 4; i++) {
      await page.waitForTimeout(100);
      const t = await page.evaluate(() => (document.querySelector('#app') || {}).innerText || '');
      if (t.length > 10 && t === last) stable++; else stable = 0;
      last = t;
    }
    return page.evaluate(() => ({ text: (document.querySelector('#app') || {}).innerText || '', hash: location.hash, cls: (document.querySelector('#app') || {}).className || '' }));
  };
  const setDone = (page) => page.evaluate(() => { ZQ.state.reset(); ZQ.state.flags.set({ setupDone: true }); ZQ.state.profile.set({ name: 'Test' }); ZQ.state.settings.set({ strictPrereqs: false }); });
  const play = async (page, route, limit = 120) => {
    await visit(page, route);
    let c = null;
    for (let i = 0; i < limit; i++) {
      c = await page.evaluate(async () => {
        const t = ZQ.test; if (!t) return { kind: 'none' };
        const c = t.current();
        if (c.kind === 'done') return { kind: 'done' };
        if (['read', 'ok', 'rev', 'qok', 'qno', 'done'].includes(c.state)) await t.continue();
        else { t.answerCorrect(); await t.check(); await t.continue(); }
        return { kind: c.kind };
      });
      if (c.kind === 'done' || c.kind === 'none') break;
      await page.waitForTimeout(60);
    }
    return c;
  };

  /* ---------- the populated state, by real use ---------- */
  const build = async () => {
    const { ctx, page, errors, ready } = await open(real.base, VIEWPORTS[0][1]);
    await setDone(page);
    const out = {};
    out.lesson = await play(page, `lesson/${COURSE}/${LESSON}`, 150);
    out.review = await play(page, `review/${COURSE}/review-1`, 60);
    out.problems = await play(page, `problems/${COURSE}/problems-1`, 60);
    await page.waitForTimeout(400);
    await page.evaluate(() => {
      const S = ZQ.state;
      S.examFinished({ id: 'topic-0.1', score: 6, items: 10, passed: false, bySkill: {}, results: [{ id: 'x1', ok: true, skills: [] }, { id: 'x2', ok: false, skills: [], difficulty: 3 }], seconds: 300 });
      const f = ZQ.content.fluencyList()[0];
      if (f) S.fluency.result({ course: f.course, id: f.id, right: 5, n: 8, passed: false, families: {} });
      S.redo.add({ id: 'scratch-redo', kind: 'screen', ref: { course: 'number-sense', lesson: 'l1-what-a-fraction-measures', screen: 1 }, skills: [], difficulty: 2 });
    });
    const text = await page.evaluate(() => ZQ.state.export());
    const d = JSON.parse(text);
    await ctx.close();
    out.doc = d; out.text = text; out.errors = errors;
    return out;
  };

  const b = await build();
  check('build: the lesson, the review and the problem set play to the end', b.lesson.kind === 'done' && b.review.kind === 'done' && b.problems.kind === 'done', JSON.stringify([b.lesson, b.review, b.problems]));
  const d = b.doc;
  const has = (v) => (Array.isArray(v) ? v.length > 0 : v && typeof v === 'object' ? Object.keys(v).length > 0 : !!v);
  const missing = ['lessons', 'reviews', 'problems', 'exams', 'redo', 'skills', 'xp', 'mp', 'hours', 'fluency'].filter(k => !has(d[k]));
  if (!(d.streak && d.streak.current >= 1)) missing.push('streak');
  check('build: the populated state holds progress, XP, MP, streak, mastery, redo, problem-set saves, exams, fluency', !missing.length, 'missing ' + missing.join(','));
  check('build: no console error while playing', !b.errors.length, b.errors.join(' | '));

  /* ---------- the route list: ids the router knows, with real params ---------- */
  const lists = await (async () => {
    const { ctx, page } = await open(real.base, VIEWPORTS[0][1]);
    const r = await page.evaluate(() => ({
      ids: ZQ.screens.map(s => s.id),
      drill: (ZQ.content.drills ? ZQ.content.drills() : []).map(x => x.id)[0] || null,
      fluency: (ZQ.content.fluencyList() || [])[0] || null,
      prep: (ZQ.content.prepPaths ? ZQ.content.prepPaths() : []).map(p => p.id),
    }));
    await ctx.close();
    return r;
  })();
  const routes = [
    ['setup'], ['today'], ['learn'], [`course/${COURSE}`], [`lesson/${COURSE}/${LESSON}`], ['review'], [`review/${COURSE}/review-1`],
    [`homework/${COURSE}/homework-1`], ['exam/topic-0.1'], ['exam/mock-oa-arith'], [`problems/${COURSE}/problems-1`], [`testout/${COURSE}/2`],
    ['redo'], ['bank'], ['practice'], ['practice/weekly'], ['weekly'], ['warmup'], ['you'], ['system'], ['prepare'], ['fluency-list'], ['drill'],
  ];
  if (lists.fluency) routes.push([`fluency/${lists.fluency.course}/${lists.fluency.id}`]);
  if (lists.drill) routes.push([`drill/${lists.drill}`]);
  (lists.prep || []).slice(0, 2).forEach(p => routes.push([`prepare/${p}`]));
  const covered = new Set(routes.map(r => r[0].split('/')[0]));
  const uncovered = lists.ids.filter(i => !covered.has(i));
  check('routes: every screen id the router registers has a route here', !uncovered.length, 'not covered: ' + uncovered.join(','));

  /* ---------- 1. empty and populated state, per route, per viewport ---------- */
  for (const [vn, vp] of VIEWPORTS) {
    for (const state of ['empty', 'populated']) {
      const { ctx, page, errors, ready } = await open(real.base, vp);
      const bad = [];
      for (const [route] of routes) {
        const mark = errors.length;
        if (state === 'empty') await setDone(page); else await page.evaluate((t) => { const r = ZQ.state.import(t); if (!r.ok) throw new Error(r.error); }, b.text);
        const r = await visit(page, route);
        const why = [];
        if (r.text.trim().length < 15) why.push('empty text');
        if (/This screen failed to render/.test(r.text)) why.push('screen failed: ' + r.text.slice(0, 120).replace(/\s+/g, ' '));
        if (errors.length > mark) why.push(...errors.slice(mark));
        if (why.length) bad.push(`#${route}: ${why.join('; ')}`);
      }
      check(`1. ${state} state, ${vn}: ${routes.length} routes render without error`, !bad.length, bad.join(' || '));
      await ctx.close();
    }
    /* a truly empty profile (setup not done): #setup renders, and every other route lands on it, with text */
    {
      const { ctx, page, errors } = await open(real.base, vp);
      const bad = [];
      for (const [route] of routes) {
        const mark = errors.length;
        await page.evaluate(() => ZQ.state.reset());
        const r = await visit(page, route);
        const why = [];
        if (r.text.trim().length < 15) why.push('empty text');
        if (route !== 'system' && !/^#setup/.test(r.hash)) why.push('did not land on #setup: ' + r.hash);
        if (/This screen failed to render/.test(r.text)) why.push('screen failed');
        if (errors.length > mark) why.push(...errors.slice(mark));
        if (why.length) bad.push(`#${route}: ${why.join('; ')}`);
      }
      check(`1. truly empty profile, ${vn}: #setup renders, and every route that needs setup lands on it`, !bad.length, bad.join(' || '));
      await ctx.close();
    }
  }

  /* ---------- 2. an unwritten lesson, on the mini fixture ---------- */
  if (wanted('unwritten') || !only) {
    const h = openHarness({ name: 'screen-states' });
    try {
      const v = h.validate([]);
      check('2. setup: the mini fixture validates with 0 errors and writes a manifest', v.code === 0 && fs.existsSync(h.path('content/manifest.json')), v.errors.join(' | '));
      const cj = JSON.parse(fs.readFileSync(h.path('content/courses/algo-think/course.json'), 'utf8'));
      const lessons = cj.levels.flatMap(l => l.lessons);
      const missingLesson = lessons.find(l => !fs.existsSync(h.path(`content/courses/algo-think/${l}.json`)));
      const lv = cj.levels.find(l => l.lessons.includes(missingLesson));
      const reviewMissing = cj.levels.map(l => l.review).find(r => r && !fs.existsSync(h.path(`content/courses/algo-think/${r}.json`)));
      const hwMissing = cj.levels.map(l => l.homework).find(r => r && !fs.existsSync(h.path(`content/courses/algo-think/${r}.json`)));
      check('2. setup: the fixture has an unwritten lesson, review and homework in algo-think', !!(missingLesson && reviewMissing && hwMissing), JSON.stringify([missingLesson, reviewMissing, hwMissing]));
      const mini = await serve(h.path('content'));
      try {
        for (const [vn, vp] of VIEWPORTS) {
          const { ctx, page, errors } = await open(mini.base, vp);
          await setDone(page);
          let r = await visit(page, 'course/algo-think');
          const nw = await page.evaluate(() => [...document.querySelectorAll('.zc-nwtag')].length);
          check(`2. ${vn}: the course map shows the unwritten lessons as "Not yet written"`, /Not yet written/.test(r.text) && nw > 0 && !errors.length, `${nw} tags; ${errors.join(' | ')}`);
          const nwFor = await page.evaluate((l) => { const e = document.querySelector(`[data-lesson="${l}"], [href$="/${l}"], [data-go$="/${l}"]`); return e ? e.textContent : null; }, missingLesson);
          if (nwFor != null) check(`2. ${vn}: the row of ${missingLesson} says "Not yet written"`, /Not yet written/.test(nwFor), nwFor.slice(0, 100));
          for (const route of [`lesson/algo-think/${missingLesson}`, `review/algo-think/${reviewMissing}`, `homework/algo-think/${hwMissing}`, 'learn', 'today']) {
            const mark = errors.length;
            r = await visit(page, route);
            const card = /lesson|review|homework/.test(route.split('/')[0]) ? /Not yet written|not ready|not been written/i.test(r.text) : r.text.trim().length > 15;
            check(`2. ${vn}: #${route} shows ${/lesson|review|homework/.test(route.split('/')[0]) ? 'a "not written" card' : 'its screen'}, no error`, card && !/failed to render/.test(r.text) && errors.length === mark, r.text.slice(0, 100).replace(/\s+/g, ' ') + ' ' + errors.slice(mark).join(' | '));
          }
          await ctx.close();
        }
      } finally { await mini.close(); }
      void lv;
    } finally { h.close(); }
  }

  /* ---------- 3. export, import into a fresh context, deep-equal ---------- */
  if (wanted('round') || wanted('import') || !only) {
    const { ctx, page } = await open(real.base, VIEWPORTS[0][1]);
    const before = await page.evaluate(() => ZQ.state.export());
    check('3. a fresh context starts empty', JSON.parse(before).xp === 0 && !Object.keys(JSON.parse(before).lessons).length);
    const res = await page.evaluate((t) => ZQ.state.import(t), b.text);
    const after = await page.evaluate(() => ZQ.state.export());
    const eq = (x, y) => { try { assert.deepStrictEqual(JSON.parse(x), JSON.parse(y)); return ''; } catch (e) { return String(e.message).slice(0, 400); } };
    check('3. import accepted the export', res.ok === true, JSON.stringify(res));
    check('3. the export after import deep-equals the first export (every key)', !eq(b.text, after), eq(b.text, after));
    await page.reload();
    await page.waitForFunction(() => window.ZQ && ZQ.state, null, { timeout: 30000 });
    await page.waitForTimeout(800);
    const reloaded = await page.evaluate(() => ZQ.state.export());
    check('3. after a reload the saved state still deep-equals it', !eq(b.text, reloaded), eq(b.text, reloaded));
    const bad = await page.evaluate((t) => { const o = JSON.parse(t); o.v = 999; return ZQ.state.import(JSON.stringify(o)); }, b.text);
    const kept = await page.evaluate(() => ZQ.state.export());
    check('3. a wrong version is refused and the state is untouched', bad.ok === false && !eq(b.text, kept), JSON.stringify(bad));
    const junk = await page.evaluate(() => ZQ.state.import('{not json'));
    check('3. a file that is not JSON is refused', junk.ok === false);
    await ctx.close();
  }

  await browser.close();
  await real.close();
  const secs = Math.round((Date.now() - T0) / 1000);
  console.log(`${fails.length ? 'FAIL' : 'PASS'}: ${fails.length} failed, ${secs} s`);
  process.exit(fails.length ? 1 : 0);
};
main().catch(e => { console.error(e); process.exit(2); });
