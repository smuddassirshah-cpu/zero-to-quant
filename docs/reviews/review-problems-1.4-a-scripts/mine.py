"""Second read, vectors problems-1 to -3: the reader's own keys, slips and stated numbers.

Nothing is imported from the author's script. Each key is worked from the item's text (the vectors and matrices below
are typed from the prose) with NumPy, and with sympy where a symbol appears, then compared with the stored answer and
with every stored `wrong` value or `wrong[].tex`. Numbers printed in feedback and explanations are checked beside them.

Usage (repo root): <venv>/bin/python docs/reviews/review-problems-1.4-a-scripts/mine.py [-v]"""
import json
import re
import sys
from math import acos, degrees, sqrt

import numpy as np
import sympy as sp

V = '-v' in sys.argv
checks = fails = 0
notes = []
A = np.array


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)
    elif V:
        print('ok  ', msg)


SETS = {n: json.load(open(f'app/content/courses/vectors/problems-{n}.json')) for n in (1, 2, 3)}
k = sp.Symbol('k')


def part(n, item, j):
    it = next(i for i in SETS[n]['items'] if i['id'] == item)
    return it['parts'][j - 1]


def read(tex):
    """A stored answer or wrong tex as a sympy Matrix: '(a, b)' is a column, a pmatrix its rows."""
    m = re.search(r'\\begin\{pmatrix\}(.*)\\end\{pmatrix\}', tex)
    conv = lambda s: sp.nsimplify(sp.sympify(re.sub(r'(\d)k', r'\1*k', s.strip())), rational=True)
    if m:
        return sp.Matrix([[conv(x) for x in r.split('&')] for r in m.group(1).split('\\\\')])
    if tex.startswith('('):
        return sp.Matrix([conv(x) for x in tex.strip('()').split(',')])
    return conv(tex)


def same(a, b):
    a, b = sp.Matrix([a]) if not hasattr(a, 'shape') else a, sp.Matrix([b]) if not hasattr(b, 'shape') else b
    return a.shape == b.shape and all(abs(complex(sp.simplify(x - y).subs(k, 0.731))) < 1e-9 for x, y in zip(a, b))


def mat(x):
    """my value (list, nested list, numpy array or sympy thing) as a sympy Matrix or scalar"""
    if isinstance(x, (list, tuple, np.ndarray)):
        return sp.Matrix(np.array(x, dtype=object).tolist()).applyfunc(lambda e: sp.nsimplify(e, rational=True, tolerance=1e-12))
    return x


def key(n, item, j, mine, wrongs=None, places=None, pct=False):
    """numeric part: mine is my value (a fraction of 1 for a % part); expression part: mine is a list, matrix or sympy expression."""
    w = part(n, item, j)['widget']
    where = f'problems-{n} {item} {j}'
    stored = {x['id']: x for x in w.get('wrong', [])}
    ok(set(stored) == set(wrongs or {}), f'{where}: every stored wrong re-derived ({sorted(set(stored) ^ set(wrongs or {}))})')
    if w['kind'] == 'numeric':
        tol = w['tol']['abs']
        ok(abs(mine - w['answer']) <= tol + 1e-12, f'{where} answer: mine {mine:.7g}, stored {w["answer"]}')
        ok((w.get('unit') == '%') == pct, f'{where}: unit % as expected')
        if places is not None:
            ok(abs(round(mine * (100 if pct else 1), places) / (100 if pct else 1) - w['answer']) <= tol + 1e-12, f'{where}: my value rounded to {places} places is accepted')
        for wid, val in (wrongs or {}).items():
            if wid in stored:
                ok(abs(val - stored[wid]['value']) <= stored[wid]['tol']['abs'] + 1e-12, f'{where} wrong {wid}: mine {val:.7g}, stored {stored[wid]["value"]}')
        vals = sorted([(w['answer'], tol, 'answer')] + [(x['value'], x['tol']['abs'], x['id']) for x in stored.values()])
        for (a, ta, ia), (b, tb, ib) in zip(vals, vals[1:]):
            ok(a + ta < b - tb, f'{where}: bands of {ia} and {ib} do not touch')
    else:
        ok(same(read(w['answer']), mat(mine)), f'{where} answer: stored {w["answer"]} equals mine')
        for wid, val in (wrongs or {}).items():
            if wid in stored:
                ok(same(read(stored[wid]['tex']), mat(val)), f'{where} wrong {wid}: stored {stored[wid]["tex"]} equals mine')
                ok(not same(read(stored[wid]['tex']), read(w['answer'])), f'{where} wrong {wid} differs from the answer')


