#!/usr/bin/env node
/* Scratch cases for ENGINE-BACKLOG 576: a table cell's own wrong: [{ id, value }] id is a valid feedback.byKey key (table.js returns it),
   and an unknown key is still refused. Copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs) and edits one table screen of algo-think l1-counting-work.
   Run: node app/tools/test-validate-table-wrong.mjs. One PASS or FAIL line per case, exit 1 on a failure. The repo is never touched. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'tw', fixtures: [] });   // a scratch copy of tools/fixtures/mini-app (see lib/validate-harness.mjs)
const tmp = h.dir;
const copy = h.dir;
const run = () => h.validate();
const f = path.join(copy, 'content', 'courses', 'algo-think', 'l1-counting-work.json');
const orig = fs.readFileSync(f, 'utf8');
let fails = 0;
const say = (ok, name) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`); if (!ok) fails++; };
const edit = (fn) => { const j = JSON.parse(orig); fn(j.screens[3]); fs.writeFileSync(f, JSON.stringify(j, null, 2) + '\n'); };
const wrong = (s) => { s.widget.rows[1][2].wrong = [{ id: 'cell-trap', value: 105, tol: { abs: 0 } }]; };
say(run().code === 0, 'untouched copy: 0 errors');
edit((s) => { wrong(s); s.feedback.byKey['cell-trap'] = 'You counted n squared over two.'; });
const a = run();
say(a.code === 0 && !/cannot return the key/.test(a.out), 'cell wrong id as byKey key: accepted');
edit((s) => { wrong(s); s.feedback.byKey['not-a-key'] = 'You counted n squared over two.'; });
const b = run();
say(b.code === 1 && /cannot return the key "not-a-key"/.test(b.out), 'unknown byKey key: still refused');
fs.rmSync(tmp, { recursive: true, force: true });
process.exit(fails ? 1 : 0);
