#!/usr/bin/env node
/* Tests for engine pass V-A (ENGINE-BACKLOG 591 to 599): option shuffle, required items, per-paper tracks, seen draws across exams,
   importHint reading a test's setup, expression forms, the exam Skip marking path (589) and a written part's credit.
     Part 1 (plain node, no browser): the expression `form` checks on real Compute Engine output, and importHint over setup lines.
     Part 2 (Playwright, Chromium): the rest, on synthetic exams served through ZQ.content.exam (nothing under app/content is touched).
   Usage: node tools/test-engine-runtime.mjs [--mobile] [--local-cdn <dir>] [--unit-only]
   Exit 0 when all pass, 1 on a failure, 2 on a setup problem. The Compute Engine comes from the local CDN folder when one is given
   (else the ZQ_LOCAL_CDN variable); without it the expression unit tests are skipped with a note. */
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const CHROMIUM = '/opt/pw-browsers/chromium';
const argv = process.argv.slice(2);
const mobile = argv.includes('--mobile'), unitOnly = argv.includes('--unit-only');
const li = argv.indexOf('--local-cdn');
const localCdn = li >= 0 && argv[li + 1] && !argv[li + 1].startsWith('--') ? path.resolve(argv[li + 1]) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const die = (m) => { console.error('test-engine-runtime: ' + m); process.exit(2); };
const fails = [];
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails.push(name); };

