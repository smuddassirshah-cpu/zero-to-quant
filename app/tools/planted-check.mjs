#!/usr/bin/env node
/* Planted-wrong-solution check (ENGINE-BACKLOG 844). Run from app/:
     node tools/planted-check.mjs --drill <id> [--drill <id2>] | --all-drills [--require] [--near-miss] [--local-cdn <pkgs>]
   A drill may carry `planted`: [{ "code": "<a plausibly wrong solution>", "slip": "<one sentence naming the mistake>" }].
   Each drill's starter, every planted solution and the model solution run against the hidden tests in the real runtime (Pyodide, or the
   C++ toolchain), through `playthrough.mjs --drill <id> --planted`, so the runner is playthrough's own.
   Passes when the model solution passes every hidden test and the starter and every planted solution fail at least one.
   --require also fails a drill with fewer than two planted solutions; without it, drills with none are counted and skipped.
   --near-miss (ENGINE-BACKLOG 918) also fails a drill none of whose planted solutions is marked "nearMiss": true: the near-miss is the method one step short of the
   target (the slower order, the greedy without the exchange case, the off-by-one window). It is run like any plant, so it must fail a hidden test.
   Prints one line per failure and a one-line summary; exits 1 on any failure. ZQ_APP_DIR points it at a copy of app/ (the test uses this). */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = process.env.ZQ_APP_DIR ? path.resolve(process.env.ZQ_APP_DIR) : path.resolve(HERE, '..');
const DRILLS = path.join(APP, 'content', 'drills');
const argv = process.argv.slice(2), ids = [], pass = [];
let all = false, require = false, nearMiss = false;
const die = (m) => { console.error(`planted-check: ${m}`); process.exit(2); };
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === '--drill') { const v = argv[++i]; if (!v || v.startsWith('--')) die('--drill needs an id'); ids.push(v); }
  else if (a === '--all-drills') all = true;
  else if (a === '--require') require = true;
  else if (a === '--near-miss') nearMiss = true;
  else if (a === '--local-cdn') { pass.push(a); if (argv[i + 1] && !argv[i + 1].startsWith('--')) pass.push(argv[++i]); }
  else if (a === '--help' || a === '-h') { console.log(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('*/')[0].replace(/^#!.*\n\/\* ?/, '')); process.exit(0); }
  else die(`unknown argument ${a} (try --help)`);
}
if (!all && !ids.length) die('give --drill <id> or --all-drills');
const every = fs.readdirSync(DRILLS).filter(f => f.endsWith('.json') && f !== 'index.json').map(f => f.replace(/\.json$/, '')).sort();
const want = all ? every : ids;
for (const id of want) if (!every.includes(id)) die(`--drill ${id}: no such file in content/drills`);
const lines = [];
const withPlanted = [];
let skipped = 0;
for (const id of want) {
  const d = JSON.parse(fs.readFileSync(path.join(DRILLS, id + '.json'), 'utf8'));
  const n = Array.isArray(d.planted) ? d.planted.length : 0;
  if (nearMiss && !(Array.isArray(d.planted) && d.planted.some(p => p && p.nearMiss === true))) lines.push(`FAIL ${id}: no planted solution is marked "nearMiss": true (the method one step short of the target)`);
  if (require && n < 2) lines.push(`FAIL ${id}: ${n} planted solution${n === 1 ? '' : 's'}, --require wants at least two`);
  if (n) withPlanted.push(id); else if (!require) skipped++;
}
let checked = 0, planted = 0;
if (withPlanted.length) {
  const r = spawnSync('node', [path.join(HERE, 'playthrough.mjs'), ...withPlanted.flatMap(id => ['--drill', id]), '--planted', ...pass],
    { env: process.env, encoding: 'utf8', maxBuffer: 1 << 26 });
  const out = (r.stdout || '') + (r.stderr || '');
  const seen = new Set();
  for (const l of out.split('\n')) {
    let m;
    if ((m = /^PLANTED-FAIL (\S+) \| (.*)$/.exec(l))) { lines.push(`FAIL ${m[1]}: ${m[2]}`); seen.add(m[1]); }
    else if ((m = /^PLANTED-OK (\S+) \| (\d+) planted/.exec(l))) { seen.add(m[1]); }
  }
  for (const id of withPlanted) if (!seen.has(id)) lines.push(`FAIL ${id}: the playthrough gave no result (${out.trim().split('\n').slice(-1)[0] || 'no output'})`);
  for (const id of withPlanted) { checked++; planted += JSON.parse(fs.readFileSync(path.join(DRILLS, id + '.json'), 'utf8')).planted.length; }
}
lines.forEach(l => console.log(l));
const failed = lines.length;
console.log(`planted-check: ${checked} drill${checked === 1 ? '' : 's'} checked, ${planted} planted solution${planted === 1 ? '' : 's'}, ${skipped} skipped without any, ${failed} failure${failed === 1 ? '' : 's'}`);
process.exit(failed ? 1 : 0);
