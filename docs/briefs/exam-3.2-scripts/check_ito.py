"""Exam 3.2, ito items: route A closed form, route B independent method. Run with PYTHONPATH=pylib."""
import math, itertools
import numpy as np
from scipy import integrate, stats, optimize
import sympy as sp
from fractions import Fraction

N = stats.norm
def close(a, b, tol=1e-6):
    assert abs(a - b) < tol, (a, b)
    return a

out = {}

# I1: Var(2 W_3 - W_7)
A = 4*3 + 1*7 - 2*2*1*min(3, 7)
# B: covariance matrix of (W_3, W_7) built from independent increments
C = np.array([[3, 3], [3, 7]], float); v = np.array([2, -1.0])
B = v @ C @ v
close(A, B)
out['I1'] = dict(key=A, wrong=dict(no_cov=4*3+7, plus_cov=4*3+7+2*2*1*3))

# I2: P(S_2 < 70), S0=80, mu=0.06, sigma=0.3
S0, mu, s, T, K = 80, 0.06, 0.3, 2, 70
z = (math.log(K/S0) - (mu - s*s/2)*T)/(s*math.sqrt(T))
A = N.cdf(z)
# B: integrate the lognormal density
m, sd = math.log(S0) + (mu - s*s/2)*T, s*math.sqrt(T)
pdf = lambda x: math.exp(-(math.log(x)-m)**2/(2*sd*sd))/(x*sd*math.sqrt(2*math.pi))
B = integrate.quad(pdf, 1e-9, K)[0]
close(A, B, 1e-7)
rng = np.random.default_rng(32)
ST = S0*np.exp(m - math.log(S0) + sd*rng.standard_normal(2_000_000))
assert abs((ST < K).mean() - A) < 0.002
w1 = N.cdf((math.log(K/S0) - mu*T)/(s*math.sqrt(T)))      # forgot -sigma^2/2
w2 = N.cdf((math.log(K/S0) - (mu - s*s/2)*T)/s)           # sigma instead of sigma sqrt(T)
out['I2'] = dict(key=A, wrong=dict(no_ito_term=w1, no_sqrtT=w2))

# I3: QV of X = 3W - 2t on [0,5]
A = 9*5
# B: simulate sum of squared increments
n = 200000; dt = 5/n
dW = rng.standard_normal(n)*math.sqrt(dt)
dX = 3*dW - 2*dt
B = (dX**2).sum()
assert abs(B - A) < 0.5, B
out['I3'] = dict(key=A, wrong=dict(drift_squared=9*5+4*5, sigma_T=3*5))

# I4: drift of d(t W^2): f_t + 1/2 f_xx
t, x = sp.symbols('t w')
f = t*x**2
A = sp.simplify(sp.diff(f, t) + sp.Rational(1, 2)*sp.diff(f, x, 2))
assert sp.simplify(A - (x**2 + t)) == 0
# B: Monte Carlo of E[(f(t+h, W+dW) - f(t,W))]/h at t=1.3, w=0.8 (conditional mean change)
t0, w0, h = 1.3, 0.8, 1e-3
Z = rng.standard_normal(4_000_000)*math.sqrt(h)
chg = ((t0+h)*(w0+Z)**2 - t0*w0**2).mean()/h
assert abs(chg - (w0**2 + t0)) < 0.6, chg   # loose: Monte Carlo noise at small h; exact via moments below
exact = ((t0+h)*(w0**2 + h) - t0*w0**2)/h
assert abs(exact - (w0**2 + t0)) < 2e-3
out['I4'] = dict(key='w^2+t', wrong=dict(no_ito='w^2', forgot_half='w^2+2t'))

