"""Second computation of every stated number in pack `cpp` (docs/briefs/drills-1.1-1.9.md, pack cpp).

Run from the repo root with the scratchpad venv Python:
    <scratchpad>/venv/bin/python docs/reports/drills-cpp-check.py
For each drill it holds an independent Python model of the C++ function (written apart from the
builder that produced the `expect` values, by another method where one exists) and compares it with
every example and hidden test. Calls that are C++ lambdas are matched by their text to a value
worked out here by hand or by the model. It also checks the brief's worked answer appears in the
brief, the `how` count, examples repeated in the tests, the index rows and the pack mix.
The C++ solution, the starter and the planted solutions are run in the real runtime by
`playthrough.mjs --drill` and `planted-check.mjs --require`; this script does not compile C++.
Exit 0 when everything agrees.
"""
import json, math, os, sys, re, itertools
from fractions import Fraction
from statistics import NormalDist

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DR = os.path.join(ROOT, 'app', 'content', 'drills')
errors = []
MODELS = {}      # id -> function(test) -> expected value
BRIEF = {}       # id -> text that must appear in the brief (the worked answer)


def model(drill_id, brief_answer):
    def deco(f):
        MODELS[drill_id] = f
        BRIEF[drill_id] = brief_answer
        return f
    return deco


def close(a, b, rel=1e-9, ab=1e-12):
    if isinstance(a, list):
        return isinstance(b, list) and len(a) == len(b) and all(close(x, y, rel, ab) for x, y in zip(a, b))
    return abs(a - b) <= max(rel * max(abs(a), abs(b)), ab)


# ------------------------------------------------------------------ cpp-fee-pence
@model('cpp-fee-pence', 'the answer is 62')
def _(t):
    n, b = t['args']
    return math.ceil(Fraction(n * b, 10000))


# ------------------------------------------------------------------ cpp-longest-rise
@model('cpp-longest-rise', 'The answer is 3')
def _(t):
    xs = t['args'][0]
    ups = [b > a for a, b in zip(xs, xs[1:])]
    return max([len(list(g)) for k, g in itertools.groupby(ups) if k] or [0])


# ------------------------------------------------------------------ cpp-fill-csv
def _whole(s, minus):
    if minus and s.startswith('-'):
        s = s[1:]
    return len(s) > 0 and all('0' <= c <= '9' for c in s)


@model('cpp-fill-csv', 'The answer is 151,400')
def _(t):
    text = t['args'][0]
    total = 0
    for raw in text.split('\n'):
        line = raw[:-1] if raw[-1:] == '\r' else raw
        if line.count(',') != 1:
            continue
        q, p = line.split(',')
        if _whole(q, True) and _whole(p, False):
            total += int(q) * int(p)
    return total


# ------------------------------------------------------------------ cpp-temp-limit
def _nest(start, caps):
    rec, stack, lim = [], [], start
    for c in caps:                       # open each block inside the last
        stack.append(lim)
        lim = min(lim, c)
        rec.append(lim)
    while stack:                         # close the innermost; record unless it was the outermost
        lim = stack.pop()
        if stack:
            rec.append(lim)
    rec.append(lim)
    return rec


@model('cpp-temp-limit', '{200, 200, 50, 200, 200, 500}')
def _(t):
    if 'compiles' in t:
        return False                     # a copy of TempLimit must not compile
    if t['call'] == 'nest':
        return _nest(*t['args'])
    if t['call'] == 'siblings':
        start, caps = t['args']
        out = []
        for c in caps:
            out += [c if c < start else start, start]
        return out
    if 'make_unique<TempLimit>(lim, 1)' in t['call']:
        return [1, 7]                    # 7 lowered to 1, then reset() restores 7
    if 'TempLimit x(a, 10)' in t['call']:
        return [10, 20, 50, 60]          # two limits, each restored on leaving the block
    raise KeyError(t['call'])


# ------------------------------------------------------------------ cpp-take-all
@model('cpp-take-all', '`Fill::copies` is still 0')
def _(t):
    if t['call'] == 'run_take':
        m, n = t['args']
        dst = [('a%d' % i, i + 1) for i in range(m)]
        src = [('b%d' % i, i + 1) for i in range(n)]
        dst.extend(src)
        src = []
        return ['0', str(len(dst)), str(len(src))] + ['%s:%d' % f for f in dst]
    if 'make_fills("b", 400)' in t['call']:
        return [0, 405, 0, 400]          # no copies, 5 + 400 fills, src empty, the last fill is b399 with qty 400
    if 's.emplace_back("c0", 9)' in t['call']:
        return 'b0 b1 c0 0'
    raise KeyError(t['call'])


