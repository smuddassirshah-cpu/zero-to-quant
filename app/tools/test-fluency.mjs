#!/usr/bin/env node
/* Tests for generated fluency sets (ENGINE-BACKLOG 815; author side docs/AUTHORING.md section 16).
     Part 1 (plain node): the safe evaluator (every operator and function, every error), every format, poly(), templates and their
             escapes, the family rules (checkFamily), seeds, the weighted order and the distinct-prompt rule.
     Part 2 (Playwright, Chromium): every family of every set (the real sets under content/courses and the fixtures under
             tools/fixtures/fluency) at 50 seeds, graded by the real widgets: the answer is correct, each `wrong` is not, every
             `accept` form is correct, `upToConstant` accepts a constant added, and for a `form` family each expression in the
             prompt typed back is not correct (the grader returns the key `form`). A numeric family is also graded by the node
             mirror in tools/fluency-rules.mjs, which must agree with the widget.
   Usage: node tools/test-fluency.mjs [--local-cdn <pkgs>] [--unit-only] [--seeds 50] [--set <course>/<set id> | fixture/<id>]
   The Compute Engine and MathLive come from --local-cdn (or ZQ_LOCAL_CDN); without them part 2 is skipped with a note, and an
   expression family cannot be graded. Exit 0 pass, 1 failure, 2 setup problem. */
import { spawn, execSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { gen, loadSet, fixtureFiles, APP, numericGrade, typedAnswer, typedValue, grade } from './fluency-rules.mjs';

const argv = process.argv.slice(2);
const val = (k) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : null; };
const localCdn = val('--local-cdn') ? path.resolve(val('--local-cdn')) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const unitOnly = argv.includes('--unit-only'), SEEDS = parseInt(val('--seeds') || '50', 10);
const only = val('--set');
const CHROMIUM = '/opt/pw-browsers/chromium';
const die = (m) => { console.error('test-fluency: ' + m); process.exit(2); };
const fails = []; let total = 0;
const check = (name, ok, detail = '') => { total++; if (!ok) { fails.push(name); console.log(`FAIL ${name}  ${detail}`); } };
const throws = (name, f, re) => { total++; try { f(); fails.push(name); console.log(`FAIL ${name}  did not throw`); } catch (e) { if (!(e instanceof gen.GenError) || (re && !re.test(e.message))) { fails.push(name); console.log(`FAIL ${name}  threw ${e && e.constructor && e.constructor.name}: ${e && e.message}`); } } };

