"""Recompute every number in app/content/courses/trig/problems-<n>.json twice.

Method 1 is exact: sympy, with surds, pi and the trig functions kept symbolic, then evaluated to 30 digits, or
exact fractions. Method 2 is a separate route: coordinates of the points worked out from the story and measured
with a distance or an atan2, the other rule (the sine rule against the right-angled route, the right-angled route
against the cosine rule), a scan of the model over a fine grid, or a bisection. Calculator values the questions
give (such as cos 55 = 0.5736) are used where the question tells the learner to use them, and the two routes are
then compared at that rounding.

For each numeric part the script checks that the two methods agree; that the key lies inside its band; that the
value at the rounding the question asks for is accepted, and so are the other sensible routes listed (a rounded
value carried from an earlier part); that the figure printed in feedback.correct appears there and is accepted;
that every wrong value is the value its named slip gives (computed here), has a byKey line, lies outside the key's
band and does not overlap another wrong. Expression parts: the key, each accept line and each wrong tex are turned
into sympy and compared with my own expression at sample points; each wrong must differ from the key. Set parts:
each value of the set computed twice, and each wrong set differs. Choice parts: one keyed option and the fact
behind it. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-trig-numbers.py
"""
import json, os, re, sys, math
from fractions import Fraction as F
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'trig')
fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    return {it['id']: it for it in json.load(open(p))['items']} if os.path.exists(p) else None


def within(v, key, tol):
    return abs(v - key) <= tol + 1e-12


def ev(e):
    return float(sp.N(e, 30))


DEG = sp.pi / 180
rad = lambda d: d * math.pi / 180
deg = lambda r: r * 180 / math.pi


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------- part checks
def num(items, iid, k, exact, alt, slips, asked=None, extra_ok=(), printed=None, agree=1e-9):
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
    if printed is not None:
        ok(printed in part['feedback']['correct'].replace('{,}', ''), f'{tag}: printed {printed} not in feedback')
        ok(within(float(printed), key, tol), f'{tag}: printed {printed} refused')
    wrong_checks(part, tag, slips, key, tol)
    ok('Any form' not in w.get('accept', ''), f'{tag}: accept promises a form')
    ok(re.search(r'decimal|place|fraction|whole number|nearest', part['question']) is not None, f'{tag}: question names no form')
    return e


def wrong_checks(part, tag, slips, key, tol):
    w = part['widget']
    ids = [x['id'] for x in w.get('wrong', [])]
    ok(set(ids) == set(slips), f'{tag}: wrong ids {ids} vs slips {list(slips)}')
    by = part['feedback'].get('byKey', {})
    for x in w.get('wrong', []):
        wt = x.get('tol', w['tol'])['abs']
        s = slips.get(x['id'])
        ok(s is not None and within(float(s), x['value'], wt), f'{tag}: wrong {x["id"]} = {x["value"]} vs slip {s} (tol {wt})')
        ok(abs(x['value'] - key) > tol + wt, f'{tag}: wrong {x["id"]} band meets the key band')
        ok(x['id'] in by, f'{tag}: wrong {x["id"]} has no byKey line')
        for y in w.get('wrong', []):
            if y is not x:
                yt = y.get('tol', w['tol'])['abs']
                ok(abs(x['value'] - y['value']) > wt + yt, f'{tag}: wrongs {x["id"]} and {y["id"]} overlap')


