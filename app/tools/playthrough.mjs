#!/usr/bin/env node
/* Playthrough (docs/PLAN.md section 11): plays every written lesson with its authored answers, then opens every
   other route once, and fails on any check that is not correct, any lesson that does not reach its completion
   screen, and any console error.

   Usage (from the repository root or anywhere):
     node app/tools/playthrough.mjs                        every written lesson, then every route
     node app/tools/playthrough.mjs --lesson conditional/l3-shrinking     one lesson (add --routes for the routes too)
     node app/tools/playthrough.mjs --routes-only          only the routes
     node app/tools/playthrough.mjs --shots out/shots      a screenshot per lesson screen and per route
     node app/tools/playthrough.mjs --local-cdn <dir>      serve cdn.jsdelivr.net from local npm packages (see below)
     node app/tools/playthrough.mjs --headed               watch it

   Needs Playwright (the globally installed package is found too) and Chromium at /opt/pw-browsers/chromium, else
   Playwright's own. Starts `python3 -m http.server` on a free port serving app/. A fresh browser profile is used, setup
   is completed through its form, then each lesson opens at #lesson/<course>/<lesson> and is driven through
   window.ZQ.test: answerCorrect(), check(), continue(), until current().kind is 'done'.

   --local-cdn <dir>: for machines without access to cdn.jsdelivr.net. <dir> holds unpacked npm tarballs:
     <dir>/pyodide-0.27.7/package/...                      for /pyodide/v0.27.7/full/...
     <dir>/mathlive-0.105.0/package/...                    for /npm/mathlive@0.105.0/...
     <dir>/cortex-js-compute-engine-0.30.2/package/...     for /npm/@cortex-js/compute-engine@0.30.2/...
   (npm pack pyodide@0.27.7 mathlive@0.105.0 @cortex-js/compute-engine@0.30.2, then untar each into <name>-<version>/.)
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
const opt = { lessons: [], shots: null, localCdn: null, routes: null, lessonsOn: true, headed: false, timeout: 20000 };
for (let i = 0; i < argv.length; i++) {
  const a = argv[i], next = () => { const v = argv[++i]; if (v == null || v.startsWith('--')) die(`${a} needs a value`); return v; };
  if (a === '--lesson') opt.lessons.push(next());
  else if (a === '--shots') opt.shots = path.resolve(next());
  else if (a === '--local-cdn') { const v = argv[i + 1]; if (v && !v.startsWith('--')) { opt.localCdn = path.resolve(v); i++; } else opt.localCdn = process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : die('--local-cdn needs a directory (or set ZQ_LOCAL_CDN)'); }
  else if (a === '--routes') opt.routes = true;
  else if (a === '--no-routes') opt.routes = false;
  else if (a === '--routes-only') { opt.routes = true; opt.lessonsOn = false; }
  else if (a === '--headed') opt.headed = true;
  else if (a === '--help' || a === '-h') { console.log(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('*/')[0].replace(/^#!.*\n\/\* ?/, '')); process.exit(0); }
  else die(`unknown argument ${a} (try --help)`);
}
if (opt.routes == null) opt.routes = opt.lessons.length === 0;
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
  return { lessons: out, courses: order.filter(c => fs.existsSync(path.join(CONTENT, 'courses', c, 'course.json'))) };
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
  const { lessons: allLessons, courses } = writtenLessons();
  const lessons = opt.lessonsOn ? (opt.lessons.length ? opt.lessons : allLessons) : [];
  for (const l of opt.lessons) if (!allLessons.includes(l)) die(`--lesson ${l}: no such written lesson (the file must exist and be listed in its course.json)`);
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

    const shot = async (name) => { if (opt.shots) { await page.waitForTimeout(300); await page.screenshot({ path: path.join(opt.shots, name.replace(/[^\w.-]+/g, '_') + '.png') }); } };
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
    console.log(`setup done. ${lessons.length} lesson${lessons.length === 1 ? '' : 's'} to play.`);

    /* Lessons */
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
            const applied = await page.evaluate(() => ZQ.test.answerCorrect());
            const r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, key: r.key ?? null, pending: !!r.pending } : null; });
            if (r && r.pending) { // long-form: the first check opens the self-marking, the second grades it
              await page.evaluate(() => ZQ.test.answerCorrect());
              const r2 = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, key: r.key ?? null } : null; });
              checks++;
              if (r2 && !r2.ok) fails.push(`${c.phase} ${c.screenIndex} (${c.kind}): not correct, key ${JSON.stringify(r2.key)}`);
            } else if (r) {
              checks++;
              if (!r.ok) fails.push(`${c.phase} ${c.screenIndex} (${c.kind}): not correct, key ${JSON.stringify(r.key)}`);
            } else if (c.state === 'idle' && applied === false && c.kind !== 'title' && c.kind !== 'demonstrate' && c.kind !== 'generalise') {
              fails.push(`${c.phase} ${c.screenIndex} (${c.kind}): answerCorrect() could not apply the authored answer`);
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

    /* Every other route once */
    if (opt.routes) {
      const exams = fs.existsSync(path.join(CONTENT, 'exams')) ? fs.readdirSync(path.join(CONTENT, 'exams')).filter(f => /^topic-.*\.json$/.test(f)).map(f => f.replace(/\.json$/, '')) : [];
      const drills = fs.existsSync(path.join(CONTENT, 'drills', 'index.json')) ? readJSON(path.join(CONTENT, 'drills', 'index.json')).map(d => d.id || d) : [];
      const routes = ['today', 'learn', ...courses.map(c => `course/${c}`), 'review', 'you', 'system', 'drill',
        ...drills.slice(0, 1).map(d => `drill/${d}`), ...(exams.includes('topic-1.5') ? ['exam/topic-1.5'] : exams.slice(0, 1).map(e => `exam/${e}`)), 'setup'];
      for (const r of routes) {
        where = '#' + r;
        const before = consoleErrors.length;
        try {
          await go(r);
          const blank = await page.evaluate(() => { const a = document.querySelector('#app'); return !a || a.innerText.trim().length < 20 || /This screen failed to render/.test(a.innerText); });
          if (blank) failures.push(`#${r}: the screen is empty or failed to render`);
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
