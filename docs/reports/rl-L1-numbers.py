"""Recompute every number stated in rl level 1 (Bandits) and check it at its JSON path.

Run: <venv>/bin/python docs/reports/rl-L1-numbers.py   (NumPy, SciPy and the standard library; exits 0 when every check passes)

Two routes per number. Hand values come from closed forms here and from fractions. Seeded agents are re-implemented below,
independently of the lesson solutions (an Agent class with one step method), and must reproduce both the stated values and
every hidden-test `expect`; each code widget's `solution` is also run against its own tests in CPython, and its starter must
fail one. Recorded curves (200 seeds) are recomputed from the same re-implementation. Thompson's P(A beats B) is checked by
quadrature and by 10^6 NumPy draws.
"""
import math, os, random, sys
from fractions import Fraction as F

import numpy as np
from scipy import integrate, stats

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level('rl', 1)
E, C = lv.expect, lv.claim
PS = [0.45, 0.55, 0.60]


def J(ref, path):
    _, doc = lv._file(ref)
    node = doc
    for part in path.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.lstrip('-').isdigit() else node[part]
    return node


# ---------- an independent bandit implementation ----------
class Agent:
    def __init__(self, ps, seed, kind, eps=0.1, alpha=None, optimistic=False, c=None):
        self.ps, self.rng, self.kind, self.eps, self.alpha, self.c = ps, random.Random(seed), kind, eps, alpha, c
        k = len(ps)
        self.Q = [1.0] * k if optimistic else [0.0] * k
        self.n = [1] * k if optimistic else [0] * k
        self.pulls = [0] * k
        self.w, self.l = [0] * k, [0] * k
        self.t, self.total, self.cum = 0, 0, 0.0

    def tie(self):
        m = max(self.Q)
        return self.rng.choice([i for i, q in enumerate(self.Q) if q == m])

    def choose(self):
        k = len(self.ps)
        if self.kind == 'greedy':
            return self.tie()
        if self.kind == 'eps':
            return self.rng.randrange(k) if self.rng.random() < self.eps else self.tie()
        if self.kind == 'decay':
            return self.rng.randrange(k) if self.rng.random() < 1 / math.sqrt(self.t) else self.tie()
        if self.kind == 'ucb':
            if self.c is None:
                sc = [math.inf if self.pulls[i] == 0 else self.Q[i] + math.sqrt(2 * math.log(self.t) / self.pulls[i]) for i in range(k)]
            else:
                sc = [math.inf if self.pulls[i] == 0 else self.Q[i] + self.c * math.sqrt(math.log(self.t) / self.pulls[i]) for i in range(k)]
            return sc.index(max(sc))
        if self.kind == 'ts':
            d = [self.rng.betavariate(1 + self.w[i], 1 + self.l[i]) for i in range(k)]
            return d.index(max(d))

    def step(self, ps=None):
        self.t += 1
        a = self.choose()
        p = (ps or self.ps)[a]
        r = 1 if self.rng.random() < p else 0
        self.pulls[a] += 1; self.n[a] += 1
        if r: self.w[a] += 1
        else: self.l[a] += 1
        if self.alpha is None:
            self.Q[a] += (r - self.Q[a]) / self.n[a]      # the update the lessons specify, float for float
        else:
            self.Q[a] += self.alpha * (r - self.Q[a])
        self.total += r
        self.cum += max(self.ps) - self.ps[a]
        return r

    def run(self, T):
        for _ in range(T):
            self.step()
        return self


def regret_of(ps, counts):
    return sum(c * (max(ps) - p) for c, p in zip(counts, ps))


def mean_regret(kind, seeds=range(200), T=1000, **kw):
    return sum(Agent(PS, s, kind, **kw).run(T).cum for s in seeds) / len(seeds)


