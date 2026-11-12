#!/usr/bin/env node
/* Second read, vectors: what LaTeX does the app's math field (MathLive 0.105.0, as expression.js builds it) hold after a learner
   types a matrix or a vector on a keyboard? Opens the local MathLive in headless Chromium, types each string key by key into a
   <math-field> and prints mf.value. With --grade, each LaTeX is then graded by exprGrade against the part named beside it.

   node docs/reviews/review-problems-1.4-a-scripts/mathlive-typed.mjs --local-cdn <pkgs>      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const CHROMIUM = '/opt/pw-browsers/chromium';

/* [typed keys, set, item, part, what it is] */
const ROWS = [
  ['[[1,0.25],[0,1]]', 2, 'p-italic-letters', 1, 'the right matrix'],
  ['[[1,0],[0.25,1]]', 2, 'p-italic-letters', 1, 'the `rows` slip'],
  ['[[1.5,0.25],[0,1]]', 2, 'p-italic-letters', 3, 'the `order` slip'],
  ['[[0.8,0.6],[-0.6,0.8]]', 2, 'p-site-plan', 1, 'the `clockwise` slip'],
  ['[[0.3,-0.1],[-0.2,0.4]]', 3, 'p-goat-feed', 3, 'the `no-divide` slip'],
  ['[[3,-1],[-2,4]]', 3, 'p-goat-feed', 3, 'the right matrix'],
  ['[[2(k+3),k+2],[5,2]]', 3, 'p-engraver-dial', 1, 'the right matrix, entry (1, 1) as 2(k+3)'],
  ['[[6+2k,2+k],[5,2]]', 3, 'p-engraver-dial', 1, 'the right matrix'],
  ['[[7,3k+1],[5,2k+1]]', 3, 'p-engraver-dial', 1, 'the `order` slip'],
  ['((3,-1),(-2,4))', 3, 'p-goat-feed', 3, 'the right matrix in round brackets'],
  ['(4,8)', 2, 'p-italic-letters', 2, 'the right vector'],
  ['[4,8]', 2, 'p-italic-letters', 2, 'the right vector, square brackets'],
  ['4,8', 2, 'p-italic-letters', 2, 'the right vector, no brackets'],
  ['(0.6,0.8)', 1, 'p-drone-crosswind', 1, 'the right vector'],
  ['(-0.1,0.15,-0.05)', 1, 'p-active-bets', 1, 'the right vector'],
  ['2-k', 3, 'p-engraver-dial', 2, 'the right expression'],
];

const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const partOf = (n, id, k) => JSON.parse(fs.readFileSync(`app/content/courses/vectors/problems-${n}.json`, 'utf8')).items.find(i => i.id === id).parts[k - 1].widget;

const mlFile = ['mathlive.min.js', 'dist/mathlive.min.js'].map(f => path.join(cdn, 'mathlive-0.105.0', 'package', f)).find(f => fs.existsSync(f));
const browser = await pw.chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
const page = await browser.newPage();
await page.setContent('<!doctype html><html><body><div id="host"></div></body></html>');
await page.addScriptTag({ path: mlFile });
await page.waitForFunction(() => !!window.customElements.get('math-field'));
for (const [keys, n, id, k, what] of ROWS) {
  const latex = await page.evaluate(async (keys) => {
    const host = document.getElementById('host'); host.innerHTML = '';
    const mf = document.createElement('math-field'); mf.mathVirtualKeyboardPolicy = 'manual'; host.appendChild(mf);
    await new Promise(r => setTimeout(r, 350)); mf.focus(); await new Promise(r => setTimeout(r, 150));
    return 'ready';
  }, keys).then(async () => { await page.click('math-field'); await page.keyboard.type(keys, { delay: 12 }); return page.evaluate(() => document.querySelector('math-field').value); });
  const w = partOf(n, id, k);
  const r = G.exprGrade(ce, w, latex, latex);
  console.log(`${what.padEnd(42)} keys ${keys.padEnd(26)} field ${latex}\n${''.padEnd(42)} -> ${r.ok ? 'ACCEPTED' : 'refused'}${r.key ? ', key ' + r.key : ''}${r.line ? ', line "' + r.line + '"' : ''}`);
}
await browser.close();
