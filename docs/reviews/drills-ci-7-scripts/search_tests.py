"""Searches for the small inputs that separate a passing wrong candidate from the
model, and times the slow candidates on proposed large tests.
usage: search_tests.py <drills dir> [pieces] [three] [tol] [smooth] [bb]"""
import json
import multiprocessing as mp
import os
import random
import sys
import time
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1]
what = sys.argv[2:]


def model(did):
    j = json.load(open(os.path.join(D, did + '.json')))
    env = {}
    exec(j['solution'], env)
    return env[j['fn']]


def cand(label):
    c = {}
    for name in ('wrong.py', 'wrong2.py', 'wrong3.py'):
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            e = {}
            exec(open(p).read(), e)
            c.update(e['CANDIDATES'])
    did, src, _ = c[label]
    env = {}
    exec(src, env)
    j = json.load(open(os.path.join(D, did + '.json')))
    return env[j['fn']]


def timed(fn, args, limit):
    def run(q):
        t0 = time.time()
        r = fn(*args)
        q.put((time.time() - t0, r))
    q = mp.Queue()
    p = mp.Process(target=run, args=(q,))
    p.start()
    p.join(limit)
    if p.is_alive():
        p.terminate()
        return 'over %d s' % limit, None
    t, r = q.get()
    return '%.2f s' % t, r


if 'pieces' in what:
    m, c = model('ci-mirror-pieces'), cand('pieces_greedy_both_ends')
    found = []
    for n in range(1, 11):
        for s in map(''.join, product('ab', repeat=n)):
            t = '1\n%s\n' % s
            if m(t) != c(t):
                found.append((s, m(t), c(t)))
        if found:
            break
    print('pieces: shortest strings on which both greedies fail:', found[:6])

if 'three' in what:
    m, c = model('ci-three-feed-common'), cand('three_best_of_three_orders')
    R = random.Random(7)
    best = None
    for _ in range(200000):
        n = R.randint(3, 6)
        a, b, cc = (''.join(R.choice('xyz') for _ in range(R.randint(2, n))) for _ in range(3))
        if m(a, b, cc) != c(a, b, cc):
            if best is None or len(a + b + cc) < len(''.join(best[:3])):
                best = (a, b, cc, m(a, b, cc), c(a, b, cc))
    print('three: shortest found', best)

if 'tol' in what:
    m, c = model('ci-tolerant-common'), cand('tol_greedy_both_ways')
    c2 = cand('tol_greedy_from_each_start')
    R = random.Random(3)
    best = None
    for _ in range(300000):
        a = [R.randint(0, 6) for _ in range(R.randint(2, 5))]
        b = [R.randint(0, 6) for _ in range(R.randint(2, 5))]
        tol = R.randint(0, 2)
        if m(a, b, tol) != c(a, b, tol) and m(a, b, tol) != c2(a, b, tol):
            if best is None or len(a) + len(b) < len(best[0]) + len(best[1]):
                best = (a, b, tol, m(a, b, tol), c(a, b, tol), c2(a, b, tol))
    print('tol: shortest found', best)

if 'smooth' in what:
    m = model('ci-smooth-orderings')
    for sizes, d in (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 9), ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 8),
                     ([40, 10, 90, 20, 110, 60, 30, 100, 70, 50, 80], 90), ([40, 10, 90, 20, 110, 60, 30, 100, 70, 50, 80], 80)):
        print('smooth', sizes, d, 'model', timed(m, (sizes, d), 20),
              'shortcut walk', timed(cand('smooth_shortcut_then_walk'), (sizes, d), 20)[0])

if 'bb' in what:
    m = model('ci-mirror-pieces')
    for label, s in (('lcg ab 400', ''.join('ab'[(x >> 16) & 1] for x in
                                             (lambda v: [v.append((v[-1] * 1103515245 + 12345) % 2 ** 31) or v[-1] for _ in range(400)])([7]))),
                     ('aab-ish 400', ''.join('ab'[(i * i * i + i // 3) % 5 % 2] for i in range(400))),
                     ('abc 400', ''.join('abc'[(i * i + i // 7) % 3] for i in range(400)))):
        t = '1\n%s\n' % s
        print('bb', label, 'model', timed(m, (t,), 20), 'branch and bound', timed(cand('pieces_branch_and_bound'), (t,), 20)[0],
              'greedy both ends', timed(cand('pieces_greedy_both_ends'), (t,), 20)[1])
