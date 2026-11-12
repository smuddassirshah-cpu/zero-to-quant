"""Recompute every number in app/content/courses/eigen/problems-<n>.json twice.

Route 1 is exact: sympy Rationals and Matrices (characteristic roots, nullspaces, exact
powers by diagonalisation). Route 2 is floating point by another method: NumPy
np.linalg.eig, eigh and svd, matrix_power, or direct iteration of the recurrence or chain.

Checks, per part (helpers taken from problems-least-squares-numbers.py):
- numeric: both routes agree; key within tol; the question names its form; each wrong value
  equals its named slip, lies outside the key band, and no two wrong bands overlap.
- numeric sets (answers, unordered): the set equals the computed set; each wrong set differs.
- expression (vectors typed whole): key and every accept form (a number in front of a vector
  is multiplied in) equal the exact answer; each wrong equals its slip and differs from the key.
- choice: the keyed option, and every distractor has a why.
Per item, over every learner-facing string: `arith` (every chain a = b = c of plain arithmetic
is evaluated) and `vocab` (every printed number is a given or a computed value).
Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-eigen-numbers.py
"""
import json, os, re, sys, itertools, math
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

TR = standard_transformations + (implicit_multiplication_application,)
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'eigen')
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
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'eigen', f'set {n}: header')
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
    m = re.match(r'^(.+?)\s*([\(\[][^()\[\]]*[\)\]])$', s)
    if m:
        return parse_entry(m.group(1)) * parse_obj(m.group(2))
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




def numset(items, iid, k, exact, alt, slips):
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'numeric' and w.get('unordered') is True, f'{tag}: not a numeric set')
    ex = sorted(float(x) for x in exact)
    ok(np.allclose(ex, sorted(np.real(alt)), atol=1e-9), f'{tag}: routes differ')
    ok(np.allclose(sorted(w['answers']), ex, atol=1e-12), f'{tag}: answers {w["answers"]} vs {ex}')
    got = {x['id']: sorted(float(t) for t in x['value'].split(',')) for x in w.get('wrong', [])}
    ok(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} vs {sorted(slips)}')
    ok(set(got) <= set(p['feedback'].get('byKey', {})), f'{tag}: byKey lines missing')
    for wid, val in slips.items():
        if wid in got:
            ok(np.allclose(got[wid], sorted(float(x) for x in val)), f'{tag}: wrong {wid} {got[wid]} vs slip {val}')
            ok(not np.allclose(got[wid], ex), f'{tag}: wrong {wid} equals the key')


def eigvals_np(A):
    return np.linalg.eigvals(npf(A))


def eigvec_np(A, lam, fix=-1):
    """Second route for an eigenvector: NumPy eig, scaled so entry `fix` is 1."""
    vals, vecs = np.linalg.eig(npf(A))
    i = int(np.argmin(abs(vals - float(lam))))
    x = np.real(vecs[:, i])
    return x / x[fix]


# ------------------------------------------------------------------ self-test of the text checks
_fake = {'t': {'prose': 'Costs £12.', 'parts': [{'question': 'q', 'widget': {'kind': 'numeric'}, 'feedback': {'correct': r'$2y = 7 - 3 = 5$ and $(1, 2) + (1, 1) = (2, 3)$', 'generic': 'g'}, 'explain': {'text': r'Here $x = 4/2 = 2$ and 47 appears.'}}]}}
_n = len(fails)
arith(_fake, 't')
vocab(_fake, 't', [4, 7])
ok(len(fails) == _n + 2 and 'false step' in fails[_n] and '47' in fails[_n + 1], 'self-test: arith and vocab catch planted faults')
del fails[_n:_n + 2]
ok(same(parse_obj(r'\frac{1}{5}(3, 2)'), M([[R(3, 5), R(2, 5)]])) and same(parse_obj('0.25(1, 2, 1)'), M([[R(1, 4), R(1, 2), R(1, 4)]])),
   'self-test: a number in front of a vector is multiplied in')