def choice(n, item, j, right):
    got = [o['id'] for o in part(n, item, j)['widget']['options'] if o.get('correct')]
    ok(got == [right], f'problems-{n} {item} {j}: correct option {got} is {right}')


ang = lambda a, b: degrees(acos(float(a @ b) / sqrt(float(a @ a) * float(b @ b))))

# ---------------- problems-1 ----------------
u, v, T = A([3., 1.]), A([1., 2.]), A([9., 8.])
ab = np.linalg.solve(np.column_stack([u, v]), T)
key(1, 'p-charging-robot', 1, [2, 3], {'swapped': [3, 2]})
ok(np.allclose(ab, [2, 3]) and 3 * 3 + 2 == 11, 'robot: solve gives (2, 3); the swapped pair gives 11 in the first coordinate')
L1, L2 = 2 * u, 3 * v
key(1, 'p-charging-robot', 2, L1 @ L2, {'unweighted': u @ v, 'only-u': L1 @ v, 'only-v': u @ L2})
key(1, 'p-charging-robot', 3, ang(L1, L2), {'radians': np.radians(ang(L1, L2)), 'no-root': degrees(acos(30 / (40 * 45)))}, 0)
ok(abs(30 / sqrt(1800) - 0.7071) < 5e-5 and abs(sqrt(1800) - 42.43) < 5e-3 and L1 @ L1 == 40 and L2 @ L2 == 45, 'robot: 0.7071, 42.43, 40, 45')
key(1, 'p-charging-robot', 4, np.linalg.norm(L1 + L2), {'no-cross': sqrt(85), 'path': sqrt(40) + sqrt(45), 'minus': np.linalg.norm(L1 - L2), 'no-root': 145}, 2)
ok(9 ** 2 + 8 ** 2 == 145, 'robot: 81 + 64 = 145')

b, w, r = A([.5, .3, .2]), A([.4, .45, .15]), A([.02, -.01, .04])
a = w - b
key(1, 'p-active-bets', 1, a, {'flipped': b - w, 'added': w + b})
ok(abs(a.sum()) < 1e-12, 'active: entries add to 0')
key(1, 'p-active-bets', 2, a @ r, {'flipped': -(a @ r), 'fund': w @ r, 'benchmark': b @ r}, 2, pct=True)
ok(abs(w @ r - 0.0095) < 1e-12 and abs(b @ r - 0.015) < 1e-12, 'active: 0.0095 and 0.015')
key(1, 'p-active-bets', 3, np.linalg.norm(a), {'no-root': a @ a, 'abs-sum': np.abs(a).sum(), 'sum': a.sum()}, 4)
key(1, 'p-active-bets', 4, ang(a, r), {'acute': 180 - ang(a, r), 'radians': np.radians(ang(a, r))}, 0)
ok(abs(np.linalg.norm(r) - 0.04583) < 5e-6 and abs(r @ r - 0.0021) < 1e-12, 'active: |r| = 0.04583')
ok(abs(-0.0055 / (0.1871 * 0.04583) + 0.6415) < 2e-4, 'active: cosine -0.6415 from the rounded values the question hands over')
ok(round(degrees(acos(-0.0055 / (0.1871 * 0.04583)))) == 130, 'active: 130 degrees from the rounded values')

dep, wind = A([12., 16.]), A([-8., 1.])
d = dep / np.linalg.norm(dep)
key(1, 'p-drone-crosswind', 1, d, {'not-unit': [3, 4], 'swapped': d[::-1], 'whole': dep})
key(1, 'p-drone-crosswind', 2, wind @ d, {'sign': -(wind @ d), 'not-unit': wind @ dep, 'three-four': wind @ A([3, 4]), 'swapped': wind @ d[::-1]})
cross = sqrt(wind @ wind - (wind @ d) ** 2)
ok(abs(abs(wind @ A([-.8, .6])) - 7) < 1e-12, 'drone: crosswind 7 by the perpendicular unit vector too')
key(1, 'p-drone-crosswind', 3, cross, {'wind-speed': sqrt(65), 'added': sqrt(65 + 16), 'no-root': 49})
along = sqrt(25 ** 2 - cross ** 2)
key(1, 'p-drone-crosswind', 4, along, {'no-cancel': 25, 'subtracted': 25 - 7, 'no-root': 576})
key(1, 'p-drone-crosswind', 5, 20 / (along + wind @ d) * 60, {'no-wind': 20 / 24 * 60, 'tailwind': 20 / 28 * 60, 'air-only': 20 / 25 * 60, 'hours': 1})
# the whole flight as vectors: air velocity = ground velocity - wind must be 25 long
ground = 20 * d
ok(abs(np.linalg.norm(ground - wind) - 25) < 1e-12, 'drone: ground velocity 20 km/h along the route needs an air speed of exactly 25')

