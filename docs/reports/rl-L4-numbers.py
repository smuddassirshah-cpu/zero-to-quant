"""Recompute every number stated in rl level 4 (policy gradients) and check it at its JSON path.

Run: <venv>/bin/python docs/reports/rl-L4-numbers.py   (NumPy and the standard library; about 20 s; exits 0 when every check passes)

Two routes per number: the corridor by a linear solve and by the closed form; gradients by formula and by central
differences; variances by enumeration and by the two-point formula; best baselines by formula and by a grid search over b;
the execution optimum by backward induction and by enumerating all 3^5 schedules. Seeded results (REINFORCE runs, the policy
network) are re-run here with code written apart from the lesson solutions, and every code widget's solution is run against
its hidden tests in CPython with its starter failing one. Shipped modules are checked byte for byte.
"""
import hashlib, itertools, math, os, random, statistics as st, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402
AI = os.path.join(HERE, '..', '..', 'app', 'content', 'data', 'ai')
sys.path.insert(0, AI)
from autograd import Tensor, grad_check, sgd_step  # noqa: E402
import rl_ops_l4 as ops  # noqa: E402

lv = Level('rl', 4)
E, C = lv.expect, lv.claim
R2 = math.sqrt(2)


def sha(name):
    with open(os.path.join(AI, name), 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


C(sha('autograd.py').startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0 (SHA-256 5917d4ec91f7...)')
C(sha('rl_ops_l3.py').startswith('eba4d2b39835'), 'rl_ops_l3.py is unchanged from L3 (SHA-256 eba4d2b39835...)')
C(ops.__version__ == '1.0', 'rl_ops_l4 version 1.0')


def widgets(node, out):
    if isinstance(node, dict):
        if node.get('kind') in ('code', 'trainer'):
            out.append(node)
        for v in node.values():
            widgets(v, out)
    elif isinstance(node, list):
        for v in node:
            widgets(v, out)
    return out


for fid, doc in lv.files.items():
    for w in widgets(doc, []):
        if 'data' in w:
            C(w['data'] == {'autograd.py': 'content/data/ai/autograd.py', 'rl_ops_l4.py': 'content/data/ai/rl_ops_l4.py'},
              f'{fid}: ships autograd.py and rl_ops_l4.py by path, so the text is the frozen file')


# ---------------- run each code widget's tests in CPython ----------------
def run_tests(w, src):
    old = os.getcwd()
    os.chdir(AI)  # the modules a widget ships sit here
    ns = {'__name__': '__main__', '__learner_source__': src}
    res = []
    try:
        exec(src, ns)
        for c in w['tests']:
            try:
                if c.get('setup'):
                    exec(c['setup'], ns)
                got, exp = eval(c['call'], ns), eval(c['expect'], dict(ns))
                if c.get('compare') == 'isclose':
                    tol = c.get('tol', {})
                    rel, ab = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)
                    g, x = np.asarray(got, dtype=float).ravel(), np.asarray(exp, dtype=float).ravel()
                    res.append(g.shape == x.shape and all(math.isclose(a, b, rel_tol=rel, abs_tol=ab) for a, b in zip(g, x)))
                else:
                    res.append(got == exp)
            except Exception:
                res.append(False)
    except Exception:
        res = [False] * len(w['tests'])
    finally:
        os.chdir(old)
    return res


for fid, doc in lv.files.items():
    for k, w in enumerate(x for x in widgets(doc, []) if x['kind'] == 'code'):
        good = run_tests(w, w['solution'])
        C(all(good), f'{fid} code {k}: solution passes all {len(good)} hidden tests', str(good))
        C(not all(run_tests(w, w['starter'])), f'{fid} code {k}: starter fails')

# ---------------- l13: the short corridor ----------------
def J_solve(p):
    P = np.array([[1 - p, p, 0], [p, 0, 1 - p], [0, 1 - p, 0]])
    return np.linalg.solve(np.eye(3) - P, -np.ones(3))[0]


for p in (0.5, 2 - R2, 0.05, 0.95, 0.25, 0.7, 0.6):
    C(abs(J_solve(p) - ops.corridor_value(p)) < 1e-9, f'J({p:.4f}) linear solve = closed form')
grid = np.linspace(0.01, 0.99, 98001)
pbest = grid[np.argmax([(2 * x - 4) / (x * (1 - x)) for x in grid])]
C(abs(pbest - (2 - R2)) < 1e-4 and abs(ops.corridor_value(2 - R2) + 6 + 4 * R2) < 1e-12, 'best p = 2 - sqrt 2 by grid search, J = -(6 + 4 sqrt 2)')
E('l13', 'screens[1].explain.text', round(2 - R2, 4)); E('l13', 'screens[1].explain.text', round(ops.corridor_value(2 - R2), 3))
E('l13', 'screens[1].feedback.correct', round(-ops.corridor_value(2 - R2), 2))
E('l13', 'screens[2].widget.answer', ops.corridor_value(0.5))
gap = math.log((2 - R2) / (R2 - 1))
C(abs(gap - math.log(R2)) < 1e-12, 'odds (2 - sqrt 2)/(sqrt 2 - 1) = sqrt 2')
E('l13', 'screens[3].widget.answer', round(gap, 4)); E('l13', 'screens[3].widget.wrong[0].value', round(R2, 4)); E('l13', 'screens[3].widget.wrong[1].value', round(math.log(2 - R2), 4))
E('l13', 'screens[4].widget.answer', round(ops.corridor_value(0.95), 2)); E('l13', 'screens[4].widget.wrong[0].value', round(ops.corridor_value(0.05), 2))
E('l13', 'screens[4].widget.wrong[2].value', round(ops.corridor_value(2 - R2), 2))
C(abs(0.9 + 0.1 / 2 - 0.95) < 1e-15, 'epsilon-greedy right chance 0.9 + 0.05')
E('l13', 'screens[7].widget.answer', round(ops.softmax([2.5] * 3)[0], 4)); E('l13', 'screens[7].widget.wrong[0].value', round(2.5 / 3, 4))
lv.stated('l13', 'screens[1].widget.options', 'about 19 steps', round(-ops.corridor_value(0.25)) == 19)
E('l13', 'screens[9].widget.answer', 600 * 0.5)
E('l13', 'quiz[0].widget.answer', ops.softmax([0, math.log(3)])[1])
E('l13', 'quiz[1].widget.answer', round(ops.corridor_value(0.25), 2))
C(all(ops.corridor_episode(1.0, random.Random(0), 50) == [1] * 50 for _ in [0]) and ops.corridor_episode(0.0, random.Random(0), 50) == [0] * 50, 'always right and always left never reach G (50-step cap hit)')
for p in (0.5, 0.6):
    rng = random.Random(1)
    m = st.mean(len(ops.corridor_episode(p, rng)) for _ in range(40000))
    C(abs(m + ops.corridor_value(p)) < 0.25, f'simulated mean walk at p = {p} is {m:.2f} steps, near -J')

# ---------------- l14: the score and REINFORCE ----------------
pi = [0.5, 0.5]; r = [10, 11]
dJ = pi[0] * (r[0] - sum(a * b for a, b in zip(pi, r)))
h = 1e-6
fd = (sum(x * y for x, y in zip(ops.softmax([h, 0]), r)) - sum(x * y for x, y in zip(ops.softmax([-h, 0]), r))) / (2 * h)
C(abs(dJ + 0.25) < 1e-12 and abs(fd + 0.25) < 1e-8, 'dJ/dtheta_A = -0.25 by formula and by central differences')
E('l14', 'screens[0].widget.answer', dJ)
est = [r[0] * (1 - pi[0]), r[1] * (-pi[0])]
E('l14', 'screens[1].feedback.correct', est[1]); E('l14', 'screens[1].feedback.correct', dJ)
var = sum(p * x * x for p, x in zip(pi, est)) - (sum(p * x for p, x in zip(pi, est))) ** 2
C(var == 27.5625 and ((est[0] - est[1]) / 2) ** 2 == 27.5625, 'variance 27.5625 by enumeration and by the two-point formula')
E('l14', 'screens[4].widget.answer', var); E('l14', 'screens[4].widget.wrong[0].value', 27.625); E('l14', 'screens[4].widget.wrong[1].value', math.sqrt(var))
lv.stated('l14', 'screens[4].explain.text', '21 times the signal', math.sqrt(var) / 0.25 == 21)
sc = ops.grad_log_softmax([math.log(0.2), math.log(0.5), math.log(0.3)], 1)
C(np.allclose(sc, [-0.2, 0.5, -0.3]), 'score at pi = (0.2, 0.5, 0.3), arm 2 pulled')
E('l14', 'screens[2].widget.answer', sc[0])
E('l14', 'screens[5].widget.answer', -3)
E('l14', 'screens[9].widget.answer', 120 * (1 - 0.3)); E('l14', 'screens[9].widget.wrong[0].value', 120 * 0.3)
E('l14', 'quiz[0].widget.answer', round(1 - 1 / 3, 4)); E('l14', 'quiz[1].widget.answer', 8 * 0.75); E('l14', 'quiz[2].widget.answer', 5)
th = [0.3, -1.2, 0.8]
for a in range(3):
    g = ops.grad_log_softmax(th, a)
    num_ = [(math.log(ops.softmax([t + (h if j == b else 0) for j, t in enumerate(th)])[a]) - math.log(ops.softmax([t - (h if j == b else 0) for j, t in enumerate(th)])[a])) / (2 * h) for b in range(3)]
    C(max(abs(x - y) for x, y in zip(g, num_)) < 1e-6, f'rl_ops_l4 grad_log_softmax(th, {a}) matches central differences')
# own REINFORCE, written apart: dial difference d = theta_1 - theta_0, so p_B = sigmoid(d)
def bandit_own(rew, steps, lr, seed):
    rng, t0, t1 = random.Random(seed), 0.0, 0.0
    for _ in range(steps):
        pB = 1 / (1 + math.exp(t0 - t1))
        a = 0 if rng.random() < 1 - pB else 1
        t0 += lr * rew[a] * ((a == 0) - (1 - pB)); t1 += lr * rew[a] * ((a == 1) - pB)
    return 1 / (1 + math.exp(t0 - t1))
ban = [bandit_own([10, 11], 2000, 0.01, s) for s in range(10)]
C(st.mean(ban) > 0.85, f'plain REINFORCE on the venues: mean final p_B over seeds 0-9 is {st.mean(ban):.3f}, above the test line 0.8 with a margin')
ban20 = [bandit_own([10, 11], 2000, 0.01, s) for s in range(20)]
print('  bandit seeds 0-19 min', round(min(ban20), 3), 'mean', round(st.mean(ban20), 3))
def corr_own(episodes, lr, seed, beta=None):
    rng, d, b, gp, gb = random.Random(seed), 0.0, 0.0, [], []
    for _ in range(episodes):
        p = 1 / (1 + math.exp(-d))
        acts = ops.corridor_episode(p, rng)
        x = y = 0.0
        for t, a in enumerate(acts):
            G = -(len(acts) - t); s_ = a - p
            x += G * s_; y += (G - b) * s_
            if beta is not None:
                b += beta * (G - b)
        gp.append(x); gb.append(y)
        d += 2 * lr * (x if beta is None else y)
    return 1 / (1 + math.exp(-d)), (st.pvariance(gb) / st.pvariance(gp) if beta is not None else None)
cp = [corr_own(1000, 0.001, s)[0] for s in range(10)]
C(0.55 < st.mean(cp) < 0.62, f'plain REINFORCE on the corridor: mean final p over seeds 0-9 is {st.mean(cp):.4f}, inside 0.53 to 0.64 with a margin')
# ---------------- l15: baselines ----------------
def var_b(pi, rew, b, k=0):
    e = [(rr - b) * ((a == k) - pi[k]) for a, rr in enumerate(rew)]
    m = sum(p * x for p, x in zip(pi, e))
    return sum(p * x * x for p, x in zip(pi, e)) - m * m, m
for b_, want in ((0, 27.5625), (10, 0.0625), (10.5, 0.0), (11, 0.0625)):
    v, m = var_b([0.5, 0.5], [10, 11], b_)
    C(abs(v - want) < 1e-12 and abs(v - (10.5 - b_) ** 2 / 4) < 1e-12 and abs(m + 0.25) < 1e-12, f'b = {b_}: variance {want} two ways, mean -0.25')
E('l15', 'screens[0].widget.answer', -0.25); E('l15', 'screens[3].widget.answer', 0.0625); E('l15', 'quiz[0].widget.answer', 0.0625)
lv.stated('l15', 'screens[3].explain.text', 'a factor of 441', 27.5625 / 0.0625 == 441)
E('l15', 'screens[2].widget.answer', 0.2 * 0.8 + 0.8 * -0.2)
def bstar(pi, rew, k=0):
    s = [(a == k) - pi[k] for a in range(len(pi))]
    return sum(p * x * x * g for p, x, g in zip(pi, s, rew)) / sum(p * x * x for p, x in zip(pi, s))
def bgrid(pi, rew):
    bs = np.linspace(-5, 20, 250001)
    return bs[np.argmin([var_b(pi, rew, b)[0] for b in bs[::50]]) * 50]
for pi_, rew_, want in (([0.2, 0.8], [10, 11], 10.2), ([0.5, 0.5], [10, 11], 10.5), ([0.5, 0.5], [4, 8], 6), ([0.25, 0.75], [2, 6], 3), ([0.6, 0.4], [5, 15], 11)):
    C(abs(bstar(pi_, rew_) - want) < 1e-9 and abs(bgrid(pi_, rew_) - want) < 1e-3, f'b* = {want} by formula and by a grid over b ({pi_}, {rew_})')
E('l15', 'screens[4].widget.answer', 10.2); E('l15', 'screens[4].widget.wrong[0].value', 0.2 * 10 + 0.8 * 11); E('l15', 'quiz[2].widget.answer', 6)
E('l15', 'screens[5].widget.answer', round(-9 - ops.corridor_value(2 - R2), 2))
E('l15', 'screens[9].widget.answer', 400 * (1 - 0.81)); E('l15', 'screens[9].widget.wrong[1].value', 400 * 0.81)
E('l15', 'screens[6].widget.tests[6].expect', round(var_b([0.2, 0.5, 0.3], [1, 2, 4], 0, k=1)[0], 10))
C(abs(var_b([0.2, 0.5, 0.3], [1, 2, 4], 0, k=1)[1] - 0.5 * (2 - 2.4)) < 1e-12, 'three-arm estimates average to the true gradient pi_1 (r_1 - J) = -0.2')
# reinforce with a running baseline on the venues (own code)
def rwb_own(rew, steps, lr, seed, beta=0.1):
    rng, t, b, P_, B_ = random.Random(seed), [0.0, 0.0], 0.0, [], []
    for _ in range(steps):
        pi_ = ops.softmax(t); a = ops.sample(pi_, rng); rr = rew[a]
        s0 = (a == 0) - pi_[0]
        P_.append(rr * s0); B_.append((rr - b) * s0)
        t = [t[j] + lr * (rr - b) * ((a == j) - pi_[j]) for j in range(2)]
        b += beta * (rr - b)
    return ops.softmax(t)[1], st.pvariance(B_) / st.pvariance(P_)
rw = [rwb_own([10, 11], 1000, 0.1, s) for s in range(5)]
C(min(x[0] for x in rw) > 0.97 and max(x[1] for x in rw) < 0.15, f'baselined venues, seeds 0-4: min p_B {min(x[0] for x in rw):.4f}, max ratio {max(x[1] for x in rw):.4f} (test lines 0.95, 0.25)')
# ---------------- homework: train_corridor ----------------
hc = [corr_own(1000, 0.001, s, beta=0.1) for s in range(20)]
C(max(x[1] for x in hc[:5]) < 0.4 and 0.55 < st.mean(x[0] for x in hc[:10]) < 0.62, 'homework thresholds hold with margins (ratio < 0.5, mean p in 0.53 to 0.64)')
lo, hi = min(x[1] for x in hc), max(x[1] for x in hc)
lv.stated('homework', 'items[h4-train-corridor].explain.text', 'between 0.17 and 0.33 on seeds 0 to 19', round(lo, 2) >= 0.17 and round(hi, 2) <= 0.33)
print('  homework ratio seeds 0-19', round(lo, 4), round(hi, 4))
SC, GR = [0.4, -0.6, 0.4, 0.4, -0.6, -0.2, 0.8], [5.0, 15.0, 6.0, 4.0, 14.0, 9.0, 3.0]
bs = np.linspace(0, 20, 200001)
vv = [np.mean([((g - b) * s) ** 2 for s, g in zip(SC, GR)]) for b in bs[::10]]
C(abs(bs[::10][int(np.argmin(vv))] - sum(s * s * g for s, g in zip(SC, GR)) / sum(s * s for s in SC)) < 1e-3, 'homework sample b* minimises the mean square of (G - b)s, by formula and by grid')
E('homework', 'items[h4-three-arm-var].widget.answer', var_b([0.5, 0.25, 0.25], [4, 0, 8], 0)[0]); E('homework', 'items[h4-three-arm-var].widget.wrong[0].value', round(math.sqrt(6), 4))
E('homework', 'items[h4-three-arm-var].widget.wrong[1].value', round((4 + 0 + 16) / 3, 4))
# ---------------- l16: the execution task ----------------
val, plan = ops.exec_dp()
best_enum = max((sum(rr for rr in [0]) + 0, s) for s in [()])  # placeholder replaced below
def sched_value(s):
    l, tot = ops.LOTS, 0.0
    for i, k in enumerate(s):
        l, _, rr, _ = ops.exec_step(l, ops.STEPS - i, k); tot += rr
    return tot
allv = {s: sched_value(s) for s in itertools.product(range(3), repeat=5)}
bv = max(allv.values())
C(val == bv == 33.0 and plan == [1, 1, 1, 1, 0], 'optimum 33 for 1, 1, 1, 1, 0 by backward induction and by enumerating 243 schedules')
E('l16', 'screens[2].widget.answer', 33); E('l16', 'screens[0].widget.answer', allv[(2, 2, 0, 0, 0)])
E('l16', 'screens[2].widget.wrong[1].value', allv[(2, 1, 1, 0, 0)]); E('l16', 'screens[2].widget.wrong[0].value', 36)
E('l16', 'screens[0].widget.wrong[0].value', 32); E('l16', 'screens[0].widget.wrong[1].value', 35)
lp = np.log(0.5)
E('l16', 'screens[3].widget.answer', round(-(2 * lp + -1 * lp) / 2, 4)); E('l16', 'screens[3].widget.wrong[0].value', round(-(2 * lp - lp), 4))
adv = np.array([300.0, -100, -200])
E('l16', 'screens[6].widget.answer', round(adv[0] / adv.std(), 4)); C(np.allclose(adv / adv.std(), adv / 100 / (adv / 100).std()), 'normalised advantages are unit-free')
E('l16', 'screens[6].feedback.correct', round(adv.std(), 4))
kl = 0.6 * math.log(1.2) + 0.4 * math.log(0.8); rkl = 0.5 * math.log(0.5 / 0.6) + 0.5 * math.log(0.5 / 0.4)
C(abs(kl - sum(p * math.log(p / q) for p, q in zip([0.6, 0.4], [0.5, 0.5]))) < 1e-15, 'KL two ways')
E('l16', 'screens[7].widget.answer', round(kl, 4)); E('l16', 'screens[7].widget.wrong[0].value', round(rkl, 4))
E('l16', 'quiz[0].widget.answer', round(-2 * math.log(0.25), 4))
# the policy network: log_softmax gradient-checked, then seeded training with an own loss built from cross-entropy pieces
P = ops.init_policy(3); X = np.stack([ops.features(4, 5), ops.features(2, 3), ops.features(1, 1)])
def own_loss(P, X, A, adv):
    z = ops.policy_logits(P, X)
    lp_ = ops.log_softmax(z)
    mask = np.zeros(z.shape); mask[np.arange(len(A)), A] = 1.0
    return -((lp_ * (mask * np.asarray(adv)[:, None])).sum()) / len(A)
C(grad_check(lambda: own_loss(P, X, [1, 0, 2], [0.7, -1.2, 0.4]), P) < 1e-6, 'softmax policy gradient (log_softmax through the network) matches central differences')
zz = Tensor(np.array([[1.0, 2.0, 0.5], [0.0, -1.0, 3.0]]))
C(grad_check(lambda: (ops.log_softmax(zz) * np.array([[1.0, 0, 0], [0, 0, -0.5]])).sum(), [zz]) < 1e-6, 'log_softmax gradient check on the test logits')
def train_own(episodes, seed, lr=0.5, scale=1.0, norm=False):
    P_ = ops.init_policy(seed); rng = np.random.default_rng(seed + 1000)
    for _ in range(episodes // 32):
        X_, A_, G_, _ = ops.run_batch(P_, 32, rng)
        a_ = scale * (G_ - G_.mean(axis=0))
        if norm:
            a_ = a_ / (a_.std() + 1e-8)
        for p in P_:
            p.zero_grad()
        own_loss(P_, X_, A_, a_.reshape(-1)).backward(); sgd_step(P_, lr)
    return ops.network_value(P_)
init0 = ops.network_value(ops.init_policy(0))
tr = [train_own(960, s) for s in range(10)]
C(min(tr) > 32.88 and min(tr[:3]) > 32.5 + 0.3, f'960 episodes: seeds 0-9 worth {min(tr):.3f} to {max(tr):.3f}, above 32.88; test line 32.5')
lv.stated('l16', 'summary.ideas[1]', 'above £32.88', min(tr) > 32.88)
E('l16', 'summary.ideas[1]', round(init0, 2))
x100 = [train_own(960, s, scale=100) for s in range(10)]
n100 = [train_own(960, s, scale=100, norm=True) for s in range(10)]
n1 = [train_own(960, s, norm=True) for s in range(10)]
col = [s for s, v in enumerate(x100) if abs(v - 31.0) < 0.01]
C(len(col) == 3 and all(v > 32.9 for s, v in enumerate(x100) if s not in col), f'rewards x100 at lr 0.5: seeds {col} collapse to 31.00, the rest above 32.9')
C(max(abs(a - b) for a, b in zip(n100, n1)) < 1e-6, f'normalised pence and pounds runs agree on all 10 seeds (largest gap {max(abs(a - b) for a, b in zip(n100, n1)):.1e})')
lv.stated('l16', 'screens[5].prose', '3 of 10 seeds', len(col) == 3)
lv.stated('l16', 'screens[5].widget.options', 'about £32.9', all(tr[s] > 32.85 for s in col))
C(abs(allv[(0, 1, 1, 1, 1)] - 31) < 1e-12 and abs(allv[(0, 0, 0, 0, 0)] - 10) < 1e-12, 'other schedules: 0,1,1,1,1 earns 31; dumping everything earns 10')
# ---------------- review-4 ----------------
E('review', 'items[r4-softmax].widget.answer', round(1 / (1 + math.exp(-0.8)), 4))
E('review', 'items[r4-corridor].widget.answer', round(ops.corridor_value(0.7), 2))
E('review', 'items[r4-score].widget.answer', 0.7); E('review', 'items[r4-estimate].widget.answer', 25 * -0.4)
E('review', 'items[r4-rtg].widget.answer', -1 + 4 + 2)
E('review', 'items[r4-var].widget.answer', var_b([0.5, 0.5], [6, 9], 6)[0])
E('review', 'items[r4-bstar].widget.answer', bstar([0.25, 0.75], [2, 6]))
E('review', 'items[r4-loss].widget.answer', round(-(math.log(0.8) - math.log(0.2)) / 2, 4))
# ---------------- problems-4 ----------------
J9 = 0.6 * 5 + 0.4 * 15
E('problems', 'items[0].parts[2].widget.answer', 0.6 * (5 - J9))
v1, m1 = var_b([0.6, 0.4], [5, 15], 0)
C(abs(m1 + 2.4) < 1e-12, 'router estimates average to -2.4')
E('problems', 'items[0].parts[3].widget.answer', round(v1, 2))
E('problems', 'items[1].parts[0].widget.answer', 0.6 * 0.16 + 0.4 * 0.36)
E('problems', 'items[1].parts[1].widget.answer', bstar([0.6, 0.4], [5, 15]))
v9 = var_b([0.6, 0.4], [5, 15], 9)[0]
E('problems', 'items[1].parts[2].widget.answer', round(v9, 2)); E('problems', 'items[1].parts[3].widget.answer', round(v9 / v1, 4))
E('problems', 'items[1].parts[3].widget.wrong[0].value', round(v1 / v9, 2))
E('problems', 'items[2].parts[0].widget.answer', round(ops.corridor_value(0.6), 2))
adv0 = -8 - round(ops.corridor_value(0.6), 2)
E('problems', 'items[2].parts[1].widget.answer', round(adv0, 2))
term = round(adv0, 2) * 0.4
E('problems', 'items[2].parts[2].widget.answer', round(term, 2))
gap2 = math.log(1.5) + 2 * 0.01 * round(term, 2)
pn = 1 / (1 + math.exp(-gap2)); pn_exact = 1 / (1 + math.exp(-(math.log(1.5) + 2 * 0.01 * (-8 - ops.corridor_value(0.6)) * 0.4)))
C(round(pn, 4) == round(pn_exact, 4) == 0.607, 'new p 0.6070 from rounded and unrounded carries')
E('problems', 'items[2].parts[3].widget.answer', round(pn, 4))
E('problems', 'items[2].parts[3].widget.wrong[0].value', round(1 / (1 + math.exp(-(math.log(1.5) + 0.01 * round(term, 2)))), 4))

# the trainer's own loop, run as shipped with report() collecting the curve
tw = [w for w in widgets(lv.files['l16-a-policy-network'], []) if w['kind'] == 'trainer'][0]
curve = []
old = os.getcwd(); os.chdir(AI)
exec(tw['starter'], {'report': lambda step, loss, **kw: curve.append(loss), '__name__': '__main__'})
os.chdir(old)
C(len(curve) == 200 and curve[0] < 30 and min(curve[-20:]) > 32.5, f'trainer loop: 200 reports, first batch {curve[0]:.2f}, last 20 above 32.5')

lv.check_wrongs()
lv.report()