def num_set(items, iid, k, exact, alt, slips, asked=None):
    """exact, alt: lists of values by two routes. slips: {wrong id: list of values}. asked: the values at the rounding asked."""
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    tol = w['tol']['abs']
    keys = sorted(w['answers'])
    e, a = sorted(float(x) for x in exact), sorted(float(x) for x in alt)
    ok(len(e) == len(a) == len(keys), f'{tag}: counts {len(e)} {len(a)} {len(keys)}')
    for x, y, kv in zip(e, a, keys):
        ok(abs(x - y) <= 1e-7 * max(1, abs(x)), f'{tag}: methods differ {x} vs {y}')
        ok(within(x, kv, tol), f'{tag}: value {x} outside key {kv} +- {tol}')
    if asked:
        for x, kv in zip(sorted(asked), keys):
            ok(within(x, kv, tol), f'{tag}: asked rounding {x} refused')
    ids = [x['id'] for x in w.get('wrong', [])]
    ok(set(ids) == set(slips), f'{tag}: wrong ids {ids} vs slips {list(slips)}')
    by = part['feedback'].get('byKey', {})
    for x in w.get('wrong', []):
        vals = sorted(float(v) for v in str(x['value']).split(','))
        s = sorted(float(v) for v in slips[x['id']])
        wt = x.get('tol', {'abs': 1e-9})['abs']
        ok(len(vals) == len(s) and all(within(p, q, max(wt, 0.005)) for p, q in zip(vals, s)), f'{tag}: wrong set {x["id"]} {vals} vs slip {s}')
        ok(len(vals) != len(keys) or any(abs(p - q) > tol + wt for p, q in zip(vals, keys)), f'{tag}: wrong set {x["id"]} equals the key')
        ok(x['id'] in by, f'{tag}: wrong {x["id"]} has no byKey line')
    ok('count' in by, f'{tag}: no count line')


# ------------------------------------------------ TeX to sympy (only the shapes these sets use)
SYM = {c: sp.Symbol(c, positive=True) for c in 'sxtCAB'}