def run_code(w):
    """Run a code widget's solution against its examples and tests in CPython, and its starter; return (all pass, starter fails)."""
    def cases(src):
        ns = {'__name__': '__main__', '__learner_source__': src}
        exec(src, ns)
        out = []
        for c in w['examples'] + w['tests']:
            if c.get('setup'):
                exec(c['setup'], ns)
            got = eval(c['call'], ns)
            exp = eval(c['expect'], dict(ns))
            tol = c.get('tol', {})
            if c.get('compare') == 'isclose':
                def close(a, b):
                    if isinstance(a, dict): return set(a) == set(b) and all(close(a[k], b[k]) for k in a)
                    if isinstance(a, (list, tuple)): return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
                    return math.isclose(float(a), float(b), rel_tol=tol.get('rel', 1e-9 if not tol else 0), abs_tol=tol.get('abs', 1e-12 if not tol else 0))
                out.append(close(got, exp))
            else:
                out.append(list(got) == list(exp) if isinstance(got, tuple) and isinstance(exp, (tuple, list)) else got == exp)
        return out
    good = all(cases(w['solution']))
    try:
        starter_fails = not all(cases(w['starter'])[len(w['examples']):])
    except Exception:
        starter_fails = True
    return good, starter_fails


def check_code(ref, path):
    w = J(ref, path)
    good, sf = run_code(w)
    C(good, f'{ref} {path}: solution passes every case in CPython')
    C(sf, f'{ref} {path}: starter fails a hidden test')
    return w


def expect_of(w, call):
    for c in w['tests']:
        if c['call'] == call:
            return eval(c['expect'], {'math': math})
    raise KeyError(call)


# ================= l1 =================
# hook: seed 12, 30 orders round robin
rng = random.Random(12); w = [0, 0, 0]
for i in range(30):
    w[i % 3] += 1 if rng.random() < PS[i % 3] else 0
C(w == [7, 3, 5], 'l1 hook: 7, 3 and 5 fills of 10 (seed 12)')
fr = J('l1', 'screens[0].canvas.controls[0].frames')
C(fr[-1]['values'] == {'A': 0.7, 'B': 0.3, 'C': 0.5} and len(fr) == 11, 'l1 hook frames end at 0.7, 0.3, 0.5')
E('l1', 'screens[0].explain.text', 0.7); E('l1', 'screens[0].explain.text', 0.3)
E('l1', 'screens[1].widget.answer', 1000 * (0.60 - 0.45))
E('l1', 'screens[1].explain.text', 450); E('l1', 'screens[1].explain.text', 600)
E('l1', 'screens[1].widget.wrong[2].value', 1000 * (0.55 - 0.45))
rnd = float(1000 * (F(60, 100) - F(160, 300)))
C(abs(rnd - 66.6667) < 1e-4, 'random-play regret 66.67 (fractions)')
E('l1', 'screens[2].widget.answer', round(rnd, 2)); E('l1', 'screens[2].widget.wrong[0].value', round(1000 * 1.6 / 3, 2))
E('l1', 'screens[2].widget.wrong[1].value', 1000 * (0.6 - 0.5)); E('l1', 'screens[2].explain.text', 0.5333)
q = 0.0
for i, r in enumerate([1, 0, 1, 1], 1):
    q += (r - q) / i
C(abs(q - 0.75) < 1e-12 and abs(q - 3 / 4) < 1e-12, 'running mean of 1,0,1,1 is 0.75 both ways')
E('l1', 'screens[3].widget.rows[0][4].answer', 0.75); E('l1', 'screens[3].widget.rows[0][3].answer', round(1 - 2 / 3, 4))
E('l1', 'screens[3].widget.rows[0][4].wrong[1].value', round(2 / 3 + (1 - 2 / 3) / 3, 4))
w5 = check_code('l1', 'screens[4].widget')
r3 = random.Random(3)
C(expect_of(w5, '[pull(0.5, rng) for _ in range(8)]') == [1 if r3.random() < 0.5 else 0 for _ in range(8)], 'pull test list from seed 3')
E('l1', 'screens[4].explain.text', 45); C(abs(regret_of(PS, [200, 300, 500]) - 45) < 1e-9, '[200,300,500] regret 45')
C(abs(regret_of([0.2, 0.9, 0.5, 0.4], [10, 0, 5, 5]) - 11.5) < 1e-9, 'four-arm regret 11.5')
w6 = check_code('l1', 'screens[5].widget')
for s in (1, 0, 5, 6):
    a = Agent(PS, s, 'greedy').run(1000)
    C(tuple(expect_of(w6, f'run_greedy([0.45, 0.55, 0.6], 1000, {s})')) == (a.total, a.pulls), f'greedy seed {s} = ({a.total}, {a.pulls})')
