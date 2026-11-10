#!/usr/bin/env node
/* Unit tests for ENGINE-BACKLOG 838 to 841 (authoring reach of Fluency families; docs/AUTHORING.md section 16), plain node, no browser:
     838  let and where: ln, log10, exp, sin, cos, tan (radians), pi and if(cond, a, b); a where on vars alone is tested before any let;
          a let that divides by zero rejects the draw
     839  a wrong[] entry with `when`
     840  formats cfrac, +cfrac, (frac), sfN, +sfN; placeholders mono(v; c, k) and falling(n; r); poly drops power 1
     841  the text shapes of form "fraction" and "exact-angle" (the grading with the real widgets is in tools/test-answer-forms.mjs)
   Usage: node tools/test-fluency-reach.mjs. One FAIL line per failure and a summary; exit 1 on any failure. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const gen = createRequire(import.meta.url)('../js/engine/gen.js');
const g = { console, setTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g); g.ZQ = {};
vm.runInContext(fs.readFileSync(path.join(APP, 'js/engine/grade.js'), 'utf8'), g);
const G = g.ZQ.grade;

let n = 0; const fails = [];
const check = (name, ok, detail = '') => { n++; if (!ok) { fails.push(name); console.log(`FAIL ${name}  ${detail}`); } };
const R = (t, env = {}, mode) => { try { return gen.render(t, env, mode); } catch (e) { return 'ERR ' + e.message; } };
const Q = (a, b = 1) => gen.evaluate(`${a}/${b}`);
const E = (src, env) => gen.evaluate(src, env);
const near = (v, x, tol = 1e-12) => typeof v === 'number' && Math.abs(v - x) < tol;
const throws = (name, fn, re) => { let m = null; try { fn(); } catch (e) { m = String(e.message); } check(name, m !== null && (!re || re.test(m)), String(m)); };

/* ---------- 838: functions, pi, if ---------- */
check('ln(1) is exactly 0, ln(10) a float', E('ln(1)').n === 0n && near(E('ln(10)'), Math.LN10));
check('log10 of a power of ten is exact', E('log10(1000)').n === 3n && E('log10(1/100)').n === -2n && near(E('log10(50)'), Math.log10(50)));
check('exp(0) is exactly 1, exp(1) a float', E('exp(0)').n === 1n && near(E('exp(1)'), Math.E));
check('sin, cos, tan in radians', near(E('sin(pi/6)'), 0.5, 1e-12) && near(E('cos(pi)'), -1) && near(E('tan(pi/4)'), 1, 1e-12) && E('sin(0)').n === 0n && E('cos(0)').n === 1n && E('tan(0)').n === 0n);
check('pi is a constant', near(E('pi'), Math.PI) && near(E('2*pi'), 2 * Math.PI) && R('{pi:dp5}') === '3.14159');
check('a degrees form through pi', R('{sin(30*pi/180):dp3}') === '0.500' && R('{cos(60*pi/180):dp3}') === '0.500');
check('ln(97)/ln(4) to 4 dp', R('{ln(97)/ln(4):dp4}') === '3.3000');
throws('ln of zero', () => E('ln(0)'), /not positive/);
throws('log10 of a negative', () => E('log10(-1)'), /not positive/);
throws('ln of text', () => E("ln('x')"), /needs numbers/);
throws('sin takes one argument', () => E('sin(1, 2)'), /takes 1/);
check('if picks a branch', E('if(1 < 2, 5, 7)').n === 5n && E('if(1 > 2, 5, 7)').n === 7n);
check('if evaluates only the chosen branch', E('if(2 > 1, 5, 1/0)').n === 5n && E('if(b != 0, a / b, 0)', { a: Q(6), b: Q(0) }).n === 0n);
throws('if needs a condition', () => E('if(1, 2, 3)'), /condition/);
throws('if takes three arguments', () => E('if(1 < 2, 3)'), /takes 3/);
check('pi and the new functions are reserved names', gen.checkFamily({ id: 'a', vars: { pi: { int: [1, 2] } }, prompt: 'x', widget: { kind: 'numeric', answer: '1' }, solution: ['x'] }).some((m) => /reserved/.test(m)) && gen.checkFamily({ id: 'a', vars: { sin: { int: [1, 2] } }, prompt: 'x', widget: { kind: 'numeric', answer: '1' }, solution: ['x'] }).some((m) => /reserved/.test(m)));
check('pi is not an unknown name in a static check', gen.checkFamily({ id: 'a', vars: { a: { int: [1, 2] } }, let: { p: 'sin(a * pi / 2)' }, prompt: '{pi:dp2} {p:dp1}', widget: { kind: 'numeric', answer: '{p}' }, solution: ['{p}'] }).length === 0);
const fam = (extra = {}) => ({ id: 'f', vars: { a: { int: [1, 9] }, b: { int: [-2, 2] } }, prompt: 'P ${a} {b}$.', widget: { kind: 'numeric', answer: '{a}', tol: { abs: 0 } }, wrong: [{ id: 'w', value: '{a + 1}', line: 'L' }], solution: ['S {a}.'], ...extra });
const zero = gen.sample(fam({ let: { r: 'a / b' } }), { seeds: 100, set: 't' });
check('a let that divides by zero rejects the draw and raises no error', zero.errors.length === 0 && zero.failed === 0 && zero.rejected > 0 && zero.items.every((it) => it.vars.b !== '0'), `${zero.errors.length} errors, ${zero.rejected} rejected`);
const early = gen.sample(fam({ let: { r: 'a / b' }, where: ['b != 0'] }), { seeds: 100, set: 't' });
check('a where on vars alone is tested first, so the let never runs on the excluded draws', early.errors.length === 0 && early.failed === 0);
const order = [];
const ordered = gen.sample(fam({ let: { r: 'a / b' }, where: ['r > 0', 'b != 0'] }), { seeds: 100, set: 't' });
check('a where that needs a let still waits for the let, and the early where still runs first', ordered.errors.length === 0 && ordered.items.every((it) => Number(it.vars.b) !== 0 && Number(it.lets.r) > 0), JSON.stringify(ordered.errors));
const sameRng = gen.sample(fam({ let: { r: 'a / b' }, where: ['b != 0'] }), { seeds: 30, set: 't' }), sameRng2 = gen.sample(fam({ let: { r: 'a / b' } }), { seeds: 30, set: 't' });
check('the early where does not change which draws are accepted', JSON.stringify(sameRng.items.map((x) => x.vars)) === JSON.stringify(sameRng2.items.map((x) => x.vars)));
const withCond = gen.sample(fam({ let: { r: 'if(b == 0, 0, a / b)' } }), { seeds: 20, set: 't' });
check('if(b == 0, 0, a / b) keeps the zero draw', withCond.failed === 0 && withCond.items.some((it) => it.vars.b === '0'));

