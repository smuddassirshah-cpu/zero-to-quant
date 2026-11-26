#!/usr/bin/env python3
"""Concept audit, round 2: markov levels 4 and 5.

Independent recomputation and Monte Carlo checks of the claims in
l13 to l22, review-4/5, homework-4/5 and problems-4/5.
Exits 0 when every check passes. A check that fails because the content
is wrong stays failing and is a finding in docs/reviews/audit-markov-4-5-r2.md.
NOTE lines are evidence for `imprecise` findings and do not fail the script.

Run from anywhere: python docs/reports/markov-L4-5-concepts-r2.py
"""
import json, math, os, sys, random
from fractions import Fraction as F
from itertools import product
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'markov')
def load(name):
    with open(os.path.join(ROOT, name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)

FAILS = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ((' | ' + detail) if detail else ''))
    if not ok:
        FAILS.append(name)
def note(msg):
    print('NOTE ' + msg)
def close(a, b, tol):
    return abs(a - b) <= tol
def text_of(o):
    return json.dumps(o, ensure_ascii=False)

def stationary(P):
    P = np.asarray(P, float); n = len(P)
    A = np.vstack([P.T - np.eye(n), np.ones(n)])
    b = np.zeros(n + 1); b[-1] = 1
    return np.linalg.lstsq(A, b, rcond=None)[0]

def screens(doc):
    return doc.get('screens', []) + doc.get('quiz', []) + doc.get('items', [])
def by_title(doc, title):
    return next(s for s in doc['screens'] if s.get('title') == title)
def by_id(doc, i):
    return next(s for s in screens(doc) if s.get('id') == i)
def slips(w):
    return {x['id']: x['value'] for x in w.get('wrong', [])}

rng = np.random.default_rng(20261126)

# ---------------------------------------------------------------- l13
l13 = load('l13-balanced-flows')
P = [[.7, .3, 0, 0], [.5, .2, .3, 0], [0, .5, .2, .3], [0, 0, .5, .5]]
pi = stationary(P)
check('l13 inventory pi by solving piP=pi equals balance weights', np.allclose(pi, np.array([1, .6, .36, .216]) / 2.176, atol=1e-9))
check('l13 key P(2 or 3 lots)', close(pi[2] + pi[3], by_title(l13, 'Normalise')['widget']['answer'], 5e-4))
C = np.array([[0, .8, .2], [.2, 0, .8], [.8, .2, 0]])
piC = stationary(C)
check('l13 cycle: uniform stationary, flows 0.267 v 0.067, so not reversible',
      np.allclose(piC, 1 / 3) and close(piC[0] * C[0, 1], .2667, 1e-3) and close(piC[1] * C[1, 0], .0667, 1e-3))
Q = [[.7, .3, 0, 0], [.6, .1, .3, 0], [0, .6, .1, .3], [0, 0, .6, .4]]
check('l13 order queue pi0 = 8/15', close(stationary(Q)[0], by_title(l13, 'An order queue')['widget']['answer'], 1e-3))
w = by_id(l13, 'q-find-reverse')['widget']
check('l13 q-find-reverse key and slips', close(.5 * .2 / .3, w['answer'], 1e-3) and close(.3 * .2 / .5, slips(w)['inverted'], 1e-3) and close(.5 * .3 * .2, slips(w)['tiny'], 1e-3))
# detailed balance sufficient, not necessary: MC of the reversal formula on the cycle (homework-4 h-time-reversal)
n = 400000
x = np.empty(n, int); x[0] = rng.integers(3); u = rng.random(n)
for t in range(1, n):
    x[t] = (x[t - 1] + 1) % 3 if u[t] < .8 else (x[t - 1] - 1) % 3
today_B = x[1:] == 1
est = np.mean(x[:-1][today_B] == 0)
hw4 = load('homework-4')
check('hw4 time reversal: P(yesterday A | today B) = pi_A P_AB / pi_B = 0.8 (MC %.4f)' % est,
      close(est, .8, .006) and close(by_id(hw4, 'h-time-reversal')['widget']['answer'], .8, 1e-9))

# ---------------------------------------------------------------- l14
l14 = load('l14-walks-on-networks')
def walk_matrix(n, edges):
    W = np.zeros((n, n))
    for a, b, wt in edges:
        W[a, b] += wt; W[b, a] += wt
    return W / W.sum(1, keepdims=True), W.sum(1)
