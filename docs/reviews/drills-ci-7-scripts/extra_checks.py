"""Computes every proposed test of extra_tests.json three ways where the input is
small (model solution, mine.py, the brute force of checks.py) and two ways where
it is large (model, mine.py), checks the arguments against the prose
constraints, and checks that each candidate named in `catches` now fails
natively (wrong value or still running at 10 s).
usage: extra_checks.py <drills dir>"""
import json
import multiprocessing as mp
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv, argv = [sys.argv[0]], sys.argv
import checks  # noqa: E402

D = argv[1]
extra = json.load(open(os.path.join(HERE, 'extra_tests.json')))
mine = {}
exec(open(os.path.join(HERE, 'mine.py')).read(), mine)
cands = {}
for name in ('wrong.py', 'wrong2.py'):
    e = {}
    exec(open(os.path.join(HERE, name)).read(), e)
    cands.update(e['CANDIDATES'])


def run(src, fn, call, q):
    env = {}
    exec(src, env)
    q.put(eval(call, env))


bad = 0
for did, tests in extra.items():
    j = json.load(open(os.path.join(D, did + '.json')))
    fn = j['fn']
    env = {}
    exec(j['solution'], env)
    for t in tests:
        want = eval(t['expect'])
        seen = []
        eval(t['call'], {fn: lambda *a: seen.append(a)})
        checks.PROSE[did](*seen[0])
        got = [eval(t['call'], env), eval(t['call'], {fn: mine[fn]})]
        small = len(repr(seen[0])) < 80
        if small:
            got.append(eval(t['call'], {fn: checks.RAND[did][1]}))
        ok = all(g == want for g in got)
        caught = []
        for label in t['catches']:
            q = mp.Queue()
            p = mp.Process(target=run, args=(cands[label][1], fn, t['call'], q))
            p.start()
            p.join(10)
            if p.is_alive():
                p.terminate()
                caught.append(label + ': still running at 10 s')
            else:
                r = q.get()
                caught.append(label + (': wrong value %r' % (r,))[:40] if r != want else label + ': NOT CAUGHT')
                bad += r == want
        bad += not ok
        print('%-22s %s | %d solutions agree: %s | %s' % (did, t['call'][:60], len(got), ok, '; '.join(caught)))
print('extra tests: %d problems' % bad)
