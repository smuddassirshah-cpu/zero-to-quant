"""My own model of all 25 drills, written from each brief alone, against every `expect`.

Run with the scratchpad venv Python (it needs mpmath):  python mine.py
Method differs from the C++ model where one exists: Fractions for rounding, ties and thresholds,
mpmath at 40 digits for the pricing formulas, a recursion over tree nodes for the Bermudan put,
counting for ranks, a regular expression for the fills file, a stack for the nested limits.
Calls written as C++ expressions are read by a small translation or, for the eight lambdas, by hand.
"""
import functools, json, os, re, subprocess, sys
from fractions import Fraction as F
import mpmath as mp

mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness  # noqa: E402


def half_away(x):
    """Round a Fraction to the nearest whole number, halves away from zero."""
    s = -1 if x < 0 else 1
    return s * int((abs(x) + F(1, 2)) // 1)


# ---- cpp ----
def clip_probe(r, cap):
    out, n = [], 0
    for x in r:
        y = min(max(x, -cap), cap)
        n += y != x
        out.append(y)
    return out + [n]


def fee_pence(n, bps):
    x = F(n * bps, 10000)
    return int(-((-x) // 1))


def high_water(p):
    return [max(p[:i + 1]) for i in range(len(p))]


def longest_rise(c):
    ups = ''.join('u' if b > a else '.' for a, b in zip(c, c[1:]))
    return max((len(m) for m in re.findall('u+', ups)), default=0)


def run_log(ts):
    kept, out = [], []
    for t in ts:
        ok = not kept or t >= kept[-1]
        out.append(int(ok))
        if ok:
            kept.append(t)
    return out + [len(kept), kept[-1] - kept[0] if len(kept) >= 2 else 0]


def round_to_tick(price, tick=0.25):
    return float(half_away(F(price) / F(tick)) * F(tick))


def count_crossings(xs, level):
    sides = [1 if x > level else -1 for x in xs if x != level]
    return sum(a != b for a, b in zip(sides, sides[1:]))


def after_drop(v, m):
    keep = [x for x in v if x >= m]
    return keep + [len(v) - len(keep)]


def rates(frm, bps, asks):
    return [[b for f, b in zip(frm, bps) if f <= a][-1] for a in asks] + [len(frm)]


def probe(xs, want_lo, want_hi):
    if not xs:
        return [0, 999, 999]
    return [1, min(xs) if want_lo else 999, max(xs) if want_hi else 999]


class SessionTime:
    def __init__(self, m):
        self.m = m - 1440 * (m // 1440)

    def minutes(self):
        return self.m

    def __add__(self, k):
        return SessionTime(self.m + k)

    def __sub__(self, a):
        d = self.m - a.m
        return d if d >= 0 else d + 1440

    def __lt__(self, b):
        return self.m < b.m


def nest(start, caps):
    lim, r, stack = start, [], []
    for c in caps:                      # on the way in
        stack.append(lim)
        lim = min(lim, c)
        r.append(lim)
    while stack:                        # each block closes
        lim = stack.pop()
        r.append(lim)
    # the helper records the limit after each inner block closes and once at the end:
    # that is one reading per close when there is at least one block
    return r if caps else [start]


def siblings(start, caps):
    r = []
    for c in caps:
        r += [min(start, c), start]
    return r


def latency_trimmed_mean(t, k):
    s = sorted(t)
    mid = s[k:len(s) - k] if 2 * k < len(s) else []
    return float(F(sum(mid), len(mid))) if mid else 0.0


def fills_value(text):
    total = 0
    for line in text.split('\n'):
        if line.endswith('\r'):
            line = line[:-1]
        m = re.fullmatch(r'(-?[0-9]+),([0-9]+)', line)
        if m:
            total += int(m.group(1)) * int(m.group(2))
    return total


def mean_ranks(s):
    return [float(sum(y < x for y in s) + F(sum(y == x for y in s) + 1, 2)) for x in s]


def movers(syms, px, pct):
    first, last = {}, {}
    for s, p in zip(syms, px):
        first.setdefault(s, F(p))
        last[s] = F(p)
    mv = {s: abs(last[s] - first[s]) / first[s] for s in first}
    keep = [s for s in mv if mv[s] * 100 >= F(pct)]
    return sorted(keep, key=lambda s: (-mv[s], s))


def run_take(m, n):
    d = ['a%d:%d' % (i, i + 1) for i in range(m)] + ['b%d:%d' % (i, i + 1) for i in range(n)]
    return ['0', str(m + n), '0'] + d


# ---- cpp-pricing ----
def df_compounded(r, t, m):
    r, t = mp.mpf(r), mp.mpf(t)
    return float(mp.exp(-r * t) if m == 0 else mp.exp(-m * t * mp.log(1 + r / m)))


def Phi(x):
    return mp.ncdf(x)


def prob_between(mu, sigma, a, b):
    mu, sigma, a, b = map(mp.mpf, (mu, sigma, a, b))
    return 0.0 if a > b else float(Phi((b - mu) / sigma) - Phi((a - mu) / sigma))


def cash_call(s, k, r, sigma, t, payout):
    s, k, r, sigma, t, payout = map(mp.mpf, (s, k, r, sigma, t, payout))
    if t == 0:
        return float(payout) if s > k else 0.0
    d2 = (mp.log(s / k) + (r - sigma ** 2 / 2) * t) / (sigma * mp.sqrt(t))
    return float(payout * mp.exp(-r * t) * Phi(d2))


def curve_df(times, zeros, t):
    T = [mp.mpf(0)] + [mp.mpf(x) for x in times]
    Y = [mp.mpf(0)] + [mp.mpf(x) * mp.mpf(z) for x, z in zip(times, zeros)]
    t = mp.mpf(t)
    if t >= T[-1]:
        y = mp.mpf(zeros[-1]) * t
    else:                               # a line from the origin is the flat first rate
        i = max(j for j in range(len(T)) if T[j] <= t)
        y = Y[i] + (Y[i + 1] - Y[i]) * (t - T[i]) / (T[i + 1] - T[i])
    return float(mp.exp(-y))


class Call:
    def __init__(self, k): self.k = k
    def __call__(self, s): return max(s - self.k, 0.0)


class Forward:
    def __init__(self, k): self.k = k
    def __call__(self, s): return s - self.k


class Scaled:
    def __init__(self, q, inner): self.q, self.inner = q, inner
    def __call__(self, s): return self.q * self.inner(s)


def bermudan_put(s, k, u, d, growth, n, dates):
    s, k, u, d, g = map(mp.mpf, (s, k, u, d, growth))
    q = (g - d) / (u - d)
    dates = set(dates)

    @functools.lru_cache(maxsize=None)
    def value(i, j):                    # node with j ups after step i
        price = s * u ** j * d ** (i - j)
        if i == n:
            return max(k - price, mp.mpf(0))
        cont = (q * value(i + 1, j + 1) + (1 - q) * value(i + 1, j)) / g
        return max(cont, k - price) if i in dates and i >= 1 else cont
    return float(value(0, 0))


def pounds_to_pence(x):
    return half_away(F(x) * 100)


def add_pounds(a, b):
    return pounds_to_pence(a) + pounds_to_pence(b)


def split_pence(p, n):
    sign, a = (-1 if p < 0 else 1), abs(p)
    big = a % n                         # this many parts are a penny larger in size
    return [sign * (a // n + (1 if i < big else 0)) for i in range(n)]


def stats(xs):
    xs = [F(x) for x in xs]
    n = len(xs)
    mean = sum(xs) / n if n else F(0)
    var = sum((x - mean) ** 2 for x in xs) / (n - 1) if n >= 2 else F(0)
    return [n, float(mean), float(var)]


def stats_of(xs): return stats(xs)
def merged(a, b): return stats(a + b)


# the lambdas, by hand, keyed on (drill, kind, index); the working is beside each
BY_HAND = {
    # limit 7, cap 1 lowers it to 1; reset() ends the object and puts 7 back
    ('cpp-temp-limit', 'tests', 9): [1, 7],
    # two limits, each lowered by its own object (50 to 10, 60 to 20), both restored at the brace
    ('cpp-temp-limit', 'tests', 10): [10, 20, 50, 60],
    # 5 fills then 400 moved on: no copy, 405 held, source empty, the last has qty 400
    ('cpp-take-all', 'tests', 6): [0, 405, 0, 400],
    # b0 b1 moved, the emptied source is reused for c0, moved again, source empty again
    ('cpp-take-all', 'tests', 7): 'b0 b1 c0 0',
    # 2 * (15 - 10)
    ('cpp-scaled-payoff', 'tests', 7): 10.0,
    # 0.5 * (-8 - 0)
    ('cpp-scaled-payoff', 'tests', 8): -4.0,
    # -2 * max(120 - 110, 0) + (120 - 95) = -20 + 25
    ('cpp-scaled-payoff', 'tests', 9): 5.0,
    # i % 7 for i below 100000: computed below, exactly
    ('cpp-running-stats', 'tests', 13): stats([i % 7 for i in range(100000)]),
}


def translate(call):
    """A C++ call expression as Python, for the three drills whose calls are plain expressions."""
    c = re.sub(r'std::make_unique<(\w+)>', r'\1', call)
    c = re.sub(r'std::vector<[a-z ]+>\{([^}]*)\}', r'[\1]', c)
    c = re.sub(r'(\d)LL', r'\1', c)
    return c


def main():
    rows = [json.loads(l) for l in subprocess.run([sys.executable, os.path.join(HERE, 'harness.py'), 'expects'], capture_output=True, text=True).stdout.splitlines()]
    bad = n = 0
    per = {}
    for r in rows:
        key = (r['id'], r['kind'], r['i'])
        if key in BY_HAND:
            got = BY_HAND[key]
        elif r['args'] is not None:
            got = globals()[r['call']](*r['args'])
        else:
            got = eval(translate(r['call']))
        if isinstance(got, bool) or isinstance(r['expect'], bool):
            ok = got is r['expect'] or got == r['expect'] and isinstance(got, bool)
        elif r['compare'] == 'isclose':
            ok = harness.close(got, r['expect'], r['tol'])
        else:
            ok = got == r['expect']
        n += 1
        per[r['id']] = per.get(r['id'], 0) + 1
        if not ok:
            bad += 1
            print('DISAGREE', key, 'mine', got, 'expect', r['expect'])
    print('%d drills, %d cases, disagreements %d' % (len(per), n, bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