g1, g0 = Agent(PS, 1, 'greedy').run(1000), Agent(PS, 0, 'greedy').run(1000)
E('l1', 'screens[5].explain.text', g1.total); C(g1.pulls == [1000, 0, 0] and g0.pulls == [0, 1000, 0], 'seed 1 all A, seed 0 all B')
E('l1', 'screens[6].canvas.state.caption', g0.total)
locks = sum(1 for s in range(200) if Agent(PS, s, 'greedy').run(1000).pulls.index(max(Agent(PS, s, 'greedy').run(1000).pulls)) != 2)
C(locks == 127, f'greedy locked onto a worse venue in {locks} of 200 seeds')
E('l1', 'screens[6].prose', 127); E('l2', 'screens[0].prose', 127)
E('l1', 'screens[6].widget.answer', regret_of(PS, g0.pulls)); E('l1', 'screens[6].explain.text', 150)
P_, Q_ = regret_of(PS, [333, 333, 334]), regret_of(PS, [12, 40, 948])
C(abs(P_ - 66.6) < 1e-9 and abs(Q_ - 3.8) < 1e-9, 'trap: P 66.6, Q 3.8')
E('l1', 'screens[7].feedback.correct', 3.8); E('l1', 'screens[7].explain.text', 66.6)
E('l1', 'screens[8].widget.answer', regret_of([0.55, 0.55], [700, 300])); E('l1', 'screens[8].widget.wrong[0].value', 550)
lostf = 2000 * (0.61 - 0.58) + 3000 * (0.61 - 0.52)
C(abs(lostf - 330) < 1e-9 and abs(lostf * 1.8 - 594) < 1e-9, 'transfer 330 fills, £594')
E('l1', 'screens[10].widget.answer', 594); E('l1', 'screens[10].widget.wrong[1].value', round(3000 * 0.09 * 1.8, 2))
E('l1', 'screens[10].widget.wrong[2].value', round((2000 * 0.42 + 3000 * 0.48 + 1000 * 0.39) * 1.8, 2))
E('l1', 'quiz[0].widget.answer', 0.6 + (0 - 0.6) / 6); E('l1', 'quiz[0].widget.wrong[1].value', round(0.6 - 0.6 / 5, 2))
E('l1', 'quiz[1].widget.answer', regret_of(PS, [400, 100, 500])); E('l1', 'quiz[1].widget.wrong[0].value', 400 * 0.45 + 100 * 0.55 + 500 * 0.6)

# ================= l2 =================
E('l2', 'screens[0].widget.answer', round(100 * (0.6 - 1.6 / 3), 2)); E('l2', 'screens[0].widget.wrong[0].value', 100 * (0.15 + 0.05) / 2)
E('l2', 'screens[0].widget.wrong[2].value', 100 * 0.6)
rec = {e: mean_regret('eps', eps=e) for e in (0, 0.01, 0.1, 0.3)}
for e, v in zip((0, 0.01, 0.1, 0.3), (56.0, 40.6, 24.0, 30.0)):
    C(round(rec[e], 1) == v, f'epsilon {e}: mean regret {rec[e]:.3f} rounds to {v}')
    E('l2', 'screens[1].explain.text', v)
curves = J('l2', 'screens[1].canvas.params.series')
C(all(abs(c['values'][-1] - rec[e]) < 0.006 for c, e in zip(curves, (0, 0.01, 0.1, 0.3))), 'l2 explore curves end at the recomputed means')
E('l2', 'screens[2].widget.answer', round(1000 * 0.3 * (0.6 - 1.6 / 3), 2)); E('l2', 'screens[2].explain.text', 30.0)
w4 = check_code('l2', 'screens[3].widget')
for call, (T, e, s, ps) in {'epsilon_greedy([0.45, 0.55, 0.6], 1000, 0.1, 0)': (1000, 0.1, 0, PS), 'epsilon_greedy([0.45, 0.55, 0.6], 1000, 0.3, 4)': (1000, 0.3, 4, PS),
                            'epsilon_greedy([0.1, 0.9], 2000, 0.05, 3)': (2000, 0.05, 3, [0.1, 0.9])}.items():
    C(expect_of(w4, call) == Agent(ps, s, 'eps', eps=e).run(T).total, f'{call} reproduced')