Pv, deg = walk_matrix(4, [(0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 2, 1)])   # A B C D
check('l14 pi = deg / 2|E| on the venue network', np.allclose(stationary(Pv), deg / deg.sum()))
def mean_return(Pm, i):
    n = len(Pm); idx = [k for k in range(n) if k != i]
    A = np.eye(n - 1) - Pm[np.ix_(idx, idx)]
    h = np.linalg.solve(A, np.ones(n - 1))
    return 1 + Pm[i, idx] @ h
check('l14 mean return to D is 8 by first-step solve (Kac)', close(mean_return(Pv, 3), 8, 1e-9))
Pw, st = walk_matrix(3, [(0, 1, 1), (1, 2, 2), (0, 2, 3)])
check('l14 weighted return to B is 4', close(mean_return(Pw, 1), by_title(l14, 'Links with strengths')['widget']['answer'], 1e-9))
def board_graph(moves):
    idx = {(r, c): r * 8 + c for r in range(8) for c in range(8)}
    A = np.zeros((64, 64))
    for (r, c), i in idx.items():
        for dr, dc in moves:
            if (r + dr, c + dc) in idx:
                A[i, idx[(r + dr, c + dc)]] = 1
    return A
KN = board_graph([(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)])
check('l14 knight: degrees add to 336, corner return 168, centre 42',
      KN.sum() == 336 and close(mean_return(KN / KN.sum(1, keepdims=True), 0), 168, 1e-6) and close(mean_return(KN / KN.sum(1, keepdims=True), 27), 42, 1e-6))
if '168 legal moves from square to square' in text_of(l14):
    note('l14 "168 legal moves from square to square": 168 is the count of unordered pairs (links); ordered moves number %d' % int(KN.sum()))
KG = board_graph([(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)])
check('hw4 king: degrees add to 420, corner return 140', KG.sum() == 420 and close(mean_return(KG / KG.sum(1, keepdims=True), 0), 140, 1e-6))
SQ, _ = walk_matrix(4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)])
check('l14 square: P^1001[A,A] = 0, yet time share 1/4 (periodic, no convergence)',
      np.linalg.matrix_power(SQ, 1001)[0, 0] == 0 and close(np.linalg.matrix_power(SQ, 1000)[0, 0], .5, 1e-9))
if 'strengths add to $2|E|$' in text_of(l14):
    note('l14 code explain: with weights the strengths add to twice the total link strength, not 2|E|')

# ---------------------------------------------------------------- l15
l15 = load('l15-sampling-by-chain')
grid = [.40, .45, .50, .55, .60, .65, .70]
wts = np.array([p ** 12 * (1 - p) ** 8 for p in grid])
post = wts / wts.sum()
def metropolis_P(w):
    k = len(w); M = np.zeros((k, k))
    for i in range(k):
        for j in (i - 1, i + 1):
            if 0 <= j < k:
                M[i, j] = .5 * min(1, w[j] / w[i])
        M[i, i] = 1 - M[i].sum()
    return M
MP = metropolis_P(wts)
canvasP = np.array(by_title(l15, 'A chain you can watch')['canvas']['params']['P'])
check('l15 canvas P equals the Metropolis matrix', np.abs(canvasP - MP).max() < 6e-4)
check('l15 Metropolis chain is stationary at the posterior and satisfies detailed balance',
      np.allclose(post @ MP, post) and np.allclose(post[:, None] * MP, (post[:, None] * MP).T))
check('l15 first key w(.65)/w(.60)', close(wts[5] / wts[4], by_title(l15, 'One step by hand')['widget']['answer'], 2e-3))
d = lambda k: np.linalg.matrix_power(MP, k)[0, 0]
first = next(k for k in range(1, 60) if d(k) < .06)
check('l15 forgetting: d(5)=%.3f d(10)=%.3f first below 0.06 at k=%d' % (d(5), d(10), first),
      close(d(5), .187, 1.5e-3) and close(d(10), .099, 1.5e-3) and abs(first - by_title(l15, 'Forgetting the start')['widget']['answer']) <= 1)
ev = np.sort(np.abs(np.linalg.eigvals(MP)))[::-1]
half = math.log(2) / -math.log(ev[1])
check('l15 "halves about every five steps": half-life %.2f steps' % half, 4 <= half <= 6)
check('l15 posterior mean 0.578 and P(p>0.5) = 0.7301', close(post @ grid, .578, 5e-4) and close(post[3:].sum(), .7301, 1e-4))
move = post @ (1 - np.diag(MP))
check('l15 "moved on 79%% of its steps": stationary move share %.4f' % move, close(move, .79, .006))
AA = np.zeros((7, 7))
for i in range(7):
    for j in (i - 1, i + 1):
        if 0 <= j < 7: AA[i, j] = .5
    AA[i, i] = 1 - AA[i].sum()
