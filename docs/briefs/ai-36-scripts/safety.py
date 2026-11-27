"""ai-safety numbers. Gridworld gaming (value iteration and Q-learning), best-of-n over-optimisation,
pass@k, red-team bounds, threshold decisions, weak-to-strong PGR."""
import numpy as np, math
from math import comb
from scipy import stats

# ---------- gridworld 5x5; start (4,0) bottom-left; goal (0,4) top-right (+10, terminal); coin (4,1) +1 on entry, respawns
R, Cc = 5, 5; START = (4, 0); GOAL = (0, 4); COIN = (4, 1); G = 0.95
ACTS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up down left right
def step(s, a):
    r, c = s; dr, dc = ACTS[a]; nr, nc = min(max(r+dr, 0), R-1), min(max(c+dc, 0), Cc-1); return (nr, nc)
def reward(s, a, s2, kind, phi=None):
    rw = 10.0 if s2 == GOAL else 0.0
    if kind == 'coin' and s2 == COIN and s != COIN: rw += 1.0
    if kind == 'shaped':   # coin replaced by potential-based shaping toward the goal
        rw += G*phi(s2)*(s2 != GOAL) - phi(s)
    return rw
states = [(r, c) for r in range(R) for c in range(Cc)]
def vi(kind, phi=None, iters=2000):
    V = {s: 0.0 for s in states}
    for _ in range(iters):
        V = {s: 0.0 if s == GOAL else max(reward(s, a, step(s, a), kind, phi) + G*V[step(s, a)]*(step(s, a) != GOAL) for a in range(4)) for s in states}
    pol = {s: int(np.argmax([reward(s, a, step(s, a), kind, phi) + G*V[step(s, a)]*(step(s, a) != GOAL) for a in range(4)])) for s in states}
    return V, pol
def rollout(pol, kind, n=40, phi=None):
    s = START; ret = 0; coins = 0; path = [s]
    for t in range(n):
        s2 = step(s, pol[s]); rw = reward(s, pol[s], s2, kind, phi); ret += G**t*rw; coins += (s2 == COIN); s = s2; path.append(s)
        if s == GOAL: return ret, t+1, coins, path
    return ret, None, coins, path
for kind in ['goal', 'coin']:
    V, pol = vi(kind); ret, T, coins, path = rollout(pol, kind)
    print('%s reward: V(start) %.4f, reaches goal in %s steps, coins in 40 steps %d, path start %s' % (kind, V[START], T, coins, path[:5]))
print('closed forms: loop value from the coin cell gamma/(1-gamma^2) = %.4f ; straight from coin cell 10*gamma^6 = %.4f' % (G/(1-G*G), 10*G**6))
print('V(start) coin world by closed form 1/(1-gamma^2) = %.4f' % (1/(1-G*G)))
phi = lambda s: -(abs(s[0]-GOAL[0]) + abs(s[1]-GOAL[1]))   # minus Manhattan distance
V, pol = vi('shaped', phi); ret, T, coins, path = rollout(pol, 'shaped', phi=phi)
print('potential-shaped: V(start) %.4f reaches goal in %s steps; goal-only V(start) 10*g^7 = %.4f; shaped V = goal-only V - phi(start) = %.4f' % (V[START], T, 10*G**7, 10*G**7 - phi(START)))
# Q-learning, seeded
def qlearn(kind, episodes=2000, alpha=0.5, eps=0.2, seed=0, maxlen=60):
    rng = np.random.default_rng(seed); Q = {s: np.zeros(4) for s in states}
    for _ in range(episodes):
        s = START
        for t in range(maxlen):
            a = rng.integers(4) if rng.random() < eps else int(np.argmax(Q[s]))
            s2 = step(s, a); rw = reward(s, a, s2, kind); done = s2 == GOAL
            Q[s][a] += alpha*(rw + (0 if done else G*Q[s2].max()) - Q[s][a]); s = s2
            if done: break
    return {s: int(np.argmax(Q[s])) for s in states}, Q
for kind in ['goal', 'coin']:
    for seed in [0, 1]:
        pol, Q = qlearn(kind, seed=seed); ret, T, coins, path = rollout(pol, kind)
        print('Q-learning %s seed %d: greedy reaches goal in %s steps, coins %d, Q(start) max %.3f' % (kind, seed, T, coins, Q[START].max()))

# ---------- best-of-n: KL and over-optimisation with a heavy-tailed proxy error
for n in [4, 16, 64]: print('best-of-%d KL = log n - (n-1)/n = %.4f' % (n, math.log(n) - (n-1)/n))
def bon_gold(n, err, seed, trials=20000):
    rng = np.random.default_rng(seed); g = rng.standard_normal((trials, n))
    e = rng.standard_normal((trials, n))*0.5 if err == 'normal' else stats.t.rvs(1.5, size=(trials, n), random_state=rng)*0.5
    p = g + e; return g[np.arange(trials), p.argmax(1)].mean(), p.max(1).mean()
