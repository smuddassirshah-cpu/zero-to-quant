"""Recompute every number in app/content/courses/least-squares/problems-<n>.json twice.

Route 1 is exact: sympy Rationals and Matrices (dot products, nullspace, Gram-Schmidt by hand,
normal equations solved exactly). Route 2 is a different method in floating point: NumPy
(np.linalg.lstsq, np.linalg.qr, the SVD for null spaces, np.linalg.det, np.cross), never the
same formula as route 1 where another exists.

Checks, per part:
- numeric: both routes agree; the key lies within its tol of them; the question names its form;
  each `wrong` value equals what its named slip gives (to the 0.01 it is printed to), lies outside
  the key's band, and no two wrong bands overlap; every wrong id has a byKey line.
- expression (vectors typed whole): the key and every accept form equal the exact answer entry
  by entry; each wrong form equals its slip and differs from the key and from the other wrongs;
  a question whose answer has a non-whole entry names its form.
- choice: the keyed option, and every distractor has a why.
Per item, over every learner-facing string (prose, questions, feedback, byKey, explain, option
text and why):
- `arith`: every chain $a = b = c$ inside a maths span whose sides are plain arithmetic
  (numbers, + - x /, fractions, tuples) is evaluated, and consecutive sides must agree.
- `vocab`: every number printed must be a given of the item or a value this script computed
  for it (stale numbers fail); whole numbers 0 to 5 are free (entries, part numbers).
Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-least-squares-numbers.py
"""
import json, os, re, sys, itertools, math
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

TR = standard_transformations + (implicit_multiplication_application,)
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'least-squares')
fails, checks = [], 0
FORM = re.compile(r'decimal|places?\b|fraction|whole number|nearest|in pounds|per cent|%|exact', re.I)
R = sp.Rational
M = sp.Matrix
SYMS = {'k': sp.Symbol('k')}


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


# ------------------------------------------------------------------ loading
def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'least-squares', f'set {n}: header')
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


# ------------------------------------------------------------------ numeric parts
def num(items, iid, k, exact, alt, slips=None):
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e = float(exact)
    ok(math.isclose(e, float(alt), rel_tol=1e-9, abs_tol=1e-9), f'{tag}: routes differ {e} vs {float(alt)}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    ok(bool(FORM.search(p['question'])), f'{tag}: question states no form')
    slips = slips or {}
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    ok(set(wrongs) <= set(p['feedback'].get('byKey', {})), f'{tag}: byKey lines missing')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= 0.0051 + 1e-12, f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} inside the key band')
    for a, b in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a], wrongs[b]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a} and {b} overlap')
    return e


