"""Recompute every number stated in rl level 2 (MDPs and value iteration) and check it at its JSON path.

Run: <venv>/bin/python docs/reports/rl-L2-numbers.py   (NumPy and the standard library; exits 0 when every check passes)

Two routes per number. The gridworld is rebuilt here as arrays (P[a, s, t], R[a, s, t]); optimal values come from value
iteration on those arrays and again from policy iteration's linear solves, and the deterministic values also from the
closed form V(d) = 0.9^(d-1) - 0.4(1 - 0.9^d) over breadth-first distances. Two-state systems are solved by Cramer's rule
and by np.linalg.solve. Each code widget's solution is run against its tests in CPython (prelude included) and its
starter must fail one.
"""
import math, os, sys
from collections import deque
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level('rl', 2)
E, C = lv.expect, lv.claim


def J(ref, path):
    _, doc = lv._file(ref)
    node = doc
    for part in path.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.lstrip('-').isdigit() else node[part]
    return node


# ---------- the gridworld as arrays ----------
CELLS = [f'r{r}c{c}' for r in range(1, 5) for c in range(1, 6) if (r, c) != (2, 3)]
IX = {s: i for i, s in enumerate(CELLS)}
END = {'r1c5': 1.0, 'r2c5': -1.0}
ACTS = 'URDL'
DIR = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDE = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}


def nxt(s, a):
    r, c = int(s[1]), int(s[3])
    r2, c2 = r + DIR[a][0], c + DIR[a][1]
    t = f'r{r2}c{c2}'
    return t if 1 <= r2 <= 4 and 1 <= c2 <= 5 and t != 'r2c3' else s


def arrays(slip, step=-0.04):
    n = len(CELLS)
    P = np.zeros((4, n, n)); R = np.zeros((4, n, n))
    for ai, a in enumerate(ACTS):
        for s in CELLS:
            i = IX[s]
            if s in END:
                P[ai, i, i] = 1.0
                continue
            for b, p in ((a, 1 - 2 * slip), (SIDE[a][0], slip), (SIDE[a][1], slip)):
                if p > 0:
                    t = nxt(s, b)
                    P[ai, i, IX[t]] += p
                    R[ai, i, IX[t]] = END.get(t, 0.0) + step
    return P, R


def vi(P, R, g=0.9, tol=1e-10):
    e = (P * R).sum(2); V = np.zeros(P.shape[1]); k = 0; deltas = []
    while True:
        k += 1
        n = (e + g * P @ V).max(0)
        d = np.max(np.abs(n - V)); deltas.append(d); V = n
        if d < tol:
            return V, k, deltas


def qtab(P, R, V, g=0.9):
    return (P * R).sum(2) + g * P @ V


def pi_solve(P, R, g=0.9):
    e = (P * R).sum(2); n = P.shape[1]
    pol = np.zeros(n, int); it = 0; starts = []
    while True:
        it += 1
        Pp = P[pol, np.arange(n)]; rp = e[pol, np.arange(n)]
        V = np.linalg.solve(np.eye(n) - g * Pp, rp); starts.append(V[IX['r4c1']])
        Q = e + g * P @ V
        best = Q.max(0)
        new = np.array([pol[s] if Q[pol[s], s] > best[s] - 1e-9 else int(np.flatnonzero(Q[:, s] > best[s] - 1e-9)[0]) for s in range(n)])
        if (new == pol).all():
            return V, pol, it, starts
        pol = new


def run_code(w):
    def cases(src):
        ns = {'__name__': '__main__', '__learner_source__': src}
        if w.get('prelude'):
            exec(w['prelude'], ns)
        exec(src, ns)
        out = []
        for c in w['examples'] + w['tests']:
            if c.get('setup'):
                exec(c['setup'], ns)
            got, exp = eval(c['call'], ns), eval(c['expect'], dict(ns))
            tol = c.get('tol', {})
            if c.get('compare') == 'isclose':
                def close(a, b):
                    if hasattr(a, 'tolist'): a = a.tolist()
                    if isinstance(a, dict): return set(a) == set(b) and all(close(a[k], b[k]) for k in a)
                    if isinstance(a, (list, tuple)): return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
                    return math.isclose(float(a), float(b), rel_tol=tol.get('rel', 0 if tol else 1e-9), abs_tol=tol.get('abs', 0 if tol else 1e-12))
                out.append(close(got, exp))
            else:
                out.append(got == exp if not isinstance(got, tuple) else list(got) == list(exp))
        return out
    good = all(cases(w['solution']))
    try:
        sf = not all(cases(w['starter'])[len(w['examples']):])
    except Exception:
        sf = True
    return good, sf


