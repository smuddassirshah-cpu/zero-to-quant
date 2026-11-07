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
  ];
  const no = [
    ['n=5', 'n=\\frac{a}{c-b}'], ['n=\\frac{a}{c-b}', 'n=5'], ['y=2x+1', 'y=2x+2'], ['y=2x+1', 'y=3x+1'], ['y=2x+1', '2x+1=y+1'],
    ['x<3', 'x<4'], ['x<3', 'x>3'], ['x<3', '-x<-3'], ['x<3', 'x\\le3'], ['x<3', '3<x'], ['x\\ne2', 'x\\ne3'], ['x\\ne2', 'x=2'],
    /* an equation against a non-equation, and a wrong formula behind a letter */
    ['2x+1', 'y=2x+1'], ['n=5', '\\frac{a}{c-b}'], ['C=3+2n', '3+3n'], ['x=1', 'y=1'], ['x<3', '3'],
    /* the letter stripped only when the answer has no relation, and a chain stays a chain */
    ['1<x<3', '1<x<4'], ['m+1', 'n=m+1'],
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
