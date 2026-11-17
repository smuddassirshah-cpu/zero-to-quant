#!/usr/bin/env python3
"""Second reader's own check for review-delta-ah-2 (standard library only).

validation/problems-2 p-spread-blocks and trig/problems-3 p-daylight-model.
Imports no author script. Run from the repo root:
    python3 docs/reviews/review-delta-ah-2-scripts/check.py
Exit 0 when every check passes.
"""
import itertools
import json
import math
import random
import re
import sys
from fractions import Fraction as F

checks = 0
fails = []


def ok(cond, what):
    global checks
    checks += 1
    if not cond:
        fails.append(what)
        print("FAIL", what)


def find(o, pid):
    if isinstance(o, dict):
        if o.get("id") == pid:
            return o
        for v in o.values():
            r = find(v, pid)
            if r:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, pid)
            if r:
                return r


def in_band(w, x, key=None):
    key = w["answer"] if key is None else key
    return abs(x - key) <= w["tol"]["abs"] + 1e-12


def slips_clear(w, keys):
    """Every slip band is disjoint from every key band and every other slip band."""
    tol = w["tol"]["abs"]
    vals = []
    for s in w.get("wrong", []):
        v = s["value"]
        if isinstance(v, str):
            vals.extend((float(x), tol) for x in v.split(","))
        else:
            vals.append((float(v), s.get("tol", {"abs": tol})["abs"]))
    for v, t in vals:
        for k in keys:
            ok(abs(v - k) > t + tol, f"slip {v} overlaps key {k}")
    singles = [s for s in w.get("wrong", []) if not isinstance(s["value"], str)]
    for a, b in itertools.combinations(singles, 2):
        ok(abs(a["value"] - b["value"]) > a.get("tol", {"abs": tol})["abs"] + b.get("tol", {"abs": tol})["abs"],
           f"slips {a['value']} and {b['value']} overlap")


# ---------------------------------------------------------------- validation
H = 8
val = find(json.load(open("app/content/courses/validation/problems-2.json")), "p-spread-blocks")
vp = [p["widget"] for p in val["parts"]]


def days(t):
    """Label of row t: the daily changes of days t+1 .. t+H."""
    return set(range(t + 1, t + H + 1))


def corr(k):
    """Exact correlation of labels k rows apart, independent equal-variance changes."""
    return F(len(days(0) & days(k)), H)


# part 1, exact
ok(corr(3) == F(5, 8), "p1 exact 5/8")
ok(vp[0]["answer"] == 0.625, "p1 key")
ok(sorted(days(0) & days(3)) == [4, 5, 6, 7, 8], "p1 shared days t+4..t+8")
ok(F(3, 8) == 1 - corr(3) and vp[0]["wrong"][0]["value"] == 0.375, "p1 slip offset")
ok(F(len(set(range(3, 9))), 8) == F(3, 4) and vp[0]["wrong"][1]["value"] == 0.75, "p1 slip one-more")
slips_clear(vp[0], [0.625])
ok([corr(k) for k in range(9)] == [F(8 - k, 8) for k in range(9)], "rule: corr = (8-k)/8")

# part 1, simulation: 400,000 independent daily changes, sample correlation at lags 0..8
rng = random.Random(20261117)
n = 400_000
d = [rng.gauss(0, 1) for _ in range(n + H + 1)]
pre = [0.0]
for x in d:
    pre.append(pre[-1] + x)
lab = [pre[t + H + 1] - pre[t + 1] for t in range(n)]


def scorr(k):
    a, b = lab[: n - k], lab[k:]
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    return cov / math.sqrt(va * vb)


sim = {k: scorr(k) for k in (3, 4, 5, 7, 8)}
print("sim corr by lag:", {k: round(v, 4) for k, v in sim.items()})
for k, v in sim.items():
    ok(abs(v - float(corr(k))) < 0.01, f"sim corr lag {k}")
ok(abs(sim[3] - 0.375) > 0.2 and abs(sim[3] - 0.75) > 0.1, "sim separates p1 key from slips")

