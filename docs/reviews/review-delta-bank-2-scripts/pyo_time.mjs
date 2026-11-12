/* Times the borderline candidates of cands.py in Pyodide 0.27.7 under node (V8, the engine Chromium uses), one hidden
   test at a time, against the page's 5 s limit per case. Models are timed too.
   usage (repo root): node docs/reviews/review-delta-bank-2-scripts/pyo_time.mjs <pkgs>/pyodide-0.27.7/package */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const dir = path.resolve(process.argv[2]);
const { loadPyodide } = await import(path.join(dir, 'pyodide.mjs'));
const py = await loadPyodide({ indexURL: dir + '/' });
const bank = {};
for (const n of [1, 2, 3, 4]) bank[n] = fs.readFileSync(path.join(here, '../../../app/content/bank', `coding-${n}.json`), 'utf8');
py.globals.set('BANK', py.toPy(bank));
py.globals.set('CANDS_SRC', fs.readFileSync(path.join(here, 'cands.py'), 'utf8'));
py.runPython(`
import json, time, sys
sys.setrecursionlimit(3000)
ns = {}
exec(CANDS_SRC, ns)
C = ns['C']
items = {}
for n, txt in BANK.items():
    for it in json.loads(txt)['items']:
        if it['widget']['kind'] == 'code':
            items[it['id']] = it
PAIRS = [  # only candidates that CPython finishes inside 4 s a case (code_run.py); the rest are far over the limit here
 ('ds-pointers-merge-ticks', 'alt:pop0-on-copies'), ('pf-collections-top-symbols', 'alt:first-seen-list'),
 ('at-search-count-in-range', 'slice-len'), ('at-search-count-in-range', 'index-method'),
 ('at-greedy-orders-to-fill', 'alt:pop-front'), ('ds-hashing-price-mode', 'alt:count-quadratic'),
]
def timed(src, tests, cap=40.0):
    out = []
    for c in tests:
        env = {}
        exec(src, env)
        t = time.perf_counter()
        try:
            if c.get('setup'): exec(c['setup'], env)
            a = eval(c['call'], env)
            ok = a == eval(c['expect'], env)
        except Exception as x:
            ok = type(x).__name__
        dt = time.perf_counter() - t
        out.append((round(dt, 2), ok))
        if dt > cap: break
    return out
for iid in sorted(set(p[0] for p in PAIRS)):
    w = items[iid]['widget']
    r = timed(w['solution'], w['tests'])
    print(f'{iid} model: slowest case {max(x[0] for x in r)} s')
for iid, nm in PAIRS:
    w = items[iid]['widget']
    src = next(s for m, _, s in C[iid] if m == nm)
    # only the large tests can be slow; time the last three
    r = timed(src, w['tests'][-3:])
    worst = max(x[0] for x in r)
    print(f'{iid} | {nm} | last three tests (s, right?) {r} | ' + ('STOPPED in the page (over 5 s)' if worst > 5 else 'runs inside 5 s'))
`);
