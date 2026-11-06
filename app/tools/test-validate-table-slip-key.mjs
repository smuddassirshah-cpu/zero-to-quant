#!/usr/bin/env node
/* Scratch cases for ENGINE-BACKLOG 584: a table byKey key equal to an editable cell id warns ([table-slip-key]) when that cell has wrong[] entries.
   Copies app/ to a temp folder and edits one table screen of algo-think l1-counting-work. Run: node app/tools/test-validate-table-slip-key.mjs. Exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-tsk-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const run = () => { try { return { out: execFileSync('node', [path.join(copy, 'tools', 'validate.mjs'), '--no-manifest'], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 }), code: 0 }; } catch (e) { return { out: String(e.stdout || '') + String(e.stderr || ''), code: e.status || 1 }; } };
const f = path.join(copy, 'content', 'courses', 'algo-think', 'l1-counting-work.json');
const orig = fs.readFileSync(f, 'utf8');
let fails = 0;
const say = (ok, name) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`); if (!ok) fails++; };
const edit = (fn) => { const j = JSON.parse(orig); fn(j.screens[3]); fs.writeFileSync(f, JSON.stringify(j, null, 2) + '\n'); };
const wrong = (s) => { s.widget.rows[1][2].wrong = [{ id: 'cell-trap', value: 105, tol: { abs: 0 } }]; };
const hit = (o) => /algo-think.*\[table-slip-key\] key "r1c2"/.test(o);
say(run().code === 0, 'untouched copy: 0 errors');
edit((s) => { wrong(s); s.feedback.byKey.r1c2 = 'You counted n squared over two.'; });
const a = run();
say(a.code === 0 && hit(a.out) && /"cell-trap"/.test(a.out), 'cell-id key on a cell with wrong[]: warns, names the wrong id');
edit((s) => { wrong(s); delete s.feedback.byKey.r1c2; s.feedback.byKey['cell-trap'] = 'You counted n squared over two.'; });
say(!/algo-think.*table-slip-key/.test(run().out), 'wrong-id key: no warning');
edit((s) => { s.feedback.byKey.r1c2 = 'You counted n squared over two.'; });
say(!/algo-think.*table-slip-key/.test(run().out), 'cell-id key on a cell with no wrong[]: no warning');
fs.rmSync(tmp, { recursive: true, force: true });
process.exit(fails ? 1 : 0);
