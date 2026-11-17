#!/usr/bin/env node
/* Gallery survey: opens the System gallery (#system) in light and dark at 440x956 and 1376x900, saves one element
   screenshot per gallery card and measures console errors, horizontal overflow, empty entries and contrast.

   Run from app/:
     node tools/gallery-shots.mjs --out <dir> [--local-cdn <pkgs>] [--only light-440,dark-1376] [--no-load-code] [--sheets]

   --out <dir>        where screenshots and report.json go (default ./gallery-shots; never commit it)
   --local-cdn <dir>  serve cdn.jsdelivr.net and Google Fonts from unpacked npm packages (same layout as playthrough.mjs)
   --no-load-code     leave the code cards unloaded (they fetch Python or clang on request)
   --sheets           also write contact sheets (<out>/sheets/<combo>-NN.png) that pack the cards for quick reading

   Output: <out>/<theme>-<width>/<NNN>-<slug>.png, <out>/report.json (per combo: entries, console errors, findings),
   <out>/summary.txt (the findings as text). The page serves itself from app/ on a free port, so nothing else needs
   to be running. GALLERY_DEBUG=1 prints each stage.

   Reading the numbers: a shot is the card's own box, so anything that runs past the card shows only in the overflow
   list. An SVG group's box ignores clip-path, so "overflow ... g" on a clipped plot is not a fault by itself; the
   "page scrolls sideways" line names what really widens the page. Text contrast composites HTML backgrounds and the
   SVG shape under a label; it does not see halos (paint-order strokes), gradients or images. */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = fs.existsSync(path.join(HERE, '..', 'index.html')) ? path.resolve(HERE, '..') : path.resolve(process.cwd());
const argv = process.argv.slice(2);
const arg = (k, d = null) => { const i = argv.indexOf(k); return i < 0 ? d : (argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true); };
const OUT = path.resolve(arg('--out', 'gallery-shots'));
const CDN = arg('--local-cdn') ? path.resolve(arg('--local-cdn')) : (process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null);
const ONLY = arg('--only') ? String(arg('--only')).split(',') : null;
const LOAD_CODE = !argv.includes('--no-load-code');
const SHEETS = argv.includes('--sheets');

const loadPlaywright = async () => {
  try { return await import('playwright'); } catch { /* fall through */ }
  for (const r of [process.env.NODE_PATH, '/opt/node-tools/node_modules', '/usr/local/lib/node_modules', '/usr/lib/node_modules'].filter(Boolean).flatMap(s => s.split(':'))) {
    try { return createRequire(path.join(r, 'x.js'))('playwright'); } catch { /* next */ }
  }
  console.error('Playwright is not installed'); process.exit(2);
};

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm', '.zip': 'application/zip',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.map': 'application/json', '.whl': 'application/zip', '.tar': 'application/x-tar' };
const serve = () => new Promise((res) => {
  const s = http.createServer((q, r) => {
    let p = decodeURIComponent(new URL(q.url, 'http://x').pathname); if (p.endsWith('/')) p += 'index.html';
    const f = path.join(APP, path.normalize(p));
    if (!f.startsWith(APP) || !fs.existsSync(f) || !fs.statSync(f).isFile()) { r.writeHead(404); r.end(); return; }
    r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'cache-control': 'no-store' }); fs.createReadStream(f).pipe(r);
  });
  s.listen(0, '127.0.0.1', () => res(s));
});
const cdnFile = (u) => {
  let m;
  if ((m = u.pathname.match(/^\/pyodide\/v([\d.]+)\/full\/(.*)$/))) return path.join(CDN, `pyodide-${m[1]}`, 'package', m[2]);
  if ((m = u.pathname.match(/^\/npm\/(@[^/]+\/[^@/]+|[^@/]+)@([^/]+)\/(.*)$/))) return path.join(CDN, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package', m[3]);
  return null;
};
const routeCdn = async (ctx) => {
  if (!CDN) return;
  await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
    const f = cdnFile(new URL(route.request().url()));
    if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
    return route.fulfill({ status: 404, body: '' });
  });
  const fontsDir = path.join(CDN, 'fonts'), realFonts = fs.existsSync(path.join(fontsDir, 'fonts.css'));
  await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, r => {
    if (realFonts) {
      const u = new URL(r.request().url());
      const f = u.hostname === 'fonts.googleapis.com' ? path.join(fontsDir, 'fonts.css') : path.join(fontsDir, 'gstatic', path.normalize(u.pathname).replace(/^([/\\]|\.\.)+/, ''));
      if (f.startsWith(fontsDir) && fs.existsSync(f) && fs.statSync(f).isFile()) return r.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': f.endsWith('.css') ? 'text/css' : 'font/woff2', 'access-control-allow-origin': '*' } });
    }
    return r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } });
  });
};

