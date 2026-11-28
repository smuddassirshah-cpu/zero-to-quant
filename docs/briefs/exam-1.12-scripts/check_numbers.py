"""Recompute every number stated in app/content/exams/topic-1.12.json by a second route and assert it at its path.

Route A is build.py (floats and closed forms). Route B here is independent: exact Fractions for every sum, count and
chance, logs taken through a different identity, an independent bigram count (index arrays and np.add.at), the shipped
autograd.py for the two code items' gradients and losses, and both code items run in CPython as the page runs them (one
namespace, prelude, then the code, then each case's setup and call in order, judged by the engine's own __zq_judge read
from code.js): the solution passes every hidden test and example, the starter fails every test, and each mutant first
fails its named test. Coverage runs strict: every number on screen is compared or marked literal with a reason.
Run through the CI runner: node tools/run-number-scripts.mjs --python <venv> --only exam-1.12
"""
import json
import math
import os
import re
import signal
import sys
import time
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', '..', 'app')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, _walk, ZQ_LIB  # noqa: E402

EXAM = os.path.join(APP, 'content', 'exams', 'topic-1.12.json')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, DATA)
import autograd as AG  # noqa: E402  the shipped module, read only


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


def given(iid, path, *vals, part=None):
    """Inputs stated in the item: each must appear in its text (they are then used below)."""
    for v in vals:
        say(iid, path, v, part=part)


def correct_id(iid, part=None):
    return [o['id'] for o in node(W(iid, part))['options'] if o.get('correct')]


def lg2(x):
    """log base 2 by a second identity: log2 = log10 / log10(2)."""
    return math.log10(float(x)) / math.log10(2)


def ln(x):
    return math.log1p(float(x) - 1)


LN2 = ln(2)


def Hb(p):
    return -sum(float(x) * lg2(x) for x in p if x > 0)


# ------------------------------------------------------------------ difficulty 2
iid = 'e-tail-move-bits'
p = F(125, 10000)
given(iid, 'prose', 0.0125)
key(iid, lg2(1 / p), nd=4)
wrong(iid, 'nats', -ln(p))
wrong(iid, 'log10', -math.log10(float(p)))
wrong(iid, 'reciprocal', 1 / p)
ex._rec(1 / p == 80, 'e-tail-move-bits: 1/0.0125 = 80', '')
say(iid, 'feedback.correct', 80)
say(iid, 'feedback.correct', round(lg2(80), 2))
say(iid, 'explain.text', 80)
say(iid, 'explain.text', 64)
say(iid, 'explain.text', round(lg2(80), 2))
ex._rec(lg2(64) == 6.0, 'e-tail-move-bits: a 1 in 64 event carries 6 bits', '')

iid = 'e-ticker-pairs'
given(iid, 'prose', 400, 1530)
key(iid, 1530 + 400)
wrong(iid, 'no-end', 1530)
wrong(iid, 'marks-twice', 1530 + 2 * 400)
wrong(iid, 'inside-only', 1530 - 400)
say(iid, 'feedback.correct', 1930)
say(iid, 'explain.text', 1930)
ex._rec(len('.ibm.') - 1 == 4 and len('ibm') == 3, 'e-ticker-pairs: .ibm. gives 4 pairs from 3 letters', '')

iid = 'e-slippage-grad'
q, pf, mid = 400, F(5030, 100), F(5025, 100)
given(iid, 'prose', 400, 50.30, 50.25)
ex._rec(q * (pf - mid) == 20, 'e-slippage-grad: C = 20', '')
say(iid, 'prose', 20)
key(iid, q * -1)
wrong(iid, 'sign', q)
wrong(iid, 'other-input', pf - mid)
wrong(iid, 'value', q * (pf - mid))
say(iid, 'feedback.correct', 400)
say(iid, 'feedback.byKey.value', 20)
say(iid, 'explain.text', 400)

iid = 'e-perplexity-sixteen'
given(iid, 'prose', 16)
key(iid, 4 * LN2, nd=4)
wrong(iid, 'bits', lg2(16))
wrong(iid, 'log10', math.log10(16))
wrong(iid, 'inverse', F(1, 16))
say(iid, 'feedback.correct', round(4 * LN2, 4))
say(iid, 'explain.text', round(4 * LN2, 4))

iid = 'e-count-six-ten-three'
layers = [(6, 10), (10, 3)]
key(iid, sum((a + 1) * b for a, b in layers))
wrong(iid, 'edges', sum(a * b for a, b in layers))
wrong(iid, 'one-bias', sum(a * b for a, b in layers) + 1)
wrong(iid, 'hidden-only', 7 * 10)
say(iid, 'feedback.correct', 7)
for v in (70, 33, 103):
    say(iid, 'feedback.correct', v)
    say(iid, 'explain.text', v)
ex._rec(10 + 3 == 13, 'e-count-six-ten-three: 13 neurons carry a bias', '')
say(iid, 'feedback.byKey.edges', 13)

iid = 'e-draw-on-a-total'
row = [F(25, 100), F(35, 100), F(15, 100), F(25, 100)]
given(iid, 'prose', 0.25, 0.35, 0.15, 0.6)
tot = [sum(row[:k + 1]) for k in range(4)]
u = F(6, 10)
pick = next(k for k, t in enumerate(tot) if t > u)
ex._rec(pick == 2 and correct_id(iid) == ['x'], 'e-draw-on-a-total: first total strictly above 0.6 is x', str(tot))
ex._rec(0.25 + 0.35 == 0.6 and int(np.searchsorted(np.cumsum([0.25, 0.35, 0.15, 0.25]), 0.6, side='right')) == 2,
        'e-draw-on-a-total: in floats too, searchsorted right on 0.6 gives x', '')
for t in tot:
    say(iid, 'explain.text', t)
say(iid, 'feedback.correct', tot[2])
say(iid, 'widget.options', tot[2])

# ------------------------------------------------------------------ difficulty 3
iid = 'e-order-kinds-entropy'
p7 = [F(1, 2), F(1, 4), F(1, 8), F(1, 16), F(1, 16)]
Hx = sum(x * (x.denominator.bit_length() - 1) for x in p7)   # -log2 of a power of 1/2, exactly
ex._rec(Hx == F(15, 8), 'e-order-kinds-entropy: H = 15/8 exactly', '')
key(iid, Hx, nd=4)
wrong(iid, 'equal', lg2(5))
wrong(iid, 'nats', float(Hx) * LN2)
wrong(iid, 'sum', 1 + 2 + 3 + 4 + 4)
wrong(iid, 'mean', F(14, 5))
for v in (0.5, 0.375, 0.25, 1.875):
    say(iid, 'feedback.correct', v)
    say(iid, 'explain.text', v)
say(iid, 'explain.text', round(lg2(5), 3))

iid = 'e-huffman-five-types'
p8 = [F(40, 100), F(25, 100), F(20, 100), F(10, 100), F(5, 100)]
given(iid, 'prose', 0.4, 0.25, 0.2, 0.1, 0.05, 0.15, 0.35, 0.6)
# route B: run Huffman's merges and read each depth
import heapq  # noqa: E402
heap = [(pp, k, (k,)) for k, pp in enumerate(p8)]
heapq.heapify(heap)
depth = [0] * 5
merges = []
cnt = 5
while len(heap) > 1:
    a = heapq.heappop(heap)
    b = heapq.heappop(heap)
    for s in a[2] + b[2]:
        depth[s] += 1
    merges.append((a[0], b[0]))
    heapq.heappush(heap, (a[0] + b[0], cnt, a[2] + b[2]))
    cnt += 1
