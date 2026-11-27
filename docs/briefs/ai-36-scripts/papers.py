"""ai-papers numbers: phase diagram (n=2, m=1), Chinchilla Approach 3 on synthetic data, seeds and error bars."""
import numpy as np, math, itertools
from scipy import optimize, stats
from toy import train, eval_loss

# ---- compute-optimal allocation from published Approach 3 constants (quoted from Hoffmann et al. 2022)
E, A, B, al, be = 1.69, 406.4, 410.7, 0.3392, 0.2849
def nopt(C, A=A, B=B, al=al, be=be):
    G = (al*A/(be*B))**(1/(al+be)); return G*(C/6)**(be/(al+be))
def nopt_numeric(C):
    f = lambda logN: A/np.exp(logN)**al + B/(C/6/np.exp(logN))**be
    r = optimize.minimize_scalar(f, bounds=(np.log(1e6), np.log(1e14)), method='bounded', options={'xatol': 1e-10})
    return np.exp(r.x)
C = 5.76e23
n1, n2 = nopt(C), nopt_numeric(C)
print('Approach 3 constants: a = beta/(alpha+beta) = %.4f' % (be/(al+be)))
print('C=5.76e23: N_opt %.4g (closed) %.4g (numeric); D_opt %.4g; tokens per param %.2f' % (n1, n2, C/6/n1, C/6/n1/n1))
L = lambda N, D: E + A/N**al + B/D**be
print('loss at 70e9, 1.4e12: %.4f ; at 280e9, 300e9: %.4f' % (L(70e9, 1.4e12), L(280e9, 300e9)))
print('check 6ND: 6*70e9*1.4e12 = %.4g ; 6*280e9*300e9 = %.4g' % (6*70e9*1.4e12, 6*280e9*300e9))

# ---- synthetic grid: losses from the published constants plus noise; fit Approach 3 with Huber on log loss
rng = np.random.default_rng(2026)
Ns = np.array([1e7, 3e7, 1e8, 3e8, 1e9]); Ds = np.array([2e8, 6e8, 2e9, 6e9, 2e10])
grid = np.array([(N, D) for N in Ns for D in Ds])
y = np.array([L(N, D) for N, D in grid])*np.exp(rng.normal(0, 0.01, len(grid)))
def huber(r, d=1e-3):
    a = np.abs(r); return np.where(a <= d, 0.5*r*r, d*(a-0.5*d))
def obj(p, X, y):
    a, b, e, alp, bet = p
    pred = np.logaddexp.reduce([a - alp*np.log(X[:, 0]), b - bet*np.log(X[:, 1]), np.full(len(X), e)], axis=0)
    return huber(pred - np.log(y)).sum()
best = None
for a0, b0, e0, al0, be0 in itertools.product([0, 5, 10], [0, 5, 10], [-1, 0.5], [0.2, 0.5], [0.2, 0.5]):
    r = optimize.minimize(obj, [a0, b0, e0, al0, be0], args=(grid, y), method='L-BFGS-B')
    if best is None or r.fun < best.fun: best = r
a_, b_, e_, al_, be_ = best.x
print('fit (L-BFGS-B, Huber 1e-3, 72 starts): E %.4f A %.1f B %.1f alpha %.4f beta %.4f' % (np.exp(e_), np.exp(a_), np.exp(b_), al_, be_))
# second method: nonlinear least squares on log loss from the true point
def resid(p): a, b, e, alp, bet = p; return np.logaddexp.reduce([a - alp*np.log(grid[:, 0]), b - bet*np.log(grid[:, 1]), np.full(len(grid), e)], axis=0) - np.log(y)
r2 = optimize.least_squares(resid, [np.log(A), np.log(B), np.log(E), al, be])
print('fit (least_squares from truth): E %.4f A %.1f B %.1f alpha %.4f beta %.4f' % (np.exp(r2.x[2]), np.exp(r2.x[0]), np.exp(r2.x[1]), r2.x[3], r2.x[4]))
print("a from Huber fit %.4f, from least squares %.4f" % (be_/(al_+be_), r2.x[4]/(r2.x[3]+r2.x[4])))

# ---- phase diagram, n=2 features, m=1 hidden; feature 0 importance 1, feature 1 importance r
def classify(W):
    w = W[0]
    big = np.abs(w) > 0.5
    if big.all() and np.sign(w[0]) != np.sign(w[1]): return 'superposed'
    if big[1] and not big[0]: return 'feature-2-only'
    if big[0] and not big[1]: return 'feature-1-only'
    return 'other'
cells = [(1.0, 0.0), (1.0, 0.5), (1.0, 0.9), (1.0, 0.99), (0.1, 0.9), (0.1, 0.99), (3.0, 0.0), (3.0, 0.9)]
for r_, S in cells:
    I = np.array([1.0, r_])
    out = []
    for seed in range(4):
        W, b = train(2, 1, S, I, steps=3000, seed=seed); out.append((eval_loss(W, b, 2, S, I), classify(W), np.round(W[0], 3)))
    out.sort(key=lambda t: t[0])
    print('r=%.1f S=%.2f best: %s %s loss %.5f | seeds: %s' % (r_, S, out[0][1], out[0][2], out[0][0], [o[1] for o in out]))

# ---- seeds and error bars (ai-papers L3): accuracy of two methods over 5 paired seeds
a = np.array([71.2, 72.5, 70.8, 73.1, 71.9]); b = np.array([72.0, 73.6, 71.1, 74.0, 72.3])
d = b - a
print('mean A %.3f B %.3f diff %.3f' % (a.mean(), b.mean(), d.mean()))
se_pair = d.std(ddof=1)/np.sqrt(5); t_pair = d.mean()/se_pair
se_unp = np.sqrt(a.var(ddof=1)/5 + b.var(ddof=1)/5)
print('paired se %.4f t %.3f p %.4f | scipy %s' % (se_pair, t_pair, 2*stats.t.sf(t_pair, 4), stats.ttest_rel(b, a)))
print('unpaired se %.4f t %.3f | scipy welch %s' % (se_unp, d.mean()/se_unp, stats.ttest_ind(b, a, equal_var=False)))
print('P(at least one false win in 20 benchmarks at 5%%) %.4f ; Bonferroni level %.4f' % (1-0.95**20, 0.05/20))
# benchmark standard error: 1,000 items at 72% accuracy
print('se of 72%% on 1000 items %.4f ; on 200 items %.4f' % (math.sqrt(.72*.28/1000), math.sqrt(.72*.28/200)))
