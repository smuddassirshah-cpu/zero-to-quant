"""ito level 4 performance task h-aloud-unknown-drift (homework-4.json): every stated fact computed twice.
Route A is symbolic (sympy). Route B is numeric (seeded simulation of the self-financing hedge under three drifts,
one of them path-dependent, and a one-step Taylor check of the discrete-hedge leftover).
Run from the repo root: python3 docs/reports/ito-4-perf-numbers.py (sympy, numpy; without sympy route A is skipped)."""
import json, math, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'ito', 'homework-4.json')
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
it = [i for i in items if i['id'] == 'h-aloud-unknown-drift'][0]
check('item is last (index 7 of 8)', items.index(it) == 7 and len(items) == 8)
check('performance aloud, top-level longform', it.get('performance') == 'aloud' and it.get('kind') == 'longform')
check('seconds 300 within 15 to 1800', it['seconds'] == 300 and 15 <= it['seconds'] <= 1800)
check('think 30, lockAtZero true', it.get('think') == 30 and it.get('lockAtZero') is True)
check('three follow-ups (1 to 5)', len(it['followUps']) == 3)
check('no scaffold fields', not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')))
rub = it['rubric']
check('rubric 3 to 5 rows', 3 <= len(rub) <= 5)
check('rubric sums to 10', sum(r['points'] for r in rub) == 10)
# fix pass (review-perf-retrofit-3): required rows follow DECISIONS Session X, one per named part, never every row
check('3 required rows, not every row', sum(1 for r in rub if r.get('required') is True) == 3 and 3 < len(rub))
check('homework 6 to 12 items', 6 <= len(items) <= 12)
check('one performance task in the level', sum(1 for i in items if i.get('performance')) == 1)
check('title has no maths', '$' not in it['title'])
txt = it['prompt'] + it['model'] + ''.join(r['text'] for r in rub) + ''.join(it['followUps'])
check('no em or en dash, no exclamation', not any(c in txt for c in '—–!'))
check('five-minute claim matches seconds', 'five minutes' in it['prompt'] and it['seconds'] == 5 * 60)
check('30 seconds to plan matches think', '30 seconds to plan' in it['prompt'] and it['think'] == 30)
# the plan: 1 + 2 + 1 + 1 minutes fill the 300 seconds
check('plan minutes 1 + 2 + 1 + 1 = 5', (1 + 2 + 1 + 1) * 60 == it['seconds'])
check('the plan is in the model', all(w in it['model'] for w in ('One minute for assumptions', 'two for the hedge', 'one for the equation')))

# 1. Route A: symbolic
try:
    import sympy as sp
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False
    print('sympy missing: route A skipped')
if HAVE_SYMPY:
    t, S, r, sig, T = sp.symbols('t S r sigma T', positive=True)
    mu = sp.Symbol('mu_t', real=True)       # any value at this instant: the drift's form is never used
    D = sp.Symbol('Delta', real=True)
    V = sp.Function('V')(t, S)
    Vt, VS, VSS = sp.diff(V, t), sp.diff(V, S), sp.diff(V, S, 2)
    # Ito's lemma with dS = mu_t S dt + sigma S dW, (dS)^2 = sigma^2 S^2 dt
    dV_dt = Vt + mu * S * VS + sp.Rational(1, 2) * sig**2 * S**2 * VSS
    dV_dW = sig * S * VS
    # zero-cost self-financing book: short one claim, Delta shares, cash C = V - Delta S
    C = V - D * S
    check('book worth zero at the start', sp.simplify(-V + D * S + C) == 0)
    book_dt = -dV_dt + D * mu * S + r * C
    book_dW = -dV_dW + D * sig * S
    check('dW coefficient = sigma S (Delta - V_S)', sp.simplify(book_dW - sig * S * (D - VS)) == 0)
    Dstar = sp.solve(sp.Eq(book_dW, 0), D)[0]
    check('Delta = V_S', sp.simplify(Dstar - VS) == 0)
    left = sp.expand(book_dt.subs(D, Dstar))
    check('mu_t cancels at Delta = V_S', sp.diff(left, mu) == 0)
    check('drift terms are -mu S V_S + mu S Delta', sp.simplify(sp.expand(book_dt).coeff(mu) - (-S * VS + S * D)) == 0)
    check('leftover = -V_t - 1/2 s^2 S^2 V_SS + rV - rS V_S',
          sp.simplify(left - (-Vt - sp.Rational(1, 2) * sig**2 * S**2 * VSS + r * V - r * S * VS)) == 0)
    bs = Vt + r * S * VS + sp.Rational(1, 2) * sig**2 * S**2 * VSS - r * V
    check('leftover = 0 is the Black-Scholes equation', sp.simplify(left + bs) == 0)
    # the classic book -V + Delta S earning r on its value gives the same equation
    classic = sp.expand((-dV_dt + Dstar * mu * S) - r * (-V + Dstar * S))
    check('classic book gives the same equation', sp.simplify(classic + bs) == 0)
    # a claim paying 1 at T: V = e^{-r(T - t)}
    one = sp.exp(-r * (T - t))
    check('V_t = r V for the bond', sp.simplify(sp.diff(one, t) - r * one) == 0)
    check('bond solves the equation', sp.simplify(sp.diff(one, t) + r * S * sp.diff(one, S) + sp.Rational(1, 2) * sig**2 * S**2 * sp.diff(one, S, 2) - r * one) == 0)
    check('bond pays 1 at T', one.subs(t, T) == 1)
    # the Black-Scholes call solves the equation (symbolic route for the final claim of the model)
    K = sp.Symbol('K', positive=True); tau = T - t
    N = lambda x: (1 + sp.erf(x / sp.sqrt(2))) / 2
    d1 = (sp.log(S / K) + (r + sig**2 / 2) * tau) / (sig * sp.sqrt(tau)); d2 = d1 - sig * sp.sqrt(tau)
    call = S * N(d1) - K * sp.exp(-r * tau) * N(d2)
    res = sp.diff(call, t) + r * S * sp.diff(call, S) + sp.Rational(1, 2) * sig**2 * S**2 * sp.diff(call, S, 2) - r * call
    vals = [{S: 100, K: 100, r: sp.Rational(5, 100), sig: sp.Rational(1, 5), T: 1, t: 0}, {S: 83, K: 97, r: sp.Rational(3, 100), sig: sp.Rational(7, 20), T: 2, t: sp.Rational(1, 2)}]
    for k, v in enumerate(vals):
        check(f'call residual 0 at point {k}', abs(float(res.subs(v).evalf(30))) < 1e-20)

# 2. Route B: numeric
def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs_call(S, K, r, sig, tau):
    d1 = (math.log(S / K) + (r + sig**2 / 2) * tau) / (sig * math.sqrt(tau)); d2 = d1 - sig * math.sqrt(tau)
    return S * Phi(d1) - K * math.exp(-r * tau) * Phi(d2)
S0, K_, r_, sig_, T_ = 100.0, 100.0, 0.05, 0.2, 1.0
erfv = np.vectorize(math.erf)
def delta(t, S):
    tau = T_ - t
    d1 = (np.log(S / K_) + (r_ + sig_**2 / 2) * tau) / (sig_ * math.sqrt(tau))
    return 0.5 * (1 + erfv(d1 / math.sqrt(2)))
def run(drift, steps, paths, seed):
    """Short one call, Delta shares, cash C = V - Delta S at the start; each rebalance paid from cash (self-financing)."""
    g = np.random.default_rng(seed)
    dt = T_ / steps
    S = np.full(paths, S0); runmax = S.copy()
    V0 = bs_call(S0, K_, r_, sig_, T_)
    D = delta(0, S); cash = V0 - D * S
    worth0 = -V0 + D * S + cash
    trade_change = 0.0
    for k in range(steps):
        mu = drift(k * dt, S, runmax)                      # known at the start of the step: adapted
        z = g.standard_normal(paths)
        S = S * np.exp((mu - sig_**2 / 2) * dt + sig_ * math.sqrt(dt) * z)
        runmax = np.maximum(runmax, S)
        cash = cash * math.exp(r_ * dt)
        if k < steps - 1:
            Dn = delta((k + 1) * dt, S)
            before = D * S + cash
            cash = cash - (Dn - D) * S
            after = Dn * S + cash
            trade_change = max(trade_change, float(np.max(np.abs(after - before))))
            D = Dn
    book = D * S + cash - np.maximum(S - K_, 0)
    return float(np.sqrt(np.mean(book**2))), float(np.mean(book)), float(np.max(np.abs(worth0))), trade_change, S
drifts = {
    'constant 12%': lambda t, S, m: 0.12 + 0 * S,
    'path-dependent': lambda t, S, m: 0.4 * np.tanh((m - S) / 10) - 0.1,     # depends on the running maximum
    'constant -30%': lambda t, S, m: -0.30 + 0 * S,
}
errs = {}
for name, f in drifts.items():
    e_coarse = run(f, 50, 4000, 11)[0]
    e_fine, m_fine, w0, tc, ST = run(f, 800, 4000, 11)
    errs[name] = e_fine
    check(f'{name}: book worth zero at the start', w0 < 1e-12)
    check(f'{name}: a rebalance leaves the book value unchanged', tc < 1e-9)
    check(f'{name}: error shrinks about as 1/sqrt(steps)', e_fine < 0.35 * e_coarse)
    check(f'{name}: replication error small at 800 steps', e_fine < 0.3)
    print(f'{name}: RMS error 50 steps {e_coarse:.4f}, 800 steps {e_fine:.4f}')
vals = list(errs.values())
check('every drift: error at 800 steps under 3% of the price', max(vals) < 0.03 * bs_call(S0, K_, r_, sig_, T_))
# the drift matters for the real-world chance of paying off, not for the price
def p_itm(mu, n=400000, seed=5):
    z = np.random.default_rng(seed).standard_normal(n)
    ST = S0 * np.exp((mu - sig_**2 / 2) * T_ + sig_ * math.sqrt(T_) * z)
    return float(np.mean(ST > K_))
p12, pq = p_itm(0.12), p_itm(r_)
check('P(S_T > K) under mu = 12% matches the formula', abs(p12 - Phi((math.log(S0 / K_) + (0.12 - sig_**2 / 2)) / sig_)) < 0.004)
check('Q(S_T > K) matches Phi(d2) = 0.5596', abs(pq - 0.559618) < 0.004 and abs(Phi((r_ - sig_**2 / 2) / sig_) - 0.559618) < 1e-6)
check('real-world and risk-neutral chances differ', abs(p12 - pq) > 0.1)
# discrete rebalancing leaves 1/2 Gamma (dS)^2 against theta: one-step Taylor check for the short-call book
tau, dS, dt = 1.0, 2.0, 1 / 252
V = bs_call(S0, K_, r_, sig_, tau); h = 1e-3
Dl = (bs_call(S0 + h, K_, r_, sig_, tau) - bs_call(S0 - h, K_, r_, sig_, tau)) / (2 * h)
G = (bs_call(S0 + h, K_, r_, sig_, tau) - 2 * V + bs_call(S0 - h, K_, r_, sig_, tau)) / h**2
Th = (bs_call(S0, K_, r_, sig_, tau - 1e-6) - V) / 1e-6                      # dV/dt = -dV/dtau
exact = -(bs_call(S0 + dS, K_, r_, sig_, tau - dt) - V) + Dl * dS + r_ * (V - Dl * S0) * dt
taylor = -(0.5 * G * dS**2 + Th * dt) + r_ * (V - Dl * S0) * dt
check('one-step book P&L = -(1/2 Gamma dS^2 + Theta dt) + interest, to Taylor order', abs(exact - taylor) < 0.003)
check('gamma 0.018762 and theta -6.4140 (the shared call)', abs(G - 0.018762) < 5e-6 and abs(Th + 6.4140) < 5e-4)

print(f'{n_checks} checks, {len(fails)} failures')
sys.exit(1 if fails else 0)
