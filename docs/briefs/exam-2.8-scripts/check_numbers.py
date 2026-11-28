"""Recompute every number stated in app/content/exams/topic-2.8.json by a second route and assert it at its path.

Route A is build.py (floats and closed forms). Route B here is independent: exact Fractions for every sum, chance and
weight, a NumPy linear solve for the two-state values, Simpson integration of the Beta densities, a brute-force game
search for the stick game and the tree, a fixed-point iteration for the stopping problems, and both code items run in
CPython: the solution passes every hidden test and example, the starter fails every test, each mutant first fails its
named test, and a second implementation written differently (index arrays, its own random calls) gives every seeded
expected value. Coverage runs strict: every number on screen is compared or marked literal with a reason.
Run: ZQ_NUMBERS_STRICT=1 python3 docs/briefs/exam-2.8-scripts/check_numbers.py
"""
import json
import math
import os
import random
import signal
import sys
import time
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-2.8.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam"), coverage strict."""

    def __init__(self, path):
        self.course, self.n, self.results, self.coverage = 'exam', 0, [], 'strict'
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
items = doc['items']
idx = {it['id']: k for k, it in enumerate(items)}


def P(iid, part=None):
    base = f'items[{idx[iid]}]'
    return base if part is None else f'{base}.parts[{part}]'


def W(iid, part=None):
    return P(iid, part) + '.widget'


def node(path):
    return _walk(doc, path)[0]


def key(iid, value, part=None, nd=None):
    w = node(W(iid, part))
    v = float(value)
    want = round(v, nd) if nd is not None else v
    ok = abs(w['answer'] - want) <= 1e-9 and abs(w['answer'] - v) <= w['tol']['abs'] + 1e-12
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {want!r}', '' if ok else 'route B differs')


CHECKED = set()


def wrong(iid, wid, value, part=None):
    CHECKED.add((iid, part, wid))
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    ok = len(hit) == 1 and abs(hit[0]['value'] - float(value)) <= max(hit[0]['tol']['abs'], 1e-9)
    ex._rec(ok, f'{iid} wrong "{wid}" = {float(value)!r}', '' if ok else f'found {hit}')


def say(iid, path, value, part=None, nd=None):
    v = float(value) if isinstance(value, F) else value
    if nd is not None:
        v = round(v, nd)
    ex.expect('exam', f'{P(iid, part)}.{path}', v)


def given(iid, path, *vals):
    """Inputs stated in the item: each must appear in its text (they are then used below)."""
    for v in vals:
        say(iid, path, v)


def correct_id(iid, part=None):
    return [o['id'] for o in node(W(iid, part))['options'] if o.get('correct')]


def r4(x):
    return round(float(x), 4)


# ------------------------------------------------------------------ difficulty 2
# e-regret-four-venues
iid = 'e-regret-four-venues'
ps, ns = [F(52, 100), F(48, 100), F(61, 100), F(55, 100)], [300, 150, 400, 150]
given(iid, 'prose', 0.52, 0.48, 0.61, 0.55, 300, 150, 400, 1000)
best = max(ps)
reg = sum(n * (best - p) for n, p in zip(ns, ps))
key(iid, reg)
wrong(iid, 'fills', sum(n * p for n, p in zip(ns, ps)))
wrong(iid, 'per-order', reg / 1000)
wrong(iid, 'worst-only', 150 * (best - F(48, 100)))
for v in (0.09, 0.13, 0.06, 27, 19.5, 9, 55.5):
    say(iid, 'feedback.correct', v)
say(iid, 'feedback.byKey.fills', 1000 * best)
for v in (300, 0.09, 150, 0.13, 0.06, 55.5):
    say(iid, 'explain.text', v)

# e-return-with-fees
iid = 'e-return-with-fees'
rw, g = [3, -1, 0, 5], F(4, 5)
G = sum(g ** k * x for k, x in enumerate(rw))
key(iid, G)
wrong(iid, 'no-disc', sum(rw))
wrong(iid, 'disc-first', G * g)
wrong(iid, 'fee-added', sum(g ** k * abs(x) for k, x in enumerate(rw)))
say(iid, 'feedback.correct', g ** 3)
say(iid, 'feedback.byKey.fee-added', g)
say(iid, 'explain.text', g ** 2)
say(iid, 'explain.text', g ** 3 * 5)
given(iid, 'prose', 0.8)

# e-td-wide-spread
iid = 'e-td-wide-spread'
V, rr, Vn, a, g = F(2, 5), F(-1, 10), F(9, 10), F(1, 5), F(19, 20)
given(iid, 'prose', 0.4, -0.1, 0.9, 0.2, 0.95)
delta = rr + g * Vn - V
key(iid, V + a * delta)
wrong(iid, 'delta', delta)
wrong(iid, 'no-disc', V + a * (rr + Vn - V))
wrong(iid, 'target', rr + g * Vn)
say(iid, 'feedback.correct', a * delta)
say(iid, 'feedback.byKey.no-disc', rr + Vn - V)
say(iid, 'explain.text', g * Vn)

# e-softmax-three-dials: route B by series for e
e1 = sum(F(1, math.factorial(k)) for k in range(25))
ein = sum(F((-1) ** k, math.factorial(k)) for k in range(25))
tot = e1 + 1 + ein
iid = 'e-softmax-three-dials'
key(iid, e1 / tot, nd=4)
wrong(iid, 'two-moves', e1 / (e1 + 1))
wrong(iid, 'uniform', F(1, 3))
wrong(iid, 'third', ein / tot)
say(iid, 'feedback.correct', r4(e1))
say(iid, 'feedback.correct', r4(tot))
for v in (e1, ein, tot, e1 / tot, 1 / tot, ein / tot):
    say(iid, 'explain.text', r4(v))

# e-three-replies: brute-force minimax
iid = 'e-three-replies'
tree = {'a': [6, 2, 9], 'b': [5, 7, 4], 'c': [8, 3, 10]}
given(iid, 'prose', 6, 2, 9, 5, 7, 4, 8, 3, 10)
val = max(min(v) for v in tree.values())
key(iid, val)
wrong(iid, 'helps', max(max(v) for v in tree.values()))
wrong(iid, 'worst', min(min(v) for v in tree.values()))
wrong(iid, 'average', F(sum(tree['c']), 3))
ex._rec(max(tree, key=lambda k: sum(tree[k])) == 'c', 'e-three-replies: c has the best average', '')

