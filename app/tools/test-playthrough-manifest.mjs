// Test for the playthrough's manifest check (engine pass 9, item f; ENGINE-BACKLOG 1161, 1164, 1166). Run from app/: node tools/test-playthrough-manifest.mjs
// Plays a temporary copy of app/ whose content/manifest.json lacks one problem set and one review (as after `git checkout content/manifest.json` before the validator has run):
// --problems and --set must stop at once with "Run the validator first", and name the set, before any browser starts. No browser or CDN is needed.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-manifest-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true });
const mp = path.join(copy, 'content/manifest.json'), man = JSON.parse(fs.readFileSync(mp, 'utf8'));
delete man.problems['ito/problems-3'];
man.files = man.files.filter((f) => f !== 'courses/ito/review-1.json');
fs.writeFileSync(mp, JSON.stringify(man));
const play = (...a) => { const r = spawnSync('node', [path.join(HERE, 'playthrough.mjs'), ...a], { env: { ...process.env, ZQ_APP_DIR: copy }, encoding: 'utf8', timeout: 60000 }); return { code: r.status, out: (r.stdout || '') + (r.stderr || '') }; };
const cases = [
  ['a problem set missing from the manifest', ['--problems', 'ito/problems-3'], /--problems ito\/problems-3: not listed in content\/manifest\.json/],
  ['a review missing from the manifest', ['--set', 'ito/review-1'], /--set ito\/review-1: not listed in content\/manifest\.json/],
];
let bad = 0;
for (const [name, args, re] of cases) {
  const { code, out } = play(...args);
  const ok = code !== 0 && re.test(out) && /Run the validator first/.test(out) && !/opened in state empty|has no Problem set row/.test(out);
  if (!ok) { bad++; console.log(`FAIL ${name} (exit ${code})\n${out.split('\n').slice(-6).join('\n')}`); } else console.log(`ok ${name}`);
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
