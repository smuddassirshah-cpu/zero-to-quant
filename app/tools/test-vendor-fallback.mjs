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
const LESSONS = { python: 'first-python/l1-calculator', cpp: 'cpp-pricing/l1-doubles', expr: 'algebra/l1-symmetries' };
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
