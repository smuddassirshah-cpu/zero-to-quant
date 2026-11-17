#!/usr/bin/env node
/* Scratch cases for the rules of engine pass 9b (ENGINE-BACKLOG 1182, 1203, 1205; docs/AUTHORING.md section 5), pattern of test-validate-pass9.mjs.
   Copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs), writes the problem-set fixture into the copy's equations folder as problems-3.json, plants one case in each part
   and reads the report by part. Nothing under app/content is touched.
     [carry-band]  a "from part k" value held against part k's printed working (the pdes p-grid-modes case: 0.2200 from part 3, where $0.9702^{50}$ is 0.22032)
     [band-edge]   a key stored past the asked places whose band edge lands on the next rounding (0.46654 +-0.00006 at 4 places takes 0.4666)
     [later-key]   a byKey, generic or why line that prints the answer of a later numeric part
   Usage: node tools/test-validate-pass9b.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'pass9b', fixtures: ['problems'] });
const copy = h.dir;
fs.rmSync(path.join(copy, 'tools/fixtures/problems'), { recursive: true, force: true });
const fixture = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/problems/problems-fixture-3.json'), 'utf8'));
const file = path.join(copy, 'content/courses/equations/problems-3.json');
const d = JSON.parse(JSON.stringify(fixture)); d.id = 'problems-3';
const num = (answer, tol, extra = {}) => ({ kind: 'numeric', answer, tol, ...extra });
const Q4 = 'What is the value? Give 4 decimal places.', Q3 = 'What is the value? Give 3 decimal places.';
const OK_FB = 'The working gives the answer.', OK_EX = 'Work it through step by step.';
/* a part: question, widget, feedback.correct, explain.text, byKey, generic */
const P = (question, widget, o = {}) => ({ question, widget, correct: o.correct ?? OK_FB, explain: o.explain ?? OK_EX, byKey: o.byKey ?? {}, generic: o.generic ?? 'Not quite. Check the step again.' });
/* item: five parts; expect: [part, kind, substring] */
const ITEMS = [
  { name: 'carry', parts: [
    P(Q3, num(0.22, { abs: 0.0005 }), { correct: 'Fifty steps: $0.9702^{50} \\approx 0.220$.' }),
    P('Using 0.2200 from part 1, what is the gap to 0.2231? Give 4 decimal places.', num(0.0031, { abs: 5e-5 })),
    P('Using 0.220 from part 1, what is the gap to 0.2231? Give 4 decimal places.', num(0.0031, { abs: 5e-5 })),
    P('Using 0.2203 from part 1, what is the gap to 0.2231? Give 4 decimal places.', num(0.0028, { abs: 5e-5 })),
    P('Using 0.2200 from part 2, what is the gap to 0.2231? Give 4 decimal places.', num(0.0031, { abs: 5e-5 })),
  ], expect: [[1, 'warn', '[carry-band] the question carries 0.2200 from part 1'], [2, 'nowarn', 'from part 1, but'], [3, 'nowarn', 'from part 1, but'], [4, 'nowarn', 'carries 0.2200 from part 2']] },
  { name: 'band-edge', parts: [
    P(Q4, num(0.46654, { abs: 6e-5 })),
    P(Q4, num(0.46654, { abs: 5e-5 })),
    P(Q4, num(0.4665, { abs: 6e-5 })),
    P(Q4, num(0.46654, { abs: 1e-4 })),
    P(Q4, num(0.46644, { abs: 5e-5 })),
  ], expect: [[0, 'warn', '[band-edge]'], [1, 'nowarn', '[band-edge]'], [2, 'nowarn', '[band-edge]'], [3, 'nowarn', '[band-edge]'], [4, 'nowarn', '[band-edge]']] },
  { name: 'later-key', parts: [
    P('What is the first value? Give 4 decimal places.', num(0.5, { abs: 5e-5 }), { byKey: { slip: 'You took the square root; the later answer is 1.7795.' } }),
    P('What is the second value? Give 4 decimal places.', num(1.7795, { abs: 5e-5 }), { generic: 'Check the step.' }),
    P('What is the third value? Give 4 decimal places.', num(0.25, { abs: 5e-5 }), { byKey: { slip: 'The third is 0.25 and nothing else.' } }),
    P('Using 1.7795 from part 2, what is the next value? Give 4 decimal places.', num(2.5, { abs: 5e-5 }), { byKey: { slip: 'You used 1.7795 again.' } }),
    P('What is the last value? Give 4 decimal places.', num(7, { abs: 1e-9 }), { byKey: { slip: 'The last is 7.' } }),
  ], expect: [[0, 'warn', '[later-key]'], [1, 'nowarn', '[later-key]'], [2, 'nowarn', '[later-key]'], [3, 'nowarn', '[later-key]'], [4, 'nowarn', '[later-key]']] },
  { name: 'later-key-short', parts: [
    P('What is the first value? Give 4 decimal places.', num(0.5, { abs: 5e-5 }), { byKey: { slip: 'The later answer is 7.' } }),
    P('What is the second value? Give a whole number.', num(7, { abs: 1e-9 })),
    P('What is the third value? Give 4 decimal places.', num(0.25, { abs: 5e-5 })),
    P('What is the fourth value? Give 4 decimal places.', num(0.25, { abs: 5e-5 })),
    P('What is the fifth value? Give 4 decimal places.', num(0.25, { abs: 5e-5 })),
  ], expect: [[0, 'nowarn', '[later-key]']] },
];
d.items.forEach((it) => { it.parts = it.parts.slice(0, 5); while (it.parts.length < 5) it.parts.push(JSON.parse(JSON.stringify(it.parts[0]))); });
while (d.items.length < ITEMS.length) d.items.push(JSON.parse(JSON.stringify(d.items[0])));
d.items.length = ITEMS.length;
ITEMS.forEach((def, i) => {
  const it = d.items[i]; it.id = 'p-case-' + i; it.prose = 'A desk checks a figure that comes out of a small sum.';
  def.parts.forEach((c, k) => { it.parts[k].question = c.question; it.parts[k].widget = c.widget; it.parts[k].feedback = { correct: c.correct, generic: c.generic, byKey: c.byKey }; it.parts[k].explain = { text: c.explain }; });
});
fs.writeFileSync(file, JSON.stringify(d, null, 2));
const out = h.validate(['--no-manifest']).out;
const lines = out.split('\n').filter((l) => /^(error|warning)/.test(l) && /equations\/problems-3/.test(l));
let pass = 0, fail = 0;
ITEMS.forEach((def, i) => {
  for (const [k, kind, sub] of def.expect) {
    const mine = lines.filter((l) => l.includes(`items[${i}].parts[${k}]`));
    const hit = mine.some((l) => l.includes(sub) && /^warning/.test(l));
    const bad = kind === 'nowarn' ? mine.some((l) => l.includes(sub)) : !hit;
    const name = `${def.name} part ${k + 1}`;
    if (bad) { console.log(`FAIL ${name}: ${kind} "${sub}" (lines: ${mine.map((l) => l.slice(0, 240)).join(' | ') || 'none'})`); fail++; } else { console.log(`PASS ${name}: ${kind} "${sub}"`); pass++; }
  }
});
h.close();
console.log(`test-validate-pass9b: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