/* ---------- Part 1 ---------- */
const E = (src, env) => gen.evaluate(src, env);
const F = (src, spec = '', env, mode) => gen.format(E(src, env), spec, mode);
const unit = () => {
  /* arithmetic, exact */
  [['2+3*4', '14'], ['(2+3)*4', '20'], ['-2^2', '-4'], ['2^3^2', '512'], ['(-2)^2', '4'], ['2^-2', '0.25'], ['7 % 3', '1'], ['-7 % 3', '2'], ['7 % -3', '-2'],
    ['1/3+1/6', '0.5'], ['0.1+0.2', '0.3'], ['3/4', '0.75'], ['1/3', '\\frac{1}{3}'], ['2/4', '0.5'], ['10/4*2', '5'], ['1 - 2 - 3', '-4'], ['8/2/2', '2'],
    ['(-1)^7', '-1'], ['(-1)^8', '1'], ['(2/3)^2', '\\frac{4}{9}'], ['0^0', '1'], ['3 - -2', '5'], ['+5', '5'], ['fact(20)', '2432902008176640000'], ['2^100', '1267650600228229401496703205376']]
    .forEach(([s, want]) => check(`evaluate ${s}`, F(s) === want, F(s)));
  /* floats appear only from a root or a fractional power */
  check('sqrt(2) is a float to 12 figures', F('sqrt(2)') === '1.41421356237', F('sqrt(2)'));
  check('2^(1/2) is a float', F('2^(1/2)') === '1.41421356237');
  check('sqrt(16/9) stays exact', F('sqrt(16/9)') === '\\frac{4}{3}');
  check('sqrt(2)*sqrt(2) is not an exact 2 but prints as 2', F('sqrt(2)*sqrt(2)') === '2');
  /* functions */
  [['gcd(12,18)', '6'], ['gcd(-12,18)', '6'], ['gcd(0,5)', '5'], ['gcd(12,18,8)', '2'], ['lcm(4,6)', '12'], ['lcm(4,6,10)', '60'], ['lcm(0,3)', '0'], ['abs(-3/2)', '1.5'], ['abs(4)', '4'],
    ['min(3,-2,5)', '-2'], ['max(1/2,1/3)', '0.5'], ['max(2)', '2'], ['floor(-7/2)', '-4'], ['ceil(-7/2)', '-3'], ['floor(7/2)', '3'], ['ceil(7/2)', '4'], ['floor(5)', '5'],
    ['round(5/2)', '3'], ['round(-5/2)', '-3'], ['round(2.675,2)', '2.68'], ['round(1/3,2)', '0.33'], ['round(-1/3,2)', '-0.33'], ['round(1234.5678,0)', '1235'],
    ['sqrt(49)', '7'], ['sqrt(0)', '0'], ['comb(5,2)', '10'], ['comb(5,0)', '1'], ['comb(5,5)', '1'], ['comb(5,7)', '0'], ['comb(52,5)', '2598960'], ['fact(0)', '1'], ['fact(5)', '120'],
    ['sign(-3)', '-1'], ['sign(0)', '0'], ['sign(2/3)', '1']]
    .forEach(([s, want]) => check(`function ${s}`, F(s) === want, F(s)));
  /* comparisons and logic */
  [['1<2 and 2<3', true], ['1>2 or 3==3', true], ['not (1==1)', false], ['1/3 == 2/6', true], ['0.5 == 1/2', true], ['2 != 2', false], ['2 <= 2', true], ['3 >= 4', false], ['not 1 > 2', true],
    ['1 < 2 and 2 < 1 or 3 == 3', true], ["v == 'x'", true, { v: 'x' }], ["v != 'x'", false, { v: 'x' }], ["v == 'y'", false, { v: 'x' }], ['sqrt(4) == 2', true]]
    .forEach(([s, want, env]) => check(`logic ${s}`, E(s, env) === want, String(E(s, env))));
  /* errors are GenError, never another exception, and never run code */
  ['1/0', '5 % 0', 'sqrt(-1)', 'gcd(1.5, 2)', 'lcm(1/2, 3)', 'foo(1)', 'unknown', '2a', 'a = 1', '1 +', '(1', '1)', 'fact(171)', 'fact(-1)', 'comb(5)', 'comb(-1, 2)', 'round(1, 11)', 'min()',
    'x.constructor', 'constructor', '__proto__', 'toString', 'this', 'eval(1)', "Function('return 1')()", 'abs(1,2)', '1 < ', 'not', "v + 1", 'true', '0^-1', '2^500', "'x' + 1", '1 and 2', 'not 1', '3 $ 4', '1 2']
    .forEach((s) => throws(`error: ${s}`, () => E(s, { v: 'x' })));
  check('an id cannot reach Object.prototype', (() => { try { E('hasOwnProperty'); return false; } catch (e) { return e instanceof gen.GenError; } })());
  check('no eval and no Function in gen.js', !/\beval\s*\(|\bnew\s+Function\b|\bFunction\s*\(/.test(fs.readFileSync(path.join(APP, 'js/engine/gen.js'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')));

  /* formats */
  [['3', '', '3'], ['-3', '', '-3'], ['3', '+', '+3'], ['-3', '+', '-3'], ['0', '+', '+0'], ['1', 'c', ''], ['-1', 'c', '-'], ['5', 'c', '5'], ['-5', 'c', '-5'], ['0', 'c', '0'], ['1', '+c', '+'], ['-1', '+c', '-'],
    ['5', '+c', '+5'], ['-5', '+c', '-5'], ['3', '()', '3'], ['-3', '()', '(-3)'], ['-1/2', '()', '(-0.5)'], ['0', '()', '0'], ['3/4', 'frac', '\\frac{3}{4}'], ['-3/4', 'frac', '-\\frac{3}{4}'],
    ['4/2', 'frac', '2'], ['0', 'frac', '0'], ['3/4', '+frac', '+\\frac{3}{4}'], ['-3/4', '+frac', '-\\frac{3}{4}'], ['5', '+frac', '+5'], ['2/3', 'dp2', '0.67'], ['-2/3', 'dp2', '-0.67'],
    ['5', 'dp2', '5.00'], ['1/200', 'dp2', '0.01'], ['-1/300', 'dp2', '0.00'], ['7/2', 'dp0', '4'], ['-7/2', 'dp0', '-4'], ['2/3', '+dp1', '+0.7'], ['-2/3', '+dp1', '-0.7'], ['0', '+dp1', '+0.0'],
    ['sqrt(2)', 'dp3', '1.414'], ['sqrt(2)', '+dp3', '+1.414'], ['1/3', 'dp10', '0.3333333333'], ['3/4', '', '0.75'], ['1/3', '', '\\frac{1}{3}'], ['-1/3', '', '-\\frac{1}{3}'], ['1/8', '', '0.125'],
    ['3/4', 'c', '0.75'], ['-3/4', '+c', '-0.75'], ['sqrt(2)', 'c', '1.41421356237']]
    .forEach(([s, spec, want]) => check(`format {${s}:${spec}}`, F(s, spec) === want, F(s, spec)));
  check('num mode writes 1/3 as n/d', F('1/3', '', undefined, 'num') === '1/3');
  check('num mode writes 3/4 as a decimal', F('3/4', '', undefined, 'num') === '0.75');
  check('num mode keeps whole numbers', F('-6', '', undefined, 'num') === '-6');
  check('a text value passes through', gen.format('x', '') === 'x');
  throws('a format on text', () => gen.format('x', '+'));
  throws('the format +() does not exist', () => gen.format(E('3'), '+()'));
  throws('an unknown format', () => gen.format(E('3'), 'zz'));
  throws('dp11 is refused', () => gen.format(E('3'), 'dp11'));
  throws('a boolean cannot be written', () => gen.format(true, ''));
  /* poly */
  [['x', ['1', '0', '-1'], 'x^2-1'], ['x', ['2', '-1', '0'], '2x^2-x'], ['x', ['0', '0'], '0'], ['x', ['-1', '0', '5'], '-x^2+5'], ['t', ['1', '1'], 't+1'], ['x', ['0', '3', '0'], '3x'],
    ['x', ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'], 'x^{11}+1'], ['x', ['1/2', '-3/2'], '0.5x-1.5'], ['y', ['-1', '-1', '-1'], '-y^2-y-1'], ['x', ['3'], '3'], ['x', ['-1'], '-1'],
    ['x', ['1', '1/3'], 'x+\\frac{1}{3}']]
    .forEach(([v, cs, want]) => check(`poly(${v}; ${cs.join(', ')})`, gen.polyText(v, cs.map((c) => E(c))) === want, gen.polyText(v, cs.map((c) => E(c)))));
  throws('poly with a root coefficient', () => gen.polyText('x', [E('sqrt(2)'), E('1')]));
  /* templates */
  const R = (t, env = {}, mode) => gen.render(t, env, mode);
  const env = { a: E('2'), b: E('-3'), v: 'x', h: E('3/4') };
  check('template: plain, signed, brackets', R('{a}({v}{b:+}) {b:()} {a*b:+}', env) === '2(x-3) (-3) -6', R('{a}({v}{b:+}) {b:()} {a*b:+}', env));
  check('template: braces escaped for LaTeX', R('\\frac{{{a}}}{{{b}}}', env) === '\\frac{2}{-3}', R('\\frac{{{a}}}{{{b}}}', env));
  check('template: x^{{{a}}}', R('x^{{{a}}}', env) === 'x^{2}');
  check('template: an expression before the colon', R('{a*b:+} and {h:frac} and {h*2:dp1}', env) === '-6 and \\frac{3}{4} and 1.5', R('{a*b:+} and {h:frac} and {h*2:dp1}', env));
  check('template: poly through a var that holds a letter', R('{poly(v; a, b, 0)}', env) === '2x^2-3x', R('{poly(v; a, b, 0)}', env));
  check('template: poly through a literal letter', R('{poly(t; 1, a)}', env) === 't+2', R('{poly(t; 1, a)}', env));
  check('template: poly with a function in a coefficient', R('{poly(x; gcd(4, 6), 1)}', env) === '2x+1', R('{poly(x; gcd(4, 6), 1)}', env));
  check('template: a literal-only text is unchanged', R('Find the value.') === 'Find the value.');
  check('template: an escaped pair alone', R('{{}}') === '{}');
  check('template: num mode', R('{h}', env, 'num') === '0.75' && R('{1/3}', env, 'num') === '1/3');
  ['{a', 'a}', '{}', '{a:zz}', '{a:+:c}', '{a b}', '{poly(x 1)}', '{poly(x; )}', '{poly(2; 1)}', '{a:}', '{ }'].forEach((t) => throws(`template error: ${t}`, () => R(t, env)));
  throws('template: an unknown name', () => R('{zz}', env));

  /* family rules */
  const fam = (over = {}) => ({ id: 'f', vars: { a: { int: [2, 9] }, b: { int: [-9, 9], not: [0] } }, let: { p: 'a*b' }, prompt: 'Expand ${a}(x{b:+})$.', widget: { kind: 'expression', answer: '{a}x{p:+}' }, solution: ['${p}$.'], ...over });
  check('a well formed family has no problems', gen.checkFamily(fam()).length === 0, gen.checkFamily(fam()).join('; '));
  const bad = (name, over, re) => { const m = gen.checkFamily(fam(over)); check(`family rule: ${name}`, m.some((x) => re.test(x)), m.join(' | ') || 'no message'); };
  bad('an unknown name in the prompt', { prompt: '${zz}$' }, /"zz" is neither a var nor a let/);
  bad('an unknown function', { let: { p: 'foo(a)' } }, /unknown function "foo"/);
  bad('a let that reads a later let', { let: { p: 'q + 1', q: 'a' } }, /"q" is not a var or an earlier let/);
  bad('a let named like a var', { let: { a: '1' } }, /already a var/);
  bad('a reserved var name', { vars: { gcd: { int: [1, 2] } } }, /reserved/);
  bad('an upper-case var name', { vars: { A: { int: [1, 2] } } }, /starts with a lower-case letter/);
  bad('a var with both int and pick', { vars: { a: { int: [1, 2], pick: [1] } } }, /exactly one of int and pick/);
  bad('a backwards range', { vars: { a: { int: [5, 2] } } }, /low at most high/);
  bad('a fractional bound', { vars: { a: { int: [1.5, 2] } } }, /whole numbers/);
  bad('an empty pick', { vars: { a: { pick: [] } } }, /non-empty/);
  bad('everything excluded', { vars: { a: { int: [1, 2], not: [1, 2] } } }, /every value is excluded/);
  bad('step on pick', { vars: { a: { pick: [1, 2], step: 2 } } }, /step/);
  bad('an unknown var field', { vars: { a: { int: [1, 2], zz: 1 } } }, /unknown field "zz"/);
  bad('a choice widget', { widget: { kind: 'choice', answer: 'a' } }, /"numeric" or "expression"/);
  bad('form on a numeric widget', { widget: { kind: 'numeric', answer: '1', form: 'expanded' } }, /widget\.form/);
  bad('an unknown form', { widget: { kind: 'expression', answer: 'x', form: 'tidy' } }, /widget\.form/);
  bad('an unknown widget field', { widget: { kind: 'expression', answer: 'x', hints: 1 } }, /widget\.hints/);
  bad('a missing answer', { widget: { kind: 'expression' } }, /widget\.answer is required/);
  bad('no solution', { solution: [] }, /solution/);
  bad('a stray brace', { prompt: 'x}' }, /stray/);
  bad('an unclosed brace', { prompt: '{a' }, /never closed/);
  bad('a bad where', { where: ['a ='] }, /where\[0\]/);
  bad('a where naming an unknown var', { where: ['zz > 1'] }, /"zz" is not a var or a let/);
  bad('a wrong without a tex', { wrong: [{ id: 'w' }] }, /wrong\[0\]\.tex is required/);
  bad('a numeric wrong on an expression widget', { wrong: [{ id: 'w', tex: 'x', value: 1 }] }, /use "tex"/);
  bad('wrong ids used twice', { wrong: [{ id: 'w', tex: 'x' }, { id: 'w', tex: 'y' }] }, /used twice/);
  bad('a bad weight', { weight: 0 }, /weight/);
  bad('a field the family does not take', { hint: 'x' }, /unknown field "hint"/);
  bad('a non-kebab id', { id: 'Bad_Id' }, /kebab/);
  bad('an expression accept that is not a list', { widget: { kind: 'expression', answer: 'x', accept: 'x' } }, /accept/);

  /* ENGINE-BACKLOG 830 to 833: the new forms, set answers and a pick of tuples */
  const ok1 = (name, over) => { const m = gen.checkFamily(fam(over)); check(`family rule: ${name}`, m.length === 0, m.join(' | ')); };
  ok1('form factorised-fully', { widget: { kind: 'expression', answer: '2(x+1)(x+2)', form: 'factorised-fully' } });
  ok1('form completed-square', { widget: { kind: 'expression', answer: '(x+1)^2', form: 'completed-square' } });
  ok1('an expression set answer', { widget: { kind: 'expression', answers: ['{a}', '{b}'], unordered: true } });
  ok1('a numeric set answer with a wrong set', { widget: { kind: 'numeric', answers: ['{a}', '{b}'], unordered: true, tol: { abs: 0 } }, wrong: [{ id: 'w', value: '{-a}, {-b}' }] });
  bad('answers with an answer', { widget: { kind: 'expression', answer: 'x', answers: ['1', '2'], unordered: true } }, /not both/);
  bad('answers without unordered', { widget: { kind: 'expression', answers: ['1', '2'] } }, /unordered must be true/);
  bad('unordered without answers', { widget: { kind: 'expression', unordered: true } }, /answers is a list of two or more/);
  bad('one answer only', { widget: { kind: 'expression', answers: ['1'], unordered: true } }, /two or more/);
  bad('answers with form', { widget: { kind: 'expression', answers: ['1', '2'], unordered: true, form: 'simplified' } }, /form is not used with answers/);
  bad('answers with accept (expression)', { widget: { kind: 'expression', answers: ['1', '2'], unordered: true, accept: ['x'] } }, /accept is not used with answers/);
  bad('answers with a per cent unit', { widget: { kind: 'numeric', answers: ['1', '2'], unordered: true, unit: '%' } }, /unit "%"/);
  bad('an unknown name in answers', { widget: { kind: 'expression', answers: ['{a}', '{zz}'], unordered: true } }, /"zz" is neither a var nor a let/);
  const tup = (over) => fam({ vars: { rs: { pick: [[1, 6], [2, 3], [-2, 5]], as: ['r', 's'] } }, let: {}, prompt: 'Roots ${r}$ and ${s}$.', solution: ['${r}$ and ${s}$.'], widget: { kind: 'numeric', answers: ['{r}', '{s}'], unordered: true, tol: { abs: 0 } }, ...over });
  check('tuple pick: a well formed family has no problems', gen.checkFamily(tup()).length === 0, gen.checkFamily(tup()).join('; '));
  const badT = (name, vars, re) => { const m = gen.checkFamily(tup({ vars })); check(`tuple pick rule: ${name}`, m.some((x) => re.test(x)), m.join(' | ') || 'no message'); };
  badT('a tuple of the wrong length', { rs: { pick: [[1, 6], [2]], as: ['r', 's'] } }, /tuples, each with 2/);
  badT('as without a pick', { rs: { int: [1, 3], as: ['r', 's'] } }, /with a pick of tuples/);
  badT('a single name', { rs: { pick: [[1], [2]], as: ['r'] } }, /two or more names/);
  badT('a reserved name', { rs: { pick: [[1, 6]], as: ['r', 'gcd'] } }, /reserved/);
  badT('a name used twice', { a: { int: [1, 2] }, rs: { pick: [[1, 6]], as: ['r', 'a'] } }, /already a var/);
  badT('not with tuples', { rs: { pick: [[1, 6], [2, 3]], as: ['r', 's'], not: [1] } }, /not cannot be used/);
  badT('a pick of tuples without as is not numbers', { rs: { pick: [[1, 6]] } }, /list of numbers or text/);
  const tr = gen.sample(tup(), { seeds: 120, set: 't' });
  check('tuple pick: one draw sets both names, as written, and all tuples appear', tr.failed === 0 && tr.items.every((it) => ['1,6', '2,3', '-2,5'].includes(`${it.vars.r},${it.vars.s}`)) && new Set(tr.items.map((it) => `${it.vars.r},${it.vars.s}`)).size === 3);
  check('tuple pick: the set widget is filled from the tuple', tr.items.every((it) => it.widget.answers.join(',') === `${it.vars.r},${it.vars.s}` && it.widget.unordered === true && typeof it.widget.answers[0] === 'number'));
  check('tuple pick: where may read the names, and no draw is lost to a half-matching tuple', gen.sample(tup({ where: ['r < s'] }), { seeds: 100, set: 't' }).items.every((it) => +it.vars.r < +it.vars.s));
  const nw = gen.sample(tup({ wrong: [{ id: 'w', value: '{-r}, {-s}' }] }), { seeds: 5, set: 't' });
  check('numeric set: a wrong value stays a comma-separated text', nw.failed === 0 && nw.items.every((it) => it.wrong[0].value === `${-it.vars.r}, ${-it.vars.s}`));
  const bt = gen.sample(tup({ wrong: [{ id: 'w', value: 'two, three' }] }), { seeds: 3, set: 't' });
  check('numeric set: a wrong value that is not numbers is an error in the draw', bt.failed === 3);
  const mixed = gen.sample(fam({ vars: { w: { pick: [['up', 1], ['down', -1]], as: ['word', 'g'] } }, let: {}, where: ["(word == 'up' and g == 1) or (word == 'down' and g == -1)"], prompt: 'Go ${g}$ {word}.', solution: ['${g}$.'], widget: { kind: 'expression', answer: '{g}x' } }), { seeds: 60, set: 't' });
  check('tuple pick: text and numbers in one tuple, no draw rejected', mixed.failed === 0 && mixed.rejected === 0 && mixed.items.every((it) => (it.vars.word === 'up') === (it.vars.g === '1')));

  /* drawing */
  const f1 = fam({ vars: { a: { int: [2, 9] }, b: { int: [-9, 9], not: [0] }, c: { int: [0, 20], step: 5 }, v: { pick: ['x', 'y'] } }, let: { p: 'a*b' }, where: ['gcd(a, abs(b)) == 1'],
    prompt: '{v}: {a} {b:+} {c}', wrong: [{ id: 'w', tex: '{a}{v}{b:+}', line: 'Line {a}.' }] });
  const run = gen.sample(f1, { seeds: 200, set: 't' });
  check('draw: where holds in every draw', run.items.every((it) => { const [a, b] = [Number(it.vars.a), Number(it.vars.b)]; const g = (x, y) => (y ? g(y, x % y) : Math.abs(x)); return g(a, Math.abs(b)) === 1; }));
  check('draw: not is honoured', run.items.every((it) => it.vars.b !== '0'));
  check('draw: step is honoured', run.items.every((it) => [0, 5, 10, 15, 20].includes(Number(it.vars.c))));
  check('draw: pick draws the text values', run.items.every((it) => ['x', 'y'].includes(it.vars.v)) && new Set(run.items.map((it) => it.vars.v)).size === 2);
  check('draw: a signed var reads back as text', run.items.every((it) => it.prompt.includes(it.vars.v)));
  check('draw: rejected draws are counted', run.rejected > 0 && run.attempts > 200, `${run.rejected} of ${run.attempts}`);
  check('draw: the same seed gives the same items', JSON.stringify(gen.sample(f1, { seeds: 20, set: 't' }).items) === JSON.stringify(gen.sample(f1, { seeds: 20, set: 't' }).items));
  check('draw: another set name draws other items', JSON.stringify(gen.sample(f1, { seeds: 20, set: 't' }).items) !== JSON.stringify(gen.sample(f1, { seeds: 20, set: 'u' }).items));
  check('draw: the wrong line is rendered', run.items.every((it) => it.wrong[0].line === `Line ${it.vars.a}.`));
  const never = gen.sample(fam({ where: ['a > 100'] }), { seeds: 5, set: 't' });
  check('draw: a where that never holds fails every draw, and says why', never.failed === 5 && never.rejected === never.attempts);
  const erring = gen.sample(fam({ let: { p: 'sqrt(0 - a)' } }), { seeds: 5, set: 't' });
  check('draw: an evaluation error is reported, not thrown', erring.failed === 5 && /negative/.test(erring.errors[0][0]));
  const zero = gen.sample(fam({ let: { p: 'a / 0' } }), { seeds: 5, set: 't' });
  check('draw: a let that divides by zero rejects the draw, with no error (838)', zero.failed === 5 && zero.rejected === zero.attempts && zero.errors.length === 0);
  const zeroWhere = gen.sample(fam({ where: ['a / 0 > 1'] }), { seeds: 5, set: 't' });
  check('draw: a where that divides by zero is still an error', zeroWhere.failed === 5 && /division by zero/.test(zeroWhere.errors[0][0]));
  const set = { id: 'set-x', n: 20, families: [fam({ id: 'one', weight: 2 }), fam({ id: 'two', prompt: 'T ${a}(x{b:+})$.' }), fam({ id: 'three', prompt: 'H ${a}(x{b:+})$.' })] };
  const order = gen.schedule(set.families, 20);
  check('weights: a weight-2 family takes half the turns', order.filter((i) => i === 0).length === 10 && order.filter((i) => i === 1).length === 5 && order.filter((i) => i === 2).length === 5, order.join(''));
  check('weights: the order is round robin, not blocks', order.slice(0, 4).join('') !== '0000' && new Set(order.slice(0, 4)).size === 3);
  const items = gen.generate(set, 'seed-1');
  check('generate: n items', items.length === 20, String(items.length));
  check('generate: no two the same prompt', new Set(items.map((it) => it.prompt)).size === 20);
  check('generate: the families come in by weight', items.filter((it) => it.family === 'one').length === 10);
  check('generate: the same seed, the same set', JSON.stringify(gen.generate(set, 'seed-1')) === JSON.stringify(items));
  check('generate: another seed, another set', JSON.stringify(gen.generate(set, 'seed-2').map((x) => x.prompt)) !== JSON.stringify(items.map((x) => x.prompt)));
  const pi = gen.playerItem(items[0], set, 0);
  check('playerItem: the runSet shape', pi.id === 'set-x-1' && pi.question === items[0].prompt && pi.widget.kind === 'expression' && pi.feedback.generic.length > 0 && pi.explain.text.length > 0 && pi.generated === true);
  const wi = gen.generate({ id: 's', n: 5, families: [fam({ id: 'w', wrong: [{ id: 'slip', tex: '{a}x', line: 'Slip.' }] })] }, 3).map((it, k) => gen.playerItem(it, { id: 's' }, k))[0];
  check('playerItem: the wrong line comes first, then the solution', /^Slip\. /.test(wi.feedback.byKey.slip) && wi.feedback.byKey.slip.includes(wi.feedback.generic) && wi.widget.wrong[0].id === 'slip');
  check('rng: the same stream as ZQ.arith.rng', (() => { const r = gen.rng('abc'); const r2 = gen.rng('abc'); return r() === r2() && r() === r2(); })());
  check('passMark: 18 of 20 at 0.9, 9 of 10, defaults', gen.passMark({ pass: 0.9 }, 20) === 18 && gen.passMark({ pass: 0.9 }, 10) === 9 && gen.passMark({}, 20) === 18 && gen.passMark({ pass: 0.85 }, 20) === 17);
  /* the fixtures draw cleanly */
  fixtureFiles().forEach((f) => {
    const d = JSON.parse(fs.readFileSync(f, 'utf8'));
    if (path.basename(f) === 'fluency-l1-letters-for-numbers.json') { check('fixture fluency-l1-letters-for-numbers.json: a sample set with the authoring-reach families (838 to 841)', d.sample === true && d.families.length === 9 && d.families.some((x) => x.widget.form === 'fraction') && d.families.some((x) => x.widget.form === 'exact-angle')); return; }
    check(`fixture ${path.basename(f)}: has the four families the brief names (numeric, expanded, factorised, upToConstant)`,
      d.sample === true && d.families.some((x) => x.widget.kind === 'numeric') && d.families.some((x) => x.widget.form === 'expanded') && d.families.some((x) => x.widget.form === 'factorised') && d.families.some((x) => x.widget.upToConstant));
    check(`fixture ${path.basename(f)}: a full attempt draws 20 items`, gen.generate(d, 11).length === 20);
  });
};

/* ---------- Part 2 ---------- */
const sets = () => {
  const out = [];
  if (only) { const { doc, course } = loadSet(only); out.push({ ref: only, course, doc }); return out; }
  const dir = path.join(APP, 'content/courses');
  for (const c of fs.existsSync(dir) ? fs.readdirSync(dir) : []) {
    const d = path.join(dir, c);
    if (!fs.statSync(d).isDirectory()) continue;
    for (const f of fs.readdirSync(d).filter((x) => /^fluency-.+\.json$/.test(x))) out.push({ ref: `${c}/${f.slice(0, -5)}`, course: c, doc: JSON.parse(fs.readFileSync(path.join(d, f), 'utf8')) });
  }
  fixtureFiles().forEach((f) => { const doc = JSON.parse(fs.readFileSync(f, 'utf8')); out.push({ ref: `fixture/${path.basename(f, '.json')}`, course: doc.course, doc }); });
  return out;
};
const loadPlaywright = async () => {
  try { return await import('playwright'); } catch { /* not local */ }
  const roots = [];
  try { roots.push(execSync('npm root -g', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()); } catch { /* no npm */ }
  (process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).forEach((p) => roots.push(p));
  for (const r of roots) { const f = path.join(r, 'playwright', 'index.mjs'); if (fs.existsSync(f)) return import(pathToFileURL(f).href); }
  die('Playwright is not installed (npm i -g playwright)');
};
const freePort = () => new Promise((res, rej) => { const s = net.createServer(); s.unref(); s.on('error', rej); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); });
const MIME = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm' };
const cdnFile = (u) => {
  let m;
  if ((m = u.pathname.match(/^\/npm\/(@[^/]+\/[^@/]+|[^@/]+)@([^/]+)\/(.*)$/))) return path.join(localCdn, `${m[1].replace(/^@/, '').replace('/', '-')}-${m[2]}`, 'package', m[3]);
  return null;
};
const mathSegments = (prompt) => (String(prompt).match(/\$[^$]+\$/g) || []).map((x) => x.slice(1, -1));

const browser = async () => {
  const list = sets();
  if (!list.length) { console.log('note: no fluency sets to grade'); return; }
  const { chromium } = await loadPlaywright();
  const port = await freePort();
  const proc = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', APP], { stdio: 'ignore' });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 100; i++) { try { if ((await fetch(base + '/index.html')).ok) break; } catch { /* not up */ } await new Promise((r) => setTimeout(r, 100)); }
  const b = await chromium.launch({ headless: true, ...(fs.existsSync(CHROMIUM) ? { executablePath: CHROMIUM } : {}) });
  try {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 860 } });
    await ctx.route(/^https:\/\/cdn\.jsdelivr\.net\//, async (route) => {
      const f = cdnFile(new URL(route.request().url()));
      if (f && fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
      return route.fulfill({ status: 404, body: '' });
    });
    await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, (r) => r.fulfill({ status: 200, body: '', headers: { 'content-type': 'text/css' } }));
    const page = await ctx.newPage();
    page.on('pageerror', (e) => { check('no uncaught error in the page', false, String(e).slice(0, 200)); });
    await page.goto(base + '/#today');
    await page.waitForFunction(() => window.ZQ && ZQ.widgets && ZQ.grade && ZQ.gen, null, { timeout: 30000 });
    /* the engine in the page must be the one the node tools use: same items for the same seed */
    const probe = list[0];
    const nodeItems = gen.generate(probe.doc, 'probe-1').map((x) => x.prompt).join('|');
    const pageItems = await page.evaluate((d) => ZQ.gen.generate(d, 'probe-1').map((x) => x.prompt).join('|'), probe.doc);
    check('the page draws the same items as node for the same seed', nodeItems === pageItems, 'engine differs between the browser and node');
    /* ENGINE-BACKLOG 842: the saved record is keyed by course and set id; two courses may share a set id and must not share a record */
    const keyed = await page.evaluate(() => {
      const F = ZQ.state.fluency, saved = ZQ.state.doc.fluency; const k1 = 'zz-one/fluency-shared', k2 = 'zz-two/fluency-shared';
      F.result({ course: 'zz-one', id: 'fluency-shared', right: 19, n: 20, passed: true, families: { a: [19, 1] } });
      F.result({ course: 'zz-two', id: 'fluency-shared', right: 4, n: 20, passed: false, families: { b: [4, 16] } });
      const a = F.get('zz-one', 'fluency-shared'), b = F.get('zz-two', 'fluency-shared');
      const out = { a: a && [a.attempts, a.best, !!a.passedAt, Object.keys(a.families).join()], b: b && [b.attempts, b.best, !!b.passedAt, Object.keys(b.families).join()], keys: [k1 in saved, k2 in saved, 'fluency-shared' in saved] };
      delete saved[k1]; delete saved[k2];
      return out;
    });
    check('two courses with one set id keep separate records', JSON.stringify(keyed) === JSON.stringify({ a: [1, 19, true, 'a'], b: [1, 4, false, 'b'], keys: [true, true, false] }), JSON.stringify(keyed));
    const maths = await page.evaluate(() => ZQ.grade.maths().then((m) => !!(m && m.ce && m.mathlive)));
    if (!maths) console.log('note: the Compute Engine or MathLive did not load (give --local-cdn <pkgs>); expression families are skipped');
    for (const s of list) {
      for (const f of s.doc.families || []) {
        const tag = `${s.ref} ${f.id}`;
        if (gen.checkFamily(f).length) { check(`${tag}: well formed`, false, gen.checkFamily(f)[0]); continue; }
        const numeric = f.widget.kind === 'numeric';
        if (!numeric && !maths) continue;
        const r = gen.sample(f, { seeds: SEEDS, set: s.doc.id });
        check(`${tag}: draws ${SEEDS} items`, r.failed === 0, `${r.failed} failed`);
        /* one job per item: [{ spec, tries: [{ text, want: 'ok'|'no', what }] }] */
        const jobs = r.items.map((it) => {
          const w = { ...it.widget, wrong: it.wrong.map((x) => { const o = { id: x.id }; if (x.tex !== undefined) o.tex = x.tex; if (x.value !== undefined) { o.value = x.value; if (x.tol) o.tol = x.tol; } return o; }) };
          const tries = [];
          const setTries = (vals) => {   // a set answer (ENGINE-BACKLOG 832): any order, labels, "or", one value short, one too many
            const all = vals;
            tries.push({ text: all.join(', '), want: 'ok', what: 'set answer' });
            tries.push({ text: all.slice().reverse().join(', '), want: 'ok', what: 'set answer reversed' });
            tries.push({ text: all.map((x) => `x = ${x}`).join(' or '), want: 'ok', what: 'set answer as x = a or x = b' });
            tries.push({ text: all.slice(1).join(', '), want: 'no', what: 'a value missing', key: 'count' });
            tries.push({ text: [...all, all[0]].join(', '), want: 'no', what: 'a value too many', key: 'count' });
            if (!numeric && all.length === 2) {   // a \pm b when the two values are a + b and a - b
              const i = all[0].lastIndexOf('+');
              if (i > 0 && all[0].slice(0, i) + '-' + all[0].slice(i + 1) === all[1]) tries.push({ text: `${all[0].slice(0, i)}\\pm ${all[0].slice(i + 1)}`, want: 'ok', what: 'a \\pm b' });
            }
          };
          if (it.widget.answers) {
            setTries(it.widget.answers.map((a) => (numeric ? grade().fmtNum(+a) : a)));
            it.wrong.forEach((x) => tries.push({ text: numeric ? x.value : x.tex, want: 'no', what: `wrong ${x.id}`, id: x.id }));
          } else if (numeric) {
            tries.push({ text: typedAnswer(it), want: 'ok', what: 'answer' });
            it.wrong.forEach((x) => tries.push({ text: typedValue(it.widget, x.value), want: 'no', what: `wrong ${x.id}`, id: x.id }));
          } else {
            tries.push({ text: it.widget.answer, want: 'ok', what: 'answer' });
            [].concat(it.widget.accept || []).forEach((a) => tries.push({ text: a, want: 'ok', what: 'accept' }));
            it.wrong.forEach((x) => tries.push({ text: x.tex, want: 'no', what: `wrong ${x.id}`, id: x.id }));
            if (it.widget.upToConstant) tries.push({ text: `${it.widget.answer}+7`, want: 'ok', what: 'answer plus a constant' });
            if (it.widget.form) mathSegments(it.prompt).forEach((m) => tries.push({ text: m, want: 'no', what: `the prompt's own "${m}" typed back (form ${it.widget.form})` }));
          }
          return { spec: w, seed: it.seed, prompt: it.prompt, tries };
        });
        const got = await page.evaluate(async (jobs) => {
          const out = [], host = document.createElement('div'); document.body.append(host);
          for (const j of jobs) {
            host.innerHTML = '';
            const wdg = ZQ.widgets.create(host, j.spec, {});
            const res = [];
            for (const t of j.tries) { wdg.reset ? wdg.reset() : null; wdg.set(t.text); const g = await wdg.grade(); res.push({ ok: !!g.ok, key: g.key ?? null }); }
            if (wdg.destroy) wdg.destroy();
            out.push(res);
          }
          host.remove();
          return out;
        }, jobs);
        const bad = { answer: 0, wrongOk: 0, formOk: 0, mirror: 0, route: 0, key: 0 };
        const first = [];
        jobs.forEach((j, ji) => j.tries.forEach((t, ti) => {
          const g = got[ji][ti];
          const wantOk = t.want === 'ok';
          if (g.ok !== wantOk) { first.length < 3 && first.push(`seed ${j.seed} ${j.prompt}: ${t.what} "${t.text}" was ${g.ok ? 'correct' : 'not correct'}`); if (wantOk) bad.answer++; else if (t.what.startsWith('wrong')) bad.wrongOk++; else bad.formOk++; }
          if (numeric) { const m = numericGrade(j.spec, t.text); if (m.ok !== g.ok) bad.mirror++; }
          if (!wantOk && t.id && g.key !== t.id) bad.route++;
          if (t.key && g.key !== t.key) { bad.key++; first.length < 3 && first.push(`seed ${j.seed} ${j.prompt}: ${t.what} "${t.text}" returned key ${g.key}, not ${t.key}`); }
        }));
        check(`${tag}: the answer is graded correct (every accept form, a constant for upToConstant)`, bad.answer === 0, `${bad.answer} failures; ${first.join(' || ')}`);
        check(`${tag}: no wrong is graded correct`, bad.wrongOk === 0, `${bad.wrongOk} failures; ${first.join(' || ')}`);
        if (f.widget.form) check(`${tag}: form ${f.widget.form} is enforced (the prompt's own expression typed back fails)`, bad.formOk === 0, `${bad.formOk} failures; ${first.join(' || ')}`);
        if (f.widget.answers) check(`${tag}: a set answer is graded in any order, and a missing or extra value returns the key count`, bad.key === 0, `${bad.key} failures; ${first.join(' || ')}`);
        if (numeric) check(`${tag}: the node mirror grades as the widget does`, bad.mirror === 0, `${bad.mirror} differences`);
        if (bad.route) console.log(`note  ${tag}: ${bad.route} wrong answers were matched to another wrong id (a coinciding draw; the line shown is the other one's)`);
      }
      console.log(`done  ${s.ref}: ${(s.doc.families || []).length} families at ${SEEDS} seeds`);
    }
    await ctx.close();
  } finally { await b.close(); proc.kill(); }
};

unit();
const main = async () => {
  if (!unitOnly) {
    if (!localCdn || !fs.existsSync(path.join(localCdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'))) console.log('note: no local Compute Engine (give --local-cdn <pkgs>); the browser grading still runs where the network reaches the CDN, else the expression families are skipped');
    await browser();
  }
  console.log(`test-fluency: ${total - fails.length}/${total} passed${fails.length ? `, ${fails.length} FAILED` : ''}`);
  process.exit(fails.length ? 1 : 0);
};
main().catch((e) => { console.error(e); process.exit(2); });
