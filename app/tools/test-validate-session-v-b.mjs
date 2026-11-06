#!/usr/bin/env node
/* Scratch cases for the session V validator pass B (ENGINE-BACKLOG 600 series): 584 refinement, 585 default shuffle and exclusions,
   [shuffle-false], [float-example], [wrong-band], [float-artefact], [math-thousands-comma], and the schema fields required, tracks and form.
   Copies app/ to a temp folder and edits algo-think l1-counting-work (screens 2 and 3), first-python l8-many-values, exam topic-0.7 and mock-oa-strats.
   Run: node app/tools/test-validate-session-v-b.mjs. Exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-vb-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const run = () => { try { return { out: execFileSync('node', [path.join(copy, 'tools', 'validate.mjs'), '--no-manifest'], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 }), code: 0 }; } catch (e) { return { out: String(e.stdout || '') + String(e.stderr || ''), code: e.status || 1 }; } };
const files = {
  lesson: path.join(copy, 'content', 'courses', 'algo-think', 'l1-counting-work.json'),
  code: path.join(copy, 'content', 'courses', 'first-python', 'l8-many-values.json'),
  exam: path.join(copy, 'content', 'exams', 'topic-0.7.json'),
  mock: path.join(copy, 'content', 'exams', 'mock-oa-strats.json'),
};
const orig = Object.fromEntries(Object.entries(files).map(([k, f]) => [k, fs.readFileSync(f, 'utf8')]));
const reset = () => Object.entries(files).forEach(([k, f]) => fs.writeFileSync(f, orig[k]));
const edit = (k, fn) => { const j = JSON.parse(orig[k]); fn(j); fs.writeFileSync(files[k], JSON.stringify(j, null, 2) + '\n'); };
let fails = 0;
const say = (ok, name) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`); if (!ok) fails++; };
const has = (o, tag, file) => new RegExp(`${file}.*\\[${tag}\\]`).test(o);
const L = 'algo-think/l1-counting-work', CODE = 'first-python/l8-many-values';
const sec = (fn) => edit('lesson', (j) => fn(j.screens[2]));

say(run().code === 0, 'untouched copy: 0 errors');

/* 585: every choice shuffles unless shuffle is false */
sec((s) => { delete s.widget.shuffle; s.explain.text = 'The second option adds the steps, which is the count.'; });
say(has(run().out, 'shuffled-position', L), '585: no shuffle field and "the second option": warns (default shuffle)');
sec((s) => { s.widget.shuffle = false; s.explain.text = 'The second option adds the steps, which is the count.'; });
let r = run().out;
say(!has(r, 'shuffled-position', L), '585: shuffle: false and "the second option": no shuffled-position warning');
say(has(r, 'shuffle-false', L), 'shuffle: false on plain text options: [shuffle-false] warns');
sec((s) => { delete s.widget.shuffle; s.prose = 'Compare the second option in the table.'; s.explain.text = 'The second option adds the steps, which is the count.'; });
say(!has(run().out, 'shuffled-position', L), '585: the screen prose itself says "second option": excluded');
sec((s) => { delete s.widget.shuffle; s.noPosCheck = true; s.explain.text = 'The second option adds the steps, which is the count.'; });
say(!has(run().out, 'shuffled-position', L), '585: noPosCheck: true: excluded');

/* shuffle: false is allowed for ordered numbers and for options that refer to each other */
sec((s) => { s.widget.shuffle = false; s.widget.options.forEach((o, i) => { o.text = String(10 * (i + 1)); }); });
say(!has(run().out, 'shuffle-false', L), 'shuffle: false on ordered numbers: no warning');
sec((s) => { s.widget.shuffle = false; const d = s.widget.options.filter((o) => !o.correct); d[d.length - 1].text = 'Both of the above'; });
say(!has(run().out, 'shuffle-false', L), 'shuffle: false with "Both of the above": no warning');
sec((s) => { s.widget.shuffle = 'no'; });
r = run();
say(r.code !== 0 && new RegExp(`${L}.*shuffle is true or false`).test(r.out), 'shuffle that is not a boolean: error');

/* 584 refinement: a cell-id line beside a wrong-id line is deliberate */
const tab = (fn) => edit('lesson', (j) => fn(j.screens[3]));
const wr = (s) => { s.widget.rows[1][2].wrong = [{ id: 'cell-trap', value: 105, tol: { abs: 0 } }]; };
tab((s) => { wr(s); s.feedback.byKey.r1c2 = 'You counted n squared over two.'; });
say(has(run().out, 'table-slip-key', L), '584: cell-id line, no wrong-id line: warns');
tab((s) => { wr(s); s.feedback.byKey.r1c2 = 'Generic line for the cell.'; s.feedback.byKey['cell-trap'] = 'You counted n squared over two.'; });
say(!has(run().out, 'table-slip-key', L), '584: cell-id line beside a wrong-id line: no warning');

