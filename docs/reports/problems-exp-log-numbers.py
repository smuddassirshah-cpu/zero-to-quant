"""Recompute every number in app/content/courses/exp-log/problems-<n>.json twice.

Method 1 is exact where it can be: fractions, or sympy (log, exp, roots kept symbolic and then
evaluated to 30 digits). Method 2 is independent: the story worked step by step (month by month,
hour by hour, a loop of halvings), a bisection for each unknown power, a series for e^x and ln,
or a brute search over whole numbers. For each numeric part the script checks that the two methods
agree; that the key lies inside its own band; that the value at the rounding the question asks for
is accepted, and so is the figure printed last in `feedback.correct` (and any rounded route the
explanation prints); that every `wrong` value is the value its named slip gives (computed here),
has a byKey line, lies outside the key's band and does not overlap another `wrong`. Percent parts
check the decimal slip (the figure typed as a fraction) and that `accept` gives the per cent figure.
Expression parts are compared with sympy at sample points (a route separate from the app's grader;
the engine grader was run separately, see the report). Choice parts check the keyed option and the
arithmetic behind it. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-exp-log-numbers.py
"""
import json, os, re, sys, math
from fractions import Fraction as F
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'exp-log')
fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    return {it['id']: it for it in json.load(open(os.path.join(COURSE, f'problems-{n}.json')))['items']}


# ---------------------------------------------------------------- second-route helpers (no math.log / math.exp)
def exp_series(x, terms=250):
    if x < 0:
        return 1 / exp_series(-x, terms)
    s, t = 0.0, 1.0
    for k in range(terms):
        s += t
        t *= x / (k + 1)
    return s


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def ln_b(y):
    """ln y by bisection on the exp series."""
    return bisect(lambda x: exp_series(x) - y, -60, 60)


def log10_b(y):
    return ln_b(y) / ln_b(10)


def ev(e):
    return float(sp.N(e, 30))


def within(v, key, tol):
    return abs(v - key) <= tol + 1e-12


def printed_last(text):
    s = text.replace('{,}', '').replace(',', '')
    hits = re.findall(r'(-?\d+(?:\.\d+)?)', re.sub(r'\$[^$]*\\tfrac\{[^}]*\}\{[^}]*\}', '', s))
    return float(hits[-1]) if hits else None


# ---------------------------------------------------------------- part checks
def num(items, iid, k, exact, alt, slips, asked=None, extra_ok=(), agree=1e-9, printed=True, pct=False):
    """exact, alt: the two routes. slips: {wrong id: value from the slip}. asked: the value at the rounding
    the question asks for. extra_ok: other sensible values that must be accepted."""
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    e, a = float(exact), float(alt)
    ok(abs(e - a) <= agree * max(1, abs(e)), f'{tag}: methods differ {e} vs {a}')
    key, tol = w['answer'], w['tol']['abs']
    ok(within(e, key, tol), f'{tag}: exact {e} outside key {key} +- {tol}')
    if asked is not None:
        ok(within(asked, key, tol), f'{tag}: asked rounding {asked} refused')
    for v in extra_ok:
        ok(within(v, key, tol), f'{tag}: sensible value {v} refused')
    if printed:
        p = printed_last(part['feedback']['correct'])
        if pct:
            p = p / 100 if p is not None else None
        ok(p is not None and within(p, key, tol), f'{tag}: printed last figure {p} refused')
    ids = [x['id'] for x in w.get('wrong', [])]
    ok(set(ids) == set(slips), f'{tag}: wrong ids {ids} vs slips {list(slips)}')
    by = part['feedback'].get('byKey', {})
    for x in w.get('wrong', []):
        wt = x.get('tol', w['tol'])['abs']
        s = slips.get(x['id'])
        ok(s is not None and within(float(s), x['value'], wt), f'{tag}: wrong {x["id"]} = {x["value"]} vs slip {s} (tol {wt})')
        ok(not within(x['value'], key, tol) and abs(x['value'] - key) > tol + wt, f'{tag}: wrong {x["id"]} band meets the key band')
        ok(x['id'] in by, f'{tag}: wrong {x["id"]} has no byKey line')
        for y in w.get('wrong', []):
            if y is not x:
                yt = y.get('tol', w['tol'])['abs']
                ok(abs(x['value'] - y['value']) > wt + yt, f'{tag}: wrongs {x["id"]} and {y["id"]} overlap')
    if pct:
        ok(w.get('unit') == '%', f'{tag}: % unit missing')
        m = re.search(r'(-?\d+(?:\.\d+)?)%', w['accept'])
        ok(m is not None and within(float(m.group(1)) / 100, key, tol), f'{tag}: accept per cent figure refused')
        ok('decimal' in slips and within(key / 100, slips['decimal'], 1e-6), f'{tag}: decimal slip missing or wrong')
    ok('Any form' not in w.get('accept', ''), f'{tag}: accept promises a form')
    return e


