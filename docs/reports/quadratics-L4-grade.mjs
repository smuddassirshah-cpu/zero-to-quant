/* Engine graders on every expression widget and every numeric set of quadratics level 4 (l14 to l19, review-4,
   homework-4, parts included), plus the forms a learner would type. Run from the repository root:
     node docs/reports/quadratics-L4-grade.mjs --local-cdn <pkgs>
   For each expression widget: the answer and every accept entry must grade correct (with the widget's form), every
   wrong entry must grade to its own key, and each typed form below must give the stated result:
   'ok' (correct), 'form' (equal but the wrong shape), 'no' (not equal, no wrong key), 'count', or a wrong id.
   The grading copies widgets/expression.js grade() over the real grade.js and Compute Engine (as
   tools/test-engine-runtime.mjs does). Numeric sets go through grade.js numSetGrade. Exit 0 when all pass. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
vm.runInContext(fs.readFileSync('app/js/engine/widgets/expression.js', 'utf8'), g);
const G = g.ZQ.grade, F = g.ZQ.widgets.exprForms;

const head = (j) => (Array.isArray(j) ? j[0] : null), args = (j) => (Array.isArray(j) ? j.slice(1) : []);
const hasSum = (j) => head(j) === 'Add' || head(j) === 'Subtract' || args(j).some(hasSum);
const size = (j) => (Array.isArray(j) ? 1 + args(j).reduce((a, x) => a + size(x), 0) : 1);
const isSumLike = (j) => head(j) === 'Add' || head(j) === 'Subtract';
function gradeExpr(spec, L) {
  const fo = { functions: spec.functions || [], integers: spec.integers || [] };
  if (spec.answers) { const r = G.exprSetGrade(ce, spec, L); return r.ok ? 'ok' : (r.key || 'no'); }
  const eq = (t) => { try { if (G.exprEqual(ce, L, t, fo)) return true; } catch { /* fall through */ } const n = G.normExpr(L); return !!n && n === G.normExpr(t); };
  const formOk = () => {
    if (spec.form === 'fraction') return G.shapeFraction(L);
    if (spec.form === 'exact-angle') return G.shapeExactAngle(L);
    if (!spec.form) return true;
    try {
      return G.withParsed(ce, L, fo.functions, (e) => {
        const j = e.json;
        if (spec.form === 'expanded') return isSumLike(j) ? args(j).every(t => !hasSum(t)) : !hasSum(j);
        if (spec.form === 'factorised') return G.shapeFactorised(j);
        if (spec.form === 'factorised-fully') return G.shapeFullyFactorised(j);
        if (spec.form === 'completed-square') return G.shapeCompletedSquare(j);
        const constant = !(e.unknowns || []).filter(v => v !== 'iota').length;
        if (spec.form === 'rectangular') return constant ? F.rectangular(j) : true;
        if (spec.form === 'simplified') { if (constant && F.reducible(j)) return false; try { return size(j) <= size(e.simplify().json); } catch { return true; } }
        return true;
      });
    } catch { return true; }
  };
  const same = [spec.answer, ...(spec.accept || [])].filter(Boolean).some(eq);
  if (same) return formOk() ? 'ok' : 'form';
  const w = (spec.wrong || []).find(x => x.tex && eq(x.tex));
  return w ? w.id : 'no';
}
const gradeNumSet = (spec, text) => { const r = G.numSetGrade(spec, text); return r.ok ? 'ok' : (r.key || 'no'); };