# e-beta-new-quote
iid = 'e-beta-new-quote'
a0, b0, k, n = 2, 4, 9, 15
key(iid, F(a0 + k, a0 + b0 + n), nd=4)
wrong(iid, 'raw', F(k, n))
wrong(iid, 'flat', F(1 + k, 2 + n))
wrong(iid, 'swap', F(a0 + n - k, a0 + b0 + n))
wrong(iid, 'prior', F(a0, a0 + b0))
say(iid, 'feedback.correct', F(a0 + k, a0 + b0 + n), nd=4)
say(iid, 'feedback.correct', 11)
say(iid, 'feedback.byKey.raw', 15)
say(iid, 'feedback.correct', 21)
say(iid, 'explain.text', 0.6)

# ------------------------------------------------------------------ difficulty 3
# e-ucb-three-venues: scores by Decimal-free floats via a second formula (bonus^2 = 2 ln t / n)
iid = 'e-ucb-three-venues'
rec = {'P': (90, 0.58), 'Q': (40, 0.55), 'R': (20, 0.40)}
two_ln = 2 * math.log1p(149)
say(iid, 'prose', r4(two_ln))
bon = {kk: (two_ln / nn) ** 0.5 for kk, (nn, m) in rec.items()}
sc = {kk: m + bon[kk] for kk, (nn, m) in rec.items()}
ex._rec(max(sc, key=sc.get) == 'R' and correct_id(iid) == ['R'], 'e-ucb-three-venues: R has the top score and is the key', '')
for kk in sc:
    say(iid, 'widget.options', r4(sc[kk]))
    say(iid, 'explain.text', r4(bon[kk]))
say(iid, 'widget.options', r4(bon['P']))
say(iid, 'widget.options', r4(bon['R']))
for kk in sc:
    say(iid, 'feedback.correct', r4(sc[kk]))
given(iid, 'prose', 0.58, 0.55, 0.40, 90, 40, 20)
ex._rec(sum(nn for nn, m in rec.values()) == 150, 'e-ucb-three-venues: the pulls add to t = 150', '')

# e-floor-five-signals
iid = 'e-floor-five-signals'
ps = [F(30, 100), F(42, 100), F(50, 100), F(56, 100), F(62, 100)]
qbar = sum(ps) / 5
fl = 25000 * F(12, 100) * (max(ps) - qbar)
key(iid, fl)
wrong(iid, 'per-trade', fl / 25000)
wrong(iid, 'no-eps', 25000 * (max(ps) - qbar))
wrong(iid, 'worst', 25000 * F(12, 100) * (max(ps) - min(ps)))
say(iid, 'feedback.correct', qbar)
say(iid, 'feedback.byKey.no-eps', max(ps) - qbar)
say(iid, 'feedback.byKey.worst', max(ps) - min(ps))
say(iid, 'explain.text', 25000 * F(12, 100))
say(iid, 'explain.text', max(ps) - qbar)
given(iid, 'prose', 0.30, 0.42, 0.50, 0.56, 0.62, 0.12, 25000)
ex.literal('12%', why='the stated exploring rate 0.12 written as a percentage in a byKey line')

# e-ewma-old-reward: weight by unrolling the recursion on a reward stream
iid = 'e-ewma-old-reward'
al = F(1, 4)
weights = [F(0)] * 6          # weight of reward j (0 = oldest of six) after all six updates
for t in range(6):
    weights = [w * (1 - al) for w in weights]
    weights[t] += al
wk = weights[5 - 4]            # four updates before the latest
key(iid, wk, nd=4)
ex._rec(weights[5] == al, 'e-ewma-old-reward: the latest reward carries alpha', '')
wrong(iid, 'no-alpha', wk / al)
wrong(iid, 'k-plus', weights[5 - 5])
wrong(iid, 'k-minus', weights[5 - 3])
say(iid, 'explain.text', 1 - al)
say(iid, 'feedback.byKey.no-alpha', al)

# e-quiet-or-carrying: NumPy solve
iid = 'e-quiet-or-carrying'
Pm = np.array([[0.7, 0.3], [0.6, 0.4]])
rv = np.array([2.0, -1.0])
v = np.linalg.solve(np.eye(2) - 0.9 * Pm, rv)
key(iid, v[0], nd=4)
wrong(iid, 'inventory', v[1])
wrong(iid, 'gamma-r', np.linalg.solve(np.eye(2) - 0.9 * Pm, 0.9 * rv)[0])
wrong(iid, 'n-only', 2 / (1 - 0.9))
A = np.eye(2) - 0.9 * Pm
for x in (A[0, 0], abs(A[0, 1]), A[1, 0], A[1, 1], 1.01, round(np.linalg.det(A), 6)):   # 0.27 follows a binary minus
    say(iid, 'feedback.correct', round(float(x), 4))
say(iid, 'feedback.correct', round(float(v[0]), 2))
say(iid, 'explain.text', round(float(v[0]), 2))
say(iid, 'explain.text', round(float(v[1]), 2))
say(iid, 'explain.text', round(float(v[0] - v[1]), 2))
ex._rec(abs(2 * A[1, 1] + A[0, 1] * 1 - 1.01) < 1e-12, 'e-quiet-or-carrying: Cramer numerator 2 x 0.64 - 0.27 = 1.01', '')
given(iid, 'prose', 0.3, 0.6, 0.9)

# e-slip-bottom-row: from the shown values, by listing the landings
iid = 'e-slip-bottom-row'
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'content', 'data', 'ai'))
import rl_ops_l3 as g3  # noqa: E402  (read only: the course grid's transition model)
tr = g3.transition('r4c3', 'R', 0.1)
shown = {'r4c3': F(2168, 10000), 'r4c4': F(2830, 10000), 'r3c3': F(2915, 10000)}
for s, x in shown.items():
    say(iid, 'prose', x)
score = sum(F(p).limit_denominator(100) * (F(-4, 100) + F(9, 10) * shown[t]) for t, p in tr.items())
key(iid, score, nd=4)
wrong(iid, 'no-slip', F(-4, 100) + F(9, 10) * shown['r4c4'])
wrong(iid, 'edge-zero', F(-4, 100) + F(9, 10) * (F(8, 10) * shown['r4c4'] + F(1, 10) * shown['r3c3']))
wrong(iid, 'no-step', score + F(4, 100))
ex._rec(set(tr) == {'r4c4', 'r3c3', 'r4c3'}, 'e-slip-bottom-row: R from r4c3 lands r4c4, r3c3 or stays', str(tr))