/* Runs in the page: one record per gallery card. */
const measure = () => {
  const cvs = document.createElement('canvas'); cvs.width = cvs.height = 1; const cx = cvs.getContext('2d', { willReadFrequently: true });
  const rgba = (s) => { if (!s || s === 'none') return null; cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = s; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
  const over = (f, b) => { const a = f[3]; return [f[0] * a + b[0] * (1 - a), f[1] * a + b[1] * (1 - a), f[2] * a + b[2] * (1 - a), 1]; };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const hex = (c) => '#' + c.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const pageBg = (() => { const b = rgba(getComputedStyle(document.body).backgroundColor); const h = rgba(getComputedStyle(document.documentElement).backgroundColor); return over(b || [0, 0, 0, 0], h && h[3] ? over(h, [255, 255, 255, 1]) : [255, 255, 255, 1]); })();
  /* Background behind an element: HTML ancestors' background colours, composited. Images and gradients are not read. */
  const bgOf = (el) => {
    const stack = []; let e = el, img = false;
    while (e && e.nodeType === 1) { if (!(e instanceof SVGElement) || e.tagName === 'svg') { const s = getComputedStyle(e); const c = rgba(s.backgroundColor); if (c && c[3] > 0) stack.push(c); if (s.backgroundImage && s.backgroundImage !== 'none') img = true; if (c && c[3] === 1) break; } e = e.parentElement; }
    let b = pageBg; for (let i = stack.length - 1; i >= 0; i--) b = over(stack[i], b);
    return { c: b, img };
  };
  /* For SVG text: the fill of the nearest earlier sibling shape that contains the text centre, if any (a label drawn on a filled cell). */
  const svgUnder = (el, base) => {
    const svg = el.ownerSVGElement; if (!svg) return base;
    const r = el.getBoundingClientRect(), px = r.left + r.width / 2, py = r.top + r.height / 2; let b = base;
    const shapes = svg.querySelectorAll('rect, circle, ellipse, path, polygon');
    for (const s of shapes) {
      if (s.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_PRECEDING) break;   // s comes after el: stop
      const cs = getComputedStyle(s); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const f = rgba(cs.fill); if (!f || f[3] === 0) continue;
      const q = s.getBoundingClientRect(); if (px < q.left || px > q.right || py < q.top || py > q.bottom) continue;
      if (s.tagName === 'path' || s.tagName === 'polygon') { try { const pt = svg.createSVGPoint(); pt.x = px; pt.y = py; const m = s.getScreenCTM(); if (m && !s.isPointInFill(pt.matrixTransform(m.inverse()))) continue; } catch (e) { continue; } }
      const a = f[3] * parseFloat(cs.fillOpacity || 1) * parseFloat(cs.opacity || 1);
      b = over([f[0], f[1], f[2], a], b);
    }
    return b;
  };
  const sel = (el) => { const parts = []; let e = el; for (let i = 0; e && i < 3 && !e.classList.contains('ds-card'); i++, e = e.parentElement) { const c = (e.getAttribute('class') || '').trim().split(/\s+/).filter(Boolean).slice(0, 3).join('.'); parts.unshift(e.tagName.toLowerCase() + (c ? '.' + c : '')); } return parts.join(' > '); };
  const visible = (el) => { const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) return false; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) < 0.05) return false; if (e.hasAttribute('hidden')) return false; } return true; };
  const effOpacity = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1 && !e.classList.contains('ds-card'); e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity || 1); return o; };
  const vw = document.documentElement.clientWidth;
  const out = [];
  document.querySelectorAll('.ds-gal .ds-card').forEach((card, idx) => {
    const kind = card.dataset.kind, gal = card.parentElement.dataset.gal, body = card.querySelector('.ds-card-b');
    const cr = card.getBoundingClientRect(), br = body ? body.getBoundingClientRect() : { height: 0, width: 0 };
    const rec = { idx, gal, kind, w: Math.round(cr.width), h: Math.round(cr.height), bodyH: Math.round(br.height), overflow: [], empty: [], text: [], strokes: [], errors: [] };
    if (card.classList.contains('is-missing')) rec.errors.push('no sample for this kind');
    card.querySelectorAll('.ds-warn').forEach(w => rec.errors.push(w.textContent.trim().slice(0, 160)));
    if (!body || br.height < 8) rec.empty.push('card body has no height');
    if (cr.right > vw + 1) rec.overflow.push({ what: 'card wider than viewport', by: Math.round(cr.right - vw) });
    /* overflow: descendants past the card's right or left edge, unless an ancestor scrolls or clips them on purpose */
    const seen = new Set();
    card.querySelectorAll('.ds-card-b *').forEach(el => {
      if (!visible(el) || el.closest('.katex-mathml, .sr-only, .visually-hidden')) return;
      const r = el.getBoundingClientRect(); if (r.right <= cr.right + 1 && r.left >= cr.left - 1 && r.right <= vw + 1) return;
      let clip = null; for (let e = el.parentElement; e && e !== card; e = e.parentElement) { const s = getComputedStyle(e); if (/(auto|scroll|hidden|clip)/.test(s.overflowX)) { const q = e.getBoundingClientRect(); if (q.right <= cr.right + 1 && q.left >= cr.left - 1) { clip = s.overflowX; break; } } }
      if (el instanceof SVGElement && el.tagName !== 'svg') { const s = el.ownerSVGElement; if (s && getComputedStyle(s).overflow !== 'visible') { const q = s.getBoundingClientRect(); if (q.right <= cr.right + 1 && q.left >= cr.left - 1) clip = clip || 'svg-clip'; } }
      const key = sel(el) + '|' + clip; if (seen.has(key)) return; seen.add(key);
      rec.overflow.push({ what: sel(el), by: Math.round(Math.max(r.right - cr.right, cr.left - r.left)), clip: clip || 'none', text: (el.textContent || '').trim().slice(0, 40) });
    });
    card.querySelectorAll('.ds-card-b *').forEach(el => { if (el.scrollWidth > el.clientWidth + 2 && visible(el) && !(el instanceof SVGElement) && !el.closest('.katex')) { const s = getComputedStyle(el); if (/(auto|scroll)/.test(s.overflowX)) rec.overflow.push({ what: sel(el), by: el.scrollWidth - el.clientWidth, clip: 'scrolls', text: '' }); else if (/(hidden|clip)/.test(s.overflowX) && s.textOverflow !== 'ellipsis') rec.overflow.push({ what: sel(el), by: el.scrollWidth - el.clientWidth, clip: 'cut-off', text: (el.textContent || '').trim().slice(0, 40) }); } });
    /* empty drawings */
    if (body) {
      body.querySelectorAll('svg').forEach(s => { const r = s.getBoundingClientRect(); if (!visible(s)) return; if (r.height < 4 || r.width < 4) rec.empty.push('svg with no size: ' + sel(s)); else if (!s.querySelector('path, line, rect, circle, text, polygon, polyline, ellipse, use, image, foreignObject')) rec.empty.push('svg with no marks: ' + sel(s)); });
      body.querySelectorAll('canvas').forEach(c => { if (!visible(c)) return; try { const g = c.getContext('2d'); if (!g) { rec.empty.push('canvas without a 2d context (WebGL?): ' + sel(c)); return; } const d = g.getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i]) n++; if (!n) rec.empty.push('canvas is blank: ' + sel(c)); else rec.canvasPx = n; } catch (e) { rec.empty.push('canvas unreadable: ' + e.message); } });
      if (!body.querySelector('svg, canvas, table, button, input, textarea, math-field, .cv, [class*="cv"]') && !(body.textContent || '').trim()) rec.empty.push('card body is empty');
    }
    /* text contrast */
    const tseen = new Map();
    const walker = document.createTreeWalker(body || card, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      if (!n.nodeValue.trim()) continue; const el = n.parentElement; if (!el || !visible(el)) continue;
      if (el.closest('math-field, .ML__keyboard, details.ds-spec, script, style')) continue;
      const cs = getComputedStyle(el); const isSvg = el instanceof SVGElement;
      let fg = rgba(isSvg ? cs.fill : cs.color); if (!fg) continue;
      const op = effOpacity(el) * (isSvg ? parseFloat(cs.fillOpacity || 1) : 1);
      const b0 = bgOf(el); const bg = isSvg ? svgUnder(el, b0.c) : b0.c;
      fg = over([fg[0], fg[1], fg[2], fg[3] * op], bg);
      const cr2 = ratio(fg, bg), size = parseFloat(cs.fontSize), big = size >= 24 || (size >= 18.66 && parseInt(cs.fontWeight, 10) >= 700);
      if (cr2 < (big ? 3 : 4.5)) { const k = sel(el) + hex(fg) + hex(bg); const t = tseen.get(k); if (t) t.n++; else tseen.set(k, { what: sel(el), fg: hex(fg), bg: hex(bg), ratio: +cr2.toFixed(2), size, text: n.nodeValue.trim().slice(0, 30), disabled: !!el.closest('[disabled], [aria-disabled="true"]'), bgImg: b0.img, n: 1 }); }
    }
    rec.text = [...tseen.values()];
    /* stroke and fill contrast of SVG marks: anything under 1.5:1 against what is behind it cannot be seen */
    const sseen = new Map();
    (body || card).querySelectorAll('svg path, svg line, svg rect, svg circle, svg polyline, svg polygon, svg ellipse').forEach(el => {
      if (!visible(el)) return; const cs = getComputedStyle(el); const b = bgOf(el).c; const op = effOpacity(el);
      const st = rgba(cs.stroke), sw = parseFloat(cs.strokeWidth) || 0, fl = rgba(cs.fill);
      const sa = st ? st[3] * op * parseFloat(cs.strokeOpacity || 1) : 0, fa = fl ? fl[3] * op * parseFloat(cs.fillOpacity || 1) : 0;
      const push = (kind, c, a) => { const eff = over([c[0], c[1], c[2], a], b); const r = ratio(eff, b); const raw = hex(c); const k = kind + raw + sel(el); const o = sseen.get(k); if (o) { o.n++; return; } sseen.set(k, { kind, what: sel(el), raw, alpha: +a.toFixed(2), bg: hex(b), ratio: +r.toFixed(2), n: 1 }); };
      if (st && sa > 0.02 && sw > 0) push('stroke', st, sa);
      if (fl && fa > 0.02 && el.tagName !== 'line') push('fill', fl, fa);   // a line has no interior, its default black fill paints nothing
    });
    rec.strokes = [...sseen.values()];
    out.push(rec);
  });
  /* what makes the page itself scroll sideways: the outermost elements past the viewport edge */
  const wide = []; document.querySelectorAll('body *').forEach(el => { if (el.closest('.katex-mathml')) return; const r = el.getBoundingClientRect(); if (r.right > vw + 1 && r.width > 0 && visible(el) && !wide.some(w => w.el.contains(el))) { let clipped = false; for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) { if (/(auto|scroll|hidden|clip)/.test(getComputedStyle(e).overflowX) && e.getBoundingClientRect().right <= vw + 1) { clipped = true; break; } } if (!clipped) wide.push({ el, by: Math.round(r.right - vw) }); } });
  const pageWide = wide.slice(0, 12).map(w => ({ by: w.by, what: (w.el.closest('.ds-card') ? '[' + w.el.closest('.ds-card').dataset.kind + '] ' : '') + w.el.tagName.toLowerCase() + '.' + (w.el.getAttribute('class') || '').trim().split(/\s+/).slice(0, 3).join('.') }));
  return { vw, pageWide, docW: document.documentElement.scrollWidth, bodyW: document.body.scrollWidth, pageBg: hex(pageBg), theme: document.documentElement.getAttribute('data-theme'), cards: out };
};

