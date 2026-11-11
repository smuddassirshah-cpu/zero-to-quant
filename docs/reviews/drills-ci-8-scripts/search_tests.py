"""Search small inputs for the shortest test that separates a passing wrong candidate from the model.
usage: search_tests.py <drills dir>   (prints one proposed call and its expected value per candidate)"""
import itertools
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checks  # noqa: E402

drills = checks.load(sys.argv[1])
e = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wrong.py')).read(), e)
C = e['CANDIDATES']


def fns(label):
    did, code, _ = C[label]
    m, c = {}, {}
    exec(drills[did]['solution'], m)
    exec(code, c)
    fn = drills[did]['fn']
    return m[fn], c[fn]


def report(label, args, want, got):
    print('%-34s %r -> want %r, candidate gives %r' % (label, args, want, got))


# stone hops: every string up to 13 places, every lo <= hi
for label in ('hops_greedy_levels_with_lo', 'hops_levels_first_last_stone'):
    m, c = fns(label)
    found = None
    for n in range(2, 14):
        for bits in itertools.product('.~', repeat=n - 2):
            s = '.' + ''.join(bits) + '.'
            for lo in range(1, n + 1):
                for hi in range(lo, n + 1):
                    if m(s, lo, hi) != c(s, lo, hi):
                        found = (s, lo, hi)
                        break
                if found:
                    break
            if found:
                break
        if found:
            break
    if found:
        report(label, found, m(*found), c(*found))
    else:
        print(label, 'no difference up to 13 places')

# double checks: random small job lists, shortest disagreement
m, c = fns('checks_window_last_five')
rng = random.Random(3)
best = None
for _ in range(300000):
    n = rng.randint(2, 6)
    jobs = []
    for _ in range(n):
        a = rng.randint(0, 14)
        b = min(14, a + rng.randint(0, 9))
        jobs.append([a, b, rng.randint(1, min(5, b - a + 1))])
    if m(jobs) != c(jobs) and (best is None or len(jobs) < len(best)):
        best = jobs
        if len(jobs) <= 3:
            break
if best:
    report('checks_window_last_five', best, m(best), c(best))
    assert checks.b_fewest_checks(best) == m(best)

for label in ('stop_highest_price_ever', 'stop_buy_remainder_rests'):
    m, c = fns(label)
    rng = random.Random(4)
    best = None
    for _ in range(100000):
        n = rng.randint(2, 6)
        ev = []
        for _ in range(n):
            k = rng.choice('SSBT')
            ev.append('B %d' % rng.randint(1, 3) if k == 'B' else '%s %d %d' % (k, rng.randint(1, 9), rng.randint(1, 3)))
        t = '%d\n' % n + '\n'.join(ev) + '\n'
        if m(t) != c(t) and (best is None or n < best[0]):
            best = (n, t)
    report(label, best[1], m(best[1]), c(best[1]))
    assert checks.b_solve_stop_cascade(best[1]) == m(best[1])
