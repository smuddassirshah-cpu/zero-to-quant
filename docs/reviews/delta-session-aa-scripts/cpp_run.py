"""Delta read, session AA: the 25 `cpp` drills after the fix pass (d71960f), against the files before it.

Run from the repo root with the scratchpad venv Python (native compiler; CXX=clang++ for the second one):
    ZQ_TMP=<scratch dir> python docs/reviews/delta-session-aa-scripts/cpp_run.py [fuzz]

Uses the first reader's harness (docs/reviews/drills-cpp-scripts/harness.py) for building and comparing.
For every drill: model on every example and test, starter, each planted solution (NEW marks one the fix pass added,
with the tests it fails and what it returned), my own solution where tests or starter changed (mine_cpp.py), the
`how` count, the index row, and the probes of mine_cpp.PROBES. `fuzz` adds a differential run of cpp-fill-csv
(model and mine against a Python reading of the brief on random texts). Exits 1 on any problem.
"""
import importlib.util
import json
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BEFORE = 'd71960f^'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = load(os.path.join(HERE, '..', 'drills-cpp-scripts', 'harness.py'), 'harness')
M = load(os.path.join(HERE, 'mine_cpp.py'), 'mine_cpp')


def old(i):
    r = subprocess.run(['git', 'show', f'{BEFORE}:app/content/drills/{i}.json'], capture_output=True, text=True, cwd=ROOT)
    return json.loads(r.stdout)


def key(t):
    return json.dumps({k: t.get(k) for k in ('call', 'args', 'expect', 'compiles')}, sort_keys=True)


index = {r['id']: r for r in json.load(open(os.path.join(ROOT, 'app/content/drills/index.json')))}
bad = 0
mix = {}
for d in H.drills():
    k = d['id']
    o = old(k)
    ne = len(d['examples'])
    oldkeys = {key(t) for t in o['examples'] + o['tests']}
    newt = [j for j, t in enumerate(d['tests']) if key(t) not in oldkeys]
    r = H.run(d, d['solution'])
    f = H.fails(r)
    line = [f'{k:20} d{d["difficulty"]} tests {len(d["tests"]):2}', 'model ok' if not f else f'MODEL FAILS {f}']
    bad += bool(f)
    s = H.fails(H.run(d, d['starter'], d['tests']))
    line.append(f'starter fails {len(s)}/{len(d["tests"])}' + (' (changed)' if d['starter'] != o['starter'] else ''))
    bad += not s
    if k in M.SOLUTIONS:
        r = H.run(d, M.SOLUTIONS[k])
        f = H.fails(r)
        line.append('mine ok' if not f else f'MINE DISAGREES {[(j, str(r[j][1])[:60]) for j in f]}')
        bad += bool(f)
    m = re.search(r'Submit runs (\d+) hidden tests', d.get('how', ''))
    if not m or int(m.group(1)) != len(d['tests']):
        line.append('HOW COUNT WRONG')
        bad += 1
    row = index.get(k)
    if not row or any(row.get(a) != d.get(a) for a in ('name', 'course', 'difficulty')):
        line.append(f'INDEX ROW DIFFERS {row}')
        bad += 1
    mix.setdefault((d['course'], d['difficulty']), []).append(k)
    print(' | '.join(line) + (f' | new or changed tests {newt}' if newt else ''))
    oldslips = {p['slip'] for p in o.get('planted', [])}
    oldcode = {p['code'] for p in o.get('planted', [])}
    for j, p in enumerate(d.get('planted', [])):
        r = H.run(d, p['code'], d['tests'])
        f = H.fails(r)
        if not f:
            print(f'      planted[{j}] PASSES EVERY HIDDEN TEST: {p["slip"]}')
            bad += 1
        elif p['code'] not in oldcode:
            only_new = all(x in newt for x in f)
            print(f'      planted[{j}] NEW fails tests {f}{" (new tests only)" if only_new else ""} -> {str(r[f[0]][1])[:70]} | {p["slip"]}')
    for (pid, name, expect_pass), code in M.PROBES.items():
        if pid != k:
            continue
        r = H.run(d, code, d['tests'])
        f = H.fails(r)
        verdict = 'passes every hidden test' if not f else f'fails tests {f} -> {str(r[f[0]][1])[:80]}'
        print(f'      probe "{name}": {verdict}')
        if expect_pass is not None and expect_pass != (not f):
            bad += 1
print('mix by course and difficulty:', {f'{a} d{b}': len(v) for (a, b), v in sorted(mix.items())})

if 'fuzz' in sys.argv:
    def ref(text):
        """The brief of cpp-fill-csv, read directly."""
        total = 0
        for line in text.split('\n'):
            if line.endswith('\r'):
                line = line[:-1]
            parts = line.split(',')
            if len(parts) != 2:
                continue
            q, p = parts
            if not re.fullmatch(r'-?[0-9]+', q) or not re.fullmatch(r'[0-9]+', p):
                continue
            total += int(q) * int(p)
        return total
    rng = random.Random(20261110)
    cases = []
    for _ in range(400):
        n = rng.randint(0, 14)
        text = ''.join(rng.choice('0123456789' * 3 + ',,,--\r\n\n\n +x') for _ in range(n))
        cases.append({'call': 'fills_value', 'args': [text], 'types': ['std::string'], 'expect': ref(text), 'compare': 'equal'})
    d = next(x for x in H.drills() if x['id'] == 'cpp-fill-csv')
    for who, code in (('model', d['solution']), ('mine', M.SOLUTIONS['cpp-fill-csv'])):
        r = H.run(d, code, cases)
        f = H.fails(r)
        print(f'fuzz cpp-fill-csv {who}: {len(cases) - len(f)} of {len(cases)} agree with the brief read in Python'
              + (f'; first {json.dumps(cases[f[0]]["args"][0])} -> {r[f[0]][1]} want {cases[f[0]]["expect"]}' if f else ''))
        bad += bool(f)
# The test this review proposes for cpp-fill-csv (finding 2), in place of tests[14]: the model and my solution give 6,
# the probe that drops every \r at a line end gives 18, and planted[4] (drops every \r) still fails.
d = next(x for x in H.drills() if x['id'] == 'cpp-fill-csv')
case = [{'call': 'fills_value', 'args': ["1\r2,5\n3,4\r\r\n6,1\n"], 'types': ['std::string'], 'expect': 6, 'compare': 'equal'}]
probe = next(c for (i, name, _), c in M.PROBES.items() if i == 'cpp-fill-csv')
got = {'model': H.run(d, d['solution'], case)[0], 'mine': H.run(d, M.SOLUTIONS['cpp-fill-csv'], case)[0],
       'probe': H.run(d, probe, case)[0], 'planted[4]': H.run(d, d['planted'][4]['code'], case)[0]}
print('proposed cpp-fill-csv test:', got)
bad += not (got['model'][0] and got['mine'][0] and not got['probe'][0] and not got['planted[4]'][0])
print('problems:', bad, '| compiler', H.CXX)
sys.exit(1 if bad else 0)