check('l15 always-accept chain is uniform', np.allclose(stationary(AA), 1 / 7))
jump = post * (1 - np.diag(MP)); jump /= jump.sum()
check('hw4 longform: move-only record shares, mean and tail',
      np.allclose(jump, [.027, .081, .145, .212, .243, .207, .086], atol=1.5e-3) and close(jump @ grid, .5764, 3e-4) and close(jump[3:].sum(), .747, 1e-3))
# expected average of the first 200 steps from 0.40, and of steps 21..200
dist = np.zeros(7); dist[0] = 1; tot = 0; tot_late = 0
for t in range(1, 201):
    dist = dist @ MP; tot += dist @ grid
    if t > 20: tot_late += dist @ grid
check('hw4 longform: first 200 steps average %.4f, steps 21 to 200 average %.4f' % (tot / 200, tot_late / 180),
      close(tot / 200, .5721, 2e-4) and close(tot_late / 180, .5776, 2e-4))
# Monte Carlo: many chains in parallel
def run_chains(nchains, steps, start, record=False):
    s = np.full(nchains, start); visits = np.zeros((nchains, 7)); hist = [] if record else None
    logw = np.log(wts)
    for _ in range(steps):
        prop = s + np.where(rng.random(nchains) < .5, 1, -1)
        ok = (prop >= 0) & (prop < 7)
        pc = np.clip(prop, 0, 6)
        acc = ok & (np.log(rng.random(nchains)) < logw[pc] - logw[s])
        s = np.where(acc, pc, s)
        visits[np.arange(nchains), s] += 1
        if record: hist.append((s.copy(), acc.copy()))
    return visits, hist
vis, _ = run_chains(300, 100000, 0)
err = np.abs(vis / 100000 - post).max(1)
check('l15 "100,000 steps agree to about 0.003": median max error %.4f, 90th pct %.4f over 300 runs' % (np.median(err), np.quantile(err, .9)),
      .0015 <= np.median(err) <= .006)
check('l15 ergodic theorem: time average of p over 100,000 steps within 0.004 of 0.578 in 95%+ of runs',
      np.mean(np.abs((vis / 100000) @ grid - .578) < .004) > .95)
# homework-4 longform sampling sds: 20 chains of 200 steps from 0.40
reps = 3000
vis2, hist = run_chains(reps * 20, 200, 0, record=True)
g = np.array(grid)
full = (vis2 @ g / 200).reshape(reps, 20).mean(1)
states = np.stack([h[0] for h in hist]); accs = np.stack([h[1] for h in hist])
late = g[states[20:]].mean(0).reshape(reps, 20).mean(1)
mv_sum = (g[states] * accs).sum(0).reshape(reps, 20).sum(1); mv_n = accs.sum(0).reshape(reps, 20).sum(1)
her = mv_sum / mv_n
print('     hw4 MC: all-step mean %.4f sd %.4f | steps 21-200 mean %.4f sd %.4f | her move-only pooled mean %.4f sd %.4f'
      % (full.mean(), full.std(), late.mean(), late.std(), her.mean(), her.std()))
check('hw4 longform: corrected estimate (burn-in 20) has mean 0.5776 and sd about 0.005', close(late.mean(), .5776, 4e-4) and .0035 <= late.std() <= .0065)
check('hw4 longform: "sampling sd of her mean is about 0.004"', .003 <= her.std() <= .0055 or .003 <= full.std() <= .0055)
w = by_title(l15, 'An unfair proposal')['widget']
check('l15 Hastings key 9/14 and slips', close(3 * .3 / (2 * .7), w['answer'], 2e-3) and close(.3 / .7, slips(w)['q-only'], 2e-3) and close(3 * .7 / (2 * .3), slips(w)['flip'], .01))
# dropping rejected steps on the 2-value chain gives 1/2; ergodic theorem on a periodic chain
check('l15 move-only record on weights (1,3) is half H', close((.75 * (1 / 6)) / (.75 * (1 / 6) + .25 * .5), .5, 1e-12))