w, c, s = A([.6, .3, .1]), A([.01, -.12, .08]), A([-.03, .04, -.02])
key(1, 'p-stress-hedge', 1, w @ c, {'unweighted': c.sum(), 'equal': c.mean()}, 1, pct=True)
shift = A([0, -1, 1])
h = -(w @ c) / (shift @ c)
key(1, 'p-stress-hedge', 2, h, {'sign': -(w @ c) / (-0.12 + 0.08), 'gold-only': 0.022 / 0.08, 'equity-only': 0.022 / 0.12}, 2)
w2 = w + h * shift
ok(np.allclose(w2, [.6, .19, .21]) and abs(w2 @ c) < 1e-12, 'hedge: new weights (0.6, 0.19, 0.21) are at right angles to c')
key(1, 'p-stress-hedge', 3, w2 @ s, {'old': w @ s, 'shift-added': w @ s + 0.11 * 0.06}, 2, pct=True)
ok(abs(0.11 * (0.04 + 0.02) - 0.0066) < 1e-12, 'hedge: the move costs 0.0066')
key(1, 'p-stress-hedge', 4, w2 @ (c + s) / 2, {'unhedged': w @ (c + s) / 2, 'no-half': w2 @ (c + s)}, 2, pct=True)

# ---------------- problems-2 ----------------
S, D, top = A([[1, .25], [0, 1]]), A([[1.5, 0], [0, 1]]), A([2., 8.])
key(2, 'p-italic-letters', 1, S, {'rows': S.T})
key(2, 'p-italic-letters', 2, S @ top, {'rows': S.T @ top, 'once': top + A([.25, 0])})
key(2, 'p-italic-letters', 3, D @ S, {'order': S @ D, 'entrywise': D * S})
key(2, 'p-italic-letters', 4, (D @ S @ top)[0], {'order': (S @ D @ top)[0], 'slant-only': (S @ top)[0], 'widen-only': (D @ top)[0]})

R = A([[.8, -.6], [.6, .8]])
key(2, 'p-site-plan', 1, R, {'clockwise': R.T, 'swapped': [[.6, -.8], [.8, .6]]})
key(2, 'p-site-plan', 2, R.T @ R, {'square': R @ R, 'entrywise': R.T * R})
gpt = A([11., 2.])
key(2, 'p-site-plan', 3, R.T @ gpt, {'forward': R @ gpt, 'swapped': A([[.6, .8], [-.8, .6]]) @ gpt})
step = R @ (A([10., 5.]) - A([10., -5.]))
ok(np.allclose(step, [-6, 8]), 'site: the ground step is (-6, 8)')
e1 = A([1., 0.])
key(2, 'p-site-plan', 4, ang(step, e1), {'plan-angle': 90, 'clockwise': ang(R.T @ A([0, 10.]), e1), 'theta': degrees(acos(.8))}, 1)
notes.append(f'site 4: the acute angle between the pipe as a line and the ground x-axis is {180 - ang(step, e1):.1f}, the stored `clockwise` value')

