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
    pre = re.fullmatch(r'(\\frac\{[^{}]*\}\{[^{}]*\}|[\d.]+)\s*(\[\[.*\]\]|\(.*\))', s, re.S)
    if pre and not s.startswith(('(', '[', '\\begin')):
        return parse_entry(pre.group(1)) * parse_obj(pre.group(2))                  # "10[[...]]", "\\frac{1}{5}(3,4)": a number times the object
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


def stale(items, iid, old_values):
    """Re-authored item: none of the old setting's figures may remain in its text (review-problems-1.4-a finding 8)."""
    text = text_of(items[iid])
    for v in old_values:
        ok(v not in text, f'{iid}: stale value {v} still in the item')


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
    # p-charging-robot (re-authored, review-problems-1.4-a findings 8 and 9): u = (4, 1), v = (1, 3), charger (11, 11)
    u, v, T = M([4, 1]), M([1, 3]), M([11, 11])
    ab = M.hstack(u, v).LUsolve(T)
    obj(I, 'p-charging-robot', 1, ab.T, np.linalg.solve(np.array([[4, 1], [1, 3.]]), [11, 11.]), {'swapped': [[3, 2]]})
    a, b = ab
    ok(ab == M([2, 3]) and 4 * 3 + 2 * 1 == 14, 'robot: a = 2, b = 3; the swapped slip gives 14, not 11')
    ok(3 * (4 * 2 + 3) - (2 + 9) == 22 and 11 * a == 22 and b == 11 - 8, 'robot p1: three times the first, less the second, leaves 11a = 22; b = 3')
    L1, L2 = a * u, b * v
    d12 = L1.dot(L2)
    num(I, 'p-charging-robot', 2, d12, 2 * 3 * float(np.dot([4, 1], [1, 3])),
        {'unweighted': u.dot(v), 'only-u': (a * u).dot(v), 'only-v': u.dot(b * v)})
    ok(L1 == M([8, 2]) and L2 == M([3, 9]) and u.dot(v) == 7 and 6 * 7 == 42, 'robot: 2u = (8, 2), 3v = (3, 9), u.v = 7')
    th = sp.acos(d12 / (L1.norm() * L2.norm()))
    num(I, 'p-charging-robot', 3, deg(float(th)), acos_deg_np([8, 2], [3, 9]),
        {'radians': float(th), 'no-root': deg(math.acos(42 / (68 * 90)))})
    ok(abs(deg(float(th)) - deg(float(sp.acos(u.dot(v) / (u.norm() * v.norm()))))) < 1e-9, 'robot: the angle between the legs is the angle between u and v')
    stated(I, 'p-charging-robot', 3, r'\approx 0.5369', d12 / (L1.norm() * L2.norm()), 0.5369, 4)
    stated(I, 'p-charging-robot', 3, r'\approx 78.23', sp.sqrt(6120), 78.23, 2)
    ok(L1.dot(L1) == 68 and L2.dot(L2) == 90, 'robot: |2u|^2 = 68 and |3v|^2 = 90')
    straight = sp.sqrt(L1.dot(L1) + 2 * d12 + L2.dot(L2))
    path = L1.norm() + L2.norm()
    diff = path - straight
    num(I, 'p-charging-robot', 4, diff, np.linalg.norm([8, 2.]) + np.linalg.norm([3, 9.]) - np.linalg.norm([11, 11.]),
        {'straight': straight, 'path': path, 'no-cross': path - sp.sqrt(L1.dot(L1) + L2.dot(L2))}, rel=1e-9)
    ok(straight == sp.sqrt(242) and 11 ** 2 + 11 ** 2 == 242 and abs(float(straight) - 15.56) <= 0.005 and abs(float(path) - 17.73) <= 0.005,
       'robot p4: straight line sqrt(242) = 15.56, path 17.73')
    ok(abs((8.25 + 9.49 - 15.56) - 2.18) < 1e-9 and abs((17.73 - 15.56) - 2.18) <= 0.015 and abs(float(diff) - 2.18) <= 0.015, 'robot p4: rounded routes stay in the 2.18 band')
    stale(I, 'p-charging-robot', ['(3, 1)', '(1, 2)', '(9, 8)', '(6, 2)', '(3, 6)', 'sqrt{40}', 'sqrt{45}', '12.04', '145', '1800'])

    # p-active-bets
    bw, ww, rr = M([R(5, 10), R(3, 10), R(2, 10)]), M([R(4, 10), R(45, 100), R(15, 100)]), M([R(2, 100), R(-1, 100), R(4, 100)])
    aa = ww - bw
    obj(I, 'p-active-bets', 1, aa.T, np.array([0.4, 0.45, 0.15]) - np.array([0.5, 0.3, 0.2]),
        {'flipped': (-aa).T, 'added': (ww + bw).T})
    ok(sum(aa) == 0, 'active weights add to 0')
    ar = aa.dot(rr)
    num(I, 'p-active-bets', 2, ar, np.dot([0.4, 0.45, 0.15], [0.02, -0.01, 0.04]) - np.dot([0.5, 0.3, 0.2], [0.02, -0.01, 0.04]),
        {'flipped': -ar, 'fund': ww.dot(rr), 'benchmark': bw.dot(rr), 'decimal': ar / 100})
    stated(I, 'p-active-bets', 2, '-0.55', ar * 100, -0.55, 2)
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
    num(I, 'p-stress-hedge', 1, R1, np.dot([0.6, 0.3, 0.1], [0.01, -0.12, 0.08]), {'unweighted': sum(c), 'equal': sum(c) / 3, 'decimal': R1 / 100})
    stated(I, 'p-stress-hedge', 1, '-2.2', R1 * 100, -2.2, 1)
    ok('2 decimal places' in part(I, 'p-stress-hedge', 1)['question'], 'hedge p1: asks for 2 places, so the decimal slip -0.0002 is at the asked rounding')
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
        {'old': w0.dot(s), 'shift-added': w0.dot(s) - hh * move.dot(s), 'decimal': R2 / 100})
    stated(I, 'p-stress-hedge', 3, '-1.46', R2 * 100, -1.46, 2)
    ok(hh * move.dot(s) == R(-66, 10000), 'hedge: the move costs 0.0066 in the rate rise')
    R3 = w1.dot((c + s) / 2)
    num(I, 'p-stress-hedge', 4, R3, np.dot([0.6, 0.19, 0.21], (np.array([0.01, -0.12, 0.08]) + np.array([-0.03, 0.04, -0.02])) / 2),
        {'unhedged': w0.dot((c + s) / 2), 'no-half': w1.dot(c + s), 'decimal': R3 / 100})
    stated(I, 'p-stress-hedge', 4, '-0.73', R3 * 100, -0.73, 2)
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
    q4 = part(I, 'p-site-plan', 4)['question']
    ok('between 0 and 180' in q4 and 'step from the borehole to the well' in q4 and 'pipe make with' not in q4, 'site p4: asks for the step, in degrees between 0 and 180')
    ok(abs((180 - phi) - 53.1) < 0.05 and abs(deg(float(sp.acos((Rm.T * M([0, 10]))[0] / 10))) - (180 - phi)) < 1e-9, 'site p4: the clockwise slip 53.1 is the acute angle 180 - phi and the angle of (6, 8)')
    ok((Rm.T * M([0, 10])) == M([6, 8]) and Rm * M([0, 10]) == M([-6, 8]), 'site p4: R^T(0, 10) = (6, 8) and R(0, 10) = (-6, 8)')

    # p-factor-risk (re-authored, finding 8): hedge the market exposure with a future
    Bm = M([[R(11, 10), R(3, 10)], [R(9, 10), R(-2, 10)], [R(14, 10), R(6, 10)]])
    wv = M([R(4, 10), R(35, 100), R(25, 100)])
    Fm = M([[R(144, 10000), R(3, 1000)], [R(3, 1000), R(49, 10000)]])
    Bn, wn, Fn = np.array([[1.1, 0.3], [0.9, -0.2], [1.4, 0.6]]), np.array([0.4, 0.35, 0.25]), np.array([[0.0144, 0.003], [0.003, 0.0049]])
    e = Bm.T * wv
    obj(I, 'p-factor-risk', 1, e.T, wn @ Bn,
        {'unweighted': M([[sum(Bm[:, 0]), sum(Bm[:, 1])]]), 'equal': M([[sum(Bm[:, 0]) / 3, sum(Bm[:, 1]) / 3]])})
    ok(e == M([R(1105, 1000), R(1, 5)]) and sum(wv) == 1, 'factor: e = (1.105, 0.2), weights add to 1')
    x_h = e[0] - R(1, 2)
    num(I, 'p-factor-risk', 2, x_h, (wn @ Bn)[0] - 0.5, {'to-zero': e[0], 'added': e[0] + R(1, 2), 'size': e[1] - R(1, 2)})
    hedge = x_h * M([1, R(1, 4)])
    e2 = e - hedge
    obj(I, 'p-factor-risk', 3, e2.T, wn @ Bn - 0.605 * np.array([1, 0.25]),
        {'market-only': M([[e2[0], e[1]]]), 'size-whole': M([[e2[0], e[1] - x_h]]), 'added': (e + hedge).T})
    ok(hedge == M([R(605, 1000), R(15125, 100000)]) and e2 == M([R(1, 2), R(4875, 100000)]), 'factor: hedge (0.605, 0.15125), hedged exposures (0.5, 0.04875)')
    var2 = (e2.T * Fm * e2)[0]
    e2n = np.array([0.5, 0.04875])
    num(I, 'p-factor-risk', 4, var2, e2n @ Fn @ e2n,
        {'diagonal': (e2.T * M.diag(Fm[0, 0], Fm[1, 1]) * e2)[0], 'no-f': (e2.T * e2)[0], 'unhedged': (e.T * Fm * e)[0]})
    t1, t2, t3 = e2[0] ** 2 * Fm[0, 0], 2 * e2[0] * e2[1] * Fm[0, 1], e2[1] ** 2 * Fm[1, 1]
    ok(t1 == R(36, 10000) and abs(float(t2) - 0.000146) < 5e-7 and abs(float(t3) - 0.000012) < 5e-7 and t1 + t2 + t3 == var2, 'factor p4: terms 0.0036 + 0.000146 + 0.000012')
    ok(abs(float(t2 / var2) - 0.04) < 0.005, 'factor p4: the cross term is about 4% of the total')
    var1 = (e.T * Fm * e)[0]
    ok(abs(float(var1) - 0.01910) < 5e-6 and abs(wn @ (Bn @ Fn @ Bn.T) @ wn - float(var1)) < 1e-12, 'factor p5: unhedged variance 0.01910, by the w^T B F B^T w route too')
    cut = 1 - var2 / var1
    cut_rounded = 1 - 0.00376 / 0.01910
    num(I, 'p-factor-risk', 5, cut, 1 - (e2n @ Fn @ e2n) / (wn @ (Bn @ Fn @ Bn.T) @ wn),
        {'ratio': var2 / var1, 'difference': var1 - var2, 'volatility': 1 - sp.sqrt(var2 / var1), 'decimal': cut / 100}, rel=1e-9)
    ok(abs(cut_rounded - 0.8031) < 5e-5 and abs(cut_rounded - 0.803) <= 0.0005 and abs(float(cut) - 0.803) <= 0.0005, 'factor p5: the rounded and the exact cut both sit in the 80.3% band')
    ok(abs((0.01910 - 0.00376) - 0.01534) < 1e-12 and abs(float(var1 - var2) - 0.01534) < 1e-5, 'factor p5: the fall in variance is 0.01534 from the rounded variances (0.015347 unrounded)')
    stale(I, 'p-factor-risk', ['(0.5, 0.3, 0.2)', '1.2', '0.0225', '0.0064', '1.04', '0.02415', '0.00472', '0.0263', '16.2', '0.025116', 'bt-w'])

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

    # p-colour-sensor (re-authored, finding 8): a leak, then a gain; the inverse of a product
    Ms = M([[R(7, 10), R(2, 10)], [R(1, 10), R(6, 10)]])
    Ds = M([[2, 0], [0, 1]])
    Mn, Dn = np.array([[0.7, 0.2], [0.1, 0.6]]), np.diag([2., 1.])
    Cs = Ds * Ms
    obj(I, 'p-colour-sensor', 1, Cs, Dn @ Mn, {'order': Ms * Ds, 'entrywise': Ds.multiply_elementwise(Ms)})
    corners = (Dn @ Mn) @ np.array([[0, 1, 1, 0], [0, 0, 1, 1.]])
    shoelace = 0.5 * abs(sum(corners[0, i] * corners[1, (i + 1) % 4] - corners[0, (i + 1) % 4] * corners[1, i] for i in range(4)))
    num(I, 'p-colour-sensor', 2, abs(Cs.det()), shoelace,
        {'added': Cs[0, 0] * Cs[1, 1] + Cs[0, 1] * Cs[1, 0], 'diagonal': Cs[0, 0] * Cs[1, 1], 'leak-only': abs(Ms.det())})
    ok(Cs.det() == Ds.det() * Ms.det() == R(4, 5) and Ds.det() == 2 and Ms.det() == R(2, 5), 'sensor p2: det C = det D x det M = 2 x 0.4 = 0.8')
    Ci = Cs.inv()
    obj(I, 'p-colour-sensor', 3, Ci, np.linalg.inv(Dn @ Mn),
        {'no-divide': adj(Cs), 'times-det': adj(Cs) * Cs.det(), 'no-negate': M([[R(3, 4), R(1, 2)], [R(1, 8), R(7, 4)]]), 'leak-only': Ms.inv()})
    ok(Ci == adj(Cs) / Cs.det() and (Ci * Cs)[0, 0] == 1 and R(75, 100) * R(14, 10) - R(5, 10) * R(1, 10) == 1, 'sensor p3: the 2 x 2 recipe and the check 1.05 - 0.05 = 1')
    rd = M([200, 60])
    tt = Ci * rd
    obj(I, 'p-colour-sensor', 4, tt.T, np.linalg.solve(Dn @ Mn, [200, 60.]),
        {'forward': (Cs * rd).T, 'leak-only': (Ms.inv() * rd).T, 'no-divide': (adj(Cs) * rd).T, 'swapped': M([[tt[1], tt[0]]])})
    ok(Ms * tt == M([100, 60]) and Ds * Ms * tt == rd, 'sensor p4: M(120, 80) = (100, 60); the gain doubles the red to (200, 60)')
    pick(I, 'p-colour-sensor', 5, 'gain-first')
    ok(Ms.inv() * Ds.inv() == Ci and Ds.inv() * Ms.inv() != Ci and Ds.inv() * rd == M([100, 60]) and Ms.inv() * M([100, 60]) == tt,
       'sensor p5: (DM)^-1 = M^-1 D^-1; D^-1 r = (100, 60); the other order is a different matrix')
    stale(I, 'p-colour-sensor', ['(130, 70)', '(140, 60)', '0.8&0.3', '0.56', '0.62', '182', 'Minv', 'linalg', '(70, 30)', '(125, 75)'])

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
    ok(sp.solve(2 + k_, k_) == [-2] and abs(float(sp.solve(added, k_)[0]) - (-2.444)) < 0.001 and abs(-2 - float(sp.solve(added, k_)[0])) <= 0.5,
       'engraver p3: k = -2 (2 + k = 0) lands on the added band, as the byKey line now says')
    ok('2 + k = 0' in part(I, 'p-engraver-dial', 3)['feedback']['byKey']['added'], 'engraver p3: the added line names the sign slip too')
    ok(all(f in part(I, 'p-engraver-dial', 1)['widget']['accept'] for f in ('[[2(k+3), 2+k], [5, 2]]', '[[2(3+k), 2+k], [5, 2]]')), 'engraver p1: factorised typings accepted')
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