# ---------------------------------------------------------------- l16
l16 = load('l16-arrivals')
pois = lambda k, m: math.exp(-m) * m ** k / math.factorial(k)
check('l16 Poisson keys', close(pois(0, 2), .1353, 5e-4) and close(pois(5, 6), .1606, 5e-4) and close(pois(0, 6), .0025, 3e-4) and close(pois(0, 1), .3679, 1e-3) and close(pois(0, 5), .0067, 3e-4))
T = 200000.0
tb = np.cumsum(rng.exponential(1 / 5, int(T * 5 * 1.1))); tb = tb[tb < T]
isbuy = rng.random(len(tb)) < .6
mins = tb.astype(int)
buys = np.bincount(mins[isbuy], minlength=int(T)); sells = np.bincount(mins[~isbuy], minlength=int(T))
corr = np.corrcoef(buys, sells)[0, 1]
m_hi = sells[buys >= 5].mean(); m_lo = sells[buys == 0].mean()
check('l16 thinning: buys and sells independent (corr %.4f; mean sells %.3f when buys>=5, %.3f when buys=0)' % (corr, m_hi, m_lo),
      abs(corr) < .01 and abs(m_hi - 2) < .03 and abs(m_lo - 2) < .06)
t2 = np.cumsum(rng.exponential(.5, 2400000)); fixed = rng.uniform(1000, t2[-1] - 1000, 200000)
j = np.searchsorted(t2, fixed)
gap = t2[j] - t2[j - 1]
check('l16 inspection paradox: typical gap %.3f, gap containing a fixed time %.3f' % (np.diff(t2).mean(), gap.mean()),
      close(np.diff(t2).mean(), .5, .003) and close(gap.mean(), 1.0, .01))
# conditional uniformity (quiz, hw4): given 3 arrivals in [0,3], first before 1 with chance 19/27
cnt = 0; hit = 0
arr = rng.exponential(.5, (600000, 12)).cumsum(1)
n3 = (arr < 3).sum(1) == 3
check('hw4 first of three before time 1: MC %.4f v 19/27' % np.mean(arr[n3, 0] < 1), close(np.mean(arr[n3, 0] < 1), 19 / 27, .006))
seq = rng.random((400000, 80)) < .6                       # True = buy
sells_c = (~seq).cumsum(1); third = (sells_c == 3).argmax(1)   # index of the third sell
has3 = sells_c[:, -1] >= 3
check('hw4 exactly 2 buys before the third sell: MC %.4f v 0.13824' % np.mean(third[has3] == 4), close(np.mean(third[has3] == 4), .13824, .003))
if 'Poisson' not in by_id(l16, 'q-varying-rate')['prose']:
    note('l16 q-varying-rate: the prose never says the arrivals are Poisson, yet the feedback says the count is Poisson')

# ---------------------------------------------------------------- l17, l18
urn = {}
def polya(r, b, n, pr):
    if n == 0:
        urn[F(r, r + b)] = urn.get(F(r, r + b), 0) + pr; return
    polya(r + 1, b, n - 1, pr * F(r, r + b)); polya(r, b + 1, n - 1, pr * F(b, r + b))
polya(1, 1, 3, F(1))
check('l17 Polya urn after three draws: 1/5..4/5 each with chance 1/4', urn == {F(k, 5): F(1, 4) for k in range(1, 5)})
check('l17 fair price chance 4/9; contract 20', F(4, 9) * 125 + F(5, 9) * 80 == 100 and close(.6 * 20 + .4 * 70, 40, 1e-12))
drift = lambda f, s, n, p: p * f(s + 1, n + 1) + (1 - p) * f(s - 1, n + 1) - f(s, n)
p6 = F(3, 5)
ok = all(drift(lambda s, n: s * s - n, s, n, F(1, 2)) == 0 and drift(lambda s, n: F(2, 3) ** s, s, n, p6) == 0
         and drift(lambda s, n: (s - n * F(1, 5)) ** 2 - F(24, 25) * n, s, n, p6) == 0
         and drift(lambda s, n: s ** 3 - 3 * n * s, s, n, F(1, 2)) == 0 for s in range(-6, 7) for n in range(6))
check('l18 hidden martingales pass the one-step test; (3/2)^S grows by 7/6', ok and drift(lambda s, n: F(3, 2) ** s, 0, 0, p6) == F(1, 6))
check('l18 sd of S_100^2 is about 141', close(math.sqrt(2 * 100 ** 2 - 2 * 100), 141, 1))
check('l18 E[r^S10] = 1 by the binomial sum', sum(math.comb(10, k) * p6 ** k * (1 - p6) ** (10 - k) * F(2, 3) ** (2 * k - 10) for k in range(11)) == 1)

