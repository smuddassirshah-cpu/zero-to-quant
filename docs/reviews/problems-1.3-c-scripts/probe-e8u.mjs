#!/usr/bin/env node
/* Why does the grader refuse \frac{400}{e^{8u}} against 400e^{-8u}? Prints what the Compute Engine makes of each form.
   node docs/reviews/problems-1.3-c-scripts/probe-e8u.mjs --local-cdn <pkgs> */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
for (const s of ['\\frac{400}{e^{8u}}', '400e^{-8u}', '\\frac{400}{e^{7u}}', '\\frac{4}{e^{8u}}', '\\frac{400}{e^{9u}}', '\\frac{400}{e^{10u}}']) {
  const E = ce.parse(s);
  const out = [0.5, 1.7, 2.9].map((u) => { try { return E.subs({ u }).N().re; } catch (e) { return 'threw'; } });
  const want = [0.5, 1.7, 2.9].map((u) => { const m = s.match(/(\d+)\}\{e\^\{(\d+)u|(\d+)e\^\{-(\d+)u/); const a = +(m[1] || m[3]), k = +(m[2] || m[4]); return a * Math.exp(-k * u); });
  console.log(s.padEnd(22), JSON.stringify(E.json), '\n    engine', out.join('  '), '\n    true  ', want.join('  '));
}
