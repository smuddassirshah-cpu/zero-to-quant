"""Recompute every number in app/content/courses/vectors/problems-<n>.json twice.

Method 1 is exact: sympy Rationals and Matrices (exact inverses, determinants, square roots,
acos in closed form where one exists). Method 2 is a different route in floating point: NumPy
arrays and np.linalg (solve, inv, det, norm, matrix_rank), or a worked alternative such as the
cosine rule or a step-by-step composition. For each numeric part: both methods agree; the key
lies within its tol of them; each `wrong` value matches its named slip, lies outside the key's
band, and no two wrong bands overlap; every wrong id has a byKey line; a non-whole key's
question names its form. Expression parts (vectors and matrices): the key and every accept form
equal the exact answer entry by entry, and every wrong form differs. Choice parts: the keyed
option. `stated` ties an intermediate figure printed in feedback or explain to its text and its
value. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-vectors-numbers.py
"""
import json, os, re, sys, itertools, math
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR = standard_transformations + (implicit_multiplication_application,)

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'vectors')
fails, checks = [], 0
FORM = re.compile(r'decimal|places?\b|fraction|whole number|nearest|per cent|percentage|%', re.I)
R = sp.Rational
k_ = sp.Symbol('k')


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'vectors', f'set {n}: header')
    ok(3 <= len(d['items']) <= 5, f'set {n}: item count')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'set {n}: no difficulty 5')
    for it in d['items']:
        ok(3 <= it['difficulty'] <= 5, f'{it["id"]}: difficulty')
        ok(3 <= len(it['parts']) <= 5, f'{it["id"]}: part count')
    parts = [p for it in d['items'] for p in it['parts']]
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
    ok(3 * typed >= 2 * len(parts), f'set {n}: typed parts {typed} of {len(parts)}')
    return {it['id']: it for it in d['items']}


def part(items, iid, k):
    return items[iid]['parts'][k - 1]


def text_of(p):
    return json.dumps(p, ensure_ascii=False)


def num(items, iid, k, exact, alt, slips=None, rel=1e-9):
    """exact: sympy or Fraction value; alt: float from the second route; slips: {id: value}."""
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e = float(exact)
    ok(math.isclose(e, float(alt), rel_tol=rel, abs_tol=1e-9), f'{tag}: methods differ {e} vs {float(alt)}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    if float(w['answer']) != int(w['answer']) or tol > 0 and tol < 0.5:
        ok(bool(FORM.search(p['question'])), f'{tag}: question states no form')
    if float(w['answer']) == int(w['answer']) and tol == 0:
        ok(bool(re.search(r'whole number', p['question'])), f'{tag}: whole-number part does not say so')
    slips = slips or {}
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    ok(set(wrongs) <= set(p['feedback'].get('byKey', {})), f'{tag}: byKey lines missing')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= max(wt, 1e-9), f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} inside the key band')
        ok(abs(float(val) - e) > tol, f'{tag}: slip {wid} equals the answer')
    for a, b in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a], wrongs[b]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a} and {b} overlap')
    return e


def parse_entry(s):
    s = s.strip()
    s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    return sp.nsimplify(parse_expr(s, local_dict={'k': k_}, transformations=TR), rational=True)


def parse_obj(s):
    """'(a, b)', '[a, b]', '[[a, b], [c, d]]' or a pmatrix -> sympy Matrix."""
    s = s.strip()
    m = re.fullmatch(r'\\begin\{pmatrix\}(.*)\\end\{pmatrix\}', s, re.S)
    if m:
        rows = [r.split('&') for r in m.group(1).split('\\\\')]
        return sp.Matrix([[parse_entry(x) for x in r] for r in rows])
    if s.startswith('[['):
        rows = re.findall(r'\[([^\[\]]*)\]', s[1:-1])
        return sp.Matrix([[parse_entry(x) for x in r.split(',')] for r in rows])
    inner = s[1:-1]
    parts, depth, cur = [], 0, ''
    for ch in inner:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    parts.append(cur)
    return sp.Matrix([[parse_entry(x) for x in parts]])


