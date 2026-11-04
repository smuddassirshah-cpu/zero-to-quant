"""Exam 3.2, measure-prob items. Run with PYTHONPATH=pylib."""
import math, itertools
import numpy as np
from scipy import integrate, stats
from fractions import Fraction as F

out = {}
rng = np.random.default_rng(321)

# M1: atoms of sigma(A,B,C) on {1..9}
Om = set(range(1, 10)); A = {1, 2, 3, 4}; B = {3, 4, 5, 6}; C = {6, 7}
sig = {}
for w in Om: sig[w] = (w in A, w in B, w in C)
atoms = {}
for w, key in sig.items(): atoms.setdefault(key, set()).add(w)
k = len(atoms)
A1 = 2**k
# B: close the family under complement and union by brute force
fam = {frozenset(), frozenset(Om), frozenset(A), frozenset(B), frozenset(C)}
changed = True
while changed:
    changed = False
    for s in list(fam):
        c = frozenset(Om - s)
        if c not in fam: fam.add(c); changed = True
    for s, t in itertools.combinations(list(fam), 2):
        u = s | t
        if u not in fam: fam.add(u); changed = True
assert len(fam) == A1 == 64, (len(fam), k)
out['M1'] = dict(atoms=k, key=A1, wrong=dict(generators=2**3, powerset=2**9))

# M2: which families on {a,b,c,d} are sigma-algebras
Om2 = frozenset('abcd')
def fs(*sets): return {frozenset(s) for s in sets}
fams = {
 'F1': fs('', 'abcd', 'a', 'bcd'),
 'F2': fs('', 'abcd', 'a', 'b'),
 'F3': fs('', 'abcd', 'ab', 'cd', 'a', 'bcd'),
 'F4': fs('', 'abcd', 'ab', 'cd', 'ac', 'bd'),
 'F5': {frozenset(s) for r in range(5) for s in itertools.combinations('abcd', r)},
 'F6': fs('', 'abcd', 'ab'),
}
def is_sigma(f):
    if Om2 not in f: return False
    if any(Om2 - s not in f for s in f): return False
    return all(s | t in f for s, t in itertools.combinations(f, 2))
res2 = {k: is_sigma(v) for k, v in fams.items()}
assert res2 == dict(F1=True, F2=False, F3=False, F4=False, F5=True, F6=False), res2
out['M2'] = dict(key='F1, F5')

# M3: tail formula  P(X>t)=1 (t<2), (2/t)^3 (t>=2): E = 3
A3 = 2 + integrate.quad(lambda t: (2/t)**3, 2, math.inf)[0]
# B: density route: X has atom-free density 24/x^4 on [2, inf)?  P(X>t)=(2/t)^3 -> pdf 3*8/t^4 ; E = int x * 24/x^4 dx
B3 = integrate.quad(lambda x: x*24/x**4, 2, math.inf)[0]
assert abs(A3 - 3) < 1e-9 and abs(B3 - 3) < 1e-9
U = rng.random(4_000_000); X = 2/U**(1/3)   # inverse cdf: P(X>t) = (2/t)^3
assert abs(X.mean() - 3) < 0.03, X.mean()
out['M3'] = dict(key=3, wrong=dict(drop_flat_part=1, forget_half=4))

# M4: limit and expectation, X_n on U ~ U(0,1)
nn = 2000
# a: n 1{U<1/n^2}: E = 1/n -> 0, limit 0  ; b: n^2 1{U<1/n^2}: E = 1 , limit 0 ; c: U^n: E = 1/(n+1) -> 0
# d: n U^n : E = n/(n+1) -> 1, limit 0 ; e: min(n, 1/U): E = 1 + ln n -> inf, limit 1/U with E = inf
Ea = nn*(1/nn**2); Eb = nn**2*(1/nn**2); Ec = 1/(nn+1); Ed = integrate.quad(lambda u: nn*u**nn, 0, 1)[0]
Ee = integrate.quad(lambda u: min(nn, 1/u), 0, 1, points=[1/nn], limit=200)[0]
assert abs(Ea - 1/nn) < 1e-12 and Eb == 1 and abs(Ed - nn/(nn+1)) < 1e-9
assert abs(Ee - (1 + math.log(nn))) < 1e-6
out['M4'] = dict(key='a, c, e', wrong='b (mean 1, limit 0), d (mean -> 1, limit 0)')

# M5: Var(E[X|G]) fair die, G = sigma({1,2,3,4},{5},{6})
blocks = [{1, 2, 3, 4}, {5}, {6}]
pm = [F(len(b), 6) for b in blocks]; cm = [F(sum(b), len(b)) for b in blocks]
mean = sum(p*m for p, m in zip(pm, cm)); assert mean == F(7, 2)
A5 = sum(p*(m - mean)**2 for p, m in zip(pm, cm))
within = sum(p*F(sum((x - m)**2 for x in b), len(b)) for p, m, b in zip(pm, cm, blocks))
tot = F(35, 12); assert A5 + within == tot
# B: sampling
x = rng.integers(1, 7, 3_000_000)
g = np.where(x <= 4, 2.5, x.astype(float))
assert abs(g.var() - float(A5)) < 0.01
out['M5'] = dict(key=A5, float=float(A5), wrong=dict(within=float(within), total=float(tot)))