def code(ref, path):
    w = J(ref, path)
    good, sf = run_code(w)
    C(good, f'{ref} {path}: solution passes every case'); C(sf, f'{ref} {path}: starter fails a hidden test')
    return w


PS, RS = arrays(0.1); PD, RD = arrays(0.0)
VS, kS10, dS = vi(PS, RS); VD, kD10, dD = vi(PD, RD)
_, kS6, _ = vi(PS, RS, tol=1e-6); _, kD6, _ = vi(PD, RD, tol=1e-6)
VSp, polS, itS, startsS = pi_solve(PS, RS); VDp, polD, itD, _ = pi_solve(PD, RD)
C((kS6, kS10, kD6) == (25, 38, 8), f'sweeps {kS6}, {kS10}, {kD6}')
C(np.max(np.abs(VS - VSp)) < 1e-9 and np.max(np.abs(VD - VDp)) < 1e-9, 'value iteration agrees with policy iteration\'s solve')
C((itS, itD) == (4, 5), f'policy iteration evaluations {itS} slippery, {itD} deterministic')
# deterministic closed form over BFS distances to the +1 avoiding the pit
dist = {'r1c5': 0}; dq = deque(['r1c5'])
while dq:
    t = dq.popleft()
    for s in CELLS:
        if s not in END and s not in dist and any(nxt(s, a) == t for a in ACTS):
            dist[s] = dist[t] + 1; dq.append(s)
Vd = lambda d: 0.9 ** (d - 1) - 0.4 * (1 - 0.9 ** d)
C(all(abs(VD[IX[s]] - Vd(dist[s])) < 1e-12 for s in CELLS if s not in END), 'deterministic values equal V(d)')
C([round(Vd(d), 4) for d in range(1, 8)] == [0.96, 0.824, 0.7016, 0.5914, 0.4923, 0.4031, 0.3228], 'V(1..7)')
table = {'r1c1': 0.4502, 'r1c2': 0.5800, 'r1c3': 0.7323, 'r1c4': 0.8896, 'r2c1': 0.3568, 'r2c2': 0.4502, 'r2c4': 0.5500, 'r3c1': 0.2714, 'r3c2': 0.3348,
         'r3c3': 0.2915, 'r3c4': 0.3969, 'r3c5': 0.1634, 'r4c1': 0.1944, 'r4c2': 0.2381, 'r4c3': 0.2168, 'r4c4': 0.2830, 'r4c5': 0.1961}
C(all(round(VS[IX[s]], 4) == v for s, v in table.items()), 'slippery value table matches the brief')
Q = qtab(PS, RS, VS)
gS = {s: ACTS[int(np.argmax(Q[:, IX[s]]))] for s in table}
C(gS['r3c5'] == 'L' and gS['r4c5'] == 'L' and gS['r3c3'] == 'R', 'slippery: r3c5 and r4c5 go L')
# every value shown on a slippery grid canvas is the table value
cells = J('l6', 'screens[2].canvas.params.cells')
C(all(cells[int(s[1]) - 1][int(s[3]) - 1] == f'{v:.4f}' for s, v in table.items()), 'l6 grid canvas shows the slippery table')
Vr = {s: round(VS[IX[s]], 4) for s in CELLS}


def qv(V, s, a, slip, step=-0.04, g=0.9):
    tot = 0.0
    for b, p in ((a, 1 - 2 * slip), (SIDE[a][0], slip), (SIDE[a][1], slip)):
        if p > 0:
            t = nxt(s, b); tot += p * (END.get(t, 0.0) + step + g * (0 if t in END else V[t]))
    return tot