ex._rec(merges == [(F(5, 100), F(10, 100)), (F(15, 100), F(20, 100)), (F(25, 100), F(35, 100)), (F(40, 100), F(60, 100))],
        'e-huffman-five-types: the stated merges are Huffman\'s, with no ties', str(merges))
ex._rec(depth == [1, 2, 3, 4, 4], f'e-huffman-five-types: depths {depth}', '')
avg = sum(pp * d for pp, d in zip(p8, depth))
key(iid, avg, nd=4)
wrong(iid, 'entropy', Hb(p8))
wrong(iid, 'fixed', math.ceil(lg2(5)))
wrong(iid, 'unweighted', F(sum(depth), 5))
for v in (0.4, 0.5, 0.6, 0.2, 2.1):
    say(iid, 'feedback.correct', v)
say(iid, 'explain.text', 2.1)
say(iid, 'explain.text', round(Hb(p8), 2))
say(iid, 'explain.text', p8[3] + p8[4])

iid = 'e-zlib-on-ticks'
given(iid, 'prose', 600000, 3.2, 260000)
z = F(260000 * 8, 600000)
key(iid, z, nd=4)
wrong(iid, 'bytes', F(260000, 600000))
wrong(iid, 'inverse', 1 / z)
wrong(iid, 'model', F(32, 10))
say(iid, 'feedback.correct', 260000 * 8)
say(iid, 'feedback.correct', round(float(z), 2))
say(iid, 'explain.text', 260000 * 8)
say(iid, 'explain.text', round(float(z), 2))
say(iid, 'explain.text', 600000 * F(32, 10) / 8)
ex._rec(600000 * F(32, 10) / 8 < 260000, 'e-zlib-on-ticks: the model\'s code (240,000 bytes) is the shorter', '')

iid = 'e-fixed-forecast-gap'
cnts = [20, 30, 50]
ph = [F(c, 100) for c in cnts]
qq = [F(2, 10), F(4, 10), F(4, 10)]
given(iid, 'prose', 100, 20, 30, 50, 0.2, 0.4)
gap = sum(float(a) * ln(a / b) for a, b in zip(ph, qq))
key(iid, gap, nd=6)
wrong(iid, 'bits', gap / LN2)
wrong(iid, 'reverse', sum(float(b) * ln(b / a) for a, b in zip(ph, qq)))
wrong(iid, 'total', 100 * gap)
wrong(iid, 'floor', -sum(float(a) * ln(a) for a in ph))
# the decomposition: average NLL under q = H(p-hat) + D(p-hat || q), in nats
avg_nll = -sum(float(a) * ln(b) for a, b in zip(ph, qq))
ex._rec(abs(avg_nll - (-sum(float(a) * ln(a) for a in ph)) - gap) < 1e-12, 'e-fixed-forecast-gap: average NLL = H + D', '')
for v in (0.2, 0.3, 0.5, 0.4, 1.25, 0.75):
    say(iid, 'feedback.correct', v)
say(iid, 'feedback.correct', round(gap, 4))
say(iid, 'explain.text', round(gap, 4))
say(iid, 'explain.text', 0.2)

iid = 'e-flag-table-mi'
J = [[F(3, 10), F(1, 10)], [F(2, 10), F(4, 10)]]
given(iid, 'prose', 0.3, 0.1, 0.2, 0.4)
px = [sum(rw) for rw in J]
py = [sum(c) for c in zip(*J)]
ratios = [J[i][j] / (px[i] * py[j]) for i in range(2) for j in range(2)]
ex._rec(ratios == [F(3, 2), F(1, 2), F(2, 3), F(4, 3)], 'e-flag-table-mi: the four ratios', str(ratios))
I = sum(float(J[i][j]) * lg2(J[i][j] / (px[i] * py[j])) for i in range(2) for j in range(2))
I_b = Hb(px) + Hb(py) - Hb([v for rw in J for v in rw])
ex._rec(abs(I - I_b) < 1e-12, 'e-flag-table-mi: KL route equals H(X) + H(Y) - H(X, Y)', '')
key(iid, I, nd=5)
wrong(iid, 'cond', Hb(py) - I)
wrong(iid, 'nats', I * LN2)
wrong(iid, 'joint', Hb([v for rw in J for v in rw]))
for v in px + py:
    say(iid, 'feedback.correct', v)
say(iid, 'feedback.correct', round(I, 3))
for v in (1.5, 0.5):
    say(iid, 'explain.text', v)
say(iid, 'explain.text', round(I, 3))
ex.literal('\\tfrac23', why='a ratio of a cell to its product, checked exactly as Fraction(2, 3) in the ratios claim above')
ex.literal('\\tfrac43', why='a ratio of a cell to its product, checked exactly as Fraction(4, 3) in the ratios claim above')
say(iid, 'feedback.byKey.cond', Hb(py))

iid = 'e-five-state-bias'
given(iid, 'prose', 5, 500, 0.015)
bias = F(4 * 2) / (2 * 500) / LN2
key(iid, 0.015 - float(bias), nd=6)
wrong(iid, 'no-ln2', F(15, 1000) - F(8, 1000))
wrong(iid, 'no-minus-one', 0.015 - 15 / (1000 * LN2))
wrong(iid, 'bias', float(bias))
wrong(iid, 'two-outcomes', 0.015 - 4 * 1 / (1000 * LN2))
say(iid, 'feedback.correct', round(float(bias), 4))
say(iid, 'feedback.correct', round(0.015 - float(bias), 4))
say(iid, 'explain.text', round(float(bias), 4))
say(iid, 'explain.text', round(0.015 - float(bias), 4))
say(iid, 'explain.text', 0.015)
say(iid, 'feedback.byKey.bias', 0.015)
for v in (8, 1000):
    say(iid, 'explain.text', v)
say(iid, 'feedback.correct', 1000)

iid = 'e-smooth-payoff-grad'
w_, x_ = 0.5, 2.0
given(iid, 'prose', 0.5, 2)
e1 = sum(F(1, math.factorial(k)) for k in range(30))       # e by its series
g = float(e1 / (1 + e1)) * x_
key(iid, g, nd=6)
wrong(iid, 'no-x', float(e1 / (1 + e1)))
wrong(iid, 'used-w', float(e1 / (1 + e1)) * w_)
wrong(iid, 'no-log', float(e1) * x_)
for v in (round(float(e1), 4), round(float(1 + e1), 4), round(g, 4)):
    say(iid, 'feedback.correct', v)
    say(iid, 'explain.text', v)
say(iid, 'feedback.byKey.no-x', 2)

iid = 'e-two-uses-of-x'
x_, y_ = -2, 3
given(iid, 'prose', -2, 3)
z_of = lambda xx: (xx * y_ + 1) * xx  # noqa: E731
d_exact = 2 * x_ * y_ + 1
ex._rec(abs((z_of(x_ + 1e-6) - z_of(x_ - 1e-6)) / 2e-6 - d_exact) < 1e-6, 'e-two-uses-of-x: a central difference agrees with -11', '')
key(iid, d_exact)
wrong(iid, 'direct', x_ * y_ + 1)
wrong(iid, 'through-p', x_ * y_)
wrong(iid, 'sign', -d_exact)
for v in (-5, -6, -11):
    say(iid, 'feedback.correct', v)
    say(iid, 'explain.text', v)
say(iid, 'explain.text', 2)

iid = 'e-no-seen-set'