for err in ['normal', 't']:
    row = []
    for n in [1, 4, 16, 64, 256, 1024]:
        g1, p1 = bon_gold(n, err, 0); g2, _ = bon_gold(n, err, 1); row.append('n=%d gold %.3f/%.3f proxy %.2f' % (n, g1, g2, p1))
    print(err, ' | '.join(row))
# closed form for normal error: E[g | p] = p * var(g)/var(p) = p/1.25 -> gold of best = E[max proxy]/1.25
print('normal error check: gold = proxy/1.25 for n=16: see proxy column')

# ---------- pass@k
def pass_at_k(n, c, k): return 1.0 if n - c < k else 1 - comb(n-c, k)/comb(n, k)
def pass_at_k_prod(n, c, k): return 1 - np.prod(1 - k/np.arange(n-c+1, n+1))
for n, c, k in [(20, 3, 1), (20, 3, 5), (20, 3, 10)]:
    print('pass@%d n=%d c=%d: %.5f (product form %.5f); naive 1-(1-c/n)^k %.5f' % (k, n, c, pass_at_k(n, c, k), pass_at_k_prod(n, c, k), 1-(1-c/n)**k))
# ---------- red teaming
for n in [300, 1000]:
    print('0 of %d: rule of three %.5f exact 95%% upper %.5f (beta %.5f)' % (n, 3/n, 1-0.05**(1/n), stats.beta.ppf(0.95, 1, n)))
print('P(at least one in 1000 tries at p=0.01) %.5f ; at 0.001 %.5f' % (1-0.99**1000, 1-0.999**1000))
# 4 successes in 500 attempts: Wilson and Clopper-Pearson
x, n = 4, 500; ph = x/n; z = 1.959964
w = (ph + z*z/(2*n) + np.array([-1, 1])*z*math.sqrt(ph*(1-ph)/n + z*z/(4*n*n)))/(1+z*z/n)
cp = stats.beta.ppf([0.025, 0.975], [x, x+1], [n-x+1, n-x])
print('4/500: Wilson %s Clopper-Pearson %s' % (np.round(w, 5), np.round(cp, 5)))
# ---------- threshold decision: 84 of 200 tasks vs threshold 50%
p = 84/200; se = math.sqrt(p*(1-p)/200)
print('84/200 = %.3f se %.4f one-sided 95%% upper %.4f ; exact CP upper %.4f' % (p, se, p+1.644854*se, stats.beta.ppf(0.95, 85, 116)))
print('with a 10-point elicitation margin: upper + 0.10 = %.4f' % (p+1.644854*se+0.10))
# ---------- debate halving
print('rounds to localise one wrong addend among 1024 by halving: %d' % math.ceil(math.log2(1024)))

# ---------- weak-to-strong
from sklearn.linear_model import LogisticRegression
def w2s(seed, systematic):
    rng = np.random.default_rng(seed); d = 20; n = 4000
    w = rng.normal(size=d); X = rng.normal(size=(3*n, d)); y = (X@w + 0.5*rng.normal(size=3*n) > 0).astype(int)
    Xa, ya, Xb, yb, Xt, yt = X[:n], y[:n], X[n:2*n], y[n:2*n], X[2*n:], y[2*n:]
    if systematic:
        weak = LogisticRegression(max_iter=1000).fit(Xa[:, :5], ya)          # sees 5 of 20 features
        wl = weak.predict(Xb[:, :5]); weak_acc = weak.score(Xt[:, :5], yt)
    else:
        acc_target = None
        flip = rng.random(n) < 0.25; wl = np.where(flip, 1-yb, yb)           # random label noise
        weak_acc = 0.75*1 + 0                                                # placeholder, replaced below
    strong = LogisticRegression(max_iter=1000).fit(Xb, wl); w2s_acc = strong.score(Xt, yt)
    ceil = LogisticRegression(max_iter=1000).fit(Xb, yb).score(Xt, yt)
    if not systematic:
        weak_acc = np.mean(wl == yb)   # the supervisor's own accuracy on the labels it gave
    return weak_acc, w2s_acc, ceil, (w2s_acc - weak_acc)/(ceil - weak_acc)
for systematic in [True, False]:
    for seed in [0, 1]:
        print('w2s %s seed %d: weak %.4f w2s %.4f ceiling %.4f PGR %.3f' % ('systematic' if systematic else 'random-noise', seed, *w2s(seed, systematic)))