# ================= l5 =================
V = 0.0
for _ in range(500):
    V = sum(max(x, 0.9 * V) for x in range(1, 7)) / 6
C(abs(V - 55 / 12) < 1e-12 and F(11, 6) / F(2, 5) == F(55, 12), 'dice game 55/12 by iteration and by the threshold equation')
E('l5', 'screens[0].widget.answer', round(55 / 12, 4)); E('l5', 'screens[0].widget.wrong[2].value', round(11 / 6, 4))
thr = {k: (sum(range(k, 7)) / 6) / (1 - 0.9 * (k - 1) / 6) for k in range(1, 7)}
for k, v in thr.items():
    E('l5', 'screens[1].explain.text', round(v, 2))
E('l5', 'screens[1].explain.text', round(0.9 * 55 / 12, 3))
E('l5', 'screens[2].widget.answer', 17); C(len([s for s in CELLS if s not in END]) == 17, '17 decision states')
E('l5', 'screens[4].widget.answer', round(-0.04 - 0.9 * 0.04 + 0.81 * 0.96, 4)); E('l5', 'screens[4].widget.wrong[2].value', round(0.9 * (-0.04) + 0.81 * (-0.04) + 0.729 * 0.96, 4))
E('l5', 'screens[5].widget.answer', round(0.9 ** 10, 4)); E('l5', 'screens[5].widget.wrong[1].value', round(0.9 ** 9, 4)); E('l5', 'screens[5].widget.wrong[2].value', round(0.9 ** 11, 4))
g3 = -0.04 + 0.9 * -0.04 + 0.81 * 0.96
E('l5', 'screens[6].widget.answer', round(g3, 4)); C(round(Vd(3), 4) == round(g3, 4), 'l5 bump trap: the 3-move return equals the value three moves from the goal (0.7016)')
E('l5', 'screens[6].widget.wrong[0].value', round(-0.04 + 0.9 * 0.96, 4)); E('l5', 'screens[6].widget.wrong[1].value', round(0.9 * -0.04 + 0.81 * 0.96, 4)); E('l5', 'screens[6].widget.wrong[2].value', 0.81)
code('l5', 'screens[7].widget')
E('l5', 'screens[8].widget.answer', 1 / (1 - 0.9)); E('l5', 'screens[8].widget.wrong[0].value', 0.9 / (1 - 0.9))
E('l5', 'quiz[0].widget.answer', -1 - 0.5 + 0.25 * 10); E('l5', 'quiz[2].explain.text', 4.125)

# ================= l6 =================
a, b, c, d = 1 - 0.72, -0.18, -0.36, 1 - 0.54
det = a * d - b * c
vC, vB = (d * 1 - b * 3) / det, (a * 3 - c * 1) / det
C(abs(vC - 15.625) < 1e-12 and abs(vB - 18.75) < 1e-12 and abs(det - 0.064) < 1e-12, 'Calm 15.625, Busy 18.75 (Cramer)')
E('l6', 'screens[0].widget.answer', 15.625); E('l6', 'screens[0].widget.wrong[1].value', round(0.9 * 15.625, 4))
v99 = np.linalg.solve(np.eye(2) - 0.99 * np.array([[0.8, 0.2], [0.4, 0.6]]), [1, 3])
E('l6', 'screens[1].explain.text', round(v99[0], 2)); E('l6', 'screens[1].explain.text', round(v99[1], 2)); E('l6', 'screens[1].explain.text', round(5 / 3, 2))
bk = 0.8 * 0.96 + 0.1 * (-0.04 + 0.9 * 0.8896) + 0.1 * (-0.04 + 0.9 * 0.55)
E('l6', 'screens[2].widget.answer', round(bk, 4)); C(round(bk, 4) == 0.8896, 'Bellman check at r1c4 reproduces 0.8896')
upr = {s: ('R' if s.startswith('r1') else 'U') for s in CELLS if s not in END}
pol_idx = np.array([0 if s in END else ACTS.index(upr[s]) for s in CELLS])
e = (PD * RD).sum(2); vupr = np.linalg.solve(np.eye(19) - 0.9 * PD[pol_idx, np.arange(19)], e[pol_idx, np.arange(19)])
C(abs(vupr[IX['r4c1']] - Vd(7)) < 1e-12 and abs(vupr[IX['r3c3']] + 0.4) < 1e-12 and abs(vupr[IX['r4c3']] + 0.4) < 1e-12, 'up-then-right: start V(7), wall loop -0.4')
E('l6', 'screens[3].widget.answer', round(Vd(7), 4)); E('l6', 'screens[3].widget.wrong[2].value', round(0.9 ** 6, 4))
E('l6', 'screens[4].widget.answer', -0.04 / 0.1)
k = math.ceil(math.log(1e-6) / math.log(0.9)); C(0.9 ** k <= 1e-6 < 0.9 ** (k - 1), f'{k} sweeps for a millionth')
E('l6', 'screens[5].widget.answer', k); E('l6', 'screens[5].hints[2].text', round(math.log(1e-6) / math.log(0.9), 1))
E('l6', 'screens[6].explain.text', round(0.9 * 15.625, 4))
code('l6', 'screens[7].widget')
for i, v in enumerate((Vd(7), VS[IX['r4c1']], VD[IX['r4c1']])):
    E('l6', f'screens[7].canvas.params.rows[{i}][2]', round(v, 4))
