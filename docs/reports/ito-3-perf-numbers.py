"""ito level 3 performance task h-derive-black (homework-3.json): every stated fact computed twice.
Route A is symbolic (sympy). Route B is numeric (seeded simulation and finite differences).
Run from the repo root: python3 docs/reports/ito-3-perf-numbers.py (sympy, numpy; without sympy route A is skipped)."""
import json, math, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'ito', 'homework-3.json')
fails = []
n_checks = 0
def check(name, ok):
    global n_checks
    n_checks += 1
    if not ok:
        fails.append(name)
        print('FAIL', name)

# 0. Shape of the item and the homework limits
doc = json.load(open(HW))
items = doc['items']
it = [i for i in items if i['id'] == 'h-derive-black'][0]
check('item is last (index 7 of 8)', items.index(it) == 7 and len(items) == 8)
check('performance derivation', it.get('performance') == 'derivation' and it.get('kind') == 'longform')
check('no scaffold fields', not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')))
rub = it['rubric']
check('rubric 3 to 5 rows', 3 <= len(rub) <= 5)
check('rubric sums to 10', sum(r['points'] for r in rub) == 10)
# fix pass (review-perf-retrofit-3): required rows follow DECISIONS Session X, one per named part, never every row
check('4 required rows, not every row', sum(1 for r in rub if r.get('required') is True) == 4 and 4 < len(rub))
check('homework 6 to 12 items', 6 <= len(items) <= 12)
check('one performance task in the level', sum(1 for i in items if i.get('performance')) == 1)
check('a difficulty 5 item', any(i.get('difficulty') == 5 for i in items))
check('title has no maths', '$' not in it['title'])
txt = it['prompt'] + it['model'] + ''.join(r['text'] for r in rub)
check('no em or en dash, no exclamation', not any(c in txt for c in '—–!'))

# 1. The stated number: e^{0.06} = 1.0618 (r = 4%, 1.5 years to delivery)
x = 0.04 * 1.5
a = math.exp(x)
b = sum(x ** k / math.factorial(k) for k in range(12))
check('exponent 0.04 * 1.5 = 0.06', abs(x - 0.06) < 1e-15)
check('e^0.06 two ways agree', abs(a - b) < 1e-14)
check('e^0.06 rounds to 1.0618', round(a, 4) == 1.0618 and round(b, 4) == 1.0618)
check('the number is in the model', '1.0618' in it['model'] and 'e^{0.06}' in it['model'])

# 2. Route A: symbolic
try:
    import sympy as sp
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False
    print('sympy missing: route A skipped')
if HAVE_SYMPY:
    t, s, r, mu, sig, TF, T, K, Fv = sp.symbols('t s r mu sigma T_F T K F', positive=True)
    # 2a. dF by Ito's lemma on f(t, s) = s e^{r(T_F - t)}
    f = s * sp.exp(r * (TF - t))
    ft, fs, fss = sp.diff(f, t), sp.diff(f, s), sp.diff(f, s, 2)
    check('f_t = -r f', sp.simplify(ft + r * f) == 0)
    check('f_ss = 0', fss == 0)
    driftF = ft + mu * s * fs + sp.Rational(1, 2) * sig**2 * s**2 * fss
    volF = sig * s * fs
    check('dF drift = (mu - r) F', sp.simplify(driftF - (mu - r) * f) == 0)
    check('dF vol = sigma F', sp.simplify(volF - sig * f) == 0)
    # 2b. dV for a general V(t, F), then the book -V + Delta S
    V = sp.Function('V')
    Vt = sp.Derivative(V(t, Fv), t); VF = sp.Derivative(V(t, Fv), Fv); VFF = sp.Derivative(V(t, Fv), Fv, 2)
    dV_dt = Vt + (mu - r) * Fv * VF + sp.Rational(1, 2) * sig**2 * Fv**2 * VFF
    dV_dW = sig * Fv * VF
    S = Fv * sp.exp(-r * (TF - t))         # the share in terms of F
    D = sp.Symbol('Delta')
    book_dW = -dV_dW + D * sig * S
    Dstar = sp.solve(sp.Eq(book_dW, 0), D)[0]
    check('Delta = e^{r(T_F - t)} V_F', sp.simplify(Dstar - sp.exp(r * (TF - t)) * VF) == 0)
    check('dW coefficient = sigma (Delta S - F V_F)', sp.simplify(book_dW - sig * (D * S - Fv * VF)) == 0)
    book_dt = sp.expand(-dV_dt + Dstar * mu * S)
    check('mu cancels in the book', sp.simplify(sp.diff(book_dt, mu)) == 0)
    check('book dt = -V_t - 1/2 s^2 F^2 V_FF + r F V_F',
          sp.simplify(book_dt - (-Vt - sp.Rational(1, 2) * sig**2 * Fv**2 * VFF + r * Fv * VF)) == 0)
    rhs = r * (-V(t, Fv) + Dstar * S)
    check('r Pi = r(-V + F V_F)', sp.simplify(rhs - r * (-V(t, Fv) + Fv * VF)) == 0)
    pde = sp.expand(book_dt - rhs)       # = 0 is the equation, times -1
    target = Vt + sp.Rational(1, 2) * sig**2 * Fv**2 * VFF - r * V(t, Fv)
    check('equation V_t + 1/2 s^2 F^2 V_FF - rV = 0', sp.simplify(pde + target) == 0)
    check('no F V_F term survives', sp.simplify(sp.diff(pde.subs(VF, sp.Symbol('q')), sp.Symbol('q'))) == 0)
    # 2c. Risk-neutral drift: mu = r gives forward drift 0
    check('forward drift is 0 at mu = r', sp.simplify(driftF.subs(mu, r)) == 0)
    # 2d. Check on the claim paying F_T - K: static replication value and the equation
    Ssym = sp.Symbol('S', positive=True)
    rep = sp.exp(r * (TF - T)) * Ssym - K * sp.exp(-r * (T - t))
    Fofs = Ssym * sp.exp(r * (TF - t))
    check('replication value = e^{-r(T-t)}(F - K)', sp.simplify(rep - sp.exp(-r * (T - t)) * (Fofs - K)) == 0)
    Vfwd = sp.exp(-r * (T - t)) * (Fv - K)
    check('V_t = r V for the forward claim', sp.simplify(sp.diff(Vfwd, t) - r * Vfwd) == 0)
    check('V_FF = 0 for the forward claim', sp.diff(Vfwd, Fv, 2) == 0)
    check('forward claim solves the equation',
          sp.simplify(sp.diff(Vfwd, t) + sp.Rational(1, 2) * sig**2 * Fv**2 * sp.diff(Vfwd, Fv, 2) - r * Vfwd) == 0)
    check('payoff at T is F_T - K', sp.simplify(Vfwd.subs(t, T) - (Fv - K)) == 0)
    # 2e. Check against the share: U(t, S) = V(t, S e^{r(T_F - t)})
    # chain rule on concrete test functions (sympy Subs objects do not simplify reliably for an undefined function)
    z = sp.Symbol('z', positive=True)
    tests = [sp.exp(2 * t) * z**3, sp.sin(t) * sp.log(z) + z**sp.Rational(5, 2), sp.exp(-t * z / 50) + t**2 * z]
    for k, Wz in enumerate(tests):
        U = Wz.subs(z, Fofs)
        bs = sp.diff(U, t) + r * Ssym * sp.diff(U, Ssym) + sp.Rational(1, 2) * sig**2 * Ssym**2 * sp.diff(U, Ssym, 2) - r * U
        black = (sp.diff(Wz, t) + sp.Rational(1, 2) * sig**2 * z**2 * sp.diff(Wz, z, 2) - r * Wz).subs(z, Fofs)
        check(f'BS operator on U = Black operator on V at F (test {k})', sp.simplify(bs - black) == 0)
        check(f'U_t = V_t - r F V_F (test {k})', sp.simplify(sp.diff(U, t) - (sp.diff(Wz, t) - r * z * sp.diff(Wz, z)).subs(z, Fofs)) == 0)
        check(f'S U_S = F V_F (test {k})', sp.simplify(Ssym * sp.diff(U, Ssym) - (z * sp.diff(Wz, z)).subs(z, Fofs)) == 0)
        check(f'S^2 U_SS = F^2 V_FF (test {k})', sp.simplify(Ssym**2 * sp.diff(U, Ssym, 2) - (z**2 * sp.diff(Wz, z, 2)).subs(z, Fofs)) == 0)

# 3. Route B: numeric
def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs_call(S, K, r, sig, tau):
    d1 = (math.log(S / K) + (r + sig**2 / 2) * tau) / (sig * math.sqrt(tau)); d2 = d1 - sig * math.sqrt(tau)
    return S * Phi(d1) - K * math.exp(-r * tau) * Phi(d2)
def black_call(F, K, r, sig, tau):
    d1 = (math.log(F / K) + sig**2 / 2 * tau) / (sig * math.sqrt(tau)); d2 = d1 - sig * math.sqrt(tau)
    return math.exp(-r * tau) * (F * Phi(d1) - K * Phi(d2))
r_, sig_, mu_, T_, TF_, K_, S0 = 0.04, 0.25, 0.11, 1.0, 2.5, 105.0, 100.0
# 3a. Black's call equals the share-based price of the same payoff (F_T - K)^+
def Vcall(t, F):
    tau = T_ - t
    S = F * math.exp(-r_ * (TF_ - t))
    return math.exp(r_ * (TF_ - T_)) * bs_call(S, K_ * math.exp(-r_ * (TF_ - T_)), r_, sig_, tau)
F0 = S0 * math.exp(r_ * TF_)
check('Black call = share-based call', abs(Vcall(0, F0) - black_call(F0, K_, r_, sig_, T_)) < 1e-10)
# 3b. Finite-difference residual of V_t + 1/2 s^2 F^2 V_FF - r V at several points
for (t0, Fp) in [(0.0, F0), (0.3, 95.0), (0.7, 130.0)]:
    h, dt = 1e-2, 1e-5
    Vt_ = (Vcall(t0 + dt, Fp) - Vcall(t0 - dt, Fp)) / (2 * dt) if t0 > 0 else (Vcall(t0 + dt, Fp) - Vcall(t0, Fp)) / dt
    VFF_ = (Vcall(t0, Fp + h) - 2 * Vcall(t0, Fp) + Vcall(t0, Fp - h)) / h**2
    VF_ = (Vcall(t0, Fp + h) - Vcall(t0, Fp - h)) / (2 * h)
    res = Vt_ + 0.5 * sig_**2 * Fp**2 * VFF_ - r_ * Vcall(t0, Fp)
    check(f'Black residual small at t={t0}, F={Fp}', abs(res) < 2e-3)
    # the share's equation with an extra r F V_F term would fail: the rFV_F term really is absent
    check(f'adding r F V_F breaks it at t={t0}', abs(res + r_ * Fp * VF_) > 1.0)
# 3c. Simulated dF has drift (mu - r): E[F_T] = F_0 e^{(mu - r)T}
rng = np.random.default_rng(31)
Z = rng.standard_normal(400000)
ST = S0 * np.exp((mu_ - sig_**2 / 2) * T_ + sig_ * math.sqrt(T_) * Z)
FT = ST * math.exp(r_ * (TF_ - T_))
m, se = FT.mean(), FT.std() / math.sqrt(len(FT))
check('E[F_T] = F_0 e^{(mu - r)T} within 4 SE', abs(m - F0 * math.exp((mu_ - r_) * T_)) < 4 * se)
# 3d. Under the risk-neutral drift F has drift 0, so e^{-rT} E_Q[F_T - K] = e^{-rT}(F_0 - K)
STq = S0 * np.exp((r_ - sig_**2 / 2) * T_ + sig_ * math.sqrt(T_) * Z)
FTq = STq * math.exp(r_ * (TF_ - T_))
mq, seq = FTq.mean(), FTq.std() / math.sqrt(len(FTq))
check('E_Q[F_T] = F_0 within 4 SE', abs(mq - F0) < 4 * seq)
# 3e. Discrete hedge: short one call on F, hold e^{r(T_F - t)} V_F shares, cash at r. Error shrinks, whatever mu is.
def hedge_error(mu, steps, paths, seed):
    g = np.random.default_rng(seed)
    dt = T_ / steps
    S = np.full(paths, S0)
    V0 = Vcall(0, F0)
    def delta_shares(t, S):
        F = S * math.exp(r_ * (TF_ - t)); tau = T_ - t
        d1 = (np.log(F / K_) + sig_**2 / 2 * tau) / (sig_ * math.sqrt(tau))
        VF = math.exp(-r_ * tau) * 0.5 * (1 + np.vectorize(math.erf)(d1 / math.sqrt(2)))
        return math.exp(r_ * (TF_ - t)) * VF
    D = delta_shares(0, S)
    cash = V0 - D * S
    for k in range(steps):
        z = g.standard_normal(paths)
        S = S * np.exp((mu - sig_**2 / 2) * dt + sig_ * math.sqrt(dt) * z)
        cash = cash * math.exp(r_ * dt)
        tk = (k + 1) * dt
        if k < steps - 1:
            Dn = delta_shares(tk, S)
            cash = cash - (Dn - D) * S          # self-financing: rebalance paid from cash
            D = Dn
    FT = S * math.exp(r_ * (TF_ - T_))
    book = D * S + cash - np.maximum(FT - K_, 0)
    return float(np.sqrt(np.mean(book**2)))
e1 = hedge_error(0.11, 50, 4000, 7); e2 = hedge_error(0.11, 800, 4000, 7)
e3 = hedge_error(-0.20, 800, 4000, 8)
check('hedge error shrinks with finer steps', e2 < 0.35 * e1)
check('hedge error small at 800 steps', e2 < 0.4)
check('hedge works the same with another drift', abs(e3 - e2) < 0.3 * e2)
print(f'hedge RMS error: 50 steps {e1:.4f}, 800 steps {e2:.4f}, 800 steps with mu = -0.2 {e3:.4f}')

print(f'{n_checks} checks, {len(fails)} failures')
sys.exit(1 if fails else 0)
