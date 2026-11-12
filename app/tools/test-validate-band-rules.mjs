#!/usr/bin/env node
/* Scratch cases for the answer-band and answer-form rules of engine pass AA 2 (ENGINE-BACKLOG 894, 898, 905, 907, 909, 910, 911; docs/AUTHORING.md section 5).
   Copies app/ to a temp folder, writes the problem-set fixture into the copy's equations folder as problems-3.json, plants one case in each part
   (all in one file, so the validator runs once), and reads the report by part. Nothing under app/content is touched.
     [tight-band]          the answer rounded as the question asks, a figure the part's own feedback or explanation prints, an unrounded answer with a half-unit band
     [wide-wrong-band]     a wrong band over half its own value
     [accept-form]         "any form equal to" something the numeric field cannot type
     [wrong-equals-answer] an expression wrong[].tex the grader reads as the answer (error); the written-text comparison always, the value comparison with --local-cdn
     [percent-form]        (ENGINE-BACKLOG 936) a question asking "in %" with no unit "%" and no percent-or-decimal slip
     [negative-key]        (938) a negative key with no wrong entry at its absolute value
     form "solved", domain and scale are accepted when well formed and refused when not
   Usage: node tools/test-validate-band-rules.mjs [--local-cdn <pkgs>]. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2), ci = argv.indexOf('--local-cdn');
const cdn = ci >= 0 ? path.resolve(argv[ci + 1]) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-band-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
fs.rmSync(path.join(copy, 'tools/fixtures/problems'), { recursive: true, force: true });
const fixture = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/problems/problems-fixture-3.json'), 'utf8'));
const file = path.join(copy, 'content/courses/equations/problems-3.json');
const run = (...a) => { try { return execFileSync('node', [path.join(copy, 'tools', 'validate.mjs'), '--no-manifest', ...a], { cwd: copy, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }); } catch (e) { return String(e.stdout || '') + String(e.stderr || ''); } };

const d = JSON.parse(JSON.stringify(fixture)); d.id = 'problems-3';
const num = (answer, tol, extra = {}) => ({ kind: 'numeric', answer, tol, ...extra });
const expr = (answer, extra = {}) => ({ kind: 'expression', answer, accept: [answer], ...extra });
/* [item, part, name, question, widget, feedback.correct, explain.text, expect] ; expect: a list of [kind, substring] where kind is warn, nowarn or error */
const OK_FB = '$x = 4$.', OK_EX = 'Work it through: $x = 4$.';
const CASES = [
  [0, 0, 'rounded-answer-outside-band', 'What is the ratio? Give a decimal to 2 places.', num(3.14159, { abs: 0.0001 }), OK_FB, OK_EX, [['warn', '[tight-band]'], ['warn', 'rounded as the question asks']]],
  [0, 1, 'rounded-answer-inside-band', 'What is the ratio? Give a decimal to 2 places.', num(3.14, { abs: 0.005 }), OK_FB, OK_EX, [['nowarn', '[tight-band]']]],
  [0, 2, 'unrounded-with-a-half-unit-band', 'What is the ratio? Give a decimal to 4 places.', num(0.1093754321, { abs: 0.00005 }), OK_FB, OK_EX, [['warn', '[tight-band]'], ['warn', 'one unit out']]],
  [0, 3, 'unrounded-with-a-unit-band', 'What is the ratio? Give a decimal to 4 places.', num(0.1093754321, { abs: 0.0001 }), OK_FB, OK_EX, [['nowarn', '[tight-band]']]],
  [0, 4, 'feedback-prints-a-figure-outside-the-band', 'What is the rate? Give a decimal to 2 places.', num(2.5278, { abs: 0.005 }), 'Check: $2.5278 \\approx 2.53$ per hour.', OK_EX, [['nowarn', '[tight-band]']]],
  [1, 0, 'explain-prints-a-figure-just-outside-the-band', 'What is the rate? Give a decimal to 4 places.', num(2.5278, { abs: 0.0005 }), OK_FB, 'The rate is $\\tfrac{91}{36} \\approx 2.53$.', [['warn', '[tight-band]'], ['warn', 'explain.text prints 2.53']]],
  [1, 1, 'feedback-prints-a-figure-just-outside-the-band', 'What is the total?', num(318, { abs: 0 }), 'So the total is $x = 317.9$.', OK_EX, [['warn', 'feedback.correct prints 317.9']]],
  [1, 2, 'a-far-figure-is-not-a-band-fault', 'What is the total?', num(318, { abs: 0 }), 'So the total is $79$.', OK_EX, [['nowarn', '[tight-band]']]],
  [1, 3, 'a-part-asked-in-units-is-skipped', 'What is the rate, in units of $10^{-5}$? Give 3 decimal places.', num(4.862, { abs: 0.0001 }), 'It is $\\approx 0.00004862$.', OK_EX, [['nowarn', '[tight-band]']]],
  [1, 4, 'a-percent-printed-with-its-sign', 'What is the chance? Give a percentage to 1 decimal place.', num(0.1587, { abs: 0.0005 }, { unit: '%' }), 'So $P = 15.9\\%$.', OK_EX, [['nowarn', 'prints']]],
  [2, 0, 'wide-wrong-band', 'What is the length?', num(10, { abs: 0 }, { wrong: [{ id: 'wide', value: 0.5236, tol: { abs: 0.5 } }] }), OK_FB, OK_EX, [['warn', '[wide-wrong-band]']]],
  [2, 1, 'narrow-wrong-band', 'What is the length?', num(10, { abs: 0 }, { wrong: [{ id: 'narrow', value: 5, tol: { abs: 1 } }] }), OK_FB, OK_EX, [['nowarn', '[wide-wrong-band]']]],
  [2, 2, 'accept-form-an-expression', 'What is the chance? Give a decimal to 4 places.', num(0.2025, { abs: 0.0005 }, { accept: 'Any form equal to $0.45^2$, or 0.2025 ± 0.0005' }), OK_FB, OK_EX, [['warn', '[accept-form]']]],
  [2, 3, 'accept-form-a-fraction', 'What is the chance? Give a decimal to 4 places.', num(0.5, { abs: 0.0005 }, { accept: 'Any form equal to $\\tfrac{1}{2}$, or 0.5 ± 0.0005' }), OK_FB, OK_EX, [['nowarn', '[accept-form]']]],
  [2, 4, 'accept-form-a-word', 'What is the chance? Give a decimal to 4 places.', num(0.5, { abs: 0.0005 }, { accept: '0.5, or any form equal to it.' }), OK_FB, OK_EX, [['nowarn', '[accept-form]']]],
  [3, 0, 'wrong-equals-the-answer-by-text', 'Write the rule.', expr('2x+1', { wrong: [{ id: 'same', tex: '2 x + 1' }] }), OK_FB, OK_EX, [['error', '[wrong-equals-answer]']]],
  [3, 1, 'wrong-differs-from-the-answer', 'Write the rule.', expr('2x+1', { wrong: [{ id: 'other', tex: '2x+2' }] }), OK_FB, OK_EX, [['nowarn', '[wrong-equals-answer]']]],
  [3, 2, 'form-solved-is-allowed', 'Solve for h.', expr('h\\le10', { form: 'solved', wrong: [{ id: 'flip', tex: 'h\\ge10' }] }), OK_FB, OK_EX, [['nowarn', 'form is']]],
  [3, 3, 'form-unknown-is-refused', 'Solve for h.', expr('h\\le10', { form: 'tidy' }), OK_FB, OK_EX, [['error', '.form']]],
  [3, 4, 'domain-and-scale-well-formed', 'Write the rule.', expr('\\arcsin(s)', { domain: { s: [0.05, 0.9] } }), OK_FB, OK_EX, [['nowarn', 'domain']]],
  [4, 0, 'domain-malformed', 'Write the rule.', expr('\\arcsin(s)', { domain: { s: [0.9, 0.05] } }), OK_FB, OK_EX, [['error', 'domain.s']]],
  [4, 1, 'scale-malformed', 'What is the rate, in units of $10^{-5}$?', num(4.86, { abs: 0.005 }, { scale: -1 }), OK_FB, OK_EX, [['error', '.scale']]],
  [4, 2, 'scale-well-formed', 'What is the rate, in units of $10^{-5}$?', num(4.86, { abs: 0.005 }, { scale: 1e-5 }), OK_FB, OK_EX, [['nowarn', '.scale']]],
  [5, 0, 'percent-asked-with-no-unit-and-no-slip', 'What is the return, in %?', num(5.4, { abs: 0.05 }), OK_FB, OK_EX, [['warn', '[percent-form]']]],
  [5, 1, 'percent-asked-with-unit-percent', 'Give the return as a percentage.', num(0.054, { abs: 0.0005 }, { unit: '%' }), OK_FB, OK_EX, [['nowarn', '[percent-form]']]],
  [5, 2, 'percent-asked-with-the-decimal-slip', 'What is the return, in per cent? Give 1 decimal place.', num(5.4, { abs: 0.05 }, { wrong: [{ id: 'decimal', value: 0.054, tol: { abs: 0.0005 } }] }), OK_FB, OK_EX, [['nowarn', '[percent-form]']]],
  [5, 3, 'negative-key-with-no-absolute-value-slip', 'What is the change?', num(-12, { abs: 0 }, { wrong: [{ id: 'other', value: 7, tol: { abs: 0 } }] }), OK_FB, OK_EX, [['warn', '[negative-key]']]],
  [5, 4, 'negative-key-with-its-absolute-value', 'What is the change?', num(-12, { abs: 0 }, { wrong: [{ id: 'sign', value: 12, tol: { abs: 0 } }] }), OK_FB, OK_EX, [['nowarn', '[negative-key]']]],
  [6, 0, 'a-positive-key-asked-in-units', 'What is the length, in metres?', num(12, { abs: 0 }), OK_FB, OK_EX, [['nowarn', '[percent-form]'], ['nowarn', '[negative-key]']]],
  [6, 1, 'tie-slip-with-a-narrow-band', 'What is the total? Give 2 decimal places.', num(10, { abs: 0.005 }, { wrong: [{ id: 'tie', value: 8.645, tol: { abs: 0.0049 } }] }), OK_FB, OK_EX, [['warn', '[wrong-band]']]],
  [6, 2, 'tie-slip-with-the-default-band', 'What is the total? Give 2 decimal places.', num(10, { abs: 0.005 }, { wrong: [{ id: 'tie', value: 8.645 }] }), OK_FB, OK_EX, [['warn', '[wrong-band]']]],
  [6, 3, 'tie-slip-with-a-half-unit-band', 'What is the total? Give a decimal to 2 places.', num(10, { abs: 0.005 }, { wrong: [{ id: 'tie', value: 8.645, tol: { abs: 0.005 } }] }), OK_FB, OK_EX, [['nowarn', '[wrong-band]']]],
  [6, 4, 'tie-key-with-a-narrow-band', 'What is the total? Give a decimal to 2 places.', num(8.645, { abs: 0.004 }), OK_FB, OK_EX, [['warn', '[tight-band]']]],
];
const items = [...new Set(CASES.map((c) => c[0]))];
while (d.items.length < items.length) d.items.push(JSON.parse(JSON.stringify(d.items[0])));
d.items.forEach((it, i) => { it.id = 'p-case-' + i; it.parts = it.parts.slice(0, 5); while (it.parts.length < 5) it.parts.push(JSON.parse(JSON.stringify(it.parts[0]))); });
for (const [i, k, , question, widget, correct, explain] of CASES) {
  const p = d.items[i].parts[k];
  p.question = question; p.widget = widget; p.feedback = { correct, generic: 'Not quite. Check the step again.', byKey: {} }; p.explain = { text: explain };
}
d.items.length = items.length;
let pass = 0, fail = 0;
const grade = (out, label) => {
  const lines = out.split('\n').filter((l) => /^(error|warning)/.test(l) && /equations\/problems-3/.test(l));
  for (const [i, k, name, , , , , expect] of CASES) {
    const mine = lines.filter((l) => l.includes(`items[${i}].parts[${k}]`));
    for (const [kind, sub] of expect) {
      const hit = mine.some((l) => l.includes(sub) && (kind === 'error' ? /^error/.test(l) : /^warning/.test(l) || kind === 'nowarn'));
      const bad = kind === 'nowarn' ? mine.some((l) => l.includes(sub)) : !hit;
      if (bad) { console.log(`FAIL ${label} ${name}: ${kind} "${sub}" (lines: ${mine.map((l) => l.slice(0, 200)).join(' | ') || 'none'})`); fail++; } else { console.log(`PASS ${label} ${name}: ${kind} "${sub}"`); pass++; }
    }
  }
};
fs.writeFileSync(file, JSON.stringify(d, null, 2));
const out = run();
grade(out, 'text');
if (!/0 errors|^error/m.test(out) && false) { /* errors are expected for the malformed cases */ }
/* the value comparison: wrong[].tex written differently but equal to the answer */
if (cdn && fs.existsSync(cdn)) {
  const e = JSON.parse(fs.readFileSync(file, 'utf8'));
  e.items[3].parts[1].widget = expr('2x+1', { wrong: [{ id: 'equal-by-value', tex: '1+x+x' }] });
  fs.writeFileSync(file, JSON.stringify(e, null, 2));
  const withCdn = run('--local-cdn', cdn), without = run();
  const has = (o) => o.split('\n').some((l) => /^error/.test(l) && l.includes('items[3].parts[1]') && l.includes('[wrong-equals-answer]'));
  if (has(withCdn) && !has(without)) { console.log('PASS value comparison: 1+x+x is found equal to 2x+1 with --local-cdn, not without'); pass++; } else { console.log(`FAIL value comparison: with cdn ${has(withCdn)}, without ${has(without)}`); fail++; }
} else console.log('SKIP value comparison (give --local-cdn <pkgs>)');
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`test-validate-band-rules: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