# the course grid's optimal values, to check that the shown values and "U is best" hold
def vi_course(slip, gamma=0.9):
    Vc = {s: 0.0 for s in g3.CELLS}
    for _ in range(400):
        Vc = {s: 0.0 if s in g3.TERMINAL else max(sum(p * (g3.reward(t) + gamma * Vc[t]) for t, p in g3.transition(s, aa, slip).items()) for aa in 'URDL') for s in g3.CELLS}
    return Vc


Vc = vi_course(0.1)
Vd = vi_course(0.0)
ex._rec(all(abs(Vc[s] - float(x)) < 5e-5 for s, x in shown.items()), 'e-slip-bottom-row: shown values are V* to 4 places', '')
qc = {aa: sum(p * (g3.reward(t) + 0.9 * Vc[t]) for t, p in g3.transition('r4c3', aa, 0.1).items()) for aa in 'URDL'}
ex.stated('exam', P(iid) + '.explain.text', 'U is, and its score equals', max(qc, key=qc.get) == 'U' and abs(qc['U'] - Vc['r4c3']) < 1e-9)
for v in (0.2830, 0.2915, 0.2168, 0.2095):
    say(iid, 'feedback.correct', v)
say(iid, 'feedback.byKey.edge-zero', 0.2168)
for v in (0.8, 0.1, 0.2095, 0.2168):
    say(iid, 'explain.text', v)
given(iid, 'prose', 0.8, 0.1, 0.04, 0.9)
say(iid, 'feedback.byKey.no-step', 0.04)

# e-certificate-sweeps: smallest k by counting up
iid = 'e-certificate-sweeps'
gg, c1, tg = F(4, 5), F(5, 2), F(1, 1000)


def first_k(cond):
    kk = 0
    while not cond(kk):
        kk += 1
    return kk


k12 = first_k(lambda kk: gg ** kk * c1 / (1 - gg) <= tg)
key(iid, k12)
wrong(iid, 'no-tail', first_k(lambda kk: gg ** kk * c1 <= tg))
wrong(iid, 'floor', k12 - 1)
wrong(iid, 'no-first', first_k(lambda kk: gg ** kk / (1 - gg) <= tg))
say(iid, 'feedback.correct', tg * (1 - gg) / c1)
say(iid, 'feedback.correct', round(math.log(8e-5) / math.log(0.8), 1))
say(iid, 'feedback.correct', 1 - gg)
say(iid, 'explain.text', round(math.log(8e-5) / math.log(0.8), 1))
say(iid, 'explain.text', tg * (1 - gg) / c1)
say(iid, 'feedback.byKey.no-tail', 1 / (1 - gg))
say(iid, 'feedback.byKey.floor', 42)
say(iid, 'feedback.byKey.no-first', 2.5)
given(iid, 'prose', 0.8, 2.5)
given(iid, 'question', 0.001)

# e-mc-two-episodes: forward sums
iid = 'e-mc-two-episodes'
g9 = F(9, 10)
e1r, e2r = [1, -2, 4, 3], [0, 3]


def fwd(rew, t, gm):
    return sum(gm ** (j - t) * rew[j] for j in range(t, len(rew)))


G1, G1b, G2 = fwd(e1r, 0, g9), fwd(e1r, 2, g9), fwd(e2r, 0, g9)
key(iid, (G1 + G2) / 2, nd=4)
wrong(iid, 'every', (G1 + G1b + G2) / 3)
wrong(iid, 'no-disc', F(fwd(e1r, 0, 1) + fwd(e2r, 0, 1), 2))
wrong(iid, 'ep1', G1)
say(iid, 'feedback.correct', G1)
say(iid, 'feedback.correct', G2)
say(iid, 'feedback.correct', (G1 + G2) / 2)
say(iid, 'feedback.byKey.every', G1b)
for v in (fwd(e1r, 3, g9), G1b, fwd(e1r, 1, g9), G1, G2, (G1 + G2) / 2):
    say(iid, 'explain.text', v)
given(iid, 'prose', 0.9)

# e-optimistic-end-cell
iid = 'e-optimistic-end-cell'
q, rr, a, gm, q0 = F(6, 5), F(96, 100), F(1, 5), F(9, 10), F(6, 5)
key(iid, q + a * (rr - q))
wrong(iid, 'no-mask', q + a * (rr + gm * q0 - q))
wrong(iid, 'target', rr)
wrong(iid, 'no-step', q + a * (1 - q))
say(iid, 'explain.text', gm * q0)
say(iid, 'feedback.byKey.no-mask', q0)
say(iid, 'feedback.byKey.no-step', 0.04)
say(iid, 'feedback.byKey.no-step', rr)
say(iid, 'feedback.correct', rr)
given(iid, 'prose', 1.2, 0.04, 0.96, 0.2, 0.9)
ex._rec(max(max(sum(p * (g3.reward(t) + 0.9 * Vd[t]) for t, p in g3.transition(c, aa, 0.0).items()) for aa in 'URDL') for c in g3.OPEN) <= 0.96 + 1e-12, 'e-optimistic-end-cell: no Q* on the deterministic grid is above 0.96, so 1.2 is optimistic', '')
say(iid, 'explain.text', q)
say(iid, 'feedback.correct', q)

# e-step-size-rule: the two sums, numerically
iid = 'e-step-size-rule'
h = sum(1 / k for k in range(1, 10 ** 6))
s2 = sum(1 / k ** 2 for k in range(1, 10 ** 6))
s4 = sum(1 / k ** 4 for k in range(1, 10 ** 6))
ex._rec(h > 13 and s2 < 1.65 and s4 < 1.1, 'e-step-size-rule: sum 1/n diverges (13.8 by a million), sum 1/n^2 and 1/n^4 stay finite', '')
ex._rec(correct_id(iid) == ['harmonic'], 'e-step-size-rule key is 1/n', '')
given(iid, 'prose', 0.007)
say(iid, 'widget.options', 0.1)

# e-venue-three-estimate
iid = 'e-venue-three-estimate'
pi, rw = [F(1, 2), F(3, 10), F(1, 5)], 12
score = [(1 if j == 2 else 0) - pi[j] for j in range(3)]
key(iid, rw * score[0])
wrong(iid, 'sign', -rw * score[0])
wrong(iid, 'pulled-chance', -rw * pi[2])
wrong(iid, 'own-dial', rw * score[2])
for v in score:
    say(iid, 'explain.text', v)
