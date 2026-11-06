#!/usr/bin/env node
/* Scratch cases for the level-review pass rule (ENGINE-BACKLOG 574). Copies app/ to a temp folder, removes `pass` from one mapped level
   review and expects the validator to report it; the untouched copy must report none. Run: node app/tools/test-validate-review-pass.mjs.
   One PASS or FAIL line per case, exit 1 on a failure. The repo is never touched. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-pass-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const run = () => { try { return { out: execFileSync('node', [path.join(copy, 'tools', 'validate.mjs'), '--no-manifest'], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 }), code: 0 }; } catch (e) { return { out: String(e.stdout || '') + String(e.stderr || ''), code: e.status || 1 }; } };
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
