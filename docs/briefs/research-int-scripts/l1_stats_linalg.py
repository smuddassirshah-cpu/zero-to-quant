"""research-int level 1: l1 two regressions, l2 correlation limits, l3 estimators, l4 tests, l5 matrices."""
import math, sys
from fractions import Fraction as F
import numpy as np
from scipy import integrate, stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from chk import two, done, Phi

# ---------- l1 ----------
# (a) population-style example: sx=2, sy=3, r=0.6
sx, sy, r = 2.0, 3.0, 0.6
byx, bxy = r*sy/sx, r*sx/sy
two("l1 b_yx hand", byx, 0.9); two("l1 b_xy hand", bxy, 0.4); two("l1 product = r^2", byx*bxy, r*r)
# method B: build a sample with exactly these moments, then polyfit both ways
rng = np.random.default_rng(1); n = 200
z = rng.standard_normal((n, 2)); z -= z.mean(0)
q, _ = np.linalg.qr(z)            # orthonormal columns, mean zero
q *= math.sqrt(n-1)               # unit sample variance, zero sample correlation
x = sx*q[:, 0]; y = sy*(r*q[:, 0] + math.sqrt(1-r*r)*q[:, 1])
two("l1 polyfit y on x", np.polyfit(x, y, 1)[0], 0.9, 1e-9)
two("l1 polyfit x on y", np.polyfit(y, x, 1)[0], 0.4, 1e-9)
two("l1 slope of x-on-y line drawn in (x,y) plane = 1/b_xy", 1/np.polyfit(y, x, 1)[0], 2.5, 1e-9)
two("l1 geometric mean of 0.9 and 2.5 = sy/sx", math.sqrt(0.9*2.5), 1.5)
# (b) possible pairs: (0.5,1.2) possible, (0.8,1.5) not
two("l1 product 0.5*1.2", 0.5*1.2, 0.6); print("     r from 0.6 =", round(math.sqrt(0.6), 4), "; 0.8*1.5 =", 0.8*1.5, "> 1 impossible")
# (c) eight-point dataset for the scatter hook
X = [1, 2, 3, 4, 5, 6, 7, 8]; Y = [2, 1, 4, 3, 7, 5, 8, 9]
n8 = 8; mx = F(sum(X), n8); my = F(sum(Y), n8)
Sxx = sum((F(a)-mx)**2 for a in X); Syy = sum((F(b)-my)**2 for b in Y); Sxy = sum((F(a)-mx)*(F(b)-my) for a, b in zip(X, Y))
print("     8-pt: Sxx", Sxx, "Syy", Syy, "Sxy", Sxy, "b_yx", Sxy/Sxx, "b_xy", Sxy/Syy, "r^2", Sxy**2/(Sxx*Syy))
res = sm.OLS(Y, sm.add_constant(X)).fit(); res2 = sm.OLS(X, sm.add_constant(Y)).fit()
two("l1 8pt b_yx", float(Sxy/Sxx), res.params[1]); two("l1 8pt b_xy", float(Sxy/Syy), res2.params[1])
two("l1 8pt R2 y on x", float(Sxy**2/(Sxx*Syy)), res.rsquared); two("l1 8pt R2 x on y", float(Sxy**2/(Sxx*Syy)), res2.rsquared)
print("     8pt intercepts y on x:", float(my - Sxy/Sxx*mx), "x on y:", float(mx - Sxy/Syy*my), " means", mx, my)
# (d) duplicated data, n = 10
rng = np.random.default_rng(7); xd = np.arange(1, 11, dtype=float); yd = np.round(2 + 0.8*xd + rng.normal(0, 2, 10), 1)
r1 = sm.OLS(yd, sm.add_constant(xd)).fit(); r2 = sm.OLS(np.r_[yd, yd], sm.add_constant(np.r_[xd, xd])).fit()
two("l1 dup slope unchanged", r1.params[1], r2.params[1]); two("l1 dup R2 unchanged", r1.rsquared, r2.rsquared)
two("l1 se ratio (n=10) = sqrt((n-2)/(2n-2)) = 2/3", math.sqrt((10-2)/(2*10-2)), r2.bse[1]/r1.bse[1])
two("l1 t ratio = 3/2", 1.5, r2.tvalues[1]/r1.tvalues[1])
print("     dup data y:", list(yd), "slope", round(r1.params[1], 4), "t", round(r1.tvalues[1], 3), "->", round(r2.tvalues[1], 3), "p", round(r1.pvalues[1], 5), "->", round(r2.pvalues[1], 6))
# (e) attenuation: var(x)=4, noise var 1
fac = 4/(4+1); two("l1 attenuation factor", fac, 0.8)
z = rng.standard_normal((400, 2)); z -= z.mean(0); q, _ = np.linalg.qr(z); q *= math.sqrt(399)
xt = 2*q[:, 0]; e = 1*q[:, 1]; yt = 2*xt
two("l1 slope y on (x+e), true slope 2", np.polyfit(xt+e, yt, 1)[0], 2*fac, 1e-9)