say(iid, 'feedback.correct', score[0])
say(iid, 'feedback.byKey.pulled-chance', pi[2])
say(iid, 'feedback.byKey.own-dial', pi[2])
ex._rec(sum(score) == 0, 'e-venue-three-estimate: score entries sum to 0', '')
given(iid, 'prose', 0.5, 0.3, 0.2, 12)

# e-baseline-mean-payment
iid = 'e-baseline-mean-payment'
pi, rw = [F(3, 4), F(1, 4)], [4, 12]
J = sum(p * x for p, x in zip(pi, rw))
ex._rec(J == 6, 'e-baseline-mean-payment: the mean payment is 6', '')


def ests(b):
    return [(rw[0] - b) * (1 - pi[0]), (rw[1] - b) * (0 - pi[0])]


def mom(b):
    e = ests(b)
    m = sum(p * x for p, x in zip(pi, e))
    return m, sum(p * x * x for p, x in zip(pi, e)) - m * m, sum(p * x * x for p, x in zip(pi, e))


m6, var6, sq6 = mom(J)
key(iid, var6)
wrong(iid, 'nomean', sq6)
wrong(iid, 'sd', math.sqrt(var6))
wrong(iid, 'none', mom(0)[1])
ex._rec(m6 == mom(0)[0] == pi[0] * (rw[0] - J), 'e-baseline-mean-payment: the mean is the true gradient with and without b', '')
for v in ests(J) + [m6, sq6, var6]:
    say(iid, 'feedback.correct', v)
say(iid, 'feedback.byKey.nomean', m6 ** 2)
for v in ests(0) + [mom(0)[1], m6, var6]:
    say(iid, 'explain.text', v)
given(iid, 'prose', 0.75, 0.25, 6)

# e-ab-nine-leaves: alpha-beta by a recursive search with a leaf counter
iid = 'e-ab-nine-leaves'
br = [(4, 8, 6), (9, 7, 2), (3, 9, 9)]
given(iid, 'prose', 4, 8, 6, 9, 7, 2, 3)
cnt = [0]


def ab(nodes, maximise, alpha, beta):
    if isinstance(nodes, int):
        cnt[0] += 1
        return nodes
    best = -math.inf if maximise else math.inf
    for ch in nodes:
        v = ab(ch, not maximise, alpha, beta)
        if maximise:
            best, alpha = max(best, v), max(alpha, v)
        else:
            best, beta = min(best, v), min(beta, v)
        if alpha >= beta:
            break
    return best


root = ab([list(b) for b in br], True, -math.inf, math.inf)
key(iid, cnt[0])
wrong(iid, 'all', 9)
wrong(iid, 'value', root)
wrong(iid, 'first-leaf', 3 + 1 + 1)
ex._rec(root == max(min(b) for b in br) == 4, 'e-ab-nine-leaves: root value 4 equals plain minimax', '')

# e-uct-six-of-nine
iid = 'e-uct-six-of-nine'
avg = F(6, 9)
bonus = math.sqrt(2 * math.log(30) / 9)
key(iid, float(avg) + bonus, nd=4)
wrong(iid, 'nob', avg)
wrong(iid, 'nosq', float(avg) + math.sqrt(2) * math.log(30) / 9)
wrong(iid, 'own-n', float(avg) + math.sqrt(2 * math.log(9) / 9))
say(iid, 'feedback.correct', r4(avg))
say(iid, 'feedback.correct', r4(bonus))
say(iid, 'feedback.correct', r4(float(avg) + bonus))
ex.claim(True, 'e-uct-six-of-nine: "30 / 9" is ln 30 over 9 visits, inputs stated in the prose', covers=[30 / 9])
for v in (math.log(30), math.log(30) / 9, bonus, avg, float(avg) + bonus):
    say(iid, 'explain.text', r4(v))

# e-selfplay-update
iid = 'e-selfplay-update'
q, opp, a = F(1, 5), F(-3, 5), F(1, 2)
key(iid, q + a * (-opp - q))
wrong(iid, 'sign', q + a * (opp - q))
wrong(iid, 'target', -opp)
say(iid, 'feedback.correct', -opp)
say(iid, 'feedback.correct', -opp - q)
say(iid, 'feedback.byKey.sign', -opp)
given(iid, 'prose', 0.5, 0.2, -0.6)
say(iid, 'explain.text', -0.6)
say(iid, 'explain.text', 0.4)


# ------------------------------------------------------------------ difficulty 4
def simpson(f, n=2000):
    hh = 1 / n
    return hh / 3 * sum((1 if k in (0, n) else 4 if k % 2 else 2) * f(k * hh) for k in range(n + 1))


iid = 'e-thompson-one-try-each'
pB05 = simpson(lambda v: 2 * (1 - 0.5 * v) * 0.5, 2000)       # B's density on [0, 0.5], with u = 0.5v
key(iid, pB05, part=0, nd=2)
wrong(iid, 'density', 2 * (1 - 0.5), part=0)
wrong(iid, 'uniform', 0.5, part=0)
wrong(iid, 'a-cdf', 0.5 ** 2, part=0)
pAB = simpson(lambda x: 2 * x * (2 * x - x * x))
key(iid, pAB, part=1, nd=4)
wrong(iid, 'uniform-b', simpson(lambda x: 2 * x * x), part=1)
wrong(iid, 'half', 0.5, part=1)
key(iid, 60 * F(5, 6), part=2)
wrong(iid, 'all', 60, part=2)
wrong(iid, 'half', 30, part=2)
pAB2 = simpson(lambda x: 3 * x * x * (2 * x - x * x))
key(iid, pAB2, part=3, nd=2)
wrong(iid, 'old', pAB, part=3)
wrong(iid, 'uniform-b', simpson(lambda x: 3 * x ** 3), part=3)
# a Monte Carlo check of both chances
rng = random.Random(11)
mc1 = sum(rng.betavariate(2, 1) > rng.betavariate(1, 2) for _ in range(200000)) / 200000
mc2 = sum(rng.betavariate(3, 1) > rng.betavariate(1, 2) for _ in range(200000)) / 200000
ex._rec(abs(mc1 - 5 / 6) < 0.005 and abs(mc2 - 0.9) < 0.005, f'e-thompson-one-try-each: sampled chances {mc1:.4f} and {mc2:.4f}', '')
say(iid, 'feedback.correct', 0.25, part=0)
say(iid, 'feedback.correct', 0.75, part=0)
say(iid, 'feedback.byKey.density', 0.5, part=0)
say(iid, 'question', 0.5, part=0)
say(iid, 'feedback.correct', F(4, 3), part=1)
say(iid, 'feedback.correct', F(1, 2), part=1)
say(iid, 'feedback.correct', round(pAB, 4), part=1)
say(iid, 'question', F(5, 6), part=2)
say(iid, 'feedback.correct', F(5, 6), part=2)
say(iid, 'feedback.correct', F(3, 2), part=3)
say(iid, 'feedback.correct', F(3, 5), part=3)
say(iid, 'feedback.byKey.uniform-b', F(3, 4), part=3)
say(iid, 'explain.text', F(5, 6))
say(iid, 'explain.text', 0.9)
ex._rec(abs(1 - pAB2 - 0.1) < 1e-9, 'e-thompson-one-try-each: B wins one draw in ten after A\'s second fill', '')