def scaled(x, entry=-1):
    x = M(x)
    return x / x[entry if entry >= 0 else len(x) + entry]


def null1(A, entry=-1):
    """Route 1 for an eigenvector: the exact nullspace, scaled so one entry is 1."""
    ns = M(A).nullspace()
    ok(len(ns) == 1, 'nullspace is not one-dimensional')
    return scaled(ns[0], entry)


# ======================================================== level 1: eigenvectors
I = load(1)
if I:
    # ---- p-sketch-warp
    iid = 'p-sketch-warp'
    b = sp.Symbol('b')
    Ab = M([[4, b], [1, -1]])
    v = M([3, 1])
    Av = Ab * v
    lam = Av[1] / v[1]
    num(I, iid, 1, lam, np.array([1.0, -1.0]) @ np.array([3.0, 1.0]), {'sign': 3 + 1})
    bval = sp.solve(sp.Eq(Av[0], lam * v[0]), b)[0]
    num(I, iid, 2, bval, (2.0 * 3 - 12.0), {'dropped-sign': -bval, 'wrong-entry': sp.solve(sp.Eq(Av[0], lam * v[1]), b)[0],
                                             'carried': sp.solve(sp.Eq(Av[0], 4 * v[0]), b)[0]})
    A = Ab.subs(b, bval)
    ok(A * v == lam * v, 'warp: v is an eigenvector with eigenvalue 2')
    ev = sorted(A.eigenvals().keys())
    mu = A.trace() - lam
    ok(ev == sorted([lam, mu]) and lam * mu == A.det(), 'warp: trace and determinant agree')
    others = [x for x in eigvals_np(A) if abs(x - 2) > 1e-6]
    num(I, iid, 3, mu, others[0], {'added': A.trace() + lam, 'trace-sign': (4 + 1) - lam, 'det-sign': (-4 - 6) / lam})
    x2 = null1(A - sp.eye(2))
    obj(I, iid, 4, x2, eigvec_np(A, 1), {'other': v, 'sign': M([-x2[0], 1]), 'swapped': M([x2[1], x2[0]])})
    w = M([5, 2])
    A4w = A ** 4 * w
    xs = v.row_join(M([-2, 1])).LUsolve(w)
    obj(I, iid, 5, A4w, np.linalg.matrix_power(npf(A), 4) @ npf(w).ravel(),
        {'one-warp': A * w, 'times-four': 4 * lam * v + 4 * mu * x2,
         'carried': lam ** 4 * xs[0] * v + mu ** 4 * xs[1] * M([-2, 1])})
    ok(w == v + x2 and A * M([-2, 1]) == M([-14, -3]), 'warp: w = v + x2; A(-2, 1) stated')
    vocab(I, iid, [Av.subs(b, bval), 4 * 3, lam * v[0], bval, -10, 4 * 3 - 6, A.det(), A - sp.eye(2), A * x2, 8 - 6,
                   A4w, 16 * v, A * w, 4 * lam * v + 4 * mu * x2, lam ** 4 * xs[0] * v + mu ** 4 * xs[1] * M([-2, 1]),
                   A * M([-2, 1]), 2 ** 4])
    arith(I, iid)

    # ---- p-garden-path
    iid = 'p-garden-path'
    A = M([[1, 6], [1, 0]])
    lamb = sp.Symbol('lambda')
    roots = sp.solve(A.charpoly(lamb).as_expr(), lamb)
    numset(I, iid, 1, roots, eigvals_np(A),
           {'sign': sp.solve(lamb ** 2 + lamb - 6, lamb), 'dropped-sign': [3, 2], 'diagonal': [A[0, 0], A[1, 1]]})
    x1 = null1(A - 3 * sp.eye(2))
    x2 = null1(A + 2 * sp.eye(2))
    obj(I, iid, 2, x1, eigvec_np(A, 3), {'other': x2, 'sign': M([-x1[0], 1])})
    u0 = M([1, 1])
    X = x1.row_join(x2)
    c = X.LUsolve(u0)
    obj(I, iid, 3, c, np.linalg.solve(npf(X), np.ones(2)),
        {'swapped': M([c[1], c[0]]), 'not-split': u0, 'carried': M([[-3, -2], [1, 1]]).LUsolve(u0)})
    t = [1, 1]
    for n in range(2, 13):
        t.append(t[-1] + 6 * t[-2])          # route 2: the recurrence itself

    def tn(n):
        return (X * sp.diag(3 ** n, (-2) ** n) * c)[1]
    ok(all(tn(n) == t[n] for n in range(12)), 'garden: closed form matches the recurrence')
    num(I, iid, 4, tn(10), float(t[10]),
        {'sign': c[0] * 3 ** 10 - c[1] * 2 ** 10, 'first-entry': (X * sp.diag(3 ** 10, 2 ** 10) * c)[0],
         'one-short': tn(9), 'swapped': c[1] * 3 ** 10 + c[0] * 2 ** 10})
    ok(t[11] == 105469 and t[2] == 7 and (X * sp.diag(3 ** 10, 2 ** 10) * c)[0] == t[11], 'garden: t_11 and t_2')
    vocab(I, iid, [A * x1, x1, x2, c, 3 ** 10, 2 ** 10, c[0] * 3 ** 10, c[1] * 2 ** 10, tn(10), 10, 7, 9, 6, -6,
                   c[1] * 3 ** 10 + c[0] * 2 ** 10, tn(9), t[11], c[0] * 3 ** 10 - c[1] * 2 ** 10])
    arith(I, iid)

    # ---- p-hill-bikes
    iid = 'p-hill-bikes'
    p = sp.Symbol('p')
    Mp = M([[1 - p, R(15, 100)], [p, R(85, 100)]])
    pval = sp.solve(sp.Eq((Mp * M([200, 400]))[0], 200), p)[0]

    def hill_share(pf):
        vals, vecs = np.linalg.eig(npf(Mp.subs(p, pf)))
        x = np.real(vecs[:, np.argmin(abs(vals - 1))])
        return x[0] / x.sum()
    lo, hi = 0.01, 0.99                      # route 2: bisection on the NumPy steady state
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if hill_share(mid) < 1 / 3 else (mid, hi)
    num(I, iid, 1, pval, (lo + hi) / 2, {'swapped': sp.solve(p * 400 - R(15, 100) * 200, p)[0],
                                         'total': sp.solve(p * 200 - R(15, 100) * 600, p)[0]})
    Mm = Mp.subs(p, pval)
    l2 = Mm.trace() - 1
    ok(sorted(Mm.eigenvals().keys()) == sorted([1, l2]) and Mm.det() == l2, 'bikes: eigenvalues 1 and 0.55, det 0.55')
    num(I, iid, 2, l2, min(eigvals_np(Mm)),
        {'trace': Mm.trace(), 'det-sign': Mm[0, 0] * Mm[1, 1] + Mm[0, 1] * Mm[1, 0],
         'carried': Mp.subs(p, R(75, 1000)).trace() - 1})
    s0 = M([600, 0])
    ok(s0 == M([200, 400]) + 400 * M([1, -1]) and Mm * M([1, -1]) == l2 * M([1, -1]), 'bikes: split and eigenvector')
    h2 = (Mm ** 2 * s0)[0]
    num(I, iid, 3, h2, 200 + 400 * float(l2) ** 2,
        {'one-night': (Mm * s0)[0], 'no-steady': 600 * l2 ** 2, 'river': (Mm ** 2 * s0)[1],
         'carried': 200 + 400 * R(775, 1000) ** 2})
    k = next(k for k in range(1, 40) if (Mm ** k * s0)[0] < 230)
    kf = math.ceil(math.log(30 / 400) / math.log(0.55))
    num(I, iid, 4, k, kf, {'rounded-down': k - 1, 'no-steady': next(j for j in range(1, 40) if 600 * l2 ** j < 30)})
    vocab(I, iid, [200, 400, 600, R(15, 100), pval, 200 * pval, Mm, Mm.trace(), Mm[0, 0] * Mm[1, 1], Mm[0, 1] * Mm[1, 0],
                   l2, R(64, 100), R(775, 1000), R(75, 1000), R(45, 100), Mm * s0, h2, 400 * l2 ** 2, l2 ** 2, 600 * l2 ** 2,
                   (Mm ** 2 * s0)[1], 200 + 400 * R(775, 1000) ** 2, 230, 30, round(float(l2 ** 4), 4),
                   400 * l2 ** 4, 200 + round(float(400 * l2 ** 4), 1), round(float(l2 ** 5), 4), round(float(400 * l2 ** 5), 1),
                   math.log(0.075) / math.log(0.55), 220, 15, 60, 0.7 * 420, 0.15 * 180])
    arith(I, iid)

    # ---- p-lazy-frog
    iid = 'p-lazy-frog'
    h = R(1, 2)
    Mf = M([[0, h, 0], [1, 0, 1], [0, h, 0]])
    s = null1(Mf - sp.eye(3))
    s = s / sum(s)
    vals, vecs = np.linalg.eig(npf(Mf))
    sn = np.real(vecs[:, np.argmin(abs(vals - 1))])
    obj(I, iid, 1, s, sn / sn.sum(), {'unscaled': M([1, 2, 1]), 'uniform': M([R(1, 3)] * 3)})
    xa, xb = M([1, -2, 1]), M([1, 0, -1])
    la = (Mf * xa)[0] / xa[0]
    ok(Mf * xa == la * xa and Mf * xb == sp.zeros(3, 1), 'frog: (1, -2, 1) and (1, 0, -1) are eigenvectors')
    num(I, iid, 2, la, (npf(Mf) @ npf(xa).ravel())[1] / -2.0, {'dropped-sign': -la, 'middle-entry': xa[1]})
    ok(sorted(Mf.eigenvals().keys()) == [-1, 0, 1], 'frog: eigenvalues 1, 0, -1')
    e1 = M([1, 0, 0])
    ok(all((Mf ** n * e1)[1] == 1 for n in (1, 3, 5)) and (Mf ** 2 * e1) != s, 'frog: never settles, on pad 2 at odd minutes')
    pick(I, iid, 3, 'flips')
    Lf = (sp.eye(3) + Mf) / 2
    lab = M([(Lf * xa)[0] / xa[0], (Lf * xb)[0] / xb[0]])
    lvals = sorted(np.linalg.eigvals(npf(Lf)).real)
    obj(I, iid, 4, lab, [lvals[0], lvals[1]],
        {'kept-m': M([la, 0]), 'no-half': 2 * lab, 'halved-only': M([la / 2, 0])})
    ok(e1 == s + h * xb + R(1, 4) * xa, 'frog: start split')
    p3 = (Lf ** 3 * e1)[0]
    num(I, iid, 5, p3, (np.linalg.matrix_power(npf(Lf), 3) @ np.array([1.0, 0, 0]))[0],
        {'half-dropped': s[0] + h ** 3, 'steady-only': s[0], 'not-lazy': (Mf ** 3 * e1)[0], 'carried': s[0] + h * 1})
    vocab(I, iid, [s, Mf * xa, Lf, h * h ** 3, h ** 3, p3, s[0] + h ** 3, R(2, 3), 0.25, 0.0625])
    arith(I, iid)




print(f"{checks} checks, {len(fails)} failures")
for f in fails:
    print("FAIL", f)
sys.exit(1 if fails else 0)