const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 48);

const main = async () => {
  const { chromium } = await loadPlaywright();
  const server = await serve(), base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  const combos = [];
  for (const theme of ['light', 'dark']) for (const [w, h] of [[440, 956], [1376, 900]]) combos.push({ theme, w, h, id: `${theme}-${w}` });
  const report = { app: APP, when: new Date().toISOString(), localCdn: !!CDN, combos: {} };
  /* one combination; a run that stalls (seen once: the page stopped answering after the reload) is abandoned after 5 minutes and tried once more */
  const runCombo = async (c) => {
    const dir = path.join(OUT, c.id); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const ctx = await browser.newContext({ viewport: { width: c.w, height: c.h }, deviceScaleFactor: 1, colorScheme: c.theme, reducedMotion: 'reduce', hasTouch: c.w < 600 });   // not isMobile: with a page wider than the viewport it shifts element screenshots
    await routeCdn(ctx);
    const page = await ctx.newPage();
    const consoleErrors = [], failed = [];
    page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 300)); });
    page.on('pageerror', e => consoleErrors.push('pageerror: ' + String(e.message).slice(0, 300)));
    page.on('requestfailed', r => failed.push(r.url().slice(0, 160) + ' ' + (r.failure() ? r.failure().errorText : '')));
    page.on('response', r => { if (r.status() >= 400) failed.push(r.status() + ' ' + r.url().slice(0, 160)); });
    await page.goto(base + '/index.html#system', { waitUntil: 'load' });
    await page.waitForFunction(() => window.ZQ && ZQ.setSetting && document.querySelector('.ds-gal .ds-card'), null, { timeout: 30000 });
    await page.evaluate((t) => { ZQ.setSetting('theme', t); ZQ.setSetting('motion', 'reduced'); }, c.theme);
    await page.reload({ waitUntil: 'load' });
    await page.waitForFunction(() => window.ZQSystem && document.querySelectorAll('.ds-gal[data-gal="widget"] .ds-card').length > 0, null, { timeout: 30000 });
    const themeAttr = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    if (themeAttr !== c.theme) console.error(`${c.id}: data-theme is ${themeAttr}`);
    const step = (t) => { if (process.env.GALLERY_DEBUG) console.error(`${c.id}: ${t}`); };
    step('theme set');
    let codeNote = 'not loaded';
    if (LOAD_CODE) {
      const n = await page.evaluate(() => { const b = [...document.querySelectorAll('.ds-card [data-load]')]; b.forEach(x => x.click()); return b.length; });
      try {
        await page.waitForFunction(() => [...document.querySelectorAll('.ds-card')].filter(k => k.querySelector('[data-load]')).every(k => { const b = k.querySelector('.ds-card-b'); return b.querySelector('textarea, .cm-editor, [class*="code"]') && !/Loading|loading/.test(b.textContent.slice(0, 4000)); }), null, { timeout: 120000 });
        codeNote = `${n} code cards loaded`;
      } catch (e) { codeNote = `${n} code cards clicked; still loading after 120 s`; }
    }
    step('code ' + codeNote);
    /* settle: fonts, MathLive, lazy images, then a quiet moment */
    await page.evaluate(async () => { await document.fonts.ready; if (document.querySelector('math-field') && window.customElements) await Promise.race([customElements.whenDefined('math-field'), new Promise(r => setTimeout(r, 15000))]); });
    try { await page.waitForLoadState('networkidle', { timeout: 20000 }); } catch (e) { /* carry on */ }
    await page.evaluate(async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(1500);
    step('settled');
    const m = await page.evaluate(measure);
    step('measured');
    const mathPending = await page.evaluate(() => [...document.querySelectorAll('.ds-card')].filter(k => /\$[^$]+\$/.test([...k.querySelectorAll('.ds-card-b *')].filter(e => !e.children.length && !e.closest('textarea, pre, code, .cvc, [class*="console"], [class*="code"]')).map(e => e.textContent).join(' '))).map(k => k.dataset.kind));
    await page.addStyleTag({ content: '.ds-bar { position: static !important; } .shell-header { position: static !important; } .tabbar, .proto { visibility: hidden !important; }' });   // the sticky header and toolbar and the fixed tab bar would sit over the cards in the shots
    const cards = await page.$$('.ds-gal .ds-card');
    for (let i = 0; i < cards.length; i++) {
      const rec = m.cards[i]; rec.file = `${String(i + 1).padStart(3, '0')}-${rec.gal[0]}-${slug(rec.kind)}.png`;
      try { await cards[i].screenshot({ path: path.join(dir, rec.file), animations: 'disabled' }); } catch (e) { rec.errors.push('screenshot failed: ' + String(e.message).split('\n')[0]); }
    }
    /* the sections above the gallery (tokens, type, buttons, answer states, art) as five more shots */
    const secs = await page.$$('.ds > section:not(#ds-canvases):not(#ds-widgets)');
    for (let i = 0; i < secs.length; i++) { try { await secs[i].screenshot({ path: path.join(dir, `000-section-${i + 1}.png`), animations: 'disabled' }); } catch (e) { /* skip */ } }
    report.combos[c.id] = { theme: c.theme, width: c.w, height: c.h, entries: m.cards.length, canvasCards: m.cards.filter(x => x.gal === 'canvas').length, widgetCards: m.cards.filter(x => x.gal === 'widget').length,
      docScrollWidth: m.docW, pageWide: m.pageWide, pageOverflow: m.docW > m.vw, pageBg: m.pageBg, code: codeNote, rawMathLeft: mathPending, consoleErrors, failedRequests: [...new Set(failed)], cards: m.cards };
    console.log(`${c.id}: ${m.cards.length} entries (${report.combos[c.id].canvasCards} canvas, ${report.combos[c.id].widgetCards} widget), console errors ${consoleErrors.length}, failed requests ${new Set(failed).size}, page overflow ${m.docW > m.vw ? m.docW - m.vw + 'px' : 'none'}, code: ${codeNote}`);
    if (SHEETS) await sheets(browser, dir, c, m.cards);
    await ctx.close();
  };
  for (const c of combos.filter(c => !ONLY || ONLY.includes(c.id))) {
    for (let attempt = 1; attempt <= 2; attempt++) {
      let timer; const stall = new Promise((_, rej) => { timer = setTimeout(() => rej(new Error('stalled')), 300000); });
      try { await Promise.race([runCombo(c), stall]); clearTimeout(timer); break; }
      catch (e) { clearTimeout(timer); console.error(`${c.id}: attempt ${attempt} failed (${String(e.message).split('\n')[0]})`); for (const x of browser.contexts()) await x.close().catch(() => {}); if (attempt === 2) report.combos[c.id] = { failed: String(e.message) }; }
    }
  }
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 1));
  summary(report);
  await browser.close(); server.close();
};

