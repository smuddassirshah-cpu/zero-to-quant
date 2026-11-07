#!/usr/bin/env node
/* DOM test of the tested-out resume rule (ENGINE-BACKLOG 461, 617). After a topic exam is passed, a half-finished lesson of that topic
   must not stay on Today. A resume save that is not a deliberate reopen-and-answer after the pass (leaving a lesson that was only
   reopened, the browser Back button, a reload on a lesson route) must not revive it. Reopening from Learn and answering does.
   Checks, on topic 0.1 (number-sense lesson 1) with the pass written the way the exam screen writes it (ZQ.state.examFinished):
     1. a part-open lesson is on Today before the pass and hidden after it;
     2. reopening the lesson after the pass and only leaving it (no answer) keeps it hidden;
     3. a reload keeps it hidden, and reloading on the lesson route then leaving keeps it hidden;
     3c. a stale resume saved after the pass by the old code (no pickedAt) is skipped;
     4. opening the lesson from the course map (the Learn path) after the pass, then leaving, shows it again, and it survives a reload.
   Usage: node tools/test-today-tested-out.mjs [--mobile] [--local-cdn <dir>]   Exit 0 when all pass, 1 on a failure, 2 on a setup problem. */
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const CHROMIUM = '/opt/pw-browsers/chromium';
const argv = process.argv.slice(2);
const mobile = argv.includes('--mobile');
const li = argv.indexOf('--local-cdn');
const localCdn = li >= 0 && argv[li + 1] && !argv[li + 1].startsWith('--') ? path.resolve(argv[li + 1]) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const die = (m) => { console.error('test-today-tested-out: ' + m); process.exit(2); };

