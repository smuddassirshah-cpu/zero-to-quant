#!/usr/bin/env node
/* Regression test for ENGINE-BACKLOG 618 (the expression grader and equations).
     Part 1: ZQ.grade.exprEqual on equations, inequalities and a learner's leading "n =" (the cases of review-equations-1-2
             Engine 1 and review-equations-3-4 finding 18), on the real grade.js with the local Compute Engine.
     Part 2: over every `expression` widget in app/content: each authored answer and accept form grades equal to itself and to
             nothing in a different relation; each wrong[] value routes to its own key, as the widget's grade() would route it.
     Part 3: the audit (--audit): lists authored items whose answer, accept or wrong text holds a relation, and says which
             of them accept the bogus equation "zzq=7" (a wrong equation).
   Usage: node tools/test-expr-equations.mjs [--local-cdn <pkgs>] [--audit] [--full] [--grade <path to a grade.js>]
   The Compute Engine comes from --local-cdn or the ZQ_LOCAL_CDN variable. Exit 0 pass, 1 failure, 2 setup problem. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..');
const argv = process.argv.slice(2);
const arg = (k) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? path.resolve(argv[i + 1]) : null; };
const cdn = arg('--local-cdn') || (process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null);
const gradeFile = arg('--grade') || path.join(APP, 'js/engine/grade.js');
const audit = argv.includes('--audit'), full = argv.includes('--full');
const die = (m) => { console.error('test-expr-equations: ' + m); process.exit(2); };
const ceFile = cdn && path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
if (!ceFile || !fs.existsSync(ceFile)) die('give --local-cdn <pkgs> (or ZQ_LOCAL_CDN) with the local Compute Engine');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const C = g.ComputeEngine.ComputeEngine || g.ComputeEngine, ce = new C();
g.ZQ = {};
vm.runInContext(fs.readFileSync(gradeFile, 'utf8'), g);
const G = g.ZQ.grade;
const fails = []; let n = 0;
const check = (name, ok, detail = '') => { n++; if (!ok) { fails.push(name); console.log(`FAIL ${name}  ${detail}`); } };
const eq = (a, b, o) => !!G.exprEqual(ce, a, b, o);

if (!audit) {
  /* ---------- Part 1 ---------- */
  const yes = [
    ['y=2x+1', '2x+1=y'], ['y=2x+1', '2y=4x+2'], ['y=2x+1', '-y=-2x-1'], ['n=\\frac{a}{c-b}', 'n=\\frac{a}{c-b}'],
    ['n=\\frac{a}{c-b}', '\\frac{a}{c-b}=n'], ['x<3', '3>x'], ['x<3', '2x<6'], ['x\\le3', '3\\ge x'], ['x+1<y', 'y>x+1'],
    ['x\\ne2', '2x\\ne4'], ['x\\ne2', '2\\neq x'],
    /* a learner's leading letter and = when the answer has no = */
    ['n=\\frac{a}{c-b}', '\\frac{a}{c-b}'], ['C = 3 + 2n', '3+2n'], ['\\text{cost} = 3 + 2n', '3+2n'], ['3 + 2n = C', '3+2n'], ['C_1 = 3 + 2n', '2n+3'],
    /* ENGINE-BACKLOG 836: a plain-text function name before a bracket is the function */
    ['\\frac{\\ln 97}{\\ln 4}', 'ln(97)/ln(4)'], ['ln(97)/ln(4)', '\\frac{\\ln(97)}{\\ln(4)}'], ['\\sqrt{6}', 'sqrt(2)*sqrt(3)'], ['e^{x}', 'exp(x)'],
    ['\\frac{\\sin x}{\\cos x}', 'tan(x)'], ['\\log(x)', 'log(x)'], ['2\\sin(x)', '2sin(x)'], ['x\\cdot y(z)', 'xy(z)'], ['\\sin(x)', '\\sin(x)'],
  ];
  const no = [
    ['n=5', 'n=\\frac{a}{c-b}'], ['n=\\frac{a}{c-b}', 'n=5'], ['y=2x+1', 'y=2x+2'], ['y=2x+1', 'y=3x+1'], ['y=2x+1', '2x+1=y+1'],
    ['x<3', 'x<4'], ['x<3', 'x>3'], ['x<3', '-x<-3'], ['x<3', 'x\\le3'], ['x<3', '3<x'], ['x\\ne2', 'x\\ne3'], ['x\\ne2', 'x=2'],
    /* an equation against a non-equation, and a wrong formula behind a letter */
    ['2x+1', 'y=2x+1'], ['n=5', '\\frac{a}{c-b}'], ['C=3+2n', '3+3n'], ['x=1', 'y=1'], ['x<3', '3'],
    /* the letter stripped only when the answer has no relation, and a chain stays a chain */
    ['1<x<3', '1<x<4'], ['m+1', 'n=m+1'],
    /* 836: the letters l and n are no longer the quotient 97/4, and a name without a bracket stays letters */
    ['\\frac{97}{4}', 'ln(97)/ln(4)'], ['ln(97)/ln(4)', '\\frac{97}{4}'], ['\\frac{\\log 97}{\\log 5}', 'ln(97)/ln(4)'], ['\\sin(x)', 'cos(x)'], ['sin(x)', 'sinx'], ['\\sqrt{2}', 'sqrt(3)'],
  ];
  yes.forEach(([a, b]) => check(`equal: ${a}  vs  ${b}`, eq(a, b)));
  no.forEach(([a, b]) => check(`unequal: ${a}  vs  ${b}`, !eq(a, b)));
  /* input first, as the widget calls it: ('n = expr' typed, 'expr' authored) is equal, the reverse is not */
  check('authored n=expr does not accept a bare expr', !eq('\\frac{a}{c-b}', 'n=\\frac{a}{c-b}'));
  check('the same-direction equation accepts itself', eq('1<x<3', '1<x<3'));

  /* ENGINE-BACKLOG 620: a function-call, decorated or subscripted left side, and the item's own expression restated.
     Written as the widget calls it: eq(input, authored). */
  const yes620 = [
    ['4k+1', 'f(k)=4k+1'], ['4k+1', 'f(k) = 4k+1'], ['4k+1', '4k+1=f(k)'], ['4k+1', 'a_k=4k+1'], ['4k+1', 'f(k)=1+4k'],
    ['5(x-4)', 'f(x)=5(x-4)'], ['5(x-4)', 'f\\left(x\\right)=5x-20'], ['0.5x+4', 'g(x)=0.5x+4'], ['0.5x+4', 'y=0.5x+4'], ['x^2', 'h(t)=x^2'],
    ['\\frac{1}{1-r}', 'S_\\infty=\\frac{1}{1-r}'], ['\\frac{1}{1-r}', 'S_{\\infty}=\\frac{1}{1-r}'], ['2u_n+1', 'u_{n+1}=2u_n+1'], ['3n', 'a_{n+1}=3n'],
    ['3n', '\\bar{x}=3n'], ['3n', "x'=3n"], ['3n', 'x_{\\text{max}}=3n'], ['3n', 'f(x,y)=3n'],
    /* restated expression: both sides the same, the right equals the answer */
    ['x^3+9x^2+27x+27', '(x+3)^3=x^3+9x^2+27x+27'], ['x^3+9x^2+27x+27', '(x+3)^3 = 27+27x+9x^2+x^3'],
    ['16x^4-32x^3+24x^2-8x+1', '(2x-1)^4=16x^4-32x^3+24x^2-8x+1'],
    /* a segment name of two or more letters */
    ['\\sqrt{2}', 'OB=\\sqrt{2}'], ['\\sqrt{3}', 'TM=\\sqrt{3}'], ['x+1', 'AB=x+1'], ['\\sqrt{2}', '\\sqrt{2}=OB'],
  ];
  const no620 = [
    ['4k+1', 'f(k)=4k+5'], ['4k+1', 'f(k)=4k'], ['4k+1', 'f(k)=k+4'], ['5(x-4)', 'f(x)=5(x+4)'], ['0.5x+4', 'y=5'], ['0.5x+4', 'f(x)=5'],
    ['4x', 'f(x)=y'], ['\\frac{1}{1-r}', 'S_\\infty=\\frac{1}{r-1}'], ['2u_n+1', 'u_{n+1}=2u_n'], ['4k+1', 'f(k)=g(k)'],
    /* restated expression with a wrong right side, or two sides that differ */
    ['x^3+9x^2+27x+27', '(x+3)^3=x^3+27'], ['x^3+9x^2+27x+27', '(x+3)^3=x^3+3x^2+9x+27'], ['x^3+9x^2+27x+27', '(x+2)^3=x^3+9x^2+27x+27'],
    ['x^3+9x^2+27x+27', 'x^3+27=x^3+9x^2+27x+27'], ['5', 'x+1=5'], ['x+1', 'f(x)=x+1=y'],
    ['\\sqrt{2}', 'OB=\\sqrt{3}'], ['\\sqrt{2}', 'OB=2'], ['\\sqrt{3}', 'TM=1'], ['x', 'xy=x'], ['xy', 'xy=5'], ['x+1', 'AB=CD'],
  ];
  yes620.forEach(([a, b]) => check(`620 equal: ${a}  vs  ${b}`, eq(b, a)));
  no620.forEach(([a, b]) => check(`620 unequal: ${a}  vs  ${b}`, !eq(b, a)));
  /* the real items: correct forms pass, the listed slips still route to their own keys */
  const exprIn = (v, out = []) => { if (Array.isArray(v)) v.forEach(x => exprIn(x, out)); else if (v && typeof v === 'object') { if (v.kind === 'expression' && typeof v.answer === 'string') out.push(v); Object.values(v).forEach(x => exprIn(x, out)); } return out; };
  for (const [loc, i, L] of [['screens', 2, 'OB='], ['screens', 4, 'TM=']]) {
    const d = JSON.parse(fs.readFileSync(path.join(APP, 'content/courses/trig/l4-exact-values.json'), 'utf8'));
    for (const w of exprIn(d[loc][i])) {
      const o = { functions: w.functions || [], integers: w.integers || [] };
      [w.answer, ...(w.accept || [])].filter(f => eq(f, w.answer, o)).forEach(f => check(`620 trig l4 ${loc}[${i}] ${L}${f} passes`, eq(L + f, w.answer, o)));
      for (const x of w.wrong || []) if (x.tex) { check(`620 trig l4 ${loc}[${i}] ${L}${x.id} is not the answer`, !eq(L + x.tex, w.answer, o)); check(`620 trig l4 ${loc}[${i}] ${L}${x.id} routes to its key`, eq(L + x.tex, x.tex, o)); }
    }
  }
  const lefts = ['f(k)=', 'a_k=', 'f(x)=', '(x+3)^3=', '(2x-1)^4='];
  for (const [file, loc, i] of [['series/homework-2', 'items', 0], ['series/l11-powers-of-a-bracket', 'screens', 2], ['series/homework-3', 'items', 0]]) {
    const d = JSON.parse(fs.readFileSync(path.join(APP, 'content/courses', file + '.json'), 'utf8'));
    for (const w of exprIn(d[loc][i])) {
      const o = { functions: w.functions || [], integers: w.integers || [] }, all = [w.answer, ...(w.accept || [])];
      const mine = lefts.filter(L => file !== 'series/homework-2' ? L !== 'f(k)=' && L !== 'a_k=' : L === 'f(k)=' || L === 'a_k=');
      for (const L of mine.filter(L => !L.startsWith('(') || (L === '(x+3)^3=') === (w.answer.startsWith('x^3')) )) {
        check(`620 item ${file} ${loc}[${i}] ${L}answer passes`, all.every(f => eq(L + f, w.answer, o)));
        for (const x of w.wrong || []) {
          if (!x.tex) continue;
          check(`620 item ${file} ${loc}[${i}] ${L}${x.id} is not the answer`, !eq(L + x.tex, w.answer, o));
          if (!L.startsWith("(")) check(`620 item ${file} ${loc}[${i}] ${L}${x.id} routes to its key`, eq(L + x.tex, x.tex, o)); // a restated expression with a wrong right side is a false equation: generic line
        }
      }
    }
  }
}

