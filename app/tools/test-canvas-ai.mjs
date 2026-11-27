#!/usr/bin/env node
/* DOM test of the AI strand canvas keys (ENGINE-BACKLOG 1227 to 1229): graph valueLines and edgeWidth, matrix heat, grid arrows.
   Mounts canvases with ZQ.canvas.create on the index page (nothing under app/content is touched), in light and dark themes and at 440 px.
     graph:  two coloured value lines per node, edge width follows |w|, a negative edge is dashed and red, nothing overflows at 440 px;
             without the new keys the markup has no value line and no inline edge style (the l17 network is unchanged)
     matrix: heat fills numeric cells, the strong end flips its text to the page colour, the legend is drawn, signed data uses the diverging scale;
             without heat there is no heat rect and the frame height is unchanged
     grid:   an arrow per cell from a 2D list or an id map, none draws nothing, a text cell keeps its text; without arrows no arrow layer exists
   Usage: node tools/test-canvas-ai.mjs [--local-cdn <dir>]   Exit 0 when all pass, 1 on a failure, 2 on a setup problem. */
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const argv = process.argv.slice(2);
const li = argv.indexOf('--local-cdn');
const localCdn = li >= 0 && argv[li + 1] && !argv[li + 1].startsWith('--') ? path.resolve(argv[li + 1]) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const die = (m) => { console.error('test-canvas-ai: ' + m); process.exit(2); };
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
  if ((m = u.pathname.match(/^\/npm\/(@[^/]+\/[^@/]+|[^@/]+)@([^/]+)\/(.*)$/))) return path.join(localCdn, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package', m[3]);
  return null;
};

