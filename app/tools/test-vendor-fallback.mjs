#!/usr/bin/env node
/* Self-hosting fallback test: with cdn.jsdelivr.net unreachable, the app still runs from app/vendor/ (README.md, "Self-hosting (offline use)").
   Run from app/:  node tools/test-vendor-fallback.mjs --vendor <dir> [--absent]
     --vendor <dir>  a folder made by tools/fetch-vendor.sh (pyodide/, mathlive/, compute-engine/, yowasp-clang/). Each is symlinked into app/vendor for the
                     run and removed afterwards; one that already exists in app/vendor is used as it is and left alone. Without --vendor, app/vendor is used.
     --absent        the opposite check: run with the four folders hidden and show that the failure is the expected one (Python and C++ fail saying there is no
                     local copy; the maths editor falls back to its plain text box and the expression lesson still passes).
   Part 1: a Playwright page with every cdn.jsdelivr.net request aborted loads ZQ.grade.maths(): MathLive registers <math-field> from vendor/mathlive/ without a
   failed request, and the Compute Engine from vendor/compute-engine/ grades x^2-1 equal to (x-1)(x+1) and not to x^2+1.
   Part 2: playthrough.mjs --local-cdn <empty folder> (every jsDelivr request answered 404, the same as an unreachable CDN, and nothing else served) plays one
   Python lesson (code widgets run by Pyodide), one C++ lesson (YoWASP Clang) and one expression lesson; each must pass, so each can only have loaded from vendor/.
   Part 3 (--absent only, ENGINE-BACKLOG 1214): with the CDN refused, no vendor/ copy, and a Python and a C++ code screen of a lesson, and the Python drill page:
   the page reports the load failure within 20 s under a neutral heading ("Python could not load", "C++ could not load"), not "Not quite right.": no wrong-answer
   chip or frame, no XP, Try again offered and it retries the load. In a normal run the numpy lesson (numpy-pandas/l1-not-lists) is the NumPy-from-vendor case (1215).
   Needs Playwright and Chromium. Exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import { spawnSync, execSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const argv = process.argv.slice(2);
const arg = (n) => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : null; };
const ABSENT = argv.includes('--absent');
const SRC = arg('--vendor') ? path.resolve(arg('--vendor')) : null;
const NAMES = ['pyodide', 'mathlive', 'compute-engine', 'yowasp-clang'];
const LESSONS = { python: 'first-python/l1-calculator', cpp: 'cpp-pricing/l1-doubles', expr: 'algebra/l1-symmetries', ...(ABSENT ? {} : { numpy: 'numpy-pandas/l1-not-lists' }) };   // numpy: a lesson whose code imports NumPy, so its wheels load from vendor/pyodide (ENGINE-BACKLOG 1215)
const GIVE_UP_MS = 20000;   // ENGINE-BACKLOG 1214: with the CDN refusing and no vendor/ copy, Python (lesson and drill) and C++ must report within this
const CHROMIUM = '/opt/pw-browsers/chromium';
const loadPlaywright = async () => {
  try { return await import('playwright'); } catch { /* not local */ }
  const roots = [];
  try { roots.push(execSync('npm root -g', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()); } catch { /* no npm */ }
  (process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).forEach(p => roots.push(p));
  for (const r of roots) { const f = path.join(r, 'playwright', 'index.mjs'); if (fs.existsSync(f)) return import(pathToFileURL(f).href); }
  console.error('Playwright is not installed (npm i -g playwright)'); process.exit(2);
};
const { chromium } = await loadPlaywright();
let bad = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) bad++; };

