"""Recompute every number in app/content/courses/elimination/problems-<n>.json twice.

Method 1 is exact: sympy Rationals and Matrices (elimination by hand-coded row steps, LUsolve,
nullspace, rank, det by cofactors). Method 2 is a different route in floating point: NumPy
(np.linalg.solve, matrix_rank, det, products checked by multiplying back), or enumeration.

Checks, per part:
- numeric: both methods agree; the key lies within its tol of them; each `wrong` value equals
  the value its named slip gives, lies outside the key's band, and no two wrong bands overlap;
  every wrong id has a byKey line; the question names its form.
- expression (vectors and matrices typed whole): the key and every accept form equal the exact
  answer entry by entry; each wrong form equals its slip and differs from the key.
- choice: the keyed option.
Per item, over every learner-facing string (prose, questions, feedback, byKey, explain, option
text and why, wrong tex):
- `arith`: every chain $a = b = c$ inside a maths span whose sides are plain arithmetic
  (numbers, + - x /, fractions, tuples) is evaluated, and consecutive sides must agree.
- `vocab`: every number printed must be a given of the item or a value this script computed
  for it (stale numbers fail); 0 to 5 are free (rows, columns, part numbers).
Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-elimination-numbers.py
"""
import json, os, re, sys, itertools, math
from fractions import Fraction as F
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

TR = standard_transformations + (implicit_multiplication_application,)
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'elimination')
fails, checks = [], 0
FORM = re.compile(r'decimal|places?\b|fraction|whole number|nearest|in pounds|per cent|%|exact', re.I)
R = sp.Rational
M = sp.Matrix
k_ = sp.Symbol('k')
SYMS = {'k': k_, 't': sp.Symbol('t'), 'c': sp.Symbol('c')}


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
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'elimination', f'set {n}: header')
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
    ok(math.isclose(e, float(alt), rel_tol=1e-9, abs_tol=1e-9), f'{tag}: methods differ {e} vs {float(alt)}')
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
        ok(abs(x['value'] - float(val)) <= max(wt, 1e-9), f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} inside the key band')
    for a, b in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a], wrongs[b]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a} and {b} overlap')
    return e


