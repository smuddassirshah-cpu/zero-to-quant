#!/usr/bin/env node
/* Playthrough (docs/PLAN.md section 11): plays every written lesson with its authored answers, then opens every
   other route once, and fails on any check that is not correct, any lesson that does not reach its completion
   screen, and any console error. With --sets it also plays every written level review and homework, and with
   --exams every exam, through the set-mode test hook (window.ZQ.test), answering each item correctly.

   Usage (from the repository root or anywhere):
     node app/tools/playthrough.mjs                        every written lesson, then every route
     node app/tools/playthrough.mjs --all                  lessons, routes, every review and homework, every exam
     node app/tools/playthrough.mjs --all --shard 2/4      only every 4th item of the full ordered item list (lessons, then sets, then exams), starting at the 2nd: shard i of n
                                                           (1-based) runs the items whose zero-based index % n === i-1, so shards 1/4 to 4/4 cover each item once. The routes and
                                                           their checks run in shard 1 only; --routes-only with any other shard has no items and passes with a note. Prints "shard i/n: K of N items"
     node app/tools/playthrough.mjs --all --list           print the item ids (lesson/, set/, exam/) the run would play, one per line, and exit (works with --shard; no browser)
     node app/tools/playthrough.mjs --sets                 every written level review and homework only
     node app/tools/playthrough.mjs --exams                every exam in content/exams only (combine with --sets)
     node app/tools/playthrough.mjs --set number-sense/review-1   one review or homework (repeatable)
     node app/tools/playthrough.mjs --exam topic-1.5       one exam (repeatable); topic-*, stage-* and mock-* all play the same way
     node app/tools/playthrough.mjs --lesson conditional/l3-shrinking     one lesson (add --routes for the routes too)
     node app/tools/playthrough.mjs --bank probability-1   every item of one bank file (repeatable, or --bank all): dealt, answered right from its key, pass or fail per item
     node app/tools/playthrough.mjs --drill sample-cpp-row-sums   one drill (repeatable; --drills for every file in content/drills): the starter fails, the model
                                                           solution passes every hidden test, the stopwatch is read and recorded (add --mobile, --narrow or --tablet to repeat it at those sizes)
     node app/tools/playthrough.mjs --session              the sample drill session: both drills, minutes per drill, result, carry, expiry (--drills includes it)
     node app/tools/playthrough.mjs --routes-only          (also: mock-oa-code holdout and resit checks, mock versions in Prepare) only the routes, then the interview bank deck (due and new items, the 3-day box,
                                                           a miss, prerequisites, an old save, the pace line) and one exam sat with a
                                                           skewed Date.now so per-item seconds and the pace line are checked
     node app/tools/playthrough.mjs --shots out/shots      a screenshot per lesson screen and per route
     node app/tools/playthrough.mjs --shots out --mobile   also a 440 x 956 screenshot of each (name-440.png): the user's phone, iPhone 17 Pro Max
     node app/tools/playthrough.mjs --narrow               the old 390 x 844 pass (name-390.png), the stricter width; combine with --mobile
     node app/tools/playthrough.mjs --tablet               1032 x 1376 and 1376 x 1032 passes (name-1032.png, name-1376.png): iPad Pro 13-inch,
                                                           portrait and landscape. Every width gets the same "page is wider than the window"
                                                           checks. --mobile --tablet runs desktop (1280 x 860), phone and both tablet orientations.
                                                           The passes resize the window; touch is NOT emulated (no hasTouch or isMobile)
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
   Items with `parts` (ENGINE-BACKLOG 467) are answered part by part through the same hook (current() carries part and parts; continue()
   opens the next part before it moves on), code parts included. A timed review with a parts item is also sat to zero in part 2 (credit
   on the summary, the rest missed); a homework with a three-part item is sat with the last part left open (the draft keeps the open
   parts, the item is marked by its credit and is not right); a mock with a parts item is sat answering part 1 only (net score from the
   credit, "1 of n parts" on the result). A mock with `draw` (468) is checked for seeds (same seed, same items), balance across
   families, unseen items first, and the attempt's `drawn` and `seed`. Engine samples ("sample": true) are played with everything else
   and must stay out of the mock list, the bank deck, the drill list and the Review, Drill and You pages (checked with the routes).

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
const opt = { mobile: false, narrow: false, tablet: false, why: false, lessons: [], shots: null, localCdn: null, routes: null, lessonsOn: true, headed: false, timeout: 20000, sets: false, exams: false, setIds: [], examIds: [], bankIds: [], drillIds: [], drillsAll: false, sessionRun: false, all: false, shard: null, list: false };
for (let i = 0; i < argv.length; i++) {
  const a = argv[i], next = () => { const v = argv[++i]; if (v == null || v.startsWith('--')) die(`${a} needs a value`); return v; };
  if (a === '--lesson') opt.lessons.push(next());
  else if (a === '--shots') opt.shots = path.resolve(next());
  else if (a === '--local-cdn') { const v = argv[i + 1]; if (v && !v.startsWith('--')) { opt.localCdn = path.resolve(v); i++; } else opt.localCdn = process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : die('--local-cdn needs a directory (or set ZQ_LOCAL_CDN)'); }
  else if (a === '--mobile') opt.mobile = true;
  else if (a === '--narrow') opt.narrow = true;
  else if (a === '--tablet') opt.tablet = true;
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
  else if (a === '--list') opt.list = true;
  else if (a === '--shard') { const v = next(), m = /^(\d+)\/(\d+)$/.exec(v); if (!m || +m[1] < 1 || +m[2] < 1 || +m[1] > +m[2]) die(`--shard needs i/n with 1 <= i <= n (for example 2/4), got "${v}"`); opt.shard = { i: +m[1], n: +m[2] }; }
  else if (a === '--help' || a === '-h') { console.log(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('*/')[0].replace(/^#!.*\n\/\* ?/, '')); process.exit(0); }
  else die(`unknown argument ${a} (try --help)`);
}

/* items 504-506: the extra viewport passes. Desktop is 1280 x 860; --mobile adds the user's phone (iPhone 17 Pro Max, 440 x 956),
   --narrow adds the old 390 x 844 pass, --tablet adds the user's iPad Pro 13-inch (1032 x 1376 portrait, 1376 x 1032 landscape).
   Resizing sets the width and height of every pass; it does not emulate touch. */
const DESKTOP = { w: 1280, h: 860 };
const EXTRA = [];
if (opt.mobile) EXTRA.push({ w: 440, h: 956 });
if (opt.narrow) EXTRA.push({ w: 390, h: 844 });
if (opt.tablet) EXTRA.push({ w: 1032, h: 1376 }, { w: 1376, h: 1032 });
const ANY_EXTRA = EXTRA.length > 0;
let curVp = DESKTOP;
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
/* item 515: numeric widgets with unit "%" anywhere in a lesson file, with the forms a learner would type for the authored key */
const pctWidgets = (root) => {
  const out = [], seen = (v, at) => {
    if (Array.isArray(v)) return v.forEach((x, i) => seen(x, `${at}[${i}]`));
    if (!v || typeof v !== 'object') return;
    if (v.kind === 'numeric' && v.unit === '%' && typeof v.answer === 'number') {
      const k = Math.round(v.answer * 1e10) / 1e8, typed = [String(k), k + '%'];
      /* items 516, 517: the accept figure that represents the key is typed, not simply the leading one: the figure after the last "=" or "\\approx", else any figure whose hundredth is within tolerance of the key (resolved in the page), else the leading figure, which then fails; skipped unless the leading figure is followed by % */
      const txt = String(typeof v.accept === 'string' ? v.accept : '').replace(/\\%/g, '%'), head = txt.split(':')[0];
      const lead = head.match(/([-−–]?\d[\d,]*(?:\.\d+)?)(\s*%)?/), num = /[-−–]?\d[\d,]*(?:\.\d+)?/g, clean = (n) => n.replace(/,/g, '').replace(/[−–]/g, '-');
      let figs = null;
      if (lead && lead[2]) {
        const tail = txt.split(/=|\\approx/).slice(1).pop(), tailFig = tail ? (tail.match(num) || [])[0] : undefined;
        figs = { lead: clean(lead[1]), tail: tailFig === undefined ? null : clean(tailFig), all: (txt.match(num) || []).map(clean) };
      }
      out.push({ at, answer: v.answer, tol: v.tol, typed, figs });
    }
    Object.entries(v).forEach(([k, x]) => seen(x, `${at}.${k}`));
  };
  seen(root, '');
  return out;
};
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
  /* Engine samples (ENGINE-BACKLOG 467): a review or homework with "sample": true sits in a course folder off the map; it is played too */
  for (const c of order) {
    const dir = path.join(CONTENT, 'courses', c);
    if (!fs.existsSync(dir)) continue;
    fs.readdirSync(dir).filter(f => /^(review|homework)-.*\.json$/.test(f)).sort().forEach(f => {
      const id = f.replace(/\.json$/, '');
      if (sets.some(x => x.id === `${c}/${id}`)) return;
      let d = null; try { d = readJSON(path.join(dir, f)); } catch { /* the validator reports it */ }
      if (d && d.sample === true) sets.push({ id: `${c}/${id}`, kind: /^review-/.test(id) ? 'review' : 'homework', route: `${/^review-/.test(id) ? 'review' : 'homework'}/${c}/${id}`, sample: true });
    });
  }
  const exams = fs.existsSync(path.join(CONTENT, 'exams')) ? fs.readdirSync(path.join(CONTENT, 'exams')).filter(f => /^(topic|stage|mock)-.*\.json$/.test(f)).map(f => f.replace(/\.json$/, '')).sort() : [];
  return { lessons: out, courses: order.filter(c => fs.existsSync(path.join(CONTENT, 'courses', c, 'course.json'))), sets, exams };
};

/* ---------- Static server on a free port ---------- */
const freePort = () => new Promise((res, rej) => { const s = net.createServer(); s.unref(); s.on('error', rej); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); });
/* ENGINE-BACKLOG 575: the free port is probed and released before python binds it, so parallel shards can pick the same one. A server that dies
   (EADDRINUSE) is retried on a new port, and a "ready" answer only counts while our own process is still alive (it may have come from a sibling's server). */
