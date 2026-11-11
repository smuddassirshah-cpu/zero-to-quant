"""Put candidates from wrong.py and right.py into a COPY of app/, to run them on the drill page
(Chromium and Pyodide) through planted-check. Never point this at the real app/: it rewrites drill files.

usage: page_probe.py <copy of app> [--tests] [--model] <label> [<label> ...]
Then, from the real app/:
  ZQ_APP_DIR=<copy> node tools/planted-check.mjs --drill <id> ... --local-cdn <pkgs>
Default: the candidates become the drill's `planted` list, so a line "FAIL <id>: ..." means that
candidate passes every hidden test in the browser.
--tests: the proposed tests of extra_tests.json are put in first (and the tests they replace taken
out), so 0 failures means the model passes and every candidate is now caught.
--model: the first candidate of a drill becomes its model solution and the starter its one plant, so
the line "the model solution passes X of Y hidden tests" says how a right solution in another
style fares on the page."""
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
app = os.path.abspath(sys.argv[1])
assert app != os.path.abspath(os.path.join(here, '..', '..', '..', 'app')), 'use a copy'
with_tests = '--tests' in sys.argv
as_model = '--model' in sys.argv
labels = [a for a in sys.argv[2:] if a not in ('--tests', '--model')]
C = {}
for name in ('wrong.py', 'right.py'):
    e = {}
    exec(open(os.path.join(here, name)).read(), e)
    C.update(e['CANDIDATES'])
extra = json.load(open(os.path.join(here, 'extra_tests.json')))
todo = {}
for label in labels:
    did, code, _ = C[label]
    todo.setdefault(did, []).append((label, code))
for did, cands in todo.items():
    f = os.path.join(app, 'content', 'drills', did + '.json')
    d = json.load(open(f))
    d['planted'] = [{'code': code.strip() + '\n', 'slip': label} for label, code in cands]
    if as_model:
        d['solution'] = cands[0][1].strip() + '\n'
        d['planted'] = [{'code': d['starter'], 'slip': 'starter'}]
    if with_tests:
        new = extra.get(did, [])
        drop = {t['replaces'] for t in new if 'replaces' in t}
        d['tests'] = [t for i, t in enumerate(d['tests']) if i not in drop] + [{k: t[k] for k in ('call', 'expect', 'compare')} for t in new]
    json.dump(d, open(f, 'w'), indent=2)
    print(did, [p['slip'] for p in d['planted']], len(d['tests']), 'tests', '(model replaced)' if as_model else '')
print('ids:', ' '.join('--drill ' + d for d in todo))
