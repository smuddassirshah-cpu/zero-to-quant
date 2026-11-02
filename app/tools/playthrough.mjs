#!/usr/bin/env node
/* Playthrough (docs/PLAN.md section 11): plays every written lesson with its authored answers, then opens every
   other route once, and fails on any check that is not correct, any lesson that does not reach its completion
   screen, and any console error. With --sets it also plays every written level review and homework, and with
   --exams every exam, through the set-mode test hook (window.ZQ.test), answering each item correctly.

   Usage (from the repository root or anywhere):
     node app/tools/playthrough.mjs                        every written lesson, then every route
     node app/tools/playthrough.mjs --all                  lessons, routes, every review and homework, every exam
     node app/tools/playthrough.mjs --sets                 every written level review and homework only
     node app/tools/playthrough.mjs --exams                every exam in content/exams only (combine with --sets)
     node app/tools/playthrough.mjs --set number-sense/review-1   one review or homework (repeatable)
     node app/tools/playthrough.mjs --exam topic-1.5       one exam (repeatable); topic-*, stage-* and mock-* all play the same way
     node app/tools/playthrough.mjs --lesson conditional/l3-shrinking     one lesson (add --routes for the routes too)
     node app/tools/playthrough.mjs --routes-only          only the routes
     node app/tools/playthrough.mjs --shots out/shots      a screenshot per lesson screen and per route
     node app/tools/playthrough.mjs --shots out --mobile   also a 390 px wide screenshot of each (name-390.png)
     node app/tools/playthrough.mjs --shots out --why      also each lesson task's (and set item's) Explanation sheet after the right
                                                           answer (name-why.png), and after a wrong one where the
                                                           tool can make one (a choice distractor, a numeric answer
                                                           well off): name-wrong.png and name-wrong-why.png; an
                                                           exam's result page with every explanation open
     node app/tools/playthrough.mjs --local-cdn <dir>      serve cdn.jsdelivr.net from local npm packages (see below)
     node app/tools/playthrough.mjs --headed               watch it

   A mock exam (mock-*) is also checked for what is special about it: a forward-only paper refuses to go back or jump
   ahead (and a no-skip paper refuses to move on unanswered), generated items repeat for the same seed (#exam/<id>/<seed>)
   and differ for another, a second sitting with the clock moved to zero (ZQExam.setRemaining; no real timer is waited
   for) submits itself and is marked with the paper's own scoring, and every attempt is kept. A review whose file has
   timed: { seconds, lockAtZero: true } is likewise sat once with the clock moved to zero: it must end by itself and be
   recorded with what was answered.

   Needs Playwright (the globally installed package is found too) and Chromium at /opt/pw-browsers/chromium, else
   Playwright's own. Starts `python3 -m http.server` on a free port serving app/. A fresh browser profile is used, setup
   is completed through its form, then each lesson opens at #lesson/<course>/<lesson> and is driven through
   window.ZQ.test: answerCorrect(), check(), continue(), until current().kind is 'done'. Sets and exams use the same
   four calls: current().kind is 'start' (continue() begins), 'item' (answer, check, continue), 'submit', then 'done';
   a review must be recorded with every item right, a homework marked with every item right, an exam passed with
   every question right.
   A screen with a code widget is checked only after its Python (or C++ compiler) status reads ready; if it cannot load
   (no CDN access without --local-cdn) that is a failure, and an answer that applies with nothing to check is a failure too.

   --local-cdn <dir>: for machines without access to cdn.jsdelivr.net. <dir> holds unpacked npm tarballs:
     <dir>/pyodide-0.27.7/package/...                      for /pyodide/v0.27.7/full/...
     <dir>/mathlive-0.105.0/package/...                    for /npm/mathlive@0.105.0/...
     <dir>/cortex-js-compute-engine-0.30.2/package/...     for /npm/@cortex-js/compute-engine@0.30.2/...
     <dir>/yowasp-clang-21.1.4-3/package/...               for /npm/@yowasp/clang@21.1.4-3/... (the C++ compiler)
   (npm pack pyodide@0.27.7 mathlive@0.105.0 @cortex-js/compute-engine@0.30.2 @yowasp/clang@21.1.4-3, then untar each
   into <name>-<version>/.)
   The directory can also come from the ZQ_LOCAL_CDN environment variable. Google Fonts are stubbed with empty CSS.
   Without the flag those requests go to the network, and their failures are not counted as errors.

   Exit status: 0 when everything passed, 1 on any failure (a readable list is printed), 2 on a setup problem. */
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const CONTENT = path.join(APP, 'content');
const CHROMIUM = '/opt/pw-browsers/chromium';
const IGNORE_HOSTS = /(^|\.)cdn\.jsdelivr\.net$|(^|\.)fonts\.googleapis\.com$|(^|\.)fonts\.gstatic\.com$/;