/* Contact sheets: cards packed in columns on pages about 1500 px square, each labelled with its number. */
const sheets = async (browser, dir, c, cards) => {
  const sdir = path.join(OUT, 'sheets'); fs.mkdirSync(sdir, { recursive: true });
  const scale = c.w > 600 ? 0.62 : 0.85, colW = Math.round(Math.max(...cards.map(k => k.w)) * scale), cols = Math.max(1, Math.floor(1560 / (colW + 8))), maxH = 1560;
  const pages = []; let cur = null;
  const fresh = () => { cur = { cols: Array.from({ length: cols }, () => ({ h: 0, items: [] })) }; pages.push(cur); };
  fresh();
  for (const k of cards) {
    if (!k.file) continue; const h = Math.round(k.h * scale) + 22;
    let col = cur.cols.find(x => x.h + h <= maxH || x.h === 0);
    if (!col) { fresh(); col = cur.cols[0]; }
    col.items.push(k); col.h += h;
  }
  const ctx = await browser.newContext({ viewport: { width: cols * (colW + 8) + 8, height: 800 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  for (let i = 0; i < pages.length; i++) {
    const html = `<body style="margin:0;padding:4px;background:#808080;display:flex;gap:8px;align-items:flex-start;font:12px/18px monospace">${pages[i].cols.map(col => `<div style="width:${colW}px">${col.items.map(k => `<div style="background:#ff0;color:#000;height:18px;overflow:hidden;white-space:nowrap">${k.idx + 1} ${k.kind.replace(/</g, '&lt;')}</div><img style="display:block;width:${Math.round(k.w * scale)}px;margin-bottom:4px" src="file://${path.join(dir, k.file)}">`).join('')}</div>`).join('')}</body>`;
    const f = path.join(sdir, `_${c.id}-${i}.html`); fs.writeFileSync(f, html);
    await page.goto('file://' + f); await page.waitForLoadState('load');
    await page.screenshot({ path: path.join(sdir, `${c.id}-${String(i + 1).padStart(2, '0')}.png`), fullPage: true });
    fs.unlinkSync(f);
  }
  await ctx.close();
  console.log(`  ${pages.length} contact sheets in ${sdir}`);
};

const summary = (report) => {
  const lines = [];
  for (const [id, c] of Object.entries(report.combos)) {
    if (c.failed) { lines.push(`## ${id}: FAILED ${c.failed}`); continue; }
    lines.push(`## ${id}: ${c.entries} entries; console errors ${c.consoleErrors.length}; raw $ maths left in ${c.rawMathLeft.length}`);
    for (const e of [...new Set(c.consoleErrors)].slice(0, 20)) lines.push('  console: ' + e);
    if (c.pageOverflow) lines.push(`  page scrolls sideways by ${c.docScrollWidth - c.width}px: ` + c.pageWide.map(w => `${w.what} +${w.by}`).join('; '));
    for (const e of c.failedRequests.slice(0, 20)) lines.push('  request: ' + e);
    for (const k of c.cards) {
      const o = k.overflow.filter(x => x.clip === 'none' || x.clip === 'cut-off' || !x.clip);
      const lowT = k.text.filter(t => !t.disabled), inv = k.strokes.filter(s => s.kind === 'stroke' && s.ratio < 1.25 && s.alpha > 0.5 && !/cv-body|cvb-dot|cvb-hd|cvs-dot|cv-knob/.test(s.what));   // dots and bodies carry a background-coloured ring on purpose
      if (k.errors.length || k.empty.length || o.length || lowT.length || inv.length) {
        lines.push(`  [${k.idx + 1}] ${k.gal} ${k.kind}`);
        k.errors.forEach(e => lines.push('     error: ' + e)); k.empty.forEach(e => lines.push('     empty: ' + e));
        o.slice(0, 6).forEach(x => lines.push(`     overflow ${x.by}px (${x.clip || 'card'}): ${x.what} ${x.text ? JSON.stringify(x.text) : ''}`));
        lowT.slice(0, 8).forEach(t => lines.push(`     text ${t.ratio}:1 ${t.fg} on ${t.bg} ${t.size}px x${t.n}: ${t.what} ${JSON.stringify(t.text)}${t.bgImg ? ' (background image behind)' : ''}`));
        inv.slice(0, 6).forEach(s => lines.push(`     ${s.kind} ${s.ratio}:1 ${s.raw} a=${s.alpha} on ${s.bg} x${s.n}: ${s.what}`));
      }
    }
  }
  /* marks that keep one raw colour in both themes and fall under 3:1 in either */
  const ids = Object.keys(report.combos);
  for (const w of [440, 1376]) {
    const L = report.combos[`light-${w}`], D = report.combos[`dark-${w}`]; if (!L || !D || L.failed || D.failed) continue;
    lines.push(`## fixed colours at ${w}: same raw colour in both themes, under 3:1 in one`);
    L.cards.forEach((k, i) => { const d = D.cards[i]; if (!d) return; const dm = new Map(d.strokes.map(s => [s.kind + s.what + s.raw, s]));
      const hits = k.strokes.filter(s => { const o = dm.get(s.kind + s.what + s.raw); return o && (s.ratio < 3 || o.ratio < 3) && Math.abs(s.ratio - o.ratio) > 1.5 && s.alpha > 0.5; }).map(s => { const o = dm.get(s.kind + s.what + s.raw); return `${s.kind} ${s.raw} light ${s.ratio}:1 dark ${o.ratio}:1 ${s.what}`; });
      if (hits.length) { lines.push(`  [${k.idx + 1}] ${k.kind}`); hits.slice(0, 5).forEach(h => lines.push('     ' + h)); } });
  }
  fs.writeFileSync(path.join(OUT, 'summary.txt'), lines.join('\n') + '\n');
  console.log(`report.json and summary.txt written to ${OUT} (${ids.join(', ')})`);
};

main().catch(e => { console.error(e); process.exit(1); });
