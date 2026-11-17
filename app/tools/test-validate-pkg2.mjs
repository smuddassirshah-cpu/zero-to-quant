#!/usr/bin/env node
/* Scratch cases for the validator rules of engine pass 7 remainder, package 2 (ENGINE-BACKLOG 1029, 1079, 1130, 1138, 1142, 1175; docs/AUTHORING.md section 5).
   Pattern of test-validate-pass9.mjs: copies tools/fixtures/mini-app (lib/validate-harness.mjs), writes the problem-set fixture as problems-3.json of the equations course, plants one case
   in each part and reads the report by part. Parts are placed in order, five to an item; an ITEM case fills a whole item (a chain of parts). Nothing under app/content is touched.
     [slip-expr]        a numeric wrong[] entry's "slip" expression that does not read or does not give the entry's value   (1029)
     [no-chain]         a problem whose later parts never cite an earlier part                                              (1079)
     [carry-band]       "Using x from part k" with a wrong band narrower than the key band                                   (1130)
     [quotient-band]    a printed quotient of two restated figures that leaves the key's band                               (1138)
     [shown-arithmetic] widened: "x is $a \times b$" and a quotient inside \Phi\big(...\big)                                (1142)
     [slip-band]        a slip typed at the places the part asks that falls in the key's band or outside its own band        (1175)
   Usage: node tools/test-validate-pkg2.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'pkg2', fixtures: ['problems'] });
const copy = h.dir;
fs.rmSync(path.join(copy, 'tools/fixtures/problems'), { recursive: true, force: true });
const fixture = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/problems/problems-fixture-3.json'), 'utf8'));
const file = path.join(copy, 'content/courses/equations/problems-3.json');
const d = JSON.parse(JSON.stringify(fixture)); d.id = 'problems-3';
const num = (answer, tol, extra = {}) => ({ kind: 'numeric', answer, tol, ...extra });
const OK_FB = 'The working gives the answer.', OK_EX = 'Work it through step by step.';
const Q5 = 'What is the value? Give a decimal to 5 places.', Q4 = 'What is the value? Give 4 decimal places.', Q2 = 'What is the value? Give 2 decimal places.', Q0 = 'What is the value? Give the nearest whole number.';
/* a part: [name, question, widget, feedback.correct, explain.text, expect]; expect: [kind, substring] with kind warn or nowarn */
const PARTS = [
  /* 1029 [slip-expr] */
  ['slip-expression-gives-the-value', Q2, num(1.73, { abs: 0.005 }, { wrong: [{ id: 'cubed', value: 0.43, tol: { abs: 0.005 }, slip: '0.25 * 1.2^3' }] }), OK_FB, OK_EX, [['nowarn', '[slip-expr]']]],
  ['slip-expression-gives-another-value', Q2, num(1.73, { abs: 0.005 }, { wrong: [{ id: 'cubed', value: 0.5, tol: { abs: 0.005 }, slip: '0.25 * 1.2^3' }] }), OK_FB, OK_EX, [['warn', '[slip-expr]'], ['warn', 'works out to 0.432']]],
  ['slip-expression-does-not-read', Q2, num(1.73, { abs: 0.005 }, { wrong: [{ id: 'cubed', value: 0.43, tol: { abs: 0.005 }, slip: 'one quarter of 1.2 cubed' }] }), OK_FB, OK_EX, [['warn', 'does not read as arithmetic']]],
  ['slip-expression-with-functions-and-a-rounded-value', Q4, num(2.1, { abs: 0.0005 }, { wrong: [{ id: 'root', value: 1.4142, slip: 'sqrt(2)' }, { id: 'lg', value: 0.6931, slip: 'ln(2)' }, { id: 'ex', value: 7.3891, slip: 'exp(2)' }] }), OK_FB, OK_EX, [['nowarn', '[slip-expr]']]],
  ['slip-expression-that-is-not-a-string', Q2, num(1.73, { abs: 0.005 }, { wrong: [{ id: 'cubed', value: 0.43, tol: { abs: 0.005 }, slip: 0.43 }] }), OK_FB, OK_EX, [['warn', 'slip is an arithmetic expression']]],
];
/* an item: [name, [[question, widget, feedback.correct, explain.text], ...], expect] */
const ITEMS = [
];
const place = PARTS.map((c, n) => [Math.floor(n / 5), n % 5, c]);
const itemBase = Math.ceil(PARTS.length / 5);
const nItems = Math.max(itemBase + ITEMS.length, 3);
while (d.items.length < nItems) d.items.push(JSON.parse(JSON.stringify(d.items[0])));
d.items.forEach((it, i) => { it.id = 'p-case-' + i; it.prose = 'A desk checks a figure that comes out of a small sum.'; it.parts = it.parts.slice(0, 5); while (it.parts.length < 5) it.parts.push(JSON.parse(JSON.stringify(it.parts[0]))); });
const fill = (p, question, widget, correct, explain) => { p.question = question; p.widget = widget; p.feedback = { correct, generic: 'Not quite. Check the step again.', byKey: {} }; p.explain = { text: explain }; };
for (const [i, k, [, question, widget, correct, explain]] of place) fill(d.items[i].parts[k], question, widget, correct, explain);
ITEMS.forEach(([, parts], j) => { const it = d.items[itemBase + j]; it.parts = it.parts.slice(0, parts.length); parts.forEach(([q, w, c, e], k) => fill(it.parts[k], q, w, c, e)); });
d.items.length = nItems;
fs.writeFileSync(file, JSON.stringify(d, null, 2));
const out = h.validate(['--no-manifest']).out;
const lines = out.split('\n').filter((l) => /^(error|warning)/.test(l) && /equations\/problems-3/.test(l));
let pass = 0, fail = 0;
const judge = (name, mine, expect) => {
  for (const [kind, sub] of expect) {
    const hit = mine.some((l) => l.includes(sub) && /^warning/.test(l));
    const bad = kind === 'nowarn' ? mine.some((l) => l.includes(sub)) : !hit;
    if (bad) { console.log(`FAIL ${name}: ${kind} "${sub}" (lines: ${mine.map((l) => l.slice(0, 260)).join(' | ') || 'none'})`); fail++; } else { console.log(`PASS ${name}: ${kind} "${sub}"`); pass++; }
  }
};
for (const [i, k, [name, , , , , expect]] of place) judge(name, lines.filter((l) => l.includes(`items[${i}].parts[${k}]`)), expect);
ITEMS.forEach(([name, , expect], j) => judge(name, lines.filter((l) => new RegExp(`items\\[${itemBase + j}\\](?!\\d)`).test(l)), expect));
h.close();
console.log(`test-validate-pkg2: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
