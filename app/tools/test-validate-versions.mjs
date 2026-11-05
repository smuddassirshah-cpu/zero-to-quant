#!/usr/bin/env node
/* Scratch cases for the mock-version rules (ENGINE-BACKLOG 547). Copies app/ to a temp folder, applies tools/apply-item6-content.mjs
   there (so the copy is valid), then breaks one thing per case and expects the validator to report it (or, for "ok", nothing).
   Run from anywhere: node app/tools/test-validate-versions.mjs. One PASS or FAIL line per case, exit 1 on a failure. The repo is never touched. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-versions-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const run = (cmd, args) => { try { return { out: execFileSync('node', [path.join(copy, 'tools', cmd), ...args], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }), code: 0 }; } catch (e) { return { out: String(e.stdout || '') + String(e.stderr || ''), code: e.status || 1 }; } };
run('apply-item6-content.mjs', []);
const exam = (id) => path.join(copy, 'content', 'exams', id + '.json');
const prepFile = path.join(copy, 'content', 'prep.json');
const edit = (f, fn) => { const j = JSON.parse(fs.readFileSync(f, 'utf8')); fn(j); fs.writeFileSync(f, JSON.stringify(j, null, 2) + '\n'); };
const snap = (f) => fs.readFileSync(f, 'utf8');
const cases = [
  ['ok-as-shipped', () => {}, null],
  ['missing-versionOf', () => edit(exam('mock-oa-sig-2'), j => { delete j.versionOf; }), 'looks like a version of mock-oa-sig'],
  ['wrong-base-name', () => edit(exam('mock-oa-sig-3'), j => { j.versionOf = 'mock-oa-trader'; }), 'is named mock-oa-trader-<n>'],
  ['unknown-base', () => edit(exam('mock-oa-sig-3'), j => { j.versionOf = 'mock-nothing'; }), 'is not a mock exam file'],
  ['unreachable-from-prep', () => edit(prepFile, j => { j.paths.forEach(p => { if (Array.isArray(p.mocks)) p.mocks = p.mocks.filter(m => m !== 'mock-oa-sig'); }); }), 'unreachable from prep'],
];
let pass = 0, fail = 0;
for (const [name, mutate, has] of cases) {
  const keep = [exam('mock-oa-sig-2'), exam('mock-oa-sig-3'), exam('mock-oa-trader-2'), exam('mock-oa-trader-3'), prepFile].map(f => [f, snap(f)]);
  mutate();
  const r = run('validate.mjs', []);
  const errs = r.out.split('\n').filter(l => /^error/.test(l));
  let problem = null;
  if (has === null) { if (r.code !== 0 || errs.length) problem = `expected no error, got ${errs.length}: ${errs[0] || r.out.slice(-200)}`; }
  else if (!errs.some(l => l.includes(has))) problem = `no error contains "${has}" (got ${errs.length}: ${errs[0] || 'none'})`;
  keep.forEach(([f, t]) => fs.writeFileSync(f, t));
  if (problem) { console.log(`FAIL ${name}: ${problem}`); fail++; } else { console.log(`PASS ${name}`); pass++; }
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`${fail ? 'FAIL' : 'PASS'} summary: ${pass} of ${pass + fail} version cases passed`);
process.exit(fail ? 1 : 0);
