#!/usr/bin/env node
/* One-off probes of exprEqual: node docs/reviews/problems-1.3-c-scripts/exprs.mjs --local-cdn <pkgs>
   Each row: [key, typed]. Prints what the engine's expression grader says. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = {}; vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const K = '-100e^{-2u}-400e^{-8u}+500e^{-5u}';
const ROWS = [
  [K, '-\\frac{100}{e^{2u}}-\\frac{400}{e^{8u}}+\\frac{500}{e^{5u}}'],
  [K, '\\frac{500}{e^{5u}}-\\frac{100}{e^{2u}}-\\frac{400}{e^{8u}}'],
  [K, '-100e^{-2u}-400e^{-8u}+\\frac{500}{e^{5u}}'],
  [K, '-\\frac{100}{e^{2u}}-400e^{-8u}+500e^{-5u}'],
  [K, '-100e^{-2u}-\\frac{400}{e^{8u}}+500e^{-5u}'],
  [K, '-100(e^{-2u}+4e^{-8u}-5e^{-5u})'],
  [K, '100(5e^{-5u}-e^{-2u}-4e^{-8u})'],
  [K, '-100e^{-2u}+500e^{-5u}-400e^{-8u}'],
  ['-\\frac{100}{e^{2u}}', '-100e^{-2u}'],
  ['\\frac{10re^{-10r}-(1-e^{-10r})}{r^2}', '\\frac{10r-e^{10r}+1}{r^2e^{10r}}'],
  ['\\frac{10re^{-10r}-(1-e^{-10r})}{r^2}', '\\frac{10r}{r^2e^{10r}}-\\frac{1}{r^2}+\\frac{1}{r^2e^{10r}}'],
  ['\\frac{10re^{-10r}-(1-e^{-10r})}{r^2}', '\\frac{e^{-10r}(10r+1)-1}{r^2}'],
  ['\\frac{10re^{-10r}-(1-e^{-10r})}{r^2}', '\\frac{10e^{-10r}}{r}+\\frac{e^{-10r}-1}{r^2}'],

  ['400e^{-8u}', '\\frac{400}{e^{8u}}'], ['e^{-8u}', '\\frac{1}{e^{8u}}'], ['400e^{-7u}', '\\frac{400}{e^{7u}}'], ['400e^{-9u}', '\\frac{400}{e^{9u}}'],
  ['400e^{-6u}', '\\frac{400}{e^{6u}}'], ['400e^{-10u}', '\\frac{400}{e^{10u}}'], ['4e^{-8u}', '\\frac{4}{e^{8u}}'], ['400e^{-8x}', '\\frac{400}{e^{8x}}'],
  ['e^{-10r}', '\\frac{1}{e^{10r}}'], ['-16e^{-0.5t}', '-\\frac{16}{e^{0.5t}}'],
];
for (const [a, b] of ROWS) {
  let r; try { r = G.exprEqual(ce, b, a, {}); } catch (e) { r = 'threw ' + e.message; }
  console.log(String(r).padEnd(6), b, '   vs key   ', a);
}