# ------------------------------------------------------------------ cpp-tick-round
@model('cpp-tick-round', '100.25')
def _(t):
    price = t['args'][0]
    tick = t['args'][1] if len(t['args']) > 1 else 0.25
    lo = math.floor(price / tick)            # the tick at or below, then pick the nearer of lo and lo + 1
    d_lo, d_hi = Fraction(price) - lo * Fraction(tick), (lo + 1) * Fraction(tick) - Fraction(price)
    if d_lo < d_hi:
        k = lo
    elif d_hi < d_lo:
        k = lo + 1
    else:
        k = lo + 1 if price > 0 else lo       # half-way: away from zero
    return k * tick


# ------------------------------------------------------------------ cpp-clip-returns
@model('cpp-clip-returns', '`{0.02, -0.1, 0.1, -0.01, 2}`')
def _(t):
    rets, cap = t['args']
    out = [cap if r > cap else -cap if r < -cap else r for r in rets]
    return out + [sum(1 for r in rets if abs(r) > cap)]


# ------------------------------------------------------------------ cpp-tick-log
@model('cpp-tick-log', 'the answer is 10')
def _(t):
    ts = t['args'][0]
    flags, last, first, n = [], None, None, 0
    for x in ts:
        ok = last is None or x >= last
        flags.append(1 if ok else 0)
        if ok:
            first = x if first is None else first
            last, n = x, n + 1
    return flags + [n, (last - first) if n >= 2 else 0]


# ------------------------------------------------------------------ cpp-high-water
@model('cpp-high-water', '`{-3, -1, -1, 4, 4}`')
def _(t):
    xs = t['args'][0]
    return list(itertools.accumulate(xs, max)) if xs else []


# ------------------------------------------------------------------ cpp-fee-tier
@model('cpp-fee-tier', 'the answer is 8')
def _(t):
    frm, bps, asks = t['args']
    import bisect
    return [bps[bisect.bisect_right(frm, a) - 1] for a in asks] + [len(frm)]


# ------------------------------------------------------------------ cpp-range-out
@model('cpp-range-out', '`{1, -1, 3.5}`')
def _(t):
    xs, want_lo, want_hi = t['args']
    lo = hi = 999
    if not xs:
        return [0, lo, hi]
    s = sorted(xs)
    return [1, s[0] if want_lo else lo, s[-1] if want_hi else hi]


# ------------------------------------------------------------------ cpp-session-time
def _wrap(m):
    while m < 0:
        m += 1440
    while m >= 1440:
        m -= 1440
    return m


@model('cpp-session-time', 'is 10')
def _(t):
    if 'compiles' in t:
        return False                      # explicit constructor: no copy-initialisation from int
    c = t['call']
    m = re.fullmatch(r'\(SessionTime\((.+?)\) \+ \(?(-?\d+)\)?\)\.minutes\(\)', c)
    if m:
        return _wrap(eval(m.group(1)) + int(m.group(2)))
    m = re.fullmatch(r'SessionTime\((-?[\d *+]+)\)\.minutes\(\)', c)
    if m:
        return _wrap(eval(m.group(1)))
    m = re.fullmatch(r'SessionTime\((-?\d+)\) - SessionTime\((-?\d+)\)', c)
    if m:                                 # minutes forward from a to b
        a, b = _wrap(int(m.group(2))), _wrap(int(m.group(1)))
        return b - a if b >= a else b - a + 1440
    m = re.fullmatch(r'SessionTime\((-?\d+)\) < SessionTime\((-?\d+)\)', c)
    if m:
        return _wrap(int(m.group(1))) < _wrap(int(m.group(2)))
    raise KeyError(c)


# ------------------------------------------------------------------ cpp-crossings
@model('cpp-crossings', 'The answer is 3')
def _(t):
    m = re.fullmatch(r'count_crossings\(std::vector<(int|long long|double)>\{(.*)\}, (.+)\)', t['call'])
    num = (lambda s: float(s)) if m.group(1) == 'double' else (lambda s: int(s.rstrip('L')))
    xs = [num(s) for s in m.group(2).split(', ')] if m.group(2) else []
    level = num(m.group(3))
    signs = [1 if x > level else -1 for x in xs if x != level]     # drop the values at the level
    return sum(1 for a, b in zip(signs, signs[1:]) if a != b)