vm = np.linalg.solve(np.eye(2) - 0.95 * np.array([[0.75, 0.25], [0.5, 0.5]]), [4, 1])
detm = 0.2875 * 0.525 - 0.2375 * 0.475
C(abs(vm[0] - (0.525 * 4 + 0.2375) / detm) < 1e-9, f'quoting rule flat {vm[0]:.4f} by both routes')
E('l6', 'screens[9].widget.answer', round(vm[0], 2)); E('l6', 'screens[9].widget.wrong[0].value', round(vm[1], 2)); E('l6', 'screens[9].widget.wrong[1].value', 80)
E('l6', 'quiz[0].widget.answer', 2 / (1 - 0.8)); E('l6', 'quiz[1].widget.answer', 1 + 0.9 * 3)

# ================= l7 =================
E('l7', 'screens[0].widget.answer', 0.96)
Vk = np.zeros(19); first_pos = None
for kk in range(1, 9):
    Vk = (e + 0.9 * PD @ Vk).max(0)
    if first_pos is None and Vk[IX['r4c1']] > 0: first_pos = kk
C(first_pos == 7, 'start turns positive on sweep 7'); E('l7', 'screens[1].widget.answer', 7)
E('l7', 'screens[2].widget.answer', round(0.8 * 0.96 + 0.2 * -0.04, 2))
qu = qv(Vr, 'r3c5', 'U', 0.1); ql = qv(Vr, 'r3c5', 'L', 0.1)
C(round(ql, 4) == 0.1634 and qu < ql, 'r3c5: L beats U'); E('l7', 'screens[3].widget.answer', round(qu, 4))
C(abs(dS[23] - 1.3353e-6) < 1e-9 and dS[24] < 1e-6 <= dS[23], 'slippery change first below 1e-6 on sweep 25')
C(all(abs(dD[i] - 0.96 * 0.9 ** i) < 1e-12 for i in range(7)) and dD[7] == 0, 'deterministic changes 0.96 * 0.9^(k-1), then 0 at sweep 8')
E('l7', 'screens[4].widget.answer', 25); kb = next(k for k in range(1, 400) if 0.9 ** k <= 1e-6)
C(kb == 132 == math.ceil(math.log(1e-6) / math.log(0.9)) and 0.96 * 0.9 ** 130 > 1e-6 >= 0.96 * 0.9 ** 131, 'l7 bound: 0.9^k <= 1e-6 first at k = 132 (and the dashed bound 0.96 x 0.9^(k-1) first below at 132)')
E('l7', 'screens[4].widget.wrong[1].value', kb)
pts = J('l7', 'screens[4].canvas.params.functions[1].points')
C(len(pts) == 25 and all(abs(p[1] - dS[i]) < 1e-12 for i, p in enumerate(pts)), 'chart points are the slippery changes')
dv = [0.0]
for _ in range(5):
    dv.append(sum(max(x, 0.9 * dv[-1]) for x in range(1, 7)) / 6)
