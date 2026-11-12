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


# ======================================================== level 2: projections
def qr_np(cols):
    """NumPy QR with the signs fixed so that diag(R) > 0, as Gram-Schmidt gives."""
    Q, Rm = np.linalg.qr(np.column_stack([npf(c).ravel() for c in cols]))
    D = np.diag(np.sign(np.diag(Rm)))
    return Q @ D, D @ Rm


I = load(2)
if I:
    # ---- p-grey-pixel
    iid = 'p-grey-pixel'
    g, b = M([1, 1, 1]), M([200, 140, 80])
    P = g * g.T / g.dot(g)
    Id = sp.eye(3)
    gb = npf(g).ravel()
    coef = np.linalg.lstsq(gb[:, None], npf(b).ravel(), rcond=None)[0][0]
    obj(I, iid, 1, P * b, coef * gb, {'no-divide': g * g.T * b})
    col = (Id - P) * b
    obj(I, iid, 2, col, npf(b).ravel() - coef * gb, {'reversed': -col, 'carried': b - g * g.T * b})
    ok(col.dot(g) == 0, 'grey: the colour part is orthogonal to g')
    F = P + R(1, 2) * (Id - P)
    Fn = np.outer(gb, gb) / 3 + 0.5 * (np.eye(3) - np.outer(gb, gb) / 3)
    Fb = F * b
    obj(I, iid, 3, Fb, Fn @ npf(b).ravel(), {'halved-all': b / 2, 'grey-halved': R(1, 2) * P * b + (Id - P) * b})
    ok(P * P == P and P * (Id - P) == sp.zeros(3, 3) and F * F == P + R(1, 4) * (Id - P), 'grey: P^2 = P and F^2 = P + (I - P)/4')
    obj(I, iid, 4, F * Fb, Fn @ (Fn @ npf(b).ravel()), {'projection': Fb, 'halved-twice-all': Fb / 2})
    vocab(I, iid, [g.dot(b), P * b, col, Fb, F * Fb, g * g.T * b, b - g * g.T * b, b / 2, R(1, 2) * P * b + (Id - P) * b,
                   Fb / 2, col / 2, col / 4, g.dot(b) / 3])
    arith(I, iid)

    # ---- p-power-line
    iid = 'p-power-line'
    a, b, J = M([4, 3]), M([2, 9]), M([8, 6])
    an, bn = npf(a).ravel(), npf(b).ravel()
    xh = a.dot(b) / a.dot(a)
    xn = np.linalg.lstsq(an[:, None], bn, rcond=None)[0][0]
    num(I, iid, 1, xh, xn, {'no-divide': a.dot(b), 'by-length': a.dot(b) / norm(a)})
    p = xh * a
    e = b - p
    obj(I, iid, 2, e, bn - xn * an, {'p-not-e': p, 'added': b + p, 'carried': b - (a.dot(b) / norm(a)) * a, 'sign': M([-e[0], e[1]])})
    ok(e.dot(a) == 0, 'power: e is perpendicular to a')
    dist = norm(e)
    num(I, iid, 3, dist, abs(an[0] * bn[1] - an[1] * bn[0]) / np.linalg.norm(an),
        {'along': norm(p), 'to-origin': norm(b), 'squared': e.dot(e)})
    ok(J == 2 * a, 'power: the pylon J = (8, 6) is on the line')
    extra = sp.sqrt(e.dot(e) + (p - J).dot(p - J)) - dist
    num(I, iid, 4, extra, np.linalg.norm(bn - npf(J).ravel()) - np.linalg.norm(bn - xn * an),
        {'added': norm(p - J), 'total': norm(b - J), 'squares': (b - J).dot(b - J) - e.dot(e)})
    vocab(I, iid, [a.dot(b), a.dot(a), 8, 27, xh, p, e, b + p, b - 7 * a, 7, dist, e.dot(e), norm(p), 85, norm(b), e[0] ** 2,
                   e[1] ** 2, e[0] * a[0], norm(p - J), (b - J).dot(b - J), norm(b - J), extra, J])
    arith(I, iid)

    # ---- p-solar-drone
    iid = 'p-solar-drone'
    a1, a2, b = M([1, 0, 2]), M([0, 1, 1]), M([-2, 1, 9])
    A = a1.row_join(a2)
    n = A.T.nullspace()[0]
    n = n / n[2]
    nn = np.cross(npf(a1).ravel(), npf(a2).ravel())
    obj(I, iid, 1, n, nn / nn[2], {'sign': M([-2, 1, 1]), 'one-edge': M([-a1[2] / a1[0], 0, 1])})
    e = (n.dot(b) / n.dot(n)) * n
    xn = np.linalg.lstsq(npf(A), npf(b).ravel(), rcond=None)[0]
    pn = npf(A) @ xn
    ns = M([-2, 1, 1])
    obj(I, iid, 2, e, npf(b).ravel() - pn, {'no-divide': n.dot(b) * n, 'carried': (ns.dot(b) / ns.dot(ns)) * ns})
    p = b - e
    obj(I, iid, 3, p, pn, {'added': b + e, 'carried': b - n.dot(b) * n})
    ok(A.T * (b - p) == M([0, 0]), 'solar: the error is perpendicular to both edges')
    x = A[:2, :].LUsolve(p[:2, :])
    ok(A * x == p, 'solar: p is in the plane')
    obj(I, iid, 4, x, xn, {'straight-down': b[:2, :], 'carried': (b + e)[:2, :]})
    ok(A.T * A == M([[5, 2], [2, 2]]) and A.T * b == M([16, 10]), 'solar: stated normal equations')
    ok(2 * (b + e)[0] + (b + e)[1] == -13, 'solar: the added point fails the plane test')
    vocab(I, iid, [n, n.dot(b), n.dot(n), e, p, b + e, b - n.dot(b) * n, (ns.dot(b) / ns.dot(ns)) * ns, ns.dot(b) / ns.dot(ns),
                   n.dot(b) * n, x, A.T * b, A.T * A, -13, 11])
    arith(I, iid)

    # ---- p-dye-mix
    iid = 'p-dye-mix'
    a1, a2, b = M([2, 3, 6]), M([8, 5, 3]), M([9, 17, 13])
    A = a1.row_join(a2)
    Qn, Rn = qr_np([a1, a2])
    q1 = a1 / norm(a1)
    r12 = q1.dot(a2)
    num(I, iid, 1, r12, Rn[0, 1], {'no-unit': a1.dot(a2), 'coefficient': a1.dot(a2) / a1.dot(a1)})
    v = a2 - r12 * q1
    q2 = v / norm(v)
    obj(I, iid, 2, q2, Qn[:, 1], {'not-normalised': v, 'used-a1': a2 - r12 * a1})
    Q = q1.row_join(q2)
    Rm = M([[norm(a1), r12], [0, norm(v)]])
    ok(Q * Rm == A and Rm == M([[7, 7], [0, 7]]), 'dye: A = QR with R = [[7, 7], [0, 7]]')
    Qtb = Q.T * b
    obj(I, iid, 3, Qtb, Qn.T @ npf(b).ravel(), {'a-not-q': A.T * b, 'used-a2': M([Qtb[0], a2.dot(b) / 7])})
    xh = Rm.LUsolve(Qtb)
    xl, res, _, _ = np.linalg.lstsq(npf(A), npf(b).ravel(), rcond=None)
    obj(I, iid, 4, xh, xl, {'top-down': M([Qtb[0] / Rm[0, 0], Qtb[1] / Rm[1, 1]]), 'transposed': Rm.T.LUsolve(Qtb)})
    ok(xh == (A.T * A).LUsolve(A.T * b), 'dye: QR agrees with the normal equations')
    e = b - A * xh
    slip = M([Qtb[0] / Rm[0, 0], Qtb[1] / Rm[1, 1]])
    num(I, iid, 5, norm(e), math.sqrt(res[0]),
        {'squared': e.dot(e), 'carried': norm(b - A * slip), 'lengths': norm(b) - norm(A * xh)})
    ok(e.dot(a1) == 0 and e.dot(a2) == 0 and b.dot(b) == Qtb.dot(Qtb) + e.dot(e), 'dye: miss perpendicular, Pythagoras')
    vocab(I, iid, [a1.dot(a2), r12, norm(a1), v, a2 - r12 * a1, r12 * q1, 16, 15, 18, 36, 9, Qtb, A.T * b, a2.dot(b) / 7,
                   18, 51, 78, 54, 34, 39, xh, slip, A * xh, e, e.dot(e), b.dot(b), Qtb.dot(Qtb), norm(b - A * slip),
                   norm(b) - norm(A * xh), e[0] * a1[0], e[1] * a1[1], e[2] * a1[2], e[0] * a2[0], e[1] * a2[1], e[2] * a2[2],
                   Rm[0, 1] * xh[1], Qtb[0]])
    arith(I, iid)