/* ---------- Part 1b: engine pass AA 2 (ENGINE-BACKLOG 898, 904, 905, 906, 908), on G.exprGrade, the grade the widget returns ----------
   The fault rows come from the second readers' grade-check scripts (docs/reviews/problems-0.2-a-scripts, -0.2-b-, -0.3-a-, -1.3-c-). */
if (!audit && G.exprGrade) {
  const X = (spec) => ({ kind: 'expression', ...spec });
  const gr = (spec, typed) => G.exprGrade(ce, X(spec), typed, typed);
  const ok = (spec, t) => gr(spec, t).ok === true;
  const key = (spec, t) => { const r = gr(spec, t); return r.ok ? 'ok' : r.key; };
  /* 905: a "Solve" part does not grade the question retyped, or a half-solved line */
  const bakery = { answer: 'h\\le10', accept: ['10\\ge h'], wrong: [{ id: 'no-flip', tex: 'h\\ge10' }] };
  ['h\\le10', '10\\ge h', 'h<=10', 'h≤10', 'h\\leq 10.0'].forEach(t => check(`905 solved: ${t} passes`, ok(bakery, t)));
  ['240-18h\\ge60', '-18h\\ge-180', '18h+60\\le240', '2h\\le20', '60\\le240-18h'].forEach(t => check(`905 solved: ${t} is equal but not solved (key form)`, key(bakery, t) === 'form', JSON.stringify(gr(bakery, t))));
  check('905 solved: a wrong slip still routes to its key', key(bakery, 'h\\ge10') === 'no-flip' && key(bakery, 'h\\le9') === null);
  check('905 solved: the form line says what to do', /not solved/.test(gr(bakery, '240-18h\\ge60').line));
  const fridge = { answer: 'F\\le41', accept: ['41\\ge F'], wrong: [{ id: 'stopped', tex: 'F\\le9' }] };
  check('905 fridge: F\\le41 passes, the retyped question and F-32\\le9 do not', ok(fridge, 'F\\le41') && key(fridge, '\\frac{F-32}{1.8}\\le5') === 'form' && key(fridge, 'F-32\\le9') === 'form' && key(fridge, 'F\\le9') === 'stopped');
  const van = { answer: 't<7.5', accept: ['t<\\frac{15}{2}', '7.5>t'] };
  check('905 van: t<7.5 and its accept forms pass, the retyped question does not', ok(van, 't<7.5') && ok(van, '7.5>t') && ok(van, 't<\\frac{15}{2}') && key(van, '24000-2400t>6000') === 'form');
  const eqn = { answer: 'x=4' };
  check('905 an equation answer: x=4 and 4=x pass; 2x=8 and 2x+3=11 are not solved', ok(eqn, 'x=4') && ok(eqn, '4=x') && key(eqn, '2x=8') === 'form' && key(eqn, '2x+3=11') === 'form' && key(eqn, 'x=5') === null);
  const yx = { answer: 'y=2x+1' };
  check('905 no auto rule when the other side holds letters (y=2x+1 keeps accepting 2y=4x+2)', ok(yx, '2y=4x+2') && ok(yx, 'y=2x+1'));
  const yxs = { answer: 'y=2x+1', form: 'solved' };
  check('905 form "solved" asked for: y=2x+1 and 2x+1=y pass, 2y=4x+2 does not', ok(yxs, 'y=2x+1') && ok(yxs, '2x+1=y') && key(yxs, '2y=4x+2') === 'form' && key(yxs, 'y-1=2x') === 'form' && key(yxs, 'y=2x+2') === null);
  check('905 an answer that is not a relation has no solved rule', ok({ answer: '2x+1' }, '2x+1') && ok({ answer: '5' }, '5') && ok({ answer: '2x+1' }, 'y=2x+1'));
  check('905 a chain answer is compared as text, as before', ok({ answer: '0\\le h\\le10' }, '0\\le h\\le10'));

  /* 904: a typed left side is dropped before the shape checks, and nested and inverse names are labels */
  const lin = { answer: '1.5x+4', form: 'simplified' };
  ['m(e(x))=1.5x+4', 'y=1.5x+4', 'f^{-1}(x)=1.5x+4', 'B(T(n))=1.5x+4', 'f(-x)=1.5x+4', 'gf(x)=1.5x+4', 'g\\left(f\\left(x\\right)\\right)=1.5x+4', 'f^{-1}\\left(x\\right)=1.5x+4', 'A_1=1.5x+4', '1.5x+4=y'].forEach(t => check(`904 label: ${t} passes`, ok(lin, t), JSON.stringify(gr(lin, t))));
  check('904 label: the inverse written for its answer, and the composite of the 0.3 a items', ok({ answer: '\\frac{x-4}{1.5}', accept: ['\\frac{x-4}{1.5}'] }, 'f^{-1}(x)=\\frac{x-4}{1.5}') && ok({ answer: '5n-100', form: 'simplified' }, 'B(T(n))=5n-100') && ok({ answer: '4x^2+4x-2' }, 'g(f(x))=4x^2+4x-2'));
  check('904 label: a wrong right side is still wrong, and a slip routes to its key', !ok(lin, 'm(e(x))=1.5x+5') && key({ ...lin, wrong: [{ id: 'slip', tex: '1.5x+5' }] }, 'm(e(x))=1.5x+5') === 'slip');
  check('904 label: a product is not a label (x(x+1)=5 for the answer 5, f(f(x)) head inside its brackets)', !ok({ answer: '5' }, 'x(x+1)=5') && !ok({ answer: '5' }, 'f(f(x))=5'));
  check('904 label: a head letter of the answer is not dropped (the answer is f(x)+1 itself)', !ok({ answer: 'f(x)+1', functions: ['f'] }, 'f(x)=f(x)+2'));
  const sq = { answer: '-0.2(x-10)^2+20', form: 'completed-square', wrong: [{ id: 'sign-h', tex: '-0.2(x+10)^2+20' }] };
  check('904 shape: y= before a completed square passes the shape check (canal arch)', ok(sq, 'y=-0.2(x-10)^2+20') && ok(sq, 'y=20-0.2(x-10)^2') && key(sq, 'y=-0.2x^2+4x') === 'form' && key(sq, 'y=-0.2(x+10)^2+20') === 'sign-h');
  const ff = { answer: '(x+4)(x+5)', form: 'factorised' };
  check('904 shape: A= before a factorised answer passes, expanded and fully factorised too', ok(ff, 'A=(x+4)(x+5)') && ok({ answer: '(x+4)(x+5)', form: 'factorised-fully' }, 'A=(x+5)(x+4)') && ok({ answer: 'x^2+9x+20', form: 'expanded' }, 'A=x^2+9x+20') && key(ff, 'A=x^2+9x+20') === 'form');
  check('904 shape: the restated expression is shape-checked on its right side', ok({ answer: 'x^3+9x^2+27x+27', form: 'expanded' }, '(x+3)^3=x^3+9x^2+27x+27') && key({ answer: 'x^3+9x^2+27x+27', form: 'expanded' }, '(x+3)^3=(x+3)^3') === 'form');

  /* 898: both parts of a value, a sampling range, equal forms with a tiny term */
  check('898 complex: sqrt(x-5) is not 3 sqrt(x-5), nor sqrt(5-x)', !eq('\\sqrt{x-5}', '3\\sqrt{x-5}') && !eq('\\sqrt{x-5}', '\\sqrt{5-x}') && eq('\\sqrt{x-5}', '\\sqrt{x-5}') && eq('\\sqrt{x-5}', '(x-5)^{0.5}'));
  check('898 complex: ln(x-5) against 2 ln(x-5) differs', !eq('\\ln(x-5)', '2\\ln(x-5)') && eq('\\ln(x-5)+\\ln(x-5)', '2\\ln(x-5)'));
  check('898 tiny term: 400/e^{8u} equals 400e^{-8u}', eq('\\frac{400}{e^{8u}}', '400e^{-8u}') && eq('400e^{-8u}', '400e^{-8u}') && !eq('\\frac{400}{e^{8u}}', '400e^{-7u}'));
  check('898 tiny term: the barbell hedge row of the 1.3 c reader', ok({ answer: '-100e^{-2u}-400e^{-8u}+500e^{-5u}', accept: ['500e^{-5u}-100e^{-2u}-400e^{-8u}'] }, '-\\frac{100}{e^{2u}}-\\frac{400}{e^{8u}}+\\frac{500}{e^{5u}}'));
  check('898 real domain: an imaginary side against an undefined one is a skipped point (tan(arcsin s) and s/sqrt(1-s^2))', eq('\\tan(\\arcsin(s))', '\\frac{s}{\\sqrt{1-s^2}}'));
  check('898 domain: a sampling range per symbol', eq('\\arcsin(s)', '\\arcsin(s)', { domain: { s: [0.05, 0.9] } }) && eq('\\sin(\\arcsin(s))', 's', { domain: { s: [0.05, 0.9] } }) && !eq('\\sin(\\arcsin(s))', '2s', { domain: { s: [0.05, 0.9] } }));
  check('898 domain: the item spec carries it (exprOpts), and a wrong value inside it is still wrong', G.exprOpts({ domain: { s: [0.1, 0.9] } }).domain.s[1] === 0.9 && ok({ answer: '\\sin(\\arcsin(s))', domain: { s: [0.05, 0.9] } }, 's') && !ok({ answer: '\\sin(\\arcsin(s))', domain: { s: [0.05, 0.9] } }, 's^2'));
  check('898 domain: a range that cannot separate two forms says so (x and |x| agree on 0.3 to 3, differ on a negative range)', eq('x', '|x|') && !eq('x', '|x|', { domain: { x: [-3, -0.3] } }));

  /* 906, 908: plain-text spellings */
  check('908 power with a bracketed exponent: 80*0.9^(n-1)', eq('80*0.9^(n-1)', '80\\cdot0.9^{n-1}') && eq('2^(n-1)', '2^{n-1}') && eq('5*3^(n-1)', '5\\cdot3^{n-1}') && eq('3^(1/2)', '\\sqrt{3}') && eq('x^(2)', 'x^2') && !eq('2^n-1', '2^{n-1}') && eq('2^\\left(n-1\\right)', '2^{n-1}'));
  check('908 decimal times a bracket: 0.25(500) is 125, not 0.255005...', eq('0.25(500)', '125') && eq('0.25\\left(500\\right)', '125') && eq('0.25(500)-3', '122') && eq('1.5(2)', '3') && eq('0.5(x+4)', '0.5x+2') && eq('.5(x+4)', '0.5x+2') && !eq('0.25(500)', '0.2550'));
  check('906 a thousands comma: 12,000-s', eq('12,000-s', '12000-s') && eq('12{,}000-s', '12000-s') && eq('0.04s+0.065(12,000-s)=660', '0.04s+0.065(12000-s)=660') && eq('1,250,000+x', '1250000+x') && !eq('12,000-s', '12-s'));
  check('906 a pair is not a thousand (2,100) and a list keeps its commas', eq('(2,100)', '(2,100)') && !eq('(2,100)', '(2,1)') && !eq('(2,100)', '2100'));
}