class V:
    def __init__(self, data, prev=()):
        self.data, self.grad, self._prev, self._backward = data, 0.0, tuple(prev), lambda: None

    def __mul__(self, other):
        other = other if isinstance(other, V) else V(other)
        out = V(self.data * other.data, (self, other))

        def _bw():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _bw
        return out

    def backward(self, seen_set):
        topo, seen = [], set()

        def build(v):
            if seen_set and v in seen:
                return
            seen.add(v)
            for c in v._prev:
                build(c)
            topo.append(v)
        build(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()


for flag in (False, True):
    xv = V(2.0)
    ev = xv * 3
    yv = ev * ev
    yv.backward(seen_set=flag)
    if flag:
        true_g = xv.grad
    else:
        bug_g, bug_e = xv.grad, ev.grad
given(iid, 'prose', 2.0, 3)
key(iid, bug_g)
wrong(iid, 'true', true_g)
wrong(iid, 'e-grad', bug_e)
say(iid, 'feedback.correct', bug_e)
say(iid, 'feedback.correct', bug_e * 3)
say(iid, 'feedback.correct', bug_g)
say(iid, 'explain.text', bug_e * 3)
say(iid, 'explain.text', bug_g)
say(iid, 'explain.text', true_g)

iid = 'e-neuron-one-step'
w_, b_, x_, lr = 0.2, 0.2, 1.5, 0.1
given(iid, 'prose', 0.2, 1.5, 0.1)
n_ = w_ * x_ + b_
ex2 = math.exp(2 * n_)
o_ = (ex2 - 1) / (ex2 + 1)          # tanh by its exponential form
g_ = 2 * (o_ - 1) * (1 - o_ * o_) * x_
key(iid, w_ - lr * g_, nd=6)
wrong(iid, 'uphill', w_ + lr * g_)
wrong(iid, 'no-x', w_ - lr * g_ / x_)
wrong(iid, 'slope-of-n', w_ - lr * 2 * (o_ - 1) * (1 - n_ * n_) * x_)
wrong(iid, 'no-two', w_ - lr * g_ / 2)
say(iid, 'feedback.correct', round(o_, 4))
say(iid, 'feedback.correct', round(g_, 4))
say(iid, 'feedback.correct', round(w_ - lr * g_, 4))
say(iid, 'feedback.correct', n_)
say(iid, 'explain.text', n_)
say(iid, 'explain.text', round(o_, 4))
say(iid, 'explain.text', round(2 * (o_ - 1), 4))
say(iid, 'explain.text', round(1 - o_ * o_, 4))
say(iid, 'explain.text', round(g_, 4))
say(iid, 'explain.text', round(w_ - lr * g_, 4))
ex._rec(abs(-1.0758 * 0.7864 * 1.5 - round(g_, 4)) < 0.0001, 'e-neuron-one-step: the printed factors give -1.2691', '')
say(iid, 'feedback.byKey.no-x', 1.5)

iid = 'e-check-by-bumps'
up, dn, md, bp = F(693649, 10 ** 6), F(692149, 10 ** 6), F(692898, 10 ** 6), F(7503, 10 ** 4)
given(iid, 'prose', 0.7503, 0.001, 0.693649, 0.692149, 0.692898)
cd = (up - dn) / F(2, 1000)
fd = (up - md) / F(1, 1000)
ex._rec(cd == F(3, 4), 'e-check-by-bumps: central difference 0.75 exactly', '')
rel = abs(bp - cd) / max(bp, cd)
ex._rec(round(float(rel), 6) == 0.0004 or float(f'{float(rel):.2g}') == 0.0004, f'e-check-by-bumps: relative error {float(rel):.6g} is 0.00040 at 2 sf', '')
key(iid, float(f'{float(rel):.2g}'))
ex._rec(abs(node(W(iid))['answer'] - float(rel)) <= node(W(iid))['tol']['abs'], 'e-check-by-bumps: the band takes the unrounded error', '')
wrong(iid, 'absolute', abs(bp - cd))
wrong(iid, 'forward', abs(bp - fd) / max(bp, fd))
say(iid, 'feedback.correct', cd)
say(iid, 'feedback.correct', 0.002)
say(iid, 'feedback.correct', abs(bp - cd))
say(iid, 'feedback.correct', 0.0004)
say(iid, 'explain.text', 0.002)
say(iid, 'explain.text', cd)
say(iid, 'explain.text', 0.0004)
say(iid, 'feedback.byKey.absolute', 0.7503)

iid = 'e-input-gradient-entry'
Wm = [[F(1), F(-2)], [F(1, 2), F(3)], [F(-1), F(4)]]
Gm = [[F(2), F(1)], [F(-1), F(1, 2)]]
dX = [[sum(Gm[i][j] * Wm[k][j] for j in range(2)) for k in range(3)] for i in range(2)]
key(iid, dX[1][2])
wrong(iid, 'row-1', dX[0][2])
wrong(iid, 'w-row-1', dX[1][0])
wrong(iid, 'sign', -dX[1][2])
given(iid, 'prose', 0.5)
say(iid, 'feedback.correct', 0.5)
say(iid, 'feedback.correct', dX[1][2])
say(iid, 'explain.text', dX[1][2])

iid = 'e-dev-total-in-bits'
given(iid, 'prose', 50000, 3203, 22807)
nats = F(50000, 22807)
key(iid, float(nats) / LN2, nd=6)
wrong(iid, 'nats', nats)
wrong(iid, 'per-name', F(50000, 3203))
wrong(iid, 'no-ends', float(F(50000, 22807 - 3203)) / LN2)
wrong(iid, 'times-ln2', float(nats) * LN2)
for path in ('feedback.correct', 'explain.text'):
    say(iid, path, round(float(nats), 4))
    say(iid, path, round(float(nats) / LN2, 4))

iid = 'e-mlp-size-four'
given(iid, 'prose', 4, 27, 6, 80)
pieces = [27 * 6, (4 * 6) * 80, 80, 80 * 27, 27]
key(iid, sum(pieces))
wrong(iid, 'no-table', sum(pieces[1:]))
wrong(iid, 'one-symbol', 27 * 6 + 6 * 80 + 80 + 80 * 27 + 27)
wrong(iid, 'table-each', 4 * 27 * 6 + sum(pieces[1:]))
for v in pieces + [sum(pieces)]:
    say(iid, 'feedback.correct', v)
for v in (162, 24, 1920, 2160, 4349):
    say(iid, 'explain.text', v)
say(iid, 'feedback.byKey.no-table', 162)
say(iid, 'feedback.byKey.one-symbol', 24)

iid = 'e-epochs-at-48'
given(iid, 'prose', 182531, 30000, 48)
ep = F(30000 * 48, 182531)
key(iid, ep, nd=6)
wrong(iid, 'steps', round(F(182531, 48)))
wrong(iid, 'batch-32', F(30000 * 32, 182531))
wrong(iid, 'inverse', 1 / ep)
for path in ('feedback.correct', 'explain.text'):
    say(iid, path, round(float(ep), 2))
say(iid, 'feedback.correct', 30000 * 48)
say(iid, 'explain.text', round(F(182531, 48)))
say(iid, 'feedback.byKey.batch-32', 32)

# ------------------------------------------------------------------ difficulty 4
iid = 'e-pair-in-bits'
p22 = [F(45, 100), F(35, 100), F(20, 100)]
q22 = [F(1, 4), F(1, 2), F(1, 4)]
given(iid, 'prose', 0.45, 0.35, 0.2, 0.25, 0.5)
Hp = Hb(p22)
Hpq = sum(a * (b.denominator.bit_length() - 1) for a, b in zip(p22, q22))   # q's entries are powers of 1/2: exact
ex._rec(Hpq == F(165, 100), 'e-pair-in-bits: H(p, q) = 1.65 exactly', '')
Hq = sum(b * (b.denominator.bit_length() - 1) for b in q22)
Hqp = -sum(float(b) * lg2(a) for a, b in zip(p22, q22))
key(iid, Hp, part=0, nd=6)
wrong(iid, 'nats', Hp * LN2, part=0)
wrong(iid, 'model', Hq, part=0)
wrong(iid, 'equal', lg2(3), part=0)
say(iid, 'feedback.correct', round(Hp, 4), part=0)
for v in p22:
    say(iid, 'feedback.correct', v, part=0)
for v in (lg2(1 / p22[0]), lg2(1 / p22[1]), lg2(1 / p22[2])):
    say(iid, 'feedback.correct', round(v, 4), part=0)
key(iid, Hpq, part=1, nd=6)
wrong(iid, 'swapped', Hqp, part=1)
wrong(iid, 'nats', float(Hpq) * LN2, part=1)
say(iid, 'feedback.correct', Hpq, part=1)
for v in (0.45, 0.35, 0.2):
    say(iid, 'feedback.correct', v, part=1)
D = float(Hpq) - Hp
Dr = Hqp - float(Hq)
D_b = sum(float(a) * lg2(a / b) for a, b in zip(p22, q22))
Dr_b = sum(float(b) * lg2(b / a) for a, b in zip(p22, q22))
ex._rec(abs(D - D_b) < 1e-12 and abs(Dr - Dr_b) < 1e-12, 'e-pair-in-bits: both divergences by their own sums', '')
key(iid, D_b, part=2, nd=6)
wrong(iid, 'reverse', Dr_b, part=2)
wrong(iid, 'added', float(Hpq) + Hp, part=2)
wrong(iid, 'nats', D_b * LN2, part=2)
for v in (1.65, round(Hp, 4), round(D_b, 4)):
    say(iid, 'feedback.correct', v, part=2)
key(iid, Dr_b, part=3, nd=6)
wrong(iid, 'symmetric', D_b, part=3)
wrong(iid, 'nats', Dr_b * LN2, part=3)
say(iid, 'feedback.correct', round(Hqp, 4), part=3)
say(iid, 'feedback.correct', Hq, part=3)
say(iid, 'feedback.correct', round(Dr_b, 4), part=3)
for v in (round(Hp, 4), 1.65, round(D_b, 4), round(Dr_b, 4)):
    say(iid, 'explain.text', v)
ex._rec(abs(D_b - Dr_b) > 0.005, 'e-pair-in-bits: the two divergences differ at 4 places', '')

iid = 'e-volume-buckets'
rows23 = {'low': (60, 60), 'mid': (70, 50), 'high': (110, 50)}
given(iid, 'prose', 400, 60, 70, 50, 110)
n23 = sum(a + b for a, b in rows23.values())
up23 = sum(a for a, b in rows23.values())
ex._rec(n23 == 400 and up23 == 240, 'e-volume-buckets: 400 days, 240 up and 160 down', '')
say(iid, 'question', 240, part=0)
say(iid, 'question', 160, part=0)
HY = Hb([F(up23, n23), F(n23 - up23, n23)])
key(iid, HY, part=0, nd=6)
wrong(iid, 'fair', 1, part=0)
wrong(iid, 'nats', HY * LN2, part=0)
say(iid, 'feedback.correct', 0.6, part=0)
say(iid, 'feedback.correct', 0.4, part=0)
say(iid, 'feedback.correct', round(HY, 3), part=0)
say(iid, 'feedback.byKey.fair', 0.6, part=0)


def mi_rows(rws):
    tot = sum(a + b for a, b in rws)
    hy = Hb([F(sum(a for a, b in rws), tot), F(sum(b for a, b in rws), tot)])
    hyx = sum(F(a + b, tot) * Hb([F(a, a + b), F(b, a + b)]) for a, b in rws)
    return hy - float(hyx), float(hyx)


I3, HYX3 = mi_rows(list(rows23.values()))
key(iid, I3, part=1, nd=6)
wrong(iid, 'cond', HYX3, part=1)
wrong(iid, 'nats', I3 * LN2, part=1)
for v in (1, round(Hb([F(70, 120), F(50, 120)]), 4), round(Hb([F(110, 160), F(50, 160)]), 4), 0.3, 0.4,
          round(HY, 4), round(HYX3, 4), round(I3, 4)):
    say(iid, 'feedback.correct', v, part=1)
merged = [(130, 110), (110, 50)]
ex._rec(merged[0] == (60 + 70, 60 + 50), 'e-volume-buckets: low and mid merge to 130 up and 110 down', '')
given(iid, 'question', 130, 110, part=2)
Im, HYXm = mi_rows(merged)
key(iid, Im, part=2, nd=6)
wrong(iid, 'unchanged', I3, part=2)
wrong(iid, 'cond', HYXm, part=2)
for v in (round(Hb([F(130, 240), F(110, 240)]), 4), round(HYXm, 4), round(Im, 4)):
    say(iid, 'feedback.correct', v, part=2)
say(iid, 'feedback.byKey.unchanged', round(100 * F(70, 120)), part=2)
say(iid, 'feedback.byKey.unchanged', round(100 * F(50, 120)), part=2)
ex._rec(F(70, 120) > F(57, 100) and F(70, 120) < F(59, 100), 'e-volume-buckets: mid splits about 58:42', '')
b3 = 2 * 1 / (2 * 400 * LN2)
b2 = 1 * 1 / (2 * 400 * LN2)
lead = (I3 - b3) - (Im - b2)
key(iid, lead, part=3, nd=6)
wrong(iid, 'plug-in', I3 - Im, part=3)
wrong(iid, 'no-ln2', (I3 - 2 / 800) - (Im - 1 / 800), part=3)
say(iid, 'question', 400, part=3)
say(iid, 'feedback.correct', round(b3, 4), part=3)
say(iid, 'feedback.correct', round(b2, 4), part=3)
say(iid, 'feedback.correct', round(lead, 4), part=3)
say(iid, 'feedback.correct', 800, part=3)
for v in (round(I3, 4), round(Im, 4), round(lead, 4)):
    say(iid, 'explain.text', v)
ex._rec(abs(b3 - 2 * b2) < 1e-15, 'e-volume-buckets: the three-bucket bias is twice the two-bucket one', '')
# a learner who carries H(sign) to 3 places and the row entropies to 4 lands inside every band
r_hy = round(HY, 3)
rw4 = [1.0, round(Hb([F(70, 120), F(50, 120)]), 4), round(Hb([F(110, 160), F(50, 160)]), 4)]
I3r = r_hy - (0.3 * rw4[0] + 0.3 * rw4[1] + 0.4 * rw4[2])
Imr = r_hy - (0.6 * round(Hb([F(130, 240), F(110, 240)]), 4) + 0.4 * rw4[2])
leadr = (round(I3r, 4) - round(b3, 4)) - (round(Imr, 4) - round(b2, 4))
for part_, v in ((1, I3r), (2, Imr), (3, leadr)):
    w_ = node(W(iid, part_))
    ex._rec(abs(round(v, 4) - w_['answer']) <= w_['tol']['abs'], f'e-volume-buckets part {part_}: the rounded route {round(v, 4)} is in the band', '')

iid = 'e-node-two-consumers'
u_, v_ = F(2), F(3, 2)
given(iid, 'prose', 2, 1.5)
k_ = u_ * v_
m_ = k_ + u_
n_ = m_ * k_
key(iid, n_, part=0)
wrong(iid, 'm-only', m_, part=0)
wrong(iid, 'k-squared', k_ * k_, part=0)
for v in (k_, m_, n_):
    say(iid, 'feedback.correct', v, part=0)
# route B: derivatives of n = u^2 v^2 + u^2 v
dk = m_ + k_
du = 2 * u_ * v_ ** 2 + 2 * u_ * v_
ex._rec(du == k_ * 1 + dk * v_, 'e-node-two-consumers: the closed form agrees with the two paths', '')
key(iid, dk, part=1)
wrong(iid, 'direct', m_, part=1)
wrong(iid, 'through-m', k_, part=1)
for v in (m_, k_, dk):
    say(iid, 'feedback.correct', v, part=1)
say(iid, 'question', dk, part=2)
key(iid, du, part=2)
wrong(iid, 'm-path', k_, part=2)
wrong(iid, 'k-path', dk * v_, part=2)
wrong(iid, 'direct-k', k_ + m_ * v_, part=2)
for v in (k_, dk * v_, du):
    say(iid, 'feedback.correct', v, part=2)
say(iid, 'feedback.byKey.m-path', dk * v_, part=2)
say(iid, 'feedback.byKey.m-path', 1.5, part=2)
say(iid, 'feedback.byKey.direct-k', m_, part=2)
# Priya: '=' for '+=' with the closures of n, m, k in that order
g = {}
g['m'], g['k'] = k_, m_            # n = m * k
g['k'], g['u'] = g['m'], g['m']    # m = k + u overwrites k.grad
g['u'], g['v'] = v_ * g['k'], u_ * g['k']
key(iid, g['u'], part=3)
wrong(iid, 'true', du, part=3)
wrong(iid, 'm-closure', g['k'], part=3)
wrong(iid, 'k-path', dk * v_, part=3)
for v in (m_, k_, 1.5, g['u']):
    say(iid, 'feedback.correct', v, part=3)
say(iid, 'feedback.byKey.k-path', dk, part=3)
say(iid, 'feedback.byKey.k-path', m_, part=3)
say(iid, 'feedback.byKey.k-path', k_, part=3)
for v in (m_, k_, dk, du, 1.5, 9, 6, g['u']):
    say(iid, 'explain.text', v)
ex._rec(2 * u_ * v_ ** 2 == 9 and 2 * u_ * v_ == 6, 'e-node-two-consumers: 9 + 6 from the closed form', '')

iid = 'e-temperature-same-u'
row = [F(1, 10), F(5, 10), F(3, 10), F(1, 10)]
given(iid, 'prose', 0.1, 0.5, 0.3, 0.58)
u = F(58, 100)
tot1 = [sum(row[:k + 1]) for k in range(4)]
pick1 = next(k for k, t in enumerate(tot1) if t > u)
ex._rec(pick1 == 1 and correct_id(iid, 0) == ['a'], 'e-temperature-same-u: T = 1 picks a', str(tot1))
for t in tot1:
    say(iid, 'feedback.correct', t, part=0)
say(iid, 'widget.options', tot1[1], part=0)
say(iid, 'widget.options', 0.1, part=0)
# T = 2: softmax(z / T) with z = ln p takes the square root of each chance and rescales; route B through logits
z = np.log([float(x) for x in row]) / 2.0
th = np.exp(z - z.max()) / np.exp(z - z.max()).sum()
rt = [math.sqrt(float(x)) for x in row]
ex._rec(np.allclose(th, [x / sum(rt) for x in rt], rtol=1e-12), 'e-temperature-same-u: softmax(z/2) equals root chances rescaled', '')
key(iid, th[1], part=1, nd=6)
sq = [x * x for x in row]
wrong(iid, 'colder', sq[1] / sum(sq), part=1)
wrong(iid, 'unscaled', rt[1], part=1)
wrong(iid, 'unchanged', row[1], part=1)
for v in rt + [sum(rt), th[1]]:
    say(iid, 'feedback.correct', round(float(v), 4), part=1)
say(iid, 'feedback.byKey.colder', 2, part=1)
say(iid, 'question', 2, part=1)
toth = list(np.cumsum(th))
pickh = next(k for k, t in enumerate(toth) if t > float(u))
ex._rec(pickh == 2 and correct_id(iid, 2) == ['e'], 'e-temperature-same-u: T = 2 picks e', str(toth))
for t in toth[:3]:
    say(iid, 'feedback.correct', round(float(t), 4), part=2)
    say(iid, 'widget.options', round(float(t), 4), part=2)
say(iid, 'question', 0.58, part=2)
extra = ln(F(1, 2) / F(th[1]))
key(iid, extra, part=3, nd=6)
wrong(iid, 'bits', extra / LN2, part=3)
wrong(iid, 'sign', -extra, part=3)
wrong(iid, 'chances', 0.5 - th[1], part=3)
for v in (0.5, round(float(th[1]), 4), round(extra, 4)):
    say(iid, 'feedback.correct', v, part=3)
ex._rec(abs(round(ln(0.5 / round(float(th[1]), 4)), 4) - extra) <= node(W(iid, 3))['tol']['abs'], 'e-temperature-same-u: the cost from the printed chance, at 4 places, is in the band', '')
for v in (0.5, round(float(th[1]), 4), round(float(toth[1]), 4), 0.58, round(extra, 4)):
    say(iid, 'explain.text', v)

iid = 'e-bigram-of-weeks'
weeks = ['uud', 'udd', 'uu', 'dud']
ix = {'.': 0, 'u': 1, 'd': 2}
a_, b_ = [], []
for w in weeks:
    s = [0] + [ix[c] for c in w] + [0]
    a_ += s[:-1]
    b_ += s[1:]
Nw = np.zeros((3, 3), dtype=int)
np.add.at(Nw, (np.array(a_), np.array(b_)), 1)
letters = sum(len(w) for w in weeks)
key(iid, int(Nw.sum()), part=0)
wrong(iid, 'letters', letters, part=0)
wrong(iid, 'two-marks', letters + 2 * len(weeks), part=0)
for v in (letters, len(weeks), int(Nw.sum())):
    say(iid, 'feedback.correct', v, part=0)
ex._rec(int(Nw[1].sum()) == 6 and int(Nw[1, 0]) == 1, 'e-bigram-of-weeks: row u holds 6 pairs, 1 to the end', str(Nw.tolist()))
sm = F(int(Nw[1, 0]) + 1, int(Nw[1].sum()) + 3)
key(iid, sm, part=1, nd=6)
wrong(iid, 'raw', F(int(Nw[1, 0]), int(Nw[1].sum())), part=1)
wrong(iid, 'plus-one', F(int(Nw[1, 0]) + 1, int(Nw[1].sum()) + 1), part=1)
wrong(iid, 'twenty-seven', F(int(Nw[1, 0]) + 1, int(Nw[1].sum()) + 27), part=1)
for v in (6, 3, round(float(sm), 4)):
    say(iid, 'feedback.correct', v, part=1)
say(iid, 'feedback.byKey.raw', F(1, 6), part=1)
say(iid, 'feedback.byKey.twenty-seven', 27, part=1)
Pw = [[F(int(Nw[i, j]) + 1, int(Nw[i].sum()) + 3) for j in range(3)] for i in range(3)]
held = [0, 1, 2, 0]
chs = [Pw[a][b] for a, b in zip(held, held[1:])]
ex._rec(chs == [F(4, 7), F(4, 9), F(1, 2)], 'e-bigram-of-weeks: ud costs 4/7, 4/9 and 1/2', str(chs))
costs = [-ln(c) for c in chs]
nll = sum(costs) / 3
key(iid, nll, part=2, nd=6)
wrong(iid, 'total', sum(costs), part=2)
wrong(iid, 'bits', nll / LN2, part=2)
wrong(iid, 'no-end', sum(costs[:2]) / 2, part=2)
for v in costs + [nll]:
    say(iid, 'feedback.correct', round(v, 4), part=2)
for fr in ('\\tfrac47', '\\tfrac49', '\\tfrac12'):
    ex.literal(fr, why='the three smoothed chances of .ud., checked exactly as Fractions in the claim above')
key(iid, nll / LN2, part=3, nd=6)
wrong(iid, 'times', nll * LN2, part=3)
wrong(iid, 'perplexity', math.exp(nll), part=3)
say(iid, 'feedback.correct', round(nll, 4), part=3)
say(iid, 'feedback.correct', round(nll / LN2, 4), part=3)
say(iid, 'feedback.byKey.perplexity', round(nll, 4), part=3)
for v in (int(Nw.sum()), 6, 1, 9, round(float(sm), 4), round(nll, 4), round(nll / LN2, 4)):
    say(iid, 'explain.text', v)
ex.literal('\\tfrac29', why='the smoothed chance of the end after u, checked exactly as Fraction(2, 9) in the key above')

iid = 'e-bigram-net-four-pairs'
pairs = [(1, 1), (1, 2), (1, 2), (2, 0)]
# route B: the shipped autograd on the one-layer network
Wt = AG.Tensor(np.zeros((3, 3)))
xs, ys = np.array([a for a, b in pairs]), np.array([b for a, b in pairs])
loss = AG.cross_entropy(Wt[xs], ys)
loss.backward()
key(iid, loss.item(), part=0, nd=6)
wrong(iid, 'bits', lg2(3), part=0)
wrong(iid, 'zero', 0, part=0)
say(iid, 'feedback.correct', round(loss.item(), 4), part=0)
gud = float(Wt.grad[1, 2])
ex._rec(abs(gud - (-0.25)) < 1e-15, 'e-bigram-net-four-pairs: autograd gives -0.25 for W[u, d]', f'{gud}')
key(iid, gud, part=1, nd=6)
wrong(iid, 'no-mean', gud * 4, part=1)
wrong(iid, 'one-row', (F(1, 3) - 1) / 4, part=1)
wrong(iid, 'sign', -gud, part=1)
say(iid, 'feedback.correct', -1, part=1)
say(iid, 'feedback.correct', -0.25, part=1)
key(iid, 0 - 2 * gud, part=2, nd=6)
wrong(iid, 'uphill', 2 * gud, part=2)
wrong(iid, 'unit-step', -gud, part=2)
say(iid, 'question', -0.25, part=2)
say(iid, 'feedback.correct', -0.25, part=2)
say(iid, 'feedback.correct', 0.5, part=2)
# the floor: run descent long enough on the shipped autograd and compare with the counts' loss
Wt = AG.Tensor(np.zeros((3, 3)))
for _ in range(4000):
    Wt.zero_grad()
    L_ = AG.cross_entropy(Wt[xs], ys)
    L_.backward()
    AG.sgd_step([Wt], 2.0)
floor = (ln(3) + 2 * ln(F(3, 2))) / 4
ex._rec(0 < L_.item() - floor < 2e-3, f'e-bigram-net-four-pairs: descent approaches {floor:.6f} from above ({L_.item():.6f})', '')
key(iid, floor, part=3, nd=6)
wrong(iid, 'u-row', (ln(3) + 2 * ln(F(3, 2))) / 3, part=3)
wrong(iid, 'zero', 0, part=3)
wrong(iid, 'bits', floor / LN2, part=3)
say(iid, 'feedback.correct', 1.5, part=3)
say(iid, 'feedback.correct', round(floor, 4), part=3)
for v in (-0.25, 0.5, round(floor, 4)):
    say(iid, 'explain.text', v)
ex.literal('\\tfrac13', why='the equal start chance and the counts\' share of u after u, both exact thirds of the stated pairs')
ex.literal('\\tfrac23', why='the counts\' share of d after u: two of the three u pairs, stated in the prose')

iid = 'e-planted-forward-back'
Cp = AG.Tensor(np.array([[0.5], [-1.0], [2.0]]))
W1p = AG.Tensor(np.array([[0.5, -0.25], [1.0, 0.5]]))
b1p = AG.Tensor(np.array([0.25, 0.3]))
W2p = AG.Tensor(np.array([[1.0, 0.0, -1.0], [2.0, -1.0, 0.5]]))
b2p = AG.Tensor(np.array([0.0, 0.2, 0.0]))
given(iid, 'prose', 0.5, -1, 2, -0.25, 0.25, 0.3, 0.2)
Eb = Cp[np.array([[2, 1]])].reshape(1, 2)
Hh = (Eb @ W1p + b1p).tanh()
Zz = Hh @ W2p + b2p
Lz = AG.cross_entropy(Zz, np.array([1]))
Hh_keep = Hh
Lz.backward()
hv, zv, Lv = Hh.data[0], Zz.data[0], Lz.item()
pv = AG.softmax(zv)
dz = Zz.grad[0]
dh = Hh.grad[0]
say(iid, 'question', 2, part=0)
say(iid, 'question', -1, part=0)
key(iid, hv[1], part=0, nd=6)
wrong(iid, 'no-tanh', float(Eb.data[0] @ W1p.data[:, 1] + b1p.data[1]), part=0)
wrong(iid, 'first-unit', hv[0], part=0)
wrong(iid, 'sign', -hv[1], part=0)
for v in (2, -0.25, 0.5, 0.3, -0.7, round(hv[1], 4)):
    say(iid, 'feedback.correct', v, part=0)
say(iid, 'feedback.byKey.sign', -0.7, part=0)
for v in (round(hv[0], 4), round(hv[1], 4)):
    say(iid, 'question', v, part=1)
    say(iid, 'explain.text', v)
ex._rec(abs(round(hv[1], 4) * -1 + 0.2 - zv[1]) < 0.0001, 'e-planted-forward-back: the rounded h gives the same logit at 4 places', '')
key(iid, zv[1], part=1, nd=6)
wrong(iid, 'no-bias', zv[1] - 0.2, part=1)
wrong(iid, 'first-logit', zv[0], part=1)
for v in (round(hv[0], 4), round(hv[1], 4), 0.2, round(zv[1], 4)):
    say(iid, 'feedback.correct', v, part=1)
say(iid, 'feedback.byKey.no-bias', 0.2, part=1)
for v in zv:
    say(iid, 'question', round(float(v), 4), part=2)
    say(iid, 'explain.text', round(float(v), 4))
# the loss from the rounded logits the question prints lies inside the key's band
zr = np.round(zv, 4)
Lr = float(np.log(np.exp(zr).sum()) - zr[1])
ex._rec(abs(Lr - node(W(iid, 2))['answer']) <= node(W(iid, 2))['tol']['abs'], f'e-planted-forward-back: loss from printed logits {Lr:.6f} is in the band', '')
key(iid, Lv, part=2, nd=6)
wrong(iid, 'bits', Lv / LN2, part=2)
wrong(iid, 'chance', pv[1], part=2)
wrong(iid, 'no-logit', Lv + zv[1], part=2)
ez = np.exp(zv)
for v in list(np.round(zv, 4)) + list(np.round(ez, 4)) + [sum(round(float(x), 4) for x in ez), round(float(pv[1]), 4), round(Lv, 4)]:
    say(iid, 'feedback.correct', float(v), part=2)
ex._rec(abs(sum(round(float(x), 4) for x in ez) - float(ez.sum())) < 1.5e-4,
        'e-planted-forward-back: the printed exponentials add to the printed sum', '')
key(iid, dz[1], part=3, nd=6)
wrong(iid, 'chance', pv[1], part=3)
wrong(iid, 'sign', -dz[1], part=3)
say(iid, 'feedback.correct', round(float(pv[1]), 4), part=3)
say(iid, 'feedback.correct', round(float(dz[1]), 4), part=3)
ex._rec(np.allclose(dz, pv - np.array([0, 1, 0])), 'e-planted-forward-back: autograd gives p - y for the logits', '')
for v in dz:
    say(iid, 'question', round(float(v), 5), part=4)
key(iid, dh[1], part=4, nd=6)
wrong(iid, 'first-row', float(dz @ W2p.data[0]), part=4)
wrong(iid, 'a-only', float(dz[1] * W2p.data[1, 1]), part=4)
for v in (2, 0.5, round(float(dz[0]), 5), round(-float(dz[1]), 5), round(float(dz[2]), 5), round(float(dh[1]), 4)):
    say(iid, 'feedback.correct', v, part=4)
ex._rec(abs(round(float(dz[0]), 5) * 2 + round(float(dz[1]), 5) * -1 + round(float(dz[2]), 5) * 0.5 - dh[1]) <= node(W(iid, 4))['tol']['abs'],
        'e-planted-forward-back: the printed p - y gives a gradient inside the band', '')
say(iid, 'explain.text', round(Lv, 4))
say(iid, 'explain.text', round(float(dh[1]), 4))

# ------------------------------------------------------------------ code items, run in CPython as the page runs them
with open(os.path.join(APP, 'js', 'engine', 'widgets', 'code.js'), encoding='utf8') as f:
    _js = f.read()
JUDGE_SRC = re.search(r'(def __zq_judge\(.*?)`;', _js, re.S).group(1)
_jns = {}
exec(JUDGE_SRC, _jns)
zq_judge = _jns['__zq_judge']


class TO(Exception):
    pass


def _alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, _alarm)
TIMES = {}


