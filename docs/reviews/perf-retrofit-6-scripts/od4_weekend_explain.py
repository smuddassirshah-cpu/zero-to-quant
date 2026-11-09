"""opt-dash homework-4 h4-weekend-explain: shipped solution, starter, a reader solution (its own Greeks and
prices from scipy.stats.norm, not the loaded bs_greeks or bs_price), reader-planted slips (none from the
author's list) on every example and test, and the explain's vanna claim by a second route (a finite difference
of vega in S, not the analytic vanna). Venv Python, from this folder."""
import sys, math
from harness import item, run, summary

it = item("opt-dash", "homework-4.json", "h4-weekend-explain")
w = it["widget"]
bad = 0

READER = r'''
from scipy.stats import norm as _N
import math as _m

def _px(S, K, r, s, T, kind, q):
    a = (_m.log(S / K) + (r - q + s * s / 2) * T) / (s * _m.sqrt(T)); b = a - s * _m.sqrt(T)
    c = S * _m.exp(-q * T) * _N.cdf(a) - K * _m.exp(-r * T) * _N.cdf(b)
    return c if kind == "call" else c - S * _m.exp(-q * T) + K * _m.exp(-r * T)   # parity

def _gk(S, K, r, s, T, kind, q):
    a = (_m.log(S / K) + (r - q + s * s / 2) * T) / (s * _m.sqrt(T)); b = a - s * _m.sqrt(T)
    eq, er = _m.exp(-q * T), _m.exp(-r * T)
    dc = eq * _N.cdf(a)
    g = eq * _N.pdf(a) / (S * s * _m.sqrt(T))
    v = S * eq * _N.pdf(a) * _m.sqrt(T)
    th_c = -S * eq * _N.pdf(a) * s / (2 * _m.sqrt(T)) - r * K * er * _N.cdf(b) + q * S * eq * _N.cdf(a)
    if kind == "call":
        return dc, g, v, th_c
    # parity: put = call - S e^{-qT} + K e^{-rT}; theta = -dV/dT
    return dc - eq, g, v, th_c - q * S * eq + r * K * er

def explain_day(book, S0, S1, r, days, q=0.0):
    tau = days / 365.0
    tot = dict(delta=0.0, gamma=0.0, vega=0.0, theta=0.0, actual=0.0)
    for p in book:
        s0, s1 = p["vol0"] / 100.0, p["vol1"] / 100.0
        D, G, V, TH = _gk(S0, p["K"], r, s0, p["T"], p["kind"], q)
        tot["delta"] += p["qty"] * D * (S1 - S0)
        tot["gamma"] += p["qty"] * G * (S1 - S0) ** 2 / 2
        tot["vega"] += p["qty"] * V * (s1 - s0)
        tot["theta"] += p["qty"] * TH * tau
        tot["actual"] += p["qty"] * (_px(S1, p["K"], r, s1, p["T"] - tau, p["kind"], q) - _px(S0, p["K"], r, s0, p["T"], p["kind"], q))
    tot["explained"] = tot["delta"] + tot["gamma"] + tot["vega"] + tot["theta"]
    tot["residual"] = tot["actual"] - tot["explained"]
    return tot
'''

sol = w["solution"]
def slip(*pairs):
    s = sol
    for old, new in pairs:
        assert old in s, old
        s = s.replace(old, new)
    return s

SLIPS = {
    "Greeks at the mid share price": slip(("bs_greeks(S0, K, r, vol0, T, kind, q)", "bs_greeks((S0 + S1) / 2, K, r, vol0, T, kind, q)")),
    "gamma term on dS, not dS squared": slip(("g[\"gamma\"] * dS ** 2", "g[\"gamma\"] * dS")),
    "both prices at the shortened T": slip(("before = bs_price(S0, K, r, vol0, T, kind, q)", "before = bs_price(S0, K, r, vol0, T - dt, kind, q)")),
    "short positions counted long (abs qty)": slip(("n, K, T, kind = p[\"qty\"]", "n, K, T, kind = abs(p[\"qty\"])")),
    "Greeks fed vol in points": slip(("g = bs_greeks(S0, K, r, vol0, T, kind, q)", "g = bs_greeks(S0, K, r, p['vol0'], T, kind, q)")),
    "q passed to the Greeks, not to the prices": slip(("before = bs_price(S0, K, r, vol0, T, kind, q)", "before = bs_price(S0, K, r, vol0, T, kind)"),
                                                     ("after = bs_price(S1, K, r, vol1, T - dt, kind, q)", "after = bs_price(S1, K, r, vol1, T - dt, kind)")),
    "weekend counted as one trading day (days - 2 when days is 3)": slip(("dS, dt = S1 - S0, days / 365", "dS, dt = S1 - S0, (days - 2 if days == 3 else days) / 365")),
}

print("h4-weekend-explain")
f, _ = summary(w, sol, "shipped solution"); bad += bool(f)
bad += any(x[0] != "pass" for x in run(w, sol, "examples"))
f, _ = summary(w, READER, "reader solution (scipy, parity puts)"); bad += bool(f)
bad += any(x[0] != "pass" for x in run(w, READER, "examples"))
f, _ = summary(w, w["starter"], "starter"); bad += len(f) != len(w["tests"])
for name, src in SLIPS.items():
    f, _ = summary(w, src, "slip: " + name)
    if not f:
        print("     ^ passes every test"); bad += 1

# The explain's numbers: residual -2.52 after the weekend fall; vanna summed over the book about -2.32.
g = {}
exec(w["prelude"], g)
exec(sol, g)
d = g["explain_day"](g["weekend_book"], 100.0, 96.5, 0.04, 3, q=0.01)
print("  residual after the weekend fall: %.4f" % d["residual"])
bad += round(d["residual"], 2) != -2.52
van = 0.0
for p in g["weekend_book"]:
    s0, s1 = p["vol0"] / 100, p["vol1"] / 100
    h = 1e-3
    vu = g["bs_greeks"](100.0 + h, p["K"], 0.04, s0, p["T"], p["kind"], 0.01)["vega"]
    vd = g["bs_greeks"](100.0 - h, p["K"], 0.04, s0, p["T"], p["kind"], 0.01)["vega"]
    van += p["qty"] * (vu - vd) / (2 * h) * (96.5 - 100.0) * (s1 - s0)
print("  vanna term by a bump of vega in S: %.4f (explain: about -2.32)" % van)
bad += round(van, 2) != -2.32
# The convention the task uses, and where the course teaches it: 3 calendar days, theta per year / 365.
print("  weekend theta: 3 calendar days, dt = 3/365 =", round(3 / 365, 6))
print("bad:", bad)
sys.exit(1 if bad else 0)