# ---------------------------------------------------------------- l19
l19 = load('l19-optional-stopping')
def ruin(i, N, p):
    """Chance of N before 0 and expected duration, by solving the first-step equations exactly."""
    p = F(p); q = 1 - p; n = N - 1
    def solve(rhs_const, bN):
        A = [[F(0)] * n for _ in range(n)]; b = [F(rhs_const)] * n
        for k in range(1, N):
            A[k - 1][k - 1] = F(1)
            if k + 1 < N: A[k - 1][k] = -p
            else: b[k - 1] += p * bN
            if k - 1 > 0: A[k - 1][k - 2] = -q
        for c in range(n):                       # Gaussian elimination
            piv = next(r for r in range(c, n) if A[r][c] != 0)
            A[c], A[piv] = A[piv], A[c]; b[c], b[piv] = b[piv], b[c]
            for r in range(n):
                if r != c and A[r][c] != 0:
                    f = A[r][c] / A[c][c]
                    A[r] = [x - f * y for x, y in zip(A[r], A[c])]; b[r] -= f * b[c]
        return [b[r] / A[r][r] for r in range(n)]
    return solve(0, 1)[i - 1], solve(1, 0)[i - 1]
cases = {(3, 10, F(1, 2)): (F(3, 10), F(21)), (2, 5, F(1, 2)): (F(2, 5), F(6)), (2, 4, F(3, 5)): (F(9, 13), F(50, 13)),
         (5, 10, F(2, 5)): (F(32, 275), F(211, 11)), (3, 10, F(3, 5)): (F(41553, 58025), F(48291, 2321))}
check('l19 ruin chances and durations agree with first-step solves (optional stopping gives the same)',
      all(ruin(*k) == v for k, v in cases.items()))
P49, T49 = ruin(50, 100, F(49, 100))
check('l19 p=0.49, 50 of 100: P=%.4f, E[T]=%.1f' % (P49, T49), close(float(P49), .1192, 5e-5) and close(float(T49), 1904.1, .06))
# the trap screen says 23 of 200 reached 100 and the stopped average is 11.75; that needs an unfinished game at 8,000 bets
dist = np.zeros(101); dist[50] = 1.0
for _ in range(8000):
    new = np.zeros(101); new[0] = dist[0]; new[100] = dist[100]
    new[2:101] += .49 * dist[1:100]; new[0:99] += .51 * dist[1:100]
    dist = new
unfinished = dist[1:100].sum()
txt = text_of(by_title(l19, 'The wrong martingale'))
if '11.75' in txt and '23 of 200' in txt:
    note('l19 trap: 23 of 200 at 100 gives an average of 11.50, not 11.75, unless a game is still running at bet 8,000 '
         '(chance per game %.4f, so %.2f such games expected in 200); the text does not say so' % (unfinished, 200 * unfinished))
# Wald for the die game
tot = 0; games = 200000
rolls = rng.integers(1, 7, (games, 120))
firstsix = (rolls == 6).argmax(1)
tot = np.where(np.arange(120)[None, :] <= firstsix[:, None], rolls, 0).sum(1).mean()
check('l19 Wald, die until first 6: MC total %.3f v 21' % tot, close(tot, 21, .15))
# Wald needs identically distributed (or bounded) steps: independent mean-0 steps +-2^(n-1), stop at the first win
wins = rng.random((games, 60)) < .5; fw = wins.argmax(1)
ST = 2.0 ** fw - (2.0 ** fw - 1)
note('l19 Wald as stated ("independent steps with mean mu, T with finite mean"): doubling stakes are independent mean-0 steps, '
     'E[T] = %.3f, yet E[S_T] = %.3f, not 0. The identity needs identically distributed (or bounded) steps.' % ((fw + 1).mean(), ST.mean()))
w = by_title(l19, 'An unfair game')['widget']
r = F(3, 2)
check('l19 unfair key 32/275 and flip slip', (1 - r ** 5) / (1 - r ** 10) == F(32, 275) and close(float((1 - (1 / r) ** 5) / (1 - (1 / r) ** 10)), slips(w)['flip'], 5e-4))
# sampling error claim on the duration screen: sd of S_T^2 - T over 300 games
def ruin_mc(i, N, p, games):
    s = np.full(games, i); t = np.zeros(games, int); live = np.ones(games, bool)
    while live.any():
        step = np.where(rng.random(games) < p, 1, -1)
        s = np.where(live, s + step, s); t += live
        live &= (s > 0) & (s < N)
    return s, t
s, t = ruin_mc(3, 10, .5, 100000)
se300 = (s * s - t).std() / math.sqrt(300)
check('l19 duration screen: mean T %.2f; 12.1 is within sampling error of 9 (se over 300 games %.2f)' % (t.mean(), se300),
      close(t.mean(), 21, .3) and abs(12.1 - 9) < 2 * se300)

