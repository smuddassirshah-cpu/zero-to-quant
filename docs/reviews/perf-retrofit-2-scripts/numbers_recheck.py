"""Second read, batch 2: every number in the seven longform models, by a route
other than the authors'. Exact fractions where possible, a seeded simulation or
brute force as the second route. Exit 0 when all agree.
Run from this folder: python3 numbers_recheck.py
"""
import math, random, sys
from fractions import Fraction as F
from itertools import product

FAILS = []
def check(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        FAILS.append(msg)
def near(a, b, tol):
    return abs(a - b) <= tol

# ---------------- systems L1, h1-branch-aloud ----------------
n, keep, miss_ns, body_ns = 10_000_000, 0.3, 5, 1
check(n * min(keep, 1 - keep) * miss_ns / 1e6 == 15, 'branch: 3,000,000 misses at 5 ns is 15 ms')
check(n * body_ns / 1e6 == 10 and 15 / 25 == 0.6, 'branch: body 10 ms, branch 60% of 25 ms')
# two-bit counter: stationary law of a birth-death chain on 0..3, up on keep (taken)
w = [F(1), F(3, 7), F(9, 49), F(27, 343)]
pi = [x / sum(w) for x in w]
rate = (pi[2] + pi[3]) * F(7, 10) + (pi[0] + pi[1]) * F(3, 10)
check(rate == F(210, 580), 'two-bit counter: exact miss rate 210/580 = %.4f' % float(rate))
rng = random.Random(7); c = 1; wrong = 0; T = 400_000
for _ in range(T):
    taken = rng.random() < 0.3
    wrong += (c >= 2) != taken
    c = min(3, c + 1) if taken else max(0, c - 1)
check(near(wrong / T, float(rate), 0.004), 'two-bit counter: simulated %.4f' % (wrong / T))
check(near(n * float(rate) * 5 / 1e6, 18, 0.15), 'two-bit counter: about 18 ms (%.2f)' % (n * float(rate) * 5 / 1e6))
check(n * 0.01 * 5 / 1e6 == 0.5 and n * 0.5 * 5 / 1e6 == 25, 'branch: 99% pass 0.5 ms; half pass 25 ms')
check(25 / 10 == 2.5, 'branchless at 1 ns: 2.5 times faster')
# branchless loop keeps the kept prices in order and never writes past n - 1
for trial in range(200):
    m = rng.randrange(1, 40); p = [rng.randrange(100) for _ in range(m)]; lim = 50
    out = [None] * m; k = 0; top = -1
    for i in range(m):
        out[k] = p[i]; top = max(top, k); k += p[i] <= lim
    assert out[:k] == [x for x in p if x <= lim] and top <= m - 1
check(True, 'branchless rewrite: 200 random lists match the branch loop, writes stay below n')

# ---------------- systems L3, h3-process-aloud ----------------
call, switch, sched = 0.2, 2.0, 1.0
per = 2 * call + (switch + sched + switch)
check(near(per, 5.4, 1e-12), 'process: 0.4 + 5 = 5.4 us an order')
check(near(20_000 * per, 108_000, 1e-6), 'process: 108,000 us = 108 ms a second, %.1f%% of a core' % (20_000 * per / 1e4))
check(round(100 * 5 / 5.4) == 93, 'process: the wake is 93% of the cost')
# event count of one busy second, second route
events = {'call': 0, 'switch': 0, 'sched': 0}
for _ in range(20_000):
    events['call'] += 2; events['switch'] += 1   # write, read; sleep in read
    events['sched'] += 1; events['switch'] += 1  # wake: pick, switch back in
tot = events['call'] * call + events['switch'] * switch + events['sched'] * sched
check(near(tot, 108_000, 1e-6), 'process: event count gives 108 ms')
# latency on the order's path: the switch out happened before the order existed (SY3-1)
latency = call + sched + switch + call
check(near(latency, 3.4, 1e-12) and latency < 5, 'process: added wait on the path is 1 + 2 = 3 us of wake (3.4 us with both calls), not "at least 5"')

# ---------------- pdes L1, h-derive-lazy-walk ----------------
dx, dt, p, q = F(1, 10), F(4, 1000), F(45, 100), F(35, 100)
r = 1 - p - q
D = (p + q) * dx ** 2 / (2 * dt); c = (p - q) * dx / dt
check(r == F(1, 5) and D == 1 and c == F(5, 2), 'lazy walk: r = 0.2, D = 1, c = 2.5')
steps = int(1 / dt)
mean1 = (p - q) * dx; msq = (p + q) * dx ** 2; var1 = msq - mean1 ** 2
check(steps == 250 and mean1 == F(1, 100) and msq == F(8, 1000) and var1 == F(79, 10000), 'lazy walk: 250 steps, step mean 0.01, mean square 0.008, variance 0.0079')
check(steps * mean1 == F(5, 2) and steps * var1 == F(1975, 1000), 'lazy walk: mean 2.5, variance 1.975')
check(2 * D * 1 - steps * var1 == F(25, 1000) == c ** 2 * dt * 1, 'lazy walk: gap 0.025 = c^2 dt t')
# second route: exact distribution by convolution on the lattice
dist = {0: F(1)}
for _ in range(steps):
    nd = {}
    for k, v in dist.items():
        nd[k + 1] = nd.get(k + 1, 0) + v * p
        nd[k - 1] = nd.get(k - 1, 0) + v * q
        nd[k] = nd.get(k, 0) + v * r
    dist = nd
m = sum(F(k) * dx * v for k, v in dist.items())
vv = sum((F(k) * dx) ** 2 * v for k, v in dist.items()) - m ** 2
check(m == F(5, 2) and vv == F(1975, 1000), 'lazy walk: lattice convolution gives mean 2.5 and variance 1.975 exactly')
# remainder orders: the update residual of a smooth solution, divided by dt
def u(x, t, Dc=1.0, cc=2.5):
    return math.exp(-(x - cc * t) ** 2 / (4 * Dc * t)) / math.sqrt(4 * math.pi * Dc * t)
res = []
for h in (0.1, 0.05, 0.025):
    tt = 1.0; ddt = (1 - 0.2) * h * h / 2.0           # D = 1 held fixed
    pq = 2.5 * ddt / h                                 # p - q from c = 2.5
    pp, qq = (0.8 + pq) / 2, (0.8 - pq) / 2
    x = 0.7
    lhs = u(x, tt + ddt)
    rhs = pp * u(x - h, tt) + qq * u(x + h, tt) + 0.2 * u(x, tt)
    res.append(abs(lhs - rhs) / ddt)
check(res[0] / res[1] > 1.8 and res[1] / res[2] > 1.8, 'lazy walk: whole truncation error over dt falls with dx (%.2e, %.2e, %.2e)' % tuple(res))
# the space remainder alone, over dt: order dx^2, not dx (PD1-1), since p - q is of order dx
def ux(x, t, e=1e-4): return (u(x + e, t) - u(x - e, t)) / (2 * e)
def uxx(x, t, e=1e-4): return (u(x + e, t) - 2 * u(x, t) + u(x - e, t)) / (e * e)
sp = []
for h in (0.2, 0.1, 0.05):
    ddt = 0.8 * h * h / 2.0; pq = 2.5 * ddt / h; pp, qq = (0.8 + pq) / 2, (0.8 - pq) / 2
    x, tt = 0.7, 1.0
    rem = pp * u(x - h, tt) + qq * u(x + h, tt) + 0.2 * u(x, tt) - u(x, tt) - (-(pp - qq) * h * ux(x, tt) + 0.5 * 0.8 * h * h * uxx(x, tt))
    sp.append(abs(rem) / ddt)
check(sp[0] / sp[1] > 3.5 and sp[1] / sp[2] > 3.5, 'lazy walk: space remainder over dt falls by about 4 per halving (%.2e, %.2e, %.2e): order dx^2, so "of size dx" is only a bound' % tuple(sp))

# ---------------- measure-prob L1, h-build-space ----------------
pk = lambda k: F(1, k * (k + 1))
check(all(sum(pk(k) for k in range(1, m + 1)) == 1 - F(1, m + 1) for m in range(1, 60)), 'space: partial sums 1 - 1/(m + 1)')
check(all(1 - sum(pk(k) for k in range(1, n0)) == F(1, n0) for n0 in range(1, 40)), 'space: P({n, n+1, ...}) = 1/n by the complement')
check(all(sum(pk(k) for k in range(n0, m + 1)) == F(1, n0) - F(1, m + 1) for n0 in range(1, 15) for m in range(n0, 40)), 'space: P({n..m}) = 1/n - 1/(m+1)')
# continuity from above needs only some finite term: counting measure on tails of N
check(True, 'space: with counting measure, tails {n, n+1, ...} all infinite, intersection empty, so finiteness is needed (shown by the model)')

# ---------------- measure-prob L2, h-build-integral ----------------
def mean_phi(n):
    N = 2 ** n
    return sum(F(k, N) * F(2 * k + 1, N * N) for k in range(N))
check(all(mean_phi(n) == F((2 ** n - 1) * (4 * 2 ** n + 1), 6 * 4 ** n) for n in range(1, 12)), 'integral: band sum equals (N-1)(4N+1)/(6N^2)')
check(mean_phi(1) == F(3, 8) and mean_phi(3) == F(231, 384), 'integral: 3/8 and 231/384')
check(all(F(2, 3) - mean_phi(n) == F(3 * 2 ** n + 1, 6 * 4 ** n) for n in range(1, 12)), 'integral: shortfall (3N+1)/(6N^2)')
# second route: E[phi_n] = sum over bands of the chance X >= k/N, times 1/N
def mean_phi_tail(n):
    N = 2 ** n
    return sum(F(1, N) * (1 - F(k * k, N * N)) for k in range(1, N))
check(all(mean_phi(n) == mean_phi_tail(n) for n in range(1, 10)), 'integral: tail sum of the bands agrees')
# Y = 2 sqrt U - 1 by a midpoint rule in U
M = 400_000
yp = sum(max(2 * math.sqrt((i + 0.5) / M) - 1, 0) for i in range(M)) / M
ym = sum(max(1 - 2 * math.sqrt((i + 0.5) / M), 0) for i in range(M)) / M
check(near(yp, 5 / 12, 1e-5) and near(ym, 1 / 12, 1e-5), 'integral: E[Y+] = 5/12 and E[Y-] = 1/12 by a midpoint rule in U')

# ---------------- measure-prob L3, h-prove-urn ----------------
def atoms(n):
    for s in product((0, 1), repeat=n):
        red, pr = 1, F(1)
        for k, d in enumerate(s):
            share = F(red, k + 2)
            pr *= share if d else 1 - share
            red += d
        yield s, pr, red
for n0 in range(0, 9):
    okstep = True; em = F(0)
    for s, pr, red in atoms(n0):
        Mn = F(red, n0 + 2)
        nxt = Mn * F(red + 1, n0 + 3) + (1 - Mn) * F(red, n0 + 3)
        okstep &= (nxt == Mn) and pr > 0 and 0 < Mn < 1
        em += pr * Mn
    check(okstep and em == F(1, 2), 'urn n = %d: step holds on every atom, all atoms positive, 0 < M < 1, E[M] = 1/2' % n0)
check(F(3, 4) * F(4, 5) + F(1, 4) * F(3, 5) == F(3, 4), 'urn: red, red atom averages to 3/4')
rng = random.Random(11); reds = 0; T = 200_000
for _ in range(T):
    red, tot = 1, 2
    for k in range(6):
        d = rng.random() < red / tot; red += d; tot += 1
    reds += d
check(near(reds / T, 0.5, 0.005), 'urn: simulated chance that draw 6 is red %.4f' % (reds / T))

# ---------------- puzzles L4, hw4-kelly-draw ----------------
b, p, rr, q = 1.2, 0.45, 0.25, 0.30
g = lambda f: p * math.log(1 + b * f) + q * math.log(1 - f)
fs = (p * b - q) / (b * (p + q))
check(near(fs, 4 / 15, 1e-12), 'kelly: f* = 4/15')
grid = max((g(i / 100000), i / 100000) for i in range(0, 99999))
check(near(grid[1], 4 / 15, 2e-5), 'kelly: grid maximum at %.5f' % grid[1])
check(near(g(fs), 0.0319, 5e-5) and near(g(2 * fs), -0.0060, 5e-5), 'kelly: g(f*) = %.4f, g(2f*) = %.4f' % (g(fs), g(2 * fs)))
check(near(1 + 2 * fs * (p * b - q), 1.128, 1e-12), 'kelly: mean multiplier at twice Kelly 1.128')
check(near(p - (1 - p) / b, -0.0083, 5e-5) and near(p - q / b, 0.2, 1e-12), 'kelly: slips -0.0083 and 0.2')
lo, hi = 0.3, 0.99
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if g(mid) > 0 else (lo, mid)
check(near(lo, 0.513, 5e-4), 'kelly: zero of g at %.4f' % lo)
g2 = lambda f: 0.1 * math.log(1 + 20 * f) + 0.9 * math.log(1 - f)
f2 = (0.1 * 20 - 0.9) / 20
check(near(g2(2 * f2), 0.0114, 5e-5), 'kelly: 20 to 1 at p = 0.1, g(2f*) = %.4f' % g2(2 * f2))
rng = random.Random(5); n = 20000; lw = 0.0
for _ in range(n):
    u_ = rng.random()
    lw += math.log(1 + b * fs) if u_ < p else (0.0 if u_ < p + rr else math.log(1 - fs))
check(near(lw / n, g(fs), 0.006), 'kelly: simulated growth per match %.4f' % (lw / n))

print('failures:', len(FAILS))
sys.exit(1 if FAILS else 0)
