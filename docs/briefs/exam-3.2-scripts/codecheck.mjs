// node codecheck.mjs <pkgs>
// Runs the Python code widget of topic-3.2 (e-explicit-code) in Pyodide 0.27.7, the app's runtime: the solution passes every
// hidden test and example (isclose with the case tolerance), the untouched starter does not, and the time per test is shown.
import fs from 'fs'; import path from 'path'; import { createRequire } from 'module'; import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(process.argv[2], 'pyodide-0.27.7/package') + '/';
const exam = JSON.parse(fs.readFileSync(path.join(here, '../../../app/content/exams/topic-3.2.json'), 'utf8'));
const widgets = [];
for (const it of exam.items) if (it.widget && it.widget.kind === 'code' && it.widget.language === 'python') widgets.push({ id: it.id, w: it.widget });
const require = createRequire(root);
const { loadPyodide } = require(root + 'pyodide.js');
const py = await loadPyodide({ indexURL: root, stdout: () => {}, stderr: () => {} });
py.runPython(`
import json, time, math
def close(a, b, tol):
    if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    return math.isclose(a, b, rel_tol=tol.get('rel', 0), abs_tol=tol.get('abs', 0))
def run_widget(spec, source):
    ns = {'__name__': '__main__'}
    res = []
    try:
        if spec.get('prelude'): exec(spec['prelude'], ns)
        exec(source, ns)
    except Exception as ex:
        return [('load', False, repr(ex)[:200], 0)]
    for i, t in enumerate(spec['tests']):
        t0 = time.time()
        try:
            actual = eval(t['call'], ns); expect = eval(t['expect'], ns)
            ok = close(actual, expect, t.get('tol', {'rel': 1e-9}))
            res.append((i, bool(ok), '' if ok else 'wrong value', time.time() - t0))
        except Exception as ex:
            res.append((i, False, 'error ' + repr(ex)[:150], time.time() - t0))
    return res
`);
let bad = 0;
for (const { id, w } of widgets) {
  py.globals.set('SPEC', JSON.stringify({ prelude: w.prelude || '', tests: w.tests }));
  py.globals.set('EX', JSON.stringify({ prelude: w.prelude || '', tests: w.examples }));
  py.globals.set('SOL', w.solution); py.globals.set('STA', w.starter);
  const r = JSON.parse(py.runPython(`
spec = json.loads(SPEC); ex = json.loads(EX)
json.dumps({'sol': run_widget(spec, SOL), 'ex': run_widget(ex, SOL), 'sta': run_widget(spec, STA)})
`));
  const solFail = r.sol.filter(x => !x[1]), exFail = r.ex.filter(x => !x[1]), staPass = r.sta.filter(x => x[1]);
  const slowest = Math.max(...r.sol.map(x => x[3])).toFixed(3);
  console.log(`${id}: solution ${r.sol.length - solFail.length}/${r.sol.length} (slowest ${slowest} s), examples ${r.ex.length - exFail.length}/${r.ex.length}, starter passes ${staPass.length}/${r.sta.length}`);
  console.log('   starter results: ' + r.sta.map(x => (x[1] ? 'pass' : 'FAIL') + (x[2] ? ' (' + x[2].slice(0, 22) + ')' : '')).join(' | '));
  for (const x of solFail) console.log('   SOLUTION FAIL', JSON.stringify(x));
  if (solFail.length || exFail.length || staPass.length === r.sta.length) bad++;
}
console.log(bad ? 'PROBLEMS ' + bad : 'ALL PYTHON CODE OK');
