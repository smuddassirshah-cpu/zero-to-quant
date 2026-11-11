"""Check the tests proposed in extra_tests.json.
usage: extra_checks.py <drills dir> [--pyodide <pkgs>]
For each proposed test: the call is inside the prose constraints (checks.py),
the model solution and mine.py both give a value (printed; it must equal the
proposed expect), every planted solution's verdict is unchanged or better, and
each candidate of wrong.py named in "kills" returns something else or runs out
of time (limit 20 s natively for the one call).
With --pyodide, the model and each named candidate are also timed on the one
call in Pyodide under node (cap 40 s)."""
import json
import multiprocessing as mp
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks  # noqa: E402

PYO_PY = r'''
import json, time
spec = json.load(open('/spec.json'))
ns = {}
exec(spec['code'], ns)
t0 = time.time()
try:
    got = repr(eval(spec['call'], ns))
except BaseException as e:
    got = type(e).__name__
print('PYO', json.dumps({'s': round(time.time() - t0, 2), 'got': got[:60]}))
'''
PYO_JS = r'''
import fs from 'node:fs'; import path from 'node:path';
const dir = path.resolve(process.argv[2]);
const { loadPyodide } = await import(path.join(dir, 'pyodide.mjs'));
const py = await loadPyodide({ indexURL: dir + '/' });
py.FS.writeFile('/spec.json', fs.readFileSync(process.argv[3], 'utf8'));
py.runPython(fs.readFileSync(process.argv[4], 'utf8'));
'''


def pyo(pkgs, code, call, cap=40):
    with tempfile.TemporaryDirectory() as tmp:
        spec, script, js = (os.path.join(tmp, f) for f in ('spec.json', 't.py', 't.mjs'))
        json.dump({'code': code, 'call': call}, open(spec, 'w'))
        open(script, 'w').write(PYO_PY)
        open(js, 'w').write(PYO_JS)
        pkg = os.path.join(pkgs, 'pyodide-0.27.7', 'package')
        try:
            r = subprocess.run(['node', js, pkg, spec, script], capture_output=True, text=True, timeout=cap + 20)
        except subprocess.TimeoutExpired:
            return 'over %d s' % cap
        line = [x for x in r.stdout.splitlines() if x.startswith('PYO ')]
        if not line:
            return 'died: ' + (r.stderr.strip().splitlines() or ['?'])[-1][:80]
        d = json.loads(line[-1][4:])
        return '%s s -> %s' % (d['s'], d['got'])


def _one(src, call, q):
    env = {}
    exec(src, env)
    t0 = time.time()
    try:
        got = repr(eval(call, env))
    except BaseException as e:  # noqa
        got = type(e).__name__
    q.put((got, time.time() - t0))


def one(src, call, limit=20):
    q = mp.Queue()
    p = mp.Process(target=_one, args=(src, call, q))
    p.start()
    p.join(limit)
    if p.is_alive():
        p.terminate()
        return 'TIME', limit
    return q.get(timeout=2)


if __name__ == '__main__':
    drills = checks.load(sys.argv[1])
    pkgs = sys.argv[sys.argv.index('--pyodide') + 1] if '--pyodide' in sys.argv else None
    extra = json.load(open(os.path.join(HERE, 'extra_tests.json')))
    wrong = {}
    exec(open(os.path.join(HERE, 'wrong.py')).read(), wrong)
    mine = open(os.path.join(HERE, 'mine.py')).read()
    bad = 0
    for did, tests in extra.items():
        j = drills[did]
        name = checks.fn_name(j)
        for t in tests:
            rec = []

            def recorder(*a, **k):
                rec.append(a)
                raise RuntimeError('recorded')
            try:
                eval(t['call'], {name: recorder})
            except RuntimeError:
                pass
            try:
                checks.CHECK[did](*rec[0])
                inside = 'inside constraints'
            except AssertionError as e:
                inside = 'OUTSIDE %s' % e
                bad += 1
            m, tm = one(j['solution'], t['call'])
            y, ty = one(mine, t['call'])
            ok = m == y == repr(eval(t['expect']))
            bad += not ok
            print('%s | %s' % (did, t['call'][:70]))
            print('   %s; model %s (%.2f s), mine %s (%.2f s), expect %s: %s' % (inside, m[:40], tm, y[:40], ty, t['expect'], 'agree' if ok else 'DISAGREE'))
            if pkgs:
                print('   pyodide model: %s' % pyo(pkgs, j['solution'], t['call']))
            for label in t['kills']:
                code = wrong['CANDIDATES'][label][1]
                g, tg = one(code, t['call'])
                dead = g != m
                bad += not dead
                line = '   %-44s %s (%.1f s) %s' % (label, g[:30], tg, 'caught' if dead else 'STILL PASSES')
                if pkgs:
                    line += ' | pyodide: %s' % pyo(pkgs, code, t['call'])
                print(line)
            for k, p in enumerate(j['planted']):
                g, tg = one(p['code'], t['call'], limit=6)
                if g == m:
                    continue
                print('   planted[%d] also fails here (%s)' % (k, g[:24]))
    print('extra tests: %d problems' % bad)
