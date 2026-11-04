// node exprcheck.cjs <pkgs>   Grades each expression item of topic-3.2 through the app's real grader (exprEqual):
// the key and the accept forms must grade right, each wrong form must grade wrong, and a few learner spellings too.
const fs = require('fs'); const path = require('path');
const pkgs = process.argv[2];
const ceFile = path.join(pkgs, 'cortex-js-compute-engine-0.30.2/package/dist/compute-engine.min.umd.js');
global.window = { ZQ: {} }; global.document = { addEventListener() {} };
require('vm').runInThisContext(fs.readFileSync(ceFile, 'utf8'));
const CE = globalThis.ComputeEngine; const C = CE.ComputeEngine || CE;
const root = path.resolve(__dirname, '../../..');
require(path.join(root, 'app/js/engine/grade.js'));
const G = window.ZQ.grade; const ce = new C();
const exam = JSON.parse(fs.readFileSync(path.join(root, 'app/content/exams/topic-3.2.json'), 'utf8'));
let bad = 0;
const T = (id, input, want, key, o) => {
  const r = G.exprEqual(ce, input, key, o); const ok = r === want; if (!ok) bad++;
  console.log(ok ? 'ok  ' : 'FAIL', id, JSON.stringify(input), '=>', r, '(want', want + ')');
};
const extra = {
  'e-drift-t2w2': { right: ['t^2+2tw^2', '2tw^2+t^2', '2*t*w*w+t*t', 't^2+2w^2t'], wrong: ['2tw^2', '2tw^2+2t^2', '2t^2w', 't^2w^2', '2tw^2-t^2'] },
  'e-sixth-repair': { right: ['w^6-15t w^4+45 t^2 w^2-15t^3', 'w^6-15*t*w^4+45*t^2*w^2-15*t^3', '-15t^3+45t^2w^2-15tw^4+w^6'], wrong: ['w^6-15tw^4+45t^2w^2', 'w^6+15tw^4+45t^2w^2+15t^3', 'w^6-15tw^4+45t^2w^2-15t^2', 'w^6-15tw^4+45t^2w^2-10t^3'] },
  'e-coefficient-k': { right: ['\\frac{4-4(-1)^k}{\\pi k^3}', '\\frac{4(1-\\cos(k\\pi))}{\\pi k^3}', '\\frac{4}{\\pi k^3}(1-(-1)^k)'], wrong: ['\\frac{2(1-(-1)^k)}{\\pi k^3}', '\\frac{4(1-(-1)^k)}{\\pi k^2}', '\\frac{4(1+(-1)^k)}{\\pi k^3}', '\\frac{4}{\\pi k^3}'] },
};
for (const it of exam.items) {
  const w = it.widget; if (!w || w.kind !== 'expression') continue;
  const o = { integers: w.integers || [] };
  T(it.id, w.answer, true, w.answer, o);
  for (const a of w.accept || []) T(it.id + ' accept', a, true, w.answer, o);
  for (const x of w.wrong || []) T(it.id + ' wrong ' + x.id, x.tex, false, w.answer, o);
  const e = extra[it.id] || {};
  for (const a of e.right || []) T(it.id + ' extra-right', a, true, w.answer, o);
  for (const a of e.wrong || []) T(it.id + ' extra-wrong', a, false, w.answer, o);
}
console.log(bad ? 'FAILURES ' + bad : 'all expression checks pass');
process.exit(bad ? 1 : 0);
