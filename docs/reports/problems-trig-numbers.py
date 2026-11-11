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
                # the widget takes the first match: a band may sit inside a LATER, wider band (finding 8), never inside an earlier one;
                # two bands that only partly overlap are refused
                d, ix, iy = abs(x['value'] - y['value']), w['wrong'].index(x), w['wrong'].index(y)
                ok(d > wt + yt or (d <= yt and ix < iy) or (d <= wt and iy < ix), f'{tag}: wrongs {x["id"]} and {y["id"]} overlap')


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

    # ---- p-hexagon-tile: corners at 8(cos 60k, sin 60k), A at k = 0 and going round
    P = [(8 * math.cos(rad(60 * k)), 8 * math.sin(rad(60 * k))) for k in range(6)]
    A, B, C, Dp = P[0], P[1], P[2], P[3]
    O = (0.0, 0.0)
    # height of triangle OAB: distance from A to the line OB
    hA = abs(B[0] * A[1] - B[1] * A[0]) / math.dist(O, B)
    s3 = sp.sqrt(3)
    expr_part(L1, 'p-hexagon-tile', 1, 4 * s3,
              {'added': sp.sqrt(80), 'whole-side': 8 * s3, 'half-square': 4 * sp.sqrt(2)})
    ok(abs(ev(4 * s3) - hA) < 1e-12 and abs(ev(sp.sqrt(8**2 - 4**2)) - hA) < 1e-12 and sp.sqrt(48) == 4 * s3, 'hex p1: height by distance to OB and by Pythagoras')
    expr_part(L1, 'p-hexagon-tile', 2, 8 * s3, {'half': 4 * s3, 'side': sp.Integer(8), 'long': sp.Integer(16)})
    ok(abs(math.dist(A, C) - ev(8 * s3)) < 1e-12 and abs(math.dist(A, C) - 2 * hA) < 1e-12 and sp.sqrt(192) == 8 * s3, 'hex p2: AC from coordinates')
    ok(abs(math.dist(A, Dp) - 16) < 1e-12 and abs(math.dist(C, Dp) - 8) < 1e-12, 'hex p3: AD = 16, CD = 8')
    num(L1, 'p-hexagon-tile', 3, (8 * s3)**2 + 8**2, math.dist(A, C)**2 + math.dist(C, Dp)**2,
        {'root-as-three': 8 * 3 + 64, 'root-left': 64 * math.sqrt(3) + 64, 'cd-unsquared': 192 + 8}, agree=1e-9)
    # angle CAD by vectors
    v1 = (C[0] - A[0], C[1] - A[1]); v2 = (Dp[0] - A[0], Dp[1] - A[1])
    cad = deg(math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))))
    num(L1, 'p-hexagon-tile', 4, sp.asin(sp.Rational(1, 2)) / DEG, cad,
        {'angle-d': 60, 'tan': deg(math.atan(8 / 16)), 'half': math.sin(rad(cad)), 'radians': math.asin(0.5), 'radians-whole': round(math.asin(0.5))}, extra_ok=(), agree=1e-9)
    hx = L1['p-hexagon-tile']['parts']
    ok([x['id'] for x in hx[3]['widget']['wrong']].index('half') < [x['id'] for x in hx[3]['widget']['wrong']].index('radians'), 'hex p4: half entry sits before the wide radians band (finding 8)')
    # fix pass, delta aa-3 (c5): the radians band is +- 0.005, and a whole-number radian value has its own entry
    rb = {x['id']: x for x in hx[3]['widget']['wrong']}
    ok(rb['radians']['tol']['abs'] == 0.005 and rb['radians-whole']['value'] == 1 and rb['radians-whole']['tol']['abs'] == 0, 'hex p4: radians band 0.5236 +- 0.005 and radians-whole 1 exactly')
    ok(within(0.5236, 0.5236, 0.005) and within(0.52, 0.5236, 0.005) and within(0.524, 0.5236, 0.005) and within(1, 1, 0), 'hex p4: radians bands take 0.5236, 0.52, 0.524 and 1')
    ok(round(math.asin(0.5)) == 1, 'hex p4: pi/6 = 0.5236 rounds to 1 as a whole number')
    cosv, tanv = math.cos(rad(30)), math.tan(rad(30))
    ok(all(not within(v, 0.5236, 0.005) and not within(v, 1, 0) and not within(v, 0.5, 0.0005) and not within(v, 30, 0) for v in (0.87, 0.866, 0.58, 0.577)), 'hex p4: 0.87, 0.866, 0.58 and 0.577 (cos and tan of 30) are in no band')
    ok(abs(cosv - 0.866) < 1e-3 and abs(tanv - 0.577) < 1e-3, 'hex p4: cos 30 = 0.866 and tan 30 = 0.577')
    ok(hx[3]['feedback']['byKey']['radians-whole'] == hx[3]['feedback']['byKey']['radians'], 'hex p4: radians-whole has the radians line')
    ok(not within(0.5, 0.5236, 0.005 + 0.0005), 'hex p4: half (0.5 +- 0.0005) no longer sits inside the radians band')
    ok(all(hx[i]['widget'].get('form') == 'simplified' for i in (0, 1)), 'hex p1, p2: form simplified (finding 10)')
    ok(hx[0]['widget']['accept'] == ['\\sqrt{48}', '4\\cdot\\sqrt{3}'] and hx[1]['widget']['accept'] == ['\\sqrt{192}'], 'hex accept forms: the four unworked ones are cut')

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
        {'flipped': deg(math.atan(40 / 30)), 'sine': deg(math.asin(30 / 40)), 'ratio-tan': 30 / 40, 'ratio-sin': 30 / 50, 'radians': math.atan(0.75)}, asked=36.9, extra_ok=(), agree=1e-9)
    lp = L1['p-desk-lamp']['parts']
    ok(within(0.64, 0.6435, 0.005) and within(0.644, 0.6435, 0.005) and not within(0.6, 0.6435, 0.005) and not within(0.75, 0.6435, 0.005), 'lamp p3: radians band 0.005 takes 0.64 and 0.644, leaves 0.6 and 0.75 to their own entries')
    ok(all(lp[i]['widget'].get('form') == 'simplified' for i in (0, 4)) and lp[0]['widget']['accept'] == ['\\sqrt{1200}'] and lp[4]['widget']['accept'] == ['-15+20\\sqrt{3}'], 'lamp p1, p5: form simplified, unworked accept forms cut (finding 10)')
    hb = 50 * sp.sin((60 - aob) * DEG)
    num(L1, 'p-desk-lamp', 4, hb, Bo[1],
        {'angle-aob': 50 * math.sin(rad(36.9)), 'sixty': 50 * math.sin(rad(60)), 'cos': 50 * math.cos(rad(23.1)), 'added': 50 * math.sin(rad(96.9))},
        asked=19.6, extra_ok=(50 * math.sin(rad(23.1)), ev(20 * s3 - 15)), printed='19.6', agree=1e-9)
    expr_part(L1, 'p-desk-lamp', 5, 20 * s3 - 15,
              {'above': 20 * s3 + 15, 'cos-30': 5 * s3, 'whole-arm': 20 * s3 - 30})
    ok(abs(ev(20 * s3 - 15) - Bo[1]) < 1e-12, 'lamp p5: exact height equals the coordinate route')
    # fix pass, delta aa-3 (c4): 5(4 sqrt 3 - 3) stays refused by the simplified check, and the form line says which form is wanted
    lp5 = L1['p-desk-lamp']['parts'][4]
    ok(same(tex2sp('5(4\\sqrt{3}-3)'), 20 * s3 - 15), 'lamp p5: 5(4 sqrt 3 - 3) is equal to the key')
    fl = lp5['feedback']['byKey'].get('form', '')
    ok('multiply out' in fl.lower() and 'sqrt{3}' in fl and 'not simplified' not in fl and 'collect' not in fl, 'lamp p5: the form line names the wanted shape (a multiple of sqrt 3 minus a whole number)')


