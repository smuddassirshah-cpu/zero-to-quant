#!/usr/bin/env node
/* DOM test of the dice-sim canvas (ENGINE-BACKLOG 1217) on the fixture lesson tools/fixtures/dice-sim/l1-dice.json
   (served under the fake course zq-fixture; never real content).
     1. controlsAfter "check": Run and Reset are disabled before the check and open after it (the player's gate covers .cvb-extra);
     2. a run animates and then the counters add up (Rolled = Kept + Filtered out) and the trace's last point sits at Kept / Rolled;
     3. the same seed gives the same sequence (two fresh canvases, one run 10 then 100, one run 110 at once), a different seed another;
     4. Reset returns to no rolls and the next run repeats the first one exactly;
     5. with reduced motion a run shows its final state at once; the live region carries the summary.
   Usage: node tools/test-dice-sim.mjs [--mobile] [--local-cdn <dir>]   Exit 0 when all pass, 1 on a failure, 2 on a setup problem. */
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const FIXTURE = path.join(HERE, 'fixtures', 'dice-sim', 'l1-dice.json');
const argv = process.argv.slice(2);
const mobile = argv.includes('--mobile');
const li = argv.indexOf('--local-cdn');
const localCdn = li >= 0 && argv[li + 1] && !argv[li + 1].startsWith('--') ? path.resolve(argv[li + 1]) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const die = (m) => { console.error('test-dice-sim: ' + m); process.exit(2); };

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
  const browser = await chromium.launch();
  const fails = [];
  const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + String(detail).slice(0, 300)}`); if (!ok) fails.push(name); };
  const open = async (reduced) => {
    const ctx = await browser.newContext({ viewport: mobile ? { width: 440, height: 956 } : { width: 1280, height: 860 }, reducedMotion: reduced ? 'reduce' : 'no-preference' });
    await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
      const f = cdnFile(new URL(route.request().url()));
      if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
      return route.abort('blockedbyclient');
    });
    await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
    await ctx.route(/\/content\/courses\/zq-fixture\/l1-dice\.json$/, r => r.fulfill({ status: 200, body: fs.readFileSync(FIXTURE), headers: { 'content-type': 'application/json' } }));
    const page = await ctx.newPage();
    await page.goto(base + '/#today');
    await page.waitForFunction(() => window.ZQ && ZQ.state && ZQ.content, null, { timeout: 30000 });
    await page.evaluate(() => { ZQ.state.reset(); ZQ.state.flags.set({ setupDone: true }); ZQ.state.profile.set({ name: 'Test' }); ZQ.state.settings.set({ strictPrereqs: false }); });
    await page.evaluate(() => { location.hash = 'lesson/zq-fixture/l1-dice'; });
    await page.waitForFunction(() => window.ZQ.test && ZQ.test.current().kind === 'problem', null, { timeout: 20000 });
    await page.waitForTimeout(600);
    return page;
  };
  const read = (page) => page.evaluate(() => {
    const cv = document.querySelector('.cv-dice-sim');
    const vals = [...cv.querySelectorAll('[data-id="counters"] .cvds-val')].map((n) => +n.textContent.replace(/,/g, '')); // right to left: Filtered out, Kept, Rolled
    const dot = cv.querySelector('.cvds-dot'), grid = [...cv.querySelectorAll('[data-id="trace"] .cvds-grid')].map((n) => +n.getAttribute('y1'));
    const bs = [...document.querySelectorAll('.cvb-extra button')], note = document.querySelector('.lsn-gate-note');
    return { rolled: vals[2], kept: vals[1], out: vals[0], dotY: dot ? +dot.getAttribute('cy') : null, y0: grid[0], yTop: grid[2],
      buttons: bs.length, disabled: bs.filter(b => b.disabled).length, aria: bs.filter(b => b.getAttribute('aria-disabled') === 'true').length, note: note ? note.textContent.trim() : null,
      live: (cv.parentElement.querySelector('[aria-live]') || {}).textContent || '', dice: [...cv.querySelectorAll('.cvds-die')].map(d => d.getAttribute('class')).join('|') };
  });
  const t = (page, fn) => page.evaluate(async (f) => { const h = ZQ.test; return await (new Function('h', 'return (async () => {' + f + '})()'))(h); }, fn);
  try {
    const page = await open(false);
    /* 1: gate */
    let s = await read(page);
    check('gate: Run 10, 100, 1,000 and Reset are drawn', s.buttons === 4, JSON.stringify(s));
    check('gate: all disabled with aria-disabled before the check, with the note', s.disabled === 4 && s.aria === 4 && s.note === 'Answer first, then run it.', JSON.stringify(s));
    check('gate: no rolls yet', s.rolled === 0 && s.dotY === null, JSON.stringify(s));
    await t(page, 'h.answerWrong(); await h.check();');
    await page.waitForTimeout(500);
    s = await read(page);
    check('gate: a wrong check opens the controls (check mode)', s.disabled === 0 && s.aria === 0 && s.note === null, JSON.stringify(s));

    /* 2: run, counters, trace */
    await page.click('.cvb-extra button:nth-child(2)'); // Run 100
    await page.waitForTimeout(1500);
    s = await read(page);
    check('run 100: Rolled is 100', s.rolled === 100, JSON.stringify(s));
    check('counters add up: Rolled = Kept + Filtered out', s.rolled === s.kept + s.out && s.kept > 0, JSON.stringify(s));
    const share = s.kept / s.rolled, expY = s.y0 - (s.y0 - s.yTop) * share / 0.5;
    check('trace: the last point is at Kept / Rolled', Math.abs(s.dotY - expY) < 0.1, `${s.dotY} vs ${expY}`);
    check('live region carries the counters', new RegExp(`^100 rolled, ${s.kept} kept, share ${share.toFixed(3)}\\.`).test(s.live), s.live);
    const first100 = { kept: s.kept, dice: s.dice };
    await page.click('.cvb-extra button:nth-child(1)'); // Run 10
    await page.waitForTimeout(1000);
    s = await read(page);
    check('run 10 adds ten', s.rolled === 110 && s.rolled === s.kept + s.out, JSON.stringify(s));
    await page.click('.cvb-extra button:nth-child(4)'); // Reset
    await page.waitForTimeout(300);
    s = await read(page);
    check('reset: back to no rolls', s.rolled === 0 && s.kept === 0 && s.dotY === null, JSON.stringify(s));
    await page.click('.cvb-extra button:nth-child(2)');
    await page.waitForTimeout(1500);
    s = await read(page);
    check('reset: the next Run 100 repeats the first exactly', s.kept === first100.kept && s.dice === first100.dice, `${s.kept} vs ${first100.kept}`);

    /* 3: determinism by seed, on fresh canvases */
    const seq = await page.evaluate(async () => {
      const mk = (seed) => { const host = document.createElement('div'); document.body.append(host); return ZQ.canvas.create(host, { kind: 'dice-sim', params: { dice: 2, keep: 'd1 == 5 || d2 == 5', seed, exact: '11/36' } }, {}); };
      const a = mk(4226), b = mk(4226), c = mk(9);
      await a.run(10); await a.run(100); b.set({ ran: 110 }, { instant: true }); c.set({ ran: 110 }, { instant: true });
      const out = { a: a.counts(), b: b.counts(), c: c.counts(), la: a.last(), lb: b.last(), lc: c.last(), shareA: a.values().share };
      const big = mk(4226); big.set({ ran: 1000 }, { instant: true }); out.big = big.counts();
      [a, b, c, big].forEach((x) => x.destroy()); document.querySelectorAll('body > div:empty').forEach((n) => n.remove());
      return out;
    });
    check('seed: 10 then 100 equals 110 at once', seq.a.kept === seq.b.kept && JSON.stringify(seq.la) === JSON.stringify(seq.lb), JSON.stringify(seq));
    check('seed: another seed gives another stream', JSON.stringify([seq.c, seq.lc]) !== JSON.stringify([seq.b, seq.lb]), JSON.stringify(seq));
    check('seed 4226: 1,000 rolls keep a count the widget (305, tol 25) accepts', seq.big.rolled === 1000 && Math.abs(seq.big.kept - 305) <= 25, JSON.stringify(seq.big));
    console.log('info seed 4226, 1000 rolls: kept ' + seq.big.kept + '; 110 rolls: kept ' + seq.a.kept + '; seed 9 kept ' + seq.c.kept);

    /* second screen: no widget, so the controls are open from the start */
    await t(page, 'await h.tryAgain(); h.answerCorrect(); await h.check(); await h.continue();');
    await page.waitForTimeout(700);
    s = await page.evaluate(() => { const cv = [...document.querySelectorAll('.cv-dice-sim')].pop(), bs = [...cv.querySelectorAll('.cvb-extra button')]; return { screens: document.querySelectorAll('.cv-dice-sim').length, buttons: bs.length, disabled: bs.filter(b => b.disabled).length, dice: cv.querySelectorAll('.cvds-die').length, high: /High/.test(cv.textContent) }; });
    check('explore screen: three dice, the High label, Run 10 and 100 and Reset open (no controlsAfter)', s.buttons === 3 && s.disabled === 0 && s.dice === 3 && s.high, JSON.stringify(s));
    await page.close();

    /* 5: reduced motion */
    const rm = await open(true);
    await rm.evaluate(() => { const h = ZQ.test; h.answerWrong(); return h.check(); });
    await rm.waitForTimeout(500);
    await rm.click('.cvb-extra button:nth-child(3)'); // Run 1,000
    await rm.waitForTimeout(80);
    s = await read(rm);
    check('reduced motion: Run 1,000 shows the final state at once', s.rolled === 1000 && s.rolled === s.kept + s.out, JSON.stringify(s));
  } finally {
    await browser.close();
    proc.kill();
  }
  if (fails.length) { console.error(`test-dice-sim: ${fails.length} failed`); process.exit(1); }
  console.log('test-dice-sim: all passed');
};
main().catch((e) => { console.error(e); process.exit(2); });
