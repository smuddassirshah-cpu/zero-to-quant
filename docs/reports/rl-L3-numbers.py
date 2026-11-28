"""Recompute every number stated in rl level 3 (TD and Q-learning) and check it at its JSON path.

Run: <venv>/bin/python docs/reports/rl-L3-numbers.py   (NumPy and the standard library; about 15 s; exits 0 when every check passes)

Two routes per number. The random walk's values by a linear solve and by the closed form k/6. Seeded learners (TD, MC,
Q-learning, SARSA) are re-implemented here as online loops (an update right after each step, not after the episode is
generated, which uses the same random draws); they must reproduce the curves, counts and figures the lessons state, and
every code widget's solution is run against its tests in CPython with its starter failing one. Value iteration for the
optimal sets is rebuilt on arrays. Hand updates are recomputed in fractions where they are exact.
"""
import math, os, random, statistics as st, sys
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level('rl', 3)
E, C = lv.expect, lv.claim


def J(ref, path):
    _, doc = lv._file(ref)
    node = doc
    for part in path.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.lstrip('-').isdigit() else node[part]
    return node


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
                    if isinstance(a, dict): return set(a) == set(b) and all(close(a[k], b[k]) for k in a)
                    if isinstance(a, (list, tuple)): return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
                    return math.isclose(float(a), float(b), rel_tol=tol.get('rel', 0 if tol else 1e-9), abs_tol=tol.get('abs', 0 if tol else 1e-12))
                out.append(close(got, exp))
            else:
                out.append(list(got) == list(exp) if isinstance(got, tuple) else got == exp)
        return out
    good = all(cases(w['solution']))
    try:
        sf = not all(cases(w['starter'])[len(w['examples']):])
    except Exception:
        sf = True
    return good, sf


def code(ref, path):
    w = J(ref, path); good, sf = run_code(w)
    C(good, f'{ref} {path}: solution passes every case'); C(sf, f'{ref} {path}: starter fails a hidden test')


# ---------- random walk ----------
A = np.eye(5) - 0.5 * (np.eye(5, k=1) + np.eye(5, k=-1)); b = np.zeros(5); b[4] = 0.5
v = np.linalg.solve(A, b); TRUE = [k / 6 for k in range(1, 6)]
C(np.allclose(v, TRUE, atol=1e-12), 'random walk values k/6 by a linear solve')


def walk_online(alpha, seed, method, episodes=100):
    rng = random.Random(seed); V = [0.5] * 5; out = [math.sqrt(sum((x - t) ** 2 for x, t in zip(V, TRUE)) / 5)]
    for _ in range(episodes):
        s, visited = 2, []
        while True:
            s2 = s + (1 if rng.random() < 0.5 else -1)
            r = 1 if s2 == 5 else 0
            done = s2 in (-1, 5)
            if method == 'td':
                V[s] += alpha * ((r if done else r + V[s2]) - V[s])
            visited.append(s)
            if done:
                if method == 'mc':
                    for x in visited:
                        V[x] += alpha * (r - V[x])
                break
            s = s2
        out.append(math.sqrt(sum((x - t) ** 2 for x, t in zip(V, TRUE)) / 5))
    return out


def mean_curve(alpha, method, seeds=100):
    cs = [walk_online(alpha, s, method) for s in range(seeds)]
    return [sum(c[i] for c in cs) / seeds for i in range(101)]


T05, T1, T5 = mean_curve(0.05, 'td'), mean_curve(0.1, 'td'), mean_curve(0.5, 'td')
M01, M02 = mean_curve(0.01, 'mc'), mean_curve(0.02, 'mc')
for c, ref in ((T05, 'td05'), (T1, 'td1'), (M01, 'mc01'), (M02, 'mc02')):
    ser = next(x for x in J('l10', 'screens[1].canvas.params.series') if x['id'] == ref)
    C(all(abs(a - b) < 6e-5 for a, b in zip(ser['values'], c)), f'l10 curve {ref} reproduced online')
for c in (T1, T05, M02, M01):
    E('l10', 'screens[1].explain.text', round(c[25], 4))