def same(A, B):
    if A.shape != B.shape:
        return False
    return all(sp.simplify(a - b) == 0 for a, b in zip(A, B))


def obj(items, iid, k, exact, alt, slips):
    """exact: sympy Matrix (a vector as one row); alt: NumPy array from the second route."""
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    exact = sp.Matrix(exact)
    if exact.shape[0] != 1 and np.ndim(alt) == 1:
        exact = exact.T
    if not exact.free_symbols:
        ok(np.allclose(np.array(exact.tolist(), dtype=float).reshape(np.shape(alt)), alt), f'{tag}: methods differ')
    else:
        for kv in (0.5, 1.7, 3):
            ev = np.array(exact.subs(k_, kv).tolist(), dtype=float)
            ok(np.allclose(ev.reshape(np.shape(alt(kv))), alt(kv)), f'{tag}: methods differ at k={kv}')
    for form in [w['answer']] + w.get('accept', []):
        ok(same(parse_obj(form), exact), f'{tag}: form {form} differs from the key')
    got = {x['id']: x['tex'] for x in w.get('wrong', [])}
    ok(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} vs {sorted(slips)}')
    ok(set(got) <= set(p['feedback'].get('byKey', {})), f'{tag}: byKey lines missing')
    for wid, val in slips.items():
        if wid not in got:
            continue
        g = parse_obj(got[wid])
        v = sp.Matrix(val)
        if v.shape != g.shape and v.T.shape == g.shape:
            v = v.T
        ok(same(g, v), f'{tag}: wrong {wid} {got[wid]} vs slip {v.tolist()}')
        ok(not same(g, exact), f'{tag}: wrong {wid} equals the key')
    for a, b in itertools.combinations(list(got), 2):
        ok(not same(parse_obj(got[a]), parse_obj(got[b])), f'{tag}: wrongs {a} and {b} coincide')


def poly(items, iid, k, exact, slips):
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    for form in [w['answer']] + w.get('accept', []):
        ok(sp.simplify(parse_entry(form) - exact) == 0, f'{tag}: form {form} differs')
    got = {x['id']: x['tex'] for x in w.get('wrong', [])}
    ok(set(got) == set(slips), f'{tag}: wrong ids')
    ok(set(got) <= set(p['feedback'].get('byKey', {})), f'{tag}: byKey lines missing')
    for wid, val in slips.items():
        ok(sp.simplify(parse_entry(got[wid]) - val) == 0, f'{tag}: wrong {wid}')
        ok(sp.simplify(parse_entry(got[wid]) - exact) != 0, f'{tag}: wrong {wid} equals key')


def pick(items, iid, k, cid):
    opts = part(items, iid, k)['widget']['options']
    keyed = [o['id'] for o in opts if o.get('correct')]
    ok(keyed == [cid], f'{iid} p{k}: keyed {keyed}, expected {cid}')
    ok(all(o.get('why') for o in opts if not o.get('correct')), f'{iid} p{k}: a distractor has no why')


def stated(items, iid, k, phrase, value, printed, places):
    """The phrase is in the part's text, and `printed` is `value` rounded to `places`."""
    ok(phrase in text_of(part(items, iid, k)), f'{iid} p{k}: phrase not found: {phrase}')
    ok(abs(float(value) - printed) <= 0.5 * 10 ** (-places) + 1e-12, f'{iid} p{k}: stated {printed} vs {float(value)}')


def deg(x):
    return math.degrees(x)


def acos_deg_np(u, v):
    u, v = np.asarray(u, float), np.asarray(v, float)
    return np.degrees(np.arccos(u @ v / (np.linalg.norm(u) * np.linalg.norm(v))))


