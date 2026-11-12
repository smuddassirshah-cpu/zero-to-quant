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
    terms, depth, cur = [], 0, ''
    for ch in s:                                   # a sum of terms such as 16(3, 1) + (2, 1)
        depth += ch in '([{'
        depth -= ch in ')]}'
        if ch == '+' and depth == 0 and cur.strip():
            terms.append(cur)
            cur = ''
        else:
            cur += ch
    terms.append(cur)
    if len(terms) > 1:
        return sum((parse_obj(x) for x in terms[1:]), parse_obj(terms[0]))
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
ok(same(parse_obj('16(3, 1) + (2, 1)'), M([[50, 17]])) and same(parse_obj('(48, 16) + (2, 1)'), M([[50, 17]])),
   'self-test: a number times a vector plus a vector is added up')


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
        {'kept-m': M([la, 0]), 'no-half': 2 * lab, 'halved-only': M([la / 2, 0]), 'order': M([lab[1], lab[0]])})
    ok(e1 == s + h * xb + R(1, 4) * xa, 'frog: start split')
    p3 = (Lf ** 3 * e1)[0]
    num(I, iid, 5, p3, (np.linalg.matrix_power(npf(Lf), 3) @ np.array([1.0, 0, 0]))[0],
        {'half-dropped': s[0] + h ** 3, 'steady-only': s[0], 'not-lazy': (Mf ** 3 * e1)[0], 'carried': s[0] + h * 1})
    vocab(I, iid, [s, Mf * xa, Lf, h * h ** 3, h ** 3, p3, s[0] + h ** 3, R(2, 3), 0.25, 0.0625])
    arith(I, iid)




# ======================================================== level 2: symmetric matrices
from sympy.parsing.sympy_parser import convert_xor


def poly(items, iid, k, exact, values, slips):
    """An expression part holding a polynomial: key and accept forms equal `exact`; route 2 is
    `values`, a list of (point, NumPy value) pairs; each wrong equals its slip and differs."""
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    rr = sp.Symbol('r')
    P = lambda s: parse_expr(s, local_dict={'r': rr}, transformations=TR + (convert_xor,))
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    for x, val in values:
        ok(abs(float(exact.subs(rr, x)) - val) < 1e-9, f'{tag}: routes differ at r = {x}')
    for form in [w['answer']] + w.get('accept', []):
        ok(sp.expand(P(form) - exact) == 0, f'{tag}: form {form} differs from the key')
    got = {x['id']: P(x['tex']) for x in w.get('wrong', [])}
    ok(set(got) == set(slips) and set(got) <= set(p['feedback'].get('byKey', {})), f'{tag}: wrong ids or byKey lines')
    for wid, val in slips.items():
        ok(sp.expand(got[wid] - val) == 0 and sp.expand(got[wid] - exact) != 0, f'{tag}: wrong {wid}')