# ------------------------------------------------------------------ cpp-drop-small
@model('cpp-drop-small', '`{300, 400, 3}`')
def _(t):
    v, m = t['args']
    v = list(v)
    removed = 0
    i = 0
    while i < len(v):
        if v[i] < m:
            del v[i]
            removed += 1
        else:
            i += 1
    return v + [removed]


# ------------------------------------------------------------------ cpp-trimmed-mean
@model('cpp-trimmed-mean', 'The answer is 107.5')
def _(t):
    v, k = t['args']
    if 2 * k >= len(v):
        return 0.0
    s = sorted(v)
    mid = s[k:len(s) - k]
    return float(Fraction(sum(mid), len(mid)))


# ------------------------------------------------------------------ cpp-movers
@model('cpp-movers', '`{"BARC", "VOD"}`')
def _(t):
    syms, px, pct = t['args']
    rows = {}
    for i, s in enumerate(syms):            # positions of each symbol's first and last trade
        rows.setdefault(s, [i, i])[1] = i
    out = []
    for s, (i, j) in rows.items():
        first, last = Fraction(px[i]), Fraction(px[j])
        mv = abs(last - first) / first
        if mv * 100 >= Fraction(pct):
            out.append((mv, s))
    out.sort(key=lambda r: r[1])            # alphabetical, then a stable sort by move, largest first
    out.sort(key=lambda r: r[0], reverse=True)
    return [s for _, s in out]


# ------------------------------------------------------------------ cpp-mean-ranks
@model('cpp-mean-ranks', '`{3.5, 1, 3.5, 2}`')
def _(t):
    v = t['args'][0]
    # rank = (number strictly below) + (number equal + 1) / 2
    return [sum(1 for y in v if y < x) + (sum(1 for y in v if y == x) + 1) / 2 for x in v]


# ------------------------------------------------------------------ pricing helpers (mpmath, 40 digits)
import mpmath
mpmath.mp.dps = 40


def _Phi(x):
    return mpmath.ncdf(mpmath.mpf(x))


# ------------------------------------------------------------------ cpp-compound-df
@model('cpp-compound-df', '0.952381')
def _(t):
    r, tt, m = (mpmath.mpf(x) for x in t['args'])
    v = mpmath.e ** (-r * tt) if m == 0 else (1 + r / m) ** (-m * tt)
    return float(v)


# ------------------------------------------------------------------ cpp-prob-between
@model('cpp-prob-between', '0.682689')
def _(t):
    mu, s, a, b = (mpmath.mpf(x) for x in t['args'])
    if a > b:
        return 0.0
    return float(mpmath.quad(lambda x: mpmath.npdf(x, mu, s), [a, mu, b]) if a < mu < b
                 else mpmath.quad(lambda x: mpmath.npdf(x, mu, s), [a, b]))


# ------------------------------------------------------------------ cpp-cash-or-nothing
@model('cpp-cash-or-nothing', '0.532325')
def _(t):
    s, k, r, sg, tt, pay = (mpmath.mpf(x) for x in t['args'])
    if tt == 0:
        return float(pay) if s > k else 0.0
    d1 = (mpmath.log(s / k) + (r + sg ** 2 / 2) * tt) / (sg * mpmath.sqrt(tt))
    return float(pay * mpmath.e ** (-r * tt) * _Phi(d1 - sg * mpmath.sqrt(tt)))


# ------------------------------------------------------------------ cpp-scaled-payoff
def _payoff(expr):
    """Evaluate the C++ payoff expressions of the tests with Python classes of the same names."""
    class Forward:
        def __init__(self, k): self.k = k
        def __call__(self, s): return s - self.k

    class Call:
        def __init__(self, k): self.k = k
        def __call__(self, s): return max(s - self.k, 0.0)

    class Scaled:
        def __init__(self, q, inner): self.q, self.inner = q, inner
        def __call__(self, s): return self.q * self.inner(s)
    py = re.sub(r'std::make_unique<(\w+)>', r'\1', expr)
    return eval(py, {'Forward': Forward, 'Call': Call, 'Scaled': Scaled})


@model('cpp-scaled-payoff', 'pays 20')
def _(t):
    c = t['call']
    if c.startswith('[]'):
        if 'const Payoff& p = s' in c:
            return 2.0 * (15.0 - 10.0)
        if 'std::make_unique<Scaled>(0.5, std::make_unique<Forward>(0.0))' in c:
            return 0.5 * (-8.0 - 0.0)
        if 'book.push_back' in c:
            return -2.0 * max(120.0 - 110.0, 0) + (120.0 - 95.0)
        raise KeyError(c)
    return _payoff(c)


