"""backtest level 4 performance task (h-reversal-note): every number recomputed twice.

Run with a Python that has numpy and scipy (the scratch venv):
    python docs/reports/backtest-4-perf-numbers.py
Each figure in the prose, the results table, the model note and the rubric is
computed by two independent routes and compared with the text. Exits 0 when all agree.
"""
import json, math, os, re, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app/content/courses/backtest/homework-4.json")
FAIL = []

def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)

doc = json.load(open(HW, encoding="utf-8"))
item = next(i for i in doc["items"] if i["id"] == "h-reversal-note")
prose, model = item["widget"]["prompt"], item["widget"]["model"]
rubric = item["widget"]["rubric"]
rows = {r[0]: r[1:] for r in item["canvas"]["params"]["rows"]}
num = lambda s: float(s.replace("%", "").replace("−", "-")) / (100 if "%" in s else 1)
text = prose + model + json.dumps(rubric, ensure_ascii=False)

def says(fragment):
    return fragment in text

# inputs as the table and prose give them
gross_r, gross_h = map(num, rows["Gross Sharpe"])
net_r, net_h = map(num, rows["Net Sharpe, 5 bp a trade"])
vol_r, vol_h = map(num, rows["Volatility, a year"])
tau_r, tau_h = map(num, rows["Turnover a day"])
cost = 0.0005          # 5 bp
sd_trials, n_lb, n_th = 0.38, 6, 5
sigma_d, V, book = 0.015, 90.0, 1.0   # daily vol, £m a day, £m book

# ---- shape ----
check("rubric sums to 10 with 3 to 5 rows", sum(r["points"] for r in rubric) == 10 and 3 <= len(rubric) <= 5)
check("required rows: Results and What failed, not every row", [r["text"][:7] for r in rubric if r.get("required")] == ["Results", "What fa"])
check("homework has 6 to 12 items, one performance item",
      6 <= len(doc["items"]) <= 12 and sum(1 for i in doc["items"] if i.get("performance")) == 1)
w = item["widget"]
check("derivation shape: no starter, steps, order, derive, hints, parts",
      not any(k in w or k in item for k in ("starter", "steps", "order", "derive", "hints", "parts")))

# ---- split and grid ----
check("1,003 + 5 + 252 = 1,260 days", 1003 + 5 + 252 == 1260 and says("1,260") and says("1,003") and says("252"))
lbs, ths = [2, 3, 5, 10, 15, 20], [0, 0.01, 0.02, 0.03, 0.04]
check("6 lookbacks x 5 thresholds = 30 settings (two counts)",
      len(lbs) * len(ths) == 30 == n_lb * n_th and len([(a, b) for a in lbs for b in ths]) == 30)

# ---- net Sharpe from gross, two routes ----
def net_formula(g, vol, tau, c):          # annual: gross minus drag over vol
    return g - 252 * tau * c / vol
def net_daily(g, vol, tau, c):            # daily mean and sd, then annualise
    mu, sd = g * vol / 252, vol / math.sqrt(252)
    return (mu - tau * c) / sd * math.sqrt(252)
for label, g, vol, tau, shown in (("research", gross_r, vol_r, tau_r, net_r), ("held out", gross_h, vol_h, tau_h, net_h)):
    a, b = net_formula(g, vol, tau, cost), net_daily(g, vol, tau, cost)
    check(f"{label} net Sharpe {shown}: {a:.4f} and {b:.4f}", abs(a - b) < 1e-12 and round(a, 2) == shown)
drag = 252 * tau_r * cost
check("drag 5.04% a year and 0.504 of Sharpe (two routes)",
      abs(drag - 0.0504) < 1e-12 and abs(drag / vol_r - 0.504) < 1e-12
      and abs((gross_r - net_daily(gross_r, vol_r, tau_r, cost)) - 0.504) < 1e-12 and says("5.04\\%") and says("0.504"))
check("costs take 0.50 of 1.12", round(gross_r - net_r, 2) == 0.50 and says("0.50 of the 1.12"))

