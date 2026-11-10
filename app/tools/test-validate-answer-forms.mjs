#!/usr/bin/env node
/* Scratch cases for ENGINE-BACKLOG 830 to 832 in the content validator: the expression forms "factorised-fully" and
   "completed-square", and set answers (answers + unordered) for numeric and expression widgets. Replaces the widget of one numeric
   screen of algo-think l11-sorting-by-hand in a temp copy (nothing under app/content is touched), breaks one thing per case and
   expects the validator to report it (or, for the first cases, nothing about that screen).
   Run: node app/tools/test-validate-answer-forms.mjs. One PASS or FAIL line per case, exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-af-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const run = () => { try { return execFileSync('node', [path.join(copy, 'tools', 'validate.mjs'), '--no-manifest'], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 }); } catch (e) { return String(e.stdout || '') + String(e.stderr || ''); } };
const f = path.join(copy, 'content', 'courses', 'algo-think', 'l11-sorting-by-hand.json');
const orig = fs.readFileSync(f, 'utf8');
let fails = 0;
const say = (ok, name, detail = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails++; };
const lines = (out) => out.split('\n').filter((l) => /^(error|warning)/.test(l) && /l11-sorting-by-hand/.test(l) && /items?\[|screens\[4\]|widget/.test(l) && /screens\[4\]/.test(l));
const put = (widget, byKey = {}) => {
  const j = JSON.parse(orig); const s = j.screens[4];
  s.widget = widget; s.feedback = { ...(s.feedback || {}), byKey: { ...byKey } };
  fs.writeFileSync(f, JSON.stringify(j, null, 1));
};
const errs = (out) => lines(out).filter((l) => l.startsWith('error'));
const has = (out, re) => errs(out).some((l) => re.test(l));

const num = (over = {}) => ({ kind: 'numeric', answers: [-3, 5], unordered: true, tol: { abs: 0 }, wrong: [{ id: 'signs', value: '3, -5' }], ...over });
const exp = (over = {}) => ({ kind: 'expression', answers: ['3+\\sqrt{5}', '3-\\sqrt{5}'], unordered: true, wrong: [{ id: 'centre', tex: '-3+\\sqrt{5}, -3-\\sqrt{5}' }], ...over });
const bk = { signs: 'You changed both signs.', centre: 'The centre has the wrong sign.', count: 'Give both roots.' };

put(num(), { signs: bk.signs, count: bk.count }); let out = run();
say(errs(out).length === 0, 'a numeric set with a wrong set: no error', errs(out).join(' | '));
put(exp(), { centre: bk.centre, count: bk.count }); out = run();
say(errs(out).length === 0, 'an expression set with a wrong set: no error', errs(out).join(' | '));
put(num({ answers: [-3] }), bk); say(has(run(), /answers is a list of two or more numbers/), 'numeric: one answer is not a set');
put(num({ answers: ['-3', '5'] }), bk); say(has(run(), /answers is a list of two or more numbers/), 'numeric: answers are numbers, not text');
put(num({ unordered: false }), bk); say(has(run(), /unordered must be true/), 'numeric: unordered must be true');
{ const w = num(); delete w.unordered; put(w, bk); say(has(run(), /unordered must be true/), 'numeric: answers without unordered'); }
put(num({ answer: 5 }), bk); say(has(run(), /answers \(a set\) or answer, not both/), 'numeric: answers and answer together');
put(num({ unit: '%' }), bk); say(has(run(), /unit "%" is not used with answers/), 'numeric: no per cent unit with a set');
put(num({ wrong: [{ id: 'signs', value: -3 }] }), bk); say(has(run(), /wrong value of a set is text of two or more numbers/), 'numeric: a wrong set given as a single number');
put(num({ wrong: [{ id: 'signs', value: 'two, five' }] }), bk); say(has(run(), /wrong value of a set is text of two or more numbers/), 'numeric: a wrong set that is not numbers');
put(num({ wrong: [{ id: 'same', value: '5, -3' }] }), { same: 'x' }); say(has(run(), /grades correct and never fires/), 'numeric: a wrong set equal to the answer in another order');
put(num({ tol: { abs: 0.5 }, wrong: [{ id: 'near', value: '-3.2, 5.1' }] }), { near: 'x' }); say(has(run(), /grades correct and never fires/), 'numeric: a wrong set inside the tolerance');
{ const w = num(); delete w.tol; put(w, bk); say(has(run(), /tol must be/), 'numeric: a set still needs tol'); }
put(exp({ answers: ['3'] }), bk); say(has(run(), /answers is a list of two or more TeX strings/), 'expression: one answer is not a set');
put(exp({ unordered: 'yes' }), bk); say(has(run(), /unordered must be true/), 'expression: unordered must be true');
put(exp({ answer: '3' }), bk); say(has(run(), /answers \(a set\) or answer, not both/), 'expression: answers and answer together');
put(exp({ accept: ['3+sqrt(5)'] }), bk); say(has(run(), /accept is not used with answers/), 'expression: accept is not used with a set');
put(exp({ form: 'simplified' }), bk); say(has(run(), /form is not used with answers/), 'expression: form is not used with a set');
put(exp({ wrong: [{ id: 'centre', tex: '3' }] }), bk); say(has(run(), /wrong value of a set is TeX with the values separated by commas/), 'expression: a wrong set with no comma');
/* the key count can be given a line, and the forms are accepted */
put(num(), { ...bk, count: 'Give both roots.' }); out = run();
say(!lines(out).some((l) => /unknown key|byKey/.test(l) && /count/.test(l)), 'a byKey line named count is a key the widget can produce', lines(out).join(' | '));
put({ kind: 'expression', answer: '2(x+2)(x+3)', accept: ['2(x+2)(x+3)'], form: 'factorised-fully', wrong: [] }, { form: 'Take out the common factor.' }); out = run();
say(errs(out).length === 0, 'form factorised-fully is accepted, and form is a key', errs(out).join(' | '));
put({ kind: 'expression', answer: '(x+3)^2-4', accept: ['(x+3)^2-4'], form: 'completed-square', wrong: [] }, { form: 'Write it as a square.' }); out = run();
say(errs(out).length === 0, 'form completed-square is accepted', errs(out).join(' | '));
put({ kind: 'expression', answer: '(x+3)^2-4', accept: ['(x+3)^2-4'], form: 'completed-squares', wrong: [] }); say(has(run(), /form is "expanded"/), 'an unknown form names the full list, including the two new ones');
put({ kind: 'expression', answer: '(x+3)^2-4', accept: ['(x+3)^2-4'], form: 'completed-squares', wrong: [] }); out = run();
say(has(out, /factorised-fully/) && has(out, /completed-square/), 'the form message lists factorised-fully and completed-square');
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`test-validate-answer-forms: ${fails ? fails + ' FAILED' : 'all passed'}`);
process.exit(fails ? 1 : 0);