# ---------------------------------------------------------------- l20
l20 = load('l20-when-stopping-fails')
qf = math.comb(100, 50) / 2 ** 100
w = by_title(l20, 'A cap on time')['widget']['rows']
check('l20 cap at 100: fail chance %.4f, mean when failing %.2f' % (qf, -(1 - qf) / qf), close(qf, w[0][1]['answer'], 5e-4) and close(-(1 - qf) / qf, w[1][1]['answer'], .01))
# exact DP for the capped rule: E[S_T] = 0
dist = {0: F(1)}; reached = F(0)
for _ in range(100):
    new = {}
    for sv, pr in dist.items():
        for tv in (sv + 1, sv - 1):
            if tv == 1: reached += pr / 2
            else: new[tv] = new.get(tv, 0) + pr / 2
    dist = new
check('l20 bounded stop keeps the mean: E[S_T] = 0 exactly at cap 100', reached + sum(k * v for k, v in dist.items()) == 0 and reached == 1 - F(math.comb(100, 50), 2 ** 100))
ev = lambda d, p: 1 - 2 ** d * (1 - F(p)) ** d
check('l20 doubling: fair 0, wheel d=10 %.4f, d=7 %.4f, falls as d grows' % (ev(10, F(18, 37)), ev(7, F(18, 37))),
      ev(10, F(1, 2)) == 0 and close(float(ev(10, F(18, 37))), -.3056, 5e-5) and close(float(ev(7, F(18, 37))), -.2052, 5e-5)
      and all(ev(d + 1, F(18, 37)) < ev(d, F(18, 37)) for d in range(1, 15)))
check('l20 one fair cycle has sd about 32', close(math.sqrt(1023 / 1024 + 1023 ** 2 / 1024), 32, .1))
check('review-5 doubling 8 bets at 0.48', close(float(ev(8, F(48, 100))), -.3686, 5e-5))
# floor at -L: chance L/(L+1), E[T] = L; chart with 1,000 bets shows E[min(T,1000)]
def floor_dp(L, cap):
    d = np.zeros(L + 2); d[L] = 1.0; et = 0.0
    for _ in range(cap):
        et += d[1:L + 1].sum()
        new = np.zeros(L + 2); new[0] = d[0]; new[L + 1] = d[L + 1]
        new[2:L + 2] += .5 * d[1:L + 1]; new[0:L] += .5 * d[1:L + 1]
        d = new
    return d[L + 1], et, d[1:L + 1].sum()
up9, et9, _ = floor_dp(9, 20000)
up99, et99, live99 = floor_dp(99, 1000)
check('l20 floor at -9: chance of +1 is 0.9 and E[T] = 9', close(up9, .9, 1e-9) and close(et9, 9, 1e-6))
print('     l20 floor at -99 with the chart capped at 1,000 bets: E[min(T,1000)] = %.1f, %.2f%% of games still running' % (et99, 100 * live99))
check('l20 "at L = 99 the batch shows only about 40": truncated mean is far below 99', 25 <= et99 <= 60)

# ---------------------------------------------------------------- l21
def wait(pattern, probs):
    """Expected wait by first-step analysis on the prefix automaton (exact)."""
    m = len(pattern); letters = list(probs)
    def nxt(k, c):
        s = pattern[:k] + c
        while not pattern.startswith(s): s = s[1:]
        return len(s)
    A = [[F(0)] * m for _ in range(m)]; b = [F(1)] * m
    for k in range(m):
        A[k][k] += 1
        for c in letters:
            j = nxt(k, c)
            if j < m: A[k][j] -= F(probs[c])
    for c in range(m):
        piv = next(r for r in range(c, m) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]; b[c], b[piv] = b[piv], b[c]
        for r in range(m):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]; b[r] -= f * b[c]
    return b[0] / A[0][0]
fair = {'H': F(1, 2), 'T': F(1, 2)}
exp = {'H': 2, 'HT': 4, 'HH': 6, 'HHT': 8, 'HTH': 10, 'THT': 10, 'HHH': 14, 'HTHT': 20, 'HHHH': 30, 'HTHH': 18}
check('l21 fair-coin waits by first-step analysis match the casino rule', all(wait(k, fair) == v for k, v in exp.items()))
b6 = {'H': F(3, 5), 'T': F(2, 5)}
check('l21/review/homework biased waits', wait('HH', {'H': F(2, 3), 'T': F(1, 3)}) == F(15, 4) and wait('HT', b6) == F(25, 6)
      and wait('HTH', b6) == F(155, 18) and close(float(wait('HHH', b6)), 9.07, .005)
      and wait('LLL', {'L': F(2, 5), 'W': F(3, 5)}) == F(195, 8) and wait('LL', {'L': F(3, 10), 'W': F(7, 10)}) == F(130, 9)
      and close(float(wait('LWL', {'L': F(3, 10), 'W': F(7, 10)})), 19.2063, 1e-4))
