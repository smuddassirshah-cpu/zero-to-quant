#!/usr/bin/env node
/* Tests for machine-readable drill constraints (ENGINE-BACKLOG 866). Run from app/: node tools/test-drill-constraints.mjs
     1. tools/drill-constraints.mjs in plain node: the Python-literal call reader, each constraint key, the shape check.
     2. The validator on a temporary copy of app/: a drill with satisfied constraints passes; a test that breaks one is an error; a malformed
        constraint is an error; a drill with none carries the [no-constraints] warning; a sample drill does not. Nothing under app/content is touched.
   Exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { parseCall, paramNames, constraintShape, checkTest, drillConstraintReport } from './drill-constraints.mjs';
const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
let bad = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) bad++; };
const msgs = (cons, call, names = []) => checkTest(cons, { call }, names).messages;
const clean = (cons, call, names) => { const r = checkTest(cons, { call }, names); return r.checked && !r.messages.length; };

/* ---------- 1. the reader and the keys ---------- */
const p = parseCall("f([1, -2.5, 3e2], {'a': (1, 2)}, k=True, s='it\\'s', n=None)");
check('reader: positional, keyword, nested and signed literals', p && p.fn === 'f' && p.args.length === 5 && p.args[2].name === 'k' && p.args[3].value === "it's");
check('reader: an expression is not a literal call', parseCall('f([0] * 5)') === null && parseCall('f(list(range(3)))') === null && parseCall('f(1) + 1') === null);
check('reader: a call with no arguments', parseCall('f()').args.length === 0);
check('params: read from the starter', paramNames('import math\n\ndef best(prices, k=2, *rest):\n    pass\n').join() === 'prices,k,rest');
check('shape: a sound constraint has no message', constraintShape({ arg: 'xs', type: 'list', of: { type: 'list', len: [1, 5], of: 'int', range: [0, 9] }, sorted: 'desc' }).length === 0);
check('shape: a missing arg, a bad type, a reversed range, an unknown key', constraintShape({ type: 'list' }).length === 1 && constraintShape({ arg: 0, type: 'array' }).length === 1 && constraintShape({ arg: 0, range: [5, 1] }).length === 1 && constraintShape({ arg: 0, colour: 'red' }).length === 1);

const L = (o) => [{ arg: 'xs', type: 'list', of: 'int', ...o }];
check('len: inside passes', clean(L({ len: [1, 3] }), 'f([1, 2])', ['xs']));
check('len: too long is named', /length 4, outside \[1, 3\]/.test(msgs(L({ len: [1, 3] }), 'f([1, 2, 3, 4])', ['xs'])[0]));
check('len: an open end', clean(L({ len: [1, null] }), 'f([1, 2, 3, 4, 5])', ['xs']) && msgs(L({ len: [1, null] }), 'f([])', ['xs']).length === 1);
check('nonEmpty', msgs(L({ nonEmpty: true }), 'f([])', ['xs']).length === 1 && clean(L({ nonEmpty: true }), 'f([0])', ['xs']));
check('range on elements', clean(L({ of: { type: 'int', range: [0, 9] } }), 'f([0, 9])', ['xs']) && /\[1\] is 10/.test(msgs(L({ of: { type: 'int', range: [0, 9] } }), 'f([3, 10])', ['xs'])[0]));
check('type: a float where an int is stated', /\[0\] is a float, not an int/.test(msgs(L({}), 'f([1.5])', ['xs'])[0]));
check('type: a bool is not an int', msgs(L({}), 'f([True])', ['xs']).length === 1);
check('type: number takes ints and floats', clean(L({ of: 'number' }), 'f([1, 2.5])', ['xs']));
check('sorted ascending allows ties', clean(L({ sorted: true }), 'f([1, 1, 2])', ['xs']) && msgs(L({ sorted: true }), 'f([2, 1])', ['xs']).length === 1);
check('sorted descending', clean(L({ sorted: 'desc' }), 'f([3, 2, 2])', ['xs']) && msgs(L({ sorted: 'desc' }), 'f([1, 2])', ['xs']).length === 1);
check('distinct', msgs(L({ distinct: true }), 'f([1, 2, 1])', ['xs']).length === 1 && clean(L({ distinct: true }), 'f([1, 2, 3])', ['xs']));
check('str: length, pattern', clean([{ arg: 0, type: 'str', len: [1, 4], pattern: '[a-z]+' }], "f('abc')") && msgs([{ arg: 0, type: 'str', pattern: '[a-z]+' }], "f('aB')").length === 1);
check('scalar range with a keyword argument', msgs([{ arg: 'k', type: 'int', range: [1, 10] }], 'f([1], k=11)', ['xs', 'k']).length === 1 && clean([{ arg: 'k', type: 'int', range: [1, 10] }], 'f([1], 4)', ['xs', 'k']));
check('2D list: rows and cells', clean([{ arg: 0, type: 'list', len: [1, 3], of: { type: 'list', len: [2, 2], of: 'int', range: [0, 5] } }], 'f([[1, 2], [3, 4]])') && msgs([{ arg: 0, type: 'list', of: { type: 'list', len: [2, 2] } }], 'f([[1, 2], [3]])').length === 1);
check('dict length', clean([{ arg: 0, type: 'dict', len: [1, 2] }], "f({'a': 1})") && msgs([{ arg: 0, type: 'dict', len: [1, 2] }], 'f({})').length === 1);
check('an expression call is skipped, not failed', !checkTest(L({ len: [1, 3] }), { call: 'f([0] * 9)' }, ['xs']).checked);
check('C++ args are read from the JSON array', msgs([{ arg: 0, type: 'list', of: 'int', range: [0, 9] }], '', []).length === 0 && checkTest([{ arg: 0, type: 'list', of: 'int', range: [0, 9] }], { call: 'f', args: [[1, 20]] }).messages.length === 1);
check('strings only: nothing to check, nothing reported', !checkTest(['A string.'], { call: 'f([1])' }).checked);
const rep = drillConstraintReport({ starter: 'def f(xs):\n    pass', constraints: ['text', { arg: 'ys', type: 'list' }], tests: [], examples: [] });
check('an arg that is no parameter is an error', rep.errors.length === 1 && /not a parameter/.test(rep.errors[0].msg));

