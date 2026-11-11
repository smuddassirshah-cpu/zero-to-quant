#!/usr/bin/env node
/* Tests for deep recursion on the Python code surfaces (ENGINE-BACKLOG 917). Run from app/: node tools/test-drill-recursion.mjs [--local-cdn <pkgs>] [--no-browser]
   The fault: in Pyodide 0.27.7 the browser stack, not Python's recursion limit, ends a recursion that passes through C code at every level
   (a C functools.lru_cache, a generator expression inside min()). Python then died with no message, the page read the run as a crash, the tests
   after it were skipped and a right solution was marked wrong. Every surface (drill page, lesson code screens, exams, bank) runs Python in
   js/screens/drill-worker.js, so the worker is tested directly, then the drill page is played with tools/fixtures/drill-recursion/drill-ab-recursion.json.
     1. Source: one Python runner only, shared by drill.js and the code widget.
     2. Worker: an lru_cache recursion 800 and 1,400 deep passes; a dict recursion raised to 50,000 passes; a recursion through a generator
        expression too deep for the stack fails only that test with a RecursionError message, and the tests after it run and pass; a recursion too
        deep at load time is a load error, not a silence.
     3. Drill page: the fixture drill with an lru_cache solution that puts a generator in every call of the largest test: that test (index 2) is
        an error saying RecursionError, every other test passes, the run is not a crash and the page does not say "Python stopped".
   Needs Playwright and Chromium for parts 2 and 3 (skipped with --no-browser). Exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, spawnSync, execSync } from 'node:child_process';
import net from 'node:net';
import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const argv = process.argv.slice(2);
const cdnI = argv.indexOf('--local-cdn'), CDN = cdnI >= 0 ? path.resolve(argv[cdnI + 1]) : (process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null);
let bad = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) bad++; };

/* ---------- 1. one runner ---------- */
const read = (f) => fs.readFileSync(path.join(APP, f), 'utf8');
const users = ['js/screens/drill.js', 'js/engine/widgets/code.js'];
check('drill.js and the code widget both start js/screens/drill-worker.js', users.every(f => /drill-worker\.js/.test(read(f))));
const others = [];
(function walk(d) { for (const e of fs.readdirSync(path.join(APP, d), { withFileTypes: true })) { const p = d + '/' + e.name; if (e.isDirectory()) walk(p); else if (/\.m?js$/.test(e.name) && /loadPyodide\(/.test(read(p)) && p !== 'js/screens/drill-worker.js') others.push(p); } })('js');
check('no other file loads Pyodide', others.length === 0, others.join(', '));
const wsrc = read('js/screens/drill-worker.js');
check('the worker makes lru_cache pure Python, sets a recursion limit and survives a stack overflow', /_lru_cache_wrapper = _pure_lru\(\)/.test(wsrc) && /RECURSION_LIMIT = \d+/.test(wsrc) && /isStackOverflow/.test(wsrc));

if (argv.includes('--no-browser')) { console.log('note: --no-browser, the played checks are skipped'); }
else {
  const loadPlaywright = async () => {
    try { return await import('playwright'); } catch { /* not resolvable from here */ }
    const roots = [];
    try { roots.push(execSync('npm root -g', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()); } catch { /* no npm */ }
    (process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).forEach(p => roots.push(p));
    for (const r of roots) { const f = path.join(r, 'playwright', 'index.mjs'); if (fs.existsSync(f)) return import(pathToFileURL(f).href); }
    throw new Error('Playwright is not installed');
  };
  const freePort = () => new Promise((res, rej) => { const s = net.createServer(); s.unref(); s.on('error', rej); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); });
  const MIME = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.wasm': 'application/wasm', '.zip': 'application/zip', '.whl': 'application/zip', '.css': 'text/css' };
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-drill-recursion-'));
  const copy = path.join(tmp, 'app');
  fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
  const fx = JSON.parse(fs.readFileSync(path.join(HERE, 'fixtures/drill-recursion/drill-ab-recursion.json'), 'utf8'));
  fs.writeFileSync(path.join(copy, 'content/drills', fx.id + '.json'), JSON.stringify(fx, null, 2));
  const idxFile = path.join(copy, 'content/drills/index.json');
  const idx = JSON.parse(fs.readFileSync(idxFile, 'utf8')); idx.push({ id: fx.id, name: fx.name, course: fx.course, difficulty: fx.difficulty }); fs.writeFileSync(idxFile, JSON.stringify(idx, null, 2));
  const vout = spawnSync('node', [path.join(copy, 'tools/validate.mjs')], { cwd: copy, encoding: 'utf8' });
  check('the fixture drill validates (0 errors)', /\b0 errors\b/.test(vout.stdout + vout.stderr), (vout.stdout + vout.stderr).split('\n').filter(l => /^error/.test(l)).slice(0, 3).join(' | '));
  const port = await freePort();
  const srv = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', copy], { stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 1500));
  let browser = null;
  try {
    const { chromium } = await loadPlaywright();
    const CHROMIUM = '/opt/pw-browsers/chromium';
    browser = await chromium.launch({ ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 860 } });
    if (CDN) await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
      const u = new URL(route.request().url()); let m, f = null;
      if ((m = u.pathname.match(/^\/pyodide\/v([\d.]+)\/full\/(.*)$/))) f = path.join(CDN, `pyodide-${m[1]}`, 'package', m[2]);
      if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
      return route.fulfill({ status: 404, body: '' });
    });
    const page = await ctx.newPage();
    await page.goto(`http://127.0.0.1:${port}/#setup`);
    await page.waitForFunction(() => window.ZQ && ZQ.content && ZQ.content.ready && ZQ.state, null, { timeout: 30000 });
    await page.evaluate(() => ZQ.content.ready.then(() => { localStorage.clear(); sessionStorage.clear(); ZQ.state.reset(); }));
    await page.reload();
    await page.waitForSelector('[data-name]', { timeout: 30000 });
    await page.fill('[data-name]', 'Recursion');
    await page.click('[data-next]');
    await page.click('[data-track="Trader"]');
    await page.click('[data-next]');
    await page.click('[data-h="15"]');
    await page.click('[data-stage="1"]');
    await page.click('[data-next]');
    await page.waitForFunction(() => window.ZQ && ZQ.state && ZQ.state.flags.setupDone === true, null, { timeout: 30000 });

    /* ---------- 2. the worker ---------- */
    const t = (args, expected) => ({ args, expected });
    const spec = (tests) => ({ fn: 'f', compare: 'equal', prelude: '', tests });
    const cases = [
      { name: 'lru_cache recursion 800 and 1,400 deep', code: 'from functools import lru_cache\n@lru_cache(None)\ndef f(n):\n    return 0 if n == 0 else 1 + f(n - 1)\n', spec: spec([t('(800,)', '800'), t('(1400,)', '1400'), t('(5,)', '5')]), want: ['ok', 'ok', 'ok'] },
      { name: 'a plain recursion 2,800 deep passes at the default limit', code: 'def f(n):\n    return 0 if n == 0 else 1 + f(n - 1)\n', spec: spec([t('(2800,)', '2800')]), want: ['ok'] },
      { name: 'functools.cache with two arguments, 1,000 deep', code: 'import functools\n@functools.cache\ndef g(i, j):\n    return 0 if i == 0 else 1 + g(i - 1, j)\ndef f(n):\n    return g(n, 1)\n', spec: spec([t('(1000,)', '1000')]), want: ['ok'] },
      { name: 'dict recursion with the limit raised to 100,000 reaches 50,000', code: 'import sys\nsys.setrecursionlimit(100000)\nm = {}\ndef f(n):\n    if n == 0: return 0\n    if n not in m: m[n] = 1 + f(n - 1)\n    return m[n]\n', spec: spec([t('(50000,)', '50000'), t('(5,)', '5')]), want: ['ok', 'ok'] },
      { name: 'a plain recursion past the limit is a RecursionError on that test only', code: 'def f(n):\n    return 0 if n == 0 else 1 + f(n - 1)\n', spec: spec([t('(10,)', '10'), t('(5000,)', '5000'), t('(20,)', '20')]), want: ['ok', 'RecursionError', 'ok'] },
      { name: 'a generator in every call, too deep: that test fails with a message and the rest run', code: 'from functools import lru_cache\n@lru_cache(None)\ndef f(n):\n    return 0 if n == 0 else min(1 + f(n - 1) for _ in range(1))\n', spec: spec([t('(100,)', '100'), t('(2500,)', '2500'), t('(2800,)', '2800'), t('(30,)', '30')]), want: ['ok', 'RecursionError', 'RecursionError', 'ok'] },
      { name: 'recursion at load time is a load error, not a silence', code: 'def g(n):\n    return min(g(n + 1) for _ in range(1))\ng(0)\ndef f(n):\n    return n\n', spec: spec([t('(1,)', '1')]), want: ['load:RecursionError'] },
    ];
    const got = await page.evaluate(async (cases) => {
      const log = [];
      for (const c of cases) {
        const w = new Worker('js/screens/drill-worker.js', { type: 'module' });
        await new Promise((res, rej) => { w.onmessage = (e) => { if (e.data.type === 'ready') res(); if (e.data.type === 'fail') rej(new Error(e.data.message)); }; w.postMessage({ type: 'init', indexURL: null }); });
        const ev = []; let crash = null, done = false;
        await new Promise((res) => {
          const id = Math.random();
          w.onmessage = (e) => { const m = e.data; if (m.id !== id) return; if (m.type === 'event') { const d = JSON.parse(m.data); ev.push(d); if (d.kind === 'done') done = true; } if (m.type === 'crash') crash = m.message; if (m.type === 'end') res(); };
          w.postMessage({ type: 'run', id, code: c.code, spec: c.spec });
        });
        w.terminate();
        log.push({ crash, done, res: ev.filter(d => d.kind === 'test' || d.kind === 'error').map(d => d.kind === 'error' ? 'load:' + String(d.error).trim().split('\n').pop().split(':')[0] : d.ok ? 'ok' : (d.error ? String(d.error).trim().split('\n').pop().split(':')[0] : 'wrong')) });
      }
      return log;
    }, cases);
    cases.forEach((c, i) => {
      const g = got[i], same = JSON.stringify(g.res) === JSON.stringify(c.want);
      check(`worker: ${c.name}`, same && !g.crash && (c.want[0].startsWith('load:') || g.done), `got ${JSON.stringify(g.res)} crash ${g.crash} done ${g.done}, wanted ${JSON.stringify(c.want)}`);
    });

    /* ---------- 3. the drill page ---------- */
    const code = 'from functools import lru_cache\n\n@lru_cache(None)\ndef walk(n, deep):\n    if n == 0:\n        return 0\n    if deep:\n        return min(1 + walk(n - 1, deep) for _ in range(1))\n    return 1 + walk(n - 1, deep)\n\ndef chain(n):\n    return walk(n, n > 2000)\n';
    await page.evaluate(() => { location.hash = '#drill/drill-ab-recursion'; });
    await page.waitForFunction(() => window.ZQDrill && ZQDrill.status() === 'ready', null, { timeout: 120000 });
    await page.evaluate((c) => ZQDrill.setCode(c), code);
    await page.evaluate(() => { window.__zqSub = ZQDrill.submit(); });
    await page.waitForFunction(() => { const r = ZQDrill.results(); return r && r.mode === 'submit' && r.res && r.res.every(x => !['pending', 'running'].includes(x.status)); }, null, { timeout: 180000 });
    await page.evaluate(() => window.__zqSub);
    const pg = await page.evaluate(() => { const r = ZQDrill.results(); return { crash: r.crash, res: r.res.map(x => ({ s: x.status, e: (x.error || '').trim().split('\n').pop().slice(0, 40) })), text: document.body.innerText }; });
    check('page: the deep test is an error naming RecursionError', pg.res[2].s === 'error' && /^RecursionError/.test(pg.res[2].e), JSON.stringify(pg.res));
    check('page: every other test is graded and passes (the ones after the deep one too)', pg.res.every((x, i) => i === 2 || x.s === 'pass'), JSON.stringify(pg.res));
    check('page: the run is not a crash and the page does not say Python stopped', !pg.crash && !/Python stopped/.test(pg.text), `crash ${pg.crash}`);
    await page.waitForFunction(() => ZQDrill.status() === 'ready', null, { timeout: 60000 });
    check('page: Python is ready for the next submit', true);
  } catch (e) { let at = ''; try { at = await browser.contexts()[0].pages()[0].evaluate(() => location.hash + ' :: ' + document.body.innerText.slice(0, 200).replace(/\s+/g, ' ')); } catch { /* gone */ } check('browser run completed', false, String((e && e.stack) || e).split('\n').slice(0, 3).join(' | ') + ' | page: ' + at); }
  finally { if (browser) await browser.close(); srv.kill(); fs.rmSync(tmp, { recursive: true, force: true }); }
}
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
