"""Put candidates from wrong.py, wrong2.py and wrong3.py into a COPY of app/ as `planted`, to run them in
Chromium and Pyodide through planted-check.

usage: pyodide_probe.py <copy of app> [--tests] <label> [<label> ...]
Then, from the real app/:
  ZQ_APP_DIR=<copy> node tools/planted-check.mjs --drill <id> ... --local-cdn <pkgs>
Without --tests a line "FAIL <id>: ..." there means the candidate passes every
hidden test in the browser. With --tests the proposed tests of extra_tests.json
are appended first, and 0 failures means the model passes and every candidate
is now caught. With --model the first candidate of a drill is put in as the
model solution, so the line 'the model solution passes X of Y hidden tests' and
its reason say how a candidate fails in the browser. Never point this at the real app/: it rewrites drill files."""
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
app = os.path.abspath(sys.argv[1])
assert app != os.path.abspath(os.path.join(here, '..', '..', '..', 'app')), 'use a copy'
with_tests = '--tests' in sys.argv
as_model = '--model' in sys.argv
labels = [a for a in sys.argv[2:] if a not in ('--tests', '--model')]
w = {'CANDIDATES': {}}
for name in ('wrong.py', 'wrong2.py', 'wrong3.py'):
    if os.path.exists(os.path.join(here, name)):
        e = {}
        exec(open(os.path.join(here, name)).read(), e)
        w['CANDIDATES'].update(e['CANDIDATES'])
extra = json.load(open(os.path.join(here, 'extra_tests.json'))) if os.path.exists(os.path.join(here, 'extra_tests.json')) else {}
todo = {}
for label in labels:
    did, code, _ = w['CANDIDATES'][label]
    todo.setdefault(did, []).append((label, code))
for did, cands in todo.items():
    f = os.path.join(app, 'content', 'drills', did + '.json')
    d = json.load(open(f))
    d['planted'] = [{'code': code.strip() + '\n', 'slip': label} for label, code in cands]
    if as_model:
        d['solution'] = cands[0][1].strip() + '\n'
        d['planted'] = [{'code': d['starter'], 'slip': 'starter'}]
    if with_tests:
        d['tests'] += [{k: t[k] for k in ('call', 'expect', 'compare')} for t in extra.get(did, [])]
    json.dump(d, open(f, 'w'), indent=2)
    print(did, [p['slip'] for p in d['planted']], len(d['tests']), 'tests')
print('ids:', ' '.join('--drill ' + d for d in todo))