/* ---------- Arguments ---------- */
const argv = process.argv.slice(2);
const opt = { mobile: false, why: false, lessons: [], shots: null, localCdn: null, routes: null, lessonsOn: true, headed: false, timeout: 20000, sets: false, exams: false, setIds: [], examIds: [], all: false };
for (let i = 0; i < argv.length; i++) {
  const a = argv[i], next = () => { const v = argv[++i]; if (v == null || v.startsWith('--')) die(`${a} needs a value`); return v; };
  if (a === '--lesson') opt.lessons.push(next());
  else if (a === '--shots') opt.shots = path.resolve(next());
  else if (a === '--local-cdn') { const v = argv[i + 1]; if (v && !v.startsWith('--')) { opt.localCdn = path.resolve(v); i++; } else opt.localCdn = process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : die('--local-cdn needs a directory (or set ZQ_LOCAL_CDN)'); }
  else if (a === '--mobile') opt.mobile = true;
  else if (a === '--why') opt.why = true;
  else if (a === '--routes') opt.routes = true;
  else if (a === '--no-routes') opt.routes = false;
  else if (a === '--routes-only') { opt.routes = true; opt.lessonsOn = false; }
  else if (a === '--headed') opt.headed = true;
  else if (a === '--sets') opt.sets = true;
  else if (a === '--exams') opt.exams = true;
  else if (a === '--set') { opt.setIds.push(next()); opt.sets = true; }
  else if (a === '--exam') { opt.examIds.push(next()); opt.exams = true; }
  else if (a === '--all') opt.all = true;
  else if (a === '--help' || a === '-h') { console.log(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('*/')[0].replace(/^#!.*\n\/\* ?/, '')); process.exit(0); }
  else die(`unknown argument ${a} (try --help)`);
}
const onlySets = !opt.all && (opt.sets || opt.exams);
if (opt.all) { opt.sets = true; opt.exams = true; }
if (onlySets && !opt.lessons.length) opt.lessonsOn = false;
if (opt.routes == null) opt.routes = opt.lessons.length === 0 && !onlySets;
if (opt.localCdn && !fs.existsSync(opt.localCdn)) die(`--local-cdn: ${opt.localCdn} does not exist`);
if (opt.shots) fs.mkdirSync(opt.shots, { recursive: true });
function die(msg) { console.error('playthrough: ' + msg); process.exit(2); }

/* ---------- Playwright: the local package, else the global one ---------- */
const loadPlaywright = async () => {
  try { return await import('playwright'); } catch { /* not resolvable from here */ }
  const roots = [];
  try { roots.push(execSync('npm root -g', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()); } catch { /* no npm */ }
  (process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).forEach(p => roots.push(p));
  for (const r of roots) {
    const f = path.join(r, 'playwright', 'index.mjs');
    if (fs.existsSync(f)) return import(pathToFileURL(f).href);
  }
  die('Playwright is not installed (npm i -g playwright)');
};

/* ---------- What to play ---------- */
const readJSON = (f) => JSON.parse(fs.readFileSync(f, 'utf8'));
const writtenLessons = () => {
  const out = [];
  const cur = readJSON(path.join(CONTENT, 'curriculum.json'));
  const order = cur.stages.flatMap(s => s.topics.flatMap(t => t.courses || []));
  for (const c of order) {
    const cf = path.join(CONTENT, 'courses', c, 'course.json');
    if (!fs.existsSync(cf)) continue;
    const doc = readJSON(cf);
    (doc.levels || []).forEach(lv => (lv.lessons || []).forEach(l => {
      if (fs.existsSync(path.join(CONTENT, 'courses', c, l + '.json'))) out.push(`${c}/${l}`);
    }));
  }
  /* Written level reviews and homework, in course order: { route, id, kind } */
  const sets = [];
  for (const c of order) {
    const cf = path.join(CONTENT, 'courses', c, 'course.json');
    if (!fs.existsSync(cf)) continue;
    (readJSON(cf).levels || []).forEach(lv => {
      if (lv.review && fs.existsSync(path.join(CONTENT, 'courses', c, lv.review + '.json'))) sets.push({ id: `${c}/${lv.review}`, kind: 'review', route: `review/${c}/${lv.review}` });
      if (lv.homework && fs.existsSync(path.join(CONTENT, 'courses', c, lv.homework + '.json'))) sets.push({ id: `${c}/${lv.homework}`, kind: 'homework', route: `homework/${c}/${lv.homework}` });
    });
  }
  const exams = fs.existsSync(path.join(CONTENT, 'exams')) ? fs.readdirSync(path.join(CONTENT, 'exams')).filter(f => /^(topic|stage|mock)-.*\.json$/.test(f)).map(f => f.replace(/\.json$/, '')).sort() : [];
  return { lessons: out, courses: order.filter(c => fs.existsSync(path.join(CONTENT, 'courses', c, 'course.json'))), sets, exams };
};

/* ---------- Static server on a free port ---------- */
const freePort = () => new Promise((res, rej) => { const s = net.createServer(); s.unref(); s.on('error', rej); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); });
const startServer = async () => {
  const port = await freePort();
  const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', APP], { stdio: ['ignore', 'ignore', 'pipe'] });
  let err = ''; proc.stderr.on('data', d => { err += d; if (err.length > 4000) err = err.slice(-4000); });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i++) {
    if (proc.exitCode != null) die('the static server stopped: ' + err);
    try { const r = await fetch(base + '/index.html'); if (r.ok) return { proc, base }; } catch { /* not up yet */ }
    await new Promise(r => setTimeout(r, 100));
  }
  proc.kill(); die('the static server did not start');
};

/* ---------- Local CDN ---------- */
const MIME = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm', '.zip': 'application/zip',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.map': 'application/json', '.whl': 'application/zip', '.tar': 'application/x-tar' };
const cdnFile = (u) => {
  let m;
  if ((m = u.pathname.match(/^\/pyodide\/v([\d.]+)\/full\/(.*)$/))) return path.join(opt.localCdn, `pyodide-${m[1]}`, 'package', m[2]);
  if ((m = u.pathname.match(/^\/npm\/(@[^/]+\/[^@/]+|[^@/]+)@([^/]+)\/(.*)$/))) return path.join(opt.localCdn, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package', m[3]);
  return null;
};

/* ---------- Run ---------- */
const main = async () => {
  const { chromium } = await loadPlaywright();
  const { lessons: allLessons, courses, sets: allSets, exams: allExams } = writtenLessons();
  const lessons = opt.lessonsOn ? (opt.lessons.length ? opt.lessons : allLessons) : [];
  for (const l of opt.lessons) if (!allLessons.includes(l)) die(`--lesson ${l}: no such written lesson (the file must exist and be listed in its course.json)`);
  for (const x of opt.setIds) if (!allSets.some(s2 => s2.id === x)) die(`--set ${x}: no such written review or homework (the file must exist and be named in its course.json)`);
  for (const x of opt.examIds) if (!allExams.includes(x)) die(`--exam ${x}: no such exam in content/exams`);
  const sets = opt.setIds.length ? allSets.filter(s2 => opt.setIds.includes(s2.id)) : opt.sets ? allSets : [];
  const exams = opt.examIds.length ? opt.examIds : opt.exams ? allExams : [];
  const { proc, base } = await startServer();
  const browser = await chromium.launch({ headless: !opt.headed, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
  const failures = [], consoleErrors = [];
  let where = 'start';
  const cleanup = async () => { try { await browser.close(); } catch { /* closed */ } proc.kill(); };
  process.on('SIGINT', async () => { await cleanup(); process.exit(130); });
  try {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 860 }, acceptDownloads: true });
    if (opt.localCdn) {
      await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
        const f = cdnFile(new URL(route.request().url()));
        if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
        return route.fulfill({ status: 404, body: '' });
      });
      await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
    }
    const page = await ctx.newPage();
    const hostOf = (u) => { try { return new URL(u).hostname; } catch { return ''; } };
    page.on('console', (m) => {
      if (m.type() !== 'error') return;
      const loc = m.location() && m.location().url;
      if (/^Failed to load resource/.test(m.text()) && IGNORE_HOSTS.test(hostOf(loc))) return;
      consoleErrors.push({ where, text: m.text() + (loc ? `  (${loc})` : '') });
    });
    page.on('pageerror', (e) => consoleErrors.push({ where, text: 'Uncaught ' + (e.stack || e.message) }));
    page.on('requestfailed', (r) => { if (!IGNORE_HOSTS.test(hostOf(r.url()))) consoleErrors.push({ where, text: `request failed: ${r.url()} (${r.failure() && r.failure().errorText})` }); });
    page.on('response', (r) => { if (r.status() >= 400 && r.url().startsWith(base)) consoleErrors.push({ where, text: `HTTP ${r.status()} ${r.url().slice(base.length)}` }); });

    /* items 199, 205: --mobile adds a 390 px wide copy of every screenshot (the viewport narrows, then returns) */
    /* inbox (backtest 1): a failing code screen names its first failing test (or the error) in the failure line */
    const codeWhy = async () => { try { return await page.evaluate(() => { const n = document.querySelector('.wd-res > .wd-res-err, .wd-res-row.bad'); return n ? ' (' + n.textContent.replace(/\s+/g, ' ').trim().slice(0, 240) + ')' : ''; }); } catch { return ''; } };
    const shot = async (name) => {
      if (!opt.shots) return;
      const file = (sfx) => path.join(opt.shots, name.replace(/[^\w.-]+/g, '_') + sfx + '.png');
      /* item 278: past the enter patch (350 ms), then until canvas tweens and CSS animations have settled (at most 3 s) */
      await page.waitForTimeout(420);
      try { await page.waitForFunction(() => (!window.ZQ || !ZQ.canvas || !ZQ.canvas.busy || ZQ.canvas.busy() === 0) && !document.getAnimations().some((a) => a.playState === 'running' && a.effect && a.effect.getComputedTiming().iterations !== Infinity), null, { timeout: 3000, polling: 50 }); } catch { /* still moving: shoot anyway */ }
      await page.screenshot({ path: file('') });
      if (opt.mobile) { await page.setViewportSize({ width: 390, height: 844 }); await page.waitForTimeout(350); await page.screenshot({ path: file('-390') }); await page.setViewportSize({ width: 1280, height: 860 }); await page.waitForTimeout(150); }
    };
    const whyShot = async (name) => { if (!opt.why || !opt.shots) return; if (await page.evaluate(() => !!(ZQ.test.why && ZQ.test.why()))) { await page.waitForTimeout(450); await shot(name); await page.evaluate(() => ZQ.test.closeWhy()); await page.waitForTimeout(250); } };
    const go = async (hash) => {
      await page.evaluate((h) => { location.hash = h; }, hash);
      await page.waitForFunction((h) => location.hash === '#' + h || location.hash.startsWith('#' + h.split('/')[0]), hash, { timeout: opt.timeout });
      await page.waitForTimeout(400);
    };

    /* Fresh profile, then setup through the form */
    where = 'setup';
    // A new browser context starts with empty storage; clear it anyway, then reload once everything has settled
    await page.goto(base + '/#setup');
    await page.waitForFunction(() => window.ZQ && ZQ.content && ZQ.content.ready && ZQ.state, null, { timeout: opt.timeout });
    await page.evaluate(() => ZQ.content.ready.then(() => { localStorage.clear(); sessionStorage.clear(); ZQ.state.reset(); }));
    await page.reload();
    await page.waitForFunction(() => window.ZQ && ZQ.content && ZQ.content.ready, null, { timeout: opt.timeout });
    await page.evaluate(() => ZQ.content.ready);
    await page.waitForSelector('[data-name]', { timeout: opt.timeout });
    await page.fill('[data-name]', 'Playthrough');
    await page.click('[data-next]');
    await page.click('[data-track="Trader"]');
    await page.click('[data-next]');
    await page.click('[data-h="15"]');
    await page.click('[data-stage="1"]');
    await shot('setup-3');
    await page.click('[data-next]');
    await page.waitForFunction(() => window.ZQ && ZQ.state && ZQ.state.flags.setupDone === true, null, { timeout: opt.timeout });
    console.log(`setup done. ${lessons.length} lesson${lessons.length === 1 ? '' : 's'}${sets.length ? `, ${sets.length} review and homework set${sets.length === 1 ? '' : 's'}` : ''}${exams.length ? `, ${exams.length} exam${exams.length === 1 ? '' : 's'}` : ''} to play.`);

    /* Lessons */
    /* Item 112: a code screen is checked only once Python is ready (or has failed to load, which is a failure) */
    /* item 304: a C++ code widget (.wd-cpp) waits up to 5 minutes for the compiler (about 26 MB to download, then a
       warm-up compile), and its load failure is a failure with the reason the widget gives */
    const waitPython = async () => {
      const has = await page.evaluate(() => ({ any: !!document.querySelector('.wd-py'), cpp: !!document.querySelector('.wd-cpp .wd-py') }));
      if (!has.any) return null;
      const lang = has.cpp ? 'The C++ compiler' : 'Python', wait = has.cpp ? 300000 : 90000;
      try {
        await page.waitForFunction(() => ![...document.querySelectorAll('.wd-py')].some(e => ['idle', 'loading', 'restarting', 'running'].includes(e.dataset.s)), null, { timeout: Math.max(opt.timeout, wait) });
      } catch { return `${lang} did not become ready within ${wait / 1000} s`; }
      const bad = await page.evaluate(() => { const e = [...document.querySelectorAll('.wd-py')].find(x => x.dataset.s === 'unavailable'); return e ? (e.title || 'unavailable') : null; });
      return bad ? `${lang} could not load, so the code tests did not run (pass --local-cdn without CDN access): ${bad}` : null;
    };

    for (const id of lessons) {
      where = `#lesson/${id}`;
      const fails = [];
      const t0 = Date.now();
      try {
        await go(`lesson/${id}`);
        await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind !== 'loading', null, { timeout: opt.timeout });
        let guard = 0, last = '', same = 0, checks = 0;
        while (true) {
          const c = await page.evaluate(() => ZQ.test.current());
          if (c.kind === 'done') break;
          const key = `${c.phase}:${c.screenIndex}:${c.state}`;
          same = key === last ? same + 1 : 0; last = key;
          if (same >= 3) { fails.push(`stuck at ${c.phase} ${c.screenIndex} (${c.kind}, state ${c.state})`); break; }
          if (++guard > 200) { fails.push('more than 200 steps without reaching the end'); break; }
          if (opt.shots && same === 0) await shot(`${id}-${c.phase}-${String(c.screenIndex).padStart(2, '0')}-${c.kind}`);
          if (c.state === 'idle' || c.state === 'engaged') {
            const py = await waitPython();
            if (py) { fails.push(`${c.phase} ${c.screenIndex} (${c.kind}): ${py}`); break; }
            const nm = `${id}-${c.phase}-${String(c.screenIndex).padStart(2, '0')}-${c.kind}`;
            if (opt.why && opt.shots && c.phase === 'lesson' && await page.evaluate(() => !!(ZQ.test.answerWrong && ZQ.test.answerWrong()))) {
              const rw = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok } : null; });
              if (rw && !rw.ok) { await shot(nm + '-wrong'); await whyShot(nm + '-wrong-why'); await page.evaluate(() => ZQ.test.tryAgain()); await page.waitForTimeout(200); }
            }
            const applied = await page.evaluate(() => ZQ.test.answerCorrect());
            const r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, key: r.key ?? null, pending: !!r.pending } : null; });
            if (r && r.ok && !r.pending) await whyShot(nm + '-why');
            if (r && r.pending) { // long-form: the first check opens the self-marking, the second grades it
              await page.evaluate(() => ZQ.test.answerCorrect());
              const r2 = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, key: r.key ?? null } : null; });
              checks++;
              if (r2 && !r2.ok) fails.push(`${c.phase} ${c.screenIndex} (${c.kind}): not correct, key ${JSON.stringify(r2.key)}`);
            } else if (r) {
              checks++;
              if (!r.ok) fails.push(`${c.phase} ${c.screenIndex} (${c.kind}): not correct, key ${JSON.stringify(r.key)}${await codeWhy()}`);
            } else if (c.state === 'idle' && applied === false && c.kind !== 'title' && c.kind !== 'demonstrate' && c.kind !== 'generalise') {
              fails.push(`${c.phase} ${c.screenIndex} (${c.kind}): answerCorrect() could not apply the authored answer`);
            } else if (applied !== false) {
              // the answer applied but there was nothing to check: never reveal and move on silently
              fails.push(`${c.phase} ${c.screenIndex} (${c.kind}): the authored answer applied but check() had nothing to grade (the screen never became ready)`);
            }
            const after = await page.evaluate(() => ZQ.test.current());
            if (after.phase === 'lesson' && ['no', 'idle', 'engaged'].includes(after.state)) await page.evaluate(() => ZQ.test.reveal()); // so Continue can move on
          }
          await page.evaluate(() => ZQ.test.continue());
        }
        const fin = await page.evaluate((lid) => { const [c, l] = lid.split('/'); const r = ZQ.state.lesson(c, l); return r ? { done: r.done, quiz: r.bestQuiz } : null; }, id);
        if (!fails.length && (!fin || !fin.done)) fails.push('the completion screen was reached but the lesson is not recorded as done');
        await shot(`${id}-done`);
        console.log(`${fails.length ? 'FAIL' : 'ok  '} ${id}  ${checks} checks, ${((Date.now() - t0) / 1000).toFixed(1)} s${fin && fin.quiz ? `, quiz ${fin.quiz[0]}/${fin.quiz[1]}` : ''}`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL ${id}  threw`);
      }
      fails.forEach(f => failures.push(`#lesson/${id}: ${f}`));
    }

    /* Reviews, homework and exams through the set-mode hook. Each page installs window.ZQ.test on mount; wait for a hook
       that is past 'loading', then: 'start' and 'submit' -> continue(); 'item' -> answerCorrect(), check() (a pending
       long-form check is answered and checked again), continue(); until 'done'. */
    /* item 445: a set that reports no items, or a hook that never answers (a course file mid-write by another agent, or a
       worker left busy by the lessons before), is reloaded and played once more before it counts as a failure */
    const playSet = async (route, label, verify, attempt = 1) => {
      where = '#' + route;
      const fails = [];
      const t0 = Date.now();
      let checks = 0;
      const probed = new Set();
      try {
        await page.evaluate(() => { delete window.ZQ.test; });
        if (await page.evaluate((r) => location.hash === '#' + r, route)) await go('review');   // the same hash would not remount
        await go(route);
        await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind !== 'loading', null, { timeout: opt.timeout });
        let guard = 0, last = '', same = 0;
        while (true) {
          const c = await page.evaluate(() => ZQ.test.current());
          if (c.kind === 'done') break;
          if (c.kind === 'empty') { fails.push('the set has no items'); break; }
          const key = `${c.kind}:${c.screenIndex}:${c.state}:${c.paper ?? ''}`;
          same = key === last ? same + 1 : 0; last = key;
          if (same >= 4) { fails.push(`stuck at ${c.kind} ${c.screenIndex} (state ${c.state})`); break; }
          if (++guard > 400) { fails.push('more than 400 steps without reaching the end'); break; }
          if (opt.shots && same === 0) await shot(`${label}-${c.kind}-${String(c.screenIndex).padStart(2, '0')}`);
          if (c.kind === 'item' && c.forward && c.screenIndex <= 1 && !probed.has(`${c.paper}:${c.screenIndex}`)) {
            /* a forward-only paper: no jumping ahead, no going back, and with skip: false no moving on unanswered */
            probed.add(`${c.paper}:${c.screenIndex}`);
            const pr = await page.evaluate(async (c) => {
              const at = () => ZQ.test.current().screenIndex, i0 = at(), out = {};
              window.ZQExam.go(i0 + 2); out.jump = at() - i0;
              if (i0 >= 1) { window.ZQExam.go(i0 - 1); out.back = at() - i0; }
              if (c.noSkip && c.state === 'idle') { await ZQ.test.continue(); out.skip = at() - i0; }
              return out;
            }, c);
            if (pr.jump) fails.push(`paper ${c.paper + 1}: a forward-only paper let the learner jump ahead`);
            if (pr.back) fails.push(`paper ${c.paper + 1}: a forward-only paper let the learner go back`);
            if (pr.skip) fails.push(`paper ${c.paper + 1}: a no-skip paper moved on without an answer`);
          }
          if (c.kind === 'item' && (c.state === 'idle' || c.state === 'engaged')) {
            const py = await waitPython();
            if (py) { fails.push(`item ${c.screenIndex + 1}: ${py}`); break; }
            const applied = await page.evaluate(() => ZQ.test.answerCorrect());
            let r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, key: r.key ?? null, pending: !!r.pending } : null; });
            if (r && r.pending) {
              await page.evaluate(() => ZQ.test.answerCorrect());
              r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, key: r.key ?? null, pending: !!r.pending } : null; });
            }
            checks++;
            if (!r) fails.push(`item ${c.screenIndex + 1}${c.paper != null ? ` (paper ${c.paper + 1})` : ''}: ${applied === false ? 'answerCorrect() could not apply the authored answer' : 'nothing to check'}`);
            else if (!r.ok) fails.push(`item ${c.screenIndex + 1}${c.paper != null ? ` (paper ${c.paper + 1})` : ''}: not correct, key ${JSON.stringify(r.key)}${await codeWhy()}`);
            else await whyShot(`${label}-item-${String(c.screenIndex).padStart(2, '0')}-why`); // item 335: set items' Explanation sheets
          }
          await page.evaluate(() => ZQ.test.continue());
          await page.waitForTimeout(120);
        }
        const v = await verify();
        if (v.fail) fails.push(v.fail);
        await shot(`${label}-done`);
        /* item 335: an exam's result page with every question's explanation opened */
        if (opt.why && opt.shots && /^exam\//.test(route)) { await page.evaluate(() => document.querySelectorAll('.exm-ri-h[aria-expanded="false"]').forEach((b) => b.click())); await page.waitForTimeout(400); await page.screenshot({ path: path.join(opt.shots, `${label}-done-why`.replace(/[^\w.-]+/g, '_') + '.png'), fullPage: true }); }
        console.log(`${fails.length ? 'FAIL' : 'ok  '} ${label}  ${checks} items, ${v.note || ''}, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL ${label}  threw`);
      }
      if (attempt === 1 && fails.some(f => f === 'the set has no items' || /^threw: .*(Timeout|waitForFunction)/.test(f))) {
        console.log(`     ${label}: retrying once after a reload`);
        try { await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(800); } catch { /* the retry reports it */ }
        return playSet(route, label, verify, 2);
      }
      fails.forEach(f => failures.push(`#${route}: ${f === 'the set has no items' ? f + ' (twice: check that its items exist and validate; a course file may have been mid-write)' : f}`));
    };
    /* A review with timed: { lockAtZero: true } is sat once with the clock moved to zero after one answer: it must end by
       itself, with the unanswered items missed and the review recorded (no real timer is waited for) */
    const timedChecks = async (st, timed) => {
      where = '#' + st.route;
      const fails = [];
      const t0 = Date.now();
      try {
        await go('review');
        await page.evaluate(() => { delete window.ZQ.test; });
        await go(st.route);
        await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind === 'start', null, { timeout: opt.timeout });
        await page.evaluate(() => ZQ.test.continue());
        await page.waitForFunction(() => window.ZQSet && ZQ.test.current().kind === 'item', null, { timeout: opt.timeout });
        const py = await waitPython();
        if (py) fails.push(py);
        else {
          await page.evaluate(() => ZQ.test.answerCorrect());
          const r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok } : null; });
          if (!r || !r.ok) fails.push('the first item could not be answered correctly before the clock ran out');
          await page.evaluate(() => ZQSet.setRemaining(0));
          await page.waitForFunction(() => ZQ.test.current().kind === 'done', null, { timeout: 5000 }).catch(() => fails.push('the clock reached zero but the set did not end by itself'));
          const rec = await page.evaluate((k) => ZQ.state.reviews[k] || null, st.id);
          if (!rec) fails.push('the timed-out review was not recorded');
          else if (rec.score !== 1) fails.push(`the timed-out review recorded ${rec.score} right (one item was answered)`);
        }
        console.log(`${fails.length ? 'FAIL' : 'ok  '} ${st.id} (timed ${timed.seconds} s, clock at zero), ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL ${st.id} (timed)  threw`);
      }
      fails.forEach(f => failures.push(`#${st.route}: ${f}`));
    };
    for (const st of sets) {
      if (st.kind === 'review') { const t = readJSON(path.join(CONTENT, 'courses', ...st.id.split('/')) + '.json').timed; if (t && t.lockAtZero) await timedChecks(st, t); }
      await playSet(st.route, st.id, async () => {
        if (st.kind === 'review') {
          const r = await page.evaluate((k) => ZQ.state.reviews[k] || null, st.id);
          if (!r) return { fail: 'the review was not recorded' };
          return { fail: r.score !== r.items || !r.items ? `recorded ${r.score} of ${r.items}` : null, note: `recorded ${r.score} of ${r.items}` };
        }
        const h = await page.evaluate((k) => ZQ.state.homework[k] || null, st.id);
        if (!h || !h.submitted) return { fail: 'the homework was not submitted' };
        const c = await page.evaluate(() => ZQ.test.current());
        const note = `marked ${h.score} of ${h.items} right, ${c.marks} of ${c.of} marks`;
        return { fail: h.score !== h.items || !h.items ? note : null, note };
      });
    }
    /* A mock exam: forward-only papers are probed while it is played (above); here the generated items must repeat for one
       seed and differ for another, and a second sitting with the clock moved to zero must submit itself (no timer is waited for) */
    const mockChecks = async (ex) => {
      where = `#exam/${ex}`;
      const fails = [];
      const doc = readJSON(path.join(CONTENT, 'exams', ex + '.json'));
      const papers = (Array.isArray(doc.parts) ? doc.parts : [doc]).filter(p => p.kind === 'paper' || !Array.isArray(doc.parts));
      const t0 = Date.now();
      try {
        const open = async (hash) => {
          await go('review');   // a changed hash is what remounts the screen, so leave it first
          await page.evaluate(() => { delete window.ZQ.test; });
          await go(hash);
          await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind !== 'loading', null, { timeout: opt.timeout });
        };
        if (JSON.stringify(doc).includes('"generator"')) {
          const grab = async (seed) => {
            await open(`exam/${ex}/${seed}`);
            await page.evaluate(() => ZQ.test.continue());
            await page.waitForFunction(() => window.ZQExam && ZQExam.handles().length, null, { timeout: opt.timeout });
            return page.evaluate(() => ZQExam.handles().map(h => h && h.item && h.item.generated ? h.item.question : null).filter(Boolean));
          };
          const a = await grab(4242), b = await grab(4242), c2 = await grab(4243);
          if (!a.length) fails.push('no generated questions appeared');
          else if (JSON.stringify(a) !== JSON.stringify(b)) fails.push('the same seed gave different generated questions');
          else if (JSON.stringify(a) === JSON.stringify(c2)) fails.push('a different seed gave the same generated questions');
        }
        await open(`exam/${ex}`);
        const before = await page.evaluate((id) => (ZQ.state.exams[id] || { attempts: [] }).attempts.length, ex);
        let guard = 0, answered = new Set();
        while (++guard < 80) {
          const c = await page.evaluate(() => ZQ.test.current());
          if (c.kind === 'done') break;
          if (c.kind === 'start') await page.evaluate(() => ZQ.test.continue());
          else if (c.kind === 'item') {
            if (!answered.has(c.paper)) {
              answered.add(c.paper);
              await page.evaluate(() => ZQ.test.answerCorrect());
              await page.evaluate(() => ZQExam.setRemaining(0));
            }
          }
          await page.waitForTimeout(150);
        }
        const c = await page.evaluate(() => ZQ.test.current());
        if (c.kind !== 'done') fails.push('the clock reached zero but the exam did not finish by itself');
        else {
          const r = await page.evaluate((id) => { const a = ZQ.state.exams[id].attempts; return { n: a.length, last: a[a.length - 1], note: (document.querySelector('.exm-hero-note') || {}).textContent || '' }; }, ex);
          if (r.n !== before + 1) fails.push(`the timed-out sitting was not kept as an attempt (${before} before, ${r.n} after)`);
          if (!/Time ran out/.test(r.note)) fails.push('the result does not say that time ran out');
          if (!(c.score >= 1 && c.score <= papers.length)) fails.push(`timed out with one answer per paper but scored ${c.score}`);
          if (typeof r.last.net !== 'number' || typeof r.last.max !== 'number') fails.push('the attempt carries no net score');
          await shot(`${ex}-timeup`);
        }
        console.log(`${fails.length ? 'FAIL' : 'ok  '} ${ex} (mock checks)  seed, clock at zero, attempts kept, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL ${ex} (mock checks)  threw`);
      }
      fails.forEach(f => failures.push(`#exam/${ex}: ${f}`));
    };
    for (const ex of exams) {
      await playSet(`exam/${ex}`, ex, async () => {
        const c = await page.evaluate(() => ZQ.test.current());
        if (c.kind !== 'done') return { fail: 'the result page was not reached' };
        const note = `scored ${c.score} of ${c.total}${c.max != null && c.max !== c.total ? `, net ${c.net} of ${c.max}` : ''}, ${c.passed ? 'passed' : 'not passed'}`;
        return { fail: !c.passed || c.score !== c.total || !c.total ? note : null, note };
      });
      if (/^mock-/.test(ex)) await mockChecks(ex);
    }

    /* Every other route once */
    if (opt.routes) {
      const exams = fs.existsSync(path.join(CONTENT, 'exams')) ? fs.readdirSync(path.join(CONTENT, 'exams')).filter(f => /^topic-.*\.json$/.test(f)).map(f => f.replace(/\.json$/, '')) : [];
      const drills = fs.existsSync(path.join(CONTENT, 'drills', 'index.json')) ? readJSON(path.join(CONTENT, 'drills', 'index.json')).map(d => d.id || d) : [];
      /* The Prepare for page (ENGINE-BACKLOG 455): the default path, then one deep link for each kind of path in content/prep.json */
      const prepFile = path.join(CONTENT, 'prep.json');
      const prepPaths = fs.existsSync(prepFile) ? (readJSON(prepFile).paths || []) : [];
      const prepRoutes = prepPaths.length ? ['prepare', ...['general', 'stage', 'firm'].map(k => prepPaths.find(p => p.kind === k)).filter(Boolean).map(p => `prepare/${p.id}`)] : [];
      const routes = ['today', 'learn', ...courses.map(c => `course/${c}`), 'review', ...prepRoutes, 'you', 'system', 'drill',
        ...drills.slice(0, 1).map(d => `drill/${d}`), ...(exams.includes('topic-1.5') ? ['exam/topic-1.5'] : exams.slice(0, 1).map(e => `exam/${e}`)), 'setup'];
      for (const r of routes) {
        where = '#' + r;
        const before = consoleErrors.length;
        try {
          await go(r);
          const blank = await page.evaluate(() => { const a = document.querySelector('#app'); return !a || a.innerText.trim().length < 20 || /This screen failed to render/.test(a.innerText); });
          if (blank) failures.push(`#${r}: the screen is empty or failed to render`);
          if (/^prepare(\/|$)/.test(r)) {
            /* Prepare for: the chosen path lists every step, and nothing spills sideways (also at 390 px with --mobile) */
            const pid = r.split('/')[1] || (['general', 'stage', 'firm'].map(k => prepPaths.find(p => p.kind === k)).find(Boolean) || {}).id, want = ((prepPaths.find(p => p.id === pid) || {}).steps || []).length;
            const probe = () => page.evaluate(() => ({ steps: document.querySelectorAll('.pp-step').length, wide: document.documentElement.scrollWidth > window.innerWidth + 1, bad: document.querySelectorAll('.pp-step a[href="#course/undefined"]').length }));
            for (const w of opt.mobile ? [1280, 390] : [1280]) {
              if (w !== 1280) { await page.setViewportSize({ width: w, height: 844 }); await page.waitForTimeout(300); }
              const got = await probe();
              if (got.steps !== want) failures.push(`#${r} at ${w} px: ${got.steps} steps drawn, ${want} in prep.json`);
              if (got.wide) failures.push(`#${r} at ${w} px: the page is wider than the window`);
              if (got.bad) failures.push(`#${r}: a step links to an unknown course`);
              if (w !== 1280) { await page.setViewportSize({ width: 1280, height: 860 }); await page.waitForTimeout(150); }
            }
          }
          await shot('route-' + r);
        } catch (e) { failures.push(`#${r}: threw ${String(e.message || e).split('\n')[0]}`); }
        console.log(`${consoleErrors.length > before ? 'ERR ' : 'ok  '} #${r}`);
      }
    }
  } finally {
    await cleanup();
  }

  /* Report */
  const byWhere = {};
  consoleErrors.forEach(e => (byWhere[e.where] = byWhere[e.where] || []).push(e.text));
  Object.entries(byWhere).forEach(([w, list]) => Array.from(new Set(list)).forEach(t => failures.push(`${w}: console error: ${t}`)));
  if (failures.length) {
    console.log(`\n${failures.length} problem${failures.length === 1 ? '' : 's'}:`);
    failures.forEach(f => console.log('  - ' + f));
    process.exit(1);
  }
  console.log('\nAll passed.');
};
main().catch((e) => { console.error(e); process.exit(2); });
