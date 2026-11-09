// Test for the playthrough's display-overflow check (ENGINE-BACKLOG 701). Run from app/: node tools/test-playthrough-overflow.mjs [--local-cdn <pkgs>]
// Plays a temporary copy of app/ whose ito/homework-2 is tools/fixtures/overflow/homework-2.json: one longform with an over-wide
// model display (must fail with the line below, desktop and --mobile) and one clean longform (must not be named).
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-overflow-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true });
fs.copyFileSync(path.join(HERE, 'fixtures/overflow/homework-2.json'), path.join(copy, 'content/courses/ito/homework-2.json'));
const extra = process.argv.slice(2);
let bad = 0;
for (const mobile of [false, true]) {
  const r = spawnSync('node', [path.join(HERE, 'playthrough.mjs'), '--set', 'ito/homework-2', ...(mobile ? ['--mobile'] : []), ...extra], { env: { ...process.env, ZQ_APP_DIR: copy }, encoding: 'utf8', timeout: 600000 });
  const out = (r.stdout || '') + (r.stderr || ''), tag = mobile ? 'mobile' : 'desktop';
  const wide = out.match(/ito\/homework-2#fx-wide: display wider than its column at (\d+)px: x_0\+x_1\+x_2/g) || [];
  const widths = wide.map((l) => +l.match(/at (\d+)px/)[1]);
  const okWide = mobile ? widths.includes(440) : widths.includes(1280);
  const okClean = !/#fx-clean: display wider/.test(out);
  if (!okWide || !okClean) { bad++; console.log(`FAIL ${tag}: wide flagged ${JSON.stringify(widths)}, clean unflagged ${okClean}\n${out.split('\n').slice(-12).join('\n')}`); }
  else console.log(`ok ${tag}: over-wide display flagged at ${[...new Set(widths)].join(', ')}px, clean item passes`);
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