/* ---------- Part 2 and 3: content ---------- */
const files = [];
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).forEach(e => { const p = path.join(d, e.name); if (e.isDirectory()) walk(p); else if (e.name.endsWith('.json') && e.name !== 'manifest.json') files.push(p); });
walk(path.join(APP, 'content'));
const widgets = [];
const find = (v, file, p) => {
  if (Array.isArray(v)) v.forEach((x, i) => find(x, file, `${p}[${i}]`));
  else if (v && typeof v === 'object') { if (v.kind === 'expression' && typeof v.answer === 'string') widgets.push({ w: v, where: `${path.relative(APP, file)} ${p}` }); Object.entries(v).forEach(([k, x]) => find(x, file, `${p}.${k}`)); }
};
files.forEach(f => { try { find(JSON.parse(fs.readFileSync(f, 'utf8')), f, ''); } catch { /* not content JSON */ } });
const REL = /<|>|=|\\(?:le|ge|ne|lt|gt)(?![A-Za-z])|≤|≥|≠/;
const fo = (w) => ({ functions: Array.isArray(w.functions) ? w.functions : [], integers: Array.isArray(w.integers) ? w.integers : [] });
const forms = (w) => [w.answer, ...(w.accept || [])].filter(Boolean);

if (audit) {
  let items = 0, accepts = 0;
  for (const { w, where } of widgets) {
    const texts = [...forms(w), ...(w.wrong || []).map(x => x.tex).filter(Boolean)];
    if (!texts.some(t => REL.test(t))) continue;
    items++;
    const bad = forms(w).some(f => REL.test(f) && eq('zzq=7', f, fo(w)));
    const shadow = (w.wrong || []).some(x => x.tex && REL.test(x.tex) && eq('zzq=7', x.tex, fo(w)));
    if (bad || shadow) accepts++;
    console.log(`${bad || shadow ? 'ACCEPTS' : 'ok     '} ${where}  answer=${w.answer}${bad ? ' [answer/accept takes a wrong equation]' : ''}${shadow ? ' [wrong[] relation shadows other input]' : ''}`);
  }
  console.log(`expression widgets: ${widgets.length}; with a relation in answer, accept or wrong: ${items}; accepting the wrong equation zzq=7: ${accepts}`);
  process.exit(0);
}
/* Forms without a relation go through code this change leaves alone, and a few authored ones were never LaTeX (text-mode
   spellings such as 5*3^(n-1), 3^(1/2), and wrong values the widget's own normExpr fallback settles): those are counted as
   notes. A form WITH a relation must pass. */
