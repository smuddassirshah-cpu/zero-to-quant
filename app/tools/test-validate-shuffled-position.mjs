#!/usr/bin/env node
/* Scratch cases for ENGINE-BACKLOG 585: [shuffled-position], [key-length] and [multi-keys-uniform].
   Copies app/ to a temp folder and edits algo-think l1-counting-work (screen 2, a choice) and exam topic-0.7.
   Run: node app/tools/test-validate-shuffled-position.mjs. Exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-sp-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const run = () => { try { return { out: execFileSync('node', [path.join(copy, 'tools', 'validate.mjs'), '--no-manifest'], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 }), code: 0 }; } catch (e) { return { out: String(e.stdout || '') + String(e.stderr || ''), code: e.status || 1 }; } };
const lf = path.join(copy, 'content', 'courses', 'algo-think', 'l1-counting-work.json');
const ef = path.join(copy, 'content', 'exams', 'topic-0.7.json');
const lorig = fs.readFileSync(lf, 'utf8'), eorig = fs.readFileSync(ef, 'utf8');
let fails = 0;
const say = (ok, name) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`); if (!ok) fails++; };
const edit = (fn) => { const j = JSON.parse(lorig); fn(j.screens[2]); fs.writeFileSync(lf, JSON.stringify(j, null, 2) + '\n'); };
const editExam = (fn) => { const j = JSON.parse(eorig); fn(j); fs.writeFileSync(ef, JSON.stringify(j, null, 2) + '\n'); };
const has = (o, tag, file) => new RegExp(`${file}.*\\[${tag}\\]`).test(o);
const L = 'algo-think/l1-counting-work', E = 'topic-0\\.7';

say(run().code === 0, 'untouched copy: 0 errors');
edit((s) => { s.widget.shuffle = true; s.explain.text = 'The second option adds the steps, which is the count.'; });
say(has(run().out, 'shuffled-position', L), 'shuffle with "the second option" in explain: warns');
edit((s) => { s.widget.shuffle = true; s.feedback.generic = 'Not quite. Check the last answer against the table.'; });
say(has(run().out, 'shuffled-position', L), 'shuffle with "the last answer" in feedback: warns');
edit((s) => { s.widget.shuffle = true; s.widget.options.find((o) => !o.correct).why = 'Option B counts the steps twice.'; });
say(has(run().out, 'shuffled-position', L), 'shuffle with "Option B" in a why: warns');
edit((s) => { s.widget.shuffle = true; s.explain.text = 'The first map shows the count. Each step adds one.'; });
say(!has(run().out, 'shuffled-position', L), 'shuffle with "the first map": no warning');
edit((s) => { s.explain.text = 'The second option adds the steps, which is the count.'; });
say(!has(run().out, 'shuffled-position', L), 'no shuffle with "the second option": no warning');

const long = 'The count is the sum of all the steps taken';
edit((s) => { s.widget.options.forEach((o) => { o.text = o.correct ? long : 'Twice the steps'; }); });
say(has(run().out, 'key-length', L), 'key over 1.5 times every distractor: key-length warns');
edit((s) => { s.widget.options.forEach((o, i) => { o.text = o.correct ? long : (i === 0 ? 'Twice the steps taken now' : 'The sum of all the step counts'); }); });
say(!has(run().out, 'key-length', L), 'one distractor near the key length: no key-length warning');
edit((s) => { s.widget.options.forEach((o) => { o.text = o.correct ? 'Sum of all' : 'N'; }); });
say(!has(run().out, 'key-length', L), 'key under 12 characters: no key-length warning');
fs.writeFileSync(lf, lorig);

/* topic-0.7 already holds several multis; set every one to the same (or a varied) number of keys */
const setMulti = (pick) => editExam((j) => { let n = 0; j.items.forEach((it) => { if (it.widget && it.widget.kind === 'multi') { const c = pick(n++); it.widget.options.forEach((o, k) => { o.correct = k < c; }); } }); return n; });
setMulti(() => 2);
say(has(run().out, 'multi-keys-uniform', E), 'every multi has two keys: multi-keys-uniform warns');
setMulti((n) => (n === 0 ? 1 : 2));
say(!has(run().out, 'multi-keys-uniform', E), 'key counts differ: no warning');
editExam((j) => { let n = 0; j.items.forEach((it) => { if (it.widget && it.widget.kind === 'multi' && n++ >= 3) it.widget = { kind: 'numeric', answer: 1, tol: { abs: 0 } }; }); });
say(!has(run().out, 'multi-keys-uniform', E), 'three multis: no warning');

fs.rmSync(tmp, { recursive: true, force: true });
process.exit(fails ? 1 : 0);