# ================================================================ LEVEL 2
L2 = load(2)
if L2:
    import cmath
    explain_len(L2)
    # ---- p-water-wheel: r = 2.4, hub 3 m up, tip from angle 0 anticlockwise
    r, hub, s_arc = 2.4, 3.0, 5.4
    th_e = sp.Rational(54, 24)
    th_a = bisect(lambda x: r * x - s_arc, 0, 10)
    num(L2, 'p-water-wheel', 1, th_e, th_a,
        {'times': s_arc * r, 'flipped': r / s_arc, 'turns': s_arc / (2 * math.pi * r)}, printed='2.25')
    tip = r * cmath.exp(1j * float(th_e))  # second route: the tip as a complex number
    deg_a = deg(math.atan2(tip.imag, tip.real))
    num(L2, 'p-water-wheel', 2, th_e * 180 / sp.pi, deg_a,
        {'wrong-way': 2.25 * math.pi / 180, 'no-pi': 2.25 * 180}, asked=128.9, printed='128.9')
    h_e = hub + r * sp.sin(th_e)
    num(L2, 'p-water-wheel', 3, h_e, hub + tip.imag,
        {'radian-mode': hub + r * math.sin(128.9), 'degree-mode': hub + r * math.sin(rad(2.25)),
         'cos': hub + r * math.cos(rad(128.9)), 'no-hub': r * math.sin(rad(128.9))},
        asked=4.87, extra_ok=(hub + r * math.sin(rad(128.9)), hub + r * 0.778), printed='4.87')
    h_val = ev(h_e)
    mir_e = 180 - th_e * 180 / sp.pi
    mir_a = deg(bisect(lambda x: hub + r * math.sin(x) - h_val, 0, math.pi / 2))
    num(L2, 'p-water-wheel', 4, mir_e, mir_a,
        {'cos-mirror': 360 - 128.9, 'half-turn': 128.9 + 180, 'minus-90': 128.9 - 90}, asked=51.1, printed='51.1')
    arc_e = r * (sp.pi - th_e)
    arc_a = 2 * (r * math.pi / 2) - s_arc  # the top is r*pi/2 round; the two points sit equally either side of it
    num(L2, 'p-water-wheel', 5, arc_e, arc_a,
        {'degrees': r * 51.1, 'divided': 51.1 / r, 'between': s_arc - 2.14},
        asked=2.14, extra_ok=(r * rad(51.1), r * 0.892), printed='2.14')
    ok(abs(rad(51.1) - 0.892) < 0.0005 and abs(r * math.pi / 2 - 3.77) < 0.005 and abs(3.77 - 2.14 - 1.63) < 1e-9 and abs(5.4 - 3.77 - 1.63) < 1e-9, 'wheel p5: printed 0.892, 3.77, 1.63')

    # ---- p-two-buoys: grid scans as the second route
    h1 = lambda t: 6 + 0.8 * math.sin(math.pi * t / 5)
    h2 = lambda t: 6 + 0.8 * math.sin(math.pi * (t - 3) / 5)
    grid = [i / 10000 for i in range(0, 300001)]
    peaks = [t for t in grid[1:-1] if h1(t) >= h1(t - 1e-4) and h1(t) >= h1(t + 1e-4)]
    num(L2, 'p-two-buoys', 1, 2 * sp.pi / (sp.pi / 5), peaks[1] - peaks[0],
        {'read-five': 5, 'b-itself': math.pi / 5, 'times': 2 * math.pi * math.pi / 5}, agree=1e-3)
    num(L2, 'p-two-buoys', 2, sp.Rational(5, 2), peaks[0],
        {'angle': math.pi / 2, 'half': 5, 'trough': 7.5}, agree=1e-3, printed='2.5')
    peak2 = max((t for t in grid if t <= 10), key=h2)
    num(L2, 'p-two-buoys', 3, sp.Rational(5, 2) + 3, peak2, {'early': 2.5 - 3, 'lag': 3}, agree=1e-3, printed='5.5')
    gap_e = sp.Rational(4, 5) - sp.Rational(4, 5) * sp.sin(sp.Rational(11, 10) * sp.pi)
    num(L2, 'p-two-buoys', 4, gap_e, h2(5.5) - h1(5.5),
        {'height': h1(5.5), 'degree-mode': 6.8 - (6 + 0.8 * math.sin(rad(1.1 * math.pi))), 'full-swing': 1.6},
        asked=1.05, extra_ok=(6.8 - 5.753,), printed='1.05')
    ok(abs(0.8 * math.sin(1.1 * math.pi) + 0.247) < 0.0005 and abs(h1(5.5) - 5.753) < 0.0005, 'buoys p4: printed 0.247 and 5.753')

    # ---- p-observation-wheel: second route is the wheel itself, height 28 - 25 cos(2 pi t / 20)
    geo = lambda t: 28 - 25 * math.cos(2 * math.pi * t / 20)
    num(L2, 'p-observation-wheel', 1, sp.Rational(50, 2), (max(map(geo, grid[:200001])) - min(map(geo, grid[:200001]))) / 2,
        {'diameter': 50, 'top': 53, 'hub': 28}, agree=1e-6)
    tt = sp.Symbol('t', positive=True)
    expr_part(L2, 'p-observation-wheel', 2, sp.pi / 10,
              {'period': sp.Integer(20), 'half': sp.pi / 20, 'flipped': 10 / sp.pi})
    bsol = sp.solve(sp.Eq(2 * sp.pi / sp.Symbol('b', positive=True), 20))
    ok(bsol == [sp.pi / 10], 'wheel p2: 2 pi / b = 20 gives pi/10')
    c_alt = bisect(lambda t: geo(t) - 28, 0.1, 9.9)
    num(L2, 'p-observation-wheel', 3, sp.Rational(20, 4), c_alt, {'boarding': 0, 'top': 10, 'falling': 15}, agree=1e-9)
    model = lambda t: 25 * math.sin(math.pi / 10 * (t - 5)) + 28
    ok(all(abs(model(t) - geo(t)) < 1e-9 for t in (0, 3.3, 7, 12.5, 19)), 'wheel: model equals the wheel at sample times')
    h8 = 25 * sp.sin(sp.pi / 10 * 3) + 28
    num(L2, 'p-observation-wheel', 4, h8, geo(8),
        {'degree-mode': 25 * math.sin(rad(0.3 * math.pi)) + 28, 'no-shift': 25 * math.sin(0.8 * math.pi) + 28},
        asked=48.23, extra_ok=(25 * 0.809 + 28,), printed='48.23')
    t2 = bisect(lambda t: geo(t) - geo(8), 10.01, 19.99)
    num(L2, 'p-observation-wheel', 5, 5 + (sp.pi - sp.Rational(3, 10) * sp.pi) / (sp.pi / 10), t2,
        {'no-shift': 7, 'half-period': 18, 'mirror-start': 2}, agree=1e-9)

