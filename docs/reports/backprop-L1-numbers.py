"""Recompute every number stated in backprop level 1 (The chain rule on a graph) and check it at its JSON path.

Run: <venv>/bin/python docs/reports/backprop-L1-numbers.py   (standard library only; exits 0 when every check passes)

Route 1 is the rule (local derivatives multiplied along a path, as the lessons teach). Route 2 is independent:
a central difference of the whole expression ((f(x + h) - f(x - h)) / 2h, h = 1e-6), or a direct recomputation
of the forward pass. `two` fails when the routes disagree. The code items' model solutions are run in CPython and
their hidden-test expectations are recomputed by route 2.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("backprop", 1)
E = lv.expect


def two(label, a, b, tol=1e-6):
    lv.claim(math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol), f'{label}: routes agree ({a!r} vs {b!r})')


def cd(f, args, i, h=1e-6):
    up = list(args); dn = list(args); up[i] += h; dn[i] -= h
    return (f(*up) - f(*dn)) / (2 * h)


def D(ref):
    return lv._file(ref)[1]


# ---------- the course expression L = (ab + c) f ----------
def Lc(a, b, c, f):
    return (a * b + c) * f


C = (1.5, -2.0, 4.0, -3.0)
a, b, c, f = C
e = a * b; d = e + c; L = d * f
rule = {'a': f * 1 * b, 'b': f * 1 * a, 'c': f * 1, 'f': d}
for i, k in enumerate('abcf'):
    two(f'course dL/d{k}', rule[k], cd(Lc, C, i))
two('dL/de = dL/dd = f', f, cd(lambda ee: (ee + c) * f, (e,), 0))
lv.claim((e, d, L) == (-3, 1, -3), 'course forward values e=-3, d=1, L=-3')
lv.claim(rule == {'a': 6, 'b': -4.5, 'c': -3, 'f': 1}, 'course gradients 6, -4.5, -3, 1')
two('nudge a by 0.01 moves L by 0.06', Lc(1.51, b, c, f) - L, 0.06, 1e-9)

# l1 screen 1: a step of 0.5 in each input
steps = {k: Lc(*[v + (0.5 if j == i else 0) for j, v in enumerate(C)]) for i, k in enumerate('abcf')}
lv.claim(steps == {'a': 0.0, 'b': -5.25, 'c': -4.5, 'f': -2.5}, 'l1 s1 slider steps give 0, -5.25, -4.5, -2.5')
for k, v in (('a', 0), ('b', -5.25), ('c', -4.5), ('f', -2.5)):
    E('l1', 'screens[0].explain.text', v)
E('l1', 'screens[0].widget.options', 2.25); E('l1', 'screens[0].widget.options', 1.5); E('l1', 'screens[0].widget.options', 0.5)
E('l1', 'screens[2].widget.rows[0][2].answer', -3); E('l1', 'screens[2].widget.rows[1][2].answer', 1); E('l1', 'screens[2].widget.rows[2][2].answer', -3)
lv.claim((-e, -e + c, e * f) == (3, 7, 9), 'l1 s3 slips: sign of e, carried sign into d, e times f')
# l1 s4: M = e^{xy} + z^2
M = math.exp(0.5 * 2) + (-1.5) ** 2
two('M route 2 (math.e + 2.25)', M, math.e + 2.25)
E('l1', 'screens[3].widget.answer', round(M, 3)); E('l1', 'screens[3].explain.text', 4.968282)
E('l1', 'screens[3].widget.wrong[0].value', round(math.e - 2.25, 3))
E('l1', 'screens[5].explain.text', -1.5); two('K = ab + a', 1.5 * -2 + 1.5, -1.5)
# l1 s7 forward_pass tests
ns = {}; exec(lv.text('l1', 'screens[6].widget.solution'), ns)
for t in json.loads(json.dumps(D('l1')['screens'][6]['widget']['tests'])):
    got = eval(t['call'], ns); exp = eval(t['expect'])
    args = eval(t['call'][len('forward_pass'):])
    ee = args[0] * args[1]; dd = ee + args[2]
    lv.claim(got == exp == {'e': ee, 'd': dd, 'L': dd * args[3]}, f'forward_pass test {t["call"]}')
# l1 transfer: P&L
r1 = 206 / 200 - 1; r2 = 49 / 50 - 1; R = 0.6 * r1 + 0.4 * r2; PL = 500000 * R
two('P&L route 2 (holdings: 1500 shares x £6 + 4000 shares x -£1)', PL, 1500 * 6 + 4000 * -1)
E('l1', 'screens[8].widget.answer', 5000); E('l1', 'screens[8].widget.wrong[1].value', 500000 * (0.6 * r1 + 0.4 * 0.02))
E('l1', 'quiz[1].widget.answer', (2 - 5) * 4)

# ---------- l2 ----------
two('l2 s1 d moves 0.01', (-2.99 + 4) - 1, 0.01, 1e-9)
two('l2 s3 de/db', cd(lambda bb: 1.5 * bb, (-2.0,), 0), 1.5)
E('l2', 'screens[2].widget.answer', 1.5)
two('l2 s4 (u^3)\' at 2', cd(lambda u: u ** 3, (2.0,), 0), 12); two('l2 s4 (e^u)\' at 0', cd(math.exp, (0.0,), 0), 1); two('l2 s4 (ln u)\' at 4', cd(math.log, (4.0,), 0), 0.25)
E('l2', 'screens[3].widget.rows[2][2].wrong[0].value', round(math.log(4), 3))
two('l2 s5 de/da', cd(lambda aa: aa * -2, (1.5,), 0), -2); two('l2 s5 dL/dd', cd(lambda dd: dd * -3, (1.0,), 0), -3)
two('l2 s6 nudge a: e moves -0.02', 1.51 * -2 - (1.5 * -2), -0.02, 1e-9)
E('l2', 'screens[6].widget.options', 2.5); E('l2', 'screens[6].widget.options', 100)
# l2 transfer: the bond of limits l15
P = lambda y: sum(4 / (1 + y) ** t for t in range(1, 6)) + 100 / (1 + y) ** 5
Pd = sum(-4 * t / (1 + 0.05) ** (t + 1) for t in range(1, 6)) - 500 / 1.05 ** 6
two('bond slope rule vs central difference', Pd, cd(P, (0.05,), 0), 1e-7)
lv.claim(round(P(0.05), 2) == 95.67 and round(Pd, 2) == -420.98, 'bond P(0.05) = 95.67, P\'(0.05) = -420.98')
E('l2', 'screens[8].prose', 95.67); E('l2', 'screens[8].prose', -420.98); E('l2', 'screens[8].widget.answer', round(-420.98 * 0.001, 3))
E('l2', 'quiz[0].widget.answer', -0.5); E('l2', 'quiz[1].widget.answer', 1); two('l2 quiz 3: e^(ln 3)', math.exp(math.log(3)), 3, 1e-12)
E('l2', 'quiz[2].widget.wrong[0].value', round(math.log(3), 4))

# ---------- l3 ----------
two('l3 s2 product along path', 1 * -3 * 1 * -2, cd(Lc, C, 0))
E('l3', 'screens[1].widget.answer', 6); E('l3', 'screens[2].widget.answer', 6 * 0.02)
lv.claim(all(abs(Lc(x, b, c, f) - (6 * x - 12)) < 1e-12 for x in (0.5, 1.5, 2.5)), 'l3 s4: L = 6a - 12 on the plotted range')
E('l3', 'screens[4].widget.rows[0][2].answer', -3); E('l3', 'screens[4].widget.rows[1][2].answer', 1)
E('l3', 'screens[5].widget.answer', -4.5); two('l3 s6 dL/db central', cd(Lc, C, 1), -4.5)
E('l3', 'screens[5].explain.text', -0.045); two('l3 s6 nudge b moves L by -0.045', Lc(a, b + 0.01, c, f) - L, -0.045, 1e-9)
relu = lambda a_, b_, c_, f_: max(0.0, a_ * b_ + c_) * f_
two('l3 s7 relu off: dL/da = 0', cd(relu, (1.5, -2.0, 2.0, -3.0), 0), 0)
two('l3 s9 dPL/dp1', 500000 * 0.6 / 200, cd(lambda p1: 500000 * (0.6 * (p1 / 200 - 1) + 0.4 * (49 / 50 - 1)), (206.0,), 0), 1e-6)
E('l3', 'screens[8].widget.answer', 1500); E('l3', 'screens[8].widget.wrong[0].value', 500000 * 0.6)
two('l3 quiz 1', cd(Lc, (2.0, 5.0, -1.0, 0.5), 0), 2.5); E('l3', 'quiz[0].widget.answer', 2.5)
two('l3 quiz 3', -3 * -0.02, Lc(a, b, 3.98, f) - L, 1e-9)

# ---------- l4: L = (e^{wx + b})^2 ----------
Lchain = lambda w, x, bb: math.exp(w * x + bb) ** 2
CH = (2.0, 0.5, -1.5)
q = math.exp(2 * 0.5 - 1.5); gs = 2 * q * q
two('l4 dL/dw', gs * 0.5, cd(Lchain, CH, 0)); two('l4 dL/dx', gs * 2, cd(Lchain, CH, 1)); two('l4 dL/db', gs, cd(Lchain, CH, 2))
for path, v in (('screens[0].widget.rows[2][1].answer', 0.6065), ('screens[0].widget.rows[3][1].answer', 0.3679), ('screens[1].widget.rows[4][2].answer', 1.2131),
                ('screens[5].widget.answer', 0.3679)):
    E('l4', path, v)
two('l4 L = e^-1', Lchain(*CH), math.exp(-1), 1e-12)
lv.claim(round(q, 4) == 0.6065 and round(q * q, 4) == 0.3679 and round(2 * q, 4) == 1.2131 and round(gs, 4) == 0.7358 and round(gs * 2, 4) == 1.4715 and round(gs * 0.5, 4) == 0.3679, 'l4 table values to 4 places')
lv.claim(round(1.2131 * 0.5 * 1, 4) == 0.6065 or round(0.5 * 1 * 1.2131, 4) == 0.6066, 'l4 trap slip value (skipped exp) is 0.6065 to 4 places from rounded figures')
two('l4 trap slip: 2q * 0.5 unrounded', 2 * q * 0.5, 0.6065, 1e-4)
E('l4', 'screens[0].widget.rows[2][1].wrong[0].value', round(math.exp(0.5), 4))
two('l4 s4 2e^{2s} at s = -0.5', 2 * math.exp(-1), cd(lambda s: math.exp(s) ** 2, (-0.5,), 0))
two('l4 s5 2w e^{2(wx+b)}', 2 * 2 * math.exp(-1), cd(Lchain, CH, 1))
ns = {}; exec(lv.text('l4', 'screens[7].widget.solution'), ns)
for t in D('l4')['screens'][7]['widget']['tests']:
    args = eval(t['call'][len('all_gradients'):])
    got = eval(t['call'], ns); exp = eval(t['expect'])
    num = {k: cd(Lc, args, i) for i, k in enumerate('abcf')}
    ee = args[0] * args[1]
    num['e'] = cd(lambda x: (x + args[2]) * args[3], (ee,), 0); num['d'] = cd(lambda x: x * args[3], (ee + args[2],), 0)
    lv.claim(got == exp and all(math.isclose(got[k], num[k], abs_tol=1e-6) for k in got), f'all_gradients test {t["call"]} against central differences')
E('l4', 'screens[8].widget.answer', 10001)
two('l4 quiz 1: e * 2', math.exp(1) * 2, cd(lambda v: math.exp(v * 2), (0.5,), 0)); E('l4', 'quiz[0].widget.answer', round(2 * math.e, 4))
E('l4', 'quiz[0].widget.wrong[1].value', round(math.e, 4)); E('l4', 'quiz[0].widget.wrong[0].value', round(math.e * 0.5, 4))
two('l4 quiz 2', cd(lambda y: (y + 2) ** 2, (1.0,), 0), 6)

# ---------- review-1 ----------
E('review', 'items[0].widget.answer', (3 - 5) ** 2 * 0.5)
two('review dq/dt', cd(lambda t: -4 * t, (0.25,), 0), -4); two('review (ln u)\' at 0.2', cd(math.log, (0.2,), 0), 5)
E('review', 'items[3].widget.wrong[0].value', round(math.log(0.2), 4))
two('review dL/db', cd(Lc, (-1.0, 4.0, 6.0, 2.5), 1), -2.5); E('review', 'items[5].widget.answer', -1.8 * 0.05)
two('review relu', cd(lambda x: 5 * max(0.0, x - 2), (1.4,), 0), 0)
two('review dL/dq', cd(lambda qq: (2 * qq + 1) ** 2, (-1.0,), 0), -4)
two('review cube', cd(lambda y: (2 + y) ** 3, (1.0,), 0), 27); E('review', 'items[8].widget.lines', 27)
two('review 2x e^{x^2} at x = 0.7', 2 * 0.7 * math.exp(0.49), cd(lambda x: math.exp(x * x), (0.7,), 0))

# ---------- homework-1 ----------
V = 100 * math.exp(-0.04 * 5)
two('hw dV/dr', -5 * V, cd(lambda r: 100 * math.exp(-r * 5), (0.04,), 0)); E('homework', 'items[0].widget.answer', round(-5 * V, 2))
E('homework', 'items[0].prose', round(V, 2)); E('homework', 'items[0].widget.wrong[2].value', round(-0.04 * V, 2))
Lsl = lambda x, y, z: (x * y + math.log(z)) ** 2
for i, k in enumerate('xyz'):
    two(f'hw order dL/d{k}', {'x': 36, 'y': 24, 'z': 12}[k], cd(Lsl, (2.0, 3.0, 1.0), i), 1e-5)
for idx, fn, f_, keys in ((2, 'grads_square_log', Lsl, 'xyz'),):
    ns = {}; exec(D('homework')['items'][idx]['widget']['solution'], ns)
    for t in D('homework')['items'][idx]['widget']['tests']:
        args = eval(t['call'][len(fn):]); got = eval(t['call'], ns); exp = eval(t['expect'])
        lv.claim(all(math.isclose(got[k], exp[k], rel_tol=1e-12) and math.isclose(exp[k], cd(f_, args, i), rel_tol=1e-5, abs_tol=1e-6) for i, k in enumerate(keys)), f'{fn} test {args}')
ns = {}; exec(D('homework')['items'][3]['widget']['solution'], ns)


def ev(spec, vals):
    if isinstance(spec, str):
        return vals[spec]
    if isinstance(spec, (int, float)):
        return float(spec)
    o = spec[0]
    return {'add': lambda: ev(spec[1], vals) + ev(spec[2], vals), 'mul': lambda: ev(spec[1], vals) * ev(spec[2], vals),
            'exp': lambda: math.exp(ev(spec[1], vals)), 'pow': lambda: ev(spec[1], vals) ** spec[2]}[o]()


for t in D('homework')['items'][3]['widget']['tests']:
    inner = t['call'][len('grad_of('):-1]
    spec, vals = eval('(' + inner + ')')
    got = ns['grad_of'](spec, vals); exp = eval(t['expect'])
    names = list(vals)
    numg = {k: cd(lambda *xs: ev(spec, dict(zip(names, xs))), [vals[n] for n in names], i) for i, k in enumerate(names)}
    lv.claim(all(math.isclose(got[k], exp[k], rel_tol=1e-12) and math.isclose(exp[k], numg[k], rel_tol=1e-5, abs_tol=1e-6) for k in names), f'grad_of test {spec}')
E('homework', 'items[4].widget.answer', 2 * 2000000)
# performance task model answer
pq = math.exp(0.4); ps = pq - 1; pL = ps * ps
gx = 2 * ps * pq * 0.8; gy = 2 * ps * pq * 0.5
Lp = lambda x, y: (math.exp(x * y) - 1) ** 2
two('perf dL/dx', gx, cd(Lp, (0.5, 0.8), 0)); two('perf dL/dy', gy, cd(Lp, (0.5, 0.8), 1))
for v in (round(pq, 6), round(ps, 6), round(pL, 6), round(2 * ps, 6), round(2 * ps * pq, 6), round(gx, 6), round(gy, 6),
          round(Lp(0.51, 0.8), 6), round(Lp(0.51, 0.8) - pL, 6), round(gx * 0.01, 6), round(math.exp(0.408), 6)):
    E('homework', 'items[5].model', v)
lv.claim(abs((Lp(0.51, 0.8) - pL) / (gx * 0.01) - 1) < 0.03, 'perf nudge agrees with the gradient to about 2%')

# ---------- problems-1 ----------
E('problems', 'items[0].parts[0].widget.answer', (1.2 - 0.7) * 4); E('problems', 'items[0].parts[3].widget.answer', 4 * 0.02)
two('problems 1 dg/dm', cd(lambda m: (m - 0.7) * 4, (1.2,), 0), 4)
E('problems', 'items[1].parts[0].widget.answer', round(3 * math.log(2), 4)); two('problems 2 dy/du', cd(lambda u: 3 * math.log(u), (2.0,), 0), 1.5)
E('problems', 'items[1].parts[3].feedback.correct', round(3 * math.log(2.02) - 3 * math.log(2), 5))
Vfx = lambda X: 200 * 50 / X
two('problems 3 dV/dX', cd(Vfx, (1.25,), 0), -6400, 1e-6); E('problems', 'items[2].parts[0].widget.answer', Vfx(1.25))
E('problems', 'items[2].parts[3].feedback.correct', round(Vfx(1.26) - Vfx(1.25), 2)); E('problems', 'items[2].parts[1].widget.answer', -1 / 1.25 ** 2)

lv.check_wrongs()
lv.report()
