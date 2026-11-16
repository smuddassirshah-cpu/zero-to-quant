#!/usr/bin/env python3
"""Second reader's recompute of arma problems-1 to problems-3 (review-problems-arma-1-3.md).

Imports nothing from the author's script. Every key, every `wrong` value and the numbers printed in
prose, feedback and explain are rebuilt from the problem text, by a route other than the closed form
where one exists (direct sums, brute search, seeded simulation, statsmodels psi weights, scipy tails).
Exit 0 always (CI runs every script here); a failing check prints a FINDING line.
Run: <scratchpad>/venv/bin/python docs/reports/problems-arma-numbers-read.py
"""
import json
import math
import os
import re
import sys
from fractions import Fraction as F

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, "..", "..", "app", "content", "courses", "arma")
SETS = {n: json.load(open(os.path.join(COURSE, f"problems-{n}.json"), encoding="utf-8")) for n in (1, 2, 3)}

checks = 0
fails = []


def chk(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(name)
        print(f"FINDING {name} {detail}")


def close(a, b, tol):
    return abs(a - b) <= tol + 1e-12


def item(n, iid):
    return next(it for it in SETS[n]["items"] if it["id"] == iid)


def part(n, iid, k):
    return item(n, iid)["parts"][k - 1]


def key(n, iid, k, mine, name=None):
    """The file's key equals mine, and mine rounded as the question asks is inside the band."""
    w = part(n, iid, k)["widget"]
    tag = name or f"{iid} part {k}"
    chk(f"{tag} key", close(w["answer"], mine, 1e-4 * max(1, abs(mine)) if w["tol"]["abs"] else 0), f"file {w['answer']} mine {mine}")
    q = part(n, iid, k)["question"]
    m = re.search(r"to (\d) (?:decimal )?places?", q)
    scale = 100 if w.get("unit") == "%" else 1
    if m:
        typed = round(mine * scale, int(m.group(1))) / scale
        chk(f"{tag} rounded form accepted", close(typed, w["answer"], w["tol"]["abs"]), f"typed {typed}")


def wrong(n, iid, k, wid, mine):
    """The file's wrong value equals mine, is refused by the key band and sits in no other wrong band."""
    w = part(n, iid, k)["widget"]
    e = next(x for x in w["wrong"] if x.get("id") == wid)
    tag = f"{iid} part {k} wrong {wid}"
    chk(f"{tag} value", close(e["value"], mine, 2e-4 * max(1, abs(mine))), f"file {e['value']} mine {mine}")
    chk(f"{tag} refused by key", abs(e["value"] - w["answer"]) > w["tol"]["abs"] + e["tol"]["abs"], "bands touch")
    for o in w["wrong"]:
        if o is not e:
            chk(f"{tag} clear of {o.get('id')}", abs(e["value"] - o["value"]) > e["tol"]["abs"] + o["tol"]["abs"])


def says(n, iid, k, text, where=("feedback", "explain", "question", "options")):
    """A number string the reader computed appears in the part's learner-facing text."""
    blob = json.dumps(part(n, iid, k), ensure_ascii=False)
    chk(f"{iid} part {k} prints {text}", text in blob)


def typed_ok(n, iid, k, value, name):
    w = part(n, iid, k)["widget"]
    chk(f"{iid} part {k} accepts {name}", close(value, w["answer"], w["tol"]["abs"]), f"typed {value} key {w['answer']} tol {w['tol']['abs']}")



class block:
    """A problem's checks. If the content has moved on (a problem re-authored), say so and carry on: exit stays 0."""

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        return self

    def __exit__(self, et, ev, tb):
        if et is not None and issubclass(et, Exception):
            print(f"FINDING block {self.name} stopped: {et.__name__} {ev} (content changed since the read?)")
            fails.append(f"block {self.name}")
            return True
        return False


rng = np.random.default_rng(20261116)

# ---------------------------------------------------------------- shape of the sets
for n, s in SETS.items():
    chk(f"set {n} has 3 to 5 items", 3 <= len(s["items"]) <= 5)
    chk(f"set {n} has a difficulty 5", any(it["difficulty"] == 5 for it in s["items"]))
    typed = sum(p["widget"]["kind"] != "choice" for it in s["items"] for p in it["parts"])
    total = sum(len(it["parts"]) for it in s["items"])
    chk(f"set {n} typed share at least two thirds", typed * 3 >= total * 2, f"{typed}/{total}")
    for it in s["items"]:
        chk(f"{it['id']} has 3 to 5 parts", 3 <= len(it["parts"]) <= 5)
        for k, p in enumerate(it["parts"], 1):
            w = p["widget"]
            if w["kind"] == "numeric":
                chk(f"{it['id']} part {k} states its form", bool(re.search(r"Give (a|an|your) ", p["question"])))
            else:
                chk(f"{it['id']} part {k} one correct option", sum(bool(o.get("correct")) for o in w["options"]) == 1)
            chk(f"{it['id']} part {k} explain at most 3 sentences", len(re.findall(r"[.?](?:\s|$)", re.sub(r"\$[^$]*\$", "X", p["explain"]["text"]))) <= 3)

# ================================================================ problems-1
# ---- p-airport-anomaly: slope and t from the sums, then AR(1) variance and a normal tail
with block("p-airport-anomaly"):
    Sxx, Sxy, s2 = F(1250), F(-2875, 10), F(32, 10)
    g = Sxy / Sxx
    key(1, "p-airport-anomaly", 1, float(g))
    wrong(1, "p-airport-anomaly", 1, "flip", float(Sxx / Sxy))
    wrong(1, "p-airport-anomaly", 1, "sign", float(-g))
    se = math.sqrt(s2 / Sxx)
    t = float(g) / se
    key(1, "p-airport-anomaly", 2, t)
    wrong(1, "p-airport-anomaly", 2, "no-sqrt", float(g / (s2 / Sxx)))
    wrong(1, "p-airport-anomaly", 2, "s-not-s2", float(g) / math.sqrt(math.sqrt(3.2) / 1250))
    wrong(1, "p-airport-anomaly", 2, "sign", -t)
    says(1, "p-airport-anomaly", 2, "0.0506")
    chk("airport se 0.0506", round(se, 4) == 0.0506)
    typed_ok(1, "p-airport-anomaly", 2, round(-0.23 / 0.0506, 2), "t from the printed se")
    # Dickey-Fuller points with a constant, 364 pairs: simulate walks (second route to the quoted table)
    W = np.cumsum(rng.standard_normal((40000, 365)), axis=1)


    def df_t(X):
        y = np.diff(X, axis=1)
        x = X[:, :-1]
        xc = x - x.mean(1, keepdims=True)
        yc = y - y.mean(1, keepdims=True)
        b = (xc * yc).sum(1) / (xc * xc).sum(1)
        res = yc - b[:, None] * xc
        s2_ = (res * res).sum(1) / (x.shape[1] - 2)
        return b / np.sqrt(s2_ / (xc * xc).sum(1))


    tw = df_t(W)
    q1, q5 = np.quantile(tw, [0.01, 0.05])
    chk("DF 1% point near -3.45 at 365 days", abs(q1 + 3.45) < 0.06, f"sim {q1:.3f}")
    chk("DF 5% point near -2.87 at 365 days", abs(q5 + 2.87) < 0.04, f"sim {q5:.3f}")
    chk("airport statistic beyond the 1% point", t < q1)
    phi = 1 + g
    var = float(s2 / (1 - phi * phi))
    key(1, "p-airport-anomaly", 4, var)
    wrong(1, "p-airport-anomaly", 4, "shock", 3.2)
    wrong(1, "p-airport-anomaly", 4, "no-square", float(s2 / (1 - phi)))
    # variance by summing the damped shocks, a route that never uses 1/(1 - phi^2)
    chk("airport variance by a 400-term sum", close(sum(3.2 * 0.77 ** (2 * j) for j in range(400)), var, 1e-9))
    chk("airport sds 2.80 and 1.79", round(math.sqrt(var), 2) == 2.80 and round(math.sqrt(3.2), 2) == 1.79)
    p_tail = stats.norm.sf(5 / math.sqrt(var))
    key(1, "p-airport-anomaly", 5, p_tail)
    wrong(1, "p-airport-anomaly", 5, "shock-sd", stats.norm.sf(5 / math.sqrt(3.2)))
    wrong(1, "p-airport-anomaly", 5, "no-square", stats.norm.sf(5 / math.sqrt(float(s2 / (1 - phi)))))
    chk("airport tail by simulation", abs((rng.standard_normal(4_000_000) * math.sqrt(var) > 5).mean() - p_tail) < 4e-4)
    chk("airport days a year 14 and 1", round(p_tail * 365) == 14 and round(stats.norm.sf(5 / math.sqrt(3.2)) * 365) == 1)
    # FINDING candidates (review findings 1 and 2)
    chk("airport: S_xx/364 agrees with the part-4 variance (one data set)", abs(float(Sxx) / 364 - var) / var < 0.15,
        f"S_xx/364 = {float(Sxx) / 364:.2f} against {var:.2f}")
    typed_ok(1, "p-airport-anomaly", 5, round(stats.norm.sf(1.78), 3), "the tail at the printed 1.78 sds, to 3 places (0.038)")
    e = next(x for x in part(1, "p-airport-anomaly", 5)["widget"]["wrong"] if x["id"] == "shock-sd")
    chk("airport part 5 shock-sd slip typed to 3 places reaches its line", close(round(e["value"], 3), e["value"], e["tol"]["abs"]),
        f"0.003 against {e['value']} tol {e['tol']['abs']}")
# ---- p-ppp-screen: counts by exact fractions, rates by seeded simulation on 360 months
with block("p-ppp-screen"):
    dfw, dfa, nw, na = F(5, 100), F(20, 100), F(45, 100), F(89, 100)
    key(1, "p-ppp-screen", 1, float(36 * dfw))
    wrong(1, "p-ppp-screen", 1, "power", float(36 * dfa))
    wrong(1, "p-ppp-screen", 1, "normal", float(36 * nw))
    ppv = 12 * dfa / (12 * dfa + 36 * dfw)
    key(1, "p-ppp-screen", 2, float(ppv))
    wrong(1, "p-ppp-screen", 2, "power-only", 0.2)
    wrong(1, "p-ppp-screen", 2, "false-share", float(1 - ppv))
    ppn = 12 * nw * 0 + 12 * na / (12 * na + 36 * nw)
    key(1, "p-ppp-screen", 3, float(ppn))
    wrong(1, "p-ppp-screen", 3, "power-only", 0.89)
    wrong(1, "p-ppp-screen", 3, "false-share", float(1 - ppn))
    miss = 12 * (1 - dfa) / (12 * (1 - dfa) + 36 * (1 - dfw))
    key(1, "p-ppp-screen", 4, float(miss))
    wrong(1, "p-ppp-screen", 4, "miss-rate", 0.8)
    wrong(1, "p-ppp-screen", 4, "prior", 0.25)
    for s in ("9.6", "43.8", "34.2"):
        says(1, "p-ppp-screen", 4, s)
    chk("ppp counts 2.4, 4.2, 10.68, 26.88, 9.6, 43.8", (12 * dfa, 12 * dfa + 36 * dfw, 12 * na, 12 * na + 36 * nw, 12 * (1 - dfa), 12 * (1 - dfa) + 36 * (1 - dfw))
        == (F(24, 10), F(42, 10), F(1068, 100), F(2688, 100), F(96, 10), F(438, 10)))
    # enumeration route for part 2: 4800 series in the stated proportions
    chk("ppp part 2 by counting 4800 series", close((1200 * 0.20) / (1200 * 0.20 + 3600 * 0.05), float(ppv), 1e-12))
    # the four stated rates, 30,000 seeded paths of 360 months each (stationary start for the AR(1))
    E = rng.standard_normal((30000, 360))
    tw360 = df_t(np.cumsum(E, axis=1))
    A = np.empty_like(E)
    A[:, 0] = E[:, 0] / math.sqrt(1 - 0.98 ** 2)
    for j in range(1, 360):
        A[:, j] = 0.98 * A[:, j - 1] + E[:, j]
    ta = df_t(A)
    r = [(tw360 < -2.87).mean(), (ta < -2.87).mean(), (tw360 < -1.645).mean(), (ta < -1.645).mean()]
    print("ppp simulated rates (walk DF, AR DF, walk normal, AR normal):", [round(float(x), 3) for x in r])
    chk("ppp rate: DF point takes 5% of walks", abs(r[0] - 0.05) < 0.01, f"{r[0]:.3f}")
    chk("ppp rate: DF point takes 20% of the AR(1)s", abs(r[1] - 0.20) < 0.025, f"{r[1]:.3f}")
    chk("ppp rate: normal point takes 45% of walks", abs(r[2] - 0.45) < 0.015, f"{r[2]:.3f}")
    chk("ppp rate: normal point takes 89% of the AR(1)s", abs(r[3] - 0.89) < 0.02, f"{r[3]:.3f}")
    # claim in part 5: the changes of an AR(1) with phi 0.98 are autocorrelated (rho_1 = -(1 - phi)/2)
    dA = np.diff(A[:4000], axis=1)
    chk("ppp part 5 claim: differenced AR(1) has negative lag-1 autocorrelation", np.mean([np.corrcoef(d[1:], d[:-1])[0, 1] for d in dA]) < 0)
# ---- p-gdp-trend
with block("p-gdp-trend"):
    sdA = 3.5 * math.sqrt(2)
    key(1, "p-gdp-trend", 1, sdA / 100)
    wrong(1, "p-gdp-trend", 1, "same", 0.035)
    wrong(1, "p-gdp-trend", 1, "double", 0.07)
    u = 3.5 * rng.standard_normal(2_000_000)
    chk("gdp part 1 by simulation of u_t - u_{t-1}", abs(np.diff(u).std() - sdA) < 0.01)
    chk("gdp 'more than five times'", sdA / 0.9 > 5)
    sdB = math.sqrt(sum(0.9 ** 2 for _ in range(12)))
    key(1, "p-gdp-trend", 3, sdB / 100)
    wrong(1, "p-gdp-trend", 3, "linear", 0.108)
    chk("gdp variance 9.72", close(12 * 0.81, 9.72, 1e-9))
    h = next(k for k in range(1, 200) if 0.9 * math.sqrt(k) > 3.5)   # brute search
    key(1, "p-gdp-trend", 4, h)
    chk("gdp horizon is least and holds after", 0.9 * math.sqrt(h - 1) <= 3.5 and all(0.9 * math.sqrt(k) > 3.5 for k in range(h, 400)))
    wrong(1, "p-gdp-trend", 4, "round-down", 15)
    wrong(1, "p-gdp-trend", 4, "no-square", round(3.5 / 0.9))
    chk("gdp 3.49 and 3.60 and 15.1", round(0.9 * math.sqrt(15), 2) == 3.49 and round(0.9 * 4, 2) == 3.60 and round((3.5 / 0.9) ** 2, 1) == 15.1)
    # plausibility of the prose under model B: residual sd of a line fitted to a 120-step walk of step sd 0.9
    Wg = np.cumsum(0.9 * rng.standard_normal((4000, 120)), axis=1)
    tt = np.arange(120) - 59.5
    res = Wg - Wg.mean(1, keepdims=True) - ((Wg * tt).sum(1) / (tt * tt).sum())[:, None] * tt
    chk("gdp prose: a 3.5% residual sd is ordinary for model B", 0.05 < (res.std(1) > 3.5).mean() < 0.95, f"share above 3.5: {(res.std(1) > 3.5).mean():.2f}")
# ---- p-gold-drift
with block("p-gold-drift"):
    lg = math.log(1820 / 1450)
    mu_bp = lg / 500 * 1e4
    key(1, "p-gold-drift", 1, mu_bp)
    wrong(1, "p-gold-drift", 1, "simple", (1820 / 1450 - 1) / 500 * 1e4)
    chk("gold 0.2273 and 25.5%", round(lg, 4) == 0.2273 and round((1820 / 1450 - 1) * 100, 1) == 25.5)
    # telescoping by a random path between the two closes
    path = np.concatenate([[1450.0], np.exp(rng.normal(7.3, 0.2, 499)), [1820.0]])
    chk("gold mean of 500 log returns from any path", close(np.diff(np.log(path)).mean() * 1e4, mu_bp, 1e-9))
    se_bp = 110 / math.sqrt(500)
    tg = 4.55 / se_bp
    key(1, "p-gold-drift", 2, round(tg, 2))
    typed_ok(1, "p-gold-drift", 2, round(mu_bp / se_bp, 2), "t from the unrounded mean")
    wrong(1, "p-gold-drift", 2, "no-sqrt", mu_bp / (110 / 500))
    wrong(1, "p-gold-drift", 2, "sd", mu_bp / 110)
    chk("gold 4.92, 22.4, 24.6", round(se_bp, 2) == 4.92 and round(math.sqrt(500), 1) == 22.4 and round(1.1 * math.sqrt(500), 1) == 24.6)
    n_need = next(k for k in range(1, 10000) if 4.55 * math.sqrt(k) / 110 >= 2)
    key(1, "p-gold-drift", 4, n_need)
    typed_ok(1, "p-gold-drift", 4, math.ceil((2 * 110 / mu_bp) ** 2), "n from the unrounded mean")
    typed_ok(1, "p-gold-drift", 4, round(48.4 ** 2), "n from the printed 48.4")
    wrong(1, "p-gold-drift", 4, "no-square", round(2 * 110 / 4.55))
    wrong(1, "p-gold-drift", 4, "t-one", math.ceil((110 / 4.55) ** 2))
    chk("gold nine years", round(n_need / 252) == 9)
# ================================================================ problems-2
# ---- p-etf-flows
with block("p-etf-flows"):
    r1 = F(81000, 180000)
    key(2, "p-etf-flows", 1, float(r1))
    wrong(2, "p-etf-flows", 1, "flip", float(1 / r1))
    Q = 200 * 202 * (r1 ** 2 / 199 + F(24, 100) ** 2 / 198)
    key(2, "p-etf-flows", 2, float(Q))
    wrong(2, "p-etf-flows", 2, "box-pierce", float(200 * (r1 ** 2 + F(24, 100) ** 2)))
    wrong(2, "p-etf-flows", 2, "no-n-k", float(200 * 202 * (r1 ** 2 + F(24, 100) ** 2)))
    chk("etf chi2_2 5% point 5.99", round(stats.chi2.ppf(0.95, 2), 2) == 5.99 and float(Q) > 5.99)
    key(2, "p-etf-flows", 3, float(r1 ** 2))
    wrong(2, "p-etf-flows", 3, "double", 0.9)
    wrong(2, "p-etf-flows", 3, "sample", 0.24)
    chk("etf band 0.139", round(1.96 / math.sqrt(200), 3) == 0.139)
    sig2 = 900 * (1 - r1 ** 2)
    key(2, "p-etf-flows", 4, math.sqrt(sig2))
    wrong(2, "p-etf-flows", 4, "no-square", math.sqrt(900 * (1 - r1)))
    wrong(2, "p-etf-flows", 4, "series-sd", 30)
    wrong(2, "p-etf-flows", 4, "variance", float(sig2))
    x = np.empty(400000)
    ee = math.sqrt(float(sig2)) * rng.standard_normal(400000)
    x[0] = 0
    for j in range(1, 400000):
        x[j] = 0.45 * x[j - 1] + ee[j]
    chk("etf: an AR(1) with this shock sd has variance 900 and rho_2 0.2025", abs(x[1000:].var() - 900) < 12 and abs(np.corrcoef(x[2:], x[:-2])[0, 1] - 0.2025) < 0.006)
    chk("etf 'about 11%'", round((1 - math.sqrt(float(sig2)) / 30) * 100) == 11)
# ---- p-vol-index-order
with block("p-vol-index-order"):
    band = 1.96 / math.sqrt(680)
    key(2, "p-vol-index-order", 1, band)
    wrong(2, "p-vol-index-order", 1, "sd", 1 / math.sqrt(680))
    wrong(2, "p-vol-index-order", 1, "over-n", 1.96 / 680)
    pacf = [-0.21, -0.13, 0.05, -0.03, 0.04, -0.092]
    chk("vol PACF: lags 1, 2 and 6 outside, 3 to 5 inside, 7 to 20 inside", [abs(v) > band for v in pacf] == [True, True, False, False, False, True] and 0.06 < band)
    p1 = stats.binom.pmf(1, 18, 0.05)
    key(2, "p-vol-index-order", 3, p1)
    wrong(2, "p-vol-index-order", 3, "at-least", 1 - 0.95 ** 18)
    wrong(2, "p-vol-index-order", 3, "none", 0.95 ** 18)
    wrong(2, "p-vol-index-order", 3, "no-count", 0.05 * 0.95 ** 17)
    chk("vol exactly-one by simulation", abs(((rng.random((400000, 18)) < 0.05).sum(1) == 1).mean() - p1) < 0.003)
    bic = lambda k, l: k * math.log(680) - 2 * l
    gap = bic(8, -807.9) - bic(4, -812.4)
    key(2, "p-vol-index-order", 4, gap)
    wrong(2, "p-vol-index-order", 4, "aic", (2 * 8 + 2 * 807.9) - (2 * 4 + 2 * 812.4))
    wrong(2, "p-vol-index-order", 4, "no-fit", 4 * math.log(680))
    wrong(2, "p-vol-index-order", 4, "sign", -gap)
    chk("vol ln 680 = 6.52", round(math.log(680), 2) == 6.52)
# ---- p-peg-fridays
with block("p-peg-fridays"):
    g0 = sum(4 * 0.88 ** (2 * j) for j in range(2000))          # damped sum, not the closed form
    key(2, "p-peg-fridays", 1, g0)
    wrong(2, "p-peg-fridays", 1, "no-square", 4 / (1 - 0.88))
    wrong(2, "p-peg-fridays", 1, "sd-top", 2 / (1 - 0.88 ** 2))
    chk("peg sd 4.21", round(math.sqrt(g0), 2) == 4.21)
    key(2, "p-peg-fridays", 2, 0.88 ** 5)
    wrong(2, "p-peg-fridays", 2, "linear", 1 - 5 * 0.12)
    wrong(2, "p-peg-fridays", 2, "daily", 0.88)
    sw = sum(4 * 0.88 ** (2 * j) for j in range(5))              # five daily shocks, each faded by Friday
    key(2, "p-peg-fridays", 3, sw)
    chk("peg weekly shock variance two routes", close(sw, g0 * (1 - 0.88 ** 10), 1e-9))
    typed_ok(2, "p-peg-fridays", 3, round(17.73 * (1 - 0.5277 ** 2), 2), "the value from the restated 17.73 and 0.5277")
    wrong(2, "p-peg-fridays", 3, "daily", 4)
    wrong(2, "p-peg-fridays", 3, "five", 20)
    wrong(2, "p-peg-fridays", 3, "no-square", g0 * (1 - 0.88 ** 5))
    d = np.empty(1_000_000)
    ed = 2 * rng.standard_normal(1_000_000)
    d[0] = 0
    for j in range(1, 1_000_000):
        d[j] = 0.88 * d[j - 1] + ed[j]
    wk = d[1000::5]
    fit = np.polyfit(wk[:-1], wk[1:], 1)
    chk("peg by simulation: weekly slope 0.5277 and weekly shock variance 12.79", abs(fit[0] - 0.5277) < 0.01 and abs((wk[1:] - np.polyval(fit, wk[:-1])).var() - sw) < 0.25)
    b104 = 1.96 / math.sqrt(104)
    kmax = max(k for k in range(1, 50) if 0.5277 ** k > b104)
    key(2, "p-peg-fridays", 4, kmax)
    wrong(2, "p-peg-fridays", 4, "sd-band", max(k for k in range(1, 50) if 0.5277 ** k > 1 / math.sqrt(104)))
    wrong(2, "p-peg-fridays", 4, "one", 1)
    chk("peg 0.192, 0.278, 0.147, 0.098", [round(v, 3) for v in (b104, 0.5277 ** 2, 0.5277 ** 3, 1 / math.sqrt(104))] == [0.192, 0.278, 0.147, 0.098])
    chk("peg part 3 restates the variance it needs", "17.73" in part(2, "p-peg-fridays", 3)["question"], "question says 'the variance from part 1' with no value")
# ---- p-freight-ar2
with block("p-freight-ar2"):
    rr = [F(2, 100), F(145, 1000), F(-4, 100), F(5, 100), F(3, 100)]
    Q5 = 400 * 402 * sum(v * v / (400 - k) for k, v in enumerate(rr, 1))
    key(2, "p-freight-ar2", 1, float(Q5))
    wrong(2, "p-freight-ar2", 1, "box-pierce", float(400 * sum(v * v for v in rr)))
    wrong(2, "p-freight-ar2", 1, "no-n-k", float(400 * 402 * sum(v * v for v in rr)))
    chk("freight chi2 points 9.49 and 11.07 with Q between", round(stats.chi2.ppf(0.95, 4), 2) == 9.49 and round(stats.chi2.ppf(0.95, 5), 2) == 11.07 and 9.49 < float(Q5) < 11.07)
    chk("freight 0.0000528 of 0.0000665", round(float(rr[1] ** 2 / 398), 7) == 0.0000528 and round(float(sum(v * v / (400 - k) for k, v in enumerate(rr, 1))), 7) == 0.0000665)
    chk("freight: only the lag-2 residual bar is outside 0.098", [abs(float(v)) > 1.96 / 20 for v in rr] == [False, True, False, False, False])
    b1, b2 = np.linalg.solve(np.array([[1, 0.42], [0.42, 1]]), np.array([0.42, 0.33]))   # the 2 by 2 system itself
    key(2, "p-freight-ar2", 3, b2)
    wrong(2, "p-freight-ar2", 3, "acf", 0.33)
    wrong(2, "p-freight-ar2", 3, "no-divide", 0.33 - 0.42 ** 2)
    key(2, "p-freight-ar2", 4, 0.42 * (1 - 0.186))
    typed_ok(2, "p-freight-ar2", 4, round(b1, 3), "b_1 from the unrounded b_2")
    wrong(2, "p-freight-ar2", 4, "ar1", 0.42)
    wrong(2, "p-freight-ar2", 4, "plus", 0.42 * (1 + 0.186))
    try:
        from statsmodels.tsa.arima_process import ArmaProcess
        ac = ArmaProcess([1, -b1, -b2], [1]).acf(3)
        chk("freight: the AR(2) with these b has rho_1 0.42 and rho_2 0.33", close(ac[1], 0.42, 1e-9) and close(ac[2], 0.33, 1e-9))
    except ImportError:
        print("NOTE statsmodels missing: AR(2) acf check skipped")
# ================================================================ problems-3
# ---- p-smoothed-fund: by simulation of the reported series as well as by weights
with block("p-smoothed-fund"):
    v1 = F(36, 100) + F(16, 100)
    key(3, "p-smoothed-fund", 1, math.sqrt(v1) * 0.04)
    wrong(3, "p-smoothed-fund", 1, "add-sds", 0.04)
    wrong(3, "p-smoothed-fund", 1, "no-sqrt", float(v1) * 0.04)
    rho = F(24, 100) / v1
    key(3, "p-smoothed-fund", 2, float(rho))
    wrong(3, "p-smoothed-fund", 2, "ratio", 2 / 3)
    wrong(3, "p-smoothed-fund", 2, "cov", 0.24)
    th = F(2, 3)
    chk("smoothed: theta/(1 + theta^2) at theta 2/3 is 6/13", th / (1 + th * th) == rho == F(6, 13))
    key(3, "p-smoothed-fund", 3, 1.96 * 0.6 * 0.04)
    wrong(3, "p-smoothed-fund", 3, "uncond", 1.96 * math.sqrt(v1) * 0.04)
    wrong(3, "p-smoothed-fund", 3, "full", 1.96 * 0.04)
    v12 = 12 * v1 + 2 * 11 * F(24, 100)
    key(3, "p-smoothed-fund", 4, math.sqrt(v12) * 0.04)
    chk("smoothed 12-month sum by regrouping true returns: 0.36 + 11 + 0.16", v12 == F(36, 100) + 11 + F(16, 100) == F(1152, 100))
    wrong(3, "p-smoothed-fund", 4, "root-12", math.sqrt(12 * v1) * 0.04)
    wrong(3, "p-smoothed-fund", 4, "true", math.sqrt(12) * 0.04)
    wrong(3, "p-smoothed-fund", 4, "once", math.sqrt(12 * v1 + 11 * F(24, 100)) * 0.04)
    R = 4 * rng.standard_normal((300000, 13))
    rep = 0.6 * R[:, 1:] + 0.4 * R[:, :-1]
    chk("smoothed by simulation: sd 2.88, rho_1 0.4615, 12-month sd 13.58, conditional sd 2.4",
        abs(rep[:, 0].std() - 2.8844) < 0.02 and abs(np.corrcoef(rep[:, 0], rep[:, 1])[0, 1] - 6 / 13) < 0.006
        and abs(rep.sum(1).std() - 13.576) < 0.07 and abs((rep[:, 5] - 0.4 * R[:, 5]).std() - 2.4) < 0.02)
    chk("smoothed 28% and 26%", round((1 - math.sqrt(v1)) * 100) == 28 and round((1 - math.sqrt(12 * v1 / v12)) * 100) == 26)
    typed_ok(3, "p-smoothed-fund", 4, 0.136, "13.6%")
# ---- p-inflation-arma: forecasts by running the recursion with future shocks at 0
with block("p-inflation-arma"):
    mu, ph, thm = 0.25, 0.82, -0.35
    eps = 0.55 - 0.43
    key(3, "p-inflation-arma", 1, eps)
    wrong(3, "p-inflation-arma", 1, "gap", 0.55 - 0.25)
    wrong(3, "p-inflation-arma", 1, "sign", -eps)


    def fc(h, e_n=eps, theta=thm):
        xprev, eprev, out = 0.55, e_n, []
        for _ in range(h):
            xnew = mu + ph * (xprev - mu) + theta * eprev
            out.append(xnew)
            xprev, eprev = xnew, 0.0
        return out


    f = fc(12)
    key(3, "p-inflation-arma", 2, f[0])
    wrong(3, "p-inflation-arma", 2, "no-ma", fc(1, theta=0)[0])
    wrong(3, "p-inflation-arma", 2, "theta-sign", fc(1, theta=0.35)[0])
    key(3, "p-inflation-arma", 3, f[1])
    wrong(3, "p-inflation-arma", 3, "ma-again", f[1] + thm * eps)
    wrong(3, "p-inflation-arma", 3, "from-xn", mu + ph ** 2 * 0.30)
    h9 = next(i + 1 for i, v in enumerate(f) if abs(v - mu) < 0.05)
    key(3, "p-inflation-arma", 4, h9)
    wrong(3, "p-inflation-arma", 4, "no-ma", next(i + 1 for i, v in enumerate(fc(30, theta=0)) if abs(v - mu) < 0.05))
    wrong(3, "p-inflation-arma", 4, "off-by-one", h9 - 1)
    chk("inflation gaps 0.0509 and 0.0417, 7.09", round(f[7] - mu, 4) == 0.0509 and round(f[8] - mu, 4) == 0.0417 and round(math.log(0.05 / 0.204) / math.log(0.82), 2) == 7.09)
# ---- p-inventory-half-life: brute search and direct sums
with block("p-inventory-half-life"):
    hl = math.log(0.5) / math.log(0.915)
    key(3, "p-inventory-half-life", 1, hl)
    chk("inventory half-life by bisection on 0.915^h", abs(0.915 ** 7.803 - 0.5) < 1e-4)
    wrong(3, "p-inventory-half-life", 1, "linear", 0.5 / 0.085)
    wrong(3, "p-inventory-half-life", 1, "approx", math.log(2) / 0.085)
    wrong(3, "p-inventory-half-life", 1, "flip", 1 / hl)
    q15 = 30.0
    for _ in range(15):
        q15 *= 0.915
    key(3, "p-inventory-half-life", 2, q15)
    typed_ok(3, "p-inventory-half-life", 2, round(30 * 0.5 ** (15 / 7.80), 2), "the value by half-lives of 7.80")
    wrong(3, "p-inventory-half-life", 2, "half", 15)
    wrong(3, "p-inventory-half-life", 2, "linear", 30 - 15 * 0.085 * 30)
    hw = 1.96 * math.sqrt(sum(2.4 ** 2 * 0.915 ** (2 * j) for j in range(15)))
    key(3, "p-inventory-half-life", 3, hw)
    wrong(3, "p-inventory-half-life", 3, "walk", 1.96 * 2.4 * math.sqrt(15))
    wrong(3, "p-inventory-half-life", 3, "one-step", 1.96 * 2.4)
    wrong(3, "p-inventory-half-life", 3, "limit", 1.96 * math.sqrt(sum(2.4 ** 2 * 0.915 ** (2 * j) for j in range(3000))))
    qs = np.full(400000, 30.0)
    for _ in range(15):
        qs = 0.915 * qs + 2.4 * rng.standard_normal(400000)
    chk("inventory by simulation: mean 7.91 and half-width 11.25", abs(qs.mean() - q15) < 0.04 and abs(1.96 * qs.std() - hw) < 0.05)
    m5 = next(k for k in range(1, 500) if 30 * 0.915 ** k < 5)
    key(3, "p-inventory-half-life", 4, m5)
    wrong(3, "p-inventory-half-life", 4, "round-down", m5 - 1)
    wrong(3, "p-inventory-half-life", 4, "linear", next(k for k in range(1, 500) if 30 - 2.55 * k < 5))
    chk("inventory 5.08, 4.64, 2.585, 20.16", [round(v, 2) for v in (30 * 0.915 ** 20, 30 * 0.915 ** 21)] == [5.08, 4.64] and round(math.log2(6), 3) == 2.585 and round(2.585 * 7.80, 2) == 20.16)
    chk("inventory part 4 restates the half-life it uses", "7.80" in part(3, "p-inventory-half-life", 4)["question"], "question says 'the half-life from part 1' with no value")
    # FINDING candidates: numbers shared with the course and with the set
    l7 = open(os.path.join(COURSE, "l7-today-depends-on-yesterday.json"), encoding="utf-8").read()
    chk("inventory: phi 0.915 is not the fitted phi of l7 screens[11]", "0.915" not in l7, "l7 screens[11]: phi-hat 0.915, gap after 5 days 2 x 0.915^5")
    a = part(3, "p-smoothed-fund", 3)["widget"]["answer"] * 100
    b = next(x["value"] for x in part(3, "p-inventory-half-life", 3)["widget"]["wrong"] if x["id"] == "one-step")
    chk("set 3: two problems do not share the half-width 1.96 x 2.4 = 4.704", not close(a, b, 1e-6), "p-smoothed-fund part 3 key and p-inventory-half-life part 3 one-step")
# ---- p-dual-listing
with block("p-dual-listing"):
    bic3 = lambda k, l: k * math.log(750) - 2 * l
    gap3 = bic3(3, -1460.2) - bic3(4, -1449.7)
    key(3, "p-dual-listing", 1, gap3)
    wrong(3, "p-dual-listing", 1, "aic", (6 + 2920.4) - (8 + 2899.4))
    wrong(3, "p-dual-listing", 1, "sign", -gap3)
    # impulse path by running the model on a single unit shock
    xs, e_prev, x_prev = [], 1.0, 1.0
    for _ in range(12):
        x_new = 0.88 * x_prev + 0.25 * e_prev
        xs.append(x_new)
        x_prev, e_prev = x_new, 0.0
    key(3, "p-dual-listing", 2, xs[0])
    wrong(3, "p-dual-listing", 2, "ar", 0.88)
    wrong(3, "p-dual-listing", 2, "ma", 0.25)
    wrong(3, "p-dual-listing", 2, "product", 0.88 * 0.25)
    key(3, "p-dual-listing", 3, xs[4])
    wrong(3, "p-dual-listing", 3, "ar", 0.88 ** 5)
    wrong(3, "p-dual-listing", 3, "off-by-one", xs[5])
    try:
        from statsmodels.tsa.arima_process import arma2ma
        psi = arma2ma([1, -0.88], [1, 0.25], lags=7)
        chk("dual: statsmodels psi weights give 1.13 and 0.6777", close(psi[1], 1.13, 1e-9) and close(psi[5], xs[4], 1e-9))
    except ImportError:
        print("NOTE statsmodels missing: psi-weight check skipped")
    lo, hi = 1.0, 30.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if 1.13 * 0.88 ** (mid - 1) > 0.5 else (lo, mid)
    key(3, "p-dual-listing", 4, lo)
    wrong(3, "p-dual-listing", 4, "ar", math.log(0.5) / math.log(0.88))
    wrong(3, "p-dual-listing", 4, "half-peak", 1 + math.log(0.5) / math.log(0.88))
    chk("dual 'about two days longer'", round(lo - math.log(0.5) / math.log(0.88)) == 2)
    p2 = json.dumps(item(2, "p-peg-fridays"))
    chk("dual: 0.88^5 = 0.5277 is not also the key of p-peg-fridays part 2 (problems-2)", not ("0.88" in p2 and close(part(3, "p-dual-listing", 3)["widget"]["wrong"][0]["value"], part(2, "p-peg-fridays", 2)["widget"]["answer"], 1e-9)),
        "both problems: phi 0.88, five steps, 0.5277")
# ---- exam pairings (exams/stage-2.json part 2, read by hand; each is a review finding)
with block("exam pairings"):
    st = open(os.path.join(COURSE, "..", "..", "exams", "stage-2.json"), encoding="utf-8").read()
    chk("etf: rho_1 0.45 with 0.2025 is not the pair of stage-2 parts[1].items[4]", not ("0.45" in st and "0.2025" in st and close(part(2, "p-etf-flows", 1)["widget"]["answer"], 0.45, 1e-9)),
        "exam: rho_1-hat 0.45, 0.05 - 0.2025")
    chk("inflation: theta is not the 0.35 of stage-2 parts[1].items[5]", not ("Forecasts from an MA(1)" in st and "+ 0.35" in st and "-0.35" in item(3, "p-inflation-arma")["prose"]),
        "exam: MA(1) with 0.35, one-step uses the shock, two-step does not")
    fr = json.dumps(item(2, "p-freight-ar2"))
    chk("freight: parts 3 and 4 are not the Yule-Walker item stage-2 parts[1].items[4]", not ("An AR(2) from two autocorrelations" in st and "b_1 + b_2" in fr and "PACF at lag 2" in fr),
        "same two equations, same ask, same two slip lines; parts 1 and 2 follow stage-2 parts[1].items[2]")

# ---------------------------------------------------------------- numbers of the proposed fixes (review)
with block("proposed fixes"):
    print("--- proposed fixes (review-problems-arma-1-3.md)")
    gF = F(-6624, 10) / 2880
    chk("fix 1: S_xx 2,880 and S_xy -662.4 give gamma -0.23, se 1/30, t -6.90, S_xx/364 near 7.86",
        gF == F(-23, 100) and close(math.sqrt(3.2 / 2880), 1 / 30, 1e-12) and close(float(gF) * 30, -6.9, 1e-12) and abs(2880 / 364 - 7.8605) < 0.06)
    chk("fix 1 slips: flip -4.3478, no-sqrt -207, s-not-s2 -9.2286", close(2880 / -662.4, -4.3478, 1e-4) and close(-0.23 * 900, -207, 1e-9) and close(-0.23 / math.sqrt(math.sqrt(3.2) / 2880), -9.2286, 1e-4))
    pt = stats.norm.sf(5 / math.sqrt(3.2 / (1 - 0.77 ** 2)))
    chk("fix 2: tol 0.0008 takes 0.037 and 0.038, stays clear of 0.09; tol 0.0005 takes 0.003; P(Z > 1.783) = 0.037",
        abs(0.038 - pt) < 0.0008 and abs(0.037 - pt) < 0.0008 and 0.09 - pt > 0.0014 and abs(0.003 - 0.00259) <= 0.0005 and pt - 0.00259 > 0.0013 and round(stats.norm.sf(1.783), 3) == 0.037)
    r = F(79200, 180000)
    Qn = 200 * 202 * (r * r / 199 + F(576, 10000) / 198)
    chk("fix etf: rho_1 0.44, flip 2.2727, Q 51.0564, Box-Pierce 50.24, no-n-k 10148.48, rho_2 0.1936, sigma 26.9399, no-square 22.4499, variance 725.76, 10%",
        r == F(44, 100) and close(float(1 / r), 2.2727, 1e-4) and close(float(Qn), 51.0564, 1e-4) and close(200 * (0.1936 + 0.0576), 50.24, 1e-9)
        and close(40400 * (0.1936 + 0.0576), 10148.48, 1e-6) and close(math.sqrt(900 * (1 - 0.1936)), 26.9399, 1e-4) and close(math.sqrt(900 * 0.56), 22.4499, 1e-4)
        and close(900 * 0.8064, 725.76, 1e-9) and round((1 - math.sqrt(0.8064)) * 100) == 10 and round(0.24 - 0.1936, 2) == 0.05)
    f1 = 0.25 + 0.82 * 0.30 - 0.20 * 0.12
    f2 = 0.25 + 0.82 * (f1 - 0.25)
    chk("fix inflation (theta -0.20): 0.472, theta-sign 0.52, 0.43204, ma-again 0.40804, gaps 0.0553 and 0.0454, 7.51, horizon 9",
        close(f1, 0.472, 1e-12) and close(0.25 + 0.246 + 0.024, 0.52, 1e-12) and close(f2, 0.43204, 1e-12) and close(f2 - 0.024, 0.40804, 1e-12)
        and round(0.222 * 0.82 ** 7, 4) == 0.0553 and round(0.222 * 0.82 ** 8, 4) == 0.0454 and round(math.log(0.05 / 0.222) / math.log(0.82), 2) == 7.51
        and next(h for h in range(1, 99) if 0.222 * 0.82 ** (h - 1) < 0.05) == 9)
    chk("fix dual part 3 at 7 days: 0.524777, AR path 0.408676, off-by-one 0.461803, 0.4644",
        close(1.13 * 0.88 ** 6, 0.524777, 1e-6) and close(0.88 ** 7, 0.408676, 1e-6) and close(1.13 * 0.88 ** 7, 0.461803, 1e-6) and round(0.88 ** 6, 4) == 0.4644)
    chk("fix dual part 4 explain: 5.42 + 1 + 0.96 = 7.38", round(math.log(0.5) / math.log(0.88), 2) == 5.42 and round(math.log(1.13) / -math.log(0.88), 2) == 0.96
        and round(1 + math.log(0.5 / 1.13) / math.log(0.88), 2) == 7.38)

print(f"{checks} checks, {len(fails)} failing (each a FINDING line above)")
sys.exit(0)