C(T1[25] < T05[25] < M02[25] < M01[25] and all(T1[i] < M02[i] for i in range(20, 101)), 'TD below MC from 20 episodes on')
E('l10', 'screens[5].canvas.params.rows[0][1]', round(T1[25], 4)); E('l10', 'screens[5].canvas.params.rows[1][2]', round(M02[100], 4))
E('l10', 'screens[6].prose', round(T5[10], 4)); E('l10', 'screens[6].prose', round(T5[100], 4)); C(T5[100] > T5[10], 'alpha 0.5 does not improve after 10 episodes')
m20 = st.mean(walk_online(0.1, s, 'td')[-1] for s in range(20)); E('l10', 'screens[4].canvas.params.rows[2][1]', round(m20, 4))
C(m20 < 0.09, 'seeds 0-19 mean RMS below the test threshold')
E('l10', 'screens[3].widget.answer', round(float(F(1, 6) ** 2), 4)); E('l10', 'screens[0].widget.answer', 0.5 + 0.1 * (0.7 - 0.5))
E('l10', 'screens[8].widget.answer', round(101.20 + 0.1 * 0.30, 2)); E('l10', 'quiz[0].widget.answer', 2 + 0.5 * (1 + 0.9 * 3 - 2))
code('l10', 'screens[4].widget')

# ---------- l9 ----------
eps = [(['B', 'C'], [-1, 9]), (['B', 'A', 'B', 'C'], [-1, -1, -1, 9]), (['B', 'A'], [-1, -1])]
def G(rw, g):
    out, acc = [], 0.0
    for i in range(len(rw) - 1, -1, -1):
        acc = rw[i] + g * acc; out.insert(0, acc)
    return out
fv = {}
for states, rw in eps:
    for s in dict.fromkeys(states):
        fv.setdefault(s, []).append(G(rw, 1)[states.index(s)])
C({s: sum(x) / len(x) for s, x in fv.items()} == {'B': 4, 'C': 9, 'A': 3}, 'corridor first-visit estimates 4, 9, 3')
E('l9', 'screens[0].widget.answer', 4); E('l9', 'screens[7].widget.answer', 3); E('l9', 'screens[0].widget.wrong[1].value', round(8 / 3, 4))
E('l9', 'screens[3].widget.answer', round(G([-1, -1, -1, 9], 0.9)[0], 3)); E('l9', 'screens[3].canvas.params.rows[2][2]', round(G([-1, -1, -1, 9], 0.9)[1], 2))
E('l9', 'screens[2].widget.answer', round(TRUE[1], 4)); E('l9', 'screens[5].widget.answer', 0.5 / math.sqrt(100))
rng = random.Random(7); seen = set()
for _ in range(3):
    s = 2
    while 0 <= s <= 4:
        seen.add(s); s += 1 if rng.random() < 0.5 else -1
C(0 not in seen and 4 in seen, 'seed 7: A unvisited after 3 episodes')
E('l9', 'screens[9].widget.answer', round((3.2 - 1.4 + 0.6 + 2.0) / 4, 2)); E('l9', 'quiz[2].widget.answer', (2 / 0.1) ** 2)
code('l9', 'screens[4].widget')

# ---------- gridworld Q-learning ----------
CELLS = [f'r{r}c{c}' for r in range(1, 5) for c in range(1, 6) if (r, c) != (2, 3)]
END = {'r1c5': 1.0, 'r2c5': -1.0}; OPEN = [s for s in CELLS if s not in END]
D = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
def mv(s, a):
    r, c = int(s[1]) + D[a][0], int(s[3]) + D[a][1]; t = f'r{r}c{c}'
    return t if 1 <= r <= 4 and 1 <= c <= 5 and t != 'r2c3' else s
SIDE = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
def trans(s, a, slip):
    out = {}
    for bb, p in ((a, 1 - 2 * slip), (SIDE[a][0], slip), (SIDE[a][1], slip)):
        if p > 0:
            t = mv(s, bb); out[t] = out.get(t, 0) + p
    return out