E('l2', 'screens[3].feedback.correct', 0.00667); E('l2', 'screens[3].feedback.correct', 6.67)
sd = sum(t ** -0.5 for t in range(1, 1001)); sd2 = float(integrate.quad(lambda x: x ** -0.5, 1, 1000)[0]) + 0.5 * (1 + 1000 ** -0.5) + 0.0  # Euler-Maclaurin first terms
C(abs(sd - 61.801) < 1e-3 and abs(sd - sd2) < 0.05, f'sum 1/sqrt t = {sd:.4f} (Euler-Maclaurin {sd2:.4f})')
E('l2', 'screens[4].widget.answer', round(sd, 1)); E('l2', 'screens[4].widget.wrong[1].value', round(math.sqrt(1000), 1))
E('l2', 'screens[4].widget.wrong[2].value', round(1000 ** -0.5, 4))
opt, gre = mean_regret('greedy', optimistic=True), mean_regret('greedy')
C(round(opt, 1) == 27.9 and round(gre, 1) == 61.8, f'optimistic {opt:.2f}, greedy {gre:.2f}')
E('l2', 'screens[5].prose', 27.9); E('l2', 'screens[5].prose', 61.8)
E('l2', 'screens[5].widget.answer', round(1 / 3, 4)); E('l2', 'screens[5].widget.wrong[1].value', 0.25)
E('l2', 'screens[6].widget.answer', round(0.9 ** 20, 4)); E('l2', 'screens[6].widget.wrong[2].value', round(1 - 0.9 ** 20, 4))
rng = random.Random(21); m = 0.0
for t in range(1, 1001):
    r = 1 if rng.random() < (0.6 if t <= 500 else 0.4) else 0
    m += (r - m) / t
C(abs(m - 0.499) < 0.0005, f'drift run sample mean ends at {m:.4f}'); E('l2', 'screens[6].explain.text', round(m, 2))
check_code('l2', 'screens[7].widget'); E('l2', 'screens[7].prose', round(1 - 0.9 ** 30, 4))
for v, e in ((66.7, 0.1), (200, 0.3)):
    C(abs(10000 * e * (0.6 - 1.6 / 3) - v) < 0.05, f'10,000-order floor at {e} is {v}')
E('l2', 'screens[8].explain.text', 66.7); E('l2', 'screens[8].explain.text', 200)
E('l2', 'screens[10].widget.answer', 200000 * 0.05 * 0.04 * 1.5); E('l2', 'screens[10].widget.wrong[0].value', 200000 * 0.05 * 0.04)
E('l2', 'screens[10].widget.wrong[1].value', 200000 * 0.04 * 1.5); E('l2', 'screens[10].widget.wrong[2].value', 200000 * 0.05 * 1.5)
E('l2', 'quiz[0].widget.answer', 0.2 * (0.7 - 0.45)); E('l2', 'quiz[1].widget.answer', round((0.4 + 0.2 * 0.6) + 0.2 * (1 - 0.52), 3))

# ================= l3 =================
E('l3', 'screens[0].widget.answer', round(math.sqrt(0.24 / 10), 4)); E('l3', 'screens[0].widget.wrong[0].value', round(math.sqrt(0.55 * 0.45 / 100), 4))
E('l3', 'screens[0].widget.wrong[2].value', round(math.sqrt(0.24), 4))
E('l3', 'screens[2].widget.answer', 1 / (4 * 100 * 0.01))
hz = lambda n, e: math.exp(-2 * n * e * e)
C(abs(stats.binom(400, 0.5).sf(0) - 1) < 1e-9, 'sanity: scipy loaded')
E('l3', 'screens[3].prose', round(hz(100, 0.1), 4)); E('l3', 'screens[3].prose', round(2 * hz(100, 0.1), 4))
E('l3', 'screens[3].widget.answer', round(2 * hz(400, 0.1), 5)); E('l3', 'screens[3].widget.wrong[0].value', round(hz(400, 0.1), 5))
E('l3', 'screens[3].widget.wrong[1].value', 0.25 / (400 * 0.01)); E('l3', 'screens[1].feedback.correct', 0.00067)
# the bound really holds: exact binomial upper tail is below Hoeffding at n = 100, eps = 0.1, p = 0.5
C(stats.binom(100, 0.5).sf(59) <= hz(100, 0.1), 'exact tail at n=100 is below e^{-2}')
bon = lambda t, n: math.sqrt(2 * math.log(t) / n)
for t, n, v in ((100, 10, 0.9597), (100, 50, 0.4292), (1000, 10, 1.1754)):
    C(round(bon(t, n), 4) == v, f'bonus t={t} n={n} = {v}')