C(abs(dv[2] - (15 + 3 * 3.15) / 6) < 1e-12, 'second dice sweep 4.075'); E('l7', 'screens[5].widget.answer', round(dv[2], 3))
for v in (dv[3], dv[4], dv[5]):
    E('l7', 'screens[5].explain.text', round(v, 3))
Vg = np.zeros(19); kg = 0
while True:
    kg += 1; dmax = 0
    for i, s in enumerate(CELLS):
        if s in END: continue
        n = max((PS[ai, i] * (RS[ai, i] + 0.9 * Vg)).sum() for ai in range(4)); dmax = max(dmax, abs(n - Vg[i])); Vg[i] = n
    if dmax < 1e-6: break
C(np.max(np.abs(Vg - VS)) < 1e-5, f'Gauss-Seidel reaches the same values in {kg} sweeps'); E('l7', 'screens[6].explain.text', kg)
code('l7', 'screens[7].widget')
QD = qtab(PD, RD, VD)
C({ACTS[a] for a in np.flatnonzero(QD[:, IX['r4c1']] > QD[:, IX['r4c1']].max() - 1e-9)} == {'U', 'R'}, 'r4c1 ties U and R')
E('l7', 'screens[8].feedback.correct', round(Vd(6), 4))
E('l7', 'screens[9].widget.options[0].text', round(0.9 ** 50, 4))
E('l7', 'screens[10].widget.answer', max(8, 0.99 * (4.10 + 11.80) / 2)); E('l7', 'screens[10].feedback.correct', round(0.99 * 7.95, 4))
E('l7', 'quiz[0].widget.answer', round(-0.04 + 0.9 * 0.5914, 4))
kq = next(k for k in range(1, 100) if 2 * 0.5 ** k < 0.001); E('l7', 'quiz[1].widget.answer', kq)

# ================= l8 =================
up = np.zeros(19, int)
vup = np.linalg.solve(np.eye(19) - 0.9 * PS[up, np.arange(19)], (PS * RS).sum(2)[up, np.arange(19)])
vupr = {s: round(vup[IX[s]], 4) for s in CELLS}
qR = qv(vupr, 'r4c1', 'R', 0.1)
C(round(vup[IX['r4c1']], 4) == -0.3686 and round(qR, 4) == -0.3573, 'always up: start -0.3686; R scores -0.3573')
E('l8', 'screens[0].widget.answer', round(qR, 4))
C([round(x, 4) for x in startsS] == [-0.3686, 0.0845, 0.1943, 0.1944], f'policy iteration start values {startsS}')
E('l8', 'screens[1].hints[2].text', 0.1943); E('l8', 'screens[1].widget.answer', itS)
E('l8', 'screens[2].widget.answer', round(startsS[1] - startsS[0], 3)); E('l8', 'screens[2].explain.text', round(qR + 0.3686, 4))
GD = np.argmax(QD, 0)
diff = [s for s in CELLS if s not in END and GD[IX[s]] != polD[IX[s]]]
C(len(diff) == 7 and np.max(np.abs(VD - VDp)) < 1e-14, f'policies differ in {len(diff)} cells, values agree')
E('l8', 'screens[4].prose', 7)
P2, R2 = arrays(0.2); V2, _, _ = vi(P2, R2); Q2 = qtab(P2, R2, V2)
C(ACTS[int(np.argmax(Q2[:, IX['r2c4']]))] == 'L', 'slip 0.2: r2c4 chooses L'); E('l8', 'screens[6].explain.text', round(V2[IX['r2c4']], 4))
P0, R0 = arrays(0.1, step=0.0); V0, _, _ = vi(P0, R0); C(ACTS[int(np.argmax(qtab(P0, R0, V0)[:, IX['r3c5']]))] == 'D', 'step cost 0: r3c5 chooses D')
qsk = 0.5 + 0.95 * (0.8 * vm[0] + 0.2 * vm[1]); E('l8', 'screens[8].widget.answer', round(qsk, 2)); C(qsk > vm[1], 'skewing improves the limit state')
code('l8', 'screens[5].widget')