/* ---------- Part 1: unit tests in plain node ---------- */
const loadInto = (win, rel) => vm.runInContext(fs.readFileSync(path.join(APP, rel), 'utf8'), win, { filename: rel });
const unit = async () => {
  const win = { ZQ: { widgets: { register() {}, shuffle: (a) => a } }, console };
  win.window = win; vm.createContext(win);
  loadInto(win, 'js/engine/widgets/expression.js');
  const F = win.ZQ.widgets.exprForms;
  check('expression: exprForms exported', !!F && typeof F.rectangular === 'function' && typeof F.reducible === 'function');
  const ceFile = localCdn ? path.join(localCdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js') : null;
  if (!ceFile || !fs.existsSync(ceFile)) { console.log('note: no local Compute Engine (give --local-cdn <pkgs>); the expression form unit tests are skipped'); }
  else {
    const g = { console, setTimeout, clearTimeout }; g.window = g; g.globalThis = g; vm.createContext(g);
    vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
    const C = g.ComputeEngine.ComputeEngine || g.ComputeEngine, ce = new C();
    const J = (s) => ce.parse(s).json;
    const rect = {
      yes: ['-1+2\\iota', '\\frac{1}{2}+\\frac{\\sqrt{3}}{2}\\iota', '2\\iota', '\\iota', '3-\\iota', '5', '0.5+0.866\\iota', '\\frac{4}{5}+\\frac{7}{5}\\iota', '-\\frac{1}{2}-\\frac{\\sqrt{3}}{2}\\iota', '\\sqrt{2}\\iota', '1+\\sqrt{2}+\\iota'],
      no: ['\\frac{4+7\\iota}{2-3\\iota}', '(1+\\iota)^2', '2(1+\\iota)', '1+2+3\\iota', '\\frac{1+\\iota}{2}', 'e^{\\iota\\pi/3}', '(2+\\iota)(1-\\iota)', '\\frac{1}{1+\\iota}'],
    };
    rect.yes.forEach(s => check(`rectangular accepts ${s}`, F.rectangular(J(s)) === true, JSON.stringify(J(s))));
    rect.no.forEach(s => check(`rectangular rejects ${s}`, F.rectangular(J(s)) === false, JSON.stringify(J(s))));
    const red = { no: ['\\frac{\\sqrt{3}}{2}', '1+\\sqrt{2}', '\\frac{3}{2}', '2\\sqrt{3}', '\\pi/2'], yes: ['2+3', '\\frac{1}{2}+\\frac{1}{3}', '\\frac{4+7\\iota}{2-3\\iota}', '2\\cdot3'] };
    red.no.forEach(s => check(`simplified constant accepts ${s}`, F.reducible(J(s)) === false, JSON.stringify(J(s))));
    red.yes.forEach(s => check(`simplified constant rejects ${s}`, F.reducible(J(s)) === true, JSON.stringify(J(s))));
  }
  /* importHint reads a test's setup (the code widget is loaded with the same stubs) */
  const w2 = { ZQ: { widgets: { register() {} } }, console };
  w2.window = w2; vm.createContext(w2);
  try {
    loadInto(w2, 'js/engine/widgets/code.js');
    const I = w2.ZQ.widgets.codeImports;
    check('code: codeImports exported', !!I);
    if (I) {
      check('importHint: a learner import is hinted', /import numpy/.test(I.importHint('import numpy as np\nx = 1')));
      const h = I.harness([{ call: 'f(1)', expect: '1', setup: 'import pandas as pd\ndf = pd.DataFrame()' }, { call: 'g()', expect: '2' }], 'import numpy as np\ndef f(x): return x');
      check('importHint: a test setup import is hinted (function mode)', /if False:\n\s+import pandas/.test(h), h.slice(0, 120));
      check('importHint: no setup, no hint', !/if False/.test(I.harness([{ call: 'g()', expect: '2' }], 'x = 1')));
    }
  } catch (e) { check('code.js loads for the importHint test', false, String(e && e.message || e)); }
};

/* ---------- Part 2: browser ---------- */
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

/* synthetic exams */
const choiceItem = (id, extra = {}) => ({ id, difficulty: 3, skills: ['t-skill'], title: id, question: `Pick the right one (${id}).`, widget: { kind: 'choice', options: [{ id: 'a', text: 'Alpha', correct: true }, { id: 'b', text: 'Beta', why: 'No.' }, { id: 'c', text: 'Gamma' }, { id: 'd', text: 'Delta' }, { id: 'e', text: 'Epsilon' }, { id: 'f', text: 'Zeta' }] }, feedback: { correct: 'Yes.', generic: 'No.' }, explain: { text: 'Because.' }, ...extra });
const longItem = (id, extra = {}) => ({ id, difficulty: 3, skills: ['t-skill'], title: id, kind: 'longform', prompt: 'Explain it.', model: 'The model.', rubric: [{ points: 4, text: 'First' }, { points: 4, text: 'Second' }, { points: 1, text: 'Third' }, { points: 1, text: 'Fourth' }], ...extra });
const paper = (id, name, items, extra = {}) => ({ kind: 'paper', id, name, minutes: 20, pass: 0.5, items, ...extra });
const DOCS = {
  'mock-test-req': { id: 'mock-test-req', name: 'Required test', style: 'trader', parts: [paper('p', 'Paper', [choiceItem('q1', { required: true }), choiceItem('q2'), choiceItem('q3')])] },
  'mock-test-tracks': { id: 'mock-test-tracks', name: 'Tracks test', style: 'trader', parts: [paper('p1', 'Core paper', [choiceItem('c1'), choiceItem('c2')]), paper('p2', 'Research prompt', [choiceItem('r1'), choiceItem('r2')], { tracks: ['research'] })] },
  'mock-test-skip': { id: 'mock-test-skip', name: 'Skip test', style: 'trader', parts: [paper('p', 'Paper', [choiceItem('s1'), longItem('s2')], { pass: 1 })] },
  'mock-test-parts': { id: 'mock-test-parts', name: 'Parts test', style: 'trader', parts: [paper('p', 'Paper', [{ id: 'm1', difficulty: 3, skills: ['t-skill'], title: 'm1', parts: [{ question: 'Part one.', widget: choiceItem('x').widget }, { question: 'Part two.', widget: { kind: 'longform', prompt: 'Explain it.', model: 'The model.', rubric: longItem('y').rubric } }] }], { pass: 0.5 })] },
};

const main = async () => {
  await unit();
  if (unitOnly) { console.log(fails.length ? `${fails.length} failed` : 'all passed'); process.exit(fails.length ? 1 : 0); }
  const { chromium } = await loadPlaywright();
  const port = await freePort();
  const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', APP], { stdio: 'ignore' });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i++) { try { if ((await fetch(base + '/index.html')).ok) break; } catch { /* not up */ } await new Promise(r => setTimeout(r, 100)); }
  const browser = await chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
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
    const errors = [];
    page.on('pageerror', e => errors.push(String(e))); page.on('console', m => { if (m.type() === 'error') console.log('console:', m.text().slice(0, 300)); });
    await page.goto(base + '/#today');
    await page.waitForFunction(() => window.ZQ && ZQ.state && ZQ.prereq && ZQ.content && ZQ.player && ZQ.mock, null, { timeout: 30000 });
    await page.waitForTimeout(500);
    await page.evaluate((docs) => {
      const d = JSON.parse(ZQ.state.export()); d.flags.setupDone = true; ZQ.state.import(d);
      ZQ.state.profile.set({ track: 'Trader' });
      const orig = ZQ.content.exam; window.__docs = docs;
      ZQ.content.exam = (id) => (docs[id] ? Promise.resolve(JSON.parse(JSON.stringify(docs[id]))) : orig(id));
    }, DOCS);
    const go = async (h) => { await page.evaluate((x) => { delete window.ZQ.test; location.hash = x; }, h); await page.waitForTimeout(500); await page.waitForFunction(() => window.ZQ.test && ZQ.test.current().kind !== 'loading', null, { timeout: 20000 }).catch(async (e) => { throw new Error(`${e.message.split('\n')[0]} at ${await page.evaluate(() => location.hash + ' | ' + document.body.innerText.slice(0, 200).replace(/\s+/g, ' '))}`); }); };
    const cur = () => page.evaluate(() => ZQ.test.current());
    /* sit an exam: per item a plan function name decides the answer: 'right' (the hook), 'wrong' (a wrong option by id), 'write' (type text). Returns the final info. */
    const sit = async (route, plan = {}, onMark = null) => {
      await page.evaluate(() => { location.hash = '#review'; }); await page.waitForTimeout(300);
      await go(route);
      let guard = 0;
      while (++guard < 60) {
        const c = await cur();
        if (c.kind === 'done') return c;
        if (c.kind === 'start') { await page.evaluate(() => ZQ.test.continue()); await page.waitForTimeout(150); continue; }
        if (c.kind === 'mark') { if (onMark) await onMark(); else await page.evaluate(() => ZQ.test.continue()); await page.waitForTimeout(300); continue; }
        if (c.kind === 'item') {
          const how = plan[`${c.paper}.${c.screenIndex}`] || 'right';
          if (how === 'wrong') await page.evaluate(() => { const c = ZQ.test.current(), h = ZQExam.handles()[c.screenIndex]; h.widget.set(h.widget.spec.options.find(o => !o.correct).id); });
          else await page.evaluate(() => ZQ.test.answerCorrect());
          await page.waitForTimeout(80);
          await page.evaluate(() => ZQ.test.continue());
          await page.waitForTimeout(200);
          continue;
        }
        await page.waitForTimeout(100);
      }
      throw new Error('the exam did not finish');
    };
    const text = () => page.evaluate(() => (document.querySelector('.exm-res') || document.body).innerText.replace(/\s+/g, ' '));

    /* 1. shuffle by default, stable within an attempt, new for another, off with shuffle: false; grading by id */
    const orders = await page.evaluate(() => {
      const spec = (extra) => ({ id: 'shuf', difficulty: 3, question: 'Q', widget: { kind: 'choice', ...extra, options: ['a', 'b', 'c', 'd', 'e', 'f'].map((id, i) => ({ id, text: id.toUpperCase(), correct: i === 0 })) }, feedback: { correct: '', generic: '' }, explain: { text: 'x' } });
      const mount = (s, key) => { const host = document.createElement('div'); document.body.append(host); const h = ZQ.player.renderItem(JSON.parse(JSON.stringify(s)), host, { mode: 'set', key }); const ids = [...host.querySelectorAll('.opt')].map(b => b.dataset.id); return { ids, h, host }; };
      ZQ.attempt = 111;
      const a1 = mount(spec({}), 'k'), a2 = mount(spec({}), 'k');
      const multi = (() => { const s = spec({}); s.widget.kind = 'multi'; return s; })();
      const m1 = mount(multi, 'k'), m2 = mount(multi, 'k');
      const others = []; for (let n = 2; n < 8; n++) { ZQ.attempt = 111 * n; others.push(mount(spec({}), 'k').ids.join('')); }
      ZQ.attempt = 111;
      const off = mount(spec({ shuffle: false }), 'k');
      const pick = mount(spec({}), 'k'); pick.h.widget.set('a'); const right = pick.h.widget.grade();
      const pickWrong = mount(spec({}), 'k'); pickWrong.h.widget.set('b'); const wrong = pickWrong.h.widget.grade();
      document.querySelectorAll('body > div:not(#app):not(.proto)').forEach(n => { if (n.querySelector('.opt')) n.remove(); });
      return { a1: a1.ids.join(''), a2: a2.ids.join(''), m1: m1.ids.join(''), m2: m2.ids.join(''), others, off: off.ids.join(''), right: right.ok, wrong: wrong.ok, wrongKey: wrong.key };
    });
    check('shuffle: the default order is stable within an attempt', orders.a1 === orders.a2, `${orders.a1} ${orders.a2}`);
    check('shuffle: multi is stable within an attempt too', orders.m1 === orders.m2, `${orders.m1} ${orders.m2}`);
    check('shuffle: the default reorders the options', orders.a1 !== 'abcdef' || orders.others.some(o => o !== 'abcdef'), orders.a1);
    check('shuffle: another attempt gives another order', orders.others.some(o => o !== orders.a1), JSON.stringify(orders.others));
    check('shuffle: shuffle false keeps the authored order', orders.off === 'abcdef', orders.off);
    check('shuffle: grading follows the option id, not its place', orders.right === true && orders.wrong === false && orders.wrongKey === 'b', JSON.stringify(orders));

    /* 2. required */
    const reqStart = async () => { await page.evaluate(() => { location.hash = '#review'; }); await page.waitForTimeout(300); await go('exam/mock-test-req'); return text(); };
    const startText = await reqStart();
    check('required: the start card says which question must be right', /Must be right to pass/.test(startText) && /question 1/.test(startText), startText.slice(0, 300));
    const rWrong = await sit('exam/mock-test-req', { '0.0': 'wrong' });
    check('required: a wrong required item fails the paper though the share is met (2 of 3 at 50%)', rWrong.passed === false && rWrong.score === 2, JSON.stringify(rWrong));
    check('required: the result page says why', /required item was wrong/i.test(await text()), (await text()).slice(0, 400));
    const rRight = await sit('exam/mock-test-req', { '0.1': 'wrong', '0.2': 'wrong' });
    check('required: the required item right and the share missed (1 of 3) still fails by share', rRight.passed === false, JSON.stringify(rRight));
    const rBoth = await sit('exam/mock-test-req', { '0.1': 'wrong' });
    check('required: the required item right and the share met passes', rBoth.passed === true, JSON.stringify(rBoth));
    const tag = await (async () => { await page.evaluate(() => { location.hash = '#review'; }); await page.waitForTimeout(300); await go('exam/mock-test-req'); await page.evaluate(() => ZQ.test.continue()); await page.waitForTimeout(200); return page.evaluate(() => [...document.querySelectorAll('[data-required]')].length); })();
    check('required: the required question carries the tag on the paper', tag === 1, String(tag));

    /* 3. tracks */
    const trackStart = async (route) => { await page.evaluate(() => { location.hash = '#review'; }); await page.waitForTimeout(300); await go(route); return text(); };
    let t = await trackStart('exam/mock-test-tracks');
    check('tracks: an off-track paper is named as left out on the start card', /Left out for your track: Research prompt \(research\)/.test(t), t.slice(0, 300));
    check('tracks: the start card links to sit it too', await page.evaluate(() => !!document.querySelector('.exm-tracks a[href="#exam/mock-test-tracks/all"]')));
    let fin = await sit('exam/mock-test-tracks');
    check('tracks: an off-track learner sits one paper (4 items become 2)', fin.total === 2 && fin.passed === true, JSON.stringify(fin));
    fin = await sit('exam/mock-test-tracks/all', { '1.0': 'wrong', '1.1': 'wrong' });
    check('tracks: with "all" the off-track paper is optional and never gates', fin.total === 4 && fin.passed === true, JSON.stringify(fin));
    check('tracks: the result row says optional', /Optional for your track, not counted/.test(await text()), (await text()).slice(0, 300));
    fin = await sit('exam/mock-test-tracks/as-research', { '1.0': 'wrong', '1.1': 'wrong' });
    check('tracks: as a research learner the paper counts and gates', fin.total === 4 && fin.passed === false, JSON.stringify(fin));
    fin = await sit('exam/mock-test-tracks/as-research');
    check('tracks: as a research learner, all right passes', fin.passed === true, JSON.stringify(fin));
    await page.evaluate(() => ZQ.state.profile.set({ track: 'Researcher' }));
    t = await trackStart('exam/mock-test-tracks');
    check('tracks: a Researcher profile sits both papers with no left-out line', !/Left out for your track/.test(t));
    await page.evaluate(() => ZQ.state.profile.set({ track: 'Trader' }));

    /* 4. the 589 Skip marking path: Skip scores the written item 0 and the row says so */
    const skipped = await sit('exam/mock-test-skip', {}, async () => {
      await page.waitForSelector('.exm-skipmark', { timeout: 10000 });
      if (process.env.ZQ_DEBUG) console.log(await page.evaluate(() => JSON.stringify([...document.querySelectorAll('.exm-q')].map(q => [q.dataset.qI, q.hidden, getComputedStyle(q).display, q.getBoundingClientRect().height]))));
      await page.locator('.exm-skipmark').click({ timeout: 5000 });
    });
    const sk = await text();
    check('skip marking: the paper fails (the written item scores 0, pass 100%)', skipped.passed === false && skipped.score === 1, JSON.stringify(skipped));
    check('skip marking: the result row says "Marking skipped"', /Marking skipped/.test(sk), sk.slice(0, 400));
    check('skip marking: the line says it scores 0', /skipped marking this written answer, so it scores 0/.test(await page.evaluate(() => document.body.innerHTML.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' '))));
    const marked = await sit('exam/mock-test-skip', {}, async () => {
      await page.waitForSelector('.exm-donemark', { timeout: 10000 });
      const rows = page.locator('.exm-q:not([hidden]) .wd-rb'); const n = await rows.count();
      for (let k = 0; k < n; k++) await rows.nth(k).click();
      await page.locator('.exm-donemark').click();
    });
    check('skip marking: Finish marking with every point ticked passes', marked.passed === true && marked.score === 2, JSON.stringify(marked));

    /* 5. a written part inside parts scores ticks over points */
    const partsRun = async (ticks) => sit('exam/mock-test-parts', {}, async () => {
      await page.waitForSelector('.exm-donemark', { timeout: 10000 });
      const rows = page.locator('.exm-q:not([hidden]) .wd-rb');
      for (let k = 0; k < ticks; k++) await rows.nth(k).click();
      await page.locator('.exm-donemark').click();
    });
    let pr = await partsRun(2);   // 8 of 10 points
    check('parts: a written part marked 8 of 10 earns 0.8, so the item is worth 0.9', Math.abs(pr.net - 0.9) < 1e-6, JSON.stringify(pr));
    pr = await partsRun(1);       // 4 of 10 points
    check('parts: a written part marked 4 of 10 earns 0.4, so the item is worth 0.7', Math.abs(pr.net - 0.7) < 1e-6, JSON.stringify(pr));

    /* 6. draws seen in another exam count as seen */
    const seen = await page.evaluate(() => {
      ZQ.state.examFinished({ id: 'topic-other-seen', score: 1, items: 1, passed: true, bySkill: {}, seconds: 1, results: [], extra: { drawn: ['bank/test-file/item-1'] } });
      const own = ZQ.mock.seenInfo('mock-test-req'), self = ZQ.mock.seenInfo('topic-other-seen');
      return { own: own['bank/test-file/item-1'] || null, self: self['bank/test-file/item-1'] || null, seen: ZQ.mock.seenOf('mock-test-req')['bank/test-file/item-1'] || 0, label: ZQ.mock.seenLabel(own['bank/test-file/item-1']) };
    });
    check('seen: a draw sat in another exam counts as seen', seen.own && seen.own.why === 'other' && seen.seen > 0, JSON.stringify(seen));
    check('seen: in its own exam it is a sitting', seen.self && seen.self.why === 'sat', JSON.stringify(seen));
    check('seen: the label names another exam', /another exam/.test(seen.label), seen.label);
    check('no page errors', errors.length === 0, errors.slice(0, 2).join(' | '));
  } catch (e) {
    check('no exception', false, String(e && e.stack || e).split('\n').slice(0, 12).join(' | '));
  }
  await browser.close();
  proc.kill();
  console.log(fails.length ? `${fails.length} failed` : 'all passed');
  process.exit(fails.length ? 1 : 0);
};
main().catch(e => { console.error(e); process.exit(2); });
