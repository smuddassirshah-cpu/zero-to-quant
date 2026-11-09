"""Reader checks for the two derivations of batch 12: markets L3 h-carry-two-rates and micro L3 h-derive-tilted-quotes.
Every number in the model and rubric is recomputed by two routes. Run with the venv Python (needs SciPy for the LP).
markets: route A is the closed forms in Decimal at 40 digits; route B is a linear programme over every trade the
prompt allows (borrow or deposit for six months or a year, long or short share, long or short forward), which finds
the no-arbitrage band without being told which plan is cheapest. micro: route A is exact Bayes over the 2 x 2 x 2 tree
in Fractions; route B is a bisection on the ask that makes the maker's expected profit on a buy zero, and a seeded
simulation."""
import sys, random, itertools
from decimal import Decimal as Dm, getcontext
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog

getcontext().prec = 40
fails = 0


def ok(cond, msg):
    global fails
    if not cond:
        fails += 1
    print(("ok   " if cond else "FAIL ") + msg)


def near(a, b, tol=5e-5):
    return abs(float(a) - float(b)) < tol


# ---------------- markets L3 ----------------
S0, D, t, T = Dm(64), Dm("1.20"), Dm("0.5"), Dm(1)
rb, rd, fee = Dm("1.07"), Dm("1.03"), Dm("0.50")
pw = lambda x, y: (x.ln() * y).exp()
up = (S0 - D * pw(rb, -t)) * pw(rb, T)              # dividend repays debt
up_dep = S0 * rb - D * pw(rd, T - t)                # dividend deposited: F - (64*1.07 - 1.2*1.03^0.5)
lo = (S0 - D * pw(rd, -t)) * pw(rd, T) - fee        # dividend set aside at 3%
lo_bor = S0 * rd - D * pw(rb, T - t) - fee          # dividend borrowed at 7%
one = lambda r: (S0 - D * pw(r, -t)) * pw(r, T)
print(f"markets: up {up:.6f}, up(deposit) {up_dep:.6f}, lo {lo:.6f}, lo(borrow) {lo_bor:.6f}, one rate 5% {one(Dm('1.05')):.6f}")
for got, want, name in [(up, "67.2387", "upper bound"), (up_dep, "67.2621", "deposit variant"), (lo, "64.2021", "lower bound"),
                        (lo_bor, "64.1787", "borrow variant"), (one(Dm("1.05")), "65.9704", "one rate 5%"), (Dm("67.80") - up, "0.5613", "profit at 67.80"),
                        (D * pw(rb, -t), "1.1601", "six-month loan"), (S0 - D * pw(rb, -t), "62.8399", "one-year loan"), (D * pw(rd, -t), "1.1824", "six-month deposit"),
                        (S0 - D * pw(rd, -t), "62.8176", "one-year deposit"), ((S0 - D * pw(rd, -t)) * rd, "64.7021", "deposit pays"), (D * pw(Dm("1.05"), t), "1.2296", "1.2 x 1.05^0.5")]:
    ok(abs(got - Dm(want)) < Dm("0.00005"), f"markets {name}: {got:.6f} rounds to {want}")
ok(lo < one(Dm("1.05")) < up, "markets: 5% one-rate price inside the band")
for r in ["1.00", "1.02", "1.05", "1.10"]:   # part 3: with one rate and no fee the two closed forms coincide
    r = Dm(r)
    a = (S0 - D * pw(r, -t)) * pw(r, T)
    b = (S0 - D * pw(r, -t)) * pw(r, T) - 0
    ok(abs(a - (S0 * r - D * pw(r, T - t))) < Dm("1e-30") and a == b, f"markets part 3 at r = {r}: both bounds {a:.6f}")


def best_profit(Fq, rb=1.07, rd=1.03, fee=0.5):
    """Max riskless delivery profit over all allowed trades, cash today and in six months >= 0, positions <= 1.
    x = [B05, B1, D05, D1, L, S, fl, fs]: borrow 6m, borrow 1y, deposit 6m, deposit 1y, long share, short share, long fwd, short fwd."""
    g05b, g05d = rb ** 0.5, rd ** 0.5
    # delivery cash (riskless once L - S + fl - fs = 0): -rb B1 + rd D1 - fee S - F fl + F fs
    c = -np.array([0, -rb, 0, rd, 0, -fee, -Fq, Fq])
    A_ub = [[-1, -1, 1, 1, 64, -64, 0, 0],               # cash today >= 0
            [g05b, 0, -g05d, 0, -1.2, 1.2, 0, 0]]        # cash in six months >= 0 (dividend in, owed dividend out)
    A_eq = [[0, 0, 0, 0, 1, -1, 1, -1]]                  # no share exposure at delivery
    res = linprog(c, A_ub=A_ub, b_ub=[0, 0], A_eq=A_eq, b_eq=[0], bounds=[(0, 200)] * 4 + [(0, 1)] * 4, method="highs")
    return -res.fun


def edge(lo_, hi_, inside_is_low):
    for _ in range(80):
        m = (lo_ + hi_) / 2
        arb = best_profit(m) > 1e-10
        if arb == inside_is_low:
            hi_ = m
        else:
            lo_ = m
    return (lo_ + hi_) / 2


