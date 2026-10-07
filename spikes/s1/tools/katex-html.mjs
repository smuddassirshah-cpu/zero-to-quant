// Spike S1: renders the 40-formula specimen with KaTeX's HTML output, as the web app will, so a test can
// screenshot it beside the probe's MathML sheet. Writes compare/katex-html.html. Never published.
//
// Usage: node tools/katex-html.mjs
//
// Decision notes:
// - KaTeX, its CSS and its fonts come from the local npm copy (npm/katex-0.19.0/package), the CSS by a
//   file:// URL, so the page renders only on this machine. KaTeX's CSS finds its fonts relative to itself.
// - The sheet mirrors the probe's: 390 px wide, the same numbers, labels and inline wrappers, light
//   colours of the probe's tokens, so the two screenshots compare formula by formula.
// - Every formula renders with throwOnError: true and strict: 'error', so a typo or a non-strict
//   construct in probe/specimen.js stops the tool instead of reaching the owner as a red error.
// - The page sets data-ready and data-fonts on <html> once document.fonts settles, so a test can wait for
//   the KaTeX fonts and see whether any failed to load before it takes the screenshot. Firefox may refuse
//   file:// fonts from another folder [recalled]; screenshot it in Chromium or WebKit.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const KATEX_DIST = path.join(ROOT, 'npm', 'katex-0.19.0', 'package', 'dist');
const OUT = path.join(ROOT, 'compare', 'katex-html.html');
const KATEX_VERSION = '0.19.0';

const katex = (await import(pathToFileURL(path.join(KATEX_DIST, 'katex.mjs')).href)).default;
const { SPECIMEN, INLINE_BEFORE, INLINE_AFTER } = await import(pathToFileURL(path.join(ROOT, 'probe', 'specimen.js')).href);

if (katex.version !== KATEX_VERSION) {
  console.error(`katex-html: expected KaTeX ${KATEX_VERSION}, found ${katex.version}`);
  process.exit(1);
}
if (SPECIMEN.length !== 40) {
  console.error(`katex-html: the specimen has ${SPECIMEN.length} formulas, not 40`);
  process.exit(1);
}

const escapeHtml = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

const failures = [];
const items = SPECIMEN.map((s, i) => {
  const n = i + 1;
  let out;
  try {
    out = katex.renderToString(s.tex, { output: 'htmlAndMathml', displayMode: s.display, throwOnError: true, strict: 'error' });
  } catch (e) {
    failures.push(`${n} ${s.id}: ${e instanceof Error ? e.message : String(e)}`);
    return '';
  }
  const label = `<p class="label">${n}. ${escapeHtml(s.label)} (${s.display ? 'display' : 'inline'})</p>`;
  const formula = s.display
    ? `<div class="formula">${out}</div>`
    : `<p class="formula">${escapeHtml(INLINE_BEFORE)}${out}${escapeHtml(INLINE_AFTER)}</p>`;
  return `<div class="item" data-formula="${escapeHtml(s.id)}">${label}${formula}</div>`;
});

if (failures.length) {
  console.error(`katex-html: ${failures.length} formulas failed to render:\n${failures.join('\n')}`);
  process.exit(1);
}

const cssHref = pathToFileURL(path.join(KATEX_DIST, 'katex.min.css')).href;
const html = `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=390">
<title>Specimen, KaTeX HTML output</title>
<link rel="stylesheet" href="${escapeHtml(cssHref)}">
<style>
  * { box-sizing: border-box; }
  html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
  body { width: 390px; margin: 0; padding: 12px 16px 32px; background: #ffffff; color: #15191c; font: 400 16px/1.45 system-ui, -apple-system, 'Segoe UI', sans-serif; }
  p { margin: 0; }
  .sheet { border-top: 2px solid #5d666c; padding: 8px 0 0; }
  .head { font-weight: 600; }
  .item { padding: 8px 0; border-bottom: 1px solid #c3c8c0; }
  .label { font-size: 13px; color: #4b545a; }
  .formula { overflow-x: auto; overflow-y: hidden; padding: 2px 0; }
</style>
</head>
<body>
<section class="sheet" aria-label="KaTeX HTML specimen sheet: ${SPECIMEN.length} numbered formulas">
<p class="head">Specimen: ${SPECIMEN.length} formulas, KaTeX ${escapeHtml(katex.version)} HTML output (the web app).</p>
${items.join('\n')}
</section>
<script>
  document.fonts.ready.then(() => {
    const faces = Array.from(document.fonts).filter(f => f.family.includes('KaTeX'));
    const count = s => faces.filter(f => f.status === s).length;
    document.documentElement.dataset.fonts = 'loaded ' + count('loaded') + ', error ' + count('error') + ', unloaded ' + count('unloaded');
    document.documentElement.dataset.ready = '1';
  });
</script>
</body>
</html>
`;

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, html);
console.log(`katex-html: wrote ${path.relative(ROOT, OUT)} (${SPECIMEN.length} formulas, ${Buffer.byteLength(html)} bytes)`);