const startServer = async () => {
  let err = '';
  for (let attempt = 0; attempt < 6; attempt++) {
    const port = await freePort();
    const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', APP], { stdio: ['ignore', 'ignore', 'pipe'] });
    err = ''; proc.stderr.on('data', d => { err += d; if (err.length > 4000) err = err.slice(-4000); });
    const base = `http://127.0.0.1:${port}`;
    let up = false;
    for (let i = 0; i < 100 && proc.exitCode == null; i++) {
      try { const r = await fetch(base + '/index.html'); if (r.ok) { await new Promise(r => setTimeout(r, 250)); up = proc.exitCode == null; break; } } catch { /* not up yet */ }
      await new Promise(r => setTimeout(r, 100));
    }
    if (up) return { proc, base };
    if (proc.exitCode == null) { proc.kill(); die('the static server did not start'); }
    await new Promise(r => setTimeout(r, 100 + Math.floor(Math.random() * 400)));   // stopped, usually EADDRINUSE: pick another port
  }
  die('the static server stopped on every port tried: ' + err);
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
  const lessons0 = opt.lessonsOn ? (opt.lessons.length ? opt.lessons : allLessons) : [];
  for (const l of opt.lessons) if (!allLessons.includes(l)) die(`--lesson ${l}: no such written lesson (the file must exist and be listed in its course.json)`);
  for (const x of opt.setIds) if (!allSets.some(s2 => s2.id === x)) die(`--set ${x}: no such written review or homework (the file must exist and be named in its course.json)`);
  for (const x of opt.examIds) if (!allExams.includes(x)) die(`--exam ${x}: no such exam in content/exams`);
  const sets0 = opt.setIds.length ? allSets.filter(s2 => opt.setIds.includes(s2.id)) : opt.sets ? allSets : [];
  const exams0 = opt.examIds.length ? opt.examIds : opt.exams ? allExams : [];
  /* ENGINE-BACKLOG 550: the full ordered item list is lessons, then sets, then exams; --shard i/n keeps the items whose index % n === i-1 */
  const full = [...lessons0.map(id => ({ k: 'lesson', id })), ...sets0.map(st => ({ k: 'set', id: st.id })), ...exams0.map(id => ({ k: 'exam', id }))];
  const mine = opt.shard ? full.filter((_, ix) => ix % opt.shard.n === opt.shard.i - 1) : full;
  const lessons = lessons0.filter(id => mine.some(m => m.k === 'lesson' && m.id === id));
  const sets = sets0.filter(st => mine.some(m => m.k === 'set' && m.id === st.id));
  const exams = exams0.filter(id => mine.some(m => m.k === 'exam' && m.id === id));
  if (opt.list) { mine.forEach(m => console.log(`${m.k}/${m.id}`)); return; }
  if (opt.shard) console.log(`shard ${opt.shard.i}/${opt.shard.n}: ${mine.length} of ${full.length} items${opt.routes ? (opt.shard.i === 1 ? ', plus the routes and their checks' : ', routes run in shard 1 only') : ''}`);
  const runRoutes = opt.routes && (!opt.shard || opt.shard.i === 1);
  const { proc, base } = await startServer();
  let browser = null, ctx = null, page = null, relaunches = 0, browserGone = false;
  const failures = [], consoleErrors = [];
  let where = 'start';
  const cleanup = async () => { try { if (browser) await browser.close(); } catch { /* closed */ } proc.kill(); };
  process.on('SIGINT', async () => { await cleanup(); process.exit(130); });
  const hostOf = (u) => { try { return new URL(u).hostname; } catch { return ''; } };
  /* ENGINE-BACKLOG 550: launch Chromium and give it a fresh context and page with the same options and listeners; used at the start and again on a relaunch */
  const openBrowser = async () => {
    if (browser) { try { await browser.close(); } catch { /* already closed */ } }
    browserGone = false; curVp = DESKTOP;
    browser = await chromium.launch({ headless: !opt.headed, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
    browser.on('disconnected', () => { browserGone = true; });
    ctx = await browser.newContext({ viewport: { width: 1280, height: 860 }, acceptDownloads: true });
    if (opt.localCdn) {
      await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
        const f = cdnFile(new URL(route.request().url()));
        if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
        return route.fulfill({ status: 404, body: '' });
      });
      await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
    }
    page = await ctx.newPage();
    page.on('console', (m) => {
      if (m.type() !== 'error') return;
      const loc = m.location() && m.location().url;
      if (/^Failed to load resource/.test(m.text()) && IGNORE_HOSTS.test(hostOf(loc))) return;
      consoleErrors.push({ where, text: m.text() + (loc ? `  (${loc})` : '') });
    });
    page.on('pageerror', (e) => consoleErrors.push({ where, text: 'Uncaught ' + (e.stack || e.message) }));
    page.on('requestfailed', (r) => { if (!IGNORE_HOSTS.test(hostOf(r.url()))) consoleErrors.push({ where, text: `request failed: ${r.url()} (${r.failure() && r.failure().errorText})` }); });
    page.on('response', (r) => { if (r.status() >= 400 && r.url().startsWith(base)) consoleErrors.push({ where, text: `HTTP ${r.status()} ${r.url().slice(base.length)}` }); });
  };
  try {
    await openBrowser();
    const setVp = async (v, settle = 300) => { curVp = v; await page.setViewportSize({ width: v.w, height: v.h }); await page.waitForTimeout(settle); };

    /* items 199, 205, 504: --mobile, --narrow and --tablet add a copy of every screenshot per extra viewport (name-440, -390, -1032, -1376; the viewport resizes, then returns) */
    /* inbox (backtest 1): a failing code screen names its first failing test (or the error) in the failure line */
    const codeWhy = async () => { try { return await page.evaluate(() => { const n = document.querySelector('.wd-res > .wd-res-err, .wd-res-row.bad'); return n ? ' (' + n.textContent.replace(/\s+/g, ' ').trim().slice(0, 240) + ')' : ''; }); } catch { return ''; } };
    const shot = async (name) => {
      if (!opt.shots) return;
      const file = (sfx) => path.join(opt.shots, name.replace(/[^\w.-]+/g, '_') + sfx + '.png');
      /* item 278: past the enter patch (350 ms), then until canvas tweens and CSS animations have settled and an exam result page has finished its staged reveal (the `.final` class; item 509; at most 4 s) */
      await page.waitForTimeout(420);
      try { await page.waitForFunction(() => (!window.ZQ || !ZQ.canvas || !ZQ.canvas.busy || ZQ.canvas.busy() === 0) && !document.querySelector('.exm-res:not(.final)') && !document.getAnimations().some((a) => a.playState === 'running' && a.effect && a.effect.getComputedTiming().iterations !== Infinity), null, { timeout: 4000, polling: 50 }); } catch { /* still moving: shoot anyway */ }
      await page.screenshot({ path: file('') });
      if (ANY_EXTRA) { for (const v of EXTRA) { await setVp(v, 350); await page.screenshot({ path: file('-' + v.w) }); if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)) console.log(`note  ${name} at ${v.w} x ${v.h}: the page is wider than the window`); } await setVp(DESKTOP, 150); }
    };
    const whyShot = async (name) => { if (!opt.why || !opt.shots) return; if (await page.evaluate(() => !!(ZQ.test.why && ZQ.test.why()))) { await page.waitForTimeout(450); await shot(name); await page.evaluate(() => ZQ.test.closeWhy()); await page.waitForTimeout(250); } };
    const go = async (hash) => {
      await page.evaluate((h) => { location.hash = h; }, hash);
      await page.waitForFunction((h) => location.hash === '#' + h || location.hash.startsWith('#' + h.split('/')[0]), hash, { timeout: opt.timeout });
      await page.waitForTimeout(400);
    };

    /* Fresh profile, then setup through the form (again after a relaunch) */
    const freshSetup = async () => {
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
    };
    await freshSetup();
    console.log(`setup done. ${lessons.length} lesson${lessons.length === 1 ? '' : 's'}${sets.length ? `, ${sets.length} review and homework set${sets.length === 1 ? '' : 's'}` : ''}${exams.length ? `, ${exams.length} exam${exams.length === 1 ? '' : 's'}` : ''} to play.`);

    /* ENGINE-BACKLOG 550: each item runs under `guarded`. When the browser has closed (the item threw "Target page, context or browser has been
       closed", or the disconnected event fired) Chromium is relaunched, setup is redone and the item is played once more; an ordinary failure is never retried.
       ZQ_TEST_CLOSE_AFTER=k (test hook) closes the context after the k-th item to prove the relaunch. */
    const closedRe = /Target page, context or browser has been closed|Browser has been closed|browser has disconnected|Target closed/i;
    let nItems = 0, played = 0;
    const relaunch = async (label, why) => {
      relaunches++;
      console.log(`     ${label}: ${why}; relaunching the browser (relaunch ${relaunches})`);
      await openBrowser();
      await freshSetup();
    };
    const guarded = async (label, fn) => {
      if (browserGone) await relaunch(label, 'the browser had disconnected before the item');
      const f0 = failures.length, e0 = consoleErrors.length;
      let thrown = null;
      try { await fn(); } catch (e) { thrown = e; }
      const closed = browserGone || (thrown && closedRe.test(String(thrown.message || thrown))) || failures.slice(f0).some(f => closedRe.test(f));
      if (closed) {
        failures.length = f0; consoleErrors.length = e0;
        await relaunch(label, 'the browser closed during the item');
        try { await fn(); } catch (e) { failures.push(`${label}: threw ${String(e.message || e).split('\n')[0]}`); }
      } else if (thrown) failures.push(`${label}: threw ${String(thrown.message || thrown).split('\n')[0]}`);
      played++;
      if (process.env.ZQ_TEST_CLOSE_AFTER && ++nItems === +process.env.ZQ_TEST_CLOSE_AFTER) { console.log(`     (test hook: closing the context after item ${nItems})`); try { await ctx.close(); } catch { /* closed */ } }
    };

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

    /* Prerequisite gating (ENGINE-BACKLOG 490): before a lesson, review, homework or mock is played, every prerequisite of it is marked met
       (ZQ.prereq.unlock), so the locked card never stands in the way of a playthrough */
    const unlockRoute = async (route) => {
      const m = /^(?:lesson|review|homework)\/([^/]+)\/([^/]+)/.exec(route);
      if (m) return page.evaluate(([c, i]) => (window.ZQ && ZQ.prereq ? ZQ.prereq.unlock(c, i) : 0), [m[1], m[2]]);
      const e = /^exam\/([^/?]+)/.exec(route);
      if (e) {
        const f = path.join(CONTENT, 'exams', e[1] + '.json'), refs = fs.existsSync(f) ? readJSON(f).requires : null;
        if (Array.isArray(refs) && refs.length) return page.evaluate((r) => ZQ.prereq.unlockRefs(r), refs);
      }
      return 0;
    };
    for (const id of lessons) await guarded(`lesson/${id}`, async () => {
      where = `#lesson/${id}`;
      const fails = [];
      const t0 = Date.now();
      try {
        await unlockRoute(`lesson/${id}`);
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
        /* item 515: a numeric widget with unit "%" is also typed as a learner would, from the authored key (answer x 100, with and without a % sign) and from the leading per cent figure of its accept text (item 516); every form must grade right. Catches a key stored as the per cent. */
        try {
          const pcts = pctWidgets(readJSON(path.join(CONTENT, 'courses', ...id.split('/')) + '.json'));
          if (pcts.length) {
            const bad = await page.evaluate((list) => {
              const G = ZQ.grade, out = [];
              for (const w of list) {
                const ok = (n) => { const x = G.parseNum(n) / 100; return Number.isFinite(x) && G.within(x, +w.answer, w.tol); };
                if (w.figs) { const f = w.figs, n = (f.tail !== null && ok(f.tail)) ? f.tail : (f.all.find(ok) ?? f.lead); w.typed.push(n, n + '%'); }
                for (const t of w.typed) {
                const v0 = G.parseNum(t), v = t.includes('%') ? v0 : v0 / 100;
                if (!(Number.isFinite(v) && G.within(v, +w.answer, w.tol))) out.push(`${w.at}: typing "${t}" is not graded right (key ${w.answer})`);
                }
              }
              return out;
            }, pcts);
            bad.forEach(b => fails.push(`unit % key: ${b}`));
          }
        } catch (e) { fails.push('unit % check threw: ' + String(e.message || e).split('\n')[0]); }
        const fin = await page.evaluate((lid) => { const [c, l] = lid.split('/'); const r = ZQ.state.lesson(c, l); return r ? { done: r.done, quiz: r.bestQuiz } : null; }, id);
        if (!fails.length && (!fin || !fin.done)) fails.push('the completion screen was reached but the lesson is not recorded as done');
        await shot(`${id}-done`);
        console.log(`${fails.length ? 'FAIL' : 'ok  '} ${id}  ${checks} checks, ${((Date.now() - t0) / 1000).toFixed(1)} s${fin && fin.quiz ? `, quiz ${fin.quiz[0]}/${fin.quiz[1]}` : ''}`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL ${id}  threw`);
      }
      fails.forEach(f => failures.push(`#lesson/${id}: ${f}`));
    });

    /* Reviews, homework and exams through the set-mode hook. Each page installs window.ZQ.test on mount; wait for a hook
       that is past 'loading', then: 'start' and 'submit' -> continue(); 'item' -> answerCorrect(), check() (a pending
       long-form check is answered and checked again), continue(); until 'done'. */
    /* item 445: a set that reports no items, or a hook that never answers (a course file mid-write by another agent, or a
       worker left busy by the lessons before), is reloaded and played once more before it counts as a failure */
    const playSet = async (route, label, verify, attempt = 1, tick = null) => {
      where = '#' + route;
      const fails = [];
      const t0 = Date.now();
      let checks = 0, perfStarters = 0, markedReal = 0;
      const probed = new Set();
      try {
        await page.evaluate(() => { delete window.ZQ.test; });
        if (!/^testout\//.test(route)) await unlockRoute(route);
        if (await page.evaluate((r) => location.hash === '#' + r, route)) await go('review');   // the same hash would not remount
        await go(route);
        await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind !== 'loading', null, { timeout: opt.timeout });
        let guard = 0, last = '', same = 0;
        while (true) {
          const c = await page.evaluate(() => ZQ.test.current());
          if (c.kind === 'done') break;
          if (c.kind === 'empty') { fails.push('the set has no items'); break; }
          const key = `${c.kind}:${c.screenIndex}:${c.state}:${c.paper ?? ''}:${c.part ?? ''}`;   // an item with parts moves on by part
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
            if (/^homework\//.test(route)) {
              /* items 530, 534: a performance code item's starter must fail its tests; a longform item is marked through the real
                 Mark my answer button (an empty box is refused unless the item is aloud), not only through the test hook */
              const hi = await page.evaluate(() => { const j = ZQ.test.current().screenIndex, it = (window.ZQHomework ? ZQHomework.items() : [])[j]; const w = it ? (it.kind === 'longform' ? it : it.widget || {}) : {}; return it ? { perf: it.performance || null, kind: w.kind || null, lang: w.language || 'python', starter: w.starter || '', aloud: Number(w.seconds) > 0 } : null; });
              if (hi && hi.perf === 'code' && hi.kind === 'code') {
                await page.evaluate((x) => { const j = ZQ.test.current().screenIndex; ZQHomework.handles()[j].set(x.starter + (x.lang === 'cpp' ? '\n// starter check\n' : '\n# starter check\n')); }, hi);
                const sr = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok } : null; });
                if (!sr) fails.push(`item ${c.screenIndex + 1}: the performance task's starter could not be checked`);
                else if (sr.ok) fails.push(`item ${c.screenIndex + 1}: the performance task's starter passes every hidden test`);
                else perfStarters++;
              }
              if (hi && hi.kind === 'longform') {
                const btn = page.locator('.hw-item:not([hidden]) [data-mark]');
                const marked = () => page.evaluate(() => { const j = ZQ.test.current().screenIndex; return !!(ZQHomework.handles()[j].value() || {}).marked; });
                if (!hi.aloud) {
                  await btn.click(); await page.waitForTimeout(80);
                  if (await marked()) fails.push(`item ${c.screenIndex + 1}: Mark my answer opened the model with an empty box on a written item`);
                  await page.locator('.hw-item:not([hidden]) textarea').fill('Working for the playthrough.');
                }
                await btn.click(); await page.waitForTimeout(80);
                if (!(await marked())) fails.push(`item ${c.screenIndex + 1}: Mark my answer did not open the model${hi.aloud ? ' with an empty notes box' : ''}`);
                else { markedReal++; if (opt.shots) await shot(`${label}-item-${String(c.screenIndex).padStart(2, '0')}-marked`); }
              }
            }
            const applied = await page.evaluate(() => ZQ.test.answerCorrect());
            let r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, key: r.key ?? null, pending: !!r.pending } : null; });
            if (r && r.pending) {
              await page.evaluate(() => ZQ.test.answerCorrect());
              r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, key: r.key ?? null, pending: !!r.pending } : null; });
            }
            checks++;
            if (!r) fails.push(`item ${c.screenIndex + 1}${c.part != null ? ` part ${c.part + 1}` : ''}${c.paper != null ? ` (paper ${c.paper + 1})` : ''}: ${applied === false ? 'answerCorrect() could not apply the authored answer' : 'nothing to check'}`);
            else if (!r.ok) fails.push(`item ${c.screenIndex + 1}${c.part != null ? ` part ${c.part + 1}` : ''}${c.paper != null ? ` (paper ${c.paper + 1})` : ''}: not correct, key ${JSON.stringify(r.key)}${await codeWhy()}`);
            else await whyShot(`${label}-item-${String(c.screenIndex).padStart(2, '0')}-why`); // item 335: set items' Explanation sheets
          }
          await page.evaluate(() => ZQ.test.continue());
          await page.waitForTimeout(120);
        }
        const v = await verify();
        if (v.fail) fails.push(v.fail);
        if (perfStarters || markedReal) v.note = `${v.note || ''}${perfStarters ? `, ${perfStarters} performance starter${perfStarters === 1 ? '' : 's'} fail` : ''}${markedReal ? `, ${markedReal} longform marked by the button` : ''}`;
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
    /* ---------- Follow-up parts in sets (ENGINE-BACKLOG 467) ---------- */
    const reopen = async (hash) => {
      await go('review');   // a changed hash is what remounts the screen, so leave it first
      await page.evaluate(() => { delete window.ZQ.test; });
      await go(hash);
      await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind !== 'loading', null, { timeout: opt.timeout });
    };
    /* A timed review that locks, with an item with parts after the first: part 1 of that item is answered and part 2 opened when the clock
       reaches zero. The item scores its credit (1 of n parts) on the summary, the parts never reached count as missed, and the review is
       recorded with only the items right in full. */
    const timedPartsChecks = async (st) => {
      const doc = readJSON(path.join(CONTENT, 'courses', ...st.id.split('/')) + '.json');
      const k = (doc.items || []).findIndex((it, i) => i > 0 && Array.isArray(it.parts));
      if (k < 0) return;
      where = '#' + st.route;
      const fails = [], t0 = Date.now(), N = doc.items[k].parts.length;
      try {
        await reopen(st.route);
        await page.evaluate(() => ZQ.test.continue());
        await page.waitForFunction(() => window.ZQSet && ZQ.test.current().kind === 'item', null, { timeout: opt.timeout });
        for (let i = 0; i < k; i++) {
          const py = await waitPython(); if (py) { fails.push(py); break; }
          await page.evaluate(() => ZQ.test.answerCorrect());
          const r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok } : null; });
          if (!r || !r.ok) fails.push(`item ${i + 1} could not be answered correctly`);
          await page.evaluate(() => ZQ.test.continue());
        }
        const py = await waitPython(); if (py) fails.push(py);
        await page.evaluate(() => ZQ.test.answerCorrect());
        const p1 = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { ok: !!r.ok, partial: !!r.partial } : null; });
        if (!p1 || !p1.ok || !p1.partial) fails.push(`part 1 of item ${k + 1} should check as a right, partial result (${JSON.stringify(p1)})`);
        await page.evaluate(() => ZQ.test.continue());   // opens part 2
        const mid = await page.evaluate(() => ZQ.test.current());
        if (mid.screenIndex !== k || mid.part !== 1) fails.push(`after part 1, the set should show part 2 of item ${k + 1} (screen ${mid.screenIndex}, part ${mid.part})`);
        await page.evaluate(() => ZQSet.setRemaining(0));
        await page.waitForFunction(() => ZQ.test.current().kind === 'done', null, { timeout: 5000 }).catch(() => fails.push('the clock reached zero but the set did not end by itself'));
        const rec = await page.evaluate((id) => ZQ.state.reviews[id] || null, st.id);
        if (!rec) fails.push('the timed-out review was not recorded');
        else if (rec.score !== k) fails.push(`the review recorded ${rec.score} right, expected ${k} (item ${k + 1} is right in 1 of ${N} parts only)`);
        const sum = await page.evaluate(() => ({ credit: (document.querySelector('.hw-credit') || {}).textContent || '', late: [...document.querySelectorAll('.hw-late')].map(n => n.textContent).join(' '), rows: [...document.querySelectorAll('.hw-res-m')].map(n => n.textContent) }));
        const credit = Math.round((k + 1 / N) * 10) / 10;
        if (!new RegExp(`${credit} of ${doc.items.length}`).test(sum.credit)) fails.push(`the summary should count ${credit} of ${doc.items.length} with part credit: "${sum.credit}"`);
        if (sum.rows[k] !== `1 of ${N} parts`) fails.push(`the summary row for item ${k + 1} says "${sum.rows[k]}", expected "1 of ${N} parts"`);
        if (!/Time ran out/.test(sum.late)) fails.push(`the summary does not say that time ran out: "${sum.late}"`);
        console.log(`${fails.length ? 'FAIL' : 'ok  '} ${st.id} (timed parts)  clock at zero in part 2: credit ${credit}, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL ${st.id} (timed parts)  threw`);
      }
      fails.forEach(f => failures.push(`#${st.route}: ${f}`));
    };
    /* Homework with parts: an item's parts open one by one, the draft keeps how many are open, and an item left with a part unanswered
       is marked by its credit (2 of 3 parts is two thirds of the item's marks) and counts as not right. The record is cleared first,
       because the full play above has already submitted it. */
    const partsHomeworkChecks = async (st) => {
      const doc = readJSON(path.join(CONTENT, 'courses', ...st.id.split('/')) + '.json');
      const k = (doc.items || []).findIndex(it => Array.isArray(it.parts) && it.parts.length >= 3 && !it.parts.some(p => ((p && p.widget) || {}).kind === 'code'));
      if (k < 0) return;
      where = '#' + st.route;
      const fails = [], t0 = Date.now(), item = doc.items[k], N = item.parts.length;
      try {
        await go('review');   // leaving the page first: closing it saves a draft, which the reset below must come after
        await page.evaluate((s) => { const d = JSON.parse(ZQ.state.export()); delete d.homework[s.id]; ZQ.state.import(JSON.stringify(d)); ZQ.store.set('hw.result.' + s.id, null); ZQ.store.set('hw.draft.' + s.id, null); }, st);
        await reopen(st.route);
        await page.evaluate(() => ZQ.test.continue());   // the intro
        /* the parts item may sit anywhere: answer the items before it as an ordinary play does, then its parts */
        for (let g = 0; g < 60 && (await page.evaluate(() => ZQ.test.current())).screenIndex !== k; g++) {   // one pass a part or an item
          const py = await waitPython(); if (py) { fails.push(py); break; }
          await page.evaluate(() => ZQ.test.answerCorrect());
          const r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { pending: !!r.pending } : null; });
          if (r && r.pending) { await page.evaluate(() => ZQ.test.answerCorrect()); await page.evaluate(async () => { await ZQ.test.check(); }); }
          await page.evaluate(() => ZQ.test.continue());
        }
        for (let p = 0; p < N - 1; p++) {
          await page.evaluate(() => ZQ.test.answerCorrect());
          await page.evaluate(() => ZQ.test.continue());   // opens the next part
        }
        const mid = await page.evaluate(() => ZQ.test.current());
        if (mid.part !== N - 1 || mid.screenIndex !== k) fails.push(`the item should show its last part (screen ${mid.screenIndex}, part ${mid.part}, item ${k})`);
        /* the draft keeps the open parts and the answers */
        await reopen(st.route);
        await page.evaluate(() => ZQ.test.continue());
        await page.evaluate((i) => ZQHomework.go(i), k);
        const kept = await page.evaluate((i) => { const v = ZQHomework.handles()[i].value(); return { open: v && v.open, answered: v && v.parts.filter(x => x != null && x !== '' && !(Array.isArray(x) && !x.length)).length }; }, k);
        if (kept.open !== N || kept.answered !== N - 1) fails.push(`the draft kept ${kept.open} open parts and ${kept.answered} answers, expected ${N} and ${N - 1}`);
        let guard = 0, left = false;
        while (++guard < 80) {
          const c = await page.evaluate(() => ZQ.test.current());
          if (c.kind === 'done') break;
          if (c.kind === 'item' && c.screenIndex === k && !left) { left = true; await page.evaluate((v) => ZQHomework.go(v), k + 1 < doc.items.length ? k + 1 : 'review'); continue; }   // leave the last part of the parts item unanswered
          if (c.kind === 'item') {
            const py = await waitPython(); if (py) { fails.push(py); break; }
            await page.evaluate(() => ZQ.test.answerCorrect());
            let r = await page.evaluate(async () => { const r = await ZQ.test.check(); return r ? { pending: !!r.pending } : null; });
            if (r && r.pending) { await page.evaluate(() => ZQ.test.answerCorrect()); await page.evaluate(async () => { await ZQ.test.check(); }); }
          }
          await page.evaluate(() => ZQ.test.continue());
          await page.waitForTimeout(100);
        }
        const out = await page.evaluate((id) => { const R = ZQ.store.get('hw.result.' + id, null), h = ZQ.state.homework[id]; return { R, score: h && h.score, items: h && h.items }; }, st.id);
        const x = out.R && out.R.items && out.R.items[k];
        if (!x) fails.push('no stored result for the item with parts');
        else {
          const want = Math.round(((N - 1) / N) * (item.difficulty || 3) * 100) / 100;
          if (Math.abs(x.credit - (N - 1) / N) > 1e-9 || x.ok || x.got !== want) fails.push(`item ${k + 1}: credit ${x.credit}, ok ${x.ok}, marks ${x.got}; expected ${(N - 1)}/${N}, false, ${want}`);
          if (!Array.isArray(x.parts) || x.parts.filter(q => q.ok).length !== N - 1) fails.push(`item ${k + 1}: the stored parts are ${JSON.stringify(x.parts)}`);
          if (out.score !== out.items - 1) fails.push(`homework scored ${out.score} of ${out.items} right, expected ${out.items - 1} (the item with an unanswered part is not right)`);
        }
        const row = await page.evaluate((i) => { const r = document.querySelectorAll('.hw-res-r')[i]; return ((r && r.querySelector('.hw-rl-t .secondary')) || {}).textContent || ''; }, k);
        if (!new RegExp(`${N - 1} of ${N} parts right`).test(row)) fails.push(`the summary row says "${row}", expected "${N - 1} of ${N} parts right"`);
        console.log(`${fails.length ? 'FAIL' : 'ok  '} ${st.id} (parts checks)  open parts kept in the draft, part credit in the marks, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL ${st.id} (parts checks)  threw`);
      }
      fails.forEach(f => failures.push(`#${st.route}: ${f}`));
    };
    for (const st of sets) await guarded(`set/${st.id}`, async () => {
      if (st.kind === 'review') { const t = readJSON(path.join(CONTENT, 'courses', ...st.id.split('/')) + '.json').timed; if (t && t.lockAtZero) { await timedChecks(st, t); await timedPartsChecks(st); } }
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
        /* item 531: a homework holding a performance item records the level's task in state.perf */
        const hd = readJSON(path.join(CONTENT, 'courses', ...st.id.split('/')) + '.json'), hn = (/(\d+)$/.exec(st.id) || [])[1];
        const pf = (hd.items || []).filter(it => it && it.performance);
        if (pf.length) {
          const got = await page.evaluate((k) => (ZQ.state.perf.get() || {})[k] || null, `${st.id.split('/')[0]}/L${hn}`);
          if (!got) return { fail: `${note}; the performance task was not recorded in state.perf (${st.id.split('/')[0]}/L${hn})`, note };
          if (got.how !== 'auto' && got.how !== 'self') return { fail: `${note}; state.perf has an odd record ${JSON.stringify(got)}`, note };
        }
        return { fail: h.score !== h.items || !h.items ? note : null, note };
      });
      if (st.kind === 'homework') await partsHomeworkChecks(st);
    });
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
        let guard = 0, answered = new Set(), drawnParts = false;
        while (++guard < 80) {
          const c = await page.evaluate(() => ZQ.test.current());
          if (c.kind === 'done') break;
          if (c.kind === 'start') await page.evaluate(() => ZQ.test.continue());
          else if (c.kind === 'item') {
            if (!answered.has(c.paper)) {
              answered.add(c.paper);
              if (c.parts > 1) drawnParts = true;   /* a drawn paper can open on an item with parts, which the file alone does not show */
              await page.evaluate(() => ZQ.test.answerCorrect());
              /* ENGINE-BACKLOG 570: the answer registers asynchronously for some widgets; zero the clock only once exam state counts it */
              await page.waitForFunction(() => ZQ.test.current().state === 'engaged', null, { timeout: opt.timeout }).catch(() => {});
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
          /* the one answer is the first part of an item with parts when a paper opens with one: that item is not right in full (partial credit) */
          const partsFirst = drawnParts || papers.some(p => (p.items || []).length && Array.isArray(p.items[0].parts));
          if (!(c.score >= (partsFirst ? 0 : 1) && c.score <= papers.length)) fails.push(`timed out with one answer per paper but scored ${c.score}`);
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
    /* ---------- Follow-up parts and drawn items (ENGINE-BACKLOG 467, 468) ---------- */
    const itemsOf = (doc) => (Array.isArray(doc.parts) ? doc.parts.filter(p => p.kind === 'paper') : [doc]).flatMap(p => p.items || []);
    /* A mock's draw: the same seed gives the same items, another seed another set, the entries are balanced across families, a family
       offers its unseen items before its seen ones, nothing is drawn twice, and the attempt keeps what it drew (seed and uids) */
    const drawChecks = async (ex) => {
      const doc = readJSON(path.join(CONTENT, 'exams', ex + '.json'));
      const papers = Array.isArray(doc.parts) ? doc.parts.filter(p => p.kind === 'paper') : [doc];
      const entries = papers.flatMap(p => p.draw || []);
      if (!entries.length) return;
      where = `#exam/${ex}`;
      const fails = [], t0 = Date.now();
      /* the pool of an entry, read from the files as the engine reads it: [{ uid, family }] */
      const poolOf = (e) => {
        const [kind, name] = e.from.split('/'), tags = e.tags || [], band = Array.isArray(e.difficulty) ? e.difficulty : e.difficulty != null ? [e.difficulty, e.difficulty] : null, out = [];
        const keep = (t, d) => (!tags.length || (t || []).some(x => tags.includes(x))) && (!band || (d >= band[0] && d <= band[1]));
        const dir = path.join(CONTENT, kind);
        for (const f of fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => /^[a-z0-9-]+\.json$/.test(f) && f !== 'index.json') : []) {
          const id = f.replace(/\.json$/, ''), d = readJSON(path.join(dir, f));
          if (d.sample === true && doc.sample !== true) continue;
          if (kind === 'bank') { if (!(name === '*' || id === name || id.startsWith(name + '-'))) continue; (d.items || []).forEach(it => { if (keep(it.tags, it.difficulty)) out.push({ uid: `bank/${id}/${it.id}`, family: it.tags[0] }); }); }
          else if (name === '*' || d.pack === name || d.id === name || String(d.id).startsWith(name + '-')) { const tg = Array.isArray(d.tags) ? d.tags : [], t = [...tg, ...(d.pattern && !tg.includes(d.pattern) ? [d.pattern] : [])]; if (!t.length) t.push(d.pack || d.id); if (keep(t, d.difficulty)) out.push({ uid: `drills/${id}`, family: t[0] }); }
        }
        return out;
      };
      try {
        const grab = async (seed) => {
          await reopen(`exam/${ex}/${seed}`);
          await page.evaluate(() => ZQ.test.continue());
          await page.waitForFunction(() => window.ZQExam && ZQExam.handles().length, null, { timeout: opt.timeout });
          return page.evaluate(() => ZQExam.handles().map(h => (h && h.item && h.item.drawn ? h.item.drawn.uid : null)).filter(Boolean));
        };
        /* the entries of an exam share one used set (the engine's draw): an item an earlier entry could claim is not counted again */
        const claimed = new Set();
        const want = entries.reduce((a, e) => { const free = poolOf(e).filter(x => !claimed.has(x.uid)).slice(0, e.n); free.forEach(x => claimed.add(x.uid)); return a + free.length; }, 0);
        const a = await grab(777), b = await grab(777);
        if (a.length !== want) fails.push(`${a.length} items drawn, ${want} expected from the draw entries`);
        if (new Set(a).size !== a.length) fails.push(`an item was drawn twice in one attempt: ${a.join(', ')}`);
        if (JSON.stringify(a) !== JSON.stringify(b)) fails.push('the same seed drew different items');
        let differs = false;
        for (let s = 778; s < 790 && !differs; s++) differs = JSON.stringify(await grab(s)) !== JSON.stringify(a);
        if (!differs) fails.push('twelve other seeds all drew the same items');
        /* balance: an entry whose pool holds several families, drawn from, offers at least min(n, families) of them */
        const drawn = await grab(900);
        entries.forEach(e => {
          const pool = poolOf(e), fams = new Set(pool.map(x => x.family)), mine = drawn.filter(u => pool.some(x => x.uid === u)), got = new Set(mine.map(u => pool.find(x => x.uid === u).family));
          if (got.size < Math.min(e.n, fams.size)) fails.push(`${e.from}: ${mine.length} drawn from ${got.size} of ${fams.size} families (should be balanced)`);
        });
        /* the engine's own draw with a seen map: unseen first within a family, whatever the seed */
        const seenTest = await page.evaluate(async (a) => {
          const doc = await ZQ.content.exam(a.ex), papers = Array.isArray(doc.parts) ? doc.parts.filter(p => p.kind === 'paper') : [doc], out = [];
          for (const p of papers) for (const e of p.draw || []) {
            const first = await ZQ.mock.draw([e], { seed: 5, exam: a.ex, sample: doc.sample === true });
            const seen = {}; first.forEach((it) => { seen[it.drawn.uid] = 1; });
            const again = await ZQ.mock.draw([e], { seed: 6, exam: a.ex, sample: doc.sample === true, seen });
            out.push({ from: e.from, n: e.n, first: first.map(i => i.drawn.uid), again: again.map(i => i.drawn.uid) });
          }
          return out;
        }, { ex });
        seenTest.forEach(t => {
          const entry = entries.find(e => e.from === t.from), pool = poolOf(entry), fresh = pool.filter(x => !t.first.includes(x.uid));
          const byFam = {}; pool.forEach(x => { (byFam[x.family] = byFam[x.family] || []).push(x.uid); });
          /* a family that still has unseen items draws no seen item */
          Object.entries(byFam).forEach(([f, uids]) => {
            const unseen = uids.filter(u => !t.first.includes(u)), tookSeen = t.again.filter(u => uids.includes(u) && t.first.includes(u)), tookUnseen = t.again.filter(u => uids.includes(u) && !t.first.includes(u));
            if (tookSeen.length && tookUnseen.length < unseen.length) fails.push(`${t.from}: family ${f} drew a seen item while ${unseen.length - tookUnseen.length} unseen were left`);
          });
          if (fresh.length >= t.n && t.again.some(u => t.first.includes(u)) && new Set(pool.map(x => x.family)).size === 1) fails.push(`${t.from}: a resit drew a seen item with ${fresh.length} unseen in a one-family pool`);
        });
        /* the attempt keeps what it drew, with the seed */
        const kept = await page.evaluate((id) => { const a = ZQ.state.exams[id].attempts, l = a[a.length - 1]; return { n: a.length, drawn: l && l.drawn, seed: l && l.seed }; }, ex);
        if (!kept.n) fails.push('no attempt was recorded to read the drawn items from');
        else if (!Array.isArray(kept.drawn) || kept.drawn.length !== want || typeof kept.seed !== 'number') fails.push(`the last attempt keeps drawn ${JSON.stringify(kept.drawn)} and seed ${kept.seed}`);
        console.log(`${fails.length ? 'FAIL' : 'ok  '} ${ex} (draw checks)  ${want} items per attempt, seed, balance, unseen first, attempt record, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL ${ex} (draw checks)  threw`);
      }
      fails.forEach(f => failures.push(`#exam/${ex}: ${f}`));
    };
    /* An item with parts in an exam: the first one is answered in part 1 only (the later parts are never opened), every other item in
       full. It must score its credit (the share of parts right) with the wrong mark on the rest, show "k of n parts" on the result,
       open the unreached parts there, and still count as not right. */
    const partsExamChecks = async (ex) => {
      const doc = readJSON(path.join(CONTENT, 'exams', ex + '.json'));
      if (Array.isArray(doc.parts) || (doc.draw && doc.draw.length)) return;
      const its = doc.items || [], target = its.findIndex(it => Array.isArray(it.parts));
      if (target < 0) return;
      where = `#exam/${ex}`;
      const fails = [], t0 = Date.now(), N = its[target].parts.length, sc = Object.assign({ right: 1, wrong: 0, blank: 0 }, doc.scoring || {});
      try {
        await reopen(`exam/${ex}/4321`);
        await page.evaluate(() => ZQ.test.continue());
        await page.waitForFunction(() => ZQ.test.current().kind === 'item', null, { timeout: opt.timeout });
        const before = await page.evaluate((id) => (ZQ.state.exams[id] || { attempts: [] }).attempts.length, ex);
        let guard = 0;
        while (++guard < 120) {
          const c = await page.evaluate(() => ZQ.test.current());
          if (c.kind === 'done') break;
          if (c.kind !== 'item') { await page.evaluate(() => ZQ.test.continue()); continue; }
          const py = await waitPython(); if (py) { fails.push(py); break; }
          await page.evaluate(() => ZQ.test.answerCorrect());
          if (c.screenIndex === target) {
            /* part 1 only: move on without opening part 2 */
            await page.evaluate((n) => (n === 0 ? ZQExam.submit() : ZQExam.go(ZQExam.part().current + 1)), its.length - 1 === target ? 0 : 1);
          } else await page.evaluate(() => ZQ.test.continue());
          await page.waitForTimeout(100);
        }
        const r = await page.evaluate((id) => { const a = ZQ.state.exams[id].attempts; return { n: a.length, last: a[a.length - 1] }; }, ex);
        if (r.n !== before + 1) fails.push('the sitting was not recorded');
        else {
          const rightN = its.length - 1 + 1 / N, wrongN = 1 - 1 / N, net = Math.round((rightN * sc.right + wrongN * sc.wrong) * 1e6) / 1e6;
          if (Math.abs(r.last.net - net) > 1e-6) fails.push(`net ${r.last.net}, expected ${net} (item ${target + 1} answered in part 1 of ${N}: credit ${(1 / N).toFixed(3)})`);
          const row = await page.evaluate((k) => { const a = document.querySelectorAll('.exm-ri')[k]; return a ? { text: a.querySelector('.exm-v').textContent, ok: a.dataset.ok, parts: a.querySelectorAll('.lsn-part').length } : null; }, target);
          if (!row) fails.push('the result page has no row for the parts item');
          else {
            if (!new RegExp(`1 of ${N} parts`).test(row.text)) fails.push(`the result row says "${row.text}", expected "1 of ${N} parts"`);
            if (row.ok !== 'false') fails.push('an item with unanswered parts counted as right');
            if (row.parts !== N) fails.push(`the result shows ${row.parts} parts, expected all ${N} (the unreached ones are opened locked)`);
          }
          await shot(`${ex}-parts-result`);
        }
        console.log(`${fails.length ? 'FAIL' : 'ok  '} ${ex} (parts checks)  part 1 only: credit, net score, result row, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL ${ex} (parts checks)  threw`);
      }
      fails.forEach(f => failures.push(`#exam/${ex}: ${f}`));
    };
    /* ---------- Holdout and resit integrity (PLAN 2c item 6, F05.6, ENGINE-BACKLOG 546): part of --routes-only and --exam mock-oa-code ----------
       (a) a profile that has verified every drill of the mock's pool is told, on the start card, on each drawn question and in the
       results, that both problems were previously seen (reason: solved in the library), and the attempt stores `seen`; (b) two
       consecutive sittings by a fresh profile draw four distinct problems while the pool allows, the second labelled "sat on". */
    const holdoutChecks = async (ex) => {
      const f = path.join(CONTENT, 'exams', ex + '.json');
      if (!fs.existsSync(f)) return;
      const doc = readJSON(f), papers = (doc.parts || []).filter(p => p.kind === 'paper'), entries = papers.flatMap(p => p.draw || []);
      const drillPools = entries.filter(e => /^drills\//.test(e.from));
      if (!drillPools.length) return;
      where = `#exam/${ex}`;
      const fails = [], t0 = Date.now();
      let saved = null;
      const fresh = (verify) => page.evaluate(([v, refs]) => {
        const d = JSON.parse(ZQ.state.export());
        d.exams = {}; d.redo = []; d.drills = {};
        (v || []).forEach(id => { d.drills[id] = { verified: true, code: 'x', at: 1 }; });
        d.prereq = { met: {}, testouts: {}, opened: {}, started: {}, grandfathered: true };
        d.flags.setupDone = true;
        const ok = ZQ.state.import(JSON.stringify(d)).ok;
        ZQ.prereq.unlockRefs(refs);   // the mock's own requires, as unlockRoute does for every other exam
        return ok;
      }, [verify, doc.requires || []]);
      /* sit once: the start card text, the label on each question, then the result */
      const sit = async (seed) => {
        await reopen(`exam/${ex}/${seed}`).catch(async (e) => { throw new Error(`the exam did not open: ${(await page.evaluate(() => document.body.innerText.slice(0, 120).replace(/\\s+/g, ' ')))}`); });
        const start = await page.evaluate(() => document.body.innerText);
        await page.evaluate(() => ZQ.test.continue());
        await page.waitForFunction(() => window.ZQExam && ZQExam.handles().length, null, { timeout: opt.timeout });
        const n = await page.evaluate(() => ZQExam.handles().length), labels = [];
        for (let i = 0; i < n + 2; i++) {
          const c = await page.evaluate(() => ZQ.test.current());
          if (c.kind === 'done') break;
          labels.push(await page.evaluate(() => Array.from(document.querySelectorAll('.exm-seen')).map(e => e.textContent.trim()).join('|')));
          await page.evaluate(() => ZQ.test.continue());
          await page.waitForTimeout(150);
        }
        const done = await page.evaluate(() => ZQ.test.current().kind === 'done');
        const result = await page.evaluate(() => document.body.textContent);
        const at = await page.evaluate((id) => ((ZQ.state.exams[id] || {}).attempts || []).slice(-1)[0] || null, ex);
        return { start, labels: labels.filter(Boolean), done, result, at };
      };
      try {
        saved = await page.evaluate(() => ZQ.state.export());
        const ids = await page.evaluate(async (pools) => {
          const out = [];
          for (const r of ZQ.content.drills()) { const id = typeof r === 'string' ? r : r.id, d = await ZQ.content.drill(id).catch(() => null); if (d && pools.some(p => { const name = p.split('/')[1]; return name === '*' || d.pack === name || d.id === name || String(d.id).startsWith(name + '-'); })) out.push(id); }
          return out;
        }, drillPools.map(e => e.from));
        if (ids.length < 4) fails.push(`only ${ids.length} drills in the pool, expected the pool to allow four distinct problems`);
        /* (a) everything verified */
        if (!(await fresh(ids))) throw new Error('could not import a profile');
        const a = await sit(31337);
        if (!/Previously seen/.test(a.start)) fails.push('(a) the start card does not say previously seen');
        if (a.labels.length < entries.reduce((x, e) => x + (e.n || 1), 0)) fails.push(`(a) ${a.labels.length} drawn questions show a "previously seen" label, expected one per drawn problem`);
        if (!a.labels.every(l => /Previously seen: solved in the drill library/.test(l))) fails.push(`(a) the label does not give the reason: ${a.labels.join(' / ')}`);
        if (!a.done) fails.push('(a) the result page was not reached');
        else {
          if (!/Previously seen: solved in the drill library/.test(a.result)) fails.push('(a) the results do not carry the label');
          if (!a.at || !a.at.seen || Object.keys(a.at.seen).length !== (a.at.drawn || []).length) fails.push('(a) the attempt does not store seen for every drawn problem');
        }
        /* (b) a fresh profile, two sittings */
        if (!(await fresh([]))) throw new Error('could not import a fresh profile');
        const b1 = await sit(1), b2 = await sit(2);
        const d1 = (b1.at && b1.at.drawn) || [], d2 = (b2.at && b2.at.drawn) || [];
        if (b1.labels.length) fails.push(`(b) a fresh profile saw "previously seen" on the first sitting: ${b1.labels.join(' / ')}`);
        if (new Set([...d1, ...d2]).size !== d1.length + d2.length || !d1.length) fails.push(`(b) two sittings did not draw distinct problems: ${d1.join(', ')} then ${d2.join(', ')}`);
        if (b2.labels.length) fails.push(`(b) the second sitting labelled a problem previously seen with the pool unexhausted: ${b2.labels.join(' / ')}`);
        /* a third sitting still has two unseen problems; a fifth must repeat and say "sat on" */
        for (const sd of [3, 4]) await sit(sd);
        const b5 = await sit(5);
        if (!b5.labels.length || !b5.labels.every(l => /Previously seen: sat on /.test(l))) fails.push(`(b) a sitting after the pool is used up should label its problems "sat on <date>": ${b5.labels.join(' / ')}`);
        console.log(`${fails.length ? 'FAIL' : 'ok  '} #exam/${ex} holdout  ${ids.length}-drill pool: verified profile sees "previously seen", two sittings draw four distinct problems  (${((Date.now() - t0) / 1000).toFixed(1)}s)`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log(`FAIL #exam/${ex} holdout  threw`);
      } finally {
        if (saved) { try { await page.evaluate((d) => ZQ.state.import(d), saved); } catch { /* the run ends anyway */ } }
      }
      fails.forEach(x => failures.push(`#exam/${ex} holdout: ${x}`));
    };
    /* Fixed versions in Prepare (PLAN 2c item 6, F05.7, ENGINE-BACKLOG 547): a mock with <id>-<n> files shows "Version 1, 2, 3" under the base mock
       a path names, and its button offers the next unsat version first. Part of --routes-only. */
    const versionChecks = async () => {
      const prep = path.join(CONTENT, 'prep.json'), paths = fs.existsSync(prep) ? (readJSON(prep).paths || []) : [];
      const files = fs.readdirSync(path.join(CONTENT, 'exams')).map(f => f.replace(/\.json$/, ''));
      const base = paths.flatMap(p => (p.mocks || []).map(m => ({ p, m }))).find(x => files.some(f => new RegExp('^' + x.m + '-\\d+$').test(f)));
      if (!base) return;
      const want = [base.m, ...files.filter(f => new RegExp('^' + base.m + '-\\d+$').test(f)).sort()];
      where = `#prepare/${base.p.id}`;
      const fails = [], t0 = Date.now();
      let saved = null;
      try {
        saved = await page.evaluate(() => ZQ.state.export());
        const read = async () => { await go('review'); await go(`prepare/${base.p.id}`); await page.waitForSelector(`.pp-mock[data-mock="${base.m}"]`, { timeout: opt.timeout }); return page.evaluate((m) => { const li = document.querySelector(`.pp-mock[data-mock="${m}"]`); return { vs: Array.from(li.querySelectorAll('[data-version]')).map(a => a.dataset.version), next: (li.querySelector('[data-next-version]') || {}).dataset ? li.querySelector('[data-next-version]').dataset.nextVersion : null }; }, base.m); };
        await page.evaluate(() => { const d = JSON.parse(ZQ.state.export()); d.exams = {}; ZQ.state.import(JSON.stringify(d)); });
        let got = await read();
        if (JSON.stringify(got.vs) !== JSON.stringify(want)) fails.push(`versions listed ${got.vs.join(', ')}, expected ${want.join(', ')}`);
        if (got.next !== want[0]) fails.push(`the unsat state should offer ${want[0]}, offered ${got.next}`);
        await page.evaluate(([e]) => { const d = JSON.parse(ZQ.state.export()); d.exams = { [e]: { attempts: [{ at: 1, score: 1, items: 2, passed: false, bySkill: {} }] } }; ZQ.state.import(JSON.stringify(d)); }, [want[0]]);
        got = await read();
        if (want.length > 1 && got.next !== want[1]) fails.push(`with version 1 sat, the next should be ${want[1]}, offered ${got.next}`);
        console.log(`${fails.length ? 'FAIL' : 'ok  '} #prepare  ${base.m}: versions ${want.length} grouped, next unsat offered  (${((Date.now() - t0) / 1000).toFixed(1)}s)`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log('FAIL #prepare versions  threw');
      } finally {
        if (saved) { try { await page.evaluate((d) => ZQ.state.import(d), saved); } catch { /* the run ends anyway */ } }
      }
      fails.forEach(x => failures.push(`#prepare versions: ${x}`));
    };
    for (const ex of exams) await guarded(`exam/${ex}`, async () => {
      await playSet(`exam/${ex}`, ex, async () => {
        const c = await page.evaluate(() => ZQ.test.current());
        if (c.kind !== 'done') return { fail: 'the result page was not reached' };
        const note = `scored ${c.score} of ${c.total}${c.max != null && c.max !== c.total ? `, net ${c.net} of ${c.max}` : ''}, ${c.passed ? 'passed' : 'not passed'}`;
        return { fail: !c.passed || c.score !== c.total || !c.total ? note : null, note };
      });
      if (/^mock-/.test(ex)) await mockChecks(ex);
      if (/^mock-/.test(ex)) { await drawChecks(ex); await partsExamChecks(ex); }
      if (ex === 'mock-oa-code') await holdoutChecks(ex);
    });

    /* ---------- Interview bank deck and per-item timing (ENGINE-BACKLOG 456, 457): part of --routes-only ----------
       Date.now is skewed from the tool (window.__skew, in seconds), so an item can "take" 90 s and a schedule can be
       moved forward by days without waiting; the exam clock reads performance.now and is not affected. */
    const skew = (sec) => page.evaluate((n) => { if (window.__skew === undefined) { window.__skew = 0; const real = Date.now.bind(Date); Date.now = () => real() + window.__skew * 1000; } window.__skew += n; return window.__skew; }, sec);
    const unskew = () => page.evaluate(() => { window.__skew = 0; });
    const bankFiles = () => (fs.existsSync(path.join(CONTENT, 'bank')) ? fs.readdirSync(path.join(CONTENT, 'bank')).filter(f => /^[a-z0-9-]+\.json$/.test(f)).map(f => readJSON(path.join(CONTENT, 'bank', f))).filter(d => d.sample !== true) : []);   // a sample file is hidden from the deck
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
      const all = fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => /^[a-z0-9-]+\.json$/.test(f)).map(f => f.replace(/\.json$/, '')).sort() : [];
      const names = all.filter(n => readJSON(path.join(dir, n + '.json')).sample !== true);   // sample files are never dealt
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
                  /* an item with parts: part k+1 opens on continue once part k is checked; the item is right when every part is */
                  for (let q = 1; it.parts && q < it.parts.length; q++) {
                    await page.evaluate(() => ZQ.test.continue());
                    await page.evaluate(() => ZQ.test.answerCorrect());
                    const rq = await page.evaluate(() => ZQ.test.check().then(r => r && { ok: !!r.ok }));
                    r = { ok: !!(r && r.ok && rq && rq.ok) };
                  }
                  if (((it.widget || (it.parts && it.parts[0].widget) || {}).kind) === 'longform') {
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
       moved on 130 s while the drill is open; no real minutes are waited), and with --mobile, --narrow or --tablet the whole run repeats at each of those sizes
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
        /* item 512: every pass starts from an unsolved drill. A solved one reopens on Continue (Submit leaves the page when the code is the verified code), so a second viewport pass would leave the drill on its first Submit */
        await page.evaluate((id2) => { delete ZQ.state.drills.get()[id2]; ZQ.store.set(`drill.${id2}.state`, null); }, id);
        await go('drill/' + id);
        await page.waitForFunction(() => window.ZQDrill, null, { timeout: opt.timeout });
        const bad = await drillReady(cpp);
        if (bad) { mine.push(bad); throw new Error(bad); }
        if (ANY_EXTRA && await wide()) mine.push(`the page is wider than the ${curVp.w} px window`);
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
        if (ANY_EXTRA && await wide()) mine.push(`after the run the page is wider than the ${curVp.w} px window`);
        console.log(`${mine.length ? 'FAIL' : 'ok  '} --drill ${id}  ${cpp ? 'C++' : 'Python'}, ${ref.passed} of ${ref.total} tests with the model solution, starter fails: ${!st.ok}`);
      } catch (e) { if (!mine.length) mine.push('threw ' + String(e.message || e).split('\n')[0]); console.log(`FAIL --drill ${id}  ${mine[0]}`); if (process.env.ZQDBG) console.log(e.stack, await page.evaluate(() => ({ h: location.hash, z: !!window.ZQDrill, t: document.body.innerText.slice(0, 300) }))); }
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
        if (ANY_EXTRA && await wide()) bad(`the setup page is wider than the ${curVp.w} px window`);
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
          if (i === 0 && ANY_EXTRA && await wide()) bad(`the session page is wider than the ${curVp.w} px window`);
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
        if (ANY_EXTRA && await wide()) bad(`the result page is wider than the ${curVp.w} px window`);
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
        if (ANY_EXTRA && await wide()) fails.push(`the filtered list is wider than the ${curVp.w} px window`);
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
        if (ANY_EXTRA && await wide()) fails.push(`the session setup is wider than the ${curVp.w} px window`);
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
      for (const v of ANY_EXTRA ? EXTRA : [DESKTOP]) {
        if (ANY_EXTRA) await setVp(v);
        for (const id of ids) await drillOne(id);
        if (opt.sessionRun || opt.drillsAll) await sessionPlay();
        await unskewClock();
      }
      if (ANY_EXTRA) await setVp(DESKTOP, 200);
    }
    /* Engine samples ("sample": true) load by route but appear in no learner-facing list or count (ENGINE-BACKLOG 467, 468) */
    const sampleChecks = async () => {
      const mf = JSON.parse(fs.readFileSync(path.join(CONTENT, 'manifest.json'), 'utf8')), samples = mf.samples || [];
      if (!samples.length) return;
      where = '#review';
      const fails = [], t0 = Date.now();
      try {
        const names = samples.filter(f => /^(exams|bank|drills)\//.test(f)).map(f => readJSON(path.join(CONTENT, f)).name).filter(Boolean);
        const got = await page.evaluate((files) => ({ flagged: files.filter(f => !ZQ.content.isSample(f)), mocks: ZQ.content.mocks(), banks: ZQ.content.bankIds(), drills: ZQ.content.drills().map(d => d.id || d) }), samples);
        if (got.flagged.length) fails.push(`the engine does not know these as samples: ${got.flagged.join(', ')}`);
        samples.forEach(f => {
          const id = f.replace(/^[a-z]+\//, '').replace(/\.json$/, '');
          if (/^exams\//.test(f) && got.mocks.includes(id)) fails.push(`${f} is listed among the mock assessments`);
          if (/^bank\//.test(f) && got.banks.includes(id)) fails.push(`${f} is listed among the bank files`);
          if (/^drills\//.test(f) && got.drills.includes(id)) fails.push(`${f} is listed among the drills`);
        });
        for (const r of ['review', 'drill', 'you']) {
          await go(r);
          /* A sample leaks only as a whole entry: a line of the page text or a leaf element (card title, list item, link) equal to its name.
             A real item whose name merely contains the sample's name ("Longest run with equal zeros and ones") is not a leak (ENGINE-BACKLOG 499). */
          const entries = new Set(await page.evaluate(() => {
            const root = document.querySelector('#app'), out = root.innerText.split('\n').map(x => x.trim());
            root.querySelectorAll('*').forEach(el => { if (!el.children.length) out.push((el.textContent || '').trim()); });
            return out.filter(Boolean);
          }));
          names.forEach(n => { if (entries.has(n.trim())) fails.push(`#${r} shows the sample "${n}"`); });
        }
        console.log(`${fails.length ? 'FAIL' : 'ok  '} samples  ${samples.length} hidden from mocks, bank, drills and the Review, Drill and You pages, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log('FAIL samples  threw');
      }
      fails.forEach(f => failures.push(`samples: ${f}`));
    };


    /* ---------- Prerequisite gating (ENGINE-BACKLOG 490): part of --routes-only ----------
       The profile is swapped for a fresh one (and put back at the end). Checks: the first Stage 0 lesson is open; a Stage 3 lesson (a level 2 lesson
       of a Stage 3 course, so it holds before and after the requires lists are written) is locked, with a correct card, "Start here" opening, no "Open
       anyway" under Strict mode; outside Strict it shows and records the override; a test-out unlocks, and a failed one waits 24 hours; an old save with
       finished lessons is grandfathered; the course map draws the lock; Today names a locked course. */
    const gatingChecks = async () => {
      where = '#lesson (locked)';
      const fails = [], t0 = Date.now();
      const cur = readJSON(path.join(CONTENT, 'curriculum.json'));
      const firstLesson = (c, lvN) => { const cf = path.join(CONTENT, 'courses', c, 'course.json'); if (!fs.existsSync(cf)) return null; const lv = (readJSON(cf).levels || []).find(l => lvN == null || l.n === lvN); return lv ? (lv.lessons || []).find(l => fs.existsSync(path.join(CONTENT, 'courses', c, l + '.json'))) || null : null; };
      const firstOf = (stageId, lvN) => { for (const st of cur.stages.filter(x => x.id === stageId)) for (const t of st.topics) for (const c of t.courses || []) { const l = firstLesson(c, lvN); if (l) return `${c}/${l}`; } return null; };
      const allOf = (stageId, lvN) => { const out = []; for (const st of cur.stages.filter(x => x.id === stageId)) for (const t of st.topics) for (const c of t.courses || []) { const l = firstLesson(c, lvN); if (l) out.push(`${c}/${l}`); } return out; };
      /* the fixture is the first level 2 lesson (Stage 3, then Stage 2) that is locked on the fresh profile; a course optional for the role is advisory under Strict (ENGINE-BACKLOG 583) */
      const lockedCands = [...allOf(3, 2), ...allOf(2, 2)];
      const open0 = firstOf(0, 1);
      let locked3 = lockedCands[0] || null;
      if (!open0 || !locked3) { console.log('skip gating  no written Stage 0 level 1 lesson or Stage 2 or 3 level 2 lesson to check'); return; }
      const [oc, ol] = open0.split('/');
      let lc, ll;
      const widths = [DESKTOP, ...EXTRA];
      let saved = null;
      const evalOnly = (fn, arg) => page.evaluate(fn, arg);
      const importDoc = (patch) => page.evaluate((p) => {
        const d = JSON.parse(ZQ.state.export());
        d.lessons = {}; d.reviews = {}; d.homework = {}; d.exams = {}; d.redo = [];
        d.prereq = { met: {}, testouts: {}, opened: {}, grandfathered: true };
        d.settings.strictPrereqs = true; d.flags.setupDone = true;
        const r = ZQ.state.import(Object.assign(d, p || {}));
        return r && r.ok;
      }, patch);
      const route = async (r) => { await page.evaluate(() => { delete window.ZQ.test; }); await go('today'); await go(r); await page.waitForTimeout(500); };
      try {
        saved = await evalOnly(() => ZQ.state.export());
        if (!(await importDoc())) throw new Error('could not import a fresh profile');
        const lockedNow = await evalOnly((cs) => cs.filter(x => { const [c, l] = [x.split('/')[0], x.split('/')[1]]; return ZQ.prereq.lessonLocked(c, l); }), lockedCands);
        locked3 = lockedNow[0] || lockedCands[0];
        [lc, ll] = locked3.split('/');
        /* 1. Stage 0: open */
        await route(`lesson/${oc}/${ol}`);
        let st = await evalOnly(([c, l]) => ({ locked: ZQ.prereq.lessonLocked(c, l), card: !!document.querySelector('.lk'), lesson: !!document.querySelector('.lsn') }), [oc, ol]);
        if (st.locked || st.card || !st.lesson) fails.push(`${open0}: a Stage 0 first lesson should open on a fresh profile (locked ${st.locked}, card ${st.card}, lesson ${st.lesson})`);
        /* 2. Stage 3 lesson: locked, correct card */
        for (const wv of widths) {
          const w = wv.w;
          if (wv !== DESKTOP) await setVp(wv);
          await route(`lesson/${lc}/${ll}`);
          const c = await evalOnly(([c, l]) => {
            const m = ZQ.prereq.missingFor(c, l), q = (s) => [...document.querySelectorAll(s)];
            const direct = q('#lk-direct-h ~ details .lk-row').map(r => r.dataset.ref), indirectRows = q('.lk-more .lk-row').length;
            const startBtn = document.querySelector('.lk-start'), start = startBtn ? startBtn.dataset.start : null;
            const sm = start && /^lesson\/([^/]+)\/([^/]+)/.exec(start);
            return {
              locked: ZQ.prereq.lessonLocked(c, l), card: !!document.querySelector('.lk'), lesson: !!document.querySelector('.lsn'), title: (document.querySelector('.lk h1') || {}).textContent || '',
              want: m.direct.map(n => n.ref).sort(), direct: direct.sort(), allUnmet: m.direct.concat(m.indirect).every(n => !ZQ.prereq.refMet(n.ref)),
              nIndirect: m.indirect.length, indirectRows, hasMore: q('.lk-more').length, start, startOpens: sm ? !ZQ.prereq.lessonLocked(sm[1], sm[2]) : null,
              countText: (document.querySelector('#lk-direct-h .lk-n') || {}).textContent, openBtn: !!document.querySelector('[data-open]'), strictNote: !!document.querySelector('.lk-strict'),
              testouts: q('.lk-testout').length, wide: document.documentElement.scrollWidth > window.innerWidth + 1,
            };
          }, [lc, ll]);
          if (!c.locked) fails.push(`${locked3}: not locked on a fresh profile`);
          if (!c.card || c.lesson) fails.push(`${locked3} at ${w} px: the route should show the locked card, not the lesson`);
          if (!/is locked/.test(c.title)) fails.push(`${locked3}: the card title is "${c.title}"`);
          if (JSON.stringify(c.want) !== JSON.stringify(c.direct)) fails.push(`${locked3}: the card lists ${JSON.stringify(c.direct)} as direct, the rules give ${JSON.stringify(c.want)}`);
          if (!c.allUnmet) fails.push(`${locked3}: the card lists something already met`);
          if (c.countText !== String(c.want.length)) fails.push(`${locked3}: the direct count reads ${c.countText}, expected ${c.want.length}`);
          if (c.nIndirect && !c.hasMore) fails.push(`${locked3}: ${c.nIndirect} indirect prerequisites but no collapsed line`);
          if (c.hasMore && c.indirectRows !== c.nIndirect) fails.push(`${locked3}: ${c.indirectRows} indirect rows drawn, ${c.nIndirect} expected`);
          if (!c.start) fails.push(`${locked3}: no "Start here" button`); else if (!c.startOpens) fails.push(`${locked3}: "Start here" leads to ${c.start}, which is itself locked`);
          if (c.openBtn || !c.strictNote) fails.push(`${locked3}: Strict mode should hide "Open anyway" and say why`);
          if (c.wide) fails.push(`${locked3} at ${w} px: the locked card is wider than the window`);
          if (w === 1280) await shot('gate-locked-card');
          if (wv !== DESKTOP) await setVp(DESKTOP, 150);
        }
        /* 3. The course map draws the lock; Today names a locked course for a learner who started at Stage 3 */
        await route(`course/${lc}`);
        const mp = await evalOnly(([c, l]) => ({ n: document.querySelectorAll('.zc-node.s-locked').length, id: !!document.querySelector(`.zc-node.s-locked[data-id="${l}"]`) }), [lc, ll]);
        if (!mp.n || !mp.id) fails.push(`#course/${lc}: the locked lesson is not drawn locked (${mp.n} locked nodes)`);
        await evalOnly((l) => { const n = document.querySelector(`.zc-node.s-locked[data-id="${l}"]`); if (n) n.scrollIntoView({ block: 'center' }); }, ll);
        await shot('gate-course-map');
        await importDoc({ profile: Object.assign(JSON.parse(await evalOnly(() => ZQ.state.export())).profile, { startStage: 3 }) });
        await route('today');
        const td = await evalOnly(() => ({ line: !!document.querySelector('.lk-line'), start: !!document.querySelector('.lk-line [data-go]') }));
        if (!td.line && !(await evalOnly(() => ZQ.content.courses().some(c => c.stage >= 3 && ZQ.prereq.courseLocked(c.id) === false)))) fails.push('#today: a Stage 3 start with everything locked should say so');
        else if (td.line && !td.start) fails.push('#today: the locked line has no Start here');
        await importDoc();
        /* 4. Outside Strict mode: Open anyway shows, opens and records the override; the count shows on You */
        await evalOnly(() => ZQ.state.settings.set({ strictPrereqs: false }));
        await route(`lesson/${lc}/${ll}`);
        const ob = await evalOnly(() => ({ open: !!document.querySelector('[data-open]'), strictNote: !!document.querySelector('.lk-strict') }));
        if (!ob.open || ob.strictNote) fails.push(`${locked3}: outside Strict mode "Open anyway" should show`);
        else {
          await page.click('[data-open]'); await page.waitForTimeout(700);
          const op = await evalOnly(() => ({ lesson: !!document.querySelector('.lsn'), card: !!document.querySelector('.lk'), n: ZQ.prereq.openedCount() }));
          if (!op.lesson || op.card || op.n !== 1) fails.push(`${locked3}: Open anyway should open the lesson and record one override (lesson ${op.lesson}, card ${op.card}, recorded ${op.n})`);
          await route('you');
          if (!(await evalOnly(() => /opened early/i.test(document.querySelector('#app').innerText)))) fails.push('#you: the opened-early count is not shown');
        }
        await importDoc();
        await route('you');
        const sw = await evalOnly(() => { const b = document.querySelector('#yu-strictprereqs'); return b ? b.checked : null; });
        if (sw !== true) fails.push(`#you: the "Strict prerequisites" switch should be on by default (found ${sw})`);
        /* 5. A failed test-out waits 24 hours; a passed one unlocks */
        const pick = await evalOnly(([c, l]) => { const n = ZQ.prereq.missingFor(c, l).direct.find(x => x.kind === 'level' && x.testOut.can); return n ? { c: n.course, n: n.n } : null; }, [lc, ll]);
        if (!pick) console.log('     gating: no direct prerequisite with a written review to test out of; the test-out checks are skipped');
        else {
          await evalOnly((p) => ZQ.state.prereq.testout({ key: `${p.c}/L${p.n}`, score: 0, items: 6, passed: false, missed: [] }), pick);
          await route(`testout/${pick.c}/${pick.n}`);
          const wait = await evalOnly(() => (document.querySelector('.rvs-empty') || {}).innerText || '');
          if (!/Try again later/i.test(wait)) fails.push(`#testout/${pick.c}/${pick.n}: a failed test-out should wait 24 hours (page says "${wait.replace(/\s+/g, ' ').slice(0, 80)}")`);
          await importDoc();
          await playSet(`testout/${pick.c}/${pick.n}`, `testout ${pick.c}/L${pick.n}`, async () => {
            const r = await evalOnly((p) => ({ met: ZQ.prereq.levelMet(p.c, p.n), rec: ZQ.state.prereq.get().testouts[`${p.c}/L${p.n}`] || null, still: ZQ.prereq.missingFor(p.c, p.n).count }), pick);
            if (!r.met || !r.rec || !r.rec.passed) return { fail: `a passed test-out should mark the level met (met ${r.met}, record ${JSON.stringify(r.rec)})` };
            return { note: `${r.rec.score} of ${r.rec.items} right, level met` };
          });
          const after = await evalOnly(([c, l, p]) => ZQ.prereq.missingFor(c, l).direct.some(n => n.ref === `${p.c}/L${p.n}`), [lc, ll, pick]);
          if (after) fails.push(`${locked3}: the card still lists ${pick.c}/L${pick.n} after it was tested out`);
          await importDoc();
        }
        /* 6. An old save (no prereq record, every lesson of the level before it finished) is grandfathered once */
        const lv1 = readJSON(path.join(CONTENT, 'courses', lc, 'course.json')).levels.find(l => l.n === 1);
        const doneL = (lv1.lessons || []).filter(l => fs.existsSync(path.join(CONTENT, 'courses', lc, l + '.json')));
        const old = await evalOnly(([c, ls]) => {
          const d = JSON.parse(ZQ.state.export());
          d.lessons = {}; ls.forEach(l => { d.lessons[`${c}/${l}`] = { attempts: 1, done: true, firstTry: null, xp: 0, bestQuiz: null, mastered: false, perfect: false, completedAt: Date.now(), secondsSpent: 0, position: null, positionAt: null }; });
          d.reviews = {}; d.exams = {}; d.homework = {}; delete d.prereq; d.flags.setupDone = true;
          const r = ZQ.state.import(d);
          return { ok: r && r.ok, met: !!ZQ.state.prereq.get().met[`${c}/L1`], grand: ZQ.state.prereq.get().grandfathered, unlocked: !ZQ.prereq.lessonLocked(c, (ZQ.content.courseLessons(c).find(x => x.level === 2 && x.kind === 'lesson') || {}).id) };
        }, [lc, doneL]);
        if (!old.ok || !old.met || !old.grand) fails.push(`an old save with ${lc} level 1 finished was not grandfathered (${JSON.stringify(old)})`);
        else if (!old.unlocked && !readJSON(path.join(CONTENT, 'courses', lc, 'course.json')).levels.find(l => l.n === 2).requires) fails.push(`${lc} level 2 should be open for an old save that finished level 1`);
        /* 7. Engine pass E fix pass (ENGINE-BACKLOG 491 to 498) */
        /* 7a. The Refresh chip shows above a lesson's first screen whatever its kind (not only a title screen) */
        const chipCand = (() => {
          for (const st of cur.stages) for (const t of st.topics) for (const c of t.courses || []) {
            const cf = path.join(CONTENT, 'courses', c, 'course.json'); if (!fs.existsSync(cf)) continue;
            const lvs = readJSON(cf).levels || [];
            for (const [i, lv] of lvs.entries()) {
              if (i === 0 && !Array.isArray(lv.requires)) continue;
              const refs = Array.isArray(lv.requires) ? lv.requires : [`${c}/L${lvs[i - 1].n}`];
              for (const e of refs) {
                const r = typeof e === 'string' ? e : (e && e.gate !== false ? e.ref : null); if (!r) continue; /* object entries (ENGINE-BACKLOG 551); a diagnostic never gates */
                const m = /^([^/]+)\/L(\d+)$/.exec(r); if (!m) continue;
                const rf = path.join(CONTENT, 'courses', m[1], 'course.json'); if (!fs.existsSync(rf)) continue;
                const rl = (readJSON(rf).levels || []).find(x => x.n === +m[2]);
                if (!rl || !rl.review || !fs.existsSync(path.join(CONTENT, 'courses', m[1], rl.review + '.json'))) continue;
                for (const l of lv.lessons || []) {
                  const lf = path.join(CONTENT, 'courses', c, l + '.json'); if (!fs.existsSync(lf)) continue;
                  const first = ((readJSON(lf).screens || [])[0] || {}).type;
                  if (first && first !== 'title') return { c, l, ref: `${m[1]}/L${m[2]}`, first };
                }
              }
            }
          }
          return null;
        })();
        if (!chipCand) console.log('     gating: no lesson with a non-title first screen and a reviewed prerequisite; the Refresh chip check is skipped');
        else {
          const old = Date.now() - 31 * 86400000;
          await importDoc({ prereq: { met: { [chipCand.ref]: { at: old, how: 'testout' } }, testouts: {}, opened: {}, grandfathered: true } });
          await evalOnly(([c, l]) => ZQ.prereq.unlock(c, l), [chipCand.c, chipCand.l]);
          for (const wv of widths) {
          const w = wv.w;
            if (wv !== DESKTOP) await setVp(wv);
            await route(`lesson/${chipCand.c}/${chipCand.l}`);
            const ch = await evalOnly(() => { const a = document.querySelector('.lsn .rf-chip'); return { chip: !!a, href: a ? a.getAttribute('href') : '', wide: document.documentElement.scrollWidth > window.innerWidth + 1 }; });
            if (!ch.chip) fails.push(`${chipCand.c}/${chipCand.l} (first screen "${chipCand.first}") at ${w} px: no Refresh chip after ${chipCand.ref} was met 31 days ago`);
            else if (!/^#review\//.test(ch.href)) fails.push(`the Refresh chip links to ${ch.href}`);
            if (ch.wide) fails.push(`${chipCand.c}/${chipCand.l} at ${w} px: the Refresh chip made the page wider than the window`);
            if (wv !== DESKTOP) await setVp(DESKTOP, 150);
          }
          const lk = await evalOnly((ref) => { const c = ref.split('/')[0], n = +ref.split('/L')[1]; const lv = ZQ.content.course(c).levels.find(x => x.n === n); return { review: lv.review, locked: ZQ.prereq.itemLocked(c, lv.review) }; }, chipCand.ref);
          if (lk.locked) fails.push(`the Refresh link target ${chipCand.ref} ${lk.review} is locked`);
        }
        /* 7b. A level that is met is open as a place to work even when its own references are unmet */
        await importDoc();
        const mt = await evalOnly(() => {
          const L = ZQ.content.allCourses().flatMap(c => (c.levels || []).map(lv => ({ c: c.id, lv }))).find(({ c, lv }) => lv.review && ZQ.content.exists(c, lv.review) !== false && (lv.lessons || []).some(id => ZQ.content.exists(c, id) !== false) && ZQ.prereq.levelLocked(c, lv.n));
          return L ? { c: L.c, n: L.lv.n, review: L.lv.review, hw: L.lv.homework || '', lessons: L.lv.lessons } : null;
        });
        if (!mt) console.log('     gating: no locked level with a written review on a fresh profile; the met-level checks are skipped');
        else {
          await evalOnly((m) => ZQ.state.prereq.testout({ key: `${m.c}/L${m.n}`, score: 6, items: 6, passed: true, missed: [] }), mt);
          const r = await evalOnly((m) => ({ met: ZQ.prereq.levelMet(m.c, m.n), level: ZQ.prereq.levelLocked(m.c, m.n), review: ZQ.prereq.itemLocked(m.c, m.review), hw: m.hw ? ZQ.prereq.itemLocked(m.c, m.hw) : false, lessons: m.lessons.filter(id => ZQ.content.exists(m.c, id) !== false && ZQ.prereq.lessonLocked(m.c, id)) }), mt);
          if (!r.met || r.level || r.review || r.hw || r.lessons.length) fails.push(`${mt.c}/L${mt.n} tested out but not open: ${JSON.stringify(r)}`);
          await route(`review/${mt.c}/${mt.review}`);
          if (await evalOnly(() => !!document.querySelector('.lk'))) fails.push(`#review/${mt.c}/${mt.review}: a level that is met showed the locked card`);
          await importDoc();
        }
        /* 7b2. Readiness contract (PLAN 2c item 2): a trader is never offered graphs-dp or contests as Today's next work, and edges into an
           optional course are advisory (brainteasers L3 needs contests/L2; the graphs-dp edges into brainteasers L2 and game-theory L2 are diagnostics since item 8); a developer and an undecided learner still block. */
        {
          const OPT = ['graphs-dp', 'contests'];
          const todayCourse = async () => { await route('today'); return evalOnly(() => { const h = document.querySelector('.zt-hero'); return h ? h.getAttribute('aria-label') || '' : ''; }); };
          const optNames = await evalOnly((ids) => ids.map(i => ZQ.content.course(i).name), OPT);
          await importDoc({ profile: Object.assign(JSON.parse(await evalOnly(() => ZQ.state.export())).profile, { track: 'Trader', startStage: 0 }) });
          const fresh = await todayCourse();
          if (optNames.some(n => fresh.startsWith(n + ','))) fails.push(`a fresh trader was offered "${fresh}" on Today`);
          /* every written lesson of a required or recommended course done: Today must still not offer an optional course */
          await evalOnly(() => {
            const d = JSON.parse(ZQ.state.export()); d.profile.track = 'Trader';
            for (const c of ZQ.content.allCourses()) {
              if (ZQ.content.readiness.status(c.id, 'trader') === 'optional') continue;
              for (const x of ZQ.content.courseLessons(c.id)) if (x.kind === 'lesson' && x.written === true) d.lessons[`${c.id}/${x.id}`] = { attempts: 1, done: true, firstTry: null, xp: 0, bestQuiz: null, mastered: true, perfect: false, completedAt: Date.now(), secondsSpent: 0, position: null };
            }
            ZQ.state.import(d);
          });
          const after = await todayCourse();
          if (optNames.some(n => after.startsWith(n + ','))) fails.push(`a trader with all required and recommended work done was offered "${after}" on Today`);
          await importDoc({ profile: Object.assign(JSON.parse(await evalOnly(() => ZQ.state.export())).profile, { track: 'Trader' }) });
          const adv = (track) => evalOnly((t) => {
            ZQ.state.profile.set({ track: t });
            ZQ.prereq.unlockRefs(['brainteasers/L1', 'game-theory/L1', 'micro/L3', 'limits/L4', 'brainteasers/L2', 'mental/L3', 'series/L2', 'exp-log/L3']);
            const rest = ZQ.prereq.missingFor('brainteasers', ZQ.content.course('brainteasers').levels.find(l => l.n === 3).lessons[0]);
            return { bt: ZQ.prereq.levelLocked('brainteasers', 3), gt: ZQ.prereq.levelLocked('game-theory', 2), note: ZQ.prereq.advisoryForLevel('brainteasers', 3).length, direct: rest.direct.map(n => n.ref) };
          }, track);
          const tr = await adv('Trader');
          if (tr.bt || tr.gt) fails.push(`trader: brainteasers L3 locked ${tr.bt}, game-theory L2 locked ${tr.gt}; edges into contests should be advisory and graphs-dp diagnostics never lock`);
          if (!tr.note) fails.push('trader: brainteasers L3 shows no advisory note for contests/L2');
          await importDoc(); await evalOnly(() => ZQ.prereq.unlockRefs(['brainteasers/L1', 'game-theory/L1', 'micro/L3', 'limits/L4', 'brainteasers/L2', 'mental/L3', 'series/L2', 'exp-log/L3']));
          await evalOnly(() => ZQ.state.profile.set({ track: 'Trader' }));
          await route(`lesson/brainteasers/${await evalOnly(() => ZQ.content.course('brainteasers').levels.find(l => l.n === 3).lessons[0])}`);
          if (await evalOnly(() => !!document.querySelector('.lk') || !document.querySelector('.lsn'))) fails.push('trader: brainteasers L3 first lesson did not open without contests met');
          for (const t of ['Developer', 'Undecided']) {
            await importDoc(); await evalOnly(() => ZQ.prereq.unlockRefs(['brainteasers/L1', 'brainteasers/L2', 'mental/L3', 'series/L2', 'exp-log/L3']));
            const r = await evalOnly((t) => { ZQ.state.profile.set({ track: t }); return ZQ.prereq.levelLocked('brainteasers', 3); }, t);
            if (!r) fails.push(`${t}: brainteasers L3 should still lock while contests/L2 is unmet`);
          }
          await importDoc();
        }
        /* 7c. A started level (one lesson finished) keeps its other lessons open, and does not count as met */
        const sl = await evalOnly(() => {
          const L = ZQ.content.allCourses().flatMap(c => (c.levels || []).map(lv => ({ c: c.id, lv }))).find(({ c, lv }) => (lv.lessons || []).filter(id => ZQ.content.exists(c, id) !== false).length >= 2 && ZQ.prereq.levelLocked(c, lv.n));
          return L ? { c: L.c, n: L.lv.n, ids: L.lv.lessons.filter(id => ZQ.content.exists(L.c, id) !== false) } : null;
        });
        if (!sl) console.log('     gating: no locked level with two written lessons; the started-level check is skipped');
        else {
          const sr = await evalOnly((m) => {
            const d = JSON.parse(ZQ.state.export());
            d.lessons = { [`${m.c}/${m.ids[0]}`]: { attempts: 1, done: true, firstTry: null, xp: 0, bestQuiz: null, mastered: false, perfect: false, completedAt: Date.now(), secondsSpent: 0, position: null, positionAt: null } };
            d.prereq = { met: {}, testouts: {}, opened: {}, grandfathered: true }; d.reviews = {}; d.exams = {};
            ZQ.state.import(d); ZQ.prereq.sync();
            return { open: m.ids.map(id => !ZQ.prereq.lessonLocked(m.c, id)), met: ZQ.prereq.levelMet(m.c, m.n), started: !!ZQ.state.prereq.get().started[`${m.c}/L${m.n}`] };
          }, sl);
          if (!sr.started || !sr.open.every(Boolean) || sr.met) fails.push(`${sl.c}/L${sl.n}: a level with one finished lesson should stay open and not count as met (${JSON.stringify(sr)})`);
          await importDoc();
        }
        /* 7d. Direct and indirect grouping does not depend on list order; the card's closure equals one computed here from course.json */
        const ord = await evalOnly(([c, l]) => {
          const m = ZQ.prereq.missingFor(c, l), d = m.direct[0], e = d && d.refs.map(r => ZQ.prereq.missingRefs([r]).direct[0]).find(Boolean);
          if (!d || !e) return null;
          const a = ZQ.prereq.missingRefs([d.ref, e.ref]), b = ZQ.prereq.missingRefs([e.ref, d.ref]);
          return { a: a.direct.map(n => n.ref).sort(), b: b.direct.map(n => n.ref).sort(), want: [d.ref, e.ref].sort() };
        }, [lc, ll]);
        if (ord && (JSON.stringify(ord.a) !== JSON.stringify(ord.want) || JSON.stringify(ord.b) !== JSON.stringify(ord.want))) fails.push(`missingRefs groups by list order: ${JSON.stringify(ord)}`);
        {
          const closure = new Set(), cache = {}, courseDoc = (c) => (cache[c] = cache[c] || readJSON(path.join(CONTENT, 'courses', c, 'course.json')));
          const { refsOf } = (await import('node:module')).createRequire(import.meta.url)('../js/prereq.js');   // the one requires normaliser (ENGINE-BACKLOG 551): gating strings, objects allowed
          const refsOfLevel = (c, n) => { const lvs = courseDoc(c).levels, lv = lvs.find(x => x.n === n), i = lvs.indexOf(lv); return Array.isArray(lv.requires) ? refsOf(lv.requires) : i > 0 ? [`${c}/L${lvs[i - 1].n}`] : []; };
          const walk = (refs) => refs.forEach(r => {
            const m = /^([^/]+)\/(.+)$/.exec(r), c = m[1];
            const n = /^L\d+$/.test(m[2]) ? +m[2].slice(1) : courseDoc(c).levels.find(x => (x.lessons || []).includes(m[2])).n;
            const k = `${c}/L${n}`;
            if (closure.has(k)) return;
            closure.add(k); walk(refsOfLevel(c, n));
          });
          const lcd = courseDoc(lc), llv = lcd.levels.find(x => (x.lessons || []).includes(ll));
          walk((lcd.lessonRequires && lcd.lessonRequires[ll] && refsOf(lcd.lessonRequires[ll])) || refsOfLevel(lc, llv.n));
          const got = await evalOnly(([c, l]) => { const m = ZQ.prereq.missingFor(c, l); return m.direct.concat(m.indirect).map(n => `${n.course}/L${n.n}`); }, [lc, ll]);
          if (JSON.stringify([...closure].sort()) !== JSON.stringify([...new Set(got)].sort())) fails.push(`${locked3}: the card lists ${new Set(got).size} levels, the closure computed from course.json has ${closure.size}`);
        }
        /* 7d2. Route limitation (ENGINE-BACKLOG 551): the gating closure of a course (gate: false left out, own course excluded) reaches courses with a level that has no
           written lesson; the engine's list equals one computed here from course.json and the lesson files, and Learn shows "Route limited:" on such a course's card */
        {
          const cache = {}, courseDoc = (c) => (cache[c] = cache[c] || (fs.existsSync(path.join(CONTENT, 'courses', c, 'course.json')) ? readJSON(path.join(CONTENT, 'courses', c, 'course.json')) : null));
          const { refsOf } = (await import('node:module')).createRequire(import.meta.url)('../js/prereq.js');
          const written = (c, lv) => (lv.lessons || []).some(id => fs.existsSync(path.join(CONTENT, 'courses', c, id + '.json')));
          const levelRefs = (c, lv, i, lvs) => (Array.isArray(lv.requires) ? refsOf(lv.requires) : i > 0 ? [`${c}/L${lvs[i - 1].n}`] : []).concat((lv.lessons || []).flatMap(l => (courseDoc(c).lessonRequires && courseDoc(c).lessonRequires[l]) ? refsOf(courseDoc(c).lessonRequires[l]) : []));
          const expect = (self) => {
            const seen = new Set(), bad = new Set();
            const visit = (ref) => {
              const m = /^([^/]+)\/(.+)$/.exec(ref), c = m && m[1], d = c && courseDoc(c);
              if (!d) return;
              const lvs = d.levels || [], i = lvs.findIndex(x => /^L\d+$/.test(m[2]) ? x.n === +m[2].slice(1) : (x.lessons || []).includes(m[2]));
              if (i < 0 || seen.has(`${c}/${lvs[i].n}`)) return;
              seen.add(`${c}/${lvs[i].n}`);
              if (c !== self && !written(c, lvs[i])) bad.add(c);
              levelRefs(c, lvs[i], i, lvs).forEach(visit);
            };
            const sd = courseDoc(self);
            (sd.levels || []).forEach((lv, i, lvs) => levelRefs(self, lv, i, lvs).forEach(visit));
            return [...bad].sort();
          };
          const ids = cur.stages.flatMap(st => st.topics.flatMap(t => t.courses || [])).filter(c => courseDoc(c));
          const got = await evalOnly((cs) => Object.fromEntries(cs.map(c => [c, ZQ.prereq.routeLimitsForCourse(c).map(x => x.course).sort()])), ids);
          const diff = ids.filter(c => JSON.stringify(got[c]) !== JSON.stringify(expect(c)));
          if (diff.length) fails.push(`route limitation differs from course.json for ${diff.slice(0, 5).join(', ')}${diff.length > 5 ? ` and ${diff.length - 5} more` : ''} (engine ${JSON.stringify(got[diff[0]])}, files ${JSON.stringify(expect(diff[0]))})`);
          const lim = ids.includes('pdes') && got.pdes.length ? 'pdes' : ids.find(c => got[c].length);
          if (lim) {
            await route('learn');
            const stg = cur.stages.find(st => st.topics.some(t => (t.courses || []).includes(lim)));
            await evalOnly((n) => { const b = (sel) => document.querySelector(sel); if (b('.zl-view [data-view="courses"]')) b('.zl-view [data-view="courses"]').click(); if (b('.zl-tab[data-tab="all"]')) b('.zl-tab[data-tab="all"]').click(); if (b(`.zl-stages [data-stage="${n}"]`)) b(`.zl-stages [data-stage="${n}"]`).click(); }, stg.id);
            await page.waitForTimeout(400);
            const card = await evalOnly((c) => { const el = document.querySelector(`.zl-card[data-course="${c}"] .zl-route`); return el ? el.textContent : null; }, lim);
            if (card === null || !/^Route limited: .+ unwritten$/.test(card)) fails.push(`Learn: the ${lim} card should show "Route limited: <course> unwritten" (got ${JSON.stringify(card)})`);
          }
        }
        /* 7e. A test-out remembers the items it showed, across attempts */
        const sn = await evalOnly(() => { const k = 'gating-probe/L1'; ZQ.state.prereq.testout({ key: k, score: 0, items: 2, passed: false, seen: ['a', 'b'] }); ZQ.state.prereq.testout({ key: k, score: 0, items: 2, passed: false, seen: ['b', 'c'] }); return ZQ.state.prereq.get().testouts[k].seen; });
        if (JSON.stringify(sn) !== JSON.stringify(['a', 'b', 'c'])) fails.push(`a test-out should remember the items shown on every attempt (got ${JSON.stringify(sn)})`);
        await importDoc();
        /* 7f. A top-level requires on any exam file (here a stand-in topic exam) shows the locked card */
        await evalOnly(([c, l]) => {
          const ref = ZQ.prereq.missingFor(c, l).direct[0].ref, real = ZQ.content.exam;
          window.__realExam = real;
          ZQ.content.exam = (id) => (id === 'topic-gating-probe' ? Promise.resolve({ id, name: 'Gating probe', requires: [ref], items: [] }) : real.call(ZQ.content, id));
        }, [lc, ll]);
        await route('exam/topic-gating-probe');
        const ex = await evalOnly(() => ({ card: !!document.querySelector('.lk'), title: (document.querySelector('.lk h1') || {}).textContent || '' }));
        await evalOnly(() => { ZQ.content.exam = window.__realExam; delete window.__realExam; });
        if (!ex.card || !/is locked/.test(ex.title)) fails.push(`#exam/topic-gating-probe: an exam file with requires should show the locked card (card ${ex.card}, title "${ex.title}")`);
        await importDoc();
        console.log(`${fails.length ? 'FAIL' : 'ok  '} gating  Stage 0 open, ${locked3} locked with its card${ANY_EXTRA ? ' at ' + [DESKTOP, ...EXTRA].map(v => v.w).join(', ') + ' px' : ''}, Strict, Open anyway, test-out, old save, Refresh chip, met level open, started level, exam requires, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log('FAIL gating  threw');
      } finally {
        if (saved) { try { await evalOnly((d) => ZQ.state.import(d), saved); } catch { /* the run ends anyway */ } }
      }
      fails.forEach(f => failures.push(`gating: ${f}`));
    };

    /* ---------- Result provenance (PLAN 2c item 3, N01): part of --routes-only ----------
       (a) a homework of only longform items, all ticked in full, moves no prerequisite and no mastery-map cell (skills elo, mp, seen, correct) and
       the You screen shows it under Self-marked; (b) an old save without `how`, `passedAuto` or `selfMarked` imports and migrates as AUTHORING.md
       says: a met record is kept, an old exam pass cannot meet a level; (c) a topic exam passed only on self rows does not meet its levels,
       and the same pass on auto rows does. */
    const provenanceChecks = async () => {
      where = '#you (self-marked)';
      const fails = [], t0 = Date.now();
      let saved = null;
      try {
        saved = await page.evaluate(() => ZQ.state.export());
        const base = (p) => page.evaluate((patch) => {
          const d = JSON.parse(ZQ.state.export());
          d.lessons = {}; d.reviews = {}; d.homework = {}; d.exams = {}; d.redo = []; d.skills = {}; delete d.selfMarked;
          d.prereq = { met: {}, testouts: {}, opened: {}, started: {}, grandfathered: true };
          d.settings.strictPrereqs = true; d.flags.setupDone = true;
          return ZQ.state.import(Object.assign(d, patch || {})).ok;
        }, p);
        /* a homework with a longform item, and the course that holds it */
        const hw = await page.evaluate(async () => {
          for (const c of ZQ.content.courses()) {
            for (const lv of (c.levels || [])) {
              if (!lv.homework) continue;
              const D = await ZQ.content.homework(c.id, lv.homework).catch(() => null);
              const long = D && Array.isArray(D.items) ? D.items.filter(it => ZQ.state.provenance(it) === 'self') : [];
              if (long.length) return { cid: c.id, n: lv.n, id: lv.homework, items: long.map(it => ({ id: it.id, difficulty: it.difficulty || 3, skills: it.skills || [] })) };
            }
          }
          return null;
        });
        if (!hw) { console.log('skip provenance  no homework with a longform item'); return; }
        /* (a) */
        if (!(await base())) throw new Error('could not import a fresh profile');
        await page.evaluate(() => ZQ.prereq.sync());
        const before = await page.evaluate(() => ({ met: JSON.stringify(ZQ.state.prereq.get().met), skills: JSON.stringify(ZQ.state.skills), mp: ZQ.state.summary().mp }));
        await page.evaluate((h) => {
          ZQ.state.homeworkAssigned({ course: h.cid, level: h.n });
          ZQ.state.homeworkSubmitted({ course: h.cid, level: h.n, id: h.id, items: h.items.length, selfMarks: {}, results: h.items.map(it => ({ id: it.id, ok: true, difficulty: it.difficulty, skills: it.skills, how: ZQ.state.provenance({ kind: 'longform' }), ref: { course: h.cid, lesson: h.id, item: it.id } })) });
          ZQ.prereq.sync();
        }, hw);
        const after = await page.evaluate(() => ({ met: JSON.stringify(ZQ.state.prereq.get().met), skills: JSON.stringify(ZQ.state.skills), mp: ZQ.state.summary().mp, self: JSON.stringify(ZQ.state.selfMarked) }));
        if (after.met !== before.met) fails.push('a longform-only homework changed the prerequisite met records');
        if (after.skills !== before.skills) fails.push('a longform-only homework changed a mastery-map skill record (elo, mp, seen or correct)');
        if (after.mp !== before.mp) fails.push(`a longform-only homework added mastery points (${before.mp} to ${after.mp})`);
        const skillIds = [...new Set(hw.items.flatMap(it => it.skills))];
        if (skillIds.length && !skillIds.every(k => JSON.parse(after.self)[k])) fails.push('the self-marked skills are not stored in state.selfMarked');
        await go('today'); await go('you'); await page.waitForTimeout(400);
        const you = await page.evaluate(() => { const c = document.querySelector('[data-card="selfmarked"]'); return { shown: !!c && !c.hidden, text: c ? c.innerText : '', cells: document.querySelectorAll('.yu-cell:not(.b0)').length }; });
        if (skillIds.length && (!you.shown || !/Self-marked/.test(you.text))) fails.push('the You screen does not show the Self-marked block');
        if (you.cells) fails.push(`${you.cells} mastery-map cell(s) are shaded after a longform-only homework`);
        /* (b) an old save: no how, no passedAuto, no selfMarked */
        const key = `${hw.cid}/L${hw.n}`;
        const old = await page.evaluate(([h, k]) => {
          const d = JSON.parse(ZQ.state.export());
          d.lessons = {}; d.homework = {}; delete d.selfMarked; d.redo = [];
          d.skills = { 'old-skill': { mp: 4, elo: 1040, seen: 3, correct: 2, lastAt: 1 } };
          d.reviews = { [`${h.cid}/old-review`]: { score: 8, items: 10, at: 1, passed: true } };
          d.exams = { 'topic-9.9': { attempts: [{ at: 1, score: 9, items: 10, passed: true, bySkill: {} }] } };
          d.prereq = { met: { [k]: { at: 1, how: 'derived' } }, testouts: {}, opened: {}, started: {}, grandfathered: true };
          const r = ZQ.state.import(JSON.stringify(d));
          return { ok: r.ok, self: JSON.stringify(ZQ.state.selfMarked), skills: JSON.stringify(ZQ.state.skills['old-skill']), kept: ZQ.prereq.levelMet(h.cid, h.n), attempt: ZQ.state.exams['topic-9.9'].attempts[0].passedAuto, review: ZQ.state.reviews[`${h.cid}/old-review`].passedAuto };
        }, [hw, key]);
        if (!old.ok) fails.push('an old save without provenance fields did not import');
        if (old.self !== '{}') fails.push(`an old save should migrate to an empty selfMarked, got ${old.self}`);
        if (old.skills !== JSON.stringify({ mp: 4, elo: 1040, seen: 3, correct: 2, lastAt: 1 })) fails.push('an old skills record was altered by the import');
        if (!old.kept) fails.push('an existing met record was lost on import');
        if (old.attempt !== undefined || old.review !== undefined) fails.push('the import invented a passedAuto on an old record');
        /* (c) a topic exam passed on self rows only */
        const topic = await page.evaluate(() => { for (const s of ZQ.content.allStages()) for (const t of s.topics) { const c = (t.courses || []).find(id => (ZQ.content.course(id) || {}).levels && ZQ.content.course(id).levels.length); if (c) return { id: t.id, cid: c, n: ZQ.content.course(c).levels[0].n }; } return null; });
        if (!topic) fails.push('no topic with a course to test the exam rule on');
        else {
          await base();
          /* PLAN 2c item 4 (rule 4): the pass meets a level only when its auto rows cover the level's essential skills (the review's item skills) at the floor, so the rows carry them */
          const rule = (passedAuto) => page.evaluate(async (t) => {
            const lv0 = ZQ.content.course(t.t.cid).levels.find(l => l.n === t.t.n), RV = await ZQ.content.review(t.t.cid, lv0.review);
            const ess = [...new Set(((RV && RV.items) || []).flatMap(it => it.skills || []))];
            const rows = [...ess.map((sk, i) => ({ id: 'a' + i, ok: !!t.pa, how: 'auto', skills: [sk] })), { id: 'b', ok: true, how: 'self', skills: [] }, { id: 'c', ok: true, how: 'self', skills: [] }];
            const x = { id: 'topic-' + t.t.id, score: 2, items: rows.length, passed: true, results: rows };
            ZQ.state.examFinished(Object.assign(x, { passedAuto: t.pa }));
            ZQ.prereq.sync();
            const a = ZQ.state.exams[x.id].attempts.slice(-1)[0];
            return { met: ZQ.prereq.levelMet(t.t.cid, t.t.n), passedAuto: a.passedAuto, passed: a.passed };
          }, { t: topic, pa: passedAuto });
          const self = await rule(false);
          if (self.met) fails.push(`a topic exam passed only on self rows met ${topic.cid} level ${topic.n}`);
          await base();
          const auto = await rule(true);
          if (!auto.met && auto.passedAuto !== true) fails.push('a recorded passedAuto of true was not stored');
          else if (!auto.met) fails.push(`a topic exam passed on auto rows did not meet ${topic.cid} level ${topic.n}`);
        }
        /* (d) an old passed attempt with no passedAuto: fully auto on an exam with no self item (topic-1.5), not counted on one with longform (topic-1.1).
           Under rule 4 it holds no per-skill record, so even where it counts as a pass (topicPassed) it meets no level. */
        for (const [tid, want] of [['1.5', true], ['1.1', false]]) {
          await base();
          const got = await page.evaluate((t) => {
            const T = ZQ.content.topic(t), c = (T.courses || []).find(id => (ZQ.content.course(id) || {}).levels && ZQ.content.course(id).levels.length);
            if (!c) return null;
            const d = JSON.parse(ZQ.state.export());
            d.exams = { ['topic-' + t]: { attempts: [{ at: 1, score: 9, items: 10, passed: true, bySkill: {} }] } };
            ZQ.state.import(JSON.stringify(d)); ZQ.prereq.sync();
            return { met: ZQ.prereq.levelMet(c, ZQ.content.course(c).levels[0].n), passed: ZQ.content.topicPassed(t) };
          }, tid);
          if (!got) fails.push(`topic ${tid} has no course with levels to test an old attempt`);
          else if (got.met !== false || got.passed !== want) fails.push(`an old passed attempt with no passedAuto on topic-${tid} should ${want ? '' : 'not '}count as a pass and meet no level (met ${got.met}, topicPassed ${got.passed})`);
        }
        console.log(`${fails.length ? 'FAIL' : 'ok  '} provenance  ${hw.id}: longform-only homework moves no met record or map cell, shown as Self-marked; old save migrates; self-only exam pass meets nothing, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log('FAIL provenance  threw');
      } finally {
        if (saved) { try { await page.evaluate((d) => ZQ.state.import(d), saved); } catch { /* the run ends anyway */ } }
      }
      fails.forEach(f => failures.push(`provenance: ${f}`));
    };

    /* ---------- Capstone card and role verdicts (PLAN 2c item 8, F06, ENGINE-BACKLOG 564, 566): part of --routes-only ----------
       A fresh profile: no role is ready (ZQ.content.readiness.roleState), Today never says "ready" as a role verdict, and the You screen draws the Capstone card
       with one read-only block per role, the learner's own role first, no sideways scroll, and a note that the reviewer fills content/capstones.json. */
    const capstoneChecks = async () => {
      where = '#you (capstone)';
      const fails = [];
      let saved = null;
      try {
        saved = await page.evaluate(() => ZQ.state.export());
        await page.evaluate(() => {
          const d = JSON.parse(ZQ.state.export());
          d.lessons = {}; d.reviews = {}; d.homework = {}; d.exams = {}; d.redo = []; d.skills = {}; d.flags.setupDone = true;
          d.prereq = { met: {}, testouts: {}, opened: {}, started: {}, grandfathered: true };
          d.profile = Object.assign(d.profile || {}, { track: 'Researcher' });
          ZQ.state.import(d); ZQ.prereq.sync(); ZQ.content._setCapstones([]);
        });
        const roles = await page.evaluate(() => ['trader', 'researcher', 'developer', 'strats', 'strats-deriv'].map(r => ({ r, ready: ZQ.content.readiness.roleState(r).ready, v: ZQ.content.readiness.verdict(r) })));
        roles.filter(x => x.ready || /^ready/i.test(x.v)).forEach(x => fails.push(`a fresh profile shows ${x.r} as ready`));
        await go('today'); await page.waitForTimeout(400);
        const today = await page.evaluate(() => (document.querySelector('.screen-today') || document.body).innerText);
        if (/\bready\b/i.test(today)) fails.push(`Today says "ready" for a fresh profile: ${(today.match(/.{0,30}\bready\b.{0,20}/i) || [''])[0].replace(/\s+/g, ' ')}`);
        await go('you'); await page.waitForTimeout(400);
        const you = await page.evaluate(() => { const c = document.querySelector('[data-card="capstone"]'); return { has: !!c, text: c ? c.innerText : '', roles: c ? [...c.querySelectorAll('.yu-cp')].map(n => n.dataset.role) : [], wide: document.documentElement.scrollWidth > window.innerWidth + 1, vw: window.innerWidth }; });
        if (!you.has) fails.push('the You screen has no Capstone card');
        else {
          if (you.roles.join(',') !== 'researcher,trader,developer,strats,strats-deriv') fails.push(`capstone roles in order ${you.roles.join(',')}, expected the learner's role first`);
          if (!/content\/capstones\.json/.test(you.text)) fails.push('the Capstone card does not say the reviewer fills content/capstones.json');
          if (/\bready\b/i.test(you.text.replace(/A role is ready only[^.]*\./i, ''))) fails.push('the Capstone card shows "ready" as a verdict');
          if (you.wide) fails.push(`the You screen scrolls sideways with the Capstone card at ${you.vw} px`);
        }
        console.log(`${fails.length ? 'FAIL' : 'ok  '} capstone  fresh profile: no role ready, Today clear of "ready", You card for ${you.roles.length} roles, no sideways scroll`);
      } catch (e) {
        fails.push('threw: ' + String(e.message || e).split('\n')[0]);
        console.log('FAIL capstone  threw');
      } finally {
        if (saved) { try { await page.evaluate((d) => ZQ.state.import(d), saved); } catch { /* the run ends anyway */ } }
      }
      fails.forEach(f => failures.push(`capstone: ${f}`));
    };

    /* Every other route once */
    if (opt.bankIds.length) await bankPlay(opt.bankIds);
    if (runRoutes) {
      /* the route checks (bank counts, samples hidden from You) assume a fresh profile; after played items (--all, shard 1) start one */
      if (played > 0) await freshSetup();
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
            /* Prepare for: the chosen path lists every step, and nothing spills sideways (also at every --mobile, --narrow and --tablet width) */
            const pid = r.split('/')[1] || (['general', 'stage', 'firm'].map(k => prepPaths.find(p => p.kind === k)).find(Boolean) || {}).id, want = ((prepPaths.find(p => p.id === pid) || {}).steps || []).length;
            const probe = () => page.evaluate(() => ({ steps: document.querySelectorAll('.pp-step').length, wide: document.documentElement.scrollWidth > window.innerWidth + 1, bad: document.querySelectorAll('.pp-step a[href="#course/undefined"]').length }));
            for (const wv of [DESKTOP, ...EXTRA]) {
              const w = wv.w;
              if (wv !== DESKTOP) await setVp(wv);
              const got = await probe();
              if (got.steps !== want) failures.push(`#${r} at ${w} px: ${got.steps} steps drawn, ${want} in prep.json`);
              if (got.wide) failures.push(`#${r} at ${w} px: the page is wider than the window`);
              if (got.bad) failures.push(`#${r}: a step links to an unknown course`);
              if (wv !== DESKTOP) await setVp(DESKTOP, 150);
            }
          }
          await shot('route-' + r);
        } catch (e) { failures.push(`#${r}: threw ${String(e.message || e).split('\n')[0]}`); }
        console.log(`${consoleErrors.length > before ? 'ERR ' : 'ok  '} #${r}`);
      }
      /* The interview bank deck and per-item timing (ENGINE-BACKLOG 456, 457), then an exam sat with a skewed clock */
      await bankChecks();
      await drillRouteChecks();
      await sampleChecks();
      await gatingChecks();
      await provenanceChecks();
      await capstoneChecks();
      if (!exams.includes('mock-oa-code')) await holdoutChecks('mock-oa-code');
      await versionChecks();
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
    console.log(`\nbrowser relaunches: ${relaunches}`);
    process.exit(1);
  }
  console.log(`\nbrowser relaunches: ${relaunches}`);
  console.log('All passed.');
};
main().catch((e) => { console.error(e); process.exit(2); });