# e-take-or-wait: fixed-point iteration of each rule
iid = 'e-take-or-wait'
offers = [1, 2, 3, 4, 5]
gw = F(3, 4)


def rule_fixed(kmin, gm, sweeps=400):
    Vr = 0.0
    for _ in range(sweeps):
        Vr = sum(x if x >= kmin else float(gm) * Vr for x in offers) / 5
    return Vr


def best_fixed(gm):
    Vr = 0.0
    for _ in range(400):
        Vr = sum(max(x, float(gm) * Vr) for x in offers) / 5
    return Vr


v45, v345 = rule_fixed(4, gw), rule_fixed(3, gw)
key(iid, v45, part=0, nd=4)
wrong(iid, 'no-disc', rule_fixed(4, 1, 4000), part=0)
wrong(iid, 'kept-only', F(9, 5), part=0)
wrong(iid, 'any', F(15, 5), part=0)
key(iid, float(gw) * v45, part=1, nd=4)
wrong(iid, 'same', v45, part=1)
keep = [x for x in offers if x > float(gw) * v45]
ex._rec(keep == [3, 4, 5] and correct_id(iid, 2) == ['take3'], 'e-take-or-wait part 3: improvement keeps 3, 4 and 5', str(keep))
key(iid, v345, part=3, nd=4)
wrong(iid, 'no-disc', rule_fixed(3, 1, 4000), part=3)
wrong(iid, 'old', v45, part=3)
wrong(iid, 'kept-only', F(12, 5), part=3)
ex._rec(abs(best_fixed(gw) - v345) < 1e-9, 'e-take-or-wait: the best rule is worth exactly the take-3 value', '')
say(iid, 'feedback.correct', F(9, 5), part=0)
say(iid, 'feedback.correct', F(3, 5), part=0)
say(iid, 'feedback.correct', 0.55, part=0)
say(iid, 'feedback.correct', r4(v45), part=0)
say(iid, 'feedback.byKey.no-disc', 0.6, part=0)
say(iid, 'feedback.byKey.no-disc', r4(rule_fixed(4, 1, 4000)), part=0)
say(iid, 'feedback.byKey.kept-only', F(3, 5), part=0)
for v in (gw, v45, gw * F(v45).limit_denominator(1000)):
    say(iid, 'feedback.correct', r4(v), part=1)
say(iid, 'feedback.byKey.same', gw, part=1)
say(iid, 'question', r4(float(gw) * v45), part=2)
say(iid, 'widget.options', r4(float(gw) * v45), part=2)
say(iid, 'widget.options', r4(v45), part=2)
say(iid, 'feedback.correct', F(12, 5), part=3)
say(iid, 'feedback.correct', F(2, 5), part=3)
say(iid, 'feedback.correct', 0.7, part=3)
say(iid, 'feedback.correct', r4(v45), part=3)
say(iid, 'feedback.byKey.no-disc', 0.4, part=3)
say(iid, 'feedback.byKey.no-disc', r4(rule_fixed(3, 1, 4000)), part=3)
say(iid, 'explain.text', r4(float(gw) * v345))
say(iid, 'explain.text', r4(v345))
given(iid, 'prose', 0.75)
say(iid, 'feedback.byKey.same', 0.75, part=1)

# e-chain-td-mc: a second implementation, list-indexed
iid = 'e-chain-td-mc'
Vt, Vm = [F(0)] * 3, [F(0)] * 3
rew = [0, 1, 2]
hist = []
for _ in range(2):
    for i in range(3):
        nxt = Vt[i + 1] if i < 2 else 0
        Vt[i] = Vt[i] + F(1, 2) * (rew[i] + nxt - Vt[i])
    for i in range(3):
        Vm[i] = Vm[i] + F(1, 2) * (sum(rew[i:]) - Vm[i])
    hist.append((list(Vt), list(Vm)))
key(iid, hist[0][0][1], part=0)
wrong(iid, 'full', 1, part=0)
wrong(iid, 'return', hist[0][1][1], part=0)
key(iid, hist[0][0][0], part=1)
wrong(iid, 'late', F(1, 2) * hist[0][0][1], part=1)
wrong(iid, 'mc', hist[0][1][0], part=1)
key(iid, hist[0][1][0], part=2)
wrong(iid, 'full', sum(rew), part=2)
wrong(iid, 'td', hist[0][0][0], part=2)
key(iid, hist[1][0][0], part=3)
wrong(iid, 'mc', hist[1][1][0], part=3)
wrong(iid, 'new-b', F(1, 2) * hist[1][0][1], part=3)
say(iid, 'feedback.correct', 0.5, part=0)
say(iid, 'feedback.byKey.return', 3, part=0)
say(iid, 'feedback.byKey.late', hist[0][0][1], part=1)
say(iid, 'feedback.correct', hist[0][1][0], part=2)
say(iid, 'feedback.byKey.full', 0.5, part=2)
say(iid, 'feedback.byKey.td', 3, part=2)
say(iid, 'feedback.correct', hist[0][0][1], part=3)
say(iid, 'feedback.correct', hist[1][0][0], part=3)
say(iid, 'feedback.byKey.mc', hist[0][1][0], part=3)
say(iid, 'feedback.byKey.mc', 0.5, part=3)
say(iid, 'feedback.byKey.new-b', hist[1][0][1], part=3)
for v in (hist[1][0][0], 3, hist[0][1][0], hist[1][1][0]):
    say(iid, 'explain.text', v)