/* typed forms, keyed by the widget's answer (or its answers joined by " | ") */
const T = {
  '\\frac{7}{10}': [['\\frac{7}{10}', 'ok'], ['7/10', 'ok'], ['0.7', 'form'], ['\\frac{42}{60}', 'form'], ['\\frac{84}{120}', 'form'], ['\\frac{7}{120}', 'top-only']],
  'x-3': [['x-3', 'ok'], ['-3+x', 'ok'], ['x+3', 'wrong-bracket'], ['-3', 'cancel-xsq'], ['x^2-9', 'no'], ['(x-3)', 'ok'], ['\\frac{x^2-9}{x+3}', 'form'], ['\\frac{(x-3)(x+3)}{x+3}', 'form'], ['\\frac{x-3}{x}', 'whole']],
  '2(x+2)': [['2(x+2)', 'ok'], ['2(2+x)', 'ok'], ['(x+2)\\cdot2', 'ok'], ['2x+4', 'form'], ['\\frac{(x^2-4)(2x+6)}{(x+3)(x-2)}', 'form'], ['\\frac{x^2-4}{x+3}\\times\\frac{2x+6}{x-2}', 'form'], ['x+2', 'lost-two'], ['2(x-2)', 'sign']],
  'x(x+2)': [['x(x+2)', 'ok'], ['(x+2)x', 'ok'], ['x^2+2x', 'form'], ['\\frac{1}{x(x+2)}', 'flip-first'], ['\\frac{x^2+x}{x-2}\\div\\frac{x+1}{x^2-4}', 'form']],
  '2x+1': [['2x+1', 'ok'], ['1+2x', 'ok'], ['x+1+x', 'ok'], ['2', 'tops'], ['2x+2', 'one-twice'], ['x(x+1)', 'no'], ['\\frac{2x+1}{x(x+1)}', 'whole']],
  'x+8': [['x+8', 'ok'], ['8+x', 'ok'], ['3x+6-2x+2', 'ok'], ['3(x+2)-2(x-1)', 'form'], ['x+4', 'lost-minus'], ['5x+4', 'added'], ['\\frac{x+8}{(x-1)(x+2)}', 'whole']],
  '(x-1)(x-2)(x+3)': [['(x-1)(x-2)(x+3)', 'ok'], ['(x+3)(x-1)(x-2)', 'ok'], ['(x-1)(x^2+x-6)', 'form'], ['x^3-7x+6', 'form'], ['(x+1)(x+2)(x-3)', 'signs']],
  '(x-1)^2(x+2)': [['(x-1)^2(x+2)', 'ok'], ['(x+2)(x-1)^2', 'ok'], ['(x-1)(x-1)(x+2)', 'ok'], ['(x-1)(x^2+x-2)', 'form'], ['x^3-3x+2', 'form'], ['(x+1)^2(x-2)', 'signs'], ['(x-1)(x+2)', 'lost-square']],
  '3x+4y=26': [['3x+4y=26', 'ok'], ['y=-\\frac{3}{4}x+\\frac{13}{2}', 'ok'], ['y=-0.75x+6.5', 'ok'], ['4y=26-3x', 'ok'], ['y-2=-\\frac{3}{4}(x-6)', 'ok'], ['26=3x+4y', 'ok'],
    ['4x-3y=18', 'radius-gradient'], ['3x+4y=1', 'through-centre'], ['-\\frac{3}{4}x+\\frac{13}{2}', 'no']],
  '5x-2': [['5x-2', 'ok'], ['-2+5x', 'ok'], ['2x-2+3x', 'ok'], ['2(x-1)+3x', 'form'], ['5', 'tops'], ['5x-1', 'one-unmultiplied'], ['\\frac{5x-2}{x(x-1)}', 'whole']],
  '(x+1)(x-2)(x-3)': [['(x+1)(x-2)(x-3)', 'ok'], ['(x-3)(x-2)(x+1)', 'ok'], ['(x+1)(x^2-5x+6)', 'form'], ['x^3-4x^2+x+6', 'form'], ['(x-1)(x+2)(x+3)', 'signs']],
  '(x-2)(2x-1)(x+3)': [['(x-2)(2x-1)(x+3)', 'ok'], ['(2x-1)(x+3)(x-2)', 'ok'], ['(x-2)(2x^2+5x-3)', 'form'], ['2x^3+x^2-13x+6', 'form'], ['(x+2)(2x+1)(x-3)', 'signs'], ['(x-2)(x-1)(x+3)', 'lost-two']],
  /* numeric sets */
  '2 | -0.6': [['2, -0.6', 'ok'], ['-3/5, 2', 'ok'], ['x = 2 or x = -0.6', 'ok'], ['2', 'count'], ['-2, 0.6', 'signs']],
  '3 | -4': [['3, -4', 'ok'], ['x = -4, x = 3', 'ok'], ['3', 'count'], ['-3, 4', 'signs']],
  '4 | -4': [['4, -4', 'ok'], ['\\pm 4', 'ok'], ['y = 4 or y = -4', 'ok'], ['16, -16', 'no-root'], ['4', 'count']],
  '10 | 30': [['10, 30', 'ok'], ['30, 10', 'ok'], ['p = 10 or p = 30', 'ok'], ['-10, -30', 'signs'], ['20', 'count']],
  '-1 | -3': [['-1, -3', 'ok'], ['-3, -1', 'ok'], ['1, 3', 'signs'], ['-1', 'count']],
  '10 | -10': [['10, -10', 'ok'], ['\\pm 10', 'ok'], ['k = 10 or k = -10', 'ok'], ['4.47, -4.47', 'used-r-squared'], ['4.472, -4.472', 'used-r-squared'], ['10', 'count']],
};