X = {s: sp.Symbol(s, positive=True) for s in 'nt'}


def expr_part(items, iid, k, mine, slips, var):
    """mine: my own sympy expression for the answer. slips: {wrong id: sympy expression of the slip}."""
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    s = X[var]

    def parse(tex):
        t = tex.replace('\\cdot', '*').replace('\\times', '*')
        t = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
        t = t.replace('e^{', 'E**(').replace('^{', '**(').replace('{', '(').replace('}', ')').replace('^', '**')
        t = re.sub(r'(\d)\(', r'\1*(', t)
        t = re.sub(r'(\d)([a-zE])', r'\1*\2', t)
        t = re.sub(r'\)\(', r')*(', t)
        return sp.sympify(t, locals={var: s, 'E': sp.E}, rational=True)

    pts = [0.3, 0.7, 1.1, 1.9, 2.4, 3.0]
    same = lambda A, B: all(abs(ev(A.subs(s, p)) - ev(B.subs(s, p))) <= 1e-9 * max(1, abs(ev(B.subs(s, p)))) for p in pts)
    ok(same(parse(w['answer']), mine), f'{tag}: answer differs from mine')
    ok(sp.simplify(parse(w['answer']) - mine) == 0, f'{tag}: answer not equal to mine symbolically')
    for a in w.get('accept', []):
        ok(same(parse(a), mine), f'{tag}: accept {a} differs')
    ids = [x['id'] for x in w['wrong']]
    ok(set(ids) == set(slips), f'{tag}: wrong ids {ids} vs {list(slips)}')
    for x in w['wrong']:
        ok(same(parse(x['tex']), slips[x['id']]), f'{tag}: wrong {x["id"]} is not its slip')
        ok(not same(parse(x['tex']), mine), f'{tag}: wrong {x["id"]} equals the answer')
        ok(x['id'] in part['feedback']['byKey'], f'{tag}: wrong {x["id"]} has no byKey line')
    ok('ln(' not in w['answer'] + ''.join(w.get('accept', [])).replace('\\ln(', ''), f'{tag}: plain ln( in answer or accept')


def pick(items, iid, k, key, fact):
    part = items[iid]['parts'][k - 1]
    opts = part['widget']['options']
    right = [o['id'] for o in opts if o.get('correct')]
    ok(right == [key], f'{iid} p{k}: keyed option {right}, expected {key}')
    ok(all('why' in o for o in opts if not o.get('correct')), f'{iid} p{k}: an option has no why')
    ok(fact, f'{iid} p{k}: the arithmetic behind the key fails')


def stated(msg, a, b, tol=1e-9):
    ok(abs(float(a) - float(b)) <= tol, f'stated {msg}: {a} vs {b}')


def first_whole(pred, lo=0, hi=10000):
    for v in range(lo, hi):
        if pred(v):
            return v
    return None