E('l3', 'screens[5].widget.rows[0][3].answer', 0.9597); E('l3', 'screens[5].widget.rows[1][3].answer', 0.4292)
E('l3', 'screens[5].widget.rows[0][4].answer', round(0.4 + bon(100, 10), 4)); E('l3', 'screens[5].prose', round(2 * math.log(100), 4))
E('l3', 'screens[5].widget.rows[0][3].wrong[0].value', round(2 * math.log(100) / 10, 4))
for k, q, n in (('P', 0.62, 900), ('Q', 0.50, 8), ('R', 0.58, 91)):
    E('l3', 'screens[6].hints[2].text', round(q + bon(1000, n), 4))
w8 = check_code('l3', 'screens[7].widget')
for s in (0, 3):
    a = Agent(PS, s, 'ucb').run(1000)
    C(tuple(expect_of(w8, f'run_ucb([0.45, 0.55, 0.6], 1000, {s})')) == (a.total, a.pulls), f'UCB1 seed {s} reproduced')
u1, e1, u5 = mean_regret('ucb'), mean_regret('eps', eps=0.1), mean_regret('ucb', c=0.5)
C((round(u1, 1), round(e1, 1), round(u5, 1)) == (37.8, 24.0, 18.3), f'UCB1 {u1:.2f}, eps {e1:.2f}, c=0.5 {u5:.2f}')
for v in (37.8, 24.0, 18.3):
    E('l3', 'screens[8].prose', v)
# crossover: 20 seeds, 60,000 pulls
cps = (40000, 50000)
ce, cu = {c: 0.0 for c in cps}, {c: 0.0 for c in cps}
for s in range(20):
    ae, au = Agent(PS, s, 'eps', eps=0.1), Agent(PS, s, 'ucb')
    for t in range(1, 50001):
        ae.step(); au.step()
        if t in ce:
            ce[t] += ae.cum / 20; cu[t] += au.cum / 20
C(cu[40000] > ce[40000] and cu[50000] < ce[50000], f'UCB1 overtakes between 40,000 ({cu[40000]:.1f} v {ce[40000]:.1f}) and 50,000 ({cu[50000]:.1f} v {ce[50000]:.1f})')
E('l3', 'screens[8].explain.text', 5500); C(abs(2 * math.log(1000) / 0.05 ** 2 - 5526) < 1, 'about 5,500 pulls (5,526)')
zs = 0.25 + bon(60, 4)
E('l3', 'screens[10].widget.answer', round(zs, 4)); E('l3', 'screens[10].widget.wrong[0].value', round(bon(60, 4), 4))
E('l3', 'screens[10].widget.wrong[2].value', round(14 / 25 + bon(60, 25), 4)); E('l3', 'screens[10].feedback.correct', round(0.5 + bon(60, 30), 4))
E('l3', 'quiz[0].widget.answer', round(bon(1000, 10), 4)); E('l3', 'quiz[1].explain.text', round(100 ** 2 / (2 * math.sqrt(10)), 1))
E('l3', 'quiz[2].widget.answer', round(math.exp(-1), 4)); E('l3', 'quiz[2].widget.wrong[0].value', round(2 * math.exp(-1), 4))

# ================= l4 =================
pq = lambda a1, b1, a2, b2: integrate.quad(lambda x: stats.beta(a1, b1).pdf(x) * stats.beta(a2, b2).cdf(x), 0, 1, limit=200)[0]
pab = pq(8, 4, 31, 21)
g = np.random.default_rng(0); mc = float((g.beta(8, 4, 10 ** 6) > g.beta(31, 21, 10 ** 6)).mean())
C(round(pab, 4) == 0.6921 and abs(mc - pab) < 0.002, f'P(A beats B) quadrature {pab:.5f}, 10^6 draws {mc:.5f}')
E('l4', 'screens[0].widget.answer', round(8 / 12, 4)); E('l4', 'screens[0].widget.wrong[1].value', round(31 / 52, 4)); E('l4', 'screens[0].widget.wrong[2].value', round(8 / 11, 4))
E('l4', 'screens[2].prose', 0.6921); E('l4', 'screens[2].widget.answer', round(pab, 2))
E('l4', 'screens[3].widget.answer', round(8 / 13, 4)); E('l4', 'screens[3].widget.wrong[0].value', round(9 / 13, 4)); E('l4', 'screens[3].widget.wrong[2].value', round(7 / 11, 4))
w5 = check_code('l4', 'screens[4].widget')
rng = random.Random(0); pv = sum(rng.betavariate(8, 4) > rng.betavariate(31, 21) for _ in range(20000)) / 20000
E('l4', 'screens[4].feedback.correct', round(pv, 4)); C(abs(pv - pab) < 0.01, f'seed 0 share {pv} within 0.01')
E('l4', 'screens[4].explain.text', round(math.sqrt(0.69 * 0.31 / 20000), 4))
w6 = check_code('l4', 'screens[5].widget')
for s in (0, 1, 2):
    a = Agent(PS, s, 'ts').run(1000)
    C(tuple(expect_of(w6, f'run_thompson([0.45, 0.55, 0.6], 1000, {s})')) == (a.total, a.pulls), f'Thompson seed {s} reproduced')