check('l21 ABRACADABRA wait by first-step solve over 11 states', wait('ABRACADABRA', {c: F(1, 26) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}) == 26 ** 11 + 26 ** 4 + 26 == 3670344487444778)
fl = rng.random((200000, 150)) < .5
def first_time(bits, pat):
    m = len(pat); hitm = np.ones((bits.shape[0], bits.shape[1] - m + 1), bool)
    for k, c in enumerate(pat):
        hitm &= bits[:, k:bits.shape[1] - m + 1 + k] == (c == 'H')
    return hitm.argmax(1) + m
a, b = first_time(fl, 'HTH').mean(), first_time(fl, 'HHT').mean()
check('l21 MC separates HTH (%.3f) from HHT (%.3f)' % (a, b), close(a, 10, .08) and close(b, 8, .08))
sl = slips(by_id(load('l21-waiting-for-patterns'), 'q-biased-ht')['widget'])
if close(sl.get('hh', 0), 4.4444, 1e-3):
    note('l21 q-biased-ht slip hh: feedback says "you used 0.6^2", which gives 1/0.36 = %.4f; the banded value 4.4444 is the full HH wait 1/0.36 + 1/0.6' % (1 / .36))

# ---------------------------------------------------------------- l22
l22 = load('l22-arrivals-fair-game')
sizes = np.array([100, 200, 500]); pr = np.array([.5, .3, .2])
EY, EY2 = sizes @ pr, sizes ** 2 @ pr
N = rng.poisson(20, 300000)
tot = np.array([0.0] * len(N))
draws = rng.choice(sizes, size=N.sum(), p=pr)
tot = np.bincount(np.repeat(np.arange(len(N)), N), weights=draws, minlength=len(N))
check('l22 compound Poisson: MC mean %.0f var %.0f v 4,200 and 1,340,000' % (tot.mean(), tot.var()),
      EY == 210 and EY2 == 67000 and close(tot.mean(), 4200, 10) and close(tot.var(), 1340000, 15000))
check('l22 "the mean alone is exceeded about half the time": P(S > 4200) = %.3f' % np.mean(tot > 4200), .42 <= np.mean(tot > 4200) <= .55)
check('l22 hedge sizing and slips', close(4200 + 2 * math.sqrt(1340000), 6515, 1) and close(4200 + 2 * math.sqrt(458000), 5554, 2))
I = rng.poisson(4, 500000)
check('l22 E[(N5-10)^2 | N3=4] = 8 (MC %.3f)' % np.mean((4 + I - 10.0) ** 2), close(np.mean((4 + I - 10.0) ** 2), 8, .05))
T3 = rng.exponential(.5, (300000, 3)).sum(1)
check('l22 optional stopping at the third trade: E[N_T - 2T] = %.4f, E[T3] = %.3f' % (3 - 2 * T3.mean(), T3.mean()), close(T3.mean(), 1.5, .01))
if 't$ lots a minute' in text_of(by_title(l22, 'Net inventory')['explain']):
    check('l22 net inventory explain: mean rate is 1 lot a minute (text says "t lots a minute")', False,
          'rate = lambda E[Y] = 5 x 0.2 = 1 lot a minute; the mean after t minutes is t lots')
r5 = load('review-5')
check('review-5 claims sd', close(math.sqrt(30 * 5e6), by_id(r5, 'r-claims-sd')['widget']['answer'], 1))