def run_page(src, w, cases, tag=None, cwd=None):
    """One namespace: ZQ_LIB, the prelude, the code, then each case's setup and call in order."""
    here = os.getcwd()
    if cwd:
        os.chdir(cwd)
    out = []
    try:
        ns = {'__learner_source__': src}
        exec(ZQ_LIB, ns)
        exec(w.get('prelude', ''), ns)
        try:
            exec(src, ns)
        except Exception:
            return ['load-error'] * len(cases)
        for k, c in enumerate(cases):
            signal.setitimer(signal.ITIMER_REAL, 5.0)
            try:
                t0 = time.perf_counter()
                if c.get('setup'):
                    exec(c['setup'], ns)
                got = eval(c['call'], ns)
                if tag:
                    TIMES[(tag, k + 1)] = time.perf_counter() - t0
                tol = c.get('tol')
                tl = (tol.get('rel', 0), tol.get('abs', 0)) if tol else None
                want = eval(c['expect'], {**ns})
                out.append('ok' if zq_judge(got, want, c.get('compare', 'equal'), tl) == 1.0 else 'fail')
            except TO:
                out.append('timeout')
            except Exception:
                out.append('error')
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
    finally:
        os.chdir(here)
    return out


def code_checks(iid, cwd=None):
    w = node(W(iid))
    sol = run_page(w['solution'], w, w['tests'], tag=iid, cwd=cwd)
    ex._rec(all(r_ == 'ok' for r_ in sol), f'{iid}: solution passes all {len(sol)} hidden tests', str(sol))
    sol_ex = run_page(w['solution'], w, w['examples'], cwd=cwd)
    ex._rec(all(r_ == 'ok' for r_ in sol_ex), f'{iid}: solution passes the examples', str(sol_ex))
    st = run_page(w['starter'], w, w['tests'], cwd=cwd)
    ex._rec(all(r_ != 'ok' for r_ in st), f'{iid}: starter fails all {len(st)} hidden tests', str(st))
    ex._rec(f'runs {len(w["tests"])} hidden tests' in w['how'], f'{iid}: how names {len(w["tests"])} tests', '')
    ex._rec(len(w['mutants']) >= 2, f'{iid}: at least two mutants', '')
    for m in w['mutants']:
        res = run_page(m['source'], w, w['tests'], cwd=cwd)
        first = next((k + 1 for k, r_ in enumerate(res) if r_ != 'ok'), None)
        ex._rec(first == m['test'], f'{iid}: mutant first fails test {m["test"]} ({m["symptom"][:50]})', str(res))
    fbk = node(P(iid) + '.feedback').get('byKey', {})
    firsts = {m['test'] for m in w['mutants']}
    for kk in fbk:
        n_ = int(kk.split('-')[1])
        ex._rec(1 <= n_ <= len(w['tests']), f'{iid}: byKey {kk} names a real test', '')
        ex._rec(n_ in firsts, f'{iid}: byKey {kk} is the first failure of some mutant, so a learner can reach it', '')
    return w