# ---- expected best of 30, two routes ----
from scipy import integrate, stats
emax_int = integrate.quad(lambda x: 30 * x * stats.norm.pdf(x) * stats.norm.cdf(x) ** 29, -10, 10)[0]
rng = np.random.default_rng(2026)
emax_mc = rng.standard_normal((200_000, 30)).max(axis=1).mean()
check(f"E[max of 30] = 2.043 (integral {emax_int:.4f}, simulation {emax_mc:.4f})",
      round(emax_int, 3) == 2.043 and abs(emax_mc - emax_int) < 0.005 and says("2.043"))
check("expected best 2.043 x 0.38 = 0.78 (and integral x 0.38)",
      round(2.043 * sd_trials, 2) == 0.78 and round(emax_int * sd_trials, 2) == 0.78 and says("0.78"))
check("best 0.62 does not reach 0.78", net_r < 2.043 * sd_trials)

# ---- standard errors, two routes ----
def se_lo(sr, days):
    srd = sr / math.sqrt(252)
    return math.sqrt((1 + srd ** 2 / 2) / days) * math.sqrt(252)
years_r = 1003 / 252
check(f"research years 3.98 ({years_r:.4f})", round(years_r, 2) == 3.98 and says("3.98"))
check("research SE about 0.50 (Lo and 1/sqrt(T))",
      round(se_lo(net_r, 1003), 2) == 0.50 and round(1 / math.sqrt(years_r), 2) == 0.50)
check("held-out SE about 1.00 (Lo and 1/sqrt(1))", round(se_lo(net_h, 252), 2) == 1.00)
sims = rng.standard_normal((20_000, 252)) * 0.01 + net_h * 0.01 / math.sqrt(252)
sr_hat = sims.mean(axis=1) / sims.std(axis=1, ddof=1) * math.sqrt(252)
check(f"held-out SE by simulation ({sr_hat.std():.3f}) near 1.00", abs(sr_hat.std() - 1.0) < 0.03)
check("0.35 is within one standard error of zero", net_h < se_lo(net_h, 252))

# ---- impact at the £1m book (fix pass BT4-1) ----
# Basis: the item's own model. Its rule holds -1, 0 or +1 books, so a trade is the whole book
# (£1m, or £2m on a flip); turnover 0.40 means fewer trades, not smaller ones. Impact follows the course's
# per-trade rule c * sigma * sqrt(Q / V), as l11 screens 10 and 11 and homework-2 h2-capacity charge it.
Q = book                                  # £m in one trade
imp_a = 1.0 * sigma_d * math.sqrt(Q / V)
imp_b = sigma_d / math.sqrt(V / Q)        # route B: sigma over sqrt(V/Q) = sqrt(90)
check(f"impact 0.0016 = 16 bp on a £1m trade ({imp_a:.6f}, {imp_b:.6f})",
      abs(imp_a - imp_b) < 1e-15 and round(imp_a, 4) == 0.0016 and round(imp_a * 1e4) == 16
      and says("0.0016") and says("16 bp"))
check("the old charge (impact on the average £0.4m trade, 10 bp) is gone", "0.4/90" not in model and "10 bp a trade" not in text)
# a flip is two books: impact on £2m, stated only as 'worse'
imp_flip = sigma_d * math.sqrt(2 * Q / V)
check(f"a flip costs more ({imp_flip * 1e4:.1f} bp on £2m)", imp_flip > imp_a and says("flip"))
all_in = cost + imp_a
check(f"20.8 bp all in ({all_in * 1e4:.3f})", round(all_in * 1e4, 1) == 20.8 and says("20.8 bp"))
d_a = 252 * tau_r * all_in / vol_r        # route A: annual drag over vol
n_a = gross_r - d_a
n_b = net_daily(gross_r, vol_r, tau_r, all_in)   # route B: daily mean and sd
# route C: simulate the rule's trading, 100 trades a 252-day year at turnover 0.40 (one book each), cost per trade
trades_per_year = 252 * tau_r
d_c = trades_per_year * all_in / vol_r
check(f"drag at 20.8 bp = 2.10 ({d_a:.4f}, {d_c:.4f})", round(d_a, 2) == 2.10 and abs(d_a - d_c) < 1e-12 and says("2.10"))
check(f"research net at £1m = -0.98 ({n_a:.4f}, {n_b:.4f})", round(n_a, 2) == -0.98 and abs(n_a - n_b) < 1e-12
      and says("-0.98") and "about −1.0 or worse" in text)
