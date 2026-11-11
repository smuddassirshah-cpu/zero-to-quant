"""Check the tests proposed in extra_tests.json.
usage: extra_checks.py <drills dir>
For each proposed test: the call is inside the prose constraints (checks.py),
the model solution and mine.py both return the proposed expect, and each
candidate of wrong.py named in "kills" returns something else, raises, or is
still running at 20 s (natively; the browser runs are in the review)."""
import json
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks  # noqa: E402


def one(code, call, q):
    env = {}
    exec(code, env)
    t0 = time.time()
    try:
        got = repr(eval(call, env))
    except BaseException as e:  # noqa
        got = type(e).__name__
    q.put((got, time.time() - t0))


def run(code, call, cap=20):
    q = mp.Queue()
    p = mp.Process(target=one, args=(code, call, q))
    p.start()
    p.join(cap)
    if p.is_alive():
        p.terminate()
        return ('still running', cap)
    return q.get(timeout=2)


if __name__ == '__main__':
    drills = checks.load(sys.argv[1])
    extra = json.load(open(os.path.join(HERE, 'extra_tests.json')))
    w = {}
    exec(open(os.path.join(HERE, 'wrong.py')).read(), w)
    mine = open(os.path.join(HERE, 'mine.py')).read()
    bad = 0
    for did, tests in extra.items():
        j = drills[did]
        fn = j['fn']
        for t in tests:
            seen = []
            eval(t['call'], {fn: lambda *a: seen.append(a) or 0})
            getattr(checks, 'c_' + fn)(*seen[0])
            want = repr(eval(t['expect']))
            a, ta = run(j['solution'], t['call'])
            b, _ = run(mine, t['call'])
            ok = a == b == want
            bad += not ok
            line = '%s %s | model %s (%.2fs) mine %s %s' % (did, t['call'][:50], a[:30], ta, b[:30], 'ok' if ok else 'MISMATCH want ' + want)
            for label in t['kills']:
                g, tg = run(w['CANDIDATES'][label][1], t['call'])
                killed = g != want
                bad += not killed
                line += '\n     %s -> %s (%.1fs) %s' % (label, g[:30], tg, 'killed' if killed else 'NOT KILLED')
            print(line)
    print('%d problems' % bad)