# e-backward-by-hand: route B is the shipped autograd, which computes the same gradients by its own closures
iid = 'e-backward-by-hand'
wg = code_checks(iid)
gns = {}
exec(wg['prelude'], gns)


def ag_grads(Pd, X, y):
    T = {k_: AG.Tensor(v.copy()) for k_, v in Pd.items()}
    L_ = AG.cross_entropy((AG.Tensor(X) @ T['W1'] + T['b1']).tanh() @ T['W2'] + T['b2'], np.asarray(y))
    L_.backward()
    return {k_: t.grad for k_, t in T.items()}, L_.item()


for k, t in enumerate(wg['tests'][:5]):
    ns_ = dict(gns)
    exec(t['setup'], ns_)
    G_b, L_b = ag_grads(ns_['P'], ns_['X'], ns_['y'])
    ex._rec(abs(L_b - ns_['loss_fn'](ns_['P'], ns_['X'], ns_['y'])) < 1e-12, f'{iid}: autograd and loss_fn agree on test {k + 1}\'s case', '')
    if t['compare'] == 'isclose':
        ns_['mlp_grads'] = lambda Pd, X, y: ag_grads(Pd, X, y)[0]
        got = eval(t['call'], ns_)
        got = got.tolist() if hasattr(got, 'tolist') else [g_.tolist() for g_ in got]
        tl = (t['tol']['rel'], t['tol']['abs'])
        ex._rec(zq_judge(got, eval(t['expect']), 'isclose', tl) == 1.0, f'{iid}: autograd gives test {k + 1}\'s expected gradients', '')