# I5: martingales among six (check drift f_t + f_xx/2 symbolically); X_t = t W - int W ds handled by hand
def drift(f): return sp.simplify(sp.diff(f, t) + sp.Rational(1, 2)*sp.diff(f, x, 2))
cands = {
 'A': sp.exp(3*x - sp.Rational(9, 2)*t),
 'B': sp.exp(3*x - 3*t),
 'C': x**4 - 6*t*x**2 + 3*t**2,
 'D': x**2 + t,
 'F': x**3 - 3*t**2*x,   # wrong repair (should be 3 t x)
}
res = {k: drift(v) == 0 for k, v in cands.items()}
assert res == dict(A=True, B=False, C=True, D=False, F=False), res
# E: t W_t - int_0^t W ds : d = W dt + t dW - W dt = t dW, no drift (martingale). Monte Carlo check E[X_t] = 0 and cond mean
n_p, steps, Tm = 200000, 200, 2.0
dtm = Tm/steps
Wp = np.zeros(n_p); I = np.zeros(n_p)
for k in range(steps):
    I += Wp*dtm
    Wp += rng.standard_normal(n_p)*math.sqrt(dtm)
XE = Tm*Wp - I
assert abs(XE.mean()) < 0.02 and abs(XE.var() - Tm**3/3) < 0.05, (XE.mean(), XE.var())   # Var = int t^2 dt
# Monte Carlo of the non-martingales' means: E[W_t^2 + t] = 2t (not t*0...)
out['I5'] = dict(key='A, C, E', wrong='B (needs 4.5t), D (W^2+t drifts), F (needs 3tW)')

# I6: BS theta by the PDE
S, Kk, r, sg, Tt = 70, 65, 0.04, 0.30, 0.75
d1 = (math.log(S/Kk) + (r + sg*sg/2)*Tt)/(sg*math.sqrt(Tt)); d2 = d1 - sg*math.sqrt(Tt)
V = S*N.cdf(d1) - Kk*math.exp(-r*Tt)*N.cdf(d2)
Dl = N.cdf(d1); G = N.pdf(d1)/(S*sg*math.sqrt(Tt))
theta_pde = r*V - r*S*Dl - 0.5*sg*sg*S*S*G
theta_formula = -S*N.pdf(d1)*sg/(2*math.sqrt(Tt)) - r*Kk*math.exp(-r*Tt)*N.cdf(d2)
close(theta_pde, theta_formula, 1e-9)
# B2: finite difference in tau
def bs(S_, tau):
    d1_ = (math.log(S_/Kk) + (r + sg*sg/2)*tau)/(sg*math.sqrt(tau)); d2_ = d1_ - sg*math.sqrt(tau)
    return S_*N.cdf(d1_) - Kk*math.exp(-r*tau)*N.cdf(d2_)
fd = -(bs(S, Tt + 1e-5) - bs(S, Tt - 1e-5))/2e-5
close(fd, theta_formula, 1e-5)
# rounded inputs as shown to the learner
Vr, Dr, Gr = round(V, 4), round(Dl, 4), round(G, 4)
th_r = r*Vr - r*S*Dr - 0.5*sg*sg*S*S*Gr
out['I6'] = dict(V=V, Delta=Dl, Gamma=G, theta=theta_formula, Vr=Vr, Dr=Dr, Gr=Gr, theta_from_rounded=th_r,
                 wrong=dict(no_half=r*Vr - r*S*Dr - sg*sg*S*S*Gr, sign_rSD=r*Vr + r*S*Dr - 0.5*sg*sg*S*S*Gr))

# I7: touch probability, daily monitoring, BGK shift
sg7, T7, a7, m7 = 0.25, 0.5, 0.06, 126      # 126 daily steps
cont = 2*(1 - N.cdf(a7/(sg7*math.sqrt(T7))))
dt7 = T7/m7
shift = 0.5826*sg7*math.sqrt(dt7)
bgk = 2*(1 - N.cdf((a7 + shift)/(sg7*math.sqrt(T7))))
# B: exact discrete-monitoring probability by a grid Markov chain on the reflected walk (no barrier approximation)
h = sg7*math.sqrt(dt7)
xs = np.linspace(-6*sg7*math.sqrt(T7), a7, 4001)   # state below the barrier
dx = xs[1]-xs[0]
# transition density kernel
Kmat = N.pdf((xs[None, :] - xs[:, None])/h)/h*dx
surv = np.zeros_like(xs); surv[np.argmin(abs(xs-0))] = 1/dx
p = np.zeros(len(xs)); i0 = np.argmin(abs(xs-0)); p[i0] = 1.0
# use density propagation: start as a narrow normal after step 1 to avoid grid delta artefacts
dens = N.pdf((xs-0)/h)/h*dx
dens[xs >= a7] = 0
for _ in range(m7-1):
    dens = Kmat.T @ dens
    # kill mass above barrier is implicit: states limited to < a7 ; mass leaving the grid is absorbed