lp_up = edge(65.0, 70.0, True)     # above the edge there is arbitrage
lp_lo = edge(60.0, 65.0, False)    # below the edge there is arbitrage
print(f"markets LP band: {lp_lo:.6f} to {lp_up:.6f}")
ok(near(lp_up, up, 1e-5) and near(lp_lo, lo, 1e-5), "markets: LP over every allowed trade finds the same band as the model (to 1e-5, the solver tolerance)")
ok(near(best_profit(67.80), 0.5613, 5e-5), f"markets: LP profit at 67.80 is {best_profit(67.80):.6f} (model 0.5613)")
ok(best_profit(66.0) < 1e-10 and best_profit(64.19) > 0 and best_profit(67.25) > 0, "markets: no arbitrage inside, arbitrage at 64.19 and 67.25")
ok(near(best_profit(65.970366, 1.05, 1.05, 0.0), 0, 1e-6), "markets: one rate 5%, no fee: no arbitrage at 65.9704")
ok(best_profit(65.98, 1.05, 1.05, 0.0) > 0 and best_profit(65.96, 1.05, 1.05, 0.0) > 0, "markets: one rate: arbitrage just above and just below, so one price")

# ---------------- micro L3 ----------------


def exact(al, be, de):
    """Exact Bayes over value x type x side."""
    pb = {+1: F(0), -1: F(0)}
    ps = {+1: F(0), -1: F(0)}
    for v, typ in itertools.product((+1, -1), ("inf", "un")):
        pv = F(1, 2) * (al if typ == "inf" else 1 - al)
        if typ == "inf":
            (pb if v == +1 else ps)[v] += pv
        else:
            pb[v] += pv * be
            ps[v] += pv * (1 - be)
    nb, ns = pb[+1] + pb[-1], ps[+1] + ps[-1]
    a = (pb[+1] * de - pb[-1] * de) / nb if nb else None   # no buys: E[D | buy] undefined
    b = -(ps[+1] * de - ps[-1] * de) / ns if ns else None
    return a, b, pb[+1] + pb[-1], ps[+1] + ps[-1]


def model_a(al, be, de):
    return al * de / (al + 2 * (1 - al) * be)


def model_b(al, be, de):
    return al * de / (al + 2 * (1 - al) * (1 - be))


grid = [F(i, 10) for i in range(1, 10)]
bad = 0
for al, be in itertools.product(grid, [F(0)] + grid + [F(1)]):
    a, b, _, _ = exact(al, be, F(21))
    bad += (a != model_a(al, be, F(21))) + (b != model_b(al, be, F(21)))
ok(bad == 0, "micro: closed forms equal exact Bayes on a 9 x 11 grid of alpha in (0, 1) and beta in [0, 1]")
ok(all(model_a(al, F(1, 2), 7) == al * 7 == model_b(al, F(1, 2), 7) for al in grid), "micro (b): beta = 1/2 gives a = b = alpha delta")
a, b, pbuy, psell = exact(F(1, 5), F(3, 4), F(21))
ok(a == 3 and b == 7 and pbuy == F(7, 10) and psell == F(3, 10), f"micro (c): a {a}, b {b}, P(buy) {pbuy}, P(sell) {psell}")
ok(F(1, 10) / pbuy == F(1, 7) and F(1, 10) / psell == F(1, 3), "micro (c): P(informed | buy) 1/7, P(informed | sell) 1/3")
ok((a - b) / 2 == -2 and a + b == 10, "micro (c): spread 10p centred 2p below V")


def ask_by_bisection(al, be, de, lo_=0.0, hi_=None):
    hi_ = de if hi_ is None else hi_
    for _ in range(100):
        m = (lo_ + hi_) / 2
        prof = 0.5 * al * (m - de) + 0.5 * (1 - al) * be * (m - de) + 0.5 * (1 - al) * be * (m + de)
        lo_, hi_ = (lo_, m) if prof > 0 else (m, hi_)
    return (lo_ + hi_) / 2


ok(near(ask_by_bisection(0.2, 0.75, 21), 3, 1e-9) and near(ask_by_bisection(0.2, 0.25, 21), 7, 1e-9), "micro: bisection on zero profit per side gives 3p and, by the mirror, 7p")
# (d): symmetric quotes V +- 4.2
s = F(21, 5)
buy_p, sell_p = s - a, s - b
ok(buy_p == F(6, 5) and sell_p == F(-14, 5) and pbuy * buy_p + psell * sell_p == 0, "micro (d): +1.2p a buy, -2.8p a sell, 0 overall")
ok(all(exact(al, be, F(21))[2] * (al * 21 - exact(al, be, F(21))[0]) + exact(al, be, F(21))[3] * (al * 21 - exact(al, be, F(21))[1]) == 0
       for al in grid for be in grid), "micro (d): symmetric quotes at alpha delta break even on average for every alpha, beta")
rng = random.Random(12)
n, pb_, ps_, nb, ns = 400000, 0.0, 0.0, 0, 0
for _ in range(n):
    Dv = 21 if rng.random() < 0.5 else -21
    if rng.random() < 0.2:
        buy = Dv > 0
    else:
        buy = rng.random() < 0.75
    if buy:
        nb += 1; pb_ += 4.2 - Dv
    else:
        ns += 1; ps_ += Dv + 4.2
print(f"micro simulation: per buy {pb_ / nb:.3f}, per sell {ps_ / ns:.3f}, overall {(pb_ + ps_) / n:.3f}")
ok(near(pb_ / nb, 1.2, 0.1) and near(ps_ / ns, -2.8, 0.15) and near((pb_ + ps_) / n, 0, 0.06), "micro (d): simulation agrees")
# hypotheses: where does the model break?
ok(exact(F(0), F(0), F(21))[2] == 0 and exact(F(0), F(1), F(21))[3] == 0, "micro: alpha = 0 with beta = 0 (or 1) makes P(buy) (or P(sell)) 0, so that quote is undefined (MI3-1)")
ok(all(al + 2 * (1 - al) * be >= al > 0 for al in grid for be in [F(0)] + grid + [F(1)]), "micro: with alpha > 0 both denominators are at least alpha")

print(f"failures: {fails}")
sys.exit(1 if fails else 0)