wf = A([.5, .3, .2]); B = A([[1.2, .4], [.8, -.5], [1., 1.]]); Fm = A([[.0225, .003], [.003, .0064]])
choice(2, 'p-factor-risk', 1, 'bt-w')
e = B.T @ wf
key(2, 'p-factor-risk', 2, e, {'unweighted': B.sum(axis=0), 'equal': B.mean(axis=0)})
key(2, 'p-factor-risk', 3, Fm @ e, {'diagonal': np.diag(np.diag(Fm)) @ e, 'wrong-order': (Fm @ e)[::-1]})
var = e @ Fm @ e
ok(abs(var - wf @ (B @ Fm @ B.T) @ wf) < 1e-15, 'factor: e^T F e equals w^T (B F B^T) w')
key(2, 'p-factor-risk', 4, var, {'diagonal': e @ np.diag(np.diag(Fm)) @ e, 'no-f': e @ e, 'sum': (Fm @ e).sum()}, 5)
ok(abs(2 * 1.04 * .25 * .003 - .00156) < 1e-12 and abs(1.04 * .02415 - .025116) < 1e-9 and abs(.25 * .00472 - .00118) < 1e-12, 'factor: 0.00156, 0.025116, 0.00118')
key(2, 'p-factor-risk', 5, sqrt(0.0263), {'diagonal': sqrt(0.02474), 'no-root': 0.0263}, 1, pct=True)
ok(abs(sqrt(var) - 0.162) <= 0.0005 and np.linalg.det(Fm) > 0, 'factor: volatility from the unrounded variance; F is a valid covariance matrix')

Q = A([[.5, .3], [.1, .2], [.05, .2]]); pr = A([.8, 1.5, 6.]); x = A([40., 12.])
key(2, 'p-bakery-costs', 1, Q @ x, {'swapped': Q @ x[::-1], 'one-each': Q.sum(axis=1)})
key(2, 'p-bakery-costs', 2, pr @ (Q @ x), {'swapped': pr @ (Q @ x[::-1]), 'unpriced': (Q @ x).sum()}, 2)
ok(abs(6 * 4.4 / 54.88 - 0.48) < 0.005 and 4.4 / 34.4 < 0.15, 'bakery: butter nearly half the cost, a small share of the weight')
choice(2, 'p-bakery-costs', 3, 'qt-p')
cst = Q.T @ pr
ok(np.allclose(cst, [.85, 1.74]) and abs(cst @ x - 54.88) < 1e-9, 'bakery: c = (0.85, 1.74) and c.x = 54.88')
key(2, 'p-bakery-costs', 4, cst[1], {'loaf': cst[0], 'unpriced': Q[:, 1].sum()}, 2)
key(2, 'p-bakery-costs', 5, cst @ A([50., 20.]), {'this-week': 54.88, 'swapped': cst @ A([20., 50.]), 'one-each': cst.sum()}, 2)

# ---------------- problems-3 ----------------
Ag = A([[.4, .1], [.2, .3]]); bg = A([13., 14.])
key(3, 'p-goat-feed', 1, Ag, {'transposed': Ag.T})
key(3, 'p-goat-feed', 2, np.linalg.det(Ag), {'added': .12 + .02, 'flipped': -.1})
adj = A([[.3, -.1], [-.2, .4]])
key(3, 'p-goat-feed', 3, np.linalg.inv(Ag), {'no-divide': adj, 'no-negate': [[3, 1], [2, 4]], 'transposed': np.linalg.inv(Ag.T), 'times-det': adj * .1})
key(3, 'p-goat-feed', 4, np.linalg.solve(Ag, bg), {'transposed': np.linalg.inv(Ag.T) @ bg, 'no-divide': adj @ bg, 'swapped': np.linalg.solve(Ag, bg)[::-1]})

Ak = sp.Matrix([[12, 8], [3, k]])
ok(sp.expand(Ak.det() - (12 * k - 24)) == 0, 'paint: det = 12k - 24')
key(3, 'p-paint-tints', 1, float(sp.solve(Ak.det(), k)[0]), {'plus': -2, 'mixed': 4.5})
A2 = A([[12., 8.], [3., 2.]])
key(3, 'p-paint-tints', 2, np.linalg.matrix_rank(A2), {'full': 2, 'zero': 0})
choice(3, 'p-paint-tints', 3, 'none')
ok(np.linalg.matrix_rank(np.column_stack([A2, [60, 18]])) == 2 and np.linalg.matrix_rank(np.column_stack([A2, [60, 15]])) == 1, 'paint: (60, 18) has no mix, (60, 15) has many')
key(3, 'p-paint-tints', 4, (60 - 12 * 3) / 8, {'q-only': 60 / 8, 'p-only': 0})
A5 = A([[12., 8.], [3., 5.]])
key(3, 'p-paint-tints', 5, np.linalg.solve(A5, [64, 22]), {'swapped': [2, 4], 'no-divide': A([[5, -8], [-3, 12.]]) @ A([64, 22.])})