# ------------------------------------------------------------------ cpp-curve-df
@model('cpp-curve-df', '0.950279')
def _(t):
    times, zeros, x = t['args']
    x = mpmath.mpf(x)
    pts = [(mpmath.mpf(a), mpmath.mpf(a) * mpmath.mpf(z)) for a, z in zip(times, zeros)]
    if x <= pts[0][0]:
        y = mpmath.mpf(zeros[0]) * x
    elif x >= pts[-1][0]:
        y = mpmath.mpf(zeros[-1]) * x
    else:
        for (a, ya), (b, yb) in zip(pts, pts[1:]):
            if a <= x <= b:
                y = ya * (b - x) / (b - a) + yb * (x - a) / (b - a)
                break
    return float(mpmath.e ** (-y))


# ------------------------------------------------------------------ cpp-running-stats
def _moments(xs):
    n = len(xs)
    if n == 0:
        return [0, 0.0, 0.0]
    m = Fraction(sum(Fraction(x) for x in xs), n)
    # sample variance from the pairwise form: sum over pairs (xi - xj)^2 / (n (n - 1))
    if n < 2:
        return [1, float(m), 0.0]
    s1 = sum(Fraction(x) for x in xs)
    s2 = sum(Fraction(x) ** 2 for x in xs)
    v = (n * s2 - s1 * s1) / (n * (n - 1))      # exact in fractions, so no cancellation
    return [n, float(m), float(v)]


@model('cpp-running-stats', '32 / 7, about 4.571429')
def _(t):
    if t['call'] == 'stats_of':
        return _moments(t['args'][0])
    if t['call'] == 'merged':
        return _moments(t['args'][0] + t['args'][1])
    if 's.add(i % 7)' in t['call']:
        return _moments([i % 7 for i in range(100000)])
    raise KeyError(t['call'])


# ------------------------------------------------------------------ cpp-cash-split
@model('cpp-cash-split', 'gives 34, 33 and 33')
def _(t):
    c, a = t['call'], t['args']
    def pence(x):                                # nearest penny of the double x * 100, half away from zero
        v = Fraction(x * 100)
        lo = math.floor(v)
        frac = v - lo
        if frac > Fraction(1, 2) or (frac == Fraction(1, 2) and v > 0):
            return lo + 1
        return lo
    if c == 'pounds_to_pence':
        return pence(a[0])
    if c == 'add_pounds':
        return pence(a[0]) + pence(a[1])
    if c == 'split_pence':
        p, n = a
        sign = -1 if p < 0 else 1
        base, extra = divmod(abs(p), n)
        return [sign * (base + (1 if i < extra else 0)) for i in range(n)]
    raise KeyError(c)


# ------------------------------------------------------------------ cpp-bermudan-put
def _berm(s, k, u, d, g, n, dates):
    """Value by recursion over nodes, memoised; exercise allowed at listed steps and at expiry."""
    s, k, u, d, g = (Fraction(x) for x in (s, k, u, d, g))
    q = (g - d) / (u - d)
    memo = {}

    def V(i, j):
        if (i, j) in memo:
            return memo[(i, j)]
        spot = s * u ** j * d ** (i - j)
        if i == n:
            val = max(k - spot, 0)
        else:
            val = (q * V(i + 1, j + 1) + (1 - q) * V(i + 1, j)) / g
            if i in dates and i > 0:
                val = max(val, k - spot)
        memo[(i, j)] = val
        return val
    return float(V(0, 0))


BERM_BRIEF = f'{_berm(100, 100, 1.1, 0.9, 1.02, 3, [2]):.6f}, above the European {_berm(100, 100, 1.1, 0.9, 1.02, 3, []):.6f}'


@model('cpp-bermudan-put', BERM_BRIEF)
def _(t):
    return _berm(*t['args'])