# ================================================================ level 1
def level1():
    L = load(1)
    n = X['n']
    # p-yeast-culture
    expr_part(L, 'p-yeast-culture', 1, 3000 * 2 ** n, {'base-times': 6000 ** n, 'added': 3000 + 2 ** n, 'steady': 6000 * n}, 'n')
    cells = lambda h: 3000 * F(2) ** h
    back = 3000
    for _ in range(2):
        back = F(back, 2)  # two hours back, halving
    num(L, 'p-yeast-culture', 2, cells(-2), back, {'negative': 3000 * -4, 'one-hour': 3000 / 2, 'forwards': 3000 * 4})
    half = ev(3000 * sp.sqrt(2))
    g = bisect(lambda x: x * x - 2, 1, 2)  # the half-hour factor with g^2 = 2
    num(L, 'p-yeast-culture', 3, half, 3000 * g, {'halfway': 4500, 'times-half': 3000 * 2 * 0.5, 'halved': 3000 * 0.5, 'base-times': ev(sp.sqrt(6000))},
        asked=round(half), extra_ok=(3000 * 1.4142, 4242, 4243, 3000 * 1.414))
    k = F(1, 2) - (-2)
    num(L, 'p-yeast-culture', 4, k, math.log2(half / 750), {'added-powers': F(1, 2) + (-2), 'divided-powers': F(1, 2) / -2, 'ratio': half / 750})
    stated('yeast: 4243 / 750', round(4243 / 750, 2), 5.66, 1e-9)
    stated('yeast: 2^2.5', round(2 ** 2.5, 2), 5.66)

    # p-laptop-value
    f = 1 - F(25, 100)
    num(L, 'p-laptop-value', 1, f, 0.75, {'loss': F(25, 100), 'rise': 1 + F(25, 100)})
    v = [1200.0]
    for _ in range(6):
        v.append(v[-1] - v[-1] * 0.25)  # year by year
    num(L, 'p-laptop-value', 2, 1200 * f ** 2, v[2], {'steady': 1200 - 2 * 300, 'one-year': 1200 * f, 'loss-factor': 1200 * F(1, 4) ** 2, 'rise-factor': 1200 * F(5, 4) ** 2})
    v4 = 675 * f ** 2
    num(L, 'p-laptop-value', 3, v4, v[4], {'steady': 675 - (1200 - 675), 'one-year': 1200 * f ** 3, 'halved': F(675, 2)}, asked=379.69)
    stated('laptop: 0.75^2', f ** 2, 0.5625)
    lost = 1 - f ** 4
    num(L, 'p-laptop-value', 4, lost, (1200 - v[4]) / 1200,
        {'added': 4 * F(25, 100), 'kept': f ** 4, 'one-short': 1 - f ** 3, 'decimal': float(lost) / 100}, pct=True, asked=0.6836,
        extra_ok=((1200 - 379.69) / 1200,))
    stated('laptop: 1200 - 379.69', round(1200 - 379.69, 2), 820.31, 1e-6)
    stated('laptop: 0.75^4 as %', round(float(f ** 4) * 100, 2), 31.64)

    # p-rare-coin
    r2 = F(1000, 640)
    num(L, 'p-rare-coin', 1, r2, 1000 / 640, {'inverted': F(640, 1000), 'rise': r2 - 1})
    gy = sp.sqrt(sp.Rational(25, 16))
    num(L, 'p-rare-coin', 2, ev(gy), bisect(lambda x: x * x - 1.5625, 1, 2), {'halved-factor': r2 / 2, 'halved-rise': 1 + (r2 - 1) / 2, 'squared': r2 ** 2})
    stated('coin: 640 * 1.25', 640 * F(5, 4), 800)
    stated('coin: 800 * 1.25', 800 * F(5, 4), 1000)
    num(L, 'p-rare-coin', 3, ev(gy) - 1, F(1000 - 800, 800), {'factor': 1.25, 'halved-rise': (r2 - 1) / 2, 'decimal': 0.25 / 100}, pct=True, asked=0.25)
    v18 = ev(1000 * sp.Rational(5, 4) ** sp.Rational(3, 2))
    num(L, 'p-rare-coin', 4, v18, 1000 * bisect(lambda x: x * x - 1.25, 1, 2) ** 3,
        {'halfway': (1250 + 1562.5) / 2, 'simple': 1000 * (1 + 1.5 * 0.25), 'one-year': 1250, 'two-years': 1562.5, 'carried': 1000 * 1.28125 ** 1.5},
        asked=round(v18), extra_ok=(1000 * 1.118 ** 3, 1397, 1398, 1000 * 1.1180 ** 3), printed=True)
    stated('coin: 1.25^1.5 to 5 dp', round(1.25 ** 1.5, 5), 1.39754)
    cw = L['p-rare-coin']['parts'][3]['widget']
    ok(cw['tol']['abs'] == 1, 'coin 4: band is +-1')
    ok(not within(1399, cw['answer'], cw['tol']['abs']) and not within(1396, cw['answer'], cw['tol']['abs']), 'coin 4: 1399 or 1396 accepted')
    ok(all(within(v, cw['answer'], cw['tol']['abs']) for v in (1397, 1398, 1397.5, 1397.54)), 'coin 4: a sensible entry refused')

    # p-curve-point
    a = sp.Integer(64) ** sp.Rational(1, 3)
    num(L, 'p-curve-point', 1, ev(a), bisect(lambda x: x ** 3 - 64, 1, 10), {'divided': 64 / 3, 'square-root': 8})
    h = bisect(lambda x: 4 ** x - 2, 0, 2)
    num(L, 'p-curve-point', 2, F(1, 2), h, {'factor': 2, 'quarter': 0.25, 'one': 1})
    stated('curve: 4^0.25', round(4 ** 0.25, 3), 1.414)
    x3 = 3 + 5 * F(1, 2)
    num(L, 'p-curve-point', 3, x3, bisect(lambda x: 4 ** x - 2048, 0, 10), {'step-one': 3 + 5 * 1, 'counted-ratio': 3 + 32 * 0.5, 'distance-only': 5 * 0.5, 'step-two': 3 + 5 * 2})
    stated('curve: 2048 / 64', F(2048, 64), 2 ** 5)
    stated('curve: 4^5.5 = 2^11', 4 ** 5.5, 2 ** 11)
    num(L, 'p-curve-point', 4, -x3, bisect(lambda x: 0.25 ** x - 2048, -10, 0), {'no-flip': 5.5, 'reciprocal': 1 / 5.5})
    stated('curve: 4^-5.5', 4 ** -5.5, 1 / 2048)