def vi(slip):
    V = {s: 0.0 for s in CELLS}
    for _ in range(2000):
        V = {s: 0.0 if s in END else max(sum(p * (END.get(t, 0) - 0.04 + 0.9 * V[t]) for t, p in trans(s, a, slip).items()) for a in 'URDL') for s in CELLS}
    return V
def osets(V, slip):
    out = {}
    for s in OPEN:
        q = {a: sum(p * (END.get(t, 0) - 0.04 + 0.9 * V[t]) for t, p in trans(s, a, slip).items()) for a in 'URDL'}
        out[s] = {a for a in q if q[a] > max(q.values()) - 1e-9}
    return out
VD = vi(0.0); SD = osets(VD, 0.0); VS = vi(0.1); SS = osets(VS, 0.1)


class QAgent:
    def __init__(self, seed, alpha=0.1, eps=0.2, slip=0.0):
        self.rng, self.alpha, self.eps, self.slip = random.Random(seed), alpha, eps, slip
        self.Q = {(s, a): 0.0 for s in CELLS for a in 'URDL'}; self.steps = 0

    def episode(self, start=None):
        s = start or self.rng.choice(OPEN)
        while s not in END:
            a = self.rng.choice('URDL') if self.rng.random() < self.eps else max('URDL', key=lambda x: self.Q[(s, x)])
            if self.slip:
                u, acc = self.rng.random(), 0.0
                for t, p in trans(s, a, self.slip).items():
                    acc += p
                    if u < acc: break
            else:
                t = mv(s, a)
            r = END.get(t, 0.0) - 0.04
            tgt = r if t in END else r + 0.9 * max(self.Q[(t, x)] for x in 'URDL')
            self.Q[(s, a)] += self.alpha * (tgt - self.Q[(s, a)]); s = t; self.steps += 1

    def good(self, sets):
        return all(max('URDL', key=lambda x: self.Q[(s, x)]) in sets[s] for s in OPEN)


def train(seed, n, **kw):
    ag = QAgent(seed, **kw)
    for _ in range(n): ag.episode()
    return ag
r500 = [train(s, 500) for s in range(50)]
C(sum(a.good(SD) for a in r500) == 50 and sum(train(s, 200).good(SD) for s in range(50)) == 50, '50 of 50 seeds optimal at 200 and 500 episodes')
mean_steps = sum(a.steps for a in r500) / 50; C(2900 <= mean_steps <= 3000, f'about 2,900 steps: {mean_steps:.1f}')
E('l11', 'screens[5].canvas.params.rows[1][1]', round(mean_steps)); E('l11', 'screens[5].canvas.params.rows[0][1]', 50)
a50 = train(0, 50); bad = [s for s in OPEN if max('URDL', key=lambda x: a50.Q[(s, x)]) not in SD[s]]
C(bad == ['r4c1', 'r4c2', 'r4c3'], 'seed 0 at 50 episodes: three bottom-row cells wrong'); E('l11', 'screens[1].widget.answer', len(bad))
heat = J('l11', 'screens[3].canvas.params.matrices[0].rows')
C(all(abs(heat[i][j] - a50.Q[(f'r4c{i + 1}', 'URDL'[j])]) < 6e-5 for i in range(5) for j in range(4)), 'Q-table heat matrix reproduced')
a2k = train(0, 2000); mq = max(a2k.Q[('r4c1', x)] for x in 'URDL')
C(abs(mq - VD['r4c1']) < 1e-4 and round(VD['r4c1'], 4) == 0.3228, f'max Q at the start after 2,000 episodes {mq:.5f}'); E('l11', 'screens[5].canvas.params.rows[2][1]', round(mq, 4))
E('l11', 'screens[1].explain.text', round(max(r500[0].Q[('r4c1', x)] for x in 'URDL'), 4))
fixed = QAgent(0); fixed.episode('r4c1')
unt = [s for s in OPEN if all(fixed.Q[(s, x)] == 0 for x in 'URDL')]
C(len(unt) == 10, 'fixed start: 10 cells untouched after one episode'); E('l11', 'screens[4].widget.answer', 10)
fx4 = QAgent(0)
for _ in range(4): fx4.episode('r4c1')
fx3 = QAgent(0)
for _ in range(3): fx3.episode('r4c1')
C(not [s for s in OPEN if all(fx4.Q[(s, x)] == 0 for x in 'URDL')] and [s for s in OPEN if all(fx3.Q[(s, x)] == 0 for x in 'URDL')], 'every cell touched first after 4 episodes')
E('l11', 'screens[4].explain.text', 4)
E('l11', 'screens[0].widget.answer', 0.1 * 0.96); E('l11', 'screens[2].widget.answer', round(0.2 + 0.1 * (-0.04 + 0.45 - 0.2), 3))
E('l11', 'screens[10].widget.answer', round(0.2 * (0.5 + 0.95 * 2), 2)); E('l11', 'quiz[0].widget.answer', 0.5 + 0.8 * 3)
slip = {}
for seed in range(10):
    ag = QAgent(seed, eps=0.1, slip=0.1); hit = None
    for ep in range(1, 20001):
        ag.episode()
        if ep % 50 == 0 and ag.good(SS):
            hit = ep; break
    slip[seed] = hit