/* ---------- vendor folders into place, and out again ---------- */
const VENDOR = path.join(APP, 'vendor');
const linked = [], hidden = [];
const restore = () => {
  for (const l of linked.splice(0)) { try { fs.unlinkSync(l); } catch { /* gone */ } }
  for (const [from, to] of hidden.splice(0)) { try { fs.renameSync(to, from); } catch { /* gone */ } }
};
process.on('exit', restore);
for (const s of ['SIGINT', 'SIGTERM']) process.on(s, () => { restore(); process.exit(130); });
if (ABSENT) {
  for (const n of NAMES) { const p = path.join(VENDOR, n); if (fs.existsSync(p)) { const to = p + '.hidden-by-test'; fs.renameSync(p, to); hidden.push([p, to]); } }
} else if (SRC) {
  for (const n of NAMES) {
    const p = path.join(VENDOR, n);
    if (fs.existsSync(p)) continue;
    if (!fs.existsSync(path.join(SRC, n))) { console.error(`FAIL no ${n}/ in ${SRC} (run tools/fetch-vendor.sh <dir>)`); process.exit(1); }
    fs.symlinkSync(path.join(SRC, n), p, 'dir'); linked.push(p);
  }
}
if (!ABSENT) for (const n of NAMES) if (!fs.existsSync(path.join(VENDOR, n))) { console.error(`FAIL app/vendor/${n} is missing: give --vendor <dir>`); process.exit(1); }

