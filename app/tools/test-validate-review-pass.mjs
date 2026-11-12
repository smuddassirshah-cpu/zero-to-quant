#!/usr/bin/env node
/* Scratch cases for the level-review pass rule (ENGINE-BACKLOG 574). Copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs), removes `pass` from one mapped level
   review and expects the validator to report it; the untouched copy must report none. Run: node app/tools/test-validate-review-pass.mjs.
   One PASS or FAIL line per case, exit 1 on a failure. The repo is never touched. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'pass', fixtures: [] });   // a scratch copy of tools/fixtures/mini-app (see lib/validate-harness.mjs)
const tmp = h.dir;
const copy = h.dir;
const run = () => h.validate();
const f = path.join(copy, 'content', 'courses', 'odes', 'review-1.json');
const doc = JSON.parse(fs.readFileSync(f, 'utf8'));
let fails = 0;
const say = (ok, name) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`); if (!ok) fails++; };
const base = run();
say(base.code === 0 && !/needs a pass share/.test(base.out), 'review with pass: no error');
delete doc.pass;
fs.writeFileSync(f, JSON.stringify(doc, null, 2) + '\n');
const r = run();
say(r.code === 1 && /error .*odes\/review-1\.json.*needs a pass share/.test(r.out), 'review without pass: error');
fs.rmSync(tmp, { recursive: true, force: true });
process.exit(fails ? 1 : 0);