# M6: table adapted / predictable (reasoned): rows
out['M6'] = dict(rows=[('H_n = S_{n-1}', 'yes', 'yes'), ('H_n = S_n', 'yes', 'no'),
                       ('H_n = 1 if xi_{n+1} = +1 else 0', 'no', 'no'), ('H_n = max(S_0..S_{n-1})', 'yes', 'yes'),
                       ('H_n = 1 if S_n > 0 else 0', 'yes', 'no')])

# M7: optional stopping.  p = 0.4 up. M_n = (0.6/0.4)^{S_n} martingale. hit +3 before -2
p = 0.4; r = (1-p)/p
Pup = (1 - r**-2)/(r**3 - r**-2)
# B: exact by gambler's-ruin linear system on states -2..3
st = list(range(-2, 4)); idx = {s: i for i, s in enumerate(st)}
Mx = np.zeros((6, 6)); rhs = np.zeros(6)
for s in st:
    i = idx[s]
    if s in (-2, 3):
        Mx[i, i] = 1; rhs[i] = 1 if s == 3 else 0
    else:
        Mx[i, i] = 1; Mx[i, idx[s+1]] = -p; Mx[i, idx[s-1]] = -(1-p)
sol = np.linalg.solve(Mx, rhs)
assert abs(sol[idx[0]] - Pup) < 1e-12
# fair-walk slip and p-slip
out['M7'] = dict(key=Pup, wrong=dict(fair=2/5, p_as_hit=p, ratio_inverted=(1 - r**2)/(r**-3 - r**2)))

# M9: importance weight, theta = 2.5, x = 3.6
th, xx = 2.5, 3.6
A9 = math.exp(-th*xx + th**2/2)
phi = lambda z: math.exp(-z*z/2)/math.sqrt(2*math.pi)
B9 = phi(xx)/phi(xx - th)
assert abs(A9 - B9) < 1e-15
out['M9'] = dict(key=A9, wrong=dict(inverted=math.exp(th*xx - th**2/2), no_half_theta_sq=math.exp(-th*xx)))

# M10: die with Q
Q = [F(35, 100), F(25, 100), F(15, 100), F(10, 100), F(10, 100), F(5, 100)]
assert sum(Q) == 1
Z = [6*q for q in Q]
EQ2 = sum(q*f*f for q, f in zip(Q, range(1, 7)))
EP_Z_X2 = sum(F(1, 6)*z*f*f for z, f in zip(Z, range(1, 7)))
assert EQ2 == EP_Z_X2 == F(86, 10)
EQ = sum(q*f for q, f in zip(Q, range(1, 7)))
EP2 = F(91, 6)
out['M10'] = dict(Z=[float(z) for z in Z], key=float(EQ2), EQ=float(EQ), wrong=dict(EP=float(EP2), mean_sq=float(EQ**2)))

# M11: two-step tree, S0=60, u=1.25, d=0.85, r=0.04, call K=60
S0, u, d, rr, K = 60, 1.25, 0.85, 0.04, 60
q = (1 + rr - d)/(u - d)
pp = 0.6
payoff = lambda s: max(s - K, 0)
Vu = [payoff(S0*u*u), payoff(S0*u*d), payoff(S0*d*d)]
price = (q*q*Vu[0] + 2*q*(1-q)*Vu[1] + (1-q)**2*Vu[2])/(1+rr)**2
# B: backward induction
V1u = (q*payoff(S0*u*u) + (1-q)*payoff(S0*u*d))/(1+rr)
V1d = (q*payoff(S0*u*d) + (1-q)*payoff(S0*d*d))/(1+rr)
price_b = (q*V1u + (1-q)*V1d)/(1+rr)
assert abs(price - price_b) < 1e-12
# C: replicating portfolio cost
Du = (payoff(S0*u*u) - payoff(S0*u*d))/(S0*u*(u-d));
wrong_p = (pp**2*Vu[0] + 2*pp*(1-pp)*Vu[1] + (1-pp)**2*Vu[2])/(1+rr)**2
wrong_nodisc = price*(1+rr)**2
# discounted martingale check
assert abs(((q*S0*u + (1-q)*S0*d)/(1+rr)) - S0) < 1e-12
out['M11'] = dict(q=q, price=price, wrong=dict(p_used=wrong_p, no_discount=wrong_nodisc))

if __name__ == '__main__':
    for k_, v in out.items(): print(k_, v)
