"""Exam 3.2, pdes items. Run with PYTHONPATH=pylib."""
import math
import numpy as np
from scipy import integrate, stats, special
import sympy as sp

N = stats.norm
out = {}
rng = np.random.default_rng(322)

# P1: peak height of the heat kernel, D = 0.32, t = 4
D, t = 0.32, 4.0
A = 1/math.sqrt(4*math.pi*D*t)
# B: kernel from the PDE: solve u_t = D u_xx on a grid from a narrow bump with exact spectral step
L = 80.0; n = 2**14
xs = (np.arange(n) - n//2)*L/n
dx = L/n
u0 = np.zeros(n); u0[n//2] = 1/dx
k = 2*np.pi*np.fft.fftfreq(n, d=dx)
ut = np.real(np.fft.ifft(np.fft.fft(u0)*np.exp(-D*k*k*t)))
assert abs(ut.max() - A) < 1e-4, (ut.max(), A)
sd = math.sqrt(2*D*t)
assert abs(sd*math.sqrt(2*math.pi)*ut.max() - 1) < 1e-3
out['P1'] = dict(key=A, sd=sd, wrong=dict(var_Dt=1/math.sqrt(2*math.pi*D*t), no_t=1/math.sqrt(4*math.pi*D)))

# P2: u0 = 1 on [-1.2, 1.2], D = 0.4, t = 0.75, value at x = 0
D2, t2, h = 0.4, 0.75, 1.2
sd = math.sqrt(2*D2*t2)
A2 = N.cdf(h/sd) - N.cdf(-h/sd)
B2 = integrate.quad(lambda y: math.exp(-y*y/(4*D2*t2))/math.sqrt(4*math.pi*D2*t2), -h, h)[0]
assert abs(A2 - B2) < 1e-9
w1 = 2*N.cdf(h/math.sqrt(D2*t2)) - 1       # sd = sqrt(Dt)
w2 = 2*N.cdf(h/(2*D2*t2)) - 1              # sd = 2Dt
out['P2'] = dict(key=A2, wrong=dict(sd_sqrt_Dt=w1, sd_2Dt=w2))

# P3: b_k for f(x) = x(pi - x) on (0, pi), odd extension
kk = sp.symbols('k', integer=True, positive=True); x = sp.symbols('x')
bk = sp.simplify(2/sp.pi*sp.integrate(x*(sp.pi - x)*sp.sin(kk*x), (x, 0, sp.pi)))
cand = 4*(1 - (-1)**kk)/(sp.pi*kk**3)
for kv in range(1, 8):
    assert abs(float(bk.subs(kk, kv)) - float(cand.subs(kk, kv))) < 1e-12
    q = 2/math.pi*integrate.quad(lambda xx: xx*(math.pi - xx)*math.sin(kv*xx), 0, math.pi)[0]
    assert abs(q - float(cand.subs(kk, kv))) < 1e-9
# slips
w_norm = 2*(1 - (-1)**kk)/(sp.pi*kk**3)          # used 1/pi instead of 2/pi
w_pow = 4*(1 - (-1)**kk)/(sp.pi*kk**2)
for kv in (1, 2, 3):
    assert abs(float(w_norm.subs(kk, kv)) - float(cand.subs(kk, kv))) > 1e-3 or kv % 2 == 0
out['P3'] = dict(key='\\frac{4(1-(-1)^k)}{\\pi k^3}', first=[float(cand.subs(kk, v)) for v in (1, 2, 3)],
                 wrong=dict(half=str(w_norm), power=str(w_pow)))

# P4: jump from 1 to 7: value at the jump, Gibbs peak
lo, hi = 1.0, 7.0
mid = (lo + hi)/2
si_pi = special.sici(math.pi)[0]
g = si_pi/math.pi - 0.5
peak = hi + g*(hi - lo)
# B: partial sums of the Fourier series of a square wave scaled: f = mid + (hi-lo)/2 * sgn(x), x in (-pi,pi)
M = 4000
xg = np.linspace(1e-4, 0.01, 200001)
S = mid + (hi - lo)/2*(4/np.pi)*sum(np.sin((2*j - 1)*xg)/(2*j - 1) for j in range(1, 1))  # placeholder, replaced below
j = np.arange(1, M + 1)
xp = math.pi/(2*M)           # nearest first maximum for M odd harmonics
Sx = mid + (hi - lo)/2*(4/math.pi)*np.sum(np.sin((2*j - 1)*xp)/(2*j - 1))
assert abs(Sx - peak) < 5e-3, (Sx, peak)
out['P4'] = dict(mid=mid, peak=peak, gibbs=g, wrong=dict(no_overshoot=hi, share_of_level=hi*(1 + g), midpoint=mid))

# P5: rod L = 3, D = 0.3, u0 = 4 sin(pi x/L) + 2 sin(3 pi x/L), centre at t = 0.5
L5, D5, t5 = 3.0, 0.3, 0.5
def mode(kv, bk_): return bk_*math.exp(-D5*(kv*math.pi/L5)**2*t5)*math.sin(kv*math.pi/2)
A5 = mode(1, 4) + mode(3, 2)
# B: finite-difference eigen-decomposition (dense matrix exponential on the grid)
import scipy.linalg as sl
nx = 600; hh = L5/nx
xg = np.linspace(0, L5, nx + 1)[1:-1]
Lap = (np.diag(-2*np.ones(nx - 1)) + np.diag(np.ones(nx - 2), 1) + np.diag(np.ones(nx - 2), -1))/hh**2
u0v = 4*np.sin(np.pi*xg/L5) + 2*np.sin(3*np.pi*xg/L5)
ut = sl.expm(D5*t5*Lap) @ u0v
B5 = np.interp(L5/2, xg, ut)
assert abs(A5 - B5) < 5e-3, (A5, B5)
rate1 = math.exp(-D5*(math.pi/L5)**2*t5)
out['P5'] = dict(key=A5, num=B5, wrong=dict(one_rate=(4 - 2)*rate1, ignore_sign=mode(1, 4) - mode(3, 2)))

# P6: BS to heat: r = 0.06, sigma = 0.25, T = 0.75
r6, s6, T6 = 0.06, 0.25, 0.75
k6 = 2*r6/s6**2; al = -(k6 - 1)/2; be = -(k6 + 1)**2/4
# B: sympy: v = e^{alpha x + beta tau} u solves v_tau = v_xx + (k-1)v_x - k v when u_tau = u_xx
xs_, ts_ = sp.symbols('x tau'); al_, be_, kk_ = sp.symbols('alpha beta k')
ufun = sp.Function('u')
v = sp.exp(al_*xs_ + be_*ts_)*ufun(xs_, ts_)
expr = sp.diff(v, ts_) - sp.diff(v, xs_, 2) - (kk_ - 1)*sp.diff(v, xs_) + kk_*v
expr = sp.simplify(expr/sp.exp(al_*xs_ + be_*ts_))
expr = expr.subs(sp.Derivative(ufun(xs_, ts_), ts_), sp.Derivative(ufun(xs_, ts_), (xs_, 2)))
coef_ux = sp.simplify(expr.coeff(sp.Derivative(ufun(xs_, ts_), xs_)))
coef_u = sp.simplify(expr.subs(sp.Derivative(ufun(xs_, ts_), xs_), 0).subs(sp.Derivative(ufun(xs_, ts_), (xs_, 2)), 0).coeff(ufun(xs_, ts_)))
sa = sp.solve(sp.Eq(coef_ux, 0), al_)[0]
sb = sp.solve(sp.Eq(coef_u.subs(al_, sa), 0), be_)[0]
assert abs(float(sa.subs(kk_, k6)) - al) < 1e-12 and abs(float(sb.subs(kk_, k6)) - be) < 1e-12
out['P6'] = dict(k=k6, alpha=al, beta=be, tau_end=s6**2*T6/2,
                 wrong=dict(beta_no_k1_sq=-(k6 - 1)**2/4, beta_half=-(k6 + 1)/2, alpha_pos=(k6 - 1)/2))

# P7: Feynman-Kac with X: dX = 0.5 dt + 1.2 dW, h = x^2, r = 0.1, x = 2, tau = 2
mu, sg, r, x0, tau = 0.5, 1.2, 0.1, 2.0, 2.0
A7 = math.exp(-r*tau)*((x0 + mu*tau)**2 + sg**2*tau)
B7 = integrate.quad(lambda z: math.exp(-r*tau)*(x0 + mu*tau + sg*math.sqrt(tau)*z)**2*N.pdf(z), -12, 12)[0]
assert abs(A7 - B7) < 1e-9
# C: check V solves the PDE (residual)
tt, xx = sp.symbols('t x'); Tt = 2
Vf = sp.exp(-sp.Float(r)*(Tt - tt))*((xx + sp.Float(mu)*(Tt - tt))**2 + sp.Float(sg)**2*(Tt - tt))
res = sp.diff(Vf, tt) + sp.Float(mu)*sp.diff(Vf, xx) + sp.Float(sg)**2/2*sp.diff(Vf, xx, 2) - sp.Float(r)*Vf
assert abs(float(res.subs({tt: 0.3, xx: 1.1}))) < 1e-12
sim = (math.exp(-r*tau)*(x0 + mu*tau + sg*math.sqrt(tau)*rng.standard_normal(4_000_000))**2).mean()
assert abs(sim - A7) < 0.05
out['P7'] = dict(key=A7, wrong=dict(no_discount=(x0 + mu*tau)**2 + sg**2*tau, no_variance=math.exp(-r*tau)*(x0 + mu*tau)**2))

# P8: explicit scheme with the largest stable step
def explicit_heat(u0, D, dx, T):
    dt_max = dx*dx/(2*D)
    steps = math.ceil(T/dt_max - 1e-12)
    lam = D*(T/steps)/dx**2
    u = np.array(u0, float)
    for _ in range(steps):
        un = u.copy()
        un[1:-1] = u[1:-1] + lam*(u[2:] - 2*u[1:-1] + u[:-2])
        un[0] = un[-1] = 0.0
        u = un
    return steps, lam, u
nx = 20; Lr = 1.0; dx = Lr/nx; D8 = 0.15; T8 = 0.4
xg = np.linspace(0, Lr, nx + 1)
u0 = np.sin(np.pi*xg) + 0.5*np.sin(3*np.pi*xg)
steps, lam, uA = explicit_heat(u0, D8, dx, T8)
# B: exact discrete solution of the scheme via the matrix power (same dt) and eigen-decomposition of the interior stencil
m = nx - 1
Tm = np.diag(1 - 2*lam*np.ones(m)) + lam*(np.diag(np.ones(m - 1), 1) + np.diag(np.ones(m - 1), -1))
uB = np.linalg.matrix_power(Tm, steps) @ u0[1:-1]
assert np.allclose(uA[1:-1], uB, atol=1e-12)
# C: continuum solution, closest check of accuracy
cont = np.exp(-D8*np.pi**2*T8)*np.sin(np.pi*xg) + 0.5*np.exp(-D8*9*np.pi**2*T8)*np.sin(3*np.pi*xg)
assert np.max(abs(uA - cont)) < 5e-3, np.max(abs(uA - cont))
# the floor slip: steps = floor -> lam > 1/2 -> blow-up
steps_f = math.floor(T8/(dx*dx/(2*D8)))
lam_f = D8*(T8/steps_f)/dx**2
out['P8'] = dict(nx=nx, D=D8, T=T8, steps=steps, lam=lam, steps_floor=steps_f, lam_floor=lam_f,
                 centre=uA[nx//2], u_at_5=uA[5], cont_centre=cont[nx//2])

if __name__ == '__main__':
    for k_, v in out.items(): print(k_, v)