M = sp.Matrix
# ======================================================== level 1: vectors
I = load(1)
if I:
    # p-charging-robot
    u, v, T = M([3, 1]), M([1, 2]), M([9, 8])
    ab = M.hstack(u, v).LUsolve(T)
    obj(I, 'p-charging-robot', 1, ab.T, np.linalg.solve(np.array([[3, 1], [1, 2.]]), [9, 8.]), {'swapped': [[3, 2]]})
    a, b = ab
    L1, L2 = a * u, b * v
    d12 = L1.dot(L2)
    num(I, 'p-charging-robot', 2, d12, 2 * 3 * float(np.dot([3, 1], [1, 2])),
        {'unweighted': u.dot(v), 'only-u': (a * u).dot(v), 'only-v': u.dot(b * v)})
    th = sp.acos(d12 / (L1.norm() * L2.norm()))
    ok(th == sp.pi / 4, 'robot: angle is exactly pi/4')
    num(I, 'p-charging-robot', 3, deg(float(th)), acos_deg_np([6, 2], [3, 6]),
        {'radians': float(th), 'no-root': deg(math.acos(30 / (40 * 45)))})
    stated(I, 'p-charging-robot', 3, r'\approx 0.7071', d12 / (L1.norm() * L2.norm()), 0.7071, 4)
    stated(I, 'p-charging-robot', 3, r'\approx 42.43', sp.sqrt(1800), 42.43, 2)
    straight = sp.sqrt(L1.dot(L1) + 2 * d12 + L2.dot(L2))
    num(I, 'p-charging-robot', 4, straight, np.linalg.norm([9, 8.]),
        {'no-cross': sp.sqrt(85), 'path': L1.norm() + L2.norm(), 'minus': sp.sqrt(85 - 60), 'no-root': 145}, rel=1e-3)
    ok(abs(float(straight) - 12.04) <= 0.005, 'robot: 12.04 is the 2 dp value')

    # p-active-bets
    bw, ww, rr = M([R(5, 10), R(3, 10), R(2, 10)]), M([R(4, 10), R(45, 100), R(15, 100)]), M([R(2, 100), R(-1, 100), R(4, 100)])
    aa = ww - bw
    obj(I, 'p-active-bets', 1, aa.T, np.array([0.4, 0.45, 0.15]) - np.array([0.5, 0.3, 0.2]),
        {'flipped': (-aa).T, 'added': (ww + bw).T})
    ok(sum(aa) == 0, 'active weights add to 0')
    ar = aa.dot(rr)
    num(I, 'p-active-bets', 2, ar, np.dot([0.4, 0.45, 0.15], [0.02, -0.01, 0.04]) - np.dot([0.5, 0.3, 0.2], [0.02, -0.01, 0.04]),
        {'flipped': -ar, 'fund': ww.dot(rr), 'benchmark': bw.dot(rr)})
    na = aa.norm()
    num(I, 'p-active-bets', 3, na, np.linalg.norm([-0.1, 0.15, -0.05]),
        {'no-root': aa.dot(aa), 'abs-sum': sum(abs(x) for x in aa), 'sum': sum(aa)}, rel=1e-3)
    nr = rr.norm()
    ang = deg(float(sp.acos(ar / (na * nr))))
    num(I, 'p-active-bets', 4, ang, acos_deg_np([-0.1, 0.15, -0.05], [0.02, -0.01, 0.04]),
        {'acute': 180 - ang, 'radians': math.radians(ang)}, rel=1e-3)
    ok(abs(deg(math.acos(-0.0055 / (0.1871 * 0.04583))) - 130) < 0.5, 'bets: rounded inputs still give 130')
    stated(I, 'p-active-bets', 4, r'\approx 0.04583', nr, 0.04583, 5)
    stated(I, 'p-active-bets', 4, r'\approx -0.6415', ar / (na * nr), -0.6415, 4)
    ok(aa[1] > 0 and rr[1] < 0 and aa[2] < 0 and rr[2] == max(rr), 'bets: explain names US overweight falling, Japan underweight rising most')

    # p-drone-crosswind
    dep, wind = M([12, 16]), M([-8, 1])
    dh = dep / dep.norm()
    obj(I, 'p-drone-crosswind', 1, dh.T, np.array([12, 16.]) / np.hypot(12, 16),
        {'not-unit': [[3, 4]], 'swapped': [[R(4, 5), R(3, 5)]], 'whole': [[12, 16]]})
    along = wind.dot(dh)
    num(I, 'p-drone-crosswind', 2, along, np.dot([-8, 1.], [0.6, 0.8]),
        {'sign': -along, 'not-unit': wind.dot(dep), 'three-four': wind.dot(M([3, 4])), 'swapped': wind.dot(M([R(4, 5), R(3, 5)]))})
    perp_vec = wind - along * dh
    cross = sp.sqrt(wind.dot(wind) - along ** 2)
    ok(perp_vec.norm() == cross and perp_vec.dot(dh) == 0, 'drone: crosswind is the perpendicular remainder')
    num(I, 'p-drone-crosswind', 3, cross, abs(12 * 1. - 16 * -8.) / 20,
        {'wind-speed': wind.norm(), 'added': sp.sqrt(wind.dot(wind) + along ** 2), 'no-root': cross ** 2}, rel=1e-9)
    air_along = sp.sqrt(25 ** 2 - cross ** 2)
    num(I, 'p-drone-crosswind', 4, air_along, np.sqrt(25. ** 2 - 7. ** 2), {'no-cancel': 25, 'subtracted': 25 - cross, 'no-root': air_along ** 2})
    ground = air_along + along
    # second route: build the air velocity explicitly and add the wind
    nhat = np.array([-0.8, 0.6])
    air = 24 * np.array([0.6, 0.8]) - float(perp_vec.dot(M([-R(4, 5), R(3, 5)]))) * nhat
    gv = air + np.array([-8, 1.])
    ok(abs(np.linalg.norm(air) - 25) < 1e-12 and abs(gv @ nhat) < 1e-12, 'drone: air velocity is 25 long and ground track is on the route')
    num(I, 'p-drone-crosswind', 5, dep.norm() / ground * 60, 20 / np.linalg.norm(gv) * 60,
        {'no-wind': R(20, 24) * 60, 'tailwind': R(20, 28) * 60, 'air-only': R(20, 25) * 60, 'hours': dep.norm() / ground})

    # p-stress-hedge
    w0, c, s = M([R(6, 10), R(3, 10), R(1, 10)]), M([R(1, 100), R(-12, 100), R(8, 100)]), M([R(-3, 100), R(4, 100), R(-2, 100)])
    R1 = w0.dot(c)
    num(I, 'p-stress-hedge', 1, R1, np.dot([0.6, 0.3, 0.1], [0.01, -0.12, 0.08]), {'unweighted': sum(c), 'equal': sum(c) / 3})
    h = sp.Symbol('h')
    move = M([0, -1, 1])
    hh = sp.solve((w0 + h * move).dot(c), h)[0]
    hnum = np.linalg.solve(np.array([[np.dot([0, -1, 1.], [0.01, -0.12, 0.08])]]), [-np.dot([0.6, 0.3, 0.1], [0.01, -0.12, 0.08])])[0]
    num(I, 'p-stress-hedge', 2, hh, hnum,
        {'sign': -R1 / (c[2] + c[1]), 'gold-only': -R1 / c[2], 'equity-only': -R1 / -c[1]}, rel=1e-9)
    ok(abs(float(-R1 / (c[2] + c[1])) - (-0.55)) < 1e-12, 'hedge: sign slip is -0.55')
    w1 = w0 + hh * move
    ok(w1 == M([R(6, 10), R(19, 100), R(21, 100)]) and sum(w1) == 1 and w1.dot(c) == 0, 'hedge: new weights stated, sum to 1, perpendicular to crash')
    R2 = w1.dot(s)
    num(I, 'p-stress-hedge', 3, R2, np.dot([0.6, 0.19, 0.21], [-0.03, 0.04, -0.02]),
        {'old': w0.dot(s), 'shift-added': w0.dot(s) - hh * move.dot(s)})
    ok(hh * move.dot(s) == R(-66, 10000), 'hedge: the move costs 0.0066 in the rate rise')
    R3 = w1.dot((c + s) / 2)
    num(I, 'p-stress-hedge', 4, R3, np.dot([0.6, 0.19, 0.21], (np.array([0.01, -0.12, 0.08]) + np.array([-0.03, 0.04, -0.02])) / 2),
        {'unhedged': w0.dot((c + s) / 2), 'no-half': w1.dot(c + s)})
    ok(abs(float(w0.dot((c + s) / 2))) / abs(float(R3)) > 1.9, 'hedge: roughly halves the central loss')