ns_ = dict(gns)
exec(wg['tests'][6]['setup'], ns_)
G_b, _ = ag_grads(ns_['P'], ns_['X'], ns_['y'])
ex._rec(all(np.allclose(G_b[k_], ns_['REF'][k_], rtol=1e-12, atol=1e-15) for k_ in G_b), f'{iid}: the setup reference equals autograd', '')
bad = {k_: v.copy() for k_, v in G_b.items()}
bad['b2'] = bad['b2'] * 1.01
worst = max(np.abs(bad['b2'] - G_b['b2']).max(), 0)
scale = max(np.abs(v).max() for v in G_b.values())
ex._rec(math.isclose(worst / scale, float(eval(wg['tests'][6]['expect'])), rel_tol=1e-4), f'{iid}: test 7\'s planted error {worst / scale:.6g} is 1% of b2 over the largest entry', '')
say(iid, 'widget.how', '10^{-7}')
say(iid, 'widget.how', 1000)
say(iid, 'widget.how', '10^{-6}')
say(iid, 'widget.how', 0.001)
say(iid, 'feedback.correct', '10^{-6}')
say(iid, 'feedback.byKey.test-5', 1000)
say(iid, 'explain.text', '10^{-6}')
say(iid, 'question', '1e-5')
ex._rec(np.isfinite(np.array(eval(wg['tests'][4]['expect']))).all(), f'{iid}: the logits-1,000-apart case has finite gradients', '')
ns_ = dict(gns)
exec('P, X, y = make_case(9, shift=1000.0)', ns_)
Zs = np.tanh(ns_['X'] @ ns_['P']['W1'] + ns_['P']['b1']) @ ns_['P']['W2'] + ns_['P']['b2']
ex._rec(np.diff(Zs, axis=1).mean() > 900 and not np.isfinite(np.exp(Zs)).all(), f'{iid}: case 9\'s logits sit about 1,000 apart and overflow np.exp', '')
ex.literal('1%', why='the planted error on b2 (BAD = REF * 1.01 in test 7\'s setup); its effect is checked as test 7\'s expected value above')