/* Numeric: wrong band narrower than the rounding asked, float artefact, thousands comma */
const num = (tol, extra = {}) => sec((s) => {
  s.question = 'What is the total, to 2 decimal places?';
  s.widget = { kind: 'numeric', answer: 15, tol: { abs: 0.005 }, wrong: [{ id: 'slip', value: 12.3456, tol }] };
  s.feedback = { correct: 'Yes.', generic: 'Not quite.', byKey: { slip: 'You forgot the fee.' } };
  Object.assign(s.explain, extra);
});
num({ abs: 0.0001 });
say(has(run().out, 'wrong-band', L), 'wrong value 12.3456 with band 0.0001 at 2 d.p.: [wrong-band] warns');
num({ abs: 0.006 });
say(!has(run().out, 'wrong-band', L), 'band 0.006 covers the rounding: no warning');
sec((s) => { s.widget = { kind: 'numeric', answer: 15, tol: { abs: 0.005 }, wrong: [{ id: 'slip', value: 12.35, tol: { abs: 0 } }] }; s.question = 'What is the total, to 2 decimal places?'; s.feedback = { correct: 'Yes.', generic: 'Not quite.', byKey: { slip: 'You forgot the fee.' } }; });
say(!has(run().out, 'wrong-band', L), 'wrong value already at 2 d.p.: no warning');
num({ abs: 0.006 }, { text: 'Python shows 0.1 + 0.2 as 0.30000000000000004 and 1.9999999 here.' });
say(has(run().out, 'float-artefact', L), 'explain with 0.30000000000000004: [float-artefact] warns');
num({ abs: 0.006 }, { text: 'It costs $10,000$ in total, and $1,2$ is a pair.' });
r = run().out;
say(has(r, 'math-thousands-comma', L) && /"10,000"/.test(r) && !/"1,2"/.test(r), 'comma in $10,000$: [math-thousands-comma] warns; a pair does not');
num({ abs: 0.006 }, { text: 'It costs $10{,}000$ in total, and the point $(1,000)$ is a pair.' });
say(!has(run().out, 'math-thousands-comma', L), '$10{,}000$ and a bracketed pair: no warning');
num({ abs: 0.006 }, { text: 'Python shows `0.30000000000000004` for the sum.' });
say(!has(run().out, 'float-artefact', L), 'artefact inside code: no warning');

/* float example without compare */
const ex = (compare) => edit('code', (j) => { j.screens.forEach((s) => { const w = s.widget; if (w && w.kind === 'code' && Array.isArray(w.examples)) w.examples.forEach((e) => { if (compare) e.compare = compare; else delete e.compare; }); }); });
ex(null);
say(has(run().out, 'float-example', CODE), 'float example with no compare: [float-example] warns');
ex('isclose');
say(!has(run().out, 'float-example', CODE), 'float example with compare isclose: no warning');
reset();

/* Schema: required, tracks, form */
edit('exam', (j) => { j.items[0].required = 'yes'; });
r = run();
say(r.code !== 0 && /topic-0\.7.*items\[0\]\.required.*true or false/.test(r.out), 'required: "yes" on an exam item: error');
edit('exam', (j) => { j.items[0].required = true; });
say(run().code === 0, 'required: true on an exam item: 0 errors');
const paperOf = (j) => (Array.isArray(j.parts) ? j.parts.find((p) => p.kind === 'paper') : j);
edit('mock', (j) => { paperOf(j).tracks = ['nonsense']; });
r = run();
say(r.code !== 0 && /mock-oa-strats.*tracks.*unknown role "nonsense"/.test(r.out), 'tracks naming an unknown role: error');
edit('mock', (j) => { paperOf(j).tracks = ['strats', 'researcher']; });
say(run().code === 0, 'tracks naming known roles (strats, researcher): 0 errors');
edit('lesson', (j) => { j.screens[2].widget = { kind: 'expression', answer: '2x', accept: ['2x'], form: 'diagonal' }; });
r = run();
say(r.code !== 0 && /widget\.form: form is/.test(r.out), 'expression form: "diagonal": error');
edit('lesson', (j) => { j.screens[2].widget = { kind: 'expression', answer: '3+4i', accept: ['3+4i'], form: 'rectangular' }; });
say(!/widget\.form: form is/.test(run().out), 'expression form: "rectangular": accepted');

fs.rmSync(tmp, { recursive: true, force: true });
console.log(fails ? `${fails} failed` : 'all passed');
process.exit(fails ? 1 : 0);
