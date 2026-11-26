"""Fix-pass read of cpp L4 and L5 round 2 (content commit 434980dd): the numbers, recomputed away from the C++.

Second route for every value the fix pass states or relies on. The first route is the page's own unit builder and
worker run in node with YoWASP clang 21 (results are in docs/reviews/audit-cpp-4-5-r2.md, "Fix-pass read").
Exits 0 when the content is right.
"""
import math
from fractions import Fraction as F


def crr(S, K, r, s, T, n, disc=True):
    dt = T / n
    u = math.exp(s * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    D = math.exp(-r * dt) if disc else 1.0
    v = [max(S * u ** (n - j) * d ** j - K, 0.0) for j in range(n + 1)]
    for i in range(n - 1, -1, -1):
        v = [D * (p * v[j] + (1 - p) * v[j + 1]) for j in range(i + 1)]
    return v[0]


# l18 s9: the pin, the Black-Scholes value, planted bugs 1 to 3
N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
d1 = (0.05 + 0.02) / 0.2
bs = 100 * N(d1) - 100 * math.exp(-0.05) * N(d1 - 0.2)
p100, p99, p2000, p1999 = (crr(100, 100, .05, .2, 1, n) for n in (100, 99, 2000, 1999))
print('BS %.6f n100 %.6f n99 %.4f n2000 %.6f |n2000-BS| %.6f |n100-BS| %.6f' % (bs, p100, p99, p2000, abs(p2000 - bs), abs(p100 - bs)))
assert round(bs, 6) == 10.450584 and round(p100, 6) == 10.430612 and abs(p100 - 10.430612) < 1e-6
assert round(p99, 4) == 10.4683 and round(p100, 4) == 10.4306
assert abs(p2000 - bs) < 0.002          # the model solution passes on the real pricer
assert abs(p100 - bs) > 0.002           # planted bug 3 (min(steps, 100)) is caught by the convergence test
assert abs(p100 - 10.430612) < 1e-6     # ... and is invisible to the 100-step pin
assert abs(p1999 - bs) < 0.002 and abs(p99 - 10.430612) > 1e-6   # bug 2: seen by the pin only
assert abs(crr(100, 100, .05, .2, 1, 100, False) - 10.430612) > 1e-6  # bug 1: seen by the pin

# l18 s7: the fixed formula named in the prose, and the other natural fix
a = 110.0 / 100.0 - 1
b = (110.0 - 100.0) / 100.0
print(repr(a), a == 0.1, '|', repr(b), b == 0.1)
assert repr(a) == '0.10000000000000009' and a != 0.1   # FAIL is right for px[i] / px[i - 1] - 1
assert b == 0.1                                        # the other fix would pass, so the prose must name the formula


# l16 s3: test 7 and the test-1 and test-7 lines
def vwap(px, q, vint, sint, intdiv=False):
    v = 0 if vint else 0.0
    s = 0 if sint else 0.0
    for p, x in zip(px, q):
        v = v + p * x
        v = int(v) if vint else v     # std::inner_product with an int start truncates at every step
        s = s + x
        s = int(s) if sint else s
    if s == 0:
        return 0
    return v // s if intdiv else v / s


T = [([100, 101, 102], [200, 100, 100]), ([72.5], [1000]), ([], []), ([100, 101], [0, 0]),
     ([2.1, 2.11, 2.1, 2.12], [500, 300, 1000, 200]), ([10.25, 10.75], [3, 1]), ([10.0, 20.0], [0.5, 1.5])]
E = [100.75, 72.5, 0, 0, 2.1035, 10.375, 17.5]
want = {'right': (0, 0, 0, None, None), 'both int, int divide': (1, 1, 1, 1, 100), 'shares int only': (0, 1, 0, 7, 35),
        'value int only': (1, 0, 0, 6, 10), 'both int, double divide': (1, 1, 0, 6, 10)}
for name, (vi, si, idv, first, val) in want.items():
    r = [vwap(p, q, vi, si, idv) for p, q in T]
    bad = [i + 1 for i, (x, e) in enumerate(zip(r, E)) if not math.isclose(x, e, rel_tol=1e-9, abs_tol=1e-12)]
    print('vwap', name, 'fails', bad, 'first value', r[bad[0] - 1] if bad else None)
    assert (bad[0] if bad else None) == first and (r[first - 1] if first else None) == val
assert F(40300, 400) == F('100.75') and F(303, 3) == 101 and F('41.5') / 4 == F('10.375') and F(35, 2) == F('17.5')


# h4-test-drawdown: planted bug 5
def mdd(px, v=0):
    if not px:
        return 0
    pk, w = px[0], 0
    for p in px:
        pk = max(pk, p)
        w = max(w, (pk - p) / pk)
    if v == 5 and w == 0 and len(px) > 1:
        return (px[-1] - px[0]) / px[0]
    return w


assert mdd([100, 120, 90, 130, 104]) == 0.25 == mdd([100, 120, 90, 130, 104], 5)
assert mdd([100, 101, 103.5]) == 0 and abs(mdd([100, 101, 103.5], 5) - 0.035) < 1e-15   # caught by a pin of 0
assert mdd([100, 100, 100], 5) == 0 and mdd([100.0], 5) == 0 and mdd([], 5) == 0         # a flat series cannot see bug 5
assert abs((130 - 104) / 130 - 0.2) < 1e-15

# l19 s1: bytes
assert 1_000_000 * 8 == 8_000_000 and abs(8_000_000 / 10e9 * 1e3 - 0.8) < 1e-12
wasm32 = {'ptr': 4, 'int': 4}
lp64 = {'ptr': 8, 'int': 4}
assert sum(wasm32.values()) == 8 and sum(lp64.values()) == 12        # the destination's pointer and size
assert 2 * sum(wasm32.values()) == 16 and 2 * sum(lp64.values()) == 24  # with the two stores that empty the source

# l23 s5 tests[8] and h5 tests[14]: can two wrong counts cancel in the packed value?
fill = 0xDDDDDDDD - 2 ** 32                      # a count read from freed memory (the leak check's fill), as a 32-bit long
wrap = lambda v: (v + 2 ** 31) % 2 ** 32 - 2 ** 31
assert wrap(100 + 10 * fill + 1) == -1431655673  # seen in the run: a default constructor that allocates a zero counter
rng = list(range(0, 1000)) + [fill]
assert [(a, b) for a in rng for b in rng if wrap(100 * a + 10 * b) == 0] == [(0, 0)]
small = list(range(0, 60)) + [fill]
assert [(a, n, b) for a in small for n in small for b in small if wrap(1000 * a + 100 * n + 10 * b) == 0] == [(0, 0, 0)]
# with a negative count the packing is not injective (l23: p = 1, q = -10), which no coding found reaches
assert 100 * 1 + 10 * -10 == 0
print('ok')