fails = [s for s, h in slip.items() if h is None]; ok = [h for h in slip.values() if h]
C(len(fails) == 2 and (min(ok), max(ok)) == (4400, 15250), f'slippery: {len(fails)} of 10 fail, others {min(ok)} to {max(ok)}')
E('l11', 'screens[8].prose', 4400); E('l11', 'screens[8].prose', 15250)
gaps = {}
for s in OPEN:
    q = sorted(sum(p * (END.get(t, 0) - 0.04 + 0.9 * VS[t]) for t, p in trans(s, a, 0.1).items()) for a in 'URDL'); gaps[s] = q[-1] - q[-2]
C(round(gaps['r4c3'], 4) == 0.0073 and round(gaps['r2c1'], 4) == 0.0077 and sum(g < 0.01 for g in gaps.values()) == 2, 'gaps under 0.01: r4c3 0.0073, r2c1 0.0077')
E('l11', 'screens[8].prose', 0.0073)
code('l11', 'screens[5].widget')

# ---------- cliff ----------
def cliff(agent, seed, episodes=500, alpha=0.5, eps=0.1):
    rng = random.Random(seed); Q = {}
    q = lambda s, a: Q.get((s, a), 0.0)
    def pick(s):
        return rng.choice('URDL') if rng.random() < eps else max('URDL', key=lambda a: q(s, a))
    tots = []
    for _ in range(episodes):
        s = (4, 1); a = pick(s); tot = 0
        while s != (4, 8):
            r_, c_ = min(max(s[0] + D[a][0], 1), 4), min(max(s[1] + D[a][1], 1), 8)
            if r_ == 4 and 2 <= c_ <= 7:
                s2, rew = (4, 1), -100
            else:
                s2, rew = (r_, c_), -1
            tot += rew
            if s2 == (4, 8):
                Q[(s, a)] = q(s, a) + alpha * (rew - q(s, a)); s = s2; break
            a2 = pick(s2)
            nxt = q(s2, a2) if agent == 'sarsa' else max(q(s2, x) for x in 'URDL')
            Q[(s, a)] = q(s, a) + alpha * (rew + nxt - q(s, a)); s, a = s2, a2
        tots.append(tot)
    return tots, Q
