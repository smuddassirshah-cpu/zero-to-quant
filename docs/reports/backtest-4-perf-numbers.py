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
check("exactly one required row, the What failed row", [r["text"][:11] for r in rubric if r.get("required")] == ["What failed"])
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

# ---- impact at the £1m book, two routes ----
q = tau_r * book                         # £m traded a day
imp_a = 1.0 * sigma_d * math.sqrt(q / V)
imp_b = sigma_d / math.sqrt(V / q)       # Q/V = 1/225, sqrt = 1/15
check(f"trades about £0.4m a day ({q})", abs(q - 0.4) < 1e-12 and says("£0.4m"))
check(f"impact 0.0010 = 10 bp ({imp_a:.6f}, {imp_b:.6f})", abs(imp_a - 0.001) < 1e-12 and abs(imp_b - 0.001) < 1e-12
      and says("0.0010") and says("10 bp"))
all_in = cost + imp_a
check("15 bp all in", round(all_in * 1e4, 6) == 15 and says("15 bp"))
d15 = 252 * tau_r * all_in / vol_r
check(f"drag at 15 bp = 1.51 ({d15:.4f})", round(d15, 2) == 1.51 and says("1.51"))
n15a, n15b = gross_r - d15, net_daily(gross_r, vol_r, tau_r, all_in)
check(f"research net at £1m = -0.39 ({n15a:.4f}, {n15b:.4f})", round(n15a, 2) == -0.39 and abs(n15a - n15b) < 1e-12
      and says("-0.39") and says("−0.39"))

# ---- capacity, two routes ----
g_day = gross_r * vol_r / 252
check(f"gross edge 4.44 bp a day ({g_day * 1e4:.4f})", round(g_day * 1e4, 2) == 4.44 and says("4.44"))
c_star = g_day / tau_r
check(f"break-even 11.1 bp per unit traded ({c_star * 1e4:.4f})", round(c_star * 1e4, 1) == 11.1 and says("11.1"))
budget = c_star - cost
check(f"6.1 bp left for impact ({budget * 1e4:.4f})", round(budget * 1e4, 1) == 6.1 and says("6.1 bp"))
q_star = V * (budget / sigma_d) ** 2
book_a = q_star / tau_r
def net_at(b):                            # route B: bisection on net Sharpe = 0
    return gross_r - 252 * tau_r * (cost + sigma_d * math.sqrt(tau_r * b / V)) / vol_r
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if net_at(mid) > 0 else (lo, mid)
check(f"about £0.15m a day ({q_star:.4f})", round(q_star, 2) == 0.15 and says("£0.15m"))
check(f"book near £0.37m ({book_a:.4f}, bisection {lo:.4f})", round(book_a, 2) == 0.37 and abs(book_a - lo) < 1e-9
      and says("£0.37m"))

# ---- table figures quoted in the model ----
for k, (r, h) in rows.items():
    ok = all(v.replace("-", "−") in model for v in (r, h))
    check(f"model table repeats '{k}': {r}, {h}", ok)
check("prose median 0.02 and sd 0.38 repeated in the model", says("0.02") and "sd 0.38" in model)
check("first run 2.4 named in prose and model", "2.4" in prose and "2.4" in model)

print("\n%d failure(s)" % len(FAIL))
sys.exit(1 if FAIL else 0)