# ======================================================== level 3: least squares
def r2_exact(y, yhat):
    ybar = sum(y) / len(y)
    return 1 - sum((a - b) ** 2 for a, b in zip(y, yhat)) / sum((a - ybar) ** 2 for a in y)


I = load(3)
if I:
    # ---- p-runner-heart
    iid = 'p-runner-heart'
    xs = [8, 9, 10, 11, 12]
    ys = [128, 135, 139, 146, 152]
    xbar, ybar = R(sum(xs), 5), R(sum(ys), 5)
    dx = [x - xbar for x in xs]
    dy = [y - ybar for y in ys]
    sxy = sum(a * b for a, b in zip(dx, dy))
    sxx = sum(a * a for a in dx)
    xv, yv = np.array(xs, dtype=float), np.array(ys, dtype=float)
    num(I, iid, 1, sxy, np.cov(xv, yv, ddof=0)[0, 1] * 5, {'uncentred': sum(a * b for a, b in zip(xs, ys)), 'sxx': sxx})
    be = sxy / sxx
    pf = np.polyfit(xv, yv, 1)
    num(I, iid, 2, be, pf[0], {'over-n': sxy / 5, 'upside-down': sxx / sxy})
    al = ybar - be * xbar
    num(I, iid, 3, al, pf[1], {'sign': ybar + be * xbar, 'no-xbar': ybar - be})
    A5 = M([[1, x] for x in xs])
    ok((A5.T * A5).LUsolve(A5.T * M(ys)) == M([al, be]), 'runner: the normal equations give (81, 5.9)')
    xs6, ys6 = xs + [10], ys + [146]
    A6 = M([[1, x] for x in xs6])
    fit6 = (A6.T * A6).LUsolve(A6.T * M(ys6))
    pf6 = np.polyfit(np.array(xs6, dtype=float), np.array(ys6, dtype=float), 1)
    ok(fit6[1] == be and math.isclose(pf6[0], float(be)), 'runner: the slope stays 5.9 with the sixth run')
    ok(146 - (al + be * 10) == 6, 'runner: the sixth run is 6 above the line')
    pick(I, iid, 4, 'same')
    num(I, iid, 5, fit6[0], pf6[1], {'old': al, 'full-shift': al + 6, 'mean-only': R(sum(ys6), 6)})
    vocab(I, iid, [xbar, ybar, dx, dy, [a * b for a, b in zip(dx, dy)], sxy, sxx, sum(ys), sum(a * b for a, b in zip(xs, ys)),
                   be, sxy / 5, sxx / sxy, be * xbar, al, ybar + be * xbar, ybar - be, R(sum(ys6), 6), fit6[0], al + 6,
                   146 - (al + be * 10), [a * a for a in dx]])
    arith(I, iid)

    # ---- p-ramp-ball
    iid = 'p-ramp-ball'
    A = M([[1, 1], [1, 4], [1, 9]])
    b = M([R(65, 10), R(202, 10), R(463, 10)])
    y = A.T.nullspace()[0]
    y = 5 * y / y[0]
    yn = nullvec_np(A.T)
    yn = 5 * yn / yn[0]
    num(I, iid, 1, y[1], yn[1], {'sign': -y[1]})
    ok(y[2] == 3, 'ramp: y = (5, -8, 3)')
    e = (b.dot(y) / y.dot(y)) * y
    xl = np.linalg.lstsq(npf(A), npf(b).ravel(), rcond=None)[0]
    obj(I, iid, 2, e, npf(b).ravel() - npf(A) @ xl, {'no-divide': b.dot(y) * y, 'gave-p': b - e})
    p = b - e
    xh = A[:2, :].LUsolve(p[:2, :])
    ok(A * xh == p, 'ramp: p is in C(A)')
    obj(I, iid, 3, xh, xl, {'swapped': M([xh[1], xh[0]])})
    ok(A.T * A == M([[3, 14], [14, 98]]) and A.T * b == M([73, 504]) and (A.T * A) * xh == A.T * b, 'ramp: stated normal equations')
    pred = xh[0] + xh[1] * 25
    num(I, iid, 4, pred, np.array([1.0, 25.0]) @ xl,
        {'t-not-squared': xh[0] + xh[1] * 5, 'no-intercept': xh[1] * 25, 'swapped': xh[1] + xh[0] * 25})
    vocab(I, iid, [y, b.dot(y), y.dot(y), b.dot(y) / y.dot(y), e, b.dot(y) * y, p, xh, b[0] * y[0], b[1] * y[1], b[2] * y[2],
                   4 * y[1], 9 * y[2], A.T * A, A.T * b, pred, 25, xh[1] * 25, xh[0] + xh[1] * 5, xh[1] + xh[0] * 25, 9 * xh[1]])
    arith(I, iid)

    # ---- p-gas-hubs
    iid = 'p-gas-hubs'
    t = M([-1, 0, 1, 2, 3])
    yN = M([R(7, 2), 0, R(-1, 2), -3, -5])
    yS = M([2, 1, -2, -2, -4])
    A = M.hstack(sp.ones(5, 1), t)
    An = npf(A)
    G = A.T * A
    num(I, iid, 1, G[1, 1], (An.T @ An)[1, 1], {'sum': sum(t), 'sum-squared': sum(t) ** 2})
    ok(G == M([[5, 5], [5, 15]]) and A.T * yN == M([-5, -25]) and A.T * yS == M([-5, -20]), 'hubs: printed arrays')
    xN = G.LUsolve(A.T * yN)
    xS = G.LUsolve(A.T * yS)
    lN = np.linalg.lstsq(An, npf(yN).ravel(), rcond=None)[0]
    lS = np.linalg.lstsq(An, npf(yS).ravel(), rcond=None)[0]
    diag = lambda v: M([v[0] / G[0, 0], v[1] / G[1, 1]])
    obj(I, iid, 2, xN, lN, {'diagonal': diag(A.T * yN), 'swapped': M([xN[1], xN[0]]), 'no-sign': M([xN[0], -xN[1]])})
    obj(I, iid, 3, xS, lS, {'diagonal': diag(A.T * yS), 'no-sign': M([xS[0], -xS[1]])})
    sprd = yN - yS
    lD = np.linalg.lstsq(An, npf(sprd).ravel(), rcond=None)[0]   # route 2: fit the spread directly
    obj(I, iid, 4, xN - xS, lD, {'added': xN + xS, 'reversed': xS - xN})
    fit = A * (xN - xS)
    eD = sprd - fit
    ok(list(sprd) == [R(3, 2), -1, R(3, 2), -1, -1] and sum(sprd) == 0, 'hubs: stated spread, mean 0')
    eN, eS = yN - A * xN, yS - A * xS
    sstD = sum((v - sum(sprd) / 5) ** 2 for v in sprd)
    sseD = eD.dot(eD)
    num(I, iid, 5, r2_exact(list(sprd), list(fit)), np.corrcoef(npf(t).ravel(), npf(sprd).ravel())[0, 1] ** 2,
        {'ratio': sseD / sstD, 'added-sse': 1 - (eN.dot(eN) + eS.dot(eS)) / sstD, 'hub-n': r2_exact(list(yN), list(A * xN))})
    sstN = sum((v - sum(yN) / 5) ** 2 for v in yN)
    vocab(I, iid, [t, yN, yS, G, A.T * yN, A.T * yS, xN, xS, diag(A.T * yN), diag(A.T * yS), xN - xS, xN + xS, sprd, fit, eD,
                   sseD, sstD, r2_exact(list(sprd), list(fit)), sseD / sstD, eN.dot(eN), eS.dot(eS), eN.dot(eN) + eS.dot(eS),
                   1 - (eN.dot(eN) + eS.dot(eS)) / sstD, sstN, r2_exact(list(yN), list(A * xN)), 10, -20, -15, 25, 15, [v ** 2 for v in t]])
    arith(I, iid)


# ------------------------------------------------------------------ report
print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
