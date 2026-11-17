#!/usr/bin/env node
/* Scratch cases for the problem-set rules of engine pass 9 (ENGINE-BACKLOG 1154 to 1210; docs/AUTHORING.md section 5), pattern of test-validate-pass8.mjs.
   Copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs), writes the problem-set fixture into the copy's equations folder as problems-3.json, plants one case in each part
   and reads the report by part. Nothing under app/content is touched.
     [rounding-tie]     a slip on a tie at the asked places (the slip-past-places branch was withdrawn in 9b); a key a hair off a tie; a printed product that lands on a tie
     [working-band]     a printed span re-evaluated from its own rounded figures leaves the band
     [key-in-question]  a numeric key printed in its own question
   Usage: node tools/test-validate-pass9.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'pass9', fixtures: ['problems'] });
const copy = h.dir;
fs.rmSync(path.join(copy, 'tools/fixtures/problems'), { recursive: true, force: true });
const fixture = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/problems/problems-fixture-3.json'), 'utf8'));
const file = path.join(copy, 'content/courses/equations/problems-3.json');
const d = JSON.parse(JSON.stringify(fixture)); d.id = 'problems-3';
const num = (answer, tol, extra = {}) => ({ kind: 'numeric', answer, tol, ...extra });
const OK_FB = 'The working gives the answer.', OK_EX = 'Work it through step by step.';
const Q5 = 'What is the value? Give a decimal to 5 places.', Q4 = 'What is the value? Give 4 decimal places.', Q2 = 'What is the value? Give 2 decimal places.';
/* [item, part, name, question, widget, feedback.correct, explain.text, expect] ; expect: [kind, substring] with kind warn or nowarn */
const CASES = [
  /* rounding-tie: a slip stored past the asked places */
  [0, 0, 'slip-stored-past-the-places-with-a-half-step-band-is-silent-since-9b', Q5, num(0.006759, { abs: 5e-6 }, { wrong: [{ id: 'no-weight', value: 0.054688, tol: { abs: 5e-6 } }] }), OK_FB, OK_EX, [['nowarn', '[rounding-tie]']]],
  [0, 4, 'slip-exactly-on-a-tie-at-the-asked-places', Q5, num(0.006759, { abs: 5e-6 }, { wrong: [{ id: 'tie', value: 0.054685, tol: { abs: 1e-6 } }] }), OK_FB, OK_EX, [['warn', '[rounding-tie]'], ['warn', 'wrong "tie"']]],
  [0, 1, 'slip-stored-past-the-places-with-a-full-step-band', Q5, num(0.006759, { abs: 5e-6 }, { wrong: [{ id: 'no-weight', value: 0.0546875, tol: { abs: 1e-5 } }] }), OK_FB, OK_EX, [['nowarn', '[rounding-tie]']]],
  [0, 2, 'slip-stored-past-the-places-near-a-round-value', Q5, num(0.006759, { abs: 5e-6 }, { wrong: [{ id: 'near', value: 0.054699, tol: { abs: 5e-6 } }] }), OK_FB, OK_EX, [['nowarn', '[rounding-tie]']]],
  [0, 3, 'slip-at-the-asked-places', Q5, num(0.006759, { abs: 5e-6 }, { wrong: [{ id: 'plain', value: 0.05469, tol: { abs: 5e-6 } }] }), OK_FB, OK_EX, [['nowarn', '[rounding-tie]']]],
  /* rounding-tie: a key a hair off a tie */
  [1, 0, 'key-a-hair-off-a-tie-with-a-half-step-band', Q4, num(0.691956, { abs: 5e-5 }), OK_FB, OK_EX, [['warn', '[rounding-tie]'], ['warn', 'of a rounding tie']]],
  [1, 1, 'key-a-hair-off-a-tie-with-a-full-step-band', Q4, num(0.691956, { abs: 1e-4 }), OK_FB, OK_EX, [['nowarn', '[rounding-tie]']]],
  [1, 2, 'key-well-off-a-tie', Q4, num(0.691912, { abs: 5e-5 }), OK_FB, OK_EX, [['nowarn', '[rounding-tie]']]],
  [1, 3, 'key-stored-at-the-asked-places', Q4, num(0.6920, { abs: 5e-5 }), OK_FB, OK_EX, [['nowarn', '[rounding-tie]']]],
  /* rounding-tie: a printed product on a tie */
  [2, 0, 'printed-product-on-a-tie-with-a-narrow-band', Q2, num(64.99, { abs: 0.004 }), 'So the note is $75 \\times 0.8666 = 64.995$ pounds.', OK_EX, [['warn', '[rounding-tie]'], ['warn', '75 \\times 0.8666']]],
  [2, 1, 'printed-product-on-a-tie-with-a-wide-band', Q2, num(64.99, { abs: 0.01 }), 'So the note is $75 \\times 0.8666 = 64.995$ pounds.', OK_EX, [['nowarn', '75 \\times 0.8666']]],
  [2, 2, 'printed-product-followed-by-another-factor', Q2, num(64.99, { abs: 0.004 }), 'So the note is $75 \\times 0.8666 e^{-0.1}$ pounds.', OK_EX, [['nowarn', '75 \\times 0.8666']]],
  [2, 3, 'printed-product-off-a-tie', Q2, num(64.99, { abs: 0.004 }), 'So the note is $75 \\times 0.8665 = 64.9875$ pounds.', OK_EX, [['nowarn', '75 \\times 0.8665']]],
  /* working-band: a span re-evaluated from its printed figures */
  [3, 0, 'quotient-of-rounded-figures-leaves-the-band', Q5, num(0.005176, { abs: 5e-6 }), 'The sum is $10 \\times \\tfrac{0.0000266}{0.0513} \\approx 0.00518$.', OK_EX, [['warn', '[working-band]'], ['warn', 'from the printed figures']]],
  [3, 1, 'quotient-of-rounded-figures-stays-in-the-band', Q5, num(0.005176, { abs: 5e-6 }), 'The sum is $10 \\times \\tfrac{0.00002656}{0.0513} \\approx 0.00518$.', OK_EX, [['nowarn', 'from the printed figures']]],
  [3, 2, 'exponential-of-a-printed-exponent-leaves-the-band', Q4, num(0.4939, { abs: 5e-5 }), 'The ratio is $e^{-0.7048} \\approx 0.4939$.', OK_EX, [['warn', 'from the printed figures']]],
  [3, 3, 'exponential-of-a-printed-exponent-in-the-band', Q4, num(0.4942, { abs: 5e-5 }), 'The ratio is $e^{-0.7048} \\approx 0.4942$.', OK_EX, [['nowarn', 'from the printed figures']]],
  [3, 4, 'span-with-letters-is-not-evaluated', Q4, num(0.4942, { abs: 5e-5 }), 'The ratio is $x^2 \\times 3 \\approx 0.4942$.', OK_EX, [['nowarn', 'from the printed figures']]],
  /* key-in-question */
  [4, 0, 'key-restated-after-an-equals-sign', 'Using $\\operatorname{ord}(fT) = 4$ from part 2, what is the order of $f$ itself?', num(4, { abs: 0 }), OK_FB, OK_EX, [['warn', '[key-in-question]']]],
  [4, 1, 'key-as-an-exponent-in-the-question', 'What is the value of $x^4$ at $x = 2$?', num(4, { abs: 0 }), OK_FB, OK_EX, [['nowarn', '[key-in-question]']]],
  [4, 2, 'key-equals-the-places-asked', 'What is the order? Give 4 decimal places.', num(4, { abs: 0 }), OK_FB, OK_EX, [['nowarn', '[key-in-question]']]],
  [4, 3, 'long-key-printed-anywhere', 'The ratio 0.4942 is wanted again. What is it? Give 4 decimal places.', num(0.494188, { abs: 5e-5 }), OK_FB, OK_EX, [['warn', '[key-in-question]']]],
  [4, 4, 'key-not-in-the-question', 'What is the order of $f$ if $\\operatorname{ord}(fT) = 6$?', num(4, { abs: 0 }), OK_FB, OK_EX, [['nowarn', '[key-in-question]']]],
  /* working-band (9b): a whole-number key that is the printed result rounded up and printed after the span is a ceiling, not a fault */
  [5, 0, 'ceiling-key-printed-after-the-span', 'How many are needed? Give a whole number.', num(3899, { abs: 0 }), 'Take $2 \\times 1949.2 = 3898.4$, so 3899 are needed.', OK_EX, [['nowarn', '[working-band]']]],
  [5, 1, 'ceiling-key-not-printed-after-the-span', 'How many are needed? Give a whole number.', num(3899, { abs: 0 }), 'Take $2 \\times 1949.2 = 3898.4$ and stop.', OK_EX, [['warn', '[working-band]']]],
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
    const hit = mine.some((l) => l.includes(sub) && /^warning/.test(l));
    const bad = kind === 'nowarn' ? mine.some((l) => l.includes(sub)) : !hit;
    if (bad) { console.log(`FAIL ${name}: ${kind} "${sub}" (lines: ${mine.map((l) => l.slice(0, 220)).join(' | ') || 'none'})`); fail++; } else { console.log(`PASS ${name}: ${kind} "${sub}"`); pass++; }
  }
}
h.close();
console.log(`test-validate-pass9: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