/* ---------- 2. the validator ---------- */
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-constraints-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const dir = path.join(copy, 'content/drills');
const idxFile = path.join(dir, 'index.json');
const idx = JSON.parse(fs.readFileSync(idxFile, 'utf8'));
const files = fs.readdirSync(dir).filter(f => f.endsWith('.json') && f !== 'index.json').map(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
const real = files.filter(d => d.sample !== true);
const run = () => { const r = spawnSync('node', [path.join(copy, 'tools/validate.mjs'), '--no-manifest'], { cwd: copy, encoding: 'utf8' }); return r.stdout + r.stderr; };
const shipped = run();
const warnCount = (shipped.match(/\[no-constraints\]/g) || []).length;
check('as shipped: 0 errors', /\b0 errors\b/.test(shipped.split('\n').slice(-4).join('\n')), shipped.split('\n').slice(-4).join(' | '));
check('as shipped: every non-sample drill warns once (none states machine constraints yet)', warnCount === real.length, `${warnCount} warnings for ${real.length} drills`);
console.log(`note: ${warnCount} of ${real.length} drills carry [no-constraints]`);
/* a synthetic drill, listed, edited per case */
const base = JSON.parse(fs.readFileSync(path.join(HERE, 'fixtures/drill-page/drill-aa-page.json'), 'utf8'));
const baseFile = path.join(dir, base.id + '.json');
idx.push({ id: base.id, name: base.name, course: base.course, difficulty: base.difficulty }); fs.writeFileSync(idxFile, JSON.stringify(idx, null, 2));
const tryDrill = (name, mutate, expectErr, expectWarn) => {
  const d = JSON.parse(JSON.stringify(base)); mutate(d);
  fs.writeFileSync(baseFile, JSON.stringify(d, null, 2));
  const m = run().split('\n').filter(l => l.includes(`drills/${base.id}.json`));
  const errs = m.filter(l => /^error/.test(l)), warns = m.filter(l => /\[no-constraints\]/.test(l));
  const ok = expectErr === null ? errs.length === 0 : errs.some(l => expectErr.test(l));
  check(`validator: ${name}`, ok && (expectWarn === undefined || (warns.length > 0) === expectWarn), m.join(' | ').slice(0, 400));
};
const cons = (...o) => (d) => { d.constraints = ['A short list.', ...o]; };
tryDrill('satisfied constraints pass and remove the warning', cons({ arg: 'xs', type: 'list', of: 'number', len: [0, 3] }), null, false);
tryDrill('a test that breaks len is an error', cons({ arg: 'xs', type: 'list', len: [1, 1] }), /breaks the drill's stated constraints/);
tryDrill('a test that breaks an element range is an error', cons({ arg: 'xs', of: { type: 'int', range: [0, 2] } }), /outside the range \[0, 2\]/);
tryDrill('an example that breaks a constraint is an error', cons({ arg: 0, len: [4, null] }), /examples\[0\]/);
tryDrill('a malformed constraint is an error', cons({ arg: 0, type: 'array' }), /"type" is one of/);
tryDrill('an unknown parameter name is an error', cons({ arg: 'no_such_parameter', type: 'list' }), /not a parameter/);
tryDrill('constraints that is not an array is an error', (d) => { d.constraints = { arg: 0 }; }, /constraints is an array/);
tryDrill('only text constraints: the [no-constraints] warning and no error', (d) => { d.constraints = ['A short list.']; }, null, true);
tryDrill('a sample drill is not warned', (d) => { d.sample = true; }, null, false);
fs.rmSync(tmp, { recursive: true, force: true });
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
