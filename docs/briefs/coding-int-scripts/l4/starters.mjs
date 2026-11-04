// Grades every code widget's starter and solution of the level in the real app (Pyodide and clang from the local CDN).
import fs from 'fs';
import path from 'path';
import net from 'net';
import { spawn } from 'child_process';
import { execSync } from 'child_process';
import { pathToFileURL } from 'url';

const APP = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app';
const CDN = '/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/pkgs';
const COURSE = path.join(APP, 'content/courses/coding-int');
const root = execSync('npm root -g', { encoding: 'utf8' }).trim();
const { chromium } = await import(pathToFileURL(path.join(root, 'playwright', 'index.mjs')).href);

const port = await new Promise((res) => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); });
const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', APP], { stdio: 'ignore' });
const base = `http://127.0.0.1:${port}`;
for (let i = 0; i < 100; i++) { try { const r = await fetch(base + '/index.html'); if (r.ok) break; } catch { /* wait */ } await new Promise(r => setTimeout(r, 100)); }
const MIME = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm', '.zip': 'application/zip', '.whl': 'application/zip', '.tar': 'application/x-tar' };
const cdnFile = (u) => {
  let m;
  if ((m = u.pathname.match(/^\/pyodide\/v([\d.]+)\/full\/(.*)$/))) return path.join(CDN, `pyodide-${m[1]}`, 'package', m[2]);
  if ((m = u.pathname.match(/^\/npm\/(@[^/]+\/[^@/]+|[^@/]+)@([^/]+)\/(.*)$/))) return path.join(CDN, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package', m[3]);
  return null;
};
const CHROMIUM = '/opt/pw-browsers/chromium';
const browser = await chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 860 } });
await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
  const f = cdnFile(new URL(route.request().url()));
  if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
  return route.fulfill({ status: 404, body: '' });
});
await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
const page = await ctx.newPage();
await page.goto(base + '/#setup');
await page.waitForFunction(() => window.ZQ && ZQ.content && ZQ.content.ready && ZQ.state);
await page.evaluate(() => ZQ.content.ready.then(() => { localStorage.clear(); sessionStorage.clear(); ZQ.state.reset(); }));
await page.reload();
await page.waitForFunction(() => window.ZQ && ZQ.content && ZQ.content.ready);
await page.waitForSelector('[data-name]');
await page.fill('[data-name]', 'Check');
await page.click('[data-next]');
await page.click('[data-track="Trader"]');
await page.click('[data-next]');
await page.click('[data-h="15"]');
await page.click('[data-stage="1"]');
await page.click('[data-next]');
await page.waitForFunction(() => window.ZQ && ZQ.state && ZQ.state.flags.setupDone === true);

const waitReady = async () => {
  await page.waitForFunction(() => ![...document.querySelectorAll('.wd-py')].some(e => ['idle', 'loading', 'restarting', 'running'].includes(e.dataset.s)), null, { timeout: 400000 });
};
const rows = [];
const gradeBoth = async (label, getWidget) => {
  // starter touched (add a trailing comment so it counts as a try), then solution
  const out = await page.evaluate(async ({ getWidget }) => {
    const w = eval(getWidget);
    const spec = w.spec || null;
    return { has: !!w };
  }, { getWidget });
  return out;
};

for (const lessonId of ['l15-reading-an-assessment', 'l16-edge-cases-first', 'l17-two-in-sixty', 'l18-talking-while-coding', 'l19-a-live-round']) {
  const lesson = JSON.parse(fs.readFileSync(path.join(COURSE, lessonId + '.json'), 'utf8'));
  for (let i = 0; i < lesson.screens.length; i++) {
    const s = lesson.screens[i];
    if (!s.widget || s.widget.kind !== 'code') continue;
    await page.evaluate((id) => ZQ.prereq.unlock('coding-int', id), lessonId);
    await page.goto(base + `/#lesson/coding-int/${lessonId}`);
    await page.waitForFunction(() => window.ZQ && ZQ.test && ZQ.test.current().kind !== 'loading');
    await page.evaluate((i) => ZQ.test.goto(i), i);
    await page.waitForTimeout(500);
    await waitReady();
    const total = s.widget.tests.length;
    const run = async (src) => page.evaluate(async (src) => {
      const w = ZQ.test.step().widget;
      w.set(src);
      const r = await w.grade();
      return { ok: r.ok, passed: r.detail ? r.detail.passed : null, total: r.detail ? r.detail.total : null, key: r.key };
    }, src);
    const st = await run(s.widget.starter + '\n');
    await page.waitForTimeout(1500);
    await waitReady();
    const so = await run(s.widget.solution);
    rows.push({ id: `${lessonId} screen ${i + 1}`, total, starter: `${st.passed}/${st.total} (${st.key})`, solution: `${so.passed}/${so.total}`, solutionOk: so.ok, starterOk: st.ok });
    console.log(rows[rows.length - 1]);
  }
}
for (const setId of ['homework-4']) {
  const hw = JSON.parse(fs.readFileSync(path.join(COURSE, setId + '.json'), 'utf8'));
  for (let j = 0; j < hw.items.length; j++) {
    const it = hw.items[j];
    if (!it.widget || it.widget.kind !== 'code') continue;
    await page.evaluate((id) => ZQ.prereq.unlock('coding-int', id), setId);
    await page.goto(base + `/#homework/coding-int/${setId}`);
    await page.waitForFunction(() => window.ZQHomework && ZQHomework.handles().length > 0);
    await page.waitForTimeout(800);
    await waitReady();
    const run = async (src) => page.evaluate(async ({ src, j }) => {
      const w = ZQHomework.handles()[j].step.widget;
      w.set(src);
      const r = await w.grade();
      return { ok: r.ok, passed: r.detail ? r.detail.passed : null, total: r.detail ? r.detail.total : null, key: r.key };
    }, { src, j });
    const st = await run(it.widget.starter + '\n');
    const so = await run(it.widget.solution);
    rows.push({ id: `${setId} item ${j + 1} ${it.id}`, total: it.widget.tests.length, starter: `${st.passed}/${st.total} (${st.key})`, solution: `${so.passed}/${so.total}`, solutionOk: so.ok, starterOk: st.ok });
    console.log(rows[rows.length - 1]);
  }
}
fs.writeFileSync(path.join(path.dirname(new URL(import.meta.url).pathname), 'starters.json'), JSON.stringify(rows, null, 1));
const bad = rows.filter(r => !r.solutionOk || r.starterOk);
console.log(bad.length ? 'PROBLEMS: ' + JSON.stringify(bad) : 'all solutions pass, all starters fail');
await browser.close();
proc.kill();
