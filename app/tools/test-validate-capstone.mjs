#!/usr/bin/env node
/* Scratch cases for tools/capstone-rules.mjs (ENGINE-BACKLOG 565). Run from app/: node tools/test-validate-capstone.mjs. Exit 1 on a failure. */
import { checkCapstones } from './capstone-rules.mjs';
const blankRec = (role, x = {}) => ({ role, project: '', repo: '', reviewer: '', date: '', rerun: '', defence: '', external: false, ...x });
const done = (role, x = {}) => blankRec(role, { project: 'p', repo: 'https://github.com/a/b', reviewer: 'Sam', date: '2026-11-05', rerun: 'pass', external: true, ...x });
const cases = [
  ['empty list ok', [], null],
  ['five empty records ok', ['trader', 'researcher', 'developer', 'strats', 'strats-deriv'].map(r => blankRec(r)), null],
  ['complete record ok', [done('trader')], null],
  ['researcher momentum-rep ok', [done('researcher', { project: 'momentum-rep' })], null],
  ['researcher equivalent ok', [done('researcher', { project: 'my-factor', equivalentOf: 'momentum-rep' })], null],
  ['not an array', {}, 'array'],
  ['unknown role', [blankRec('undecided')], 'unknown role'],
  ['unknown field', [blankRec('trader', { colour: 'x' })], 'unknown field'],
  ['wrong type', [blankRec('trader', { external: 'yes' })], 'boolean'],
  ['duplicate role', [blankRec('trader'), blankRec('trader')], 'duplicate'],
  ['external blank reviewer', [done('trader', { reviewer: '' })], 'reviewer'],
  ['external blank rerun', [done('trader', { rerun: '' })], 'rerun'],
  ['bad repo url', [blankRec('trader', { repo: 'github.com/a' })], 'https URL'],
  ['bad date', [blankRec('trader', { date: '05/11/2026' })], 'ISO date'],
  ['impossible date', [blankRec('trader', { date: '2026-02-31' })], 'ISO date'],
  ['bad rerun', [blankRec('trader', { rerun: 'maybe' })], 'rerun'],
  ['researcher other project', [blankRec('researcher', { project: 'other' })], 'momentum-rep'],
];
let pass = 0, fail = 0;
for (const [name, input, has] of cases) {
  const errs = checkCapstones(input).map(x => `${x.where} ${x.msg}`);
  const okc = has === null ? !errs.length : errs.some(m => m.includes(has));
  console.log(`${okc ? 'PASS' : 'FAIL'} ${name}${okc ? '' : ': ' + (errs.join(' | ') || 'no error')}`); okc ? pass++ : fail++;
}
console.log(`${fail ? 'FAIL' : 'PASS'} summary: ${pass} of ${pass + fail} capstone cases passed`);
process.exit(fail ? 1 : 0);
