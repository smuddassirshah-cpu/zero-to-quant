"""How does each planted solution fail? Runs every planted solution natively, test by test, each
test in a process with a time limit, and prints the first failing test with what it returned.
usage: planted_reason.py <drills dir> [drill id ...]"""
import multiprocessing as mp
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checks  # noqa: E402


def _one(code, t, q):
    env = {}
    try:
        exec(code, env)
        got = eval(t['call'], env)
        want = eval(t['expect'], env)
        q.put(('ok' if got == want else 'value', repr(got)[:70], repr(want)[:70]))
    except BaseException as e:  # noqa
        q.put(('exception', type(e).__name__ + ': ' + str(e)[:50], ''))


def run(code, t, limit=6):
    q = mp.Queue()
    p = mp.Process(target=_one, args=(code, t, q))
    p.start()
    p.join(limit)
    if p.is_alive():
        p.terminate()
        p.join()
        return ('slow', '', '')
    return q.get(timeout=2)


if __name__ == '__main__':
    drills = checks.load(sys.argv[1])
    for did, j in drills.items():
        if sys.argv[2:] and did not in sys.argv[2:]:
            continue
        for n, p in enumerate(j['planted']):
            kinds = []
            first = None
            for i, t in enumerate(j['examples'] + j['tests']):
                r = run(p['code'], t)
                if r[0] != 'ok':
                    name = ('e%d' % i) if i < len(j['examples']) else 't%d' % (i - len(j['examples']))
                    kinds.append(name + ':' + r[0][0])
                    if first is None:
                        first = (name, t['call'][:80], r)
            print('%s planted[%d] %s' % (did, n, p['slip'][:110]))
            print('    fails %s' % ' '.join(kinds))
            if first and first[2][0] != 'slow':
                print('    first %s %s -> %s (want %s)' % (first[0], first[1], first[2][1], first[2][2]))