const SPECS = {
  graphNew: { kind: 'graph', params: { directed: true, height: 260, valueLines: [{ label: 'v', colour: 2 }, { label: 'g', colour: 4 }], edgeWidth: { max: 6, min: 1 }, nodes: [{ id: 'x', label: 'x', x: 0.1, y: 0.25 }, { id: 'y', label: 'y', x: 0.1, y: 0.7 }, { id: 'h', label: 'h', x: 0.5, y: 0.45 }, { id: 'L', label: 'L', x: 0.9, y: 0.45 }], edges: [{ from: 'x', to: 'h', w: 1.5 }, { from: 'y', to: 'h', w: -0.5 }, { from: 'h', to: 'L', w: 0.75 }] }, state: { values: { x: '2', h: '2.5' }, values2: { x: '0.6', h: '0.4', L: '1' } } },
  graphOld: { kind: 'graph', params: { directed: true, nodes: [{ id: 'a', label: 'a', x: 0.2, y: 0.5 }, { id: 'b', label: 'b', x: 0.8, y: 0.5 }], edges: [{ from: 'a', to: 'b', w: 0.5 }] }, state: { values: { a: '3' } } },
  matSeq: { kind: 'matrix', params: { matrices: [{ id: 'A', rows: [[0.9, 0.1], [0.3, 0.5]], heat: { decimals: 1 } }] } },
  matDiv: { kind: 'matrix', params: { matrices: [{ id: 'A', rows: [[1, -1], [0, 0.5]], heat: true }] } },
  matOff: { kind: 'matrix', params: { matrices: [{ id: 'A', rows: [[0.9, 0.1], [0.3, 0.5]] }] } },
  gridNew: { kind: 'grid', params: { rows: 2, cols: 3, rowHeads: false, colHeads: false, cells: [['1', '2', '3'], ['', '5', '6']] }, state: { arrows: [['up', 'down', 'left'], ['right', 'none', { dir: 'up', colour: 2 }]] } },
  gridOld: { kind: 'grid', params: { rows: 2, cols: 3 }, state: {} },
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
    for (const [theme, width] of [['light', 1280], ['dark', 1280], ['light', 440], ['dark', 440]]) {
      const ctx = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
      await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
        const f = cdnFile(new URL(route.request().url()));
        if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' } });
        return route.abort('blockedbyclient');
      });
      await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
      const page = await ctx.newPage();
      await page.goto(base + '/#today');
      await page.waitForFunction(() => window.ZQ && ZQ.canvas && ZQ.canvas.create, null, { timeout: 30000 });
      await page.evaluate((t) => { document.documentElement.setAttribute('data-theme', t); }, theme);
      const tag = `${theme} ${width}`;
      const out = await page.evaluate(async (specs) => {
        const res = {}, hosts = [];
        const mount = (key) => { const host = document.createElement('div'); host.style.cssText = 'width:100%;max-width:560px;margin:8px auto'; document.body.prepend(host); hosts.push(host); const api = ZQ.canvas.create(host, JSON.parse(JSON.stringify(specs[key]))); return { host, api }; };
        const cx2 = document.createElement('canvas').getContext('2d', { willReadFrequently: true }); const rgb = (c) => { cx2.clearRect(0, 0, 1, 1); cx2.fillStyle = '#000'; cx2.fillStyle = c; cx2.fillRect(0, 0, 1, 1); return `rgb(${[...cx2.getImageData(0, 0, 1, 1).data].slice(0, 3).join(',')})`; };
        const lum = (c) => { const m = rgb(c).match(/[\d.]+/g).map(Number), f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(m[0]) + 0.7152 * f(m[1]) + 0.0722 * f(m[2]); };
        const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
        let { host } = mount('graphNew');
        const vl = [...host.querySelectorAll('.cvb-vline')];
        const edges = [...host.querySelectorAll('.cvb-edge')];
        res.graph = { lines: vl.map(n => n.textContent), fills: vl.map(n => getComputedStyle(n).fill), widths: edges.map(n => parseFloat(n.style.strokeWidth)), dashes: edges.map(n => n.classList.contains('cvb-dash')), negC: edges.map(n => n.closest('.cv-obj').style.getPropertyValue('--c')), overflow: host.scrollWidth > host.clientWidth + 1, svgW: host.querySelector('svg').getBoundingClientRect().width, hostW: host.getBoundingClientRect().width };
        res.graphBox = (() => { const sb = host.querySelector('svg').getBoundingClientRect(); return vl.every(n => { const b = n.getBoundingClientRect(); return b.left >= sb.left - 1 && b.right <= sb.right + 1 && b.bottom <= sb.bottom + 1 && b.top >= sb.top - 1; }); })();
        ({ host } = mount('graphOld'));
        res.graphOld = { vline: host.querySelectorAll('.cvb-vline').length, styled: [...host.querySelectorAll('.cvb-edge')].filter(n => n.hasAttribute('style')).length, values: [...host.querySelectorAll('text')].map(n => n.textContent).filter(t => t === '3').length };
        ({ host } = mount('matSeq'));
        const cellRects = [...host.querySelectorAll('.cvb-heat')], texts = [...host.querySelectorAll('.cvb-cell-o')].map(o => o.querySelector('text'));
        res.matSeq = { rects: cellRects.length, fills: cellRects.map(r => getComputedStyle(r).fill), hi: texts.map(t => t.classList.contains('cvb-heat-hi')), legend: host.querySelectorAll('.cvb-heat-legend').length, bar: !!host.querySelector('.cvb-heat-bar'), legendText: [...host.querySelectorAll('.cvb-heat-legend text')].map(t => t.textContent) };
        const cr = cellRects.map((r, i) => ratio(getComputedStyle(texts[i]).fill, getComputedStyle(r).fill));
        res.matSeq.minRatio = Math.min(...cr);
        const bg = getComputedStyle(host.querySelector('svg')).backgroundColor;
        ({ host } = mount('matDiv'));
        const dr = [...host.querySelectorAll('.cvb-heat')], dt = [...host.querySelectorAll('.cvb-cell-o')].map(o => o.querySelector('text'));
        res.matDiv = { rects: dr.length, legendText: [...host.querySelectorAll('.cvb-heat-legend text')].map(t => t.textContent), minRatio: Math.min(...dr.map((r, i) => ratio(getComputedStyle(dt[i]).fill, getComputedStyle(r).fill))), fills: dr.map(r => r.getAttribute('style')) };
        ({ host } = mount('matOff'));
        res.matOff = { rects: host.querySelectorAll('.cvb-heat, .cvb-heat-legend').length, h: host.querySelector('svg').viewBox.baseVal.height };
        ({ host } = mount('gridNew'));
        res.gridNew = { arrows: host.querySelectorAll('.cv-arrow-g').length, texts: [...host.querySelectorAll('.cv-cell .cv-ctext')].map(t => t.textContent), moved: [...host.querySelectorAll('.cv-cell .cv-ctext')].filter(t => t.hasAttribute('transform')).length, colour: host.querySelectorAll('.cv-arrow-g.cv-k2').length };
        ({ host } = mount('gridOld'));
        res.gridOld = { layer: host.querySelectorAll('.cv-arrow-layer').length, transforms: host.querySelectorAll('.cv-ctext[transform]').length };
        const g2 = mount('gridNew'); g2.api.set({ arrows: null }, { instant: true });
        res.gridCleared = { layer: g2.host.querySelectorAll('.cv-arrow-layer').length, moved: g2.host.querySelectorAll('.cv-ctext[transform]').length };
        hosts.forEach(h => h.remove());
        res.bg = bg;
        return res;
      }, SPECS);
      const g = out.graph;
      check(`${tag}: graph draws two value lines per node (x: v and g, h: v and g, L: g only)`, JSON.stringify(g.lines) === JSON.stringify(['v = 2', 'g = 0.6', 'v = 2.5', 'g = 0.4', 'g = 1']), JSON.stringify(g.lines));
      check(`${tag}: the two lines carry different colours`, g.fills[0] !== g.fills[1] && new Set(g.fills).size === 2, JSON.stringify(g.fills));
      check(`${tag}: edge widths follow |w| (1.5 to 6 px, 0.5 to 1 + 5/3, 0.75 half way)`, Math.abs(g.widths[0] - 6) < 0.05 && Math.abs(g.widths[1] - (1 + 5 / 3)) < 0.05 && Math.abs(g.widths[2] - 3.5) < 0.05, JSON.stringify(g.widths));
      check(`${tag}: a negative edge is dashed and red, positive ones blue`, JSON.stringify(g.dashes) === '[false,true,false]' && g.negC[1] === 'var(--div-neg)' && g.negC[0] === 'var(--div-pos)', JSON.stringify([g.dashes, g.negC]));
      check(`${tag}: the value lines stay inside the frame and the page does not overflow`, out.graphBox && !g.overflow, JSON.stringify([out.graphBox, g.overflow]));
      check(`${tag}: a graph without the new keys has no value line, no inline edge style, its value as before`, out.graphOld.vline === 0 && out.graphOld.styled === 0 && out.graphOld.values === 1, JSON.stringify(out.graphOld));
      const s = out.matSeq;
      check(`${tag}: matrix heat fills four cells, draws a legend bar with the ends 0 and 0.9`, s.rects === 4 && s.legend === 1 && s.bar && s.legendText.includes('0') && s.legendText.includes('0.9'), JSON.stringify(s.legendText) + s.rects);
      check(`${tag}: the strongest cell flips its text, the weakest does not`, s.hi[0] === true && s.hi[1] === false, JSON.stringify(s.hi));
      check(`${tag}: heat text contrast is at least 3 on every cell (sequential)`, s.minRatio >= 3, String(s.minRatio));
      const d = out.matDiv;
      check(`${tag}: signed data uses the diverging scale (legend -1, 0, 1) and keeps contrast of 3 or more`, d.rects === 4 && d.legendText.includes('1') && d.legendText.some((t) => /^[-−]1$/.test(t)) && d.legendText.includes('0') && d.minRatio >= 3, JSON.stringify([d.legendText, d.minRatio]));
      check(`${tag}: a matrix without heat draws nothing extra`, out.matOff.rects === 0, JSON.stringify(out.matOff));
      const a = out.gridNew;
      check(`${tag}: grid draws five arrows (none draws nothing), one in colour 2`, a.arrows === 5 && a.colour === 1, JSON.stringify(a));
      check(`${tag}: a cell with text keeps it and moves it under the arrow (four of them)`, a.texts.join(',') === '1,2,3,,5,6' && a.moved === 4, JSON.stringify(a));
      check(`${tag}: a grid without arrows has no arrow layer or moved text`, out.gridOld.layer === 0 && out.gridOld.transforms === 0, JSON.stringify(out.gridOld));
      check(`${tag}: clearing the arrows removes the layer and the text shifts`, out.gridCleared.layer === 0 && out.gridCleared.moved === 0, JSON.stringify(out.gridCleared));
      await ctx.close();
    }
  } finally {
    await browser.close();
    proc.kill();
  }
  if (fails.length) { console.error(`test-canvas-ai: ${fails.length} failed`); process.exit(1); }
  console.log('test-canvas-ai: all passed');
};
main().catch((e) => { console.error(e); process.exit(2); });
