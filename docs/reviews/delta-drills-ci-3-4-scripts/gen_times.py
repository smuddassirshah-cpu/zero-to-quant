"""Write a Python script that times chosen solutions test by test, to run natively or in Pyodide.
From the repo root:
  <venv python> docs/reviews/delta-drills-ci-3-4-scripts/gen_times.py > <scratch>/times.py
  <venv python> <scratch>/times.py                                   (CPython)
  node docs/reviews/drills-ci-3-4-scripts/pyodide_time.mjs <pkgs>/pyodide-0.27.7/package <scratch>/times.py   (Pyodide under V8)
Each line: drill, label, seconds per test over 0.05 s, the total, and PASS or the failing tests.
The last block runs the tests proposed in the delta review (PROPOSED) on the model and on the candidate they are meant to stop;
a candidate that would not finish is given a small step budget instead of being run to the end."""
import inspect, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, '..', 'drills-ci-3-4-scripts'))
sys.path.insert(0, here)
import wrong, extra_cands  # noqa: E402

D = lambda i: json.load(open('app/content/drills/%s.json' % i))
jobs = []
def add(did, label, code, tests=None):
    d = D(did); jobs.append((did, label, d['fn'], code, tests or d['tests']))
def src(mod, name, fn):
    return 'import bisect, heapq, re, sys\nfrom array import array\nfrom collections import Counter, deque\n' + inspect.getsource(getattr(mod, name)).replace(name, fn)

d = D('ci-live-median')
add('ci-live-median', 'model', d['solution'])
add('ci-live-median', 'planted[3] sorted list', d['planted'][3]['code'])
add('ci-live-median', 'sorted list in array("i")', src(extra_cands, 'solve_live_median__array', 'solve_live_median'))
d = D('ci-board-words')
add('ci-board-words', 'model', d['solution'])
add('ci-board-words', 'per word (first reader)', src(wrong, 'board_words__per_word', 'board_words'))
add('ci-board-words', 'per word, counts first (first reader)', src(wrong, 'board_words__per_word_counts', 'board_words'))
d = D('ci-ring-lookup')
add('ci-ring-lookup', 'model', d['solution'])
add('ci-ring-lookup', 'dict, absent id walks up', src(extra_cands, 'find_in_ring__dict_probe', 'find_in_ring'))
d = D('ci-tick-ranges')
add('ci-tick-ranges', 'model', d['solution'])
add('ci-tick-ranges', 'dicts, absent time walks up', src(extra_cands, 'solve_tick_ranges__dict_probe', 'solve_tick_ranges'))

PROPOSED = {
    'ci-ring-lookup': [
        {'call': "(lambda r: (len(r), sum(r), r.count(-1)))(find_in_ring([10000 * ((i + 61729) % 100000) for i in range(100000)], [(i * 7919) % 999999937 for i in range(100000)]))", 'expect': None},
    ],
    'ci-tick-ranges': [
        {'call': "(lambda r: (r.count('\\n'), sum(map(int, r.split()))))(solve_tick_ranges('100000 100000\\n' + ' '.join(str(10000000 * (i // 2)) for i in range(100000)) + '\\n' + ' '.join(str((i * 7919) % 499999999993) for i in range(100000)) + '\\n'))", 'expect': None},
    ],
}
for did, tests in PROPOSED.items():
    d = D(did)
    add(did, 'model on the proposed test', d['solution'], tests)

print('import time, json')
print('JOBS = json.loads(%r)' % json.dumps(jobs))
print('''
for did, label, fn, code, tests in JOBS:
    ns = {}
    exec(code, ns)
    slow, bad, total = [], [], 0.0
    for i, t in enumerate(tests):
        t0 = time.time()
        try:
            got = eval(t['call'], {fn: ns[fn]})
            if t['expect'] is None:
                print('   value:', repr(got)); ok = True
            else:
                ok = got == eval(t['expect'])
        except BaseException as e:
            ok = False
        dt = time.time() - t0
        total += dt
        if dt > 0.05: slow.append('t%d %.2f' % (i, dt))
        if not ok: bad.append('t%d' % i)
    print(did, '|', label, '|', ', '.join(slow), '| total %.2f s |' % total, 'PASS' if not bad else 'FAILS ' + ' '.join(bad))
''')