let checks = 0, fails = 0, exprWidgets = 0, setWidgets = 0;
const used = new Set();
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('FAIL ' + msg); } };
const files = ['l14-roots-that-stay', 'l15-fractions-with-letters', 'l16-adding-and-solving', 'l17-dividing-polynomials', 'l18-circles-on-a-grid', 'l19-line-meets-curve', 'review-4', 'homework-4'];
const visit = (w, where) => {
  if (!w || typeof w !== 'object') return;
  const key = w.answers ? w.answers.join(' | ') : w.answer;
  if (w.kind === 'expression') {
    exprWidgets++;
    if (w.answers) say(gradeExpr(w, w.answers.join(', ')) === 'ok', `${where}: answers not correct`);
    else say(gradeExpr(w, w.answer) === 'ok', `${where}: answer ${w.answer} not correct in its own form`);
    for (const a of w.accept || []) say(gradeExpr(w, a) === 'ok', `${where}: accept ${a} not correct`);
    for (const x of w.wrong || []) { const r = gradeExpr(w, x.tex); say(r === x.id, `${where}: wrong ${x.id} (${x.tex}) graded ${r}`); }
    for (const [t, want] of T[key] || []) { const r = gradeExpr(w, t); say(r === want, `${where}: typed "${t}" gave ${r}, expected ${want}`); }
    say(!!T[key], `${where}: no typed forms listed for ${key}`);
    used.add(key);
  } else if (w.kind === 'numeric' && w.answers) {
    setWidgets++;
    say(gradeNumSet(w, w.answers.join(', ')) === 'ok', `${where}: answers not correct`);
    for (const x of w.wrong || []) { const r = gradeNumSet(w, x.value); say(r === x.id, `${where}: wrong ${x.id} (${x.value}) graded ${r}`); }
    for (const [t, want] of T[key] || []) { const r = gradeNumSet(w, t); say(r === want, `${where}: typed "${t}" gave ${r}, expected ${want}`); }
    say(!!T[key], `${where}: no typed forms listed for ${key}`);
    used.add(key);
  }
};
for (const f of files) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/quadratics/${f}.json`, 'utf8'));
  const lists = [['screens', doc.screens], ['quiz', doc.quiz], ['items', doc.items]];
  for (const [name, list] of lists) (list || []).forEach((s, i) => {
    visit(s.widget, `${f} ${name}[${i}]`);
    (s.parts || []).forEach((p, k) => visit(p.widget, `${f} ${name}[${i}].parts[${k}]`));
  });
}
for (const k of Object.keys(T)) say(used.has(k), `typed forms for ${k} match no widget`);
console.log(`grade: ${exprWidgets} expression widgets, ${setWidgets} numeric sets, ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