# e-beat-the-bigram: route B counts with np.add.at and scores the MLP with the shipped autograd's cross_entropy
iid = 'e-beat-the-bigram'
wb = code_checks(iid, cwd=DATA)
here = os.getcwd()
os.chdir(DATA)
words = open('names.txt').read().splitlines()
os.chdir(here)
ex._rec(len(words) == 32033, 'e-beat-the-bigram: names.txt has 32,033 names', '')
perm = np.random.default_rng(42).permutation(len(words))
tr = [words[i] for i in perm[:25626]]
dv = [words[i] for i in perm[25626:28829]]
ex._rec(len(tr) == 25626 and len(dv) == 3203, 'e-beat-the-bigram: the split is 25,626 and 3,203', '')
say(iid, 'prose', 25626)
say(iid, 'prose', 3203)
SY = '.abcdefghijklmnopqrstuvwxyz'


def pairs_of(ws):
    s = np.array([SY.index(c) for w in ws for c in '.' + w])
    e = np.array([SY.index(c) for w in ws for c in w + '.'])
    return s, e


def bigram_b(trw, dvw, alpha):
    a_, b_ = pairs_of(trw)
    Nn = np.zeros((27, 27))
    np.add.at(Nn, (a_, b_), 1)
    Pn = (Nn + alpha) / (Nn + alpha).sum(axis=1, keepdims=True)
    c_, d_ = pairs_of(dvw)
    return float(-np.log(Pn[c_, d_]).mean())