M = A([[.8, .3], [.2, .7]]); rd = A([130., 70.])
key(3, 'p-colour-sensor', 1, abs(np.linalg.det(M)), {'added': .56 + .06, 'diagonal': .56})
adjM = A([[.7, -.3], [-.2, .8]])
Minv = np.linalg.inv(M)
key(3, 'p-colour-sensor', 2, Minv, {'no-divide': adjM, 'times-det': adjM * .5, 'no-negate': [[1.4, .6], [.4, 1.6]]})
star = Minv * rd
ok(np.allclose(star, [[182, -42], [-52, 112]]), 'sensor: Minv * r is [[182, -42], [-52, 112]] (NumPy broadcasts r along the columns)')
key(3, 'p-colour-sensor', 3, star[0, 1], {'matrix-product': (Minv @ rd)[0], 'entry-10': star[1, 0], 'entry-00': star[0, 0]})
key(3, 'p-colour-sensor', 4, Minv @ rd, {'no-divide': adjM @ rd, 'forward': M @ rd, 'column-sums': star.sum(axis=0)})
ok(np.allclose(star.sum(axis=1), [140, 60]) and np.allclose(M @ [140, 60], rd), 'sensor: row sums give (140, 60); M(140, 60) = (130, 70)')

Am, Bk = sp.Matrix([[3, 1], [2, 1]]), sp.Matrix([[2, k], [1, 1]])
Ck = Bk * Am
key(3, 'p-engraver-dial', 1, Ck, {'order': Am * Bk, 'entrywise': sp.Matrix([[6, k], [2, 1]])})
key(3, 'p-engraver-dial', 2, sp.expand(Ck.det()), {'added': sp.expand(Ck[0, 0] * Ck[1, 1] + Ck[0, 1] * Ck[1, 0]), 'flipped': sp.expand(-Ck.det())})
ok(sp.expand(Bk.det() * Am.det() - Ck.det()) == 0 and Am.det() == 1, 'engraver: det C = det B det A, det A = 1')
key(3, 'p-engraver-dial', 3, float(sp.solve(Ck.det(), k)[0]), {'added': -22 / 9})
C1 = Ck.subs(k, 1)
ok(C1 == sp.Matrix([[8, 3], [5, 2]]) and C1.det() == 1, 'engraver: C_1 = [[8, 3], [5, 2]], det 1')
AB1 = (Am * Bk).subs(k, 1)
key(3, 'p-engraver-dial', 4, C1.inv(), {'no-negate': sp.Matrix([[2, 3], [5, 8]]), 'unswapped': sp.Matrix([[8, -3], [-5, 2]]), 'order': AB1.inv()})
mark = sp.Matrix([19, 12])
key(3, 'p-engraver-dial', 5, C1.inv() * mark, {'order': AB1.inv() * mark, 'forward': C1 * mark, 'unswapped': sp.Matrix([[8, -3], [-5, 2]]) * mark})
ok(Am * sp.Matrix([2, 1]) == sp.Matrix([7, 5]) and Bk.subs(k, 1) * sp.Matrix([7, 5]) == mark, 'engraver: forwards (2, 1) -> (7, 5) -> (19, 12)')

# ---------------- shape of each set ----------------
for n, dset in SETS.items():
    parts = [p for it in dset['items'] for p in it['parts']]
    typed = sum(p['widget']['kind'] != 'choice' for p in parts)
    ok(3 * typed >= 2 * len(parts), f'problems-{n}: typed {typed} of {len(parts)}')
    ok(any(it['difficulty'] == 5 for it in dset['items']) and all(3 <= it['difficulty'] <= 5 for it in dset['items']), f'problems-{n}: difficulties')
    ok(all(3 <= len(it['parts']) <= 5 for it in dset['items']) and 3 <= len(dset['items']) <= 5, f'problems-{n}: counts')
    for it in dset['items']:
        for j, p in enumerate(it['parts'], 1):
            w = p['widget']
            by = set(p['feedback'].get('byKey', {})) - {'form', 'length'}
            ids = [x['id'] for x in w.get('wrong', [])]
            if w['kind'] != 'choice':
                ok(set(ids) == by, f'problems-{n} {it["id"]} {j}: byKey lines match the wrong ids')
    print(f'problems-{n}: {len(dset["items"])} problems, {len(parts)} parts, {typed} typed')
for s_ in notes:
    print('note:', s_)
print(f'mine.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
