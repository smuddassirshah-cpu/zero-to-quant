#!/usr/bin/env node
/* DOM test of the "Check first" card (ENGINE-BACKLOG 552, 572). A diagnostic requires edge ("gate": false) must show as
   "Check first: <name>", its why line and a link to that level's review, and must never lock.
   The edge is read from every course.json (the first level with a diagnostic whose review is written), so it follows the content.
   Checks, on a profile where the gating prerequisites of the level are met and the diagnostic is not:
     1. the lesson opens (not locked, no lock card) and its start shows .lk-check with the name, the why and the review link;
     2. the Learn node card (course map) shows the same, and the node is not drawn as locked;
     3. on a fresh profile (a gating prerequisite unmet) the lesson is locked by the gating edge only: the diagnostic is not among the
        missing prerequisites, and the lock card does not list it as one to finish.
   Usage: node tools/test-check-first.mjs [--mobile] [--local-cdn <dir>]   Exit 0 when all pass, 1 on a failure, 2 on a setup problem. */
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const CONTENT = path.join(APP, 'content');
const CHROMIUM = '/opt/pw-browsers/chromium';
const argv = process.argv.slice(2);
const mobile = argv.includes('--mobile');
const li = argv.indexOf('--local-cdn');
const localCdn = li >= 0 && argv[li + 1] && !argv[li + 1].startsWith('--') ? path.resolve(argv[li + 1]) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const die = (m) => { console.error('test-check-first: ' + m); process.exit(2); };
const readJSON = (f) => JSON.parse(fs.readFileSync(f, 'utf8'));