SA = [cliff('sarsa', s)[0] for s in range(20)]; QL = [cliff('q', s)[0] for s in range(20)]
ms, mq_ = st.mean(sum(t[-100:]) / 100 for t in SA), st.mean(sum(t[-100:]) / 100 for t in QL)
C(round(ms, 2) == -20.03 and round(mq_, 2) == -31.34, f'last 100 episodes: SARSA {ms:.2f}, Q {mq_:.2f}')
C(all(sum(a[-100:]) > sum(b[-100:]) for a, b in zip(SA, QL)), 'SARSA ahead on all 20 seeds')
E('l12', 'screens[1].explain.text', round(ms, 1)); E('l12', 'screens[1].explain.text', round(mq_, 1))
E('l12', 'screens[4].canvas.params.rows[0][1]', round(ms, 2)); E('l12', 'screens[4].canvas.params.rows[1][1]', round(mq_, 2))
blocks = [round(sum(sum(t[i:i + 10]) for t in SA) / 200, 1) for i in range(0, 500, 10)]
C(blocks == J('l12', 'screens[1].canvas.params.series[0].values'), 'SARSA block curve reproduced')
def gpath(Q):
    s, n = (4, 1), 0
    while s != (4, 8) and n < 40:
        a = max('URDL', key=lambda x: Q.get((s, x), 0.0)); r_, c_ = min(max(s[0] + D[a][0], 1), 4), min(max(s[1] + D[a][1], 1), 8)
        s = (4, 1) if (r_ == 4 and 2 <= c_ <= 7) else (r_, c_); n += 1
    return n
C(gpath(cliff('q', 0)[1]) == 9 and gpath(cliff('sarsa', 0)[1]) == 13, 'seed 0 greedy routes: Q 9 moves, SARSA 13')
E('l12', 'screens[0].widget.wrong[1].value', -13)
E('l12', 'screens[3].widget.answer', round(1 - 0.975 ** 6, 4)); E('l12', 'screens[2].widget.answer', -10 + 0.5 * (-1 - 12 + 10))
C(all(sum(cliff(ag, s, eps=0.0)[0][-100:]) / 100 == -9 for ag in ('sarsa', 'q') for s in range(5)), 'epsilon 0: both -9')
E('l12', 'screens[8].widget.answer', round(9 - 0.14 * 60, 2)); E('l12', 'quiz[2].widget.answer', round(1 - 0.95 ** 4, 4))
code('l12', 'screens[4].widget')

# ---------- review-3, homework-3, problems-3 ----------
E('review', 'items[0].widget.answer', (5 + 1 + 3) / 3); E('review', 'items[1].widget.answer', 1.0 + 0.2 * (0.4 + 0.9 * 2 - 1.0))
E('review', 'items[2].widget.answer', round(0.3 + 0.1 * (-0.04 + 0.9 * 0.5 - 0.3), 3)); E('review', 'items[3].widget.answer', -10 + 0.5 * (-61 + 10))
E('review', 'items[4].widget.answer', G([2, 0, -1, 4], 0.5)[0]); E('review', 'items[5].widget.answer', round((0.5 / 0.02) ** 2))
code('homework', 'items[0].widget'); code('homework', 'items[1].widget')
def tdd(episodes, seed):
    rng = random.Random(seed); V = [0.5] * 5; n = [0] * 5
    for _ in range(episodes):
        s = 2
        while True:
            s2 = s + (1 if rng.random() < 0.5 else -1); r = 1 if s2 == 5 else 0; done = s2 in (-1, 5)
            n[s] += 1; V[s] += ((r if done else r + V[s2]) - V[s]) / n[s]
            if done: break
            s = s2
    return V
m1000 = st.mean(math.sqrt(sum((x - t) ** 2 for x, t in zip(tdd(1000, s), TRUE)) / 5) for s in range(10))
E('homework', 'items[1].feedback.correct', round(m1000, 4)); C(m1000 < 0.045, 'decaying-step threshold holds')
E('homework', 'items[3].widget.answer', 0.5 * 0.96)
q2b = -0.02 + 0.5 * (-0.04 + 0.9 * 0.48 + 0.02)
E('problems', 'items[0].parts[0].widget.answer', 0.48); E('problems', 'items[0].parts[1].widget.answer', -0.02); E('problems', 'items[0].parts[2].widget.answer', round(q2b, 3))
E('problems', 'items[1].parts[0].widget.answer', 1 + 0.9 * 0.5); E('problems', 'items[1].parts[1].widget.answer', 1 + 0.9 * 3)
E('problems', 'items[1].parts[2].widget.answer', round(0.2 * (3.7 - 1.45), 2))
E('problems', 'items[2].parts[0].widget.answer', 0.5); E('problems', 'items[2].parts[1].widget.answer', round(0.4 + 0.1 * 0.3, 2))

lv.check_wrongs()
lv.report()
