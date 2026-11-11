"""Recompute every number in app/content/courses/quadratics/problems-<n>.json twice.

Method 1 is exact: sympy (expand, factor, solve, completing the square) or fractions.
Method 2 is independent: the story worked piece by piece (row by row, plot by plot, can by
can), a search over whole numbers, a fine grid over the real line, or the value put back in.
For each numeric part the script checks that the two methods agree; that the JSON key lies
within its tol of the value; that the value at the rounding the question asks for is
accepted; that the number printed last in `feedback.correct` is accepted; that the `accept`
line's figure is accepted; that every `wrong` value matches its named slip, has a byKey line,
lies outside the key's band and does not overlap another `wrong`. Numeric sets check each
value, its rounding and each wrong set against the slip. Expression parts parse the key,
every accepted form and every wrong form from TeX with sympy and compare by simplification.
Choice parts check the keyed option and the arithmetic that decides it. Figures stated in
feedback and explanations are recomputed with `stated`. numbers_lib's Level.check_wrongs runs
over each set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-quadratics-numbers.py
"""
import json, os, re, sys, itertools, math
from fractions import Fraction as F
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, rationalize

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'quadratics')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0
x, t, n, p, v, k = sp.symbols('x t n p v k', real=True)
SYM = {'x': x, 't': t, 'n': n, 'p': p, 'v': v, 'k': k}
TR = standard_transformations + (implicit_multiplication_application, rationalize)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(nn):
    path = os.path.join(COURSE, f'problems-{nn}.json')
    return {it['id']: it for it in json.load(open(path))['items']}


def frac_to_div(s):
    while '\\frac' in s:
        i = s.index('\\frac')
        j = i + 5
        parts = []
        for _ in range(2):
            depth, kk = 0, j
            while True:
                if s[kk] == '{':
                    depth += 1
                elif s[kk] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                kk += 1
            parts.append(s[j + 1:kk])
            j = kk + 1
        s = s[:i] + '((' + parts[0] + ')/(' + parts[1] + '))' + s[j:]
    return s


def tex(s):
    s = frac_to_div(s.replace('\\tfrac', '\\frac').replace('\\dfrac', '\\frac'))
    s = s.replace('\\times', '*').replace('\\cdot', '*').replace('^', '**').replace('{', '(').replace('}', ')')
    return parse_expr(s, local_dict=SYM, transformations=TR)


def printed_value(text):
    s = text.replace('{,}', '').replace('−', '-')
    hits = list(re.finditer(r'(=|\\approx)\s*(-?\d+(?:\.\d+)?)', s))
    return float(hits[-1].group(2)) if hits else None