# ---------- l2 ----------
def rng3(a, b):
    h = math.sqrt((1-a*a)*(1-b*b)); return a*b-h, a*b+h
def numeric_range(a, b):
    cs = np.round(np.arange(-1, 1.00001, 1e-4), 4); ok = []
    for c in cs:
        R = np.array([[1, a, c], [a, 1, b], [c, b, 1]])
        if np.linalg.eigvalsh(R)[0] >= -1e-10: ok.append(c)
    return min(ok), max(ok)
for a, b in [(0.8, 0.8), (0.9, 0.9), (0.9, -0.9), (0.6, 0.8), (0.5, 0.5), (0.0, 0.0), (0.7, 0.7)]:
    lo, hi = rng3(a, b); nlo, nhi = numeric_range(a, b); hi = min(hi, 1.0)
    two(f"l2 range lo a={a} b={b}", round(lo, 4), nlo, 2e-4); two(f"l2 range hi a={a} b={b}", round(hi, 4), nhi, 2e-4)
det = lambda a, b, c: 1+2*a*b*c-a*a-b*b-c*c
two("l2 det(0.9,0.9,-0.5)", det(0.9, 0.9, -0.5), np.linalg.det(np.array([[1, .9, -.5], [.9, 1, .9], [-.5, .9, 1]])), 1e-12)
print("     min eig of (0.9,0.9,-0.5):", round(np.linalg.eigvalsh(np.array([[1, .9, -.5], [.9, 1, .9], [-.5, .9, 1]]))[0], 4))
for n in (3, 4, 5, 10):
    rho = -1/(n-1); R = (1-rho)*np.eye(n)+rho*np.ones((n, n))
    two(f"l2 equicorr n={n} min rho -1/(n-1) gives min eig 0", float(np.linalg.eigvalsh(R)[0]), 0.0, 1e-12)
two("l2 equicorr n=3 rho range lo -1/2", -1/(3-1), -0.5)
two("l2 equicorr eigenvalue 1+2rho at rho=0.4 (n=3)", 1+2*0.4, float(np.linalg.eigvalsh((0.6)*np.eye(3)+0.4*np.ones((3, 3)))[-1]))
# transitivity blurt: 0.9, 0.9 -> not >= 0.81
print("     0.9,0.9 low end", round(rng3(0.9, 0.9)[0], 4))

# ---------- l3 ----------
th, n = 10.0, 9
Emax = n*th/(n+1); Vmax = n*th**2/((n+1)**2*(n+2)); Vunb = th**2/(n*(n+2)); mse_max = 2*th**2/((n+1)*(n+2))
dens = lambda m: n*m**(n-1)/th**n
qE = integrate.quad(lambda m: m*dens(m), 0, th)[0]; qV = integrate.quad(lambda m: (m-qE)**2*dens(m), 0, th)[0]
two("l3 E[max]", Emax, qE); two("l3 Var[max]", Vmax, qV, 1e-9)
two("l3 bias of max", Emax-th, -1.0)
two("l3 Var unbiased (n+1)/n*max", Vunb, ((n+1)/n)**2*qV, 1e-9)
two("l3 MSE of max", mse_max, qV+(qE-th)**2, 1e-9)
two("l3 Var of 2*xbar", th**2/(3*n), 4*(th**2/12)/n)
sim = np.random.default_rng(3).uniform(0, th, (400000, n)).max(1)
two("l3 sim E[max] (tol .01)", Emax, float(sim.mean()), 0.01); two("l3 sim Var[max] (tol .01)", Vmax, float(sim.var()), 0.01)
# divisor MSE for the sample variance, n=10, sigma^2=1
nn = 10; k = nn-1
for d in (9, 10, 11):
    hand = (2*k+(k-d)**2)/d**2
    quad = integrate.quad(lambda s: (s/d-1)**2*stats.chi2.pdf(s, k), 0, np.inf)[0]
    two(f"l3 MSE divisor {d}", round(hand, 6), round(quad, 6), 1e-6)
