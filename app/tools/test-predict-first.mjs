#!/usr/bin/env node
/* DOM test of canvas.controlsAfter (ENGINE-BACKLOG 1211) and the quiz redo line (1212), on the fixture lesson
   tools/fixtures/predict-first/l1-gate.json (served under the fake course zq-fixture; never real content).
     1. controlsAfter "correct": the bars sim chips are disabled (disabled and aria-disabled) with the note "Answer first, then run it."
        before the check and after a wrong check; after the correct check they are enabled, the note is gone and Run works;
     2. controlsAfter "check": a wrong check already opens them;
     3. (l2-correct-patch, ENGINE-BACKLOG 1213) an option's canvas patch shows after a wrong pick, is undone by Try again, shows after the correct
        pick and stays on the solved screen, and does not show before the check;
     4. a wrong quiz answer shows "Added to your Redo queue." in its chip, and finishing the quiz does queue the item.
   Usage: node tools/test-predict-first.mjs [--mobile] [--local-cdn <dir>]   Exit 0 when all pass, 1 on a failure, 2 on a setup problem. */
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const FIXTURE = path.join(HERE, 'fixtures', 'predict-first', 'l1-gate.json');
const FIXTURE2 = path.join(HERE, 'fixtures', 'predict-first', 'l2-correct-patch.json');
const argv = process.argv.slice(2);
const mobile = argv.includes('--mobile');
const li = argv.indexOf('--local-cdn');
const localCdn = li >= 0 && argv[li + 1] && !argv[li + 1].startsWith('--') ? path.resolve(argv[li + 1]) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const die = (m) => { console.error('test-predict-first: ' + m); process.exit(2); };

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
  try {
    const ctx = await browser.newContext({ viewport: mobile ? { width: 440, height: 956 } : { width: 1280, height: 860 } });
    await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
      const f = cdnFile(new URL(route.request().url()));
      if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
      return route.abort('blockedbyclient');
    });
    await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
    await ctx.route(/\/content\/courses\/zq-fixture\/l1-gate\.json$/, r => r.fulfill({ status: 200, body: fs.readFileSync(FIXTURE), headers: { 'content-type': 'application/json' } }));
    await ctx.route(/\/content\/courses\/zq-fixture\/l2-correct-patch\.json$/, r => r.fulfill({ status: 200, body: fs.readFileSync(FIXTURE2), headers: { 'content-type': 'application/json' } }));
    const page = await ctx.newPage();
    await page.goto(base + '/#today');
    await page.waitForFunction(() => window.ZQ && ZQ.state && ZQ.content, null, { timeout: 30000 });
    await page.evaluate(() => { ZQ.state.reset(); ZQ.state.flags.set({ setupDone: true }); ZQ.state.profile.set({ name: 'Test' }); ZQ.state.settings.set({ strictPrereqs: false }); });
    await page.evaluate(() => { location.hash = 'lesson/zq-fixture/l1-gate'; });
    await page.waitForFunction(() => window.ZQ.test && ZQ.test.current().kind === 'problem', null, { timeout: 20000 });
    await page.waitForTimeout(600);
    const chips = () => page.evaluate(() => {
      const bs = [...document.querySelectorAll('.cvb-extra .cvb-chip')];
      const note = document.querySelector('.lsn-gate-note');
      return { n: bs.length, disabled: bs.filter(b => b.disabled).length, aria: bs.filter(b => b.getAttribute('aria-disabled') === 'true').length, note: note ? note.textContent.trim() : null, count: (document.querySelector('.cvb-count') || {}).textContent || '' };
    });
    const t = (fn) => page.evaluate(async (f) => { const h = ZQ.test; return await (new Function('h', 'return (async () => {' + f + '})()'))(h); }, fn);

    /* 1: "correct" */
    let c = await chips();
    check('correct: Run and Reset chips are drawn', c.n === 3, JSON.stringify(c));
    check('correct: all chips disabled with aria-disabled before the check', c.disabled === c.n && c.aria === c.n, JSON.stringify(c));
    check('correct: the note reads "Answer first, then run it."', c.note === 'Answer first, then run it.', JSON.stringify(c));
    await t('h.answerWrong(); await h.check();');
    await page.waitForTimeout(500);
    c = await chips();
    check('correct: still held after a wrong check', c.disabled === c.n && c.note, JSON.stringify(c));
    await t('await h.tryAgain(); h.answerCorrect(); await h.check();');
    await page.waitForTimeout(500);
    c = await chips();
    check('correct: enabled and the note gone after the correct check', c.disabled === 0 && c.aria === 0 && c.note === null, JSON.stringify(c));
    await page.click('.cvb-extra .cvb-chip:first-child');
    await page.waitForTimeout(700);
    c = await chips();
    check('correct: Run 10 works after the check', /10 trials/.test(c.count), JSON.stringify(c));
    await t('await h.continue();');
    await page.waitForTimeout(500);

    /* 2: "check" */
    c = await chips();
    check('check: held on the next screen', c.n >= 2 && c.disabled === c.n && c.note, JSON.stringify(c));
    await t('h.answerWrong(); await h.check();');
    await page.waitForTimeout(500);
    c = await chips();
    check('check: a wrong check opens the controls', c.disabled === 0 && c.aria === 0 && c.note === null, JSON.stringify(c));

    /* 3: correct-option canvas patch (1213) */
    await page.evaluate(() => { location.hash = 'lesson/zq-fixture/l2-correct-patch'; });
    await page.waitForFunction(() => window.ZQ.test && ZQ.test.current().lesson === 'zq-fixture/l2-correct-patch' && ZQ.test.current().kind === 'problem', null, { timeout: 20000 });
    await page.waitForTimeout(600);
    const cvText = () => page.evaluate(() => (document.querySelector('.lsn-canvas') || {}).textContent || '');
    const has = async (v) => (await cvText()).includes(v);
    check('patch: neither value shows before the check', !(await has('77.7')) && !(await has('55.5')), await cvText());
    await page.click('.wd-opt[data-id="right"]');
    await page.waitForTimeout(300);
    check('patch: picking does not apply the patch before the check', !(await has('77.7')), await cvText());
    await page.click('.wd-opt[data-id="slip"]');
    await t('await h.check();');
    await page.waitForTimeout(600);
    check('patch: a wrong pick applies its own patch', await has('55.5'), await cvText());
    await t('await h.tryAgain();');
    await page.waitForTimeout(500);
    check('patch: Try again undoes it', !(await has('55.5')), await cvText());
    await page.click('.wd-opt[data-id="right"]');
    await t('await h.check();');
    await page.waitForTimeout(900);
    check('patch: the correct pick applies the correct option patch', await has('77.7'), await cvText());
    await page.waitForTimeout(1200);
    check('patch: it stays on the solved screen', await has('77.7'), await cvText());

    /* 4: the quiz line */
    await page.evaluate(() => { location.hash = 'lesson/zq-fixture/l1-gate'; });
    await page.waitForFunction(() => window.ZQ.test && ZQ.test.current().lesson === 'zq-fixture/l1-gate', null, { timeout: 20000 });
    await page.waitForTimeout(600);
    await t('await h.goto("quiz");');
    await page.waitForTimeout(500);
    await t('h.answerWrong(); await h.check();');
    await page.waitForTimeout(600);
    const chipText = await page.evaluate(() => (document.querySelector('.lsn-chip.is-no') || {}).textContent || '');
    check('quiz: a wrong answer shows "Added to your Redo queue."', /Added to your Redo queue\./.test(chipText), chipText);
    await t('await h.continue();');
    await page.waitForTimeout(800);
    const queued = await page.evaluate(() => JSON.parse(ZQ.state.export()).redo.filter(r => r.kind === 'quiz' && r.ref && r.ref.item === 'q-one').length);
    check('quiz: finishing the quiz does queue the wrong item', queued === 1, String(queued));
  } finally {
    await browser.close();
    proc.kill();
  }
  if (fails.length) { console.error(`test-predict-first: ${fails.length} failed`); process.exit(1); }
  console.log('test-predict-first: all passed');
};
main().catch((e) => { console.error(e); process.exit(2); });