# ================= review-2 =================
b22 = qv(Vr, 'r2c2', 'U', 0.1); E('review', 'items[0].widget.answer', round(b22, 4)); C(round(b22, 4) == 0.4502, 'r2c2 backup is its own value')
v2 = np.linalg.solve(np.eye(2) - 0.8 * np.array([[0.9, 0.1], [0.5, 0.5]]), [0, 10]); C(abs(v2[1] - 3.5 * v2[0]) < 1e-9, 'v_Y = 3.5 v_X')
E('review', 'items[1].widget.answer', round(v2[0], 2)); E('review', 'items[1].widget.wrong[0].value', round(v2[1], 2))
E('review', 'items[2].widget.answer', math.ceil(math.log(0.001) / math.log(0.95)))
E('review', 'items[4].widget.answer', round(-2.71 + 0.729 * 20, 2))
d8 = {k: (sum(range(k, 7)) / 6) / (1 - 0.8 * (k - 1) / 6) for k in range(1, 7)}
C(max(d8, key=d8.get) == 4, 'gamma 0.8: keep 4 and up'); E('review', 'items[5].widget.answer', round(d8[4], 4)); E('review', 'items[5].widget.wrong[0].value', round(d8[5], 4))
E('review', 'items[6].widget.answer', -0.1 / 0.05)

# ================= homework-2 =================
code('homework', 'items[0].widget'); w2 = code('homework', 'items[1].widget')
Vk = np.zeros(19); first = None
for i in range(10):
    n = (e_s := (PS * RS).sum(2)) + 0.9 * PS @ Vk
    n = n.max(0)
    if first is None: first = np.max(np.abs(n - Vk))
    Vk = n
bound = 0.9 ** 10 * first / 0.1
C(abs(first - 0.76) < 1e-12 and np.max(np.abs(Vk - VS)) <= bound, f'bound after 10 sweeps {bound:.4f} covers the error {np.max(np.abs(Vk - VS)):.4f}')
E('homework', 'items[1].feedback.correct', round(bound, 4)); E('homework', 'items[1].feedback.correct', round(np.max(np.abs(Vk - VS)), 4))
kc = math.ceil(math.log(1e-4 * 0.1 / 0.96) / math.log(0.9)); E('homework', 'items[3].widget.answer', kc)
C(0.9 ** kc * 9.6 <= 1e-4 < 0.9 ** (kc - 1) * 9.6, f'{kc} sweeps for the certificate')

# ================= problems-2 =================
vh = np.linalg.solve(np.eye(2) - 0.9 * np.array([[0.5, 0.5], [0.6, 0.4]]), [1, 4])
C(abs(vh[0] - 2.44 / 0.109) < 1e-9, 'hold policy by Cramer'); E('problems', 'items[0].parts[0].widget.answer', round(vh[0], 2))
E('problems', 'items[0].parts[1].widget.answer', round(0.9 * round(vh[1], 2), 2))
vp = np.linalg.solve(np.eye(2) - 0.9 * np.array([[0, 1], [0.6, 0.4]]), [0, 4]); C(abs(vp[1] - 4 / 0.154) < 1e-9 and vp[0] > vh[0], 'push policy improves A')
E('problems', 'items[0].parts[3].widget.answer', round(vp[0], 2))
q13 = {a: qv(Vr, 'r1c3', a, 0.1) for a in ACTS}
E('problems', 'items[1].parts[0].widget.answer', round(q13['R'], 4)); E('problems', 'items[1].parts[1].widget.answer', round(q13['L'], 4))
E('problems', 'items[1].parts[2].widget.answer', round(q13['R'] - max(q13['U'], q13['D'], q13['L']), 4)); C(abs(q13['U'] - q13['D']) < 1e-12, 'U and D tie at r1c3')
E('problems', 'items[2].parts[0].widget.answer', round(2.5 / 0.6, 4)); E('problems', 'items[2].parts[1].widget.answer', round(0.8 * 2.5 / 0.6, 4))

lv.check_wrongs()
lv.report()