# shrunk coin
def mse_binom(p, nn, f):
    ks = np.arange(nn+1); w = stats.binom.pmf(ks, nn, p); return float((w*(f(ks)-p)**2).sum())
for p in (0.5, 0.9):
    hand_plain = p*(1-p)/10; bias = (10*p+1)/12-p; var = 10*p*(1-p)/144
    two(f"l3 coin p={p} MSE k/n", hand_plain, mse_binom(p, 10, lambda k: k/10), 1e-12)
    two(f"l3 coin p={p} MSE (k+1)/(n+2)", bias**2+var, mse_binom(p, 10, lambda k: (k+1)/12), 1e-12)
    print(f"     p={p}: bias {bias:.5f} var {var:.6f}")
two("l3 E[1/xbar] n=5 lam=2 -> n/(n-1)*lam", 5/4*2, float(stats.gamma(a=5, scale=1/(5*2)).expect(lambda t: 1/t)), 1e-7)
print("     k=10 of 10: plain", 1.0, "shrunk", round(11/12, 4))

# ---------- l4 ----------
z = (60-50)/5
two("l4 z=2 two-sided p (normal)", 2*(1-Phi(2)), 2*stats.norm.sf(2), 1e-12); print("     p", round(2*stats.norm.sf(2), 5))
pe = 2*stats.binom.sf(59, 100, 0.5); print("     exact binomial two-sided p", round(pe, 5), " one-sided", round(stats.binom.sf(59, 100, .5), 5))
two("l4 exact two-sided p, hand sum of pmf", sum(math.comb(100, k) for k in range(60, 101))*2/2**100, pe, 1e-12)
# power: sigma=1, n=25, effect 0.5, alpha .05 two sided
se = 1/5; crit = 1.959964*se; delta = 0.5
pw_hand = (1-Phi((crit-delta)/se)) + Phi((-crit-delta)/se)
pw_lib = stats.norm.sf(1.959964-delta/se) + stats.norm.cdf(-1.959964-delta/se)
two("l4 power n=25 effect 0.5", pw_hand, pw_lib, 1e-9); print("     power", round(pw_lib, 4))
sims = np.random.default_rng(5).normal(delta, 1, (200000, 25)).mean(1)/se
two("l4 power sim (tol .004)", pw_lib, float((np.abs(sims) > 1.959964).mean()), 0.004)
# n needed for power 0.8 at effect 0.5: n = ((1.96+0.8416)/0.5)^2
nreq = ((1.959964+0.841621)/0.5)**2; print("     n for 80% power, effect .5:", round(nreq, 2), "-> 32")
pw32 = stats.norm.sf(1.959964-0.5*math.sqrt(32)) + stats.norm.cdf(-1.959964-0.5*math.sqrt(32)); print("     power at n=32", round(pw32, 4))
two("l4 P(>=1 false positive in 20 at 5%)", 1-0.95**20, 1-stats.binom.pmf(0, 20, 0.05), 1e-12); print("     ", round(1-0.95**20, 4))
sim20 = (np.random.default_rng(9).random((200000, 20)) < .05).any(1).mean(); two("l4 sim (tol .005)", 1-0.95**20, float(sim20), 0.005)
two("l4 Bonferroni level for 20", 0.05/20, 0.0025)
P = [0.001, 0.008, 0.012, 0.03, 0.2]; m = 5
bonf = sum(p <= 0.05/m for p in P)
srt = sorted(P); holm = 0
for i, p in enumerate(srt):
    if p <= 0.05/(m-i): holm += 1
    else: break
bh = max([i+1 for i, p in enumerate(srt) if p <= (i+1)/m*0.05] or [0])
two("l4 Bonferroni rejects", bonf, int(multipletests(P, 0.05, "bonferroni")[0].sum()))
two("l4 Holm rejects", holm, int(multipletests(P, 0.05, "holm")[0].sum()))
two("l4 BH rejects", bh, int(multipletests(P, 0.05, "fdr_bh")[0].sum()))
print("     reject counts Bonf/Holm/BH:", bonf, holm, bh)
p3 = 2*(1-Phi(3)); two("l4 p of t=3", p3, 2*stats.norm.sf(3), 1e-12); print("     p", round(p3, 5), " x50 =", round(50*p3, 4), " Sidak:", round(1-(1-p3)**50, 4))
two("l4 Sharpe 1 over 4 years t", 1*math.sqrt(4), 2.0)