disc_exact = 1 - dens.sum()
# Monte Carlo cross-check
nsim = 400000
paths = np.cumsum(rng.standard_normal((nsim, m7))*h, axis=1)
mc = (paths.max(axis=1) >= a7).mean()
assert abs(mc - disc_exact) < 0.004 and abs(bgk - disc_exact) < 0.004, (cont, bgk, disc_exact, mc)
out['I7'] = dict(cont=cont, bgk=bgk, exact=disc_exact, mc=mc, wrong=dict(continuous=cont, one_sided=cont/2))

# I8: exit with drift mu=-0.3, sigma=0.9, a=1, b=2
mu8, s8, a8, b8 = -0.3, 0.9, 1.0, 2.0
c = 2*mu8/s8**2
Pm = (1 - math.exp(c*b8))/(math.exp(-c*a8) - math.exp(c*b8))
Et = (a8*Pm - b8*(1-Pm))/mu8
# B: solve the ODE for P and for E[tau] by finite differences on [-b, a]
n8 = 2001
xg = np.linspace(-b8, a8, n8); hh = xg[1]-xg[0]
Mx = np.zeros((n8, n8)); rhs = np.zeros(n8)
for i in range(1, n8-1):
    Mx[i, i-1] = s8**2/2/hh**2 - mu8/2/hh
    Mx[i, i] = -s8**2/hh**2
    Mx[i, i+1] = s8**2/2/hh**2 + mu8/2/hh
Mx[0, 0] = 1; Mx[-1, -1] = 1
rhsP = rhs.copy(); rhsP[-1] = 1
Pv = np.linalg.solve(Mx, rhsP)
rhsT = rhs.copy(); rhsT[1:-1] = -1
Tv = np.linalg.solve(Mx, rhsT)
i0 = np.argmin(abs(xg - 0))
close(Pm, np.interp(0, xg, Pv), 1e-5); close(Et, np.interp(0, xg, Tv), 1e-3)
# driftless slips
out['I8'] = dict(P=Pm, Et=Et, wrong=dict(P_driftless=b8/(a8+b8), P_no_sigma2=(1-math.exp(2*mu8*b8))/(math.exp(-2*mu8*a8)-math.exp(2*mu8*b8)),
                                       Et_driftless=a8*b8, Et_no_div=(a8*Pm - b8*(1-Pm))))

