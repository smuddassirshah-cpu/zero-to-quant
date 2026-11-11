"""Delta read, session AA: the 30 `py` drills after the fix pass (7fde608), against the files before it.

Run from the repo root with the scratchpad venv Python:
    python docs/reviews/delta-session-aa-scripts/py_run.py

For every drill: the model on every example and hidden test, the starter, each planted solution (NEW marks one the
fix pass added, with the cases it fails and what it returned), my own solution where the tests changed (mine_py.py),
the `how` count against the number of tests, and the index row against the file. Comparison is the review harness's
copy of the page's `__zq_eq`. Exits 1 on any problem.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import warnings

warnings.simplefilter('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BEFORE = '7fde608^'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = load(os.path.join(HERE, '..', 'drills-py-scripts', 'harness.py'), 'harness')
MINE = load(os.path.join(HERE, 'mine_py.py'), 'mine_py').SOLUTIONS


def old(i):
    r = subprocess.run(['git', 'show', f'{BEFORE}:app/content/drills/{i}.json'], capture_output=True, text=True, cwd=ROOT)
    return json.loads(r.stdout)


ds = H.drills()
index = {r['id']: r for r in json.load(open(os.path.join(ROOT, 'app/content/drills/index.json')))['drills']} \
    if isinstance(json.load(open(os.path.join(ROOT, 'app/content/drills/index.json'))), dict) else \
    {r['id']: r for r in json.load(open(os.path.join(ROOT, 'app/content/drills/index.json')))}
work = tempfile.mkdtemp()
for d in ds.values():
    for name, src in (d.get('data') or {}).items():
        shutil.copy(os.path.join(ROOT, 'app', src), os.path.join(work, name))
os.chdir(work)
bad = 0
mix = {}
for k, d in ds.items():
    o = old(k)
    n = len(d.get('examples', [])) + len(d['tests'])
    oldcases = {(t['call'], t['expect']) for t in o.get('examples', []) + o['tests']}
    newt = [f't{j}' for j, t in enumerate(d['tests']) if (t['call'], t['expect']) not in oldcases]
    line = [f'{k:26} d{d["difficulty"]} tests {len(d["tests"])}']
    f = H.run_all(d, d['solution'])
    line.append('model ok' if not f else f'MODEL FAILS {f}')
    bad += bool(f)
    f = H.run_all(d, d['starter'])
    hidden = [x for x in f if x[0].startswith('t')]
    line.append(f'starter fails {len(hidden)}/{len(d["tests"])}')
    bad += not hidden
    if k in MINE:
        f = H.run_all(d, MINE[k])
        line.append('mine ok' if not f else f'MINE DISAGREES {f}')
        bad += bool(f)
    m = re.search(r'Submit runs (\d+) hidden tests', d.get('how', ''))
    if not m or int(m.group(1)) != len(d['tests']):
        line.append('HOW COUNT WRONG')
        bad += 1
    row = index.get(k)
    if not row or any(row.get(a) != d.get(a) for a in ('name', 'course', 'difficulty')):
        line.append(f'INDEX ROW DIFFERS {row}')
        bad += 1
    mix.setdefault(d['difficulty'], []).append(k)
    print(' | '.join(line) + (f' | new or changed tests {newt}' if newt else ''))
    oldpl = {p['code'] for p in o.get('planted', [])}
    oldslips = {p['slip'] for p in o.get('planted', [])}
    for j, p in enumerate(d.get('planted', [])):
        f = [x for x in H.run_all(d, p['code']) if x[0].startswith('t')]
        new = p['slip'] not in oldslips
        if not f:
            print(f'      planted[{j}] PASSES EVERY HIDDEN TEST: {p["slip"]}')
            bad += 1
        elif new or (p['code'] not in oldpl and '-v' in sys.argv):
            print(f'      planted[{j}] NEW fails {[(a, b[:70]) for a, b in f][:3]} ({len(f)}) | {p["slip"]}')
        elif newt:
            hit = [a for a, _ in f if a in newt]
            if hit:
                print(f'      planted[{j}] (old) also fails new {hit}: {[b[:60] for a, b in f if a in newt][:2]}')
print('mix by difficulty:', {a: len(b) for a, b in sorted(mix.items())})
print('problems:', bad)
shutil.rmtree(work, ignore_errors=True)
sys.exit(1 if bad else 0)