# ------------------------------------------------------------------ rounded numbers stated in briefs and notes
def brief_numbers():
    nd = NormalDist()
    checks = [
        ('cpp-compound-df', f'{1.025 ** -4:.6f}', '0.905951'),
        ('cpp-compound-df', f'{1 / 1.05:.6f}', '0.952381'),
        ('cpp-prob-between', f'{nd.cdf(1) - nd.cdf(-1):.6f}', '0.682689'),
        ('cpp-cash-or-nothing', f'{(math.log(1) + (0.05 - 0.02)) / 0.2:.2f}', '0.15'),
        ('cpp-cash-or-nothing', f'{math.exp(-0.05) * nd.cdf(0.15):.6f}', '0.532325'),
        ('cpp-curve-df', f'{(0.032 * 1 + 0.035 * 2) / 2:.3f}', '0.051'),
        ('cpp-curve-df', f'{math.exp(-0.051):.6f}', '0.950279'),
        ('cpp-running-stats', f'{32 / 7:.6f}', '4.571429'),
        ('cpp-fill-csv', f'{100 * 2510 - 40 * 2490:,}', '151,400'),
        ('cpp-fee-pence', f'{123456 * 5 / 10000}', '61.728'),
        ('cpp-trimmed-mean', f'{(99 + 101 + 110 + 120) / 4}', '107.5'),
        ('cpp-movers', f'{10 / 250:.2f} {4 / 100:.2f} {50 / 5000:.2f}', '0.04 0.04 0.01'),
        ('cpp-fee-pence', f'{2 ** 31 / 100 / 1e6:.0f}', '21'),      # an int overflows past about 21 million pounds at 1 bp
        ('cpp-cash-split', repr(0.29 * 100), '28.999999999999996'),
        ('cpp-running-stats', f'{math.ulp(1e18):.0f}', '128'),
    ]
    for i, got, want in checks:
        if got != want:
            errors.append(f'{i}: stated number {want}, recomputed {got}')
    return len(checks)


# ================================================================== driver
def main():
    files = sorted(f for f in os.listdir(DR) if f.startswith('cpp-') and f.endswith('.json'))
    index = {r['id']: r for r in json.load(open(os.path.join(DR, 'index.json')))}
    mix = {}
    checked = 0
    for f in files:
        d = json.load(open(os.path.join(DR, f)))
        i = d['id']
        if i not in MODELS:
            errors.append(f'{i}: no model in this script')
            continue
        if d.get('pack') != 'cpp' or d.get('language') != 'cpp':
            errors.append(f'{i}: pack or language')
        if d['course'] not in ('cpp', 'cpp-pricing'):
            errors.append(f'{i}: course {d["course"]}')
        row = index.get(i)
        if not row or row['name'] != d['name'] or row['course'] != d['course'] or row['difficulty'] != d['difficulty']:
            errors.append(f'{i}: index row disagrees with the file')
        if not 300 <= d['pace'] <= 1200:
            errors.append(f'{i}: pace {d["pace"]}')
        mix.setdefault(d['course'], {}).setdefault(d['difficulty'], 0)
        mix[d['course']][d['difficulty']] += 1
        if not d['how'].startswith(f'Submit runs {len(d["tests"])} hidden tests.'):
            errors.append(f'{i}: how count')
        if BRIEF[i] not in d['brief']:
            errors.append(f'{i}: worked answer {BRIEF[i]!r} not in the brief')
        if len(d.get('planted', [])) < 2:
            errors.append(f'{i}: fewer than two planted')
        calls = [json.dumps({k: v for k, v in t.items() if k != 'note'}, sort_keys=True) for t in d['tests']]
        for ex in d['examples']:
            key = json.dumps({k: v for k, v in ex.items() if k != 'note'}, sort_keys=True)
            if key not in calls:
                errors.append(f'{i}: example {ex.get("call")} is not also a hidden test')
        for kind in ('examples', 'tests'):
            for n, t in enumerate(d[kind]):
                want = MODELS[i](t)
                got = t['expect']
                ok = close(want, got) if t.get('compare') == 'isclose' else want == got
                if not ok:
                    errors.append(f'{i} {kind}[{n}]: file {got!r}, model {want!r}')
                checked += 1
    want_mix = {'cpp': {1: 6, 2: 7, 3: 4}, 'cpp-pricing': {1: 2, 2: 3, 3: 3}}
    if len(files) == 25 and mix != want_mix:
        errors.append(f'mix {mix} is not {want_mix}')
    nb = brief_numbers()
    for f in files:                                   # voice in learner-facing prose
        d = json.load(open(os.path.join(DR, f)))
        prose = [d['brief'], d['hint'], d['how']] + d['constraints'] + d['notes'] + \
                [p['slip'] for p in d['planted']] + [e.get('note', '') for e in d['examples']]
        for p in prose:
            if '!' in re.sub(r'`[^`]*`', '', p) or '—' in p or '–' in p:
                errors.append(f'{d["id"]}: exclamation mark or dash in {p[:40]!r}')
    print(f'{nb} rounded numbers in briefs and notes recomputed')
    print('mix', json.dumps(mix, sort_keys=True))
    print(f'{len(files)} drills, {checked} cases compared')
    for e in errors:
        print('ERROR', e)
    print(f'errors: {len(errors)}')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