# ================================================================ level 2
def level2():
    L = load(2)
    n = X['n']

    def halvings(N):
        c, s = 0, N
        while s > 1:
            s = -(-s // 2)  # suspects left, rounding up
            c += 1
        return c

    # p-fault-search
    num(L, 'p-fault-search', 1, ev(sp.log(2048, 2)), halvings(2048), {'halved': 1024, 'off-by-one': 10})
    num(L, 'p-fault-search', 2, ev(sp.log(32, 2) + sp.log(2048, 2)), halvings(32 * 2048), {'multiplied-logs': 5 * 11, 'times-batches': 32 * 11, 'added-count': 32 + 11, 'carried': 5 + 10})
    stated('search: 2^16', 2 ** 16, 65536)
    stated('search: 5 * 65536', 5 * 65536, 327680)
    wk = math.ceil(ev(16 + sp.log(5, 2)))
    num(L, 'p-fault-search', 3, wk, halvings(327680), {'rounded-down': 18, 'added-five': 21, 'times-five': 80})
    ok(2 ** 18 < 327680 <= 2 ** 19, 'search: 2^18 < 327680 <= 2^19')
    stated('search: 2^19', 2 ** 19, 524288)
    stated('search: 2^18', 2 ** 18, 262144)

    # p-forty-doublings
    l2 = 0.30103
    stated('forty: log 2 to 5 dp', round(ev(sp.log(2, 10)), 5), l2)
    p1 = 40 * l2
    num(L, 'p-forty-doublings', 1, p1, round(log10_b(2 ** 40), 4), {'swapped': 2 * ev(sp.log(40, 10)), 'added': 40 + l2}, agree=1e-4,
        extra_ok=(ev(sp.log(2 ** 40, 10)),))
    num(L, 'p-forty-doublings', 2, math.floor(p1), len(str(2 ** 40)) - 1, {'rounded-up': 13, 'power': 40, 'carried': math.floor(2 * ev(sp.log(40, 10)))})
    m = 10 ** 0.0412
    num(L, 'p-forty-doublings', 3, m, 2 ** 40 / 10 ** 12, {'fraction-part': 0.0412, 'one-plus': 1.0412}, agree=1e-3, asked=1.10, extra_ok=(1.1,))
    stated('forty: exact 2^40', 2 ** 40, 1099511627776)
    stated('forty: 10^0.0412 to 4 dp', round(m, 4), 1.0995)
    d = math.ceil((16 - p1) / l2)
    num(L, 'p-forty-doublings', 4, d, first_whole(lambda j: 2 ** (40 + j) > 10 ** 16), {'rounded-down': 13, 'tenfold-steps': round(16 - p1), 'total': 40 + d})
    stated('forty: key is 14', d, 14)
    stated('forty: gap / log 2', round((16 - 12.0412) / l2, 2), 13.15)
    stated('forty: factor needed 10^16 / 1.10e12', round(10 ** 16 / 1.10e12), 9091)
    stated('forty: log 9091 to 4 dp', round(ev(sp.log(9091, 10)), 4), 3.9586)
    stated('forty: log 9091 / log 2', round(3.9586 / l2, 2), 13.15)
    ok(2 ** 13 == 8192 and 8192 < 10 ** 16 / 1.10e12 < 2 ** 14, 'forty: 2^13 short, 2^14 enough')
    ok(2 ** 53 < 10 ** 16 < 2 ** 54, 'forty: 2^53 < 10^16 < 2^54')
    ok(round(13.1503) == 13 and d == 14, 'forty: nearest rounding of 13.15 gives 13, not the key')

    # p-drawdown-recovery
    v1 = 50000 * F(4, 5) ** 2
    walk = 50000.0
    for _ in range(2):
        walk -= 0.2 * walk
    num(L, 'p-drawdown-recovery', 1, v1, walk, {'added-falls': 50000 * F(6, 10), 'one-fall': 50000 * F(4, 5)})
    gain = F(50000) / v1 - 1
    num(L, 'p-drawdown-recovery', 2, gain, (50000 - walk) / walk, {'two-twenties': 0.40, 'the-loss': 0.36, 'factor': F(50000) / v1, 'carried': F(50000, 30000) - 1, 'decimal': float(gain) / 100}, pct=True)
    stated('recovery: 32000 * 1.2^2', 32000 * 1.2 ** 2, 46080, 1e-6)
    stated('recovery: 1.5625 = 1.25^2', F(50000) / v1, F(5, 4) ** 2)
    nexact = ev(2 * sp.log(sp.Rational(5, 4)) / sp.log(sp.Rational(111, 100)))
    nround = 2 * 0.09691 / 0.04532
    num(L, 'p-drawdown-recovery', 3, nexact, bisect(lambda x: 1.11 ** x - 1.5625, 0, 20),
        {'no-power': 0.09691 / 0.04532, 'inverted': 0.04532 / (2 * 0.09691), 'simple': 0.5625 / 0.11, 'carried': ev(sp.log(1.4) / sp.log(sp.Rational(111, 100))), 'divided-numbers': 1.5625 / 1.11},
        asked=4.28, extra_ok=(nround,))
    stated('recovery: log 1.25 to 5 dp', round(ev(sp.log(1.25, 10)), 5), 0.09691)
    stated('recovery: log 1.11 to 5 dp', round(ev(sp.log(1.11, 10)), 5), 0.04532)
    stated('recovery: 0.19382 / 0.04532', round(0.19382 / 0.04532, 2), 4.28)
    stated('recovery: 2 * 0.09691', 2 * 0.09691, 0.19382)
    ok('11%' in L['p-drawdown-recovery']['prose'] and '8%' not in L['p-drawdown-recovery']['prose'], 'recovery: prose growth rate is 11%')
    mm = first_whole(lambda j: 32000 * F(111, 100) ** j > 50000)
    num(L, 'p-drawdown-recovery', 4, mm, math.ceil(nexact), {'rounded-down': 4, 'with-falls': mm + 2})
    stated('recovery: month 4', round(32000 * 1.11 ** 4), 48578)
    stated('recovery: month 5', round(32000 * 1.11 ** 5), 53922)
    ok(round(nexact) == 4 and mm == 5, 'recovery: nearest rounding of n gives 4, not the key 5')

    # p-app-users
    expr_part(L, 'p-app-users', 1, 2000 * sp.Rational(13, 10) ** n, {'rate-only': 2000 * sp.Rational(3, 10) ** n, 'joined': 2600 ** n, 'steady': 2000 + 600 * n}, 'n')
    quot = ev(sp.log(sp.Rational(25) / sp.Rational(13, 10), 10))
    ratio = ev(sp.log(25, 10) / sp.log(sp.Rational(13, 10), 10))
    pick(L, 'p-app-users', 2, 'ratio', F(50000, 2000) == 25 and abs(ratio - ev(sp.log(25) / sp.log(sp.Rational(13, 10)))) < 1e-12
         and abs(ratio - bisect(lambda x: 1.3 ** x - 25, 0, 50)) < 1e-9 and abs(quot - 1.284) < 5e-4
         and abs(ev(sp.log(25, 10) - sp.log(sp.Rational(13, 10), 10)) - quot) < 1e-12
         and abs(25 / 1.3 - 19.23) < 5e-3 and 1.3 ** (25 / 1.3) > 100 and abs(quot - ratio) > 1)
    ok({o['id'] for o in L['p-app-users']['parts'][1]['widget']['options']} == {'ratio', 'quotient', 'difference', 'numbers'}, 'app 2: option ids')
    stated('app: log 25/1.3 to 3 dp', round(quot, 3), 1.284)
    stated('app: 1.3^19.23 to 0 dp', round(1.3 ** 19.23), 155, 1)
    nu = ev(sp.log(25) / sp.log(sp.Rational(13, 10)))
    num(L, 'p-app-users', 3, nu, bisect(lambda x: 1.3 ** x - 25, 0, 50),
        {'joined': ev(sp.log(50000) / sp.log(2600)), 'divided': 25 / 1.3, 'rate-only': ev(sp.log(25) / sp.log(sp.Rational(3, 10))), 'simple': (50000 - 2000) / 600},
        asked=12.27, extra_ok=(1.3979 / 0.1139, 1.39794 / 0.11394))
    stated('app: log 25 to 4 dp', round(ev(sp.log(25, 10)), 4), 1.3979)
    stated('app: log 1.3 to 4 dp', round(ev(sp.log(1.3, 10)), 4), 0.1139)
    stated('app: fixed 600 a month reaches 50,000 at n = 80', 2000 + 600 * 80, 50000)
    num(L, 'p-app-users', 4, first_whole(lambda j: 2000 * F(13, 10) ** j > 50000), math.ceil(nu), {'rounded-down': 12, 'joined': math.ceil(ev(sp.log(50000) / sp.log(2600)))})
    stated('app: month 12', round(2000 * 1.3 ** 12), 46596)
    stated('app: month 13', round(2000 * 1.3 ** 13), 60575)


# ================================================================ level 3
def level3():
    L = load(3)
    t = X['t']
    r = sp.Rational(55, 1000)
    # p-savings-doubling
    expr_part(L, 'p-savings-doubling', 1, 2400 * sp.exp(r * t), {'percent': 2400 * sp.exp(sp.Rational(11, 2) * t), 'yearly': 2400 * sp.Rational(211, 200) ** t, 'factor': 2400 * sp.exp(sp.Rational(211, 200) * t)}, 't')
    T = ev(sp.log(2) / r)
    num(L, 'p-savings-doubling', 2, T, bisect(lambda x: exp_series(0.055 * x) - 2, 0, 50),
        {'rule-72': 72 / 5.5, 'yearly': ev(sp.log(2) / sp.log(sp.Rational(211, 200))), 'percent': ev(sp.log(2)) / 5.5, 'factor': 2 / 0.055},
        asked=12.60, extra_ok=(0.6931 / 0.055,))
    stated('savings: 0.6931/0.055', round(0.6931 / 0.055, 2), 12.60)
    t3 = 3 * T
    num(L, 'p-savings-doubling', 3, t3, bisect(lambda x: 2400 * exp_series(0.055 * x) - 19200, 0, 100),
        {'eight-times': 8 * T, 'four': 4 * T, 'two': 2 * T}, asked=37.81, extra_ok=(3 * 12.60, 37.80))
    stated('savings: 19200/2400', F(19200, 2400), 8)
    half_db = 2400 * 2 ** 1.5
    direct = ev(2400 * sp.exp(r * sp.Rational(189, 10)))
    num(L, 'p-savings-doubling', 4, half_db, 2400 * exp_series(0.055 * t3 / 2),
        {'halfway-pounds': (2400 + 19200) / 2, 'midpoint': (4800 + 9600) / 2, 'years': ev(2400 * sp.exp(r * sp.Rational(3, 2)))},
        asked=round(half_db), extra_ok=(direct, round(direct), 2400 * 2.8284, round(2400 * 2.8284)), agree=1e-9)
    stated('savings: 2 sqrt 2 to 4 dp', round(2 * math.sqrt(2), 4), 2.8284)
    yrs = [x for x in L['p-savings-doubling']['parts'][3]['widget']['wrong'] if x['id'] == 'years'][0]['value']
    stated('savings: years slip 2400 e^(0.055 * 1.5) to 1 dp', round(2400 * exp_series(0.055 * 1.5), 1), yrs, 1e-9)
    stated('savings: years slip by doublings', round(2400 * 2 ** (1.5 / 12.6), 1), 2606.4, 0.05)

    # p-weekly-target
    lr = [F(30, 1000), F(-12, 1000), F(45, 1000), F(-20, 1000)]
    tot = sum(lr)
    prices = [40.0]
    for x in lr:
        prices.append(prices[-1] * exp_series(float(x)))
    num(L, 'p-weekly-target', 1, tot, ln_b(prices[-1] / 40), {'signs': sum(abs(x) for x in lr), 'averaged': tot / 4})
    fri = ev(40 * sp.exp(sp.Rational(43, 1000)))
    num(L, 'p-weekly-target', 2, fri, prices[-1], {'one-plus': 40 * 1.043, 'added': 40.043, 'carried': ev(40 * sp.exp(sp.Rational(107, 1000)))}, asked=41.76, extra_ok=(40 * 1.04394,))
    need = ev(sp.log(sp.Rational(4500, 4176)))  # the value the question names: Friday's close of 41.76
    num(L, 'p-weekly-target', 3, need, ln_b(45 / 41.76), {'simple': (45 - 41.76) / 41.76, 'from-monday': ev(sp.log(sp.Rational(9, 8))), 'inverted': -need, 'difference': 45 - 41.76},
        asked=0.0747, extra_ok=(0.0748, round(0.1178 - 0.043, 4), ev(sp.log(sp.Rational(9, 8)) - sp.Rational(43, 1000))))
    w3 = L['p-weekly-target']['parts'][2]['widget']
    ok(w3['answer'] == 0.074724 and w3['tol']['abs'] == 0.0001, 'weekly 3: key 0.074724 +- 0.0001')
    ok(within(0.0747, w3['answer'], w3['tol']['abs']) and within(0.0748, w3['answer'], w3['tol']['abs']), 'weekly 3: 0.0747 or 0.0748 refused')
    ok(not within(0.0746, w3['answer'], w3['tol']['abs']) and not within(0.0749, w3['answer'], w3['tol']['abs']), 'weekly 3: 0.0746 or 0.0749 accepted')
    ok(w3['accept'].startswith('0.0747'), 'weekly 3: accept leads with 0.0747')
    stated('weekly: ln(45/41.76) to 4 dp', round(need, 4), 0.0747)
    stated('weekly: ln 1.125 - 0.043 to 4 dp (Monday route)', round(math.log(1.125) - 0.043, 4), 0.0748)
    stated('weekly: Friday close is 41.76 to 2 dp', round(40 * math.exp(0.043), 2), 41.76)
    stated('weekly: ln 1.125 to 4 dp', round(ev(sp.log(sp.Rational(9, 8))), 4), 0.1178)
    wk = sp.Rational(747, 10000) / 3  # the question names 0.0747
    num(L, 'p-weekly-target', 4, wk, bisect(lambda x: 3 * x - 0.0747, 0, 1), {'cube-root': 0.0747 ** (1 / 3), 'times-three': 3 * 0.0747, 'carried': 0.0776 / 3},
        asked=0.0249, extra_ok=(0.0748 / 3, ln_b((45 / 41.76) ** (1 / 3)), need / 3))
    w4 = L['p-weekly-target']['parts'][3]['widget']
    ok(w4['answer'] == 0.0249, 'weekly 4: key is 0.0249')
    simple = ev(sp.exp(sp.Rational(249, 10000)) - 1)  # the question names 0.0249
    num(L, 'p-weekly-target', 5, simple, exp_series(0.0249) - 1,
        {'log-as-simple': 0.0249, 'simple-split': ((45 - 41.76) / 41.76) / 3, 'decimal': 0.0252 / 100, 'e-power': exp_series(0.0249)},
        pct=True, asked=0.0252, extra_ok=(0.0252, 0.02521, (45 / 41.76) ** (1 / 3) - 1))
    w5 = L['p-weekly-target']['parts'][4]['widget']
    dec5 = [x for x in w5['wrong'] if x['id'] == 'decimal'][0]
    ok(w5['answer'] == 0.025213 and w5['tol']['abs'] == 5e-05, 'weekly 5: key 0.025213 +- 5e-5')
    ok(not within(0.0251, w5['answer'], 5e-05) and not within(0.0253, w5['answer'], 5e-05), 'weekly 5: 2.51 or 2.53 accepted')
    ok(dec5['tol']['abs'] == 5e-07, 'weekly 5: decimal band is +-5e-7')
    ok(within(0.0252 / 100, dec5['value'], 5e-07) and within(0.02521 / 100, dec5['value'], 5e-07), 'weekly 5: decimal band refuses 0.0252 or 0.02521 typed')
    ok(not within(0.0249 / 100, dec5['value'], 5e-07) and not within(0.0259 / 100, dec5['value'], 5e-07), 'weekly 5: decimal band takes 0.0249 or 0.0259 typed')
    stated('weekly: e^0.0249 - 1 to 6 dp', round(math.exp(0.0249) - 1, 6), 0.025213)
    stated('weekly: 41.76 e^0.0747 reaches 45', round(41.76 * math.exp(0.0747), 2), 45.0, 0.01)
    stated('weekly: e^0.043 to 5 dp', round(math.exp(0.043), 5), 1.04394)
    stated('weekly: e^0.0249 to 4 dp', round(math.exp(0.0249), 4), 1.0252)
    stated('weekly: 41.76 * 1.0252^3 reaches 45', round(41.76 * 1.0252 ** 3, 1), 45.0)
    stated('weekly: simple 7.76%', round((45 - 41.76) / 41.76, 4), 0.0776)

    # p-log-chart-line
    kx = sp.log(9) / 8
    k = ev(kx)
    num(L, 'p-log-chart-line', 1, k, (ln_b(135) - ln_b(15)) / 8,
        {'simple-total': (135 - 15) / 15 / 8, 'ratio-over-years': 9 / 8, 'yearly-factor': 9 ** (1 / 8) - 1, 'log10': ev(sp.log(9, 10) / 8), 'decimal': 0.2747 / 100},
        pct=True, asked=0.2747)
    stated('chart: ln 9 to 4 dp', round(ev(sp.log(9)), 4), 2.1972)
    pr = L['p-log-chart-line']
    ok('start of 2017' in pr['prose'] and 'start of 2025' in pr['prose'] and 2025 - 2017 == 8, 'chart: prose dates 2017 to 2025, 8 years')
    ok('start of 2021' in pr['parts'][2]['question'] and 2017 + 4 == 2021, 'chart: part 3 date 2021, 4 years in')
    Tk = ev(sp.log(2) / kx)
    num(L, 'p-log-chart-line', 2, Tk, bisect(lambda x: exp_series(k * x) - 2, 0, 20),
        {'rule-72': 72 / 27.47, 'inverse': 1 / k, 'percent': ev(sp.log(2)) / 27.47, 'tripling': ev(sp.log(3) / kx)}, asked=2.52, extra_ok=(0.6931 / 0.2747,))
    p4 = ev(15 * sp.exp(4 * kx))
    num(L, 'p-log-chart-line', 3, p4, ev(sp.sqrt(15 * 135)), {'pounds-midpoint': (15 + 135) / 2, 'whole-doublings': 15 * 2, 'rounded-up': 15 * 4},
        asked=45, extra_ok=(15 * 2 ** (4 / 2.52), 15 * 2 ** 1.587, 15 * 2 ** 1.59))
    stated('chart: 4/2.52 to 2 dp', round(4 / 2.52, 2), 1.59)
    stated('chart: 4/2.52 to 3 dp', round(4 / 2.52, 3), 1.587)
    stated('chart: 2^1.587 to 2 dp', round(2 ** 1.587, 2), 3.00)
    h = 12 * ev(sp.log(3) / sp.log(9))
    num(L, 'p-log-chart-line', 4, h, 12 * (ln_b(45) - ln_b(15)) / (ln_b(135) - ln_b(15)),
        {'pounds': 12 * (45 - 15) / (135 - 15), 'ratio': 12 * 45 / 135}, extra_ok=(12 * ln_b(15 * 2 ** (4 / 2.52) / 15) / ln_b(9),))

    # p-monthly-deposit
    g12 = F(1004, 1000) ** 12
    bal = 1.0
    for _ in range(12):
        bal += bal * 0.048 / 12  # month by month
    num(L, 'p-monthly-deposit', 1, g12, bal, {'once': 1.048, 'continuous': round(math.exp(0.048), 4), 'whole-rate': 1.048 ** 12}, asked=1.0491, agree=1e-12)
    rc = ev(sp.log(sp.Rational(1004, 1000)) * 12)
    num(L, 'p-monthly-deposit', 2, rc, ln_b(float(g12)), {'quoted': 0.048, 'factor-rate': 1.0491 - 1, 'decimal': 0.0479 / 100, 'log10': ev(sp.log(1.0491, 10))},
        pct=True, asked=0.0479, extra_ok=(ev(sp.log(1.0491)),))
    stated('deposit: e^0.048 to 4 dp', round(math.exp(0.048), 4), 1.0492)
    d2 = L['p-monthly-deposit']['parts'][1]['widget']
    dec2 = [x for x in d2['wrong'] if x['id'] == 'decimal'][0]
    ok(dec2['tol']['abs'] == 5e-07, 'deposit 2: decimal band is +-5e-7')
    ok(within(0.0479 / 100, dec2['value'], 5e-07) and within(0.04793 / 100, dec2['value'], 5e-07), 'deposit 2: decimal band refuses 0.0479 or 0.04793 typed')
    ok(not within(0.048 / 100, dec2['value'], 5e-07) and not within(0.0491 / 100, dec2['value'], 5e-07), 'deposit 2: decimal band takes 0.048 or 0.0491 typed')
    ok('\\ln(e^{rt}) = rt' in L['p-monthly-deposit']['parts'][2]['question'], 'deposit 3: bridge sentence present')
    stated('deposit: ln(e^(rt)) = rt at r = 0.0479, t = 5', ev(sp.log(sp.exp(sp.Rational(479, 10000) * 5))), 0.2395, 1e-12)
    lr5 = 5 * rc
    num(L, 'p-monthly-deposit', 3, lr5, ln_b(float(g12) ** 5), {'quoted': 5 * 0.048, 'simple': 1.0491 ** 5 - 1, 'one-year': 0.0479}, asked=0.2395, extra_ok=(5 * 0.0479,))
    end = float(6000 * F(1004, 1000) ** 60)
    m = 6000.0
    for _ in range(60):
        m *= 1.004
    num(L, 'p-monthly-deposit', 4, end, m, {'one-plus': 6000 * 1.2395, 'quoted': 6000 * math.exp(0.24), 'simple-interest': 6000 * (1 + 5 * 0.048)},
        asked=7624, extra_ok=(6000 * math.exp(0.2395), 6000 * 1.2706))
    stated('deposit: e^0.2395 to 4 dp', round(math.exp(0.2395), 4), 1.2706)
    stated('deposit: 6000 e^0.2395 to 2 dp', round(6000 * math.exp(0.2395), 2), 7623.68)
    stated('deposit: 6000 * 1.004^60 to 2 dp', round(end, 2), 7623.84)


for f in (level1, level2, level3):
    f()

# every lesson of each level appears in at least one problem (by the skills and the ideas listed in the report)
for n, ids in ((1, 4), (2, 4), (3, 4)):
    items = load(n)
    ok(len(items) == ids, f'set {n}: {len(items)} items')
    ok(any(it['difficulty'] == 5 for it in items.values()), f'set {n}: no difficulty 5')
    parts = [p for it in items.values() for p in it['parts']]
    typed = [p for p in parts if p['widget']['kind'] in ('numeric', 'expression')]
    ok(3 * len(typed) >= 2 * len(parts), f'set {n}: typed parts {len(typed)} of {len(parts)}')
    for it in items.values():
        ok(3 <= len(it['parts']) <= 5, f'{it["id"]}: {len(it["parts"])} parts')

print(f'problem sets checked: [1, 2, 3]; checks: {checks}; failures: {len(fails)}')
for msg in fails:
    print('FAIL', msg)
sys.exit(1 if fails else 0)