/* ---------- 839: when ---------- */
const wh = gen.sample(fam({ wrong: [{ id: 'always', value: '{a + 1}', line: 'A' }, { id: 'later', value: '{a + 2}', line: 'B', when: 'a > 5' }] }), { seeds: 100, set: 't' });
check('a wrong with when is offered only where the condition holds', wh.items.every((it) => it.wrong.some((x) => x.id === 'always') && it.wrong.some((x) => x.id === 'later') === (Number(it.vars.a) > 5)) && wh.items.some((it) => it.wrong.length === 1) && wh.items.some((it) => it.wrong.length === 2));
const whLet = gen.sample(fam({ let: { p: 'a * 2' }, wrong: [{ id: 'x', value: '{p}', line: 'A', when: 'p != a * 2 or a > 4' }] }), { seeds: 50, set: 't' });
check('when can use lets', whLet.items.every((it) => it.wrong.length === (Number(it.vars.a) > 4 ? 1 : 0)));
check('when with a condition on a text var', gen.sample({ id: 'f', vars: { v: { pick: ['x', 'y'] }, a: { int: [1, 3] } }, prompt: 'P ${v}$ {a}.', widget: { kind: 'numeric', answer: '{a}' }, wrong: [{ id: 'w', value: '{a + 1}', line: 'L', when: "v == 'x'" }], solution: ['S'] }, { seeds: 30, set: 't' }).items.every((it) => it.wrong.length === (it.vars.v === 'x' ? 1 : 0)));
const bad = (name, f, re) => { const m = gen.checkFamily(f); check(name, m.some((x) => re.test(x)), m.join('; ')); };
bad('when must be text', fam({ wrong: [{ id: 'w', value: '{a}', when: 3 }] }), /when: a condition in text/);
bad('when must use known names', fam({ wrong: [{ id: 'w', value: '{a}', when: 'zz > 1' }] }), /when: "zz" is not a var or a let/);
bad('when must use known functions', fam({ wrong: [{ id: 'w', value: '{a}', when: 'foo(a) > 1' }] }), /unknown function "foo"/);
check('when is an allowed field', gen.checkFamily(fam({ wrong: [{ id: 'w', value: '{a}', when: 'a > 1' }] })).length === 0);
const notBool = gen.sample(fam({ wrong: [{ id: 'w', value: '{a}', when: 'a + 1' }] }), { seeds: 3, set: 't' });
check('a when that is not a condition is an error on the draw', notBool.failed === 3 && /not a condition/.test(notBool.errors[0][0]));
const never = gen.sample(fam({ wrong: [{ id: 'w', value: '{a}', when: 'a > 100' }] }), { seeds: 20, set: 't' });
check('a wrong that is never offered leaves an empty list', never.items.every((it) => it.wrong.length === 0));