# ======================================================== level 2: matrices
I = load(2)
if I:
    # p-italic-letters
    S = M([[1, R(1, 4)], [0, 1]])
    ok(S * M([1, 0]) == M([1, 0]) and S * M([0, 1]) == M([R(1, 4), 1]), 'italic: S fixes e1 and sends e2 to (0.25, 1)')
    obj(I, 'p-italic-letters', 1, S, np.column_stack([[1, 0], [0.25, 1]]), {'rows': S.T})
    top = M([2, 8])
    obj(I, 'p-italic-letters', 2, (S * top).T, 2 * np.array([1, 0.]) + 8 * np.array([0.25, 1]),
        {'rows': (S.T * top).T, 'once': [[R(9, 4), 8]]})
    Dm = M([[R(3, 2), 0], [0, 1]])
    obj(I, 'p-italic-letters', 3, Dm * S, np.array([[1.5, 0], [0, 1]]) @ np.array([[1, 0.25], [0, 1]]),
        {'order': S * Dm, 'entrywise': Dm.multiply_elementwise(S)})
    num(I, 'p-italic-letters', 4, (Dm * S * top)[0], (np.array([[1.5, 0], [0, 1]]) @ np.array([4., 8]))[0],
        {'order': (S * Dm * top)[0], 'slant-only': (S * top)[0], 'widen-only': (Dm * top)[0]})

    # p-site-plan
    Rm = M([[R(4, 5), -R(3, 5)], [R(3, 5), R(4, 5)]])
    th = math.atan2(0.6, 0.8)
    Rn = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    obj(I, 'p-site-plan', 1, Rm, Rn, {'clockwise': Rm.T, 'swapped': M([[R(3, 5), -R(4, 5)], [R(4, 5), R(3, 5)]])})
    obj(I, 'p-site-plan', 2, Rm.T * Rm, Rn.T @ Rn, {'square': Rm * Rm, 'entrywise': Rm.T.multiply_elementwise(Rm)})
    bh = Rm.T * M([11, 2])
    obj(I, 'p-site-plan', 3, bh.T, np.linalg.solve(Rn, [11, 2.]),
        {'forward': (Rm * M([11, 2])).T, 'swapped': (M([[R(3, 5), -R(4, 5)], [R(4, 5), R(3, 5)]]).T * M([11, 2])).T})
    ok(Rm * bh == M([11, 2]), 'site: check R(10, -5) = (11, 2)')
    step = Rm * (M([10, 5]) - bh)
    ok(step == M([-6, 8]), 'site: ground step (-6, 8)')
    phi = deg(float(sp.acos(step[0] / step.norm())))
    ground_step = Rn @ np.array([10, 5.]) - np.array([11, 2.])
    num(I, 'p-site-plan', 4, phi, np.degrees(np.arctan2(ground_step[1], ground_step[0])),
        {'plan-angle': 90, 'clockwise': deg(float(sp.acos((Rm.T * M([0, 10]))[0] / 10))), 'theta': deg(th)}, rel=1e-9)
    ok(abs(phi - (90 + deg(th))) < 1e-9, 'site: angle is 90 + theta')

    # p-factor-risk
    Bm = M([[R(12, 10), R(4, 10)], [R(8, 10), R(-5, 10)], [1, 1]])
    wv = M([R(1, 2), R(3, 10), R(1, 5)])
    Fm = M([[R(225, 10000), R(3, 1000)], [R(3, 1000), R(64, 10000)]])
    pick(I, 'p-factor-risk', 1, 'bt-w')
    ok(Bm.T.shape == (2, 3) and (Bm.T * wv).shape == (2, 1) and (Bm * Bm.T * wv).shape == (3, 1), 'factor: sizes of the options')
    e = Bm.T * wv
    Bn, wn, Fn = np.array([[1.2, 0.4], [0.8, -0.5], [1.0, 1.0]]), np.array([0.5, 0.3, 0.2]), np.array([[0.0225, 0.003], [0.003, 0.0064]])
    obj(I, 'p-factor-risk', 2, e.T, wn @ Bn, {'unweighted': M([[3, R(9, 10)]]), 'equal': M([[1, R(3, 10)]])})
    ok(M([[sum(Bm[:, 0]), sum(Bm[:, 1])]]) == M([[3, R(9, 10)]]), 'factor: unweighted column sums')
    Fe = Fm * e
    obj(I, 'p-factor-risk', 3, Fe.T, Fn @ (Bn.T @ wn),
        {'diagonal': (M.diag(Fm[0, 0], Fm[1, 1]) * e).T, 'wrong-order': M([[Fe[1], Fe[0]]])})
    var = (e.T * Fe)[0]
    var_alt = wn @ (Bn @ Fn @ Bn.T) @ wn
    num(I, 'p-factor-risk', 4, var, var_alt,
        {'diagonal': (e.T * M.diag(Fm[0, 0], Fm[1, 1]) * e)[0], 'no-f': (e.T * e)[0], 'sum': sum(Fe)})
    stated(I, 'p-factor-risk', 4, '0.025116 + 0.00118', e[0] * Fe[0], 0.025116, 6)
    ok(e[1] * Fe[1] == R(118, 100000), 'factor: second term 0.00118')
    ok(2 * e[0] * e[1] * Fm[0, 1] == R(156, 100000), 'factor: cross term 0.00156')
    vol = sp.sqrt(var)
    num(I, 'p-factor-risk', 5, vol, np.sqrt(var_alt), {'diagonal': sp.sqrt((e.T * M.diag(Fm[0, 0], Fm[1, 1]) * e)[0]), 'no-root': var}, rel=1e-9)
    stated(I, 'p-factor-risk', 5, r'\approx 0.1622', vol, 0.1622, 4)
    stated(I, 'p-factor-risk', 5, '15.7%', sp.sqrt((e.T * M.diag(Fm[0, 0], Fm[1, 1]) * e)[0]) * 100, 15.7, 1)

    # p-bakery-costs
    Qm = M([[R(1, 2), R(3, 10)], [R(1, 10), R(1, 5)], [R(1, 20), R(1, 5)]])
    pv, xo = M([R(4, 5), R(3, 2), 6]), M([40, 12])
    Qn, pn = np.array([[0.5, 0.3], [0.1, 0.2], [0.05, 0.2]]), np.array([0.8, 1.5, 6.0])
    use = Qm * xo
    obj(I, 'p-bakery-costs', 1, use.T, 40 * Qn[:, 0] + 12 * Qn[:, 1], {'swapped': (Qm * M([12, 40])).T, 'one-each': (Qm * M([1, 1])).T})
    cost = pv.dot(use)
    num(I, 'p-bakery-costs', 2, cost, (Qn.T @ pn) @ np.array([40, 12.]), {'swapped': pv.dot(Qm * M([12, 40])), 'unpriced': sum(use)})
    pick(I, 'p-bakery-costs', 3, 'qt-p')
    cvec = Qm.T * pv
    ok(cvec == M([R(85, 100), R(174, 100)]), 'bakery: c = (0.85, 1.74)')
    num(I, 'p-bakery-costs', 4, cvec[1], Qn[:, 1] @ pn, {'loaf': cvec[0], 'unpriced': sum(Qm[:, 1])})
    ok(cvec.dot(xo) == cost, 'bakery: c . x reproduces part 2')
    num(I, 'p-bakery-costs', 5, cvec.dot(M([50, 20])), pn @ (Qn @ np.array([50, 20.])),
        {'this-week': cost, 'swapped': cvec.dot(M([20, 50])), 'one-each': sum(cvec)})

