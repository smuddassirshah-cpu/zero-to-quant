// Test for the playthrough's phone-width text check (engine pass 9, item d; ENGINE-BACKLOG 1159, 1167). Run from app/: node tools/test-playthrough-text-overflow.mjs [--local-cdn <pkgs>]
// Plays a temporary copy of app/ with tools/fixtures/overflow/problems-overflow.json added as a problem-set fixture: one inline maths span holding a long comma list that does not wrap.
// With --mobile it must fail with "at 440 px text runs past the window"; on the clean fixture (tools/fixtures/problems/problems-fixture-3.json) --mobile must stay green.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-textwide-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true });
fs.copyFileSync(path.join(HERE, 'fixtures/overflow/problems-overflow.json'), path.join(copy, 'tools/fixtures/problems/problems-overflow.json'));
const extra = process.argv.slice(2);
let bad = 0;
const play = (ref, mobile) => { const r = spawnSync('node', [path.join(HERE, 'playthrough.mjs'), '--problems', ref, ...(mobile ? ['--mobile'] : []), ...extra], { env: { ...process.env, ZQ_APP_DIR: copy }, encoding: 'utf8', timeout: 240000 }); return (r.stdout || '') + (r.stderr || ''); };
const cases = [
  ['fixture/problems-overflow', true, true, 'the wide span fails at 440 px'],
  ['fixture/problems-overflow', false, false, 'the wide span is not checked without --mobile'],
  ['fixture/problems-fixture-3', true, false, 'the clean set stays green at 440 px'],
];
for (const [ref, mobile, expectFail, name] of cases) {
  const out = play(ref, mobile), failed = /at 440 px (?:text runs past the window|text clipped by its box|the page is wider)/.test(out);
  if (failed !== expectFail) { bad++; console.log(`FAIL ${name}\n${out.split('\n').slice(-10).join('\n')}`); } else console.log(`ok ${name}`);
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
