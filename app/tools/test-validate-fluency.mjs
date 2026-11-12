#!/usr/bin/env node
/* Scratch cases for the generated fluency set rules (ENGINE-BACKLOG 812, 813, 816). Copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs), writes the fixture
   set into the copy's course folder as a real set (so nothing under app/content is touched), breaks one thing per case and expects
   the validator to report it (or, for the first case, nothing). One PASS or FAIL line per case, exit 1 on a failure.
   Run from anywhere: node app/tools/test-validate-fluency.mjs */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'fluency', fixtures: [] });   // a scratch copy of tools/fixtures/mini-app (see lib/validate-harness.mjs)
const tmp = h.dir;
const copy = h.dir;
const run = (...args) => h.validate(args);
const fixture = JSON.parse(fs.readFileSync(path.join(APP, 'tools/fixtures/fluency/fluency-l3-opening-brackets.json'), 'utf8'));
delete fixture.sample; delete fixture.course;
const dir = path.join(copy, 'content/courses/equations');
const file = path.join(dir, 'fluency-l3-opening-brackets.json');
fs.rmSync(path.join(copy, 'tools/fixtures/fluency'), { recursive: true, force: true });   // the copy holds only the case's set
const fam = (d, id) => d.families.find((f) => f.id === id);
const cases = [
  ['ok-as-shipped', () => {}, null],
  ['lesson-not-on-the-map', (d) => { d.lesson = 'l99-nothing'; d.id = 'fluency-l99-nothing'; fs.renameSync(file, path.join(dir, 'fluency-l99-nothing.json')); }, 'is not on the course map'],
  ['id-does-not-match-the-file', (d) => { d.id = 'fluency-other'; }, 'must be "fluency-l3-opening-brackets"'],
  ['no-families', (d) => { d.families = []; }, 'at least one family'],
  ['pass-out-of-range', (d) => { d.pass = 0.3; }, 'pass is a share'],
  ['n-out-of-range', (d) => { d.n = 3; }, 'n is a whole number from 5 to 50'],
  ['duplicate-family-id', (d) => { d.families[1].id = d.families[0].id; }, 'is used twice'],
  ['unknown-name-in-prompt', (d) => { fam(d, 'expand-single').prompt = 'Expand ${a}({v}{zz:+})$.'; }, '"zz" is neither a var nor a let'],
  ['unknown-function', (d) => { fam(d, 'expand-single').let.p = 'twice(a)'; }, 'unknown function "twice"'],
  ['product-without-star', (d) => { fam(d, 'expand-single').let.p = '2a'; }, 'a product needs a *'],
  ['stray-brace', (d) => { fam(d, 'expand-single').prompt = 'Expand $a(x)$}.'; }, 'stray'],
  ['unclosed-brace', (d) => { fam(d, 'expand-single').prompt = 'Expand ${a'; }, 'never closed'],
  ['choice-widget', (d) => { fam(d, 'expand-single').widget = { kind: 'choice', answer: 'x' }; }, '"numeric" or "expression"'],
  ['unknown-format', (d) => { fam(d, 'expand-single').prompt = 'Expand ${a}({v}{b:zz})$.'; }, 'unknown format'],
  ['wrong-equals-the-answer', (d) => { fam(d, 'expand-single').vars.a = { int: [1, 9] }; }, 'first-term-only'],
  ['wrong-with-when-is-protected', (d) => { const f = fam(d, 'expand-single'); f.vars.a = { int: [1, 9] }; f.wrong[0].when = 'a > 1'; }, null],
  ['when-names-something-unknown', (d) => { fam(d, 'expand-single').wrong[0].when = 'zz > 1'; }, '"zz" is not a var or a let'],
  ['numeric-wrong-inside-tolerance', (d) => { fam(d, 'evaluate-linear').widget.tol = { abs: 100 }; }, 'grades as correct'],
  ['where-rejects-nearly-everything', (d) => { fam(d, 'expand-single').where = ['a == 9 and b > 0']; }, 'reject '],
  ['where-never-holds', (d) => { fam(d, 'expand-single').where = ['a > 100']; }, 'could not be completed'],
  ['division-by-zero', (d) => { fam(d, 'expand-single').where = ['a / (b - b) > 0']; }, 'division by zero'],
  ['let-division-by-zero-rejects', (d) => { fam(d, 'expand-single').let.p = 'a / (b - b)'; }, 'could not be completed'],
  ['too-few-distinct-prompts', (d) => { const f = fam(d, 'expand-single'); f.vars = { a: { int: [2, 4] }, b: { int: [1, 3] }, v: { pick: ['x'] } }; }, 'distinct prompts'],
  ['a-text-var-in-arithmetic', (d) => { fam(d, 'expand-single').let.p = 'a * v'; }, 'needs numbers'],
  ['exclamation-in-a-line', (d) => { fam(d, 'expand-single').wrong[0].line = 'You only did the first term!'; }, 'no exclamation marks'],
  ['american-spelling-in-a-step', (d) => { fam(d, 'expand-single').solution[0] = 'Multiply each term and then analyze the result.'; }, 'American spelling'],
  ['em-dash-in-a-step', (d) => { fam(d, 'expand-single').solution[1] = 'So — done.'; }, 'em-dash'],
  ['unbalanced-dollar', (d) => { fam(d, 'expand-single').prompt = 'Expand ${a}({v}{b:+}.'; }, 'unbalanced'],
  ['sentence-over-35-words', (d) => { fam(d, 'expand-single').solution[1] = 'So we multiply every term inside the bracket by the number outside it, one after the other, and then we write each product down in the same order as before so that nothing is lost on the way, which gives the result below for you to check twice.'; }, 'the gate is 35'],
  ['unknown-family-field', (d) => { fam(d, 'expand-single').hint = 'x'; }, 'unknown field "hint"'],
  ['form-on-a-numeric-widget', (d) => { fam(d, 'evaluate-linear').widget.form = 'expanded'; }, 'widget.form'],
  ['let-reads-a-later-let', (d) => { fam(d, 'antiderivative-power').let = { c: 'k1 * m', k1: 'k + 1' }; }, 'not a var or an earlier let'],
  /* ENGINE-BACKLOG 830 to 834: the new forms, set answers and a pick of tuples */
  ['numeric-set-wrong-equals-the-answer', (d) => { fam(d, 'roots-numeric').wrong[0].value = '{s}, {r}'; }, 'grades as correct'],
  ['expression-set-wrong-equals-the-answer', (d) => { fam(d, 'roots-expression').wrong[0].tex = '{-d/c:frac}, {-b/a:frac}'; }, 'grades as correct'],
  ['set-answers-without-unordered', (d) => { delete fam(d, 'roots-numeric').widget.unordered; }, 'unordered'],
  ['set-with-an-answer-as-well', (d) => { fam(d, 'roots-expression').widget.answer = '{r}'; }, 'not both'],
  ['set-with-a-form', (d) => { fam(d, 'roots-surd').widget.form = 'simplified'; }, 'form is not used with answers'],
  ['numeric-set-wrong-not-numbers', (d) => { fam(d, 'roots-numeric').wrong[0].value = 'two, five'; }, 'draws could not be completed'],
  ['tuple-of-the-wrong-length', (d) => { fam(d, 'roots-numeric').vars.roots.pick[0] = [1]; }, 'tuples, each with 2'],
  ['tuple-name-already-a-var', (d) => { fam(d, 'roots-numeric').vars.roots.as = ['r', 'v']; }, 'already a var'],
  ['unknown-form', (d) => { fam(d, 'factorise-fully').widget.form = 'factorised-full'; }, 'widget.form'],
  ['fully-wrong-is-the-key-typed-differently', (d) => { fam(d, 'factorise-fully').wrong[0].tex = '{k}({v}{p:+})({v}{q:+})'; }, 'common-factor-dropped'],
  ['stray-nan', (d) => { fam(d, 'evaluate-linear').let.r = 'a + b*x'; fam(d, 'evaluate-linear').solution[1] = '${a} + {sqrt(0-1)}$.'; }, 'sqrt of a negative'],
];
let pass = 0, fail = 0;
for (const [name, mutate, has] of cases) {
  const d = JSON.parse(JSON.stringify(fixture));
  fs.writeFileSync(file, JSON.stringify(d, null, 2));
  const renamed = [];
  mutate(d);
  const target = fs.existsSync(file) ? file : path.join(dir, 'fluency-l99-nothing.json');
  fs.writeFileSync(target, JSON.stringify(d, null, 2));
  const r = run('--no-manifest');
  const errs = r.out.split('\n').filter((l) => /^error/.test(l) && /fluency/.test(l));
  let problem = null;
  if (has === null) { if (r.code !== 0 || errs.length) problem = `expected no error, got ${errs.length}: ${errs[0] || r.out.slice(-300)}`; }
  else if (!errs.some((l) => l.includes(has))) problem = `no error contains "${has}" (got ${errs.length}: ${errs[0] || 'none'})`;
  if (!problem && has === null) {   // the manifest lists the set, and the set is a real one
    const m = run();
    const man = JSON.parse(fs.readFileSync(path.join(copy, 'content/manifest.json'), 'utf8'));
    const row = man.fluency && man.fluency['equations/fluency-l3-opening-brackets'];
    if (m.code !== 0 || !row || row.lesson !== 'l3-opening-brackets' || row.families !== fixture.families.length || row.n !== 20 || row.sample || !man.files.includes('courses/equations/fluency-l3-opening-brackets.json')) problem = `manifest row wrong: ${JSON.stringify(row)}`;
  }
  fs.rmSync(path.join(dir, 'fluency-l99-nothing.json'), { force: true });
  void renamed;
  if (problem) { console.log(`FAIL ${name}: ${problem}`); fail++; } else { console.log(`PASS ${name}`); pass++; }
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`test-validate-fluency: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