check("the reviewer's 21 bp rounding would give -1.00; the text uses 20.8 bp, which gives -0.98",
      round(gross_r - 252 * tau_r * 0.0021 / vol_r, 2) == -1.00)

# ---- break-even book, two routes ----
g_day = gross_r * vol_r / 252
check(f"gross edge 4.44 bp a day ({g_day * 1e4:.4f})", round(g_day * 1e4, 2) == 4.44 and says("4.44"))
c_star = g_day / tau_r
check(f"break-even 11.1 bp per unit traded ({c_star * 1e4:.4f})", round(c_star * 1e4, 1) == 11.1 and says("11.1"))
budget = c_star - cost
check(f"6.1 bp left for impact ({budget * 1e4:.4f})", round(budget * 1e4, 1) == 6.1 and says("6.1 bp"))
B_a = V * (budget / sigma_d) ** 2         # route A: invert c sigma sqrt(B/V) = budget
def net_at(b):                            # route B: bisection on net Sharpe = 0, impact on the whole book b
    return gross_r - 252 * tau_r * (cost + sigma_d * math.sqrt(b / V)) / vol_r
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if net_at(mid) > 0 else (lo, mid)
check(f"break-even book about £0.15m ({B_a:.4f}, bisection {lo:.4f})", round(B_a, 2) == 0.15 and abs(B_a - lo) < 1e-9
      and says("£0.15m") and "£0.37m" not in text and "0.00061" in model)
check("at £0.15m the rule is at zero net; at £1m it loses (net at 0.15 and 1)", abs(net_at(lo)) < 1e-9 and net_at(1.0) < 0)
check("with flips (two-book trades some days) the break-even book is smaller",
      V * (budget / sigma_d) ** 2 / 2 < B_a and says("less where it flips"))

# ---- trials: the bar assumes independence (BT4-4) ----
check("the 0.78 bar states its independence assumption", "treats the 30 settings as independent" in model)
rho_sim = rng.standard_normal((100_000, 1))
corr = 0.6 * rho_sim + 0.8 * rng.standard_normal((100_000, 30))      # pairwise correlation 0.36
check("correlated settings give a lower expected best than independent ones",
      corr.max(axis=1).mean() < emax_int)

# ---- rubric passes (BT4-2): minimal sets, none skipping a part the question names ----
import itertools
pts = [r["points"] for r in rubric]
req_rows = [i for i, r in enumerate(rubric) if r.get("required")]
passes = [c for k in range(1, 6) for c in itertools.combinations(range(5), k)
          if sum(pts[i] for i in c) >= 7 and all(i in c for i in req_rows)]
print("     passing tick sets:", [[i + 1 for i in c] for c in passes])
check("required rows are 2 (results) and 4 (what failed), not every row", req_rows == [1, 3])
check("every passing set holds the results row and the what-failed row", all({1, 3} <= set(c) for c in passes) and passes)

# ---- table figures quoted in the model ----
for k, (r, h) in rows.items():
    ok = all(v.replace("-", "−") in model for v in (r, h))
    check(f"model table repeats '{k}': {r}, {h}", ok)
check("prose median 0.02 and sd 0.38 repeated in the model", says("0.02") and "sd 0.38" in model)
check("first run 2.4 named in prose and model", "2.4" in prose and "2.4" in model)

print("\n%d failure(s)" % len(FAIL))
sys.exit(1 if FAIL else 0)