/* ---------- a small static server over app/ (follows the symlinks) ---------- */
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm',
  '.zip': 'application/zip', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.whl': 'application/zip', '.wav': 'audio/wav', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  const f = path.join(APP, path.normalize(u === '/' ? '/index.html' : u));
  if (!f.startsWith(APP) || !fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' });
  if (req.method === 'HEAD') return res.end();
  fs.createReadStream(f).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}`;

/* ---------- part 1: the maths libraries, CDN blocked ---------- */
{
  const browser = await chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
  const ctx = await browser.newContext();
  const blocked = [], vendorReq = [];
  await ctx.route(/^https:\/\/(cdn\.jsdelivr\.net|fonts\.(googleapis|gstatic)\.com)\//, (r) => { blocked.push(r.request().url()); return r.abort(); });
  const page = await ctx.newPage();
  page.on('response', (r) => { if (r.url().startsWith(base + '/vendor/')) vendorReq.push([r.status(), r.url().slice(base.length)]); });
  await page.goto(base + '/index.html');
  await page.waitForFunction(() => window.ZQ && window.ZQ.grade && window.ZQ.grade.maths, null, { timeout: 20000 });
  const r = await page.evaluate(async () => {
    const m = await window.ZQ.grade.maths();
    const out = { mathlive: !!m.mathlive, field: !!window.customElements.get('math-field'), ce: !!m.ce };
    if (m.ce) {
      const eq = (a, b) => { try { return !!m.ce.parse(a).simplify().isEqual(m.ce.parse(b).simplify()); } catch { return null; } };
      out.same = eq('x^2-1', '(x-1)(x+1)'); out.diff = eq('x^2-1', 'x^2+1');
    }
    if (m.mathlive) { const f = document.createElement('math-field'); f.value = '\\frac{x}{2}+\\sqrt{3}'; f.style.fontSize = '24px'; document.body.append(f); await new Promise(r => setTimeout(r, 2500)); out.value = f.value; out.fonts = document.fonts.check('16px KaTeX_Main'); }
    return out;
  });
  if (ABSENT) {
    check('absent: the maths editor reports no MathLive and no Compute Engine', !r.mathlive && !r.ce, JSON.stringify(r));
  } else {
    check('maths: MathLive registers math-field from vendor/mathlive', r.mathlive && r.field && vendorReq.some(([s, u]) => s === 200 && u === '/vendor/mathlive/mathlive.min.js'), JSON.stringify([r, vendorReq.slice(0, 5)]));
    /* MathLive 0.105 resolves fontsDirectory (./fonts) and soundsDirectory (./sounds) next to its own script, and asks for fonts only when the KaTeX
       families are not already in the page; the app has them from vendor/katex, so none is requested here. Sounds load on a key press. Both folders are
       copied anyway; the check is that nothing under vendor/mathlive/ failed and the maths fonts are usable. */
    check('maths: nothing under vendor/mathlive failed, and the KaTeX fonts are usable in the field', !vendorReq.some(([s, u]) => s >= 400 && /^\/vendor\/mathlive\//.test(u)) && r.fonts === true, JSON.stringify([r.fonts, vendorReq.filter(([s]) => s >= 400)]));
    check('maths: a math-field holds the typed formula', /frac\{x\}\{2\}/.test(r.value || ''), String(r.value));
    check('maths: Compute Engine from vendor/compute-engine grades x^2-1 equal to (x-1)(x+1), not to x^2+1', r.ce && r.same === true && r.diff === false, JSON.stringify(r));
  }
  check('the CDN was blocked (the page asked for it and got nothing)', blocked.some(u => /cdn\.jsdelivr\.net/.test(u)));
  await browser.close();
}
/* ---------- part 3 (--absent): a load failure is not a wrong answer, and it is reported within seconds ---------- */
if (ABSENT) {
  const browser = await chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
  const open = async (hash, setup, arg, hang = false) => {
    const ctx = await browser.newContext({ viewport: { width: 1000, height: 900 } });
    await ctx.route(/^https:\/\/(cdn\.jsdelivr\.net|fonts\.(googleapis|gstatic)\.com)\//, (r) => (hang && /cdn\.jsdelivr/.test(r.request().url()) ? undefined : r.abort()));   // hang: the request is never answered, as behind a proxy that holds the connection
    const page = await ctx.newPage();
    await page.goto(base + '/#setup');
    await page.waitForFunction(() => window.ZQ && ZQ.content && ZQ.content.ready && ZQ.state, null, { timeout: 20000 });
    await page.evaluate(() => ZQ.content.ready);
    await page.waitForSelector('[data-name]', { timeout: 20000 });
    await page.fill('[data-name]', 'Offline');
    await page.click('[data-next]'); await page.click('[data-track="Trader"]'); await page.click('[data-next]');
    await page.click('[data-h="15"]'); await page.click('[data-stage="1"]'); await page.click('[data-next]');
    await page.waitForFunction(() => ZQ.state.flags.setupDone === true, null, { timeout: 20000 });
    if (setup) await page.evaluate(setup, arg);
    const t0 = Date.now();
    await page.evaluate((h) => { location.hash = h; }, hash);
    return { ctx, page, t0 };
  };
  const lessonCase = async (what, course, lesson, screen, sel, hang = false) => {
    const { ctx, page, t0 } = await open(`lesson/${course}/${lesson}`, ([c, l, i]) => { ZQ.prereq.unlock(c, l); ZQ.state.lessonPosition.set(c, l, { phase: 'lesson', i, xp: 0, checks: 0, okChecks: 0, anyCheck: false, results: {}, quiz: [] }); }, [course, lesson, screen], hang);
    try {
      await page.waitForSelector(`${sel} .wd-py[data-s="unavailable"]`, { timeout: GIVE_UP_MS });
      const ms = Date.now() - t0;
      check(`absent: ${what} reports the failed load within ${GIVE_UP_MS / 1000} s${hang ? ' with the CDN holding the connection open' : ''} (${(ms / 1000).toFixed(1)} s)`, ms < GIVE_UP_MS);
      const btn = page.locator('.lsn-primary');
      await page.waitForFunction(() => { const b = document.querySelector('.lsn-primary'); return b && !b.disabled; }, null, { timeout: 5000 });
      const xp0 = await page.textContent('.lsn-xp-n');
      await btn.click();
      await page.waitForSelector('.lsn-chip', { timeout: 5000 });
      const r = await page.evaluate(() => ({ head: document.querySelector('.lsn-chip-h b').textContent, cls: document.querySelector('.lsn-chip').className, frame: document.querySelector('.lsn').className, primary: document.querySelector('.lsn-primary').textContent, xp: document.querySelector('.lsn-xp-n').textContent, text: document.querySelector('.lsn-verdict').textContent }));
      check(`absent: ${what} heading is neutral ("${r.head}"), not "Not quite right."`, r.head === `${what} could not load` && !/Not quite right|Give it another shot/.test(r.text), JSON.stringify(r));
      check(`absent: ${what} shows no wrong-answer styling, no XP change`, !/is-no/.test(r.cls) && !/is-no/.test(r.frame) && r.xp === xp0, JSON.stringify(r));
      check(`absent: ${what} offers Try again`, r.primary === 'Try again', r.primary);
      await btn.click();
      const loading = await page.evaluate(() => document.querySelector('.lsn-chip') === null);
      check(`absent: ${what} Try again clears the notice and retries the load`, loading);
      await page.waitForSelector(`${sel} .wd-py[data-s="unavailable"]`, { timeout: GIVE_UP_MS });
      check(`absent: ${what} reports again after the retry`, true);
    } catch (e) { check(`absent: ${what} lesson case`, false, String(e.message || e).split('\n')[0] + ' | ' + await page.evaluate(() => location.hash + ' ' + [...document.querySelectorAll('.wd-py, .drl-py')].map(e => e.textContent).join(' / ') + ' ' + document.body.innerText.replace(/\s+/g, ' ').slice(0, 120)).catch(() => '')); }
    await ctx.close();
  };
  await lessonCase('Python', 'first-python', 'l1-calculator', 2, '.wd-code:not(.wd-cpp)');
  await lessonCase('Python', 'first-python', 'l1-calculator', 2, '.wd-code:not(.wd-cpp)', true);
  await lessonCase('C++', 'cpp-pricing', 'l1-doubles', 5, '.wd-cpp');
  {
    const { ctx, page, t0 } = await open('drill/annualised-vol');
    try {
      await page.waitForSelector('.drl-notice', { state: 'attached', timeout: GIVE_UP_MS });
      const ms = Date.now() - t0, head = (await page.textContent('.drl-notice .t-h2')).trim();
      check(`absent: the drill page reports the failed load within ${GIVE_UP_MS / 1000} s (${(ms / 1000).toFixed(1)} s) as "Python could not load"`, ms < GIVE_UP_MS && /^Python could not load$/.test(head), head);
    } catch (e) { check('absent: drill page case', false, String(e.message || e).split('\n')[0] + ' | ' + await page.evaluate(() => location.hash + ' ' + [...document.querySelectorAll('.wd-py, .drl-py')].map(e => e.textContent).join(' / ') + ' ' + document.body.innerText.replace(/\s+/g, ' ').slice(0, 120)).catch(() => '')); }
    await ctx.close();
  }
  await browser.close();
}
server.close();

/* ---------- part 2: real lessons through the playthrough, with the CDN answering 404 ---------- */
const empty = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-empty-cdn-'));
for (const [what, lesson] of Object.entries(LESSONS)) {
  const r = spawnSync(process.execPath, [path.join(HERE, 'playthrough.mjs'), '--lesson', lesson, '--local-cdn', empty, '--no-cache', '--no-routes'], { cwd: APP, encoding: 'utf8', timeout: 900000 });
  const tail = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').slice(-6).join(' | ').slice(0, 600);
  if (ABSENT && what === 'expr') check(`absent: ${what} lesson ${lesson} still passes on the plain text box (the editor degrades, it does not fail)`, r.status === 0, tail);
  else if (ABSENT) check(`absent: ${what} lesson ${lesson} fails`, r.status !== 0, tail);
  else check(`${what} lesson ${lesson} passes from vendor/ with the CDN down`, r.status === 0, tail);
  if (ABSENT && r.status !== 0 && what !== 'expr') {
    const text = (r.stdout || '') + (r.stderr || '');
    check(`absent: ${what} failure says there is no local copy`, /no local copy|could not be loaded|unreachable|unavailable/i.test(text), tail);
  }
}
fs.rmSync(empty, { recursive: true, force: true });
restore();
console.log(bad ? `\n${bad} failed` : '\nall passed');
process.exit(bad ? 1 : 0);