/* ---------- 840: formats ---------- */
const env = { v: 'x', h: Q(1, 2), a: Q(1), b: Q(-1), m: Q(-1, 3), r: Q(7, 4), z: Q(0) };
const eqs = [
  ['{a:cfrac}x', 'x'], ['{b:cfrac}x', '-x'], ['{h:cfrac}x', '\\frac{1}{2}x'], ['{m:cfrac}x', '-\\frac{1}{3}x'], ['{r:cfrac}', '\\frac{7}{4}'], ['{3:cfrac}x', '3x'], ['{-3:cfrac}x', '-3x'], ['{z:cfrac}', '0'],
  ['{a:+cfrac}x', '+x'], ['{b:+cfrac}x', '-x'], ['{h:+cfrac}x', '+\\frac{1}{2}x'], ['{m:+cfrac}x', '-\\frac{1}{3}x'], ['{3:+cfrac}x', '+3x'], ['{z:+cfrac}', '+0'],
  ['{m:(frac)}', '\\left(-\\frac{1}{3}\\right)'], ['{r:(frac)}', '\\frac{7}{4}'], ['{b:(frac)}', '(-1)'], ['{a:(frac)}', '1'], ['{-5:(frac)}', '(-5)'], ['{m*3:(frac)}', '(-1)'],
  ['{1234.5:sf2}', '1200'], ['{0.0034567:sf3}', '0.00346'], ['{9.996:sf3}', '10.0'], ['{2/3:sf3}', '0.667'], ['{5:sf3}', '5.00'], ['{97:sf1}', '100'], ['{-0.5:sf1}', '-0.5'], ['{12345678:sf3}', '12300000'],
  ['{100:sf3}', '100'], ['{99.95:sf3}', '100'], ['{0.5:sf1}', '0.5'], ['{0.95:sf1}', '1'], ['{ln(97)/ln(4):sf3}', '3.30'], ['{exp(10):sf4}', '22030'], ['{0:sf3}', '0.00'], ['{a:+sf2}', '+1.0'], ['{b:+sf2}', '-1.0'], ['{1/3:sf10}', '0.3333333333'],
  ['{mono(v; 1, 2)}', 'x^2'], ['{mono(v; -1, 2)}', '-x^2'], ['{mono(v; 3, 1)}', '3x'], ['{mono(v; -3, 1)}', '-3x'], ['{mono(v; 1, 1)}', 'x'], ['{mono(v; -1, 1)}', '-x'], ['{mono(v; 5, 0)}', '5'], ['{mono(v; 1, 0)}', '1'], ['{mono(v; -1, 0)}', '-1'],
  ['{mono(v; 0, 3)}', '0'], ['{mono(v; h, 3)}', '\\frac{1}{2}x^3'], ['{mono(v; -h, 10)}', '-\\frac{1}{2}x^{10}'], ['{mono(v; 2, -1)}', '2x^{-1}'], ['{mono(v; 2, h)}', '2x^{\\frac{1}{2}}'], ['{mono(y; 4, 9)}', '4y^9'], ['{mono(t; 2*3, 4 - 1)}', '6t^3'],
  ['{poly(v; 1, 0)}', 'x'], ['{poly(v; 1, 0, 1)}', 'x^2+1'], ['{poly(v; -1, 5)}', '-x+5'], ['{poly(v; 0, 0)}', '0'],
  ['{falling(10; 4)}', '10 \\times 9 \\times 8 \\times 7'], ['{falling(7; 1)}', '7'], ['{falling(5; 5)}', '5 \\times 4 \\times 3 \\times 2 \\times 1'], ['{falling(3 + 4; 2)}', '7 \\times 6'],
];
eqs.forEach(([t, want]) => check(`render ${t}`, R(t, env) === want, R(t, env)));
const surd = { r: '\\sqrt{3}' };
check('poly writes a surd variable (a text var holding a surd)', R('{poly(r; 2, -1)}', surd) === '2\\sqrt{3}-1' && R('{poly(r; 1, 4)}', surd) === '\\sqrt{3}+4' && R('{poly(r; 0, 4)}', surd) === '4');
check('mono writes a surd variable too', R('{mono(r; 2, 1)}', surd) === '2\\sqrt{3}');
['{m:+(frac)}', '{a:sf0}', '{a:sf11}', '{a:dp11}', '{a:zz}', '{a:+()}'].forEach((t) => throws(`format error ${t}`, () => gen.template(t), /unknown format/));
throws('falling needs n at least r', () => R('{falling(3; 4)}', {}) === 'x' || gen.render('{falling(3; 4)}', {}), /at least/);
throws('falling takes at least one factor', () => gen.render('{falling(3; 0)}', {}), /1 to 20/);
throws('falling needs whole numbers', () => gen.render('{falling(3.5; 2)}', {}), /whole number/);
throws('mono needs an exact coefficient', () => gen.render('{mono(v; sqrt(2), 2)}', { v: 'x' }), /exact/);
throws('mono takes v; c, k', () => gen.template('{mono(v; 2)}'), /coefficient and a power/);
throws('mono needs a semicolon', () => gen.template('{mono(v, 2, 3)}'), /mono needs/);
throws('falling takes two arguments', () => gen.template('{falling(3)}'), /falling takes/);
check('the static check reads mono and falling', gen.checkFamily(fam({ prompt: 'P ${mono(a; b, 2)}$ ${falling(a; zz)}.' })).some((m) => /"zz" is neither a var nor a let/.test(m)) && gen.checkFamily(fam({ prompt: 'P ${mono(v; a, 2)}$.' })).length === 0);

