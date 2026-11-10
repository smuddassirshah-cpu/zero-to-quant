// Test for tools/planted-check.mjs (ENGINE-BACKLOG 844). Run from app/: node tools/test-planted-check.mjs [--local-cdn <pkgs>] [--no-cpp]
// Plays a temporary copy of app/ with the fixture drills of tools/fixtures/planted/ added to content/drills:
//   planted-py-caught   one planted solution that a hidden test catches: the tool must pass
//   planted-py-missed   one planted solution that passes every hidden test: the tool must fail and name it
//   planted-cpp-caught, planted-cpp-missed   the same in C++ (--no-cpp skips them: the first C++ compile is slow)
// and checks --require (a drill with one planted solution fails) and the skip count (a drill with none is skipped, not failed).
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const args = process.argv.slice(2), noCpp = args.includes('--no-cpp'), extra = args.filter(a => a !== '--no-cpp');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-planted-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true });
for (const f of fs.readdirSync(path.join(HERE, 'fixtures/planted')).filter(f => f.endsWith('.json'))) fs.copyFileSync(path.join(HERE, 'fixtures/planted', f), path.join(copy, 'content/drills', f));
let bad = 0;
// the copy's own validator lists the fixtures in its manifest (the app loads only listed files) and checks their shape: 0 errors wanted
const v = spawnSync('node', [path.join(copy, 'tools/validate.mjs')], { encoding: 'utf8', maxBuffer: 1 << 26 });
const vOut = (v.stdout || '') + (v.stderr || '');
if (v.status !== 0 || !/\b0 errors/.test(vOut)) { bad++; console.log(`FAIL validator on the fixtures\n${vOut.split('\n').slice(-12).join('\n')}`); }
else console.log('ok validator accepts the fixture drills');
// shape rules: a planted entry with an empty code and a numeric slip, and a planted that is not an array, are errors
const badFile = path.join(copy, 'content/drills/planted-bad-shape.json');
const base = JSON.parse(fs.readFileSync(path.join(HERE, 'fixtures/planted/planted-py-caught.json'), 'utf8'));
for (const [label, planted, re] of [['empty code, numeric slip', [{ code: ' ', slip: 5 }], /planted\[0\]\.code[\s\S]*planted\[0\]\.slip|planted\[0\]\.slip[\s\S]*planted\[0\]\.code/], ['not an array', 'x', /planted is an array/], ['entry is a string', ['x'], /planted\[0\]/]]) {
  fs.writeFileSync(badFile, JSON.stringify({ ...base, id: 'planted-bad-shape', planted }));
  const b = spawnSync('node', [path.join(copy, 'tools/validate.mjs')], { encoding: 'utf8', maxBuffer: 1 << 26 });
  const o = (b.stdout || '') + (b.stderr || '');
  if (b.status === 0 || !re.test(o)) { bad++; console.log(`FAIL validator shape (${label}): exit ${b.status}`); } else console.log(`ok validator rejects planted: ${label}`);
}
fs.rmSync(badFile);
spawnSync('node', [path.join(copy, 'tools/validate.mjs')], { encoding: 'utf8', maxBuffer: 1 << 26 });   // restore the copy's manifest
const run = (label, cliArgs, wantExit, wantLines) => {
  const r = spawnSync('node', [path.join(HERE, 'planted-check.mjs'), ...cliArgs, ...extra], { env: { ...process.env, ZQ_APP_DIR: copy }, encoding: 'utf8', maxBuffer: 1 << 26 });
  const out = (r.stdout || '') + (r.stderr || '');
  const miss = wantLines.filter(re => !re.test(out));
  if (r.status !== wantExit || miss.length) { bad++; console.log(`FAIL ${label}: exit ${r.status} (wanted ${wantExit}), missing ${miss.map(String).join(' ')}\n${out.split('\n').slice(-12).join('\n')}`); }
  else console.log(`ok ${label}: exit ${r.status}, ${out.trim().split('\n').slice(-1)[0]}`);
};
run('python, planted solution caught', ['--drill', 'planted-py-caught'], 0, [/1 drill checked, 1 planted solution, 0 skipped without any, 0 failures/]);
run('python, planted solution passes every test', ['--drill', 'planted-py-missed'], 1, [/FAIL planted-py-missed: planted\[0\] passes all 4 hidden tests \(slip: Applies the bounds/, /1 failure/]);
run('--require, one planted solution is too few', ['--drill', 'planted-py-caught', '--require'], 1, [/FAIL planted-py-caught: 1 planted solution, --require wants at least two/]);
if (!noCpp) {
  run('C++, planted solution caught', ['--drill', 'planted-cpp-caught'], 0, [/1 drill checked, 1 planted solution, 0 skipped without any, 0 failures/]);
  run('C++, planted solution passes every test', ['--drill', 'planted-cpp-missed'], 1, [/FAIL planted-cpp-missed: planted\[0\] passes all 4 hidden tests/]);
}
run('a drill with no planted solutions is skipped', ['--drill', 'sample-clamp'], 0, [/0 drills checked, 0 planted solutions, 1 skipped without any, 0 failures/]);
fs.rmSync(tmp, { recursive: true, force: true });
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
