"""Run the model, my own solution, the starter and every planted solution of a pack
on every example and hidden test.

Usage (repo root): python3 run.py <pack> [drill id ...] [--no-planted] [--limit=s]
My solutions live in mine_<pack>.py as functions named after each drill's `fn`.
A drill with no function there is reported as `mine: none`.
Each run is its own process. Exit 1 on any fault: the model fails, mine disagrees
with an `expect`, the starter passes, a planted solution passes, a `how` count or
an index row is out of step."""
import glob
import json
import multiprocessing as mp
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = 'app/content/drills'


def load(pack):
    out = {}
    for f in sorted(glob.glob(os.path.join(DRILLS, 'ci-*.json'))):
        j = json.load(open(f))
        if (j.get('tags') or [''])[0] == f'pack-{pack}':
            out[j['id']] = j
    return out


def cases(drill):
    return [('ex', i, t) for i, t in enumerate(drill['examples'])] + [('t', i, t) for i, t in enumerate(drill['tests'])]


def _run(src, drill, q, fn_only):
    sys.setrecursionlimit(1000)
    env = {}
    try:
        exec(src, env)
    except BaseException as e:  # noqa
        q.put(('load', 0, 'load error %r' % (e,)))
        q.put(None)
        return
    if fn_only and drill['fn'] not in env:
        q.put(('none', 0, ''))
        q.put(None)
        return
    for kind, i, t in cases(drill):
        try:
            if t.get('setup'):
                exec(t['setup'], env)
            got = eval(t['call'], env)
            want = eval(t['expect'], {})
            if got != want or (type(got) is not type(want)):
                q.put((kind, i, 'got %s want %s' % (repr(got)[:90], repr(want)[:90])))
        except BaseException as e:  # noqa
            q.put((kind, i, type(e).__name__))
    q.put(None)


def run(src, drill, limit, fn_only=False):
    """-> (fails list of (label, msg), total seconds, timed_out)"""
    q = mp.Queue()
    p = mp.Process(target=_run, args=(src, drill, q, fn_only))
    t0 = time.time()
    p.start()
    fails, done = [], False
    while time.time() - t0 < limit:
        try:
            m = q.get(timeout=0.05)
        except Exception:
            if not p.is_alive() and q.empty():
                break
            continue
        if m is None:
            done = True
            break
        fails.append(('%s%d' % (m[0], m[1]), m[2]))
    dt = time.time() - t0
    if p.is_alive():
        p.terminate()
    p.join()
    if not done and dt < limit:
        fails.append(('crash', 'process died'))
    return fails, dt, (not done and dt >= limit)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    pack = int(args[0])
    only = args[1:]
    limit = 10.0
    for a in sys.argv:
        if a.startswith('--limit='):
            limit = float(a[8:])
    drills = load(pack)
    mine_src = open(os.path.join(HERE, f'mine_{pack}.py')).read()
    idx = json.load(open(os.path.join(DRILLS, 'index.json')))
    rows = idx['drills'] if isinstance(idx, dict) else idx
    index = {r['id']: r for r in rows}
    bad = 0
    nm = 0
    for did, d in drills.items():
        if only and did not in only:
            continue
        line = [did]
        f, dt, to = run(d['solution'], d, 30)
        if f or to:
            bad += 1
            line.append('MODEL FAILS %s' % f[:3])
        else:
            line.append('model ok %.2fs' % dt)
        f, dt, to = run(mine_src, d, 300, fn_only=True)
        if f and f[0][0] == 'none0':
            line.append('mine: none')
        elif f or to:
            bad += 1
            line.append('MINE DISAGREES %s%s' % (f[:4], ' TIMEOUT' if to else ''))
        else:
            nm += 1
            line.append('mine ok %.2fs' % dt)
        f, dt, to = run(d['starter'], d, 10)
        tf = [x for x in f if x[0].startswith('t')]
        if not tf:
            bad += 1
            line.append('STARTER PASSES')
        if '--no-planted' not in sys.argv:
            res = []
            for k, pl in enumerate(d.get('planted', [])):
                f, dt, to = run(pl['code'], d, limit)
                tf = [x for x in f if x[0].startswith('t')]
                if tf:
                    res.append('%s' % tf[0][0] + ('' if tf[0][1].startswith('got') else '!'))
                elif to:
                    res.append('slow')
                elif dt >= 5:
                    # right answers, but past the page's 5 seconds even natively
                    res.append('slow-thin(%.1fs)' % dt)
                else:
                    bad += 1
                    res.append('PASSES(%.1fs)' % dt)
            line.append('planted ' + ' '.join(res))
        m = re.search(r'runs (\d+) hidden tests', d['how'])
        if not m or int(m.group(1)) != len(d['tests']):
            bad += 1
            line.append('HOW COUNT %s vs %d' % (m and m.group(1), len(d['tests'])))
        row = index.get(did)
        if row is None:
            bad += 1
            line.append('NO INDEX ROW')
        else:
            for k in ('difficulty', 'name', 'pattern', 'pace'):
                if k in row and row[k] != d.get(k):
                    bad += 1
                    line.append('INDEX %s %r vs %r' % (k, row[k], d.get(k)))
        print(' | '.join(line), flush=True)
    print('faults: %d; my solutions agreeing: %d' % (bad, nm))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