def tex2sp(tex):
    t = tex.replace('\\left', '').replace('\\right', '').replace('\\cdot', '*').replace('\\times', '*').replace(' ', '')
    for _ in range(6):
        t = re.sub(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
        t = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', t)
    t = t.replace('\\pi', 'pi').replace('^{', '**(').replace('{', '(').replace('}', ')').replace('^', '**')
    t = re.sub(r'\\(sin|cos|tan)([A-Za-z])', r'\1(\2)', t)
    t = re.sub(r'\\(sin|cos|tan)\(', r'\1(', t)
    t = re.sub(r'(\d|\))(sqrt|pi|sin|cos|[sxtCAB]\b|\()', r'\1*\2', t)
    t = re.sub(r'(pi)(\()', r'\1*\2', t)
    return sp.sympify(t, locals={**SYM, 'pi': sp.pi, 'sqrt': sp.sqrt, 'sin': sp.sin, 'cos': sp.cos})


def same(a, b, syms=()):
    pts = [0.37, 0.81, 1.3, 1.9, 2.6] if syms else [None]
    for p in pts:
        sub = {s: p for s in syms}
        if abs(complex(sp.N(a.subs(sub) - b.subs(sub), 20))) > 1e-9:
            return False
    return True


def rel(tex):
    """an equation 'L=R' as L-R"""
    l, r = tex.split('=')
    return tex2sp(l) - tex2sp(r)


def expr_part(items, iid, k, mine, slips, syms=(), equation=False):
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    conv = rel if equation else tex2sp
    if equation:
        def eqv(a, b):  # nonzero constant multiple
            for p in (0.37, 1.3, 2.6):
                pass
            q = sp.simplify(a / b)
            return q.is_number and q != 0
    else:
        eqv = lambda a, b: same(a, b, syms)
    ok(eqv(conv(w['answer']), mine), f'{tag}: answer {w["answer"]} is not mine')
    for a in w.get('accept', []):
        ok(eqv(conv(a), mine), f'{tag}: accept {a} is not mine')
    ids = [x['id'] for x in w.get('wrong', [])]
    ok(set(ids) == set(slips), f'{tag}: wrong ids {ids} vs slips {list(slips)}')
    by = part['feedback'].get('byKey', {})
    for x in w.get('wrong', []):
        got = conv(x['tex'])
        ok(eqv(got, slips[x['id']]), f'{tag}: wrong {x["id"]} {x["tex"]} is not its slip')
        ok(not eqv(got, mine), f'{tag}: wrong {x["id"]} equals the key')
        ok(x['id'] in by, f'{tag}: wrong {x["id"]} has no byKey line')


def expr_set(items, iid, k, mine, alt, slips):
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    got = sorted(ev(tex2sp(a)) for a in w['answers'])
    ok(all(abs(p - ev(q)) < 1e-12 for p, q in zip(got, sorted(mine, key=ev))), f'{tag}: answers {got} vs mine')
    ok(all(abs(p - q) < 1e-9 for p, q in zip(got, sorted(alt))), f'{tag}: answers {got} vs second route {alt}')
    by = part['feedback'].get('byKey', {})
    for x in w.get('wrong', []):
        vals = sorted(ev(tex2sp(v)) for v in x['tex'].split(','))
        ok(all(abs(p - q) < 1e-9 for p, q in zip(vals, sorted(slips[x['id']]))), f'{tag}: wrong set {x["id"]} {vals}')
        ok(vals != got, f'{tag}: wrong set {x["id"]} equals the key')
        ok(x['id'] in by, f'{tag}: wrong {x["id"]} has no byKey line')


def choice(items, iid, k, key_id, fact):
    part = items[iid]['parts'][k - 1]
    opts = part['widget']['options']
    keyed = [o['id'] for o in opts if o.get('correct')]
    ok(keyed == [key_id], f'{iid} p{k}: keyed {keyed}, wanted {key_id}')
    ok(all(o.get('correct') or o.get('why') for o in opts), f'{iid} p{k}: an option has no why')
    ok(bool(fact), f'{iid} p{k}: the fact behind the key fails')


def explain_len(items):
    for iid, it in items.items():
        for k, p in enumerate(it['parts'], 1):
            t = re.sub(r'\$[^$]*\$', 'M', p['explain']['text'])
            n = len([s for s in re.split(r'(?<=[.?])\s+', t) if s.strip()])
            ok(n <= 3, f'{iid} p{k}: explain has {n} sentences')


# ================================================================ LEVEL 1
L1 = load(1)
if L1:
    explain_len(L1)
    # ---- p-zip-wire: platforms at (0, 14) and (35, 2)
    S, E = (0.0, 14.0), (35.0, 2.0)
    wire_e = sp.sqrt(12**2 + 35**2)
    wire_a = math.dist(S, E)
    ok(wire_e == 37, 'zip: 12, 35, 37 is a Pythagorean triple')
    num(L1, 'p-zip-wire', 1, wire_e, wire_a,
        {'added': 12 + 35, 'used-14': math.hypot(14, 35), 'subtracted': math.sqrt(35**2 - 12**2)})
    th = math.atan2(S[1] - E[1], E[0] - S[0])  # second route: the angle from coordinates
    num(L1, 'p-zip-wire', 2, sp.Rational(12, 37), math.sin(th),
        {'tan': F(12, 35), 'cos': F(35, 37), 'flipped': F(37, 12)}, asked=0.324, extra_ok=(float(F(12, 37)),), printed='0.324')
    # rider 20 m along the wire: walk 20 m from S towards E
    ux, uy = (E[0] - S[0]) / wire_a, (E[1] - S[1]) / wire_a
    R = (S[0] + 20 * ux, S[1] + 20 * uy)
    drop_e = 20 * sp.Rational(12, 37)
    num(L1, 'p-zip-wire', 3, drop_e, S[1] - R[1],
        {'cos': 20 * F(35, 37), 'tan': 20 * F(12, 35), 'height': 14 - 20 * F(12, 37)},
        asked=6.49, extra_ok=(20 * 0.324,), printed='6.49')
    num(L1, 'p-zip-wire', 4, sp.sqrt(20**2 - drop_e**2), R[0] - S[0],
        {'subtracted': 20 - 6.49, 'added': math.sqrt(400 + 6.49**2)},
        asked=18.92, extra_ok=(math.sqrt(400 - 6.49**2), 20 * 35 / 37), printed='18.92', agree=1e-9)
    ok(abs(math.sqrt(400 - 6.49**2) - 18.92) < 0.005 and abs(400 - 6.49**2 - 357.88) < 0.005, 'zip p4: printed 357.88 and 18.92')

    # ---- p-hexagon-tile: corners at 10(cos 60k, sin 60k), A at k = 0 and going round
    P = [(10 * math.cos(rad(60 * k)), 10 * math.sin(rad(60 * k))) for k in range(6)]
    A, B, C, Dp = P[0], P[1], P[2], P[3]
    O = (0.0, 0.0)
    # height of triangle OAB: distance from A to the line OB
    hA = abs(B[0] * A[1] - B[1] * A[0]) / math.dist(O, B)
    s3 = sp.sqrt(3)
    expr_part(L1, 'p-hexagon-tile', 1, 5 * s3,
              {'added': sp.sqrt(125), 'whole-side': 10 * s3, 'half-square': 5 * sp.sqrt(2)})
    ok(abs(ev(5 * s3) - hA) < 1e-12 and abs(ev(sp.sqrt(10**2 - 5**2)) - hA) < 1e-12, 'hex p1: height by distance to OB and by Pythagoras')
    expr_part(L1, 'p-hexagon-tile', 2, 10 * s3, {'half': 5 * s3, 'side': sp.Integer(10), 'long': sp.Integer(20)})
    ok(abs(math.dist(A, C) - ev(10 * s3)) < 1e-12 and abs(math.dist(A, C) - 2 * hA) < 1e-12, 'hex p2: AC from coordinates')
    ok(abs(math.dist(A, Dp) - 20) < 1e-12 and abs(math.dist(C, Dp) - 10) < 1e-12, 'hex p3: AD = 20, CD = 10')
    num(L1, 'p-hexagon-tile', 3, (10 * s3)**2 + 10**2, math.dist(A, C)**2 + math.dist(C, Dp)**2,
        {'root-as-three': 10 * 3 + 100, 'root-left': 100 * math.sqrt(3) + 100, 'cd-unsquared': 300 + 10}, agree=1e-9)
    # angle CAD by vectors
    v1 = (C[0] - A[0], C[1] - A[1]); v2 = (Dp[0] - A[0], Dp[1] - A[1])
    cad = deg(math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))))
    num(L1, 'p-hexagon-tile', 4, sp.asin(sp.Rational(1, 2)) / DEG, cad,
        {'angle-d': 60, 'tan': deg(math.atan(10 / 20)), 'radians': math.asin(0.5)}, extra_ok=(), agree=1e-9)

    # ---- p-lake-markers: P at the origin, A along the axis, B at 55 degrees
    Pp, Ap, Bp = (0.0, 0.0), (60.0, 0.0), (45 * math.cos(rad(55)), 45 * math.sin(rad(55)))
    choice(L1, 'p-lake-markers', 1, 'cosine', True)
    ab_given = math.sqrt(60**2 + 45**2 - 2 * 60 * 45 * 0.5736)
    ab_exact = sp.sqrt(60**2 + 45**2 - 2 * 60 * 45 * sp.cos(55 * DEG))
    num(L1, 'p-lake-markers', 2, ab_exact, math.dist(Ap, Bp),
        {'no-root': 5625 - 2 * 60 * 45 * 0.5736, 'plus': math.sqrt(5625 + 2 * 60 * 45 * 0.5736), 'pythagoras': 75},
        asked=50.27, extra_ok=(ab_given, 50.28), printed='50.27')
    ok(abs(2 * 60 * 45 * 0.5736 - 3097.44) < 1e-9 and abs(5625 - 3097.44 - 2527.56) < 1e-9, 'lake p2: printed working')
    sinA = 45 * 0.8192 / 50.27
    A_exact = sp.asin(45 * sp.sin(55 * DEG) / ab_exact) / DEG
    A_alt = deg(math.atan2(Bp[1], Bp[0] - 60) * -1 + math.pi) if False else deg(math.acos(((Pp[0] - Ap[0]) * (Bp[0] - Ap[0]) + (Pp[1] - Ap[1]) * (Bp[1] - Ap[1])) / (60 * math.dist(Ap, Bp))))
    num(L1, 'p-lake-markers', 3, A_exact, A_alt,
        {'wrong-side': deg(math.asin(60 * 0.8192 / 50.27)), 'ratio': sinA, 'radians': math.asin(sinA)},
        asked=47.2, extra_ok=(deg(math.asin(sinA)), 47.1, deg(math.asin(45 * 0.8192 / 50.28))), agree=1e-9)
    ok(abs(sinA - 0.7333) < 0.00005, 'lake p3: printed 0.7333')
    # shortest path: distance from P to line AB, by the cross product
    dist_e = 60 * sp.sin(A_exact * DEG)
    cross = abs((Bp[0] - Ap[0]) * (Pp[1] - Ap[1]) - (Bp[1] - Ap[1]) * (Pp[0] - Ap[0])) / math.dist(Ap, Bp)
    num(L1, 'p-lake-markers', 4, dist_e, cross,
        {'cos': 60 * math.cos(rad(47.2)), 'used-45': 45 * math.sin(rad(47.2)), 'tan': 60 * math.tan(rad(47.2))},
        asked=44.0, extra_ok=(60 * math.sin(rad(47.2)), 60 * math.sin(rad(47.1)), 45 * math.sin(rad(77.8))), printed='44.0', agree=1e-9)

    # ---- p-desk-lamp: O at the origin, A at 40 along 60 degrees, B at 30 along -30 degrees from A
    Ao = (40 * math.cos(rad(60)), 40 * math.sin(rad(60)))
    Bo = (Ao[0] + 30 * math.cos(rad(-30)), Ao[1] + 30 * math.sin(rad(-30)))
    expr_part(L1, 'p-desk-lamp', 1, 20 * s3, {'sin-30': sp.Integer(20), 'no-half': 40 * s3, 'half-square': 20 * sp.sqrt(2)})
    ok(abs(ev(40 * sp.sin(60 * DEG)) - Ao[1]) < 1e-12 and abs(ev(20 * s3) - Ao[1]) < 1e-12, 'lamp p1: elevation two ways')
    num(L1, 'p-desk-lamp', 2, sp.sqrt(40**2 + 30**2), math.dist((0, 0), Bo), {'added': 70, 'subtracted': math.sqrt(40**2 - 30**2)})
    aob = sp.atan(sp.Rational(30, 40)) / DEG
    aob_alt = deg(math.atan2(Ao[1], Ao[0]) - math.atan2(Bo[1], Bo[0]))
    num(L1, 'p-desk-lamp', 3, aob, aob_alt,
        {'flipped': deg(math.atan(40 / 30)), 'sine': deg(math.asin(30 / 40)), 'radians': math.atan(0.75)}, asked=36.9, agree=1e-9)
    hb = 50 * sp.sin((60 - aob) * DEG)
    num(L1, 'p-desk-lamp', 4, hb, Bo[1],
        {'angle-aob': 50 * math.sin(rad(36.9)), 'sixty': 50 * math.sin(rad(60)), 'cos': 50 * math.cos(rad(23.1)), 'added': 50 * math.sin(rad(96.9))},
        asked=19.6, extra_ok=(50 * math.sin(rad(23.1)), ev(20 * s3 - 15)), printed='19.6', agree=1e-9)
    expr_part(L1, 'p-desk-lamp', 5, 20 * s3 - 15,
              {'above': 20 * s3 + 15, 'cos-30': 5 * s3, 'whole-arm': 20 * s3 - 30})
    ok(abs(ev(20 * s3 - 15) - Bo[1]) < 1e-12, 'lamp p5: exact height equals the coordinate route')


# ================================================================ report
print(f'numbers: {checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