# ---------- l5 ----------
def eigs(A): return np.round(np.linalg.eigvalsh(np.array(A, float)), 6)
J4 = np.ones((4, 4)); print("     J4 eig", eigs(J4)); two("l5 J4 top eig = n", 4.0, eigs(J4)[-1]); two("l5 J4 rest zero", 0.0, abs(eigs(J4)[:3]).max())
u = np.array([1, 2, 2.0]); A = np.outer(u, u); two("l5 uu^T top eig = |u|^2", 9.0, eigs(A)[-1]); print("     uu^T eig", eigs(A))
n, rho = 5, 0.3; R = (1-rho)*np.eye(n)+rho*np.ones((n, n)); e = eigs(R)
two("l5 equicorr top 1+(n-1)rho", 2.2, e[-1]); two("l5 equicorr rest 1-rho", 0.7, e[0]); two("l5 det", 2.2*0.7**4, float(np.linalg.det(R)), 1e-12); print("     det", round(2.2*0.7**4, 5))
two("l5 sum sq eig = sum sq entries", 2.2**2+4*0.7**2, float((R**2).sum()), 1e-12); print("     sum sq", round((R**2).sum(), 4))
u2, v2 = np.array([1, 2.0]), np.array([3, 4.0]); M = np.outer(u2, v2); ev = np.sort(np.linalg.eigvals(M).real)
two("l5 uv^T eig = v.u", 11.0, ev[-1]); two("l5 uv^T other = 0", 0.0, ev[0], 1e-12)
S = np.array([[2, 1], [1, 2.0]]); two("l5 [[a,b],[b,a]] eig a+b", 3.0, eigs(S)[-1]); two("l5 a-b", 1.0, eigs(S)[0]); two("l5 sum sq entries 10 = 9+1", 10.0, (eigs(S)**2).sum())
w = np.array([3, 4.0]); Pj = np.outer(w, w)/25; print("     proj eig", eigs(Pj)); two("l5 proj trace = rank = 1", 1.0, float(np.trace(Pj)))
H = np.eye(3)-2*np.outer([1, 2, 2.0], [1, 2, 2.0])/9; print("     reflection eig", eigs(H))
two("l5 reflection trace = n-2", 1.0, float(np.trace(H)))
print("     rotation 90deg eig", np.linalg.eigvals(np.array([[0, -1], [1, 0.0]])))
two("l5 eig of I - (1/n)J, n=4 : 1 (x3), 0", 3.0, float((np.abs(np.linalg.eigvalsh(np.eye(4)-np.ones((4, 4))/4)-1) < 1e-9).sum()))

# ---------- l1 hook dataset (five points, neat numbers) ----------
X5 = [1, 2, 3, 4, 5]; Y5 = [2, 6, 4, 10, 8]
mx5, my5 = F(sum(X5), 5), F(sum(Y5), 5)
sxx = sum((F(a)-mx5)**2 for a in X5); syy = sum((F(b)-my5)**2 for b in Y5); sxy = sum((F(a)-mx5)*(F(b)-my5) for a, b in zip(X5, Y5))
print("     5pt hand: means", mx5, my5, "Sxx", sxx, "Syy", syy, "Sxy", sxy, "b_yx", sxy/sxx, "b_xy", sxy/syy, "r^2", sxy*sxy/(sxx*syy))
a1 = sm.OLS(Y5, sm.add_constant(X5)).fit(); a2 = sm.OLS(X5, sm.add_constant(Y5)).fit()
two("l1 5pt b_yx 1.6", float(sxy/sxx), a1.params[1]); two("l1 5pt b_xy 0.4", float(sxy/syy), a2.params[1])
two("l1 5pt R2 both 0.64", float(sxy*sxy/(sxx*syy)), a1.rsquared); two("l1 5pt R2 x on y", a1.rsquared, a2.rsquared)
two("l1 5pt intercept y on x 1.2", float(my5 - sxy/sxx*mx5), a1.params[0]); two("l1 5pt intercept x on y 0.6", float(mx5 - sxy/syy*my5), a2.params[0])
two("l1 5pt x-on-y line slope in (x,y) plane 2.5", 1/0.4, 1/a2.params[1])
two("l1 5pt sy/sx 2", math.sqrt(float(syy/sxx)), 2.0)
two("l1 5pt r", float(sxy)/math.sqrt(float(sxx*syy)), 0.8)
done()
