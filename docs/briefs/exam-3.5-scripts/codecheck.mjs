// node codecheck.mjs <pkgs>
// Runs the two Python code widgets of topic-3.5 in Pyodide 0.27.7 (the app's runtime): the solution passes every
// hidden test and example, the untouched starter does not, and a slow answer (a dict scan on every call) is timed
// on the large ActiveSymbols test.
import fs from 'fs'; import path from 'path'; import { createRequire } from 'module'; import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(process.argv[2], 'pyodide-0.27.7/package') + '/';
const exam = JSON.parse(fs.readFileSync(path.join(here, '../../../app/content/exams/topic-3.5.json'), 'utf8'));
const widgets = [];
for (const it of exam.items) if (it.widget && it.widget.kind === 'code' && it.widget.language === 'python') widgets.push({ id: it.id, w: it.widget });
const require = createRequire(root);
const { loadPyodide } = require(root + 'pyodide.js');
const py = await loadPyodide({ indexURL: root, stdout: () => {}, stderr: () => {} });
await py.loadPackage(['numpy', 'pandas']);
py.runPython(`
import json, time, math
def run_widget(spec, source):
    ns = {'__name__': '__main__'}
    res = []
    try:
        if spec.get('prelude'): exec(spec['prelude'], ns)
        ns['__learner_source__'] = source
        exec(source, ns)
    except Exception as ex:
        return [('load', False, repr(ex)[:200], 0)]
    for i, t in enumerate(spec['tests']):
        t0 = time.time()
        try:
            if t.get('setup'): exec(t['setup'], ns)
            actual = eval(t['call'], ns); expect = eval(t['expect'], ns)
            ok = actual == expect
            res.append((i, bool(ok), '' if ok else 'got %r expected %r' % (actual, expect), time.time() - t0))
        except Exception as ex:
            res.append((i, False, 'error ' + repr(ex)[:150], time.time() - t0))
    return res
SCAN = '''
class ActiveSymbols:
    def __init__(self, window):
        self.w = window
        self.last = {}
    def tick(self, symbol, t):
        self.last[symbol] = t
    def active(self, t):
        return sum(1 for u in self.last.values() if u > t - self.w)
'''
`);
let bad = 0;
for (const { id, w } of widgets) {
  py.globals.set('SPEC', JSON.stringify({ prelude: w.prelude || '', tests: w.tests }));
  py.globals.set('EX', JSON.stringify({ prelude: w.prelude || '', tests: w.examples }));
  py.globals.set('SOL', w.solution); py.globals.set('STA', w.starter); py.globals.set('ID', id);
  const out = py.runPython(`
spec = json.loads(SPEC); ex = json.loads(EX)
r = {'sol': run_widget(spec, SOL), 'ex': run_widget(ex, SOL), 'sta': run_widget(spec, STA)}
if ID == 'e-active-symbols': r['scan'] = run_widget(spec, SCAN)
json.dumps(r)
`);
  const r = JSON.parse(out);
  const solFail = r.sol.filter(x => !x[1]), exFail = r.ex.filter(x => !x[1]), staPass = r.sta.filter(x => x[1]);
  const slowest = Math.max(...r.sol.map(x => x[3])).toFixed(2);
  console.log(`${id}: solution ${r.sol.length - solFail.length}/${r.sol.length} (slowest ${slowest} s), examples ${r.ex.length - exFail.length}/${r.ex.length}, starter passes ${staPass.length}/${r.sta.length}`);
  for (const x of solFail) console.log('   SOLUTION FAIL', JSON.stringify(x));
  if (r.scan) console.log('   dict scan: ' + r.scan.map(x => (x[1] ? 'pass ' : 'fail ') + x[3].toFixed(1) + 's').join(', '));
  if (solFail.length || exFail.length || staPass.length === r.sta.length) bad++;
}
console.log(bad ? 'PROBLEMS ' + bad : 'ALL PYTHON CODE OK');