def num(items, iid, kk, exact, alt, slips=None, dp=None, agree=1e-9, printed=True):
    part = items[iid]['parts'][kk - 1]
    w = part['widget']
    tag = f'{iid} p{kk}'
    ok(w['kind'] == 'numeric' and 'answer' in w, f'{tag}: not a single numeric')
    e, a = float(exact), float(alt)
    ok(abs(e - a) <= agree * max(1, abs(e)), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    if dp is not None:
        rv = round(e, dp)
        ok(abs(rv - w['answer']) <= tol + 1e-9, f'{tag}: value at {dp} dp {rv} not accepted')
    if not float(w['answer']).is_integer():
        ok(re.search(r'decimal|places?|fraction|nearest', part['question'], re.I) is not None, f'{tag}: form not stated')
    if printed:
        pv = printed_value(part['feedback']['correct'])
        ok(pv is not None and abs(pv - w['answer']) <= tol + 1e-9, f'{tag}: printed {pv} not accepted by tol {tol}')
    lead = re.match(r'-?\d+(?:\.\d+)?$', w.get('accept', ''))
    ok(lead is not None and abs(float(lead.group()) - w['answer']) <= tol + 1e-9, f'{tag}: accept line {w.get("accept")} not a plain accepted number')
    slips = slips or {}
    wrongs = {z['id']: z for z in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    bykey = part['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        z = wrongs[wid]
        wt = z.get('tol', {'abs': 0})['abs']
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')
        ok(abs(z['value'] - float(val)) <= max(wt, 0.00005) + 1e-12, f'{tag}: wrong {wid} {z["value"]} vs slip {float(val)}')
        ok(abs(z['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {z["value"]} inside the key band')
        if dp is not None:
            ok(abs(round(float(val), dp) - z['value']) <= wt + 1e-9, f'{tag}: wrong {wid} at {dp} dp not inside its own band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A.get('tol', {'abs': 0})['abs'] + B.get('tol', {'abs': 0})['abs'], f'{tag}: wrongs {a_} and {b_} overlap')


def numset(items, iid, kk, exact_vals, alt_vals, slips, dp=None):
    part = items[iid]['parts'][kk - 1]
    w = part['widget']
    tag = f'{iid} p{kk}'
    ok(w['kind'] == 'numeric' and w.get('unordered') is True, f'{tag}: not an unordered set')
    tol = w['tol']['abs']
    ev = sorted(float(z) for z in exact_vals)
    av = sorted(float(z) for z in alt_vals)
    ok(len(ev) == len(av) and all(abs(a - b) <= 1e-6 for a, b in zip(ev, av)), f'{tag}: methods differ {ev} vs {av}')
    keys = sorted(w['answers'])
    ok(len(keys) == len(ev) and all(abs(a - b) <= tol + 1e-12 for a, b in zip(keys, ev)), f'{tag}: keys {keys} vs {ev}')
    if dp is not None:
        ok(all(abs(round(e, dp) - kv) <= tol + 1e-9 for e, kv in zip(ev, keys)), f'{tag}: {dp} dp values not accepted')
        ok(re.search(r'decimal|places?', part['question'], re.I) is not None, f'{tag}: form not stated')
    bykey = part['feedback'].get('byKey', {})
    ok('count' in bykey, f'{tag}: no count line')
    wrongs = {z['id']: z['value'] for z in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, vals in slips.items():
        got = sorted(float(s) for s in wrongs[wid].split(','))
        want = sorted(float(s) for s in vals)
        ok(all(abs(a - b) <= tol + 1e-9 for a, b in zip(got, want)), f'{tag}: wrong {wid} {got} vs slip {want}')
        ok(any(abs(a - b) > tol for a, b in zip(got, keys)), f'{tag}: wrong {wid} equals the key')
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')


def expr_part(items, iid, kk, truth, slips):
    part = items[iid]['parts'][kk - 1]
    w = part['widget']
    tag = f'{iid} p{kk}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    same = lambda a, b: sp.simplify(tex(a) - tex(b)) == 0
    for s in [w['answer']] + w.get('accept', []):
        ok(same(s, truth), f'{tag}: {s} differs from the worked answer {truth}')
        ok(not re.search(r'(?<!\\)\b(ln|log|exp|sin|cos|tan|sqrt)\(', s), f'{tag}: plain-text function name in {s}')
    bykey = part['feedback'].get('byKey', {})
    wrongs = {z['id']: z['tex'] for z in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, tt in wrongs.items():
        ok(not same(tt, truth), f'{tag}: wrong {wid} {tt} equals the key')
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')
        if wid in slips:
            ok(same(tt, slips[wid]), f'{tag}: wrong {wid} {tt} is not the slip {slips[wid]}')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        ok(not same(wrongs[a_], wrongs[b_]), f'{tag}: wrongs {a_} and {b_} are equal')
    if w.get('form'):
        ok('form' in bykey, f'{tag}: form set but no byKey form line')


def pick(items, iid, kk, correct_id):
    w = items[iid]['parts'][kk - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{kk}: keyed {keyed}, expected {correct_id}')
    ok(all(o.get('correct') or o.get('why') for o in w['options']), f'{iid} p{kk}: a distractor has no why')


def stated(label, shown, value, tol=1e-9):
    ok(abs(float(shown) - float(value)) <= tol, f'stated {label}: {shown} vs {float(value)}')


def grid(f, lo, hi, step):
    """real points on a fine grid where f holds (second method for inequalities)"""
    m = int(round((hi - lo) / step))
    return [lo + i * step for i in range(m + 1) if f(lo + i * step)]


def run_level(nn, fn):
    items = load(nn)
    fn(items)
    lv = Level('quadratics', nn)
    lv.check_wrongs(f'problems-{nn}')
    bad = [r for r in lv.results if not r[0]]
    ok(not bad, f'level {nn}: numbers_lib check_wrongs {len(bad)} bad')


# ================================================================== level 1
def level1(L):
    # cinema: (x+3)(x+8)
    block = sp.expand((x + 3) * (x + 8))
    ok(block == x**2 + 11*x + 24, 'cinema: expansion')
    ok(all(sum(1 for r in range(xx + 3) for s in range(xx + 8)) == block.subs(x, xx) for xx in range(1, 15)), 'cinema: seat count by rows')
    expr_part(L, 'p-cinema-block', 1, 'x^2+11x+24', {'corner': 'x^2+24', 'added': 'x^2+11x+11', 'swapped': 'x^2+24x+11'})
    new = block - 6
    ok(sp.factor(new) == (x + 2) * (x + 9), 'cinema: factor x^2+11x+18')
    pairs = [(a, 18 // a) for a in range(1, 19) if 18 % a == 0 and a <= 18 // a]
    ok([q for q in pairs if sum(q) == 11] == [(2, 9)], 'cinema: factor pair by search')
    expr_part(L, 'p-cinema-block', 2, '(x+2)(x+9)', {'sum-nine': '(x+3)(x+6)', 'one-eighteen': '(x+1)(x+18)', 'signs': '(x-2)(x-9)'})
    num(L, 'p-cinema-block', 3, ((x + 2) * (x + 9)).subs(x, 10), block.subs(x, 10) - 6,
        {'kept': 13 * 18, 'sum-nine': 13 * 16, 'one-eighteen': 11 * 28})
    stated('cinema: 12 x 19', 228, 12 * 19); stated('cinema: 100+110+24', 234, 100 + 110 + 24)
    pick(L, 'p-cinema-block', 4, 'no-middle')
    kk = sp.solve(sp.Eq(2 * k, 11), k)[0]
    ok(not kk.is_integer and kk == F(11, 2), 'cinema: 2k = 11 has k = 5.5')
    ok(not any(sp.expand((x + kw)**2 - (x**2 + 11*x)).coeff(x, 1) == 0 for kw in range(-30, 31)), 'cinema: no whole k makes the middle term 11x')
    ok(sp.expand((x + 4)**2) == x**2 + 8*x + 16 and sp.expand((x + 3)**2) == x**2 + 6*x + 9, 'cinema: distractor squares')
    ok(24 - 8 == 16 and 24 - 15 == 9, 'cinema: seats taken out in distractors')

    # allotment
    A = x**2 + 9*x + 20; B = 2*x**2 + 15*x + 28
    ok(sp.factor(A) == (x + 4) * (x + 5), 'allotment: factor A')
    expr_part(L, 'p-allotment-plots', 1, '(x+4)(x+5)', {'sum-twelve': '(x+2)(x+10)', 'sum-21': '(x+1)(x+20)'})
    ok(sp.expand(sp.factor(B) - (x + 4) * (2*x + 7)) == 0, 'allotment: factor B')
    ok([q for q in [(a, 56 // a) for a in range(1, 57) if 56 % a == 0] if sum(q) == 15] == [(7, 8), (8, 7)], 'allotment: split pair for ac = 56')
    expr_part(L, 'p-allotment-plots', 2, '(x+4)(2x+7)', {'no-group': '(x+7)(x+8)', 'wrong-pair': '(2x+4)(x+7)'})
    ok(sp.expand((2*x + 4) * (x + 7)) == 2*x**2 + 18*x + 28 and sp.expand((x + 7) * (x + 8)) == x**2 + 15*x + 56, 'allotment: slips expanded')
    total = sp.factor(A + B)
    ok(sp.simplify(total - 3 * (x + 4)**2) == 0, 'allotment: total factor')
    expr_part(L, 'p-allotment-plots', 3, '3(x+4)^2', {'both-sides': '6(x+4)^2', 'lost-square': '3(x+4)'})
    num(L, 'p-allotment-plots', 4, (3 * (x + 4)**2).subs(x, 6), A.subs(x, 6) + B.subs(x, 6),
        {'three-squared': (3 * 10)**2, 'both-sides': 6 * 100})
    stated('allotment: plot A at 6', 110, 10 * 11); stated('allotment: plot B at 6', 190, 10 * 19)

    # steel plates
    steel = (6*x)**2 - 3**2
    expr_part(L, 'p-steel-plates', 1, '36x^2-9', {'six': '6x^2-9', 'hole': '36x^2-3', 'both': '6x^2-3'})
    ok(sp.expand(sp.factor(steel) - 9 * (2*x + 1) * (2*x - 1)) == 0 and sp.factor_list(steel)[0] == 9 and len(sp.factor_list(steel)[1]) == 2, 'plates: factor fully')
    expr_part(L, 'p-steel-plates', 2, '9(2x+1)(2x-1)', {'inside': '9(2x+3)(2x-3)', 'square': '(6x-3)^2'})
    ok(sp.expand(9 * (2*x + 3) * (2*x - 3)) == 36*x**2 - 81 and sp.expand((6*x - 3)**2).coeff(x, 1) == -36, 'plates: slip claims')
    wide = sp.expand((6*x + 2)**2 - 9)
    ok(wide == 36*x**2 + 24*x - 5, 'plates: wider plate expanded')
    expr_part(L, 'p-steel-plates', 3, '36x^2+24x-5', {'each-term': '36x^2-5', 'one-strip': '36x^2+12x-5'})
    ok(sp.factor(wide) == (6*x - 1) * (6*x + 5), 'plates: factor wider')
    ok(sp.expand((6*x + 2 + 3) * (6*x + 2 - 3)) == wide, 'plates: difference of squares route')
    ok(30 * -6 == 36 * -5 and 30 - 6 == 24, 'plates: split numbers')
    ok(sp.expand((6*x - 5) * (6*x + 1)) == 36*x**2 - 24*x - 5, 'plates: signs slip expanded')
    expr_part(L, 'p-steel-plates', 4, '(6x+5)(6x-1)', {'signs': '(6x-5)(6x+1)'})
    num(L, 'p-steel-plates', 5, ((6*x + 5) * (6*x - 1)).subs(x, 5), 32 * 32 - 3 * 3,
        {'old': steel.subs(x, 5), 'each-term': 36 * 25 - 5, 'no-hole': 32**2, 'signs': 25 * 31})
    stated('plates: first plate at 5', 891, 9 * 11 * 9); stated('plates: 35 x 29', 1015, 35 * 29)


# ================================================================== level 2
def level2(L):
    h = 15 + 10*t - 5*t**2
    # q from completing the square, then from the maximum on a grid
    q = sp.expand(h + 5 * (t - 1)**2)
    ok(q.free_symbols == set(), 'stone: q is a number')
    hmax = max(float(h.subs(t, i / 1000)) for i in range(0, 3001))
    num(L, 'p-cliff-stone', 1, q, hmax, {'sign': 15 - 5, 'no-five': 15 + 1})
    roots = sp.solve(sp.Eq(h, 0), t)
    ok(sorted(roots) == [-1, 3], 'stone: sea roots')
    land = [i / 1000 for i in range(1, 5001) if abs(float(h.subs(t, i / 1000))) < 1e-9]
    num(L, 'p-cliff-stone', 2, max(roots), land[0],
        {'negative': -1, 'no-root': 1 + 4, 'carried': 1 + math.sqrt(2)})
    ok(sp.expand(5 * (t - 3) * (t + 1) - (5*t**2 - 10*t - 15)) == 0, 'stone: factorised check')
    top = sp.solve(sp.Eq(h, 15), t)
    numset(L, 'p-cliff-stone', 3, top, [z for z in range(-5, 6) if h.subs(t, z) == 15], {'sign': [0, -2]})
    e18 = sp.solve(sp.Eq(h, 18), t)
    g18 = [z for z in (1 - math.sqrt(0.4), 1 + math.sqrt(0.4))]
    ok(all(abs(float(h.subs(t, z)) - 18) < 1e-9 for z in g18), 'stone: 18 m roots put back')
    numset(L, 'p-cliff-stone', 4, [float(z) for z in e18], g18, {'no-root': [0.6, 1.4], 'times-five': [1 - math.sqrt(10), 1 + math.sqrt(10)]}, dp=2)
    stated('stone: sqrt 0.4', 0.632, math.sqrt(0.4), 5e-4)

    # bus
    gap = t**2 - (6*t - 10)
    disc = sp.discriminant(sp.expand(gap), t)
    num(L, 'p-bus-chase', 1, disc, (-6)**2 - 4 * 1 * 10, {'sign-b': -36 - 40, 'plus': 36 + 40, 'reversed': 40 - 36})
    ok(min(float(gap.subs(t, i / 100)) for i in range(0, 1001)) > 0, 'bus: gap never zero on a grid')
    qq = sp.expand(gap - (t - 3)**2)
    num(L, 'p-bus-chase', 2, qq, min(float(gap.subs(t, i / 1000)) for i in range(0, 10001)), {'start': 10, 'halved': 10 - 3, 'sign': 10 + 9}, agree=1e-6)
    sam = t**2 - 6*t + 7
    ok(sp.expand(sam - ((t - 3)**2 - 2)) == 0, 'bus: Sam square form')
    sr = sorted(sp.solve(sam, t))
    first = next(i / 100000 for i in range(0, 1000000) if float(sam.subs(t, i / 100000)) <= 0)
    num(L, 'p-bus-chase', 3, sr[0], first, {'larger': sr[1], 'half-root': 3 - math.sqrt(8), 'no-root': 3 - 2}, dp=2, agree=2e-5)
    stated('bus: 3 - 1.414', 1.586, 3 - 1.414); stated('bus: sqrt 2', 1.414, math.sqrt(2), 5e-4)
    vs = sp.solve(sp.Eq(sp.discriminant(t**2 - v*t + 10, t), 0), v)
    vmin = max(vs)
    slow = next(i / 100000 for i in range(600000, 700000) if (i / 100000)**2 - 40 >= 0)
    num(L, 'p-bus-chase', 4, vmin, slow, {'no-root': 40, 'no-four': math.sqrt(10)}, dp=2, agree=2e-5)
    stated('bus: extra speed', 0.32, float(vmin) - 6, 5e-3)

    # cans
    tri = n * (n + 1) / 2
    r120 = sp.solve(sp.Eq(tri, 120), n)
    num(L, 'p-can-stack', 1, max(r120), next(m for m in range(1, 100) if m * (m + 1) // 2 == 120), {'negative': -16, 'sign': 16})
    ok(sp.expand((n + 16) * (n - 15)) == n**2 + n - 240 and sp.expand((n - 16) * (n + 15)) == n**2 - n - 240, 'cans: factorisations')
    num(L, 'p-can-stack', 2, sp.discriminant(n**2 + n - 200, n), 1**2 - 4 * 1 * (-200), {'sign-c': 1 - 800, 'no-double': 1 + 400})
    ok(28**2 == 784 and 29**2 == 841 and math.isqrt(801)**2 != 801, 'cans: 801 not square')
    r100 = max(sp.solve(n**2 + n - 200, n))
    bis = next(i / 100000 for i in range(0, 3000000) if (i / 100000)**2 + i / 100000 - 200 >= 0)
    num(L, 'p-can-stack', 3, r100, bis, {'sign-b': (1 + math.sqrt(801)) / 2, 'no-half': -1 + math.sqrt(801), 'carried': (-1 + math.sqrt(401)) / 2}, dp=2, agree=2e-5)
    stated('cans: sqrt 801', 28.302, math.sqrt(801), 5e-4); stated('cans: 27.302 / 2', 13.651, 27.302 / 2)
    rows = math.floor(float(r100))
    used = sum(range(1, rows + 1))
    num(L, 'p-can-stack', 4, 100 - rows * (rows + 1) // 2, 100 - used, {'rounded-up': 14 * 15 // 2 - 100, 'rows': rows})
    stated('cans: 13 rows', 91, 13 * 14 / 2); stated('cans: 14 rows', 105, 14 * 15 / 2)


# ================================================================== level 3
def level3(L):
    y = -F(1, 5) * x * (x - 20)
    rts = sp.solve(y, x)
    ok(sorted(rts) == [0, 20], 'arch: roots')
    vx = -sp.Rational(4) / (2 * -sp.Rational(1, 5))   # -b/2a with y = -0.2x^2 + 4x
    num(L, 'p-canal-arch', 1, sum(rts) / 2, vx, {'root': 20, 'sign': -10})
    top = y.subs(x, 10)
    num(L, 'p-canal-arch', 2, top, max(float(y.subs(x, i / 100)) for i in range(0, 2001)), {'sign': -20, 'no-a': 100})
    expr_part(L, 'p-canal-arch', 3, '-0.2(x-10)^2+20', {'sign-h': '-0.2(x+10)^2+20', 'sign-a': '0.2(x-10)^2+20', 'no-a': '-(x-10)^2+20'})
    ok(sp.expand(-sp.Rational(1, 5) * (x - 10)**2 + 20 - y) == 0, 'arch: square form equals factorised form')
    ok((-(x - 10)**2 + 20).subs(x, 0) == -80, 'arch: no-a slip at the foot')
    band = sp.solve_univariate_inequality(y >= sp.Rational(64, 5), x, relational=False)
    width = band.sup - band.inf
    pts = grid(lambda z: -0.2 * z * (z - 20) >= 12.8 - 1e-9, 0, 20, 0.001)
    num(L, 'p-canal-arch', 4, width, pts[-1] - pts[0], {'half': 6, 'right-end': band.sup, 'left-end': band.inf}, agree=1e-6)
    stated('arch: 12.8 - 20', -7.2, 12.8 - 20); stated('arch: -7.2 / -0.2', 36, -7.2 / -0.2, 1e-9)

    # bikes
    R = p * (150 - 5*p)
    zero = sp.solve(150 - 5*p, p)[0]
    num(L, 'p-bike-hire', 1, zero, next(c for c in range(0, 200) if 150 - 5 * c == 0), {'no-divide': 150})
    best = sp.solve(sp.diff(R, p), p)[0]
    num(L, 'p-bike-hire', 2, best, max(range(0, 31), key=lambda c: c * (150 - 5 * c)), {'zero': 30})
    num(L, 'p-bike-hire', 3, R.subs(p, best), max(c * (150 - 5 * c) for c in range(0, 31)), {'bikes': 75, 'no-drop': 15 * 150})
    P = (p - 8) * (150 - 5*p)
    bp = sp.solve(sp.diff(P, p), p)[0]
    num(L, 'p-bike-hire', 4, bp, max(range(0, 31), key=lambda c: (c - 8) * (150 - 5 * c)), {'full-cost': 15 + 8, 'no-cost': 15, 'sign': (-8 + 30) / 2})
    ok(sp.expand(P - (605 - 5 * (p - 19)**2)) == 0 and P.subs(p, 19) == 605, 'bikes: square form of profit')
    pick(L, 'p-bike-hire', 5, 'inside')
    sol = sp.solve_univariate_inequality(P >= 525, p, relational=False)
    ok(sol == sp.Interval(15, 23), f'bikes: profit at least 525 is {sol}')
    ok(grid(lambda c: (c - 8) * (150 - 5 * c) >= 525 - 1e-9, 0, 40, 0.01)[0] == 15 and abs(grid(lambda c: (c - 8) * (150 - 5 * c) >= 525 - 1e-9, 0, 40, 0.01)[-1] - 23) < 1e-9, 'bikes: band on a grid')
    ok(19 - 16 == 3 and 19 + 16 == 35, 'bikes: no-root distractor ends')

    # sprinkler
    water = 3*x - sp.Rational(1, 2) * x**2
    bank = sp.Rational(1, 2) * x
    g = sp.expand(water - bank)
    expr_part(L, 'p-sprinkler-bank', 1, '2.5x-0.5x^2', {'added': '3.5x-0.5x^2', 'sign': '2.5x+0.5x^2'})
    meet = sp.solve(sp.Eq(water, bank), x)
    land = max(meet)
    num(L, 'p-sprinkler-bank', 2, land, next(i / 1000 for i in range(1, 10001) if abs(float(g.subs(x, i / 1000))) < 1e-12),
        {'flat': max(sp.solve(water, x)), 'vertex': sp.Rational(5, 2)})
    num(L, 'p-sprinkler-bank', 3, bank.subs(x, land), water.subs(x, land), {'flat': bank.subs(x, 6), 'square-half': 15 - (0.5 * 5)**2})
    gmax = g.subs(x, sp.solve(sp.diff(g, x), x)[0])
    num(L, 'p-sprinkler-bank', 4, gmax, max(float(g.subs(x, i / 1000)) for i in range(0, 5001)),
        {'water-top': water.subs(x, 3), 'no-square': 2.5 * 2.5, 'x-value': 2.5})
    stated('sprinkler: gap at 3', 3, water.subs(x, 3) - bank.subs(x, 3)); stated('sprinkler: bank at 3', 1.5, bank.subs(x, 3))
    stated('sprinkler: 6.25 - 3.125', 3.125, 6.25 - 3.125)


run_level(1, level1)
run_level(2, level2)
run_level(3, level3)
print(f'quadratics problem sets 1 to 3; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