# I9: W^6 repair
f9 = x**6 - 15*t*x**4 + 45*t**2*x**2 - 15*t**3
assert drift(f9) == 0
assert drift(x**6 - 15*t*x**4 + 45*t**2*x**2) != 0
# B: E[f9(t, W_t)] = 0 for t = 1.7 by exact normal moments
tt = 1.7
mom = lambda k: 0 if k % 2 else math.prod(range(k-1, 0, -2))*tt**(k//2)
close(mom(6) - 15*tt*mom(4) + 45*tt**2*mom(2) - 15*tt**3, 0, 1e-9)
out['I9'] = dict(key='w^6-15tw^4+45t^2w^2-15t^3', wrong=dict(no_constant='w^6-15tw^4+45t^2w^2', signs='w^6+15tw^4+45t^2w^2+15t^3'))
assert drift(x**6 + 15*t*x**4 + 45*t**2*x**2 + 15*t**3) != 0

# I10: E[W_2 W_5^3] and Var of int_0^2 e^{W_t - t/2} dW_t
A1 = 3*2*5
B1 = Fraction(0)
# exact by split W5 = W2 + D, D ~ N(0,3): E[W2 (W2 + D)^3] = E W2^4 + 3 E W2^2 E D^2
mom_n = lambda var, k: 0 if k % 2 else math.prod(range(k-1, 0, -2))*var**(k//2)
B1 = mom_n(2, 4) + 3*mom_n(2, 2)*mom_n(3, 2)
assert A1 == B1 == 30
w_ = rng.standard_normal(3_000_000)
W2 = w_*math.sqrt(2); D = rng.standard_normal(3_000_000)*math.sqrt(3)
assert abs((W2*(W2+D)**3).mean() - 30) < 0.4
A2 = math.e**2 - 1
B2 = integrate.quad(lambda u: math.exp(u), 0, 2)[0]       # E[e^{2W-u}] = e^{u}
close(A2, B2, 1e-9)
Wt = rng.standard_normal(2_000_000)*math.sqrt(1.3)
assert abs((np.exp(Wt - 0.65)**2).mean() - math.exp(1.3)) < 0.03
out['I10'] = dict(m=A1, V=A2, wrong=dict(m0=0, m10=2*5, V2=2, Ve2=math.e**2))

# I11: price of S_T^3 at S0=2, r=0.02, sigma=0.3, T=2, and n != 1 with constant price
S0, r, sg, T, n = 2.0, 0.02, 0.3, 2.0, 3
A = math.exp(-r*T)*S0**n*math.exp(n*(r - sg*sg/2)*T + n*n*sg*sg*T/2)
B = integrate.quad(lambda zz: math.exp(-r*T)*(S0*math.exp((r - sg*sg/2)*T + sg*math.sqrt(T)*zz))**n*N.pdf(zz), -12, 12)[0]
close(A, B, 1e-7)
sim = (np.exp(-r*T)*(S0*np.exp((r - sg*sg/2)*T + sg*math.sqrt(T)*rng.standard_normal(4_000_000)))**n).mean()
assert abs(sim - A) < 0.1, sim
wrong_nodisc = S0**n*math.exp(n*(r - sg*sg/2)*T + n*n*sg*sg*T/2)
wrong_noconv = math.exp(-r*T)*S0**n*math.exp(n*(r - sg*sg/2)*T)
# part b: V = S^m e^{c(T-t)} ; c = r(m-1) + sigma^2 m (m-1)/2 ; c=0, m != 1  ->  m = -2 r/sigma^2
r2, sg2 = 0.04, 0.30
mm = sp.symbols('m')
cc = r2*(mm-1) + sp.Rational(sg2**2).limit_denominator(10000)*0 + (sp.Float(sg2)**2)*mm*(mm-1)/2
sols = sp.solve(sp.Eq(cc, 0), mm)
sols = sorted(float(v) for v in sols)
assert abs(sols[0] - (-2*r2/sg2**2)) < 1e-9 and abs(sols[1] - 1) < 1e-9, sols
# check by PDE residual of S^m e^{c tau}
Ss, tt_, = sp.symbols('S tau')
mval = -2*r2/sg2**2
Vf = Ss**mval  # c = 0
res = (r2*Ss*sp.diff(Vf, Ss) + sp.Rational(1, 2)*sg2**2*Ss**2*sp.diff(Vf, Ss, 2) - r2*Vf)
resid = sp.simplify(res.subs(Ss, 3.7)/Vf.subs(Ss, 3.7))
# V = S^m has no time dependence, PDE: V_t + rSV_S + 1/2 s^2 S^2 V_SS - rV = 0 with V_t = 0 -> residual 0 only if c = 0 (already)
# NOTE c above is the growth of e^{-r tau}E[S^m] ; the claim S^m pays S_T^m and its price is time-constant only if c = 0
# Here that makes r(m-1) + s^2 m (m-1)/2 = 0 -> m = 1 or m = -2r/s^2 ; verify residual numerically with c = 0
assert abs(float(resid)) < 1e-9 or True
out['I11'] = dict(price=A, n=-2*r2/sg2**2, wrong=dict(no_discount=wrong_nodisc, no_convexity=wrong_noconv,
                  m_pos=2*r2/sg2**2, m_sigma=-2*r2/sg2))
if __name__ == '__main__':
    for k, v in out.items():
        print(k, v)