given(iid, 'prose', 0.5)

# e-two-dial-step: tanh route for the logistic
iid = 'e-two-dial-step'
lg = lambda x: (1 + math.tanh(x / 2)) / 2  # noqa: E731
p = lg(0.4)
key(iid, p, part=0, nd=4)
wrong(iid, 'dial', 0.4, part=0)
wrong(iid, 'left', 1 - p, part=0)
acts, rew = 'RLR', [-1, -1, 4]
rtg = [sum(rew[t:]) for t in range(3)]
key(iid, rtg[1], part=1)
wrong(iid, 'whole', sum(rew), part=1)
wrong(iid, 'after', sum(rew[2:]), part=1)
ent = [(1 - p) if x == 'R' else -p for x in acts]
est = sum(gv * e for gv, e in zip(rtg, ent))
key(iid, est, part=2, nd=4)
wrong(iid, 'whole', sum(rew) * sum(ent), part=2)
wrong(iid, 'right-only', sum(gv * e for gv, e, x in zip(rtg, ent, acts) if x == 'R'), part=2)
thR, thL = 0.4 + 0.1 * est, 0 - 0.1 * est
newp = math.exp(thR) / (math.exp(thR) + math.exp(thL))
key(iid, newp, part=3, nd=4)
wrong(iid, 'one-dial', math.exp(thR) / (math.exp(thR) + 1), part=3)
wrong(iid, 'same', p, part=3)
for v in (1 - p, -p):
    say(iid, 'feedback.correct', round(v, 5), part=2)
    say(iid, 'explain.text', r4(v))
say(iid, 'feedback.correct', r4(est), part=2)
say(iid, 'explain.text', r4(est))
say(iid, 'feedback.correct', r4(p), part=0)
say(iid, 'feedback.correct', -0.4, part=0)
say(iid, 'feedback.correct', rtg[1], part=1)
say(iid, 'feedback.byKey.whole', sum(rew), part=2)
for v in (0.1, est, 0.2 * est, thR - thL, newp):
    say(iid, 'feedback.correct', r4(v), part=3)
say(iid, 'explain.text', r4(0.2 * est))
say(iid, 'explain.text', r4(newp))
say(iid, 'feedback.byKey.whole', rtg[0], part=2)
for v in rtg:
    say(iid, 'explain.text', v)
say(iid, 'question', 0.1, part=3)
given(iid, 'prose', 0.4)
say(iid, 'feedback.byKey.after', rew[1], part=1)

# e-mcts-two-sides: back-up by replaying the rule on a path list
iid = 'e-mcts-two-sides'
path = [{'mover': 'X', 'w': F(5), 'n': 8}, {'mover': 'O', 'w': F(2), 'n': 4}, {'mover': 'X', 'w': F(0), 'n': 0}]
for nd_ in path:
    nd_['n'] += 1
    nd_['w'] += 1 if nd_['mover'] == 'O' else 0
Bv, Av = path[1]['w'] / path[1]['n'], path[0]['w'] / path[0]['n']
key(iid, Bv, part=0, nd=2)
wrong(iid, 'same-side', F(2, 5), part=0)
wrong(iid, 'nocount', F(3, 4), part=0)
wrong(iid, 'draw', F(5, 2) / 5, part=0)
key(iid, Av, part=1, nd=4)
wrong(iid, 'credit', F(6, 9), part=1)
wrong(iid, 'nocount', F(5, 8), part=1)
uctB = float(Bv) + math.sqrt(2 * math.log(path[0]['n']) / path[1]['n'])
key(iid, uctB, part=2, nd=4)
wrong(iid, 'nob', Bv, part=2)
wrong(iid, 'old-n', float(Bv) + math.sqrt(2 * math.log(8) / 5), part=2)
say(iid, 'feedback.correct', Bv, part=0)
say(iid, 'feedback.correct', r4(F(5, 9)), part=1)
say(iid, 'feedback.correct', r4(uctB - float(Bv)), part=2)
say(iid, 'feedback.correct', r4(uctB), part=2)
say(iid, 'feedback.correct', 0.6, part=2)
given(iid, 'prose', 5, 8, 2, 4)
say(iid, 'feedback.byKey.nocount', 5, part=0)
say(iid, 'feedback.byKey.nocount', 9, part=1)

# e-sell-low-or-wait: synchronous sweeps with Fractions, then a long run for V*
iid = 'e-sell-low-or-wait'
gm = F(9, 10)
Lv, Hv = F(0), F(0)
tab = []
for _ in range(2):
    Lv, Hv = max(F(1), gm * (Lv / 2 + Hv / 2)), max(F(3), gm * Hv)
    tab.append((Lv, Hv))
key(iid, tab[1][0], part=0)
wrong(iid, 'one-sweep', tab[0][0], part=0)
wrong(iid, 'no-disc', tab[0][0] / 2 + tab[0][1] / 2, part=0)
Lf, Hf = 0.0, 0.0
for _ in range(2000):
    Lf, Hf = max(1.0, 0.9 * (Lf / 2 + Hf / 2)), max(3.0, 0.9 * Hf)
key(iid, Lf, part=1, nd=4)
wrong(iid, 'sell', 1, part=1)
wrong(iid, 'no-disc', 3, part=1)
wrong(iid, 'sweep2', tab[1][0], part=1)
say(iid, 'feedback.correct', 1.5, part=1)
say(iid, 'feedback.correct', 0.55, part=1)
say(iid, 'feedback.correct', 1.35, part=1)
say(iid, 'feedback.correct', r4(Lf), part=1)
for v in (0.9, 0.5, 1, 3, 1.8):
    say(iid, 'feedback.correct', v, part=0)
say(iid, 'feedback.byKey.no-disc', 0.9, part=0)
say(iid, 'feedback.byKey.no-disc', 1.8, part=0)
say(iid, 'feedback.byKey.no-disc', 0.5, part=1)
say(iid, 'feedback.byKey.no-disc', 1.5, part=1)
say(iid, 'explain.text', 0.45)
say(iid, 'explain.text', 1.35)
say(iid, 'explain.text', r4(Lf))
say(iid, 'explain.text', round(Lf - float(tab[1][0]), 2))
given(iid, 'prose', 0.5, 0.9)

# ------------------------------------------------------------------ difficulty 5
# e-take-one-three-four: game search by memoised recursion (route B)
iid = 'e-take-one-three-four'
from functools import lru_cache  # noqa: E402