# ======================================================== level 3: inverses and systems
I = load(3)
if I:
    def adj_noswap(Mx):
        return M([[Mx[0, 0], -Mx[0, 1]], [-Mx[1, 0], Mx[1, 1]]])

    def adj(Mx):
        return M([[Mx[1, 1], -Mx[0, 1]], [-Mx[1, 0], Mx[0, 0]]])

    # p-goat-feed
    A = M([[R(4, 10), R(1, 10)], [R(2, 10), R(3, 10)]])
    An = np.array([[0.4, 0.1], [0.2, 0.3]])
    bb = M([13, 14])
    obj(I, 'p-goat-feed', 1, A, np.column_stack([[0.4, 0.2], [0.1, 0.3]]), {'transposed': A.T})
    dA = A.det()
    num(I, 'p-goat-feed', 2, dA, np.linalg.det(An), {'added': A[0, 0] * A[1, 1] + A[0, 1] * A[1, 0], 'flipped': -dA})
    Ai = A.inv()
    ok(Ai == adj(A) / dA, 'feed: inverse is the 2 x 2 recipe')
    obj(I, 'p-goat-feed', 3, Ai, np.linalg.inv(An),
        {'no-divide': adj(A), 'no-negate': M([[3, 1], [2, 4]]), 'transposed': A.T.inv(), 'times-det': adj(A) * dA})
    xx = Ai * bb
    obj(I, 'p-goat-feed', 4, xx.T, np.linalg.solve(An, [13, 14.]),
        {'transposed': (A.T.inv() * bb).T, 'no-divide': (adj(A) * bb).T, 'swapped': M([[xx[1], xx[0]]])})
    ok(A * xx == bb and A[0, :] * xx == M([13]) and A[0, 0] * xx[0] == 10 and A[1, 0] * xx[0] == 5, 'feed: check 10 + 3 = 13, 5 + 9 = 14')

    # p-paint-tints
    Ak = M([[12, 8], [3, k_]])
    kk = sp.solve(Ak.det(), k_)
    num(I, 'p-paint-tints', 1, kk[0], [kv for kv in np.arange(-10, 10.5, 0.5) if abs(np.linalg.det(np.array([[12, 8], [3, kv]]))) < 1e-9][0],
        {'plus': sp.solve(12 * k_ + 24, k_)[0], 'mixed': sp.solve(sp.Eq(R(12) / k_, R(8, 3)), k_)[0]})
    A2 = Ak.subs(k_, 2)
    num(I, 'p-paint-tints', 2, A2.rank(), np.linalg.matrix_rank(np.array([[12, 8], [3, 2.]])), {'full': 2, 'zero': 0})
    pick(I, 'p-paint-tints', 3, 'none')
    aug = M.hstack(A2, M([60, 18]))
    ok(aug.rank() == 2 and A2.rank() == 1, 'paint: (60, 18) is off the column line (no solution)')
    ok(M.hstack(A2, M([60, 15])).rank() == 1 and 3 * 5 == 15, 'paint: (60, 15) on the line; p = 5 gives blue 15')
    q = sp.Symbol('q')
    qq = sp.solve(12 * 3 + 8 * q - 60, q)[0]
    ok((A2 * M([3, qq]))[1] == 15, 'paint: blue checks at (3, 3)')
    num(I, 'p-paint-tints', 4, qq, (60 - 12 * 3) / 8, {'q-only': R(60, 8), 'p-only': 0})
    A5 = Ak.subs(k_, 5)
    ok(A5.det() == 36 and (12 * k_ - 24).subs(k_, 5) == 36, 'paint: det 36 at k = 5')
    x5 = A5.inv() * M([64, 22])
    obj(I, 'p-paint-tints', 5, x5.T, np.linalg.solve(np.array([[12, 8], [3, 5.]]), [64, 22.]),
        {'swapped': M([[x5[1], x5[0]]]), 'no-divide': (adj(A5) * M([64, 22])).T})
    ok(adj(A5) * M([64, 22]) == M([144, 72]), 'paint: 320 - 176 = 144 and -192 + 264 = 72')

    # p-colour-sensor
    Ms = M([[R(8, 10), R(3, 10)], [R(2, 10), R(7, 10)]])
    Mn = np.array([[0.8, 0.3], [0.2, 0.7]])
    rd = M([130, 70])
    corners = Mn @ np.array([[0, 1, 1, 0], [0, 0, 1, 1.]])
    shoelace = 0.5 * abs(sum(corners[0, i] * corners[1, (i + 1) % 4] - corners[0, (i + 1) % 4] * corners[1, i] for i in range(4)))
    num(I, 'p-colour-sensor', 1, abs(Ms.det()), shoelace, {'added': Ms[0, 0] * Ms[1, 1] + Ms[0, 1] * Ms[1, 0], 'diagonal': Ms[0, 0] * Ms[1, 1]})
    Mi = Ms.inv()
    obj(I, 'p-colour-sensor', 2, Mi, np.linalg.inv(Mn), {'no-divide': adj(Ms), 'times-det': adj(Ms) * Ms.det(), 'no-negate': M([[R(14, 10), R(6, 10)], [R(4, 10), R(16, 10)]])})
    star = np.linalg.inv(Mn) * np.array([130, 70.])
    num(I, 'p-colour-sensor', 3, Mi[0, 1] * rd[1], star[0, 1], {'matrix-product': (Mi * rd)[0], 'entry-10': Mi[1, 0] * rd[0], 'entry-00': Mi[0, 0] * rd[0]}, rel=1e-9)
    ok(np.allclose(star, [[182, -42], [-52, 112]]) and np.allclose(star.sum(axis=1), [140, 60]) and np.allclose(star.sum(axis=0), [130, 70]),
       'sensor: the * array, its row sums and its column sums')
    tt = Mi * rd
    obj(I, 'p-colour-sensor', 4, tt.T, np.linalg.solve(Mn, [130, 70.]),
        {'no-divide': (adj(Ms) * rd).T, 'forward': (Ms * rd).T, 'column-sums': rd.T})
    ok(Ms * tt == rd, 'sensor: M(140, 60) = (130, 70)')

    # p-engraver-dial
    Ae = M([[3, 1], [2, 1]])
    Bk = M([[2, k_], [1, 1]])
    Ck = Bk * Ae
    obj(I, 'p-engraver-dial', 1, Ck, lambda kv: np.array([[2, kv], [1, 1.]]) @ np.array([[3, 1], [2, 1.]]),
        {'order': Ae * Bk, 'entrywise': Bk.multiply_elementwise(Ae)})
    dC = sp.expand(Ck.det())
    ok(sp.simplify(dC - Bk.det() * Ae.det()) == 0, 'engraver: det C = det B det A')
    ok(all(abs(np.linalg.det(np.array([[2, kv], [1, 1.]]) @ np.array([[3, 1], [2, 1.]])) - (2 - kv)) < 1e-9 for kv in (-1, 0.5, 3)), 'engraver: det numerically')
    added = sp.expand(Ck[0, 0] * Ck[1, 1] + Ck[0, 1] * Ck[1, 0])
    poly(I, 'p-engraver-dial', 2, dC, {'added': added, 'flipped': -dC})
    ok(sp.simplify(sp.expand((Ae * Bk).det()) - dC) == 0, 'engraver: the order slip has the same determinant')
    k0 = sp.solve(dC, k_)[0]
    num(I, 'p-engraver-dial', 3, k0, [kv for kv in range(-5, 6) if abs(np.linalg.det(np.array([[2, kv], [1, 1.]]) @ np.array([[3, 1], [2, 1.]]))) < 1e-9][0],
        {'added': sp.solve(added, k_)[0]})
    C1 = Ck.subs(k_, 1)
    ok(C1 == M([[8, 3], [5, 2]]) and C1.det() == 1, 'engraver: C_1 and its determinant')
    obj(I, 'p-engraver-dial', 4, C1.inv(), np.linalg.inv(np.array([[8, 3], [5, 2.]])),
        {'no-negate': M([[2, 3], [5, 8]]), 'unswapped': adj_noswap(C1), 'order': (Ae * Bk.subs(k_, 1)).inv()})
    mark = M([19, 12])
    pt = C1.inv() * mark
    obj(I, 'p-engraver-dial', 5, pt.T, np.linalg.solve(np.array([[8, 3], [5, 2.]]), [19, 12.]),
        {'order': ((Ae * Bk.subs(k_, 1)).inv() * mark).T, 'forward': (C1 * mark).T, 'unswapped': (adj_noswap(C1) * mark).T})
    ok(Ae * pt == M([7, 5]) and Bk.subs(k_, 1) * M([7, 5]) == mark, 'engraver: forward check (2, 1) -> (7, 5) -> (19, 12)')

print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
