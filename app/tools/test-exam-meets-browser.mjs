#!/usr/bin/env node
/* DOM test of the exam-pass rule (ENGINE-BACKLOG 1052): the reported case end to end. A stored topic 0.2 exam pass with fn-lines 1 of 2 opens the first
   exp-log lesson that needs functions level 2 (no lesson done, no skill record); with 0 of 2 the lesson stays locked, the locked row says why (names the
   skill and its score in that attempt) and keeps Test out, with no sideways scroll at 440.
   Usage: node tools/test-exam-meets-browser.mjs [--mobile] [--local-cdn <dir>]   Exit 0 when all pass, 1 on a failure, 2 on a setup problem.
   Scaffolding as tools/test-check-first.mjs. */
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
const die = (m) => { console.error('test-exam-meets-browser: ' + m); process.exit(2); };
const readJSON = (f) => JSON.parse(fs.readFileSync(f, 'utf8'));

const EXAM = readJSON(path.join(CONTENT, 'exams', 'topic-0.2.json'));
/* the first exp-log lesson whose level or lesson requires functions/L2, and its other requirements */
const pickLesson = () => {
  const co = readJSON(path.join(CONTENT, 'courses', 'exp-log', 'course.json'));
  const refsOf = (l) => (l || []).map(r => typeof r === 'string' ? r : r.ref);
  for (const lv of co.levels) for (const id of lv.lessons || []) {
    if (!fs.existsSync(path.join(CONTENT, 'courses', 'exp-log', id + '.json'))) continue;
    const refs = refsOf((co.lessonRequires || {})[id] || lv.requires);
    if (refs.includes('functions/L2')) return { id, n: lv.n, others: refs.filter(r => r !== 'functions/L2') };
  }
  return null;
};
/* the attempt of a full pass with `missed` of the fn-lines items wrong */
const attemptWith = (missed) => {
  const by = {}; let left = missed, right = 0;
  EXAM.items.forEach(it => (it.skills || []).forEach(s => { const b = by[s] || (by[s] = [0, 0]); b[1]++; if (s === 'fn-lines' && left > 0) left--; else { b[0]++; right++; } }));
  return { at: Date.now(), score: right, items: EXAM.items.length, passed: true, passedAuto: true, bySkill: by, bySkillAuto: by };
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
  const L = pickLesson();
  if (!L) die('no exp-log lesson requires functions/L2');
  const nFl = EXAM.items.filter(it => (it.skills || []).includes('fn-lines')).length;
  if (nFl !== 2) die(`topic-0.2 holds ${nFl} fn-lines items, this case assumes 2`);
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
    /* a stored profile: only the topic 0.2 attempt, the lesson's other prerequisites recorded met, strict prerequisites on, no lesson done, no skill record */
    const profile = (attempt) => page.evaluate(([a, others]) => {
      const d = JSON.parse(ZQ.state.export());
      d.lessons = {}; d.reviews = {}; d.homework = {}; d.skills = {}; d.redo = [];
      d.exams = { 'topic-0.2': { attempts: [a] } };
      d.prereq = { met: Object.fromEntries(others.map(k => [k, { how: 'auto', at: Date.now() }])), testouts: {}, opened: {}, started: {}, grandfathered: true };
      d.settings.strictPrereqs = true; d.flags.setupDone = true;
      const r = ZQ.state.import(d);
      return !!(r && r.ok);
    }, [attempt, L.others]);
    const go = async (h) => { await page.evaluate((x) => { delete window.ZQ.test; location.hash = x; }, h); await page.waitForTimeout(1200); };
    console.log(`lesson: exp-log/${L.id} (level ${L.n}) needs functions/L2; ${mobile ? 'mobile 440' : 'desktop 1280'}`);

    check('profile with fn-lines 1 of 2 imports', await profile(attemptWith(1)));
    await page.evaluate(() => ZQ.content.loadEssentials('functions'));
    await go(`lesson/exp-log/${L.id}`);
    let r = await page.evaluate(() => ({ lock: !!document.querySelector('.lk'), open: !!document.querySelector('.lsn'), met: ZQ.prereq.levelMet('functions', 2) }));
    check('1 of 2 on fn-lines: functions level 2 is met and the lesson opens', r.met && r.open && !r.lock, JSON.stringify(r));

    await go('today');
    check('profile with fn-lines 0 of 2 imports', await profile(attemptWith(2)));
    await go(`lesson/exp-log/${L.id}`);
    r = await page.evaluate(() => {
      const row = document.querySelector('.lk-row[data-ref="functions/L2"]');
      return { lock: !!document.querySelector('.lk'), row: !!row, text: row ? (row.querySelector('.lk-exam') || {}).textContent || null : null, testout: !!(row && row.querySelector('.lk-testout')),
        wide: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1, rowWide: row ? row.scrollWidth > row.clientWidth + 1 : false };
    });
    check('0 of 2: the lesson is locked', r.lock && r.row, JSON.stringify(r));
    check('0 of 2: the row says why, naming the skill and score', r.text === 'Your topic exam pass does not cover this level: 0 of 2 on straight-line graphs.', String(r.text));
    check('0 of 2: the row keeps its Test out button', r.testout);
    check('no sideways scroll', !r.wide && !r.rowWide, JSON.stringify(r));
  } catch (e) {
    check('no exception', false, String(e && e.stack || e).split('\n').slice(0, 3).join(' | '));
  }
  await browser.close();
  proc.kill();
  console.log(fails.length ? `${fails.length} failed` : 'all passed');
  process.exit(fails.length ? 1 : 0);
};
main().catch(e => { console.error(e); process.exit(2); });
