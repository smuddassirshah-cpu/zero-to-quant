#!/usr/bin/env node
/* Scratch cases for the problem-set rules of engine pass 8 part A (ENGINE-BACKLOG 1082 to 1146; docs/AUTHORING.md section 5), pattern of test-validate-band-rules.mjs.
   Copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs), writes the problem-set fixture into the copy's equations folder as problems-3.json, plants one case in each part
   and reads the report by part. Nothing under app/content is touched.
     [working-band]    the final figure the part's own working prints lies outside the key's band
     [rounding-tie]    a key or slip on an exact rounding tie with a band that takes neither rounding; a printed tie with a key that takes one
     [table-source]    a tail area, quantile or table value in the working with no value or source in the stem or question
     [percent-unit]    (error) a percentage asked with no unit "%"
     [wide-wrong-tol]  a wrong band wider than its own value
     [wrong-band]      no longer fires for a slip that rounds to 0 at the asked places (session AF ruling)
     [escaped-apostrophe]  a literal backslash before an apostrophe in learner prose
   Usage: node tools/test-validate-pass8.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'pass8', fixtures: ['problems'] });
const copy = h.dir;
fs.rmSync(path.join(copy, 'tools/fixtures/problems'), { recursive: true, force: true });
const fixture = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/problems/problems-fixture-3.json'), 'utf8'));
const file = path.join(copy, 'content/courses/equations/problems-3.json');
const d = JSON.parse(JSON.stringify(fixture)); d.id = 'problems-3';
const num = (answer, tol, extra = {}) => ({ kind: 'numeric', answer, tol, ...extra });
const OK_FB = 'The working gives the answer.', OK_EX = 'Work it through step by step.';
/* [item, part, name, question, widget, feedback.correct, explain.text, expect, (optional) item prose] ; expect: [kind, substring] with kind warn, nowarn or error */
const CASES = [
  /* working-band */
  [0, 0, 'working-ends-outside-the-band', 'What is the ratio? Give a decimal to 3 places.', num(1.476, { abs: 0.0005 }), 'So the ratio is $x = 1.44$.', OK_EX, [['warn', '[working-band]']]],
  [0, 1, 'working-ends-inside-the-band', 'What is the ratio? Give a decimal to 3 places.', num(1.476, { abs: 0.0005 }), 'So the ratio is $x = 1.476$.', OK_EX, [['nowarn', '[working-band]']]],
  [0, 2, 'explain-ends-outside-the-band', 'What is the ratio? Give a decimal to 3 places.', num(1.476, { abs: 0.0005 }), OK_FB, 'Divide through: $x \\approx 1.44$.', [['warn', '[working-band]'], ['warn', 'explain.text']]],
  [0, 3, 'working-prints-a-slip-value', 'What is the ratio? Give a decimal to 3 places.', num(1.476, { abs: 0.0005 }, { wrong: [{ id: 'slip', value: 1.44, tol: { abs: 0.0005 } }] }), 'You get $x = 1.44$ if you stop early; the answer is 1.476.', OK_EX, [['nowarn', '[working-band]']]],
  [0, 4, 'a-number-follows-the-last-span', 'What is the ratio? Give a decimal to 3 places.', num(1.476, { abs: 0.0005 }), 'The step gives $x = 1.44$, then 7 more lines follow.', OK_EX, [['nowarn', '[working-band]']]],
  [1, 0, 'working-ends-in-more-steps', 'What is the ratio? Give a decimal to 3 places.', num(1.476, { abs: 0.0005 }), 'So $x = 1.44 \\times 2$.', OK_EX, [['nowarn', '[working-band]']]],
  [1, 1, 'working-rounds-in-the-band-at-the-asked-places', 'What is the ratio? Give a decimal to 2 places.', num(1.476, { abs: 0.005 }), 'So $x = 1.4761$.', OK_EX, [['nowarn', '[working-band]']]],
  [1, 2, 'working-in-per-cent-outside-the-band', 'What is the chance? Give a percentage to 1 decimal place.', num(0.1587, { abs: 0.0005 }, { unit: '%' }), 'So $P = 15.5\\%$.', OK_EX, [['warn', '[working-band]']]],
  [1, 3, 'working-in-per-cent-inside-the-band', 'What is the chance? Give a percentage to 1 decimal place.', num(0.1587, { abs: 0.0005 }, { unit: '%' }), 'So $P = 15.9\\%$.', OK_EX, [['nowarn', '[working-band]']]],
  [1, 4, 'working-a-part-asked-in-units-is-skipped', 'What is the rate, in units of $10^{-5}$? Give 3 decimal places.', num(4.862, { abs: 0.0001 }), 'It is $x = 4.5$.', OK_EX, [['nowarn', '[working-band]']]],
  /* rounding-tie */
  [2, 0, 'key-on-a-tie-with-a-narrow-band', 'What is the total? Give 2 decimal places.', num(8.645, { abs: 0.004 }), OK_FB, OK_EX, [['warn', '[rounding-tie]'], ['warn', 'the key 8.645']]],
  [2, 1, 'key-on-a-tie-with-a-half-unit-band', 'What is the total? Give 2 decimal places.', num(8.645, { abs: 0.005 }), OK_FB, OK_EX, [['nowarn', '[rounding-tie]']]],
  [2, 2, 'slip-on-a-tie-with-a-narrow-band', 'What is the total? Give 2 decimal places.', num(10, { abs: 0.005 }, { wrong: [{ id: 'tie', value: 8.645, tol: { abs: 0.0049 } }] }), OK_FB, OK_EX, [['warn', '[rounding-tie]'], ['warn', 'wrong "tie"']]],
  [2, 3, 'slip-on-a-tie-with-the-default-band', 'What is the total? Give 2 decimal places.', num(10, { abs: 0.005 }, { wrong: [{ id: 'tie', value: 8.645 }] }), OK_FB, OK_EX, [['warn', '[rounding-tie]']]],
  [2, 4, 'slip-to-the-nearest-hundred-on-a-tie', 'What is the cost, to the nearest hundred pounds?', num(6000, { abs: 50 }, { wrong: [{ id: 'tie', value: 5550, tol: { abs: 40 } }] }), OK_FB, OK_EX, [['warn', '[rounding-tie]']]],
  [3, 0, 'key-is-one-rounding-of-a-printed-tie', 'What is the chance? Give 4 decimal places.', num(0.0313, { abs: 0.00003 }), 'So the chance is $p = 0.03125$.', OK_EX, [['warn', '[rounding-tie]'], ['warn', 'feedback.correct prints 0.03125']]],
  [3, 1, 'key-with-a-band-over-both-roundings-of-a-printed-tie', 'What is the chance? Give 4 decimal places.', num(0.0313, { abs: 0.0001 }), 'So the chance is $p = 0.03125$.', OK_EX, [['nowarn', '[rounding-tie]']]],
  [3, 2, 'key-off-a-tie', 'What is the chance? Give 4 decimal places.', num(0.0316, { abs: 0.00003 }), 'So the chance is $p = 0.0316$.', OK_EX, [['nowarn', '[rounding-tie]']]],
  /* table-source */
  [4, 0, 'normal-tail-with-no-source', 'What is the chance the trade loses? Give a decimal to 3 places.', num(0.139, { abs: 0.0005 }), 'So $P(Z > 1.084) = 0.139$.', OK_EX, [['warn', '[table-source]']]],
  [4, 1, 'normal-tail-names-a-table', 'Use a normal table. What is the chance the trade loses? Give a decimal to 3 places.', num(0.139, { abs: 0.0005 }), 'So $P(Z > 1.084) = 0.139$.', OK_EX, [['nowarn', '[table-source]']]],
  [4, 2, 'normal-tail-states-the-value', 'Take $\\Phi(1.084) = 0.861$. What is the chance the trade loses? Give a decimal to 3 places.', num(0.139, { abs: 0.0005 }), 'So $1 - \\Phi(1.084) = 0.139$.', OK_EX, [['nowarn', '[table-source]']]],
  [4, 3, 'quantile-stated-in-the-question', 'Using the normal quantile 1.96, what is the upper end? Give 2 decimal places.', num(5.2, { abs: 0.005 }), 'It is $3 + 1.96 \\times 2 = 6.92$.', OK_EX, [['nowarn', '[table-source]']]],
  [4, 4, 'p-value-asked-with-no-source', 'What is the p-value? Give 4 decimal places.', num(0.0281, { abs: 0.00005 }), OK_FB, OK_EX, [['warn', '[table-source]']]],
  [5, 0, 'a-random-variable-t-is-not-a-table', 'What is $P(T \\le 2)$? Give the exact decimal.', num(0.784, { abs: 0.0005 }), 'So $P(T \\le 2) = 0.784$.', OK_EX, [['nowarn', '[table-source]']]],
  [5, 1, 'the-formula-for-the-tail-is-given', 'With 2 degrees of freedom, $P(\\chi^2_2 \\ge x) = e^{-x/2}$. What is the p-value for $x = 7.143$? Give 4 decimal places.', num(0.0281, { abs: 0.00005 }), 'So $P(\\chi^2_2 \\ge 7.143) = e^{-3.5715} = 0.0281$.', OK_EX, [['nowarn', '[table-source]']]],
  /* percent-unit */
  [5, 2, 'percentage-asked-with-no-unit', 'What is the return, as a percentage? Give 1 decimal place.', num(5.4, { abs: 0.05 }), OK_FB, OK_EX, [['error', '[percent-unit]']]],
  [5, 3, 'percentage-asked-with-the-unit', 'What is the return, as a percentage? Give 1 decimal place.', num(0.054, { abs: 0.0005 }, { unit: '%' }), OK_FB, OK_EX, [['nowarn', '[percent-unit]']]],
  [5, 4, 'what-percentage-asked-with-no-unit', 'What percentage of the days were quiet? Give 1 decimal place.', num(62.5, { abs: 0.05 }), OK_FB, OK_EX, [['error', '[percent-unit]']]],
  [6, 0, 'percent-squared-is-not-a-percentage', 'What is the variance, in %²? Give 2 decimal places.', num(8.67, { abs: 0.005 }), OK_FB, OK_EX, [['nowarn', '[percent-unit]']]],
  [6, 1, 'percentage-points-are-not-a-percentage', 'What is the standard error, in percentage points? Give 4 decimal places.', num(0.6667, { abs: 0.00005 }), OK_FB, OK_EX, [['nowarn', '[percent-unit]']]],
  [6, 2, 'no-percentage-asked', 'What is the length, in metres?', num(12, { abs: 0 }), OK_FB, OK_EX, [['nowarn', '[percent-unit]']]],
  /* wide-wrong-tol */
  [6, 3, 'wrong-band-wider-than-its-value', 'What is the length, in metres? Give 2 decimal places.', num(5.25, { abs: 0.005 }, { wrong: [{ id: 'units', value: 0.0793, tol: { abs: 0.5 } }] }), OK_FB, OK_EX, [['warn', '[wide-wrong-tol]']]],
  [6, 4, 'wrong-band-within-its-value', 'What is the length, in metres? Give 2 decimal places.', num(5.25, { abs: 0.005 }, { wrong: [{ id: 'units', value: 0.79, tol: { abs: 0.05 } }] }), OK_FB, OK_EX, [['nowarn', '[wide-wrong-tol]']]],
  /* wrong-band: a slip that rounds to 0 at the asked places */
  [7, 0, 'slip-rounding-to-zero-is-not-narrow', 'What is the length? Give your answer to the nearest whole number.', num(12, { abs: 0 }, { wrong: [{ id: 'times-s', value: 0.075, tol: { abs: 0.0005 } }] }), OK_FB, OK_EX, [['nowarn', '[wrong-band]']]],
  [7, 1, 'slip-rounding-to-zero-at-two-places', 'What is the length? Give 2 decimal places.', num(12.34, { abs: 0.005 }, { wrong: [{ id: 'tiny', value: 0.0004321, tol: { abs: 0.00001 } }] }), OK_FB, OK_EX, [['nowarn', '[wrong-band]']]],
  [7, 2, 'slip-not-rounding-to-zero-is-still-narrow', 'What is the length? Give 2 decimal places.', num(12.34, { abs: 0.005 }, { wrong: [{ id: 'near', value: 0.0793, tol: { abs: 0.0001 } }] }), OK_FB, OK_EX, [['warn', '[wrong-band]']]],
  [7, 3, 'slip-with-extra-decimals-at-whole-number-is-narrow', 'What is the length? Give your answer to the nearest whole number.', num(12, { abs: 0 }, { wrong: [{ id: 'near', value: 7.4321, tol: { abs: 0.001 } }] }), OK_FB, OK_EX, [['warn', '[wrong-band]']]],
  /* escaped-apostrophe */
  [8, 0, 'backslash-before-an-apostrophe', 'What is Monday\\\'s total, in pounds? Give a whole number.', num(12, { abs: 0 }), OK_FB, OK_EX, [['warn', '[escaped-apostrophe]']]],
  [8, 1, 'plain-apostrophe', "What is Monday's total, in pounds? Give a whole number.", num(12, { abs: 0 }), OK_FB, OK_EX, [['nowarn', '[escaped-apostrophe]']]],
];
const items = [...new Set(CASES.map((c) => c[0]))];
while (d.items.length < items.length) d.items.push(JSON.parse(JSON.stringify(d.items[0])));
d.items.forEach((it, i) => { it.id = 'p-case-' + i; it.prose = 'A desk checks a figure that comes out of a small sum.'; it.parts = it.parts.slice(0, 5); while (it.parts.length < 5) it.parts.push(JSON.parse(JSON.stringify(it.parts[0]))); });
for (const [i, k, , question, widget, correct, explain] of CASES) {
  const p = d.items[i].parts[k];
  p.question = question; p.widget = widget; p.feedback = { correct, generic: 'Not quite. Check the step again.', byKey: {} }; p.explain = { text: explain };
}
d.items.length = items.length;
fs.writeFileSync(file, JSON.stringify(d, null, 2));
const out = h.validate(['--no-manifest']).out;
const lines = out.split('\n').filter((l) => /^(error|warning)/.test(l) && /equations\/problems-3/.test(l));
let pass = 0, fail = 0;
for (const [i, k, name, , , , , expect] of CASES) {
  const mine = lines.filter((l) => l.includes(`items[${i}].parts[${k}]`));
  for (const [kind, sub] of expect) {
    const hit = mine.some((l) => l.includes(sub) && (kind === 'error' ? /^error/.test(l) : /^warning/.test(l)));
    const bad = kind === 'nowarn' ? mine.some((l) => l.includes(sub)) : !hit;
    if (bad) { console.log(`FAIL ${name}: ${kind} "${sub}" (lines: ${mine.map((l) => l.slice(0, 220)).join(' | ') || 'none'})`); fail++; } else { console.log(`PASS ${name}: ${kind} "${sub}"`); pass++; }
  }
}
/* the rules run on problem sets only: the same fault in a lesson draws no [percent-unit] error */
const lesson = path.join(copy, 'content/courses/equations/l1-letters-for-numbers.json');
const L = JSON.parse(fs.readFileSync(lesson, 'utf8'));
const scr = (L.screens || []).find((s) => s.widget && s.widget.kind === 'numeric');
if (scr) {
  scr.question = 'What is the return, as a percentage? Give 1 decimal place.'; scr.widget.unit = undefined; delete scr.widget.unit;
  fs.writeFileSync(lesson, JSON.stringify(L, null, 2));
  const lo = h.validate(['--no-manifest']).out.split('\n').filter((l) => /^error/.test(l) && l.includes('[percent-unit]') && l.includes('l1-letters'));
  if (lo.length === 0) { console.log('PASS percent-unit does not run on a lesson'); pass++; } else { console.log('FAIL percent-unit ran on a lesson: ' + lo[0]); fail++; }
} else console.log('SKIP lesson check (the fixture lesson has no numeric screen)');
h.close();
console.log(`test-validate-pass8: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
