#!/usr/bin/env node
/* Scratch cases for the problem-set rules (ENGINE-BACKLOG 845 to 851; docs/AUTHORING.md section 5). Copies app/ to a temp folder, writes the fixture set
   (tools/fixtures/problems) into the copy's equations folder as problems-3.json (level 3 of that course), breaks one thing per case and expects the validator to
   report it (or, for the first case, nothing and a manifest entry). Nothing under app/content is touched. One PASS or FAIL line per case, exit 1 on a failure.
   Run from anywhere: node app/tools/test-validate-problems.mjs */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-problems-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const run = (...args) => { try { return { out: execFileSync('node', [path.join(copy, 'tools', 'validate.mjs'), ...args], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }), code: 0 }; } catch (e) { return { out: String(e.stdout || '') + String(e.stderr || ''), code: e.status || 1 }; } };
const fixture = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/problems/problems-fixture-3.json'), 'utf8'));
const dir = path.join(copy, 'content/courses/equations');
fs.rmSync(path.join(copy, 'tools/fixtures/problems'), { recursive: true, force: true });   // the copy holds only the case's set
const file = path.join(dir, 'problems-3.json');
const part = (d, i, k) => d.items[i].parts[k];
const cases = [
  ['ok-as-shipped', () => {}, null],
  ['a level without a problem set is not an error', null, 'none'],
  ['file-name-not-a-level-number', (d, f) => { fs.renameSync(f, path.join(dir, 'problems-x.json')); }, 'problems-<n>.json with n a level'],
  ['level-past-the-last', (d, f) => { d.id = 'problems-9'; d.level = 9; fs.renameSync(f, path.join(dir, 'problems-9.json')); }, 'n a level of the course'],
  ['id-does-not-match-the-file', (d) => { d.id = 'problems-2'; }, 'must match the file name'],
  ['level-field-wrong', (d) => { d.level = 2; }, 'level must be 3'],
  ['course-field-wrong', (d) => { d.course = 'functions'; }, 'course must be'],
  ['too-few-items', (d) => { d.items = d.items.slice(0, 2); }, '3 to 5 items'],
  ['too-many-items', (d) => { while (d.items.length < 6) { const c = JSON.parse(JSON.stringify(d.items[0])); c.id = 'x' + d.items.length; d.items.push(c); } }, '3 to 5 items'],
  ['an-item-without-parts', (d) => { const it = d.items[0]; d.items[0] = { id: it.id, difficulty: 3, skills: it.skills, question: 'q', widget: part(d, 0, 1).widget, feedback: part(d, 0, 1).feedback, explain: part(d, 0, 1).explain }; }, 'uses parts'],
  ['two-parts-only', (d) => { d.items[0].parts = d.items[0].parts.slice(0, 2); }, '3 to 5 parts'],
  ['six-parts', (d) => { while (d.items[0].parts.length < 6) d.items[0].parts.push(JSON.parse(JSON.stringify(d.items[0].parts[1]))); }, '3 to 5 parts (found 6)'],
  ['seven-parts', (d) => { while (d.items[0].parts.length < 7) d.items[0].parts.push(JSON.parse(JSON.stringify(d.items[0].parts[1]))); }, 'parts'],
  ['a-longform-part', (d) => { part(d, 0, 2).widget = { kind: 'longform', prompt: 'Explain.', model: 'x', rubric: [{ points: 10, text: 'x' }] }; }, 'cannot be longform'],
  ['a-code-part', (d) => { part(d, 0, 2).widget = { kind: 'code', language: 'python', starter: 'x', tests: [], solution: 'x' }; }, 'cannot be in a problem set'],
  ['difficulty-2', (d) => { d.items[0].difficulty = 2; }, 'difficulty'],
  ['no-difficulty-5', (d) => { d.items[2].difficulty = 4; }, 'at least one item at difficulty 5'],
  ['unknown-skill', (d) => { d.items[0].skills = ['eq-nothing']; }, 'unknown skill'],
  ['skill-from-another-level', (d) => { d.items[1].skills = ['eq-expressions']; }, "not taught in this level's lessons"],
  ['no-skills', (d) => { delete d.items[0].skills; }, 'name at least one skill'],
  ['timed-is-refused', (d) => { d.timed = { seconds: 600 }; }, 'untimed'],
  ['pass-is-refused', (d) => { d.pass = 0.8; }, 'no pass mark'],
  ['due-days-is-refused', (d) => { d.dueDays = 7; }, 'not a gate'],
  ['unknown-field', (d) => { d.extra = 1; }, 'unknown field "extra"'],
  ['minutes-not-a-number', (d) => { d.minutes = 'forty'; }, 'minutes is a whole number'],
  ['minutes-too-small', (d) => { d.minutes = 3; }, 'minutes is a whole number'],
  ['hints-on-an-item', (d) => { d.items[0].hints = ['x']; }, 'have no hints'],
  ['duplicate-item-id', (d) => { d.items[1].id = d.items[0].id; }, 'duplicate id'],
  ['part-without-feedback', (d) => { delete part(d, 1, 1).feedback; }, 'feedback'],
  ['part-wrong-equals-the-answer', (d) => { part(d, 0, 1).widget.wrong = [{ id: 'same', value: 4, tol: { abs: 0 } }]; }, 'wrong'],
  ['exclamation-in-prose', (d) => { d.items[0].prose = 'A plumber charges a fee!'; }, 'exclamation'],
  ['em-dash-in-an-explanation', (d) => { part(d, 0, 0).explain.text = 'The fee \u2014 paid once.'; }, 'em-dash'],
  ['warn-non-integer-numeric-without-a-form', (d) => { part(d, 0, 1).widget.answer = 4.5; part(d, 0, 1).question = 'How many hours are worked?'; }, 'warning:[answer-form]'],
  ['no-warning-when-the-form-is-stated', (d) => { part(d, 0, 1).widget.answer = 4.5; part(d, 0, 1).question = 'How many hours are worked, to 1 decimal place?'; }, 'nowarning:[answer-form]'],
  ['no-warning-form-a-decimal', (d) => { part(d, 0, 1).widget.answer = 4.5; part(d, 0, 1).question = 'How many hours are worked? Give a decimal.'; }, 'nowarning:[answer-form]'],
  ['no-warning-form-to-n-places', (d) => { part(d, 0, 1).widget.answer = 4.5; part(d, 0, 1).question = 'What is the rate? Answer to 4 places.'; }, 'nowarning:[answer-form]'],
  ['no-warning-form-exact-value', (d) => { part(d, 0, 1).widget.answer = 4.5; part(d, 0, 1).question = 'What is the mean? Give the exact value.'; }, 'nowarning:[answer-form]'],
  ['no-warning-form-as-a-fraction', (d) => { part(d, 0, 1).widget.answer = 4.5; part(d, 0, 1).question = 'What is the chance? Write it as a fraction.'; }, 'nowarning:[answer-form]'],
  ['no-warning-form-in-pounds', (d) => { part(d, 0, 1).widget.answer = 4.5; part(d, 0, 1).question = 'What is the fee? Give it in pounds.'; }, 'nowarning:[answer-form]'],
  ['no-warning-form-to-the-nearest', (d) => { part(d, 0, 1).widget.answer = 4.5; part(d, 0, 1).question = 'What is the price? Round to the nearest penny.'; }, 'nowarning:[answer-form]'],
  ['warn-when-only-exactly-appears', (d) => { part(d, 0, 1).widget.answer = 4.5; part(d, 0, 1).question = 'What is the chance of exactly 3 hits?'; }, 'warning:[answer-form]'],
  ['performance-item-is-refused', (d) => { d.items[0].performance = 'derivation'; }, 'performance belongs'],
];
let pass = 0, fail = 0;
for (const [name, mutate, has] of cases) {
  fs.rmSync(file, { force: true });
  ['problems-x.json', 'problems-9.json'].forEach((f) => fs.rmSync(path.join(dir, f), { force: true }));
  if (mutate) {
    const d = JSON.parse(JSON.stringify(fixture));
    d.id = 'problems-3';
    fs.writeFileSync(file, JSON.stringify(d, null, 2));
    mutate(d, file);
    const target = fs.existsSync(file) ? file : fs.existsSync(path.join(dir, 'problems-x.json')) ? path.join(dir, 'problems-x.json') : path.join(dir, 'problems-9.json');
    fs.writeFileSync(target, JSON.stringify(d, null, 2));
  }
  const r = run('--no-manifest');
  const isW = typeof has === 'string' && /^(no)?warning:/.test(has), want = isW ? has.replace(/^(no)?warning:/, '') : has;
  const errs = r.out.split('\n').filter((l) => (isW ? /^warning/.test(l) && /equations/.test(l) : /^error/.test(l)) && /problems/.test(l));
  let problem = null;
  if (isW && has.startsWith('no')) { if (errs.some((l) => l.includes(want))) problem = `unexpected warning: ${errs[0]}`; }
  else if (has === null || has === 'none') { if (r.code !== 0 || errs.length) problem = `expected no error, got ${errs.length}: ${errs[0] || r.out.slice(-300)}`; }
  else if (!errs.some((l) => l.includes(want))) problem = `no ${isW ? 'warning' : 'error'} contains "${want}" (got ${errs.length}: ${errs[0] || 'none'})`;
  if (!problem && has === null) {   // the manifest lists the set with the level, the item count and the minutes
    const m = run();
    const man = JSON.parse(fs.readFileSync(path.join(copy, 'content/manifest.json'), 'utf8'));
    const row = man.problems && man.problems['equations/problems-3'];
    if (m.code !== 0 || !row || row.level !== 3 || row.items !== fixture.items.length || row.minutes !== fixture.minutes || row.sample || !man.files.includes('courses/equations/problems-3.json')) problem = `manifest entry missing or wrong: ${JSON.stringify(row)}`;
  }
  if (!problem && has === 'none') {   // no file: no problems key in the manifest
    const m = run();
    const man = JSON.parse(fs.readFileSync(path.join(copy, 'content/manifest.json'), 'utf8'));
    if (m.code !== 0 || (man.problems && man.problems['equations/problems-3'])) problem = 'a course with no problem file should have no problems entry in the manifest';
  }
  if (problem) { console.log(`FAIL ${name}: ${problem}`); fail++; } else { console.log(`PASS ${name}`); pass++; }
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`test-validate-problems: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
