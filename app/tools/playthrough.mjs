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
     node app/tools/playthrough.mjs --bank probability-1   every item of one bank file (repeatable, or --bank all): dealt, answered right from its key, pass or fail per item
     node app/tools/playthrough.mjs --drill sample-cpp-row-sums   one drill (repeatable; --drills for every file in content/drills): the starter fails, the model
                                                           solution passes every hidden test, the stopwatch is read and recorded (add --mobile for 390 px)
     node app/tools/playthrough.mjs --session              the sample drill session: both drills, minutes per drill, result, carry, expiry (--drills includes it)
     node app/tools/playthrough.mjs --routes-only          only the routes, then the interview bank deck (due and new items, the 3-day box,
                                                           a miss, prerequisites, an old save, the pace line) and one exam sat with a
                                                           skewed Date.now so per-item seconds and the pace line are checked
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
const opt = { mobile: false, why: false, lessons: [], shots: null, localCdn: null, routes: null, lessonsOn: true, headed: false, timeout: 20000, sets: false, exams: false, setIds: [], examIds: [], bankIds: [], drillIds: [], drillsAll: false, sessionRun: false, all: false };
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
  else if (a === '--bank') opt.bankIds.push(next());
  else if (a === '--drill') opt.drillIds.push(next());
  else if (a === '--drills') opt.drillsAll = true;
  else if (a === '--session') opt.sessionRun = true;
  else if (a === '--all') opt.all = true;
  else if (a === '--help' || a === '-h') { console.log(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('*/')[0].replace(/^#!.*\n\/\* ?/, '')); process.exit(0); }
  else die(`unknown argument ${a} (try --help)`);
}
const onlySets = !opt.all && (opt.sets || opt.exams);
if (opt.all) { opt.sets = true; opt.exams = true; }
if (onlySets && !opt.lessons.length) opt.lessonsOn = false;
if (opt.bankIds.length && !opt.lessons.length && !onlySets) opt.lessonsOn = false;
const drillRun = opt.drillIds.length || opt.drillsAll || opt.sessionRun; // item 472
if (drillRun && !opt.lessons.length && !onlySets) opt.lessonsOn = false;
if (opt.routes == null) opt.routes = opt.lessons.length === 0 && !onlySets && !opt.bankIds.length && !drillRun;
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
    const playSet = async (route, label, verify, attempt = 1, tick = null) => {
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
            if (tick) await tick(c, checks);
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
        return playSet(route, label, verify, 2, tick);
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

    /* ---------- Interview bank deck and per-item timing (ENGINE-BACKLOG 456, 457): part of --routes-only ----------
       Date.now is skewed from the tool (window.__skew, in seconds), so an item can "take" 90 s and a schedule can be
       moved forward by days without waiting; the exam clock reads performance.now and is not affected. */
    const skew = (sec) => page.evaluate((n) => { if (window.__skew === undefined) { window.__skew = 0; const real = Date.now.bind(Date); Date.now = () => real() + window.__skew * 1000; } window.__skew += n; return window.__skew; }, sec);
    const unskew = () => page.evaluate(() => { window.__skew = 0; });
    const bankFiles = () => (fs.existsSync(path.join(CONTENT, 'bank')) ? fs.readdirSync(path.join(CONTENT, 'bank')).filter(f => /^[a-z0-9-]+\.json$/.test(f)).map(f => readJSON(path.join(CONTENT, 'bank', f))) : []);
    const bankChecks = async () => {
      const docs = bankFiles();
      if (!docs.length) return;
      where = '#bank';
      const fails = [], t0 = Date.now();
      const items = docs.flatMap(d => d.items), open = items.filter(it => !it.requires), lockedN = items.length - open.length;
      try {
        /* 0. counts come from the bank files: unique uids, and the engine's own totals agree with them */
        const uids = docs.flatMap(d => d.items.map(it => `bank/${d.id}/${it.id}`));
        if (new Set(uids).size !== uids.length) fails.push('two bank items share a uid');
        const stat = await page.evaluate(() => ZQ.select.bankStatus());
        if (stat.total !== open.length || stat.locked !== lockedN || stat.fresh !== open.length) fails.push(`bankStatus says ${stat.total} drawable, ${stat.locked} locked, ${stat.fresh} new; the files give ${open.length}, ${lockedN}, ${open.length}`);
        /* 1. the Review card: due and new counts, the locked line, the start link */
        await go('review');
        await page.waitForFunction(() => { const s = document.querySelector('[data-sec="bank"]'); return s && !s.hidden; }, null, { timeout: opt.timeout });
        const card = await page.evaluate(() => ({ line: (document.querySelector('[data-bank-line]') || {}).textContent || '', start: !!document.querySelector('[data-start-bank]'), wide: document.documentElement.scrollWidth > window.innerWidth + 1 }));
        if (!card.start) fails.push('the Review card has no Start interview practice link');
        if (!new RegExp(`${open.length} new`).test(card.line)) fails.push(`the card line does not say ${open.length} new: "${card.line}"`);
        if (lockedN && !/unlock/.test(card.line)) fails.push(`the card does not mention the ${lockedN} locked question(s): "${card.line}"`);
        if (card.wide) fails.push('the Review page is wider than the window with the bank card');
        await shot('route-review-bank');
        /* 2. prerequisites: a question that names lessons is not drawn while they are unfinished */
        const drawn = await page.evaluate(() => ZQ.select.bankDeck({ n: 500 }).then(a => a.map(x => x.uid)));
        if (drawn.length !== open.length) fails.push(`the deck can draw ${drawn.length} questions, ${open.length} expected (${lockedN} locked by requires)`);
        const fams = await page.evaluate(() => ZQ.select.bankDeck({ n: 500 }).then(a => a.map(x => x.family)));
        let adj = 0; for (let k = 1; k < Math.min(fams.length, 8) ; k++) if (fams[k] === fams[k - 1]) adj++;
        if (new Set(fams).size > 1 && adj > 1) fails.push(`families are not mixed: ${adj} neighbours share a family`);
        /* 3. a deck sitting: one item "takes" 200 s, the rest 3 s; the summary has the pace line */
        await go('review');
        await page.evaluate(() => { delete window.ZQ.test; });
        await go('bank');
        await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind === 'start', null, { timeout: opt.timeout });
        await shot('bank-start');
        await page.evaluate(() => ZQ.test.continue());
        await page.waitForFunction(() => ZQ.test.current().kind === 'item', null, { timeout: opt.timeout });
        let n = 0, guard = 0;
        while ((await page.evaluate(() => ZQ.test.current().kind)) !== 'done' && ++guard < 60) {
          const c = await page.evaluate(() => ZQ.test.current());
          if (c.kind === 'item' && (c.state === 'idle' || c.state === 'engaged')) {
            await skew(n === 1 ? 200 : 3); n++;
            await page.evaluate(() => ZQ.test.answerCorrect());
            const r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, seconds: r.seconds } : null; });
            if (!r || !r.ok) fails.push(`deck item ${n}: not correct`);
            else if (typeof r.seconds !== 'number') fails.push(`deck item ${n}: no seconds on the result`);
            else if (n === 2 && r.seconds < 190) fails.push(`deck item 2 should have taken about 200 s, read ${r.seconds}`);
          }
          await page.evaluate(() => ZQ.test.continue());
          await page.waitForTimeout(100);
        }
        const sum = await page.evaluate(() => ({ pace: (document.querySelector('.hw-pace') || {}).textContent || '', note: (document.querySelector('.hw-redo') || {}).textContent || '', rows: document.querySelectorAll('.hw-res li').length, wide: document.documentElement.scrollWidth > window.innerWidth + 1 }));
        if (!/Average .* a question/.test(sum.pace)) fails.push(`the summary has no average pace: "${sum.pace}"`);
        if (!/Over pace: 1 of /.test(sum.pace)) fails.push(`the summary does not name the one item over pace: "${sum.pace}"`);
        if (new Set(docs.flatMap(d => d.items.map(it => it.tags[0]))).size > 1 && !/Slowest famil/.test(sum.pace)) fails.push(`the summary does not name the slowest families: "${sum.pace}"`);
        if (!/tomorrow|in 3 days|in 7 days|in 30 days/.test(sum.note)) fails.push(`the summary does not say when questions return: "${sum.note}"`);
        if (sum.wide) fails.push('the bank summary is wider than the window');
        await shot('bank-done');
        /* 4. the schedule: each answered item has its own entry in box 3 days (new, then right), timing is logged */
        const st = await page.evaluate(() => { const b = ZQ.state.bank.list(), d = Date.now(); return { n: Object.keys(b).length, boxes: Object.values(b).map(r => r.box), off: Object.values(b).map(r => Math.round((r.due - d) / 86400000 * 10) / 10), fam: Object.keys(ZQ.state.timing.families).length, secs: Object.values(b).filter(r => typeof r.secs === 'number').length }; });
        const want = Math.min(8, open.length);
        if (st.n !== want) fails.push(`${st.n} schedule entries after the deck, ${want} expected`);
        if (st.boxes.some(b => b !== 3)) fails.push(`first right answers should sit in the 3-day box: ${JSON.stringify(st.boxes)}`);
        if (st.off.some(o => Math.abs(o - 3) > 0.1)) fails.push(`due dates are not 3 days ahead: ${JSON.stringify(st.off)}`);
        if (!st.fam) fails.push('no per-family timing was logged');
        if (st.secs !== st.n) fails.push('not every schedule entry kept its seconds');
        /* 5. a miss goes back to box 1, due in a day; two days on it is due again and others are not; 40 days on all are due */
        const miss = await page.evaluate(() => { const uid = Object.keys(ZQ.state.bank.list())[0]; ZQ.state.bankResult({ results: [{ uid, ok: false, seconds: 9, family: 'x' }] }); const r = ZQ.state.bank.entry(uid); return { uid, box: r.box, miss: r.miss, days: Math.round((r.due - Date.now()) / 8640000) / 10 }; });
        if (miss.box !== 1 || miss.miss !== 1 || Math.abs(miss.days - 1) > 0.1) fails.push(`a miss should be box 1, due in 1 day: ${JSON.stringify(miss)}`);
        await skew(2 * 86400);
        const two = await page.evaluate(() => ZQ.select.bankDeck({ n: 500 }).then(a => ({ first: a.map(x => x.uid), due: ZQ.state.bank.due() })));
        if (two.due.length !== 1 || two.due[0] !== miss.uid) fails.push(`two days on, only the missed item should be due: ${JSON.stringify(two.due)}`);
        if (!two.first.includes(miss.uid)) fails.push('the due item is not in the next deck');
        await skew(40 * 86400);
        const all = await page.evaluate(() => ({ due: ZQ.state.bank.due().length, n: Object.keys(ZQ.state.bank.list()).length }));
        if (all.due !== all.n) fails.push(`40 days on every scheduled item should be due: ${all.due} of ${all.n}`);
        /* 6. an old save with no bank or timing loads and still works */
        const old = await page.evaluate(() => { const d = JSON.parse(ZQ.state.export()); delete d.bank; delete d.timing; const r = ZQ.state.import(JSON.stringify(d)); const b = ZQ.state.bank.list(); ZQ.state.bankResult({ results: [{ uid: 'bank/x/x', ok: true, seconds: 2, family: 'f' }] }); return { ok: r.ok, empty: Object.keys(b).length === 0, after: Object.keys(ZQ.state.bank.list()).length, fam: Object.keys(ZQ.state.timing.families).length }; });
        if (!old.ok || !old.empty || old.after !== 1 || old.fam !== 1) fails.push(`an old save without bank or timing did not load cleanly: ${JSON.stringify(old)}`);
        await unskew();
        console.log(`${fails.length ? 'FAIL' : 'ok  '} #bank  ${open.length} drawable of ${items.length} in ${docs.length} files (${lockedN} locked), deck, pace line, schedule, miss, old save, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log('FAIL #bank  threw');
      }
      try { await unskew(); } catch { /* page gone */ }
      fails.forEach(f => failures.push(`#bank: ${f}`));
    };

    /* ---------- --bank <file>: every item of one bank file, dealt through the deck and answered right from its key ----------
       Items still locked by `requires` are unlocked by importing a save with those lessons finished; every other drawable item is
       walked to the 30-day box so the deck holds only the file's items (the schedule is cleared before each file). Reports pass or fail per item. */
    const bankPlay = async (ids) => {
      const dir = path.join(CONTENT, 'bank');
      const names = fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => /^[a-z0-9-]+\.json$/.test(f)).map(f => f.replace(/\.json$/, '')).sort() : [];
      const want = ids.includes('all') ? names : ids;
      for (const id of want) if (!names.includes(id)) die(`--bank ${id}: no such file in content/bank (${names.join(', ')})`);
      let tot = 0, bad = 0;
      for (const id of want) {
        where = `#bank/${id}`;
        const doc = readJSON(path.join(dir, id + '.json')), t0 = Date.now();
        const byUid = {}; doc.items.forEach(it => { byUid[`bank/${doc.id}/${it.id}`] = it; });
        const mine = Object.keys(byUid), reqs = [...new Set(doc.items.flatMap(it => it.requires || []))];
        const res = {}, note = (uid, msg) => { if (!res[uid]) res[uid] = msg; };
        try {
          const imp = await page.evaluate((reqs) => { const d = JSON.parse(ZQ.state.export()); delete d.bank; d.lessons = d.lessons || {}; reqs.forEach(r => { if (!d.lessons[r] || !d.lessons[r].done) d.lessons[r] = { attempts: 1, done: true, firstTry: true, xp: 0, bestQuiz: 1, mastered: false, perfect: false, completedAt: Date.now(), secondsSpent: 600, position: null, positionAt: null }; }); return ZQ.state.import(JSON.stringify(d)); }, reqs);
          if (!imp || !imp.ok) throw new Error('could not import the unlocking save');
          const drawable = await page.evaluate(() => ZQ.select.bankDeck({ n: 2000 }).then(a => a.map(x => x.uid)));
          mine.filter(u => !drawable.includes(u)).forEach(u => note(u, 'not drawable after unlocking its requires'));
          const others = drawable.filter(u => !mine.includes(u));
          await page.evaluate((us) => { for (let k = 0; k < 4; k++) ZQ.state.bankResult({ results: us.map(uid => ({ uid, ok: true, seconds: 1, family: 'x' })) }); }, others);
          await page.evaluate(() => { if (!window.__deals) { const orig = ZQ.select.bankDeck; window.__deals = []; ZQ.select.bankDeck = async (o) => { const a = await orig(o); window.__deals.push(a.map(x => x.uid)); return a; }; } });
          const played = new Set(), todo = () => mine.filter(u => !played.has(u) && !res[u]);
          for (let sit = 0; sit < Math.ceil(mine.length / 8) + 4 && todo().length; sit++) {
            await go('review');
            await page.evaluate(() => { delete window.ZQ.test; });
            await go('bank');
            await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind === 'start', null, { timeout: opt.timeout });
            await page.evaluate(() => ZQ.test.continue());
            await page.waitForFunction(() => ZQ.test.current().kind === 'item', null, { timeout: opt.timeout });
            const deal = await page.evaluate(() => window.__deals[window.__deals.length - 1]);
            let guard = 0;
            while ((await page.evaluate(() => ZQ.test.current().kind)) !== 'done' && ++guard < 40) {
              const c = await page.evaluate(() => ZQ.test.current());
              if (c.kind === 'item' && (c.state === 'idle' || c.state === 'engaged')) {
                const uid = deal[c.screenIndex], it = byUid[uid];
                if (!it) { await page.evaluate(() => ZQ.test.answerCorrect()); await page.evaluate(() => ZQ.test.check()); }
                else {
                  if (!(await page.evaluate(() => ZQ.test.answerCorrect()))) note(uid, 'answerCorrect had nothing to answer');
                  if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)) note(uid, 'the page is wider than the window');
                  let r = await page.evaluate(() => ZQ.test.check().then(r => r && { ok: !!r.ok }));
                  if (it.widget.kind === 'longform') {
                    await page.evaluate(() => { [...document.querySelectorAll('input[type=checkbox]')].filter(n => n.offsetParent && !n.checked).forEach(b => b.click()); });
                    const r2 = await page.evaluate(() => ZQ.test.check().then(r => r && { ok: !!r.ok }));
                    const last = await page.evaluate(() => { const x = ZQ.test.results(); return x.length ? !!x[x.length - 1].ok : false; });
                    r = { ok: (r2 && r2.ok) || (r && r.ok) || last };
                  }
                  if (!r || !r.ok) note(uid, 'the right answer was not accepted'); else played.add(uid);
                }
              }
              await page.evaluate(() => ZQ.test.continue());
              await page.waitForTimeout(100);
            }
          }
          mine.filter(u => !played.has(u)).forEach(u => note(u, 'never dealt'));
          if (opt.shots) await shot(`bank-${id}`);
        } catch (e) { mine.forEach(u => note(u, 'threw: ' + String(e.message || e).split('\n')[0])); }
        const badN = mine.filter(u => res[u]).length;
        mine.forEach(u => { if (res[u]) { console.log(`FAIL ${u}: ${res[u]}`); failures.push(`#bank/${id}: ${u}: ${res[u]}`); } });
        console.log(`${badN ? 'FAIL' : 'ok  '} --bank ${id}  ${mine.length - badN} of ${mine.length} items right from the key${reqs.length ? `, ${reqs.length} requires lessons unlocked` : ''}, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
        tot += mine.length; bad += badN;
      }
      console.log(`bank total: ${tot - bad} of ${tot} items passed in ${want.length} file${want.length === 1 ? '' : 's'}`);
    };
    /* An exam sat with Date.now skewed: item 3 takes 90 s, the others 4 s. The result has a pace line and per-question
       seconds, and the attempt keeps itemSeconds, one per question. Time never changes the marks (everything is right). */
    const paceExamChecks = async (ex) => {
      const doc = readJSON(path.join(CONTENT, 'exams', ex + '.json'));
      await playSet(`exam/${ex}`, `${ex}-pace`, async () => {
        const c = await page.evaluate(() => ZQ.test.current());
        if (c.kind !== 'done') return { fail: 'the result page was not reached' };
        const r = await page.evaluate((id) => { const a = ((ZQ.state.exams[id] || {}).attempts || []).slice(-1)[0] || {}; return { secs: a.itemSeconds || null, line: (document.querySelector('.exm-pace') || {}).textContent || '', meta: [...document.querySelectorAll('.exm-ri-meta')].filter(n => / s(\b| of)/.test(n.textContent)).length, fam: Object.keys(ZQ.state.timing.families).length, wide: document.documentElement.scrollWidth > window.innerWidth + 1 }; }, ex);
        const bad = [];
        if (!r.secs || r.secs.length !== c.total) bad.push(`itemSeconds has ${r.secs ? r.secs.length : 'none'}, ${c.total} questions`);
        else if (Math.max(...r.secs) < 85) bad.push(`no question shows the 90 s one: ${Math.max(...r.secs)}`);
        if (!/Average .* a question/.test(r.line)) bad.push(`no pace line on the result: "${r.line}"`);
        if (!r.meta) bad.push('no question shows its seconds');
        if (!r.fam) bad.push('no per-family timing was logged from the exam');
        if (r.wide) bad.push('the result page is wider than the window');
        if (!c.passed || c.score !== c.total) bad.push(`time changed the marks: ${c.score} of ${c.total}`);
        await shot(`${ex}-pace-result`);
        return { fail: bad.length ? bad.join('; ') : null, note: `pace line "${r.line.slice(0, 60)}..."` };
      }, 1, async (c, n) => { await skew(n === 2 ? 90 : 4); });
      await unskew();
      void doc;
    };

    /* ---------- Drill library (ENGINE-BACKLOG 472): --drill <id>, --drills, --session ----------
       Each drill is opened at #drill/<id>: the starter (touched, so it can be submitted) must fail, the model solution must
       pass every hidden test and verify the drill, the stopwatch must read and be recorded with the result (Date.now is
       moved on 130 s while the drill is open; no real minutes are waited), and with --mobile the whole run is at 390 px
       with no sideways scroll. --session sits the sample session (content/drills/sessions/sample-session.json): both
       drills with their model solutions, minutes per drill from a moved clock, the result screen, what a lesson reads as
       {{carry.session.*}}, a session whose clock is moved to zero, and one that survives leaving the page. */
    const drillIdsAll = () => fs.readdirSync(path.join(CONTENT, 'drills')).filter(f => f.endsWith('.json') && f !== 'index.json').map(f => f.replace(/\.json$/, '')).sort();
    const skewBy = (ms) => page.evaluate((n) => { if (!window.__zqNow) { window.__zqNow = Date.now.bind(Date); window.__zqSkew = 0; Date.now = () => window.__zqNow() + window.__zqSkew; } window.__zqSkew += n; }, ms);
    const unskewClock = () => page.evaluate(() => { if (window.__zqNow) { Date.now = window.__zqNow; delete window.__zqNow; delete window.__zqSkew; } });
    const wide = () => page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    const drillReady = async (cpp) => {
      const wait = cpp ? 300000 : 90000;
      try { await page.waitForFunction(() => window.ZQDrill && ZQDrill.status() === 'ready', null, { timeout: Math.max(opt.timeout, wait) }); return null; }
      catch { return `${cpp ? 'The C++ compiler' : 'Python'} did not become ready within ${wait / 1000} s`; }
    };
    /* submit through the hook and wait until the run has finished; resolves to { ok, passed, total } */
    const drillSubmit = async () => {
      await page.evaluate(() => { window.__zqSub = ZQDrill.submit(); });
      await page.waitForFunction(() => { const r = ZQDrill.results(); return r && r.mode === 'submit' && (r.res ? r.res.every(x => !['pending', 'running'].includes(x.status)) : true); }, null, { timeout: 180000 });
      await page.evaluate(() => window.__zqSub);
      return page.evaluate(() => { const r = ZQDrill.results(); return r.res ? { ok: r.res.every(x => x.status === 'pass'), passed: r.res.filter(x => x.status === 'pass').length, total: r.res.length } : { ok: r.ok, passed: r.passed, total: r.total }; });
    };
    const drillOne = async (id) => {
      const file = readJSON(path.join(CONTENT, 'drills', id + '.json')), cpp = file.language === 'cpp', mine = [];
      where = '#drill/' + id;
      const before = consoleErrors.length;
      try {
        await go('drill/' + id);
        await page.waitForFunction(() => window.ZQDrill, null, { timeout: opt.timeout });
        const bad = await drillReady(cpp);
        if (bad) { mine.push(bad); throw new Error(bad); }
        if (opt.mobile && await wide()) mine.push('the page is wider than the 390 px window');
        const pill0 = await page.evaluate(() => { const t = document.querySelector('.drl-sw-t'); return t ? t.textContent : null; });
        if (!pill0 || !/^\d+:\d\d$/.test(pill0)) mine.push(`the stopwatch pill is missing or unreadable (${pill0})`);
        await shot('drill-' + id);
        const lang = await page.evaluate(() => ZQDrill.language);
        if (lang !== (cpp ? 'cpp' : 'python')) mine.push(`opened as ${lang}, the file says ${cpp ? 'cpp' : 'python'}`);
        /* the starter, touched so Submit accepts it, must fail */
        await page.evaluate((s) => ZQDrill.setCode(s), file.starter + (cpp ? '\n// starter check\n' : '\n# starter check\n'));
        const st = await drillSubmit();
        if (st.ok) mine.push('the starter passes every hidden test');
        /* the model solution must pass every test, with the stopwatch moved on */
        await skewBy(130000);
        await page.evaluate((s) => ZQDrill.setCode(s), file.solution);
        const ref = await drillSubmit();
        if (!ref.ok) mine.push(`the model solution passes ${ref.passed} of ${ref.total} hidden tests${await codeWhy()}`);
        const want = (file.tests || []).length;
        if (ref.total !== want) mine.push(`${ref.total} tests ran, the file has ${want}`);
        const info = await page.evaluate((id2) => ({ verified: ZQDrill.verified(), seconds: ZQDrill.seconds(), rec: ZQ.state.drills.get(id2), pill: (document.querySelector('.drl-sw-t') || {}).textContent, over: !!document.querySelector('.drl-sw.is-over') }), id);
        if (!info.verified) mine.push('the drill is not marked verified after the model solution');
        if (info.seconds < 129) mine.push(`the stopwatch read ${info.seconds} s after the clock moved 130 s`);
        const run = info.rec && info.rec.runs && info.rec.runs[info.rec.runs.length - 1];
        if (!run || !run.ok || run.seconds < 129 || run.total !== want) mine.push(`the record holds ${JSON.stringify(run)}; expected a passing run of ${want} tests after 129 s or more`);
        if (!info.rec || !info.rec.verified || typeof info.rec.best !== 'number' || info.rec.best < 129) mine.push(`the record has no best time (${JSON.stringify(info.rec && { verified: info.rec.verified, best: info.rec.best })})`);
        if (file.pace && file.pace < 125 && !info.over) mine.push('the stopwatch is not marked over a pace shorter than its reading');
        const m = /^(\d+):(\d\d)$/.exec(info.pill || '');
        if (!m || +m[1] * 60 + +m[2] < 129) mine.push(`the stopwatch pill shows ${info.pill}`);
        await shot('drill-' + id + '-verified');
        if (opt.mobile && await wide()) mine.push('after the run the page is wider than the 390 px window');
        console.log(`${mine.length ? 'FAIL' : 'ok  '} --drill ${id}  ${cpp ? 'C++' : 'Python'}, ${ref.passed} of ${ref.total} tests with the model solution, starter fails: ${!st.ok}`);
      } catch (e) { if (!mine.length) mine.push('threw ' + String(e.message || e).split('\n')[0]); console.log(`FAIL --drill ${id}  ${mine[0]}`); }
      mine.forEach(x => failures.push(`drill ${id}: ${x}`));
      if (consoleErrors.length > before) console.log(`ERR  ${where}`);
      await page.evaluate(() => { location.hash = '#today'; });
      await page.waitForTimeout(300);
    };
    const sessionPlay = async () => {
      const SID = 'sample-session';
      if (!fs.existsSync(path.join(CONTENT, 'drills', 'sessions', SID + '.json'))) { failures.push('session: content/drills/sessions/sample-session.json is missing'); return; }
      const sdoc = readJSON(path.join(CONTENT, 'drills', 'sessions', SID + '.json'));
      const files = sdoc.drills.map(i => readJSON(path.join(CONTENT, 'drills', i + '.json')));
      const bad = (m) => { failures.push('session: ' + m); console.log('FAIL --session  ' + m); };
      const probs = failures.length;
      where = '#drill/session';
      try {
        await page.evaluate(() => { ZQ.store.set('drill.session', null); });
        await go('drill/session/' + SID);
        await page.waitForSelector('[data-start]', { timeout: opt.timeout });
        const picks = await page.evaluate(() => [...document.querySelectorAll('.drls-pick .t-label')].map(x => x.textContent));
        if (picks.length !== 2 || picks[0] !== files[0].name || picks[1] !== files[1].name) bad(`the setup shows ${JSON.stringify(picks)}, the file lists ${JSON.stringify(files.map(f => f.name))}`);
        if (opt.mobile && await wide()) bad('the setup page is wider than the 390 px window');
        await shot('session-setup');
        await page.click('[data-start]');
        await page.waitForFunction(() => window.ZQSession && ZQSession.state && ZQSession.state().ids, null, { timeout: opt.timeout });
        const s0 = await page.evaluate(() => ZQSession.state());
        if (s0.cur !== 0 || s0.ids.join() !== sdoc.drills.join() || s0.left > 3600 || s0.left < 3590) bad(`a fresh session reads ${JSON.stringify(s0)}`);
        /* leaving the page keeps the clock and the session */
        await go('today');
        await go('drill/session');
        await page.waitForFunction(() => window.ZQSession && ZQSession.state && ZQSession.state().ids, null, { timeout: opt.timeout });
        for (let i = 0; i < 2; i++) {
          if (i === 1) await page.evaluate(() => ZQSession.switchTo(1));
          await page.waitForFunction((id) => window.ZQDrill && ZQDrill.problem() === id, sdoc.drills[i], { timeout: opt.timeout });
          const rd = await drillReady(files[i].language === 'cpp');
          if (rd) { bad(rd); return; }
          if (i === 0 && opt.mobile && await wide()) bad('the session page is wider than the 390 px window');
          if (i === 0) await shot('session-running');
          const sw = await page.evaluate(() => !!document.querySelector('.drl-sw'));
          if (sw) bad('a session drill shows its own stopwatch beside the session clock');
          await skewBy(i === 0 ? 600000 : 900000);
          await page.evaluate((s) => ZQDrill.setCode(s), files[i].solution);
          const r = await drillSubmit();
          if (!r.ok) bad(`drill ${i + 1} (${sdoc.drills[i]}): the model solution passes ${r.passed} of ${r.total}`);
        }
        const s1 = await page.evaluate(() => ZQSession.state());
        const [a, b] = s1.per;
        if (!(a.seconds >= 595 && a.seconds <= 900) || !(s1.left < 3600 - 1490) || !a.ok || !b.ok || a.passed !== a.total || b.passed !== b.total || !a.total || !b.total) bad(`before finishing the session reads ${JSON.stringify(s1)}`);
        await page.evaluate(() => ZQSession.finish());
        await page.waitForSelector('.drls-table', { timeout: opt.timeout });
        const res = await page.evaluate(() => ({ h: document.querySelector('h1').textContent, rows: [...document.querySelectorAll('.drls-table tbody tr')].map(r => r.innerText.replace(/\s+/g, ' ')), sum: (document.querySelector('.drls-sum') || {}).textContent, rec: ZQ.state.drills.sessions(), R: ZQSession.result() }));
        if (!/^2 of 2 drills solved$/.test(res.h)) bad(`the result says "${res.h}"`);
        const mins = (r) => +((/(\d+) min/.exec(r) || [])[1] || 0);
        if (res.rows.length !== 2 || !res.rows[0].includes(files[0].name) || mins(res.rows[0]) < 10 || mins(res.rows[0]) > 14 || mins(res.rows[1]) < 15 || mins(res.rows[1]) > 19 || !res.rows.every(r => /(\d+) of \1/.test(r))) bad(`the result rows read ${JSON.stringify(res.rows)}`);
        const usedMin = +((/used (\d+) min/.exec(res.sum || '') || [])[1] || 0);
        if (usedMin < 25 || usedMin > 34) bad(`the result summary reads "${res.sum}"`);
        const last = res.rec[res.rec.length - 1];
        if (!last || last.drills.length !== 2 || last.drills[0].id !== sdoc.drills[0] || !last.drills.every(d => d.ok && d.total > 0 && d.passed === d.total) || last.minutes !== 60) bad(`the state holds ${JSON.stringify(last)}`);
        if (opt.mobile && await wide()) bad('the result page is wider than the 390 px window');
        await shot('session-result');
        const carry = await page.evaluate(() => { ZQ.player.carryReset(); return ZQ.carry.session; });
        if (!carry || !(carry.minutes1 >= 10 && carry.minutes1 < 14.5) || !(carry.minutes2 >= 15 && carry.minutes2 < 19.5) || carry.solved !== 2 || carry.passed1 !== carry.total1 || !carry.total2) bad(`a lesson would read carry.session = ${JSON.stringify(carry)}`);
        /* a session whose clock is moved to zero closes itself and keeps what was done */
        await go('drill/session/' + SID);
        await page.waitForSelector('[data-start]', { timeout: opt.timeout });
        await page.click('[data-start]');
        await page.waitForFunction(() => window.ZQSession && ZQSession.state && ZQSession.state().ids, null, { timeout: opt.timeout });
        await page.evaluate(() => ZQSession.setRemaining(2));
        await page.waitForSelector('.drls-table', { timeout: 15000 });
        const out = await page.evaluate(() => ({ h: document.querySelector('h1').textContent, sum: (document.querySelector('.drls-sum') || {}).textContent, n: ZQ.state.drills.sessions().length }));
        if (!/0 of 2 drills solved/.test(out.h) || !/the clock ran out/.test(out.sum || '')) bad(`an expired session reads "${out.h}" / "${out.sum}"`);
        if (out.n !== res.rec.length + 1) bad(`${out.n} sessions are kept after two were sat, expected ${res.rec.length + 1}`);
        console.log(`${failures.length > probs ? 'FAIL' : 'ok  '} --session  sample session: both model solutions, minutes per drill ${(a.seconds / 60).toFixed(1)} and ${(b.seconds / 60).toFixed(1)}, result, carry, expiry, resume`);
      } catch (e) { bad('threw ' + String(e.message || e).split('\n')[0]); }
      await page.evaluate(() => { ZQ.store.set('drill.session', null); location.hash = '#today'; });
      await page.waitForTimeout(300);
    };
    /* the cheap checks, part of --routes-only: filters, the session setup and what the list hides */
    const drillRouteChecks = async () => {
      const listed = readJSON(path.join(CONTENT, 'drills', 'index.json')).map(d => d.id || d);
      const meta = listed.map(i => readJSON(path.join(CONTENT, 'drills', i + '.json')));
      const fails = [];
      where = '#drill (filters)';
      try {
        await page.evaluate(() => ZQ.store.set('drill.filters', null));
        await go('drill');
        await page.waitForSelector('.drlf', { timeout: opt.timeout });
        const count = () => page.evaluate(() => document.querySelectorAll('.drl-l-item').length);
        if (await count() !== listed.length) fails.push(`the list shows ${await count()} drills, index.json has ${listed.length}`);
        const hidden = await page.evaluate(() => !!document.querySelector('a[href^="#drill/sample-"]'));
        if (hidden) fails.push('a sample drill is listed');
        await page.selectOption('[data-f="min"]', '4');
        const hard = meta.filter(d => (d.difficulty || 2) >= 4).length;
        if (await count() !== hard) fails.push(`difficulty 4 to 5 lists ${await count()} drills, ${hard} qualify`);
        await page.selectOption('[data-f="max"]', '3');
        const clamp = await page.evaluate(() => ({ min: document.querySelector('[data-f="min"]').value, max: document.querySelector('[data-f="max"]').value }));
        if (+clamp.min > +clamp.max) fails.push(`the difficulty range is upside down (${clamp.min} to ${clamp.max})`);
        await page.selectOption('[data-f="language"]', 'cpp');
        if (await count() !== meta.filter(d => d.language === 'cpp' && (d.difficulty || 2) >= +clamp.min && (d.difficulty || 2) <= +clamp.max).length) fails.push('the language filter C++ lists the wrong drills');
        const msg = await page.evaluate(() => /No drill matches/.test(document.querySelector('.drl-l-groups').textContent));
        if (!msg && await count() === 0) fails.push('an empty filter result gives no message');
        if (opt.mobile && await wide()) fails.push('the filtered list is wider than the window');
        await shot('route-drill-filtered');
        const logic = await page.evaluate(() => {
          const L = ZQ.drillLib, list = [{ id: 'a', pattern: 'bits', difficulty: 2 }, { id: 'b', pattern: 'intervals', difficulty: 4, language: 'cpp' }, { id: 'c', pattern: 'intervals', difficulty: 3 }];
          const f = (o) => L.filterList(list, { pattern: '', min: 1, max: 5, language: '', ...o }).map(x => x.id).join('');
          return [f({}), f({ pattern: 'intervals' }), f({ language: 'cpp' }), f({ language: 'python' }), f({ min: 3, max: 3 }), f({ pattern: 'intervals', min: 4 })];
        });
        if (logic.join('|') !== 'abc|bc|b|ac|c|b') fails.push(`filterList gave ${logic.join('|')}`);
        await page.evaluate(() => ZQ.store.set('drill.filters', null));
        /* the session setup: a pick of two for any filters, and the set session when named */
        await go('drill/session/new');
        await page.waitForSelector('[data-start]', { timeout: opt.timeout });
        const n = await page.evaluate(() => document.querySelectorAll('.drls-pick').length);
        if (n !== 2) fails.push(`the session setup picks ${n} drills`);
        if (opt.mobile && await wide()) fails.push('the session setup is wider than the window');
        await shot('route-drill-session');
        await go('drill/sample-cpp-row-sums');
        await page.waitForFunction(() => window.ZQDrill, null, { timeout: opt.timeout });
        await page.evaluate(() => { location.hash = '#today'; });
      } catch (e) { fails.push('threw ' + String(e.message || e).split('\n')[0]); }
      fails.forEach(x => failures.push('drill library: ' + x));
      console.log(`${fails.length ? 'FAIL' : 'ok  '} drill filters and session setup`);
    };
    const drillPhase = opt.drillIds.length || opt.drillsAll || opt.sessionRun;
    if (drillPhase) {
      const ids = opt.drillsAll ? drillIdsAll() : opt.drillIds;
      for (const id of ids) if (!drillIdsAll().includes(id)) die(`--drill ${id}: no such file in content/drills`);
      if (opt.mobile) { await page.setViewportSize({ width: 390, height: 844 }); await page.waitForTimeout(300); }
      for (const id of ids) await drillOne(id);
      if (opt.sessionRun || opt.drillsAll) await sessionPlay();
      await unskewClock();
      if (opt.mobile) { await page.setViewportSize({ width: 1280, height: 860 }); await page.waitForTimeout(200); }
    }

    /* Every other route once */
    if (opt.bankIds.length) await bankPlay(opt.bankIds);
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
      /* The interview bank deck and per-item timing (ENGINE-BACKLOG 456, 457), then an exam sat with a skewed clock */
      await bankChecks();
      await drillRouteChecks();
      const paceExam = fs.existsSync(path.join(CONTENT, 'exams', 'mock-sample.json')) ? 'mock-sample' : exams.includes('topic-1.5') ? 'topic-1.5' : null;
      if (paceExam) await paceExamChecks(paceExam);
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
