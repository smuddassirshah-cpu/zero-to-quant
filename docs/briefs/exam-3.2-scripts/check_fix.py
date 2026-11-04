"""Revised numbers after the freshness grep (I6 rounding, I10b, I11, P1, P8). Run with PYTHONPATH=pylib."""
import math
import numpy as np
from scipy import integrate, stats
import sympy as sp
N = stats.norm
out = {}
rng = np.random.default_rng(3202)

# I6 shown inputs
S, Kk, r, sg, Tt = 70, 65, 0.04, 0.30, 0.75
d1 = (math.log(S/Kk) + (r + sg*sg/2)*Tt)/(sg*math.sqrt(Tt)); d2 = d1 - sg*math.sqrt(Tt)
V = S*N.cdf(d1) - Kk*math.exp(-r*Tt)*N.cdf(d2); Dl = N.cdf(d1); G = N.pdf(d1)/(S*sg*math.sqrt(Tt))
th = -S*N.pdf(d1)*sg/(2*math.sqrt(Tt)) - r*Kk*math.exp(-r*Tt)*N.cdf(d2)
Vs, Ds, Gs = 10.8791, 0.70216, 0.019056
th_s = r*Vs - r*S*Ds - 0.5*sg*sg*S*S*Gs
out['I6'] = dict(theta=th, from_shown=th_s, no_half=r*Vs - r*S*Ds - sg*sg*S*S*Gs, sign=r*Vs + r*S*Ds - 0.5*sg*sg*S*S*Gs)
assert abs(th - th_s) < 0.002

# I10b: Var int_0^2.5 e^{W-t/2} dW = e^{2.5} - 1
A = math.exp(2.5) - 1
B = integrate.quad(lambda u: math.exp(u), 0, 2.5)[0]
assert abs(A - B) < 1e-9
Wt = rng.standard_normal(6_000_000)*math.sqrt(1.0)
assert abs((np.exp(Wt - 0.5)**2).mean() - math.exp(1.0)) < 0.05
out['I10b'] = dict(key=A, wrong=dict(one_per_unit=2.5, no_lower=math.exp(2.5)))

# I11: S0 = 2, r = 0.03, sigma = 0.4, T = 2, n = 3
S0, r, sg, T, n = 2.0, 0.03, 0.4, 2.0, 3
A = math.exp(-r*T)*S0**n*math.exp(n*(r - sg*sg/2)*T + n*n*sg*sg*T/2)
B = integrate.quad(lambda zz: math.exp(-r*T)*(S0*math.exp((r - sg*sg/2)*T + sg*math.sqrt(T)*zz))**n*N.pdf(zz), -12, 12)[0]
assert abs(A - B) < 1e-7
sim = (np.exp(-r*T)*(S0*np.exp((r - sg*sg/2)*T + sg*math.sqrt(T)*rng.standard_normal(4_000_000)))**n).mean()
assert abs(sim - A) < 0.15, sim
m = -2*r/sg**2
mm = sp.symbols('m')
c = r*(mm - 1) + sp.Float(sg)**2*mm*(mm - 1)/2
sols = sorted(float(v) for v in sp.solve(sp.Eq(c, 0), mm))
assert abs(sols[0] - m) < 1e-9 and abs(sols[1] - 1) < 1e-9
# Monte Carlo: price at time 0 of S_T^m equals S0^m when c = 0
simm = (np.exp(-r*T)*(S0*np.exp((r - sg*sg/2)*T + sg*math.sqrt(T)*rng.standard_normal(6_000_000)))**m).mean()
assert abs(simm - S0**m) < 0.01, (simm, S0**m)
out['I11'] = dict(price=A, m=m, wrong=dict(no_discount=A*math.exp(r*T), no_convexity=math.exp(-r*T)*S0**n*math.exp(n*(r - sg*sg/2)*T),
                  m_pos=-m, m_sigma=-2*r/sg))

# P1: D = 0.45, t = 2.5 -> sd 1.5
D, t = 0.45, 2.5
A = 1/math.sqrt(4*math.pi*D*t)
L = 80.0; nn = 2**14; dx = L/nn
u0 = np.zeros(nn); u0[nn//2] = 1/dx
k = 2*np.pi*np.fft.fftfreq(nn, d=dx)
ut = np.real(np.fft.ifft(np.fft.fft(u0)*np.exp(-D*k*k*t)))
assert abs(ut.max() - A) < 1e-4
out['P1'] = dict(key=A, wrong=dict(var_Dt=1/math.sqrt(2*math.pi*D*t), no_t=1/math.sqrt(4*math.pi*D)))

# P8: explicit scheme, fewest equal steps with lambda <= 1/2
def explicit_heat(u0, D, dx, T):
    dt_max = dx*dx/(2*D)
    steps = math.ceil(T/dt_max - 1e-9)
    lam = D*(T/steps)/dx**2
    u = np.array(u0, float)
    for _ in range(steps):
        un = u.copy()
        un[1:-1] = u[1:-1] + lam*(u[2:] - 2*u[1:-1] + u[:-2])
        un[0] = un[-1] = 0.0
        u = un
    return steps, lam, u
def discrete_exact(u0, D, dx, T):
    steps = math.ceil(T/(dx*dx/(2*D)) - 1e-9); lam = D*(T/steps)/dx**2
    m = len(u0) - 2
    Tm = np.diag(1 - 2*lam*np.ones(m)) + lam*(np.diag(np.ones(m - 1), 1) + np.diag(np.ones(m - 1), -1))
    # eigen-decomposition route: eigenvalues 1 - 4 lam sin^2(j pi / (2 (m+1)))
    j = np.arange(1, m + 1); xs = np.arange(1, m + 1)
    Sm = np.sqrt(2/(m + 1))*np.sin(np.outer(j, xs)*np.pi/(m + 1))
    ev = 1 - 4*lam*np.sin(j*np.pi/(2*(m + 1)))**2
    coef = Sm @ np.array(u0[1:-1], float)
    return steps, Sm.T @ (ev**steps*coef)
tests = []
nx = 20; dx = 1/nx; xg = np.linspace(0, 1, nx + 1)
cases = {
 'sine-mix': (np.sin(np.pi*xg) + 0.5*np.sin(3*np.pi*xg), 0.15, dx, 0.43),
 'spike': (np.where(np.arange(nx + 1) == 10, 1.0, 0.0), 0.15, dx, 0.43),
}
nx2 = 50; xg2 = np.linspace(0, 2, nx2 + 1)
cases['wide'] = (np.exp(-((xg2 - 1)/0.3)**2), 0.08, 2/nx2, 1.7)
for name, (u0_, D_, dx_, T_) in cases.items():
    s1, lam1, uA = explicit_heat(u0_, D_, dx_, T_)
    s2, uB = discrete_exact(u0_, D_, dx_, T_)
    assert s1 == s2 and np.allclose(uA[1:-1], uB, atol=1e-12), name
    stepsf = math.floor(T_/(dx_*dx_/(2*D_)))
    lamf = D_*(T_/stepsf)/dx_**2
    # starter slip: floor steps
    u = np.array(u0_, float)
    for _ in range(stepsf):
        un = u.copy(); un[1:-1] = u[1:-1] + lamf*(u[2:] - 2*u[1:-1] + u[:-2]); un[0] = un[-1] = 0; u = un
    out['P8-' + name] = dict(steps=s1, lam=lam1, centre=float(uA[len(uA)//2]), floor_steps=stepsf, floor_lam=lamf,
                              floor_max_diff=float(np.max(abs(u - uA))))
if __name__ == '__main__':
    for k_, v in out.items(): print(k_, v)