ts, gr = mean_regret('ts'), mean_regret('greedy')
C((round(gr, 1), round(e1, 1), round(u1, 1), round(ts, 1)) == (61.8, 24.0, 37.8, 20.8), f'four agents {gr:.2f} {e1:.2f} {u1:.2f} {ts:.2f}')
for v in (61.8, 24.0, 37.8, 20.8):
    E('l4', 'screens[6].explain.text', v)
E('l4', 'screens[8].widget.answer', round(95 / 160, 4)); E('l4', 'screens[8].prose', round(50 / 60, 4)); E('l4', 'screens[8].widget.wrong[0].value', round(46 / 102, 4))
pts = pq(6, 4, 13, 9)
E('l4', 'screens[10].explain.text', round(pts, 4)); E('l4', 'screens[10].feedback.correct', round(13 / 22, 4)); E('l4', 'screens[10].widget.answer', 0.6)
E('l4', 'quiz[0].widget.answer', round(5 / 9, 4)); E('l4', 'quiz[0].widget.wrong[1].value', round(4 / 7, 4)); E('l4', 'quiz[2].widget.answer', 40)

# ================= review-1 =================
E('review', 'items[0].widget.answer', round(0.55 + 0.45 / 21, 4)); E('review', 'items[0].widget.wrong[0].value', round(0.55 + 0.45 / 20, 4))
E('review', 'items[1].widget.answer', regret_of([0.3, 0.5, 0.7], [100, 250, 650])); E('review', 'items[1].widget.wrong[0].value', 100 * 0.3 + 250 * 0.5 + 650 * 0.7)
E('review', 'items[2].widget.answer', 5000 * 0.05 * 0.2); E('review', 'items[3].widget.answer', round(0.8 * 0.7 ** 2, 3))
sc = [q + bon(200, n) for q, n in ((0.52, 120), (0.61, 70), (0.45, 9))]
C(sc.index(max(sc)) == 2, 'review UCB picks arm 3'); E('review', 'items[4].explain.text', round(sc[2], 4)); E('review', 'items[4].explain.text', round(sc[0], 4))
nH = math.ceil(math.log(100) / (2 * 0.0025)); C(hz(nH, 0.05) <= 0.01 < hz(nH - 1, 0.05), f'Hoeffding n = {nH}')
E('review', 'items[5].widget.answer', nH); E('review', 'items[5].widget.wrong[1].value', math.ceil(math.log(200) / 0.005))
E('review', 'items[5].widget.wrong[2].value', math.ceil(math.log(100) / 0.0025))
pA = pq(5, 2, 41, 31); E('review', 'items[6].explain.text', round(pA, 4)); E('review', 'items[6].explain.text', round(41 / 72, 4))
E('review', 'items[7].widget.answer', 13 / 20)

# ================= homework-1 =================
wl = check_code('homework', 'items[0].widget')
def league(ps, T, seeds):
    out = {}
    for name, kind in (('eps', 'eps'), ('ucb', 'ucb'), ('thompson', 'ts')):
        out[name] = sum(regret_of(ps, Agent(ps, s, kind).run(T).pulls) for s in seeds) / len(seeds)
    return out
for call, args in (('bandit_league([0.45, 0.55, 0.6], 500, [3])', (PS, 500, [3])), ('bandit_league([0.45, 0.55, 0.6], 1000, [0, 1, 2, 3, 4])', (PS, 1000, range(5)))):
    e_, m_ = expect_of(wl, call), league(*args)
    C(all(math.isclose(e_[k], m_[k], rel_tol=1e-9) for k in m_), f'{call} reproduced')