# ---------------------------------------------------------------- homework-5 and problems
z = .8; steps = rng.random((300000, 200)) < .5
pos = np.where(steps, 1, -1).cumsum(1); Thit = (np.abs(pos) == 2).argmax(1) + 1
check('hw5 E[0.8^T] for the first hit of +-2: MC %.4f v 8/17' % np.mean(z ** Thit), close(np.mean(z ** Thit), 8 / 17, .003))
side = pos[np.arange(len(pos)), Thit - 1]
check('hw5 S_T independent of T by symmetry (corr %.4f)' % np.corrcoef(side, Thit)[0, 1], abs(np.corrcoef(side, Thit)[0, 1]) < .01)
Pl = np.zeros((6, 6)); Pl[0, 0] = Pl[5, 5] = 1
for k in range(1, 5): Pl[k, k + 1], Pl[k, k - 1], Pl[k, k] = .3, .2, .5
check('hw5 lazy walk reaches 5 before 0 from 2 with chance 135/211', close(np.linalg.matrix_power(Pl, 20000)[2, 5], 135 / 211, 1e-9))
r = F(9, 11); Ph = (1 - r ** 4) / (1 - r ** 10)
check('hw5 unfair ruin 0.55, 4 of 10', ruin(4, 10, F(55, 100)) == (Ph, (10 * Ph - 4) / F(1, 10)) and close(float(Ph), .6376, 5e-5))
r = F(11, 9)
check('p5 signal trial 24381/51001 and duration', ruin(3, 5, F(45, 100))[0] == F(24381, 51001) and close(float(ruin(3, 5, F(45, 100))[1]), 6.0975, 1e-4))
# print shop: reflecting at 0, absorbed at 7, from 2
A = np.zeros((7, 7)); bT = np.ones(7); bZ = np.zeros(7); bZ[0] = 1
for k in range(7):
    A[k, k] = 1
    if k == 0: A[0, 1] -= 1
    else:
        A[k, k - 1] -= .5
        if k + 1 < 7: A[k, k + 1] -= .5
check('p5 print shop: E[T] = 45 and E[idle hours] = 5 by first-step solves', close(np.linalg.solve(A, bT)[2], 45, 1e-9) and close(np.linalg.solve(A, bZ)[2], 5, 1e-9))
# problems-4
Ps, dg = walk_matrix(5, [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (1, 2, 1)])   # H A B C D
adj = (Ps > 0)
def mh(accept):
    M = np.zeros((5, 5))
    for i in range(5):
        for jx in range(5):
            if adj[i, jx]: M[i, jx] = accept(i, jx) / dg[i]
        M[i, i] = 1 - M[i].sum()
    return M
Mu = mh(lambda i, jx: min(1, dg[i] / dg[jx])); Mi = mh(lambda i, jx: 1 / dg[i])
check('p4 survey: MH test deg(i)/deg(j) gives uniform, stay chances 0, .25, .25, .75, .75, repeats 0.4; 1/deg(i) gives H 16/26',
      np.allclose(stationary(Mu), .2) and np.allclose(np.diag(Mu), [0, .25, .25, .75, .75]) and close(stationary(Mi)[0], 16 / 26, 1e-9))
# taxi rank: continuous-time simulation, share of passengers who find the rank empty
ev_t = rng.random(2000000) < .6; lvl = 0; empty = 0; npass = 0
for is_taxi in ev_t:
    if is_taxi: lvl = min(3, lvl + 1)
    else:
        npass += 1
        if lvl == 0: empty += 1
        else: lvl -= 1
check('p4 taxi rank: share of passengers finding it empty, MC %.4f v 8/65' % (empty / npass), close(empty / npass, 8 / 65, .002))
wr = np.array([2., 5, 3]); qr = np.array([[0, 1, 0], [.3, 0, .7], [0, 1, 0]])
def mh_q(hastings):
    M = np.zeros((3, 3))
    for i in range(3):
        for jx in range(3):
            if qr[i, jx] > 0:
                ratio = wr[jx] * qr[jx, i] / (wr[i] * qr[i, jx]) if hastings else wr[jx] / wr[i]
                M[i, jx] = qr[i, jx] * min(1, ratio)
        M[i, i] = 1 - M[i].sum()
    return M
Mh, Mp = mh_q(True), mh_q(False)
check('p4 regime sampler: Hastings chain hits (0.2,0.5,0.3) with 10% rejections; plain rule gives Mid 50/77',
      np.allclose(stationary(Mh), [.2, .5, .3]) and close(np.array([.2, .5, .3]) @ np.diag(Mh), .1, 1e-9) and close(stationary(Mp)[1], 50 / 77, 1e-9))
Pb, db = walk_matrix(6, [(0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1)])
check('p4 payment audits: pi_D = 3/14, return to F 14, 17 hours', close(stationary(Pb)[3], 3 / 14, 1e-9) and close(mean_return(Pb, 5), 14, 1e-9)
      and math.ceil(7 * math.log(10)) == 17 and 1 - math.exp(-16 / 7) < .9)

print()
print('%d failing check(s)%s' % (len(FAILS), (': ' + '; '.join(FAILS)) if FAILS else ''))
sys.exit(1 if FAILS else 0)
