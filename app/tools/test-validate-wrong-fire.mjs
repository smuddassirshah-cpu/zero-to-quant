#!/usr/bin/env node
/* Scratch cases for ENGINE-BACKLOG 581: a numeric or table-cell wrong[] value that cannot fire. Fires when the wrong value (or its own tol)
   reaches the answer's tolerance, and warns when two wrong entries overlap. Edits one table screen of algo-think l1-counting-work in a temp copy.
   Run: node app/tools/test-validate-wrong-fire.mjs. One PASS or FAIL line per case, exit 1 on a failure. The repo is never touched. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-wf-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const run = () => { try { return execFileSync('node', [path.join(copy, 'tools', 'validate.mjs'), '--no-manifest'], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 }); } catch (e) { return String(e.stdout || '') + String(e.stderr || ''); } };
const f = path.join(copy, 'content', 'courses', 'algo-think', 'l1-counting-work.json');
const orig = fs.readFileSync(f, 'utf8');
let fails = 0;
const say = (ok, name) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`); if (!ok) fails++; };
const edit = (wrong) => { const j = JSON.parse(orig); const s = j.screens[3]; s.widget.rows[1][2].wrong = wrong; for (const w of wrong) s.feedback.byKey[w.id] = 'You counted n squared over two.'; fs.writeFileSync(f, JSON.stringify(j, null, 2) + '\n'); };
const hit = (out, id) => out.split('\n').some(l => /l1-counting-work/.test(l) && l.includes(`"${id}"`) && /can never fire|overlaps/.test(l));
/* the cell's answer is 120 with tol abs 0 */
edit([{ id: 'clean', value: 105, tol: { abs: 0 } }]);
say(!hit(run(), 'clean'), 'clean wrong value: no finding');
edit([{ id: 'same', value: 120, tol: { abs: 0 } }]);
say(hit(run(), 'same'), 'wrong value equal to the answer: finding');
edit([{ id: 'wide', value: 118, tol: { abs: 2 } }]);
say(hit(run(), 'wide'), 'wrong tolerance reaching the answer: finding');
edit([{ id: 'first', value: 105, tol: { abs: 3 } }, { id: 'second', value: 107, tol: { abs: 3 } }]);
say(hit(run(), 'second'), 'two overlapping wrong entries: finding');
edit([{ id: 'first', value: 105, tol: { abs: 1 } }, { id: 'second', value: 110, tol: { abs: 1 } }]);
const o = run();
say(!hit(o, 'first') && !hit(o, 'second'), 'two separate wrong entries: no finding');
fs.rmSync(tmp, { recursive: true, force: true });
process.exit(fails ? 1 : 0);