I = load(2)
if I:
    # ---- p-oval-pond
    iid = 'p-oval-pond'
    x, y = sp.symbols('x y')
    A = M([[5, 2], [2, 8]])
    X2 = M([x, y])
    ok(sp.expand((X2.T * A * X2)[0] - (5 * x ** 2 + 4 * x * y + 8 * y ** 2)) == 0, 'pond: A gives the stated form')
    f = lambda a, b: 5 * a * a + 4 * a * b + 8 * b * b
    hxy = (f(1, 1) - f(1, -1) - f(-1, 1) + f(-1, -1)) / 4.0 / 2.0   # route 2: half the mixed second difference
    num(I, iid, 1, A[0, 1], hxy, {'whole-cross': 2 * A[0, 1]})
    numset(I, iid, 2, sp.solve(A.charpoly(sp.Symbol('l')).as_expr(), sp.Symbol('l')), np.linalg.eigvalsh(npf(A)),
           {'diagonal': [5, 8], 'sign': [-4, -9]})
    ql = null1(A - 4 * sp.eye(2), 0) * 2
    qn = eigvec_np(A, 4, 0) * 2
    obj(I, iid, 3, ql, qn, {'big': null1(A - 9 * sp.eye(2), 0) * 2, 'sign': M([2, -ql[1]])})
    ok(ql.dot(null1(A - 9 * sp.eye(2))) == 0, 'pond: the axes are perpendicular')
    u = ql / ql.norm()
    half = sp.sqrt(R(36, 4))
    un = np.array([2.0, -1.0]) / np.sqrt(5)
    tn = np.sqrt(36 / (un @ npf(A) @ un))                           # route 2: walk out along the unit vector
    num(I, iid, 4, half, tn, {'short': sp.sqrt(R(36, 9)), 'no-root': R(36, 4), 'full-axis': 2 * half})
    ok(sp.simplify((u.T * A * u)[0] * half ** 2 - 36) == 0, 'pond: (3 u) is on the edge')
    area = sp.pi * half * sp.sqrt(R(36, 9))
    num(I, iid, 5, area, np.pi * 36 / np.sqrt(np.linalg.det(npf(A))),
        {'no-root': sp.pi * 9 * 4, 'full-axes': sp.pi * 6 * 4, 'one-axis': sp.pi * 9})
    vocab(I, iid, [A, 13, A.det(), 40, 36, 6, 9, area, sp.pi * 36, 2 * half])
    arith(I, iid)

    # ---- p-river-gauges (re-authored twice in fix passes; now K = [[8, 4, 4], [4, 7, 3], [4, 3, c]] with planned c = 2.5)
    iid = 'p-river-gauges'
    c = sp.Symbol('c')
    K = M([[8, 4, 4], [4, 7, 3], [4, 3, c]])
    Kn = lambda cv: np.array([[8, 4, 4], [4, 7, 3], [4, 3, cv]], dtype=float)
    ok(re.search(r'\\begin\{pmatrix\} 8 & 4 & 4', I[iid]['prose']) is not None and '2.5' in I[iid]['prose'], 'gauges: the current matrix and c = 2.5 are in the prose')
    # part 1: the second pivot. Route 1 exact elimination; route 2 the corner determinant over the first pivot
    m21 = K[1, 0] / K[0, 0]
    piv2 = K[1, 1] - m21 * K[0, 1]
    num(I, iid, 1, piv2, np.linalg.det(Kn(0)[:2, :2]) / 8.0, {'multiplier-one': K[1, 1] - K[0, 1], 'multiplier-two': K[1, 1] - K[1, 0] * K[0, 1]})
    ok(K[:2, :2].det() == 40 and 8 * piv2 == 56 - 16 == 40, 'gauges: corner determinant 8 x 5 = 56 - 16 = 40')
    # part 2: the third pivot c - d. Route 1 exact elimination; route 2 NumPy det K over the corner determinant at three values of c
    r2 = [0, piv2, K[1, 2] - m21 * K[0, 2]]
    ok(r2 == [0, 5, 1], 'gauges: row 2 after step 1 is (0, 5, 1)')
    m31 = K[2, 0] / K[0, 0]
    r3 = [0, K[2, 1] - m31 * K[0, 1], K[2, 2] - m31 * K[0, 2]]
    ok(r3 == [0, 1, c - 2], 'gauges: row 3 after step 1 is (0, 1, c - 2)')
    m32 = r3[1] / r2[1]
    ok(m32 == R(1, 5), 'gauges: second multiplier 1 / 5 = 0.2')
    piv3 = sp.expand(r3[2] - m32 * r2[2])
    dval = -(piv3 - c)
    detK = sp.expand(K.det())
    ok(detK == 40 * c - 88 and sp.expand(8 * piv2 * piv3 - detK) == 0, 'gauges: det K = 40c - 88 = 40(c - 2.2)')
    d_np = [-(np.linalg.det(Kn(cv)) / np.linalg.det(Kn(0)[:2, :2]) - cv) for cv in (0.0, 2.5, 4.0)]
    ok(np.allclose(d_np, 2.2), 'gauges: NumPy det K over the corner determinant gives c - 2.2 at three values of c')
    num(I, iid, 2, dval, d_np[1], {'one-step': -(r3[2] - c), 'big-multiplier': -((r3[2] - 1 * r2[2]) - c),
                                   'added': -((r3[2] + m32 * r2[2]) - c)})
    # part 3: the null vector at c = 2.2. Route 1 exact nullspace; route 2 the last right singular vector
    Kb = K.subs(c, dval)
    wv = null1(Kb)
    _, _, vt = np.linalg.svd(Kn(float(dval)))
    obj(I, iid, 3, wv, vt[-1] / vt[-1][-1],
        {'sign': M([-wv[0], -wv[1], 1]), 'swapped': M([wv[1], wv[0], 1]), 'no-b': M([-R(4, 8), wv[1], 1])})
    ok(wv == M([-R(2, 5), -R(1, 5), 1]) and Kb * wv == sp.zeros(3, 1), 'gauges: w = (-0.4, -0.2, 1) and K(2.2) w = 0')
    ok(4 * wv[0] + 3 * wv[1] + dval == 0 and 4 * wv[0] == R(-8, 5) and 3 * wv[1] == R(-3, 5), 'gauges: row 3 check -1.6 - 0.6 + 2.2 = 0')
    ok(Kb.rank() == 2, 'gauges: K(2.2) is singular')
    # part 4: w^T K w at the planned c = 2.5
    C5 = R(5, 2)
    K5 = K.subs(c, C5)
    var4 = (wv.T * K5 * wv)[0]
    ok(K5 * wv == M([0, 0, R(3, 10)]), 'gauges: K(2.5) w = (0, 0, 0.3)')
    ok([8 * wv[0], 4 * wv[1], 4 * wv[0], 7 * wv[1], 3 * wv[1]] == [R(-16, 5), R(-4, 5), R(-8, 5), R(-7, 5), R(-3, 5)], 'gauges: printed products -3.2, -0.8, -1.6, -1.4, -0.6')
    wn = np.array([-0.4, -0.2, 1.0])
    ws = M([-wv[0], -wv[1], 1])
    num(I, iid, 4, var4, wn @ Kn(2.5) @ wn, {'c-only': C5, 'sign': (ws.T * K5 * ws)[0], 'boundary': dval})
    ok(sp.expand((wv.T * K * wv)[0] - (c - dval)) == 0, 'gauges: w^T K w = c - 2.2')
    # part 5: the share explained. Route 1 exact; route 2 the R-squared of C on A and B with NumPy
    share = 1 - var4 / C5
    Kc = Kn(2.5)
    beta = np.linalg.solve(Kc[:2, :2], Kc[:2, 2])
    r2_np = beta @ Kc[:2, 2] / Kc[2, 2]
    num(I, iid, 5, share, r2_np, {'unexplained': var4 / C5, 'not-scaled': 1 - var4})
    ok(np.allclose(beta, [0.4, 0.2]) and share == dval / C5, 'gauges: C = 0.4A + 0.2B in the regression, and the share is 2.2 / c')
    ok(np.linalg.eigvalsh(Kn(2.5)).min() > 0 and abs(np.linalg.eigvalsh(Kn(2.2)).min()) < 1e-12, 'gauges: positive definite at c = 2.5, singular at c = 2.2')
    vocab(I, iid, [K, 56, 16, 40, 88, piv2, r2, r3, m21, m32, dval, piv3, wv, ws, 8 * wv[0], 4 * wv[1], 4 * wv[0], 7 * wv[1], 3 * wv[1],
                   K5 * wv, var4, C5, (ws.T * K5 * ws)[0], share, var4 / C5, 1 - var4, C5 - var4, -9, 1.8, R(-1, 2), 2.2, 2.5])
    arith(I, iid)
    # stale-value check: nothing of the two earlier versions (r = 0.2 and bound 0.28; then c - 0.375 and w = (-0.125, -0.25, 1)) is left
    old_tokens = [r'0\.28', r'1\.28', r'-0\.16', r'0\.36', r'0\.64', r'0\.72', r'r = 0\.2', r'correlation', r'2\.56', r'4\.56', r'standardis',
                  r'0\.375', r'0\.125', r'0\.25(?!\d)', r'1\.6, 1']
    blob = ' '.join(t for _, t in strings(I[iid]))
    for tok in old_tokens:
        ok(not re.search(tok, blob), f'{iid}: stale token {tok} still in the item')

    # ---- p-tank-thermometers
    iid = 'p-tank-thermometers'
    S = M([[3, 1, 1], [1, 3, 1], [1, 1, 3]])
    ev = np.linalg.eigvalsh(npf(S))
    one = M([1, 1, 1])
    l1 = (S * one)[0]
    ok(S * one == l1 * one, 'thermo: (1, 1, 1) is an eigenvector')
    num(I, iid, 1, l1, ev[-1], {'diagonal': 3, 'all-entries': sum(S * one)})
    xb = M([1, -1, 0])
    l2 = (S * xb)[0]
    ok(S * xb == l2 * xb and xb.dot(one) == 0, 'thermo: (1, -1, 0) is an eigenvector, perpendicular to (1, 1, 1)')
    num(I, iid, 2, l2, ev[0], {'added': 3 + 1, 'sign': (S * xb)[1]})
    l3 = S.trace() - l1 - l2
    num(I, iid, 3, l3, ev[1], {'no-second': S.trace() - l1, 'no-first': S.trace() - l2})
    w = one / 3
    v4 = (w.T * S * w)[0]
    num(I, iid, 4, v4, npf(w).ravel() @ npf(S) @ npf(w).ravel(), {'no-length': l1, 'ninth': l1 / 9})
    wt = M([R(6, 10), R(25, 100), R(15, 100)])
    dd = wt - w
    ok(sum(dd) == 0 and dd == M([R(4, 15), R(-1, 12), R(-11, 60)]) and dd.dot(dd) == R(67, 600), 'thermo: d and |d|^2')
    v5 = (wt.T * S * wt)[0]
    ok(v5 == v4 + l2 * dd.dot(dd), 'thermo: the two parts add')
    num(I, iid, 5, v5, npf(wt).ravel() @ npf(S) @ npf(wt).ravel(),
        {'no-eigenvalue': v4 + dd.dot(dd), 'd-only': l2 * dd.dot(dd), 'no-cov': 3 * wt.dot(wt)})
    ok(v5 == R(189, 100) and wt.dot(wt) == R(445, 1000) and wt[0] * wt[1] + wt[0] * wt[2] + wt[1] * wt[2] == R(2775, 10000), 'thermo: 1.89, 0.445 and 0.2775')
    ok(abs(float(3 * wt.dot(wt)) - 1.335) < 1e-12 and abs(float(2 * (wt[0] * wt[1] + wt[0] * wt[2] + wt[1] * wt[2])) - 0.555) < 1e-12, 'thermo: 1.335 and 0.555')
    stale = [r'0\.0467', r'0\.093', r'0\.62', r'0\.38', r'0\.31', r'1\.76', r'0\.5, 0\.3', r'0\.06']
    blob = ' '.join(t for _, t in strings(I[iid]))
    for tok in stale:
        ok(not re.search(tok, blob), f'{iid}: stale token {tok} from the old weights')
    vocab(I, iid, [S * one, S * xb, S.trace(), l3, v4, w.dot(w), dd, dd.dot(dd), 600, 67, 12, 11, 60, v5, l2 * dd.dot(dd), R(445, 1000),
                   R(2775, 10000), 3 * R(445, 1000), 2 * R(2775, 10000), wt, R(15, 100), R(9, 100), R(375, 10000), 0.1, 6, 30, 15,
                   round(float(dd.dot(dd)), 4), round(float(2 * dd.dot(dd)), 3), 2 * (wt[0] * wt[1] + wt[0] * wt[2] + wt[1] * wt[2])])
    arith(I, iid)