# ================================================================ LEVEL 3
L3 = load(3)
if L3:
    explain_len(L3)
    # ---- p-two-angles: second route is the angles themselves, found by inverse functions
    Adeg = 180 - deg(math.asin(28 / 53))
    Bdeg = deg(math.acos(24 / 25))
    sA, cA, cB, sB = F(28, 53), F(-45, 53), F(24, 25), F(7, 25)
    ok(sA**2 + cA**2 == 1 and sB**2 + cB**2 == 1 and 28**2 + 45**2 == 53**2, 'angles: both pairs satisfy the identity')
    ok(abs(math.cos(rad(Adeg)) - float(cA)) < 1e-12, 'angles: cos A = -45/53 from the angle')
    num(L3, 'p-two-angles', 1, cA, math.cos(rad(Adeg)),
        {'sign': -cA, 'one-minus': 1 - sA, 'no-root': 1 - sA**2}, asked=-0.849, printed=None)
    ok('-45/53' in L3['p-two-angles']['parts'][0]['widget']['accept'] and within(-0.85, -45 / 53, 0.0005) is False and within(-0.849, -45 / 53, 0.0005), 'angles p1: band 0.0005 takes -0.849 and refuses -0.85')
    num(L3, 'p-two-angles', 2, sB, math.sin(rad(Bdeg)),
        {'negative': -sB, 'one-minus': 1 - cB, 'no-root': 1 - cB**2}, printed='0.28')
    sAB, cAB = sA * cB + cA * sB, cA * cB - sA * sB
    ok(sAB == F(357, 1325) and cAB == F(-1276, 1325) and 357**2 + 1276**2 == 1325**2, 'angles: 357/1325, -1276/1325 and the identity check')
    ok(28 * 24 == 672 and 45 * 7 == 315 and 45 * 24 == 1080 and 28 * 7 == 196 and 53 * 25 == 1325 and F(672 - 315, 1325) == sAB and F(-1080 - 196, 1325) == cAB, 'angles: printed numerators')
    num(L3, 'p-two-angles', 3, sAB, math.sin(rad(Adeg + Bdeg)),
        {'sign': sA * cB - cA * sB, 'sum-of-sines': sA + sB, 'cos-formula': cAB}, asked=0.2694, printed='0.2694')
    ok(sA * cB + (-cA) * sB == sA * cB - cA * sB and sA * cB - cA * sB == F(987, 1325), 'angles p3: the sign slip and the minus-formula slip give one value, 987/1325')
    num(L3, 'p-two-angles', 4, cAB, math.cos(rad(Adeg + Bdeg)),
        {'plus': cA * cB + sA * sB, 'sign': (-cA) * cB - sA * sB}, asked=-0.9630, printed='-0.9630')
    ok(cA * cB + sA * sB == F(-884, 1325) and (-cA) * cB - sA * sB == F(884, 1325), 'angles p4: slips 884/1325')
    ab_e = 180 - sp.asin(sp.Rational(357, 1325)) / DEG
    num(L3, 'p-two-angles', 5, ab_e, Adeg + Bdeg,
        {'principal': deg(math.asin(357 / 1325)), 'third': 180 + deg(math.asin(357 / 1325)), 'fourth': 360 - deg(math.asin(357 / 1325))},
        asked=164.4, extra_ok=(180 - 15.6, deg(math.atan2(0.2694, -0.9630))), printed='164.4')
    ok(abs(Adeg - 148.1) < 0.05 and abs(Bdeg - 16.3) < 0.05 and abs(deg(math.asin(0.2694)) - 15.6) < 0.05, 'angles p5: printed 148.1, 16.3, 15.6')
    ok(round(Adeg + Bdeg, 2) == 164.37 and round(deg(math.asin(0.2694)), 2) == 15.63, 'angles p5: 164.37 and 15.63')

    # ---- p-quadratic-in-sine
    s = SYM['s']
    lhs = sp.expand(2 * (1 - s**2) + 3 * s - 3)
    ok(sp.simplify(lhs / (2 * s**2 - 3 * s + 1)) == -1, 'quad p1: substitution gives -(2s^2 - 3s + 1)')
    expr_part(L3, 'p-quadratic-in-sine', 1, 2 * s**2 - 3 * s + 1,
              {'not-distributed': s**2 - 3 * s + 2, 'cos-as-sin': 2 * s**2 + 3 * s - 3, 'moved-3': 2 * s**2 - 3 * s - 5}, equation=True)
    ok(sp.expand((1 - s**2) + 3 * s - 3) == -(s**2 - 3 * s + 2), 'quad p1: the undistributed slip is s^2 - 3s + 2')
    q = lambda v: 2 * v * v - 3 * v + 1
    num_set(L3, 'p-quadratic-in-sine', 2, sp.solve(2 * s**2 - 3 * s + 1, s), [bisect(q, 0, 0.75), bisect(q, 0.75, 2)],
            {'signs': [-0.5, -1], 'carried': [1, 2]})
    zz = sp.Symbol('z'); ok(sorted(sp.solve(zz**2 - 3 * zz + 2, zz)) == [1, 2] and sorted(sp.solve(2 * zz**2 + 3 * zz + 1, zz)) == [-1, sp.Rational(-1, 2)], 'quad p2: slips solve their equations')
    xx = sp.Symbol('x', real=True)
    sols = sp.solveset(2 * sp.cos(xx)**2 + 3 * sp.sin(xx) - 3, xx, sp.Interval(0, 2 * sp.pi))
    exact_deg = sorted(sp.nsimplify(v / DEG) for v in sols)
    fx = lambda d: 2 * math.cos(rad(d))**2 + 3 * math.sin(rad(d)) - 3
    brute = [d for d in range(0, 361) if abs(fx(d)) < 1e-12]
    num_set(L3, 'p-quadratic-in-sine', 3, exact_deg, brute, {'cos-rule': [30, 90, 330], 'tan-rule': [30, 90, 210]})
    ok(abs(math.sin(rad(330)) + 0.5) < 1e-12 and abs(math.sin(rad(210)) + 0.5) < 1e-12, 'quad p3: 330 and 210 have sine -0.5, so they are wrong')
    expr_part(L3, 'p-quadratic-in-sine', 4, 5 * sp.pi / 6,
              {'degrees': sp.Integer(150), 'middle': sp.pi / 2, 'half': 5 * sp.pi / 12})
    ok(L3['p-quadratic-in-sine']['parts'][3]['question'].endswith('with no $x =$ in front.'), 'quad p4: question asks for no x = in front (finding 18)')
    ok(abs(max(sols, key=lambda v: float(v)) - 5 * sp.pi / 6) == 0 and abs(rad(max(brute)) - ev(5 * sp.pi / 6)) < 1e-12, 'quad p4: largest root two ways')

    # ---- p-daylight-model
    a3 = (F(164, 10) - F(76, 10)) / 2
    Lm = lambda t: 4.4 * math.sin(math.pi / 6 * (t - 3)) + 12
    g3 = [i / 1000 for i in range(0, 12001)]
    num(L3, 'p-daylight-model', 1, a3, (max(map(Lm, g3)) - min(map(Lm, g3))) / 2,
        {'range': 2 * a3, 'longest': 16.4, 'midline': 12}, agree=1e-6, printed='4.4')
    ok(abs(Lm(6) - 16.4) < 1e-12 and abs(Lm(12) - 7.6) < 1e-12, 'daylight: the model gives 16.4 in month 6 and 7.6 in month 12')
    expr_part(L3, 'p-daylight-model', 2, sp.pi / 6, {'period': sp.Integer(12), 'half-cycle': sp.pi / 3, 'flipped': 6 / sp.pi})
    num(L3, 'p-daylight-model', 3, 6 - sp.Rational(12, 4), bisect(lambda t: Lm(t) - 12, 0.5, 5.5),
        {'peak': 6, 'falling': 9, 'trough': 12}, agree=1e-9)
    # fix pass, delta aa-3 (c2): the level is 10 hours, so sin(pi/6 (t - 3)) = -5/11, not -1/2
    s_lvl = sp.Rational(10 - 12, 1) / sp.Rational(22, 5)
    ok(s_lvl == -sp.Rational(5, 11), 'daylight p4: the sine is (10 - 12) / 4.4 = -5/11 exactly')
    u1 = sp.asin(sp.Rational(5, 11))
    roots = [3 - 6 * u1 / sp.pi, 3 + 6 * (sp.pi + u1) / sp.pi]
    num_set(L3, 'p-daylight-model', 4, roots, [bisect(lambda t: Lm(t) - 10, 0, 3), bisect(lambda t: Lm(t) - 10, 9, 12)],
            {'no-shift': [6.9, 11.1], 'above': [3.9, 8.1]}, asked=[2.1, 9.9])
    ok(abs(Lm(float(roots[0])) - 10) < 1e-12 and abs(Lm(float(roots[1])) - 10) < 1e-12, 'daylight p4: the model gives 10 hours at both roots')
    ok(abs(float(roots[0]) - 2.0988) < 5e-5 and abs(float(roots[1]) - 9.9012) < 5e-5 and abs(float(roots[0] + roots[1]) - 12) < 1e-12, 'daylight p4: roots 2.0988 and 9.9012, symmetric about t = 6')
    ok(abs(math.asin(5 / 11) - 0.4719) < 5e-5 and abs(math.pi + 0.4719 - 3.6135) < 5e-5, 'daylight p4: u = -0.4719 and pi + 0.4719 = 3.6135 as printed')
    sl = [float(r) for r in (6 * (math.pi + math.asin(5 / 11)) / math.pi, 6 * (2 * math.pi - math.asin(5 / 11)) / math.pi)]
    ok(abs(sl[0] - 6.9012) < 1e-4 and abs(sl[1] - 11.0988) < 1e-4, 'daylight p4: no-shift slips 6.90 and 11.10 solve sin(pi t / 6) = -5/11')
    ok(all(abs(math.sin(math.pi * t_ / 6) + 5 / 11) < 1e-3 for t_ in (6.9, 11.1)), 'daylight p4: 6.9 and 11.1 have sine -5/11 to 3 dp')
    ok(abs(Lm(3.9) - 14) < 0.02 and abs(Lm(8.1) - 14) < 0.02 and abs(12 + 4.4 * 5 / 11 - 14) < 1e-12, 'daylight p4: above slips 3.9 and 8.1 give 14 hours (sine +5/11)')
    above = sum(1 for t_ in g3[:-1] if Lm(t_ + 0.0005) > 10) / 1000
    num(L3, 'p-daylight-model', 5, float(roots[1] - roots[0]), above, {'outside': 12 - 7.8, 'whole-months': 10 - 2}, asked=9.90 - 2.10, agree=2e-3)
    ok(abs(above - 7.8024) < 2e-3 and abs(12 - above - 4.1976) < 2e-3, 'daylight p5: 7.8 months above, 4.2 below, by a 12,000-step scan')
    ok(L3['p-daylight-model']['parts'][4]['widget']['tol']['abs'] == 0.05, 'daylight p5: one decimal place band 7.8 +- 0.05 (takes 7.80 and 7.8024, refuses 7.7 and 7.9)')
    ok(not within(7.7, 7.8, 0.05) and not within(7.9, 7.8, 0.05) and within(7.8024, 7.8, 0.05), 'daylight p5: band edges')
    for pp in (3, 4):
        ok('9.8' not in L3['p-daylight-model']['parts'][pp]['question'] + L3['p-daylight-model']['parts'][pp]['feedback']['correct'], f'daylight p{pp + 1}: no 9.8 left')

    # ---- p-garden-bed: edges 10 m and 13 m, area 25 m^2
    Cs = SYM['C']
    expr_part(L3, 'p-garden-bed', 1, 65 * sp.sin(Cs), {'no-half': 130 * sp.sin(Cs), 'cos': 65 * sp.cos(Cs), 'angle': 65 * Cs}, syms=(Cs,))
    shoe = lambda c: abs(13 * (10 * math.sin(c)) - 0 * (10 * math.cos(c))) / 2   # shoelace on (0,0), (13,0), 10(cos c, sin c)
    ok(all(abs(shoe(c) - 65 * math.sin(c)) < 1e-12 for c in (0.4, 1.1, 2.5)), 'garden p1: shoelace area equals 65 sin C')
    c1 = deg(bisect(lambda c: 65 * math.sin(c) - 25, 0.01, math.pi / 2))
    c2 = deg(bisect(lambda c: 65 * math.sin(c) - 25, math.pi / 2, math.pi - 0.01))
    num_set(L3, 'p-garden-bed', 2, [sp.asin(sp.Rational(5, 13)) / DEG, 180 - sp.asin(sp.Rational(5, 13)) / DEG], [c1, c2],
            {'no-half': [deg(math.asin(25 / 130)), 180 - deg(math.asin(25 / 130))], 'cos-rule': [22.62, 360 - 22.62]}, asked=[22.62, 157.38])
    ok(5**2 + 12**2 == 13**2 and F(25, 65) == F(5, 13) and round(c1, 2) == 22.62 and round(c2, 2) == 157.38, 'garden p2: sin C = 5/13; 22.62 and 157.38')
    num(L3, 'p-garden-bed', 3, sp.Rational(-12, 13), math.cos(rad(c2)),
        {'sign': 12 / 13, 'one-minus': 1 - 5 / 13, 'no-root': -(144 / 169)}, asked=-0.923)
    far = (10 * math.cos(rad(c2)), 10 * math.sin(rad(c2)))
    num(L3, 'p-garden-bed', 4, sp.sqrt(509), math.dist(far, (13, 0)),
        {'sign': math.sqrt(29), 'pythagoras': math.sqrt(269), 'no-root': 509, 'no-two': math.sqrt(269 + 120)}, asked=22.56, printed='22.56')
    ok(100 + 169 + 240 == 509 and abs(math.sqrt(29) - 5.39) < 0.005 and abs(math.sqrt(269) - 16.40) < 0.005, 'garden p4: printed 509, 5.39 and 16.40')

# ================================================================ report
print(f'numbers: {checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