def mlp_b(dvw, params):
    rows_x, rows_y = [], []
    for w in dvw:
        ctx = [0, 0, 0]
        for ch in w + '.':
            rows_x.append(ctx)
            rows_y.append(SY.index(ch))
            ctx = ctx[1:] + [SY.index(ch)]
    Xd = np.array(rows_x)
    E = params['C'][Xd].reshape(len(Xd), -1)
    Z = np.tanh(E @ params['W1'] + params['b1']) @ params['W2'] + params['b2']
    return AG.cross_entropy(Z, np.array(rows_y)).item()


os.chdir(DATA)
trained = {k_: np.array(v) for k_, v in json.load(open('makemore-mlp.json')).items() if k_ != 'about'}
os.chdir(here)
bg, ml = bigram_b(tr, dv, 1), mlp_b(dv, trained)
sv = (bg - ml) / LN2
exp4 = eval(wb['tests'][3]['expect'])
ex._rec(all(abs(a - b) < 6e-5 for a, b in ((bg, exp4['bigram']), (ml, exp4['mlp']), (sv, exp4['saved_bits']))),
        f'e-beat-the-bigram: route B gives test 4 ({bg:.6f}, {ml:.6f}, {sv:.6f})', '')
for v in (bg, ml, sv):
    ex._rec(abs(v * 1e4 - math.floor(v * 1e4) - 0.5) > 0.01, f'e-beat-the-bigram: {v:.7f} is clear of a rounding tie at 4 places', '')
ex._rec(ml < bg, 'e-beat-the-bigram: the MLP beats the bigram on dev (the exit)', '')
for path in ('feedback.correct', 'explain.text'):
    say(iid, path, round(bg, 4))
    say(iid, path, round(ml, 4))
    say(iid, path, round(sv, 4))
gb = dict()
exec(wb['prelude'].replace("open('names.txt')", f"open({os.path.join(DATA, 'names.txt')!r})").replace(
    "open('makemore-mlp.json')", f"open({os.path.join(DATA, 'makemore-mlp.json')!r})"), gb)
for k, t in enumerate(wb['tests']):
    if t['compare'] != 'isclose' or 'train_names, dev_names, trained' in t['call']:
        continue
    ns_ = dict(gb)
    exec(t.get('setup', ''), ns_)
    m_ = re.match(r"dev_report\((.*), (\w+), ([0-9.]+)\)(\['mlp'\])?$", t['call'])
    trw, dvw = eval('(' + m_.group(1) + ')', ns_)
    Q = ns_[m_.group(2)]
    al = float(m_.group(3))
    b_, m2 = bigram_b(trw, dvw, al), mlp_b(dvw, Q)
    want = eval(t['expect'])
    got = m2 if m_.group(4) else {'bigram': b_, 'mlp': m2, 'saved_bits': (b_ - m2) / LN2}
    ok = abs(got - want) < 6e-5 if m_.group(4) else all(abs(got[k_] - want[k_]) < 6e-5 for k_ in want)
    ex._rec(ok, f'e-beat-the-bigram: route B gives test {k + 1}', f'{got} against {want}')
say(iid, 'widget.how', 0.0002)
say(iid, 'widget.how', 1000)
say(iid, 'widget.how', 0.1)
ex._rec(wb['tests'][5]['call'].endswith('0.1)'), 'e-beat-the-bigram: the alpha = 0.1 test exists', '')

for (tag, k), sec in sorted(TIMES.items()):
    print(f'time {tag} test {k}: {sec * 1000:.1f} ms in CPython')
lim = {iid_: 5.0 + node(W(iid_)).get('budget', 0) / 1000 for iid_ in ('e-backward-by-hand', 'e-beat-the-bigram')}
worst_share = max(sec / lim[tag] for (tag, k), sec in TIMES.items())
ex._rec(max(TIMES.values()) < 0.6, f'every graded case under 0.6 s in CPython (max {max(TIMES.values()) * 1000:.0f} ms), '
        f'so under a third of its limit at Pyodide\'s three times slower (worst {3 * worst_share:.2f} of a limit)', '')

# ------------------------------------------------------------------ structure
ramp = {d: sum(it['difficulty'] == d for it in items) for d in (2, 3, 4, 5)}
ex._rec(ramp == {2: 6, 3: 15, 4: 6, 5: 3} and len(items) == 30, f'ramp 6, 15, 6, 3 of 30: {ramp}', '')
cover = {s: sum(s in it['skills'] for it in items) for s in doc['skills']}
ex._rec(all(v >= 2 for v in cover.values()), f'every skill on 2 or more items: {cover}', '')
course_skills = set()
for c in ('info', 'backprop', 'makemore'):
    with open(os.path.join(APP, 'content', 'courses', c, 'course.json'), encoding='utf8') as f:
        course_skills |= set(json.load(f)['skills'])
ex._rec(set(doc['skills']) == course_skills, 'the exam names exactly the 16 skills of info, backprop and makemore', '')
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