# ======================================================== level 3: the SVD
I = load(3)
if I:
    # ---- p-branch-sales
    iid = 'p-branch-sales'
    A = M([[4, 4], [3, 3], [2, -2]])
    An = npf(A)
    G = A.T * A
    num(I, iid, 1, G[0, 1], (An.T @ An)[0, 1], {'diagonal-or-sign': 16 + 9 + 4, 'aat': (A * A.T)[0, 1]})
    ok(G[0, 0] == 29 and G[0, 1] == 21, 'sales: A^T A')
    Uq, sq, Vq = np.linalg.svd(An, full_matrices=False)          # route 2: NumPy SVD
    numset(I, iid, 2, list(G.eigenvals().keys()), sq ** 2,
           {'entries': [29, 21], 'carried': list(M([[29, 29], [29, 29]]).eigenvals().keys())})
    s1 = sp.sqrt(50)
    v1 = M([1, 1]) / sp.sqrt(2)
    ok(G * v1 == 50 * v1 and G * M([1, -1]) == 8 * M([1, -1]), 'sales: eigenvectors of A^T A')
    u1 = sp.simplify(A * v1 / s1)
    un = Uq[:, 0] * np.sign(Uq[0, 0])
    obj(I, iid, 3, u1, un, {'unscaled': A * M([1, 1]), 'no-root': A * M([1, 1]) / 50})
    ok(u1.dot(u1) == 1, 'sales: u1 has length 1')
    A1 = s1 * u1 * v1.T
    A1n = sq[0] * np.outer(Uq[:, 0], Vq[0])
    obj(I, iid, 4, A1[:, 0], A1n[:, 0], {'u-only': u1, 'carried': s1 * A * M([1, 1]) * v1[0]})
    ok(A1[:, 1] == A1[:, 0] and A - A1 == M([[0, 0], [0, 0], [2, -2]]), 'sales: A_1 columns equal, error rows')
    en = lambda X: sum(t ** 2 for t in X)
    share = en(A1) / en(A)
    num(I, iid, 5, share, np.sum(A1n ** 2) / np.sum(An ** 2),
        {'unsquared': s1 / (s1 + sp.sqrt(8)), 'error-share': en(A - A1) / en(A), 'half': R(1, 2)})
    vocab(I, iid, [G, A * A.T, 50, 8, en(A), en(A1), A * M([1, 1]), 10, u1, 0.64, 0.36, 400, 25, 32, 18, A1, 2 * (16 + 9),
                   s1 / (s1 + sp.sqrt(8)), en(A - A1) / en(A), share, 16, 9])
    arith(I, iid)

    # ---- p-crab-sizes
    iid = 'p-crab-sizes'
    wd = [68, 74, 60, 46, 52]
    cl = [59, 42, 40, 38, 21]
    mw, mc = R(sum(wd), 5), R(sum(cl), 5)
    ok(mw == 60 and mc == 40, 'crabs: means 60 and 40')
    Xd = M([[a - mw, b - mc] for a, b in zip(wd, cl)])
    Sg = Xd.T * Xd / 4
    Cn = np.cov(np.array(wd, float), np.array(cl, float))           # route 2: NumPy's covariance (ddof 1)
    num(I, iid, 1, Sg[0, 1], Cn[0, 1], {'over-n': (Xd.T * Xd)[0, 1] / 5, 'no-divide': (Xd.T * Xd)[0, 1],
                                        'raw': R(sum(a * b for a, b in zip(wd, cl)), 4)})
    ok(Sg == M([[130, 90], [90, R(365, 2)]]), 'crabs: the stated covariance matrix')
    numset(I, iid, 2, list(Sg.eigenvals().keys()), np.linalg.eigvalsh(Cn),
           {'diagonal': [130, R(365, 2)], 'over-n': list((Sg * 4 / 5).eigenvals().keys())})
    vecs_printed = np.array([[0.8, -0.6], [-0.6, -0.8]])
    ok(np.allclose(Cn @ vecs_printed, vecs_printed @ np.diag([62.5, 250])), 'crabs: the printed eigh output is valid')
    _vals_np, _vecs_np = np.linalg.eigh(Cn)
    ok(np.allclose(_vals_np, [62.5, 250]) and all(np.allclose(abs(_vecs_np[:, j]), abs(vecs_printed[:, j])) for j in (0, 1)), 'crabs: eigh gives the printed columns up to a sign')
    ok(any(np.allclose(_vecs_np[:, j], -vecs_printed[:, j]) for j in (0, 1)), 'crabs: this NumPy returns a sign different from the colleague run, so part 3 must say it was a colleague run')
    ok('colleague' in part(I, iid, 3)['question'] and 'either sign' in part(I, iid, 3)['question'], 'crabs: part 3 words the output as a colleague run and says a sign may differ')
    pc = null1(Sg - 250 * sp.eye(2))
    pc = pc / pc.norm()
    pc = pc * (1 if abs(pc[1]) >= abs(pc[0]) and pc[1] > 0 or abs(pc[0]) > abs(pc[1]) and pc[0] > 0 else -1)
    _, vn = np.linalg.eigh(Cn)
    v_np = vn[:, -1] * np.sign(vn[np.argmax(abs(vn[:, -1])), -1])
    obj(I, iid, 3, pc, v_np, {'first-column': M([0.8, -0.6]).applyfunc(sp.nsimplify), 'no-flip': -pc})
    x1 = Xd[0, :].T
    z1 = x1.dot(pc)
    scores = (np.array([wd, cl], float).T - [60, 40]) @ v_np
    num(I, iid, 4, z1, scores[0], {'no-flip': -z1, 'raw': M([68, 59]).dot(pc), 'pc2': x1.dot(M([R(4, 5), R(-3, 5)]))})
    zs = z1 / sp.sqrt(250)
    num(I, iid, 5, zs, scores[0] / np.std(scores, ddof=1),
        {'variance': z1 / 250, 'total': z1 / sp.sqrt(Sg.trace()), 'pc2-sd': z1 / sp.sqrt(R(125, 2))})
    # the value the feedback itself prints: 20 / 15.811 and 20 / 15.81 both give 1.265 to 3 places, and so does the exact value
    ok(round(20 / 15.811, 3) == 1.265 and round(20 / 15.81, 3) == 1.265 and round(float(zs), 3) == 1.265 and round(20 / math.sqrt(250), 6) == 1.264911,
       'crabs: 1.265 by 15.811, by 15.81 and exactly')
    ok(round(math.sqrt(250), 3) == 15.811, 'crabs: sqrt 250 = 15.811')
    ok(part(I, iid, 5)['widget']['answer'] == 1.265 and part(I, iid, 5)['widget']['tol']['abs'] == 0.0005 and 'places' in part(I, iid, 5)['question'], 'crabs: part 5 asks for 3 places with answer 1.265')
    stale = [r'15\.81(?!\d)', r'1\.26(?!\d)', r'1\.13(?!\d)']
    blob = ' '.join(t for _, t in strings(I[iid]))
    for tok in stale:
        ok(not re.search(tok, blob), f'{iid}: stale 2-place token {tok}')
    vocab(I, iid, [Xd, [a * b for a, b in Xd.tolist()], (Xd.T * Xd)[0, 1], 72, R(sum(a * b for a, b in zip(wd, cl)), 4), Sg,
                   Sg.trace(), 130 * R(365, 2), 8100, Sg.det(), 250, R(125, 2), pc, 4.8, 15.2, z1, 88, -5, sp.sqrt(250), zs,
                   z1 / 250, z1 / sp.sqrt(Sg.trace()), z1 / sp.sqrt(R(125, 2)), 200, 50, 0.8, 0.6, 68 - 60, 59 - 40, 15.811, 1.265])
    arith(I, iid)

    # ---- p-site-anomalies
    iid = 'p-site-anomalies'
    s = [30, 15, 6, 3]
    n = 31
    rng = np.random.default_rng(7)                                  # route 2: build a real demeaned 31 by 4 matrix
    Z = rng.standard_normal((n, 4))
    Z -= Z.mean(axis=0)
    Uz, _ = np.linalg.qr(Z)
    Vz, _ = np.linalg.qr(rng.standard_normal((4, 4)))
    Xc = Uz @ np.diag(s) @ Vz.T
    ok(np.allclose(Xc.mean(axis=0), 0) and np.allclose(np.linalg.svd(Xc, compute_uv=False), s), 'sites: built matrix')
    lam = [R(t * t, n - 1) for t in s]
    tot = sum(lam)
    num(I, iid, 1, tot, np.var(Xc, axis=0, ddof=1).sum(),
        {'no-divide': sum(t * t for t in s), 'over-n': R(sum(t * t for t in s), n), 'unsquared': R(sum(s), n - 1)})
    ev = np.sort(np.linalg.eigvalsh(np.cov(Xc.T)))[::-1]
    sh2 = (lam[0] + lam[1]) / tot
    num(I, iid, 2, sh2, ev[:2].sum() / ev.sum(),
        {'unsquared': R(s[0] + s[1], sum(s)), 'pc1-only': lam[0] / tot, 'carried': (lam[0] + lam[1]) / sum(t * t for t in s)})
    cum = [sum(lam[:k]) / tot for k in range(1, 5)]
    k = next(i + 1 for i, c in enumerate(cum) if c >= R(99, 100))
    kn = int(np.argmax(np.cumsum(ev) / ev.sum() >= 0.99)) + 1
    num(I, iid, 3, k, kn, {'two': 2, 'all': 4})
    U2, s2, V2 = np.linalg.svd(Xc, full_matrices=False)
    Xk = U2[:, :k] @ np.diag(s2[:k]) @ V2[:k]
    num(I, iid, 4, sum(t * t for t in s[k:]), np.sum((Xc - Xk) ** 2),
        {'unsquared': s[3], 'rank-two': s[2] ** 2 + s[3] ** 2, 'kept': sum(t * t for t in s[:3]), 'variance': lam[3]})
    ok(lam[3] == R(3, 10) and np.isclose(np.sort(np.linalg.eigvalsh(np.cov(Xc.T)))[0], 0.3), 'sites: PC4 variance 9 / 30 = 0.3 by eigvalsh of the covariance')
    ok('0.962' in part(I, iid, 3)['question'] and '3 components' in part(I, iid, 4)['question'], 'sites: parts 3 and 4 restate 0.962 and 3 components')
    vocab(I, iid, [[t * t for t in s], sum(t * t for t in s), lam, tot, lam[0] + lam[1], sh2, cum, sum(lam[:3]), sum(s), 31,
                   R(sum(t * t for t in s), n), R(sum(s), n - 1), R(s[0] + s[1], sum(s)), (lam[0] + lam[1]) / sum(t * t for t in s),
                   45, 1161, 99, R(9 * 100, 1170), 0.8])
    arith(I, iid)