const loadPlaywright = async () => {
  try { return await import('playwright'); } catch { /* not local */ }
  const roots = [];
  try { roots.push(execSync('npm root -g', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()); } catch { /* no npm */ }
  (process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).forEach(p => roots.push(p));
  for (const r of roots) { const f = path.join(r, 'playwright', 'index.mjs'); if (fs.existsSync(f)) return import(pathToFileURL(f).href); }
  die('Playwright is not installed (npm i -g playwright)');
};
const freePort = () => new Promise((res, rej) => { const s = net.createServer(); s.unref(); s.on('error', rej); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); });
const MIME = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm' };
const cdnFile = (u) => {
  let m;
  if (!localCdn) return null;
  if ((m = u.pathname.match(/^\/pyodide\/v([\d.]+)\/full\/(.*)$/))) return path.join(localCdn, `pyodide-${m[1]}`, 'package', m[2]);
  if ((m = u.pathname.match(/^\/npm\/(@[^/]+\/[^@/]+|[^@/]+)@([^/]+)\/(.*)$/))) return path.join(localCdn, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package', m[3]);
  return null;
};

const main = async () => {
  const { chromium } = await loadPlaywright();
  const port = await freePort();
  const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', APP], { stdio: 'ignore' });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i++) { try { if ((await fetch(base + '/index.html')).ok) break; } catch { /* not up */ } await new Promise(r => setTimeout(r, 100)); }
  const browser = await chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
  const fails = [];
  const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails.push(name); };
  const COURSE = 'number-sense', LESSON = 'l1-what-a-fraction-measures';
  try {
    const ctx = await browser.newContext({ viewport: mobile ? { width: 440, height: 956 } : { width: 1280, height: 860 } });
    if (localCdn) {
      await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
        const f = cdnFile(new URL(route.request().url()));
        if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
        return route.fulfill({ status: 404, body: '' });
      });
    }
    await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
    const page = await ctx.newPage();
    page.on('pageerror', e => console.log('pageerror', String(e).slice(0, 160)));
    const ready = async () => { await page.waitForFunction(() => window.ZQ && ZQ.state && ZQ.content && ZQ.content.resumeStands, null, { timeout: 30000 }); await page.waitForTimeout(500); };
    const sleep = (ms) => page.waitForTimeout(ms);
    const go = async (h) => { await page.evaluate((x) => { delete window.ZQ.test; location.hash = x; }, h); await sleep(900); };
    const reload = async () => { await page.reload(); await ready(); await sleep(500); };
    /* what Today does with the saved resume: whether it stands, and whether the card offers "Continue lesson" */
    const today = async () => {
      await go('today'); await sleep(600);
      return page.evaluate(() => {
        const r = ZQ.state.summary().resume, el = document.querySelector('[data-resume]');
        return { stands: !!r && ZQ.content.resumeStands(r), resumeCourse: r && r.course, cont: !!el && /Continue lesson/.test(el.textContent) };
      });
    };
    /* one move in the real player: read on, or answer correctly and continue */
    const step = () => page.evaluate(async () => { const t = ZQ.test; if (!t) return; const c = t.current(); if (['read', 'ok', 'rev'].includes(c.state)) await t.continue(); else { t.answerCorrect(); await t.check(); await t.continue(); } });

    await page.goto(base + '/#today');
    await ready();
    await page.evaluate(() => {
      const d = JSON.parse(ZQ.state.export());
      d.lessons = {}; d.reviews = {}; d.homework = {}; d.exams = {}; d.redo = [];
      d.prereq = { met: {}, testouts: {}, opened: {}, grandfathered: true };
      d.settings.strictPrereqs = false; d.flags.setupDone = true;
      return ZQ.state.import(d);
    });
    await reload();
    /* a part-open lesson through the real player: go forward a few screens, then leave by the route */
    await go(`lesson/${COURSE}/${LESSON}`);
    for (let i = 0; i < 4; i++) { await step(); await sleep(250); }
    await go('today'); await sleep(300);
    const before = await page.evaluate(() => { const r = ZQ.state.summary().resume; return r ? { course: r.course, lesson: r.lesson } : null; });
    check('setup: a position is saved in the lesson', !!before && before.course === COURSE && before.lesson === LESSON, JSON.stringify(before));
    const t0 = await today();
    check('before the pass the lesson stands on Today', t0.stands && t0.resumeCourse === COURSE && t0.cont, JSON.stringify(t0));

    await sleep(300);
    /* the pass, as the exam screen writes it */
    const passed = await page.evaluate(() => { ZQ.state.examFinished({ id: 'topic-0.1', score: 9, items: 10, passed: true, bySkill: {} }); return ZQ.content.topicPassed('0.1'); });
    check('setup: topic 0.1 reads as passed', passed === true);
    const t1 = await today();
    check('1. after the pass the part-open lesson is not the resume', !t1.stands && !t1.cont, JSON.stringify(t1));

    /* 2: reopened (Back button, a link) and left without an answer */
    await sleep(300);
    await go(`lesson/${COURSE}/${LESSON}`); await sleep(500);
    const t2 = await today();
    check('2. reopening and leaving without an answer keeps it hidden', !t2.stands && !t2.cont, JSON.stringify(t2));

    /* 3: reload, and a reload on the lesson route then leaving */
    await reload();
    const t3 = await today();
    check('3a. a reload keeps it hidden', !t3.stands && !t3.cont, JSON.stringify(t3));
    await go(`lesson/${COURSE}/${LESSON}`); await sleep(300);
    await reload(); await sleep(500);
    const t3b = await today();
    check('3b. a reload on the lesson route then leaving keeps it hidden', !t3b.stands && !t3b.cont, JSON.stringify(t3b));

    /* 1b: a record the old code left behind: saved after the pass, no pickedAt */
    await sleep(300);
    const stale = await page.evaluate(([c, l]) => { const pos = ZQ.state.lessonPosition.get(c, l); ZQ.state.lessonPosition.set(c, l, pos); const r = ZQ.state.summary().resume; return { at: r && r.at, picked: r && r.pickedAt, passAt: ZQ.content.examPassedAt('topic-0.1') }; }, [COURSE, LESSON]);
    check('setup: a stale resume saved after the pass has no pickedAt', stale.at > stale.passAt && !stale.picked, JSON.stringify(stale));
    const t1b = await today();
    check('1b. a stale resume saved after the pass (old code, no pickedAt) is skipped', !t1b.stands && !t1b.cont, JSON.stringify(t1b));

    /* 4: opened on purpose from the course map (the Learn path), then left without answering */
    await sleep(300);
    await go(`course/${COURSE}`);
    const node = `.zc-node[data-id="${LESSON}"]`;
    await page.waitForSelector(node, { timeout: 10000 });
    await page.evaluate((s) => document.querySelector(s).scrollIntoView({ block: 'center' }), node);
    await page.click(`${node} .zc-pw, ${node}`, { timeout: 5000 }).catch(async () => { await page.evaluate((s) => document.querySelector(s).click(), node); });
    await sleep(500);
    await page.evaluate(() => { const b = document.querySelector('.zc-pop:not([hidden]) [data-act], .sheet [data-act], .zc-sheet [data-act]'); if (b) b.click(); });
    await sleep(900);
    check('setup: the map opened the lesson', await page.evaluate((l) => location.hash.includes(l), LESSON));
    const t4 = await today();
    check('4. opened from the map after the pass, then left without an answer, it shows again', t4.stands && t4.resumeCourse === COURSE && t4.cont, JSON.stringify(t4));
    await reload();
    const t4b = await today();
    check('4b. and it survives a reload', t4b.stands && t4b.cont, JSON.stringify(t4b));
  } catch (e) {
    check('no exception', false, String(e && e.stack || e).split('\n').slice(0, 3).join(' | '));
  }
  await browser.close();
  proc.kill();
  console.log(fails.length ? `${fails.length} failed` : 'all passed');
  process.exit(fails.length ? 1 : 0);
};
main().catch(e => { console.error(e); process.exit(2); });
