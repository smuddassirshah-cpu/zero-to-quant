"""Time solutions in Pyodide 0.27.7 under node: all hidden tests of the drill in one run, as the page
runs them against its shared 5 s limit. No browser is used.
usage: pyo_time.py <drills dir> <pkgs> [--cap seconds] label [label ...]
A label is a key of right.py or wrong.py, MODEL:<drill id>, or PLANTED:<drill id>:<n>.
Prints per label: seconds over all tests, the slowest test, and tests failed (by value or exception).
A node stack overflow or a kill at the cap is reported as such."""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks  # noqa: E402

PY_SCRIPT = r'''
import json, time
spec = json.load(open('/spec.json'))
ns = {}
exec(spec['code'], ns)
times, fails = [], []
t0 = time.time()
for i, c in enumerate(spec['cases']):
    t1 = time.time()
    try:
        ok = eval(c['call'], ns) == eval(c['expect'], ns)
    except BaseException as e:
        ok = False
        fails.append('t%d:%s' % (i, type(e).__name__))
    else:
        if not ok:
            fails.append('t%d' % i)
    times.append(round(time.time() - t1, 3))
print('PYO', json.dumps({'s': round(time.time() - t0, 3), 'times': times, 'fails': fails}))
'''
JS = r'''
import fs from 'node:fs'; import path from 'node:path';
const dir = path.resolve(process.argv[2]);
const { loadPyodide } = await import(path.join(dir, 'pyodide.mjs'));
const py = await loadPyodide({ indexURL: dir + '/' });
py.FS.writeFile('/spec.json', fs.readFileSync(process.argv[3], 'utf8'));
py.runPython(fs.readFileSync(process.argv[4], 'utf8'));
'''


def run(code, cases, pkg, cap):
    with tempfile.TemporaryDirectory() as tmp:
        spec, script, js = (os.path.join(tmp, f) for f in ('spec.json', 't.py', 't.mjs'))
        json.dump({'code': code, 'cases': cases}, open(spec, 'w'))
        open(script, 'w').write(PY_SCRIPT)
        open(js, 'w').write(JS)
        try:
            r = subprocess.run(['node', js, pkg, spec, script], capture_output=True, text=True, timeout=cap + 10)
        except subprocess.TimeoutExpired:
            return 'still running at %d s' % cap
        line = [ln for ln in r.stdout.splitlines() if ln.startswith('PYO ')]
        if not line:
            return 'no result: ' + (r.stderr.strip().splitlines() or ['?'])[-1][:150]
        d = json.loads(line[-1][4:])
        slow = max(range(len(d['times'])), key=lambda i: d['times'][i])
        return '%6.2f s  slowest t%d %.2f s  %s' % (d['s'], slow, d['times'][slow], 'fails ' + ' '.join(d['fails'][:6]) if d['fails'] else 'all pass')


if __name__ == '__main__':
    drills = checks.load(sys.argv[1])
    pkg = os.path.join(sys.argv[2], 'pyodide-0.27.7', 'package')
    args = sys.argv[3:]
    cap = 40
    if args[0] == '--cap':
        cap = float(args[1])
        args = args[2:]
    C = {}
    for name in ('right.py', 'wrong.py'):
        e = {}
        exec(open(os.path.join(HERE, name)).read(), e)
        C.update(e['CANDIDATES'])
    for label in args:
        if label.startswith('MODEL:'):
            did = label[6:]
            code = drills[did]['solution']
        elif label.startswith('PLANTED:'):
            _, did, n = label.split(':')
            code = drills[did]['planted'][int(n)]['code']
        else:
            did, code, _ = C[label]
        print('%-34s %-18s %s' % (label, did, run(code, drills[did]['tests'], pkg, cap)), flush=True)