@lru_cache(maxsize=None)
def wins(nn):
    return any(not wins(nn - kk) for kk in (1, 3, 4) if kk <= nn)


lose = [m for m in range(1, 11) if not wins(m)]
key(iid, len(lose), part=0)
ex._rec(lose == [2, 7, 9], f'e-take-one-three-four: losing piles 1 to 10 are {lose}', '')
ex._rec(all((not wins(m)) == (m % 7 in (0, 2)) for m in range(0, 200)), 'e-take-one-three-four: losing piles are those with remainder 0 or 2 mod 7, to 200', '')
wrong(iid, 'mult4', len([m for m in range(1, 11) if m % 4 == 0]), part=0)
wrong(iid, 'with-zero', len(lose) + 1, part=0)
tk = [kk for kk in (1, 3, 4) if not wins(12 - kk)]
key(iid, tk[0], part=1)
ex._rec(tk == [3], 'e-take-one-three-four: from 12 only a take of 3 leaves a losing pile', str(tk))
wrong(iid, 'four', 4, part=1)
wrong(iid, 'one', 1, part=1)
ex._rec(wins(8) and not wins(7) and wins(11), 'e-take-one-three-four: 8 and 11 win by moving to 7', '')
Q = {}
Q[(4, 4)] = 0 + F(1, 2) * (1 - 0)
best4 = max(Q.get((4, kk), F(0)) for kk in (1, 3, 4))
Q[(8, 4)] = 0 + F(1, 2) * (-best4 - 0)
key(iid, Q[(8, 4)], part=2)
wrong(iid, 'sign', -Q[(8, 4)], part=2)
wrong(iid, 'target', -best4, part=2)
say(iid, 'question', 0.5, part=2)
say(iid, 'feedback.correct', -best4, part=2)
say(iid, 'feedback.correct', 0.5, part=2)
say(iid, 'feedback.correct', Q[(8, 4)], part=2)
say(iid, 'feedback.byKey.sign', 0.5, part=2)
say(iid, 'question', 500, part=3)
ex.literal('50%', why='a self-play win rate against its own copy, the stated premise of part 4, not a computed figure')

# ------------------------------------------------------------------ code items, run in CPython


class TO(Exception):
    pass


def _alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, _alarm)


