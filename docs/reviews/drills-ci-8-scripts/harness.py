"""Run a file of solutions against every example and hidden test of pack 8.
usage: harness.py <solutions.py> <drills dir> [--limit seconds]
A solutions file defines functions named as the drill's fn, or, for wrong
candidates, a dict CANDIDATES = {label: (drill id, source, comment)}.
Each candidate runs in its own process under a time limit for the whole run
(the page shares one 5 second limit; natively I allow the same)."""
import glob
import json
import multiprocessing as mp
import os
import sys
import time


def load(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, 'ci-*.json'))):
        j = json.load(open(f))
        if (j.get('tags') or [''])[0] == 'pack-8':
            out[j['id']] = j
    return out


def _run(src, drill, q):
    sys.setrecursionlimit(1000)
    env = {}
    try:
        exec(src, env)
    except Exception as e:  # noqa
        q.put(('load error %r' % e, []))
        return
    fails = []
    cases = [('ex', i, t) for i, t in enumerate(drill['examples'])] + [('t', i, t) for i, t in enumerate(drill['tests'])]
    t0 = time.time()
    for kind, i, t in cases:
        try:
            if t.get('setup'):
                exec(t['setup'], env)
            got = eval(t['call'], env)
            want = eval(t['expect'], env)
            if got != want:
                fails.append('%s%d' % (kind, i))
        except BaseException as e:  # noqa
            fails.append('%s%d:%s' % (kind, i, type(e).__name__))
    q.put(('%.2fs' % (time.time() - t0), fails))


def run(src, drill, limit):
    q = mp.Queue()
    p = mp.Process(target=_run, args=(src, drill, q))
    p.start()
    p.join(limit)
    if p.is_alive():
        p.terminate()
        p.join()
        return 'TIMEOUT>%ds' % limit, ['time']
    try:
        return q.get(timeout=2)
    except Exception:
        return 'CRASH', ['crash']


if __name__ == '__main__':
    path, d = sys.argv[1], sys.argv[2]
    limit = float(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else 5
    drills = load(d)
    src = open(path).read()
    env = {}
    exec(src, env)
    if 'CANDIDATES' in env:
        passed = 0
        for label, (did, code, comment) in env['CANDIDATES'].items():
            t, fails = run(code, drills[did], limit)
            if not fails:
                passed += 1
            print('%-34s %-24s %-12s %s' % (label, did, t, 'PASSES ALL' if not fails else 'caught: ' + ' '.join(fails[:6])))
        print('%d candidates, %d pass every test' % (len(env['CANDIDATES']), passed))
    else:
        bad = 0
        for did, j in drills.items():
            t, fails = run(src, j, 60)
            bad += bool(fails)
            print('%-26s %-10s %s' % (did, t, 'ok' if not fails else 'FAIL ' + ' '.join(fails)))
        print('%d drills, %d with a failure' % (len(drills), bad))