let wrongs = 0, notes = 0;
/* Without --full only items that hold a relation are run (a few seconds); --full runs every widget (about ten minutes). */
const soft = (name, ok, text, detail) => { if (REL.test(text)) check(name, ok(), detail); else if (full) { n++; if (!ok()) notes++; } };
for (const { w, where } of widgets) {
  const o = fo(w);
  forms(w).forEach(f => soft(`self-equal ${where} ${f}`, () => eq(f, f, o), f, ''));
  (w.wrong || []).forEach(x => {
    if (!x.tex) return;
    wrongs++;
    const same = () => forms(w).some(f => eq(x.tex, f, o));
    const hit = () => (w.wrong || []).find(y => y.tex && eq(x.tex, y.tex, o));
    soft(`wrong not an answer ${where} ${x.id}`, () => !same(), x.tex, x.tex);
    soft(`wrong routes to its key ${where} ${x.id}`, () => { const h = hit(); return !!h && (h.id === x.id || h.tex === x.tex); }, x.tex, 'routes elsewhere');
  });
}
console.log(`${widgets.length} expression widgets, ${wrongs} wrong[] values checked; ${full ? notes + ' relation-free forms not LaTeX-equal to themselves (text-mode spellings, unchanged by 618)' : 'relation-free forms skipped (use --full)'}`);
console.log(`test-expr-equations: ${n - fails.length}/${n} passed${fails.length ? ', ' + fails.length + ' FAILED' : ''}`);
process.exit(fails.length ? 1 : 0);