/* ---------- 841: the text shapes ---------- */
['\\frac{7}{9}', '-\\frac{7}{9}', '\\frac{-7}{9}', '7/9', '3', '-3', '\\dfrac{7}{9}'].forEach((t) => check(`fraction yes: ${t}`, G.shapeFraction(t)));
['0.7778', '\\frac{14}{18}', '14/18', '\\frac{4}{1}', '\\frac{0}{5}', '1\\frac{2}{3}', '', '\\frac{7.5}{9}'].forEach((t) => check(`fraction no: "${t}"`, !G.shapeFraction(t)));
['\\pi', '3\\pi', '\\frac{\\pi}{12}', '\\frac{5\\pi}{12}', '-\\frac{\\pi}{4}', '\\frac{5}{12}\\pi', '5\\pi/12', '0'].forEach((t) => check(`exact-angle yes: ${t}`, G.shapeExactAngle(t)));
['15^\\circ', '15\\degree', '15°', '\\frac{15\\pi}{180}', '\\frac{2\\pi}{4}', '0.25\\pi', '\\frac{\\pi}{1}'].forEach((t) => check(`exact-angle no: ${t}`, !G.shapeExactAngle(t)));
check('the two forms are allowed on an expression widget and not on a numeric one', gen.checkFamily({ id: 'a', vars: { a: { int: [1, 2] } }, prompt: 'x', widget: { kind: 'expression', answer: '\\frac{1}{{{a + 1}}}', form: 'fraction' }, solution: ['x'] }).length === 0 && gen.checkFamily({ id: 'a', vars: { a: { int: [1, 2] } }, prompt: 'x', widget: { kind: 'expression', answer: '\\pi', form: 'exact-angle' }, solution: ['x'] }).length === 0 && gen.checkFamily({ id: 'a', vars: { a: { int: [1, 2] } }, prompt: 'x', widget: { kind: 'numeric', answer: '1', form: 'fraction' }, solution: ['x'] }).some((m) => /widget\.form/.test(m)));

console.log(`test-fluency-reach: ${n - fails.length}/${n} passed${fails.length ? ', ' + fails.length + ' FAILED' : ''}`);
process.exit(fails.length ? 1 : 0);