# part 2: rows sharing a label day with row t are exactly rows t-7..t+7 (not t)
near = [k for k in range(-30, 31) if k != 0 and days(0) & days(k)]
ok(near == [k for k in range(-7, 8) if k != 0] and len(near) == 14, "p2 14 near rows")
ok(F(14) * F(4, 5) == F(56, 5) and vp[1]["answer"] == 11.2, "p2 key 11.2 on the stated 4/5")
# exact under a real shuffled 5-fold of 1,800 rows: a test row's 1,799 others hold 1,440 training rows
exact = F(14) * F(1440, 1799)
print("p2 exact under real shuffled 5-fold:", float(exact))
ok(in_band(vp[1], float(exact)) and round(float(exact), 1) == 11.2, "p2 exact value rounds to the key")
ok([s["value"] for s in vp[1]["wrong"]] == [12.8, 5.6, 14], "p2 slips")
ok(16 * 0.8 == 12.8 and abs(7 * 0.8 - 5.6) < 1e-12, "p2 slip arithmetic")
ok(abs(15 * 0.8 - 11.2) > 0.1 and abs(13 * 0.8 - 11.2) > 0.1, "p2 other miscounts (15, 13 rows) fall outside the band")
slips_clear(vp[1], [11.2])
# simulation: 300 shuffles of 1,800 rows into 5 folds of 360; interior rows and end rows apart
N = 1800
tot = cnt = 0
end_tot = end_cnt = 0
for _ in range(300):
    perm = list(range(N))
    rng.shuffle(perm)
    fold = [0] * N
    for i, r in enumerate(perm):
        fold[r] = i % 5
    for t in range(N):
        c = sum(1 for k in near if 0 <= t + k < N and fold[t + k] != fold[t])
        if 7 <= t < N - 7:
            tot += c
            cnt += 1
        else:
            end_tot += c
            end_cnt += 1
print("p2 sim interior mean:", round(tot / cnt, 4), " end rows mean:", round(end_tot / end_cnt, 3))
ok(abs(tot / cnt - float(exact)) < 0.02 and in_band(vp[1], tot / cnt), "p2 sim agrees with exact, in band")
ok(end_tot / end_cnt < 9.5, "p2 end rows have fewer, so 'far from the ends' is needed")

# part 3: gap g puts the last training row g+1 rows before the first test row
g_min = next(g for g in range(0, 20) if corr(g + 1) < F(2, 5))
ok(g_min == 4 == vp[2]["answer"], "p3 key 4")
ok(corr(4) == F(1, 2) and corr(5) == F(3, 8), "p3 0.5 at g=3 and 0.375 at g=4")
ok(next(k for k in range(20) if corr(k) < F(2, 5)) == 5 == vp[2]["wrong"][0]["value"], "p3 slip gap-as-distance 5")
ok(next(g for g in range(20) if corr(g + 1) == 0) == 7 == vp[2]["wrong"][1]["value"], "p3 slip full-purge 7")
ok(next(g for g in range(20) if corr(g + 1) <= F(2, 5)) == 4, "p3 'below' or 'at most' give the same key")
slips_clear(vp[2], [4])
# sklearn's rule, re-derived: train = indices[: test_start - gap], so last train = test_start - gap - 1
for g in range(0, 10):
    test_start = 1000
    last_train = list(range(test_start - g))[-1]
    ok(test_start - last_train == g + 1, "p3 distance g+1")


# part 4: largest set of rows in a block of n with every pair at least `sep` apart
def best(nrows, sep):
    f = [0] * (nrows + 1)  # f[i]: best using the first i rows
    for i in range(1, nrows + 1):
        f[i] = max(f[i - 1], 1 + (f[i - sep] if i - sep >= 0 else 0))
    return f[nrows]


def brute(nrows, sep):
    m = 0
    for mask in range(1 << nrows):
        rows = [i for i in range(nrows) if mask >> i & 1]
        if all(b - a >= sep for a, b in zip(rows, rows[1:])):
            m = max(m, len(rows))
    return m