# ------------------------------------------------------------------ expression parts
def parse_entry(s):
    s = s.strip()
    s = re.sub(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    s = s.replace('\\sqrt', 'sqrt')
    return sp.nsimplify(parse_expr(s, local_dict=SYMS, transformations=TR), rational=True)


def parse_obj(s):
    """'(a, b)', '[a, b]' or '[[a, b], [c, d]]' -> sympy Matrix (a vector as one row)."""
    s = s.strip()
    if s.startswith('[['):
        rows = re.findall(r'\[([^\[\]]*)\]', s[1:-1])
        return M([[parse_entry(x) for x in r.split(',')] for r in rows])
    if s[0] in '([' and s[-1] in ')]':
        return M([[parse_entry(x) for x in s[1:-1].split(',')]])
    return M([[parse_entry(s)]])


def same(A, B):
    return A.shape == B.shape and all(sp.simplify(a - b) == 0 for a, b in zip(A, B))


def row(v):
    v = M(v)
    return v.T if v.shape[1] == 1 and v.shape[0] > 1 else v


def obj(items, iid, k, exact, alt, slips):
    """exact: sympy vector; alt: NumPy array from the second route."""
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    exact = row(exact)
    ok(np.allclose(np.array(exact.tolist(), dtype=float).ravel(), np.ravel(alt), atol=1e-9), f'{tag}: routes differ')
    for form in [w['answer']] + w.get('accept', []):
        ok(same(parse_obj(form), exact), f'{tag}: form {form} differs from the key')
    if any(not x.is_integer for x in exact):
        ok(bool(FORM.search(p['question'])), f'{tag}: non-whole entries but the question names no form')
    got = {x['id']: x['tex'] for x in w.get('wrong', [])}
    ok(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} vs {sorted(slips)}')
    ok(set(got) <= set(p['feedback'].get('byKey', {})), f'{tag}: byKey lines missing')
    for wid, val in slips.items():
        if wid not in got:
            continue
        g, v = parse_obj(got[wid]), row(val)
        ok(same(g, v), f'{tag}: wrong {wid} {got[wid]} vs slip {v.tolist()}')
        ok(not same(g, exact), f'{tag}: wrong {wid} equals the key')
    for a, b in itertools.combinations(list(got), 2):
        ok(not same(parse_obj(got[a]), parse_obj(got[b])), f'{tag}: wrongs {a} and {b} coincide')


def pick(items, iid, k, cid):
    opts = part(items, iid, k)['widget']['options']
    keyed = [o['id'] for o in opts if o.get('correct')]
    ok(keyed == [cid], f'{iid} p{k}: keyed {keyed}, expected {cid}')
    ok(all(o.get('why') for o in opts if not o.get('correct')), f'{iid} p{k}: a distractor has no why')


# ------------------------------------------------------------------ text checks
def strings(it):
    out = [('prose', it.get('prose', ''))]
    for k, p in enumerate(it['parts'], 1):
        out.append((f'p{k} question', p['question']))
        fb = p['feedback']
        out += [(f'p{k} correct', fb['correct']), (f'p{k} generic', fb['generic'])]
        out += [(f'p{k} byKey {a}', b) for a, b in fb.get('byKey', {}).items()]
        out.append((f'p{k} explain', p['explain']['text']))
        w = p['widget']
        for o in w.get('options', []):
            out += [(f'p{k} option {o["id"]}', o['text']), (f'p{k} why {o["id"]}', o.get('why', ''))]
    return out


def to_py(seg):
    s = seg.strip()
    s = s.replace('£', '').replace('\\,', '').replace('\\;', '').replace('\\!', '').replace('{,}', '')
    s = re.sub(r'\\(?:left|right)', '', s)
    s = re.sub(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    s = re.sub(r'\\sqrt\{([^{}]*)\}', r'np.sqrt(\1)', s)
    s = s.replace('\\times', '*').replace('\\cdot', '*').replace('−', '-').replace('^2', '**2')
    s = s.strip().rstrip('.,')
    if not s or re.search(r'[A-Za-z\\_^{}]', s.replace('np.sqrt', '').replace('np.array', '')):
        return None
    s = re.sub(r'(?<!sqrt)\(([^()]*,[^()]*)\)', r'np.array([\1])', s)
    s = re.sub(r'(\d)\s*(np\.array|\()', r'\1*\2', s)
    try:
        v = eval(s, {'np': np})
    except Exception:
        return None
    return np.asarray(v, dtype=float)


def arith(items, iid):
    for where, text in strings(items[iid]):
        for span in re.findall(r'\$\$?([^$]+)\$\$?', text):
            for chain in re.split(r'\\quad|\\qquad|,\s+(?=[a-z]_?\{?\d)|\\text\{[^}]*\}|\\approx', span):
                sides = [to_py(x) for x in re.split(r'(?<![<>!\\])=', chain)]
                for a, b in zip(sides, sides[1:]):
                    if a is not None and b is not None:
                        ok(a.shape == b.shape and np.allclose(a, b, atol=0.006), f'{iid} {where}: false step in ${chain}$')


def numbers_in(text):
    t = re.sub(r'_\{[^}]*\}|_\d|\^\{[^}]*\}|\^\d', '', text)
    t = re.sub(r'\\[dt]?frac\{(-?\d+)\}\{(\d+)\}', r' \1 / \2 ', t)
    t = re.sub(r'\\tfrac1(\d)', r' 1 / \1 ', t)
    t = t.replace('{,}', '')
    return [float(x) for x in re.findall(r'(?<![\w.])-?\d+(?:\.\d+)?', t)]


def vocab(items, iid, values):
    """Every number printed in the item is a given (prose or question 1) or a computed value."""
    it = items[iid]
    allowed = set()

    def add(x):
        x = sp.sympify(x)
        if x.free_symbols:
            for a in x.atoms(sp.Number):
                allowed.add(round(float(a), 2))
        else:
            allowed.add(round(float(x), 2))

    for v in values:
        if isinstance(v, (sp.MatrixBase, list, tuple, np.ndarray)):
            for x in (M(v) if not isinstance(v, np.ndarray) else v.ravel()):
                add(x)
        else:
            add(v)
    given = set(round(x, 2) for x in numbers_in(it.get('prose', '')))
    for where, text in strings(it):
        for x in numbers_in(text):
            r = round(x, 2)
            if abs(r) <= 5 and r == int(r):
                continue
            ok(r in allowed or r in given or -r in allowed or -r in given,
               f'{iid} {where}: number {x} is neither given nor computed')


def npf(A):
    return np.array(M(A).tolist(), dtype=float)


def nullvec_np(A):
    """Second route for a one-dimensional null space: the last right singular vector."""
    _, s, vt = np.linalg.svd(npf(A))
    return vt[-1]


def gs_exact(cols):
    """Classical Gram-Schmidt in exact arithmetic: returns the unnormalised e_k."""
    es = []
    for a in cols:
        a = M(a)
        e = a - sum(((a.dot(f) / f.dot(f)) * f for f in es), sp.zeros(a.shape[0], 1))
        es.append(e)
    return es


def gs_np(cols):
    """Second route: NumPy's Householder QR; R[k, k] q_k is e_k whatever the signs."""
    Q, Rm = np.linalg.qr(np.column_stack([npf(c).ravel() for c in cols]))
    return [Rm[k, k] * Q[:, k] for k in range(Rm.shape[0])], Q, Rm


def norm(v):
    return sp.sqrt(M(v).dot(M(v)))


# ------------------------------------------------------------------ self-test of the text checks
_fake = {'t': {'prose': 'Costs £12.', 'parts': [{'question': 'q', 'widget': {'kind': 'numeric'}, 'feedback': {'correct': r'$2y = 7 - 3 = 5$ and $(1, 2) + (1, 1) = (2, 3)$', 'generic': 'g'}, 'explain': {'text': r'Here $x = 4/2 = 2$ and 47 appears.'}}]}}
_n = len(fails)
arith(_fake, 't')
vocab(_fake, 't', [4, 7])
ok(len(fails) == _n + 2 and 'false step' in fails[_n] and '47' in fails[_n + 1], 'self-test: arith and vocab catch planted faults')
del fails[_n:_n + 2]


# ======================================================== level 1: orthogonality
I = load(1)
if I:
    # ---- p-hall-drone
    iid = 'p-hall-drone'
    a1, a2 = M([1, 2, 1]), M([1, 0, -1])
    A = a1.row_join(a2)
    ok(a1.dot(a2) == 0, 'hall: the directions are orthogonal')
    y = A.T.nullspace()[0]
    y = y / y[0]
    yn = nullvec_np(A.T)
    yn = yn / yn[0]
    cs = -1                                   # slip: 1 + c = 0 read from 1 - c = 0
    obj(I, iid, 1, y, yn, {'sign': M([1, (-1 - cs) / 2, cs]), 'b-sign': M([1, (1 + 1) / 2, 1])})
    c = sp.Symbol('c')
    cval = sp.solve(y.dot(M([4, 6, c])), c)[0]
    num(I, iid, 2, cval, -(yn[0] * 4 + yn[1] * 6) / yn[2], {'sign': 4 - 6, 'added': 4 + 6})
    b = M([4, 6, cval])
    x = M([b.dot(a1) / a1.dot(a1), b.dot(a2) / a2.dot(a2)])
    xn = np.linalg.lstsq(npf(A), npf(b).ravel(), rcond=None)[0]
    ok(A * x == b, 'hall: the plan reaches (4, 6, 2)')
    obj(I, iid, 3, x, xn, {'no-divide': A.T * b, 'sign-x2': M([x[0], (4 + 2) / R(2)])})
    B = A.row_join(y)
    b2 = M([4, 6, 5])
    x3 = B.LUsolve(b2)
    Qb, Rb = np.linalg.qr(npf(B))
    x3n = np.linalg.solve(Rb, Qb.T @ npf(b2).ravel())
    ok(all(B[:, i].dot(B[:, j]) == 0 for i, j in [(0, 1), (0, 2), (1, 2)]), 'hall: three orthogonal directions')
    ok(y.dot(b2) != 0, 'hall: (4, 6, 5) is out of reach of two directions')
    obj(I, iid, 4, x3, x3n, {'kept-plan': M([x[0], x[1], x3[2]]), 'no-divide-y': M([x3[0], x3[1], y.dot(b2)]),
                             'no-divide': B.T * b2, 'sign': M([x3[0], -x3[1], x3[2]])})
    vocab(I, iid, [y, cval, b, x, A.T * b, a1.dot(a1), a2.dot(a2), x3, B.T * b2, y.dot(b2), b2 - b,
                   M([1, 2, 1]).dot(M([1, 1, 1])), 4 - 6 - 2, 21 / R(6), y.dot(y), B.LUsolve(b2 - b), x3[1]])
    arith(I, iid)

    # ---- p-station-codes
    iid = 'p-station-codes'
    c1, c2, c3 = M([1, 1, 1, 1]), M([1, -1, 1, -1]), M([1, 1, -1, -1])
    C3 = M.hstack(c1, c2, c3)
    c4 = C3.T.nullspace()[0]
    c4 = c4 / c4[0]
    c4n = nullvec_np(C3.T)
    c4n = c4n / c4n[0]
    ok(c2.dot(c1) == 0 and c2.dot(c2) != 0, 'codes: c2 passes against c1 only')
    obj(I, iid, 1, c4, c4n, {'c1-only': c2, 'flipped': -c4})
    C = C3.row_join(c4)
    xs = M([3, 1, -1, 2])
    r = C * xs
    ok(list(r) == [5, -1, 3, 5], 'codes: r = (5, -1, 3, 5) from readings (3, 1, -1, 2)')
    xl = np.linalg.lstsq(npf(C), npf(r).ravel(), rcond=None)[0]
    num(I, iid, 2, r.dot(c4) / c4.dot(c4), xl[3], {'no-divide': r.dot(c4), 'by-length': r.dot(c4) / norm(c4)})
    dec = M([r.dot(C[:, i]) / C[:, i].dot(C[:, i]) for i in range(4)])
    obj(I, iid, 3, dec, xl, {'no-divide': C.T * r, 'by-length': C.T * r / 2, 'sign': M([dec[0], dec[1], -dec[2], dec[3]])})
    xnew = M([3, 4, -1, 2])
    rise = sum(xnew[i] ** 2 * C[:, i].dot(C[:, i]) for i in range(4)) - sum(xs[i] ** 2 * C[:, i].dot(C[:, i]) for i in range(4))
    rnew = npf(C) @ npf(xnew).ravel()
    num(I, iid, 4, rise, rnew @ rnew - npf(r).ravel() @ npf(r).ravel(),
        {'cross-term': (3 * c2).dot(3 * c2), 'no-four': sum(t ** 2 for t in xnew) - sum(t ** 2 for t in xs)})
    ok(list(C * xnew) == [8, -4, 6, 2] and (C * xnew).dot(C * xnew) == 120 and r.dot(r) == 60, 'codes: stated powers')
    vocab(I, iid, [c4, r, r.dot(c4), C.T * r, dec, rise, sum(t ** 2 for t in xnew), xnew[1] ** 2, 4 * 15, 4 * 30, C * xnew, 16 - 1, 36, 120, 60, 8 / R(4)])
    arith(I, iid)

    # ---- p-crystal-cell
    iid = 'p-crystal-cell'
    a1, a2, a3 = M([2, 1, 2]), M([6, 0, 3]), M([5, 1, -1])
    e1, e2, e3 = gs_exact([a1, a2, a3])
    en, Qn, Rn = gs_np([a1, a2, a3])
    t = a2.dot(a1) / a1.dot(a1)
    obj(I, iid, 1, e2, en[1], {'length-not-squared': a2 - (a2.dot(a1) / norm(a1)) * a1, 'added': a2 + t * a1})
    area = norm(a1) * norm(e2)
    num(I, iid, 2, area, np.linalg.norm(np.cross(npf(a1).ravel(), npf(a2).ravel())),
        {'slanted': norm(a1) * norm(a2), 'triangle': area / 2})
    q1, q2 = a1 / norm(a1), e2 / norm(e2)
    orig = a3 - (a3.dot(a1) / a1.dot(a1)) * a1 - (a3.dot(a2) / a2.dot(a2)) * a2
    obj(I, iid, 3, e3, en[2], {'originals': orig, 'unit-skipped': a3 - a3.dot(q1) * q1 - a3.dot(e2) * e2})
    ok(orig == M([R(-3, 5), 0, R(-24, 5)]), 'cell: the originals slip is (-0.6, 0, -4.8)')
    vol = area * norm(e3)
    detn = abs(np.linalg.det(np.column_stack([npf(a1).ravel(), npf(a2).ravel(), npf(a3).ravel()])))
    num(I, iid, 4, vol, detn, {'no-straightening': norm(a1) * norm(a2) * norm(a3), 'squared': area * e3.dot(e3),
                               'carried': area * norm(orig)})
    ok(M.hstack(a1, a2, a3).det() == vol, 'cell: det of the edges is 27')
    vocab(I, iid, [e2, a2.dot(a1), a1.dot(a1), t * a1, a2 + t * a1, a2 - 6 * a1, area, a2.dot(a2), 18 / R(3),
                   a3.dot(q1), a3.dot(q2), a3.dot(e2), a3.dot(a1), e2.dot(e2), 9 * e2, e3, orig, vol, a3.dot(q1) * q1, a3.dot(q2) * q2, 20.12, 104.57, 43.54, 81])
    arith(I, iid)

    # ---- p-rotor-changes
    iid = 'p-rotor-changes'
    A = M([[1, 1, 1, 1], [0, 1, 0, -1]])
    s1, s2 = A.nullspace()
    ok(list(s1) == [-1, 0, 1, 0], 'rotor: s1 is the special solution with x3 = 1')
    Nn = np.linalg.svd(npf(A))[2][2:].T          # orthonormal basis of N(A), route 2
    coef = np.linalg.solve(Nn[2:, :], np.array([0.0, 1.0]))
    s2n = Nn @ coef
    roll_slip = M([-(-1 + 0 + 1), -1, 0, 1])
    obj(I, iid, 1, s2, s2n, {'roll-sign': roll_slip, 'lift-short': M([-(0 + 1), 1, 0, 1]), 'no-minus': M([1 + 0 + 1, 1, 0, 1])})
    _, e2 = gs_exact([s1, s2])
    en, _, _ = gs_np([s1, s2])
    obj(I, iid, 2, e2, en[1], {'no-divide': s2 - s2.dot(s1) * s1, 'added': s2 + (s2.dot(s1) / s1.dot(s1)) * s1,
                               'carried': gs_exact([s1, roll_slip])[1]})
    r1, r2 = A[0, :].T, A[1, :].T
    basis = M.hstack(r1, r2, s1, e2)
    ok(all(basis[:, i].dot(basis[:, j]) == 0 for i in range(4) for j in range(i + 1, 4)), 'rotor: four orthogonal vectors')
    d = M([4, 0, 2, -2])
    co = np.linalg.lstsq(npf(basis), npf(d).ravel(), rcond=None)[0]
    ce2 = d.dot(e2) / e2.dot(e2)
    num(I, iid, 3, ce2, co[3], {'no-divide': d.dot(e2), 'by-length': d.dot(e2) / norm(e2), 'no-sign': -ce2})
    cs1 = d.dot(s1) / s1.dot(s1)
    safe = cs1 * s1 + ce2 * e2
    safen = Nn @ (Nn.T @ npf(d).ravel())        # route 2: orthonormal projector from the SVD
    ok(A * safe == M([0, 0]), 'rotor: the safe part keeps lift and roll')
    obj(I, iid, 4, safe, safen, {'row-part': d - safe, 'e2-only': ce2 * e2,
                                 'used-s2': cs1 * s1 + (d.dot(s2) / s2.dot(s2)) * s2})
    vocab(I, iid, [s1, s2, e2, d, ce2, cs1, d.dot(e2), d.dot(s1), safe, d - safe, ce2 * e2, cs1 * s1, s2 - 2 * s1,
                   s2 + s1, roll_slip, e2.dot(e2), s2.dot(s1), 4 - 2])
    arith(I, iid)


# ------------------------------------------------------------------ report
print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