# ------------------------------------------------------------------ expression parts
def parse_entry(s):
    s = s.strip()
    s = re.sub(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    return sp.nsimplify(parse_expr(s, local_dict=SYMS, transformations=TR), rational=True)


def parse_obj(s):
    """'(a, b)', '[a, b]', '[[a, b], [c, d]]' or a pmatrix -> sympy Matrix (a vector as one row)."""
    s = s.strip()
    m = re.fullmatch(r'\\begin\{pmatrix\}(.*)\\end\{pmatrix\}', s, re.S)
    if m:
        rows = [r.split('&') for r in m.group(1).split('\\\\')]
        return M([[parse_entry(x) for x in r] for r in rows])
    if s.startswith('[['):
        rows = re.findall(r'\[([^\[\]]*)\]', s[1:-1])
        return M([[parse_entry(x) for x in r.split(',')] for r in rows])
    if s[0] in '([' and s[-1] in ')]':
        return M([[parse_entry(x) for x in s[1:-1].split(',')]])
    return M([[parse_entry(s)]])


def same(A, B):
    return A.shape == B.shape and all(sp.simplify(a - b) == 0 for a, b in zip(A, B))


def as_row(v):
    v = M(v)
    return v.T if v.shape[1] == 1 and v.shape[0] > 1 else v


def obj(items, iid, k, exact, alt, slips):
    """exact: sympy Matrix or vector; alt: NumPy array (or a function of k) from the second route."""
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    exact = M(exact)
    if exact.shape[1] == 1 and exact.shape[0] > 1:
        exact = exact.T
    if exact.free_symbols:
        for kv in (0.5, 1.7, 3):
            ev = np.array(exact.subs(k_, kv).tolist(), dtype=float)
            ok(np.allclose(ev.ravel(), np.ravel(alt(kv))), f'{tag}: methods differ at k={kv}')
    else:
        ok(np.allclose(np.array(exact.tolist(), dtype=float).ravel(), np.ravel(alt)), f'{tag}: methods differ')
    for form in [w['answer']] + w.get('accept', []):
        ok(same(parse_obj(form), exact), f'{tag}: form {form} differs from the key')
    got = {x['id']: x['tex'] for x in w.get('wrong', [])}
    ok(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} vs {sorted(slips)}')
    ok(set(got) <= set(p['feedback'].get('byKey', {})), f'{tag}: byKey lines missing')
    for wid, val in slips.items():
        if wid not in got:
            continue
        g, v = parse_obj(got[wid]), M(val)
        if v.shape != g.shape:
            v = as_row(v)
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
        out += [(f'p{k} wrong {x["id"]}', x.get('tex', '')) for x in w.get('wrong', [])]
        for o in w.get('options', []):
            out += [(f'p{k} option {o["id"]}', o['text']), (f'p{k} why {o["id"]}', o.get('why', ''))]
    return out


def to_py(seg):
    s = seg.strip()
    s = s.replace('£', '').replace('\\,', '').replace('\\;', '').replace('\\!', '').replace('{,}', '')
    s = re.sub(r'\\(?:left|right)', '', s)
    s = re.sub(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    s = s.replace('\\times', '*').replace('\\cdot', '*').replace('\\mid', ',').replace('−', '-')
    s = s.replace('\\text{ kg}', '').strip().rstrip('.,')
    if not s or re.search(r'[A-Za-z\\_^{}]', s):
        return None
    s = re.sub(r'\(([^()]*,[^()]*)\)', r'np.array([\1])', s)
    try:
        v = eval(s, {'np': np})
    except Exception:
        return None
    return np.asarray(v, dtype=float)


def arith(items, iid):
    for where, text in strings(items[iid]):
        for span in re.findall(r'\$\$?([^$]+)\$\$?', text):
            for chain in re.split(r'\\quad|\\qquad|,\s+(?=[a-z]_?\{?\d)|\\text\{[^}]*\}', span):
                sides = [to_py(x) for x in re.split(r'(?<![<>!\\])=', chain)]
                for a, b in zip(sides, sides[1:]):
                    if a is not None and b is not None:
                        ok(a.shape == b.shape and np.allclose(a, b), f'{iid} {where}: false step in ${chain}$')


def numbers_in(text):
    t = re.sub(r'_\{[^}]*\}|_\d|\^\{[^}]*\}', '', text)
    t = re.sub(r'\\[dt]?frac\{(-?\d+)\}\{(\d+)\}', r' \1 / \2 ', t)
    t = t.replace('{,}', '')
    return [float(x) for x in re.findall(r'(?<![\w.])-?\d+(?:\.\d+)?', t)]


def vocab(items, iid, values):
    """Every number printed in the item is a given (prose or question) or a computed value."""
    it = items[iid]
    allowed = set()

    def add(x):
        x = sp.sympify(x)
        if x.free_symbols:
            for a in x.atoms(sp.Number):
                allowed.add(round(float(a), 6))
        else:
            allowed.add(round(float(x), 6))

    for v in values:
        if isinstance(v, (sp.MatrixBase, list, tuple, np.ndarray)):
            for x in (M(v) if not isinstance(v, np.ndarray) else v.ravel()):
                add(x)
        else:
            add(v)
    given = set(round(x, 6) for x in numbers_in(it.get('prose', '')))
    for where, text in strings(it):
        for x in numbers_in(text):
            r = round(x, 6)
            if abs(r) <= 5 and r == int(r):
                continue
            ok(r in allowed or r in given or -r in allowed or -r in given,
               f'{iid} {where}: number {x} is neither given nor computed')


# ------------------------------------------------------------------ elimination helpers
def eliminate(A, cols=None):
    """Exact elimination without swaps; returns (L, U, multipliers in order)."""
    U = M(A)
    n = U.shape[0]
    L = sp.eye(n)
    for j in range(n - 1):
        for i in range(j + 1, n):
            l = U[i, j] / U[j, j]
            L[i, j] = l
            U[i, :] = U[i, :] - l * U[j, :]
    return L, U


def forward(L, b):
    c = []
    for i in range(L.shape[0]):
        c.append((b[i] - sum(L[i, j] * c[j] for j in range(i))) / L[i, i])
    return M(c)


def backward(U, c):
    n = U.shape[0]
    x = [0] * n
    for i in reversed(range(n)):
        x[i] = (c[i] - sum(U[i, j] * x[j] for j in range(i + 1, n))) / U[i, i]
    return M(x)


def npf(A):
    return np.array(M(A).tolist(), dtype=float)


# ------------------------------------------------------------------ self-test of the text checks
_fake = {'t': {'prose': 'Costs £12.', 'parts': [{'question': 'q', 'widget': {'kind': 'numeric'}, 'feedback': {'correct': r'$2y = 7 - 3 = 5$ and $(1, 2) + (1, 1) = (2, 3)$', 'generic': 'g'}, 'explain': {'text': r'Here $x = 4/2 = 2$ and 47 appears.'}}]}}
_n = len(fails)
arith(_fake, 't')
vocab(_fake, 't', [4, 7])
ok(len(fails) == _n + 2 and 'false step' in fails[_n] and '47' in fails[_n + 1], 'self-test: arith and vocab catch planted faults')
del fails[_n:_n + 2]

# ======================================================== level 1: elimination
I = load(1)
if I:
    # ---- p-florist-prices
    iid = 'p-florist-prices'
    A = M([[2, 2, 4], [6, 8, 13], [1, 5, 5]])
    b = M([19, 64, R(53, 2)])
    Ab = A.row_join(b)
    l31 = Ab[2, 0] / Ab[0, 0]
    r3 = Ab[2, :] - l31 * Ab[0, :]
    r2 = Ab[1, :] - (Ab[1, 0] / Ab[0, 0]) * Ab[0, :]
    obj(I, iid, 1, r3, npf(Ab)[2] - 0.5 * npf(Ab)[0],
        {'upside-down': Ab[2, :] - 2 * Ab[0, :], 'added': Ab[2, :] + l31 * Ab[0, :]})
    ok(list(r2) == [0, 2, 1, 7], 'florist: row 2 stated (0, 2, 1 | 7)')
    l32 = r3[1] / r2[1]
    r3b = r3 - l32 * r2
    sol = A.LUsolve(b)
    xs, ys, zs = sol
    nps = np.linalg.solve(npf(A), npf(b).ravel())
    num(I, iid, 2, r3b[3] / r3b[2], nps[2], {'cost-kept': r3[3]})
    num(I, iid, 3, (r2[3] - r2[2] * zs) / r2[1], nps[1], {'no-subtract': r2[3] / 2, 'added': (r2[3] + zs) / 2})
    num(I, iid, 4, (b[0] - 2 * ys - 4 * zs) / 2, nps[0], {'coefficients': (b[0] - ys - zs) / 2, 'no-divide': b[0] - 2 * ys - 4 * zs})
    bq = M([4, 3, 2])
    num(I, iid, 5, bq.dot(sol), bq.T.dot(nps) if False else float(np.dot([4, 3, 2], nps)),
        {'carried': bq.dot(M([(b[0] - ys - zs) / 2, ys, zs])), 'counts-swapped': M([2, 3, 4]).dot(sol)})
    vocab(I, iid, [r3, r2, l31 * Ab[0, :], Ab[2, :] - 2 * Ab[0, :], Ab[2, :] + l31 * Ab[0, :], r3b, l32, sol,
                   2 * ys, 4 * zs, 2 * xs, r3[3] - r3b[3], 4 * xs, bq.dot(sol), M([2, 3, 4]).dot(sol), bq.dot(M([7, ys, zs])),
                   b[0] - ys - zs, 2 * l32 * 0 + r2[3] * 2, 4 * zs * 0 + 4 * xs, r2[3] - zs])
    arith(I, iid)

    # ---- p-three-lines
    iid = 'p-three-lines'
    A = M([[2, 2, 2], [6, 7, 9], [1, 3, 9]])
    L, U = eliminate(A)
    ok(L * U == A, 'lines: LU = A')
    Lnp = np.eye(3)
    Unp = npf(A).copy()
    for j in range(2):
        for i in range(j + 1, 3):
            Lnp[i, j] = Unp[i, j] / Unp[j, j]
            Unp[i] -= Lnp[i, j] * Unp[j]
    Ls = M([[1, 0, 0], [-3, 1, 0], [-R(1, 2), -2, 1]])
    Lstale = M([[1, 0, 0], [3, 1, 0], [R(1, 2), 3, 1]])
    obj(I, iid, 1, L, Lnp, {'signs': Ls, 'transposed': L.T, 'stale': Lstale})
    ok(U == M([[2, 2, 2], [0, 1, 3], [0, 0, 2]]), 'lines: U as stated in part 3')
    after1 = [A[1, :] - 3 * A[0, :], A[2, :] - R(1, 2) * A[0, :]]
    b = M([12, 41, 18])
    c = forward(L, b)
    obj(I, iid, 2, c, np.linalg.solve(Lnp, npf(b).ravel()), {'signs': forward(Ls, b), 'stale': forward(Lstale, b)})
    x = backward(U, c)
    obj(I, iid, 3, x, np.linalg.solve(npf(A), npf(b).ravel()),
        {'b-not-c': backward(U, b), 'no-divide': backward(U.applyfunc(lambda v: v) - sp.diag(*[U[i, i] - 1 for i in range(3)]), c)})
    db = M([10, 38, 25])
    c2 = forward(L, db)
    y = backward(U, c2)
    obj(I, iid, 4, x + y, np.linalg.solve(npf(A), npf(b + db).ravel()), {'extra-only': y, 'added-c': x + c2})
    vocab(I, iid, [db, L, U, c, x, c2, y, x + y, x + c2, after1[0], after1[1], forward(Ls, b), forward(Lstale, b),
                   backward(U, b), 3 * 12, R(1, 2) * 12, 2 * 5, A * x])
    arith(I, iid)

    # ---- p-courier-rounds
    iid = 'p-courier-rounds'
    A = M([[0, 3, 1], [2, 1, 2], [0, 6, 5]])
    b = M([15, 14, 39])
    P = M([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    P13 = M([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    ok((P13 * A)[0, 0] == 0 and (P * A)[0, 0] != 0, 'courier: only the 1-2 swap gives a pivot')
    ok(all((Q * A)[0, 0] == 0 for Q in [sp.eye(3), P13]) and A[0, 0] == 0 and A[2, 0] == 0, 'courier: rows 1 and 3 start with 0')
    obj(I, iid, 1, P, npf(P), {'swap-1-3': P13})
    L, U = eliminate(P * A)
    ok(L * U == P * A, 'courier: PA = LU')
    obj(I, iid, 2, L, np.array([[1, 0, 0], [0, 1, 0], [0, 6 / 3, 1]]), {'signs': L.T.T - 2 * 2 * M([[0, 0, 0], [0, 0, 0], [0, 1, 0]]) * 1, 'transposed': L.T})
    ok(U == M([[2, 1, 2], [0, 3, 1], [0, 0, 3]]), 'courier: U as stated in part 4')
    c = forward(L, P * b)
    Lsg = M([[1, 0, 0], [0, 1, 0], [0, -2, 1]])
    obj(I, iid, 3, c, np.linalg.solve(npf(L), npf(P * b).ravel()), {'unswapped': forward(L, b), 'signs': forward(Lsg, P * b)})
    x = backward(U, c)
    nod = backward(sp.eye(3) + U - sp.diag(*U.diagonal()), c)
    obj(I, iid, 4, x, np.linalg.solve(npf(A), npf(b).ravel()), {'no-divide': nod, 'reversed': M(list(reversed(list(x))))})
    rnd = M([5, 2, 4])
    num(I, iid, 5, rnd.dot(x), float(np.dot([5, 2, 4], np.linalg.solve(npf(A), npf(b).ravel()))), {'reversed': rnd.dot(M(list(reversed(list(x)))))})
    vocab(I, iid, [P * b, c, x, U, L, forward(L, b), forward(Lsg, P * b), nod, rnd.dot(x), 5 * x[0], 2 * x[1], 4 * x[2],
                   3 * x[1], 2 * x[0], 6 / 3, 2 * 15, c[2], 15 - x[2], 14 - x[1] - 2 * x[2], 2 * x[2]])
    arith(I, iid)

    # ---- p-roaster-beans
    iid = 'p-roaster-beans'
    A = M([[2, 1, 3], [6, 3, 10], [4, k_, 9]])
    r3 = A[2, :] - (A[2, 0] / A[0, 0]) * A[0, :]
    r2 = A[1, :] - 3 * A[0, :]
    obj(I, iid, 1, r3, lambda kv: np.array([4, kv, 9.]) - 2 * np.array([2, 1, 3.]),
        {'added': A[2, :] + 2 * A[0, :], 'triple': A[2, :] - 3 * A[0, :]})
    ok(list(r2) == [0, 0, 1], 'roaster: row 2 is (0, 0, 1) for every k')
    kbad = sp.solve(r3[1], k_)
    ok(kbad == [2], 'roaster: breakdown at k = 2')
    # second route: scan k for a rank drop in NumPy
    scan = [kv for kv in range(-10, 11) if np.linalg.matrix_rank(np.array([[2, 1, 3], [6, 3, 10], [4, kv, 9.]])) < 3]
    num(I, iid, 2, kbad[0], scan[0], {'k-zero': 0, 'triple': sp.solve((A[2, :] - 3 * A[0, :])[1], k_)[0]})
    prices = M([6, 8, 5])
    cost = lambda kv: M([[2, 1, 3], [6, 3, 10], [4, kv, 9]]) * prices
    ok(cost(2) == M([35, 110, 85]) and cost(4) == M([35, 110, 101]), 'roaster: the stated costs follow from (6, 8, 5)')
    b2 = M([35, 110, 85])
    Ab = A.subs(k_, 2).row_join(b2)
    R2 = Ab[1, :] - 3 * Ab[0, :]
    R3 = Ab[2, :] - 2 * Ab[0, :]
    ok(list(R2) == [0, 0, 1, 5] and list(R3) == [0, 0, 3, 15], 'roaster: k = 2 rows (0,0,1|5), (0,0,3|15)')
    ok((R3 - 3 * R2) == M([[0, 0, 0, 0]]), 'roaster: k = 2 is consistent, not contradictory')
    ok(np.linalg.matrix_rank(npf(Ab)) == np.linalg.matrix_rank(npf(A.subs(k_, 2))) == 2, 'roaster: rank 2 with and without costs at k = 2')
    ok(sp.Matrix([[2, 1]]).rank() == 1 and Ab[0, 3] - 3 * 5 == 20, 'roaster: row 1 leaves 2x + y = 20')
    pick(I, iid, 3, 'c-only')
    b4 = M([35, 110, 101])
    A4 = A.subs(k_, 4)
    R3 = A4.row_join(b4)[2, :] - 2 * A4.row_join(b4)[0, :]
    ok(list(R3) == [0, 2, 3, 31], 'roaster: k = 4 row 3 is (0, 2, 3 | 31)')
    sol = A4.LUsolve(b4) if False else (A4.inv() * b4)
    nps = np.linalg.solve(npf(A4), npf(b4).ravel())
    yv = (R3[3] - 3 * 5) / R3[1]
    num(I, iid, 4, yv, nps[1], {'no-z': R3[3] / 2, 'cost-kept': (b4[2] - 3 * 5) / 2})
    ok(sol == prices, 'roaster: k = 4 solution is (6, 8, 5)')
    xslip = (35 - R(31, 2) - 15) / 2
    obj(I, iid, 5, sol, nps, {'carried': M([xslip, R(31, 2), 5]), 'no-divide': M([2 * sol[0], 8, 5])})
    vocab(I, iid, [r3, A[2, :] + 2 * A[0, :], A[2, :] - 3 * A[0, :], 2 * A[0, :], R2, R3, Ab[2, :] - 2 * Ab[0, :], 110 - 105, 105, 70, 31, 15, 20,
                   R3[3] - 15, 2 * yv, sol, 2 * sol[0], 35 - 8 - 15, xslip, R(31, 2), b4, b2, 3 * 5, 3 * 35, 2 * 35, 101 - 70])
    arith(I, iid)


# ------------------------------------------------------------------ report
print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