lw, lp = league([0.2, 0.5, 0.8], 2000, range(20)), league(PS, 2000, range(20))
C(lw['ucb'] < lw['eps'] - 8 and lw['thompson'] < lw['ucb'] - 20, f'wide arms margins: {lw}')
C(lp['thompson'] < lp['ucb'] - 10 and lp['eps'] < lp['ucb'] - 10, f'venue margins: {lp}')
for v in list(lw.values()) + list(lp.values()):
    E('homework', 'items[0].explain.text', round(v, 2))
check_code('homework', 'items[1].widget')
def drift(al, s):
    a = Agent([0.6, 0.4], s, 'eps', eps=0.1, alpha=al); late = 0
    for t in range(1, 2001):
        r = a.step(None if t <= 1000 else [0.3, 0.7])
        if t > 1000: late += r
    return late
gain = sum(drift(0.1, s) - drift(None, s) for s in range(10)) / 10
C(gain > 100, f'constant step gains {gain} fills'); E('homework', 'items[1].feedback.correct', round(gain, 1))
E('homework', 'items[3].widget.answer', 20000 * 0.05 * (0.58 - 0.45)); E('homework', 'items[3].widget.wrong[2].value', 20000 * 0.05 * 0.28)
nb = math.ceil(2 * math.log(10000) / 0.0025); C(bon(10000, nb) < 0.05 <= bon(10000, nb - 1), f'bonus below 0.05 from n = {nb}')
E('homework', 'items[4].widget.answer', nb); E('homework', 'items[4].widget.wrong[0].value', math.ceil(math.log(10000) / 0.0025))
E('homework', 'items[4].widget.wrong[1].value', math.ceil(2 * math.log(10000) / 0.05))
lf = 'items[6].model'
E('homework', lf, 50 * 0.15 + 50 * 0.05); E('homework', lf, round(math.sqrt(0.25 / 50), 2)); E('homework', lf, round(hz(50, 0.025), 2)); E('homework', lf, 100000 * 0.05)

# ================= problems-1 =================
p2 = integrate.quad(lambda x: 2 * x * x, 0, 1)[0]; p4 = integrate.quad(lambda x: 6 * x * (1 - x) * x, 0, 1)[0]
C(abs(p2 - 2 / 3) < 1e-12 and abs(p4 - 0.5) < 1e-12, 'Beta(2,1) and Beta(2,2) against a uniform: 2/3 and 1/2')
g = np.random.default_rng(1); C(abs((g.beta(2, 1, 10 ** 6) > g.random(10 ** 6)).mean() - 2 / 3) < 0.002, '2/3 by draws')
E('problems', 'items[0].parts[1].widget.answer', round(p2, 4)); E('problems', 'items[0].parts[2].widget.answer', round(100 * p2, 2)); E('problems', 'items[0].parts[3].widget.answer', p4)
b50 = [bon(50, n) for n in (30, 12, 7)]; s50 = [0.62 + b50[0], 0.48 + b50[1], 0.55 + b50[2]]
E('problems', 'items[1].parts[0].widget.answer', round(b50[2], 4)); E('problems', 'items[1].parts[1].widget.answer', round(s50[2], 4))
E('problems', 'items[1].parts[2].question', round(s50[0], 4)); E('problems', 'items[1].parts[2].question', round(s50[1], 4))
nn = math.ceil(2 * math.log(50) / 0.0049); C(bon(50, nn) < 0.07 <= bon(50, nn - 1), f'n = {nn}')
E('problems', 'items[1].parts[3].widget.answer', nn); E('problems', 'items[1].prose', round(2 * math.log(50), 4))
qb = (0.35 + 0.47 + 0.52 + 0.58) / 4
E('problems', 'items[2].parts[0].widget.answer', qb); E('problems', 'items[2].parts[1].widget.answer', round(0.08 * (0.58 - qb), 4))
E('problems', 'items[2].parts[2].widget.answer', round(50000 * 0.08 * (0.58 - qb), 6)); E('problems', 'items[2].parts[3].widget.answer', 0.08)
C(abs(50000 * (0.58 - qb) - 5000) < 1e-6, 'random routing regret 5,000')

lv.check_wrongs()
lv.report()