for nrows in range(1, 17):
    for sep in (2, 3, 8):
        ok(best(nrows, sep) == brute(nrows, sep) == math.ceil(nrows / sep), f"p4 dp vs brute {nrows},{sep}")
ok(best(200, 8) == 25 == vp[3]["answer"], "p4 key 25")
ok(list(range(0, 200, 8))[-1] == 192 and len(range(0, 200, 8)) == 25, "p4 picks s..s+192")
ok(200 // 8 + 1 == 26 == vp[3]["wrong"][0]["value"], "p4 slip fencepost 26")
ok(best(200, 7) == 29 == vp[3]["wrong"][1]["value"] and 1 + 196 // 7 == 29, "p4 slip seven-apart 29")
ok(len(days(0) & days(7)) == 1 and not days(0) & days(8), "p4 7 apart share one day, 8 apart none")
slips_clear(vp[3], [25])
# the explanation's "about 25 independent ones": variance of the mean of 200 overlapping labels
var_mean = sum(float(corr(abs(i - j))) * 8 for i in range(200) for j in range(200) if abs(i - j) < 8) / 200 ** 2
print("p4 effective count 8/var_mean:", round(8 / var_mean, 2))
ok(24 < 8 / var_mean < 27, "p4 explain: effective count about 25")

# ---------------------------------------------------------------------- trig
tr = find(json.load(open("app/content/courses/trig/problems-3.json")), "p-daylight-model")
tp = [p["widget"] for p in tr["parts"]]
hi, lo = F("17.6"), F("6.4")
a, mid = (hi - lo) / 2, (hi + lo) / 2
ok(a == F("5.6") and mid == 12 and hi - lo == F("11.2"), "t1 a, d, range")
ok(tp[0]["answer"] == 5.6 and [s["value"] for s in tp[0]["wrong"]] == [11.2, 17.6, 12], "t1 key and slips")
slips_clear(tp[0], [5.6])
b, c = math.pi / 6, 3


def L(t):
    return 5.6 * math.sin(b * (t - c)) + 12


ok(abs(2 * math.pi / b - 12) < 1e-12, "t2 period 12")
ok(abs(L(6) - 17.6) < 1e-9 and abs(L(12) - 6.4) < 1e-9 and abs(L(0) - 6.4) < 1e-9, "model peak month 6, trough month 12")
ok(abs(L(3) - 12) < 1e-9 and L(3.01) > 12 and abs(L(9) - 12) < 1e-9 and L(9.01) < 12, "t3 up at 3, down at 9")
ok(tp[2]["answer"] == 3 and [s["value"] for s in tp[2]["wrong"]] == [6, 9, 12], "t3 key and slips")
s = (F(10) - 12) / F("5.6")
ok(s == F(-5, 14), "t4 sine -5/14")
u = math.asin(float(s))
ok(f"{u:.4f}" == "-0.3652" and f"{math.pi - u:.4f}" == "3.5068", "t4 printed angles")
t1, t2 = 3 + u / b, 3 + (math.pi - u) / b
print("t4 roots:", round(t1, 5), round(t2, 5), " t5:", round(t2 - t1, 5))
ok(f"{t1 - 3:.2f}" == "-0.70" and f"{t2 - 3:.2f}" == "6.70", "t4 printed t-3")
ok(f"{t1:.2f}" == "2.30" and f"{t2:.2f}" == "9.70", "t4 printed roots")
ok(tp[3]["answers"] == [2.3, 9.7] and abs(t1 - 2.3) < 0.01 and abs(t2 - 9.7) < 0.01, "t4 keys in band")
# roots by a scan of the model, independent of asin
roots = []
x, step = 0.0, 1e-4
while x < 12:
    if (L(x) - 10) * (L(x + step) - 10) < 0:
        roots.append(x)
    x += step
ok(len(roots) == 2 and abs(roots[0] - t1) < 1e-3 and abs(roots[1] - t2) < 1e-3, "t4 exactly two roots in 0..12")
ns = sorted(6 / math.pi * v % 12 for v in (u, math.pi - u))
ok([f"{v:.1f}" for v in ns] == ["6.7", "11.3"] and tp[3]["wrong"][0]["value"] == "6.7, 11.3", "t4 slip no-shift")
ab = sorted(3 + 6 / math.pi * v for v in (-u, math.pi + u))
ok([f"{v:.1f}" for v in ab] == ["3.7", "8.3"] and tp[3]["wrong"][1]["value"] == "3.7, 8.3", "t4 slip above")
ok(abs(L(ab[0]) - 14) < 1e-9 and abs(L(ab[1]) - 14) < 1e-9, "t4 slip 'above' is 14 hours")
for v in ns + ab:
    ok(min(abs(v - 2.3), abs(v - 9.7)) > 0.02, "t4 slip values clear of both key bands")
above = sum(1 for i in range(120000) if L(i / 10000) > 10) / 10000
ok(abs(above - (t2 - t1)) < 1e-3 and in_band(tp[4], t2 - t1) and in_band(tp[4], 9.70 - 2.30), "t5 7.4 by scan and by printed roots")
ok(tp[4]["answer"] == 7.4 and f"{t2 - t1:.1f}" == "7.4" and f"{12 - 7.4:.1f}" == "4.6", "t5 key, complement 4.6")
ok([s["value"] for s in tp[4]["wrong"]] == [4.6, 8] and 10 - 2 == 8, "t5 slips")
slips_clear(tp[4], [7.4])
ok(L(6) > 10 and L(0) < 10 and L(11) < 10, "t5 above between the crossings")
# homework h3-demand-model: 820/380, peak t=2, threshold 710 gives sine +1/2 (exact angles)
ok(F(710 - 600, 220) == F(1, 2) and s != F(1, 2) and s != F(-1, 2), "no longer the homework's sine of 1/2")
ok(F(hi - lo, 2) / mid != F(220, 600), "amplitude to midline ratio differs from the homework")

ok(F(820) / hi != F(380) / lo and F(820) / F("16.4") == F(380) / F("7.6") == 50,
   "new peak and trough are not the homework's on another scale (the old pair was, by 50)")

# ----------------------------------------------------- every printed number
for prob, allowed in (
    (val, {"1,800", "8", "3", "0.625", "5", "11", "4", "6", "1", "14", "0.8", "11.2", "7", "9", "0.4", "0.5", "0.375",
           "200", "192", "25", "199", "2", "16", "196", "12.8", "5.6", "29", "26",
           "0", "0.05", "0.75"}),
    (tr, {"6", "12", "17.6", "6.4", "5.6", "11.2", "2", "3", "9", "10", "14", "5", "0.3652", "3.5068", "0.70", "6.70",
          "2.30", "9.70", "7.4", "4.6", "0", "1", "2.3", "9.7", "6.7", "11.3", "3.7", "8.3", "8", "0.001", "0.01", "0.05", "4"}),
):
    blob = json.dumps(prob, ensure_ascii=False)
    nums = set(re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?", blob))
    extra = {x.rstrip(",") for x in nums} - allowed - {"0.0005"}
    ok(not extra, f"{prob['id']}: unexplained numbers {sorted(extra)}")

# sentences over 35 words in the learner-facing strings of the two problems
for prob in (val, tr):
    strs = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k not in ("id", "kind", "slip", "skills", "placeholder", "keyboard"):
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            strs.append(o)
    walk(prob)
    for st in strs:
        for sent in re.split(r"(?<=[.?])\s+", st):
            ok(len(sent.split()) <= 35, f"long sentence: {sent[:60]}")
        ok("!" not in st and "—" not in st, f"voice mark in: {st[:50]}")
    for p in prob["parts"]:
        ok(len(re.split(r"(?<=[.?])\s+(?=[A-Z`$])", p["explain"]["text"].strip())) <= 3, f"explain over three sentences: {p['explain']['text'][:40]}")

print(f"{checks} checks, {len(fails)} failed")
sys.exit(1 if fails else 0)