# ======================================================== level 4: factorisations at work
I = load(4)
if I:
    from scipy.linalg import expm, cholesky as sp_chol
    E = sp.exp

    # ---- p-linked-lagoons
    iid = 'p-linked-lagoons'
    A = M([[-4, 2], [1, -3]])
    Mg = M([[1, 0], [1, 1]])
    ok(Mg.inv() == M([[1, 0], [-1, 1]]), 'lagoons: printed M inverse')
    B = Mg.inv() * A * Mg
    Bn = np.linalg.solve(npf(Mg), npf(A) @ npf(Mg))                       # route 2: solve, not invert
    ok(B == M([[-2, 2], [0, -5]]) and np.allclose(Bn, npf(B)), 'lagoons: B as printed')
    ok(A * Mg == M([[-2, 2], [-2, -3]]), 'lagoons: AM as printed')
    rev = Mg * A * Mg.inv()
    num(I, iid, 1, B[1, 1], Bn[1, 1], {'sign': -B[1, 1], 'unchanged': A[1, 1], 'reversed': rev[1, 1]})
    ok(B[1, 1] == -5 and A[1, 1] == -3 and rev[1, 1] == -1, 'lagoons: part 1 key -5, wrongs 5, -3, -1')
    lam = sp.roots(sp.Matrix(A).charpoly().as_expr())
    numset(I, iid, 2, list(B.eigenvals().keys()), eigvals_np(A),
           {'sign': [5, 2], 'trace-det': [A.trace(), A.det()], 'a-diagonal': [A[0, 0], A[1, 1]]})
    ok(sorted(lam) == [-5, -2] and A.det() == 10 and A.trace() == -7, 'lagoons: trace -7, det 10')
    y = M([2, -3])
    ok(B * y == -5 * y, 'lagoons: (2, -3) is an eigenvector of B for -5')
    x = Mg * y
    ok(A * x == -5 * x and A * x == M([-10, 5]), 'lagoons: A(2, -1) = (-10, 5)')
    obj(I, iid, 3, x, eigvec_np(A, -5, fix=0) * 2, {'inverse': Mg.inv() * y, 'unmoved': y})
    ok(list(Mg.inv() * y) == [2, -5] and list(Mg.inv() * M([5, 2])) == [5, -3], 'lagoons: wrongs (2, -5) and (5, -3)')
    X = M([[1, 2], [1, -1]])
    u0 = M([5, 2])
    c = X.LUsolve(u0)
    obj(I, iid, 4, c, np.linalg.solve(npf(X), npf(u0)).ravel(), {'swapped': M([c[1], c[0]]), 'w-coords': Mg.inv() * u0})
    t = sp.Symbol('t')
    ut = c[0] * E(-2 * t) * X[:, 0] + c[1] * E(-5 * t) * X[:, 1]
    tot = (ut[0] + ut[1]).subs(t, 1)
    u_num = expm(npf(A) * 1.0) @ npf(u0).ravel()                          # route 2: scipy expm
    ok(sp.simplify(ut.subs(t, 0) - u0) == M([0, 0]), 'lagoons: u(0) = u0')
    num(I, iid, 5, tot, u_num.sum(),
        {'coefficients-only': (c[0] * E(-2) + c[1] * E(-5)), 'u1-only': ut[0].subs(t, 1),
         'rates-swapped': c[0] * 2 * E(-5) + c[1] * E(-2), 'carried': 1 * 2 * E(-2) + 3 * 1 * E(-5)})
    ok(round(float(E(-2)), 4) == 0.1353 and round(float(E(-5)), 4) == 0.0067 and round(6 * 0.1353 + 0.0067, 3) == 0.819,
       'lagoons: printed exponentials and 0.819 from them')
    ok(sp.simplify(ut[1].subs(t, 1) - (3 * E(-2) - E(-5))) == 0, 'lagoons: u2(1) = 3e^-2 - e^-5')
    vocab(I, iid, [A, Mg, Mg.inv(), B, A * Mg, rev, y, x, A * x, c, u0, tot, 0.1353, 0.0067, 12, 10, -7, 0.819, 2 * c[0]])
    arith(I, iid)

    # ---- p-wind-pair
    iid = 'p-wind-pair'
    S = M([[16, 20], [20, 34]])
    L = S.cholesky()
    Ln = np.linalg.cholesky(npf(S))
    ok(L == M([[4, 0], [5, 3]]) and np.allclose(Ln, npf(L)) and L * L.T == S, 'wind: L as printed')
    num(I, iid, 1, L[1, 1], Ln[1, 1], {'no-subtract': sp.sqrt(34), 'subtract-sigma': sp.sqrt(34 - 20), 'no-root': 9})
    xv = M([8, 4])
    w = L.LUsolve(xv)
    wn = np.linalg.solve(Ln, npf(xv).ravel())
    num(I, iid, 2, w[1], wn[1], {'sign': -w[1], 'used-x1': R(4 - 5 * 8, 3), 'no-subtract': R(4, 3), 'carried': (4 - 10) / sp.sqrt(34)})
    d2 = w.dot(w)
    d2n = float(npf(xv).ravel() @ np.linalg.inv(npf(S)) @ npf(xv).ravel())      # route 2: x^T Sigma^-1 x
    naive2 = R(8, 4) ** 2 + R(4) ** 2 / 34
    num(I, iid, 3, sp.sqrt(d2), math.sqrt(d2n), {'squared': d2, 'ignore-correlation': sp.sqrt(naive2), 'carried': sp.sqrt(4 + 144)})
    rng = np.random.default_rng(11)                                           # route 3: simulate the tail
    Z = rng.standard_normal((400000, 2)) @ Ln.T
    dd = np.einsum('ij,jk,ik->i', Z, np.linalg.inv(npf(S)), Z)
    ok(abs((dd >= 8).mean() - math.exp(-4)) < 0.001, 'wind: simulated chance of d^2 >= 8 is e^-4')
    num(I, iid, 4, E(-d2 / 2), math.exp(-d2n / 2),
        {'used-d': E(-sp.sqrt(d2) / 2), 'no-half': E(-d2), 'carried': E(-naive2 / 2)})
    ok(round(1 / math.exp(-4)) == 55, 'wind: one hour in 55')
    cm, cs = S[1, 0] / S[0, 0] * 8, sp.sqrt(S[1, 1] - S[1, 0] ** 2 / S[0, 0])
    ok((xv[1] - cm) / cs == w[1] and cs == L[1, 1] and cm == 10, 'wind: w2 is the conditional z-score, 2 sd below what turbine 1 led us to expect')
    ok(R(8, 4) == 2 and float(4 / sp.sqrt(34)) < 2, 'wind: turbine 1 alone is 2 sd out, turbine 2 less')
    vocab(I, iid, [S, L, xv, w, d2, sp.sqrt(d2), naive2, sp.sqrt(naive2), E(-4), 55, 34, 25, 9, 16, 20, 10, 12, -12, 2.828, 2.114, 0.0183, cm])
    arith(I, iid)

    # ---- p-track-laps
    iid = 'p-track-laps'
    Xr = M([[2, 4], [1, 2], [2, 4]])
    yv = M([11, 5, 9])
    G = Xr.T * Xr
    ok(G == M([[9, 18], [18, 36]]), 'laps: X^T X as printed')
    l11 = sp.sqrt(G[0, 0]); l21 = G[1, 0] / l11; l22sq = G[1, 1] - l21 ** 2
    # route 2: the last pivot of elimination on G (Cholesky's L22^2) and NumPy's refusal
    piv = npf(G)[1, 1] - npf(G)[1, 0] ** 2 / npf(G)[0, 0]
    try:
        np.linalg.cholesky(npf(G) + np.diag([0, -1e-9]))
        refused = False
    except np.linalg.LinAlgError:
        refused = True
    ok(refused, 'laps: NumPy refuses the Cholesky factor of X^T X just below singular')
    num(I, iid, 1, sp.sqrt(l22sq), math.sqrt(max(piv, 0)), {'root-36': 6, 'subtract-entry': sp.sqrt(36 - 18)})
    ev = [e for e in G.eigenvals() if e != 0]
    num(I, iid, 2, ev[0], max(np.linalg.eigvalsh(npf(G))), {'diagonal': G[1, 1], 'first-entry': G[0, 0]})
    ok(G * M([1, 2]) == M([45, 90]), 'laps: X^T X (1, 2) = (45, 90)')
    s1 = sp.sqrt(ev[0]); v1 = M([1, 2]) / sp.sqrt(5); u1 = Xr * v1 / s1
    ok(sp.simplify(u1 - M([2, 1, 2]) / 3) == M([0, 0, 0]), 'laps: u1 = (2, 1, 2)/3')
    ok(sp.simplify(u1.dot(yv)) == 15 and sp.sqrt(5) * sp.sqrt(45) == 15, 'laps: u1 . y = 15 and sqrt5 sqrt45 = 15')
    bp = (v1 * u1.T / s1) * yv
    ok(sp.simplify(bp - Xr.pinv() * yv) == M([0, 0]), 'laps: X^+ y by sympy pinv')
    obj(I, iid, 3, bp.applyfunc(sp.simplify), np.linalg.pinv(npf(Xr)) @ npf(yv).ravel(),
        {'all-km': M([5, 0]), 'all-laps': M([0, R(5, 2)])})
    for alt in (M([5, 0]), M([0, R(5, 2)])):
        ok(sp.simplify(Xr * alt - Xr * bp) == M([0, 0, 0]) and alt.norm() > bp.norm(), 'laps: other fits are equally good and longer')
    ok(M([5, 0]).norm() == 5 and bp.norm() == sp.sqrt(5), 'laps: lengths 5 and sqrt 5')
    ok(G[0, 0] * 5 == (Xr.T * yv)[0] and (Xr.T * yv) == M([45, 90]), 'laps: beta1 + 2 beta2 = 5 from the normal equations')
    new = M([3, 6])
    pred = new.dot(bp)
    num(I, iid, 4, pred, float(np.array([3, 6]) @ np.linalg.lstsq(npf(Xr), npf(yv).ravel(), rcond=None)[0]),
        {'laps-as-km': M([3, 3]).dot(bp), 'km-only': 3 * bp[0]})
    ok(new.dot(M([5, 0])) == pred, 'laps: (5, 0) predicts 15 too')
    vocab(I, iid, [Xr, yv, G, l11, l21, 45, 90, 15, 22, 18, R(5, 2), 2.5, pred, 36, 9])
    arith(I, iid)

    # ---- p-machine-stops
    iid = 'p-machine-stops'
    Q = M([[R(-1, 10), R(2, 5)], [R(1, 10), R(-2, 5)]])
    ok(all(sum(Q[:, j]) == 0 for j in range(2)), 'machine: columns add to 0')
    numset(I, iid, 1, list(Q.eigenvals().keys()), eigvals_np(Q),
           {'sign': [0, R(1, 2)], 'diagonal': [Q[0, 0], Q[1, 1]]})
    ok(Q.det() == 0 and Q.trace() == R(-1, 2), 'machine: det 0 and trace -0.5')
    ss = Q.nullspace()[0]; ss = ss / sum(ss)
    Pn = expm(npf(Q) * 200.0)                                                 # route 2: P(t) for large t
    obj(I, iid, 2, ss, Pn[:, 0], {'swapped': M([ss[1], ss[0]]), 'unscaled': 5 * ss})
    ok(list(ss) == [R(4, 5), R(1, 5)], 'machine: steady state (0.8, 0.2)')
    ok(R(1, 10) * ss[0] == R(2, 5) * ss[1] == R(2, 25), 'machine: balance 0.08 an hour')
    Sw = M([[0, 1], [1, 0]])
    Qp = Sw.inv() * Q * Sw
    ok(Qp == M([[R(-2, 5), R(1, 10)], [R(2, 5), R(-1, 10)]]) and Qp.charpoly().as_expr() == Q.charpoly().as_expr(), 'machine: Q\' as printed, same polynomial')
    ssp = Sw.inv() * ss
    ok(Qp * ssp == M([0, 0]) and ssp == M([R(1, 5), R(4, 5)]), 'machine: team steady state (0.2, 0.8)')
    ok(Qp * M([1, -1]) == R(-1, 2) * M([1, -1]), 'machine: (1, -1) is an eigenvector of Q\' for -0.5')
    pick(I, iid, 3, 'moved')
    tt = sp.Symbol('t')
    ok(ssp + R(4, 5) * M([1, -1]) == M([1, 0]), 'machine: (1, 0) = (0.2, 0.8) + 0.8(1, -1)')
    pS = R(1, 5) + R(4, 5) * E(R(-1, 2) * tt)
    ok(np.isclose(float(pS.subs(tt, 5)), expm(npf(Qp) * 5.0)[0, 0]), 'machine: formula matches expm')
    num(I, iid, 4, pS.subs(tt, 5), expm(npf(Qp) * 5.0)[0, 0],
        {'running-chance': R(4, 5) + R(1, 5) * E(R(-5, 2)), 'no-steady': R(4, 5) * E(R(-5, 2)),
         'restart-rate': R(1, 5) + R(4, 5) * E(R(-2, 1)), 'one-hour': pS.subs(tt, 1)})
    ok(round(math.exp(-2.5), 4) == 0.0821 and round(0.2 + 0.8 * 0.0821, 3) == 0.266, 'machine: 0.0821 and 0.266 from it')
    ok(np.isclose(expm(npf(Q) * 5.0)[0, 0], 0.8 + 0.2 * math.exp(-2.5)), 'machine: running-chance slip is the Running entry of P(5)')
    tstar = sp.log(80) / R(1, 2)
    # route 2: bisection on the expm entry
    lo, hi = 0.0, 50.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if expm(npf(Qp) * mid)[0, 0] - 0.2 > 0.01:
            lo = mid
        else:
            hi = mid
    num(I, iid, 5, tstar, lo,
        {'running-start': sp.log(20) / R(1, 2), 'no-coefficient': sp.log(100) / R(1, 2),
         'restart-rate': sp.log(80) / R(2, 5), 'multiplied': sp.log(80) * R(1, 2)})
    ok(round(math.log(80), 3) == 4.382 and round(4.382 / 0.5, 2) == 8.76, 'machine: ln 80 = 4.382 and 8.76 from it')
    vocab(I, iid, [Q, ss, Qp, ssp, 0.04, R(2, 25), pS.subs(tt, 5), 0.0821, 0.266, 0.816, 0.685, -0.5, 0.5, 80, 4.382, tstar, 8.76, 8.8, 0.01, 5, R(-1, 2) * 5, R(1, 5) / R(1, 100), R(4, 5) / R(1, 100)])
    arith(I, iid)

print(f"{checks} checks, {len(fails)} failures")
for f in fails:
    print("FAIL", f)
sys.exit(1 if fails else 0)