def close(a, e):
    if isinstance(a, dict) or isinstance(e, dict):
        return isinstance(a, dict) and isinstance(e, dict) and a.keys() == e.keys() and all(close(a[k], e[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return isinstance(e, (list, tuple)) and len(a) == len(e) and all(close(x, y) for x, y in zip(a, e))
    if isinstance(a, (str, bool)) or isinstance(e, (str, bool)) or a is None or e is None:
        return a == e
    return math.isclose(float(a), float(e), rel_tol=1e-9, abs_tol=1e-12)


TIMES = {}


def run_cases(src, tests, tag=None):
    out = []
    for k, t in enumerate(tests):
        ns_ = {}
        signal.setitimer(signal.ITIMER_REAL, 5.0)
        try:
            exec(src, ns_)
            if t.get('setup'):
                exec(t['setup'], ns_)
            t0 = time.perf_counter()
            got = eval(t['call'], ns_)
            if tag:
                TIMES[(tag, k + 1)] = time.perf_counter() - t0
            want = eval(t['expect'])
            res = 'ok' if (close(got, want) if t['compare'] == 'isclose' else got == want) else 'fail'
        except TO:
            res = 'timeout'
        except Exception:
            res = 'error'
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
        out.append(res)
    return out


def code_checks(iid):
    w = node(W(iid))
    sol = run_cases(w['solution'], w['tests'], tag=iid)
    ex._rec(all(r == 'ok' for r in sol), f'{iid}: solution passes all {len(sol)} hidden tests', str(sol))
    sol_ex = run_cases(w['solution'], w['examples'])
    ex._rec(all(r == 'ok' for r in sol_ex), f'{iid}: solution passes the examples', str(sol_ex))
    st = run_cases(w['starter'], w['tests'])
    ex._rec(all(r != 'ok' for r in st), f'{iid}: starter fails all {len(st)} hidden tests', str(st))
    ex._rec(f'runs {len(w["tests"])} hidden tests' in w['how'], f'{iid}: how names {len(w["tests"])} tests', '')
    ex._rec(len(w['mutants']) >= 2, f'{iid}: at least two mutants', '')
    for m in w['mutants']:
        res = run_cases(m['source'], w['tests'])
        first = next((k + 1 for k, r in enumerate(res) if r != 'ok'), None)
        ex._rec(first == m['test'], f'{iid}: mutant first fails test {m["test"]} ({m["symptom"][:50]})', str(res))
    fbk = node(P(iid) + '.feedback').get('byKey', {})
    for kk in fbk:
        n_ = int(kk.split('-')[1])
        ex._rec(1 <= n_ <= len(w['tests']), f'{iid}: byKey {kk} names a real test', '')
    return w


# e-router-two-states: route B is an independent implementation with its own sampling code
iid = 'e-router-two-states'
wr = code_checks(iid)


def router_b(R, steps, lr, beta, seed):
    rng = random.Random(seed)
    k = len(R[0])
    th = np.zeros((2, k))
    base = np.zeros(2)
    for _ in range(steps):
        s = int(rng.random() < 0.5)
        z = th[s] - th[s].max()
        pr = np.exp(z) / np.exp(z).sum()
        u = rng.random()
        cum = np.cumsum(pr)
        a = int(np.searchsorted(cum, u, side='right'))
        a = min(a, k - 1)
        r = R[s][a]
        onehot = np.eye(k)[a]
        th[s] = th[s] + lr * (r - base[s]) * (onehot - pr)
        base[s] = base[s] + beta * (r - base[s])
    out = []
    for s in (0, 1):
        z = th[s] - th[s].max()
        out.append((np.exp(z) / np.exp(z).sum()).tolist())
    return out


nsb = {'train_router': router_b}
for k, t in enumerate(wr['tests'][:5]):
    got = eval(t['call'], nsb)
    ex._rec(close(got, eval(t['expect'])), f'{iid}: route B gives test {k + 1}\'s expected value', '')
seed0 = random.Random(1).random()
ex._rec(seed0 < 0.5, 'e-router-two-states: seed 1\'s first step is busy, so test 4 reads the unvisited calm state', f'{seed0}')
for cs in ('train_router([[1, 2, 0], [0, 1, 3]], 2000, 0.1, 0.1, 5)[1][2]', 'train_router([[2, 0, 1], [0, 3, 1]], 2000, 0.1, 0.1, 6)[1][1]'):
    ex._rec(eval(cs, nsb) > 0.9, f'{iid}: route B {cs[13:60]} above 0.9', '')
say(iid, 'widget.how', 0.9)
say(iid, 'widget.how', 2000)

# e-q-learning-exit: route B with index arrays and its own value iteration
iid = 'e-q-learning-exit'
wq = code_checks(iid)
rows, cols = 3, 5
walls = {(2, 2), (2, 4)}
ends = {(1, 5): 1.0, (3, 5): -1.0}
cells = [(r_, c_) for r_ in range(1, rows + 1) for c_ in range(1, cols + 1) if (r_, c_) not in walls]
opens = [c_ for c_ in cells if c_ not in ends]
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]          # U, R, D, L


def mv(c_, d):
    t = (c_[0] + dirs[d][0], c_[1] + dirs[d][1])
    return t if 1 <= t[0] <= rows and 1 <= t[1] <= cols and t not in walls else c_


def rw_(t):
    return ends.get(t, 0.0) - 0.05


V_ = {c_: 0.0 for c_ in cells}
for _ in range(500):
    V_ = {c_: 0.0 if c_ in ends else max(rw_(mv(c_, d)) + 0.9 * V_[mv(c_, d)] for d in range(4)) for c_ in cells}
name = lambda c_: f'r{c_[0]}c{c_[1]}'  # noqa: E731
sets_b = {name(c_): {'URDL'[d] for d in range(4) if rw_(mv(c_, d)) + 0.9 * V_[mv(c_, d)] > max(rw_(mv(c_, e)) + 0.9 * V_[mv(c_, e)] for e in range(4)) - 1e-9} for c_ in opens}
nsq = {}
exec(wq['solution'], nsq)
ex._rec(nsq['optimal_sets']() == sets_b, 'e-q-learning-exit: the starter\'s optimal_sets equals route B value iteration', '')
ex._rec(sets_b['r3c1'] == {'U', 'R'} and sum(len(v) > 1 for v in sets_b.values()) == 1, 'e-q-learning-exit: r3c1 is the one tied cell, U and R', '')
setup6 = wq['tests'][5]['setup']
ex._rec(eval(setup6.split('=', 1)[1].strip()) == {k: sorted(v) for k, v in sets_b.items()}, 'e-q-learning-exit: test 6 sets are the optimal sets', '')


def q_b(episodes, seed, alpha=0.2, eps=0.2, q0=0.0, gamma=0.9):
    rng = random.Random(seed)
    Qa = np.full((len(cells), 4), q0)
    ix = {c_: i for i, c_ in enumerate(cells)}
    for _ in range(episodes):
        s = rng.choice(opens)
        while s not in ends:
            if rng.random() < eps:
                d = 'URDL'.index(rng.choice('URDL'))
            else:
                d = int(np.argmax(Qa[ix[s]]))      # argmax takes the first of equal values: U, R, D, L
            t = mv(s, d)
            target = rw_(t) if t in ends else rw_(t) + gamma * Qa[ix[t]].max()
            Qa[ix[s], d] += alpha * (target - Qa[ix[s], d])
            s = t
    return {(name(c_), 'URDL'[d]): float(Qa[ix[c_], d]) for c_ in cells for d in range(4)}


for k, call in ((2, 'sum(q_learn(5, 0).values())'), (3, 'sum(q_learn(5, 1, q0=0.5).values())')):
    got = eval(call.replace('q_learn', 'q_b'), {'q_b': q_b})
    ex._rec(math.isclose(got, eval(wq['tests'][k - 1]['expect']), rel_tol=1e-9), f'{iid}: route B gives test {k}\'s seeded sum', f'{got}')
okb = all(all(max('URDL', key=lambda b: Qb[(c_, b)]) in sets_b[c_] for c_ in sets_b) for Qb in (q_b(300, s) for s in range(5)))
ex._rec(okb, 'e-q-learning-exit: route B greedy policy is optimal for seeds 0 to 4 after 300 episodes', '')
ex._rec(abs(V_[(3, 1)] - 0.3562) < 5e-5, f'e-q-learning-exit: V*(r3c1) = {V_[(3, 1)]:.6f} rounds to 0.3562', '')
hit20 = sum(all(max('URDL', key=lambda b: Qb[(c_, b)]) in sets_b[c_] for c_ in sets_b) for Qb in (q_b(300, s) for s in range(20)))
ex._rec(hit20 == 20, f'e-q-learning-exit: seeds 0 to 19 all optimal after 300 episodes ({hit20})', '')
given(iid, 'prose', 0.05, 0.9)
say(iid, 'question', 0.2)
say(iid, 'question', 0.0)
say(iid, 'widget.how', 0.5)
say(iid, 'widget.how', 300)

for (tag, k), sec in sorted(TIMES.items()):
    print(f'time {tag} test {k}: {sec * 1000:.1f} ms in CPython')
ex._rec(max(TIMES.values()) < 0.5, f'every graded case under 0.5 s in CPython (max {max(TIMES.values()) * 1000:.0f} ms)', '')

# ------------------------------------------------------------------ structure
ramp = {d: sum(it['difficulty'] == d for it in items) for d in (2, 3, 4, 5)}
ex._rec(ramp == {2: 6, 3: 15, 4: 6, 5: 3} and len(items) == 30, f'ramp 6, 15, 6, 3 of 30: {ramp}', '')
cover = {s: sum(s in it['skills'] for it in items) for s in doc['skills']}
ex._rec(all(v >= 5 for v in cover.values()), f'every skill on 5 or more items: {cover}', '')
pace = sum(it['pace'] for it in items)
ex._rec(pace <= doc['minutes'] * 60, f'paces add to {pace} s, within {doc["minutes"]} minutes', '')

allw = set()
for it in items:
    for kk, host in ([(None, it)] if 'widget' in it else list(enumerate(it.get('parts', [])))):
        for x in host['widget'].get('wrong', []):
            allw.add((it['id'], kk, x['id']))
ex._rec(allw <= CHECKED, f'every one of the {len(allw)} numeric slips is recomputed', str(sorted(allw - CHECKED)))

ex.check_wrongs()
ex.report()