/* a real diagnostic edge: { course, n, lessonId, lessonName?, ref, why, gating: [refs] } */
const pickEdge = () => {
  const cur = readJSON(path.join(CONTENT, 'curriculum.json'));
  const order = cur.stages.flatMap(s => s.topics.flatMap(t => t.courses || []));
  for (const c of order) {
    const cf = path.join(CONTENT, 'courses', c, 'course.json');
    if (!fs.existsSync(cf)) continue;
    for (const lv of readJSON(cf).levels || []) {
      const reqs = lv.requires || [];
      const diag = reqs.find(r => r && typeof r === 'object' && r.gate === false && r.why && /^[a-z0-9-]+\/L\d+$/.test(r.ref));
      const lesson = (lv.lessons || []).find(l => fs.existsSync(path.join(CONTENT, 'courses', c, l + '.json')));
      if (!diag || !lesson) continue;
      const [dc, dn] = [diag.ref.split('/')[0], +diag.ref.split('/')[1].slice(1)];
      const df = path.join(CONTENT, 'courses', dc, 'course.json');
      if (!fs.existsSync(df)) continue;
      const dlv = (readJSON(df).levels || []).find(l => l.n === dn);
      if (!dlv || !dlv.review || !fs.existsSync(path.join(CONTENT, 'courses', dc, dlv.review + '.json'))) continue;
      const gating = reqs.filter(r => typeof r === 'string' || (r && r.gate !== false)).map(r => typeof r === 'string' ? r : r.ref).filter(r => /^[a-z0-9-]+\/L\d+$/.test(r));
      return { course: c, n: lv.n, lesson, ref: diag.ref, why: diag.why, review: `review/${dc}/${dlv.review}`, gating, dcourse: dc, dn };
    }
  }
  return null;
};

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
  const edge = pickEdge();
  if (!edge) die('no gate:false diagnostic edge with a written review found in any course.json');
  const { chromium } = await loadPlaywright();
  const port = await freePort();
  const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', APP], { stdio: 'ignore' });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i++) { try { if ((await fetch(base + '/index.html')).ok) break; } catch { /* not up */ } await new Promise(r => setTimeout(r, 100)); }
  const browser = await chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
  const fails = [];
  const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails.push(name); };
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
    await page.goto(base + '/#today');
    await page.waitForFunction(() => window.ZQ && ZQ.state && ZQ.prereq && ZQ.content, null, { timeout: 30000 });
    await page.waitForTimeout(500);
    /* a profile with setup done, strict prerequisites, and the given levels met (a review pass is the usual way; the record is the same) */
    const profile = (met) => page.evaluate((m) => {
      const d = JSON.parse(ZQ.state.export());
      d.lessons = {}; d.reviews = {}; d.homework = {}; d.exams = {}; d.redo = [];
      d.prereq = { met: Object.fromEntries(m.map(k => [k, { how: 'auto', at: Date.now() }])), testouts: {}, opened: {}, grandfathered: false };
      d.settings.strictPrereqs = true; d.flags.setupDone = true;
      const r = ZQ.state.import(d);
      return !!(r && r.ok);
    }, met);
    const go = async (h) => { await page.evaluate((x) => { delete window.ZQ.test; location.hash = x; }, h); await page.waitForTimeout(700); };
    const name = await page.evaluate((e) => { const n = ZQ.prereq.diagnosticsForLevel(e.course, e.n); return n.map(x => x.ref + '|' + (x.courseName || '') + '|' + (x.n || '')); }, edge);
    console.log(`edge: ${edge.course} level ${edge.n} (${edge.lesson}) has diagnostic ${edge.ref}; ${mobile ? 'mobile 440' : 'desktop 1280'}`);

    /* 1 and 2: gating prerequisites met, diagnostic not */
    check('profile with the gating prerequisites met imports', await profile(edge.gating));
    const st = await page.evaluate((e) => ({ lessonLocked: ZQ.prereq.lessonLocked(e.course, e.lesson), levelLocked: ZQ.prereq.levelLocked(e.course, e.n), diagMet: ZQ.prereq.refMet(e.ref), diag: ZQ.prereq.diagnosticsFor(e.course, e.lesson).map(x => x.ref) }), edge);
    check('the diagnostic is unmet (precondition)', st.diagMet === false && st.diag.includes(edge.ref), JSON.stringify(st));
    check('the level and lesson are not locked by the diagnostic', st.lessonLocked === false && st.levelLocked === false, JSON.stringify(st));
    check('diagnosticsFor names the review route', await page.evaluate((e) => ZQ.prereq.diagnosticsFor(e.course, e.lesson).some(x => x.ref === e.ref && x.route === e.review), edge), name.join(','));

    await go(`lesson/${edge.course}/${edge.lesson}`);
    const ls = await page.evaluate((e) => {
      const el = document.querySelector(`.lsn-notes .lk-check[data-ref="${e.ref}"]`);
      return { lesson: !!document.querySelector('.lsn'), lockCard: !!document.querySelector('.lk'), text: el ? el.textContent.replace(/\s+/g, ' ').trim() : null, href: el && el.querySelector('a') ? el.querySelector('a').getAttribute('href') : null, wide: document.documentElement.scrollWidth > window.innerWidth + 1 };
    }, edge);
    check('lesson start opens (no lock card)', ls.lesson && !ls.lockCard, JSON.stringify(ls));
    check('lesson start: text begins "Check first:"', !!ls.text && /^Check first: /.test(ls.text), String(ls.text));
    check('lesson start: names the level', !!ls.text && new RegExp(`level ${edge.dn}\\b`).test(ls.text), String(ls.text));
    check('lesson start: carries the why line', !!ls.text && ls.text.includes(edge.why.replace(/\s+/g, ' ').trim()), String(ls.text));
    check('lesson start: links to that level\'s review', ls.href === '#' + edge.review, String(ls.href));
    check('lesson start: no sideways scroll', !ls.wide);

    await go(`course/${edge.course}`);
    const node = `.zc-node[data-id="${edge.lesson}"]`;
    await page.waitForSelector(node, { timeout: 10000 });
    const cls = await page.evaluate((s) => document.querySelector(s).className, node);
    check('Learn node is not drawn as locked', !/\bs-locked\b/.test(cls), cls);
    await page.evaluate((s) => document.querySelector(s).scrollIntoView({ block: 'center' }), node);
    await page.click(`${node} .zc-pw, ${node}`, { timeout: 5000 }).catch(async () => { await page.evaluate((s) => document.querySelector(s).click(), node); });
    await page.waitForTimeout(600);
    const card = await page.evaluate((e) => {
      const el = document.querySelector(`.zc-pop:not([hidden]) .lk-check[data-ref="${e.ref}"], .sheet .lk-check[data-ref="${e.ref}"], .zc-sheet .lk-check[data-ref="${e.ref}"]`);
      return { text: el ? el.textContent.replace(/\s+/g, ' ').trim() : null, href: el && el.querySelector('a') ? el.querySelector('a').getAttribute('href') : null };
    }, edge);
    check('Learn node card: "Check first:" text', !!card.text && /^Check first: /.test(card.text), String(card.text));
    check('Learn node card: carries the why line', !!card.text && card.text.includes(edge.why.replace(/\s+/g, ' ').trim()), String(card.text));
    check('Learn node card: links to that level\'s review', card.href === '#' + edge.review, String(card.href));

    /* 3: a gating prerequisite unmet: locked by it alone */
    check('fresh profile imports', await profile([]));
    await go(`lesson/${edge.course}/${edge.lesson}`);
    const lk = await page.evaluate((e) => {
      const m = ZQ.prereq.missingFor(e.course, e.lesson), rows = [...document.querySelectorAll('.lk-row')].map(r => r.dataset.ref);
      return { locked: ZQ.prereq.lessonLocked(e.course, e.lesson), card: !!document.querySelector('.lk'), missing: m.direct.concat(m.indirect).map(n => n.ref), rows };
    }, edge);
    check('with a gating prerequisite unmet the lesson is locked (lock card)', lk.locked && lk.card, JSON.stringify(lk));
    check('the diagnostic is not listed among the prerequisites to finish', !lk.missing.includes(edge.ref) && !lk.rows.includes(edge.ref), JSON.stringify(lk));
  } catch (e) {
    check('no exception', false, String(e && e.stack || e).split('\n').slice(0, 3).join(' | '));
  }
  await browser.close();
  proc.kill();
  console.log(fails.length ? `${fails.length} failed` : 'all passed');
  process.exit(fails.length ? 1 : 0);
};
main().catch(e => { console.error(e); process.exit(2); });
