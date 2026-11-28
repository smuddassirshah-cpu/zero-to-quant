"""Recompute every number stated in backprop level 2 (The backward pass) and check it at its JSON path.

Run: <venv>/bin/python docs/reports/backprop-L2-numbers.py   (standard library only; exits 0 when every check passes)

Route 1 runs a reference scalar `Value` (the level's final class, taken from the l8 code screen's model solution)
or the sum-over-paths rule; route 2 is a central difference of the closed-form expression (h = 1e-6). The
`=` slips are recomputed by a copy of the class whose closures use `=`, and Sam's every-node list by a class that
records every node it makes. Every code item's model solution is run against its hidden tests in CPython.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("backprop", 2)
E = lv.expect


def D(ref):
    return lv._file(ref)[1]


def two(label, a, b, tol=1e-6):
    lv.claim(math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol), f'{label}: routes agree ({a!r} vs {b!r})')


def cd(f, args, i, h=1e-6):
    up = list(args); dn = list(args); up[i] += h; dn[i] -= h
    return (f(*up) - f(*dn)) / (2 * h)


ns = {}
exec(D('l8')['screens'][3]['widget']['solution'], ns)
V = ns['Value']

# buggy copy: '=' in every closure
BUG = D('l8')['screens'][3]['widget']['solution'].replace('.grad += ', '.grad = ')
nb = {}
exec(BUG, nb)
VB = nb['Value']

# ---------- l5 ----------
g = lambda x, y: (x + y) * x
x, y = V(2.0), V(3.0); G = (x + y) * x; G.backward()
two('l5 dg/dx', x.grad, cd(g, (2.0, 3.0), 0)); two('l5 dg/dy', y.grad, cd(g, (2.0, 3.0), 1))
lv.claim((G.data, x.grad, y.grad) == (10, 7, 2), 'l5 branch: g = 10, 7 and 2')
two('l5 nudge', g(2.01, 3) - 10, 0.0701, 1e-9); E('l5', 'screens[0].widget.answer', 0.0701)
E('l5', 'screens[0].widget.wrong[0].value', round(5 * 0.01, 4)); E('l5', 'screens[0].widget.wrong[1].value', round(2 * 0.01, 4))
h3 = lambda x, y: x * y + x * x + 3 * x
x, y = V(2.0), V(3.0); Hh = x * y + x * x + 3 * x; Hh.backward()
two('l5 three uses', x.grad, cd(h3, (2.0, 3.0), 0)); lv.claim(x.grad == 10 and Hh.data == 16, 'l5 h = 16, dh/dx = 10')
# accumulation and the '=' slip
x, y = VB(2.0), VB(3.0); G = (x + y) * x; G.backward()
lv.claim(x.grad == 2, "l5 trap: '=' closures print 2 for x.grad")
x = V(3.0); Y = x * x; Y.backward(); two('l5 x*x at 3', x.grad, cd(lambda t: t * t, (3.0,), 0))
xb = VB(5.0); yb = xb + xb; yb.backward(); lv.claim(xb.grad == 1, "l7 trap: '=' sum closure on v + v gives 1")
E('l5', 'screens[8].widget.answer', -3200 + 1100)
x = V(3.0); F = (x + 2) * x; F.backward(); two('l5 quiz (a + 2)a at 3', x.grad, cd(lambda t: (t + 2) * t, (3.0,), 0)); E('l5', 'quiz[0].widget.answer', 8)
x = V(-1.5); Y = x * x; Y.backward(); lv.claim(x.grad == -3, 'l5 quiz v*v at -1.5 gives -3')

# ---------- l6 ----------
# Sam's wrong order: the sum box before the product box
x, y = V(2.0), V(3.0); s = x + y; G = s * x; G.grad = 1.0
s._backward(); G._backward()
lv.claim(y.grad == 0 and x.grad == 5, 'l6 hook: sum box first leaves y.grad = 0 (x.grad 5)')
# DFS append order on the course graph
a, b, c, f = V(1.5), V(-2.0), V(4.0), V(-3.0); e = a * b; d = e + c; L = d * f
names = {id(a): 'a', id(b): 'b', id(c): 'c', id(f): 'f', id(e): 'e', id(d): 'd', id(L): 'L'}
topo, seen = [], set()


def build(v):
    if v not in seen:
        seen.add(v)
        for p in v._prev:
            build(p)
        topo.append(v)


build(L)
order = [names[id(v)] for v in topo]
lv.claim(order == ['a', 'b', 'e', 'c', 'd', 'f', 'L'], f'l6 DFS order {order}')
lv.claim(order[4] == 'd', 'l6 s3: d appended fifth'); lv.claim(list(reversed(order)).index('e') + 1 == 5, 'l8 s2: e runs fifth reversed')
# seven-node graph o = (uv + w)u + v
o7 = lambda u, v, w: (u * v + w) * u + v
u, v, w = V(2.0), V(-1.0), V(3.0); k = u * v; m = k + w; n = m * u; o = n + v; o.backward()
lv.claim((k.data, m.data, n.data, o.data) == (-2, 1, 2, 1), 'l6 seven-node forward values')
lv.claim((n.grad, m.grad, k.grad, w.grad, u.grad, v.grad) == (1, 2, 2, 2, -1, 5), 'l6 seven-node gradients 1, 2, 2, 2, -1, 5')
for i, val in enumerate((u.grad, v.grad, w.grad)):
    two(f'l6 seven-node central {i}', val, cd(o7, (2.0, -1.0, 3.0), i))
# Sam's list of every node ever made
made = []


class VS(V):
    def __init__(self, *a_, **k_):
        super().__init__(*a_, **k_); made.append(self)

    def __add__(self, other):
        other = other if isinstance(other, V) else VS(other)
        out = VS(self.data + other.data, (self, other), '+')

        def _b():
            self.grad += out.grad; other.grad += out.grad
        out._backward = _b
        return out

    def __mul__(self, other):
        other = other if isinstance(other, V) else VS(other)
        out = VS(self.data * other.data, (self, other), '*')

        def _b():
            self.grad += other.data * out.grad; other.grad += self.data * out.grad
        out._backward = _b
        return out

    __rmul__ = __mul__


wv = VS(2.0); p_old = wv * 3; p_old.grad = 1.0
Lnew = wv * 5; wv.grad = 0.0; Lnew.grad = 1.0
for node in reversed(made):
    node._backward()
lv.claim(wv.grad == 8, f"l6 trap: Sam's every-node list gives {wv.grad}")
wv2 = V(2.0); Lb = wv2 * 5; Lb.backward(); lv.claim(wv2.grad == 5, 'l6 trap: the right answer is 5')
# topo_order tests
for idx, fid in ((6, 'l6'),):
    w_ = D(fid)['screens'][idx]['widget']; ns2 = {}
    exec(w_['prelude'] + w_['solution'], ns2)
    for t in w_['tests']:
        lv.claim(repr(eval(t['call'], ns2)) == t['expect'], f'{fid} topo_order test {t["call"]}')

# ---------- l7 ----------
a, b = V(1.5), V(-2.0); e = a * b; e.grad = 3.0; e._backward()
lv.claim((a.grad, b.grad) == (-6, 4.5), 'l7 closure by hand: (-6, 4.5)'); E('l7', 'screens[4].explain.text', 4.5)
E('l7', 'screens[8].prose', 30000); two('l7 futures dP/dF', cd(lambda F: 10 * 250 * (F - 4000), (4012.0,), 0), 2500, 1e-6)
lv.claim(10 * 250 * (4012 - 4000) == 30000, 'l7 futures P&L 30,000')
x, y = V(1.0), V(0.5); s = x + y; s.grad = 2.5; x.grad = 1.0; s._backward(); lv.claim(x.grad == 3.5, 'l7 quiz: 1.0 + 2.5')
u, w = V(0.5), V(-4.0); p = u * w; p.grad = 2.0; p._backward(); lv.claim(w.grad == 1, 'l7 quiz: w.grad = 1')
for idx in (2, 7):
    w_ = D('l7')['screens'][idx]['widget']
    for t in w_['tests']:
        n3 = {}; exec(w_['solution'], n3); exec(t.get('setup', ''), n3)
        lv.claim(repr(eval(t['call'], n3)) == t['expect'], f'l7 s{idx + 1} test {t["call"]}')

# ---------- l8 ----------
w_ = D('l8')['screens'][3]['widget']
for t in w_['tests']:
    n3 = {}; exec(w_['solution'], n3); exec(t.get('setup', ''), n3)
    lv.claim(repr(eval(t['call'], n3)) == t['expect'], f'l8 backward test {t["call"][:40]}')
two('l8 chain of ten boxes', cd(lambda t: ((((t * 2 + 1) * 2 + 1) * 2 + 1) * 2 + 1) * 2 + 1, (1.0,), 0), 32)
a, b, c, f = V(1.5), V(-2.0), V(4.0), V(-3.0)
L = (a * b + c) * f; L.backward(); L = (a * b + c) * f; L.backward(); lv.claim(a.grad == 12, 'l8 rebuilt twice: 12')
a, b, c, f = V(1.5), V(-2.0), V(4.0), V(-3.0); L = (a * b + c) * f; L.backward(); L.backward(); lv.claim(a.grad == 24, 'l8 same graph twice: 24')
a, b, c, f = V(1.5), V(-2.0), V(4.0), V(-3.0); L = (a * b + c) * f; L.backward(); a.data = 2.0; L = (a * b + c) * f; L.backward()
lv.claim(b.grad == -10.5, 'l8 trap: no reset gives -10.5'); two('l8 trap: true gradient at a = 2', cd(lambda bb: (2 * bb + 4) * -3, (-2.0,), 0), -6)
x = V(2.0); Y = x * x + 3 * x + 1; Y.backward(); lv.claim((Y.data, x.grad) == (11, 7), 'l8 x*x + 3x + 1 at 2: 11 and 7')
E('l8', 'screens[8].widget.answer', 0.8 * -400)
x = V(1.5); Y = x * x * x; Y.backward(); two('l8 quiz cube', x.grad, cd(lambda t: t ** 3, (1.5,), 0)); E('l8', 'quiz[2].widget.answer', 6.75)

# ---------- review-2 ----------
two('review (p + 4)p at -1', cd(lambda t: (t + 4) * t, (-1.0,), 0), 2); two('review xy + x', cd(lambda t: t * -2 + t, (4.0,), 0), -1)
x, y = VB(4.0), VB(1.0); G = (x + y) * x; G.backward(); lv.claim(x.grad == 4, "review '=' slip prints 4")
two('review true gradient 9', cd(lambda t: (t + 1) * t, (4.0,), 0), 9)
two('review do/dv', cd(lambda u_, v_: (u_ * v_) * u_ + v_, (3.0, 2.0), 1), 10)
u, w = V(2.0), V(0.5); q = u * w; q.grad = -4.0; q._backward(); lv.claim(u.grad == -2, 'review closure by hand -2')
x = V(-1.0); Y = 2 * x * x + x; Y.backward(); two('review 2x^2 + x at -1', x.grad, cd(lambda t: 2 * t * t + t, (-1.0,), 0))

# ---------- homework-2 ----------
for i in (0, 1, 5):
    w_ = D('homework')['items'][i]['widget']
    for t in w_['tests']:
        n3 = {}; exec(w_.get('prelude', '') + '\n' + w_['solution'], n3); exec(t.get('setup', ''), n3)
        got = eval(t['call'], n3); exp = eval(t['expect'])
        ok = got == exp if t['compare'] == 'equal' else all(math.isclose(p_, q_, rel_tol=1e-12) for p_, q_ in zip(got, exp))
        lv.claim(ok, f'homework item {i + 1} test {t["call"][:40]}')
zx = lambda x_, y_: math.exp(x_ * x_ - y_)
for pt in ((1.0, 0.5), (-0.5, 2.0)):
    two(f'hw e^(x^2 - y) dx at {pt}', 2 * pt[0] * zx(*pt), cd(zx, pt, 0)); two(f'hw e^(x^2 - y) dy at {pt}', -zx(*pt), cd(zx, pt, 1))
two('hw four shares', cd(lambda x_: (x_ + 2) * (x_ * 2), (1.0,), 0), 8)
E('homework', 'items[4].widget.answer', 8)
two('hw x*x nudge', 3.01 * 3.01 - 9, 0.0601, 1e-9); E('homework', 'items[3].model', 0.0601); E('homework', 'items[3].model', 9.0601)
lv.claim(round(3.01 * 3 - 9, 2) == 0.03, 'hw longform: one slot held gives 0.03')
# perf tests against central differences on their closed forms
two('perf chain', cd(lambda t: ((t * 4 + 1) * 3 + 2) * 0.5, (0.5,), 0), 6)
two('perf diamond', cd(lambda t: (t * 2) * (t + 5), (3.0,), 0), 22)
two('perf cube', cd(lambda t: t ** 3, (-2.0,), 0), 12)
two('perf after reset dL/dw', cd(lambda w_: 2.0 * w_ + 2.0, (-1.0,), 0), 2)

# ---------- problems-2 ----------
oa = lambda a_, b_, c_: (a_ * b_ + a_) * c_
E('problems', 'items[0].parts[1].widget.answer', oa(2, 1, 3)); two('problems 1 total', cd(oa, (2.0, 1.0, 3.0), 0), 6)
R = lambda w_: (w_ * 2) ** 2 + w_ * 3
E('problems', 'items[1].parts[0].widget.answer', R(0.5)); two('problems 2 total', cd(R, (0.5,), 0), 7)
E('problems', 'items[1].parts[4].explain.text', round(R(0.51) - R(0.5), 4))
gg = lambda x_: (x_ * 0.5 + x_) * x_
E('problems', 'items[2].parts[0].widget.answer', gg(2.0)); two('problems 3 total', cd(gg, (2.0,), 0), 6)
x, y = VB(2.0), VB(0.5); Gb = (x * y + x) * x; Gb.backward(); lv.claim(x.grad == 1, "problems 3 part 5: '=' closures leave 1")
x, y = V(2.0), V(0.5); Gv = (x * y + x) * x; Gv.backward(); lv.claim(x.grad == 6, 'problems 3: the Value class gives 6')

lv.check_wrongs()
lv.report()
