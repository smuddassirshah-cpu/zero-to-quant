/* Second reader's grader probe for quadratics level 4: extra forms a Stage 0 learner would type, run through the
   engine graders (machinery copied from docs/reports/quadratics-L4-grade.mjs). Prints one line per probe; no exit gate.
   Run from the repository root: node docs/reviews/quadratics-4-scripts/probe-grade.mjs --local-cdn <pkgs> */
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


const P = {
  '\\frac{7}{10}': ['\\frac{14}{20}', '\\frac{21}{30}', '0.70', '7\\div10', '\\frac{70}{100}'],
  'x-3': ['(x-3)', '\\frac{x-3}{x}', '\\frac{(x-3)(x+3)}{x+3}', '\\frac{x^2-9}{x+3}', '1x-3', 'x-3x'],
  '2(x+2)': ['(x+2)2', '(2x+4)', '2\\times(x+2)', '\\frac{2(x-2)(x+2)(x+3)}{(x+3)(x-2)}', '\\frac{(x-2)(x+2)}{x+3}\\times\\frac{2(x+3)}{x-2}', '(x+2)+(x+2)', '2x+2', '4(\\frac{x}{2}+1)', '\\frac{2(x+2)}{1}', '\\frac{4(x+2)}{2}'],
  'x(x+2)': ['\\frac{x(x+1)(x-2)(x+2)}{(x-2)(x+1)}', 'x\\cdot(x+2)', '(x)(x+2)', 'x(2+x)', '\\frac{x(x+1)}{x-2}\\times\\frac{(x-2)(x+2)}{x+1}', '\\frac{2x(x+2)}{2}', 'x^2+2', '(x+2)'],
  '2x+1': ['(2x+1)', '\\frac{2x+1}{x(x+1)}', 'x+(x+1)', '(x+1)+x', '2x+1x', '1+x+x'],
  'x+8': ['(x+8)', '\\frac{x+8}{(x-1)(x+2)}', '3x+6-(2x-2)', 'x+4+4', '1x+8'],
  '(x-1)(x-2)(x+3)': ['(x-1)(x+3)(x-2)', '(1-x)(2-x)(x+3)', '-(1-x)(x-2)(x+3)', '(x^2-3x+2)(x+3)', '(x-1)(x-2)(x+3)+0', '(x-1)\\cdot(x-2)\\cdot(x+3)', '(x-1)(x-2)(x- -3)', '(x-1)(x-2)', '(x-1)(x-2)(x-3)', '1(x-1)(x-2)(x+3)', '\\frac{(2x-2)(x-2)(x+3)}{2}'],
  '(x-1)^2(x+2)': ['(x+2)(x-1)(x-1)', '(1-x)^2(x+2)', '(x^2-2x+1)(x+2)', '(x-1)^2\\cdot(x+2)', '(x-1)^2(x+2)^1', '(x-1)(x+2)(x-1)', '(x-1)^2', '(x-1)(x+2)^2'],
  '3x+4y=26': ['6x+8y=52', '3x+4y-26=0', 'y=\\frac{26-3x}{4}', 'y=6.5-0.75x', 'x=\\frac{26-4y}{3}', '4y+3x=26', 'y=-\\frac{3x}{4}+6.5', 'y=-\\frac{3}{4}x+6\\frac{1}{2}', '3x+4y=25', 'y=-\\frac{3}{4}x', 'y=\\frac{3}{4}x-\\frac{5}{2}', 'y=-\\frac{4}{3}x+10', '3x+4y', '0=3x+4y-26', '-3x-4y=-26', 'y-2=-0.75(x-6)'],
  '5x-2': ['(5x-2)', '\\frac{5x-2}{x(x-1)}', '2x-2+3x', '3x+2(x-1)', '5x-2x', '5x+2'],
  '(x+1)(x-2)(x-3)': ['(x-3)(x+1)(x-2)', '(1+x)(2-x)(3-x)', '(x+1)(x^2-5x+6)', '(x-2)(x^2-2x-3)', '(x+1)(x-2)', '(x+1)(x-2)(x+3)'],
  '(x-2)(2x-1)(x+3)': ['2(x-2)(x-\\frac{1}{2})(x+3)', '(x-2)(x+3)(2x-1)', '(2-x)(1-2x)(x+3)', '(x-2)(x-0.5)(x+3)', '2(x-2)(x-0.5)(x+3)', '(2x-4)(x-\\frac{1}{2})(x+3)', '(x-2)(2x^2+5x-3)', '(2x-1)(x^2+x-6)', '(x-2)(2x-1)(x-3)'],
  '2 | -0.6': ['2 and -0.6', '-0.6 and 2', '2,-3/5', 'x=2, x=-0.6', '2 -0.6', '2; -0.6', '-0.6', '2, 0.6', '2, -0.6, 2', '2, -.6', '2, −0.6', '2, -0.60'],
  '3 | -4': ['3 and -4', '-4,3', 'x=3 or -4', '3, 4', '-3, -4', '(3, -4)'],
  '4 | -4': ['4 and -4', '+-4', '+/-4', '±4', '-4, 4', '4', '4, 4', 'y=±4'],
  '10 | 30': ['10 and 30', '£10, £30', '£10 and £30', '10,30', '30', '10, 20', '10.00, 30.00'],
  '1 | -3': ['1 and -3', '-3,1', '1, 3', 'x=1,x=-3'],
  '10 | -10': ['±10', '+-10', '10 and -10', '-10, 10', '10', '10, 10', '9.99, -10.01', '9.9, -9.9', '4.5, -4.5', '4.472, -4.472', '20, -20'],
};
const files = ['l14-roots-that-stay', 'l15-fractions-with-letters', 'l16-adding-and-solving', 'l17-dividing-polynomials', 'l18-circles-on-a-grid', 'l19-line-meets-curve', 'review-4', 'homework-4'];
const visit = (w, where) => {
  if (!w || typeof w !== 'object') return;
  const key = w.answers ? w.answers.join(' | ') : w.answer;
  const set = w.kind === 'numeric' && w.answers;
  if (w.kind !== 'expression' && !set) return;
  console.log(`\n${where}  key ${key}  form ${w.form || '-'}`);
  for (const t of P[key] || []) { let r; try { r = set ? gradeNumSet(w, t) : gradeExpr(w, t); } catch (e) { r = 'THROW ' + e.message; } console.log(`   ${String(r).padEnd(16)} ${t}`); }
  if (!P[key]) console.log('   (no probes)');
};
for (const f of files) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/quadratics/${f}.json`, 'utf8'));
  for (const [name, list] of [['screens', doc.screens], ['quiz', doc.quiz], ['items', doc.items]]) (list || []).forEach((s, i) => {
    visit(s.widget, `${f} ${name}[${i}]`);
    (s.parts || []).forEach((p, k) => visit(p.widget, `${f} ${name}[${i}].parts[${k}]`));
  });
}
